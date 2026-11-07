# Pillar 2 — Agent-Powered Liquid Software

**Tools should adapt to creative work as people and agents create, not force the work into fixed interfaces.**

Astrid is a shared foundation for open, composable creative tools. Its foundation should stay small, understandable and dependable: durable resources (timelines, media and projects), validated capabilities for changing them, and interfaces for people and agents to use the same underlying work. Specialized behavior belongs in packs and reusable components. Extend core only when a genuinely shared capability requires it.

An excellent tool is an **opinionated composition**, not a generic blank canvas. A creator can use it as-is or arrange, connect, adapt and extend its components while working. Every extension should expose useful extension points of its own: a timeline can support custom lanes, an inspector new sections, and a workspace new views. Packs can provide both agent actions and human-facing interfaces, sharing authoritative resource identities and permission checks.

**Composition has two distinct concerns:** where a component is placed (dock, float, nest, spatially arrange) and what it is bound to (timeline, selection, playback, media, task). Moving a view should not silently change the creator's data or lose its state. Both conventional 2D workspaces and spatial/3D experiences can use the same primitives; neither should be required for the other.

Build on existing components before inventing new architecture. Let creators choose their degree of customization and where tools run. The result should be a responsive creative environment whose capabilities grow through contributions—not a new framework for its own sake.

**Gaps:** [LS-001 — Portable components](../gaps/LS-001-portable-components.md) · [LS-002 — Agent workspace control](../gaps/LS-002-agent-workspace-control.md) · [LS-003 — Full-stack contributions](../gaps/LS-003-full-stack-contributions.md).

**Implementation exploration:** [Liquid workspace](../../plans/24-liquid-workspace/plan.md) · [Component design input](../../plans/24-liquid-workspace/components.md) · [Pack lifecycle](../../plans/06-packs/plan.md). These are proposals and projects, not proof that the capabilities already ship.
