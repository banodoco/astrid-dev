# Plan 27 — source inputs and open decisions

[Plan](plan.md) · [Tasks](tasks.md)

## Existing implementation to inspect

At the time of planning, the Astrid App `main` reference was [`ce7b3e7d841cddf7d401574bf00097d233c18f06`](https://github.com/banodoco/astrid-app/tree/ce7b3e7d841cddf7d401574bf00097d233c18f06). Revalidate the exact base and affected routes when work starts.

- [`VideoEditorExportRequest`](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/src/tools/video-editor/lib/browser-runtime.ts) already exposes optional codec, width, height and FPS fields. **Contract fields do not establish actual UI support or output fidelity.**
- [`useRenderState`](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/src/tools/video-editor/hooks/useRenderState.ts) coordinates export/render operations; [`useClientRender`](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/src/tools/video-editor/hooks/useClientRender.ts) contains a browser rendering route. Actual supported codecs/settings depend on the selected renderer and device.
- [Source vs Output tracks](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/docs/video-editor/source-output-tracks.md) document export inclusion intent. Verify enforcement on the relevant render path, including mixed audio/video.
- [Output format registry](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/src/tools/video-editor/runtime/outputFormatRegistry.ts) currently handles **compile-only** output formats; the [output-format family adapter](https://github.com/banodoco/astrid-app/blob/ce7b3e7d841cddf7d401574bf00097d233c18f06/src/tools/video-editor/runtime/families/outputFormatAdapter.ts) describes render-dependent execution as reserved. Don't confuse extension descriptors with a working video renderer.
- Coordinate with [Plan 18](../18-timeline-editing/plan.md) (editable timeline primitives), [Plan 25](../25-cloud-assist-v1/plan.md) (where rendering executes remotely), and [Plan 26](../26-fully-hosted-v2/plan.md) (hosted persistence and execution).

## Decisions before implementation

Audit current export UX, feature support per renderer, output audio, clip and video-variant selection, video dimensions/aspect ratio, quality controls, filename/download and long-running-job behaviour. Choose an initial supported format/device matrix and a small default set of presets. Confirm work owner, tests with actual export files, hardware/browser constraints and intended integration branch before assigning routes or spending resources.

No credentials, new cloud services or renderer replacement are authorized by this planning entry.
