# Save-state map (Release 14 plan-59, App fbb8168bd)

Paths under `src/tools/video-editor/` unless stated; App worktree `~/Developer/astrid-release-src/wt-app-save-recovery`.
Labels: [V] = read by me (main thread) in source; [H] = Haiku-reported, not re-read by me.

## 1. Stores that hold save state

1. **Command outbox, IndexedDB `astrid.command-outbox` v1, store `owners`** (`commands/commitOutbox.ts:115-116`) [H]. Key = JSON `[realmId, actorId, projectId, timelineId, ownerId]` (`:153-157`). One row per owner. Row = `OutboxRecord` (`:74-86`) [V]:
   - `scope`, `ownerId`, `generation` (bumped on every claim, `:~265`; stale claims throw "Stale outbox claim") [V]
   - `intents[]` (unsent saves, each with `basis` = `{head}` or `{after: predecessorId}`, optional `conflict`)
   - `pending?: { intentId, request, outcome?: {kind:'rejected'|'retry', error} }` (`:79`, outcome type `:36-37`) [V]
   - `accepted?` (last acknowledged prefix) , `placementContinuations?`, `initialization?`
   - API: `createCommitOutbox()` returns `{list, create, recover}` (`:569-575`) [V]. `list(scope)` `:242-252` filters by realm/actor/(project)/(timeline). **No remove-owner / remove-by-timeline API; the only deletion is the `pending` field** (`resolveRejected`, `~:356-374`) [V: no store.delete; H: grep].
   - Claimed owner API: read, append, cancel (`:346-355`), resolveRejected, rebaseRejected, dispatch, placement methods. Claims use `navigator.locks` exclusive, ifAvailable (`:~120-125`).
2. **Draft slot, IndexedDB `astrid.timeline-drafts`** (`data/timelineDraftIndexedDb.ts`) [H]. One slot per recovery key (`provider.getTimelineDraftRecoveryMetadata().recoveryKey ?? timelineId`). `clearTimelineDraft(timelineId, expectedOwnerId?)` `:235`; compare-and-delete `clearTimelineDraftIfSnapshotMatches` `:415-440`.
3. **Local save session in-memory state** (`commands/localSaveSession.ts:106-122`) [V]: `basis`, `displayBasis`, `document`, `box` (claimed owner), `record`, `closed`, `lifetime`, `writes`, `sending`, `generation`, `adoptedAcceptance`, `replaying`, `recoveryError`, `writeError`, `state: LocalSaveState` (`:29-`; status `saved|dirty|saving|retry|conflict|blocked|recovery|error`, `recoverableOwners[]`, `ownerId`, `error`, `notice`).
4. **Persistence hook React/ref state** (`hooks/useTimelinePersistence.ts`, `useTimelineSave.ts`) [H/V]: `persistence.saveError`, `isConflictExhausted(+Ref)`, `schemaIncompatible`, `saveStatus`, `watchdogTripped/watchdogReason`, `recoveryDraft` (`useTimelineSave.ts:~556`), `recoveredAsDirty`, `localOwner.recovered`.
5. Runtime recovery-card store (`integrations/runtime/recoveryCard.ts`): connection ("Astrid stopped"), not save state [H].

## 2. Editor states and what drives them

- Session `state.status` is set by `publish()` (`localSaveSession.ts:124-129`) [V]:
  - `saved` after `hold` (`:314,330`) and when queue empty (`pump`, `~:262`)
  - `dirty` on `append` (`:~362`) and after claim with intents
  - `saving` before dispatch (`~:236`)
  - `retry` when `record.pending` remains after dispatch (`~:268`), error = outcome.error only if outcome kind retry
  - `conflict` / `error` from `rollback()` when pending.outcome.kind is `rejected` (`:187-218`); `conflict` if inverse command or error.kind==='conflict'
  - `blocked` for DTO gap (`~:231`)
  - `recovery` at startup when retained owners exist (`:345`) and on `recover()` with multiple owners (`:441`)
  - `error` for write failures (`:290,338,374`), pump exceptions, "Removed change; reload failed"
- Retained-owner listing at startup (`:343-346`): `owners = list(scope).filter(intents.length || pending)`; if any, `publish('recovery')` and **no owner is claimed** (so `box` undefined and `assertOpen()` throws "closed or awaiting recovery"); else `claim()` a fresh owner.
- `state.notice` set only by `discardOversized` (`:~167`).

## 3. UI surfaces (all in `components/TimelineEditorShellCore.tsx` unless noted)

| Surface | Lines | Driven by | Actions |
|---|---|---|---|
| Watchdog banner | `~808-822` [H] | `chrome.watchdogTripped` | "Retry save" or "Dismiss" |
| **saveNoticeBanner** ("This change was not saved. …", or notice/rejected-kind message) | `~826-840` [V] | `chrome.saveNotice` = `localSaveNotice(localSaveState)` (`useTimelineSave.ts:~55-65`: `state.notice`, or `status==='error'` with error.kind in `REJECTED_SAVE_KINDS` and a message) `?? "This change was not saved. " + persistence.saveError` (`useTimelineSave.ts:~937`) | **none** (message span only) [V] |
| Conflict banner / dialog | `~846-860`, `:1208` [V] | `chrome.isConflictExhausted` | "Use latest version" (`reloadFromServer({discardRefusedSave:true})`), "Keep mine" (`retrySaveAfterConflict`) |
| Schema-incompatible banner | `~862-885` [V] | `chrome.schemaIncompatible` | "Reload" (`reloadFromServer()`) |
| **Recovery draft banner** "You have unsaved changes from <time>." | `883-905` [V] | `chrome.recoveryDraft` (set by `offerRecovery` from the draft slot, `useTimelineSave.ts:~590`, once per mount) and not conflict | "Save them" (`retryRecoveredDraft`, disabled if `retryAllowed===false`), "Discard" (`discardRecoveredDraft`) |
| Shot-timeline draft banner | `components/ShotTimelinePreview.tsx:341-366` [H] | same `recoveryDraft` | Retry, Discard, Reload |
| Save chip (toolbar) | `components/TimelineEditorShellToolbar.tsx:147-160` [H] | `chrome.saveStatus` (`useTimelineSave.ts:~940`: local status in blocked/conflict/error/recovery/retry or notice -> `error`) | none |
| Toasts | e.g. `useTimelineSave.ts:~900` element saves | errors | none |

## 4. Why the first-time message has no actions [V]

The edit path calls `localSaveSession.append()`. `append` throws synchronously before touching any store: `:350` (`writeError` set or status conflict/error: "Resolve retained local saves before editing again") and `:353` (`replaying`: "Wait for retained dependent saves to finish revalidation before editing again"). The handoff (`hooks/timelineLocalSaveHandoff.ts:~975-981`) wraps any non-TimelineSaveError into `TimelineSaveError("Local document save retained: …")` (`refuse`, `:245-247`; no rejection reason attached). The persistence layer stores the message in `persistence.saveError`, which becomes `saveNotice` -> `saveNoticeBanner`, which has **no buttons**. No draft is written for a refused edit, so `recoveryDraft` stays null and the Retry/Discard banner is absent. After refresh a new session finds retained owners, publishes `recovery`, and the mount effect reads the draft slot written earlier (by the persistence layer) and shows the draft banner. Two different stores (session error text vs draft slot) drive two different banners.

## 5. Transitions and what each clears

| Transition | Entry | Clears |
|---|---|---|
| **Discard** (draft banner) | `useTimelineSave.ts:782-793` -> `reloadFromServer({clearDraft:true})` (`useTimelinePersistence.ts:1609-1700`) [H+V] | Only the draft slot, compare-and-delete (`:1681-1697`; throws "kept for safety" if the snapshot changed). Does **not** call `discharge`; outbox owners, `pending`, session state untouched. |
| **Use latest version** | `useTimelineRealtime.ts:54-61` -> shell `:343` -> `reloadFromServer({discardRefusedSave:true})` -> `session.localDocumentSave.discharge('latest')` (`useTimelinePersistence.ts:1642`) -> `handoff.discharge` (`timelineLocalSaveHandoff.ts:~1013`) -> `session.discharge` (`localSaveSession.ts:408-430`) | `discharge` is a **no-op unless `pending.outcome.kind === 'rejected'`** (`:413`). If rejected: `resolveRejected(all intent ids)` (`commitOutbox.ts:356-374`) empties `intents` + deletes `pending` of the **one claimed owner**; the owner row stays. Then `resetToCanonical` (`:145-155`). Then the draft slot (same compare-and-delete). Other retained owners, `accepted`, `initialization`, placement continuations remain. A `retry` outcome (network error, or an untyped 409) is **not cleared**. |
| **Keep mine** | `retrySaveAfterConflict` -> `discharge('keep')` (`localSaveSession.ts:~418`) | `rebaseRejected` re-queues chain on latest head with fresh request identity; pump resends. Only if pending outcome is `rejected`. |
| **Save them** (draft) | `retryRecoveredDraft` `useTimelineSave.ts:696` | Re-POSTs draft through the normal save path; invalidated when `localOwner.recovered && status==='saved'` (`useTimelineSave.ts:~567-577`). |
| **Reload** (schema banner) | `reloadFromServer()` | clearDraft defaults true (`options.clearDraft ?? !options.preserveDraft`), no discharge. |
| **recover(ownerId)** | `localSaveSession.ts:431-445`, used from recovery state | Releases the current claim and claims the named owner; one owner at a time. Requires `state.status==='saved'` when a box is held. |
| **Refresh** | new session: `createLocalSaveSession` `:343-347` | Nothing cleared. Retained owners listed -> `recovery`; draft slot offered through `offerRecovery`. |

Net: **no handler removes an owner row**. After "Discard" on the draft banner a retained owner stays, status stays `recovery`/`error`, the session has no claimed box, and every edit throws `assertOpen` / `:350` / `:353`.

## 6. Outcome classification (`retry` vs `rejected`) with sources

Classifier `integrations/runtime/client.ts:322-348` (before my change) [V]:
- not ApiError (network `TypeError`, "Failed to fetch") -> `unknown`
- `details.reason` `head_busy` | `runtime_unavailable` -> `unknown`
- 409 + `reason==='stale_head'` -> `conflict`; `details.status==='conflict'` -> `conflict`; `details.status==='refused'` -> `refused`
- 401/403 `authorization`; 400/422 `validation`; storage/disk/space code or reason -> `storage`; status >= 500 -> `unknown`; 413 `too_large`; 404/405 `unsupported_route`
- other 4xx except 408/409/429 -> `rejected_request`; **everything else, including an untyped 409 with `code:'conflict'`, -> `unknown`**
Mapping `unknown|storage -> {kind:'retry'}`, all else `{kind:'rejected'}` at:
- `commands/localSaveSession.ts:268-279` (`transmit` callback; `error.status>=500` short-circuits to unknown at `:274`) [V]
- `commands/commitSession.ts:247-250`, `integrations/runtime/bootstrapInitialization.ts:121-124` [H]
- `commands/commitOutbox.ts:516-519`: transport throw -> `{kind:'retry', error:{reason:'transport_error'}}` [H]
Retry is applied to `pending`, which blocks the head: `pump` returns after `publish('retry')` (`localSaveSession.ts:~268`) and relies on a later pump; there is no retry budget in this loop [V: none seen]. `isRuntimeCanonicalPayloadConflict` (`client.ts:352`) used only by `dataProvider.ts` (409 `canonical_payload_mismatch` still maps to `unknown` in the outbox path) [H].
Runtime side: `runtime_protocol/timeline_commit_port.py:1064-1065` raises `ConflictError("selected media catalog digest changed")` (HTTP 409, `code: conflict`, no `details.reason`).

## 7. Throws that block editing (`commands/localSaveSession.ts`) [V]

- `:128-131 assertOpen`: recoveryError rethrown; "Local save session is closed or awaiting recovery" when `!box` (state after startup `recovery`).
- `:350` "Resolve retained local saves before editing again" (writeError, or status conflict/error).
- `:353` "Wait for retained dependent saves to finish revalidation before editing again" (`replaying`; set `:226,232,317` when an accepted prefix has a retained suffix; cleared only when the queue empties `~:262`).
- `:355-357` label/commands/same-document guards; `:374` publishes error "Local edit could not be persisted".
- `:305-309` "Local saves require a verified original display basis for recovery" (claim fails, `recoveryError` set -> every later call rethrows).
- Handoff-side: `timelineLocalSaveHandoff.ts:245-250 refuse/refuseEdit`.

## 8. Runtime selected-media record (for the digest) [V]

`runtime_protocol/timeline_commit_port.py:967-1075`. Record = realm_id, project_id, asset/generation_id/variant_id, object_id, `generation{type, source_task_id, metadata}`, `variant{variant_type, metadata, managed_output{association_id, task_id, attempt_id, ..., size, media_type, filename, durability, lifecycle, provenance}}`, `entry{object_id, media_type, size, filename, width/height/duration}`; `catalog_digest = digest(record)` (`:1061`). Import response (`service.py:5648-5676`) has no `catalog_digest`; the App gets it from `GET media-selection` (`integrations/runtime/dataProvider.ts:1788-1805`) [H] and resends it at `:880`. `_media_metadata` (`:727-739`) excludes thumbnail/viewed/is_primary/urls. `managed_output.lifecycle` carries `version` bumped by every lifecycle operation (`store.py:6026-6050,6113`) [H].

## 9. Minimal changes for 3-5 under the current structure (input for Fable)

3. **One surface.** Replace `saveNoticeBanner` and `recoveryBanner` with one banner, shown when any of: `recoveryDraft`, `saveNotice`, local status in {blocked,conflict,error,recovery,retry}. Same two actions everywhere: Save them / Retry and Discard. Message from `recoveryDraft` time if present, else the session error/notice. Remove the second copy in `ShotTimelinePreview.tsx:341-366` by sharing the component.
4. **Discard means discard.** Add `discardScope(scope)` to `createCommitOutbox` (delete every `owners` row for realm/actor/project/timeline in one readwrite transaction; stale claims then fail on generation). `session.discharge('latest')` becomes: release current claim, `discardScope`, `claim()` a fresh owner, `resetToCanonical`; run it for every retained state, not only `pending.outcome==='rejected'`. Discard and Use latest both call it, then clear the draft slot.
5. **`replaying` throw.** `:353` guards a state that only the pump can end. Minimal: in the session, when the pump stops with `record.pending` (retry or rejected) and `replaying`, publish a status the unified banner shows (it already is `retry`/`error`), and let Discard (4) clear it. CC-5 (`~/Developer/astrid-dev/plans/18-timeline-editing/`) deletes the throws; remaining there: replace `:350`/`:353` with queueing behind the retained chain.
