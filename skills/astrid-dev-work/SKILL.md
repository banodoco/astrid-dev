---
name: astrid-dev-work
description: Deliver one assigned Astrid task by mapping its behavior end-to-end, reusing current code, fixing root causes, and returning exact candidate and focused-check evidence.
---

# Deliver an Astrid task

Read the [shared run contract](../astrid-dev-shared/run-contract.md) and task brief. Work only within its accepted outcome, scope, source identity, dependencies, route, and authority. Ask the manager when those are missing or conflict; do not silently widen the task.

## Understand before changing

Trace assigned behavior end-to-end: inputs and setup, action path, state/data flow, observable outcome, and relevant existing failure/acceptance checks. Confirm the actual source and dirty state, distinguish current base from donors, and identify existing code that can be reused. Report any source mismatch before mutation.

Implement the smallest change that delivers the assigned behavior and preserves prior passing behavior. Fix demonstrated causes at their source; do not mask failures, bypass an invariant, or add a new abstraction without a current need. If the task is routed `X` or `S`, the execution lead assigns bounded research/mechanical work to `N` helpers.

## Prove and hand off

Run the explicitly named focused checks only. Capture command, candidate SHA, relevant inputs/environment, and result. On failure, preserve the first failure, repair its cause, then rerun that same failing check. Do not run broad or auto-discovered suites. A changed candidate invalidates only the proof that depends on the changed behavior; keep prior passing proof for unaffected behavior.

Return the exact candidate identity and changed paths, end-to-end behavior mapped, checks run with results, remaining gaps, and any scope/dependency issue. Do not self-certify an independent review or claim unrun checks passed.
