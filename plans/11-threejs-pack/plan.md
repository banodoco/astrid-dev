# Three.js as a pack

**Vision gaps:** [Dependable pack lifecycle](../../visions/gaps/F-004-pack-lifecycle.md) (primary).

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Move the existing built-in Three.js functionality into the native pack format, keep it included by default, and preserve its currently supported behavior. This remains a draft until the current source and executable tasks are scoped. Status, owner, and estimate live in the [project queue](../../README.md).

## Goal and scope

- **Included:** identify the current Three.js feature surface; move it into a native pack; keep default inclusion; establish behavior before conversion and focused proof after conversion.
- **Deferred:** changes to Three.js behavior or broader pack-system redesign beyond what this conversion requires.
- **Still undecided:** exact source ownership, task breakdown, dependencies, routes, and test selectors; inspect current code before defining these.

## What we build on

The starting premise—that Three.js functionality is currently built in—is user-provided and not yet verified against current source. Reuse the established native pack conventions and integration described by [Plan 06 — Packs](../06-packs/plan.md), after confirming the relevant source and default-inclusion mechanism. Exact identities and evidence belong in [inputs.md](inputs.md).

## Sequence

1. Identify source ownership, feature entry points, default-inclusion mechanism, supported behavior, and focused checks.
2. Establish the current behavior and define bounded executable tasks.
3. Move the feature into the native pack format while preserving inclusion, discovery, loading, and supported behavior.
4. Repeat the same focused behavior checks and cover any changed pack boundary.

See [tasks.md](tasks.md) for the draft work outline. Before implementation, record the actual base branch and SHA, reusable work and verified predecessor inputs, a fresh candidate branch, and the verified `pre-main` destination in [inputs.md](inputs.md).

## Completion

Complete when Three.js functionality is owned by a native pack, remains included by default, and the same focused behavior checks pass on the converted candidate. Record any behavior that cannot be covered or source-level constraint discovered during scoping. Publication follows existing authority limits; this draft does not authorize execution.

## Read next

- [tasks.md](tasks.md): draft work outline; executable task details remain to be scoped.
- [inputs.md](inputs.md): source identities, retained work, references, and limits.
