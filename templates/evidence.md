# Exercise evidence

Copy this template into your submission and replace the placeholders. Omit fields that do not apply, explaining material omissions.

- Exercise / module / learning objective:
- Learner / date:
- Repository revision and changed files:
- Runtime versions / OS / configuration / fixture version:
- Fault or scenario, if enabled:
- Agent/provider/model used for test development, if any:

## Risk and oracle

What user or business behavior matters? Link the requirement. Explain why the expected result is trustworthy independently of the implementation being tested.

## Reproduction and observations

| Case / requirement | Exact command and setup | Expected result | Actual result | Evidence location |
| --- | --- | --- | --- | --- |
| | | | | |

Record exit codes and relevant assertions. Include reset/cleanup steps. For fault exercises, distinguish baseline-pass, intended-fault-fail, and restored-baseline-pass. Mark skipped, unsupported, and infrastructure-failed cases explicitly.

## Agent use and human verification

Link the prompt or summarize its inputs and constraints. Record important incorrect assumptions, edits you made, and how you checked the generated assertions. Avoid publishing sensitive prompts or raw personal data.

## AI evaluation details, when applicable

Record SUT provider/model, prompt version, dataset version, retrieved IDs, configuration, number of trials, per-case outcomes, latency/cost, and rubric/judge version. Keep semantic quality separate from structural correctness. Note whether the SUT was a deterministic fixture or a live model.

## Decision and limits

State pass/fail/needs-investigation for the tested scope and justify the decision. List remaining risks and untested behavior. Identify the next action and owner; do not turn an incomplete run into a broad release approval.
