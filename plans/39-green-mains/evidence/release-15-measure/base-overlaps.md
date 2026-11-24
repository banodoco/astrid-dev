# Plan 39 and Plan 91: base and overlap analysis (read-only)

Date of measurement: 24 November 2026 (the day of the repo fetches). Read-only: no checkout branch changed, nothing pushed, no workflow touched.

Heads used (fetched into refs, `origin/release/15/main`):
- astrid-runtime `release/15/main` = `24e2c929` (same as the 23 Nov measurement in plan39-audit.md)
- astrid-app `release/15/main` = `d53685f3` (same as the 24 Nov measurement in app-green/REPORT.md)
- astrid-agent `release/15/main` = `514499de`
- astrid-dev `origin/main` = `321523e5` for release/15 (fetched as `origin/main`)

Method: `git ls-remote origin 'refs/heads/release/*'` per repo; `git merge-base --is-ancestor` to decide "landed"; `git merge-tree --write-tree --name-only origin/release/15/main origin/<branch>` (git 2.43, exit 1 = conflicts); branch-own files = `git diff --name-only <merge-base> origin/<branch>`. Scripts: merge/run.sh, merge/mt.sh; raw outputs: merge/*.txt; file list: r15-unlanded-files.txt.

---

## 1. Remote branches and their merge-tree result against release/15/main

**Release 16 branches:** none exist yet in astrid-runtime, astrid-app or astrid-agent (`release/16/*` returns nothing). Confirmed by ls-remote.

### 1a. astrid-runtime (`release/15/plan-*`)

| Branch | Tip | Status vs release/15/main | merge-tree | Files the branch touches (class) |
|---|---|---|---|---|
| plan-69 | a2b017f1 | LANDED | n/a | none unlanded |
| plan-77 | 0dc004be | 35 ahead, 32 behind | **CONFLICT, 1 file**: `runtime_protocol/timeline_commit_store.py` | `runtime_protocol/{__init__,service,store,timeline_commit_port,timeline_commit_store,timeline_replay_identity,visual_boundary}.py` (timeline authority); `tests/test_v33_protected_acceptance.py` (v33; 3 Plan 39 failing IDs); `tests/test_timeline_commit_{ancestry,cost,port}.py`, `test_timeline_history_state.py`, `test_timeline_replay_checkpoint.py`, `test_commit_store_wal_guards.py`, `test_visual_legacy_r13_timing.py`. No CI, no pin. |
| plan-77-r7 | 8dfa96aa | 7 ahead, 30 behind | **CONFLICT, 4 files**: `runtime_protocol/service.py`, `store.py`, `timeline_commit_store.py`, `tests/test_timeline_verified_reads.py` (add/add) | `runtime_protocol/{door,server}.py`, `contract/extensions/timeline-verified-head-v1.yaml`. Timeline authority. |
| plan-77-save | bda91409 | LANDED | n/a | - |
| plan-81 | 72b129e5 | LANDED | n/a | - |
| plan-82 | 24e2c929 | same commit as main, LANDED | n/a | - |
| plan-87 | 84d47f0a | 7 ahead, 0 behind | clean | `runtime_protocol/{server,service}.py`; `tests/test_render_lease_policy_rn8.py`, `tests/test_runtime_request_timing.py`. Not in Plan 39's failing set. |
| plan-89 | 81f04492 | 19 ahead, 0 behind | clean (textually) | `runtime_protocol/v33_manifest.py` (U33 fingerprint, +28 lines), `timeline_commit_auth.py`, `timeline_commit_execution.py`, `history_guards.py`, `store.py`, `server.py`, `backup.py`, `cli.py`; `astrid_runtime/workspace.py`; ~25 tests incl. `tests/test_timeline_commit_acceptance.py` (12 Plan 39 failing IDs), `tests/test_timeline_commit_sequential_verifier.py` (33 IDs), `tests/test_timeline_recorder_abi_authority.py` (9 IDs), `tests/test_timeline_lock_placement_limits.py`. Timeline authority + v33 + Plan 39 failing tests. No CI, no pin. |

Runtime CI, pin and lock files: **no** unlanded `release/15/plan-*` Runtime branch touches `.github/`, `tests/astrid-agent.pin`, `tests/lanes.py` or any lock file.

### 1b. astrid-app (`release/15/plan-*`)

| Branch | Tip | Status | merge-tree | Files (class) |
|---|---|---|---|---|
| plan-69, plan-69-app-landing, plan-77-save, plan-77-tooling, plan-78-motion-pack-pin, plan-81-app-pin, plan-89 | various | LANDED (plan-89 tip = main `d53685f3`) | n/a | - |
| plan-77 | 5607d00f | 75 ahead, 67 behind | **CONFLICT, 8 files**: `public/install-manifest.json`, `runtime.lock.json`, `src/integrations/runtime/dataProvider.ts` and `.test.ts`, `src/tools/video-editor/commands/localSaveSession.ts`, `src/tools/video-editor/data/DataProvider.ts`, `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts`, `hooks/useTimelineSave.ts` | PINS: `public/install-manifest.json`, `runtime.lock.json` (Plan 39 PE1 reads the manifest for pins). SAVE PATH: the editor save code the three-products journeys drive. Also ~25 vitest files under `src/tools/video-editor/**`. No `.github/`, no `tests/e2e/`, no fake-runtime. |
| plan-77-quick-indicator | e6296b64 | 6 ahead | clean | `scripts/save-loop/*` only |
| plan-77-r7 | cfb894d | 6 ahead, 9 behind | **CONFLICT, 1 file**: `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts` | `src/integrations/runtime/{client,bootstrapInitialization,dataProvider}.ts`, `data/DataProvider.ts`, `data/shotCompositionAdapter.ts`, `hooks/useTimelineHistory.ts`, `hooks/useTimelineSave.ts` and tests |
| plan-84 | 95a061b3 | 5 ahead | clean | `src/pages/Home/**` (planet) only |
| plan-87 | 399addd5 | 4 ahead | clean | `config/vite/{appBuild,vite.config}.ts`, `src/tools/video-editor/lib/renderRouter.ts` |
| plan-88 | 0c6bda56 | 18 ahead, 6 behind | clean | `scripts/save-loop/film-*` only |

App CI, fake Runtime and three-products: **no** unlanded R15 App branch touches `.github/`, `tests/e2e/` (incl. `tests/e2e/fake-runtime/*` and `tests/e2e/local/three-products*.spec.ts`), `playwright*.config.ts` or `src/test/threeProductsAuthoring.test.ts`.

### 1c. astrid-agent (`release/15/plan-*`)

| Branch | Tip | Status | merge-tree | Files (class) |
|---|---|---|---|---|
| plan-13, plan-40, plan-69, plan-69-agent-landing, plan-77-save, plan-78, plan-81, plan-81-part2b, plan-88, plan-91 | - | LANDED. plan-91 tip = main `514499de` (no Plan 91 commits yet) | n/a | - |
| plan-56 | 3956bc41 | 89 ahead, 76 behind | **CONFLICT, 1 file**: `tests/test_windows_path_budget.py` | ~60 files: `astrid/core/generation/*`, `astrid/packs/runpod/{pins.json,recipe,environment,machine.py}`, `astrid/packs/vibecomfy/{pins.json,...}`, `astrid/core/execution/generic_host.py`, `tests/test_721_http_policy_guard.py`, `tests/test_windows_path_budget.py`. Pins: yes. Not a Plan 91 failing file. |
| plan-77 | fda01977 | 14 ahead, 326 behind | **CONFLICT, 4 files**: `astrid/resources/runtime.lock.json`, `runtime.lock.json`, `tests/test_vendor_lock.py`, `tests/test_windows_path_budget.py` | **CI**: `.github/workflows/ci.yml`, `.github/workflows/windows-journey.yml`; pins: both lock files, `astrid/packs/{runpod,vibecomfy}/pins.json`, recipes; tests incl. 8 Plan 91 failing files (`test_qwen_21_turbo.py`, `test_runpod_engine_selection.py`, `test_engine_custody.py`, `test_native_batch_ingress.py`, `test_managed_host_preparation.py`, `test_pinned_source_cpu.py`, `test_r14_builtin_transitions.py`, `test_installer_backup.py`). Timeline/render code: `astrid/core/timeline/*`, `astrid/sdk/timeline/commit.py`. |
| plan-77-r7 | b7f0e96a | 3 ahead, 321 behind | clean | `astrid/sdk/{_remote_timeline,remote,workspace_client}.py`, `astrid/sdk/timeline/store.py`, `tests/editing_conformance/test_verified_head_reader.py` |
| plan-82 | 69c34457 | 2 ahead | clean | `astrid/core/generation/cli.py`, `astrid/sdk/command_timing.py`, `tests/sdk/test_command_cache_events.py` |
| plan-87 | 1e34953f | 61 ahead, 76 behind | clean | `astrid/core/execution/generic_host.py`, `custody_broker.py`, `remotion_host_*`, `astrid/packs/rendering/**`, `remotion/package-lock.json`, many tests |
| plan-89 | e3da121f | 4 ahead, 69 behind | clean | `astrid/installer/{backend,core}.py`, `tests/test_installer_history_guard_rollback.py` |

Agent CI (Plan 91's territory): only plan-77 touches `.github/workflows/*`. Pins: plan-77 and plan-56 both touch pins and lock files.

### 1d. Summary of what is still unlanded and conflicting

- Runtime: plan-77 (1 file), plan-77-r7 (4 files). plan-87 and plan-89 merge cleanly but change Plan 39's failing test files.
- App: plan-77 (8 files, including both pins), plan-77-r7 (1 file).
- Agent: plan-56 (1 file, not a failing file), plan-77 (4 files, including CI and pins).
- The merge-tree results are against `release/15/main` today. The merge-base is old on several branches, so "behind" counts are large. A conflict set will change as those branches are merged up.

---

## 2. Active Release 15 and Release 16 plans that touch Runtime/App CI, the three-products spec, timeline authority, or pins

Source: astrid-dev `origin/main` `plans/index.md`, `releases/15.md`, `releases/16.md`, and each plan's `tasks.md`/`plan.md`.

### 2a. Plan 39 (R16, Runtime and App; Agent share moved to Plan 91 by D2)

Plan 39's own named files (`plans/39-green-mains/tasks.md`): Runtime `.github/workflows/ci.yml` (RE1, RE3, RE4 in `unit` and `sandbox-process-control`), `tests/astrid-agent.pin` (RE1, pin `0e1543e0`), `tests/lanes.py` (K1b quarantine, `MAX_DECLARED_XFAIL_TESTS = 20` at `tests/lanes.py:244`), `runtime_protocol/v33_manifest.py` (RT3, `_FINGERPRINTS` unchanged at tasks.md:110), `tests/test_v33_protected_acceptance.py`, `tests/test_timeline_clip_replacement.py` (RE2); App `.github/workflows/test.yml`, `lanes.yml`, `e2e.yml`, `config/testing/*`, `scripts/quality/check-known-failures.mjs`, `public/install-manifest.json` (PE1), `tests/e2e/local/three-products.spec.ts` (PT2, PT5), `tests/e2e/fake-runtime/*` (PT2: "fake Runtime routes").

Runtime CI as it is on `release/15/main` (verified): `.github/workflows/ci.yml` jobs at lines 22 `windows-realm-publication` (hard-coded `AGENT_SHA` at :38), 96 `unit`, 205 `darwin-native` (hard-coded `AGENT_SHA` at :227), 249 `typescript-client`, 261 `boundary`, 320 `sandbox-process-control`, 395 `portability-lifecycle`, 511 `landing-reference`.

### 2b. Plan 38 (R16): replaces the Runtime `darwin-native` job

Verified: `plans/38-one-process-identity/tasks.md:36` (row E1): "`.github/workflows/ci.yml` (`darwin-native` custody spawn becomes the `host-spawn` matrix on ubuntu, macos and windows; the hard-coded `AGENT_SHA` at `:31` and `:143` is replaced by `tests/astrid-agent.pin`), `tests/astrid-agent.pin` (to the Agent `int/38` head), `tests/test_installed_pack_custody_spawn.py` (its `darwin_native` mark, its xfail mark, and its `DeclaredXfail` entry in `tests/lanes.py` removed)".

Overlaps with Plan 39 (same files, both in Release 16):
- `.github/workflows/ci.yml` in Runtime: Plan 38 E1 replaces `darwin-native`; Plan 39 RE1/RE3/RE4 edit `unit` and `sandbox-process-control`. Plan 38's line numbers are stale: on `release/15/main` the hard-coded Agent SHAs are at `ci.yml:38` and `:227`, not `:31` and `:143`.
- `tests/astrid-agent.pin`: both plans rewrite its use (Plan 38 E1 sets it to the Agent `int/38` head; Plan 39 RE1 reads it).
- `tests/lanes.py`: Plan 38 removes one `DeclaredXfail` entry; Plan 39 K1b changes the quarantine ceiling (tasks.md:50, plan.md:97 "10", code 20).
- `tests/test_installed_pack_custody_spawn.py`: Plan 39 RT13 (tasks.md:123) also names it.

### 2c. Other R16 plans, per named file

| Plan (R16) | Runtime/App CI | Three-products | Timeline authority | Pins/locks | Overlap with Plan 39 |
|---|---|---|---|---|---|
| 63 Dependable saving | - | - | Yes: CC-4 commit route, CC-13/15/16 (`plans/63/tasks.md:16-24`), Runtime `tests/test_timeline_commit_*`, `tests/sdk/test_timeline_commit_provider.py` | `tests/astrid-agent.pin` (tasks.md:52) | Same Runtime `timeline_commit_*` tests as Plan 39's 54 failing IDs (plan-89 files) |
| 76 Editing together | - | - | Yes: ET-1 reads (`plans/76/tasks.md:14`), `tests/test_timeline_commit_integration.py` (tasks.md:36, :49) | - | `test_timeline_commit_integration.py` is in the Plan 89 branch (landed later) |
| 75 Fast saving | - | - | Yes: FS-5, CC-11 `BEFORE UPDATE/DELETE` triggers in the Runtime store (`plans/75/tasks.md:13-22`) | - | Runtime store (`timeline_commit_store.py`, `history_guards.py`) also edited by Plan 89 and Plan 77 |
| 18 Timeline editing (A) | - | - | Yes: TL-2 schema owner `contract/schemas/edit-command.json`, TL-3e, TL-13a `validate_final_candidate` (`plans/18/tasks.md:23-42`) | `tests/astrid-agent.pin` (tasks.md:79) | Contract files are not in Plan 39's list |
| 09 Install and update confidence | - | - | `tests/test_v33_historical_backup_restore.py`, `tests/test_native_custody.py`, `tests/test_role_custody_authority.py` (tasks.md:43-45) | `tests/test_runtime_upgrade.py` | Same v33 test family as Plan 39's `tests/test_v33_protected_acceptance.py` (3 IDs, plan-77) |
| 31 Releases from astrid-dev | App `.github/workflows/release-sync.yml`, `served-manifest-canary.yml` (RL-2c, RL-2d) | - | - | Manifest (`install-manifest.json`) | Plan 39 K4 waits on Plan 31 RL-1b (`scripts/release_record.py`, `docs.yml`) |
| 29 One update path | - | Ruling at `plans/29/tasks.md:30-31` names three-products test drift in the App | - | `astrid/resources/runtime.lock.json` vs root `runtime.lock.json` (plans/29/tasks.md:14) | Same App three-products and lock files |
| 30 Update everywhere | - | - | - | - | none |
| 13 Execution host | - | - | - | - | `generic_host.py` only (Agent) |
| 50 Recorded boundaries | - | - | - | VibeComfy pin ratchet and `models.lock.json` (RB-6, tasks.md:39) | Plan 39 K1b/quarantine rules in `tests/lanes.py` |
| 79 Local media | - | - | Runtime client (LM-1) | Agent pin | none |
| 92 Generate within a second | - | - | Runtime resident host | - | none |
| 72 Composable delivery | - | - | - | - | none |

### 2d. Active Release 15 plans (still unlanded) that touch the same files

| R15 plan | Overlap |
|---|---|
| Plan 77 (open; Runtime, App, Agent) | Runtime `timeline_commit_store.py`, `tests/test_v33_protected_acceptance.py`; App pins and the save path; Agent CI and pins. Listed in `plans/index.md:23` and `releases/15.md`. |
| Plan 89 (open; Runtime, App, Agent) | Runtime `v33_manifest.py` and the three timeline test files that are Plan 39 failing files (54 IDs). The App branch is landed, so it's Runtime only. Agent is installer only. |
| Plan 87 and 88 | No Runtime/App CI or pin overlap with Plan 39. Plan 88 touches App `scripts/save-loop/film-*` tests, not in Plan 39's list. |
| Plan 82, 84 | None. |

### 2e. Three-products spec

- App: `tests/e2e/local/three-products*.spec.ts`, `playwright.three-products.config.ts`, `src/test/threeProductsAuthoring.test.ts` (on `release/15/main`).
- Plan 39 PT2/PT5 name `tests/e2e/local/three-products.spec.ts` and the three-products journey (tasks.md:125, :128).
- No unlanded R15 branch touches those files. The App plan-77 branch changes the save code the journey drives (`localSaveSession.ts`, `useTimelineSave.ts`), so the journey's result may change when it lands. That is an inference, not measured.
- Plan 29 tasks.md:30-31 contains the three-products rulings (test drift), so Plan 29 and Plan 39 both touch the same test expectations.

---

## 3. Branch plan: cut, merge-up, land

### 3a. What the rules say (astrid-dev `origin/main`)

- `skills/shared/workstreams/astrid-dev-release/SKILL.md:35` "A plan branch ... and a fix branch ... are cut from the release branch's current head."
- Line 36: "Merge, never rebase or force-push."
- Line 42 (step 2): "Cut the release branch ... It is cut from the newest release branch still unpublished if there is one (fixes flow forward only), otherwise from the served release." For Release 16, the newest unpublished release branch is `release/15/main`, so `release/16/main` would be cut from `release/15/main`'s head (`24e2c929` for Runtime, `d53685f3` for App, `514499de` for Agent). Release 15 is not published.
- Line 43 (step 3): the plan manager cuts `release/<NN>/plan-<PP>` after the release branch is cut, from its current head.
- Line 46 (step 6): when the release branch moves, each manager merges it into open plan and fix branches promptly. A branch lands only when it contains the release branch's current head and its proof passed on the combined tree.
- Line 42 also: the release manager cuts the branch. `releases/16.md` says "Release manager: not yet named".
- `releases/16.md` Branches table (lines 47-93): every row is `not yet cut`. The file does not say when `release/16/main` is cut or from what. The Release 16 State is Draft.
- `skills/shared/run-contract.md:94`: "To bring in a newer base, merge it in."
- No rule found (grep over `skills/`, `releases/TEMPLATE.md`, `releases/16.md`, `plans/39-green-mains`, `plans/91-agent-main-green`, `plans/index.md`, `strategy.md`) that says whether a plan may be built ahead of its release's cut. The nearest rules are step 2 (release branch first) and step 3 (plan branch from the release branch's head). Release 15's plan branches were cut before the brief was final, so there is a practice, not a rule.

### 3b. Recommended plan (for the owner to confirm)

1. Cut `release/16/main` in each repo from the R15 heads, once a release manager is named (skill step 2). Record in `releases/16.md` Branches (`Cut at` = the commit).
2. Cut `release/16/plan-39` (Runtime, App; astrid-dev row kept) and `release/16/plan-91` (astrid-agent) from `release/16/main`, after step 1. If they must start before that, cut them from `release/15/main` now and record the Cut at commit. Then merge `release/16/main` in when it exists. That merge is the one step the skill requires, so it will be recorded.
3. Merge `release/15/main` into the plan branches regularly (the skill's step 6 applies to the release branch, and R15 moves daily; Plan 91's own inputs.md:117 already says "merge-tree against release/15/main" at dispatch).
4. Land into `release/16/main` only after the plan branch contains that head and its proof passes on the combined tree.

Open question for the owner: the skill says fixes "flow forward only", but it does not say whether merges into `release/15/main` after `release/16/main` is cut reach `release/16/main`. Plans 77, 89 and the R15 fix branches still land on R15 after Release 16 starts. Decide whether R16 takes them by a forward fix branch (`release/16/fix-*`) or by merging `release/15/main` in.

### 3c. Risks

- Runtime `release/15/plan-89` (clean merge, not landed) changes the three timeline test files that are 54 of Plan 39's Runtime failing IDs, and `v33_manifest.py`. Plan 39 fixes on those files cut from `release/15/main` today will conflict or double-fix when Plan 89 lands. Plan 39 should wait for Plan 89 to land, or merge `release/15/plan-89` in, before touching those files.
- Runtime `release/15/plan-77`: conflict in `timeline_commit_store.py` with main. Plan 39's `tests/test_v33_protected_acceptance.py` (3 IDs) is changed by plan-77.
- App `release/15/plan-77`: changes `runtime.lock.json` and `public/install-manifest.json` (both pins), and the App save path. Plan 39 PE1 and any pin change in Plan 39 conflict with it.
- Agent `release/15/plan-77`: changes `.github/workflows/ci.yml` and the pins. Plan 91 gate work edits the same workflow.
- Plan 38 and Plan 39 both edit Runtime `ci.yml`, `tests/astrid-agent.pin` and `tests/lanes.py` in Release 16. Sequence them, or assign one owner for those files.

---

## 4. Plan 91 is named Release 15 in astrid-dev: what must change for Release 16

Current state on `origin/main`: Plan 91 is in no release table. `releases/15.md` and `releases/15/run.md` do not mention Plan 91; `releases/16.md` does not include it. So the "move to Release 16" the owner made is not yet recorded in the repo. The lines below are the ones that still say Release 15 or `release/15/*` for Plan 91.

### 4a. `plans/91-agent-main-green/` (must change)

| file:line | text (abridged) | change |
|---|---|---|
| inputs.md:18 | "Plan 39 ... its [Release 15 ceiling]" | link text: Plan 39's ceiling heading is named Release 15 (`plans/39-green-mains/tasks.md:164`); rename only if the owner wants the Plan 39 heading renamed |
| inputs.md:51 | "Leaving the Agent in Plan 39. That plan is in no Release 15 lane" | Release 16 |
| inputs.md:71 | "once the owner places the plan in Release 15 (D1)" | Release 16 |
| inputs.md:72 | "merge cards into `release/15/plan-91`" | `release/16/plan-91` |
| inputs.md:81 | D1 "Release 15, as its own lane ... lands in `release/15/main` after RS1" | owner decision record: Release 16, `release/16/main` |
| inputs.md:87 | D7 "every completed `release/15/main` run" | `release/16/main` once cut |
| inputs.md:89 | D9 "the Release 15 Lead compares..." | Release 16 lead (not named) |
| inputs.md:94 | D14 "...the Release 15 baseline show..." | Keep: the baseline is R15 evidence; reword only if needed |
| inputs.md:95 | D15 "`release/15/main` keeps moving ... `release/15/plan-91`" | `release/16/...` |
| inputs.md:102 | "**Base choice.** The base is `release/15/main`, and the plan branch is `release/15/plan-91`" | `release/15/main` stays the start base; plan branch `release/16/plan-91` |
| inputs.md:103-117 | per-plan comparison of 24 Nov. Stale: Plan 88 is landed (agent `release/15/plan-88` is an ancestor of `release/15/main`); plan-56 now conflicts with main in `tests/test_windows_path_budget.py` (not a Plan 91 failing file); plan-77 conflict set changed (4 files, not the 8 listed) | rewrite the base-choice list from merge/ results |
| inputs.md:117 | "Plans added to Release 15 later ... `git merge-tree ... release/15/main release/15/plan-<PP>`" | Release 16 names |
| inputs.md:123 | "[Release 15 run board](../../../../releases/15/run.md)" | point at the Release 16 run board (not yet created) |
| plan.md:13 | "then a place in the Release 15 brief and a manager" | Release 16 brief |
| plan.md:23 | "green on `release/15/main`, and on `main` once Release 15 is published" | `release/16/main`; `main` after Release 16 is published |
| plan.md:29 | "Measured on `release/15/main` at `b324d7c1`" | keep as a measurement; say it is the R15 head |
| plan.md:39 | "Included: the Agent workflows on push to `main` and to `release/15/main`" | `release/16/main` |
| plan.md:46 | "Plan 39's [Release 15 ceiling]" | link text only |
| plan.md:60 | "Release 15 already compares each lane's unit results with a hosted baseline" | Keep the fact; the baseline is R15 evidence |
| plan.md:83 | "A pull request into `release/15/main` runs only fast checks" | `release/16/main` (or keep as R15 fact) |
| plan.md:85 | "Most `release/15/main` heads have no complete run" | R15 fact; keep, but AG-0 must now look at `release/16/main` |
| plan.md:92 | "Agent `release/15/main` at the head AG-0 records" | `release/16/main`, cut from `release/15/main` |
| plan.md:97 | "green Agent workflows on `release/15/main`" | `release/16/main` |
| plan.md:106 | "three full runs on one frozen head of `release/15/plan-91`" and "one run on `release/15/main`" | `release/16/plan-91`, `release/16/main` |
| plan.md:117 | "`main` turns green when Release 15 is published" | Release 16 |
| tasks.md:7 | "**Base:** `release/15/main`. The plan branch is `release/15/plan-91` in astrid-agent, cut at AG-0." | `release/16/plan-91`, cut now from `release/15/main` (`514499de`), see section 3 |
| tasks.md:21 | "dispatches both full workflows on `release/15/plan-91`" | `release/16/plan-91`; "same comparison ... on every completed `release/15/main` run" -> `release/16/main` |
| tasks.md:63 | "AG-0 Cut `release/15/plan-91` from the `release/15/main` head" | cut `release/16/plan-91` from `release/15/main`, or from `release/16/main` once cut |
| tasks.md:115 | "AG-10 Three green full runs ... on one frozen head of `release/15/plan-91`" and "one green run on `release/15/main`" | Release 16 names |
| tasks.md:129 | "The plan branch lands in `release/15/main` with the owner's go: once after RS1 ..." | `release/16/main` |

Note: astrid-agent `release/15/plan-91` exists at `514499de` (equal to `release/15/main`, no Plan 91 commits). It is a placeholder cut; it does not need to be changed. Leave it, or note it in the release record.

### 4b. `plans/index.md` (must change)

- `plans/index.md:28` (Plan 91 row, last cell): "then a place in the Release 15 brief and a manager" -> Release 16 brief and manager. The row's state (`queued`, Unassigned) stays.

### 4c. `releases/16.md` (must add; this is where the move becomes real)

- Add a line to `## Included plans` after the Plan 39 entry (`releases/16.md:36`): Plan 91, Agent main green (moved from Release 15 by the owner; not started).
- Add `astrid-agent | release/16/plan-91 | plan 91 | not yet cut | open` to `## Branches` (after the last row at `releases/16.md:93`).
- `releases/16.md:80` `astrid-agent release/16/plan-39` row: Plan 39 kept the Runtime and App only (D2, plans/91 inputs.md:81 and plans/39/tasks.md:166). Remove it unless a Plan 39 card needs the Agent, which D2 says it does not.
- `releases/16.md:36` Plan 39 description says "the release rule that every required check is green on each pinned commit": keep, and add that the Agent share is Plan 91.

### 4d. `releases/15.md` and `releases/15/run.md` (no change for Plan 91)

- `releases/15.md`: Plan 91 is not named. Line 27 lists the plans moved out of Release 15 on 23 November (63, 76, 18, 39, 50). Plan 91 is not on that list. Adding it is optional, for the record only.
- `releases/15/run.md`: no mention of Plan 91 (grep).

### 4e. `strategy.md` and `plans/priority.md` (no change needed)

- `strategy.md`: no mention of Plan 91 (grep "91", "agent main").
- `plans/priority.md:16` lists `91-agent-main-green` in the order list. Order is the owner's decision; no release name in the file.

### 4f. Plan 39 files that describe Plan 91 as Release 15 (should change with it)

- `plans/39-green-mains/tasks.md:166`: "the Agent packets moved to Release 15, are Plan 91's" -> Release 16.
- `plans/39-green-mains/tasks.md:164`: heading "Release 15 ceiling" (referenced by Plan 91 at plan.md:46 and inputs.md:18).
- `plans/39-green-mains/plan.md:21` and `:30`: say the Agent share moved to Plan 91 on 23 November. Correct as written; add the release.

---

## 5. Verified vs not verified

Verified in code or refs: branch lists; merge-tree results; branch-own file lists; landed status; Plan 38 E1 text (tasks.md:36); Runtime `ci.yml` job lines on `release/15/main`; plan-89's changes to `v33_manifest.py`; the release skill rules on cut and merge; `releases/16.md` table; Plan 91 references by file:line.

Not verified:
- CI status on the current heads (not run; the Plan 39 and App measurements are older logs, same heads).
- Whether the owner's move of Plan 91 to Release 16 is decided beyond the brief. Nothing in astrid-dev `origin/main` records it.
- Whether Plan 77 (R15) will land before R16 cut (it is open; its conflict set may change).
- Whether `release/16/main` should receive later R15 merges (skill is silent; see 3b).
- The "behind" counts on the agent and runtime branches are large (up to 326); the merge-base is old on several branches. The conflict lists are current against today's `release/15/main`, not the planned merge-up.
- The Plan 39 failing-ID overlaps (54 Runtime IDs in plan-89 files, 3 in plan-77) use `runtime-green/failing-ids.tsv` (measured 23 Nov at `24e2c929`, same head). App failing-test overlap was not computed per test; the App measurement is on E2E specs, which no unlanded R15 branch touches.
