# Plan 27 — task index (draft)

[Plan](plan.md) · [Inputs](inputs.md) · [Catalog status](../index.md)

These are **proposed, not dispatched** tasks. Routes (N/X/S), estimates, owners, exact source revisions at execution and test selectors must be assigned under the [shared run contract](../../skills/astrid-dev-shared/run-contract.md) when implementation is authorized.

| ID / outcome | Depends on | Route | Progress | Focused evidence |
|---|---|---|---|---|
| R27-01 — Audit existing render/export routes and UI | None | TBD | Draft | Revision-pinned map of existing render UI, `VideoEditorExportRequest`, local/client/worker paths, output-format hooks and source/output/variant selection; implemented vs reserved capabilities |
| R27-02 — Define usable presets and advanced option matrix | R27-01 | TBD | Draft | Reviewed presets for format/container/codec, resolution/aspect/orientation, FPS, bitrate/quality and inclusion policy; unsupported combinations and clear defaults |
| R27-03 — Wire choices to real output | R27-02 | TBD | Draft | Chosen settings/selected tracks and timeline range propagate to the actual executor, with capability validation and no silent fallback |
| R27-04 — Deliver understandable rendering UI and state | R27-02, R27-03 | TBD | Draft | Simple default + advanced controls; clear progress, cancel/retry, error states, persistence, completion and download |
| R27-05 — Prove rendered-file correctness | R27-03, R27-04 | TBD | Draft | Real playable exports with metadata probes and audiovisual checks for representative formats/sizes/FPS, source/output inclusion, audio and negative cases; F-003/F-002 assessment |

The goal is **complete control over the rendered output**, not adding a second render engine or a cloud-running route. Coordinate with [Plan 18](../18-timeline-editing/plan.md), [Plan 25](../25-cloud-assist-v1/plan.md) and the currently implemented output format contracts to avoid duplicate work.
