# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (22:45 UTC Thu 12 Nov): read this first

### Timeline to release: publish Saturday 14 Nov by 12:00 UTC (assumed UTC)
| When (UTC) | Milestone | Owner | Status |
|---|---|---|---|
| Thu ~21:30 | Engine **U2 + dead-owner handover** (CPU reproduction, why-errors) merged | engine (here) | building; Astra about 20:30–21:15 |
| Thu ~21:30 | **`r13/cells-vc` + pin + `scripts/preflight.py`** merged | cells session | 6aede014 pushed; proof, gate and catalog fix running |
| Thu ~22:00 | **Preflight gate** on the candidate, then **live five-cell run** (current generate path) on the composed candidate | me | after the two above |
| Thu night | TTS follow-up, catalog fix, node-compat, target-asset tests, test-lane money cards (gate atomicity, 4xx) | lanes | running |
| Fri ~08:00 | **K1** (edit fix), then **M1**, then **M2**, merged into `r13/machines` | machines session | K1 fix and M4 card 5 running |
| Fri ~14:00 | **LT** (lease transition table, including the durable billing stop and the re-review rows), then **M4**, then **M3** | machines session | LT draft ready |
| **Fri 18:00** | **CUT LINE:** machines core merged and Astra-reviewed, plus a **live claim-path proof**. If not, ship without the new machines CLI (R12 renting path + today's fixes) | me | — |
| Fri ~20:00 | Test lane's "rows still blocking" report on the newest frozen head | test lane | — |
| Fri evening | Fix the remaining blocking rows; M11 (RunPod code into the pack) only if green early | lanes | — |
| **Sat 06:00** | **Freeze** the candidate; final frozen CI head | me | — |
| Sat 06:00–10:00 | Binding test-by-test comparison against R12; final live proof (all five cells, claim path); App re-pin (release 13); R1-update proof row; release record | test lane + me | — |
| **Sat ~11:00** | **Publish** (an hour of slack before 12:00) | me, with the owner's go | — |

### Streams
| Stream | State |
|---|---|
| Candidate `r13/compose` `520803167` (comparison CI on `int/r13-1f69f754`; shards 1/6 near the limit) | Since 21:35: the **fresh-pod engine-start fix** (`8a425ee6b`), the pod watchdog, claim stock-wait fix + bound, setup error details, BLE comments, Lanes `-rA` + lifecycle env, urllib/fallback-hash/h3-helper test fixes, dry-run traceback fix, uncertain-stop custody fix, bridge logs (logs are outputs; selectors pick product outputs), objinfo via the VibeComfy API. Boundary 101 passing |
| Live | Stage 2c confirmed the start failure live (`request_mismatch`). Stage 2e on the fix build: setup ok, but the claim was refused by the watchdog (`termination_denied`: the pod key can't terminate). Failed closed, 0 pods. **Waiting on PW-soft** (denied/unknown means host custody plus a warning; owner-aligned ruling), due about 23:10. Tonight $0.94; balance $94.83 |
| Machines | M1 in. Pod watchdog in, with PW-soft due. Claim wait fixed and bounded. Ctrl-C cancel fixed (re-proving). M2b committed `0b2398a1f`, held: 16 test_generation_target failures being compared by id. K1 reconcile with compose reasons, due about 23:45. LT-a design done. Cut decision Fri 10:00 |
| Cells | Preflight plus live_cells.json merged; SFX route repointed. VibeComfy fix for model placement (about 40 Lanes rows plus 3 windows_gpu) running, then one re-pin |
| Engine (fork, here) | #607 review fix done (`daf973229`); journey card, then it lands ahead of M2. Fail-safe injection tests plus the doctor-schema env-var fix on `r13/engine-stopfix` |
| Test lane | Shard-by-shard sorting of 1f69f754. Installer HOME isolation (test infra, owned). VIBECOMFY_SOURCE removed from the wrapper. Group D (R12 flake) to Plan 39. test_generation_target run locally on R12 and compose |
| Advisor (own session `…4KxQbf3m…`) | Report in (18:21); actions taken |
| Investigation | #595 warm machine, cold engine (models unloaded each job): Opus fork running |

### Rules in force
- **Tests:** no worse than R12 `main`, test by test, on hosted `int/r13` CI. No local full suites. Managers run focused proofs only.
- **Codex:** always pass `-c model_reasoning_effort=…` (`high` for Sol and Astra, `medium` for Terra, `low` for Luna). Until 16:13 every worker ran at `none`.
- **Codex safety:** every brief forbids RunPod calls and `astrid generate` or `machines`. Paid steps stay with me.
- **Reviews:** Astra for rigour and robustness; Opus for structure, taste and feel.
- **Disk:** 3.7 GB free. `home-b3` holds the uv cache the Stage 1 venv uses, so never delete it. A VibeComfy clone mirror is at `/home/user/wt/vc.git`.

### Group B (after the candidate)
T7 (the wait reason reaching the CLI), T8 (Runtime blocker list), T10 (models stay loaded between jobs), T11 (default project), T13 (CPU journey), T14 (catalog dry-run corpus), Astrid `models.lock.json` to the same model record, the Plan 50 revision.

