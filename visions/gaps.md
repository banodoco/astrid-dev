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

Or state `**Vision role:** Foundational enabler — ...` for work whose completion is not direct proof of a gap. Gaps must **not** maintain reverse lists of plans. The [plan catalog](../plans/index.md) alone owns plan status, owner and priority.

## Evidence updates gaps, not vice versa

When a PR changes a plan to `done`, its description must include a [completion assessment](../AGENTS.md#completing-a-plan-one-decision-gate): evidence against plan completion and a justified disposition for **every linked gap** (or no-gap explanation for an enabler). After a plan completes or important new evidence emerges, an agent may propose a gap update comparing the *actual* results with the desired state and closure criteria. A reviewer decides whether the gap is closed, partly evidenced, unchanged or needs recheck; the proposal doesn't change plan authority. A completed plan never closes a gap automatically.

**Checks today:** `python3 scripts/check_docs.py` validates unique gap IDs, required fields, local target paths, plan-folder structure, plan declarations, the authoritative [plan catalog](../plans/index.md) and its generated README preview. Run `python3 scripts/check_docs.py --sync` after editing catalog order or statuses. The focused GitHub Actions workflow runs those checks without pushing changes.

**Not automatically checked:** truth of evidence, whether a gap has really closed, external URLs and GitHub heading fragments. An agent may later propose evidence-grounded reassessments, reviewed by humans. Do not turn the catalog into a duplicate gap/status ledger.
