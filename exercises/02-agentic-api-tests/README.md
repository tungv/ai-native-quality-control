# Lab 02 — Develop API tests with an agent

**Status:** Uses the Go API starter. **Prerequisites:** Lab 01 and the ability to read a small Go test. **Outcome:** Reviewed tests that detect a meaningful catalog regression.

Run the `make` commands below inside `docker compose run --rm --build lab sh`, opened from the repository root. Alternatively, run a single command from the host as `docker compose run --rm --build lab make verify`, replacing the target and arguments as needed. Edit files on the host; reports are shared with your checkout.

## Brief

The catalog exposes `GET /products?q=&limit=` and `GET /products/{sku}`. Use the documented behavior to verify that filtering, lookup, and money representation remain correct. The seeded catalog includes `trail-shoes` at 12900 cents, `rain-jacket` at 8900 cents, and an out-of-stock `city-backpack` at 5900 cents.

## Tasks

1. Inspect existing tests before asking for new ones. Map the lab 01 plan onto current coverage and identify a useful gap.
2. Give the agent a bounded change request: add or improve tests in the Go service, explain the oracle, and preserve the product contract. Ask it to identify uncertainty before editing production code. Adapt the [implementation prompt](../../prompts/implement-tests.md) if useful.
3. Cover a documented successful lookup, a boundary or invalid input, and an important interaction such as search plus limit. Do not invent the accepted range, error status, ordering, or stock-filter behavior; read the contract first. If a behavior is unspecified, record a proposed clarification separately.
4. Review every generated assertion. Avoid a test that obtains its expected price from the same implementation function being checked. Check test independence and failure-message clarity.
5. Run `make test` and `make verify`. Use the supplied `price-rounding` scenario or one reversible local change to demonstrate detection of the 12900-to-129 cents regression. If claiming your new Go test detects the defect, run that test against the corresponding local code mutation and record the result; the fault-check result alone does not prove your new test detects it.
6. Restore the baseline and show it passes. Explain whether the failure came from the new test, an existing check, or both.

## Evidence and completion

Submit the test diff, review notes, and before/defect/restored results. Show at least one important assertion actually fails when its protected requirement is broken. Explain how the test would remain useful if the implementation were refactored.

**Cleanup:** Remove local mutations and restore the baseline. Keep only the intended test or documentation improvement.

**Stretch:** Add a small property or table of edge cases that tests a general invariant. Explain why each case adds information instead of only increasing a count.
