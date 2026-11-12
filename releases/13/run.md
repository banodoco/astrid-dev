# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (19:35 UTC Thu 12 Nov): read this first

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
| Candidate `r13/compose` `857c3955` (frozen CI `int/r13-857c3955`) | As before, plus the no-unload guard (`engine-nofree`) and the per-(file, code) lint ratchet. The ratchet is red until the lanes clear their rows: ruff 27 rows / 59 findings, mypy 74 / 159. The owner dropped the mypy total gate |
| Live | Stage 1: 1/5 (t2i). Stage 2a: edit failed at engine **start** with `endpoint_ownership`. The cause isn't named yet. It is **not** a volume marker (the engine root is on the container disk). A CPU reproduction of four sequential jobs is running. #595 closed, replaced by #601. No pods. Balance $95.57 (floor $67.41) |
| Machines (own session `…2mhfLHKp…`) | K1 fix; M1 `72455cf6b` (Astra re-check); M2a; M4 card 5 `354b3d1c8` held for LT; card 6b (abandoned observers). LT gets a new row: cede write-ahead |
| Cells (own session `…VzW8yjKX…`) | `r13/cells-vc` `1463cb8e` (+ LTX bump if green); pin and preflight due 21:30. Catalog card: one shared argv builder (D1); 3 contracts fixed by the cut line (#342–#344) |
| Engine (fork, here) | U2 `47950c4a0` + reason strings → Astra; warm-host reproduction; lint card after the catalog card |
| Test lane (own session `…sWuWu9cB…`) | Lint ratchet merged; drop the mypy total gate; money cards W36b and W37b (5 blockers) being fixed |
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

