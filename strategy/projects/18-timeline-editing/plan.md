# 18 — Extensible timeline editing

**Contributing:** [Astrid development skill](../../../skills/astrid-dev/SKILL.md).

**Vision gaps:** [LS-003 — Composable frontend and backend contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (supporting). This plan proves one timeline-specific foundation, not the entire workspace/component contract.

Draft: provide dependable timeline editing primitives as a pack, so people and agents can build their own ways to understand, view, and edit the same creative material. Current status, owner, and estimate live in the [project queue](../../../README.md).

## Goal and scope

- Included: inspect current timeline/editing capabilities; expose and strengthen them through a pack that reuses current state and execution contracts; demonstrate an extension offering an alternate view or workflow over the same material; preserve media, edits, and undo where supported contracts provide them.
- Deferred: wholesale timeline redesign and capabilities unrelated to a reliable extension path.
- Still undecided: implementation task breakdown, dependencies, routes, and exact focused checks pending source inspection.

## What we build on

The existing timeline, editing implementation, state ownership, execution contracts, and pack conventions are to be identified at execution start. Do not assume primitives or extension support are absent. The design direction is in the [Liquid Software vision](../../vision/pillars/liquid-software.md); source identities and recorded inputs belong in [inputs.md](inputs.md).

## Sequence

1. Map supported timeline edit, media, undo, and extension contracts.
2. Shape small, composable primitives around current behavior, preserving supported media and edit state.
3. Add one concrete alternate view, effect, or workflow over the same material, with focused evidence for the contracts it exercises.

The intended work is preserved in [tasks.md](tasks.md); executable breakdown and exact checks remain to be scoped after inspecting current code.

## Completion

The editing pack and extension example work through documented timeline primitives, supported media/edit/undo contracts remain intact, and focused evidence demonstrates the shared-material workflow. Record unsupported contracts or extension needs discovered during scoping. This does not establish unsupported preservation behavior or authorize implementation/publication; follow the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md).

## Read next

- [tasks.md](tasks.md): intended work and draft status.
- [inputs.md](inputs.md): source identities, evidence, and limits.
