PYTHON ?= python3
GO ?= go
GOFMT ?= gofmt
SCENARIO ?= baseline

.PHONY: help run test smoke eval fault-check verify check-format build db-up db-test db-down
help:
	@echo "run          Start the API on 127.0.0.1:8080 (SCENARIO=baseline by default)"
	@echo "verify       Run unit, HTTP, assistant, and deliberate-fault checks"
	@echo "test         Run Go and Python unit tests"
	@echo "smoke        Verify the real HTTP API in a temporary process"
	@echo "eval         Evaluate the assistant; writes reports/eval-<scenario>.json"
	@echo "fault-check  Prove checks detect the supplied faults"
	@echo "check-format Check Go formatting without changing files"
	@echo "build        Build artifacts/catalog-api for the current platform"
	@echo "db-test      Start disposable pgvector lab and verify SQL behavior (Docker)"
	@echo "db-down      Remove this project's disposable database containers"
run:
	cd services/catalog-api && LAB_SCENARIO="$(SCENARIO)" $(GO) run .
check-format:
	@files="$$($(GOFMT) -l services/catalog-api)" || exit $$?; test -z "$$files" || { printf 'Go formatting required:\n%s\n' "$$files"; exit 1; }
build:
	cd services/catalog-api && $(GO) build -trimpath -o ../../artifacts/catalog-api .
test:
	cd services/catalog-api && $(GO) test -race ./...
	cd services/catalog-api && $(GO) vet ./...
	$(PYTHON) -m unittest discover -s evals -p 'test_*.py' -v
smoke:
	GO="$(GO)" $(PYTHON) -m evals.run smoke --scenario "$(SCENARIO)"
eval:
	GO="$(GO)" $(PYTHON) -m evals.run eval --scenario "$(SCENARIO)"
fault-check:
	GO="$(GO)" $(PYTHON) -m evals.run faults
verify:
	$(MAKE) check-format
	$(MAKE) test
	$(MAKE) smoke SCENARIO=baseline
	$(MAKE) eval SCENARIO=baseline
	$(MAKE) fault-check
db-up:
	docker compose up -d --wait db
db-test: db-up
	docker compose exec -T db psql -U learner -d playground -v ON_ERROR_STOP=1 -f /lab/tests.sql
db-down:
	docker compose down
