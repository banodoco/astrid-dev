# Tasks: execution host refactor

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft only; not executable assignments.** The original plan supplied intended work but no task IDs or assignments. Exact breakdown, dependencies, difficulty routes, focused selectors, and review rounds remain to be scoped after inspecting the selected source. Do not infer that work is ready to start.

## Task index

No executable task cards are assigned yet. Scope them from the actual source base, preserving the original intent below:

- Map responsibilities, callers, shared state, and existing focused tests; select natural extraction boundaries.
- Characterize affected behavior before extraction and rerun those exact checks.
- Extract one cohesive responsibility at a time, preserving public entry points and avoiding a replacement execution framework.
- Explicitly cover touched lifecycle, cancellation, process ownership, and result-handling boundaries.
- Keep semantic bug fixes separately named where needed; moving code alone must not silently change execution contracts.

Before execution, each task needs a difficulty route, exact inputs and dependencies, bounded work, explicit focused checks, completion evidence, and the existing review/publication boundary. No broad suites or automatic test discovery are authorized by this draft.
