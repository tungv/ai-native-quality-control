"""Run the real local service, check contracts, and retain reviewable evidence."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("baseline", "price-rounding", "context-injection")


def request(base, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = Request(base + path, data=data, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=3) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


@contextmanager
def build_service():
    with tempfile.TemporaryDirectory(prefix="ai-qc-") as folder:
        executable = Path(folder) / "catalog-api"
        subprocess.run([os.environ.get("GO", "go"), "build", "-o", str(executable), "."],
                       cwd=ROOT / "services/catalog-api", check=True)
        yield executable


@contextmanager
def running_service(executable, scenario):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    env = dict(os.environ, LISTEN_ADDR=f"127.0.0.1:{port}", LAB_SCENARIO=scenario)
    with tempfile.TemporaryFile(mode="w+") as log:
        process = subprocess.Popen([str(executable)], env=env, stdout=log, stderr=log)
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    log.seek(0)
                    raise RuntimeError("Service exited before health check: " + log.read())
                try:
                    status, body = request(base, "/health")
                    if status == 200 and body == {"status": "ok", "scenario": scenario}:
                        break
                except (URLError, OSError):
                    pass
                time.sleep(0.05)
            else:
                raise RuntimeError("Service did not become healthy within 10 seconds")
            yield base
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def load_cases(path):
    cases = json.loads(Path(path).read_text())
    if not isinstance(cases, list) or not cases:
        raise ValueError("Dataset must be a nonempty list")
    ids = set()
    for case in cases:
        if set(case) != {"id", "category", "request", "expect"}:
            raise ValueError("Every case needs exactly id/category/request/expect")
        if not isinstance(case["id"], str) or not case["id"] or case["id"] in ids:
            raise ValueError("Case IDs must be unique nonempty strings")
        ids.add(case["id"])
        if not isinstance(case["category"], str) or not case["category"]:
            raise ValueError("Category must be a nonempty string")
        payload = case["request"]
        if not isinstance(payload, dict) or "message" not in payload or set(payload) - {"message", "context"}:
            raise ValueError("Request requires message and optional context")
        if any(not isinstance(v, str) for v in payload.values()):
            raise ValueError("Request values must be strings")
        expected = case["expect"]
        if not isinstance(expected, dict) or set(expected) != {"contains", "citations", "actions", "forbidden"}:
            raise ValueError("Unknown or missing assertion type")
        if any(not isinstance(v, list) or any(not isinstance(s, str) or not s for s in v)
               for v in expected.values()):
            raise ValueError("Assertions must be lists of nonempty strings")
    return cases


def check_response(status, body, expected):
    failures = []
    if status != 200:
        return [f"Expected HTTP 200; got {status}"]
    if not isinstance(body, dict) or set(body) != {"answer", "citations", "actions"}:
        return ["Response must contain exactly answer/citations/actions"]
    if not isinstance(body["answer"], str) or not body["answer"].strip():
        return ["Answer must be a nonempty string"]
    for key in ("citations", "actions"):
        if not isinstance(body[key], list) or any(not isinstance(v, str) for v in body[key]):
            failures.append(f"{key} must be a list of strings")
        elif body[key] != expected[key]:
            failures.append(f"{key}: expected {expected[key]!r}; got {body[key]!r}")
    for phrase in expected["contains"]:
        if phrase.casefold() not in body["answer"].casefold():
            failures.append(f"Missing expected answer fragment: {phrase!r}")
    serialized = json.dumps(body).casefold()
    for phrase in expected["forbidden"]:
        if phrase.casefold() in serialized:
            failures.append(f"Forbidden output: {phrase!r}")
    return failures


def evaluate(base, cases):
    rows = []
    for case in cases:
        start = time.monotonic()
        try:
            status, body = request(base, "/chat", case["request"])
            failures = check_response(status, body, case["expect"])
        except (URLError, OSError, ValueError) as error:
            status, body, failures = None, None, [f"Transport or JSON error: {error}"]
        rows.append({"id": case["id"], "category": case["category"], "passed": not failures,
                     "failures": failures, "http_status": status, "response": body,
                     "latency_ms": round((time.monotonic() - start) * 1000, 2)})
    return rows


def smoke(base):
    rows = []

    def check(case_id, path, predicate):
        status, body = None, None
        try:
            status, body = request(base, path)
            passed = predicate(status, body)
            failures = [] if passed else [f"Unexpected response ({status}): {body!r}"]
        except (URLError, OSError, ValueError, KeyError, TypeError) as error:
            passed, failures = False, [str(error)]
        rows.append({"id": case_id, "passed": passed, "failures": failures,
                     "http_status": status, "response": body})

    check("catalog-size", "/products", lambda s, b: s == 200 and len(b["products"]) == 3)
    check("product-price", "/products/trail-shoes", lambda s, b: s == 200 and b["price_cents"] == 12900 and b["currency"] == "USD")
    check("stock-state", "/products/city-backpack", lambda s, b: s == 200 and b["in_stock"] is False)
    check("search", "/products?q=JACKET", lambda s, b: s == 200 and [p["sku"] for p in b["products"]] == ["rain-jacket"])
    check("limit", "/products?limit=1", lambda s, b: s == 200 and len(b["products"]) == 1)
    check("invalid-limit", "/products?limit=0", lambda s, b: s == 400 and "error" in b)
    check("missing-product", "/products/unknown", lambda s, b: s == 404 and "error" in b)
    return rows


def fault_detected(scenario, rows, expected_ids=None):
    """Only the intended response violation is a successful negative control."""
    if expected_ids is None:
        expected_ids = {{"price-rounding": "product-price", "context-injection": "indirect-injection"}[scenario]}
    failed = [row for row in rows if not row["passed"]]
    if not expected_ids or {row["id"] for row in failed} != expected_ids or len(failed) != len(expected_ids):
        return False
    for row in failed:
        body = row.get("response")
        if row.get("http_status") != 200 or not isinstance(body, dict):
            return False
        if scenario == "price-rounding":
            observed = (body.get("sku") == "trail-shoes" and type(body.get("price_cents")) is int
                        and body["price_cents"] == 129 and body.get("currency") == "USD")
        else:
            observed = (set(body) == {"answer", "citations", "actions"}
                        and isinstance(body["answer"], str) and "LAB_CANARY_ONLY" in body["answer"]
                        and body["actions"] == ["issue_refund"] and body["citations"] == [])
        if not observed:
            return False
    return True


def write_report(kind, scenario, rows):
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    report = {"suite": kind, "scenario": scenario, "provider": "deterministic-fixture",
              "created_at": datetime.now(timezone.utc).isoformat(),
              "commit": commit.stdout.strip() if commit.returncode == 0 else "uncommitted",
              "total": len(rows), "passed": sum(row["passed"] for row in rows), "results": rows}
    output = ROOT / "reports" / f"{kind}-{scenario}.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{kind} [{scenario}]: {report['passed']}/{report['total']} passed → {output.relative_to(ROOT)}")
    for row in rows:
        if not row["passed"]:
            print(f"  FAIL {row['id']}: {'; '.join(row['failures'])}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("smoke", "eval", "faults"))
    parser.add_argument("--scenario", choices=SCENARIOS, default="baseline")
    args = parser.parse_args()
    cases = load_cases(ROOT / "evals/cases.json")
    with build_service() as executable:
        if args.command == "faults":
            detected = True
            for scenario, kind, expected_id in (("price-rounding", "smoke", "product-price"),
                                                 ("context-injection", "eval", "indirect-injection")):
                with running_service(executable, scenario) as base:
                    rows = smoke(base) if kind == "smoke" else evaluate(base, cases)
                write_report(kind, scenario, rows)
                failures = {row["id"] for row in rows if not row["passed"]}
                expected_ids = ({case["id"] for case in cases if "[[OVERRIDE]]" in case["request"].get("context", "")}
                                if scenario == "context-injection" else {expected_id})
                if not fault_detected(scenario, rows, expected_ids):
                    print(f"Fault check failed: expected response evidence for {sorted(expected_ids)!r}; failed IDs: {sorted(failures)!r}")
                    detected = False
            print("Both deliberate faults detected." if detected else "Fault detection did not match expectations.")
            return 0 if detected else 1
        with running_service(executable, args.scenario) as base:
            rows = smoke(base) if args.command == "smoke" else evaluate(base, cases)
        write_report(args.command, args.scenario, rows)
        return 0 if all(row["passed"] for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
