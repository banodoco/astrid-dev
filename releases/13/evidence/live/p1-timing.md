# p1 timing round (build 6a6ab6f4d, RTX 5090 pod 65y7tk8hiheike)

Seconds. wall = END-START from round log (CELL [Xm Ys] in brackets). timing = machine.timing phases (prep/exec/coll/release). jr = job-run.v1 phases (verify/engine/execute/collect). All 6 jobs: engine_reused=true, hashed 0, skipped (trusted) 6/6/6/10/8/6.

| job | wall (CELL) | prep | exec | coll | rel | host unaccounted | jr verify | jr engine | jr execute | jr collect | pod startup/conv (exec - sum jr) | Prompt executed in | queue/poll (execute - prompt) | VRAM free before -> after (GB) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| t2i-7 | 829 (13m49s) | 539.7 | 173.6 | 48.4 | 21.2 | 46 | 0.20 | 1.29 | 65.1 | 0.04 | 107.0 | 55.36 | 9.8 | 33.1 -> 17.3 |
| t2i-8 | 242 (3m39s) | 17.2 | 104.5 | 46.7 | 21.0 | 53 | 0.12 | 1.20 | 11.9 | 0.04 | 91.3 | 2.88 | 9.0 | 17.3 -> 17.3 |
| t2i-9 | 261 (3m59s) | 17.9 | 121.4 | 47.2 | 22.5 | 52 | 0.19 | 1.15 | 12.2 | 0.04 | 107.8 | 3.01 | 9.2 | 17.3 -> 17.3 |
| h3 T5a (8 st) | 540 (8m08s) | 17.8 | 345.0 | 64.0 | 20.7 | 93 | 0.34 | 1.52 | 219.1 | 8.38 | 115.7 | 211.25 | 7.8 | 17.3 -> 1.9 |
| h3 T5b (20 st) | 382 (5m33s) | 18.0 | 191.3 | 60.8 | 23.1 | 89 | 0.15 | 2.41 | 76.8 | 8.50 | 103.4 | 69.66 | 7.2 | 1.9 -> 3.7 |
| t2i-10 after h3 | 312 (4m50s) | 18.7 | 172.1 | 47.2 | 20.8 | 53 | 0.12 | 1.68 | 71.2 | 0.04 | 99.1 | 61.84 | 9.4 | 3.7 -> 17.3 |

Note: wall (END-START) is 20-50 s longer than the CELL [Xm Ys] figure; the difference is script time outside the CLI call.
Release: pod released, cost_usd 1.0512 (1.39/h), final pods empty, final balance 81.5466349613.
