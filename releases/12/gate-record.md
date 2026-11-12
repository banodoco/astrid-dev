# Release 12 gate record

State: **GATE-GREEN** (12 Nov 04:31Z). Every gate item below is green or ruled on the frozen tuple; A-FROZEN at the same time.

## Tuple

| Component | Full SHA / value |
|---|---|
| App | `237b28be935af49c23464fa6ca1cf30db67ebaa0` (re-pin commit on `scratch/r12-app-int`) |
| Agent | `0e1543e0da2215db9cb3320cfd1083174c3c62a9` (`cand/29-r12`) |
| Runtime | `42ae24aff8d2cb854f874ce134161077a3ba3641` |
| harness (`harness/29-r12`) | `1940a2fe1` (full SHA in the matrix run) |
| VibeComfy | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` |
| ComfyUI (RunPod) | `ee71d5c4993f29086b27fde1629a945ae48425bf` (from `astrid/packs/runpod/pins.json` at `0e1543e0`) |
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

Frozen Agent run: [43134432721](https://github.com/banodoco/astrid-agent/actions/runs/43134432721) on `0e1543e0` (attempt 1; attempt 2 re-ran the failed jobs for one ID, see below). The full by-ID comparison was done on the previous candidate `c5370a86` ([43085262585](https://github.com/banodoco/astrid-agent/actions/runs/43085262585) attempt 2) against [Release 10](https://github.com/banodoco/astrid-agent/actions/runs/43081197187) and [Release 11, attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43082578330) (`env/baseline-diff.py`, -rA). The final candidate is ruled as a **delta** against `c5370a86` (owner's path, 12 Nov).

- Bucket counts on `c5370a86` (regression, no-baseline, missing): 153 / 131 real (143 raw) / 315. Pre-existing 815, fixed 45.
- Rulings:
  - **89 of the 153** passed only on R10 and **all also fail on R11**. They were introduced by R11, which is shipped, so they are not R12-caused and are left untouched (recorded).
  - **64 passed on R11 and failed on `c5370a86`.** The R12-introduced product regressions among them were fixed in `0e1543e0`: the `text` alias refused by schema lookup, add_text needing an optional pack, the pack recovery command (including `astrid packs` on the installed command), and the core pack-boundary ratchet. Also fixed: the test fixtures and teardown leaks those changes exposed.
  - **Delta `0e1543e0` against `c5370a86`:**
    - **60 of the 64 now pass.** Of the 4 left, 3 (`test_installer_platforms` no-systemd cases) also fail on R10, so they're pre-existing against R10. The fourth, `test_parent_clips::test_edit_on_a_mixed_timeline_edits_whichever_matched`, is test drift. It edits an `am-sprite` clip without the motion pack in that test's inventory, and the intended fail-closed refusal fires, printing the working install command. The fixture scope missed this file. Known issue; Plan 39.
    - **New failing IDs (passed on `c5370a86`): 1.** `tests/packs/test_audio_render.py::AudioRenderTest::test_rendered_mp4_contains_audio_stream` (darwin/Remotion lane): "candidate reconciliation deadline expired acquiring custody lock". The fix round changes no execution or custody code. Its render edits (`remotion/run.py`, `storage.py`, `managed_timeline.py`, `_effect_registry.py`) only route alias maps through `clip_type_aliases`. **Attempt 2: PASSED.** In the same attempt `tests/packs/test_text_card_render.py::TextCardRenderTest::test_text_card_render_smoke`, which passed in attempt 1, failed with the identical custody-lock error. **Ruling: an intermittent pre-existing timing flake, not a regression.**
      - The raising code, `_observation_guard` in `astrid/core/execution/custody_broker.py`, is darwin-only and deadline-based. It shipped in R11 (`62dbe56ea`) and is byte-identical in R11 `a105de3a4`, `c5370a86` and `0e1543e0`.
      - Of 22 darwin jobs scanned since 9 Nov, 4 hit this error, each on exactly one test: `87d1fbbc4` (R12 lineage, before the fix round; the same `test_text_card_render_smoke`), an R13 rehearsal `bf3b6ba77` (a `test_process_group` test), and `0e1543e0` attempts 1 and 2 (a different render test each time).
      - Every affected ID passes on another attempt on the same SHA.
      - Recorded as a known issue; Plan 39.
    - **Coverage:** unit shard 5 was cancelled at the 2 h job limit, so 90 of `c5370a86`'s IDs have no CI result. They were run locally on both commits, with identical results (56 passed, 13 failed, 21 skipped) and no ID passing on the old candidate and failing on the new one. A local run is not CI-equivalent; recorded as such.
  - **No-baseline (131):** 115 are in shard 1, which has no baseline on any side. A local R11-against-candidate baseline showed them failing identically on R11, apart from one R12 teardown leak (fixed) and the new `test_windows_publish` (fixed).
  - **Non-pytest jobs:**
    - boundary, both release wheels and windows-native-and-installer pass.
    - `fast checks` is red at the mypy baseline gate. The count is identical on `c5370a86` and `0e1543e0` (current 2338 against baseline 2192), so the fix round adds 0 findings. The baseline is stale (Plan 39 AT2).
    - darwin native: the same failures as R11, plus one custody-lock flake per attempt (above). Attempt 2 also re-ran unit shard 7: 93 failing IDs, all failing in attempt 1 too, so 0 new. The other attempt-2 shard reruns are re-checks of IDs already ruled in attempt 1; any result arriving after the gate goes in the decision log.

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
- App candidate review range and verdict (no open blocker): the R12 App delta was reviewed earlier (orchestrator-commissioned review of the App delta; see the decision log). Follow-ups after it were reviewed by independent read-only Astra reviewers: `2dc109bcc..ed9327947` BLOCKER ×2 → fixed `9afd4aaa6`, re-review NO BLOCKER; the VIDEO-DROP marker `48ec9bb70` BLOCKER → corrected `ebfc9a1b7`, second review NO BLOCKER. Later commits are test-only or mechanical, read by the manager under the owner's speed rule 3: `d31b976e1`, `7a971cea5`, `d9e2798d4`. Also the two App main merges (`acfe70e7b` and `3e53462f4`, already on main), the owner-requested copy change `d3e81f98e`, and the re-pin `237b28be9`. No blocker is open.

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
- Darwin custody-lock flake (pre-existing since R11 code `62dbe56ea`): on macOS, about 1 in 5 CI darwin jobs loses one render or process-group test to "candidate reconciliation deadline expired acquiring custody lock". It passes on rerun. Plan 39.
- `tests/packs/timeline/test_parent_clips.py::test_edit_on_a_mixed_timeline_edits_whichever_matched` fails: test drift. The motion-fixture scope missed this file; the product's fail-closed refusal is correct. Plan 39.
- Matrix `direct-linux-fresh` once showed the generic "Astrid updated. Reload to continue." in place of the release-transition line (shakedown on `8f1a19086`; green on the frozen tuple). Intermittent wording; Plan 39.

## Publication steps (prepared, not run)

Publishing follows the legacy path: Agent main, then Runtime main, then App main. The App merge triggers the Railway production deploy.

**Branch protection and preconditions** (checked 12 Nov ~00:20Z; raw: decision log):
- `main` on astrid-agent, astrid-runtime and astrid-app reports `protected: false`, with required status checks off and no contexts (unauthenticated `/branches/main`). `/branches/main/protection` returns 404 without admin access, so rulesets could not be read. No CODEOWNERS or settings files exist in any of the three repos.
- Each push is a fast-forward, which requires the current `main` to be an ancestor of the pushed SHA. Main heads re-checked 12 Nov ~03:55Z: Agent `a105de3a4` (R11), Runtime `4f5477cb0`, App `3e53462f4`. All three fast-forward to the frozen SHAs (`merge-base --is-ancestor` ok). App main moved past the `6545f130` cut-off twice (acfe70e7b at 23:25Z, then the last tour push 3e53462f4). Both are merged into the candidate, and App main has been held since 3e53462f4 (orchestrator, 00:33Z).
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
- Check the served body hash: `curl -sS https://astrid.haus/install-manifest.json | sha256sum`; expect `1f3cd5b0b06579a035adf42e62e953edca07042554fd7e8af6f357a3e0bc69f1`.
- Check the served-manifest canary. An earlier ruling found it fine; the vision job's Chromium install is a follow-up.

If an agent session cannot merge to production because of permission or classifier refusal, Hannah runs the same three pushes, or merges the equivalent fast-forward PRs (`cand/29-r12` → `main`) in the GitHub UI, in the same order, then runs the post-check.
