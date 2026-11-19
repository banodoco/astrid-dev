# P55-09 current candidate compared with the destination

These receipts compare the exact e3795656 reference and 978fb66c candidate. They cover two completed shard pairs. Every primary test outcome was checked against the decoded original job log, then verified after gzip readback. Each source record includes the raw log SHA-256, byte count, full commit, job link, pytest exit and terminal summary.

| Shard | Reference / candidate primary IDs | Common IDs | Changed among common | Reference-only / candidate-only | Pytest exits |
| --- | ---: | ---: | ---: | ---: | --- |
| [Unit 6 reference](https://github.com/banodoco/astrid-agent/actions/runs/44465854222/job/135363346114) / [candidate](https://github.com/banodoco/astrid-agent/actions/runs/44535559533/job/135599907051) | 5,003 / 5,006 | 4,998 | 0 | 5 / 8 | 1 / 1 |
| [Integration 4 reference](https://github.com/banodoco/astrid-agent/actions/runs/44465860262/job/135363367303) / [candidate](https://github.com/banodoco/astrid-agent/actions/runs/44535565116/job/135599925408) | 523 / 523 | 516 | 0 | 7 / 7 | 1 / 1 |

**Unit 6.** The reference reports 4,774 primary passes and the candidate reports 4,777. Both have 219 primary failures, 4 errors and 6 skips. The same 33 failed subtests under three parents bring pytest's failure total to 252 on both. Both report 93 passing subtests. All eight candidate-only LS-15 catalogue cases pass. Five passing reference timeline-arrange cases fall outside candidate shard 6. Their disposition across all eight current shards remains open.

**Integration 4.** The reference reports 402 passed, 95 failed and 26 errors. The candidate reports 404 passed, 93 failed and 26 errors. Seven candidate-only LS-15 cases pass. All nine historical dry-run/live regressions fall outside shard 4 on both sides. Their current hosted outcome requires [candidate integration shard 3](https://github.com/banodoco/astrid-agent/actions/runs/44535565116/job/135599925333), which was running at the evidence cutoff.

**Download and match.** In each JSON, `jobs[job_id].outcomes_by_id` contains the printable exact IDs. For other IDs, hash the exact unmodified pytest node ID as UTF-8 without a newline and look up the lowercase SHA-256 hex digest in `outcomes_by_full_id_sha256`. The comparison lists all additions, absences and changes within that shard. A null in the nine-case comparison means that shard reported no such ID.

| Download | Bytes | SHA-256 |
| --- | ---: | --- |
| [Unit 6 outcomes](unit6-outcomes.json.gz) | 181,493 | `b2d0b7204c7326b00fef342347ba2af56606be33bea6d5f5ac90a11b9182e74b` |
| [Integration 4 outcomes](integration4-outcomes.json.gz) | 23,377 | `bf80e45fc258c87541ffbeaad3a6fe4a11fa835e717ce52b1f2e70129dcc1a5c` |
