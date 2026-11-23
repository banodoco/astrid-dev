# Almost Ready — trial v2 render outcome

Verified: one new render attempt, using exactly the saved `tighten/render-command.json` argv, launched by `python3 -u render/run_attempt.py 1`. No restart or installed/timeline content change. Target version 37, published parent revision `authoring-parent-revision-f9237406fdda59eea5c81e30fd6548eb7b42e0a26655058155f6db6da97e5488`, before/after read matches. Native 1920×1080, 30 fps, MP4 H.264/yuv420p, stereo AAC 48 kHz requested.

## Attempt and timings

Exact command:

```sh
bash astrid-stack.sh timelines render 77f906f3242c48179ab86ca7c3e62eb4 --project 801a01b3a87941a1ab25958c488afdbf --backend rendering.remotion --profile '{"width": 1920, "height": 1080, "fps_rational": [30, 1], "time_base": [1, 90000], "container": "mp4", "video_codec": "h264", "video_profile": null, "video_level": null, "pixel_format": "yuv420p", "audio_codec": "aac", "audio_sample_rate": 48000, "audio_channel_layout": "stereo", "duration_tolerance": 1}' --output-name almost-ready-trial-v2-20261122.mp4 --wait --timeout-seconds 14400 --json
```

Verified: foreground wrapper started 17:31:26.193 UTC; task admitted 17:31:34.919, claimed 17:31:35.291; progress 10%/render at 17:32:20.713; terminal failure 17:32:42.990. CLI exited 1; wrapper completed at 17:32:43.619, 77.425446 s total. Task `dedaae737b9448429cee630699bf1735`, run `58c11b96f5c54737926d68fb85c0aba7`, attempt `c32c89ae38664460bea6e92eacceb3dd`. Executor outputs empty. Task marked executor_failed, retryable false.

Verbatim CLI error:

```text
Headline: The render couldn't finish
Detail: capability 'rendering.render' exited 1: rendering.remotion does not support this render request
reason: local assets are not renderable: Asset 'a09025f7-40ed-4202-ba40-2d4a61d352a9' contains retired media locator field(s): thumbnailUrl
reason: runtime validation consumer context differs: this process's environment was not validated at launch (only the host and Remotion-capable capability workers are)
Fix: Review the details, correct the render settings or timeline, and try again.
```

Verified lease observations: at 17:32:28.922 the Runtime returned updated_at 17:32:25.727 and lease_expires_at 17:32:55.726 (raw `task-heartbeats.jsonl`). Inferred: successful heartbeat renewal around 17:32:25.727 given store heartbeat update semantics and 30 s expiry. This is the last observed renewal, not a proven final heartbeat; the event ledger does not emit each renewal and no final acknowledged-heartbeat diagnostic was produced for this ordinary executor failure. This attempt did not fail with lease_lost or transport_timeout. The helper's order-only list query received HTTP400, not a Runtime stall; direct task snapshot succeeded. Failed helper monitor rows were retained transparently.

Verified host preflight phases: complete_inputs 12,401 ms, owned_probe 218 ms; later complete_inputs 8,881 ms precedes backend rejection. Last20 host lines retained in `pack-host-failure-tail.log`. Runtime/host CPU immediately after failure 0.2%/0.5%, RSS 118,320/76,704 KiB. Samples began about seven seconds after failure; they cannot reconstruct the exact failure instant. They show waiting/polling rather than a persistent hot loop. Before/after request tables and raw measurement data are in `RUNTIME-HEALTH.md`. Runtime startup log had no request timing evidence that localizes historical stalls.

## Checked blockers and decision

Verified source: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a/astrid/packs/rendering/actions/render/managed_timeline.py:45` preserves thumbnailUrl in projection; `:630` admission omits it from forbidden fields. `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a/astrid/core/rendering/assets.py:260` iterates every asset; `:266` forbids thumbnailUrl; `:275` raises. The downstream field mismatch is deterministic on this pinned registry. Source trace identifies the alias as previously unused; no field/reference editing was performed.

Verified source: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a/astrid/core/rendering/remotion_runtime.py:1264` requires one exact launch-artifact context; `:1267` raises the second error. Which projected field differs is unverified. Smallest product fix inferred: remove non-media thumbnail locators in renderer-only registry projection, without modifying the published head; align admission and materialization policies. Separately, validate the exact effective consumer context at worker launch, with a safe field-diff diagnostic (`astrid/sdk/host_bootstrap.py:1347`, `generic_host.py:10248`, `remotion_runtime.py:1239`). A context repair/relaunch may be needed; a restart alone cannot fix the registry mismatch.

Verified source: editor enqueue `editor/src/tools/video-editor/lib/renderRouter.ts:961` submits timeline_ref and canonical metadata, not browser registry bytes, so its Render button is not a different registry remedy. Host heartbeat pump is a separate thread, 5 s polling and 2 s lifecycle RPC cap (`generic_host.py:555,5646,12016,12266`; guards.py:201 authority window300). Store lease30 s. No shared HTTP connection: generated client uses a fresh urllib request; host lifecycle options are copied per call. Heavy renderer is a subprocess, with Remotion concurrency1 (`rendering/renderers/remotion/run.py:1263`). No documented setting found to bypass either rejection; frame ranges retain the same validation. Full source evidence: `SOURCE-TRACE.md`, `BLOCKER-TRACE.md`.

Decision inferred from verified failures/source: stop after one new attempt; another unchanged-head/configuration-only attempt has no justified remedy for both blockers. No patch, reinstall, GitHub post, SQLite modification, unrelated process action, timeline edit, or external film assembly performed.

## Delivery and requested still/audio checks

Verified: no successful product video or provenance output; no Desktop file copied. ffprobe duration/dimensions/fps/audio, ebur128 loudness, rendered-file stills and contact sheet are unavailable. Every requested visual check is unverified: Discord names2.5; tomorrow7.9/9; unlabeled pipeline12.5/15.5; picture26.6; differing time-lapse36/40; 2million48.3; GitHub56; short hair77.9; cream UI109; orange everything150.3/shared156.6; end card195. No claim of black/missing-media frames can be made without a rendered file. Trombone26.5 and no-bells10.5–16.3 audio checks likewise remain unverified. No editor screenshots are substituted.
