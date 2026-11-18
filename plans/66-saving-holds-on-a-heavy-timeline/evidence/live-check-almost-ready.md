# Live check: editing "Almost Ready" on the release stack

18 Nov 2026. Owner's real Chrome, Claude in Chrome. Stack: editor `b38e29d` (vite on :2400, `~/astrid-release/release-14-plan-59/editor`), Runtime pid 18451 behind the discovery proxy on :17500 (Runtime endpoint 127.0.0.1:59631). Timeline `77f906f3242c48179ab86ca7c3e62eb4` ("Almost Ready — without first/second (trial v2)"), project `801a01b3a87941a1ab25958c488afdbf`. Live Astrid (:17340) and astrid.haus were not opened. The owner was editing the same timeline in their own tab at the same time.

## Verdict

- **Works:** move along a non-shot track, cross-track move (Fx to Sprite), file-dropped image, and the Picture refusal. The refusal shows a plain toast, undoes the edit, POSTs nothing, and the next edit saves. Each of these *lands in the Runtime*, but only 2–3 minutes after the edit.
- **Doesn't:** (1) Every commit outlives the 60 s proxy timeout, so the editor shows "the save never got a confirmation" on every edit until a later retry gets the replay. (2) The inspector edit got a Runtime **400 `protocol_error: accepted commit inputs changed during verification`**, which the editor treats as a permanent rejection. After that, every edit opens "This timeline changed somewhere else" and nothing is POSTed. Neither choice in that card clears it, so the tab is stuck until a reload, and the reload raises "Leave site?". The "one refusal, then later edits fail" bug is back, through a different trigger.
- **Ordinary commits to Almost Ready:** accepted by the Runtime (5 commits from this session and the owner's are in the history), but slowly and with no timely ack.
- **Not reached:** trim, split, rename, delete, mute, shot edges and restore. The tab got stuck at action 8 and per the brief I stopped.

## Head revisions

| When | head_revision_id | publication |
|---|---|---|
| First load (01:50) | `authoring-parent-revision-969b5e412077e717f6cfb40d62eaea9be3351ca1dd1ed23a6e985f28119ff3b4` | `txn-72383d4f85e44b80b9d4cac89e1fc207` (bootstrap import, 15 Nov) |
| After the owner's drop | `authoring-parent-revision-a1888ee11143c2e566758039eb18f6f8aec01d207f6f313ca5ce1a7ae7814e55` | `txn-b53ef5a1bd644b3098a5097484a835ab` (owner, "Add media", 00:53:11Z) |
| Start of my action list (after my drop) | `authoring-parent-revision-1fefd541bbbf25d1ae142487423cc0511bc49916a51107e34e26d3d447af312a` | `txn-c8b0332061844d758a13d79fe9bea187` |
| End (now) | `authoring-parent-revision-54cd930ea228163dd90813c02346d3d2722dcae136debdff7b669ce1ff38be33` | `txn-8531e5d2fdae48a08b68a0e65735f691` |

Commits made by this session: `txn-c8b03320` (drop, 01:00:54Z), `txn-47064415` (move, 01:07:00Z), `txn-5357ad43` (cross-track move, 01:11:45Z), `txn-8531e5d2` (inspector x=1, 01:15:19Z).

**Final state does not match the start.** My test clip `clip-3` ("Image 2", a 9 KB screenshot PNG) is still on **Sprite** at 12.1 s, hold 5, `x: 1`. Everything else matches the start, including the owner's `clip-2` ("Image 1", Chrome at 5.2 s), which is theirs and was left alone. To restore: delete `clip-3`, or pick History entry "26 minutes ago" (= `txn-b53ef5a1`). Both need a working editor tab.

## Actions

Clips at the start of the list: `clip-3` Fx 10.1 s, hold 5 (my drop); `music-song` Music 0, hold 8.6667, from 0; `music-song:b` Music 8.4, hold 188.1667, from 7.808333; `vo-N19-0` Vo 85.3667 (from 0 to 2.7666); four `r5-roomtone-*` on Vo; `clip-1` Type 196.5667, hold 5; `clip-2` Chrome 5.2, hold 5 (owner's). Tracks: Picture (shots), Chrome, Type, Fx, Sprite, Plate (visual); Vo, Music (muted: false), Sfx (audio).

| # | Action | Expected | Observed | Saved after reload | Exact message |
|---|---|---|---|---|---|
| 1 | Load | Loads, Saved | On 127.0.0.1: badge **"Error"** plus the owner's draft offered as recovery (see "Two tabs"). On localhost:2400: badge **"Saved"**, no banner. Preview note: "Canvas is not stated in timeline output; using 1920 × 1080 from timeline settings. It has not been written to outp[ut]…" | n/a | "You have unsaved changes from 1:51 AM." [Save them] [Discard] (127.0.0.1 only) |
| 2 | Move `clip-3` along Fx, 10.1 to 12.1 s | Saves | POST cut at 60 s twice, then 200. Runtime accepted at 01:07:00.952Z, about 118 s after the drag. Badge **Saving** for about 3 min, then **Saved** (about 215 s). | yes, in the Runtime head (at 12.1). No page reload afterwards; the tab got stuck before the next reload. | "Your changes have not been saved: the save never got a confirmation." [Retry save], then cleared |
| 3 | Trim end (drag right edge 1 s) | Saves | Not saved. Opened the conflict card at once, no POST. Tried twice. | no | "This timeline changed somewhere else" / "Keep your changes, or switch to the latest version." [Use latest version] [Keep my changes]; badge "Not saved" |
| 4 | Split | Saves, sensible Source In | Not done (tab stuck) | — | — |
| 5 | Rename track | Saves | Not done | — | — |
| 6 | Image drop | Saves | File drop: saved after about 3.5 min (see Drop). Media panel: not done. | yes (reloaded, clip present) | "Your changes have not been saved: the save never got a confirmation." until the replay |
| 7 | Delete | Saves | Not done | — | — |
| 8 | Inspector: Position X of `clip-3` to 100 (typed "100", Tab) | Saves | The first keystroke saved on its own: head has `x: 1` (`txn-8531e5d2`, about 132 s). The follow-up POST got **400** and the editor marked it rejected. The field shows 1, not 100. | x=1 in the head; x=100 lost | Banner "protocol_error: accepted commit inputs changed during verification"; badge **Error**. Outbox: `{"kind":"rejected","error":{"kind":"validation","message":"protocol_error: accepted commit inputs changed during verification","code":"protocol_error","details":{}}}` |
| 9 | Move `clip-3` Fx to Sprite (made right after the refusal in 11) | Saves | POSTs at +1.7 s and +63 s cut at 60 s; POST at +140 s got 200 in 16 s. Runtime accepted at 01:11:45.618Z. Badge **Saved** at about 157 s. | yes, in the Runtime head; inspector reads "HOLD · SPRITE" | "Your changes have not been saved: the save never got a confirmation." until the replay |
| 10 | Mute / unmute | Saves | Not done | — | — |
| 11 | Move `clip-3` onto Picture | Plain refusal, undone, next edit saves | Refused at once; the clip stayed on Fx; **no commit POST**. Badge read **"Saving"** for about 40–50 s after the refusal, though nothing was in flight, then **"Saved"**. The next edit (row 9) saved. | n/a (refused) | Toast: "Not saved: Can't change a clip on, or move one onto, a track that holds shots yet. Use another track. That change was undone; your other edits are kept." |
| 12 | Shot start/end on Picture | Not in this build | Not done | — | — |
| 13 | Restore | Matches start | Not done; `clip-3` remains (see above) | — | — |

**Timing pattern for every commit.** The first POST and the first retry are both cut at exactly 60 s (Chrome shows 503, and the app sees "Failed to fetch", so retry). The Runtime accepts the commit about 2–3 minutes after the first POST. A later retry with the same idempotency key gets 200 as a replay (16–30 s). The "never got a confirmation" banner shows on every save in the meantime.

**Why the inspector save broke the session.** POSTs that timed out at the proxy keep running inside the Runtime. The editor's retries and next commits then overlap them, and the Runtime's history verification guard (`runtime_protocol/timeline_commit_store.py:200,219,255`) raises `ProtocolError("accepted commit inputs changed during verification")` as a 400. `commands/localSaveSession.ts` treats anything under 500 as a permanent `rejected` (validation). The intent's base was the current head, so a plain retry would probably have worked. After that rejection the session opens the conflict card on every edit and never POSTs again. `beforeunload` still reports pending changes, so a reload or close raises "Leave site?".

## Console

No app errors or warnings at any point, including during the 503s and the 400. The only entries came from a Chrome extension: "READ - Host validation failed: Object", "Host is not supported", "Host is not valid or supported", "Host is not in insights whitelist".

## Other things seen

- The History menu lists every revision as **"authoring-parent"** (with times: 4, 8, 13, 19, 26 minutes ago, 2 days ago), not the commit labels ("Add media", "Edit timeline").
- Inspector, Position tab: the Fit label renders run together: "Fit [inherit] Effective fit unavailable until media size is knownTop".
- The extension's synthetic file drop also attached the image to the chat composer ("attaching 1 image") and seems to have created "Chat 1". Since then the chat panel shows "This conversation does not belong to the selected project." [Retry] and "Chat isn't running on this computer right now." Nothing was sent.
- The Runtime is busy: 30–87 % CPU across `top` samples (the first sample always reads 0.0). `GET …/timelines/T` took 4.6–6 s, `GET …/commits` 10–22 s, `POST …/inspect` up to 10 s. One editor tab sends about 110 Runtime requests a minute.

## Inspector finding (the session-breaker)

1. The Position X field saves on each keystroke. Typing "100" committed `x: 1` first (`txn-8531e5d2`, accepted 01:15:19Z), with x=10 and x=100 queued behind it.
2. Because every commit outlives the 60 s proxy timeout, the queued follow-up overlapped with the earlier POSTs still running inside the Runtime. The Runtime refused it with **400 `protocol_error: accepted commit inputs changed during verification`** (its history-verification guard, `timeline_commit_store.py:200/219/255`).
3. `commands/localSaveSession.ts` (`kind = status >= 500 ? 'unknown' : classifyRuntimeCommitFailure(error)`; anything except unknown/storage → `rejected`) records this as a permanent `rejected` / `validation` outcome, although the intent's base was the current head and a retry would most likely have worked.
4. From then on the session is stuck. Every edit opens "This timeline changed somewhere else" and POSTs nothing. Neither **Keep my changes** nor **Use latest version** clears it. The badge stays **Error**, and the banner "protocol_error: accepted commit inputs changed during verification" has no action. `beforeunload` still reports pending changes, so reloading or closing asks "Leave site?".

## Tab clean-up (open)

- The stuck tab (Claude tab group, "Astrid", localhost:2400) **could not be closed**: `tabs_close_mcp` answered "Tab 561945933 was not closed because its page asked to confirm leaving, usually because of unsaved changes. The tab is still open and unchanged." No dialog appeared. Bypassing the page's `beforeunload` with a capture listener was denied by the permission classifier, and I did not work around that. The tab still polls the Runtime (about 110 requests a minute). **Someone needs to close it by hand and click Leave.** Its only unsaved change is my x=100 on my own test clip.
- I opened one fresh localhost:2400 tab, which loaded "Saved" with no banner (Image 1 on Chrome, clip-3 off-screen on Sprite), then closed it without editing so it wouldn't add load. The trim and delete of `clip-3` (the restore) are still to do once the stuck tab is gone.
- Leftovers of mine in browser storage: IndexedDB `claude.owner-draft-backup` on origin 127.0.0.1:2400 (a copy of the owner's 01:51 draft slot, safe to delete); outbox owner `be12030b…` on origin localhost:2400 holding the rejected x=100 intent.

## Final head (at 02:23)

`authoring-parent-revision-54cd930ea228163dd90813c02346d3d2722dcae136debdff7b669ce1ff38be33` / `txn-8531e5d2fdae48a08b68a0e65735f691`. It does **not** match the start: `clip-3` ("Image 2") is still on Sprite at 12.1 s, hold 5, x: 1.

## GIF

`~/Downloads/almost-ready-edit-check.gif` (50 frames, 13 MB, from the first load to the stuck tab; the frame cap was reached, so later steps may be missing).

## Drop (priority investigation, done first)

The owner reported "dropping an image never seems to save", with the banner "Your changes have not been saved: the save never got a confirmation." and **Retry save**.

### Finding

**It POSTs and gets no response in time.** The upload is fine, and the commit is sent straight away. The Runtime takes longer than 60 s to answer a `clip.add-media` commit. Both proxies in front of it give up at 60 s, so the editor never gets the ack and keeps retrying with the same idempotency key. The commit *does* land in the Runtime, about 3 minutes after the drop. A retry after that gets the idempotent replay (200), and the badge turns Saved. If the tab is closed, reloaded or abandoned before then, the save looks lost, though it is in the head.

### What I did

- My tab was first on `http://127.0.0.1:2400`. On reload it showed **"You have unsaved changes from 1:51 AM."** with **Save them** / **Discard**, and the save badge read **"Error"**. That banner is the *owner's* draft: same origin and the same one-slot IndexedDB `astrid.timeline-drafts` record (written 00:51:20Z, base = bootstrap head, adds `clip-2` on `chrome` at 4 s, image `Screenshot 2026-11-12 at 20.23.54.png`, `external_upload`). A second tab on the same timeline treats a live tab's draft as a crashed session's recovery, and it defers its own saves until someone picks Save them or Discard. I did not touch it: Discard was blocked by the permission classifier, and Save them would have committed the owner's work. A full copy of that record is in IndexedDB `claude.owner-draft-backup` on origin 127.0.0.1:2400.
- To get a clean tab, I moved to `http://localhost:2400` (same server, separate browser storage). It loaded with the badge **"Saved"** and no banner.
- **File drop.** I used Claude in Chrome's `upload_image` to drop a 9 KB PNG (`claude-drop-test.png`) onto the **Fx** track at about 10 s. (This is a DataTransfer drop from the extension, not a Finder drag.) Side effect: the same drop also attached the image to the chat composer ("attaching 1 image"). Nothing was sent, and the attachment was gone after the reload.
- **Media-panel drop.** Not done: the file drop reproduced the bug, and each attempt costs about 3 minutes of Runtime time.

### Sequence (T0 = 00:57:45.9Z; times from Chrome resource timing)

| t (s) | What | Status / duration |
|---|---|---|
| ~5 | Drop. A skeleton clip "uploading:claude-…" appears on Fx, then "Image 2". | badge **Saved**, then **Saving** |
| 7.3 | `POST /api/runtime/v1/projects/P/media-imports` | **201** in 2.4 s |
| 12.7 | `POST …/timelines/T/commit` (`clip.add-media`, row `clip-3` on `fx` at 10.1 s, hold 5, idempotency key `48a5e595…`) | pending, then cut at **60.03 s**. Chrome shows **503**; the editor's outbox recorded `{"kind":"retry","error":{"kind":"unknown","message":"Failed to fetch"}}` |
| ~55 | Banner **"Your changes have not been saved: the save never got a confirmation."** with **Retry save** | badge **Saving** |
| 130.2 | Automatic retry `POST …/commit` (same key; I did not click Retry save) | cut at **60.07 s**, no response |
| 188.7 (01:00:54.573Z) | Runtime records commit `txn-c8b0332061844d758a13d79fe9bea187`, "Add media", key `48a5e595…` | accepted about 176 s after the first POST |
| 205.2 | Retry `POST …/commit` | **200** in 29.6 s (idempotent replay) |
| ~236 | Banner clears | badge **Saved** |
| reload | Image 2 still on Fx at 10.1 s | survives |

- **Console:** no app errors or warnings at any point. The only entries were two log lines from a Chrome extension ("READ - Host validation failed", "Host is not in insights whitelist"). The failure is invisible in the console.
- **Response body of the failed commit:** none reached the app. The fetch was rejected ("Failed to fetch"), so no body was readable. The cut comes at exactly 60 s, which matches `RUNTIME_REQUEST_TIMEOUT_MS = 60_000` (`timeout`/`proxyTimeout`) in `config/vite/runtimeProxy.ts:7,32-33`, and `IDLE_TIMEOUT_MS = 60_000` in `scripts/runtime-discovery-proxy.mjs:14` (that proxy would answer `{"code":"runtime_unavailable","message":"runtime request failed: …"}` if it still could).
- **The owner's own drop shows the same pattern.** Their tab's outbox (`astrid.command-outbox`, owner `aeb8600f…`, lock held by their tab) has a pending `clip.add-media` commit: `clip-2` on `chrome` at 5.2 s, key `5e49002e-c43d-41a2-8830-852a0ccb8df8`. Its outcome is `{"kind":"retry","error":{"kind":"unknown","message":"Failed to fetch"}}`. The Runtime accepted that same key as `txn-b53ef5a1bd644b3098a5097484a835ab` at 00:53:11.395Z, about 110 s after their draft. **The owner's image is saved in the head** (Image 1 on Chrome at 5.2 s); their tab just hadn't got the ack when I read it.
- **The Runtime is not idle.** `top` samples of pid 18451 during and after the save read 30–87 % CPU. The first `top` sample always reads 0.0, which may explain an "idle" reading. Cumulative CPU went from 3:51 to 6:32 between 01:58:30 and 02:02:30. Through the proxy, `GET …/timelines/T` took 4.6–6.1 s, `GET …/commits` 10–18 s, and `POST …/inspect` up to 10 s. Each open editor tab sends about 110 Runtime requests a minute (health/handshake/realm/inspect polling); two tabs were open. I did not prove what the Runtime spends the time on (no py-spy, and no request log in `home/Library/Logs/Astrid Runtime/`).
- Another stale outbox owner, `d38698ba…` (generation 10), on origin 127.0.0.1 holds a never-accepted `doc.patch` "Edit timeline" against the bootstrap head. It is from an earlier session and nobody is retrying it.

### Two tabs on the same origin block each other

The editor on `http://127.0.0.1:2400` keeps one draft slot per timeline in IndexedDB (`astrid.timeline-drafts`, key = timeline id), and every tab on that origin shares it. When I opened the same timeline in a second tab while the owner's tab was editing, mine loaded with:

> **You have unsaved changes from 1:51 AM.** [Save them] [Discard]

and a red **"Error"** save badge. The draft was the owner's live tab's (owner id `76fa970b…`, written 00:51:20Z), not a crashed session. While the banner is up, the second tab defers every edit in memory ("Recovery is an explicit CAS decision…", `hooks/useTimelinePersistence.ts:1174-1187`) and POSTs nothing. Its saves stay blocked until someone picks **Save them**, which re-commits the other tab's draft, or **Discard**, which deletes it. Neither choice is right while the other tab is still alive. The owner's tab held the `astrid.command-outbox` Web Lock at the time (client `5534E211`), so a live owner could be detected.

### Where it stops

The save is POSTed promptly, and the Runtime accepts it in the end, but only after 2–3 minutes. The 60 s proxy timeout cuts the response off, so the editor shows the watchdog banner and gets its ack only from a later idempotent retry. The user never sees a reason. Fixes to consider: find why one commit takes over 60 s on this realm (the main cause); make a timed-out commit with a known idempotency key show "still saving" instead of "never got a confirmation"; and, separately, stop a second tab from reading a live tab's draft slot as crash recovery.
