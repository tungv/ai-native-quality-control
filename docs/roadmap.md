# Implementation roadmap

This roadmap separates the first runnable learning loop from the intended multi-stack playground. Milestones are acceptance gates, not delivery dates. The [README](../README.md) records what currently runs.

| Milestone | Deliverable | Exit criteria |
| --- | --- | --- |
| 0 — Learning foundation | MIT repository, contribution guidance, risk-based learning path, prompts, evidence templates | A newcomer can explain the workflow and submit reviewable evidence without access to a private system. |
| 1 — Offline starter | Go API, deterministic assistant fixture, Python evals, explicit fault exercises, baseline CI | A fresh checkout can run baseline tests without a model key; a selected fault fails a relevant assertion; reset restores the baseline. |
| 2 — Database practice | Standalone PostgreSQL/pgvector lab, then API integration and migration exercises | Exact ranking/filtering assertions reproduce; database state resets; CI demonstrates persistence and migration tests. |
| 3 — Browser journeys | Next.js ecommerce UI and accessible chat, browser tests, traces | A learner tests catalog → search → cart/chat journeys, keyboard behavior, and a deliberate UI regression against the API contract. |
| 4 — Real AI evaluation | Provider-neutral adapter, retrieval, prompt versions, reviewed datasets and tool policy | Offline mode remains available; live trials record model/configuration/cost and uncertainty; direct and indirect injection cases assert actual output and tool effects. |
| 5 — End-to-end delivery | Artifact build, temporary environment deployment, smoke/E2E gates, rollback and cleanup | A learner can demonstrate a successful release and an intentionally failed release with verified recovery and no abandoned environment. |
| 6 — Advanced maintenance | Change-driven scenarios, flaky-suite diagnosis, load/accessibility/security regressions, evaluator review | Learners improve a degraded suite, preserve fault detection, justify removed tests, and defend a release decision with evidence. |

The current starter focuses on milestones 0–1 and an optional SQL entry point into milestone 2. Browser coverage, live model quality, integrated RAG, and actual CD must not be advertised as complete until their exit criteria run successfully.

## Module acceptance checklist

- A documented product contract and a small synthetic dataset with stable IDs.
- Start, health, seed, reset, test, and report capabilities described in [architecture](architecture.md).
- A default baseline and at least one isolated, deliberate regression with an independent assertion that detects it.
- A learner brief with prerequisites, scope, expected evidence, and an assessment rubric.
- A reviewed reference approach kept separate from the brief, with public visibility acknowledged.
- Repeatable commands, documented dependency versions, bounded execution, and clean teardown.
- Security boundaries and known omissions stated in language a learner can verify.
- Original or appropriately licensed code and teaching fixtures suitable for the public repository.

## Maintenance policy

Version scenarios, datasets, contracts, and prompts so evidence can be compared over time. A product contract change should identify which expected behaviors change and which regressions must still be detected. Dependency upgrades should run the affected module checks; model or retrieval changes should additionally rerun quality cases.

Treat flaky tests as investigation work: assign an owner and an expiry to any quarantine, preserve reproduction evidence, and restore a stable assertion. Do not silently weaken gates or replace semantic expectations with broad snapshots. Add new modules when they contribute a distinct testing lesson, rather than multiplying stacks without a learning objective.
