# Why the 5,897-frame render failed near 20 minutes

## Verdict: (d) undetermined

**[VERIFIED]** This was not a configured 20-minute render limit. A newly observed descendant PID 10078 was born at 21:09:34 local; its retained capture-failure record shows the census tried to capture it shortly before task failure. Capture failed at pid_for_task (kern_return: 5), and before/after observations both still found that exact process live. The broker then refused to classify a live, uncaptured process as terminal and raised the reported CustodyError.

**[UNDETERMINED]** The surviving custody JSON contains no process command/name or failure-command observations for PID 10078. Its parent was PID 7970, but the attempt’s own render logs/scratch are no longer retained. I therefore cannot identify it as Chromium, ffmpeg, Node, or say why it appeared at that moment. The supported conclusion is “a live descendant appeared and native token capture failed”; the spawn’s identity and cause are missing.

The custody root does not include the task ID. **[INFERRED]** Its command birth time, 20:50:59 local, and process ancestry align with this task’s claimed render and 21:09 failure, strongly associating this candidate with the task; the association is not explicitly keyed in the custody file.

Evidence labels below: **[VERIFIED]** means directly present in retained records/source; **[INFERRED]** means a conclusion drawn from those facts.

## 1. Timeline

The task event timestamps are UTC (+00:00); local time was CET (UTC+1).

| Event | UTC | CET | Evidence |
|---|---:|---:|---|
| Admitted | 19:49:29.956 | 20:49:29.956 | Realm events row 138, task.admitted |
| Claimed, attempt 1 | 19:49:30.337 | 20:49:30.337 | Realm events row 139, task.claimed; attempt ID bd5486737fe04fdc903674adbf2f8ade |
| Owned command process PID 7194 born | about 19:50:59 | about 20:50:59 | tmp/astrid-custody-e5vwhj91/designation-command.json; birth has whole-second precision |
| First rendered-frame progress record (first report, already 13 frames): 13/5,897 | 19:53:01.808 | 20:53:01.808 | Realm events row 142, task.progress |
| Last recorded frame-progress task.progress event: 4,638/5,897 | 20:09:32.202 | 21:09:32.202 | Realm events row 339 |
| Candidate PID 10078 born | about 20:09:34 | about 21:09:34 | tmp/astrid-custody-e5vwhj91/observed-containment.json, final capture failure |
| Failure event recorded | 20:09:35.330 | 21:09:35.330 | Realm events row 340, task.failed; task updated_at is 20:09:35.326 UTC |

**[VERIFIED]** The failure was **20m 4.993s after claim**, **20m 5.374s after admission**, and about **18m 36.3s after the owned command PID’s whole-second birth time**. It was not exactly 1,200 seconds after any of those anchors. The follow log at take/almost-ready-v38-full-3.log rounds the terminal update to 21:09:35 [20m 5s].

**[VERIFIED]** The event stream does not timestamp completion of frame 1; 19:53:01.808 is the first recorded frame-progress report, which already counted 13 frames.

The realm event log records task progress, not every lease-liveness heartbeat. Therefore 20:09:32.202 is the last recorded frame-progress event; the exact last lease-only heartbeat cannot be recovered from task events.

**[VERIFIED]** The task-event rows in the last 30 seconds before failure (from 20:09:05.330 UTC) are exactly:

- 20:09:06.877 — task.progress, 4,583/5,897 frames, 68%.
- 20:09:11.938 — 4,594/5,897.
- 20:09:16.960 — 4,605/5,897.
- 20:09:22.058 — 4,616/5,897.
- 20:09:27.116 — 4,627/5,897.
- 20:09:32.202 — 4,638/5,897.
- 20:09:35.330 — task.failed, error “post-capture candidate is LIVE; terminal disposition is ineligible”.

These are rows 334–340 in the realm event table. There are no matching task/error lines for this task or attempt ID in the retained <stack>/data/runtime/service-pack-host.log, runtime.log, <stack>~/Logs/Astrid Runtime/, or <stack>/logs/. The currently retained pack-host log is from the later host startup. **[VERIFIED]** No target attempt directory or frame-progress.log remains under <stack>/data/attempts; the remaining attempt scratch has a different ID. The target’s task record is retained in realm SQLite, but its own render logs and per-frame progress file are not. **[INFERRED from the supplied history]** The target scratch was deleted around 21:10; the present filesystem inventory confirms it is absent, not the historical deletion time.

## 2. Timers, lease, evidence, storage and Remotion checks

- **[VERIFIED] No 20-minute deadline:** astrid/core/execution/guards.py:47-48,195-202 defines a 2 GiB default generated-evidence cap, a 3,600-second execution deadline, and a 300-second authority window. None is 1,200 seconds. Runtime’s task hard deadline is 24 hours (runtime-src/runtime_protocol/store.py:457-462), not 20 minutes.
- **[VERIFIED] No 600-second custody recapture:** the stopgap sets lease_seconds: 600 in generic_host.py:5684-5694. The host poller (:12029-12118) checks task/lease/fence/epoch state and heartbeats; it does not re-capture descendants at a lease boundary. Runtime heartbeat_task (runtime_protocol/store.py:6252-6277) only validates the current lease and updates expiry fields. A second 600-second lease period therefore does not imply a custody re-admission at 1,200 seconds.
- **[VERIFIED] Census is event/process driven:** the host calls observe_tree while the owned command is live (generic_host.py:10959-10976). The broker registers census-discovered candidates and records capture failure evidence (custody_broker.py:3573-3647); the bounded retry logic is at :3649-3805. It is not a 300/600/1,200-second timer.
- **[VERIFIED] Evidence cap does not fit this failure:** guards.py:391-423 raises an evidence-cap error on measured bytes; render media/workspaces are specifically excluded from this diagnostic budget (generic_host.py:4507-4513,12651-12657). The observed error is instead the exact custody exception at custody_broker.py:3855-3865. This render’s admitted storage estimate was 6,489,963,849 scratch bytes and 406,741,131 output bytes; the task result has no output. **[INFERRED]** Neither an evidence overrun nor a storage-floor error caused this task failure.
- **[VERIFIED] Storage checks are not 20-minute events:** live checks run every 0.5 seconds (generic_host.py:10965-10972, _LIVE_GUARD_INTERVAL_SECONDS at :4472). For rendering.render, _task_storage_limits returns None (generic_host.py:4500-4505), so this path checks the free-disk floor but does not re-check the admitted scratch/output estimate; the configured floor is read by runtime_protocol/storage.py:8-15. User-reported free space was about 6.8 GiB with a 2 GiB reserve. The recorded task failure is not the storage guard’s error.
- **[VERIFIED] Remotion’s configured frame path has no apparent periodic recycle/stitch at frame 4,638:** this source pins renderer 4.0.509 (remotion/package.json:21-25). Astrid stream mode patches a memory decision (remotion/stream-frames.ts:4-39); the frame worker calls renderFrames with concurrency: 1 and retains its browser across requests (remotion/src/astrid-frame-worker.mjs:267-293,314-342). Renderer dist/render-frames.js:39-40,70-105 builds its page pool from resolved concurrency; no 1,200-second or every-N-frames browser recycle appears in that path. This request writes PNG frames (imageFormat: png) rather than doing Remotion’s renderMedia encode/stitch path. The generic Remotion delayRender default is 30,000 ms (node_modules/@remotion/renderer/dist/options/timeout.js:13-40); this project’s live-scene delay is 35,000 ms (src/LiveSceneClip.tsx:10).

## 3. Custody evidence and candidate identity

**[VERIFIED]** The matching retained broker root is <stack>/tmp/astrid-custody-e5vwhj91. In observed-containment.json, the final capture_failures item records:

- candidate PID 10078, birth 21:09:34 local, parent PID 7970, root command PID 7194; the captured process group matches that owned root;
- capture substage pid_for_task, kern_return: 5, and port acquired/released;
- identical pre- and post-capture native identity, both outcome LIVE;
- census round 0; no failure_command_observations field.

The matching rule is implemented at custody_broker.py:3601-3647; a failed capture whose post-observation is still live raises the exact terminal-disposition error at :3855-3865. The decision JSON persists the identities and native observations but not argv/process name. Thus PID 10078 is verified as the trigger candidate; what executable it was and why it spawned are not recoverable from retained evidence.

**[INFERRED]** This makes the event a process-spawn/capture race coinciding with the 20-minute mark, rather than a limit that fired because the clock or frame count reached a threshold. The exact process and reason remain undetermined, so the overall verdict is (d), not a named spawn cause.

## 4. Short renders

**[INFERRED]** A 50-second range is less exposed because it usually has fewer seconds of active census and fewer chances for a new descendant to appear, but the risk is not tied to render duration. Any owned command that creates a new process can meet the same census/capture path, even in a shorter render. No evidence identifies a frame number, clip boundary, or other deterministic render event that always triggers it.

## 5. Why the session slot stayed poisoned; clearing it

**[VERIFIED]** The managed session manager fences and asks the adapter to release, but clears _active only after the adapter returns verified {ok: true} evidence. Otherwise it raises SessionCapacityError("managed session release was not verified") and intentionally leaves the slot occupied (managed_tool_session.py:527-545). The host’s owner release route requires the exact binding and generation and quiescent session; it reports release_pending on that failure (generic_host.py:7278-7307). This explains the refusal of later renders: the prior command’s cleanup was uncertain, so the host would not admit a replacement session.

**[VERIFIED]** A supported recovery attempt without restart is the exact-owner release_managed_session path (generic_host.py:7278-7307) after the session is quiescent; it succeeds only if the adapter can then prove release. I found no force-clear/reset operation. If the adapter continues to refuse verification, the manager has no supported in-process override to clear _active; restart/disposal is the recovery evidenced in this incident. The post-failure host logs were not retained, so the later refusal itself is from the supplied event history, while its mechanism is verified in source.

## Evidence locations

- Task events and attempt record: <stack>/data/runtime/realms/221335d5-722e-48d0-a0ab-d9fde94b2277/realm.sqlite3 (events, attempts).
- Follow log: take/almost-ready-v38-full-3.log.
- Custody decision/evidence: <stack>/tmp/astrid-custody-e5vwhj91/observed-containment.json, designation-command.json, and retained-cleanup-containment.json.
- Source trees were read only: ~/Developer/astrid-release-src/wt-r14-r6-fixes and ~/Developer/astrid-release-src/wt/runtime-src.
