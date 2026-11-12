# Release 12 gate record

State: DRAFT. Qualifying window started 12 Nov ~01:25Z on the tuple below; results pending.

## Tuple

| Component | Full SHA / value |
|---|---|
| App | `237b28be935af49c23464fa6ca1cf30db67ebaa0` (re-pin commit on `scratch/r12-app-int`) |
| Agent | `0e1543e0da2215db9cb3320cfd1083174c3c62a9` (`cand/29-r12`) |
| Runtime | `42ae24aff8d2cb854f874ce134161077a3ba3641` |
| harness (`harness/29-r12`) | `1940a2fe1` (full SHA in the matrix run) |
| VibeComfy | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` |
| ComfyUI (RunPod) | `ee71d5c4` — FULL SHA TO FILL |
| runpod-lifecycle | `f2948817eeb94af8dee76be21f6d673724f1606e` |
| Pinokio | `d15c58b5cd1f7e24c1e699340b33961027f7c573` (int/r1 fallback; Pinokio rows are deferred, direct_only) |
| OMP source | `https://github.com/banodoco/oh-my-pi` @ `78f0e0960f471c2c62b943272a48c33366f239fe` |
| Manifest sha256 | `1f3cd5b0b06579a035adf42e62e953edca07042554fd7e8af6f357a3e0bc69f1` |
| `public/install` sha256 | `c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff` |
| `public/install.sh` sha256 | `591c4c51b148fccef2a7d1c45782d9ff949d5fd03d46cd82b5591e3a23d1b285` |
| `public/install.ps1` sha256 | `ea581d5d7c2d02f9f062dc15affabe1f7c3e38d641984cecf4797f13ac58b3a9` |

## Gate items

### 1. Matrix

Full `journey.yml` matrix, row=direct. All 11 rows must be green, including native Windows.

Run [43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) on harness `harness/29-r12` `1940a2fe11d8b131320dcf1c32dcfb69af288aef` with exactly the frozen tuple. All 11 rows are green, and "Journey evidence (exact tuple)": PASS ("All required scenarios and candidate identity verified"). In the earlier shakedown on `8f1a19086`, direct-linux-fresh once showed only the generic "Astrid updated. Reload to continue." rather than the release-transition line (see Known issues).

| # | Row | Run / result |
|---:|---|---|
| 1 | `direct-linux (r0-handoff-then-update)` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 2 | `direct-macos (r0-handoff-then-update)` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 3 | `direct-windows (fresh-install, native)` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 4 | `direct-linux-fresh` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 5 | `direct-macos-fresh` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 6 | `direct-linux-r9-install` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 7 | `direct-macos-r9-install` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 8 | `direct-linux-r11-update` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 9 | `direct-macos-r11-update` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 10 | `direct-linux-autostart-off` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |
| 11 | `direct-macos-autostart-off` | [run 43134528275](https://github.com/banodoco/astrid-agent/actions/runs/43134528275) / success |

### 2. Agent CI

Frozen Agent run: [attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43085262585). Compare complete test IDs with [Release 10](https://github.com/banodoco/astrid-agent/actions/runs/43081197187) and [Release 11, attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43082578330), using `env/baseline-diff.py`. Check non-pytest jobs by name too.

- Bucket counts (regression, no-baseline, missing): `{{FILL}}`
- Rulings and unaddressed regressions: `{{FILL}}`

### 3. App Tests and Direct Journey

- App Tests: [run 43134514508](https://github.com/banodoco/astrid-app/actions/runs/43134514508) on `237b28be9`: success. vitest (npm test and sdk-boundary), boundary (vendor locks against the pinned Agent and Runtime) and release-tooling-macos all pass.
- Direct Journey: [run 43134521115](https://github.com/banodoco/astrid-app/actions/runs/43134521115) on `237b28be9`: success. `direct-journey` 45 passed, 0 skipped. `three-products` 14 tests: 10 passed and exactly the 4 listed expected failures failed (P39-R12-EXT-BATCH, P39-R12-VIDEO-DROP, P39-R12-DUP-SHOT, P39-R12-TASK-SWAP); 0 unexpected, 0 flaky, 0 skipped, 0 not run.

Named expected failures (approved by the orchestrator, registry `config/testing/direct-journey-expected-failures.json`):

- `id`: `P39-R12-DUP-SHOT`; `title`: `M2 native occurrence duplicate: lost ACK, Agent label, local label, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/249`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-EXT-BATCH`; `title`: `M2 ordinary extension batch: move and hold, Agent label, lost ACK, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/250`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-TASK-SWAP`; `title`: `render R, publish R+1 before it runs: the render is R's, it plays, and it is the film the App showed`; `issue`: `https://github.com/banodoco/astrid-app/issues/251`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-VIDEO-DROP`; `title`: `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`; `issue`: `https://github.com/banodoco/astrid-app/issues/252`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.

### 4. Review

- Agent candidate review range and verdict (no open blocker): the R12 fix round `c5370a86..0e1543e0` (merge of `r12/fix-round`) was reviewed commit by commit by independent read-only Astra reviewers: `a17e0555a` BLOCKER (recovery command) → fixed `cef4c2850`; `abd1886ee` NO BLOCKER (MEDIUM fixed `dc87e6230`); `abd1886ee..cef4c2850` BLOCKER (installed `astrid` lacked `packs`) → fixed `cafa71487`; `cafa71487` NO BLOCKER. Test-only commits were read by the manager. No blocker is open. The candidate's earlier range (`origin/main..c5370a86`) was reviewed before this round (see the decision log).
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

**Branch protection and preconditions** (checked 12 Nov ~00:20Z; raw: decision log):
- `main` on astrid-agent, astrid-runtime and astrid-app reports `protected: false`, with required status checks off and no contexts (unauthenticated `/branches/main`). `/branches/main/protection` returns 404 without admin access, so rulesets could not be read. No CODEOWNERS or settings files exist in any of the three repos.
- Each push is a fast-forward, which requires the current `main` to be an ancestor of the pushed SHA. Main heads when checked: Agent `a105de3a4852cb61b9647dfe2c920118bd29f272` (R11), Runtime `4f5477cb0f5b03d28bec991a1fe34edcd8fc309f`, App `acfe70e7b56e0efe14ef2bbb977cb8aaa08d1e1a`. App main moved past the `6545f130` cut-off (acfe70e7b, an onboarding tour change at 23:25Z on 11 Nov). It is merged into the candidate, and the orchestrator is asked to hold App main still until publication.
- Before each push, check: `git merge-base --is-ancestor origin/main <SHA>`. If it fails, stop: main moved again, and the candidate must merge it and requalify.

### Agent

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main 0e1543e0da2215db9cb3320cfd1083174c3c62a9 && echo ok`
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-agent.git 0e1543e0da2215db9cb3320cfd1083174c3c62a9:refs/heads/main`
- Expected `main` SHA afterwards: `0e1543e0da2215db9cb3320cfd1083174c3c62a9`.

### Runtime

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main 42ae24aff8d2cb854f874ce134161077a3ba3641 && echo ok`
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-runtime.git 42ae24aff8d2cb854f874ce134161077a3ba3641:refs/heads/main`
- Expected `main` SHA afterwards: `42ae24aff8d2cb854f874ce134161077a3ba3641`.

### App

- Pre-check: `git fetch origin main && git merge-base --is-ancestor origin/main 237b28be935af49c23464fa6ca1cf30db67ebaa0 && echo ok`
- Confirm the re-pinned manifest raises release 11 to 12 in the same change as the tuple with `node scripts/installer/release-guard.mjs origin/main HEAD --pins`.
- Publish (fast-forward push only; never `--force`): `git push https://github.com/banodoco/astrid-app.git 237b28be935af49c23464fa6ca1cf30db67ebaa0:refs/heads/main`
- Expected `main` SHA afterwards: `237b28be935af49c23464fa6ca1cf30db67ebaa0`.

### Post-check

- Check the served release and tuple: `curl -sS https://astrid.haus/install-manifest.json | jq '{release, agent: .agent.sha, runtime: .runtime.sha}'`. Expect release `12`, Agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`, and Runtime `42ae24aff8d2cb854f874ce134161077a3ba3641`.
- Check the served body hash: `curl -sS https://astrid.haus/install-manifest.json | sha256sum`; expect `{{manifest sha256}}`.
- Check the served-manifest canary; it is being diagnosed.

If an agent session cannot merge to production because of permission or classifier refusal, Hannah runs the same three pushes, or merges the equivalent fast-forward PRs (`cand/29-r12` → `main`) in the GitHub UI, in the same order, then runs the post-check.
