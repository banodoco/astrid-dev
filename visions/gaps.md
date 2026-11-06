# Gap contract

**Vision (pillars + principles) → Gaps → Plans → Evidence → reassessment.**

A gap records a **missing, independently assessable outcome**. It is neither a task nor an implementation design. All gap files live in `visions/gaps/<stable-id>-<slug>.md`, including cross-cutting infrastructure gaps.

## Minimal record

```md
# LS-001 — Portable creative components

**Applies to:** [Agent-Powered Liquid Software](../pillars/liquid-software.md) · [In the creator's control](../principles.md#in-the-creators-control)
**Assessment:** Open (YYYY-MM-DD; evidence basis)

## Desired state
What should be true?

## Current state
What can be demonstrated now, including source revisions and limits?

## Gap
What is missing, independent of a proposed fix?

## Closure evidence
What would demonstrate the desired result, including negative cases?

## Sources and reassessment
What evidence supports the assessment, and when should it be revisited?
```

**Applies to** may name any number of pillars and cross-cutting principles. The ID prefix (`AA`, `LS`, `CI`, `CA`, `F`) is stable identity only, **not exclusive ownership**. Add a new gap only if it has a genuinely distinct closure test; don't duplicate gaps for every principle or plan. Assessment values: **open**, **partially evidenced**, **closed**, **needs recheck**, always grounded in observations.

## Plans own the links

Each `plans/<id>/plan.md` specifies one primary and, where useful, supporting gap links:

```md
**Vision gaps:** [LS-001 — Portable components](../../visions/gaps/LS-001-portable-components.md) (primary).
```

Or state `**Vision role:** Foundational enabler — ...` for work whose completion is not direct proof of a gap. Gaps must **not** maintain reverse lists of plans. The root [project queue](../README.md) alone owns plan status, owner and priority.

## Evidence updates gaps, not vice versa

After a plan completes or important new evidence emerges, an agent may propose a gap update comparing the *actual* results with the desired state and closure criteria. A reviewer decides whether the gap is closed, partly evidenced, unchanged or needs recheck; the proposal doesn't change plan authority. A completed plan never closes a gap automatically.

**Future checks, not built:** validate unique gap IDs, `Applies to` targets, basic fields and valid plan references; later let agents propose evidence-grounded reassessments. Prove the manual process before adding automation. Preserve sources and avoid a second roadmap or duplicate status ledger.
