# Astrid preview pack timeout and playback stutter

**Target:** project `801a01b3a87941a1ab25958c488afdbf`, timeline `77f906f3242c48179ab86ca7c3e62eb4`  
**Stack:** release-14 at `~/astrid-release/release-14-plan-69`  
**Measurement time:** 2026-11-22, about 17:15 CET for curl samples; about 17:25 CET for the headless playback samples.

## 1. Pack loading path

`VideoEditorProvider.tsx` builds `packRefsKey` from external element refs in the rendered preview composition. Its effect calls `setAdmittedElementScope(projectId, refs)` and `refreshAdmittedElements()` when either the project ID or that refs key changes.

The loader makes these same-origin requests from the editor at `http://localhost:2400`:

1. `GET /api/runtime/packs/project-elements?project=<project-id>` to list the project's current admitted refs.
2. For each requested ref not already cached by compiled digest, `GET /api/runtime/packs/project-elements/<project-id>/<compiled-sha256>.js` to fetch the compiled ES module. The editor verifies the bytes against the SHA-256 before importing them from a blob URL.

In this local dev stack, the browser reaches port **2400**; Vite's local proxy uses dynamic proxy port **17500**, which forwards to the Runtime door at **127.0.0.1:17501**. The curl response header identified the serving endpoint as `AstridRuntime`.

`ADMITTED_ELEMENT_LOAD_TIMEOUT_MS` aliases `ASTRID_BRIDGE_REQUEST_TIMEOUT_MS`, which is **30,000 ms**. One deadline starts before the list request and covers both that request and all bundle imports; it is not 30 seconds per request. There is no automatic retry. A new scope refresh or the **Retry preview** button (in `RemotionPreview.tsx`) starts another attempt. Existing imported modules are reused by digest.

The provider refreshes when the project's set of external element refs changes, including when a clip's pinned element revision changes. A timeline revision that leaves that set unchanged does not trigger a refresh. A project-pack document/admission revision alone does not trigger a refresh. The preview `Player` is keyed by project, timeline, and preview source in `useVideoEditorPreviewSurface.tsx`, not by timeline revision; the same Player receives revised props rather than remounting for every revision.

The suffix `Element ar-discord@sha256:... requires its exact admitted pack revision. Embedded source is preserved for migration and is not executed.` is **generic placeholder text**, not proof of a mismatch. `elementUnavailableDetail()` appends it whenever an element is unavailable; it appends the readiness error before it when loading failed.

## 2. Runtime, pack, and log evidence

### Timed requests

All five samples below went through `127.0.0.1:2400`. Each sample fetched the Runtime list once and then fetched all three listed bundles concurrently. All responses were HTTP 200.

| Sample | Element list | ar-discord bundle | ar-footage bundle | ar-type-sweep bundle |
|---|---:|---:|---:|---:|
| 1 | 1.534 s | 0.376 s | 0.431 s | 0.446 s |
| 2 | 0.178 s | 0.327 s | 0.369 s | 0.372 s |
| 3 | 0.371 s | 1.450 s | 1.447 s | 1.440 s |
| 4 | 0.353 s | 0.217 s | 1.532 s | 0.216 s |
| 5 | 0.524 s | 0.069 s | 0.065 s | 0.062 s |

An extra initial list probe took **3.020 s**. The requested five-round samples therefore span 0.178–1.534 s for the list and 0.062–1.532 s for bundle fetches, versus a shared 30 s browser deadline. Latencies were variable, but no pack request approached the deadline in these samples.

### Admitted refs now

The Runtime list returned `legacy: []`, selection digest `7579d2af…`, and all three refs with `status: admitted`:

| Element | Pinned revision | Compiled bundle digest |
|---|---|---|
| ar-discord | `sha256:994f28d18986c32550156c97a27709f0026306cc3bafeb94d8bfcc54ae774c07` | `f4b9946e8ca8b95e009c20b7e91d9e1da863348c9fb9e3ca59e5c766c97f5fcf` |
| ar-footage | `sha256:51b4150c586bdd3822b99684c82ccfbc049913fb8105c0a3a9ef935ccf3c138c` | `25f684bcfd26d0cd6c164802bdc0e635d3e0bc914b949d3411b0915f92fb35c8` |
| ar-type-sweep | `sha256:ce218423655842c13a57329556011431ec4cf961c718fc5910deca296758e895` | `eb0a428b8fee683fcb1bc2f3a38aa3e63cf18dbba949b4232d8b43548ee967b1` |

The read-only `project-pack inspect` command reported document version **3** and listed the same admitted revisions and compiled digests. It also reported `status: source-missing` for its current authoring-source lookup, while the live Runtime element list identified the pack as admitted and served each compiled bundle successfully. That source lookup discrepancy does not mean the pinned compiled revisions are absent from the Runtime.

### Logs and compile path

- `logs/editor-20261122-142917.log` contains only the startup banner and had a modification time of **14:29:46 CET**. It has no records from 17:05–17:15.
- Runtime `runtime.log` also had a **14:29:41 CET** modification time and records startup/discovery information, not per-request timings.
- `service-pack-host.log` had a **17:27:26 CET** modification time and contained **487** `transport_timeout: runtime request timed out` messages by inspection. Its messages have no timestamps, so I cannot assign them specifically to 17:05–17:15. The file does show recurring Runtime transport timeouts generally.
- No Vite/esbuild compile error was found in the inspected editor or pack-host logs. Project element compilation happens at pack admission; preview fetches serve the already-compiled module bytes. The browser also fetched all three compiled modules with HTTP 200. This evidence does not support Vite/esbuild compilation as the current preview bottleneck.
- The headless browser did see one unrelated `503` for `/__astrid/local-update-status`; no project-element list or bundle request failed.

## 3. Playback measurement

I used a single headless page at a time, then closed it. The editor's `frameupdate` listener forwards `event.detail.frame / fps` to `data-current-time`, so the displayed time below tracks Player frame updates. The timeline was 30 fps. RAF deltas are browser animation-frame intervals; the frame counts are derived from the Player's reported time.

| Start point and clip type | Wall time | RAF callbacks | RAF gaps >33 / >50 / >100 ms | RAF p95 / max | Player frame advance | Expected at 30 fps | `data-preview-revision` changes |
|---|---:|---:|---:|---:|---:|---:|---:|
| 30.77 s, inside 28.7–42.3 s time-lapse (99 short still clips) | 10.201 s | 563 | 7 / 6 / 4 | 17.4 / 216.7 ms | 923 → 926 (**3 frames**) | ~306 | 0 |
| 105.77 s, inside 102–145 s demo (video clips) | 10.009 s | 593 | 2 / 2 / 0 | 17.5 / 83.4 ms | 3173 → 3174 (**1 frame**) | ~300 | 0 |

The attribute held `authoring-parent-revision-177b640492e51c414b867feb2006ccd8e598208ab69e5bde11aac1c565940d06` throughout both intervals. Thus these runs show no revision churn or player reload while playing. Both segments advanced far less than real time; the first stayed around 30.8 s and the second around 105.8 s. The compact headless capture is evidence of severe preview playback stalling in this environment, but it is not a controlled comparison against the owner's interactive Chrome.

## 4. Conclusions and actions

### Most likely causes

- **Pack timeout — inferred, not reproduced in the five samples.** The pinned refs are present and the exact ar-discord revision is admitted. The text about requiring an exact revision is generic placeholder copy. The current list and bundle requests are successful but show latency variation; the Runtime pack-host log has many transport timeouts, and the reported stack was CPU-busy while two agents were publishing and capturing against it. That makes transient Runtime scheduling/contention the leading explanation for an earlier 30 s timeout. There is no evidence that Vite is compiling the project pack on preview load. Because those historical logs are not timestamped, the precise cause and time remain unverified.
- **Playback stutter — verified symptom; cause inferred.** The Player advanced only 1–3 frames in roughly 10 seconds in both the still-heavy time-lapse and the video demo, while the outer browser RAF loop mostly ran at 55–59 Hz. No preview revision changed. That rules against a revision-triggered Player remount as the explanation for these captures. The 99 short clips are extra work in the first segment, while the second segment's similar stall points to a broader Player/render scheduling or machine-contention problem too. The headless environment and the reported concurrent agent work are contributing factors that need an owner-Chrome comparison before assigning a single root cause.

### Owner action now

Let the two agents finish their publishing/capture work, then use **Retry preview** once. If it remains stuck, reload the editor after the stack load settles. Do not re-admit solely to fix this timeout: the Runtime currently has the exact three refs and serves their compiled bundles. Re-admission would not resolve a transient Runtime response delay.

### Product changes

1. Raise the combined preview admission deadline from **30 s to 60 s** for local Runtime contention, and record list versus bundle/import phase timing so a longer deadline does not hide which stage is slow.
2. Keep the Retry preview action accessible beside the failed clip placeholder as well as in preview chrome. It exists today, but the clip's main copy does not explain that retry can recover a transient timeout.
3. Split the message into precise cases: Runtime list/bundle timeout, missing exact admitted ref, and legacy/source migration state. Do not append the exact-revision warning to every load failure.
4. Preserve the current no-remount behavior for ordinary timeline revisions. The Player key already excludes revision IDs; the measured attribute did not change. Add observability around actual Player remounts/frame progress before making revision updates reload the Player.

## Evidence files

- Editor code: `editor/src/tools/video-editor/runtime/admitted-elements.ts`, `runtime/admittedElementLoader.ts`, `contexts/VideoEditorProvider.tsx`, `compositions/TimelineRenderer.tsx`, `components/PreviewPanel/RemotionPreview.tsx`, and `components/PreviewPanel/useVideoEditorPreviewSurface.tsx` in the release-14 checkout.
- Logs: the editor startup log, Runtime `runtime.log`, and `service-pack-host.log` under the release-14 stack above.
