Date: 2026-11-18
Kind: issue
Source: Plan 64 management run, SR-1 dispatch
Resolved by: —

SR-1 requires a deliberate v2 request identity break while an existing focused test pins the old v2 digests, and the run contract forbids changing pinned tests to obtain a pass. The task card should identify that conflict during planning and specify an approved migration of the historical assertions, including sealed-build coverage, before dispatch; the runner should surface conflicting release inclusion and branch-table prerequisites before opening a branch-row PR.
