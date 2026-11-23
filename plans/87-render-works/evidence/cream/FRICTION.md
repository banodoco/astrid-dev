# Astrid tooling friction

## Asset listing rejects JSON
- Command: `./astrid-stack.sh timelines assets 77f906f3242c48179ab86ca7c3e62eb4 --project 801a01b3a87941a1ab25958c488afdbf --json`
- Error (verbatim): `astrid timelines: error: unrecognized arguments: --json`
- Expected: machine-readable asset listing, consistent with other product commands.
- Source: timeline CLI `assets` argument parser in `astrid/packs/timeline/cli.py`.
- Workaround: use the human-readable asset listing or SDK inspection.
# Asset fetch friction

## SDK launcher attempted to bootstrap a generic pack host

Exact command (run from the work folder):

```sh
./edits/stackpy.sh cream/fetch.py cream/src R5-TOUR-T1-TYPING=sha256:de268f0ed19ae66899ee6c23fbe05a9c7a281822b95f67c4c0d4b52c97e6a78d R5-TOUR-T2-THREEJS-LANDS-NT=sha256:81d927be23a941d7624026b37223979e5526ec2be41e297eac63d4480292232d R5-TOUR-RAW-THREEJS=sha256:f6829f7778fb9fdcda9159635a0444b81a6769e9518d326607fbd403e77c0ed2 R5-TOUR-T3-KEYFRAMES-NT=sha256:83a029745279474c20740580e3018ad8fa1253147bf63228b78a183bc56db4ef R5-TOUR-T3-EQUAL-4=sha256:787379acea43aaef88d20066771cf149eb58095862a8c1668a41986f93664bef R5-TOUR-RAW-H3=sha256:9afbe1674750162fbf47587790728fc5526f26e6845744bda3e99f07573e12ef R5-TOUR-T4-FINAL-LANDS-NT=sha256:78f3f113abb19a2457ef1f7c329ad0c13683286a111746c4e66e1a8f5cc7a95c
```

Verbatim launcher failure:

```text
astrid_runtime_client.generated.ApiError: transport_timeout: runtime request timed out
astrid.sdk.host_bootstrap.PackHostBootstrapError: generic Astrid pack host could not verify runtime identity; run the Astrid install line again
astrid.sdk.autobootstrap.AutoBootstrapError: generic Astrid pack host could not verify runtime identity; run the Astrid install line again
astrid.sdk.exceptions.ServiceUnavailableError: generic Astrid pack host could not verify runtime identity; run the Astrid install line again
```

Expected: read managed media bytes from the healthy Runtime. Source: `astrid/sdk/host_bootstrap.py` and `astrid/sdk/autobootstrap.py`. Workaround: call `AstridClient.open_from_launcher(start_pack_host=False)` in `cream/fetch.py`, avoiding generic pack-host startup; the same seven object reads succeeded. No runtime or timeline state was changed.

## Detached publication rejects new imported registry aliases
- Command: `edits/stackpy.sh -m astrid.packs.rendering.docs.scripts.timeline_document publish --file cream/edit.json --idempotency-key r6-cream-ui-20261122`
- Error (verbatim): `astrid.sdk.timeline._command_state.CommandError: patch references media outside Runtime-verified inputs`
- Expected: publish the checked seven clip asset swaps and five new registry entries, after importing the five media objects with generation/variant and resolution.
- Source: `astrid/packs/rendering/docs/scripts/timeline_document.py:38` (`resolve_media_rebinds` only verifies same-alias replacements); `astrid/sdk/timeline/_doc_patch.py:356` rejects unverified new media.
- Workaround: under investigation; imports succeeded, but no timeline publication receipt was produced.

## Editor preview pack did not load
- Command: `node cream/verify/capture-stills.cjs` (Playwright, editor at `http://localhost:2400`; PlayerRef seeks at the six requested frames).
- Error (verbatim): `Preview pack could not be loaded. Preview pack loading timed out. Check the local connection and inspect/admit the project pack, then reload the editor.`
- Expected: UI recording clips visible at the requested frames in the real editor.
- Source: `editor/src/tools/video-editor/runtime/admitted-elements.ts:88`; displayed in `editor/src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx:733-737`.
- Workaround attempted: fresh editor load; the alert cleared, but the baseline stills remained black. The retry page offered no Retry preview control. Stack not restarted. No successful post-swap verification is possible until the pack loads and publication succeeds.
