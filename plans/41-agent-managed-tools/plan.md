# 41 — Agent-created tools that stay maintained

**Project:** Agent-created tools that stay maintained

**Goal:** Let an agent add a creative tool using established pack/extension contracts, test it on real work and maintain it through changes without overriding the creator's control.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** owner/scope agreement; source and dependency checks

**Start:** [Astrid development skill](../../agent/start.md) and [shared run contract](../../agent/shared/run-contract.md). [Inputs](inputs.md) · [Tasks](tasks.md). The [catalog](../index.md) owns priority, status and owner.

**Vision gaps:** [LS-005 — Agent-created tools that stay maintained](../../vision/gaps/LS-005-agent-managed-tools.md) (primary).

## Goal and scope

Let an agent add a creative tool using established pack/extension contracts, test it on real work and maintain it through changes without overriding the creator's control.

**Included:** Agent author/adapt/verify/test/update proposals, version tracking, compatibility checks and safe rollback for creator-approved tools.

**Draft refinement (26 November 2026):** The agent can modify a supported existing tool through declared extension slots and behaviors, create a whole new React/TypeScript creative tool with optional Python/backend capabilities, and open or select it as an alternative view of the same authoritative resource. Make this a genuine live creative workflow: edit scoped source, compile/test, preview, register, activate within the creator's established trust/grant scope, modify again while in use, and restore the prior working version. The normal route does not require a Rust rebuild, base app rebuild or page reload. If an incompatible change needs a scoped backend restart or explicit migration, surface it truthfully. Default creative views should progressively use the same public extension contracts, not privileged private access; the first witness is one independently authored alternate view, not conversion of every built-in tool. No extension may create a second authority for a timeline, canvas, database or resource history. See [native foundation design](../100-language-independent-foundation/architecture.md#agent-authored-tools-and-replaceable-default-interfaces).

**Boundary:** No silent arbitrary code execution or unchecked self-updates; reuse trusted pack installation and authorization. Respect Plan 78's existing trusted local authoring scope and digest-pinned render behavior; do not present it as a sandbox. New grants/trust elevation require approval, untrusted code needs the independently reviewed isolation/bridge owned with Plan 15, and ordinary open/arrange operations remain Plan 46. Plan 100 owns the resource/operation boundary, Plan 101 local/hosted delivery, Plan 47 demanding pack qualification and Plan 57 extension state/migration policy. No competing pack manager.

## What this builds on

[Plan 06 packs](../06-packs/plan.md), [Plan 17 extension points](../17-vibecomfy-extensibility/plan.md), [Plan 78 live custom-element editing](../78-live-custom-element-editing/plan.md) and [Plan 100 shared contracts](../100-language-independent-foundation/plan.md). These are foundations to verify at current source revisions, not proof of a deployed result. Prefer reusing them over inventing another runtime or state owner.

## Proposed sequence

1. Identify missing agent-facing operations in current pack authoring, tests and updates.
2. Implement narrow create/adapt/test/preview and proposed activation using existing extension interfaces.
3. Track dependency versions and propose tested repairs when upstream changes.
4. Demonstrate initial tool creation, real creative use, a later breaking update, refusal and rollback.
5. Prove an agent-authored entire React tool and a supported extension/alternate view over an existing real resource, with live update, Plan 46 open/bind, preserved canonical history and return to default; coordinate local and hosted witnesses with Plans 101/47.

## Interfaces and handoff

Before product work, pin actual accepted base/donor revisions, implementation owners and dependencies. Consume existing pack/component/project contracts; produce a tested contract or working artifact and link exact product PRs. Never infer authorization from a draft.

## Completion

Demonstrate initial tool creation, real creative use, a later breaking update, refusal and rollback. A real user requests a lighting or character tool; the agent extends an existing view, authors a complete tool with typed capability, opens it, modifies it live, switches to/from a compatible alternate resource view, and reads back the same project/revisions. A broken build or mount retains the working version; denied or broadened capability cannot silently activate; no main app/Rust rebuild for compatible frontend edits. Record actual installed local/hosted evidence, trust limits and failure cases. Record integrated candidate identity, real creator/agent outcomes and meaningful negative cases. Completion does not automatically close the associated vision gap.

**Authorization:** Draft, unassigned, queued. Owner decision and focused checks are required before implementation.
