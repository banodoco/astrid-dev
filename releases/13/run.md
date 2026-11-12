# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (23:20 UTC Thu 12 Nov): read this first

Live Stage 2f is running on the PW-soft build `bb0ae49da`. The claim worked, including its warm-up job, and t2i has been running since 23:07, slower than the earlier 6.5-minute passes. Next: if t2i passes, the other four cells on the same pod, then release.

### Timeline to release: publish Saturday 14 Nov about 11:00 UTC
| When (UTC) | Milestone | Owner | Status |
|---|---|---|---|
| Thu 23:07 | **Stage 2f:** claim, then t2i, then the other four cells from `scripts/live_cells.json` on one pod, then release | me | claim OK (5090 `nk9ukqpoy7zwme`, warm-up job succeeded); t2i running |
| Fri ~01:00 | **RunPod v2 migration** (REST v1 retires 15 Nov), then a lifecycle re-pin | machines | Codex worker running |
| Fri ~04:00 | **LT-a wiring**, then one Astra review | machines | running |
| Fri early | **K1** reconcile; **M2b**, held on 16 test_generation_target ids | machines | running |
| Fri | **#607** lands (journey card, then the test_generation_target card) | engine (here) | review fix `daf973229` done |
| Fri | VibeComfy **placement redesign** (about 40 Lanes rows, 3 windows_gpu, 2 test_entries), then a re-pin; sdk-target-tests | cells | Codex Sol running |
| Fri | Test lane: **bounded-node-ids** `eff0f0aa` (the 1 MB id stalls the CI log), W58b–W61b; then one new frozen CI head | test lane, me | waiting for "proof passed" |
| **Fri 10:00** | **Cut decision:** K1, M1 and M2 merged and green on compose | me | — |
| **Fri 18:00** | **Cut line:** if it isn't met, ship without the new machines CLI | me | — |
| **Sat 06:00** | **Freeze**; final frozen CI head | me | — |
| Sat 06:00–10:00 | Binding comparison against R12, then the final live five-cell proof, then the App re-pin and the release record | test lane, me | — |
| **Sat ~11:00** | **Publish**, with the owner's go | me | — |

### Streams
| Stream | State |
|---|---|
| Candidate `r13/compose` `bd59f32e2` | Since 22:45: PW-soft (`bb0ae49da`); the Ctrl-C fix; PR #293 (MCP whole results, IN); the CI VibeComfy checkout in tests (`9b31d6c7d`), with engine's doctor-schema fix |
| Live | The watchdog log line is confirmed on the pod: `termination_authorised=no`, so the run is under host custody, as PW-soft intends. Census at 23:19: 1 pod (ours), $1.44/h, balance $94.56 (floor $67.41) |
| Machines (own session; stays on Opus until the Fri cut) | Handover 2 at `r13-progress/machines-handover-2` `50a470be3`. Order: v2, then K1, then M2, then LT/M4 |
| Cells (own session; moving to Sonnet) | Handover at `r13-progress/cells-log` `443ed443`. Placement card, sdk-target-tests, contracts #342–#344, lifecycle re-vendor |
| Test lane (own session; moving to Sonnet) | Handover `releases/13/evidence/tests/handover.md` (Rule 0: no "preexisting" without a cited R12 run). Comparison head `1f69f754`; shards 1 and 6 NO-RESULT (the log stall) |
| Engine (fork, here) | #607; doctor-schema fix in |
| Advisor (own session `…4KxQbf3m…`) | Ruled on models at 23:17: test lane and cells on Sonnet, machines on Opus until the cut, no Haiku in any seat that rules on red-vs-R12 or custody. Its helpers moved to Haiku/Sonnet |
| Open PRs | Triage done (`evidence/open-prs.md`). Included PRs are recorded at publish; stale ones are closed and their contributors told |

### Rules in force
- **Tests:** no worse than R12 `main`, test by test, on hosted `int/r13` CI. No local full suites. Managers run focused proofs only.
- **Codex:** always pass `-c model_reasoning_effort=…` (`high` for Sol and Astra, `medium` for Terra, `low` for Luna). Until 16:13 every worker ran at `none`.
- **Codex safety:** every brief forbids RunPod calls and `astrid generate` or `machines`. Paid steps stay with me.
- **Reviews:** Astra for rigour and robustness; Opus for structure, taste and feel.
- **Disk:** 3.7 GB free. `home-b3` holds the uv cache the Stage 1 venv uses, so never delete it. A VibeComfy clone mirror is at `/home/user/wt/vc.git`.

### Group B (after the candidate)
T7 (the wait reason reaching the CLI), T8 (Runtime blocker list), T10 (models stay loaded between jobs), T11 (default project), T13 (CPU journey), T14 (catalog dry-run corpus), Astrid `models.lock.json` to the same model record, the Plan 50 revision.

