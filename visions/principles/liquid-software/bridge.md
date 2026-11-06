# Bridge — Liquid Software, from current Astrid to the vision

**Purpose:** Connect [the principle](principle.md) to existing implementation and the [Astrid Dev plans](../../../plans/). This is a design map, **not a replacement plan, task authorization or claim that the destination already ships**. Revalidate referenced source revisions when scoping work.

| Desired behavior | Current foundation | Missing/generalization to prove | Existing plan relationship |
| --- | --- | --- | --- |
| Rearrange meaningful components | App preview, timeline, inspector and [alternate two-pane shell](references/source-map.md) | Portable component instances, container adaptation, declarative dock/float/nest layout, preserved state | [Plan 18](../../../plans/18-timeline-editing/plan.md) overlaps timeline primitives; neutral workspace host is **not yet scoped** |
| Components define own extensibility | App `panel`, `inspectorSection`, `timelineOverlay`, `dataKind` registries | A common extension-host protocol accepting specialized points beyond video-editor slots | [Plan 18](../../../plans/18-timeline-editing/plan.md), [Plan 06](../../../plans/06-packs/plan.md) |
| Frontend/backend capability composition | Agent packs with `actions`, `ui`, `rendering` and skills; Runtime data authority | Shared semantic resource/binding identity and inspectable UI↔action relationships; no parallel registry | [Plan 06](../../../plans/06-packs/plan.md), [Plan 17](../../../plans/17-vibecomfy-extensibility/plan.md) |
| Shared human-agent edits | App timeline patch/proposal flow; Agent timeline commit SDK | Prove consistent domain semantics, conflict handling and no silent overwrites | [Plan 04](../../../plans/04-concurrent-edits/plan.md) |
| Agent changes the workspace | Agent tool discovery and App UI contribution services | Workspace `open/place/attach/bind/focus/save` operations usable by both direct manipulation and agents | **New scope to propose**; do not assume a generic workspace SDK exists |
| Safe just-in-time extensions | Trusted bundled UI extension host and pack build/install ambitions | Reproducible preview, activation, versioning, isolation/permissions and rollback | [Plan 06](../../../plans/06-packs/plan.md), [Plan 15](../../../plans/15-openshell-safe-execution/plan.md) (different security boundaries) |
| Spatial interaction | Existing Three.js scene/World Explorer extension | 2D-first workspace geometry, spatial renderer and semantic snapping/binding | [Plan 11](../../../plans/11-threejs-pack/plan.md) is **feature extraction**, not a spatial workspace plan |

## Smallest decisive product proof

Take **real** player, inspector and timeline components and support reversible 2D arrangements without disrupting editor behavior. Then add the existing music-beat analysis as a typed result consumed by a beat lane/mixer in a music-editing composition. User and agent can rearrange the views, share the right timeline/clock, propose and commit edits and restore the layout. After that, test a truly different domain component (generation gallery).

A pass demonstrates reusable component contracts **and** an existing backend pack acting on shared resources. It does not imply arbitrary generated code, immersive 3D, or the complete product vision is solved.

## To turn this into executable work

Identify exactly which existing plans own each deliverable; do not create overlapping tasks or move plan priorities here. A missing cross-cutting **workspace host** or **shared binding contract** needs separate scoped design/plan work under repository rules. Freeze actual source revisions, reuse existing implementations and define narrow acceptance checks before implementation.
