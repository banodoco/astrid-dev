Date: 2026-11-18
Kind: issue
Source: Plan 64 management run, SR-1 dispatch
Resolved by: —

SR-1 requires a deliberate v2 request identity break while an existing focused test pins the old v2 digests, and a run hard rule forbids changing tests merely to obtain a pass. The owner had already authorized the intentional contract break; the host clarified that the digest expectations must be updated while retaining semantic assertions and historical sealed-build coverage. The task card should explicitly distinguish this intentional migration from weakening a check before dispatch; the runner should surface conflicting release inclusion and branch-table prerequisites before opening a branch-row PR.
