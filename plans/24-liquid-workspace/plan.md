# 24 — Portable, resizable creative components

**Start here:** [Astrid development skill](../../skills/astrid-dev/SKILL.md), [shared run contract](../../skills/astrid-dev-shared/run-contract.md), [tasks](tasks.md), [inputs](inputs.md). Status and priority live in the [catalog](../index.md).

**Vision gaps:** [LS-001 — Portable creative components](../../vision/gaps/LS-001-portable-components.md) (primary).

## Goal and scope

Make the real Astrid UI **components portable and container-responsive**. Creators can move, dock, float, nest and resize the actual timeline, player, inspector and a different-domain view without losing functionality, project identity or editing state.

**Included:** component definitions versus instances; declarative 2D layout; size and adaptation protocol (minimum/ideal/maximum sizes and compact modes); lifecycle and input/focus boundaries; reversible placement/resizing; saved layouts with restoration against real components.

**Separate work:** explicit typed component connections belong to [Plan 45](../45-component-connections/plan.md), and agent workspace actions to [Plan 46](../46-agent-workspace-operations/plan.md). Pack installation, domain-specific editing, universal graphs and native VR/3D workspace layouts are out of scope. This is a strong reusable foundation, not the entire liquid-software vision in one plan.

## Existing foundation

Reuse the App's real `TimelineEditor`, `PreviewPanel`, `PropertiesPanel`, gallery/transcript candidates and existing two-pane example in [inputs](inputs.md) and [component reference](components.md). Runtime remains the domain/project authority. Don't reimplement editing primitives from [Plan 18](../18-timeline-editing/plan.md).

## Proposed sequence

1. Audit mounting/state assumptions, gesture/focus ownership, container dimensions and layout constraints of real views.
2. Define a minimal versioned component definition/instance contract, container-aware sizing/adaptation, mount/unmount and stable identity.
3. Prove dock, float, nest, resize, maximize and saved/restore layouts with real player, timeline and inspector.
4. Qualify a distinct-domain view, mobile/compact sizing, permission boundaries, failures and restoration without corrupted creative work.

## Handoff and completion

**Produces:** versioned portable component and adaptive sizing contracts with tested reversible 2D layout operations. [Plan 45](../45-component-connections/plan.md) consumes instance identities to bind resources; [Plan 46](../46-agent-workspace-operations/plan.md) consumes safe layout operations. Freeze actual accepted revisions at execution.

On the existing editor, a user rearranges and resizes the real timeline/player/inspector and one other-domain component, preserving playback, edits, selection and project authority. Reopen the layout and recover from invalid sizes or failed mounts. Mock UIs alone are not acceptable proof.

**Authorization:** Draft only. Owner approval, exact source identities, focused tests and dependencies are required before product implementation.
