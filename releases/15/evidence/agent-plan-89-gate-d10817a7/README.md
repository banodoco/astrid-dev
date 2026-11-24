# Agent plan-89 gate: save work into Agent `release/15/main`

Date: 23 November 2026. Gate by the Release 15 Lead.

- **Candidate:** astrid-agent `release/15/plan-89` at `d10817a77b280b2ca6a7b945f841e9823bbbee3f`: Plan 89's Agent work, the #560 capture fix, and a generator-only pin to Runtime `24e2c929` (Runtime #109). Runs: CI [45259689240](https://github.com/banodoco/astrid-agent/actions/runs/45259689240), Lanes [45259694852](https://github.com/banodoco/astrid-agent/actions/runs/45259694852).
- **Landed head:** `3916ff313dc631d30a8a5c4160a58ce33e94a115`. It adds one commit to the candidate, refreshing the two Runtime pin witness constants (`tests/test_vendor_lock.py:76`, `RUNTIME_PIN` in `tests/test_windows_path_budget.py`) from `737843e9` to `24e2c929`, as those tests ask when the pin moves. No assertion changed. Both tests pass locally on Runtime `24e2c929`.
- **Baselines:** unit ids against [agent-ci-baseline-8807f820](../agent-ci-baseline-8807f820/). Lanes against run 45183456544 (`b324d7c1`, release/15/main), the latest completed lanes run there; the runs on `045064b6`, `0615e4e9` and `8fdf6615` were cancelled.

| Run | New | Gone | Ruling |
|---|---:|---:|---|
| ci.yml (unit shards 1 to 8, darwin native) | 5 | 3 | **New:** three readiness ids (moving group) and the two pin witness tests (fixed in `3916ff31`). **Gone:** readiness and pinokio group members. ERROR ids identical (328). |
| lanes.yml (integration 1 to 4, opt-in) | 1 | 1 | **New:** `test_shared_redo_rechecks_source_archive_at_acceptance` (recorded flaky member). **Gone:** `test_fresh_process_command_counts` (base timed out). |

Shard 6's failed-id count (226 against 259 failed) is the known shared-id subtest split. Per-job counts and every id are in [RESULT.md](RESULT.md).

**Verdict:** gate confirmed at `3916ff31`.
