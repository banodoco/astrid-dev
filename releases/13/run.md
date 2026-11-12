# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (18:50 UTC Thu 12 Nov): read this first

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
| Candidate `r13/compose` `30a644bc` (frozen CI `int/r13-30a644bc`) | Engine layout and in-place install, A1–A3, U1, engine-fresh, h1, r2, r3, mypy and bootstrap; TTS v3; success logs; test-lane fixes; core neutrality green (vocabulary scanner + owner-ruled RunPod baseline) |
| Live | Stage 1: 1/5 (t2i). Stage 2a (diagnostics): edit failed at engine start, `endpoint_ownership` (cause unnamed; likely an earlier cell's warm server on port 8188; CPU reproduction running, and U2 adds reason strings). No pods. Balance $95.67 (floor $67.41) |
| Machines (own session `…2mhfLHKp…`) | Took over at 18:44; K1 fix, M4 card 5 |
| Cells (own session `…VzW8yjKX…`) | cells-vc, pin, preflight; recapture 36/53 offline |
| Engine (fork, here) | U2 merge → U2-live → Astra; target-asset tests; node-compat |
| Test lane (own session `…sWuWu9cB…`) | Comparing the newest frozen head; money cards (provider-gate atomicity, 4xx classifier); per-code ratchets |
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

