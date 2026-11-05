# 17 — VibeComfy extensibility with H3_AV

**Draft scope — not yet fully specified.** Current project status is in the README queue.

## Goal

Make it easier for people and their agents to build and share creative tools on VibeComfy. Use H3_AV’s abstraction over MiniMax H3 workflows to improve the existing extension primitives, then show how someone can adapt or build on H3_AV itself without forking core. See the [extensibility philosophy](../docs/extensibility-philosophy.md).

## Owner

See the root [README queue](../README.md) for ownership.

## Scope

- Included: inspect the current VibeComfy code and H3_AV workflow; reuse existing concepts; make the relevant inputs, outputs, and composition boundaries understandable and usable; let users extend and customize workflows without a core fork; provide one focused example extension and focused proof.
- Deferred: broad workflow redesign, unrelated pack work, and GPU execution for this planning effort.

## Inputs and source identity

Treat H3_AV as a concrete user-provided example, not evidence of particular APIs or missing capabilities. At execution start, identify the owning repository or repositories, current refs and SHAs, dirty work to preserve, and existing workflow and pack extension points. Freeze those identities before source changes and verify the intended `pre-main` destination then; do not assume branches or APIs from this draft.

| Input | Why it matters | Link or evidence |
|---|---|---|
| Current VibeComfy implementation | Shows which workflow primitives and extension contracts already exist and should be reused. | Inspect the owning source at execution start. |
| H3_AV | Supplies a higher-level abstraction over MiniMax H3 workflows in VibeComfy for proving customization and composition. | Inspect the user-identified pack and its source at execution start. |

## Intended work and focused proof

- Map the existing workflow inputs, outputs, composition path, and pack boundary before proposing changes.
- Improve only the extension primitives needed to make the H3_AV example composable and customizable without a core fork.
- Document the example's inputs, outputs, and extension points; add focused checks for its contract and extension behavior. Use focused workflow/contract checks for structural changes; define any real generation evidence and its authorized compute requirements during scoping. This draft runs no GPU work.

Define implementation tasks and exact focused checks after inspecting the existing code. Do not prescribe a broad suite or assume a new API before that review.

## Completion

Complete when H3_AV demonstrates the documented VibeComfy extension path, users can customize and compose the relevant workflow without forking core, and focused evidence covers the resulting contracts. Record constraints or extension needs the example does not cover.
