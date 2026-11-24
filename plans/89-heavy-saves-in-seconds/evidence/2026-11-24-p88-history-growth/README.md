# Per-commit cost growth on stock Runtime 24e2c929 (Plan 88's isolated stack)

Source: Plan 88 lane, 23 Nov 2026 (Runtime `24e2c9291d5bcaface78324696286f2dc896debc`, no server overlay; installed Agent 97d1258d; standard heavy fixture build, timeline `save-loop-heavy-93b9d0ac`, project `9d4b2592add94ebeafee5daaa6198fef`). Lines from `runtime.log` (`runtime.timeline_commit.timing`); ~12 clips per batch; 44 accepted receipts in all (1 track add, 13 media imports, 30 clip batches). No byte sizes or entry counts are logged.

| time | outcome | handler total ms | provider_commit | durable_reconciliation | port_store_accept | wire_response |
| --- | --- | --- | --- | --- | --- | --- |
| 22:02:42 | accepted | 2,642 | 1,596 | 937 | 894 | 4 |
| 22:02:52 | accepted | 5,004 | 3,185 | 1,738 | 1,870 | 9 |
| 22:03:08 | accepted | 6,835 | 4,449 | 2,287 | 2,609 | 13 |
| 22:03:29 | accepted | 9,592 | 6,462 | 3,020 | 3,735 | 18 |
| 22:04:11 | accepted | 12,603 | 8,336 | 4,145 | 4,848 | 28 |
| 22:05:06 | accepted | 15,789 | 10,735 | 4,926 | 6,612 | 28 |
| 22:06:23 | accepted | 23,323 | 16,256 | 6,887 | 9,059 | 68 |
| 22:08:00 | accepted | 26,678 | 18,187 | 8,305 | 10,812 | 50 |
| 22:09:59 | accepted | 31,336 | 22,136 | 9,007 | 12,923 | 60 |
| 22:12:15 | accepted | 35,635 | 25,096 | 10,298 | 14,657 | 65 |
| 22:14:53 | accepted | 40,533 | 29,416 | 10,889 | 17,356 | 74 |
| 22:19:15 | accepted | 247,765 | 235,785 | 11,557 | 19,153 | — |
| 22:20:15 | accepted | 44,614 | 32,398 | 11,961 | 20,449 | 77 |
| 22:21:46 | failure (client reset) | 75,117 | 32,329 | 12,427 | 19,933 | 30,148 |

Reading: each stage grows steadily with accepted history (and the timeline's growing size); one commit at 22:19:15 cost 248 s in `provider_commit`. After the failure the daemon was idle (1.3% CPU, RSS 4.0 GiB). The reset was a client-side timeout.
