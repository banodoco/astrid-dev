# Time-lapse fix tooling friction

## SDK preview diff fails after Runtime preview

- Command: `bash edits/stackpy.sh -u tlfix/probe_swap.py` (first version used `t.commit([cmd], ..., merge='atomic', dry_run=True)`).
- Verbatim error: `KeyError: '_runtime_document'`.
- Expected: return the successful registered-asset preview and its diff.
- Source: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/py/lib/python3.11/site-packages/astrid/sdk/timeline/commit_session.py:1003,1017` passes the non-execution `self.bundle` to the diff resolver; `emitter.py:185` constructs `Closure(before)`; `commit.py:308` requires `source_mapping['_runtime_document']`.
- Verified: exception occurs in SDK postprocessing after submit returns, and private outbox has no pending/flight. No publication was requested (`dry_run=True`).
- Workaround, verified successful on retry: use public SDK session `commit_many(..., base=t.head, merge='atomic', dry_run=True)` for this preview, retaining its raw Runtime receipt and canonical document. Real publication uses normal `Timeline.commit` with guarded asset-only changes and an atomic expected head.

## Runtime and editor reads time out during concurrent work

- Command: `bash edits/stackpy.sh -u tlfix/apply_fix.py --preview-only`.
- Verbatim error: `ServiceUnavailableError: neutral runtime connection was not ready: transport_timeout: runtime request timed out; run the Astrid install line again`.
- Expected: connect to the already-running isolated stack, then open the current timeline closure.
- Source: installed `astrid/sdk/autobootstrap.py:265,374,466`; `astrid/sdk/client.py:471,484`; `astrid/sdk/timeline/commit_session.py:1110`.
- Verified: this attempt failed during connection setup before asset commands were constructed or sent. Workaround: retry the read against the running stack; no install/restart performed.
- Editor command: `node tlfix/capture.cjs before`.
- Verbatim displayed error: `Preview pack could not be loaded. Preview pack loading timed out. Check the local connection and inspect/admit the project pack, then reload the editor.`
- Expected: admitted project elements and stills visible in the real editor.
- Failed request path: `/api/runtime/packs/project-elements?project=801a01b3a87941a1ab25958c488afdbf` (`ERR_ABORTED`); media reads also aborted.
- The first screenshot had a valid PlayerRef/frame/revision but displayed this error card and black picture. Primary visual inspection rejected it as verification evidence. Workaround in progress: read-only preview/page reload, require no error card plus decoded images before screenshot, crop to picture only.
- Exact editor source: `~/astrid-release/release-14-plan-69/editor/src/tools/video-editor/runtime/admitted-elements.ts:88,137` (timeout/report), `components/PreviewPanel/RemotionPreview.tsx:733` (visible error card).

## Preview remains blank after pack retry

- Read-only editor retry returned HTTP 200 for `/api/runtime/packs/project-elements` and several object reads, but the compositor at player frame 1269 had a visible image with `src=''`, `complete=false`, `naturalWidth=0`, and no canvas/background-image. The picture was blank; no `pageerror` was emitted in that probe. This is verified DOM evidence, not a verified root cause.
- Source of the still's empty URL has not been established. No project-pack or timeline source changed as a workaround.
- Supporting isolated-stack log: `home/Library/Logs/Astrid Runtime/service-pack-host.log` had 476 literal `generic host claim failed ... ApiError: transport_timeout: runtime request timed out` occurrences at the 17:20:54 CET snapshot. The stderr lines have no individual timestamps, so attribution to this exact task window is uncertain.
- Installed source: `astrid/core/execution/generic_host.py:14755,14908` retries transient failures with capped exponential backoff; `astrid_runtime_client/generated.py:687-688` maps TimeoutError to transport_timeout; `runtime_protocol/server.py:209` suppresses access logging.
- Workaround: close this task's redundant probes and make one serial editor retry while no SDK requests run. No restart, install repair, source patch or SQLite edit is authorized/performed. Saturation versus stalled transport is inferred/undetermined, not verified.

## Capture-helper errors corrected during primary review

- Command: `node tlfix/capture.cjs before` (earlier helper revisions).
- Verbatim observed failure: `Preview did not paint in 60000ms` with `imgCount=0`, `decodedImages=0` at the initial frame 0. Expected: seek the requested still frame 1269 first, then check its decoder. The initial gate was a helper error, not proof that the target still failed.
- Primary also found the helper selected `plan-data.json` but traversed `data.shots`; this plan uses `data.slots`, so it silently produced no per-slot targets. The after-output location also disagreed with the analyzer's expected `verify/after/evidence.json`.
- Fixed source sites: `tlfix/capture.cjs:97,110,127,166,209` (corrected version): plan traversal, targets, output folder, seek/paint gate and evidence location.
- Workaround/fix: consume the asserted 99-slot plan schema directly; capture only endpoint before, every intersecting slot after; seek then allow React to settle; require the expected registered PNG hash in a decoded image URL; keep before/after paths consistent. Screenshot-only CSS hides editor chrome while retaining the real composition pixels and exact picture crop. No authored editor state is changed.

## Screenshot wrapper visibility check after CSS isolation

- Command: `node tlfix/capture.cjs before > tlfix/capture-final-attempt.log 2>&1`.
- Verified: the requested frame 1269 decoded the expected registered PNG (`stage: frame1269 decoded 1`), then `locator.screenshot` timed out while repeating `element is not visible` (full call log retained).
- Source: `tlfix/capture.cjs:184` in that helper revision: screenshot-only CSS hid the outer preview wrapper while exposing the Remotion composition. Playwright requires the selected wrapper itself to be visible, so it refused the screenshot despite visible picture descendants.
- Expected: isolate the actual picture without editor buttons/counters, then capture it.
- Workaround: use `page.screenshot` with the exact inspected picture rectangle, retaining screenshot-only CSS to hide outside editor chrome. This changes only capture presentation; it does not change authored timeline state.

## Final resolution and evidence serialization

- Registered-asset and full49-change previews succeeded through the SDK session route; real publication and fresh readback succeeded at f04036cf… (receipt in RESULTS.md). Transport delays resolved sufficiently without a restart.
- Corrected screenshot capture succeeded after one read-only Retry preview. Primary image review, expected decoded PNG hash and exact frame checks accepted the baseline.
- Screenshot CSS was tightened to hide only outside the Remotion subtree, preserving all descendant visibility. A diagnostic first pass was preserved. The final corrected run was checked for complete 63-file hashes/mtimes and accepted revision before final analysis. A premature analysis of the still-present diagnostic manifest was explicitly rejected and rerun after capture completion.
- Final corrected captures yield all61 visible differences and exact endpoint equality; primary independently recomputed metrics and reviewed the contact sheet. Details in RESULTS.md and verify/primary-audit.json. No unresolved blocker remains; transport timeout cause remains undetermined.
