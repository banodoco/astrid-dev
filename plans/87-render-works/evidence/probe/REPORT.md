# r6 probe: how an agent can see and hear a timeline on the release-14 stack

Scope: read-only. Nothing was published, saved, rendered or committed. Timeline: "trial v2" (77f906f3242c48179ab86ca7c3e62eb4) in project "Almost Ready" (801a01b3a87941a1ab25958c488afdbf). Stack: ~/astrid-release/release-14-plan-69, program version 5bf20639e293, Runtime door 127.0.0.1:17501, endpoint 127.0.0.1:50301, runtime_epoch 7.

## Command environment
- CLI: `~/astrid-release/release-14-plan-69/program/run-astrid <subcommand> ...` (this runs `py/bin/python -X utf8 -I -m astrid.omp_agent` with env from `program/versions/5bf20639e293/version.json`). Not `~/.local/bin/astrid`.
- Run under perl `alarm` (no `timeout` binary on macOS). Records in this folder: `01-show.*`, `02-inputs-5s.*`, `03-composed-5s.*`, `04-composed-109s.*`, `05-inputs-109s.*`, `06-runs-list.*`, `health_probe.py`, `health_timing.py`, `pw_probe.cjs`, `pw_seek.cjs`, `pw_play.cjs`, `pw-*.png`, `issue-*.json`.

## Routes tested
| # | Command (flags after `timelines`) | Result | Exit | Time | Output / error |
|---|---|---|---|---|---|
| 01 | `show <tl> --project <p> --json` | WORKS (structure) | 0 | 0.4 s | 50 clips in page, 7 occurrences; `render_timing_context.status = unavailable` ("closure clips lack managed render timing") |
| 02 | `visualize <tl> --mode inputs --at 5 --format md --format png --json` | WORKS on 2nd and 3rd try. First try FAILED (transient) | 0 | 1–2 s | md 11,809 B, png 63,202 B, object ids sha256:2862a00a…, sha256:5a414b18… (not fetched to disk). Declared inputs only, no pixels. |
| 02a | same, first attempt | FAILED (transient) | 1 | 4 s | `{"error":{"code":"unavailable","message":"generic Astrid pack host could not verify runtime identity; run the Astrid install line again"}}` |
| 05 | `visualize ... --mode inputs --at 109 --format md --json` | WORKS | 0 | 1 s | (same inspection schema) |
| 03 | `visualize <tl> --at 5 --resolution 320x180 --format png --json` (composed) | FAILS, deterministic | 1 | 4 s | `canonical registry asset 'a09025f7-40ed-4202-ba40-2d4a61d352a9' contains retired media locator field(s): file`; `fix: Import the bytes into the runtime and reference its object_id/digest.`; `original_type: ManagedRenderValidationError` |
| 04 | `visualize <tl> --at 109 --resolution 320x180 --format png --json` (composed) | FAILS, same error | 1 | 3 s | identical message |
| 06 | `runs list --project <p> --json` | WORKS | 0 | <1 s | Lists runtime tasks (e.g. runtime.media.import.v1). `runs list --timeline` is not a valid flag. Successful render runs were not enumerated. |
| - | audio excerpt / waveform command | DOES NOT EXIST as a standalone route | - | - | Waveforms exist only in `visualize --view filmstrip --render-run <run>` (needs an existing successful render run, which I did not verify). |

The asset `a09025f7-…` is the 5 s PNG hold clip `clip-1` (track "type", at 196.57 s in authored timing). It is the only clip referencing it.

## Limiters found (source, not all triggered)
- `packs/rendering/actions/timeline_visualize/motion/window.py:27-37`: window presets. scan max 30 s / 64 frames; motion max 3 s / 60 frames; beat max 20 s / 48; frame (single still, 1280x720) max 1 s; cut = events.
- `packs/timeline/cli_visualize.py:36, 187-188`: preset window limit is enforced client-side (a whole clip is only auto-windowed if it fits the preset limit).
- `packs/rendering/actions/timeline_visualize/sweep.py:13`: `SWEEP_MAX_FRAMES = 90` for `check --sweep`.
- `packs/rendering/actions/timeline_visualize/thumbnails.py:71`: `MAX_FRAMES_PER_PAGE = 12`.
- `packs/rendering/actions/timeline_visualize/filmstrip_options.py:205`, `filmstrip_cards.py:940`: `max_frames` default 2000 extraction bound.
- `packs/rendering/actions/timeline_visualize/composed_frame.py:31-32`: cache bounds 256 entries / 512 MiB.
- `packs/rendering/actions/timeline_visualize/fast_lane.py:27`: at most 4 moments per page.
- `core/receipts/canonical.py:21,24`: canonical input 1 MiB, output 4 MiB (the "4 MB limit" in astrid-dev #1238).
- `core/execution/remotion_frame_owner.py:24-25,112-114,354-355`: frame-owner policy `max_frames` / `max_resolution` (values come from admission; not inspected).
- `core/rendering/remotion_runtime.py:546`: installed-profile guard rejects any non-empty PYTHONPATH or ASTRID_PACKS_PATH (issue #748). Not triggered in this env (no such vars in version.json env).
- `core/rendering/remotion_runtime.py:1260-1268`: runtime validation context must match the launch-time variant (issue #1253). Not reached in this session.
- No concurrency semaphore or quota was found on the visualize path. The "one local capacity slot" is in `core/execution/managed_tool_session.py` (managed tool sessions), not visualize.

The "limiter" the owner remembers is most likely the preset window caps (3 s motion, 1 s frame) and the 12-frame page size, not a global quota. Verified by reading source; the owner's exact memory is inferred.

## Runtime logs
- `home/Library/Logs/Astrid Runtime/service-pack-host.log`: repeated `generic host claim failed: ApiError: transport_timeout: runtime request timed out` (54 occurrences, through 15:02 CET). Matches the transient failure of test 02a.
- `data/runtime/generic-host.ready.json`: status ready, 44 ready capabilities. `rendering.timeline_visualize`, `rendering.render`, `rendering.timeline_export_plan`, `rendering.timeline_prepare_import` ready. Unready: generation.generate_image_codex, generation.generate_speech, hivemind.ingest_youtube, training.pool_build, training.pool_merge.
- Direct RuntimeProtocolClient health with the pack-host worker token: ok, 3/3 calls at 0.0 s (probe 'health_timing.py').
- Editor log (`logs/editor-20261122-142917.log`) shows only the start banner.
- Note: `ASTRID_INSTALL_RELEASE=13` and `identity.release=13` in version.json and discovery; the stack is named release-14 but identity says 13 (verified; cause of any confusion not established).

## Playwright fallback (editor on :2400)
- Playwright 1.60.0 from `editor/node_modules`, chromium headless, viewport 1440x900.
- The preview paints. Video element readyState reached 4 at ~9.9 s after load. The 5 s screenshot shows the Discord-style frame (`pw-02-seek-5s.png`, timecode 0:05.36 after a ruler click).
- Playback reached 1:49.56 (`pw-05-play-109s.png` shows the Three.js bird scene and the "Make me a 14-second bird flight" chat). Took about 2 min of real playback, not an instant seek.
- Seeking by ruler click works up to about 35 s at default zoom; beyond that the ruler labels are virtualised out of the DOM, and scrolling did not restore them. Play was the workable route to 109 s.
- Console/network errors (verbatim):
  - `POST http://localhost:2400/__astrid/local-update-status` → 503
  - `GET http://localhost:2400/api/runtime/v1/objects/sha256%3Ac0efc003046c485f8b58d97b7c2847a96f20f6e65c8b91b594aa64fbacb8ac79` → 404 "Failed to load resource: the server responded with a status of 404 (Not Found)"
  - several `net::ERR_ABORTED` requests for object ids (sha256:fece12c…, sha256:1598f0a…, sha256:df7b18f…), usually during seeks.
- Playwright did not click Save, Render or any write control. Zoom and ruler/Play/Pause only.

## GitHub issues (banodoco/astrid-dev), fetched via public REST (gh is not installed on this Mac)
- **#748** "Composed timeline visualization fails installed registry discovery while inputs mode works": OPEN, 1 comment (2026-11-21, reproduced on a fresh Release 13 install). Diagnosed cause: installed-mode guard `remotion_runtime.py:546` rejects PYTHONPATH/ASTRID_PACKS_PATH. No fix PR linked in the issue timeline. Not present in this stack's env, so not reproduced here.
- **#1253** "every timeline render is refused on an installed release": OPEN, no comments. Diagnosed (traced, not tested): `_validated_runtime` context mismatch (`remotion_runtime.py:~1267`) plus blank run events. No linked fix PR. Not reproduced (no render run, as instructed).
- **#1238** "timelines visualize fails the whole timeline on one stale asset": OPEN. Its first case (retired `file` locator) is exactly what I reproduced (tests 03 and 04). Its second case (canonical JSON over 4 MB) is related to `core/receipts/canonical.py:24`. Its third case is #748.
- Fix status: no linked fix PR for any of the three was found on the issue timelines. I did not check the pinned heads for a fix: `state/heads.tsv` pins release/14/plan-69 at agent 83d5f8f and runtime b2ea261 (install-manifest), and none of the three issues has a merged-PR cross-reference, so the fix is absent by default (inferred).

## Verdicts
| Route | Works? | Cause |
|---|---|---|
| visualize --mode inputs | Yes (declared placements, no pixels) | n/a |
| visualize composed (default) | No, for the whole timeline | ManagedRenderValidationError on the retired `file` locator of asset a09025f7 (`managed_timeline.py:630-636`) — **verified**. Fails before any frame is captured, so it is not time-dependent. Matches #1238 case 1. |
| visualize `--view filmstrip --render-run` | Not tested | needs a successful render run; no render run was verified |
| render | Not tested (out of scope) | #1253 (inferred from code) |
| Playwright on :2400 preview | Yes, paints in ~10 s; playback reaches 109 s | the object 404 and ERR_ABORTED noise is a missing-object issue, not verified cause |
| visualize inputs, first try | Transient failure | pack-host claim `transport_timeout` (verified in log; cause inferred as runtime load) |

Fix suggestion (inferred): drop or rewrite the `file` field on asset a09025f7 through the editor's replace-media flow (no write done here), or patch the validator to ignore a retired locator when a valid object_id/digest exists.
