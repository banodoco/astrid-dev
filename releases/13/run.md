# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (21:35 UTC Thu 12 Nov): read this first

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
| Candidate `r13/compose` `060a7555e` (comparison CI on frozen `int/r13-1f69f754`, running) | Since 20:45: SFX route repointed (`hunyuan-foley-local` → the template we proved), preflight gate plus `live_cells.json`, release-after-failure fix (truthful error, retry kept), exit-stall fix, **U2** (reason strings, network-mount rule, dead-owner handover), pod-log collection on failure, two catalog fixes. Boundary 101 passing |
| Live | **BLOCKED.** Stage 2b (`3c111cbed`): the claim works live (5090, $1.39/h, 25 min stock wait), but the first engine start on every fresh pod fails with `endpoint_ownership`. The break is in f9214240..5cca0bca; suspect the engine-layout merge `913c6b8f` (engine lane bisecting on CPU). The rerun on U2 (`cc8bc0b8c`) is blocked: `machines setup` now returns `conflict` (new, 3c111cbed..cc8bc0b8c; machines and engine lanes on it). Spent tonight: $0.33. Balance $95.19 |
| Machines (own session `…2mhfLHKp…`) | M1 merged. K1 fix round 2 (money bug). LT-a design round 2 (3 money holes), cut to 6 rows by the owner. M2a re-proof. Pod-side watchdog card (owner approved). Cut decision Fri 10:00: K1, M1 and M2 green on compose |
| Cells (own session `…VzW8yjKX…`) | cells-vc frozen `b3f20f33`, pin merged. Preflight: fixing it to read one declared `scripts/live_cells.json`. Catalog contracts #342–#344 by the cut line, or unlisted |
| Engine (fork, here) | U2 final round (Astra REWORK: 3 start/install fixes; no more rounds). #607 placement fix, then one Astra pass. Lint merged |
| Test lane (own session `…sWuWu9cB…`) | W48 (stale tests + truthful release error + W33 reorder). Exit-stall fix (unbuffered output + hard exit with pytest's own status). Per-shard auto-attribution. Comparison head: the next freeze, which will carry the exit fix |
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

