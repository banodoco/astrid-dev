# Original philosophy — Liquid Software

**Provenance:** Preserved text of the earlier user-directed “Liquid Software: A Philosophy for Composable, Agent-Native Applications” document, 2026-11-06. Retained as a source/reference, not a second canonical vision or an approved implementation spec. The distilled current entry is [../principle.md](../../pillars/liquid-software.md).

---

# Liquid Software: A Philosophy for Composable, Agent-Native Applications

## Vision

Software should be a **living, composable environment** that people and AI agents can shape together as they work.

Instead of rigid applications with predefined interfaces and capabilities, software should be assembled from reusable, opinionated components that can be arranged, extended, connected and adapted dynamically.

This applies equally to the **frontend experience** and the **backend capabilities** that power it. Both should operate on shared data, follow common protocols and be extensible through the same underlying architecture.

## 1. Shared Foundations

Everything builds on a common foundation of:

- **Typed data and resources:** Shared structures such as timelines, media assets, transcripts, scenes and graphs, with well-defined identities and relationships.
- **Capabilities:** Standardized ways to inspect, manipulate and transform these resources, accessible to both frontend components and agents.
- **Contributions:** A common mechanism for extending existing functionality without modifying its implementation.

The underlying data remains independent of any particular interface or agent. Multiple components and capabilities can operate on the same resources through consistent, validated operations.

## 2. Frontend: Spatially Composable Components

The frontend consists of independently functional components, such as timelines, inspectors, players, galleries and 3D viewers.

Every component should:

- **Be spatially composable:** Resize, move, dock, snap, float, nest or expand into different configurations.
- **Adapt to its container:** Support compact, expanded and fullscreen presentations without assuming a fixed position or screen size.
- **Support 2D and 3D:** Conventional interfaces work as normal web components, while the workspace can position them spatially alongside native 3D content.
- **Expose opinionated extension points:** Let developers define meaningful ways to extend their components, using shared contribution contracts wherever possible.
- **Maintain independent state and lifecycle:** Moving, hiding or replacing a component shouldn't disrupt its underlying data or ongoing work.

A **Tool**, such as a video editor, is an opinionated composition of components, their bindings and a default layout. Users and agents can rearrange or extend that composition without rebuilding the application.

The longer-term experience is an immersive, Minority Report-like creative workspace where components, results and agent activities can be pulled into focus and manipulated naturally.

## 3. Backend: Composable Agent Capabilities

The backend follows the same philosophy through Astrid's pack system.

Packs bundle discoverable, opinionated capabilities including:

- **Actions and tools:** Executable operations on shared resources.
- **Skills:** Guidance that teaches agents when and how to use those capabilities.
- **Rendering and processing:** Specialized implementations for generation, analysis and transformation.
- **Frontend contributions:** Interfaces through which users interact with those capabilities.

Packs can build on and extend other capabilities, allowing increasingly specialized workflows without duplicating their foundations.

For example, a music-editing pack could extend timeline editing with beat detection, audio alignment and music-aware editing operations.

## 4. Frontend and Backend: One Connected System

The frontend and backend should not be separate extension ecosystems. **A single pack can contribute both the capabilities an agent uses and the interfaces through which a person works with them.**

For example, a user asks:

*"Help me edit this video to the beat of the music."*

1. The agent discovers the appropriate music-analysis and timeline-editing capabilities.
2. It activates or assembles a music-editing interface, including beat visualizations, a mixer and timeline controls.
3. The user manipulates these components spatially while the agent analyzes the music and proposes edits.
4. Both interact with the same timeline and analysis data through shared capabilities.
5. The agent can refine the interface, extend its functionality or propose changes as the user's needs evolve.

**Spatial composition and functional composition are distinct but connected:** snapping components together determines their physical arrangement; binding them establishes shared data, context and behavior.

Users manipulate the environment through gestures, controls and conversation. Agents manipulate it through the same underlying operations and declarative workspace model.

## 5. Opinionated by Default, Extensible by Design

The goal is not to make everything infinitely configurable or force every component into one generic abstraction.

Instead:

- Components provide excellent default experiences and define how they should be extended.
- The platform standardizes extension registration, discovery, lifecycle, permissions and composition.
- Specialized contributions build on reusable contracts without losing domain-specific functionality.
- Users and agents can customize existing software or introduce new capabilities without discarding what already works.

**Generalize the mechanisms; preserve the opinions.**

## Guiding Principle

**Data defines what exists. Capabilities define what can be done. Components define how people interact with it. Packs extend the system. Workspaces compose the experience. Agents help continuously adapt it.**

The result is software that evolves with the creative process: not merely applications that agents can operate, but environments that people and agents can build, extend and reshape together while using them.
