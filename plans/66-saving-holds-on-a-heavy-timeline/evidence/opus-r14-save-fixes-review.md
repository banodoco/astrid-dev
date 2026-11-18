# Release 14 save fixes: review before the owner's install

18 Nov 2026. Read-only review. Nothing was edited, pushed or merged.

**Scope.** I reviewed three diffs:
- **App:** `fbb8168bd..816f88da9`, which is PR #300 and PR #299.
- **Runtime:** `d725811..1af7ed60`, which is PR #62.
- **Agent:** PR #400, which is commit `6b8780669` on top of `84c2f5247`. It is already merged into `release/14/main` as `9f614dff7`. The merge-base diff the brief asked for is therefore empty, so I diffed the commit itself.

I used the design (`fable-save-category-design.md` §1 and the N-table) for intent only.

**How I checked.** Four Haiku readers swept the callers and write paths. I re-read every load-bearing line myself.

**Labels.**
- **Verified:** I read the code path.
- **Inferred:** reasoned from the code but not run.
- **Reported:** from a reader, not re-checked.

I ran no tests.

**Verdict.** Four findings must be fixed before the owner tests:
- Three in the App: a dead Discard after a failed bootstrap, a sticky failure after a declined edit, and a drop that vanishes silently.
- One in the Runtime: the post-commit hook is stolen by throwaway stores.

Each fix is small. The Agent change keeps the old verdicts as far as I can read, but its oracle does not prove that.

---

## Must fix before the owner tests

### 1. App: Discard and Try again do nothing after the editor fails to start its save session

**Verified.**

**Where:**
- `src/tools/video-editor/hooks/useTimelineSave.ts:403-409`: the recovery loop. Any throw from `session.recover` rejects `localOwner.ready`.
- `useTimelineSave.ts:185-189`: `discharge` returns early when there is no handoff. Its comment, "A failed bootstrap has no session and nothing queued to leave", is wrong. The session exists, and its owner rows are still in IndexedDB.
- `useTimelineSave.ts:436-441`: sets the local state to `error`. Nothing ever clears it.

**Scenario (two tabs).**
1. Tab A has unsaved or refused work.
2. The owner opens the same timeline in tab B, for example the app window as well as the browser tab.
3. Tab B lists A's owner and recovers it.
4. `navigator.locks` with `ifAvailable` fails with "Outbox is already claimed" (`commitOutbox.ts:118-123`).

**What tab B then shows and does:**
- The bar reads "Outbox is already claimed".
- **Try again** is a no-op.
- **Discard** reloads the canonical head, but `localSaveState` stays `error`, so the bar never leaves.
- Every edit fails, because the capture awaits a rejected `ready`.
- The persistence layer retries that dead save every 8 s, indefinitely.

**Other triggers.** Any recover throw has the same result, for example an owner row without a verified display basis (`localSaveSession.ts:350-353`), or a row in the scope that is not a local save (`saveOf`, `:81-85`).

**Why the tests miss it.** The session-level test swallows recover errors (`localSaveSession.discard.test.ts:67`, `:107`: `.catch(() => {})`). It never reaches this hook path.

**Smallest fix:**
- In the loop: `try { await session.recover(owner); } catch { break; }`. The handoff is then built, and Discard reaches `discardAll`, which already handles an unclaimed box and resets `recoveryError`.
- For a failure during `sessionCreation`, have Discard call `outboxes.discardScope(scope)` and re-run the bootstrap.
- Add one hook-level test: recover throws, Discard runs, the state is saved, and the next edit saves.
- Better headline for the lock case: "This timeline has unsaved changes open in another tab."

### 2. App: an edit declined while earlier saves replay leaves a sticky failure

**Verified.**

**Where:**
- `src/tools/video-editor/commands/localSaveSession.ts:243`: `pump` sets `replaying = true` whenever a save lands while another edit is queued. It stays set until the queue drains.
- `localSaveSession.ts:398` and `:401`: during that window, `append` throws. N8 calls these assertions.
- `hooks/timelineLocalSaveHandoff.ts:980`: wraps the throw as `TimelineSaveError("Local document save retained: …")`.
- `hooks/useTimelinePersistence.ts:1150`: stores it in `session.captureFailure`. Only a reload clears it (`:1719`).
- `useTimelinePersistence.ts:754`: `doSave` rethrows it before every later save.
- `useTimelinePersistence.ts:917`: toasts the assertion text verbatim.

**Scenario (the owner's own flow).**
1. Drop image 1.
2. Drop image 2 while save 1 runs.
3. Save 1 lands, and image 2 starts sending.
4. Any edit in that window, such as a third drop or a nudge, triggers the decline.

**What follows:**
- A toast reads "Local document save retained: Wait for retained dependent saves to finish revalidation before editing again".
- After save 2 lands, the session is `saved`, but the bar stays. It reads "Earlier changes are still being saved. Try again in a moment." (`hooks/saveBar.ts:47`). That is false.
- Later edits are appended to the outbox but never flushed, because `doSave` throws before `saveMutation`.
- **Try again** sends them, but cannot clear the bar.
- Only **Discard** clears it, and Discard deletes whatever Try again had not yet sent.

This is the "permanent error state" class that the release is meant to close.

**Smallest fix:**
- Mark the two declines as authoring refusals: `authoringRefusals.add` in the handoff wrapper. They then take the existing revert path (`useTimelinePersistence.ts:1148-1149`), which:
  - undoes the edit on screen;
  - says why, once (`:1333`);
  - never sets `captureFailure`.
- Have `tryAgain` clear `session.captureFailure` and the persistence error before it resends. This covers the `conflict` and `error` states, where the revert path declines (`:1323-1324`).

### 3. App: a drop whose upload finishes after any save lands is silently abandoned

**Verified.**

**Where:**
- `src/tools/video-editor/lib/external-drop-utils.ts:404-412`: `dropScope` includes `head`.
- `external-drop-utils.ts:460-463` and `:483-486`: `removeSkeleton(); return;`, with no `onAssetDropError`.
- The new comment at `:441-442` names exactly this case.

**Scenario.**
1. Drop image 1.
2. Drop image 2 while save 1 runs.
3. Save 1 lands, and the head moves, while image 2 is still uploading.

**Result.** Image 2's placeholder disappears. No clip appears and no message is shown. The generation is uploaded but never placed.

Before this PR the placeholder stayed (I-8). Now the drop vanishes cleanly. That is the opposite of the design's definition of working: "a drop during a save succeeds". It also makes the owner's "second drop during a save" test pass or fail on upload timing.

**Smallest fix:**
- Key `dropScope` on the canonical composition only. The head moves on every save, and the Runtime revalidates the placement against its own head. **Inferred:** `dropAsset`'s own guards must still refuse a deleted track. I did not trace them.
- At minimum, call `onAssetDropError(new Error('The timeline changed while this file uploaded; drop it again.'))` before removing the placeholder.

### 4. Runtime: throwaway commit stores steal the post-commit hook

**Verified.**

**Where:** `runtime_protocol/timeline_commit_store.py:300` assigns `store._after_commit` in every `TimelineCommitStore.__init__`, and the last assignment wins. Throwaway instances are built:
- at `store.py:2324`, on render admission with `canonical_revision`;
- at `store.py:7485`, on every `integrity_report`. That runs for `/v1/doctor`, `/v1/diagnostics` (`server.py:759-767`) and `_restore_integrity` before each `timeline.restore` (`timeline_commit_port.py:155`).

Each one replaces the service's hook (`service.py:3127`).

**Scenario.**
1. The owner renders, opens diagnostics, or restores a version.
2. From then on, every unrelated write (a media import, a task heartbeat) again clears the service's proofs. This is through `_sync_replay_memo`, `timeline_commit_store.py:598-621`.
3. The next save re-walks the whole history. Slow saves return for the rest of the Runtime's life.

This is safe, because the old discard path still runs. But it silently undoes PR #62, and it makes the owner's timing evidence depend on whether a render happened first.

The stale throwaway instance also:
- keeps its caches alive;
- can run `_reestablish_connection` on the shared store from inside the post-commit hook (`:432-440`).

**Smallest fix:**
- Delete the assignment from `__init__`.
- Set `self.store._after_commit = store._absorb_own_write` in `service._timeline_commits()`, where the one service-owned store is built.
- Add a test: build a second `TimelineCommitStore` on the same `RealmStore`, then assert that the service's proofs still survive an unrelated write.

---

## Fix forward (can ship, should follow)

### 5. App: Discard pressed while a queued chain is sending saves the chain instead

**Inferred** from the code.

**Where:**
- `localSaveSession.ts:319-323`: `discardAll` awaits `sending`.
- `localSaveSession.ts:229`: `pump` re-reads `generation` on each pass, so it goes on dispatching intents 2…n.
- `localSaveSession.ts:306`: `scheduleRetry()` can arm a new timer after `discardAll`'s `clearRetry()`.
- `useTimelinePersistence.ts:1635-1642`: Discard first awaits the drain and the draft writes. During that wait, the N9 timer can fire and start a send.

**Scenario.** The bar shows "waiting" while the Runtime flaps. The owner presses Discard just as the Runtime answers. The retained edits land, then Discard reloads them. No work is lost, but the button did the opposite of its name.

**Fix:**
- Add a discard epoch, set first thing in `discardAll`, and have `pump` check it before each dispatch.
- Call `clearRetry` again after `sending` settles.
- Cancel the timer synchronously at the start of `discardUnsaved`.

### 6. App: two retry schedulers for one unavailable save

**Inferred.** In the `retry` state, `handoff.flush` rethrows a plain `Error` (`timelineLocalSaveHandoff.ts:1010`). By my reading it then takes the generic branch (`useTimelinePersistence.ts:984-988`): `retrying` plus `scheduleErrorRetry`, from 0.5 s up to 8 s, with no limit. Each persistence retry pumps, and each pump resets the N9 timer (`localSaveSession.ts:132-139`).

**Effect:**
- In production the cadence is 8 s, not the 1→30 s backoff the new test proves. The test is session-only.
- Not a storm, but two mechanisms for one fact.

**Fix.** In the generic branch, do not schedule a persistence retry when the local session reports `retry`. The session owns it.

### 7. App: Try again's dispatch order is not the bar's order

**Verified.** `tryAgain` (`useTimelineSave.ts:809-820`) checks conflict-exhausted first, then the watchdog, then the local state, then the draft. `saveBarInput` (`saveBar.ts:28-50`) headlines the local state first.

**Example.** The watchdog trips while a local refusal is retained. The conflict branch (`useTimelinePersistence.ts:957-962`) does not disarm the watchdog. The bar names the refusal, but Try again calls `retryWatchdog`. That reschedules a save, the capture is declined, and the session ends up in finding 2.

**Try again is also a no-op for:**
- `notice` (an oversize refusal);
- the `recovery` state;
- the failed bootstrap in finding 1.

**Fix.** Compute the action in the same function as the headline, for example an `action` field on `SaveBarInput`. Try again then runs that action.

### 8. App: toasts are still a second save-error surface

**Verified.** Toasts remain at `useTimelinePersistence.ts:893`, `:917`, `:1333` and `:1717`. The one at `:917` repeats every refusal the bar already shows, with the "Local document save retained:" prefix.

**Fix.** Drop the `:917` toast while the bar is up. Keep only `:1333`, which reports an undone edit.

### 9. App: headlines that will mislead the owner's test

**Verified.**
- The local `recovery` state reads "The Runtime is not answering. Your changes are kept." (`saveBar.ts:38-39`). It flashes on every reload that has retained work, while the Runtime is fine. It should be `recovered`.
- Any persistence `saveError` with a local session reads "Earlier changes are still being saved" (`saveBar.ts:47`). That includes reload failures such as "The recovery draft changed during reload; it was kept for safety" (`useTimelinePersistence.ts:1695`).

### 10. App: Discard loads the timeline twice and gives no feedback

**Verified.**
- `discardAll` runs `resetToCanonical` (`localSaveSession.ts:335`).
- `reloadFromServer` then loads and builds again (`useTimelinePersistence.ts:1644-1672`).
- The buttons have no pending or disabled state (`SaveBar.tsx:24-25`).

On the owner's long timeline the bar can sit unchanged for seconds after the click, which reads as "Discard did nothing".

**Fix:**
- Disable both buttons while their promise runs.
- Let one of the two paths do the load.

### 11. Runtime: the absorb cost grows with history, and the test hides it

**Verified.**
- On every hooked commit, `_retained_rows_unchanged` (`timeline_commit_store.py:340-351`) re-runs every retained query under `store._mutex`. The retained results are full row tuples, including the event-prefix and chain `fetchall` queries. Hooked commits include task heartbeats during a render, and imports.
- `tests/test_timeline_commit_ancestry.py:53-56` clears the statement log after `unrelated_write`. The "same cost at 3 and 30 entries" claim therefore excludes exactly the cost that now grows with history.

It is cheaper than the old full replay, but it is now paid on every write instead of on the next read.

**Fix:**
- Count the statements during the write as well, and measure on the owner's timeline with a render running.
- If the count grows with history, limit the recheck to the tables the write touched.

### 12. Agent: the "frozen" oracle is not frozen for the code this PR changed

**Verified.** `tests/editing_conformance/legacy_probe_oracle.py:17` imports `_reference_basis` from production. The differential therefore compares the new basis with itself, and the commit message's "verdicts are unchanged: the frozen-oracle differential still matches" does not cover the basis.

**My own reading finds no verdict change:**
- The new basis equals the old one under dict equality (`_failing_candidates`, `_commit_timing_validation.py:716-718`).
- The new signature splits the old keys into parts exactly, for parent or shot × word or non-word. So signature equality matches the old whole-JSON equality (`_signed_failures`, `:378`).
- `_declaration_failures` returns a finished dict before the reader's lazy caches fill.
- Signatures are compared only in memory between the candidate and the base, never persisted.
- Nothing downstream mutates the shared parts. `_restored_legacy_exemptions` (`:453-463`) only rebinds top-level keys of a fresh dict, and builds a new reader on each call.

**Cases the differential does not cover** (reported): missing `pinned_documents`, missing or empty placements, duplicate clip ids, shots with no clips, a declaration naming an absent shot.

**Fix.** Copy the old `_reference_shape` and `_reference_basis` verbatim into the oracle, then add those five cases.

### 13. Agent: instance monkeypatching in `evaluate`

**Verified.** `_timing_evaluators.py:333-336` replaces `lookup._cut_groups` with a lambda that drops `by_occurrence`. Nothing in `evaluate` calls `_cut_spans` or `_cut_on_screen` on this lookup today (`lookup.py:335-347`).

**Risk.** A future call would raise `TypeError`. `_declaration_failures` (`_commit_timing_validation.py:348`) and `validate_candidate_timing` (`:766`) both catch `TypeError` and treat it as a timing outcome. The verdict would change silently.

**Fix.** Override `_cut_groups` and `_cut_id` in `_ReadLookup` with the same signatures, and cache there.

---

## Notes

### 14. App: total Discard deletes another live tab's unsaved work

**Verified, by design.** That tab is fenced on its next access (`commitOutbox.ts:315`; test `:100-118`). A request it already has in flight can still land after the Discard. The owner should know this before testing with two tabs.

### 15. App: the screen jumps back while a queued edit sends

**Verified, pre-existing.** When a save lands while another edit is queued, the screen is reset to the landed head before the next edit is sent (`localSaveSession.ts:236-245`). A second dropped image therefore disappears until its own save lands. Tell the owner this is expected, or the test will read it as a lost drop.

### 16. App: dead state left behind

**Reported, spot-checked:**
- `useTimelineState.types.ts:265-267` and the chrome type still declare `saveNotice`, `watchdogReason`, `retryWatchdog`, `recoveryDraft`, `retryRecoveredDraft`, `discardRecoveredDraft` (no caller), `isConflictExhausted`, `retrySaveAfterConflict` and `schemaIncompatible`.
- `saveNotice` is computed (`useTimelineSave.ts:968`) and read by nothing.
- `SaveBarSources` takes six flags. The design names this as the stopgap input.
- N9's "no owner with nothing to send is kept" is not done. Every editor session still leaves one empty owner row.

### 17. Runtime: caches kept on absorb that the recheck does not cover

**Inferred, unproven.** `_absorb_own_write` now keeps several caches that `_retained_rows` does not cover:
- `entries`, including legacy entries that never go through `_verify_accepted` (`timeline_commit_store.py:1250-1266`);
- `events`, `chains` and `chain_tails`;
- `closures` and `objects`.

Before this PR, any write by this Runtime dropped them. Now they are kept on an assumption that history is immutable.

I found no write by this Runtime that edits those rows. The `command_idempotency` UPDATEs at `service.py:1895` and `:2303` and `store.py:3852` change `result_json` for other ledger rows, and ledgers that a traversal consumed are re-read.

The other things asked about are sound:
- An external writer, in any process including over WAL, changes `data_version` and discards everything.
- An autocommit write that skips the hook still faces the row recheck at the next hooked commit, or a full discard at the next boundary.

**Fix.** Add one test: a write by this Runtime edits a legacy entry's ledger row, and the next read must fetch it again.

### 18. App: smaller N6 and N7 behaviour changes

**Inferred.**
- **N7:** with `onChange` a no-op, a held stepper moves the value once per release.
- **N6:** warm-ups are no longer aborted on unmount, so each audio URL downloads once per session even after leaving the editor. That is acceptable.
- **Proxy stderr:** the pipe is fine.

---

## Questions answered

**(a) Owner-facing correctness:**
- **Blocked with no way out:** yes, in finding 1, and effectively in finding 2.
- **Unsaved work lost without Discard asking:** yes, in finding 3 (the drop). Finding 2 loses the declined edit, and Discard is then the only exit.
- **`discardScope` and other tabs:** it fences other tabs correctly. A deleted row fails the generation check at `commitOutbox.ts:315` before any write-back.
- **Retry storm:** none. Retries are bounded at 8 s or 30 s, and two schedulers overlap (finding 6). There is no automatic resend of a refused save.
- **Placeholder left behind:** none now. The cost is a silently lost drop (finding 3).
- **Runtime:** I found no way for a retained proof to survive a write to a row it consumed. Finding 17 is the unproven edge, and finding 4 removes the benefit.
- **Agent:** I found no case with a different verdict. The oracle gap is finding 12.

**(b) Elegance:** findings 6, 7, 8, 10, 13 and 16.

**(c) What would make the owner's browser test misleading:** findings 3, 4, 9, 10 and 15.
