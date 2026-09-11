# Curriculum

The program builds from repeatable local checks to a release decision across several systems. Experience in manual QC is enough to start. Learners need Git basics and the ability to read a small test; Go, SQL, TypeScript, and model APIs are learned as needed for a selected route.

Read the root [README](../README.md) for Docker setup, implemented components, and command behavior. Go, Python, and Make are supplied by the lab image; they do not need host installation. This curriculum describes exercise work; it does not imply that a planned browser app, live model integration, or deployed environment is already available.

## Choose a route

| Route | Exercises | Outcome |
| --- | --- | --- |
| Core | 00 → 01 → 02 → 03 → 05 → 07 | A reviewed test contribution and defensible evaluation report |
| Retrieval | Core + 04 | Database and ranking checks with labelled retrieval evidence |
| Delivery | Core + 06 | A verified promotion, failed-gate, and rollback demonstration |
| Browser | Core + 08 | A browser implementation or contribution with journey and accessibility checks |
| Capstone | Core + at least one extension → 09 | A cross-layer quality decision with a reproducible evidence package |

The browser, live-model, and deployment activities are extension assignments. They require building or connecting the relevant environment. A learner who completes the core route should not claim those environments were tested.

## Exercise map

| Lab | Focus | Starting point | Required artifact |
| --- | --- | --- | --- |
| [00 — Baseline and risk](../exercises/00-baseline/README.md) | Reproduce the system and identify unknowns | Supplied starter | Baseline record and prioritized risks |
| [01 — Prompt engineering](../exercises/01-prompt-engineering/README.md) | Context, constraints, independent expectations | 00 | Two prompt versions, comparison, reviewed test plan |
| [02 — Agentic API tests](../exercises/02-agentic-api-tests/README.md) | Agent-generated Go tests and meaningful assertions | 01 | Test diff, review notes, demonstrated regression |
| [03 — Assistant evaluation](../exercises/03-assistant-evaluation/README.md) | Dataset quality, grounding, evaluation limits | 02 | Case additions, metric definitions, error analysis |
| [04 — Retrieval and data](../exercises/04-retrieval-and-data/README.md) | PostgreSQL, vector ranking, eligibility | 03; database setup | Labelled queries, SQL checks, retrieval report |
| [05 — Test suite maintenance](../exercises/05-suite-maintenance/README.md) | Review, brittleness, flakes, mutation evidence | 02 and 03 | Maintained suite and before/after justification |
| [06 — CI and delivery](../exercises/06-ci-cd/README.md) | Pipeline gates, artifacts, deployment, rollback | 05; learner-controlled delivery target | Successful and failed pipeline evidence, release record |
| [07 — Security and injection](../exercises/07-security-and-injection/README.md) | Trust boundaries and bounded red teaming | 03 | Threat model, attack matrix, paired controls |
| [08 — Browser journeys](../exercises/08-browser-journeys/README.md) | Next.js UI, browser tests, accessibility | 02; implement/connect browser extension | Journey tests and reviewed browser evidence |
| [09 — Capstone](../exercises/09-capstone/README.md) | Combine risks, implementation, review, delivery | Core and one extension | Reviewable change and release recommendation |

## Common working agreement

Use a learner branch or fork. Before changing anything, read the component's contracts and run the baseline checks. Preserve the original result so new failures can be attributed correctly.

The shared starter command vocabulary runs inside the lab container:

```sh
docker compose run --rm --build lab sh
make test
make eval
make verify
exit
```

Exercise `make` examples assume this shell. For one command from the host, use `docker compose run --rm --build lab make verify` (substitute the required target and arguments). Your editor and agent can edit the host checkout; the container sees those changes and writes reports back to it.

From a host terminal, `docker compose up --build -d --wait api` starts the interactive API and `docker compose down` removes services. Run the optional [database lab's commands](../db/README.md) from the host too. The lab container has no Docker socket or external network; `make run` inside it is not accessible from a host browser. Follow the README for prerequisites and shutdown behavior. Extensions may add commands, but those commands are part of the learner's reviewed change and must be documented before another person can reproduce the exercise.

For every lab, keep an [evidence record](../templates/evidence.md). Save machine outputs as artifacts when useful; avoid committing large logs. Give a reviewer the revision, command, relevant result, and interpretation. Redact any accidental secret before sharing and rotate it if it was real.

## Checkpoints

- After lab 01, a peer should be able to explain which requirements support the proposed tests without consulting the agent.
- After lab 03, a peer should be able to distinguish a fixture pass from evidence about a live model.
- After lab 05, another learner should reproduce a detected regression and understand why the maintained suite is better.
- After lab 07, the learner should identify where enforcement belongs and show that benign behavior still works.
- At the capstone, the reviewer should be able to repeat the important checks and independently agree or disagree with the release decision.

Use the [assessment rubric](assessment.md) at these checkpoints. Revisit a weak dimension before expanding the number of tests or system components.
