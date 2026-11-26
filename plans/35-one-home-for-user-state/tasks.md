# Tasks: one home for user state

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft outline only; not executable assignments.** Scope tasks after current-source inspection. The audit in [inputs.md](inputs.md) is code-read and must be re-verified.

## Task index

| Work area | Route | Depends on | Progress |
|---|---|---|---|
| [Verify the audit and fix the keep list](#intended-work-and-proof) | TBD | Plan 32 T6d (the settings document's shape) | Draft; not dispatched |

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
