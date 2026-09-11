# Lab 03 — Build an assistant evaluation you can trust

**Status:** Uses a deterministic assistant fixture and the supplied evaluator. A live-model adapter is an optional extension. **Prerequisites:** Lab 02. **Outcome:** A reviewed dataset change and an evaluation report with accurate limits.

Run the `make` commands below inside `docker compose run --rm --build lab sh`, opened from the repository root. Alternatively, run a single command from the host as `docker compose run --rm --build lab make verify`, replacing the target and arguments as needed. Edit files on the host; reports are shared with your checkout.

## Brief

`POST /chat` accepts a message and optional context, and returns an answer, citations, and actions. The starter's fixture makes evaluation repeatable without a model account. You are evaluating this fixture's contract and the evaluator's ability to catch seeded defects.

## Tasks

1. Inspect `evals/cases.json` and the evaluator. Describe what each assertion can prove and what it cannot. Identify whether answer text, citations, actions, and money correctness are checked independently.
2. Run `make eval` and inspect `reports/eval-baseline.json`. Record case-level results and the denominator behind any aggregate success rate.
3. Add a small, purposeful set of cases using the existing schema. Include a known product question, missing or ambiguous evidence, and a boundary involving context. Only assign expected behavior supported by a documented requirement; propose contract changes separately.
4. Record why each expected outcome is correct. Have a peer or your own independent review check labels before using agent-generated cases to score the system.
5. Choose a release criterion before running the changed dataset. Critical forbidden actions should be assessed individually rather than being hidden by an overall average.
6. Demonstrate that evaluation rejects the context-injection defect: `make eval SCENARIO=context-injection` is expected to exit nonzero. Record the failing cases and explain why that exit is useful evidence. The separate `price-rounding` scenario changes the catalog API; its detection belongs to the API checks and does not imply the canned chat response changes.
7. Restore the default scenario, run `make eval`, and write a short error analysis. Distinguish fixture behavior, dataset gaps, and evaluator gaps.

## Evidence and completion

Submit the dataset diff, label rationale, baseline and defect results, metric definitions, and an honest decision. A passing deterministic fixture does not demonstrate live-model grounding, resistance to every injection, or production reliability.

**Cleanup:** Return to the default scenario. Do not change expected results or suppress a failure just to make a defective scenario pass.

## Optional live-model extension

Implement or connect a provider adapter in a separate reviewed change. Define a request/spend cap, record provider/model and prompt revisions, and use synthetic data only. Establish development, validation, and held-out cases as described in [learning design](../../docs/learning-design.md).

Repeat trials and report observed failures and variation. Evaluate retrieval, answer grounding, and tool permissions separately. If adding a model judge, compare it with human-labelled examples and report judge errors. This extension is complete only when it was actually run; a proposed adapter is a design artifact.
