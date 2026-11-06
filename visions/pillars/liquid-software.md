# Principle 2 — Agent-Powered Liquid Software

**Claim:** Software should be shaped by the creative process, not force creative work into a fixed application. People and AI agents should be able to assemble, manipulate, extend and reuse coherent tools as their needs change.

This adaptability exists in service of [artistic ambition](../artistic-ambition/principle.md): it should help people attempt more demanding, original work rather than merely rearrange interfaces.

## What this means

- **Opinionated components.** A player, inspector, timeline, gallery, transcript editor, graph or 3D viewer works well by default, adapts to its container and declares meaningful extension points. A video editor is a useful default *composition* of those components, not a mandatory rigid layout.
- **Physical composition.** Components can resize, float, dock, snap, nest, move in depth and expand. Conventional 2D interfaces remain first-class; a 3D/immersive workspace is a more expressive presentation of the same workspace model, not an excuse to make every control a 3D mesh.
- **Functional composition.** A component can bind to shared typed resources and capabilities. Spatial placement/attachment is distinct from semantic binding (for example, a beat lane sharing the timeline's clock). Users and agents should be able to inspect and change both.
- **Frontend and backend together.** Agent packs contribute skills/actions, renderers and UI. Human interactions and agent actions operate on the same authoritative project and validated domain operations, rather than maintaining duplicate semantics or data.
- **Extensions can extend extensions.** Component authors decide how their components should be extended—timeline lanes, inspector sections, scene controls, graph renderers—through common contribution machinery with specialized contracts. Compose what's available before generating new code.
- **Continuous adaptation with control.** A user asks for music-aware editing; an agent discovers beat analysis, brings a lane and mixer forward, proposes edits, and the person manipulates or rearranges those views. Changes are understandable, reversible and permissioned.

## Experience to preserve

Think **Minority Report-like creative manipulation** alongside a working, ordinary editor: background tasks and results can come into view; interface objects can be pulled together and rearranged; an agent can work in the same environment. Rendering is suspended when appropriate, without cancelling background jobs or losing durable state.

## Boundaries

Keep project state, workspace layout, interaction state and task execution distinct. Don't rebuild Runtime, turn every UI fragment into a standalone app, abandon the existing extension families, or treat Three.js as the underlying data model. Untrusted agent-created functionality must be previewed, validated and activated safely.

## Read next

- [LS-001 — Portable components](gaps/LS-001-portable-components.md)
- [LS-002 — Agent workspace control](gaps/LS-002-agent-workspace-control.md)
- [LS-003 — Full-stack contributions](gaps/LS-003-full-stack-contributions.md)
- [Component and extension examples](references/components.md)
- [Source-backed App/Agent/Runtime map](references/source-map.md)
- [Preserved originating philosophy](references/original-philosophy.md)

This is one [Astrid vision principle](../../vision.md), **not the whole vision** and not an approved implementation plan.
