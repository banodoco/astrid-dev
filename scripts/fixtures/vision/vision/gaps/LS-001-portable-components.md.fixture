# LS-001 — Creative components can't yet move freely

**Aspiration:** [Live tool composition](../pillars/liquid-software.md#live-tool-composition) (primary) · [Control at every layer](../principles/in-the-creators-control.md#control-at-every-layer) (supporting) · **Assessment:** Open, source inspection (2026-11-06).

## Desired state

Real creative components (timeline, player, inspector, gallery and others) can move, dock, resize, float and nest within a declarative workspace without losing their state, supported behavior or resource bindings.

## Current state

The [App source map](../../plans/24-liquid-workspace/inputs.md) identifies actual reusable editor views and a custom two-pane assembly. The standard editor shell still includes host-specific layout, gesture and context responsibilities. **This does not establish a general-purpose portable workspace host.**

## Gap

Component definitions, instances, presentation lifecycle, resizing and positioning are not yet proven independently portable across workspace layouts and creative domains. Responsive behavior and stable state during docking, nesting and container resizing are essential parts of this gap.

## Closure evidence

Rearrange the **real** player, inspector and timeline; retain playback, editing, selection and recovery state; save/restore the layout. Then host a genuinely different domain component using the same contract, without modifying the main editor shell.

## Sources and reassessment

[Component reference](../../plans/24-liquid-workspace/components.md) · [Pinned App code map](../../plans/24-liquid-workspace/inputs.md). Reassess only from exact candidate and tested behavior; a different mock shell does not close this gap.
