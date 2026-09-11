# Lab 01 — Engineer a prompt for a test investigation

**Status:** Uses the runnable starter; any coding assistant may be used. **Prerequisites:** Lab 00. **Outcome:** A bounded, reviewed test plan grounded in the API contract.

## Brief

Ask an agent to help investigate catalog price correctness. The contract uses integer USD cents. The `trail-shoes` fixture costs 12900 cents. Your goal is a useful investigation, with a clear source for each expected result.

## Tasks

1. Write prompt A with only the investigation objective. Save the response without implementing it.
2. Write prompt B that supplies the relevant contract and synthetic fixture, identifies allowed files, asks the agent to separate facts from assumptions, requires boundary cases and independent expectations, and prohibits changing the implementation or expected answers during planning.
3. Ask both prompts for the same deliverable: a prioritized table of proposed cases, expected outcomes, evidence sources, and test layers. Use the same model and settings where possible; record any differences.
4. Review both outputs yourself. Count unsupported assumptions, duplicated cases, proposed assertions that merely mirror implementation, and useful cases tied to a requirement.
5. Select a plan. Correct or reject at least one agent proposal, or document how a specific proposal was independently verified if no correction was needed.
6. Freeze the reviewed plan before lab 02. Record questions that require a product decision rather than allowing an agent to invent behavior.

## A prompt structure to adapt

```text
Objective: investigate [specific risk].
Known contract and synthetic fixtures: [relevant facts and paths].
Scope: read [paths]; propose tests only; do not edit files yet.
Expectations: explain each oracle; label assumptions and unanswered questions.
Deliverable: prioritized cases with inputs, expected outcome, risk, and test layer.
Review constraints: do not treat current implementation output as the specification.
```

Do not treat this structure as a magic formula. Judge whether it helps the task with the evidence you collected.

The repository also provides a reusable [test-planning prompt](../../prompts/plan-tests.md). Compare its structure with your own after freezing the initial comparison.

## Evidence and completion

Submit both prompts, sanitized outputs, a short comparison, and the reviewed plan. Explain which prompt changes helped and which evidence supports that view. One response per prompt is a small task-specific comparison; it does not establish a general model ranking.

**Cleanup:** Keep transcripts free of real credentials or customer information. No product changes are required.

**Stretch:** Ask a peer to score the plans without knowing which prompt produced them. Repeat on a different risk and record whether the original conclusion still holds.
