# Tasks: execution host refactor

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../../README.md)

**Draft only; not executable assignments.** The original plan supplied intended work but no task IDs or assignments. Exact breakdown, dependencies, difficulty routes, focused selectors, and review rounds remain to be scoped after inspecting the selected source. Do not infer that work is ready to start.

## Task index

Only the card below is recorded so far. Scope the rest from the actual source base, preserving the original intent below:

- Map responsibilities, callers, shared state, and existing focused tests; select natural extraction boundaries.
- Characterize affected behavior before extraction and rerun those exact checks.
- Extract one cohesive responsibility at a time, preserving public entry points and avoiding a replacement execution framework.
- Explicitly cover touched lifecycle, cancellation, process ownership, and result-handling boundaries.
- Keep semantic bug fixes separately named where needed; moving code alone must not silently change execution contracts.

Before execution, each task needs a difficulty route, exact inputs and dependencies, bounded work, explicit focused checks, completion evidence, and the existing review/publication boundary. No broad suites or automatic test discovery are authorized by this draft.

## Task details

### host_bootstrap retirement safety follow-ups

- **Outcome / work:** `_stop_registered_host`, a test-helper path, trusts the registration's own `support_root` rather than the current Runtime's. An empty `support_root` also opens `generic-host.lock` relative to the cwd. Bind both to the current Runtime support root.
- **Route:** N.
- **Dependencies and inputs:** Execution host bootstrap retirement code; exact file paths TBD at setup.
- **Focused checks:** Exact focused selectors TBD at setup; no broad suites.
- **Done:** Both paths use the current Runtime support root, and the focused checks are recorded.
- **Progress:** [ ]
