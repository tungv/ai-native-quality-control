# AI Native Quality Control

A learning playground for QC engineers developing AI-native test engineering skills. Practice using an agent to plan, build, review, and maintain tests—and testing software that contains AI.

The learning loop is **identify a risk → define an independent oracle → work with an agent → run the test → prove it catches a defect → review the evidence → make a release decision**. You remain responsible for the result.

**Status:** repository design plus a runnable starter lab. The source, original documentation, prompts, and synthetic fixtures are available under [MIT](LICENSE). No paid model account is needed for the starter.

## What you can run today

| Component | Included behavior | What it teaches |
| --- | --- | --- |
| Go catalog API | Products, search, stock, input validation, HTTP errors | Contract tests, boundaries, agent-generated tests |
| Shopping-assistant fixture | Canned product answers, citations, simulated actions | Evaluation datasets, grounding checks, test-oracle limitations |
| Deliberate faults | Price-unit error and retrieved-context injection simulation | Regression detection, security assertions, meaningful failures |
| Python evaluation harness | Real HTTP checks, case validation, JSON reports | Evidence, evaluator review, reproducible runs |
| PostgreSQL + pgvector | Optional isolated SQL lab with ranking and constraints | Retrieval mechanics, eligibility filters, data isolation risks |
| GitHub Actions | Baseline tests, fault detection, database checks, binary/evidence artifacts | CI gates and failure diagnosis |

The assistant is **a deterministic test fixture**, not a language model. It ignores context in baseline mode; its injected fault is a teaching simulation. The database lab is standalone, and the API stores its catalog in memory. A Next.js storefront, connected RAG/live-model adapter, browser suite, and deployment/rollback pipeline are designed extension assignments, not implemented services. See the [roadmap](docs/roadmap.md).

## Start with Docker

Install Docker with Compose v2 or newer (`docker compose`). It is the only required host runtime: Go, Python, Make, and the compiler are provided by the lab image. Clone this repository with Git, or download and extract its ZIP, then open a terminal in the repository root.

```sh
docker compose run --rm --build lab make verify
docker compose up --build -d --wait api
```

The first command builds the toolchain image and runs Go tests with the race detector, `go vet`, Python evaluator tests, baseline HTTP/evaluation checks, and deliberate-fault detection. It starts and stops its own temporary services. Image download and build require internet access; the checks run in a container with external networking disabled and need no model account. The first build can take several minutes.

The second command starts the API. Open `http://127.0.0.1:8080/products/trail-shoes` in a browser. If you already have curl, you can also try:

```sh
curl http://127.0.0.1:8080/products/trail-shoes
curl http://127.0.0.1:8080/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"Tell me about trail shoes"}'
```

The product costs `12900` USD cents. The chat answer includes `$129.00`, cites `trail-shoes`, and returns an empty `actions` list. View API output with `docker compose logs -f api`; leave the log view with Ctrl-C. Stop the services with `docker compose down`. Restarting the API restores its fixed dataset. If port 8080 is occupied, start it with `API_PORT=8081 docker compose up --build -d --wait api` and visit port 8081.

Now observe intentional failures:

```sh
docker compose run --rm --build lab make smoke SCENARIO=price-rounding
docker compose run --rm --build lab make eval SCENARIO=context-injection
```

Both commands should exit nonzero. The first detects the incorrect price; the second detects the synthetic canary and unauthorized simulated action. `docker compose run --rm --build lab make fault-check` verifies that these exact failures occur and exits successfully when both defects are detected. Expected `FAIL` lines during that command are part of its evidence.

Start your learning record with [lab 00](exercises/00-baseline/README.md) and the [evidence template](templates/evidence.md).

### Edit and repeat

Edit files with your usual editor or coding agent on the host. The lab container mounts the repository at `/workspace`, so tests see your edits immediately and reports appear in your local `reports/` folder. Use `--build` to refresh the image after Dockerfile or toolchain changes. The API image copies its source at build time; rerun `docker compose up --build -d --wait api` after changing API code.

For several exercise commands in one session:

```sh
docker compose run --rm --build lab sh
make test
make eval
make verify
exit
```

Run exercise `make` commands inside this shell, or prefix them with `docker compose run --rm --build lab`. Start the interactive API and database with `docker compose` from a host terminal. The lab shell has no Docker socket or external network, so it cannot start sibling containers or expose `make run` to your browser.

On Linux, if your user ID or group ID is not 1000 and you get a permission error writing reports or build files, set these in the host terminal before running Compose:

```sh
export LOCAL_UID=$(id -u)
export LOCAL_GID=$(id -g)
```

### Optional native setup

If you prefer local tools, install the Go version from [.go-version](.go-version), Python 3.11 or newer, Make, and a C compiler for Go's race detector. Then run `make verify` or `make run` from the repository root. Native `make run` listens at `127.0.0.1:8080`; use `LISTEN_ADDR=127.0.0.1:8081 make run` for another port and Ctrl-C to stop it. The Go and Python starter uses standard libraries only. Docker is still required for the database lab.

## Choose your learning path

| Skill | Exercises |
| --- | --- |
| Prompt engineering | [01: compare prompts against an independent risk-based plan](exercises/01-prompt-engineering/README.md) |
| Agentic test development | [02: implement and review API tests](exercises/02-agentic-api-tests/README.md) |
| AI evaluation | [03: improve cases and oracles](exercises/03-assistant-evaluation/README.md), [04: retrieval and data](exercises/04-retrieval-and-data/README.md) |
| Suite review and maintenance | [05: diagnose weak assertions, obsolete tests, and flakes](exercises/05-suite-maintenance/README.md) |
| End-to-end CI/CD | [06: gates, artifacts, deployment, rollback, and cleanup](exercises/06-ci-cd/README.md) |
| Security and red teaming | [07: injection, authorization, and paired benign controls](exercises/07-security-and-injection/README.md) |
| Browser testing | [08: build/connect a Next.js journey](exercises/08-browser-journeys/README.md) |
| Engineering judgment | [09: capstone and release recommendation](exercises/09-capstone/README.md) |

Follow the [curriculum](docs/curriculum.md) for prerequisites and routes. Every exercise asks for observable evidence and reflection on agent assistance. The [assessment rubric](docs/assessment.md) rewards risk coverage, valid oracles, fault detection, and maintainability. The [learning design](docs/learning-design.md) explains how to run this individually or with peer review.

## Commands and evidence

Run these from a host terminal in the repository root:

| Command | Purpose |
| --- | --- |
| `docker compose run --rm --build lab make help` | List entry points |
| `docker compose run --rm --build lab make test` | Go unit/race tests, static checks, Python evaluator tests |
| `docker compose run --rm --build lab make smoke` | Test the real catalog HTTP API in a temporary process |
| `docker compose run --rm --build lab make eval` | Evaluate the assistant using `evals/cases.json` |
| `docker compose run --rm --build lab make fault-check` | Confirm the checks detect both deliberate faults |
| `docker compose run --rm --build lab make verify` | Run the complete starter verification sequence |
| `docker compose up --build -d --wait api` | Start an interactive local API session |
| `docker compose logs -f api` | Follow API logs |
| `docker compose down` | Stop and remove lab services, including disposable database data |

`SCENARIO` accepts `baseline`, `price-rounding`, or `context-injection` for `make smoke` and `make eval`. `make verify` always validates the baseline and then the named fault controls. To select an interactive API fault, run `LAB_SCENARIO=context-injection docker compose up --build -d --wait api`; return to baseline with `LAB_SCENARIO=baseline docker compose up --build -d --wait api`. Chat prices stay fixed in the price fault; that fault targets the catalog contract.

The [database lab](db/README.md) also uses Docker directly from the host and requires no local Make or PostgreSQL installation.

Reports are written to `reports/<suite>-<scenario>.json` and ignored by Git. Preserve useful evidence in your learner branch, pull request, or attached artifact. Go unit output goes to the terminal; GitHub Actions retains its logs and uploads HTTP/evaluation reports and the built Linux binary for seven days. A later run overwrites the same local report filename.

Read the [API contract](services/catalog-api/README.md), [evaluation format](evals/README.md), and [database setup](db/README.md) before extending them.

## Repository map

```text
Dockerfile             Lab toolchain and minimal API runtime images
compose.yaml           Offline test runner, local API, optional database
services/catalog-api/   Runnable Go SUT, reference tests, HTTP contract
evals/                 Synthetic assistant cases, evaluator, oracle tests
db/                    Optional pgvector schema, fixtures, SQL assertions
exercises/             Ten lab briefs and learner planning templates
prompts/               Agent prompts for planning, implementation, review, triage
templates/             Evidence and defect reports
docs/                  Architecture, curriculum, assessment, threats, roadmap
.github/               CI, dependency updates, issue and PR templates
```

Fork the repository or create a learner branch. Keep the passing reference baseline as a comparison point. The supplied faults are openly documented; learners should attempt exercises before reading their implementation. A public repository cannot provide secret benchmark cases. In a cohort, a reviewer can prepare an additional unseen case to assess transfer of learning.

The [architecture](docs/architecture.md) defines how additional SUTs join the playground: each declares start, health, seed, reset, test, and reporting behavior. You can add a different API language, database, frontend, or model adapter without making every runtime mandatory for the introductory route.

## Public project

Contributions are welcome under the [contribution guide](CONTRIBUTING.md). Use only synthetic or appropriately licensed data. Run attack exercises against your isolated lab and follow the [security policy](SECURITY.md). See the [security-testing guide](docs/security-testing.md) for the boundary between a test fixture and evidence about a real AI system.

The repository is prepared for public hosting; creating a public remote is a separate maintainer step. The [launch guide](docs/public-launch.md) lists the concrete GitHub setup and validation steps. The workflow provides CI and a downloadable build artifact; it does not yet deploy a running environment.

Licensed under [MIT](LICENSE). Third-party dependencies retain their own licenses.
