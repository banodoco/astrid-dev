# LS-002 — Agent-accessible workspace composition

**Principle:** [Agent-Powered Liquid Software](../principle.md) · **Assessment:** Open, source inspection (2026-11-06).

## Desired state

An agent and a person use the same supported workspace operations to open, place, attach, bind, focus and restore component instances. Changes are inspectable, scoped, reversible and compatible with live creative work.

## Current state

Astrid Agent has pack/skill/action discovery. Astrid App has extensions, commands and scoped editing contexts. The [source review](../references/source-map.md) has **not** established a public, domain-neutral workspace manipulation API.

## Gap

Spatial **placement/attachment** and functional **resource binding** need explicit, validated operations; proximity alone must not silently connect data. Agents should compose existing software without generating frontend code for ordinary layout changes.

## Closure evidence

An agent arranges the same real components as a user, binds the correct timeline/selection/clock, offers reversible operations, does not clobber user edits, and restores a prior workspace from a saved representation.

## Sources and reassessment

[Component vocabulary](../references/components.md) · [Source map](../references/source-map.md). Closing this gap requires a real human–agent journey and negative/conflict cases, not only registered commands.
