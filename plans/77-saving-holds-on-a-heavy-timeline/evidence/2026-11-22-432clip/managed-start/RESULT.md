# Run 3 measurement

## Timeline and status (UTC)

- 23:14:17.486–23:14:19.061: preflight; 35,081,068,544 bytes free. Ports 2400, 17500 and 17501 connect_ex 111; no stack process found. Both expected hashes matched; source WAL and SHM absent.
- 23:17:03.137: estimated birth of `up` PID 4712 from `/proc` start ticks and boot clock (10 ms tick resolution). Wrapper recorded start 23:17:03.142. The installed `up` command and environment variable names are in `02-start.txt`; no admission budget variable was set.
- 23:17:34.428: first status; no discovery or health. Initial monitor incorrectly treated idle `support.healthy=true` as readiness; restarted with discovery and health status required. The initial marker `03-observation.done` is invalid. First measurement at 31.286 s; the next was at 43.444 s, labelled 30 s in the log; subsequent samples were at their scheduled times.
- 23:17:46.748: 30-second profiler dump taken at 43.606 s, exit 0, PID 4716. 23:19:03.315: 120-second dump, exit 0, PID 4716. No 300-second dump: process exited before then.
- 23:19:06.622: `up` exit 1; 123.485 s after estimated PID birth. Message: `realm root is not one healthy unambiguous canonical workspace`. No discovery or health response was observed. No Runtime process was present in the 23:19:33.142 sample; observation ended 23:19:33.339.
- Timeline index and head revision reads: not run because healthy was not observed. Head publication, revision and clip count were not measured in this attempt. No history read or commit was made.
- 23:19:55.966–23:19:56.234: ordinary `down`, exit 0, `status: stopped`, idle safe.
- 23:20:08.991–23:20:10.428: postflight, ports 2400, 17500 and 17501 connect_ex 111; no stack process found. Source WAL and SHM absent.

## CPU observations

CPU seconds from `/proc/<pid>/stat`; each cell is PID, state, cumulative user + system seconds. UTC and actual sampling times take precedence over scheduled offsets. PID 4712 was `up`; 4714 was workspace inspect; 4716 was the admission doctor.

| Observation UTC | Scheduled seconds | PID state CPU seconds |
| --- | ---: | --- |
| 2026-11-22T23:17:34.428+00:00 | 0 | 4712 S 0.22, 4714 S 0.12, 4716 R 30.48 |
| 2026-11-22T23:17:46.586+00:00 | 30 | 4712 S 0.22, 4714 S 0.12, 4716 R 42.51 |
| 2026-11-22T23:18:03.142+00:00 | 60 | 4712 S 0.22, 4714 S 0.12, 4716 R 58.93 |
| 2026-11-22T23:18:33.142+00:00 | 90 | 4712 S 0.22, 4714 S 0.12, 4716 R 88.62 |
| 2026-11-22T23:19:03.142+00:00 | 120 | 4712 S 0.22, 4714 S 0.12, 4716 R 118.46 |
| 2026-11-22T23:19:33.142+00:00 | 150 | none |

## Database SHA-256

| Database | Before | After |
| --- | --- | --- |
| Source realm | `1d0f661bb97ddf39c353f7d8538714da4d32c5dc44b4078688c096e7f8086060` | `1d0f661bb97ddf39c353f7d8538714da4d32c5dc44b4078688c096e7f8086060` |
| restore-432-proof | `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8` | `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8` |

## Files written by this measurement

SHA-256 at result generation; the mailbox may subsequently be appended. `RESULT.md` is hashed in `RESULT.sha256`; the latter cannot contain its own SHA-256.

- `start-wrapper.sh`: `3c4769b174a652e7ab81c2c996611764583332c182b53a74337b85742be6006e`
- `monitor.py`: `b522eeccf443d1bea90b94f827a469fdeeee87129dafdb5258aeb7d1520d69bc`
- `reads.py`: `f7f91243e8394cff4eb072ea59a6b9f1448493ce69c7a18d95a610e1e4c22ccd`
- `make-result.py`: `a57c745d1a2d31ec0a2a5603f215bd09aedac5e8d5a89798df91e718eab70642`
- `to-orchestrator.md`: `2315f65c86d2f35cc8cea8e41572a787ea24681529cba2d69bf7c5c6788f2424`
- `receipts/01-preflight.txt`: `bd9f80f143a540a95fdce4280249ac994fb9644c6958b04c54503ed4ab2b473b`
- `receipts/02-start.txt`: `2dc771764c4a505fdf2cfc373743de2d2ffb2be5b4e913479ba3ba17e8b2a9c9`
- `receipts/02-up.done`: `4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865`
- `receipts/02-up.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `receipts/02-up.stdout`: `38d4ca1765565c1202c3fdd374cc3287f197ee69c56f37798df317482a71a39f`
- `receipts/02-wrapper.log`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `receipts/02-wrapper.pid`: `79539c26c573f011eb75615b5c37a4a0f4008a7f242ad686d60dcb78e6f4bce1`
- `receipts/03-monitor-correction.txt`: `5c5c561fd1eb4b9981c2c89c14954f8ccc6dfee7aac83c00a2a08acca6619bec`
- `receipts/03-monitor-restart.pid`: `ede4df2c6daaae51f8b3bea8a57f26960cc0cb6f255e78c6c823b08adf72bd64`
- `receipts/03-monitor-restart.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `receipts/03-monitor.jsonl`: `7d08b76fcbff838f446f3a305223461eb496d8d3a4b5746867efacab15a45ac4`
- `receipts/03-monitor.pid`: `bed87892cad828a95face5c7b006e8a9efbace9d6fc4291d12ff8c3bd94068c3`
- `receipts/03-monitor.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `receipts/03-observation-final.done`: `12ebebdb47b067ba4206cfa885e078fdf259ac132c9545deca6ac035d528907a`
- `receipts/03-observation.done`: `bbeee75256fd7c6d9ac258acd2b22837704ae0d80696ed039236b38cfcf1fab3`
- `receipts/03-pyspy-120.txt`: `cea429e537e3030fb8ade90996e3c9a6ea37d27f5b1660f81e6a11a60a4aeae3`
- `receipts/03-pyspy-30.txt`: `c2cf14ca6859ec63efa9861506a989853ed91c24fcbebd278e9b3f70c688ba21`
- `receipts/05-down.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `receipts/05-down.stdout`: `d26a6acba6945c3db872ef05a76bb06d5ecf552175c9d704f5635c183f9f0f25`
- `receipts/05-down.txt`: `339823f2d1b363498a9d5c448d430ea30ec431a2992c8380a5110d46b3456346`
- `receipts/06-postflight.txt`: `0e2678f0bcf797423ee76a25c31ab4bc7ebe9de0082b182f90a8ffbc95ec3d62`
