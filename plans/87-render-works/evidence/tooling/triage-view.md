# r6 triage: editor preview and tooling defect groups V1-V6

Read-only. Nothing modified in any repo, no GitHub posts, no Astrid CLI run.
Trees: astrid-agent release/14/main worktree `~/Developer/astrid-release-src/wt-r14-fix-1238` ("wt"); installed agent `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a` ("inst"); editor `~/astrid-release/release-14-plan-69/editor/src` ("ed"). wt and inst are byte-identical for every file quoted below except where noted.
Labels: [V] = verified by reading the file; [I] = inference.

## GitHub search status
- Search API hit its rate limit mid-run (about 30 searches per minute); about 40 searches landed. Issue numbers below were fetched directly by number, not from search.
- Search helpers and raw JSON: `.../scratchpad/r6/tooling/gh-r6/`.
- Relevant issues (banodoco/astrid-dev, all open as of 22 Nov):
  - #1238 "timelines visualize fails the whole timeline on one stale asset" (21 Nov). Matches the retired `file` locator error in probe item 03/04.
  - #748 "Composed timeline visualization fails installed registry discovery" (22 Nov).
  - #1253 "every timeline render is refused on an installed release" (21 Nov).
  - #1262 "editor preview goes black after a paused seek" (21 Nov). Same preview seek path, different symptom.
  - #1392 "an agent cannot hear a stretch of the timeline without a render" (22 Nov). Audio, not frames.
  - #1234 "skill points at an old client; error suggests a reinstall" (21 Nov).
  - #799 "Managed installs: the Runtime start message points the wrong way" (17 Nov).
- No issue or PR found for: frame-seek URL/handle, 1:1 preview, ruler virtualisation, video registry resolution, `media open --materialize` docs, the `transport_timeout` to identity message, the preview pack timeout text, or sub-pixel preview jitter.

## V1. Preview has no frame seek handle, no 1:1 mode, ruler stops near 35 s
(a) Existing: none for the seek handle, 1:1 mode or ruler. Closest: #1262 (open, black after paused seek; same `requestSeek` path). Not a duplicate.
(b) Verified:
- `ed/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:152` `const playerRef = useRef<PlayerRef>(null);`
- `RemotionPreview.tsx:614-625` `useImperativeHandle(ref, () => ({ seek, play, pause, togglePlayPause, toggleFullscreen, get isPlaying() ... }))`. The `PreviewHandle` (lines 32-39) is available only through a React ref. It is not on `window` and has no URL input.
- `RemotionPreview.tsx:597` sets `data-astrid-preview-frame-ready`. This is the only DOM hook found.
- `RemotionPreview.tsx:148` and `:706` take `initialTime` and feed `initialFrame`. Callers pass `currentTime` (`useVideoEditorPreviewSurface.tsx:150`). So a `?t=` param would only need wiring to this existing prop.
- URL params read in the editor: `project`, `timeline`, `settings`, `localBrowserRender`, `debugTimeline`, `scenario`, add-generation params. There is no `frame` or `t`. Grep: `tools/video-editor/**`.
- No "actual size" or 1:1 option found in PreviewPanel. The Player fits to the container (see V2).
- `ed/tools/video-editor/components/TimelineEditor/TimeRuler.tsx:7` `const OVERSCAN_STEPS = 4;` and `:78-90` compute `visibleRange` from scroll and viewport only. Labels outside that window are not mounted. The ~35 s figure is from the probe log, not re-measured [I].
(c) Local fix: partly. `?t=` or a `window` handle that forwards to the existing `PreviewHandle.seek` is small [I]. 1:1 mode and ruler labels past the window are not small.

## V2. Preview `<video>` vs render `<img>` for sub-pixel motion
(a) Existing: none found. #1262 shares the preview surface only.
(b) Verified:
- The preview scale is Remotion's, not the editor's. `ed/node_modules/@remotion/player/dist/esm/index.mjs:303` and `:312` set `transform: \`scale(${scale})\``. `RemotionPreview.tsx:694-716` passes `style={{ width: '100%', height: '100%' }}` and no scale.
- Preview path: `ed/node_modules/remotion/dist/cjs/video/OffthreadVideo.js:39-43` returns `VideoForPreview` when not rendering.
- Render path: `OffthreadVideo.js` `environment.isRendering` branch returns `OffthreadVideoForRendering`. That component renders `Img` (`OffthreadVideoForRendering.js:209`).
(c) Local fix: no. The snapping cause is inferred from the probe's measurements, not from Chromium. The fix sits in Remotion or the composition layout.

## V3. Videos with "size unknown" fall back to the box size
(a) Existing: none found.
(b) Verified:
- `tests/fixtures/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx:233` `const size = parseSize((props.assetEntry as {resolution?: string} | undefined)?.resolution) ?? parseSize(p.sourceSize) ?? {w: boxW, h: boxH};`. The file is a test fixture in both trees, so the built-in element location is not confirmed.
- Registry writer for `resolution`: `astrid/sdk/media_handles.py:527-528` `if descriptor["media_type"].startswith("image/") ...: entry["resolution"] = f"{image.width}x{image.height}"`. Images only, via PIL. No video branch.
- Video probing exists: `astrid/core/media.py:244` `probe.resolution = f"{probe.width}x{probe.height}"` (ffprobe, `_parse_ffprobe_payload`). It is not called from the registry writer above [I, from reading both files].
(c) Local fix: yes [I]. Reuse the existing ffprobe helper in `media_handles.py` for `video/*` (same guard as the image branch). Needs a test. The am-footage fallback is a separate, optional change.

## V4. No CLI route to an asset's bytes
(a) Existing: none for `media open --materialize`. #1392 is an adjacent idea (audio via render), not a duplicate.
(b) Verified, and the friction log's "no route" claim does not hold:
- `astrid/core/cli/domain_media.py:311-331` defines `--materialize` ("Write a verified bounded copy to a disposable local path.") and `--max-bytes` (default `10 * 1024 * 1024`, help "Maximum bytes read/materialized (default: 10485760)"). Identical in inst.
- `astrid/sdk/media_open.py:24-26` `DEFAULT_MATERIALIZE_BYTES = 100 * 1024 * 1024`.
- `media_open.py:374-386`: with no `--materialize` and size over `max_bytes`, the result is `availability: "oversize"`, `local_path: null`, and `next_actions: [{"action": "materialize", "max_bytes": 104857600}]`.
- `media_open.py:388-389`: with `--materialize` and size over `max_bytes`, it fails with `size_limit`.
So a 50 MB video needs `media open <ref> --materialize --max-bytes 104857600`. The `--max-bytes` help text does not mention this.
(c) Local fix: yes, docs/help only: state in `--materialize` help that `--max-bytes` must be raised (and to what). This is a discoverability gap, not a missing route. Not run live [I].

## V5. Transient pack-host timeout reported as identity failure with "run the Astrid install line again"
(a) Existing: #1234 (open) is the closest on the next_action wording. #799 (open) is the closest on a misleading Runtime message. #1238 and #748 are adjacent visualize failures, not this one.
(b) Verified chain:
- `astrid_runtime_client/generated.py:686-688` maps `TimeoutError` to `ApiError(0, "transport_timeout", "runtime request timed out")`.
- `astrid/sdk/host_bootstrap.py:2180-2185`:
  ```
  runtime_client = RuntimeProtocolClient(...)
  health = runtime_client.health()
  except Exception as exc:
      raise PackHostBootstrapError(
          f"generic Astrid pack host could not verify runtime identity; {reconfigure_action}"
  ```
  The `except Exception` does not distinguish `transport_timeout` from a real identity mismatch. The original `ApiError` is chained (`from exc`) but its code is dropped from the message.
- `astrid/sdk/autobootstrap.py:510-511` wraps it as `AutoBootstrapError(str(exc))`. `autobootstrap.py:21` `RECONFIGURE_ACTION = "run the Astrid install line again"`. `autobootstrap.py:32-33` defaults `next_action` and `code="runtime_lifecycle_error"`. That matches the probe's `details` block.
- Log side: `astrid/core/execution/generic_host.py:14755` prints `generic host claim failed ... transport_timeout`.
(c) Local fix: yes. In `host_bootstrap.py` catch `ApiError` with code `transport_timeout` first and raise a retryable error (for example "runtime did not answer the identity check in time; retry"), with a retry `next_action`. Needs a unit test. The identity-mismatch path stays unchanged.

## V6. Editor preview: pack load timeout and per-clip "exact admitted pack revision" text
(a) Existing: none for the timeout text. PR #368 (open, "Plan 69: Land the project-element editor") and PRs #518 and #98 (closed, Plan 69) are the feature that introduced admission. Not duplicates.
(b) Verified:
- Timeout: `ed/tools/video-editor/runtime/admitted-elements.ts:88` `reject(new Error('Preview pack loading timed out. Check the local connection and inspect/admit the project pack, then reload the editor.'))`, armed at `:84-90` with `ADMITTED_ELEMENT_LOAD_TIMEOUT_MS`.
- Value: `admitted-elements.ts:23` `ADMITTED_ELEMENT_LOAD_TIMEOUT_MS = ASTRID_BRIDGE_REQUEST_TIMEOUT_MS`; `ed/tools/video-editor/data/astridBridgeWire.ts:10` `ASTRID_BRIDGE_REQUEST_TIMEOUT_MS = 30_000`. So 30 s, which matches the 24-30 s inventory and project-elements reads in the sweep log.
- Banner: `RemotionPreview.tsx:733` `<p>Preview pack could not be loaded. {admissionError}</p>` with a "Retry preview" button.
- Per-clip: `ed/tools/video-editor/compositions/TimelineRenderer.tsx:466` `const exact = \`Element ${ref.id}@${ref.revision} requires its exact admitted pack revision. Embedded source is preserved for migration and is not executed.\`;`. The same string is appended in every branch (`:467-470`). When phase is `error`, the message also includes the admission error text, so the timeout wording does appear. When phase is `loading`, it says "still loading".
(c) Local fix: yes, small. Two options: raise or retry the fetch, or show the timeout cause in the per-clip line when phase is `error` (already partly done). A retry on timeout would need a test.

## Notes on the friction logs
- demo FRICTION item 3 ("no CLI route to bytes") is contradicted by V4.
- demo item 1 (`visualize --at 109.56` failing on the oldest revision with the identity message, 3 of 3) is V5. The probe's head-revision failure (retired `file` locator) is #1238. These are different errors.
- demo item 1d and sweep item 9: the `PreviewHandle` ref exists (V1), so the fibre walk was not needed for a React-side caller. No window handle exists.
