# F-002 — Trustworthy user control and operation

**Applies to:** [In the creator's control](../principles.md#in-the-creators-control) · [Agent-Powered Liquid Software](../pillars/liquid-software.md) · **Assessment:** Open / partly implemented foundations (2026-11-06).

## Desired state

Human and agent actions are transparent, permissioned and recoverable. Creative state is not silently overwritten, external effects and resource use follow declared consent, untrusted execution has explicit safety boundaries, and stopping work does not destroy project data.

## Current state

Astrid Runtime has versioned project/task authority and the App/Agent have meaningful editing and conflict primitives. [Plan 01](../../plans/01-installer-consent/plan.md) is for installer choice; [Plan 04](../../plans/04-concurrent-edits/plan.md) addresses concurrent edits; [Plan 15](../../plans/15-openshell-safe-execution/plan.md) proposes qualified sandbox boundaries. These are different safeguards; together they **have not yet established this general outcome**.

## Gap

Unifying the user-facing expectations of consent, recoverability, isolation, safe resource use and simultaneous editing requires real integrated evidence, especially around agent actions and failure/refusal cases.

## Closure evidence

Focused real-path tests of affirmative/denied consent, scoped permissions, concurrent user/agent writes and conflicts, preservation of unsaved work, safe cancellation/cleanup and honest sandbox limits. No claim of unrestricted security or isolation beyond verified environments.

## Sources and reassessment

[Plan 01](../../plans/01-installer-consent/plan.md) · [Plan 04](../../plans/04-concurrent-edits/plan.md) · [Plan 15](../../plans/15-openshell-safe-execution/plan.md). Individual changes may partially improve this gap; a completed component does not make the whole product safe.
