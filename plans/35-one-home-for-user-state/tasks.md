# Tasks: one home for user state

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft outline only; not executable assignments.** Scope tasks after current-source inspection. The audit in [inputs.md](inputs.md) is code-read and must be re-verified.

## Task index

| Work area | Route | Depends on | Progress |
|---|---|---|---|
| [Verify the audit and fix the keep list](#intended-work-and-proof) | TBD | Plan 32 T6d (the settings document's shape) | Superseded by the [28 November reconciliation](#release-16-reconciliation-28-november-2026); CPU part [x] merged |

## Intended work and proof

- Re-verify each MOVE and KEEP row against current source, and record the result in inputs.md.
- App: project selection through `/v1/projects/selection`; extension settings through app-state `ext.*`, with one store; project work in `project_documents`.
- Agent: the skills, pack-disable, compute-profile and prompt-toggle choices in app-state.
- RunPod lease state in the remote activation record.
- An import from each old location, run once.
- The check that flags new side stores.
- Proof for each move: a test that the value survives a new browser or device profile and a Runtime backup and restore.
- **Set a removal date for the VibeComfy TOML import** (`astrid/core/generation/settings.py:193-231`; a reasonable one-time migration, so keep it until then). Route N, Low. Source: Plan 32 review, 9 Nov, at 7209ffcc7.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

The following proposed S35-0–6 rows are uncompleted; the earlier outline is retained as history:

| New proposed row | Owner, outcome and dependency |
| --- | --- |
| S35-0 | P35 census: all readers/writers/boot/recovery roots, actual old origins and size limits, accepted and pending unique work. Starts now. |
| S35-1 | P35 + Runtime/App versioned state identity/conflict/migration receipt and old-client/rollback contract. Consume S35-0's relevant objects, not wait every inventory item. |
| S35-2 | App + Runtime durable choices/work migration after S35-1; separate project/view/personal state; retain drafts and explicit defaults, fresh-profile/restore proof. |
| S35-3 | Agent portable skill/pack opt-outs and compute-choice migration after S35-1; preserve machine bootstrap and environment overrides; parallel with S35-2. |
| S35-4 | Runtime protected grant/revoke schema and bounded credential-reference seam with P90/P36/P38. Design alongside S35-1, publish minimal seam before TR-1; no whole S35-2/3 gate. |
| S35-5 | P35/P38 custody-phase classification and narrow gap repair; local receipt/lock/journal keep-list. Parallel contract work; do not move acquisition authority to activation blindly. |
| S35-6 | P35 + integration owners: exact migrated candidate, stale client, interrupted/repeated copy, direct/Pinokio native support, accepted/pending work, revoke/restore and rollback/retry. After affected S35 rows and consuming seams; joins final go. |

No general store/API cleanup, broad P36 consolidation or P12/P75 architecture is required for parallel starts. Evidence: [SC-35](https://github.com/banodoco/astrid-dev/blob/44d813650b7e8b3726bd41699e80c182db8f79a1/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35.md), [SC-35-severity-correction-01](https://github.com/banodoco/astrid-dev/blob/ebe295571bb58028fe72d98c3da2cbe7fd40eaa5/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35-severity-correction-01.md), [INV-04](https://github.com/banodoco/astrid-dev/blob/9e8411372fc9a0257175d0f49da65ba7bee77bbb/releases/16/evidence/scoping/INV-04.md), [AUD-01](https://github.com/banodoco/astrid-dev/blob/43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b/releases/16/evidence/scoping/AUD-01.md).

## Prepared Release 16 queue — completed 26 November 2026

The [Lead's terminal receipt](https://github.com/banodoco/astrid-dev/issues/2030#issuecomment-7191806062) confirms 11 done, zero parked and the accepted work merged into Agent and Runtime `release/16/main`. The [Plan 35 board](https://github.com/banodoco/astrid-dev/issues/2033) records DONE for R16-P35-01–09, RS1 and R. The final Agent review merge `f59cc40cba7f25872def3be4603fd78a10bf1431` and Runtime review merge `c7019b00f270a1cb173d9e4f0bf9852c95a3147c` are ancestors of their current release integration heads (verified 27 November). This completes the bounded CPU packet queue, not the full project, the deferred rows below, or final installed/native release qualification. No new product proof was executed for this record update.

## Later: real-hardware qualification (not in Release 16)

Owner, 26 November 2026: done separately, later. Not part of this plan's Release 16 run.

These rows need a real machine, an install of the App's dependencies, native Pinokio, a paid RunPod account, or another plan's unfinished work, so no ChatGPT chat without a network can prove them. Release 16 packets for the rest are in `releases/16/packets/R16-P35-*.md`.

| Row | What is left | Why it is not a Release 16 packet |
| --- | --- | --- |
| S35-2, App part | Last-opened project through `/v1/projects/selection` instead of localStorage `lastSelectedProjectId` and app-state `ui.preferences.lastOpenedProjectId` (`useProjectSelection.ts`, `projectSelectionStore.ts`); the `astrid.extension-state` IndexedDB and `astrid.ext.state.*` repository (`extensionStateRepositoryProvider.ts`, `extensionStateRepositoryIndexedDB.ts`; extension settings already go through the settings store at base, `extensionSettingsBacking.ts`); hidden shots, inpaint strokes, effect drafts and pending join clips into `project_documents` (`useHiddenShots.ts`, `useStrokePersistence.ts`, `effect-store.ts`, `useJoinClips.ts`, `clipPendingActions.ts`); last-used generation settings removed in favour of the latest generation's task spec (`useShotSettings.ts`, `useJoinSegmentsSettings.ts`, `useLastUsedEditSettings.ts`); the `project`, `draft` and `boot` scopes of `settingsStore.ts` and the lint that bans raw browser storage. The Runtime needs no change: `project_documents` takes any non-reserved kind and the task resource already returns its `spec`. | The App's tests run on vitest, which needs `npm install`; a chat has no network and no `node_modules`, so no App change has a runnable proof. |
| S35-3, pack opt-outs | The `disabled` list in `pack-sources.json` (`core/pack/source_setup.py`: `active_sources`, `inventory_report`, `provision(disable_pack=...)`). | `core/execution/custody_broker.py::_inventory_launch_policy` reads that file before the Runtime exists and pins its SHA-256 for custody; moving one field changes Plan 38's launch policy. Plan 38 runs after Plan 35. Revisit with Plan 38's owner. |
| S35-3 and S35-5, RunPod lease | `<data_root>/runpod/<account>/claim.json` (`packs/runpod/target_selection.py: RunPodSelectionOwner`, `packs/runpod/adapter.py: _cleanup_records`) into the Runtime's remote activation record. | `claim.json` is the acquisition journal that exists before any activation; the Runtime's remote activation record is per task and starts later (`service.py: task.remote_activation_*`). Where each phase lives is Plan 38's custody work, and proving a lease needs a real RunPod account and money. Keep the journal local until then. |
| S35-4, rest | An HTTP route and generated clients for the grant ledger; a support-root revocation journal that `restore` replays through `apply_revocations`; resolving a credential reference; the Plan 90 `trust approve/revoke/list` consumer (TR-1). | The route changes the hash-pinned contract (`contract/artifacts.json`) and the generated clients in each repository; the journal needs the dirfd restore path (`backup.py`); credential resolving is Plan 36's unfinished design; TR-1 is Plan 90's. The Release 16 packets stop at the Runtime service methods, which Plan 90 can call in tests. |
| S35-6 | Integration proof: exact migrated candidate, stale client, interrupted and repeated copy against a real install, direct and native Pinokio support, accepted and pending work, revoke and restore, rollback and retry. | Needs an installed candidate, a real older Astrid, native Pinokio and real restore of a real realm. The Release 16 packets prove the same cases on fakes and in-process Runtimes only. |
| Export gap | `structured_export` (and `GET /v1/export`) leaves out `user_app_state`, `project_selections` and `user_preferences`. The SQLite backup and restore keep them (proved in R16-P35-04). | `contract/schemas/export.json` is hash-pinned; adding keys changes the contract for every client. |
| CLI for choices | A command to save, list and remove compute profiles; a command for the skills opt-out list. | New commands change `cli-surface.json` and need its generator and the broad CLI tests, not a narrow proof. R16-P35-08 adds the functions only. |
| Other repositories' side-store checks | The same "new side store" check for the App (a lint on `localStorage`, `sessionStorage` and `indexedDB`) and for the Runtime. | The App lint needs the App's ESLint install. A scan of the Runtime found only install records, log and data roots, the default export folder (`service.py:7768`) and `~/Astrid/packs`; none holds a user choice. |

## Release 16 reconciliation, 28 November 2026

Evidence: first-parent history of `origin/release/16/plan-35` in astrid-agent and astrid-runtime. Agent merged into `release/16/main` by `0701ae2d0` ("Merge release/16/plan-35 into release/16/main"); Runtime by `e3f2bd8`. The App has no plan-35 branch; astrid-app `release/16/main` (`cc1d48f0`) holds no P35 work. Nothing is open in Agent or Runtime for this plan.

### Packets

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
|---|---|---|---|---|---|
| R16-P35-01 one helper for Runtime user-state documents | N | none | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_state.py` | [x] PR #665, merge `a554c82d1` |
| R16-P35-05 side-store check | N | none | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_state_side_stores.py` | [x] PR #667, merge `898cefc7f` |
| R16-P35-02 one-time import with receipt | X | 01 | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_state.py tests/test_user_state_import.py` | [x] PR #668, merge `fad0b093b` |
| R16-P35-06 choices document, safe mirror rule | X | 02 | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_choices.py` | [x] PR #669, merge `5461c0945` |
| R16-P35-08 compute profiles in Runtime, one import | N | 02 | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/core/test_compute_profile.py tests/core/test_compute_profile_volume.py tests/core/test_compute_profile_runtime.py -k "not untyped_mock_values"` | [x] PR #670, merge `4338648f2` |
| R16-P35-07 skills opt-outs mirrored to Runtime | N | 06 | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_skills_state.py tests/test_skills_state_runtime_choices.py` | [x] PR #672, merge `010659858` |
| R16-P35-09 removal date for VibeComfy TOML import | N | none | astrid-agent | `python -m pytest -p no:cacheprovider --noconftest -q tests/core/generation/test_generation_settings_legacy_removal.py` | [x] PR #674, merge `0c74617af` |
| R16-P35-R review of Agent work | S | 01, 02, 05-09 | astrid-agent | review receipt | [x] PR #676, merge `f59cc40cba7f25872def3be4603fd78a10bf1431` |
| R16-P35-03 protected grant ledger, revoke and reapprove | X | none | astrid-runtime | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_grants.py tests/test_app_state.py -k "not http_owner and not generated_python_client"` | [x] PR #125, merge `67825b519d8007c6ecbb433286cdaabd3bead97c` |
| R16-P35-04 state survives backup and restore | N | 03 | astrid-runtime | `python -m pytest -p no:cacheprovider --noconftest -q tests/test_user_state_restore.py tests/test_app_state.py -k "not http_owner and not generated_python_client"` | [x] PR #126, merge `b7e21c61593920e9e0c6006d5eef8cc8e73522b6` |
| R16-P35-RS1 review of Runtime work | S | 03, 04 | astrid-runtime | review receipt | [x] PR #127, merge `c7019b00f270a1cb173d9e4f0bf9852c95a3147c` |

### Remaining cards (owner-deferred to after Release 16, 26 November)

All rows below are outside the 4 December cut unless the owner says otherwise. They are dispatchable as written once their blocker is cleared.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
|---|---|---|---|---|---|
| S35-2a App: last-opened project via `/v1/projects/selection`; remove localStorage `lastSelectedProjectId` and `ui.preferences.lastOpenedProjectId` | X | owner's go; a machine with `npm install` | astrid-app: `useProjectSelection.ts`, `projectSelectionStore.ts` | `cd astrid-app && npx vitest run src -t "project selection"` | [ ] blocked: needs App `node_modules` and a networked machine |
| S35-2b App: extension state to one store (`astrid.extension-state` IndexedDB, `astrid.ext.state.*`) | X | S35-2a | astrid-app: `extensionStateRepositoryProvider.ts`, `extensionStateRepositoryIndexedDB.ts` | `cd astrid-app && npx vitest run src -t "extension state"` | [ ] blocked: needs App `node_modules` |
| S35-2c App: hidden shots, strokes, effect drafts, pending join clips to `project_documents` | X | S35-2a | astrid-app: `useHiddenShots.ts`, `useStrokePersistence.ts`, `effect-store.ts`, `useJoinClips.ts`, `clipPendingActions.ts` | `cd astrid-app && npx vitest run src -t "project documents"` | [ ] blocked: needs App `node_modules` |
| S35-2d App: last-used generation settings replaced by latest task spec; browser-storage lint | X | S35-2a | astrid-app: `useShotSettings.ts`, `useJoinSegmentsSettings.ts`, `useLastUsedEditSettings.ts`, `settingsStore.ts`, ESLint config | `cd astrid-app && npx eslint src --max-warnings 0 && npx vitest run src -t "settings store"` | [ ] blocked: needs App `node_modules` |
| S35-3a pack `disabled` list out of `pack-sources.json` | X | Plan 38 owner decision on `_inventory_launch_policy` | astrid-agent: `core/pack/source_setup.py`, `core/execution/custody_broker.py` | `python -m pytest -p no:cacheprovider -q tests -k "pack_sources or custody_broker"` | [ ] blocked: moves Plan 38 launch policy pin |
| S35-3b / S35-5 RunPod `claim.json` lease state | X | Plan 38 custody phases; paid RunPod account | astrid-agent: `packs/runpod/target_selection.py`, `packs/runpod/adapter.py` | `python -m pytest -p no:cacheprovider -q tests -k runpod` plus owner-run real-pod lease proof | [ ] blocked: owner money and Plan 38 |
| S35-4a grant ledger HTTP route and generated clients | X | R16-P35-03 (done); contract owner | astrid-runtime: `contract/artifacts.json`, generated clients in Agent and App | `python -m pytest -p no:cacheprovider -q tests/test_user_grants.py tests/test_app_state.py` (includes `http_owner` and `generated_python_client`) | [ ] not started |
| S35-4b revocation journal replayed by `restore` (`apply_revocations`) | X | S35-4a | astrid-runtime: `backup.py` dirfd restore path | `python -m pytest -p no:cacheprovider -q tests -k "backup and revoc"` | [ ] not started |
| S35-4c credential-reference resolution; Plan 90 `trust approve/revoke/list` (TR-1) | X | Plan 36 design; S35-4a | Plan 36 and Plan 90 owners | owned by Plan 36 / 90 | [ ] blocked: Plan 36 design unfinished |
| S35-6 installed migration/rollback integration: stale client, interrupted copy, native Pinokio, revoke and restore | X | S35-2, S35-3, S35-4; installed candidate; real older Astrid | integration owner | owner-run on a real install; record dated evidence | [ ] blocked: needs real machine and native Pinokio |
| Export gap: `user_app_state`, `project_selections`, `user_preferences` in `structured_export` / `GET /v1/export` | X | owner decision on hash-pinned `contract/schemas/export.json` | astrid-runtime plus clients | `python -m pytest -p no:cacheprovider -q tests -k export` | [ ] not started |
| CLI for compute profiles and skills opt-out | X | owner decision on `cli-surface.json` | astrid-agent | `python -m pytest -p no:cacheprovider -q tests -k "cli_surface"` | [ ] not started |
| App and Runtime side-store lints | N | S35-2d for App | astrid-app, astrid-runtime | App: `npx eslint src`; Runtime: packet-05 style scan test | [ ] blocked for App: needs `node_modules` |
