# One home for user state

**Vision gaps:** [Local-first projects](../../vision/gaps/F-005-local-files-cloud-assist.md) (primary) · [User control and recovery](../../vision/gaps/F-002-safe-user-control.md) (supporting).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

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
