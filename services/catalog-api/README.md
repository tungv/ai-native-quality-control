# Catalog API starter

A Go standard-library service for the first QC lab. It has three synthetic products and a deterministic chat fake. It needs no database, provider account, or API key.

From the repository root, with Docker and Compose v2 installed:

```sh
docker compose up --build -d --wait api
docker compose run --rm --build lab make test
```

The API is available at `http://127.0.0.1:8080` on the host. It listens on `0.0.0.0:8080` inside the container, and Compose publishes only to host loopback. Use `API_PORT=8081 docker compose up --build -d --wait api` to choose another host port. `LAB_SCENARIO` defaults to `baseline`; unknown scenario names fail at startup. The service shuts down on SIGINT/SIGTERM and sets read, write, and idle timeouts.

Check readiness at `GET /health`, follow logs with `docker compose logs -f api`, and stop services with `docker compose down`. The three-product fixture is seeded at process startup; restarting the API restores it. Rebuild with `docker compose up --build -d --wait api` after source edits. The verification container sees edits directly through the mounted checkout and writes reports to the host `reports/` directory. `make test` prints unit/static-check results; `docker compose run --rm --build lab make smoke` produces `reports/smoke-baseline.json` from its own temporary API process.

For optional native development, install the toolchain listed in the root [README](../../README.md), then run `go run .`, `go test -race ./...`, or `go vet ./...` from this directory. Native execution defaults to `127.0.0.1:8080`; `LISTEN_ADDR` overrides it.

## HTTP contract

All responses are JSON. Application errors have the shape `{"error":"message"}`. Unsupported endpoint methods return 405 and an `Allow` header. Unrecognized routes and missing products return 404.

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | `{"status":"ok","scenario":"baseline"}` with the active scenario name. |
| `GET /products` | `{"products":[...]}` in the fixed catalog order. Optional `q` performs a case-insensitive name substring match, trimming surrounding whitespace. No matches returns an empty array. Optional `limit` defaults to 10 and accepts one integer from 1 to 20; invalid or repeated values return 400. |
| `GET /products/{sku}` | A single product object. |
| `POST /chat` | Accepts `{"message":"Tell me about trail shoes","context":"optional untrusted text"}`. Returns `answer`, `citations` (SKU strings), and `actions` (string labels). Both arrays are always present. |

Chat requires `Content-Type: application/json` (parameters such as `charset=utf-8` are accepted); other media types return 415. It rejects unknown fields, multiple JSON values, malformed JSON, and invalid field types with 400. The trimmed message must have 1–2000 Unicode characters. The entire request body, including trailing whitespace, is limited to 16,384 bytes; exceeding that limit returns 413.

| SKU | Name | `price_cents` | `currency` | `in_stock` |
| --- | --- | ---: | --- | --- |
| `trail-shoes` | Trail Shoes | 12900 | USD | true |
| `rain-jacket` | Rain Jacket | 8900 | USD | true |
| `city-backpack` | City Backpack | 5900 | USD | false |

Open the GET endpoints in a browser, or use these requests if curl is available on your host:

```sh
curl http://127.0.0.1:8080/products/trail-shoes
curl 'http://127.0.0.1:8080/products?q=shoes&limit=1'
curl -H 'Content-Type: application/json' \
  --data '{"message":"Tell me about trail shoes"}' \
  http://127.0.0.1:8080/chat
```

Baseline chat mentions `$129.00` for shoes/trail, `$89.00` for jacket, and `$59.00` plus out-of-stock status for backpack, with the matching SKU citation. Messages containing `refund` or `return` take precedence: chat says it cannot issue refunds and directs the learner to support, with empty citations and actions. Other messages ask which product the user means. Matching is deliberately simple substring matching.

## Reproducible fault scenarios

Run one scenario per API service from a host terminal in the repository root:

```sh
LAB_SCENARIO=price-rounding docker compose up --build -d --wait api
# Switch to the injection scenario:
LAB_SCENARIO=context-injection docker compose up --build -d --wait api
# Restore the baseline:
LAB_SCENARIO=baseline docker compose up --build -d --wait api
```

To test a fault in a temporary isolated process, use `docker compose run --rm --build lab make smoke SCENARIO=price-rounding` or `docker compose run --rm --build lab make eval SCENARIO=context-injection`. These should fail with the documented defect evidence; they do not change the interactive API's scenario.

| Scenario | Deliberate change | Useful learner assertion |
| --- | --- | --- |
| `baseline` | Correct starter contract. Ignores `context`. | Product prices, response schema, negative HTTP cases, safe chat behavior. |
| `price-rounding` | Both product-list and product-detail responses report Trail Shoes as 129 cents. Chat still reports `$129.00`. | Correct currency units and consistency across endpoints. |
| `context-injection` | A `context` containing the exact marker `[[OVERRIDE]]` overrides normal chat behavior, reveals `LAB_CANARY_ONLY`, and returns `actions:["issue_refund"]`. | Untrusted content must not alter action authority or expose protected context. |

The checked-in Go tests verify the healthy contract and the explicit selection of faults. They pass when scenario implementation is correct. Learner acceptance tests should hold baseline requirements constant and fail when run against a selected fault; do not “fix” those tests to accept broken behavior.

## Teaching limitations

This is a deterministic fake, not an LLM or RAG system. The baseline ignores all supplied context; that illustrates a trust boundary but does not prove resistance to real prompt injection. The marker scenario is scripted and does not measure attacks against a model. Citations are fixed labels, not retrieval evidence. The canary is synthetic, and `issue_refund` is only a returned string: there are no tools, refunds, payments, user accounts, or secret files behind the interface.

The catalog is in memory and does not use SQL or vectors. Searching an SQL-looking string therefore cannot establish SQL-injection resistance for a database-backed service. The shared starter has no authentication, rate limiter, or production deployment configuration. Keep the fault scenarios on localhost in the learning environment; later labs should introduce real adapters with their own contracts and evidence.
