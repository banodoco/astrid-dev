# Liquid Software — composable, agent-native creative environments

**Status:** Working vision (not an implementation plan) · **Captured:** 2026-11-06

## Thesis

**Software should be a living creative environment that people and agents shape together while working.** Instead of being confined to rigid applications, people should be able to assemble, move, connect, extend and reuse opinionated tools. Agents should be able to discover those same tools, operate their underlying capabilities, and help adapt the environment itself.

This is **not a mandate for everything to become 3D**, nor for every component to become generic. It is a shared foundation for useful, specialized software that remains fluid in how it is composed and extended.

## How it works

### 1. One shared substrate, many ways of working

Runtime-owned, versioned resources (timelines, media, transcripts, generations, scenes, documents and their relationships) are independent of any single interface or agent. Typed capabilities provide the supported ways to inspect and change them. **The same validated domain operation** serves direct manipulation, commands, agent tools and spatial controls; proposals, permissions, undo and concurrent changes retain coherent semantics.

Keep project data, workspace arrangements, transient interaction and background task lifecycle distinct. Closing a panel must not cancel a render; rearranging a workspace must not edit a timeline.

### 2. Opinionated components are the building blocks

A component might be a timeline, player, inspector, gallery, graph, transcription editor, mixer or 3D viewer. Each has a meaningful default, accepts explicit resource/context bindings and describes its sizing, presentation and lifecycle needs. A *Tool* (such as the video editor) is an **opinionated composition** of components, bindings, extensions and a default layout—not a special-case monolith.

A component author decides how it should be extended: timeline lanes, overlays and temporal operations; inspector sections; graph node types; viewer controls, etc. **Common contribution machinery, specialized extension contracts.** A component or extension can itself expose further extension points. Generalize the mechanisms while preserving the opinions.

### 3. Composition is physical *and* functional

Users can resize, move, float, dock, snap, nest, stack, focus and maximize components; the same declarative workspace operations are available to agents. Components adapt to their *container*, from compact to expanded/fullscreen.

**Placement/attachment and binding are distinct.** Snapping a waveform beneath a timeline describes layout; binding it to the timeline's clock, selection or beat data describes behavior. Compatible semantic bindings can be suggested at a spatial gesture, but never silently created from proximity alone.

Start with a coherent 2D environment. Allow ordinary HTML/React surfaces alongside native 3D content, and later offer a spatial/immersive renderer over the **same workspace model**. Three.js is a rendering/interaction option, not the source of domain truth.

### 4. Packs extend the frontend and the agent together

Astrid packs provide discoverable actions, skills, renderers and UI contributions, building on existing domain primitives. A pack can contribute both the interface a person uses and the tools an agent invokes, with shared typed inputs/outputs, provenance and capability identity. They do not require a separate database or duplicate implementation of core editing rules.

Agents should **compose existing capabilities first**, then help create new extensions when something is genuinely missing. Newly generated code requires an explicit trusted preview, validation, activation and rollback path; composing an installed component should not require generating code.

### 5. An adaptive, spatial creative experience

Imagine a person talking to an agent while editing video. The agent discovers beat analysis, opens a music workspace, places a beat lane beneath the timeline, floats a mixer beside the player and proposes beat-aligned cuts. The user moves those objects, changes controls, inspects previews and approves edits. The components and agent tools operate on the same timeline and beat-grid data. Tasks and intermediate results may stay in the background until pulled into focus.

This is the **Minority Report-like direction**: spatially direct, conversational and continuously adaptable—but still precise, predictable and useful in an ordinary 2D editor.

## Design constraints

- **Opinionated by default; composable by design.** Keep excellent complete tools, not a blank canvas as the only entry point.
- **Extend the existing foundation.** Reuse Astrid App's extension machinery, Agent packs and the neutral Runtime. Avoid parallel state owners and competing registries.
- **One authority per durable fact.** Shared changes pass through validated domain operations with identity, versioning and recovery.
- **Agents and people share a vocabulary.** Discover, inspect, bind, place, propose, commit, undo and explain—with explicit scope and permission.
- **Resource efficiency and safety.** Hidden UI may suspend rendering; background work persists independently. Untrusted code must not inherit unrestricted browser or host privileges.
- **Prove generality with real examples.** A second independently useful tool matters more than an abstract universal API.

## Proof, not prescription

A first meaningful proof is the **real video editor** with movable inspector, timeline and player, plus a **music-editing pack** that surfaces a beat lane/mixer and backend beat-analysis/edit operations. Human and agent can arrange, bind, save and resume this workspace without losing state or overwriting each other's edits. Next prove a component from another domain (e.g., the generation gallery) fits the same contracts.

This is a product/architecture north star, **not an approved roadmap or proof that its capabilities already ship**. See the [component reference](references/components.md), [source map](references/source-map.md) and [preserved originating philosophy](references/original-philosophy.md). Implementation scope, ownership, priorities and evidence stay in [Astrid Dev plans](../../plans/).
