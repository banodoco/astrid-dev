# Component and extension reference

**Purpose:** Preserve concrete examples and the proposed design vocabulary for the [Liquid Software vision](../principle.md). **Not an API specification:** “Existing” paths are source anchors, whereas “Desired” behaviors are proposed. Verify source again before implementation.

## Objects and their roles

| Level | Examples | Responsibility |
| --- | --- | --- |
| Resource | Timeline, clip, media asset, transcript, generation, scene | Durable meaning and identity; reads/mutations through Runtime-backed domain contracts |
| Capability | Timeline edit/seek; music beats/align; generation/render | Validated operations, typed inputs/results and agent/tool discovery |
| Component definition | Timeline viewer, player, inspector, gallery, graph, 3D viewer | Reusable interactive presentation, required capabilities, adaptation rules and extension points |
| Component instance | Player A bound to timeline X, player B bound to timeline Y | Stable instance identity, scoped bindings and local view state |
| Contribution | Temporal lane, inspector section, overlay, action, custom renderer | Opinionated extension hosted by a specific component contract |
| Tool/workspace | Default video editor, music-editing environment | An opinionated composition of components, relationships, bindings and defaults |
| Pack | Timeline, Music, Rendering, custom creator pack | Distributes discoverable actions, skills, UI and processing across host boundaries |

A **component is not required to be a 3D mesh**, and not every nested control must be promotable to a standalone component. A contribution may optionally expose a portable surface if that makes semantic sense.

## Existing components to build on

| Existing surface | Source anchor (App unless noted) | Useful seam | Missing generalization |
| --- | --- | --- | --- |
| Timeline | [TimelineEditor](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/TimelineEditor/TimelineEditor.tsx) and [TimelineEditorShellCore](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/TimelineEditorShellCore.tsx) | Existing edit gestures, timeline lanes, data/view state | A portable instance with container-aware layout and scoped bindings |
| Preview/player | [PreviewPanel](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/PreviewPanel/PreviewPanel.tsx) | Playback/preview against timeline data | Reusable player that does not assume one editor shell |
| Inspector | [PropertiesPanel](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx) | Selection-driven controls and inspector contributions | Independent bindable inspector and optional extractable subviews |
| Generation gallery | [GenerationsPane](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/features/gallery/components/GenerationsPane/GenerationsPane.tsx) | Second domain to validate a portable component | Component contract independent of existing pane placement |
| 3D scene viewer | [Agent rendering-pack Three.js extension](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/rendering/ui/threejs-live-editor/extension.tsx) | Live scene, World Explorer panel and clip renderer | A general-purpose spatial *workspace* is a separate proposed capability |
| Transcript | [Agent rendering-pack transcript UI](https://github.com/banodoco/astrid-agent/tree/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/rendering/ui/transcript) and [App transcript panel adapter](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/lib/transcript-panel-adapter.ts) | Same data can appear as panel and timeline-associated material | Generic binding and placement of transcript views |
| Agent activity | [TasksPane](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/features/tasks/components/TasksPane/TasksPane.tsx) | Agent conversations/tasks as existing UI | Task/result objects in a composable workspace |

The [custom two-pane editor](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/examples/CustomTwoPaneVideoEditorExample.tsx) is the first proof that existing production surfaces can be composed in more than one layout. It does **not** prove arbitrary docking or a universal component SDK.

## Proposed minimum component contract

Every component *definition* exposes stable identity/owner, supported resource bindings and capabilities, presentation/adaptation constraints, and **component-defined extension points**. The workspace owns placement, snapping, z-order/focus, mounting and layout persistence. A component *instance* has its own ID, resolved bindings and local UI state.

Contribution kinds remain first-class: the timeline can accept **temporal lanes**, the inspector **sections**, a graph **node renderers**, a scene viewer **gizmos**, etc. Common registration, validation, lifecycle and diagnostics do not imply that every kind may be placed everywhere.

### Three distinct user/agent operations

1. **Place:** position/resize/focus a view (purely spatial).
2. **Attach:** establish a layout constraint (dock, stack, nest, follow).
3. **Bind:** explicitly connect shared context or data (same timeline, selection, time axis, asset, output).

A binding is not inferred solely from visual proximity. A component can suggest compatible bindings with user approval. Store workspace arrangements separately from domain edits.

## Example: Music-editing composition

- **Backend:** existing [music.beats](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/music/docs/SKILL.md) plus timeline commit/edit primitives.
- **Typed result:** a source-time beat grid; transform explicitly into timeline coordinates where needed.
- **Views:** beat lane, BPM/mixer controls, preview and timeline; a workspace preset arranges them.
- **Shared behavior:** user and agent can propose/adjust cuts, inspect preview, and commit through the authoritative timeline edit flow.
- **Proof:** move the beat view from a nested timeline lane to a separate docked view, retaining correct binding/state; save and restore the arrangement.

This is a **proposed end-to-end acceptance example**, not evidence that all the UI or integration currently exists.

## Questions for implementation

- Which existing surfaces can move without remounting (particularly players, WebGL and editors with internal gestures)?
- Which selection/playback contexts are shared, pinned or independent when multiple instances are open?
- Which contribution types are meaningful standalone, and which must stay host-specific?
- How can an extension announce a new component and its opinionated extension points without altering the main editor shell?
- How should compact/minimum sizes and 2D/3D presentation be negotiated without forcing every view to implement XR?
