# Lab 00 — Establish a baseline and a risk model

**Status:** Uses the runnable starter. **Prerequisites:** Docker with Compose v2 and a clone or extracted ZIP of this repository, as described in the root README. **Outcome:** Another learner can reproduce your starting state and understand your first testing priorities.

## Brief

You have joined a team maintaining a small synthetic storefront service. Before generating tests, determine which behavior is promised, which components exist, and which risks the starter can expose.

## Tasks

1. Read the root README and the contracts for the catalog and assistant. Identify the Go API, deterministic assistant fixture, evaluation cases, and optional database exercise. Record that the browser and live-model work are extensions.
2. Open the lab shell with `docker compose run --rm --build lab sh` from the repository root. Inside it, run `make test`, `make eval`, and `make verify`. Record the revision and result of each; reports also appear in your host checkout. Type `exit` when finished. If setup fails, classify that separately from a product failure and resolve it before continuing.
3. From the host terminal, start the service with `docker compose up --build -d --wait api`. Open `GET /health`, `GET /products`, and `GET /products/trail-shoes` in a browser on `http://127.0.0.1:8080`. Explain the price unit rather than inferring it from the display.
4. Create a [risk register](../templates/risk-register.md) with five risks spanning at least three surfaces. Include price correctness, untrusted retrieved content, and one risk in a component that is not yet implemented.
5. Select two risks for immediate testing. State a falsifiable expected outcome and the best test layer for each.

## Evidence and completion

Submit a [baseline record](../../templates/evidence.md) and the risk register. Show that the baseline checks complete, describe one response using its documented contract, and distinguish a present capability from a future extension.

**Cleanup:** Run `docker compose down` from the host when finished. Do not change seeded products or expected outcomes during this lab.

**Stretch:** Have a peer reproduce the baseline on a fresh checkout and record missing setup instructions as a documentation contribution.
