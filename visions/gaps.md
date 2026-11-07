# Gap contract

**Vision (pillars + principles) → Gaps → Plans → Evidence → reassessment.**

A gap records a **missing, independently assessable outcome**. It is neither a task nor an implementation design. All gap files live in `visions/gaps/<stable-id>-<slug>.md`, including cross-cutting infrastructure gaps.

## How to normalize gap boundaries

A gap is **a missing outcome we would still care about if today's proposed project were cancelled or replaced**. A project is **one chosen piece of work** intended to change that outcome. They are related, not interchangeable, and the relationship need not be one-to-one.

Before adding or rewriting a gap, answer these questions:

1. **Outcome, not implementation:** Can the heading name what people cannot yet do or rely on, without naming a particular provider, component, project milestone or proposed solution?
2. **One coherent proof:** Is the desired result specific enough to have its own acceptance evidence, including meaningful negative cases? Avoid sweeping goals like "make everything safe" unless they explicitly describe a cross-cutting class of results.
3. **Stable under replanning:** Would this missing outcome remain important if its current project, technology or owner changed? If a project can finish and the outcome still isn't demonstrated, the distinction is real.
4. **No duplicate:** Does an existing gap already have essentially the same closure test? If so, link the new plan to it or sharpen the existing gap rather than create a duplicate.
5. **Evidence and scope:** Can we say what is demonstrably true today and what would change the assessment, on a named supported environment? An absent project, missing roadmap item or unverified feature claim alone is not evidence.

Gaps are **typically one abstraction level above projects**, but do not manufacture another layer just to maintain a hierarchy. One gap can be addressed by several projects; one project can improve several gaps; a gap may exist before a project is chosen. Give a project one primary gap when appropriate and supporting relationships only where its evidence genuinely contributes. Plan status and ownership never belong in the gap file.

**Example:** [F-007](gaps/F-007-first-class-sandbox.md) asks whether people can choose and use a supported fully isolated Astrid environment. [Plan 15](../plans/15-openshell-safe-execution/plan.md) proposes OpenShell as one implementation. [F-002](gaps/F-002-safe-user-control.md) is the broader trust, permissions and recovery outcome. Completing Plan 15 could establish the narrower F-007 result while providing only partial evidence for F-002. Neither the vendor name nor a project's completion defines the gap.

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
