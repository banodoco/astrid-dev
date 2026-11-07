# 24 — Agent-powered liquid workspace

**Start here:** read [Astrid development skill](../../skills/astrid-dev/SKILL.md), follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), then review [tasks](tasks.md) and [inputs](inputs.md). The [project queue](../../README.md) owns status, owner and estimate.

**Vision gaps:** [LS-001 — Portable creative components](../../vision/gaps/LS-001-portable-components.md) (primary); [LS-002 — Agent workspace control](../../vision/gaps/LS-002-agent-workspace-control.md) and [LS-003 — Full-stack contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (supporting). A proof of this plan does not automatically close all three.

## Goal and scope

Prove that **real Astrid creative components can be composed, moved, bound and extended by both a user and an agent** using one authoritative project state and a declarative workspace model. Preserve the video editor as an excellent default, not an architectural restriction.

**Included:** 2D workspace model and reversible layout operations; stable component definitions versus instances; instance-scoped resource/context binding; container-aware behavior; component-owned specialized extension points using existing contribution machinery; agent discover/open/place/attach/bind operations; a real music-editing composition reusing existing Music/Timeline capabilities.

**Deferred:** universal graph datastore, replacing Astrid Runtime, all components at once, automatic untrusted code execution, full immersive/VR experience or making Three.js the workspace's data authority. A 3D renderer may follow once 2D semantics have proven stable.

## What this builds on

- App's real `PreviewPanel`, `TimelineEditor`, `PropertiesPanel`, example alternate shell, extension SDK and timeline state/patch operations.
- Agent's `timeline` and `music` packs and skill/action discovery.
- Runtime's authoritative project/task/artifact and revision semantics.
- Existing [Plan 18](../18-timeline-editing/plan.md) **owns dependable timeline editing primitives**, [Plan 06](../06-packs/plan.md) pack loading, [Plan 04](../04-concurrent-edits/plan.md) concurrent safety, and [Plan 11](../11-threejs-pack/plan.md) current 3D feature extraction. **Do not re-implement their ownership.**
- [Plan 23](../23-agent-learning-integration/plan.md) can later make contextual community learning available during the music workflow, but the base composition proof should not require a new Hivemind protocol.

## Proposed sequence

1. Inspect the real components' size, gesture, focus and mounting assumptions; freeze source identities and choose a narrow pilot.
2. Extract one declarative 2D workspace shell: layout/attach/focus/float/maximize with undo or restore. Prove that moving genuine editor components preserves playback and editing state.
3. Define a portable component/instance/binding contract and test with one genuinely different surface (generation gallery or transcript editor), not only the video editor.
4. Let component authors publish opinionated extension points that reuse manifest registration, lifecycle and validation; keep standalone versus host-only contributions explicit.
5. Expose the same safe workspace actions to agents; **place/attach** must remain separate from semantic **bind**.
6. Create a music-editing preset with beat grid, timeline, preview and controls, drawing backend beat analysis from existing packs and authoritative edit commands. Validate user's and agent's concurrent work without silent overwrites.

## Completion

A user can begin with the real video editor, request a music-aware editing layout, manipulate/dock/float views, collaborate with an agent and restore the default layout. The agent can inspect the workspace and use the same validated placement/binding operations. No duplicate timeline state, lost unsaved work, broken gestures or hidden background task cancellation. A second domain component confirms the contract extends beyond the original shell.

**Authorization:** Draft only. Base identities, sources/donor branches, ownership, dependency results, focused tests and integration approval are TBD; no implementation work authorized by this plan.
