# Learning design

This repository is a public, MIT-licensed practice environment for QC engineers learning to work with AI-assisted development. It teaches how to produce credible quality evidence when both the software and the people building it use AI.

The learner owns the test strategy, expected results, code review, and release decision. An agent may investigate code, propose cases, write tests, and explain failures. Its output remains a proposal until the learner verifies it against a contract, fixture, or other independent evidence.

## A connected product, several test surfaces

Use a synthetic ecommerce product as the shared context. A browser storefront, Go service, PostgreSQL retrieval layer, and shopping assistant expose different failure modes while sharing product records and business rules. Individual components should also run independently so a learner can practice one surface without first learning the whole stack.

| Surface | Questions a QC engineer must answer | Suitable evidence |
| --- | --- | --- |
| Next.js storefront | Can users complete a journey with keyboard, narrow viewport, slow network, and failed requests? | Browser assertions, accessibility findings, request traces |
| Go API | Are validation, response contracts, error handling, and concurrent requests correct? | Boundary tests, integration tests, race results when applicable |
| PostgreSQL and vector search | Is the correct data eligible, correctly ranked, isolated, and refreshed? | SQL assertions, labelled retrieval cases, ranking metrics, query plans |
| Shopping assistant | Is the answer grounded, does it respect instruction boundaries, and does it fail safely? | Evidence-labelled cases, source checks, attack regressions, repeated live runs |
| Delivery pipeline | Can an untrusted contribution be checked and a known artifact promoted or rejected? | CI artifacts, gate demonstrations, release and rollback records |

These are the target learning surfaces, not a claim that every application exists in the starter. The root README is the source of truth for runnable components. The [curriculum](curriculum.md) labels extension work explicitly.

## Three modes of practice

1. **Deterministic foundation.** Run the supplied fixtures and local checks without credentials or a paid model. Learn contract testing, regression detection, evidence recording, and repeatable evaluation. A deterministic assistant fixture exercises the evaluation workflow; it does not measure a live model's intelligence or security.
2. **Guided changes.** Add a test, introduce one reversible local defect, show that the test detects it, and restore the implementation. Keep reference expectations under human review. A clean checkout must remain a working baseline.
3. **Extensions and capstones.** Connect a browser, database, or optional model provider; add realistic failure modes; measure uncertainty; and defend a release decision. Each extension must document new dependencies, setup, reset, cost, and limitations.

The program uses evidence milestones rather than a fixed duration. Learners can complete the core route first and then specialize in browser testing, retrieval, delivery, or security.

## The learning loop

For every exercise:

1. State a risk and a falsifiable requirement before asking an agent to write tests.
2. Give the agent a bounded task, relevant contracts, allowed files, and an evidence format.
3. Review its assumptions and diff. Record rejected suggestions as well as accepted work.
4. Run the checks and inspect failures. Distinguish product defects, test defects, and environment defects.
5. Demonstrate that an important assertion catches a deliberate local regression.
6. Explain the result, uncertainty, and next decision in a short evidence report.

Successful agent use is measured by useful, reviewed evidence, not the number of prompts, generated tests, or lines of code.

## Sources of truth and evaluation discipline

Requirements and labelled fixtures define expectations. Current implementation behavior is evidence to investigate, not automatically the correct result. An agent must not silently rewrite expected outputs, disable checks, or adjust a threshold simply to make a run pass.

Separate three datasets when building an evaluation:

- **Development cases:** visible examples used to develop prompts, code, and tests.
- **Validation cases:** visible cases used to choose an approach and threshold. Record every revision made in response to their results.
- **Held-out cases:** cases reserved until the approach is frozen. If inspected or used to tune the implementation, retire them to the development set and create a new holdout.

A public repository cannot keep reference answers secret. Public challenge fixtures are useful reproducible benchmarks, but cannot establish that an agent has never seen them. For an assessment, an instructor or peer should prepare an additional private, synthetic variant outside the learner's development context. When no independent holdout exists, say so in the report.

For a live model, record the provider, exact model identifier returned when available, prompt revision, retrieval corpus revision, settings, tool policy, run count, date, and cost. Run repeated trials, report counts and variation, and inspect important individual failures. Do not infer production reliability from one successful response. A model judge may assist triage; sampled human labels and deterministic checks must test the judge itself.

## Safe public practice

All committed users, products, orders, conversations, credentials, and attacks must be synthetic. Use reserved example domains for dummy addresses. Do not copy customer support chats, production database exports, internal prompts, or real credentials into prompts, fixtures, issues, screenshots, or CI logs.

Adversarial exercises run only against the local sandbox or an environment the learner controls and is authorized to test. Their purpose is to verify trust boundaries and preserve regressions. External callbacks, genuine credentials, customer identities, and real payment or order actions are unnecessary for these exercises; use local mocks and unmistakable dummy values.

The default route should need no model API key. Optional live evaluations require deliberate opt-in and a learner-defined request or spend cap. Do not run them automatically for pull requests from forks.

## Maintaining the learning environment

Keep the default branch healthy. An intentionally faulty example belongs in a clearly labelled exercise patch, fixture, or learner branch, with an expected failure and a restoration procedure. Never depend on a hidden persistent defect in the shared baseline.

Each new exercise must provide prerequisites, explicit implementation status, a bounded task, independent expectations, evidence requirements, success criteria, and cleanup instructions. Each new system under test should provide deterministic seed/reset behavior, a documented contract, a health check, and a way to observe failures without exposing secrets.

Maintain learner-facing briefs separately from optional instructor solutions. Solutions may be public in an MIT repository, but should carry a spoiler label. The assessment values explanation and regression evidence, so copying a solution is insufficient.

See [assessment](assessment.md) for review criteria and [the evidence template](../templates/evidence.md) for a reusable record.
