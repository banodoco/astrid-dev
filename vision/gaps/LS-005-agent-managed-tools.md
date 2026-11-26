# LS-005 — Agents can't yet reliably create and maintain their own tools

**Aspiration:** [Real-time functionality](../pillars/liquid-software.md#real-time-functionality) (primary) · [Explicit permissions and privacy](../principles/in-the-creators-control.md#explicit-permissions-and-privacy) (supporting) · **Assessment:** Open; initial assessment (2026-11-10); not implementation proof.

## Desired state

An agent can build or adapt a needed tool during creative work, register it with supported interfaces, keep it working as dependencies evolve and make every consequential change inspectable, permissioned and reversible.

## Current state

Astrid has packs, agent skills and extension points, and [Plan 06](../../plans/06-packs/plan.md) covers a trusted pack lifecycle. There is not yet reliable proof of an agent creating a tool, testing it against real creative work and maintaining it through later updates. Source/plan reassessment, 26 November 2026: [Plan 78](../../plans/78-live-custom-element-editing/plan.md) defines live agent-written custom rendering element admission, exact revision pins and no editor reload, under its explicitly trusted local project-pack assumption. That is meaningful prior art, not proof of an agent authoring, replacing and maintaining a complete interactive tool or of isolation for untrusted contributions. [Plan 41's draft refinement](../../plans/41-agent-managed-tools/plan.md) targets this missing evidence; no new product qualification is claimed.

## Gap

Agent-led authoring, verification, registration, compatibility monitoring, repair and rollback are not a unified proven flow. Installing or upgrading someone else's existing pack under [F-004](F-004-pack-lifecycle.md) does not establish this capability.

## Closure evidence

For a real creative task, an agent creates or adapts a narrow tool, tests it, shows its source and permissions, and requests approval to activate it. On a later breaking dependency change, it proposes a tested repair and can revert safely. Broken, malicious and incompatible cases do not lose work or acquire execution rights.

## Sources and reassessment

[VibeComfy extension plan](../../plans/17-vibecomfy-extensibility/plan.md) · [Pack lifecycle](../../plans/06-packs/plan.md) · [Plan 41 — agent-managed tools](../../plans/41-agent-managed-tools/plan.md). Reassess against actual creator/agent work and negative cases.
