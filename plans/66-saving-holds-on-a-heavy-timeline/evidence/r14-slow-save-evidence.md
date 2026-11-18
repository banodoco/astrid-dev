# Release 14 on :2400: saves still slow, drop during a save fails (18 Nov)

## Stack (main thread, verified)

- :2400 was rebuilt at about 10:05 CET.
  - App `fbb8168bd`
  - Agent `458d9d51`
  - Runtime `d725811`: `site-packages/runtime.lock.json` `source_commit`
  - Program version `fdbff077811b`
- The realm is a fresh copy of live. Before the drops, the head was `txn-72383d4f` (the import, 969b5e41…).
- **History GETs:** `GET …/commits?limit=4` takes 3–15 ms, down from 8.8 s on the old Runtime `519b404`. So #59 is live.

## Owner's report, 10:08–10:10 CET

"SAVING IS STILL VERY SLOW AND DROPPING ANOTHER ONE ON WHILE ONE IS SAVING CAUSES THIS Failed to save asset / Failed to fetch"

## Browser evidence (tab on http://127.0.0.1:2400, main thread)

- **The first drop was accepted.** It became `txn-918889d2b125484083157bc1a2a3d9c7` "Add media" (source app, receipt `created_at` 2026-11-18T09:08:12.814Z). Its drop start time is not yet known; get it from the server logs.
- **The second drop failed.** The console shows, at 10:08:24 CET (09:08:24Z):
  `[drop] Upload failed: TypeError: Failed to fetch`, at `WorkspaceClient.importProjectMedia` (`src/integrations/runtime/generated.ts:745`), called from `client.ts:793` → `withMutation` `client.ts:343` → `withSession` `client.ts:516` → `RuntimeDataProvider.prepareMediaImportAtBoundary` `dataProvider.ts:903` → `useAssetManagement.ts:432` → `external-drop-utils.ts:337/392`.
  "Failed to fetch" is a network-level failure: a reset, refused or aborted connection, not an HTTP status. The editor then showed an "uploading:Screen…" placeholder on the Chrome track.
- **Request volume.** The tab made about 953 `/api/` requests since load. Most were `GET /api/runtime/v1/objects/sha256:…`: about half came back 206, and **a large share came back 503**. Earlier, before the rebuild, the ACP `models` route and one `/api/astrid/v1/objects` GET were also 503.
- **The proxy.** `scripts/runtime-discovery-proxy.mjs` (node, about 9.5% CPU) fronts :2400. Earlier evidence (`live-check-almost-ready.md`) says it cuts at 60 s with a 503.
- The resource-timing buffer is full, so per-request durations aren't available from the page.

## Open questions

1. How long did the first drop's commit take, from request arrival to accept, and where does the time go now that CAS re-hashing, loads and probes are fixed? Candidates:
   - the Runtime's O(N²) ancestry walk (flagged by Opus in `opus-396-review.md`);
   - the legacy compile;
   - digests;
   - the App doing a full-document handoff;
   - media import or verification of the new object.
2. Why does `importProjectMedia` fail with "Failed to fetch" while a commit runs?
   - Does the Runtime serialise every request behind `store._mutex` or a single-threaded server?
   - Does the proxy drop or 503 requests when the upstream is busy, and with what limit or timeout?
3. Why are so many `/objects/` GETs 503: proxy concurrency, upstream busy, or a timeout?

## Server-side evidence

Read-only. Nothing was restarted, written or changed. Times are raw UTC (`Z`) from realm rows or file mtimes; 10:xx CET = 09:xx Z. Live realm: `data/runtime/realms/221335d5-722e-48d0-a0ab-d9fde94b2277/` (opened by Runtime pid 56569). The older realm `7dd95cc0-…` was an earlier boot. The proxy is pid 56595. The `/usr/bin/find -newermt` call fails on this macOS ("Can't parse date/time"), so mtimes were read with Python `os.stat`.

### 1. Logs and where they go
- `home/Library/Logs/Astrid Runtime/runtime.log` (7,988 B, last write 09:08:29Z): Runtime stderr (fd 3 of pid 56569). No per-line timestamps.
- `home/Library/Logs/Astrid Runtime/service-pack-host.log` (5,801 B, last write 09:08:11Z): pack-host stderr.
- `home/Library/Logs/Astrid Runtime/service-chat.log` (82 B, 09:05:33Z); `runtime-service.log` (0 B); `installer.log`, `install.log`: startup only.
- `logs/editor.log` (129 B, last write 09:05Z): launcher stdout/stderr (pid 56561, fd 1/2). Startup banner only.
- Proxy pid 56595: fd 1/2 are unix sockets, not files. Its `console.error` upstream lines (proxy:470) go to the launcher pipe. No proxy error line exists on disk.
- `timeline_commit_timing` phase records are emitted at DEBUG only (`runtime_protocol/timeline_commit_execution.py:170-178`). None are in runtime.log, so no phase timings exist on disk.
- Realm: `realm.sqlite3` (6.8 MB, last write 09:05:11Z) and `-wal` (3.8 MB, last write 09:10:45Z). Read with `mode=ro`.

### 2. First drop, txn-918889d2b125484083157bc1a2a3d9c7
Realm rows (`command_idempotency`, `timeline_events`, `timeline_commit_history`), in project-seq order:
- 09:06:17.664 `project.select` txn-f24ead66… (seq 869)
- 09:07:56.144 `project.select` txn-3e965738… (seq 870)
- 09:08:00.934 `object.ingest` txn-9fd98bdb… (seq 871)
- 09:08:00.960 `task.create` txn-02041dd9… (seq 872)
- 09:08:00.968 `attempt.settle` txn-e6bfcdd5… (seq 873)
- 09:08:00.982 `media.import` txn-6408b385… (seq 874)
- 09:08:03.064 `app_state.update` (no txn)
- **09:08:12.814 `timeline.commit` txn-918889d2… (seq 875), label "Add media". Event id 17 at 09:08:12.813.**
- 09:08:28.864 `timeline.commit` txn-76e8a3e2… (seq 876), label "Edit timeline", previous = txn-918889d2…. Event id 18 at 09:08:28.863.
- 09:09:56.977 `object.ingest` txn-42e7a1eb… (seq 877). Next `media.import` at 09:09:57.042 (seq 880).

- Request arrival is not recorded anywhere. Realm rows are written at commit, and no log line carries a timestamp, so arrival-to-accept cannot be measured from the server.
- Last durable step before accept is `media.import` at 09:08:00.982. Gap to accept: 11.832 s.
- Phase timings: none on disk (see 1).
- Runtime.log also has a `POST …/timelines/77f906f3…/commit` (request f9b658ad4d4945a78324f6ee808b9cf3) whose reply write failed with `OSError [Errno 55] No buffer space available` (server.py:1565 → 464). The request id is not stored in the realm, so it cannot be tied to 918889d2 or 76e8a3e2.

### 3. Failed second upload (~09:08:24Z)
- Realm: no row between 09:08:00.982 and 09:09:56.977. There is no `object.ingest`, `media.import` or idempotency row for it, so nothing was committed.
- Runtime.log has one media-import traceback: `ProtocolError: request body is shorter than Content-Length` (server.py:289, via `_binary_chunks`), raised in `stage_object` (server.py:1070 → service.py:5344 → cas.py:68). It was followed by `BrokenPipeError` on the error reply (server.py:464). Untimestamped.
- Route: `POST /v1/projects/{id}/media-imports`, defined at `src/integrations/runtime/generated.ts:252` in the editor source. The line 745 in the browser stack is from a built bundle. Runtime handles it at server.py:1067-1070 and treats it as binary I/O (server.py:548).
- Likely: the upload reached the Runtime and its body was cut off before the end, so the connection closed mid-upload. The timestamp is missing, so this cannot be tied to the 09:08:24 drop with certainty.
- No 503 or timeout is logged on the Runtime side. The proxy's 503/504 lines are not on disk.

### 4. Proxy (`editor/scripts/runtime-discovery-proxy.mjs`)
Timeouts and limits:
- `CONNECT_TIMEOUT_MS = 10_000` (:13): upstream connect (:456, destroys upstream), control-body read (:258, used at :389), operation connect (:319).
- `IDLE_TIMEOUT_MS = 60_000` (:14): upstream socket idle, re-armed by bytes (:461); operation response idle (:297) and upstream idle (:321); operation registry idle (:171, :187).
- `ACP_IDLE_TIMEOUT_MS = 300_000` (:15): chat route only (:461).
- No concurrency limit, queue or agent `maxSockets`. `upstreamInFlight` (:17, :454, :467) is only a log counter. The `request()` call has no agent option.

When it returns 503:
- :426: `currentChat` throws, so the reply is `{error:'acp_unavailable'}` 503.
- :419-428: `currentRuntime` throws, so the reply is 503 with `code: runtime_unavailable` (`fail()`, :19).
- :471: upstream error that is not a timeout gives 503 `runtime_unavailable`. A timeout gives 504.
- Operation route: 503 `operation_unavailable` at :269, :398, :403. An operation upstream status ≥500 is dropped via `failOwned` (`retire` → `cancel` → 503).
- Non-operation route: a Runtime 5xx is passed through unchanged (:446-451). The proxy does not invent a 503 for it.

Client-socket destruction:
- `writeFailure` (:330-334): `if (response.headersSent) response.destroy()`. Headers are written at :451 before piping, so an upstream error mid-body (:471) destroys the client socket. A destroyed socket gives the browser "Failed to fetch".
- :473 (`incoming.on('aborted')`) destroys upstream only.
- :479 (`server.close`) destroys pending control responses only.
- For `media-imports`, no headers exist before the Runtime replies, so a proxy error there returns 503/504 JSON, not a reset.
- Likely: the proxy has no path that resets a POST before headers, so "Failed to fetch" was probably a socket reset at the OS level (the Runtime logged `ENOBUFS`, errno 55) or a browser abort.

### 5. Runtime concurrency
- `runtime_protocol/server.py:113-114`: `RuntimeHTTPServer(ThreadingHTTPServer)` with `daemon_threads = True`. One thread per connection.
- `server.py:121`: `request_queue_size = 64` (listen backlog). `server.py:189`: `timeout = 30` (per-socket).
- `server.py:1498` `_dispatch`. The outer `with self.runtime.store._mutex:` is at :1554, and runs only for requests not in the exempt branches at :1520-1553.
- Exempt from the outer mutex: `_is_binary_io` (server.py:534-548: `GET /v1/objects/<id>` at :542, `POST …/media-imports` at :548), `_is_timeline_commit` (:550), plus `/v1/update`, diagnostics and `/v1/replace`. The comment at :1540-1542 says the commit and binary routes "own short store sections".
- The inner locks are still taken. `store._mutex` is an `RLock` (store.py:1091, :973), and the Runtime uses one SQLite connection:
  - `open_object` takes it for the metadata row and CAS open (service.py:6022-6026). This is the object GET path (server.py:1239-1243).
  - `import_media` takes it at service.py:5722.
  - `commit_timeline` takes it at service.py:3206 and :3231.
- So GET `/v1/objects/<id>` and media-import do not wait on the outer lock, but both wait on the same `store._mutex` for their DB sections while a commit holds it.

### 6. Object GETs
- `objectContentUrl()` returns a plain `/v1/objects/<id>` URL (`src/integrations/runtime/client.ts:1216-1217`), used as `src` by media elements:
  - `src/shared/hooks/projects/useProjectGenerations.ts:112-114` (object and thumbnail)
  - `src/shared/hooks/variants/useVariants.ts:99,113`
  - `src/tools/video-editor/components/AgentChat/AgentTaskResults.tsx:62`
  - `src/tools/video-editor/hooks/useFinalVideoAvailable.ts:292`
- `getObject(id, byteRange)` (`generated.ts:260`, `client.ts:1207`) is used by `dataProvider.ts:1329` (`readAsset`, with a byte range) and `dataProvider.ts:157` (read). Callers of `readAsset` were not traced further.
- Likely: the hundreds of Range GETs come from `<video>`/`<audio>` elements using `objectContentUrl` (waveforms and frames). This is not confirmed by a trace.
- The 503s on object GETs cannot be traced from disk. A proxy 503 has body `code: runtime_unavailable`, while a Runtime reply has its own body, so the browser response body separates the two.
