---
name: astrid-dev-iterate
description: Implement, debug, or repair one scoped Astrid change and return an exact feature candidate with focused proof and remaining claims.
---

# Iterate on one Astrid change

Read the [shared run contract](../astrid-dev-shared/run-contract.md), the assigned brief (an issue, bug report or existing project task), and the working repository's instructions. **An issue or small fix needs no new project pack.** This is the single implementation/debug/focused-test repair loop. Work only within the accepted outcome, paths, dependencies, frozen source identity, route, and authority. Do not create another worker workflow.

## Map and change the behavior

- Confirm the actual repository, ref/SHA, dirty state, current base, donor identities, and custody before mutation. Preserve user changes; report mismatched or missing source identity to the manager.
- Trace the assigned behavior from setup and inputs through the existing action/state path to its observable result and focused acceptance check. Reuse current code and fix demonstrated causes at their source. Make the smallest complete in-scope change.
- On an `X` or `S` task, delegate as the [run contract](../astrid-dev-shared/run-contract.md#who-answers-for-a-run) requires.
- Use the cheapest venue that can prove the stated claim. Local focused checks are the default; use a hosted runner only for a real OS/CI requirement, and GPU/remote infrastructure only when it is both explicitly authorized and required by live hardware or that environment. A higher venue alone does not make proof stronger.
- A local check proves a claim only if it exercises the same path as the acceptance check. For an installed or served product, start it the way the installed service does (same profile and configuration, called over its public interface), not by calling its internals in-process. A fixture standing in for an older release uses only what that release's public interface serves. If the local setup cannot match, say so and let the hosted run be the proof.
- Run only the scoped checks the [run contract](../astrid-dev-shared/run-contract.md#checks-and-failure-repair) allows.

## Iterate freely; qualify once

Two different activities share the word "test". Keep them apart.

- **Iterating** is getting one red test to green. It is cheap and disposable. Reproduce the failing test with its exact command, keep the full raw output in your workdir, read the first error before forming a hypothesis, fix the cause, and rerun that test as often as you need. Reruns on a new commit need no permission, no review and no committed record. Stop at the worker threshold in the [run contract](../astrid-dev-shared/run-contract.md#cheapest-model-first) and hand the manager the raw output, what you tried and your best guess.
- **Qualifying** is the evidence a release gate counts. It runs once, on the frozen commit, on CI. Only this run needs the exact-SHA record described below, and nothing before it counts as evidence.

Gate rules do not apply to iteration. A scratch or diagnostic run needs no authorization, no independent review and no sanitized-only output. Keep raw logs while diagnosing; redact only what you commit, and never print credentials. Two things hold in both modes: [no check is weakened to get a pass](../astrid-dev-shared/run-contract.md#checks-and-failure-repair), and paid spend always needs its own authorization.

## Capture proof and repair failures

Record each check's proof, repair its failures and carry proof forward exactly as the [run contract](../astrid-dev-shared/run-contract.md#checks-and-failure-repair) says.

## Return a candidate

Return the exact candidate SHA/tree and source identity, changed paths, mapped behavior, focused commands and inner exits, proof carried forward with its unchanged-input basis, first failures and reruns, remaining claims/gaps, and any dependency or scope issue. A candidate is a [feature handoff only](../astrid-dev-shared/run-contract.md#review-and-promotion-boundaries).

## Source adaptation

The narrow venue, inner-exit, retry-family, exact-revision, and carry-forward principles were adapted from `banodoco/astrid-agent`'s `astrid/packs/developer/docs/fast-iteration/SKILL.md` at commit `43b6fb2cdb877afd6d37832c7f279754ba01592d` (2026-11-02). Broad suite defaults, receipt machinery, tuple-train procedures, and release gates were not imported; the local scoped-check policy in the shared contract governs.
