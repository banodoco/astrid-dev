# Save failures on "Almost Ready": evidence pack

18 Nov 2026. Read-only. Nothing installed, changed, restarted, committed or published. Timeline `77f906f3242c48179ab86ca7c3e62eb4`, project `801a01b3a87941a1ab25958c488afdbf`.

**Code under test (the install on :2400):** editor `~/astrid-release/release-14-plan-59/editor/src` (App `fbb8168bd` per QUEUE); Runtime `program/versions/fdbff077811b/py/lib/python3.11/site-packages/runtime_protocol` (Runtime `d725811`, per `runtime.lock.json`); Agent `…/site-packages/astrid` (Agent `458d9d51`). Line numbers below are the install's. The live-check file cites lines from the older Runtime `519b404` and App `b38e29d`, so its numbers differ.

**Labels.** **verified** = I read the code, the data or the log today. **reported** = from a review file, not re-checked. Where a claim is mixed, each part is labelled.

## 0. Sources

| Source | Status |
|---|---|
| `live-check-almost-ready.md`, `sonnet-commit-profile.md`, `near-instant-facts.md`, `plan-near-instant-commits.md` | read |
| `fable-near-instant-review.md`, `opus-r14-set-review.md`, `opus-396-review.md` | read |
| `r14-slow-save-evidence.md`, `QUEUE.md` | read |
| `save-state-map.md` | **absent** (not in `plan-review/`) |
| `sonnet-commit-profile-r14.md` | **absent**; `fable-still-slow-review.md` says it had not landed |
| `fable-still-slow-review.md` | not in the list, but on the same question and read (labelled as reported where used) |
| Plan 18 (`plan.md`, `tasks.md`, `inputs.md`, `statements.md`, `handover.md`) | read after `git pull --ff-only` in `~/Developer/astrid-dev` (10 files changed; Plan 18 is `queued`; every CC/TL task is unchecked) |
| Issue titles (GitHub API, unauthenticated, read today) | #826, #846, #847, #732, #842, #839, #838, #851, #852, #853, #854, #769, #720, #393 read. `gh` is not installed. |

Issue search (GitHub API, read today): no issue matches `ENOBUFS`, `unsaved changes` or `protocol_error inputs changed` as a title term. `#635` ("Timeline imports reject valid exported shots with divergent media alternatives") matches "catalog digest". It may be related, but this is unverified. `#869` matches "catalog association" and is about a publish script, so it is not this bug. Some searches were rate-limited (`Wait for retained`, `object 503`). Those two are not searched.

## 1. Incidents

Each incident gives the user-visible text, the trigger, the state record, the raise and classify sites, the store that holds the stuck state, the way out, today's fix status and the Plan 18 task.

### I-1. Saves take 176–187 s (then ~12 s)

- **Text:** "Your changes have not been saved: the save never got a confirmation." (`editor/src/tools/video-editor/components/TimelineEditorShellCore.tsx:816`, verified). Badge "Saving" for ~3 min, then "Saved" (reported, live check).
- **Trigger:** any commit. The first POST is cut at exactly 60 s (Chrome 503, "Failed to fetch"). The Runtime accepts the commit 2–3 min later. A same-key retry gets a 200 replay in 16–30 s (reported, live check).
- **Cut sites (verified):** `editor/config/vite/runtimeProxy.ts:7,32-33` (`RUNTIME_REQUEST_TIMEOUT_MS = 60_000`); `editor/scripts/runtime-discovery-proxy.mjs:14` (`IDLE_TIMEOUT_MS = 60_000`), with a timeout mapped to 504 at `:471`.
- **Classify (verified):** a non-`ApiError` (the `Failed to fetch` `TypeError`) returns `'unknown'` at `integrations/runtime/client.ts:323`. `localSaveSession.ts:275` maps `unknown` to `retry`, and the same key is re-sent.
- **Cost (reported):** profiled add-media commit 187 s uncontended. CAS re-hash ~190 of 280 profiled seconds; legacy timing probes ~80 s (`sonnet-commit-profile.md`). History GET 8.7–8.8 s, holding `store._mutex` (reported).
- **After today's fixes (reported):** 11.8 s from `media.import` to accept, and history GETs at 3–15 ms (`r14-slow-save-evidence.md`). The realm rows are present: `txn-918889d2…` "Add media" and `txn-76e8a3e2…` "Edit timeline" are in `timeline_commit_history` for this timeline (verified). Their timestamps are reported.
- **State record:** Runtime timeline history (accepted, idempotent). Editor outbox owner in IndexedDB `astrid.command-outbox`, holding the pending intent with its key (reported, live check).
- **Stuck store:** the outbox (retry lane) and the badge. The tab shows "never got a confirmation" until a replay lands.
- **Way out:** yes, but only by waiting. The retry replays and the badge turns Saved. Closing or reloading before that loses the ack, and the replay is what makes the save look real (reported).
- **Fix status:** Runtime #59 is in the install (verified: `store.py:1087` `verified_cas`; `service.py:6036-6038`; `timeline_commit_store.py:461` `_confirm_object`). Agent #394 is in (verified: `_timing_evaluators.py:283` `evaluate(collect=…)`). Agent #396 is partly in: a per-commit `memo` parameter at `astrid/sdk/timeline/commit.py:432`, but the process-level `_RESERVED_HISTORY` memo is absent (verified, count 0). App #294–#297 are reported as merged to plan-59. The 60 s proxy cut, the cut-then-retry loop and the 12 s residue remain (verified).
- **Plan 18:** CC-1, CC-2 (counts, open). TL-5 (send and adopt, open). Plan 18 does not name the 60 s cut or the proxy (see §3).

### I-2. Runtime 400 `protocol_error: accepted commit inputs changed during verification` makes a permanent "rejected"; the tab sticks

- **Text (live check, reported):** banner "protocol_error: accepted commit inputs changed during verification", badge "Error", card "This timeline changed somewhere else" with [Use latest version] [Keep my changes]. Outbox outcome `{"kind":"rejected","error":{"kind":"validation",…,"code":"protocol_error"}}`.
- **Trigger (reported, live check):** the editor's retry overlapped a POST still running in the Runtime, after the 60 s cut. The Runtime's verification guard raised. The live check's update also covers the inspector: a typed "100" sent `x: 1` first, and the follow-up overlapped (see I-10).
- **Raise sites, old build (reported):** `timeline_commit_store.py:200,219,255` in `519b404`, as a 400 `ProtocolError`.
- **Raise sites, install (verified):** `timeline_commit_store.py:68-71` `_head_busy()` returns `HeadBusyError` with the same text. It is raised at `:219, :238, :274, :453, :660`. `errors.py:88-98`: `HeadBusyError(ProtocolError)`, `status = 409`, `details.reason = "head_busy"`. The 400 for the inputs-changed condition is gone in the install. The 400 `ProtocolError("accepted commit object changed during verification")` still exists at `:269, :487, :536, :704, :713`. That is the integrity case, and it is non-retryable.
- **Classify, install (verified):** `integrations/runtime/client.ts:326` maps `reason === 'head_busy'` to `'unknown'`, so it is retried. The old path (400) was `validation`, so `rejected` (`client.ts:333`, and `localSaveSession.ts:275` maps it to `rejected`).
- **State record:** IDB `astrid.command-outbox` owner record with `pending.outcome` and `intent.conflict` (`commitOutbox.ts`, reported at 517–527). The banner reads `chrome.recoveryDraft` (see I-6).
- **Stuck store:** the outbox owner (rejected), plus the one-slot draft.
- **Way out, old build (reported):** none. Neither button cleared it, and the tab could not close (`beforeunload`).
- **Way out, install (verified in code, not run):** `localSaveSession.ts:408-413` `discharge(mode)` returns early unless outcome is `rejected`, so it works for this outcome. Both buttons reach it: "Keep my changes" calls `retrySaveAfterConflict` → `discharge('keep')` (`useTimelinePersistence.ts:1791-1802`), and "Use latest version" calls `reloadFromServer({discardRefusedSave:true})` → `discharge('latest')` (`:1642`). The `head_busy` change means the condition should no longer produce a permanent rejection. Not reproduced in a browser.
- **Fix status:** Runtime #59 (`head_busy` return) is in the install (verified). The App-side discharge is in the install (verified). Reported: #295's `rebaseRejected` path. Verified: `localSaveSession.ts:173-178` rebases on `latest.head` automatically.
- **Plan 18:** CC-4 (`head_busy` as the one retryable reason; logging the moved component), CC-5 (discharge, two-button table). Both are open.

### I-3. "The file was not added to the timeline. The timeline or track changed while the file was uploading."

- **Text:** the exact string is **not in the install** (verified: grep over `editor/src`). Closest real text: `"The file was not added to the timeline. " + DECLINED_DETAIL[reason]` (`hooks/useAssetManagement.ts:171-181`, `fileNotAddedMessage`), with reason `shot-changed` → "The shot changed while the file was uploading." (`useAssetManagement.ts:330`). The "track" wording is `preserved_track_unavailable` → "That track is no longer available." (`:171-180`). The owner's wording may come from another build or from a rewrite.
- **Trigger:** a head or shot-composition change during the upload. The check at `:330` compares `current.head.headRevisionId` and related fields with the composition (verified). The comment at `:333-335` says whole-state equality "is not the edit's business".
- **Raise and classify (verified):** `:330` `decline('shot-changed', …)`. It is a local decline, with no POST. The toast is built by `fileNotAddedMessage` (`:181`).
- **State record:** none (refused before commit). The uploaded object may exist: `object.ingest` in the realm (reported).
- **Stuck store:** none.
- **Way out:** re-drop. The toast says nothing about what to do (verified).
- **Fix status:** the OR-chain at `:330` is still present (verified). Reported: #296 "drop placement" split the OR-chain into named reasons and is merged to plan-59. It does not appear to cover this branch. Unresolved.
- **Plan 18:** CC-4 (one named reason per refusal), TL-10 (drop writers). Both open.

### I-4. "This change was not saved. Local document save retained: original verified authoring head is unavailable"

- **Text (verified):** `useTimelineSave.ts:938` prefixes "This change was not saved. "; `timelineLocalSaveHandoff.ts:246` prefixes "Local document save retained: ".
- **Raise sites (verified):** `timelineLocalSaveHandoff.ts:266` (`TimelineVersionConflictError`, when the verified head moved to a different revision or publication) and `:268` (`refuse(…)`, generic, when the head pair is missing). Both are in `checkHead` (`:254-270`). Other callers: `shared/lib/placement/placementService.ts:132,151`.
- **Trigger:** a retained local save whose verified head no longer matches the canonical document. Typical: a second tab or an agent write moved the head, or the head pair was never recorded.
- **State record:** the local document held by `localSaveSession.ts:109` (a session copy), the IDB draft, and the outbox owner.
- **Stuck store:** the session document and the draft. `reloadFromServer` does not reset the session document (reported, from `near-instant-facts.md` section on the stuck state).
- **Way out:** none verified. The message names no action. Discard in the recovery banner clears the draft only (see I-6).
- **Fix status:** none in the install.
- **Plan 18:** CC-5 (delete `LocalSave.before` and the equality check at `localSaveSession.ts:371`), TL-5 and TL-12 (the handoff is replaced). Coded reason: CC-4 and TL-4.

### I-5. "This change was not saved. Local document save retained: Wait for retained dependent saves to finish revalidation before editing again"

- **Text (verified):** the wrapped form, as above. Raised at `localSaveSession.ts:353` (verified, in `append`).
- **Trigger (reported):** the owner edits while a retained dependent suffix is replaying after a reload (`replaying` is set). Reported from `fable-still-slow-review.md`.
- **Raise and classify (verified):** `:353` throws a plain `Error`. The handoff wraps it at `timelineLocalSaveHandoff.ts:980` into "Local document save retained: …". `:350` ("Resolve retained local saves") is the sibling throw, and it is also a plain `Error`.
- **State record:** the outbox owner's retry-lane intents. Discard returns early because the outcome is not `rejected` (`localSaveSession.ts:413`, verified).
- **Stuck store:** the outbox owner and `localSaveSession` state.
- **Way out:** none in code (verified). The reload path does not clear retry-lane owners. "Reports no actions" is reported from `fable-still-slow-review.md`.
- **Fix status:** none.
- **Plan 18:** CC-5 deletes the throws at `localSaveSession.ts:364` and `commitOutbox.ts:496`. **`:350` and `:353` are not in CC-5** (verified: `Wait for retained` appears nowhere in Plan 18). This is a gap.

### I-6. After a refresh: "You have unsaved changes from 10:16 AM", with Discard that leaves the tab errored

- **Text (verified):** "You have unsaved changes from {time}." with buttons **"Save them"** and **"Discard"** (`components/TimelineEditorShellCore.tsx:883-897`). The owner's report says "Retry". The install's button is "Save them". Recorded as a discrepancy.
- **Trigger:** a refresh while the outbox or the draft holds a retry-lane change.
- **State record:** two stores. The banner reads `chrome.recoveryDraft` (IDB `astrid.timeline-drafts`, keyed by timeline id: `data/timelineDraftIndexedDb.ts:13,18,118-119`, verified). The outbox is IDB `astrid.command-outbox` (`commitOutbox.ts:115`, verified). `localSaveSession.ts:334-337,345` reads the outbox and publishes `recovery`.
- **Discard:** `discardRecoveredDraft` removes the draft only. The outbox owner stays. The next edit then throws (`:350` or `:353`), so the tab shows Error (verified by code path; reported as observed).
- **Way out:** partial. Discard removes one store. "Discard" for a retry-lane owner does nothing to the outbox (`localSaveSession.ts:413`).
- **Fix status:** none.
- **Plan 18:** CC-5 (discard total; the test table refuse, edit, Discard, reload for every gesture kind; "one home for unsaved state" in statements). Open.

### I-7. 409 "selected media catalog digest changed" retried forever

- **Text:** Runtime message "selected media catalog digest changed", `code: conflict`, status 409. The editor's user-visible text was not reproduced. The retry lane shows the I-1 banner (reported).
- **Raise (verified):** `timeline_commit_port.py:1065` `raise ConflictError("selected media catalog digest changed")`. The digest is `record["catalog_digest"] = digest(record)` at `:1061`. The record includes `managed_output` fields `durability`, `lifecycle` and `provenance` (`:1047-1051`). Those move after an import settles (reported, `fable-still-slow-review.md`).
- **Classify (verified):** `client.ts:322-345`. An `ApiError` with status 409, no typed `reason`, no `details.status`. It is not `conflict` (`details.status` absent), and 409 is excluded from the `rejected_request` branch. It falls through to `return 'unknown'` at `client.ts:344`. `localSaveSession.ts:275` retries. The same bytes are sent again.
- **State record:** the outbox intent (retry lane). Same key, same body.
- **Stuck store:** the outbox owner.
- **Way out:** none. Discard does nothing for retry-lane owners (`localSaveSession.ts:413`, verified).
- **Fix status:** none in the install.
- **Plan 18:** CC-4 ("an untyped 409 is not retryable"). Plan 18 does not contain the words "409" or "catalog digest" (verified). The digest-as-signature rule (lifecycle fields out of the guard) is not named in CC-3 or CC-6. This is a gap.

### I-8. "Failed to save asset / Failed to fetch" on a second drop during a save

- **Text (verified):** toast "Failed to save asset" with description = the error message (`hooks/useExternalDrop.ts:704`). The message is "Failed to fetch" (`TypeError`), from `importProjectMedia` (reported stack: `generated.ts:745`).
- **Trigger (reported, owner, 10:08 CET):** a second drop while the first save is in flight.
- **Runtime side (verified):** `runtime.log` (`home/Library/Logs/Astrid Runtime/runtime.log`, release-14 home) line 51–52: `ProtocolError: request body is shorter than Content-Length` (`server.py:289` per reported stack). The upload body was cut mid-stream. Also `OSError [Errno 55] No buffer space available` at `server.py:464` (see I-13).
- **Proxy side (verified):** a proxy error before headers returns 503 or 504 JSON (`runtime-discovery-proxy.mjs:469-471`). After headers, the client socket is destroyed, which the browser shows as "Failed to fetch" (reported, `r14-slow-save-evidence.md`).
- **Amplifier (reported):** `AudioAnalysisProvider.tsx:150-181` fetches every audio source whole, three at a time (verified). It restarts when the source set changes (verified). See I-14.
- **State record:** none for the failed drop. The realm has no `object.ingest` or `media.import` row between `09:08:00.982` and `09:09:56.977` (reported; the first drop's rows are verified).
- **Stuck store:** none. The placeholder "uploading:…" clip stays on the track (reported).
- **Way out:** one automatic replay (`dataProvider.ts:1400`, `recoverMediaImportAfterLostAck` at `:1735`, verified) with the same key. Reported: it replays into the same pressure.
- **Fix status:** none.
- **Plan 18:** none. The transport statement is proposed only in `fable-still-slow-review.md` ("statement (g)"). It is not in `tasks.md` (verified).

### I-9. Two tabs on one origin share the draft slot and block each other

- **Text (verified):** the second tab shows I-6's banner and a red "Error" badge (reported, live check).
- **Trigger:** a second tab opens the same timeline while the first is editing.
- **Raise and classify (verified):** `hooks/useTimelinePersistence.ts:1174-1187`. When `recoveryPendingRef` or `recoveryActiveRef` is set, edits are deferred in memory, and no POST is sent until the user picks Save them or Discard.
- **State record:** IDB `astrid.timeline-drafts`, one slot per timeline (`timelineDraftIndexedDb.ts:13,18,118-119`). The same DB is shared by every tab on one origin. The owner's live tab holds the `astrid.command-outbox` Web Lock (reported, live check).
- **Stuck store:** the shared draft slot.
- **Way out:** Save them (re-commits the other tab's draft) or Discard (deletes it). Neither is right while the other tab is alive (reported). Both are destructive.
- **Fix status:** none.
- **Plan 18:** CC-5 ("two tabs on one timeline; if two tabs still block each other, key the draft slot by owner id here", verified in `tasks.md`). Planned, not started.

### I-10. Inspector fields commit on every keystroke

- **Text:** none. The symptom is a commit storm.
- **Trigger:** typing in Position X or a timing field.
- **Raise sites (verified):** `components/PropertiesPanel/ClipPanelBody.tsx:437-439`. Position X is `NumberInput` with `onChange={(value) => { if (value !== null) onChange({ x: value }); }}`. Timing fields call `onChange({[field]: value})` on every change (`:153-157`, `handleTimingValueChange`). Both fire per keystroke (verified by reading).
- **State record:** each keystroke is a separate intent in the outbox (reported, live check: "x=1" committed first, x=10 and x=100 queued behind it).
- **Stuck store:** the outbox, with overlapping POSTs (feeds I-2).
- **Way out:** none specific. The field showed 1, not 100 (reported).
- **Fix status:** none. `near-instant-facts.md` decided "no inspector change now", and `fable-near-instant-review.md` (A3) proposed `onValueCommitted` for Position fields. Not applied.
- **Plan 18:** TL-7 converts "inspector scalars" (open). The Plan 18 text has no debounce or commit-on-blur rule (verified: no `onValueCommitted`, `keystroke` or `debounce` in the plan files).

### I-11. Moving a VO clip with a legacy `gap_after_s` is refused

- **Text (verified):** `unsupported timing declaration ('parent','','vo-N19-0').gap_after_s`, raised as `TimingCompileError` at `astrid/sdk/timeline/_timing_evaluators.py:518` (the message is built around it).
- **Trigger:** a move of a clip whose row carries a `gap_after_s` declaration. The old signature was the whole row minus `params` (reported, `near-instant-facts.md`).
- **Fix in the install (verified):** `_commit_timing_validation.py:571` now signs `json.dumps(declarations[name])`, the declaration's own value, and the findings go through `split_findings` (`:586`). An unchanged declaration on a move no longer blocks. Not run.
- **State record:** none. A refused edit. The editor undoes it.
- **Way out:** the change is undone. The clip stays in place (reported, `sonnet-commit-profile.md`).
- **Fix status:** Agent #394 is in the install (verified). Reported: the probe fault is still open for `gap_after_s` (`fable-near-instant-review.md`).
- **Plan 18:** CC-3 (R5: signed by its own value, in the delta gate). CC-7 (corpus gains `gap_after_s`). Open.

### I-12. Half catalog associations: written by the editor, refused by readers

- **Text (verified):** `catalog association requires both generation and variant` (`astrid/sdk/timeline/native_media_admission.py:65`, a `CommandError`). The check is `split_findings(incomplete(candidate), incomplete(base))` (`:63-64`), so it blocks only introduced half associations.
- **Writer (verified):** `editor/src/tools/video-editor/lib/shot-group-pack-commands.ts:189-190` sets `copiedEntry.generationId = replacement.generationId ?? …` and `variantId` separately. A `generationId` without a `variantId` is possible. The QUEUE's line citation (189-190) matches.
- **Trigger:** a pinned-group or shot-group copy whose replacement has a generation but no variant. Also a variant-less image on a pinned group (reported, `fable-near-instant-review.md` F294-1).
- **State record:** the registry entry, written to the head by the writer. The reader refuses on the next edit that touches it.
- **Stuck store:** the head's registry entry plus the outbox.
- **Way out:** none verified. Reported: `near-instant-facts.md` says the Agent refused it since #393.
- **Fix status:** reader side #393 is merged (reported, Plan 18 `inputs.md`; the split-findings gate is verified). Writer side is open (verified: `shot-group-pack-commands.ts:189-190`). Reported: App #294 "both ids or neither" in its planner; the comment at `useAssetManagement.ts:340` is verified.
- **Plan 18:** CC-6 (writers cannot store what readers refuse; `admit_registry_entry` and `admit_catalog_association`). Open. Plan 18 does not name `shot-group-pack-commands.ts` (verified).

### I-13. An accepted commit loses its reply (`ENOBUFS`), so the editor never hears

- **Text (verified in the log):** `Runtime internal error (request f9b658ad…, POST …/timelines/77f906f3…/commit)` with `OSError: [Errno 55] No buffer space available`. User-visible: "the save never got a confirmation" (I-1).
- **Raise (verified):** `server.py:464` `self.wfile.write(encoded)` in `_send`. The error propagates through `_dispatch` (`server.py:1565`). `_send_file` writes at `:487`. There is no retry on `ENOBUFS`.
- **Trigger:** kernel socket buffer pressure. `netstat -m` showed 241,090,671 denied requests since boot (reported, `r14-slow-save-evidence.md` / `fable-still-slow-review.md`).
- **State record:** the commit is accepted (the realm has the row; the request id is not stored in the realm, reported).
- **Stuck store:** the outbox (retry lane) on the editor side.
- **Way out:** yes. The same-key retry replays (reported).
- **Fix status:** none. The proposed fix (write in 64 KiB pieces, wait on `ENOBUFS`) is in `fable-still-slow-review.md` only.
- **Plan 18:** none (see §3).

### I-14. Object GETs `/objects/` return 503 and media loads stall

- **Text:** no visible text (reported, console silent).
- **Raise (verified):** the discovery proxy answers 503 `runtime_unavailable` when the upstream fails before headers (`runtime-discovery-proxy.mjs:469-471`). The Runtime's 503 sites are commit-only (reported).
- **Trigger (reported):** `WarmAudioCache` (`AudioAnalysisProvider.tsx:150-181`) and `useWaveformData.ts:39` fetch every whole source. `r14-slow-save-evidence.md` counted ~953 `/api/` requests, most `GET /v1/objects/…`, a large share 503 (reported). Possibly the restart window (reported).
- **State record:** none.
- **Stuck store:** none.
- **Way out:** none specific; media stays unplayed until reload (reported).
- **Fix status:** none.
- **Plan 18:** none. The proposed statement (g) on bounded transport is not in `tasks.md`.

### I-15. Save badge stuck on "Saving" after a refusal with nothing in flight

- **Text:** badge "Saving" for ~40–50 s after a refused Picture-track move, then "Saved" (reported, live check row 11). The refusal toast is verified: "Not saved: Can't change a clip on, or move one onto, a track that holds shots yet. Use another track. That change was undone; your other edits are kept." (`timelineLocalSaveHandoff.ts:172`, verified).
- **Trigger:** the refused move (a Picture-track refusal, `timelineLocalSaveHandoff.ts:172`).
- **Stuck store:** the badge state, which is not the outbox (reported).
- **Way out:** the next edit clears it (reported).
- **Fix status:** none. Code path not traced.
- **Plan 18:** TL-4 ("save status becomes `{status:'error', reason}`"). Open.

### I-16. A stale retained owner from an earlier session is never retried and never dropped

- **Text:** the I-6 banner (reported).
- **Trigger:** an earlier session's tab left a pending `doc.patch` "Edit timeline" against the bootstrap head (owner `d38698ba`, generation 10, on `127.0.0.1`). `near-instant-facts.md` and `fable-still-slow-review.md` report it. QUEUE reports 34 owner records there, 33 empty.
- **State record:** IDB `astrid.command-outbox` on origin `127.0.0.1:2400` (reported).
- **Way out:** Discard (retry lane: no effect, `localSaveSession.ts:413`, verified). Reported: an owner with no commands should not be retained (`fable-still-slow-review.md`).
- **Fix status:** none.
- **Plan 18:** none explicit. CC-5's "discard total" covers it in principle. The "no empty owner is retained" rule is not in `tasks.md` (verified).

## 2. Cross-cut table

Marks: ✓ = the class applies; – = it does not; "~" = partly.

Classes: **(A)** a guard over more than the change depends on. **(B)** the client's classification does not match the server's meaning. **(C)** save state held in more than one place, or more than one UI surface. **(D)** no way out (no dischargeable outcome). **(E)** commit or IO work not bounded by the change size. **(F)** resource or transport limits (connections, buffers, the proxy).

| # | Incident (short) | A | B | C | D | E | F |
|---|---|---|---|---|---|---|---|
| I-1 | 176–187 s saves, 60 s cut | ✓ | – | ✓ | ~ | ✓ | ✓ |
| I-2 | 400 "inputs changed" → permanent rejected | ✓ | ✓ | ✓ | ✓ | – | ✓ |
| I-3 | Drop refused: shot/track changed | ✓ | ✓ | – | – | – | – |
| I-4 | "original verified authoring head is unavailable" | ✓ | ✓ | ✓ | ✓ | – | – |
| I-5 | "Wait for retained dependent saves…" | – | ✓ | ✓ | ✓ | – | – |
| I-6 | "You have unsaved changes…", Discard does nothing | – | ✓ | ✓ | ✓ | – | – |
| I-7 | 409 catalog digest retried forever | ✓ | ✓ | – | ✓ | – | – |
| I-8 | "Failed to save asset / Failed to fetch" | – | – | – | ~ | – | ✓ |
| I-9 | Two tabs share the draft slot | – | ✓ | ✓ | ✓ | – | – |
| I-10 | Inspector commits per keystroke | – | – | – | – | ✓ | ✓ |
| I-11 | VO move refused for `gap_after_s` | ✓ | ✓ | – | – | – | – |
| I-12 | Half catalog association | ~ | ✓ | – | – | – | – |
| I-13 | Accepted commit loses its reply (ENOBUFS) | – | – | ✓ | – | – | ✓ |
| I-14 | `/objects/` 503s, whole-file fetches | – | – | – | – | ✓ | ✓ |
| I-15 | Badge "Saving" after refusal | – | – | ✓ | – | – | – |
| I-16 | Stale retained owner | – | – | ✓ | ✓ | – | – |

**Recurring classes:** (D) appears in 9 of 16 incidents, and (C) in 9. (B) appears in 8 of 16, and it is the cause of the stuck states: a retryable condition classified as permanent (I-2), or an untyped 409 classified as retryable (I-7). (A) appears in 6, mostly as a whole-document or whole-row guard. (F) appears in 5. (E) appears in 3.

## 3. Plan 18 coverage

| Incident | Plan 18 task | Status |
|---|---|---|
| I-1 | CC-1, CC-2 (counts, open); TL-5 | open. Not covered: the 60 s proxy cut, the cut-then-retry loop, the reply loss (I-13). |
| I-2 | CC-4 (`head_busy`), CC-5 (discharge) | open |
| I-3 | CC-4, TL-10 | open |
| I-4 | CC-5 (equality check at `localSaveSession.ts:371`), TL-5, TL-12 | open |
| I-5 | CC-5 deletes `:364` and `commitOutbox:496` only | **gap: `:350` and `:353` not named** |
| I-6 | CC-5 ("discard total", two tabs, refuse/edit/Discard/reload) | open |
| I-7 | CC-4 ("untyped 409 is not retryable") | open. **Gap: the catalog digest rule is not in CC-3 or CC-6.** |
| I-8 | none | **gap** |
| I-9 | CC-5 (draft slot keyed by owner id, if needed) | open |
| I-10 | TL-7 (inspector scalars) | partial: no commit-on-blur or debounce rule |
| I-11 | CC-3 (R5), CC-7 (corpus with `gap_after_s`) | open |
| I-12 | CC-6 | open. **Gap: `shot-group-pack-commands.ts:189-190` not named.** |
| I-13 | none | **gap** (proposed only in `fable-still-slow-review.md`) |
| I-14 | none | **gap** (statement (g) proposed only, not in `tasks.md`) |
| I-15 | TL-4 (save status as `{status:'error', reason}`) | open |
| I-16 | CC-5 (in principle) | **gap: "no empty owner is retained" is not in `tasks.md`** |

Also: Plan 18 contains no "409", "ENOBUFS", "Failed to fetch", "catalog digest", "keystroke", "debounce" (except the 500 ms editor floor in `inputs.md`), "Wait for retained" or "Retry save". The plan's root cause ("nothing treats an accepted head as settled") covers the stuck states (I-2, I-4 to I-7, I-16) and the re-verification cost (I-1). It does not cover the transport (I-8, I-13, I-14) or the editor's per-keystroke commits (I-10).

## 4. Fix status, at a glance (install, verified unless marked)

- **Fixed in the install (code present, not run in a browser):** I-1 partly (Runtime #59 verify-once; Agent #394 collect pass); I-2 partly (`head_busy` retryable; discharge wired to both buttons); I-11 (signature by declaration's own value).
- **Partly:** I-12 (reader gate present; writer `shot-group-pack-commands.ts:189-190` unchanged); I-3 (OR-chain at `useAssetManagement.ts:330` unchanged).
- **Not fixed in the install:** I-4, I-5, I-6, I-7, I-8, I-9, I-10, I-13, I-14, I-15, I-16. Agent #396's process-level memo is absent (verified).

Both Runtime checks above are on the install. The live stack and the owner's `~/Library` logs were not changed.

## 5. Open questions and unverified points

1. **Owner's exact texts.** I-3's "track changed" wording and I-6's "Retry" label are not in the install. Confirm which build the owner saw.
2. **I-2 on the live Runtime.** The 400 is reported from the old `519b404` Runtime. The install's Runtime returns 409 `head_busy`. A browser run on :2400 is the only way to confirm the buttons clear it.
3. **Timestamps.** The 11.8 s and 176–187 s figures are reported. I read the commit rows and not the timing columns.
4. **Proxy 503 bodies.** The proxy's error line is piped to the launcher and not stored on disk (reported). The 503s for `/objects/` are unproven.
5. **`save-state-map.md` and `sonnet-commit-profile-r14.md`** were absent when this pack was written.
