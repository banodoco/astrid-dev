# Overlay tooling friction

## Single-revision shot media admission fails on sandbox
- Command: `./edits/stackpy.sh overlay/probe.py` (dry run against project `23d9b5a570b2498d878edced4f3d4942`, timeline `r6-occurrence-swap-probe`). The script registers `hair/final/R6-RW-01.png`, adds one fixed-time shot-owned `am-footage` clip and asks the SDK to emit the changes and media admission together.
- Verbatim error: `astrid.sdk.workspace_client.WorkspaceClientError: semantic step assertion differs from execution`; surfaced as `astrid.sdk.timeline.sync.CommitRefused: The edit no longer matches the timeline it was made from; nothing was committed. The commands were captured from a different copy of the timeline. Inspect the saved edit with tl.pending_show("pc_57b2243aefb7"), fix the edit, then retry or drop it.` Details: `code: capture_mismatch`, `reason: capture_mismatch`, `path: []`, with base and current both `authoring-parent-revision-bc0c42e5585e6ab65c38a028f5b8a71477178ddb828784b4242b43936c35fdf3`.
- Expected: a single atomic, expected-head revision admitting the media and inserting only the new clip and its registry entry.
- Source: installed `astrid/sdk/timeline/commit_session.py:514` appends `media.admit` to emitted document changes; Runtime rejects the captured semantic step. Freeze's earlier independent reproduction is in `freeze/FRICTION.md` item 5.
- Workaround demonstrated by freeze: admit media using parent helper clips in a separate revision, insert shot clips in another, then remove the helpers in a further revision. This conflicts with the brief's one revision per job (or per clip) and outgoing-change restrictions, so was not applied to the target.

## Python script name shadowed standard library
- Command: `./edits/stackpy.sh overlay/inspect.py`
- Verbatim error: `ImportError: cannot import name 'Timeline' from partially initialized module 'astrid.sdk.timeline.api' (most likely due to a circular import)`.
- Expected: import the SDK normally. Source: Python `dataclasses.py:5` imports `inspect`, which resolved to the local script. Workaround: renamed the script to `overlay/read_bundle.py`.

## Editor preview pack timeout
- Command: `node overlay/verify/capture-hair.cjs` against the editor at `http://localhost:2400`.
- Verbatim error: `Preview pack could not be loaded. Preview pack loading timed out. Check the local connection and inspect/admit the project pack, then reload the editor.`
- Expected: admitted preview elements load and frame captures are unobscured. Source: `editor/src/tools/video-editor/runtime/admitted-elements.ts:88`.
- Workaround: wait and reload, as in `overlay/verify/capture.cjs`. The later 33-frame capture succeeded without the dialog, though late video samples appeared black at a 400 ms wait. A focused retry (`node overlay/verify/capture-late-fallback.cjs`) with a five-second wait showed the expected pictures at frames 3900, 3960, 3989, 3990, 4110 and 4149.
