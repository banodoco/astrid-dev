# Tasks: execution host refactor

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Release 14 rows (HM1 to HM3) are executable**; the extraction rows are written after HM1, for [Release 15](../../releases/15.md). The rest of this file is the original outline.

## Release 14

Steps 1 and 2 of the [sequence](plan.md#sequence), on astrid-agent `release/14/main` at `fc391dea6` (`astrid/core/execution/generic_host.py`, 18,784 lines). Nothing moves in Release 14. Work lands on `release/14/plan-13` in astrid-agent and astrid-dev.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| HM1 The map: each responsibility in `generic_host.py` (line ranges, public entry points, the module state it reads and writes), its callers in `astrid/` and `tests/`, and the existing tests that exercise it. It proposes the extraction boundaries, names the ones Plan 55 LS-6, LS-7 and LS-8 touch, and where LS-8's resident sessions sit beside the host | X | — | astrid-dev `plans/13-execution-host-refactor/map.md` (new); read-only in astrid-agent | Every top-level definition in the file is in exactly one responsibility (a script's count of definitions matches the map's); every caller named was found by a recorded search; each responsibility lists the tests that reach it, or "none" | [x] 17 Nov: R14-P13-01, `map.md` merged into astrid-dev `release/14/plan-13` at `a62ae1eb` (#822); 188 definitions recounted independently |
| HM2 Characterisation: for each responsibility HM1 marks "none" or thin, focused tests that pin today's behaviour of its public entry points, including lifecycle, cancellation, process ownership and result handling where it has them. Tests only; no product change | N | HM1 | astrid-agent `tests/core/execution/test_host_characterisation_*.py` (new) | The new tests pass on `release/14/main` and on `release/14/plan-13`; each names the responsibility it pins; a list of what is still unpinned and why | [ ] |
| HM3 `_stop_registered_host` (`astrid/sdk/host_bootstrap.py:1086`) uses the current Runtime's support root, not the registration's own, and an empty `support_root` no longer opens `generic-host.lock` relative to the working directory | N | — | astrid-agent `astrid/sdk/host_bootstrap.py`; `tests/sdk/test_host_recovery.py` | Two new cases in `tests/sdk/test_host_recovery.py` (a registration with a foreign support root; an empty one) fail before and pass after; `bash scripts/worker-env/agent-pytest.sh -q tests/sdk/test_host_recovery.py` passes | [ ] |

The prepared-worker plumbing card below waits for Plan 14's audit and stays out of Release 14.

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

Now row HM3 above.

- **Outcome / work:** `_stop_registered_host`, a test-helper path, trusts the registration's own `support_root` rather than the current Runtime's. An empty `support_root` also opens `generic-host.lock` relative to the cwd. Bind both to the current Runtime support root.
- **Route:** N.
- **Dependencies and inputs:** Execution host bootstrap retirement code; exact file paths TBD at setup.
- **Focused checks:** Exact focused selectors TBD at setup; no broad suites.
- **Done:** Both paths use the current Runtime support root, and the focused checks are recorded.
- **Progress:** [ ]

### Prepared-worker plumbing in `generic_host.py` (follow-up)

- **Outcome / work:** once Plan 14's reachability audit shows the RunPod prepared-worker island dead, remove its readiness-profile plumbing from `generic_host.py` (44 references) and `actions/run/run.py:813-866` (36). Source: Plan 32 review, 9 Nov, at 7209ffcc7. Priority: Medium.
- **Route:** N.
- **Dependencies and inputs:** Plan 14's prepared-worker audit; the `generic_host` machine-path and engine-branch parts were not audited in the review (17,135 lines).
- **Done:** no readiness-profile reference remains outside what the audit kept; focused checks recorded.
- **Progress:** [ ]
