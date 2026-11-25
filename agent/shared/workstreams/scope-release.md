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
2. **Investigate both ways.** Check proposed projects against code, task records and issues; independently scout problems from user reports, failures and handoffs, including closed/reopened issues. Consider adjacent projects for necessary prerequisites. Use [Sense check](sense-check.md) to challenge duplication, ownership and needless machinery. Generate and route the bounded research assignments as described below; commission them only where they can change a decision.
3. **Preserve evidence.** Commit and push actual assignment versions and original reports as they arrive. Project-specific findings live with the project's evidence; cross-project findings and release judgments live under `releases/<N>/evidence/scoping/`. Link existing evidence rather than copying it. One concise index records packet IDs, snapshots, immutable commit/path links and limitations. Verify remote readback before using reports downstream; retain originals and linked revisions. The existing board owns live state. Never publish secrets, private creative materials or unnecessary transcripts; use approved restricted evidence pointers when needed.
4. **Compose and sequence.** Reconcile findings, prefer reuse/subtraction and issue-sized repairs, and name one owner per shared contract and issue. Compare foundation-first, early vertical proof and dependency-led parallel delivery or a justified hybrid. Distinguish start, landing and proof dependencies, shared writers and capacity. Identify critical path, parallel lanes, early integrated witnesses, migration/rollback and pin order, evidence invalidation, scarce proof resources and freeze rehearsal. Explain why the chosen order wins; do not invent dates or waive required gates.
5. **Use existing records.** The release brief's Intent and Approach hold outcome and strategic sequencing; run.md holds operational lane/readiness order and milestones; decisions.md holds dated rulings. Project plan/inputs/tasks own design, evidence and exact dependencies. Link accepted findings. No second strategy document or tracker. Preserve active authority.
6. **Prepare review packages.** Use the [Sense check packet recipe](sense-check.md#assemble-a-review-packet). For consequential releases commission independent high-judgment synthesis of the original reports; materialise and commit the proposed documents; have a different reviewer check the actual diff against original evidence. Resolve material findings. A fresh holistic sense check then judges the revised whole, particularly sequencing and simpler alternatives, where the consequence warrants it. For a substantial release dispatched to ChatGPT, the synthesis, independent review and holistic sense check each use a different fresh `S` session; elsewhere use the run contract's configured high-judgment role. Small releases can combine stages without sacrificing necessary independence. Save each verdict and resolution against exact identities.
7. **Hand off.** Present the proposed brief, amended projects, sequence, acceptance criteria, evidence and remaining decisions to the owner. [Plan](plan.md) owns project planning, the [Lead](../../roles/leader.md) owns delivery, and [Release](release.md) owns integration and publication. On material drift, recheck affected evidence and preserve unaffected work.

### Generate and dispatch assignments

The coordinator derives the research from the named release's actual outcome, projects, predecessor and risks. No previous release's packet list, fixed packet count or prebuilt ZIP is required.

- Begin with a source and coverage pass: identify what is already known, the unresolved decisions and which source/evidence could change each decision. Recover existing work before commissioning more.
- Create bounded project checks (combine genuinely small or related ones), independent problem-first scouts for relevant failure surfaces and adjacent prerequisites, and cross-project investigations only for shared contracts, conflicting findings, coupled risks or sequencing decisions. Give the first group independent questions; let the later group consume their original reports. Add a focused reconciliation pass if coverage remains uncertain. Do not reproduce a full investigation that already has adequate evidence.
- Write one short assignment per independent question or cohesive group of questions. State its ID, expected outcome, source identities and records to read, concrete questions, dependencies, route, permitted actions and report destination. Use the [Sense check packet recipe](sense-check.md#assemble-a-review-packet) for judgments. Preserve the actual dispatched brief; use the existing evidence index for references and the board for live readiness. No duplicate tracker, mandatory blank report templates or separate schema.
- Choose difficulty before dispatch: `N` for bounded discovery, inventories and straightforward source verification; `X` for coupled analysis, architectural overlaps, conflicting evidence and substantial project checks; `S` for the genuinely hard decisions that need deepest judgment. Split separable fact-finding from judgment rather than routing an oversized mixed packet to the most expensive mode. Follow the [run contract's ChatGPT session modes](../run-contract.md#chatgpt-session-modes) and cheapest-model-first policy; put the route on each assignment. Do not silently substitute a mode. Reviewers use the independent judgment rules above.
- For a delegated run, refresh the latest approved astrid-dev instructions and verify skill installation/discovery where the environment supports it; record the instruction SHA. Sessions without installation capability read the exact approved or explicitly authorized proposed source. Verify session creation, resumption and evidence handoff with the first packet. Reuse the [dispatch workstream](../../roles/orchestrator/multi-manager-dispatch.md#every-hour) for liveness and hourly check-ins, adapted to read-only research and the coordinator's evidence writes, not its implementation or CI permissions. For ChatGPT dispatch cap active sessions at five (or the account's or owner's lower limit), including review and replacement sessions. Verify an actual hourly wake/resume mechanism or disclose the manual step; don't claim unverified automation. Fill free slots only with ready work, save verified original findings before starting dependent work, and stop the schedule at handoff.

## Completion

A reviewable, coherent release scope with justified sequence, issue dispositions, durable original findings and independent judgment. Unresolved blockers are explicit. Scope acceptance, execution and publication remain separate authorizations.
