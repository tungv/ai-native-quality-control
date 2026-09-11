# Lab 05 — Review and maintain a test suite

**Status:** Uses existing starter tests plus learner changes. **Prerequisites:** Labs 02 and 03. **Outcome:** A smaller or clearer suite with preserved or improved defect detection.

Run the `make` commands below inside `docker compose run --rm --build lab sh`, opened from the repository root. Alternatively, run a single command from the host as `docker compose run --rm --build lab make verify`, replacing the target and arguments as needed. Edit files on the host; reports are shared with your checkout.

## Brief

Your agent-assisted contributions have increased the test suite. Review the result as a maintainer. Find redundant checks, weak assertions, excessive coupling, and confusing failures before the next learner inherits them.

## Tasks

1. Inventory existing checks by risk and test layer. Identify uncovered risks and duplicate checks. A repeated assertion may be useful at another boundary; explain the decision before deleting it.
2. Ask an agent to review a bounded subset. Require file references and a concrete failure example for each recommendation. Review the suggestions yourself. The [suite-review prompt](../../prompts/review-suite.md) and [failure-triage prompt](../../prompts/triage-failure.md) are optional starting points.
3. Select one useful maintenance change: remove duplication, replace an implementation-coupled expectation, improve isolation, reduce unnecessary setup, or improve diagnostic output. If no real issue exists, create a clearly labelled local flawed example and improve that; do not invent findings about the shared baseline.
4. Record the before and after suite behavior. Repeat only where an unresolved stability concern justifies it; repeated green runs alone do not prove absence of flakiness.
5. Check defect detection using at least two purposeful local mutations, such as an incorrect price and a missing negative-path assertion's protected behavior. Count detected mutations over valid non-equivalent mutations tried, and list them. Explain this small sample rather than presenting it as comprehensive mutation coverage.
6. Run `make test`, `make eval`, and `make verify` after restoring the implementation. Explain why the maintained suite is easier to trust or maintain.

## Flake investigation option

If a real or deliberately local flaky test is available, record its reproduction conditions and failure rate over a stated run count. Investigate timing, shared state, ordering, network dependencies, and resource cleanup. Retries may collect evidence; they should not erase the underlying failure. Any quarantine must have a reason, owner, and removal condition.

## Evidence and completion

Submit a reviewed diff, a risk-to-test map, the mutation sample, and the before/after argument. The improvement must preserve important behavior and must not achieve green results by removing assertions or hiding failures.

**Cleanup:** Restore deliberate mutations and remove temporary flawed examples unless they are intentionally contributed as labelled teaching fixtures.

**Stretch:** Review another learner's suite without reading their agent transcript first. Compare independent review findings with the agent's findings.
