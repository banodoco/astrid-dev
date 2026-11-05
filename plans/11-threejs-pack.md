# 11 — Move built-in Three.js functionality into a pack

**Start here:** read [AGENTS.md](../AGENTS.md), choose a workflow in the [skills guide](../skills/README.md), follow the [run contract](../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../docs/glossary.md).

**Draft scope — not yet fully specified.** Current project status is in the README queue.

## Goal

Move the existing built-in Three.js functionality into the native pack format while keeping it included by default and preserving its current supported behavior.

## Owner

See the root [README queue](../README.md) for ownership.

## Scope

- Included: identify the current Three.js feature surface; move it into a native pack; keep default inclusion; establish behavior before conversion and focused proof after conversion.
- Deferred: changes to Three.js behavior or broader pack-system redesign beyond what this conversion requires.

## Inputs and source identity

The user-provided starting premise is that Three.js functionality is currently built in and should become a native, default-included pack. This has not been verified against current source. At execution start, identify the owning repository or repositories, current refs and SHAs, dirty work to preserve, the feature entry points, current focused checks, and the supported default-inclusion mechanism. Do not infer these identities from historical plans.

| Input | Why it matters | Link or evidence |
|---|---|---|
| Pack conventions and integration | Reuse the established native pack boundary and focused acceptance. | [Plan 06 — Packs](06-packs/plan.md); confirm current source at start. |
| Existing Three.js behavior | Defines what must survive the move. | Establish source paths and current behavior checks before editing. |

## Intended work and focused proof

- Capture current Three.js behavior with explicit feature checks before conversion.
- Move it into the native pack format, preserving core inclusion, discovery, and loading.
- Rerun those behavior checks after conversion and cover any changed pack boundary with focused tests.

Define executable tasks, difficulty levels, and exact test selectors after inspecting the existing code. Before implementation, record the actual base branch and SHA, reusable work and verified predecessor inputs, a fresh candidate branch, and the verified `pre-main` destination. These linked plans are context, not blanket scheduling gates.

## Completion

Complete when the Three.js functionality is owned by a native pack, remains included by default, and the same focused behavior checks pass on the converted candidate. Record any behavior that cannot be covered or any source-level constraint discovered during scoping.
