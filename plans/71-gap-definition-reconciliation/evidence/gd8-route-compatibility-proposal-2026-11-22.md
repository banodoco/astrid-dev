# GD-8 — proposed closure routes, IDs and consumer compatibility (review candidate)

**Written UTC:** 2026-11-22T04:10:51Z. Baseline `6d75abf9cb0d102a1fef494f78dd9184d4e45d1f`; later read-only Astrid Dev source `70d5ac857e8066f8cacf98cda7b9d5d686a12f71`.

**Decision:** `PROPOSAL ONLY / NO ID OR SOURCE MIGRATION / NO RS2 YET`.

## Deterministic baseline and deltas

- The original fixed-census archive SHA-256 is `f1ba3a7a98db0c9a6869afd1529d7c068ffbbd2f055bc6ebc4592bd7a5e1fea9`, **22 gaps, 77 plans, 232 unique issues (219 open / 13 closed), 95 authored plan–gap links across 68 plans**, nine explicitly enabler/no-gap plans. Every one of the 95 links targets an existing gap; visible curated issue-label metadata includes 18 `gap:` mentions and 72 `plan:` mentions, all resolving to valid baseline IDs; masked records do not expose their labels for this recheck. **Label coverage is sparse**, so valid labels are not an exhaustive issue-to-gap mapping or evidence of closure.
- At source `70d5ac857e8066f8cacf98cda7b9d5d686a12f71`, comparison since the fixed baseline shows **four preexisting plan.md files changed** (Plans 13, 55, 75 and 77), with their authored gap declarations unchanged. Three new plans (81/82/83) add **four authored links** (81 F-008 primary + F-001 supporting; 82 F-008; 83 F-001). Thus **95 + 4 = 99 authored current plan–gap links** *at this inspected source*, with **all 22 gap documents unchanged**. The baseline itself is not rewritten.
- #1283 alters *provisional* heavy-timeline load/CPU targets in Plan 77, not measured compliance. #1282 changed only canonical GD-4/RS1 progress. Ten issues were created after the cutoff and one existing coordination issue later updated. They are separately dated source leads, not retroactively part of the 232-ID census.

## Critical canonical route/backlink finding

The current [contribution-workflow rule](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/docs/contribution-workflow.md#define-or-reassess-a-vision-gap) states: once plans serve a gap, include **Closure approach** and **Route to closure** mapping every closure item to a delivering plan or to `unplanned`; a *routed* plan must link back via **Contributes to closure**. This is not merely a link-to-existing-gap check.

I read the **actual GitHub Markdown of all 22 baseline gap files** and their section headings, independently of the curated extractor (which intentionally sampled only common sections):

- Only **three** already have **both** `## Closure approach` and `## Route to closure`: **CA-005, F-004, F-008**. Their exact baseline Git blobs are `5334ffa9f26c7145c26e7cf8455106c13c598f36`, `41e9160f8bfb7d3345899a676031cc4cc9ebcaa5` and `a37c252e33e45f3db74e5231234fdfe5c896cded`.
- **Nineteen** lack those two sections. **Eighteen of those have at least one inbound authored plan link**; CA-001 has none. This is a genuine **route-coverage/documentation debt** relative to the published authoring rule, not evidence of 18 new vision gaps.
- Of 68 linked baseline plans, **nine** author a `Contributes to closure` statement. **59** have gap references but no explicit delivery statement. That is **not automatically 59 invalid plans**: referencing a gap can be contextual/supporting; do not manufacture closure contributions. The three already routed gap pages name the nine contributing plans exactly (CA-005 routes 48/51/73, F-004 routes 78, F-008 routes 12/17/32/33/34).
- **F-008** has eleven baseline inbound plan references, but its authored route names only five. Six additional relationships (40/50/54/55/56/59) remain contextual or unqualified as direct closure contributions; author approval and demonstrated outcome are required before adding them to the route.

**GD-8 recommendation:** Record **one source-cited prospective closure-route candidate per served gap** instead of rewriting each gap's goal/ID. For each actual closure item choose a supported delivering plan, mark it `unplanned`, or flag `PENDING EVIDENCE`; a plan cannot gain a `Contributes to closure` claim merely because it has a gap link. If a route would materially change which creator outcome counts, give it an original first-principles boundary assessment and independent review. Do not edit active plan owners' sources or weaken the route check.

## Important cross-gap mapping distinctions

| Current source conflict | Authored evidence | GD-8 proposal / proof gate |
|---|---|---|
| **F-001 operational lifecycle vs saving responsiveness** | [F-001](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/vision/gaps/F-001-platform-reliability.md#L5-L22) explicitly covers install/launch/stop/update/rollback/recovery, while [Plan 75](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/75-fast-saving/plan.md) and [Plan 77](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/77-saving-holds-on-a-heavy-timeline/plan.md) measure Runtime acceptance and editor saving. | Treat these as related reliability work, **not F-001 lifecycle closure**. Test user saved/reopened work and refusal before proposing a changed primary link or distinct durability outcome; coordinate with active plan owners. |
| **F-008 machine/engine portability vs local command latency** | [F-008](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/vision/gaps/F-008-portable-generation.md#L27-L52) requires same request across machines/engines; [Plan 55](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/55-local-speed/plan.md) and [Plans 81](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/81-once-per-command/plan.md)/[82](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/82-reuse-across-commands/plan.md) address warm overhead and command reuse. | Do not count microbench latency reduction as portability proof. Compare a real installed creator-to-usable-result scenario against multi-target execution and refusal; keep speed as `PENDING EVIDENCE` boundary if independent. |
| **CA-003 already requires public decision trace** | [CA-003](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/vision/gaps/CA-003-vision-experiments-progress.md#L5-L25) specifies three public source-linked decisions including a negative case. Plan 53 itself explicitly says it does not deliver the gap's closure test. | Retain gap boundary; improve actual source/route evidence as appropriate. Do not mark the goal/UI hierarchy alone as closure. |
| **F-003 one creative job** | [F-003](https://github.com/banodoco/astrid-dev/blob/6d75abf9cb0d102a1fef494f78dd9184d4e45d1f/vision/gaps/F-003-creative-execution.md#L5-L23) requires real editable job output and failure cleanup. Nineteen plans link it. | Need actual product run on named supported system with correct artifact, denied/failed path; a plan/task/test fixture alone is not F-003 closure. |
| **Plan 83 structural refactor** | [Plan 83](https://github.com/banodoco/astrid-dev/blob/70d5ac857e8066f8cacf98cda7b9d5d686a12f71/plans/83-execution-host-in-modules/plan.md) lists F-001 for source modularity but promises supported behavior unchanged. | Keep foundational implementation risk distinct from user lifecycle result; never declare F-001 closed by extracting modules. |
| **Plan 53 and Plan 73 shared homes** | Current contribution workflow, gap template and parser use `**Aspiration:**` for actual vision goals; exporter retains `characteristics` and legacy `appliesTo` projections. Plan 53 Dev PR #1059 and App PR #323 remain draft, Plan 73 PR #1256 is also draft as last checked. | Before any GD-9 migration or authoring-rule edit, recheck actual landed owner branches and exact App consumer; run original docs/feed/negative tests and obtain sibling custody. Do not edit these sources from GD-7/8. |

## Dated post-cutoff issue overlay

The original ten after-cutoff issue observations, plus five later original-source checks, are consolidated in [GD-8 post-cutoff source triage](gd8-postcutoff-triage-2026-11-22.md). This overlay is **not** part of the fixed 232-ID GD-6 baseline. No protected holdout content has been re-read.

## Exact next actions, evidence qualification, rollback

1. **Do not revise the accepted frozen v1 rubric**, change gap IDs or treat these proposals as migration. Preserve original raw source/case history and **HOLD consumed 1/1**.
2. Complete the **22-gap route-coverage plan** with one proposed approach/route or explicit no-route reason per gap. For each missing route item, match an actually evidenced delivering plan or `unplanned`, with source and a positive/adverse user acceptance test; preserve old plan wording until owner/project manager coordinates. This is GD-8 proposal work, not a mass edit.
3. Obtain current issue-label and plan schema projection from fixed source, including primary/supporting goals, `gap:ID` and `plan:NN` labels; compare with the live App feed and Plan 53/73 integration. Carry all existing 22 IDs and 95 baseline links plus dated four new links into a rollback/compatibility table; no generated view edits now.
4. **Independent high-judgment RS2** must review the complete integrated GD-7/GD-8 candidate after its own focused checks. An independently adverse finding becomes a task before new review, within the accepted round ceiling.
5. The owner alone makes **GD-9** on the **exact reviewed migration proposal**. Then only approved canonical gap/plan/issue changes may land after original focused tests, `python3 scripts/astrid_dev.py check`, `sync`, source-interface tests, and App qualification where affected. No final project-to-main merge without separate owner permission.

**Unresolved:** this is manager analysis, not an independent RS2 verdict, product retest, general issue-to-gap labelling, or authority to rewrite 18 gap files. No second progress writer is assigned or started. Phases 6–7 (recurring) stay deferred.

## Catalogue migration authorization boundary

The proposed mapping is **identity for every one of the 22 original gap IDs**, with no new, retired, merged, renamed or closed IDs. The route ledger is a bounded evidence request, **not** 18 automatic gap-file edits or 59 automatic plan backlinks. A different map would require independent RS2 and then explicit owner GD-9 approval with source ownership, rollback and compatibility proof.
