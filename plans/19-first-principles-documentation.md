# 19 — First-principles documentation

**Draft scope — not yet fully specified.** Current project status is in the README queue.

## Goal

Make Astrid understandable from its purpose down to its working contracts: a new reader should grasp the mental model, find the central Astrid skill, choose a workflow or pack, and learn how to extend it from concrete examples. Documentation should support a simple composable foundation where the core works and users and agents can build tools with control at every level. See the [Astrid philosophy](../philosophy.md).

## Owner

See the root [README queue](../README.md) for ownership.

## Scope

- Included: review documentation across Astrid repositories; organize it as a path from goal and mental model, through the central Astrid skill, to purpose-specific workflows, pack design, and extensibility; make code self-describing where possible; explain rationale and contracts without duplicating implementation; give each concept one canonical home with links from other repositories; check a small set of new-reader and agent journeys.
- Deferred: a mandatory comprehensive manual, wholesale rewriting of every page, and duplicated parallel documentation systems.

## Inputs and source identity

At execution start, identify the relevant repositories, current refs and SHAs, dirty work to preserve, current documentation entry points, and intended `pre-main` destination. Freeze identities before edits. Treat the proposed pyramid as a navigation and explanation goal; inspect existing material and preserve useful canonical sources.

| Input | Why it matters | Link or evidence |
|---|---|---|
| Existing Astrid repositories and docs | Reveals current canonical sources, entry points, and duplication to address. | Identify and inspect source repositories at execution start. |
| Astrid philosophy | Anchors the explanation in the intended product purpose and mental model. | [Astrid philosophy](../philosophy.md) |

## Intended work and focused proof

- Establish the top-level purpose and mental model, then link the central Astrid skill to focused workflow and pack guidance.
- Document extension contracts and examples where users or agents need to compose or build on existing tools.
- Choose a bounded set of new-reader and agent journeys and confirm each reaches the right explanation and evidence without requiring a large manual.

Choose the journeys after inspecting the current docs. Avoid copying API detail that code or generated references can keep authoritative.

## Completion

Complete when the documented path is navigable from a clear entry point to canonical sources across repositories, explains the key purpose and contracts at the right level, and the bounded journeys can be completed from the available docs and examples. Record remaining gaps without creating a second mandatory manual.
