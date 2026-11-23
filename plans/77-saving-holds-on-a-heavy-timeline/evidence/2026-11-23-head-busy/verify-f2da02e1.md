# Verification of Runtime f2da02e1 (PR 105) on a new isolated stack (isolated4)

VERDICT: FIXED for 40 titles (plain titles, no clips); 136 titles STILL REFUSED (cause: total_changes moves together with files[WAL] during the replay window; every 76-85 s replay window spans 2-3 of the ~31 s executor re-registration WAL writes; no single write maps one-to-one to a refusal instant). Clip-bearing check and mid-replay control: NOT RUN.

## Status
- Stack isolated4 is RUNNING. Not stopped.
- Isolated3 (Runtime PID 543, ports 19287/16273/16274/16276) was not touched.
- Clip-bearing check (3 text titles + 2 motion clips, then 3x open and history): NOT RUN. Needs the motion pack (`run-astrid packs add https://github.com/banodoco/poms_packs --pack-id astrid_motion --revision 2379ab54aca522019ff4f869cfdf9375bdb56dfc --subpath astrid_motion --yes`, after Runtime start, not during a replay).
- Control (second-process durable commit mid-replay on the 136 project): NOT RUN.

## Overlay evidence
- Source: banodoco/astrid-runtime, HEAD f2da02e1dcf02439ee149f1412310c72aa4bf0bb, tree 533503fa4c3639faafc185c34f8be8a39b6452c4 (verified).
- Installed base (737843e) matched the installed package exactly before overlay.
- Overlay diff vs base (5 files, all in site-packages/runtime_protocol):
  - service.py
  - timeline_commit_execution.py
  - timeline_commit_port.py
  - timeline_commit_producer.py
  - timeline_commit_store.py
  So the PR is larger than the fence alone.
- The fence is in timeline_commit_store.py (~line 492): `connection.total_changes - credited`, where `credited` is stored in `self.store._session_replay_changes`. It is incremented in service.py (~lines 2764-2770). The name credited_temp_rows does not occur in the code.
- Running process imports the overlay: PID 23408 uses /root/codex/le4/isolated4/program/versions/981fb90f1a54/py/lib/python3.11/site-packages/runtime_protocol/__init__.py. Pack-host child PID 23424 has --source-checkout under isolated4.
- Isolated3 runtime_protocol matches the copy's runtime_protocol.orig (diff empty).

## Stack
- Runtime PID 23408, instance 2016aaa57ba54a6d8fc37f5d4ce3245b, door port 19297, internal endpoint 33021.
- Pack host PID 23424. Bun chat child PID 23423.
- Realm 1a194e2b-95b1-4e58-b8bb-c45f02e021d7 (same id as isolated3; root is isolated4).
- Data root /root/codex/le4/isolated4/data; HOME /root/codex/le4/isolated4/home; env /root/codex/le4/isolated4/env.sh (no CODEX_HOME).
- Pack-host claim polling observed: WAL mtime moves about every 31-33 s with no request in flight (watcher log /root/codex/le4/isolated4/walwatch.log).

## Attempts (all times UTC, 2026-11-23)
| time | kind | titles | status | detail |
|---|---|---|---|---|
| 15:21:10 | open (a1) | 40 | ok | 1.06 s |
| 15:21:11 | history (b1) | 40 | ok | 1.05 s, 3 rows |
| 15:21:13 | reopen (c1, 2 opens) | 40 | ok x2 | 0.98 s, 0.80 s |
| 15:21:15 | open (a2) | 40 | ok | 0.80 s |
| 15:21:16 | history (b2) | 40 | ok | 6.13 s |
| 15:21:23 | reopen (c2) | 40 | ok x2 | 0.76 s, 0.82 s |
| 15:21:25 | open (a3) | 40 | ok | 0.85 s |
| 15:21:26 | history (b3) | 40 | ok | 1.19 s |
| 15:21:28 | reopen (c3) | 40 | ok x2 | 0.94 s, 0.80 s |
| 15:23:22 | open (a1) | 136 | REFUSED head_busy | 76.13 s, "accepted commit inputs changed during verification" |
| 15:24:38 | history (b1) | 136 | REFUSED head_busy | 84.23 s, same message |
| 15:26:03 | open (a2) | 136 | REFUSED head_busy | 76.36 s |
| 15:27:20 | history (b2) | 136 | REFUSED head_busy | 75.44 s |
| 15:28:36 | open (a3) | 136 | REFUSED head_busy | 72.67 s |
| 15:29:49 | history (b3) | 136 | REFUSED head_busy | 84.76 s |

Refusal detail (all six): details {base: None, conflicts: [], current: None, reason: head_busy, status: refused}.

## Refusal counts
- 40 titles: 0 refused of 9 calls (open 3, history 3, reopen 6 individual opens).
- 136 titles: 6 refused of 6 calls (open 3, history 3). Successes: 0.

## Counter that moved (runtime.log, WARNING "accepted commit inputs changed during verification at isolated-read final")
- Every warning reads: `moved total_changes, files, files[WAL]`. data_version is not listed.
- Warnings at 15:21:17 (inside a 40-title history read that still returned ok), 15:24:01, 15:24:38.649, 15:25:20.561, 15:26:03.424, 15:26:41, 15:27:20.151, 15:27:57, 15:28:35.955, 15:29:10, 15:29:49.013, 15:30:34, 15:31:14.209.
- Each of the six 136-title refusals matches a warning within about 0.1 s of its end time (15:24:38.649, 15:26:03.424, 15:27:20.151, 15:28:35.955, 15:29:49.013, 15:31:14.209). Some intermediate warnings did not produce refusals; they are internal replay retries.

## 31 s rhythm
- WAL mtime moves at: 15:23:49, 15:24:21, 15:24:53, 15:25:24, 15:25:56, 15:26:29, 15:27:01, 15:27:34, 15:28:05, 15:28:36, 15:29:09, 15:29:43, 15:30:16, 15:30:47, 15:31:17.
- Each 72-85 s replay window contains 2-3 of these writes, so every replay window spans the executor re-registration rhythm.
- No refusal instant equals a WAL write instant (the refusals fall between writes, e.g. 15:24:38.65 between 15:24:21 and 15:24:53).
- Pack-host log shows "generic host claim failed: transport_timeout: runtime request timed out" during the replays.
- Answer: the refusals coincide with the ~31 s executor re-registration rhythm in the sense that the replay windows always contain those durable writes; the fix does not prevent the total_changes move caused by them.

## Not done
- Clip-bearing check (step 3).
- Mid-replay second-process control commit (step 4).
- Earlier notes: the 40-title check used plain titles only. The defect was originally reported after clip-bearing commits, so the 40-title pass is weaker evidence.

## How to stop (not done)
- Kill PIDs 23408, 23423, 23424 (isolated4 only), or run the isolated4 copy's `py/bin/astrid-runtime down --data-root /root/codex/le4/isolated4/data` with env.sh sourced.
- Stop the WAL watcher: `pgrep -f walwatch.py` then kill that PID.
