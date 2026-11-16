# Tasks: one home for user state

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
