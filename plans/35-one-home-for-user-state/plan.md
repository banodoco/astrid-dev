# One home for user state

> **R16 retained boundary:** The 11-packet CPU lane is delivered and integrated. Preserve its actual owner deferrals; the broad original design below is not an instruction to redispatch it. The final candidate consumes its accepted state interfaces and adds preservation evidence through the existing install/save/workflow journeys.

**Project:** One home for user state

**Goal:** User choices, project choices and project work live in the Runtime (app-state and project documents), not in side files, env variables or browser storage; machine bootstrap state stays local.

**Status:** paused

**Owner:** Existing P35 custodian / Release Lead; CPU lane finished on [board #2033](https://github.com/banodoco/astrid-dev/issues/2033)

**Estimate:** 0 new implementation absent a demonstrated regression; 0.5–1.5 incremental evidence/qualification days within shared lived-in lifecycle proof. Owner-deferred mutation/restore and App relocation are not reopened.

**Waiting on:** Prepared R16 CPU implementation and reviews finished 26 Nov, all 11 packets landed in Agent/Runtime release/16/main ([Lead receipt](https://github.com/banodoco/astrid-dev/issues/2030#issuecomment-7191806062); [P35 board](https://github.com/banodoco/astrid-dev/issues/2033)). Not a R15 contribution or whole-project completion. Owner reserved App migration, pack/RunPod custody, grant API/revocation, installed migration/rollback, export/CLI and other guard work for later ([tasks](tasks.md#later-real-hardware-qualification-not-in-release-16)); no active queue or new dispatch.

**Vision gaps:** [Local-first projects](../../vision/gaps/F-005-local-files-cloud-assist.md) (primary) · [User control and recovery](../../vision/gaps/F-002-safe-user-control.md) (supporting).

**Contributing:** [Astrid development skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md).

**Draft; not ready for execution.** User choices, project choices and project work have one home: the Runtime. Today they are spread over side files, environment variables and browser storage. A read-only audit on 9 Nov (three code-read sweeps, not runtime-verified) listed the candidates. [inputs.md](inputs.md) records them.

## The rule

- **User choices** go to Runtime app-state (`/v1/app-state/user/{key}`).
- **Project choices and project work** go to `project_documents`, adding a document kind where one is missing.
- **Machine bootstrap state** stays a local file: anything read before the Runtime starts, or bound to one machine. Examples are install records, the data root, the realm catalog, discovery, process control, source profiles, locks and engine install receipts.
- **Secrets** go to [Plan 36](../36-one-credential-path/plan.md).
- **Files owned by another tool** stay where they are (`~/.claude`, `~/.codex`, `~/.hermes`, standalone VibeComfy's own `[library]` and ComfyUI address).
- A check flags any new `Path.home()`, XDG or `localStorage` write that is not on the keep list.
- **In the browser, one API.** The App already has one settings store (`src/shared/settings/settingsStore.ts`, `defineSetting`, `declarations.ts`). It keeps settings in Runtime app-state, with a localStorage snapshot for first paint and an unreachable Runtime, and has `user`, `timeline` and `device` scopes. Every browser key goes through it:
  - add a `project` scope, backed by `project_documents`;
  - add a `draft` scope: an IndexedDB recovery slot, cleared by a save receipt (today `timelineDraftIndexedDb.ts`);
  - add a `boot` scope: a value needed before the Runtime connects, such as the boot theme, the entry routing (`astrid:prefers-app`) and the onboarding fallback;
  - keep `device` for genuinely per-browser values, such as file-system handles and maybe preview volume.

  Raw `localStorage`, `sessionStorage` and `indexedDB` use outside that layer fails a lint, except for an explicit allowlist (for example the layer itself and the handle store).
- **Last-used generation settings are not stored at all.** They are the inputs of the latest generation in that scope (project, shot or tool), read from the Runtime's generation and task records (`generations.source_task_id`, `metadata_json`). Only explicit choices are stored, as settings: a project's defaults and a shot's "inherit project defaults" flag. Step 0 confirms that a generation's task keeps its full inputs; if not, the generation record gains them.

## Goal and scope

- **Included (from the audit):**
  - **App duplicates:** the last-opened project is kept in localStorage and in app-state `ui.preferences`, although the Runtime has `project_selections` and `/v1/projects/selection`. Extension settings are in localStorage and IndexedDB, although the App's settings layer reserves app-state `ext.*`.
  - **Project work held only in one browser:** hidden shots, inpaint strokes, effect drafts and pending join clips.
  - **Per-project last-used generation settings in localStorage** (shot, join-segment, lightbox edit and LoRA settings): replaced by reading the latest generation's inputs (see the rule). The explicit project defaults join [Plan 12](../12-multiple-inference-routes/plan.md)'s per-project generation settings.
  - **Browser keys that bypass the settings layer:** `usePersistentState`, `useEditorSettings` device keys, the extension service's own localStorage backing, the two extension stores, the media-import recovery record, and onboarding and connection flags. Each is either moved behind the layer with a scope, or deleted.
  - **Agent user choices in side files:** the skills opt-outs and setup selection (`~/.local/state/astrid/skills.json`), the pack `disabled` list (`pack-sources.json`), `~/.astrid/compute-profiles/`, and the `ASTRID_PREFERENCES_IN_PROMPT` toggle.
  - **RunPod lease state** (`<data_root>/runpod/<account>/claim.json`) moves to the Runtime's remote activation record. The file lock stays local.
  - One-time import from each old location, then the old copy is no longer read.
- **Not included:** generation settings and RunPod preferences, which [Plan 32](../32-generation-placement-targets/plan.md) T6d moves; secrets ([Plan 36](../36-one-credential-path/plan.md)).
- **Still undecided:** whether timeline draft `.current` pointers and the sync ledger move; device-only UI keys (decided key by key).

See [tasks.md](tasks.md) and [inputs.md](inputs.md).

## Completion

Every user choice and every piece of project work in the audit's MOVE list is read from and written to the Runtime, with its old location imported once and then ignored. The keep list is documented. The check fails on a new side store.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

The authority table identifies an owner for each object and custody phase; import-once deletion is not sufficient. Runtime may own portable preferences/grants; project state, hidden personal choices, URL intent, device bootstrap/receipts/locks, unique pending drafts/imports and secrets remain distinct. Known bounded app state is not a giant outbox. Retiring a store requires proof its unique work is migrated and recoverable.
