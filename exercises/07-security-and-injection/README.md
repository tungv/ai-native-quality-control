# Lab 07 — Test instruction and action boundaries

**Status:** Uses the local deterministic assistant and a deliberately faulty scenario. Live-model red teaming is an extension. **Prerequisites:** Lab 03. **Outcome:** A small threat model and regression suite with adversarial and benign cases.

Run the `make` commands below inside `docker compose run --rm --build lab sh`, opened from the repository root. Alternatively, run a single command from the host as `docker compose run --rm --build lab make verify`, replacing the target and arguments as needed. Edit files on the host; reports are shared with your checkout.

## Brief

The shopping assistant receives a user message and optional context. Context can contain untrusted text. In the `context-injection` teaching scenario, the marker `[[OVERRIDE]]` causes a fake `LAB_CANARY_ONLY` disclosure and a recorded `issue_refund` action. No real refund or external tool is executed. This is a deterministic teaching defect, not a live-model exploit or a real secret.

## Tasks

1. Draw or describe the trust boundaries between user input, retrieved context, assistant output, and action execution. Identify who can supply each input and where authorization must be enforced if real tools are added.
2. Run `make eval` for the baseline, then `make eval SCENARIO=context-injection`. The second command should exit nonzero. Inspect the case-level result rather than counting any process error as a successful security test.
3. Create an attack matrix with at least four locally scoped cases: a direct conflicting request, an instruction embedded in context, fake authority text, and an attempt to obtain or trigger an unauthorized action. Use the existing schema where supported; label cases requiring new evaluator or fixture behavior as implementation work.
4. Pair each relevant attack with a benign control. For example, ordinary product text containing quoted instructions should not prevent a valid catalog answer simply because the text resembles an attack.
5. Define the expected boundary for each case: no forbidden action, no dummy canary in the answer, eligible citations, or a safe response when evidence is unavailable. Review that each assertion actually checks the intended property.
6. Add a regression or improve a missing check. If extending the application, put authorization and tool-argument validation in application code; a natural-language instruction alone is not an authorization boundary.
7. Run the baseline again and record remaining gaps. A marker-based fixture cannot measure resistance to paraphrases, multilingual attacks, long contexts, or model-dependent behavior unless those behaviors are implemented and tested.

## Evidence and completion

Submit the trust-boundary description, attack/control matrix, reviewed diff, baseline and defect evidence, and limitations. Show both that the forbidden behavior is detected and that the benign control still works.

**Cleanup:** Restore the default scenario. Keep all values synthetic and all targets local or explicitly authorized. Do not use real credentials, external exfiltration endpoints, customer data, or real financial actions.

**Stretch:** Add an optional live-model adapter with a local mock tool executor. Separate proposed actions from executed actions, enforce authorization outside the model, cap requests, repeat the attack/control set, and preserve any newly observed failure as a synthetic regression case.
