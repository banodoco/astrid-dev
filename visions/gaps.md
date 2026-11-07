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

Gaps are **typically one abstraction level above projects**, but do not manufacture another layer just to maintain a hierarchy. **Each gap has exactly one primary vision pillar or principle**, followed by only genuinely relevant supporting connections. A primary connection is the clearest answer to "which aspiration does this outcome advance?"; supporting connections must describe a distinct, secondary implication rather than a general association. A gap may link only to a principle when no pillar is the natural conceptual owner. One gap can be addressed by several projects; one project can improve several gaps; a gap may exist before a project is chosen. Give a project one primary gap when appropriate and supporting relationships only where its evidence genuinely contributes. Plan status and ownership never belong in the gap file.

**Example:** [F-007](gaps/F-007-first-class-sandbox.md) asks whether people can choose and use a supported fully isolated Astrid environment. [Plan 15](../plans/15-openshell-safe-execution/plan.md) proposes OpenShell as one implementation. [F-002](gaps/F-002-safe-user-control.md) is the broader trust, permissions and recovery outcome. Completing Plan 15 could establish the narrower F-007 result while providing only partial evidence for F-002. Neither the vendor name nor a project's completion defines the gap.

## Reviewing a new or redefined gap

Before opening a PR that **creates, retires, renames or materially redefines** a gap, reconsider it from first principles. Start with the [existing gap list](README.md) and the [project catalog](../plans/index.md), not with the proposed implementation. A new project may simply be a way of closing an existing gap; a new gap is warranted only when it has a **different missing outcome and independently useful closure evidence**.

For each new or materially redefined gap, put a short, specific record in the **PR description**, not a second status registry:

```md
## Gap boundary assessment — F-005

Decision: Refine — Name local-first cloud delegation as the outcome rather than a single bundled project.
Outcome: A creator can use approved cloud compute without giving up the authority of their local project.
Existing alternatives: F-003 covers reliable creative execution; F-006 covers fully hosted state. Plan 25 is one project to approach F-005.
Why this level: The creator still needs this capability if the present Plan 25 implementation or provider is replaced.
Independent closure: A supported local project delegates work, returns editable results, and passes consent, custody, cancellation and failure tests.
Primary connection: principle:local-first-cloud-capable — Keeping local custody while drawing on cloud execution is the essential principle.
Supporting connections: principle:in-the-creators-control, principle:eliminate-needless-technical-wrangling — Consent and convenient execution matter as supporting aspirations.
Evidence: https://github.com/banodoco/astrid-dev/blob/main/plans/25-cloud-assist-v1/plan.md
```

Consider **reuse an existing gap**, **add a project to an existing gap**, **refine/split/merge existing gaps**, **create a genuinely independent gap**, and **use a foundational enabler plan without a gap**. The `Existing alternatives` and `Why this level` lines must explain *why the chosen alternative wins* over concrete nearby gaps/projects—not just say there is no overlap. If a project were replaced, would the outcome remain? Would completing the project still leave meaningful room to assess the gap? Is the closure proof specific and independent of a vendor or task checklist?

The existing [documentation CI](../.github/workflows/docs.yml) runs [`check_gap_boundaries.py`](../scripts/check_gap_boundaries.py) on PRs. It compares the proposed gap definition with the PR base. New/removed gaps and changes to the **title, Applies to relationships, Desired state, Gap, or Closure evidence** require one review record per affected stable gap ID. Changes confined to Current state, Assessment, or Sources and reassessment **do not** require another boundary decision. The check requires the decision, outcome, concrete alternatives, argument for abstraction level, independent closure test, **primary connection with its reason, explicitly defended supporting connections (or None)** and source evidence. CI compares the declared primary/supporting references with the changed gap's metadata; it **cannot judge whether those connections are philosophically warranted**. A reviewer must challenge shallow rationales, unsupported assumptions, duplicated closure tests and project-specific wording before approving. No new approval layer is created, and the [plan-completion evidence gate](../AGENTS.md#completing-a-plan-one-decision-gate) remains separate.

For a baseline review of every existing ID and its closest overlap, see the [November 7 gap abstraction audit](references/gap-abstraction-audit-2026-11-07.md). Revisit its conclusions when real evidence exposes a different boundary; do not treat it as a parallel project or gap-status database.

## Minimal record

```md
# LS-001 — Portable creative components

**Applies to:** [Agent-Powered Liquid Software](../pillars/liquid-software.md) (primary) · [In the creator's control](../principles.md#in-the-creators-control) (supporting) · **Assessment:** Open (YYYY-MM-DD; evidence basis)

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

**Applies to** must name exactly one **(primary)** pillar or principle, first, followed by zero or more explicitly labeled **(supporting)** references; never add an unlabeled or duplicate relationship. The ID prefix (`AA`, `LS`, `CI`, `CA`, `F`) is stable identity only, **not exclusive ownership**. Add a new gap only if it has a genuinely distinct closure test; don't duplicate gaps for every principle or plan. Assessment values: **open**, **partially evidenced**, **closed**, **needs recheck**, always grounded in observations.

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
