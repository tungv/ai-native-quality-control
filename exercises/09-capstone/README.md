# Lab 09 — Defend a quality and release decision

**Status:** Uses the starter plus at least one completed extension. **Prerequisites:** Core curriculum and one of labs 04, 06, or 08. **Outcome:** A reviewable contribution and a reproducible decision across system layers.

Run the `make` commands below inside `docker compose run --rm --build lab sh`, opened from the repository root. Alternatively, run a single command from the host as `docker compose run --rm --build lab make verify`, replacing the target and arguments as needed. Edit files on the host; reports are shared with your checkout.

## Brief

Choose one change with a clear user consequence. Investigate it, use an agent to help develop tests, review the result, maintain the suite, and recommend whether the candidate can be released within the tested scope.

Choose one of these prompts or propose a similarly bounded change:

- Connect catalog retrieval to the assistant and prevent answers from using ineligible or stale products.
- Add the browser storefront and ensure money values and unavailable inventory remain consistent across UI and API.
- Introduce a locally mocked assistant action with explicit authorization and test both legitimate use and injected requests.
- Add a disposable deployment target and prove that a known regression is blocked and the previous artifact can be restored.

## Required work

1. Write acceptance criteria, a prioritized risk register, and a scope statement naming at least two layers and one nonfunctional risk.
2. Establish a clean baseline and record the relevant versions, fixture revisions, and commands.
3. Use an agent for a bounded investigation or implementation task. Review its diff and explain at least one verified, corrected, or rejected suggestion.
4. Add tests at appropriate layers. Keep expectations independent of current implementation output and avoid duplicating the same shallow assertion everywhere.
5. Demonstrate that an important check catches a deliberate local regression, restore it, and preserve the intended regression test.
6. Include a negative or adversarial case with a benign control. If using a live model, record the evaluation split, run count, request budget, and observed uncertainty.
7. Review the resulting suite for clarity and maintenance cost. Remove accidental complexity only when important detection remains intact.
8. Run `make verify` and the documented extension checks. Have another person reproduce one material result or explicitly record that independent review is still pending.
9. Produce a [release decision](../templates/release-decision.md). If claiming delivery completion, include actual promotion, failed-gate, and rollback evidence from lab 06.

## Evidence and completion

Submit the reviewable change, [evidence record](../../templates/evidence.md), risk register, and release decision. Use the [assessment rubric](../../docs/assessment.md). A good submission may recommend blocking release if the evidence supports that conclusion.

State the limitations: unimplemented components, untested behavior, fixture/live-model differences, public-dataset exposure, and any unresolved defect. Explain what evidence would change the decision.

**Cleanup:** Restore all deliberate defects and remove disposable resources. Leave the default branch reproducible and passing.

**Peer variant:** After the submission is frozen, a reviewer may create a new synthetic boundary or attack case outside the learner's development context. Record whether it was truly held out, then evaluate the frozen candidate without quietly tuning it to the new case.
