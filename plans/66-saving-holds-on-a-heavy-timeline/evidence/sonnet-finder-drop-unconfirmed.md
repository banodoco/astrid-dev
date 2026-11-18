# Finder drop: "save never got a confirmation" (read-only trace, b38e29d06)

Method: four Haiku traces, then I re-read the load-bearing lines myself (marked VERIFIED). The clone is shallow (boundary b38e29d), so #289, bd70dacdd, 50451828e, fef9b97c8 and e8091486e are not in it. The history question is unanswered; it needs `git fetch --unshallow` in a copy.

## Facts (all paths under src/tools/video-editor/)

- Image/video drop: skeleton `uploading-*` row, `save:false`, `lib/external-drop-utils.ts:435`. A detached async block then awaits `prepareMediaImport`. Then `placePreparedAsset` commits ONCE with save:true (`useAssetManagement.ts:355-360` or `:378-382`). That commit removes the skeleton and adds the clip. VERIFIED: `useTimelineCommit.ts:431-435` bumps editSeq and emits scheduleSave, so the watchdog arms at `useTimelinePersistence.ts:1252`.
- The prepared-media handoff has no awaits and waits on no event. No SSE or events-stream ack is involved. Only the HTTP commit ack (`localSaveSession.ts:261`).
- The watchdog is disarmed only by `saveSuccess` (needs `attempt.seq >= editSeq`, `:842`) or by a terminal `failSave` (`:915`, `:891`, `:903`). VERIFIED: `setSaveStatus('retrying')` (`:981-987`) does NOT disarm it. A save that loops in retry therefore shows this banner 31.5 s later (500 + 30000 + 1000 ms).
- Authoring refusals (`refuseEdit`, e.g. "Can't drop onto a track that holds shots yet", `timelineLocalSaveHandoff.ts:~752`) are terminal. VERIFIED: `:910-919` disarms the watchdog and shows its own error banner plus a toast, or the edit is reverted. They are NOT the cause of THIS banner.

## Ranked candidates

### 1. The commit is classified "retry" and loops forever (most likely)
- `localSaveSession.ts:261-268`: any send error that is an ApiError with status >= 500, or that `classifyRuntimeCommitFailure` calls 'unknown'/'storage', becomes `{kind:'retry'}`. `commitOutbox.ts:491-493` also turns ANY throw from transmit into retry.
- `checkBasis(...)` (`:262`) runs inside the same try, so a basis/digest mismatch on the response also lands here.
- `pump` publishes `retry` and returns (`:278`). `flush` throws a plain Error (`:391`). `doSave` goes to `retrying` with `scheduleErrorRetry` (`:981-987`), looping every <= 8 s, never success and never terminal.
- Why a drop and not a move or trim: the drop is the only edit sending `clip.add-media` with media-selection and registry-entry data from the Runtime import. A server-side 5xx, or an unclassified rejection of that command (the digest gate or catalog_digest on a long-lived timeline), is a deterministic failure that this path retries.
- The Runtime is idle, so this is a fast error response, not a hang.
- Browser evidence that confirms it:
  - Network: repeated `POST /v1/projects/{id}/timelines/{tid}/commit` every 1-8 s with the same Idempotency key, returning 5xx/4xx. The body should contain `clip.add-media`. Also check whether `POST .../media-imports` succeeded earlier.
  - Console: the save badge shows "retrying", never "error".
- Absent evidence: no POST at all points to candidate 2; a single POST that never returns points to candidate 3.

### 2. Capture never settles or sticks (`localOwner.ready` / replaying)
- `useTimelineSave.ts:154-165, 337-401`: `capture` awaits `localOwner.ready`. Its IIFE awaits identity read, recover and `session.flush`. There are no timeouts. `ready` resolves only in `hold` (`localSaveSession.ts:318`).
- `append` throws "Wait for retained dependent saves…" while `replaying` (`:344`). `replaying` stays true if `prepareDisplay` throws (`:280-282`), until reload.
- A long-lived timeline with a retained earlier save in retry blocks the drop's save behind it.
- Caveat: `append` throws are wrapped as TimelineSaveError (`handoff:974`), which is terminal. Only a pure hang, a sticky `captureFailure` of a non-TimelineSaveError kind, or the retry loop yields THIS banner.
- Evidence: no commit POST after the drop. Console shows the earlier save in `retry`. Locks (`navigator.locks`) and an IndexedDB transaction pending. Clip in the editor, nothing in the network tab.

### 3. HTTP commit never settles
- `commitOutbox.ts:465`: `dispatching` stays true. Transport timeout is 30 s, so unlikely with an idle Runtime.
- Evidence: a commit request pending > 30 s.

### 4. Edit silently parked (no banner expected unless armed)
- Recovery pending (`:1179-1188`), reload pending (`:1199`), and an interaction flag stuck on after the drop (`:1231-1246`). These park before arming the watchdog or disarm it, so they fit the banner only when parked after arming. Low likelihood.

### Ruled out
- Waiting for uploads or SSE.
- A skeleton or `save:false` commit causing a seq mismatch. Those commits do not bump editSeq.
- Refusals. They are terminal, with their own banner.

## Smallest fix for #1
Candidate 1 was found by code reading only and is not reproduced.
- Make retry non-silent and bounded. In `doSave`'s generic catch (`useTimelinePersistence.ts:~981`), when the error is the "draft retained" retry from a committed outbox intent, keep `retrying` but do not leave the 'timeout' watchdog as the only signal: surface the last send error's message and status in the banner.
- To actually stop the loop, classify deterministic errors as rejected in `localSaveSession.ts:265`. Treat 4xx and the `checkBasis` failures as 'rejected', and cap 5xx retries at N (e.g. 5) before `rejected`. Then the existing terminal path (`:910-919`) shows the real reason.
- Do this only after the network evidence confirms which status the commit returned. If the status is 5xx, the fix is on the Runtime side instead.
