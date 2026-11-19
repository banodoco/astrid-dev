# P55-09 current candidate compared with the destination

These receipts compare the exact e3795656 reference and 978fb66c candidate. They cover three completed shard pairs. Every primary test outcome was checked against the decoded original job log, then verified after gzip readback. Each source record includes the raw log SHA-256, byte count, full commit, job link, pytest exit and terminal summary.

| Shard | Reference / candidate primary IDs | Common IDs | Changed among common | Reference-only / candidate-only | Pytest exits |
| --- | ---: | ---: | ---: | ---: | --- |
| [Unit 6 reference](https://github.com/banodoco/astrid-agent/actions/runs/44465854222/job/135363346114) / [candidate](https://github.com/banodoco/astrid-agent/actions/runs/44535559533/job/135599907051) | 5,003 / 5,006 | 4,998 | 0 | 5 / 8 | 1 / 1 |
| [Integration 4 reference](https://github.com/banodoco/astrid-agent/actions/runs/44465860262/job/135363367303) / [candidate](https://github.com/banodoco/astrid-agent/actions/runs/44535565116/job/135599925408) | 523 / 523 | 516 | 0 | 7 / 7 | 1 / 1 |

**Unit 6.** The reference reports 4,774 primary passes and the candidate reports 4,777. Both have 219 primary failures, 4 errors and 6 skips. The same 33 failed subtests under three parents bring pytest's failure total to 252 on both. Both report 93 passing subtests. All eight candidate-only LS-15 catalogue cases pass. Five passing reference timeline-arrange cases fall outside candidate shard 6. Their disposition across all eight current shards remains open.

**Integration 4.** The reference reports 402 passed, 95 failed and 26 errors. The candidate reports 404 passed, 93 failed and 26 errors. Seven candidate-only LS-15 cases pass. All nine historical dry-run/live regressions fall outside shard 4 on both sides. The completed [candidate integration shard 3](https://github.com/banodoco/astrid-agent/actions/runs/44535565116/job/135599925333) confirms all nine changed from PASS to FAIL. A tenth case, the independent managed-audio capability test, also changed from PASS to FAIL with unresolved host graph cleanup. The candidate reported 356 passed, 107 failed, 62 errors and one skip. Both pytest steps exited 1. The receipt covers 517 shared IDs in this shard.

**Download and match.** In each JSON, `jobs[job_id].outcomes_by_id` contains the printable exact IDs. For other IDs, hash the exact unmodified pytest node ID as UTF-8 without a newline and look up the lowercase SHA-256 hex digest in `outcomes_by_full_id_sha256`. The comparison lists all additions, absences and changes within that shard. A null in the nine-case comparison means that shard reported no such ID.

| Download | Bytes | SHA-256 |
| --- | ---: | --- |
| [Unit 6 outcomes](unit6-outcomes.json.gz) | 181,493 | `b2d0b7204c7326b00fef342347ba2af56606be33bea6d5f5ac90a11b9182e74b` |
| [Integration 4 outcomes](integration4-outcomes.json.gz) | 23,377 | `bf80e45fc258c87541ffbeaad3a6fe4a11fa835e717ce52b1f2e70129dcc1a5c` |

[Integration 3 outcomes](integration3-outcomes.json.gz) · SHA-256 `16fee8554eb83970bf1865c95533588d8df158e7b5f0b2d3f234259526008fe1`.

## Repaired candidate c54a6099

The [four-shard paired receipt](c54-integration-outcomes-by-id.json.gz) compares e3795656 with c54a6099. All 2,092 reference IDs are present among the 2,101 candidate IDs. Two common failures became passes, and all nine added IDs passed. Candidate shard 3, job 135721800656, reports 526 primary results: 368 passes, 95 failures, 62 explicit setup errors and one skip with unknown phase. All eight raw shard exits were 1. The receipt includes original job and log hashes. For protected parameter displays, look up the SHA-256 of the original UTF-8 node ID. This file's SHA-256 is `d4a1305cf334641ef1fa96eec559b0600a341c53746ddf86be223f7e6d62609d`. The earlier 978fb66c receipts remain separate.
