# R13 test manager: handover (12 Nov, 23:15 UTC)

**Rule 0 (orchestrator, 12 Nov 23:13): never call a failure preexisting, a flake or "not a regression" without a cited R12 run: a CI run id (R12 main CI run `43155525231`, jobs listed in `/home/user/wt/r13-tests/baseline/r12-main/REPORT.md`; R12 main Lanes runs `43155525276` and `43205560755`, logs in `/home/user/wt/r13-tests/baseline/r12-lanes/`) or a local R12 command with its log path (R12 checkout `/home/user/wt/agent-r12`, `scripts/worker-env/agent-pytest.sh <file> -q -rA -p no:cacheprovider > <log>`). Anything that can't be settled that way goes to the orchestrator as a question, not a ruling.**

Brief: `releases/13/test-manager-brief.md`. Table: `releases/13/tests.md` (single source of rows). Workspace: `/home/user/wt/r13-tests` (briefs/, runs/<card>/, triage/, tools/, baseline/, candidate/<sha8>/). Lane session ids: `/home/user/wt/r13-tests/tools-lanes.md` (machines 011EzfW2mh…, cells 011EzfVzW8…, engine via the orchestrator 011EzfW2L4…).

## Comparison head: `int/r13-1f69f754` (CI 43302480601, Lanes 43302480458), complete
- CI unit shards: 2 = 0 new; 3 = 0; 4 = 1 (H3 overlay, mine); 5 = 7 (mine, fixed `4b0f55c0`); 7 = 4 (engine) + 8 hosted-only installer (mine) + 133 timeline (Plan 39 #637); 8 = 6 (G cells ×3, P fixed `45bce4ad`). Darwin = 1 (engine, logs-as-outputs). Windows clean.
- Shards 1 and 6: NO-RESULT (stall mid-report after 100%). Cause: 1 MiB parametrize id. Fix `eff0f0aa` (below). These shards hold `tests/sdk/test_generation_target.py` (27 regressions found locally) and other R12-hole files, so the next head is the first real look at them.
- Lanes: opt-in 0; 1/4 = 9 (A engine, B cells); 2/4 = 3 (C engine) + D (Plan 39 #636); 3/4 = 96, of which 73 are the lifecycle env (fixed `9b4a3dce`) and 23 to route on the next head; 4/4 = 30 (cells, VibeComfy pin).
- Tools: `tools/shard-attrib.sh <run> <outdir>` (CI, per-shard, lane by first-parent merge) and `tools/lanes-attrib.py <run> <outdir>` (Lanes). Lanes now prints `-rA` (`7b0d8309`); before that, "absent on R12" in a file that existed at R12 means R12 passed.

## Open rows by owner
- Me: H3 overlay integrity (W58b); installer HOME isolation (W59b); `r13/tests/vibecomfy-source-env` `9b31d6c7` (pushed, with the orchestrator); `r13/tests/bounded-node-ids` `eff0f0aa` (pushed; "proof passed" sent 23:23: all 7 files pass, d18 6 failures = the same 6 as local R12 `scratchpad/r12-d18.log`, longest line 292; awaiting merge). Next head: route the 23 Lanes 3/4 failures, and hand-match the 4 renamed ids (tests.md row).
- Engine: MCP schema lost `project` (`test_mcp_generation_parity`); C f02 ×3 in #607; `test_owned_doctor_schema.py:119` reads `VIBECOMFY_SOURCE` (must land with my W60 branch); gen_target groups (wan-2.2 local ×4, no managed engine ×2, 5 unmapped); `managed_preparation.py:115` raw cache read (FYI). Merged: stopfix `14010e7a`, bridge-logs `80ef63ba`, fresh-wheel `bb9145fa`, objinfo (5 `.exception` → debug).
- Cells: VibeComfy `r13/cells-vc-fix` (placement decided only at fetch/stage: G ×3, E ×1, test_local_server_run ×16, test_entries ×2, test_local_run_site, test_t4g; then backslash ×5 and CFGGuider ×2; L2 message, L4 import-dir). Ready: `c9c05673` (B), `195e847f` (schema helper hygiene).
- Machines: BLE001 ×9 rows (machines-ble, M2b, LT-a); mypy ×5 (M2b); invoke settlement ×5 (card CC, Ctrl-C cancel is custody); gen_target `budget_cap_usd` ×8 (M2 removes the job's preferences snapshot).
- Plan 39 issues: #611 (publication latch T1–T4, R2-2), #621 (Pinokio flake), #633 (parked mypy-tm types), #636 (D order-dependent), #637 (timeline Runtime commit).

## Running workers (Codex, full access; usage limit hit 22:41, cleared 23:05; tell the orchestrator if it recurs)
- W58b (`/home/user/wt/agent-w58`, `r13/tests/h3-overlay-integrity`): restore the captured overlay bytes (sha `50f38e43…`), extras fixture sourced from VibeComfy `b3f20f33` `comfy_core@object_info_comfyui_0.24.0.1.json`; returns SHA plus before/after; must not run `test_cpu_rehearsal.py`.
- W59b (`/home/user/wt/agent-w59`, `r13/tests/installer-home-isolation`): fixture sets HOME/XDG_* to tmp, fix the test writing a real systemd unit; returns SHA plus the 8 tests reproduced and fixed, 0 regressions.
- W60b: done (`9b31d6c7`). W61b: done (diagnosis in `runs/w61/result.md`).
- Local proof (background): d18 under the Lanes marker on `/home/user/wt/agent-ids`; output in `/tmp/claude-0/…/tasks/b4k7o52ym.output`.

## Rules I apply
- Per-test comparison against R12 main `0e1543e0` (plus local one-file R12 runs for R12's hole); every result names its SHA; buckets: regression / new test failing / new test exposing R12 defect / preexisting / missing / flaky. "A flip excuses nothing": a test passing on R12 and failing on the candidate blocks; one R12 also fails the same way is preexisting (Plan 39).
- Never weaken a check. No new skip/xfail to get green (R-6); fixture or expectation changes only for deliberate, ruled behaviour, keeping every assertion. Don't re-pin a digest to launder a hand-edited captured fixture.
- Lint gate blocks only ruff F821 and BLE001, and mypy name-defined, attr-defined and call-arg; the ruff total gate is kept; I001 is a single `ruff --fix` after the lanes freeze (on the orchestrator's word). BLE001 clearing: never `logger.exception`/`error(exc_info)` on CLI paths; use debug + reasoned noqa, or report via the refusal/run log; log args must not raise inside an except.
- No RunPod/paid calls (in every brief); no local full suites; no pushes to main/cand/*/R12/int/*; no force-push or rebase; don't edit live-lane product files (hand to the lane); Astra review only for money/custody product changes; commit tests.md only when `scripts/astrid_dev.py check` passes.

## Waiting on the orchestrator
Merge `9b31d6c7` (with engine's doctor fix), `eff0f0aa` (after my "proof passed"), and W58b/W59b when sent; freeze the next head with those plus the cells VibeComfy fix, `c9c05673` and `195e847f`. Then I run shard-attrib and lanes-attrib on it and send per-bucket counts. Deadlines: blocking-rows report Fri ~20:00 UTC (send_later trigger 19:30); binding run Sat 06:00–10:00 (trigger 05:50); hourly check-in cron job `28ea29bb`.
