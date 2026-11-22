# Plan 77 measurement archive

This archive records synthetic local measurements collected on 2026-11-22 for Plan 77. Historical compiled opening and dispatch observations are separated from the current stock failure. The current stock run has no gesture measurement.

## Archive contents

- `historical-opening.json` contains old compiled opening timing, public head counts, and sanitized route intervals.
- `compiled-first-trace.jsonl` and `compiled-settled-trace.jsonl` preserve ordered measured event phases, timing values, framework stages, exact App, Agent, and Runtime SHAs, and outcome flags. Compiled artifact marker and served-byte comparison flags remain explicit.
- `compiled-settled-geometry.jsonl` preserves pointer and viewport geometry with fixture identity removed.
- `current-stock-failed-observed.json` contains the separate current stock failure, exact component SHAs, sanitized route intervals, and no gesture claim.
- `current-stock-restore.json` records the restore byte comparison and schema values.
- `current-stock-cleanup.json` records cleanup outcomes without local paths or port numbers.

The event traces retain monotonic millisecond values and event order. Request intervals retain start time, status, and elapsed time. Dynamic project and timeline segments and asset filenames are generalized. Free text, quoted errors, local paths, session and process identifiers, credentials, URLs, and unused keys are omitted.

## Source selection

The selected files cover the Round 5 compiled opening, its two collision arms and the landed Release 15 stock opening. The current stock receipt ends at the writable gate.

Selected source files with original SHA-256 and byte size

- `edit-dispatch-trace/v30/compiled-opening/observed.json` — `f97c6407d1cfd8b3aac0ae13f1db13b17bed8789525c8360de2d5f4367cf6487` — 234927 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-first/results.jsonl` — `30072f2c04d8efba7db92c317bf5af7e61dc10e0d755dadd81dd20e9a943cdfe` — 97486 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-first/versions.json` — `c71b7604fdc6ffc271e499a534e2d19e0d45b7813043a2014840f7741393af3f` — 168 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/results.jsonl` — `a0fa89abb1a353946350fa6fc6ebdf466903258508e5b39f43b3756be25e6d1f` — 116573 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/versions.json` — `c71b7604fdc6ffc271e499a534e2d19e0d45b7813043a2014840f7741393af3f` — 168 bytes
- `edit-dispatch-trace/v30/compiled-dispatch/compiled-settled/browser-geometry.jsonl` — `d528ff5550d605e0d67ecc508bd5ea1bb92c603b1491279fe995191e0ebc808c` — 8793 bytes
- `release-current/compatibility/observed.json` — `851a7be745b718c0dfef0e62057b984255bcf05502526f49d40575b0a9e3b05d` — 467614 bytes
- `release-current/compatibility/operator-compatibility/restore-bytes.json` — `b51f68a48d1f96a1a753b44355898d076832d9d1c9ce2534fe6de834e97ec406` — 331 bytes
- `release-current/compatibility/compatibility/cleanup.json` — `43c3e7e518871e0f8fb090e37633899d89fffbabc6ac3e04558d5e8bde9a93fd` — 342 bytes

## Interpretation

Opening usability timing measures the observed local compiled preview. The first and settled compiled traces both ended without a confirmed save settlement. The settled trace records completed deferred history at pointerup and still records no timeline commit request. Current stock evidence records a failed observation without a measured gesture. All data is synthetic.

## Retained build and fixture

The host's run archive keeps the signed v30 synthetic bundle under `quick-indicator/bundles/large`. The 516 MiB backup's original database is schema 33 with SHA-256 `c0b27bb02c33d5b1e72699749c07adc769dda0c0eb2ceaceab222b630c6e132d`. The host retains the separate 12 KiB support bundle for authenticated restore.

The historical instrumented compiled output remains in the run archive under `edit-dispatch-trace/v30/compiled-dispatch/preview-dist`. The 140 MiB output has SHA-256 `30cb2a430734ebf836d85b4b3a6ad505dc2c9d351fdc0ccb55252ce9bd285d25` in the compiled build receipt. Its paired timing tapes and observed geometry are in this evidence directory.

## Runtime A opening and profile

The current Runtime A cold opening reached writable in 306.552 s. The warm opening reached writable in 13.744 s. Both receipts match the same app, agent, and runtime SHAs, and share the same runtime process receipt. The warm run has no py-spy profile. The separate original 480 s failure remains a distinct observation.

Both openings use the synthetic v30 fixture with 300 clips, 9 tracks, and 10 shot occurrences. Their terminal public heads were verified with 1 active head, 300 clips, and 10 occurrences. Both matched zero timeline commit POSTs. Both receipts record process closure and profile removal.

The cold receipt retains navigation and writable CPU tick counters, browser timing, CDP task metrics, and long-task start/duration markers. Its commits history GET observations started at 1,907.134 ms, 122,439.911 ms, and 243,141.901 ms. The first two entries have no status or completion time in the source receipt. The third returned 200 with headers at 298,379.193 ms and finished at 300,445.928 ms. The warm history GET started at 1,762.289 ms, returned 200 with headers at 6,596.562 ms, and finished at 8,802.099 ms. The receipts show no matching timeline commit POST.

The cold py-spy report used 100 Hz nonblocking sampling. It reported 27,175 samples and 3,008 errors. The ranker used 26,862 decodable weighted samples. It rejected 22 weighted samples with recoverable counts and measured a residual gap of 291 weighted samples. The original raw capture is 51,298,943 bytes with SHA-256 `1b9e31399146d10df279c112389c33144e99804dba80d4d5aca62e5b80c16dc8`. The host retains the raw capture in the run archive. The archive retains only ranked module basenames and function names.

The 30 s and 120 s stack snapshots show request-handler stacks in `server.py` through `handle_one_request`, `_dispatch`, and `do_GET`, with `open_object` and `timeline_commit_store.py:evaluate` also present. At 300 s the sampled stacks are mostly `threading.py:wait`, with a small number of request and log-pipe frames. These are sampled stack findings, not proof of a lock wait or contention. Snapshot archives omit thread/process IDs, labels, paths, locals, and other introspection.

The cleanup receipt records zero new profiles remaining. Its local paths and port numbers are omitted. New sanitized receipts are `runtime-a-cold.json`, `runtime-a-warm.json`, `runtime-a-cold-profile-index.json`, `runtime-a-cold-at-{30,120,300}s.json`, `runtime-a-cold-at-{30,120,300}s-stacks.json`, and `runtime-a-profile-cleanup.json`.

## Runtime B disposable comparison

Runtime B is one disposable, unpushed trial. Runtime A and Runtime B each have one opening trial, and neither trial includes a gesture measurement. The B receipt records the same synthetic fixture counts as A, exact App, Agent, and Runtime SHAs, and a verified terminal public head with 1 active head, 300 clips, and 10 occurrences. It reached writable in 176,179.869679 ms with first usable controls at 176,179.072921 ms. Runtime CPU was 306.85 s before navigation and 166.78 s from navigation through the writable boundary. The receipt records zero timeline commit POSTs, process closure, and profile removal.

The initial commits history GET began at 1,984.319208 ms and has no status or completion timing in the source receipt. The next began at 122,547.751320 ms, returned 200 with headers at 167,044.179825 ms, and finished at 169,723.876313 ms. `runtime-b-disposable.json` retains exact browser long-task markers, CDP timing values, all recorded request counts grouped by kind and status, and boundary in-flight request timing and status. Dynamic project, timeline, and object identifiers are generalized.

The restored database matched the backup SHA-256 `c0b27bb02c33d5b1e72699749c07adc769dda0c0eb2ceaceab222b630c6e132d` at schema 33. The reused stock distribution has the verified 355-file inventory SHA-256 `f8c4fdaa6b7bbfa8df6ccb8dd874973a88ac170ce2cb7220108540d59e806801`. Installed runtime source hashes are indexed by module basename in `runtime-b-reuse-and-restore.json`. Cleanup removed the owned stack, closed three ports, and left zero new profiles. `runtime-b-source-index.json` records byte sizes and SHA-256 values for the five allowed B source receipts and checksum lists. Local paths, port values, realm and process identities, and other incidental identifiers are omitted.
