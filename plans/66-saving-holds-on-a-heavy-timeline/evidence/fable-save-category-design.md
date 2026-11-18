# Saving in the editor: what to fix now, the fundamental design, and where it goes in the plans

18 Nov 2026. Read-only: no code, install or plan was changed. Inputs: `save-failures-evidence-pack.md` (16 incidents, I-1 to I-16), `save-state-map.md`, my `fable-still-slow-review.md`, Plan 18 on astrid-dev `origin/main`, and the code installed on :2400. Five Haiku readers did the legwork; I re-read the load-bearing code.

Labels: **verified** = I read it. **Reported** = from the pack, the map or a Haiku reader. **Inferred** = reasoned, not measured. `sonnet-commit-profile-r14.md` had not landed, so every statement about how long a commit now takes is inferred.

**The short answer.** Sixteen incidents, one shape: *an edit can end up somewhere the design has no name for*. The fix is to give a change exactly one home and exactly four possible outcomes, and to draw the screen from that home alone. Seven small changes make :2400 dependable today, and six of them are the first pieces of that design.

---

# 1. What can we do to get everything working now?

**"Working" means:** a drop during a save succeeds; no save is retried for ever; every unsaved state shows the same bar with the same two buttons, and Discard always works, before and after a reload; an accepted save is never reported as lost. It does **not** yet mean a sub-second server reply: that is about 1–2 s on this document (inferred) until validation costs the change.

## The list, in order

| # | Repo | Change | Where | Size | Stops | End design or stopgap |
|---|---|---|---|---|---|---|
| N1 | Runtime | The selected-media guard signs identity and bytes only: object id, size, media type, variant id. `lifecycle`, `durability` and `provenance` leave the digest. **Landed, unmerged: Runtime #61** (reported). Merge it once it has one digest format. | `runtime_protocol/timeline_commit_port.py:1047-1065` | S | I-7 | End design (invariant 4) |
| N2 | App | No 409 is sent again with the same bytes unless the server says so (`head_busy`, `runtime_unavailable`). **Landed, unmerged: App #299** (reported): every other 409 becomes a dischargeable `conflict`. That is enough for today; merge it. The full decoder, with its total default and the three `>= 500` copies folded in, is CC-4. | `src/integrations/runtime/client.ts:322-345`; callers `commands/localSaveSession.ts:274`, `commands/commitSession.ts:248`, `integrations/runtime/bootstrapInitialization.ts:122` | S | I-7, I-2, any future untyped 409 | End design (invariant 2, client half) |
| N3 | App | **Discard is total.** Add `discardScope(scope)` to the outbox: delete every owner row for the timeline in one transaction. `discharge('latest')` becomes: release the claim, `discardScope`, clear the draft slot, claim a fresh owner, reset to the accepted head. It runs for any state, not only `rejected`. "Discard" and "Use latest version" both call it. | `commands/commitOutbox.ts:356-374`, `:569-575`; `commands/localSaveSession.ts:408-430` (the condition at `:413` goes); `hooks/useTimelineSave.ts:782-793`; `hooks/useTimelinePersistence.ts:1640-1700` | M | I-5, I-6, I-16, I-4, I-2 | End design (invariant 3). `discardScope` becomes "clear the queue row" |
| N4 | App | **One bar.** One component replaces the save notice, the recovery banner, the inline conflict bar, the conflict dialog, the watchdog banner and the copy in the shot preview. It shows whenever anything is unsaved and not in flight. It always has the same two buttons: **Try again** (resend on the latest head) and **Discard**. The headline is the reason. The badge reads the same input. | `components/TimelineEditorShellCore.tsx:808-905`, `:1204`; `components/ShotTimelinePreview.tsx:341-366`; `hooks/useTimelineSave.ts:55-65`, `:937-942` | M | I-5, I-6, I-15, I-4 | End design (invariant 1's surface). Its input changes later from six flags to one row |
| N5 | Runtime | One reply writer for both paths: write in 64 KiB pieces and, on `ENOBUFS`, wait for the socket and continue, inside the existing 30 s timeout. | `runtime_protocol/server.py:464` (`_send`), `:487` (`_send_file`) | S | I-13, part of I-8 and I-14 | End design (invariant 5) |
| N6 | App | Warm each object URL once per session: a module-level set, fetch only new URLs, do not abort because the set grew. | `src/tools/video-editor/compositions/AudioAnalysisProvider.tsx:150-181` | S | I-8, I-14 | **Stopgap in place, end design in rule.** The set moves into the one object reader (CC-9) |
| N7 | App | Position fields commit at the end of the edit, through the `onValueCommitted` path the timing fields already have. | `components/PropertiesPanel/ClipPanelBody.tsx:437-439`, `:153-157` | S | I-10, feeds I-2 | End design (one gesture, one change) |

Then, same branches, not blocking:

| # | Repo | Change | Where | Size | Stops | Kind |
|---|---|---|---|---|---|---|
| N8 | App | While retained saves replay, the edit is declined by the bar, not by an exception text. The two throws stay as assertions and their text never reaches the user. | `commands/localSaveSession.ts:350`, `:353`; wrapper `hooks/timelineLocalSaveHandoff.ts:975-981` | S | I-5 (the wording) | **Stopgap.** CC-5 deletes both throws: a new edit queues behind |
| N9 | App | An unavailable save retries by itself with backoff, and "Try again" retries at once. No owner with nothing to send is kept. | `commands/localSaveSession.ts:287`, `:343` | S | I-1 (the wait), I-16 | End design |
| N10 | Runtime | Health is served without `store._mutex`, like the identity probe. | `runtime_protocol/server.py:1520-1554` | S | part of I-1 | End design |
| N11 | Runtime, App | Log `timeline_commit_timing` for every commit; timestamp `runtime.log`; write the proxy's stderr to `logs/editor.log`. | `timeline_commit_execution.py:165-178`; `editor/scripts/dev-local-workspace.mjs:811-817` | S | makes I-1, I-8, I-14 measurable | End design (evidence) |
| N12 | App | A failed upload removes its "uploading" placeholder clip. | `hooks/useExternalDrop.ts:703-706` | S | I-8 (the leftover) | Stopgap; uploads become queue records (TL-10) |

**The minimum set that is "everything working": N1 to N7.** N1 and N2 remove the trigger and the endless retry. N3 and N4 give every state a way out. N5 and N6 remove the transport failure. N7 stops the storm that provoked I-2.

## For the App fix agent, exactly

N1 and N2 are done as #61 and #299. Build N3, N4, N7, then N8 and N9, on `release/14/save-recovery`. These are items 3 to 5 at the end of `save-state-map.md`, with three changes to what it proposes:

- **Item 3 (one surface): go further.** The map folds two banners. Fold all six surfaces, the conflict dialog included. After #299 a refused 409 arrives as `conflict`, and today's conflict card would headline it "This timeline changed somewhere else", which is false for a media refusal. The one bar headlines the reason it was given.
- **Item 4 (Discard means discard): build it as written.** `discardScope` in one transaction, for any state, called by every discarding button, and it clears the draft slot in the same action.
- **Item 5 (the `replaying` throw): as written, and say it is a stopgap** in the code comment, naming CC-5.

Details:
- **N3 first.** One new outbox function, `discardScope`. No per-owner loop, no outcome check. After it, the owner's stuck tab on :2400 clears with one press of Discard; no hand repair of IndexedDB.
- **N4:** one component with one prop, a small value computed in one function from today's state: `{kind: 'refused' | 'waiting' | 'recovered', headline, since}`. Do not add a status. Delete the five other surfaces in the same change; do not leave any behind a condition.
- **"Keep my changes" and "Save them" both become Try again.** One button, one function (`discharge('keep')` generalised the same way as Discard: any state).
- **Do not** add a retry counter, a new store, a new status value, or a second classifier. Do not generalise `discardOversized` yet; that is CC-5.

Proof before :2400 is rebuilt, one table-driven test: for each state (unavailable, refused, head moved, recovered after reload) and for one and two retained owners, the bar shows, Discard leaves a clean saved state, the next edit saves, and the same holds after a reload.

Then on :2400, as evidence: a drop; a second drop during the save; stop the Runtime during a save and start it; reload during each; Discard. Record the commit timing line and `netstat -m`. Then live.

**Not now:** proxy limits, connection pooling, more upload retries, a longer proxy timeout. Each is a second mechanism around a cause that N5 and N6 remove.

---

# 2. What's the fundamental solution?

## The idea

**A change has one home and four possible outcomes, and the screen is drawn from the home.**

Today a change can be in an outbox owner, a session copy, a draft slot and six React flags at once. A reply can be classed nine ways by status code. Eight statuses and at least thirteen throws stand between an edit and the queue. Each incident is a path through that space nobody designed. The design below has no such space.

## Five invariants

**1. One queue is the only home of unsaved work.**
- Each timeline has one ordered queue of change records in IndexedDB: the existing outbox, one row per timeline.
- The document on screen is the accepted head with the queue applied. Nothing else stores a document.
- The badge, the bar and what a reload shows are one pure function of that row. Two tabs read the same row, and one of them sends.
- One gesture is one record. A field edit commits when the edit ends.

**2. Every reply is one of four outcomes, and the server says which.**

| Outcome | Meaning | What the editor does |
|---|---|---|
| `accepted` | It is in. Here is the head. | Adopt the head, drop the record |
| `moved` | The head changed under you. Here it is. | Apply the same change to the new head and send it |
| `refused` | These bytes will never be accepted. Here is why. | Rule 3 |
| `unavailable` | Nothing was decided. | Send the same bytes again, same key |

- The reply carries the outcome as a field. Reasons are for people to read; they never decide behaviour.
- One decoder, total: no reply or a 5xx is `unavailable`; any reply it cannot read is `refused`.
- Every request that changes anything carries an idempotency key, so "send the same bytes again" is always safe. A lost reply is then an ordinary `unavailable`.
- This holds for every mutation the editor makes, uploads included, because all of them go through one `send`.

**3. A refusal leaves the queue, and nothing ever blocks an edit.**
- On `refused`, that record and the records that depend on it move out of the queue into a "not saved" list in the same row. The document returns to the head plus what is left. One bar says what and why, with **Restore** (queue it again on the current head) and **Dismiss**.
- This is what `discardOversized` does today for one kind of refusal (`localSaveSession.ts:160-170`). It becomes the only refusal path.
- A record waiting on `unavailable` stays in the queue and retries. The same bar shows it, with Discard.
- Adding to the queue has no precondition. There is no state in which the editor refuses an edit because of an earlier one.

**4. A check is signed by what it reads, and refuses only what the change introduces.**
- This is Phase 0's statements (b) and (e), extended to guards on a change's inputs: a selection is signed by identity and bytes, a drop by the track and shot it lands on, not by the whole head.
- One writer admits what readers will accept.

**5. An edit costs the change: in computation, in transport and in waiting.**
- Computation: Phase 0's statement (a).
- Transport: an immutable object's bytes are fetched once per session, through one reader. Adding one object reads that object.
- Waiting: a reply is written by one writer that survives a transient socket error. A read does not wait behind a commit's lock.

## What gets deleted

| Deleted | Where | By invariant |
|---|---|---|
| The draft database and everything that reads it | `data/timelineDraftIndexedDb.ts`; `recoveryDraft`, `recoveredAsDirty`, `offerRecovery`, `retryRecoveredDraft`, `discardRecoveredDraft` in `useTimelineSave.ts` | 1 |
| Owners: several rows per timeline, `recoverableOwners`, `recover(ownerId)`, the recovery loop | `commitOutbox.ts:153-157`, `localSaveSession.ts:343-346`, `:431-445`, `useTimelineSave.ts:380-405` | 1 |
| The session's own document copies and the equality bridge | `LocalSave.before` and `after`, `same(...)` at `localSaveSession.ts:357`, `:390`; `replaying` | 1 |
| Six save flags in React | `saveError`, `isConflictExhausted`, `schemaIncompatible`, `watchdogTripped`, `watchdogReason`, `saveStatus` | 1 |
| Five of six surfaces | save notice, recovery banner, conflict bar, conflict dialog, watchdog banner, the shot-preview copy | 1 |
| The upload's private recovery | `persistMediaImportOperation`, `recoverMediaImportAfterLostAck` (`dataProvider.ts:1718`, `:1735-1765`); the "Failed to save asset" toast | 1, 2 |
| `RuntimeCommitFailureKind` (nine kinds) and its three call-site preludes | `client.ts:307-345` | 2 |
| `isRuntimeConflict`, `isRuntimeCanonicalPayloadConflict`, `permanentRejectionMessage` | `client.ts:291`, `:352`; `localSaveSession.ts:67-77` | 2 |
| `retryable` as a per-reason flag | Plan 18 CC-4, TL-4 | 2 (the outcome carries it) |
| Statuses `retry`, `conflict`, `blocked`, `recovery`, `error` as modes | `localSaveSession.ts:30` | 3 |
| `rollback`'s retained-chain branch, `discharge('keep' \| 'latest')`, the single-track-label exception | `localSaveSession.ts:181-206`, `:408-430`, `:88-103` | 3 |
| Every throw that refuses an edit or a send for an earlier state | `localSaveSession.ts:132`, `:350`, `:353`, `:400`, `:436`; `commitOutbox.ts:496`, `:501` | 3 |
| The whole-record selection digest; the head-equality test on a drop | `timeline_commit_port.py:1061`; `useAssetManagement.ts:330` | 4 |
| Three private fetchers of object bytes and four URL builders | `AudioAnalysisProvider.tsx:149-181`, `useWaveformData.ts:29-50`, `audioAnalysisClient.ts:188`; `client.ts:1216`, `bridgeMediaUrl.ts:41`, `mediaRoutes.ts:27`, `dataProvider.ts:1651` | 5 |

Nothing is added except: the `outcome` field, `discardScope`, the one bar, the one object reader and the one reply writer.

## Every incident, and the invariant that prevents it

| Incident | Prevented by | How |
|---|---|---|
| I-1 slow saves, 60 s cut, wait for a replay | 5, 2 | Work is bounded by count. A cut is `unavailable`: same bytes, same key, replay |
| I-2 "inputs changed" became permanent | 2 | The server says `unavailable`. The client cannot call it anything else |
| I-3 drop refused because the head moved | 4 | The drop's guard reads its track and shot only. Later the drop is an intent the server judges (TL-10) |
| I-4 "original verified authoring head is unavailable" | 1, 3 | No second document to disagree with. A moved head is `moved` |
| I-5 "Wait for retained dependent saves" | 3 | Adding to the queue has no precondition. The throw is deleted |
| I-6 banner after reload; Discard does nothing | 1, 3 | One row, one bar, the same before and after a reload. Discard empties the row |
| I-7 409 retried for ever | 4, 2 | The guard no longer fires on lifecycle. An unreadable reply is `refused` |
| I-8 upload fails during a save | 5, 2, 1 | No bulk re-download. A cut upload is `unavailable` and is sent again from the queue |
| I-9 two tabs block each other | 1 | One row per timeline; both tabs read it; one sends |
| I-10 a commit per keystroke | 1 | One gesture, one record |
| I-11 move refused for an untouched `gap_after_s` | 4 | Signed by its own value, through the delta gate |
| I-12 half association written, then refused | 4 | One admission function for every writer |
| I-13 accepted commit loses its reply | 5, 2 | The writer survives `ENOBUFS`. If a reply is still lost, it is `unavailable` and replays |
| I-14 `/objects/` 503s and stalls | 5 | Bytes once, through one reader |
| I-15 badge stuck on "Saving" | 1 | The badge is the function of the row |
| I-16 stale owner never sent, never dropped | 1, 3 | No owners. A row with nothing to send does not exist |

**Not covered, plainly:**
- **A server reply under one second.** The invariants bound work; they do not make whole-document validation cheap. That needs validation that costs the change. With rule 3 the wait no longer blocks or breaks anything, but the badge will still say "Saving" for a second or two.
- **A cold start.** The first read after a restart hashes each object once: 2.2 GB on this realm. That is owner decision D14.
- **The machine running out of socket memory for other reasons.** The design makes it harmless (a retry), not impossible.
- **I-3's wording and I-6's "Retry" label** do not exist in the install (pack, open question 1). Which build the owner saw is unknown.

## How it is enforced

One typed boundary, one model test, and a few counts that may only fall.

1. **The boundary.** `send(request): Promise<Outcome>` is the only function in the editor that sees an HTTP status. `Outcome` is a four-member union generated from the Agent's list. A lint fails on `ApiError`, `.status` or a match on error text anywhere under `tools/video-editor/`.
2. **The model test, one file.** A scripted `send` plays every outcome at every queue position, a lost reply, a cut request, a reload between any two steps, and a second tab. After every step it asserts:
   - adding an edit never throws;
   - what the screen shows equals the function of the row;
   - every record is accepted, in the "not saved" list, or queued behind an `unavailable`;
   - Dismiss and Discard always leave a saved state, and the next edit saves.
   
   A new state or surface cannot be added without this test failing, because the screen is compared with the function.
3. **Counts in the one ratchet file, held at zero or falling:**
   - IndexedDB or `localStorage` opened for save state outside the queue module;
   - `throw` reachable from adding to the queue;
   - `fetch` of an object URL outside the reader;
   - object GETs per gesture on the corpus (adding one object: that object only);
   - Phase 0's computation counters.
4. **Server side.** Phase 0's grid: every operation on every corpus head introduces no finding. The corpus gains a selection whose lifecycle advanced between select and commit. A route-table test sends every mutating route twice with one key and expects one effect. A writer test delivers a reply through a socket that raises `ENOBUFS`.

---

# 3. How does that fit into future plans?

**It is Plan 18 Phase 0, sharpened in two tasks and extended by one.** Not a new plan and not a different cut. Phase 0's root, "nothing treats an accepted head as settled", already covers the server half (invariants 4 and 5's computation). The missing half is the client's: *nothing gives an unsettled change one home*. And nothing covers transport.

## Where each invariant lives

| Invariant | Phase 0 | Phase 1 | Phase 2 |
|---|---|---|---|
| 1 One queue | CC-5 (one row, one bar, drafts deleted) | TL-5 (the document is head plus queue; `after` and `replaying` go); TL-10 (uploads are queue records); TL-12 (leftovers deleted) | EX-2's view reads the same row |
| 2 Four outcomes | CC-4 (the `outcome` field, one decoder, every mutating route) | TL-4 (`EditResult` is the outcome) | EX-2's own op returns it |
| 3 Refusals leave | CC-5 | TL-4 (headlines) | — |
| 4 Signed checks | CC-3, CC-6, CC-7 | TL-10 (drop guards), TL-13a | EX-2's op registers under the gate |
| 5 Cost of the change | CC-1, CC-2, **new CC-9** | TL-7 (one gesture, one record) | — |

## Exact deltas to Plan 18

**`plan.md`, Phase 0 statements**
- **(d) rewritten:** "Every reply is one of four outcomes (accepted, moved, refused, unavailable), named by the server. A refusal leaves the queue with its dependents and its reason. Unsaved work has one home, one row per timeline, and the screen is drawn from it. Any unsaved change can be discarded, in any state, before and after a reload."
- **(g) new, bounded transport:** "An edit causes transport proportional to the change. An immutable object is fetched once per session through one reader. Every mutating request is idempotent by key, so a lost reply is a retry. A reply is not lost to a transient socket error."
- **(b) gains one sentence:** "A guard on a change's inputs is signed the same way: by what it reads."

**`statements.md`**
- **P3 rewritten** in the owner's words: "An edit is saved, waiting, or not saved, and the editor always shows which, in one place, with a way out."
- **P6 new:** "Media you already have is not downloaded again, and a file you drop is never lost to a save in progress."

**`tasks.md`, changed**
- **CC-4.** Each list entry declares its `outcome`, not `retryable`. The reply carries `outcome`. The App's decoder is the only reader of status. Scope widens from the commit route to every mutating route. An untyped 409 is `refused`. Tests: the route table; "a reply with unknown wording decodes by `outcome` alone".
- **CC-5.** Retitled "One queue, one bar, and a way out". Adds:
  - one row per timeline; owners are deleted, which settles two tabs by construction (the "key the draft slot by owner id" fallback is removed);
  - the draft database is deleted; the one display `after` it keeps until TL-5 lives in the row;
  - the deleted throws are `localSaveSession.ts:132`, `:350`, `:353`, `:400`, `:436` and `commitOutbox.ts:496`, `:501`, replacing the two it names;
  - the refusal path is `discardOversized` generalised;
  - the model test (enforcement item 2) replaces the per-gesture table as the proof;
  - no row with nothing to send exists.
- **CC-1.** The ratchet file gains object GETs per gesture and the three scans in enforcement item 3.
- **CC-3 and CC-6.** Name the selected-media digest as a signed guard. CC-6 names the writer at `shot-group-pack-commands.ts:189-190`.
- **CC-7.** The corpus gains: a selection whose lifecycle advanced; a head with many audio sources.
- **R0.** Negatives add: a lost reply, a cut upload, a reload during a refusal, two tabs.
- **TL-4.** `EditResult` becomes `{outcome, head?, code?, headline?}`. `retryable` is removed.
- **TL-5.** States the end form of invariant 1: the document is the head plus the queue replayed.
- **TL-7.** Adds the rule "a field commits when the edit ends".
- **TL-10.** A drop is an upload record and an intent in the same queue. Deletes the upload's private recovery and the head-equality test at `useAssetManagement.ts:330`.
- **TL-12.** Deletion list gains `RuntimeCommitFailureKind` and whatever of the draft code remains.

**`tasks.md`, new**
- **CC-9 Bounded transport** (statement g), route N, about 4 days, after Release 14 is published. App: one object reader and one URL builder; warm-up, waveforms and analysis go through it. Runtime: the one reply writer; health off the store mutex; the commit timing line; the idempotent route table. Proof: the counts above.

**`tasks.md`, deleted:** no task. One fallback inside CC-5 (above).

**`inputs.md`**
- "Deferred from phase 0" gains: waveform peaks stored beside the object; the two proxy hops of the local install; object metadata reads sharing the commit's mutex.
- **Estimate:** Phase 0 goes from about 23 to about 29 engineering days (CC-9 four, CC-5 two more).

## Owner decisions

| Decision | Effect of this design | Recommendation |
|---|---|---|
| **D9** release for Phase 0 | Stronger case. Ten of sixteen incidents are closed for good only by CC-4, CC-5 and CC-9 | **Release 15**, not 17 |
| **D10** corpus data | No owner content is needed. Both new shapes are synthetic | Synthetic |
| **D14** cold start | It is the largest uncovered cost: every restart re-hashes 2.2 GB on this realm | Persist `file_identity`, as recommended |
| **D4** release for Phase 1 | Invariant 1's end form waits for TL-5. Phase 0 already gives one bar and one way out, so the wait is safe | The release after Phase 0 |
| **D5, D6, D8** | Unaffected. D6: R0 reviews the model test | As recommended |
| **D11** (`stale_head`) | A raw document patch that cannot be applied to the new head is `refused` and appears in the same bar. The conflict card goes | Confirm |
| **D15, new** | On a refusal the change is removed from the timeline and listed with Restore and Dismiss. The alternative is to leave it visible and marked | **Remove and list.** It is what `too_large` does today, and it is the only choice under which the editor is never blocked |

## Plan 59

No change of scope. Its asset contract ("accepted early, refused late", handover line 83; #769) is the write side of invariant 4, which CC-6 consumes. One addition: that contract defines the selection's identity fields, so N1 and the contract share one definition.

## Which release carries what

| Release | Carries |
|---|---|
| **Release 14 fix branches, now** | N1 to N12. App on `release/14/save-recovery`; Runtime N1 with it; N5, N6, N10 and N11 on one `release/14/transport` branch per repository |
| **Release 15** (D9) | Phase 0 with the deltas above: CC-1 to CC-9 and R0 |
| **The release after** (D4) | Phase 1, including TL-5 and TL-10, which complete invariant 1; then Phase 2 |

Of today's twelve changes, three are stopgaps, each with its replacement named: N6 (CC-9's reader), N8 (CC-5's deleted throws) and N12 (TL-10).

## Not checked

- Nothing here was built or run. The stuck states were read from code, the pack and the map.
- The r14 profile. The "1–2 s" figure and the split of the 12 s are inferred.
- Whether `discardScope` can delete a row another tab holds under its Web Lock. The claim's generation check should fence the stale tab (reported, `commitOutbox.ts:272-273`); the model test's two-tab case must show it.
- Whether a `File` stored in the queue row survives a reload in every browser the editor supports. TL-10 must confirm before uploads move into the queue.
- GitHub issues beyond the titles the pack lists.
