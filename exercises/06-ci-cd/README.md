# Lab 06 — Carry evidence through CI and delivery

**Status:** The starter provides local verification and repository CI. Real deployment, promotion, and rollback are extension work in a learner-controlled target. **Prerequisites:** Lab 05; permission to configure the learner's own fork and target. **Outcome:** A repeatable pipeline and a demonstrated delivery decision.

## Brief

A passing laptop run is one input to a release. Design a pipeline that records useful evidence, rejects a known regression, and connects a tested candidate to the artifact that is deployed.

## Tasks

1. Read the existing workflow before editing it. Map its jobs to the containerized `make test`, `make eval`, and `make verify` targets; identify which systems and risks it does not check. Reproduce the core gate from the host with `docker compose run --rm --build lab make verify`. API image and database commands run from the host; the lab container has no Docker socket.
2. Run or observe the workflow on your fork for a clean change. Record the candidate revision, job results, and available artifacts. If only a local run is available, label it local evidence.
3. Demonstrate a failed gate with a reversible learner-branch defect. Restore the change and show that the gate succeeds. Keep the defective branch or diff clearly labelled as teaching material.
4. Improve one useful pipeline property, such as failure artifacts, job separation, cancellation of obsolete work, or reproducibility. Explain the problem solved and verify the changed workflow.
5. Review contribution trust boundaries: pull requests from forks must not receive deployment or model-provider secrets, and untrusted code must not be run in a privileged publishing context. Keep optional paid model evaluations outside the default fork workflow.

## Delivery extension

To complete the end-to-end delivery track, add a disposable deployment target you control. A local deployment environment is acceptable if build, promotion, smoke checks, and rollback are real and reproducible.

1. Build an identifiable candidate artifact and record its revision or digest.
2. Define the promotion criteria before running the pipeline. Promote the same checked artifact and run a health check plus one behavior-level smoke check.
3. Demonstrate that a failing candidate cannot pass the documented gate. If branch protection is a required part of enforcement, configure and record it in the fork; a workflow file alone does not enforce merge rules.
4. Roll back to a known prior artifact, repeat the smoke checks, and record observations. Define a database recovery approach if the extension includes schema/data changes; an application rollback does not automatically reverse a migration.
5. Write a [release decision](../templates/release-decision.md) and a short runbook another learner can execute.

## Evidence and completion

For CI practice, submit successful and failed gate evidence plus the reviewed change. For the delivery track, also submit artifact identity, target, promotion, smoke, rollback, and post-rollback results. Clearly distinguish the two completion scopes.

**Cleanup:** Restore the passing branch, remove disposable resources you created, and revoke any exercise-only credentials. Do not publish the intentionally faulty service to an open internet endpoint.
