---
description: Compose a coherent release from actual product evidence, design its execution strategy and prepare it for independent review and scope acceptance.
skill: true
---

# Scope a release

## When to use

Before accepting a substantial release, or when its intended outcome or predecessor changes materially. For a small patch, use the same questions in its existing brief.

## Outcome

The smallest coherent release that delivers an agreed user outcome, with a credible execution sequence and source-linked acceptance evidence.

## Inputs

Owner direction, [strategy](../../../strategy.md), draft release, actual served and integrated predecessor tuples, current projects, issues, evidence and constraints. The [run contract](../run-contract.md) owns authority, routes, review depth and coordination.

## Procedure

1. **Frame.** State the outcome, supported cases, exclusions and proof. Identify the served release for migration/regression and the newest integrated predecessor for implementation. Inspect active work, pins and main-only changes; record exact identities and unknowns.
2. **Investigate both ways.** Check proposed projects against code, task records and issues; independently scout problems from user reports, failures and handoffs, including closed/reopened issues. Consider adjacent projects for necessary prerequisites. Use [Sense check](sense-check.md) to challenge duplication, ownership and needless machinery. Delegate bounded research where it can change a decision.
3. **Preserve evidence.** Commit and push actual assignment versions and original reports as they arrive. Project-specific findings live with the project's evidence; cross-project findings and release judgments live under `releases/<N>/evidence/scoping/`. Link existing evidence rather than copying it. One concise index records packet IDs, snapshots, immutable commit/path links and limitations. Verify remote readback before using reports downstream; retain originals and linked revisions. The existing board owns live state. Never publish secrets, private creative materials or unnecessary transcripts; use approved restricted evidence pointers when needed.
4. **Compose and sequence.** Reconcile findings, prefer reuse/subtraction and issue-sized repairs, and name one owner per shared contract and issue. Compare foundation-first, early vertical proof and dependency-led parallel delivery or a justified hybrid. Distinguish start, landing and proof dependencies, shared writers and capacity. Identify critical path, parallel lanes, early integrated witnesses, migration/rollback and pin order, evidence invalidation, scarce proof resources and freeze rehearsal. Explain why the chosen order wins; do not invent dates or waive required gates.
5. **Use existing records.** The release brief's Intent and Approach hold outcome and strategic sequencing; run.md holds operational lane/readiness order and milestones; decisions.md holds dated rulings. Project plan/inputs/tasks own design, evidence and exact dependencies. Link accepted findings. No second strategy document or tracker. Preserve active authority.
6. **Prepare review packages.** Use the [Sense check packet recipe](sense-check.md#assemble-a-review-packet). For consequential releases commission independent high-judgment synthesis of the original reports; materialise and commit the proposed documents; have a different reviewer check the actual diff against original evidence. Resolve material findings. A fresh holistic sense check then judges the revised whole, particularly sequencing and simpler alternatives, where the consequence warrants it. Small releases can combine stages without sacrificing necessary independence. Save each verdict and resolution against exact identities.
7. **Hand off.** Present the proposed brief, amended projects, sequence, acceptance criteria, evidence and remaining decisions to the owner. [Plan](plan.md) owns project planning, the [Lead](../../roles/leader.md) owns delivery, and [Release](release.md) owns integration and publication. On material drift, recheck affected evidence and preserve unaffected work.

## Completion

A reviewable, coherent release scope with justified sequence, issue dispositions, durable original findings and independent judgment. Unresolved blockers are explicit. Scope acceptance, execution and publication remain separate authorizations.
