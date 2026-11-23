# Tool friction: demo shake investigation (trial v2, 101.9–145 s)

Stack: release-14-plan-69, CLI `r6/astrid-stack.sh` (= `program/run-astrid` with the start-2400.sh env).

## 1. No frame-accurate composed frame for this timeline
- Command: `astrid-stack.sh timelines visualize 77f906f3… --project 801a01b3… --revision-id <oldest revision 969b5e41…> --at 109.56 --resolution 1920x1080 --format png --json`
- Error (verbatim, stdout): `{"error":{"code":"unavailable","details":{"lifecycle_code":"runtime_lifecycle_error","next_action":"run the Astrid install line again"},"message":"generic Astrid pack host could not verify runtime identity; run the Astrid install line again"}}` — 3 of 3 tries. Pack-host log at the same time: `generic host claim failed (1 consecutive): ApiError: transport_timeout: runtime request timed out`.
- On the head revision the same command fails deterministically with the retired `file` locator on asset a09025f7 (astrid-dev #1238, reproduced by the r6 probe).
- Expected: one composed frame of the demo clip. One bad asset 87 s later, or a busy host, should not block a frame at 109.56 s.
- Source: `packs/rendering/.../managed_timeline.py:630-636` (whole-timeline validation before capture); host identity check in the generic pack host.
- Advice "run the Astrid install line again" is wrong for a transient claim timeout: nothing about the install changed and the next call can succeed.
- Workaround used: a Chrome harness that reproduces `am-footage`'s placement math with the exact source frames (`demo/harness/`), plus Playwright on the editor preview with `PlayerRef.seekTo` found through the React fiber (`demo/preview-measure/`).
- What an agent needs: `visualize --at T` that validates only the clips active at T (or skips/flags the broken one), a `--clip <id> --every-frames 1 --range a..b` frame dump at full resolution, and a retryable error for host timeouts.

## 1b. A dry-run commit reports "may or may not have been committed"
- Command: `r6/edits/stackpy.sh demo/edit_hold.py --dry` (`Timeline.commit(fn, ..., dry_run=True)`).
- Error (verbatim): `astrid.sdk.workspace_client.WorkspaceClientError: [Errno 32] Broken pipe` → `astrid.sdk.timeline.sync.CommitOutcomeUnknown: No reply could be verified; this edit may or may not have been committed. Call tl.commit() again with no arguments to confirm the saved request; the edit is not re-run blindly.`
- Expected: a dry run can never commit, so the message should say "dry run failed in transport, nothing was saved, retry". The scary wording sent me to check the head (unchanged, 7c5aefc4…) and `pending_list()` (empty) by hand.
- Source: `astrid/sdk/timeline/sync.py:1075` (`_flush`) and `:1166` (raises CommitOutcomeUnknown without checking `dry_run`).

## 1c. SERIOUS: one-param edits through `Timeline.commit` and `timelines edit --draft` rewrite unrelated clips
- `Timeline.open(P,T).commit(lambda t: t.clip("d-typing").set(push=None), dry_run=True)` built a 1.9 MB body (`doc.patch`, 449 changes): 242 `list.remove` of c17 time-lapse steps (`c17-tl-339`, `-338`, …), 204 `set`s on c17 clips, `c17-00-am-footage.at` 0.0 → -0.000333, its `app.astrid.until "c18"` removed. The d-typing change itself was **not in the patch** (`push=None` is silently a no-op). It failed only because the runtime dropped the 1.9 MB request after 20.7 s (`[Errno 32] Broken pipe`). Had it gone through, it would have wrecked another agent's c17.
- `timelines edit 77f9… --project 801a… --draft r6-demo --clip d-typing --set push.to=2.4 --no-sweep` reported `✎ c34.adapt-1 146.967–155.667 → 145.233–158.300 s` (and adapt-2, found-1..4 the same): formula re-derivation retimed six c34 text clips I never touched. I discarded the draft (`Checkout.draft(...,"r6-demo").discard()`).
- Expected: an edit's patch contains only the requested change; re-derivation of other clips' formulas is never folded into someone else's edit, or is shown and refused by default.
- Source: `astrid/sdk/timeline/commit_session.py:603` (commit → `sync.py:1075` flush); draft edit in `astrid/packs/timeline/cli.py` `_cmd_edit`.
- Workaround that worked: the detached-document route `python -m astrid.packs.rendering.docs.scripts.timeline_document checkout|check|publish`. `check` showed exactly 6 changed paths; publish pinned the base (expected head) and landed exactly 6 clip changes.

## 1d. Editor preview cannot be told apart from the film without your own harness
- The preview is a live Remotion `<Player>` (`editor/src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:694-716`), scaled by CSS `matrix(0.386458)` at a 1440x900 window. There is no `window` handle, URL param or CLI to seek it by frame; the only route was walking the React fiber from `[data-preview-revision]` to the `useRef<PlayerRef>` (`RemotionPreview.tsx:152`) and calling `seekTo(frame)`.
- What an agent needs: `?frame=N` (or `window.__astridPreview.seekTo`) and an "actual size" (1:1) preview mode, plus a composed `visualize --frame N --clip <id>` that works when an unrelated clip is broken.

## 2. Asset registry has no resolution for videos
- `timelines assets` lists every R5-TOUR video as `video/mp4  size unknown`. `am-footage` then falls back to the box size (`parseSize(resolution) ?? parseSize(sourceSize) ?? {w: boxW, h: boxH}`). ffprobe: T1/T2/T3-KEYFRAMES/T4 are 1920x1080 60 fps, T3-EQUAL-4 1920x1080 30 fps, RAW-THREEJS 1280x720 (same aspect, harmless), but **RAW-H3 is 1344x768 (1.75:1)**. So d-h3-f1 is drawn into a 16:9 box: the render path (`<img>`, object-fit fill) stretches it 1.6 % wide; the editor preview (`<video>`, object-fit contain) pillarboxes it with ~15 px #0C0906 bars per side. Preview and render disagree, and nothing warns. Expected: the registry probes video resolution on import, or `am-footage` reads `videoWidth/Height`, or `timelines check` flags an asset with no resolution on a cover-fit element.
- Source: `am-footage/component.tsx` (`const size = parseSize(...resolution) ?? parseSize(p.sourceSize) ?? {w: boxW, h: boxH}`); Remotion 4.0.509 `OffthreadVideo.js:39-43` (preview → `VideoForPreview`, render → `OffthreadVideoForRendering` → `<Img>`).

## 3. Asset bytes are only reachable by reading the CAS
- No CLI route gives the local path of an asset's bytes; I read `data/runtime/realms/<realm>/cas/sha256/<2>/<62>` directly (read-only) to ffprobe/decode the sources. Expected: `media path <asset>` or `media export`.
