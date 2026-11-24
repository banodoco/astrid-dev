# Tasks — ComfyUI Desktop and existing environments

[Plan](plan.md) · [Inputs](inputs.md)

Draft task outline. Before dispatch confirm exact symbols, existing test IDs, source identity, overlap, authorization and the support matrix; contract cards list affected assertions and seek any required approval, not silently change them.

**Task ids:** CD-0–CD-5, RS1 if applicable, R. **Critical path:** CD-0 → CD-1 → CD-2 → CD-4 → CD-5 → R (CD-3 only if approved; RS1 before consumers of its contract). **Test inventory:** Agent `tests/packs/test_vibecomfy_local.py`, `tests/test_setup_skill_branches.py`, `tests/test_installer_maintained_guides.py`, target selection/launch and generation readiness tests to enumerate at CD-0; App copy/connection tests if touched. Use `env/README.md` shared worker environment and exact selectors at dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| CD-0 Reconcile Plan 20 and map installed Desktop/Git/Portable/Pinokio discovery, launch and ownership | N | — | read-only Agent/App/Runtime sources; Plan 20 records; redacted fixture shape | Exact source trace and reproducible stale-registration/closed/running observations; identify existing test selectors and overlapping plans; scope decision before writes | [ ] |
| CD-1 Read-only discovery distinguishes existing, stale, stopped and running targets without changing selection | X | CD-0 | Agent `astrid/packs/vibecomfy/local.py:scan`, target record evidence in `astrid/core/generation/targets.py` | Fixture running/closed/stale/missing/multiple/permission-denied cases; unchanged existing scan compatibility and no writes; re-check pinned JSON contracts at dispatch | [ ] |
| CD-2 Supported start/repair and attach next steps with actual cause and ownership | X | CD-1 | Agent existing readiness and target-selection/launch boundary; no new preference store | Broken path and moved port never appear ready; refused consent or ambiguous targets do not mutate; correct next action, re-probe and normal selection | [ ] |
| CD-3 Optional native verified launch if D3 approves and manual start is inadequate | S | CD-0, CD-1; Plan 38 output if shared | Agent `target_launch.py:ProcLaunchObserver,prepare_target_launch,launch_target` and native process identity seam | Exact Desktop/Portable owner and paths, wrong owner/port/argv refusal, no duplicate spawn or kill; existing ownership assertions preserved | [ ] |
| RS1 Optional launch boundary review (one round recommended, pending owner) | S | CD-3 if undertaken | read-only | Review verified ownership/consent contract before later use; findings become RS1 rows | [ ] |
| CD-4 Existing setup skill and editor tell the true state and call the same supported path | T | CD-2; RS1 if used | Agent setup/generation/VibeComfy skills and App connection copy only as needed | Existing guide contract tests and one supported start/recovery branch; no new execution route | [ ] |
| CD-5 Real attached Desktop journey and negative/compatibility evidence | N | CD-4 | public installed CLI/editor, Plan 34 GPU protocol; synthetic project; owner-approved Windows machine | Running, stopped and broken-registration scenario; actual Desktop GPU output visible in matching editor; preserve original environment and unrelated job; record unsupported layouts and exact tuple | [ ] |
| R Review rounds (one recommended, pending owner) | S | all scoped tasks | read-only | Independent integrated proof and review under run contract; no closure before review | [ ] |
