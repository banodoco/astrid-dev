# Release 12 gate record

State: DRAFT, with no gate yet.

## Tuple

| Component | Full SHA / value |
|---|---|
| App | `{{FILL}}` (re-pin SHA) |
| Agent | `c5370a862d0b374afa412dd071418070e76f834c` |
| Runtime | `42ae24aff8d2cb854f874ce134161077a3ba3641` |
| harness (`harness/29-r12`) | `{{FILL}}` |
| VibeComfy | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` |
| ComfyUI (RunPod) | `ee71d5c4` — FULL SHA TO FILL |
| runpod-lifecycle | `f2948817eeb94af8dee76be21f6d673724f1606e` |
| Pinokio | `{{FILL}}` |
| OMP source | `https://github.com/banodoco/oh-my-pi` @ `78f0e0960f471c2c62b943272a48c33366f239fe` |
| Manifest sha256 | `{{FILL}}` |
| `public/install` sha256 | `{{FILL}}` |
| `public/install.sh` sha256 | `{{FILL}}` |
| `public/install.ps1` sha256 | `{{FILL}}` |

## Gate items

### 1. Matrix

Full `journey.yml` matrix, row=direct. All 11 rows must be green, including native Windows.

| # | Row | Run / result |
|---:|---|---|
| 1 | `{{FILL}}` | {{run link}} / {{result}} |
| 2 | `{{FILL}}` | {{run link}} / {{result}} |
| 3 | `{{FILL}}` | {{run link}} / {{result}} |
| 4 | `{{FILL}}` | {{run link}} / {{result}} |
| 5 | `{{FILL}}` | {{run link}} / {{result}} |
| 6 | `{{FILL}}` | {{run link}} / {{result}} |
| 7 | `{{FILL}}` | {{run link}} / {{result}} |
| 8 | `{{FILL}}` | {{run link}} / {{result}} |
| 9 | `{{FILL}}` | {{run link}} / {{result}} |
| 10 | `{{FILL}}` | {{run link}} / {{result}} |
| 11 | `{{FILL}}` | {{run link}} / {{result}} |

### 2. Agent CI

Frozen Agent run: [attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43085262585). Compare complete test IDs with [Release 10](https://github.com/banodoco/astrid-agent/actions/runs/43081197187) and [Release 11, attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43082578330), using `env/baseline-diff.py`. Check non-pytest jobs by name too.

- Bucket counts (regression, no-baseline, missing): `{{FILL}}`
- Rulings and unaddressed regressions: `{{FILL}}`

### 3. App Tests and Direct Journey

- App Tests run link and result/counts: `{{FILL}}`
- Direct Journey run link and result/counts (0 failures and no skipped tests, except listed expected failures): `{{FILL}}`

Named expected failures (approved by the orchestrator, registry `config/testing/direct-journey-expected-failures.json`):

- `id`: `P39-R12-DUP-SHOT`; `title`: `M2 native occurrence duplicate: lost ACK, Agent label, local label, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/249`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-EXT-BATCH`; `title`: `M2 ordinary extension batch: move and hold, Agent label, lost ACK, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/250`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-TASK-SWAP`; `title`: `render R, publish R+1 before it runs: the render is R's, it plays, and it is the film the App showed`; `issue`: `https://github.com/banodoco/astrid-app/issues/251`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-VIDEO-DROP`; `title`: `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`; `issue`: `https://github.com/banodoco/astrid-app/issues/252`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.

### 4. Review

- Agent candidate review range and verdict (no open blocker): `{{FILL}}`
- App candidate review range and verdict (no open blocker): `{{FILL}}`

### 5. Runtime

- `ci.yml` run on exactly `42ae24aff8d2cb854f874ce134161077a3ba3641`: [run 43116478710](https://github.com/banodoco/astrid-runtime/actions/runs/43116478710), failure. Its red jobs (unit ×2, portability-lifecycle ×2, sandbox-process-control) are red on Runtime main too; see the next line.
- By-test-ID comparison against Runtime main `4f5477cb0`, both with `-rA` ([base run 43116556369](https://github.com/banodoco/astrid-runtime/actions/runs/43116556369), [candidate run 43116561116](https://github.com/banodoco/astrid-runtime/actions/runs/43116561116)): **0 regressions**. No test that passed on main fails or errors on the candidate, in any of the 9 jobs. Recounted independently from the raw logs. Candidate failures (sandbox-process-control 1096, unit macOS 1083 and Linux 1087, portability-lifecycle 8 and 7) all fail on main too, and match the exact-SHA run ID for ID. Fixed by the candidate: windows-realm-publication and darwin-native go green; the darwin custody-spawn test goes FAILED → strict XFAIL (see Known issues).
- Orchestrator's independent review of `origin/main..42ae24aff8d2cb854f874ce134161077a3ba3641`: NO BLOCKER. Findings 1-4 are follow-ups and finding 5 is a pre-existing defect (see Known issues); rulings are in the decision log.
- Runtime main moves onto `42ae24aff8d2cb854f874ce134161077a3ba3641` at publish (33 commits; autostart update guard, Windows R0 handoff, windows-upgrade-unsupported, diagnostics).

## Not run / limits

- No GPU proof is part of this gate; generation, machine controls and GPU proof are outside Release 12.
- Editor data-loss fixes #252–#255 moved to Plan 39; their work in progress remains on branches.
- The Mypy gate stays red: the recorded counts are 2338 on the fixed candidate, 2325 on Release 10, and 2350 on Release 11/main. Refreshing the stale baseline is Plan 39 work.
- The R11 baseline comparison uses attempt 2 because unit shards 1 and 5 were cancelled in attempt 1 during a GitHub Actions outage; attempt 2 reran the failed and cancelled jobs on the same ref and code.
- The Windows Git-source repair evidence covers the five repair tests and `test_update_stages_recorded_git_from_restricted_service_environment`; the other installer-source cases noted in the decision log are pre-existing Plan 39 failures.
- A passing baseline comparison does not establish parity for missing or uncollected tests; non-pytest jobs also require review by name.

## Known issues shipped

- [#249](https://github.com/banodoco/astrid-app/issues/249): “Duplicate shot” fails with an error.
- [#250](https://github.com/banodoco/astrid-app/issues/250): the ordinary extension batch journey remains a known failure.
- [#251](https://github.com/banodoco/astrid-app/issues/251): the Agent cannot swap a generic task output into a timeline and commit it.
- [#252](https://github.com/banodoco/astrid-app/issues/252): a video dropped onto the timeline appears on screen but is not saved and is gone after reload.
- [#253](https://github.com/banodoco/astrid-app/issues/253): after a refused edit, later edits in the same session are refused too.
- [#254](https://github.com/banodoco/astrid-app/issues/254): the recovery “Save them” action is a Plan 39 issue.
- [#255](https://github.com/banodoco/astrid-app/issues/255): an upload in progress is lost at reload.
- Installed-pair source closure (Plan 38, already shipped in R10 and R11): on a shipped install, the Agent and Runtime measure different source-closure digests, so a host-only custody spawn of an installed pack is refused as “differs from original launch”. R12 pins it with the strict Runtime xfail `installed-pair-source-closure` (darwin lane) and leaves the code unchanged.

## Publication steps (prepared, not run)

Publishing follows the legacy path: Agent main, then Runtime main, then App main. The App merge triggers the Railway production deploy.

### Agent

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main c5370a862d0b374afa412dd071418070e76f834c && echo ok`
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-agent.git c5370a862d0b374afa412dd071418070e76f834c:refs/heads/main`
- Expected `main` SHA afterwards: `c5370a862d0b374afa412dd071418070e76f834c`.

### Runtime

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main 42ae24aff8d2cb854f874ce134161077a3ba3641 && echo ok`
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-runtime.git 42ae24aff8d2cb854f874ce134161077a3ba3641:refs/heads/main`
- Expected `main` SHA afterwards: `42ae24aff8d2cb854f874ce134161077a3ba3641`.

### App

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main {{APP_FROZEN_SHA}} && echo ok`
- Confirm the re-pinned manifest raises release 11 to 12 in the same change as the tuple with `node scripts/installer/release-guard.mjs origin/main HEAD --pins`.
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-app.git {{APP_FROZEN_SHA}}:refs/heads/main`
- Expected `main` SHA afterwards: `{{APP_FROZEN_SHA}}`.

### Post-check

- Check the served release and tuple: `curl -sS https://astrid.haus/install-manifest.json | jq '{release, agent: .agent.sha, runtime: .runtime.sha}'`. Expect release `12`, Agent `c5370a862d0b374afa412dd071418070e76f834c`, and Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`.
- Check the served body hash: `curl -sS https://astrid.haus/install-manifest.json | sha256sum`; expect `{{manifest sha256}}`.
- Check the served-manifest canary; it is being diagnosed.

If an agent session cannot merge to production because of permission or classifier refusal, Hannah runs the same three pushes, or merges the equivalent fast-forward PRs (`cand/29-r12` → `main`) in the GitHub UI, in the same order, then runs the post-check.
