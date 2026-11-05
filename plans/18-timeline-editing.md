# 18 — Extensible timeline editing

**Draft scope — not yet fully specified.** Current project status is in the README queue.

## Goal

Provide reliable, composable timeline editing primitives as a pack that lets humans and agents build and share alternate understanding, views, effects, and workflows on the same creative material. Keep the core useful on its own while giving users control over how they extend it, including through extensions built on other extensions. See the [extensibility philosophy](../docs/extensibility-philosophy.md).

## Owner

See the root [README queue](../README.md) for ownership.

## Scope

- Included: inspect current timeline and editing capabilities; expose and strengthen existing editing capabilities through a pack, reusing the current state and execution contracts; demonstrate an extension that offers an alternate view or workflow over the same material; preserve media, edits, and undo behavior where supported contracts provide them.
- Deferred: wholesale timeline redesign and capabilities unrelated to establishing a reliable extension path.

## Inputs and source identity

Do not assume editing primitives or extension support are absent. At execution start, identify the owning repository or repositories, current refs and SHAs, dirty work to preserve, existing timeline/editing contracts, and the intended `pre-main` destination. Freeze source identities before changes and preserve existing behavior based on what the source actually supports.

| Input | Why it matters | Link or evidence |
|---|---|---|
| Current timeline and editing implementation | Establishes existing capabilities, state ownership, and supported preservation behavior. | Inspect the owning source at execution start. |
| Existing pack conventions | Helps place the extension at the current composition boundary. | Inspect current pack contracts at execution start. |

## Intended work and focused proof

- Map the supported timeline edit, media, undo, and extension contracts before changing them.
- Shape small, composable primitives around current behavior, preserving supported media and edit state.
- Add one concrete alternate view, effect, or workflow as an extension over the same material, with focused evidence for the contracts it exercises.

Define implementation tasks and exact focused checks after inspecting current code. Avoid inventing a large API or claiming existing functionality is missing without evidence.

## Completion

Complete when the editing pack and its extension example work through documented timeline primitives, supported media/edit/undo contracts remain intact, and focused evidence demonstrates the shared-material workflow. Record any unsupported contracts or extension needs discovered during scoping.
