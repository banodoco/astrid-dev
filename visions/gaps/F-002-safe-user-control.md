# F-002 — User control and recovery aren't fully proven

**Applies to:** [In the creator's control](../principles.md#in-the-creators-control) (primary) · **Assessment:** Open / partly implemented foundations (2026-11-06).

## Desired state

People can understand, grant, limit and revoke what Astrid and its agents may access, change, share or spend, and can recover safely from conflicting or rejected actions. Consequential changes, external effects and resource use follow explicit authority, and a refusal is respected. A sandbox is one safeguard, not the whole definition of creator control.

## Current state

Astrid Runtime has versioned project/task authority and the App/Agent have meaningful editing and conflict primitives. [Plan 01](../../plans/01-installer-consent/plan.md) is for installer choice; [Plan 04](../../plans/04-concurrent-edits/plan.md) addresses concurrent edits; [Plan 15](../../plans/15-openshell-safe-execution/plan.md) targets the independent [F-007 sandbox outcome](F-007-first-class-sandbox.md). These are different safeguards; together they **have not yet established this broader user-control outcome**.

## Gap

The user's authority over agent/tool actions, data access, external effects, concurrent editing and reversibility has not been proven coherently across representative real workflows. This is about **permissions, consent and control**, distinct from application installation/recovery (F-001) or whether a creative task produces the right result (F-003).

## Closure evidence

Representative real workflows show clear and enforceable grant/deny/revoke permissions, correctly scoped file/network/spend access, handling of concurrent edits, inspectable changes, refusal and undo/recovery after failed or conflicting operations. Isolated execution has its own bounded closure test under F-007; passing it alone does not close this broader gap.

## Sources and reassessment

[Plan 01](../../plans/01-installer-consent/plan.md) · [Plan 04](../../plans/04-concurrent-edits/plan.md) · [Plan 15](../../plans/15-openshell-safe-execution/plan.md). Individual changes may partially improve this gap; a completed component does not make the whole product safe.
