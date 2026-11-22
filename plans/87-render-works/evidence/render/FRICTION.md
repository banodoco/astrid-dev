# Render tooling friction — 2026-11-22

## Product render rejects an admitted request

Command:

```sh
bash astrid-stack.sh timelines render 77f906f3242c48179ab86ca7c3e62eb4 --project 801a01b3a87941a1ab25958c488afdbf --backend rendering.remotion --profile '{"width": 1920, "height": 1080, "fps_rational": [30, 1], "time_base": [1, 90000], "container": "mp4", "video_codec": "h264", "video_profile": null, "video_level": null, "pixel_format": "yuv420p", "audio_codec": "aac", "audio_sample_rate": 48000, "audio_channel_layout": "stereo", "duration_tolerance": 1}' --output-name almost-ready-trial-v2-20261122.mp4 --wait --timeout-seconds 14400 --json
```

Expected: full native render of the published head. Verified exit1 after77.425446s; verbatim error:

```text
Headline: The render couldn't finish
Detail: capability 'rendering.render' exited 1: rendering.remotion does not support this render request
reason: local assets are not renderable: Asset 'a09025f7-40ed-4202-ba40-2d4a61d352a9' contains retired media locator field(s): thumbnailUrl
reason: runtime validation consumer context differs: this process's environment was not validated at launch (only the host and Remotion-capable capability workers are)
Fix: Review the details, correct the render settings or timeline, and try again.
```

Source: installed `a/astrid/core/rendering/assets.py:260-276`; admission's narrower forbidden set at `a/astrid/packs/rendering/actions/render/managed_timeline.py:630`. Consumer-context mismatch at `a/astrid/core/rendering/remotion_runtime.py:1239-1268`; launch contexts at `a/astrid/sdk/host_bootstrap.py:1347-1362`, worker readiness projection at `a/astrid/core/execution/generic_host.py:10248-10282`. Prefix `a/` means `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/a/`.

Workaround: none found within no-install-edit/no-timeline-change scope. Stop before an unsupported retry. Inferred smallest product changes and exact editor task route are in BLOCKER-TRACE.md and REPORT.md.

## Monitoring query rejected (helper mistake)

Command: GET `http://127.0.0.1:17501/api/runtime/v1/projects/801a01b3a87941a1ab25958c488afdbf/tasks?limit=1&order=admitted_desc`, Origin https://astrid.haus. Verbatim HTTP400: `task kind/order must be root_generation/admitted_desc together`. Expected latest render task. Source `r/runtime_protocol/service.py:2446` validates the pair; root_generation would exclude this non-generation render. Correct workaround: list without order, identify active render, then GET `/api/runtime/v1/tasks/dedaae737b9448429cee630699bf1735` using `task_snapshot.py`. The running renderer was unaffected. Rejected rows retained in attempt-1-progress.jsonl; last observed renewable lease retained separately. Runner corrected for any future authorized attempt.

## Initial door/OS probes (corrected)

Command `curl ... http://127.0.0.1:17501/v1/health` returned `{"error":"hosted_origin_required"}` HTTP403; adding https://astrid.haus Origin to wrong `/v1/health` path returned `{"error":"route_not_allowed"}` HTTP404. Expected health body. Source `r/runtime_protocol/door.py:597,328-345,534`: use exact hosted Origin and `/api/runtime/v1/health`. All reported timing measurements use the corrected route.

Command `ps ... thcount ...` returned `ps: thcount: keyword not found`; `ps -M ... tid ...` likewise `ps: tid: keyword not found`. macOS ps interface, no Astrid source location. Workaround `ps -M -p 5671,5735` and five-second sample thread observations. Steady after snapshot shows7 Runtime and3 host threads; before sample includes transient HTTP threads from measurements.

## Optional diagnostic object read

Command `python3 render/check_registry.py`: `urllib.error.HTTPError: HTTP Error 404: Not Found`. Expected direct object access via registry_hash from authority, but that derived hash was not available through the object route. No claim based on this failed read. Workaround: use the verified worker error, pinned task spec, installed projection/materializer source, and existing registry report evidence. Direct run door routes also returned404; supported CLI `runs show ... --evidence` succeeded and its file is retained. These were exploratory helper reads, not product render failures.
