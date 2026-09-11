# Contributing

Start with the [learning design](docs/learning-design.md) and [architecture](docs/architecture.md). Contributions should make a skill teachable and its outcome observable.

For a new lab, describe the learner, prerequisites, risk, tasks, evidence, and completion criteria. Supply synthetic fixtures, a reset procedure, an expected baseline, and at least one reproducible defect where relevant. Mark proposed capabilities as proposed until they run. Keep paid services optional.

For a code change, explain the behavior before and after, test at the narrowest useful layer, then run `docker compose run --rm --build lab make verify` from the repository root (or `make verify` with the optional native toolchain). Run the host-side commands in [the database guide](db/README.md) for database changes; the lab shell does not control Docker. Include exact commands and actual results. Report checks you could not run. Agent-generated code needs the same review as any other contribution; the author owns its correctness and provenance. Do not submit private source, customer data, credentials, or unreviewed agent transcripts.

Keep the reference baseline passing. Put intentionally broken behavior behind named, opt-in scenarios or isolated exercise artifacts with a documented expected failure. Never weaken an assertion just to obtain a green run. Do not mix solutions into exercise briefs.

Use a fork and a branch; submit a pull request with the included template. Small, independently reviewable changes are preferred. A new SUT should implement the lifecycle and reporting contract in the architecture document.

Code, original documentation, prompts, and synthetic datasets contributed here are distributed under the repository's MIT license. Only submit material you have the right to contribute. Preserve upstream notices and record any third-party asset's source and license; MIT does not relicense dependencies or copied datasets.
