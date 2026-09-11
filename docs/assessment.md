# Assessment

Assess the learner's judgment and reproducible evidence. A green run, high coverage percentage, or persuasive agent transcript is not sufficient on its own.

For each exercise, submit a short [evidence record](../templates/evidence.md), a reviewable diff when code changed, and the commands or artifacts needed to verify important claims. The reviewer checks at least one claimed result independently.

## Rubric

Score each dimension from 0 to 4. Use the descriptions below as anchors; 1 and 3 represent partial progress between them.

| Dimension | 0 — Missing | 2 — Developing | 4 — Independent |
| --- | --- | --- | --- |
| Risk and expectations | Tests have no stated requirement or oracle | Main happy path and some boundaries tied to requirements | Risks prioritized; independent expected outcomes; important uncertainty and exclusions explicit |
| Agent collaboration and review | Generated output accepted without inspection | Bounded prompt and basic diff review recorded | Clear context and constraints; unsupported assumptions rejected; meaningful improvements explained |
| Detection and maintainability | No useful assertions or disabled failures | Useful tests run and one failure explained | Deliberate regression detected; isolated, stable checks; understandable fixtures and failure messages |
| Evaluation and security reasoning | Fixture results overclaimed; sensitive data or unsafe actions used | Cases labelled and obvious trust boundaries recognized | Data leakage and holdout limits addressed; appropriate metrics; benign/adversarial pairs; enforced boundaries and uncertainty explained |
| Reproducibility and delivery | Claims cannot be reproduced | Setup, commands, revision, and results recorded | Independent rerun succeeds; artifacts support decisions; cleanup and relevant delivery/rollback evidence are complete |

Recommended completion threshold: **15/20, no dimension below 2**, plus the exercise's required evidence. This is a teaching convention for this repository, not a professional certification. For an early lab, evaluate only the scope actually exercised; for example, a local API lab needs honest security limits, not a complete deployment.

## Evidence gates

Regardless of score, return the submission for revision if it:

- changes a requirement, expected answer, or threshold only to hide a failure;
- claims a live-model, browser, database, deployment, or rollback result without running that environment;
- commits real customer data or credentials;
- runs adversarial tests against an unauthorized target;
- cannot show what changed and which check validates that change.

Missing optional extensions are not failures when the learner states their scope accurately.

## Review procedure

1. Read the risk statement before inspecting the test implementation.
2. Select an important passing assertion and ask why its expected value is correct.
3. Reproduce one reported check and one deliberately induced regression, where the lab requires one.
4. Inspect a rejected or corrected agent suggestion and the learner's reasoning.
5. Check whether failure cases include a benign control and whether the chosen metrics can conceal an important failure.
6. Record scores, one strength, one specific revision, and the completion decision.

For live-model evaluations, inspect case-level results and run metadata in addition to aggregate scores. Report sample size and observed variation. Do not rank learners on raw model success rates when their providers, datasets, or budgets differ.

## Capstone acceptance

The capstone must span at least two system layers and one nonfunctional risk. It must include an independently reviewed expectation, a test that detects a demonstrated regression, one negative or adversarial control, and a reproducible release decision. The learner must state what was not tested and why it matters.

If delivery is in scope, show the exact built artifact or revision, a successful smoke check, a deliberately blocked promotion, and a rollback with a post-rollback check in the learner-controlled target. A proposed workflow or green unit-test job alone does not complete the delivery requirement.

An instructor may add a new synthetic holdout case after the learner freezes the submission. Record when it was created and whether the learner or agent could access it. Public repository fixtures cannot serve as confidential examination material.
