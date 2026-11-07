# 27 — Complete video rendering and export options

**Start here:** read [AGENTS.md](../../AGENTS.md), follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), then review [tasks](tasks.md) and [inputs](inputs.md). Status, owner, priority and estimate belong only in the [plan catalog](../index.md).

**Vision gaps:** [F-003 — Dependable end-to-end creative execution](../../visions/gaps/F-003-creative-execution.md) (primary); [F-002 — Trustworthy user control](../../visions/gaps/F-002-safe-user-control.md) (supporting). This project would establish video-export capability within those broader gaps, not close either gap on its own.

## Goal and scope

Make finishing a video in Astrid straightforward: creators choose **what will appear in the final video** and **how the finished file will be rendered**, from sensible defaults to advanced controls. A selected export should actually produce the intended playable, downloadable video.

**Included (proposed):**
- Simple presets for common output formats/use cases, plus accessible advanced settings for **resolution and size**, width/height or aspect ratio/orientation, frame rate, **container and codec**, and relevant quality/bitrate choices where the active renderer supports them.
- An explicit choice of **which clips, tracks, video variants and timeline range** to include, with source-versus-output track semantics and a clear audio mix/inclusion policy. Avoid silently exporting reference/source footage or the wrong video variant.
- A coherent settings-to-render pipeline, for local and later remote implementations as applicable: supported capabilities, export progress, cancel/retry, validation, warnings, meaningful file names, final preview/download, and predictable settings persistence.
- A clear default export that works without teaching users codec details, with advanced controls exposed without overwhelming the standard workflow.

**Deferred:** implementing a new video renderer merely to offer settings; fully hosted execution or remote worker deployment (Plans [25](../25-cloud-assist-v1/plan.md) and [26](../26-fully-hosted-v2/plan.md)); unrelated timeline redesign (Plan [18](../18-timeline-editing/plan.md)); broad claims that every codec, device, browser or export combination is supported.

## What we build on

Astrid App already has an editor, render paths, source/output track semantics, an output-format/extension surface, and an export request interface that includes optional codec, width, height and frame-rate fields. **Do not rebuild those contracts without evidence that they are inadequate.** Inspect the current UI and real consumer routes to determine which options are user-facing and actually honoured; the presence of a TypeScript field or planner descriptor is not proof of a working export path. See [source inputs](inputs.md).

## Prerequisites and sequence

1. Audit the actual render/export UI, selectable media and tracks, local/worker/browser paths, existing presets and the supported output combinations; document what already works and where settings are lost.
2. Choose one end-to-end default and a bounded advanced option matrix; identify capability checks, validation and honest unsupported-case behaviour.
3. Connect selection and output settings through a single explicit export request to the renderer. Preserve track intent, selected clips/variants and output identity.
4. Test real rendered files at representative resolutions, formats, frame rates and media-selection cases, including audio and failure/cancel/retry; compare requested settings to output metadata and audiovisual contents.
5. Present progress, options and completed results clearly, and document supported formats and remaining gaps.

Details and acceptance evidence are indexed in [tasks.md](tasks.md). Start only after a scoped owner decision under the shared run contract.

## Completion

A creator can export a complete Astrid timeline using a simple default or selected supported advanced settings, pick the intended media/range, and receive a playable file whose size, frame rate, format, selected video and audio match the request. Evidence must include real export artifacts and metadata/playback checks, plus at least one negative/unsupported path. No claim about cloud deployment or universal format coverage is implied.

## Read next

- [tasks.md](tasks.md): draft work, dependencies and focused checks.
- [inputs.md](inputs.md): current source contracts and unverified capabilities.
