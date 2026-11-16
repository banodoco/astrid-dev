# Inputs: one home for user state

[Plan](plan.md) · [Tasks](tasks.md)

## Audit, 9 Nov 2026 (code-read, unverified)

Three read-only sweeps covered astrid-agent (core and packs), VibeComfy, astrid-app and astrid-runtime. Each finding names a file and line on astrid-agent `int/32-one-generation-path` (about `e81beb439`), VibeComfy `main`, astrid-app `main` and astrid-runtime `29a338a`.

| Area | Location | Verdict |
|---|---|---|
| App | localStorage `lastSelectedProjectId` (and app-state `ui.preferences.lastOpenedProjectId`), `useProjectSelection.ts:139-214` | Move to `project_selections` |
| App | localStorage `astrid.ext.*` and IndexedDB `astrid.extension-state`, `extensionSettingsService.ts:99`, `extensionStateRepositoryProvider.ts:116` | Move to app-state `ext.*`; one store |
| App | localStorage `astrid-hidden-shots:*`, inpaint strokes, `video-editor:draft-effects`, pending join clips | Move to `project_documents` |
| App | localStorage `last-active-shot-settings-*`, `last-active-join-segments-*`, `lightbox-edit-last-used-*`, `last-edited-lora-*` | Move to `project_documents` and app-state (with Plan 12) |
| Agent | `~/.local/state/astrid/skills.json` (`disabled_defaults`, `setup_selection`), `skills/state.py:25-136` | Move the choices; keep `installs` |
| Agent | `~/.local/state/astrid/<profile>/pack-sources.json` `disabled`, `pack/source_setup.py:153-193` | Move `disabled`; keep `active` and `cached` |
| Agent | `~/.astrid/compute-profiles/*.json`, `compute_profile.py:73-210` | Move to app-state |
| Agent | `ASTRID_PREFERENCES_IN_PROMPT` (env only), `agent_context.py:56` | Move or delete |
| RunPod | `<data_root>/runpod/<account>/claim.json`, `packs/runpod/target_selection.py:294-571` | Move lease state to the remote activation record; keep the lock |
| Keep | install records, data root, realm catalog, discovery, process control, source profiles, locks, engine receipts, `vibecomfy.toml`, `custom_nodes.lock`, harness-owned files | Stay files |

Also reported, and sent to Plan 29 on 9 Nov: the saved-autostart guard reads `preferences.autostart`, but no code in astrid-agent or astrid-runtime writes that key (installer writes `choices.autostart`), and `ASTRID_ALLOW_UNQUALIFIED_GPU` is a no-op.
