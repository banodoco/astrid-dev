# Source map — Liquid Software

**Purpose:** Source-backed technical reference for the [vision](../vision.md), not a second roadmap. Links below point to specific source revisions captured on **2026-11-06**. They establish the **observed design/code contracts**, not that the full Liquid Software behavior ships or that every referenced test currently passes.

## Captured source identities

| Repository | Ref reviewed | Commit |
| --- | --- | --- |
| [Astrid App](https://github.com/banodoco/astrid-app) | `main` / `pre-main` | [`57d39bd`](https://github.com/banodoco/astrid-app/tree/57d39bd68973dc081ade464e66bef207434436f4) |
| [Astrid Agent](https://github.com/banodoco/astrid-agent) | `main` | [`9f42441`](https://github.com/banodoco/astrid-agent/tree/9f42441231836ab461853951710f6a99860c55f9) |
| [Astrid Runtime](https://github.com/banodoco/astrid-runtime) | `main` / `pre-main` | [`9fc53b7`](https://github.com/banodoco/astrid-runtime/tree/9fc53b771134940aaac901e4cfc5d03c1db1a20a) |
| [Astrid Dev](https://github.com/banodoco/astrid-dev) | `main` | [`17ec8fc`](https://github.com/banodoco/astrid-dev/tree/17ec8fce08a34e828f53b4cd7bd1aab5758346e6) |

Agent `main` was one documentation commit ahead of Agent `pre-main` at inspection; implementation plans must freeze their own actual base/donor identities. No product code was executed or tested for this reference capture.

## Foundations with concrete evidence

| Subject | Source | What it shows | What it does **not** establish |
| --- | --- | --- | --- |
| Product-neutral data authority | [Runtime README](https://github.com/banodoco/astrid-runtime/blob/9fc53b771134940aaac901e4cfc5d03c1db1a20a/README.md) and [App Runtime vision](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/creative-workspace-runtime-vision.md) | Runtime owns workspace/task/artifact state and client protocol | Universal resource binding schema or spatial workspaces |
| Separate editor panels, reused in another layout | [CustomTwoPaneVideoEditorExample](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/examples/CustomTwoPaneVideoEditorExample.tsx) | Preview/timeline/properties can be composed through one provider | Arbitrary draggable, serializable layout |
| Editor shell assumptions | [TimelineEditorShellCore](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/TimelineEditorShellCore.tsx), [divider drag](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/components/useTimelineShellDividerDrag.ts) | Layout, gestures and host coupling that need careful extraction | Generic workspace geometry protocol |
| Editor extension contract | [SDK manifest](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/sdk/manifest.ts), [extension author contract](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/video-editor/extension-author-contract.md) | Panels, slots, inspector sections, overlays, commands, lifecycle | Arbitrary component-defined extension families today |
| Typed timeline data | [dataKind SDK](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/sdk/video/families/dataKind.ts), [data envelope](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/tools/video-editor/data/typed/envelope.ts) | Typed lanes, schemaRefs, temporal domains | General semantic type compatibility across all packs |
| Renderer-independent timeline observation | [TimelineViewStore](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/sdk/video/timeline/viewState.ts) | Playhead/selection/geometry subscriptions without tying reader to a particular renderer | A global multi-workspace view/context model |
| App/agent timeline edit integrity | [App provider compatibility](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/video-editor/provider-compatibility-matrix.md), [Agent SDK](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/sdk/timeline/api.py) | Versioned updates, proposals, commits and conflict handling have concrete implementations | Their higher-level operation APIs are currently identical |
| Pack structure | [Pack authoring guide](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/docs/packs/creating-packs.md) | Pack manifests can declare actions, skills, UI and rendering contributions | Unified live UI/backend activation and discovery |
| Music example | [Music pack](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/music/pack.yaml), [skill](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/music/docs/SKILL.md) | `music.beats`, `music.align`, `music.level`, `music.duck` and usage guidance | A complete music-editing UI exists today |
| Three.js as current creative extension | [Three.js Live Editor](https://github.com/banodoco/astrid-agent/blob/9f42441231836ab461853951710f6a99860c55f9/astrid/packs/rendering/ui/threejs-live-editor/extension.tsx) | Live scene clip, panel and authoring entry | A universal 3D desktop/workspace |
| Live updates | [App realtime system](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/structure_detail/realtime_system.md), [RuntimeDataProvider](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/src/integrations/runtime/dataProvider.ts) | General UI refresh polling and no public timeline document event cursor in this provider | General push/subscription semantics |
| Trust limits | [Extension trust posture](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/extensions/trust-and-security.md), [Tool authoring](https://github.com/banodoco/astrid-app/blob/57d39bd68973dc081ade464e66bef207434436f4/docs/video-editor/tool-authoring.md) | Trusted statically bundled browser extensions; current general Tool boundary is specific to the video editor | Safe immediate execution of arbitrary generated UI code |

## Existing direction and implementation plans

- [Extensibility philosophy](../../../docs/extensibility-philosophy.md): small dependable foundations; every extension can be extended; people choose their level of control.
- [Plan 06 — Packs v1.3](../../../plans/06-packs/plan.md): loading, trust, distribution and integration; queued separately.
- [Plan 18 — Extensible timeline editing](../../../plans/18-timeline-editing/plan.md): candidate independent timeline editing/views; draft.
- [Plan 11 — Three.js as a pack](../../../plans/11-threejs-pack/plan.md): refactor current feature ownership, **not** a general 3D workspace plan.
- [Plan 04 — Concurrent editing](../../../plans/04-concurrent-edits/plan.md): human/agent edit safety.
- [Plan 15 — OpenShell](../../../plans/15-openshell-safe-execution/plan.md): full-stack sandboxing investigation, not automatic browser extension isolation.
- [Plan 17 — VibeComfy extensibility](../../../plans/17-vibecomfy-extensibility/plan.md): another test of reusable specialized tools.

These plans retain their own scope, status, authorization and implementation evidence. This vision neither replaces nor starts them.

## Major missing seams to investigate (proposals, not established defects)

1. **Portable component host:** definition versus instance, stable bindings, container-based adaptation and layout persistence.
2. **Component-owned extension points:** generic registration/lifecycle, specialized semantics, nested/extractable contributions when explicitly supported.
3. **Semantic resource/binding vocabulary:** versioned type identity and coordinate mappings between typed resources and backend action results.
4. **Agent-controlled workspace operations:** place/attach/bind/open/focus/save and reversible proposals, distinct from project edits.
5. **Live activation:** trusted component discovery, install/build/preview/activation/rollback; untrusted code isolation and enforced capabilities before exposing arbitrary code.
6. **Realtime coordination:** useful durable events without broadcasting every pointer move, render frame or playhead tick through Runtime.
7. **Spatial rendering:** 2D-first workspace schema, future 2.5D/3D renderer and interaction semantics; do not couple domain models to Three.js.

## Proof strategy

First: reuse real video editor components under a declarative 2D layout with reliable state retention. Second: let existing music actions expose typed beat data and a pack-provided UI that binds to the same timeline. Third: use a non-video component (generation gallery or graph) to challenge the generality. Only then widen the spatial renderer and arbitrary agent-authored extension path. All product work should be scoped through the existing plan/workflow rules, with fresh current-source verification and focused tests.
