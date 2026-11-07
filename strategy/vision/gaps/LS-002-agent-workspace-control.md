# LS-002 — Agents can't yet reconfigure the workspace

**Applies to:** [Agent-Powered Liquid Software](../pillars/liquid-software.md) (primary) · [In the creator's control](../principles.md#in-the-creators-control) (supporting) · **Assessment:** Open, source inspection (2026-11-06).

## Desired state

An agent and a person use the same supported workspace operations to open, place, attach, bind, focus and restore component instances. Changes are inspectable, scoped, reversible and compatible with live creative work.

## Current state

Astrid Agent has pack/skill/action discovery. Astrid App has extensions, commands and scoped editing contexts. The [source review](../../projects/24-liquid-workspace/inputs.md) has **not** established a public, domain-neutral workspace manipulation API.

## Gap

Spatial **placement/attachment** and functional **resource binding** need explicit, validated operations; proximity alone must not silently connect data. Agents should compose existing software without generating frontend code for ordinary layout changes.

## Closure evidence

An agent arranges the same real components as a user, binds the correct timeline/selection/clock, offers reversible operations, does not clobber user edits, and restores a prior workspace from a saved representation.

## Sources and reassessment

[Component vocabulary](../../projects/24-liquid-workspace/components.md) · [Source map](../../projects/24-liquid-workspace/inputs.md). Closing this gap requires a real human–agent journey and negative/conflict cases, not only registered commands.
