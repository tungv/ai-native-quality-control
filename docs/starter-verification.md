# Starter verification record

Verified on 2026-09-11 on macOS arm64 using Go 1.27.1 and Python 3.14.4 against the initial, uncommitted source tree. Go was downloaded from the official release endpoint, checksum-verified, and supplied to Make through the `GO` override; it was not installed globally.

| Check | Observed result |
| --- | --- |
| `make verify` | Passed: Go race/unit tests, `go vet`, and all checks below |
| Python evaluator unit tests | 11 passed, including controls that reject fabricated answers and transport errors as successful fault evidence, and permit added injection cases |
| Baseline HTTP checks | 7/7 passed |
| Baseline assistant cases | 8/8 passed |
| Price fault control | Only `product-price` failed, with observed price 129 instead of 12900 cents |
| Context-injection control | Only `indirect-injection` failed, with the synthetic canary and `issue_refund` action in the response |
| Standalone injection evaluation | Exited nonzero as intended |
| Documentation links | All local targets across 33 Markdown files existed before this record was added |
| YAML files | Compose, CI, dependency configuration, and issue forms parsed successfully |

Local reports are in `reports/` and are intentionally ignored by Git. Future changes should generate new evidence rather than treating this record as a current guarantee.

Docker was unavailable, so `make db-test` and the image startup/readiness sequence were **not executed locally**. The SQL and Compose configuration received static review. The separate database CI job must pass on GitHub before database runtime behavior is treated as verified. The image tag and digest were checked against the registry.

The GitHub workflow has not run remotely, and no public repository or deployment was created during this verification. The initial CI definition used Linux and Python 3.12; the Docker-first update below replaces that setup. A live-model, browser, or deployment result is outside the implemented starter scope.

## Docker-first follow-up

The repository now includes a multi-stage `Dockerfile`, a `.dockerignore`, and Compose services for the toolchain and API. The lab image supplies Go 1.27.1, Debian Bookworm's Python 3.11, Make, Git, and a compiler for race testing. CI builds both images, runs the suite inside the lab, starts the API runtime, checks its published port, and runs the database assertions separately.

Observed locally after these changes:

- `make verify` passed again using the temporary native Go toolchain, including the new formatting gate, 11 evaluator tests, 7 baseline HTTP checks, 8 assistant cases, and both fault controls.
- A checksum-verified standalone Docker Compose 5.5.1 binary parsed the configuration successfully. Resolved configuration checks covered the default services, lab isolation, build targets, localhost port binding, and user-ID/port/scenario overrides.
- Dockerfile base-image tags and manifest digests were resolved against the official registry, with Linux arm64 and amd64 variants present.
- Compose, workflow, and dependency-update YAML parsed successfully. Independent static review found no remaining concrete Docker configuration defect.

**Docker image builds and container execution remain unverified locally.** No Docker engine is installed in this environment; the standalone Compose binary only validates configuration without an engine. The Docker CI jobs have not run remotely. A passing native run or configuration parse does not substitute for that runtime verification.
