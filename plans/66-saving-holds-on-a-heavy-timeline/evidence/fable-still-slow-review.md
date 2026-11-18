# Release 14 on :2400: still slow, and a drop during a save fails

18 Nov 2026, 10:30 CET. Read-only: nothing was changed, restarted or written to any install. Four Haiku readers gathered facts; I re-read the load-bearing code and logs myself.

Source labels: **verified** = I read the code or log, or ran the read-only command. **Reported** = a Haiku reader's finding I did not open. **Inferred** = a conclusion from code that nobody has measured.

`sonnet-commit-profile-r14.md` had not landed when I wrote this. Question 1 is therefore answered from the old profile, the realm and the code, and its split is not measured.

## Verdict

**The remaining problem is not the commit algorithm. It is bulk media traffic that every drop starts, on a transport with nothing that bounds or survives it.**

- Each drop makes the editor download every audio source of the whole timeline again. That traffic runs through three loopback hops during the save.
- Under that load the kernel ran out of socket buffer memory (`ENOBUFS`). The Runtime treats that as fatal for the reply it is writing, so an accepted commit lost its acknowledgement and an upload's connection was cut.
- The commit's own cost is now a document-sized constant of about one to two seconds (inferred), not the 12 s the owner saw.

One correction to the evidence file: **:2400 is Vite, not the discovery proxy** (verified, `lsof`: Vite pid 56610 on :2400, proxy pid 56595 on :17500, Runtime pid 56569 on :64704). A media byte crosses three hops: browser → Vite → discovery proxy → Runtime.

## 1. Where the ~12 s go

**Verdict: not measured, and mostly not commit computation. "Well under a second" for the server's reply is not reachable by removing a constant; about one to two seconds is.**

What is ruled out (verified):
- **The O(N²) ancestry walk.** This timeline has 3 history entries in the :2400 realm (`timeline_commit_history`, read with `mode=ro`). The loop at `timeline_commit_port.py:299-306` costs about 9 entry views here. It is a real defect for long histories, not today's cost.
- **CAS re-hashing and the legacy probes.** History GETs are 3–15 ms.

What the 11.8 s contains (verified unless marked):
- It is the gap from `media.import` to the accept, so it includes the editor's work: 2.1 s to the `app_state.update`, then the 500 ms save debounce (reported).
- **A commit reply was lost.** `runtime.log` has `POST …/commit` (request `f9b658ad…`) whose reply write failed with `OSError [Errno 55]` at `server.py:464`. The commit was accepted and the editor never heard. The save then lasts until the retry replays.
- **Every mutation first makes a health call** (`client.ts:490-515`). Health runs under the outer `store._mutex` (`server.py:1554`), which the commit's port reads hold in stretches (`timeline_commit_port.py:221`). The lock is not fair, so the call can wait for most of a commit (inferred).
- **The browser allows six connections to one origin.** The commit POST, the health call and the upload queue behind media downloads (inferred; see question 2 for what starts them).

The commit's own floor (inferred from the old profile, about 1.5× profiler overhead):
- One whole-document validation pass was about 1.5 s profiled, of which one `compile_timing` is about 0.5 s.
- Each port read deep-copies its result (`timeline_commit_port.py:227`), each read scope checks every history object twice (`timeline_commit_store.py:654`, `:657`), and `_validate` digests the whole document in both preview and accept.
- So the server's reply is about 1–2 s on this document while each commit validates the whole head. Getting under a second needs validation that costs the change, not the document. That is structural, and it is the residue row Plan 18 already defers.

**"Near instant" for the owner is reachable sooner by a different route:** the edit shows at once, the save settles in the background within a second or two, and a second drop is never blocked or broken by a save. Today's failure is the last clause.

## 2. Why an upload during a save fails

**Verdict: `ENOBUFS`, not lock contention. The cause is the editor's bulk downloads; the Runtime's handling turns pressure into failures.**

Lock contention is ruled out (verified):
- The upload body is staged before any lock: `server.py:1070` reads the body through `stage_object`, and `import_media` takes `store._mutex` only afterwards (`service.py:5722`).
- The Runtime logged `request body is shorter than Content-Length` (`server.py:289`), then `BrokenPipeError` on its reply. The connection was cut on the client side, mid-body. A lock wait would have delayed the upload, not truncated it.
- "Failed to fetch" is a `TypeError`, a network failure, not an abort and not an HTTP status.

`ENOBUFS` is real on this machine (verified):
- Two replies failed with it in the same ten-minute log: the commit above and a `GET …/commits`.
- `netstat -m` shows 241,090,671 "requests for memory denied" since boot. The pool is small: `kern.ipc.nmbclusters` 65536, about 128 MB, with TCP buffers auto-sizing to 4 MB each way.
- At rest the pool is 0.5% used, so the pressure comes and goes with load.

What creates the load (verified in code, attribution inferred):
- **`AudioAnalysisProvider.tsx:150-181`, `WarmAudioCache`.** It reads the whole body of every unique audio source on the timeline, three at a time. Its effect is keyed on the set of sources, so **adding one file aborts the run and starts the whole library again**. The realm holds 558 objects, 2.2 GB.
- **`useWaveformData.ts:39`.** One whole-file `fetch` per source, including video clips with volume, held in a 64-entry cache. A failed fetch deletes its entry and is fetched again.
- These are immutable objects, and both proxy hops already mark them cacheable (`objectCachePolicy.mjs`). Large bodies still miss the browser cache (inferred), so the bytes cross all three hops again.
- Three hops means up to six kernel buffers per stream. Six streams can pin more than the 128 MB pool (inferred, arithmetic).

Why the pressure becomes a failure (verified):
- The Runtime writes replies in single 1 MiB calls, or the whole JSON body at once, on a socket with a timeout (`cas.py:15`, `server.py:464`, `:487`). Python's `sendall` does not retry `ENOBUFS`.
- `ENOBUFS` is a plain `OSError`, so `_dispatch` does not treat it as a connection error (`server.py:1574`). For a file stream it closes silently (`:1586`), so object failures leave no log line.
- **A client retry already exists and did not help.** `dataProvider.ts:1400` replays the upload once with the same key (`recoverMediaImportAfterLostAck`, `:1735-1765`). It replays straight into the same pressure.

Not proven: which hop's socket failed for the upload, and the per-request initiators. One `netstat -m` sample during a drop and one DevTools network capture settle both.

**The fix that addresses the cause: the editor fetches an object's bytes once, not once per change to the source set.** Connection limits, pooling and more retries treat the symptom.

## 3. The 503s on `/objects/`

**Verdict: the same pressure, seen at a different moment. The proxy made them, not the Runtime. Unproven until one response body is read.**

- The Runtime cannot answer 503 for an object GET on this listener (verified). Its 503 sites are commit-only (`timeline_commit_execution.py:441`, `timeline_commit_provider.py:25`, `timeline_commit_port.py:23`) or on the door listener (`door.py`), which :2400 does not use.
- The discovery proxy answers 503 `runtime_unavailable` when the upstream fails before headers (`runtime-discovery-proxy.mjs:469-471`). Vite's own failure is a 500, so a 503 came from the proxy.
- Likely upstream failures (inferred):
  - the Runtime hit `ENOBUFS` writing the headers and closed without a reply;
  - a refused or reset connect. The Runtime speaks HTTP/1.0 (no `protocol_version` in `server.py`, verified), so every request is a new connection and a new thread, against a backlog of 64.
- **One mundane cause to exclude first:** the tab may have been open across the 10:05 rebuild. The log shows two Runtime boots, and every object GET during a restart is a proxy 503.
- The proxy's error line names the code and in-flight count (`:470`), but the launcher pipes it and nothing writes it to disk. That is why this cannot be answered from logs.

## 4. Is this something deeper?

**Yes, and it is the same habit one layer down. Plan 18 Phase 0 does not cover it.**

- Phase 0's root is "nothing treats an accepted head as settled". Here **nothing treats fetched bytes as settled**: content-addressed, immutable objects are downloaded again on every change.
- Phase 0 bounds a commit's *computation* by counts (CC-1, CC-2). Nothing bounds the *transport* an edit causes, and nothing says an upload is independent of a save.
- Searched (reported, with my spot checks of `plans/18-timeline-editing/`): astrid-dev `origin/main` has no mention of `ENOBUFS`, `/objects/` load, the server's thread model, the proxy, or media fetching. Plan 59 covers import admission, not transport. `gh` is not installed, so GitHub issues were not searched.
- Phase 0's "deferred" table covers the poll rate and the sub-second residue only (`inputs.md:89-94`).

## 5. What I would do

### Now, on the Release 14 fix branches

Three changes, each removing a cause, plus the measurement that today's report lacked.

| # | Repo | Change | Where |
|---|---|---|---|
| 1 | App | Warm each object URL once per session. Keep the warmed set at module level, fetch only new URLs, and do not abort a run because the set grew. | `src/tools/video-editor/compositions/AudioAnalysisProvider.tsx:150-181` |
| 2 | Runtime | One write helper for both reply paths: write in 64 KiB pieces and, on `ENOBUFS`, wait for the socket to be writable and continue, inside the existing 30 s timeout. An accepted commit must not lose its reply to a transient condition. | `runtime_protocol/server.py:464` (`_send`), `:487` (`_send_file`) |
| 3 | Runtime | Serve health without `store._mutex`, as the identity probe already does. A save must not delay the fence in front of every other mutation. | `server.py:1520-1554`; caller `editor/src/integrations/runtime/client.ts:490-515` |
| 4 | Runtime, App | Make the next report measurable: log `timeline_commit_timing` for every commit (it is computed, then dropped below DEBUG), timestamp `runtime.log` lines, and write the proxy's stderr to `logs/editor.log`. | `timeline_commit_execution.py:165-178`; `editor/scripts/dev-local-workspace.mjs:811-817` |

Proof, by count, not by clock:
- App: adding one source to a timeline with N warmed sources starts exactly one warm fetch.
- Runtime: a reply written to a socket that raises `ENOBUFS` twice is delivered whole.
- Live, as evidence: one drop, then a second drop during the save, on :2400. Record the `timeline_commit_timing` line, `netstat -m` before and during, and the browser's "stalled" time for the commit POST.

Before change 1, spend ten minutes on the DevTools capture (initiator and `Range` per object GET). If warm-up is not the bulk of the traffic, change 1 moves to whichever caller is.

**Not now:** a proxy concurrency limit, connection pooling or keep-alive, another upload retry (one exists), a larger backlog, or a waveform cache size. Each is a second mechanism around the cause.

### In the follow-up plan (Plan 18 Phase 0, two additions)

- **Statement (g), bounded transport.** An edit causes transport proportional to the change: adding one object reads that object's bytes and no others. Held by a count of object GETs per gesture on the corpus, in CC-1's ratchet file. An upload does not wait on, and cannot be failed by, a commit in flight.
- **Under (a), the sub-second residue, now with a named shape.** Validation that costs the change, not the document; one copy and one digest per commit; the ancestry walk at `timeline_commit_port.py:299-306` made linear. Start from the r14 profile.

Filed as issues, not planned:
- Waveforms download whole media files to draw a few hundred points. Peaks belong beside the object as derived data.
- The local install proxies twice (Vite, then the discovery proxy). One hop halves the buffers.
- Object reads and uploads share the commit's `store._mutex` for their metadata (`service.py:6023`, `:5373`, with an `fsync` inside the second).
- A failed object stream logs nothing (`server.py:1586`).

## 6. The stuck editor after the second drop

**Verdict: yes, the same deeper issue, in two halves. The fix plan on `release/14/save-recovery` is right in direction. Two of its four items should be made at the rule, not at the site, and one thing is missing.**

How the owner got stuck (verified in code; the IndexedDB rows are the main thread's):

1. **The Runtime refused a correct save.** `timeline_commit_port.py:1061` sets `catalog_digest = digest(record)` over the whole selected-media record. That record includes `managed_output.lifecycle`, `durability` and `provenance` (`:1047-1051`), which move after an import settles. So a fresh drop's selection can stop matching by itself (`:1065`). The bytes are already checked one line earlier (`:1058-1060`). This is the habit Phase 0 names: a guard signed by more than it depends on.
2. **The App retried it for ever.** The refusal is an untyped 409. `classifyRuntimeCommitFailure` returns `unknown` for it (`client.ts:337-345`; its comment keeps "409 (untyped head contention)" retryable), and `localSaveSession.ts:275` maps `unknown` to `retry`. The same bytes go back and are refused again.
3. **The next edit threw an internal state at the user.** While the retained owner replays, `append` throws "Wait for retained dependent saves to finish revalidation" (`localSaveSession.ts:353`). The line above throws "Resolve retained local saves" (`:351`).
4. **Discard did nothing.** `discharge` returns early unless the outcome is `rejected` (`localSaveSession.ts:413`). Both retained owners are `retry`, so no button can remove them.
5. **A third store drew the banner.** "You have unsaved changes from 10:16" comes from `chrome.recoveryDraft` (`TimelineEditorShellCore.tsx:883-893`), which is the draft store, not the outbox. Clearing one leaves the other.

So the owner's "poor structure" is accurate: **one fact, "this change is not saved yet", is held by the outbox owners, the local save session and the draft, and each has its own way out.**

The fix plan, item by item:

| Planned | Call | Why |
|---|---|---|
| Guard scoped to identity and bytes | **Keep** | Sign object digest, size, media type and variant id. Lifecycle fields leave the signature. No second guard. |
| A 409 is never retried with the same bytes | **Keep, at the classifier** | Change the rule in `client.ts:322-345`, not the session: retry only a transport failure or a reason typed retryable (`head_busy`, `runtime_unavailable`). `stale_head` stays a rebase. Every other 4xx is `rejected`. |
| One recovery surface from the first occurrence | **Keep** | It must replace the two throws at `localSaveSession.ts:351` and `:353`, not sit beside them. |
| Discard clears every retained owner | **Keep, make it total** | Remove the outcome-kind condition at `:413`, cover every owner in the scope, and clear the draft in the same action. Otherwise the banner returns on reload. |

Missing: **owner `d38698ba`.** It has no commands and a basis of `txn-72383d4f`, two heads back. Retrying it is correct for a transport failure, but it will come back `stale_head`. Check that it rebases to nothing and is dropped. An owner with no commands should not be retained at all.

Proof, one table-driven test: for each outcome kind (`retry`, `rejected`, conflict) and for one and two retained owners, Discard leaves a clean state, the next edit saves, and the same holds after a reload.

**What Plan 18 CC-5 needs to absorb:**

- **Discharge is total.** Any change that is not accepted can be discarded, whatever its outcome kind, across every owner in the scope, in one action. Today CC-5 says "a refusal can always be discharged"; a `retry` is not a refusal, and that gap is this bug.
- **One home for unsaved state.** The outbox record is the fact. The recovery banner and the draft display are read from it. CC-5 keeps "one `after` per owner for the reload display" until TL-5; that display must be derived, not a second store with its own Retry and Discard.
- **`append` never throws for a state reason.** CC-5 already deletes two throws (`localSaveSession.ts:364`, `commitOutbox.ts:496`). Add `:351` and `:353`.
- **CC-4:** an untyped 409 is not retryable. This is the same closed list; the "untyped contention" exception goes.
- **CC-3 or CC-6:** the catalog digest joins the "signature is everything the finding depends on, and nothing else" rule, with a corpus case of a selection whose lifecycle advanced.

## Not checked

- The stuck state was read from code and the main thread's IndexedDB rows. I did not reproduce it or read the fix branch.
- No change was prototyped. No request was sent to :2400. The owner's tab was not inspected.
- The split of the 11.8 s between browser queue, lost reply and server work. The r14 profile and the timing log line give it.
- Which caller produced most of the 953 requests, and whether the 503s fall in the restart window.
- That six streams over three hops exhaust the mbuf pool. It is arithmetic on the sysctl values, supported by the logged `ENOBUFS` and the denied-request counter.
- GitHub issues.
