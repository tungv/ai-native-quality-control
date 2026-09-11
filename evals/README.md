# Assistant evaluations

From the repository root, run:

```sh
docker compose run --rm --build lab make eval
```

Only Docker and Compose v2 are required on the host. The image supplies Go, Python, and Make. For repeated work, open `docker compose run --rm --build lab sh` and use the `make` targets below inside that shell; edit cases on the host and find reports in your local `reports/` folder. No separate interactive API container is needed for evaluation.

`make eval` builds the Go service, starts it on a temporary loopback port, evaluates `cases.json`, writes `reports/eval-baseline.json`, and stops the process. No API key, model download, or paid call is required. A failed case exits nonzero. `make fault-check` requires the specific failed case and actual wrong-price or canary/action response evidence in the two deliberate scenarios. Transport errors, server errors, and unrelated failures cannot count as detected faults.

The small, public dataset teaches structured oracles: HTTP success, response schema, product facts, citation IDs, forbidden canaries, and permitted action lists. These are deterministic contract checks, not an LLM benchmark. The baseline ignores retrieved context entirely. The canned response logic cannot establish real-world injection resistance, answer quality, or retrieval quality. Exact fragments are deliberately simple and can accept subtly wrong answers: improving that oracle is part of the review lab.

Every case has a unique `id`, `category`, `request`, and `expect`. The four required assertion types are `contains` (case-insensitive answer fragments), `citations` (exact ordered IDs), `actions` (exact list), and `forbidden` (case-insensitive fragments across the serialized response). Unknown assertion names fail validation. The report records individual failures, responses, elapsed request time, fixture provider, scenario, timestamp, and commit if available. Reports may reflect an uncommitted working tree; record the patch in your submission too.

All fixtures are original synthetic data released under MIT. `LAB_CANARY_ONLY` is a public test marker, never a secret. Only synthetic requests are sent to the local service. Do not add real customer data to this public dataset or CI artifacts.

Adding cases should strengthen the suite without breaking its controls. In the injection fault run, every case whose `context` contains `[[OVERRIDE]]` must fail and produce the scripted canary/action evidence; all other cases must pass. This follows the fixture's explicit activation contract. A timeout cannot satisfy it, and removing every trigger case makes fault detection fail. Additional attacks without that marker still exercise the baseline's limitations; they do not activate a real model.

For a live-model extension, add an explicit provider adapter and opt-in execution, separate development and held-out cases, repeat trials, record model/prompt/dataset versions and token cost, enforce a budget, and calibrate subjective grading against human labels. Keep deterministic CI available offline. See the [curriculum](../docs/curriculum.md).
