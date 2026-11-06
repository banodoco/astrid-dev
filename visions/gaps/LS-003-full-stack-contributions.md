# LS-003 — Composable frontend and backend contributions

**Principle:** [Agent-Powered Liquid Software](../principle.md) · **Assessment:** Open, source inspection (2026-11-06).

## Desired state

A creator or agent can discover and use one pack's creative capability, its typed results and its appropriate frontend components together—extending opinionated tools without bespoke, duplicate integrations.

## Current state

Astrid Agent pack manifests can declare actions, UI, renderers and skills. Astrid App has a video-editor extension SDK, typed data lanes, proposals and rendering hooks. Current pack UI hosting is still tied to supported host entries; **general component-owned extension points and unified live composition are unproven**.

## Gap

Common identity and discovery across pack contributions, semantic resource/result bindings, component-defined extension hosts and safe activation need proving beyond the default video editor.

## Closure evidence

An installed/trusted music capability yields a typed beat-grid result used in a real timeline view and music control surface. The interface can be rearranged, results correctly track source-to-timeline coordinates, and updates follow existing authoritative domain editing/undo. A second distinct extension domain validates generality.

## Sources and reassessment

[Pack + SDK evidence](../references/source-map.md) · [Component examples](../references/components.md). Preserve existing packs, domain authorities and permission boundaries; a manifest declaration alone is not execution proof.
