---
name: astrid-dev-iterate
description: Implement, debug, or repair one scoped Astrid change and return an exact feature candidate with focused proof and remaining claims.
---

# Iterate on one Astrid change

Read the [shared run contract](../astrid-dev-shared/run-contract.md), the assigned brief (an issue, bug report or existing project task), and the working repository's instructions. **An issue or small fix needs no new project pack.** This is the single implementation/debug/focused-test repair loop. Work only within the accepted outcome, paths, dependencies, frozen source identity, route, and authority. Do not create another worker workflow.

## Map and change the behavior

- Confirm the actual repository, ref/SHA, dirty state, current base, donor identities, and custody before mutation. Preserve user changes; report mismatched or missing source identity to the manager.
- Trace the assigned behavior from setup and inputs through the existing action/state path to its observable result and focused acceptance check. Reuse current code and fix demonstrated causes at their source. Make the smallest complete in-scope change.
- On an `X` or `S` task, delegate bounded research, reading, mechanical edits and running checks to `N` helpers, as the run contract requires, and keep the judgment and the final change yourself.
- Use the cheapest venue that can prove the stated claim. Local focused checks are the default; use a hosted runner only for a real OS/CI requirement, and GPU/remote infrastructure only when it is both explicitly authorized and required by live hardware or that environment. A higher venue alone does not make proof stronger.
- A local check proves a claim only if it exercises the same path as the acceptance check. For an installed or served product, start it the way the installed service does (same profile and configuration, called over its public interface), not by calling its internals in-process. A fixture standing in for an older release uses only what that release's public interface serves. If the local setup cannot match, say so and let the hosted run be the proof.
- Run only explicitly named, feature-focused checks. Never run broad, auto-discovered, repository-wide, or full affected suites, including opt-in suites. Planning work runs no checks unless requested. Do not invent selectors or commands: use documented narrow checks supported by the current repository and brief.

## Iterate freely; qualify once

Two different activities share the word "test". Keep them apart.

- **Iterating** is getting one red test to green. It is cheap and disposable. Reproduce the failing test with its exact command, keep the full raw output in your workdir, read the first error before forming a hypothesis, fix the cause, and rerun that test as often as you need. Reruns on a new commit need no permission, no review and no committed record. Stop after three attempts or 45 minutes without progress and hand the manager the raw output, what you tried and your best guess.
- **Qualifying** is the evidence a release gate counts. It runs once, on the frozen commit, on CI. Only this run needs the exact-SHA record described below, and nothing before it counts as evidence.

Gate rules do not apply to iteration. A scratch or diagnostic run needs no authorization, no independent review and no sanitized-only output. Keep raw logs while diagnosing; redact only what you commit, and never print credentials. Two things hold in both modes: never skip, loosen, xfail or delete a check to get a pass, and paid spend always needs its own authorization.

## Capture proof and repair failures

For each check, capture the exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. Judge the build/test/install command's result, not a CI dispatcher, pod broker, timeout, relay, upload, or other wrapper's success. Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), or `NO-RESULT` (evidence absent). A pass applies only to the exact candidate and inputs it names.

Keep product failures distinct from infrastructure failures. Retry a transient capacity/readiness/network/eviction/NO-RESULT failure with the same inputs when appropriate. Fix invalid requests instead of retrying them. After two failures with the same signature, do not run unchanged again: identify and change the cause, fixture, environment, or input first, then rerun the actual failing check. Preserve the first failure and its exact command/candidate; never replace it with a broader check.

Carry prior proof forward only when its inputs and relevant product/dependency/generated/installed bytes are unchanged and that unchanged state is evidenced. A new candidate invalidates only proof dependent on the changed behavior; keep unaffected proof. Protected surfaces or changed relevant inputs require exact-candidate proof. Do not turn a set of accepted scoped checks into a claim that the entire repository or suite passed.

## Return a candidate

Return the exact candidate SHA/tree and source identity, changed paths, mapped behavior, focused commands and inner exits, proof carried forward with its unchanged-input basis, first failures and reruns, remaining claims/gaps, and any dependency or scope issue. A candidate is a feature handoff only: this workflow does not integrate it, independently review it, promote it, publish it, or claim that those actions occurred. The release workflow composes and rechecks the integrated candidate; if that check fails, return the repair to this same iterate loop.

## Source adaptation

The narrow venue, inner-exit, retry-family, exact-revision, and carry-forward principles were adapted from `banodoco/astrid-agent`'s `astrid/packs/developer/docs/fast-iteration/SKILL.md` at commit `43b6fb2cdb877afd6d37832c7f279754ba01592d` (2026-11-02). Broad suite defaults, receipt machinery, tuple-train procedures, and release gates were not imported; the local scoped-check policy in the shared contract governs.
