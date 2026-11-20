# RS1 independent review package — exact v1 candidate, not clearance

**Disposition:** `REVIEW REQUIRED / BLOCKED`. No independent qualified RS1 verdict has been returned; no GD-5 owner acceptance has been granted; HOLD-01–10 are sealed. This is a *handoff to a separate reviewer*, not an RS1 review written by the plan author or manager.

## Source and checks

- **Candidate requiring review:** [GD-2 v1, Plan 71 PR #1102](https://github.com/banodoco/astrid-dev/pull/1102) at exact HEAD `6c1eca653659bd765a99cd810c33410b0a0622d5`, source `plans/71-gap-definition-reconciliation/evidence/gap-rubric-draft-2026-11-20.md`. The version under review is *not* the accepted canonical definition.
- **Original v0:** source merged through [PR #1089](https://github.com/banodoco/astrid-dev/pull/1089), integration commit `e03d09caf7ff84f2361de7b92eee9a00621bc3b5`.
- **Calibration sources:** [GD-3](calibration-2026-11-20.md), 16 source-linked CAL IDs and ten sealed HOLD IDs, merged through [PR #1086](https://github.com/banodoco/astrid-dev/pull/1086) at `fe2a9a38002f2337e9e39aa2b2c478c2d7f89cb9`.
- **Author-separated classifications:** [manager first pass](gd4-manager-first-pass-2026-11-20.md), [source-led second pass](gd4-second-case-assessment-2026-11-20.md) and [disagreement comparison](gd4-comparison-2026-11-20.md), merged through [PR #1100](https://github.com/banodoco/astrid-dev/pull/1100) at `cfa8d3db3374988e8ceb97efafaa314ace03e5a2`. Two calibration passes are not a substitute for a qualified independent high-judgment RS1.
- **Original CI on v1 HEAD:** `documentation`, `vision-consumer-contract`, and `review-intake` all **passed**; [run 44831249472](https://github.com/banodoco/astrid-dev/actions/runs/44831249472) and [run 44831249730](https://github.com/banodoco/astrid-dev/actions/runs/44831249730). Structural CI does not prove semantics.
- **Review request state as checked 21 Nov 2026:** PR #1102 had zero review submissions and no assigned reviewer. A Copilot reviewer request returned GitHub HTTP 422 (*not a repository collaborator*). An attempted separate automation would execute inline in the same conversation, which is **not independent**; it was disabled without claiming review. No review pass is asserted.

## Qualifications required of an RS1 reviewer

A distinct, genuinely independent reviewer (human maintainer or separately run and identifiable qualified reviewer session, not the author/manager or an unverified bot) must:

1. Read current [Manage whole-project rules](https://github.com/banodoco/astrid-dev/blob/main/skills/roles/astrid-dev-manage/workstreams/whole-project.md) and [shared run contract](https://github.com/banodoco/astrid-dev/blob/main/skills/shared/run-contract.md), **exact v1 candidate**, original CAL issues/gaps, and both authored classifications. The PR title or green check is not evidence of correctness.
2. Identify reviewer identity, distinct session/provenance and review scope; cite exact commit SHA and original evidence. If independent qualification cannot be established, return `BLOCKED` without an approval claim.
3. Challenge the five tests of a valid gap, in particular **one primary vision goal, independently valuable creator/contributor outcome, falsifiable positive/negative closure while neighbors remain open, implementation independence, and nearest existing boundary**.
4. Attempt counterexamples: unverified vs genuinely absent capability; an issue affecting several gaps; one vision goal with distinct F-005/F-006 data custody outcomes; a vendor-specific request vs stable artistic direction; CA-002/CI-002 governance/privacy outcomes without frequent issues; an isolated CI failure (#644/#964) and faulty meter (#907).
5. Challenge **four open boundary families** from the comparison: CAL-01/02 durable editing vs existing F-002/F-003/AA-001; CAL-04 audiovisual references vs artistic-control outcome; CAL-12 persistent regions vs AA-001/LS-004; CAL-07/16 perceived local latency vs F-008 portability. For any proposed split or merge demand two distinct recipient journeys and their negative tests, not counts of bugs or common tools.
6. Review possible collision with the separate Plan 53 Goals/vision-feed owner and Plan 73 Markdown-first skill migration; no shared-source edit or implicit redefinition is authorized.
7. Return **per-finding BLOCKING / NONBLOCKING**, an explicit `REJECT v1 / REWORK BEFORE HOLDOUT / ACCEPT v1 FOR HOLDOUT ONLY` verdict, and the minimum exact changes supported by citations. Acceptance *for holdout* is not acceptance of the definition for all gaps.

## Holdout stop

**HOLD-01–10 must not be opened or classified until this independent reviewer has established a frozen, exact candidate and an approved holdout protocol.** This includes avoiding indirect retrieval of these issue bodies or retrospective tuning of v1 to their presumed answers. After the freeze, a designated reviewer tests each holdout exactly once, recording case classification, goal anchor, nearest gaps, no-change/split/merge decision, positive and negative closure evidence, errors and missing inputs. If it exposes a rubric flaw, preserve the failing verdict and select a *new* untouched set for a revised rubric; never convert the original held-out failure into in-sample success. Mere source titles or search results are not passing evidence.

## RS1 completion boundary

RS1 finishes only when a qualified review with verifiable source citations exists, blocking findings are resolved within the allowed review rounds, the v1 or revised exact candidate is independently judged against the intended holdout protocol, and an explicit review verdict is recorded in canonical Plan 71 evidence and progress. **GD-5 is a separate owner decision and remains pending even after RS1.** No approval of GD-5, GD-9, the all-gap census (GD-6), or Phase 6–7 recurrence follows from this packet.

**Current allowed next action:** assign an eligible independent reviewer to [PR #1102](https://github.com/banodoco/astrid-dev/pull/1102) or to an independently source-custodied review, examine their exact response, then resolve any blocking findings. The author/manager must not self-approve the review.
