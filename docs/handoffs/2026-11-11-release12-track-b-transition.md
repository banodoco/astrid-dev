# Release 12 Track B — manager transition

This is a transition snapshot, not a freeze or acceptance. Read [Release 12](../../releases/12.md), [Track B](../../releases/12/generation.md), the owning plans' task records, and the applicable skills before acting. The orchestrator owns cross-track coordination and named paid authorization. Confirm every remote ref before use; do not depend on a previous worker or local process surviving a handoff.

## Verified work-in-progress refs

| Repository and branch | Full SHA | Status |
|---|---|---|
| Agent `release12/gen-candidate` | `1439ccc63bf8d9ed5422ac1f95ffdd6158560e1e` | Pushed B5 WIP, not `B-CANDIDATE`; merge parents are `6a2351d95bb7eabc8b0ff6f988163fe420fcb3d7` and `e1731b9e4e86638e6425cf5601160e32be683a72`. |
| Agent `plan32/r12-error-contract` | `e1731b9e4e86638e6425cf5601160e32be683a72` | Reviewed handoff integrated into B5 WIP. |
| Agent `handoff/r12-retention-fingerprint` | `6dbe7f9aefc7d2ee6004787c5fe269644fcf9a49` | Divergent, unaccepted WIP; safety controls and independent final review remain incomplete. Do not silently integrate it. |
| Agent `handoff/r12-tts-cpu-assert-stages` | `adfe6904dd7e4d2030d4d94768c59e53fd9ff466` | Synthetic diagnostic tests only, not candidate code or live proof. |
| Runtime `handoff/r12-self-observe` | `8b312c4b29bbb4fef5ac0849188678fe356b9e84` | Reviewed provisional Runtime handoff; final pin requires freeze coordination. |
| App `handoff/r12-provisional-tts-e173` | `c1dd6104df78f2849404ab1261d1ff628872aa54` | Provisional diagnostic manifest handoff, not an accepted App candidate or final tuple. |

P40-T9's accepted focused handoff is Agent `plan40/staging-int40` `d8931c281cf705273c3c7c01346b6f2722733cca`; this does not itself complete the remaining P40 acceptance rows. The [B5 focused CPU receipt](../../plans/32-generation-placement-targets/evidence/release12-b5-focused-cpu.md) records the exact merge-head checks, corrected Runtime import and proof limits. R12-F1's R10 structural comparison is recorded in [Plan 32](../../plans/32-generation-placement-targets/tasks.md); it is not live H3 qualification or a waiver of other candidate regressions.

## Gates and handoff priorities

- No `B-CANDIDATE`, `FINAL-B7` or `FINAL-TUPLE` has been accepted. Finish the remaining B5 proof and dispositions; final App integration waits for the exact accepted `A-FROZEN` input. B8, B9 and final qualification retain their recorded dependencies and release rules.
- The retention WIP models verified current receipt compatibility under the existing custody boundary; it has not established the cause of a previous live release. Review and prove remaining candidate-bearing fencing, raw receipt validation, reset, and legacy controls before considering integration. Never accept unknown custody or weaken expiry, idle or explicit release.
- Synthetic shipped/direct TTS checks use fake transport and a historical pinned schema. They do not establish live schema or engine behavior. Do not label a generic failure as a specific cause without evidence.
- Before any paid operation, obtain the orchestrator's named authorization and the owner's applicable consent; verify exact inputs, current provider census, budget and custody. Follow the release's GPU-model restriction and shared spend/idle rules. P34 must supervise continuously and confirm exact release and a post-run census. No scheduler or chat wake-up is a paid-resource safety mechanism.
- A previous attempt to publish a separate GPU evidence record was rejected by automatic approval review. Do not retry, route around the rejection, or reproduce its rejected content elsewhere; the orchestrator owns the disclosure decision.

## Portable setup and evidence limits

Use fresh dedicated checkouts at the full SHAs above. Prepare a project-compatible Python environment and pinned Runtime, VibeComfy and lifecycle sources from the repository instructions; verify `git rev-parse HEAD`, clean state and Python import origins before tests. The Runtime checkout must be present on Python's startup import path when the relevant tests import it before fixture setup. Coordinate an exclusive shared-host test window with the orchestrator and Track A; run only the authorized focused selectors and preserve exit receipts. Do not use local shell history or another agent's worktree as an inbox.

The RunPod credential is supplied through the supported private credential mechanism; environment-variable name `RUNPOD_API_KEY` is not a credential value. Never print, persist in logs, or pass a secret in command arguments. Use only the permitted lifecycle/Astrid provider interfaces, except the owner-authorized read-only billing view described in the session. Recheck authorization, account state and custody at the time of use.

Some original command logs and synthetic runners remain local and may not survive the environment. The local runners have workspace-specific paths and inherit their caller's environment; they are not portable release artifacts. The linked B5 receipt preserves selectors, source revisions, outcomes and hashes of its local receipts, not the raw logs. Recreate or improve a sanitized, environment-allowlisted harness if further reproduction is needed; do not assume those local files exist.
