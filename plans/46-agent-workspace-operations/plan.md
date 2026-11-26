# 46 — Agents can reshape the creative workspace

**Project:** Agents can reshape the creative workspace

**Goal:** Give agents the same safe, inspectable place, attach, resize, bind and restore operations as creators, allowing them to adapt an active workspace without disrupting the work.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.7

**Estimate:** TBD

**Waiting on:** owner/scope agreement; source and dependency checks

**Start:** [Astrid development skill](../../agent/start.md) and [shared run contract](../../agent/shared/run-contract.md). [Inputs](inputs.md) · [Tasks](tasks.md). The [catalog](../index.md) owns priority, status and owner.

**Vision gaps:** [LS-002 — Agents can reshape the creative workspace](../../vision/gaps/LS-002-agent-workspace-control.md) (primary).

## Goal and scope

Give agents the same safe, inspectable place, attach, resize, bind and restore operations as creators, allowing them to adapt an active workspace without disrupting the work.

**Included:** Agent inspection and reversible workspace operations, permission checks, explicit data bindings, presets and conflict recovery.

**Draft refinement (26 November 2026):** A person can ask an agent to open a specific existing canvas or 3D scene, show the correct tool/inspector alongside a timeline, bind views to explicit resource IDs and focus a chosen view. Discovery lists installed component definitions, supported resource types/ports, allowed operations and target sessions; ordinary UI control uses typed shared operations, not generated React code or simulated clicks. The core routes the request to an explicitly selected active client/window, the React shell resolves and mounts the component, and a real client acknowledgement distinguishes applied, refused, unavailable, disconnected and stale. In headless mode, no interactive target is a truthful refusal, not a hidden queue. Persistent layout/instance/binding operations use versioned state and undo; focus/viewport/drag state stays client scoped unless explicitly saved. Open is not create or edit; those require separate resource grants. Preserve locked panels, human concurrent edits, user focus preferences, permission and unknown-target refusals. Reuse Plans 24 and 45, with the common resource/operation boundary in [Plan 100](../100-language-independent-foundation/architecture.md#agent-controlled-interface-the-workspace-as-a-resource) and session identity/grants from Plan 104. This refinement does not authorize execution or create a second layout authority.

**Boundary:** No separate agent-only interface model, silent project-data mutation or accidental proximity-based connections.

## What this builds on

[Plan 24 layouts](../24-liquid-workspace/plan.md), [Plan 45 bindings](../45-component-connections/plan.md) and [Plan 04 concurrent edits](../04-concurrent-edits/plan.md). These are foundations to verify at current source revisions, not proof of a deployed result. Prefer reusing them over inventing another runtime or state owner.

## Proposed sequence

1. Expose validated workspace inspection/layout commands over Plan 24 operations.
2. Connect Plan 45 bindings with agent permission gates and reversible previews.
3. Build a music editing preset around existing music.beats and timeline authority.
4. Test equivalent human/agent actions, concurrent edits, invalid commands and rollback.
5. Demonstrate opening an existing non-video resource beside a timeline, binding and focusing the correct inspector, saving/restoring the layout, and actual client acknowledgement; exercise disconnected/wrong window, headless, stale revision, denied grant, locked panel and failed component.

## Interfaces and handoff

Before product work, pin actual accepted base/donor revisions, implementation owners and dependencies. Consume existing pack/component/project contracts; produce a tested contract or working artifact and link exact product PRs. Never infer authorization from a draft.

## Completion

Test equivalent human/agent actions, concurrent edits, invalid commands and rollback. Prove the targeted session and actual visible mount on real UI for timeline and one different domain; missing/failed component and disconnected client must not pretend success or corrupt saved layout. A headless agent can edit resources but cannot show an interface without an active target. Record integrated candidate identity, real creator/agent outcomes and meaningful negative cases. Completion does not automatically close the associated vision gap.

**Authorization:** Draft, unassigned, queued. Owner decision and focused checks are required before implementation.
