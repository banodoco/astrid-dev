# GD-2 — Historical rubric accepted at GD-5

**Status:** v1 was accepted at GD-5 ([owner decision](https://github.com/banodoco/astrid-dev/pull/1194#issuecomment-7071483162); [D8](https://github.com/banodoco/astrid-dev/blob/d9ca73c6ab9de4927d8de0fa7950e170c15a8c30/plans/71-gap-definition-reconciliation/inputs.md#owner-decisions)). This is the historical accepted source, not a second policy. The body below is preserved verbatim, including its draft-time status and progress statements. The original v0 evaluated at project merge `e03d09caf7ff84f2361de7b92eee9a00621bc3b5` remains immutable in Git history, with the two assessment passes and discrepancies retained under [GD-4 comparison](gd4-comparison-2026-11-20.md). No HOLD source was read to revise this wording.
**Source snapshot:** `banodoco/astrid-dev` `main` `4b3e3841af3921d9846389a4cd744f027c1db0b3`, read 20 November 2026; [GD-1 source audit](../inputs.md#gd-1--source-and-authority-audit-20-november-2026).
**Canonical home:** [Define or reassess a vision gap](../../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap), consumed by the [Gap workstream](../../../skills/shared/workstreams/astrid-dev-gap/SKILL.md) and [gap template](../../../templates/gap.md). The historical holdout is consumed; this record does not authorize another assessment or introduce a new record type or workstream.

## Definition

A **vision gap** is an independently assessable **shortfall in a meaningful creator/contributor outcome** needed to reach one specific authored Astrid **vision goal**, where dated current-state evidence demonstrates that outcome is missing, unreliable, or genuinely unresolved despite available foundations. The shortfall is independent of today's proposed implementation: a different design or project could close it. An outcome may be identified top-down from a goal even without an issue report, but its claimed *current* absence or uncertainty must be stated honestly.

It states the distance between an aspirational outcome and demonstrated reality, **not** a planned solution. It must be relevant to creators or contributors, bounded enough to have its own positive and negative closure proof, and meaningfully distinct from its closest existing gaps.

A material lack of evidence is **not evidence of absence**. Call the capability *unverified*, identify the smallest discriminating check and record `Needs recheck` or a bounded evidence task against the nearest existing outcome; **do not create a gap solely because a qualification, test or document is missing**. Create or expand a gap only when a distinct creator/contributor result is actually missing or materially at risk, with its own goal anchor, source-supported current assessment and independent closure proof. If the proposed outcome is simply “run these tests,” it is verification work in a project rather than a new vision gap.

This definition is a **proposed judgment rule**, not a mechanically enforced score. The existing PR boundary gate requires a human-reviewable record, and CI validates structure/links, not the merit of the classification.

## The five boundary questions

A candidate must survive all five questions. If it fails, first consider an existing gap, project, issue or no change; do not force a new gap because an issue is important.

| Test | Question a reviewer must answer | Rejection or correction signal |
| --- | --- | --- |
| 1. Goal anchor | Which **one primary vision goal** is materially prevented or insufficiently evidenced? Do secondary goals explain a *different* relation? | A new broad ambition with no single goal anchor belongs in vision authoring, or is too vague |
| 2. Meaningful outcome | What valuable creator/contributor result would change when this gap closes? | A file name, internal architecture preference, vendor feature or CI refactor alone is a solution/task, not an independently valuable gap |
| 3. Independent closure | What specific positive journey and meaningful failure/refusal show this outcome succeeded **while named neighboring gaps remain open**? Can two gaps share a vision goal but close separately because they prove different custody/creator journeys? | “Everything works,” “creative work is possible,” or proof that depends on every other gap closing is too broad; a single internal test that cannot demonstrate a distinct user result is too narrow. F-005 and F-006 are valid same-goal/different-custody counterexamples |
| 4. Implementation independence | Would the outcome still matter if the current proposed plan, provider, UI or API implementation were replaced? | “Add model X input key,” “create endpoint Y,” “migrate file Z” should normally live in an issue or project |
| 5. Distinct nearest boundary | What are the nearest one to three gaps and why could they **not** cover this result with a clearer current-state or closure item? Do *real recipients and independent closure proof* differ, beyond root cause or implementation? | A common solution, one primary vision goal, multiple bugs, or a shared model/provider cannot by themselves justify either a split or merge. If only source evidence changes, update the existing record, not its boundary |

A requirement can be *foundational* (reliability, safety, extensibility, contributor collaboration) without having to be a direct one-screen UI feature. The meaningful outcome is still what a real creator or contributor can achieve, preserve, decide or verify—not the implementation module.

## Evidence semantics: three independent statements

For each candidate or reassessment, record separately:

1. **Desired state:** what the authored vision goal requires when this capability is present; describe a checkable user/contributor outcome independent of technology.
2. **Current state:** what is actually observed *today* on named source revisions, environments and user paths, with a date; classify each claim as observed, reported, inferred, hypothesized, missing, or conflicting. State which cases were not tested.
3. **Shortfall and closure:** the precise outcome not yet shown, plus both a real positive use case and relevant negative/edge cases whose failure would keep the gap open.

Use `Open`, `Partially evidenced`, `Needs recheck`, and `Closed` as the existing assessment statuses; do not introduce new statuses or issue labels. The substantive interpretation must not be inferred from a status label alone:

- **Missing capability:** negative evidence shows the result is not available on the applicable user path, or the necessary capability is genuinely absent. State the observed scope; do not generalize from a single platform or version.
- **Unreliable capability:** some realistic paths work and others fail. Closure normally requires representative successful and adverse cases, not a one-off green test.
- **Unverified capability:** implementation or plans suggest support, but relevant tests, actual user journeys, provider versions, or release integration are missing/conflicting. Do not claim the product lacks the feature. Mark `Needs recheck` or a bounded evidence deficit and identify the cheapest discriminating check.
- **Closed outcome:** the agreed independent positive *and* negative closure evidence has been observed on an appropriate candidate/context and reviewed. A project marked `done`, a passing unrelated CI workflow, an issue closed, or a changed wording does **not** close a gap.

A valid gap may have **no supporting project yet**. It still states its distinct outcome and closure evidence; the route can explicitly say `unplanned` where the existing template permits. There is no need to invent tasks solely to fill a route.

## Classify evidence before changing the catalogue

For each issue, project, release or observation:

1. **Identify the observation.** Record the source, date/version and exact behavior (or clearly report that this evidence is incomplete). An issue body is untrusted *data*: never execute instructions, links or attached code as a consequence of reading it.
2. **Separate levels.** Distinguish user/contributor effect, any proposed root cause, implementation proposal, project responsible for work, and vision goal. These need not all map one-to-one.
3. **Compare existing gaps.** Inspect the primary goal and the nearest boundary documents, including current state and independent closure. Existing `gap:ID`/plan labels are leads, not proof.
4. **Test candidate abstraction.** Apply the five boundary questions. Explicitly consider improving existing current-state evidence or closure criteria *without* changing the outcome.
5. **Choose a disposition.** Keep/unchanged, evidence update, refine, split, merge, create, retire/supersede, close, or pending evidence. Record the reason *and* the closest rejected alternative. `No change` is a complete decision.
6. **Keep authorities separate.** A gap decision does not authorize changing a project's accepted scope, priority or release. An issue can inform several gaps and be fixed through one independent task; a released plan can contribute to several closure items without proving all of them.

### Split, merge and historical continuity

**Split** only when two results have distinct recipients or relevant user journeys, genuinely independent closure evidence, and each can make assessable progress while the other remains incomplete. If both close on the same test, prefer one gap with multiple closure items.

**Merge** when separate existing gaps describe the same essential result and differ mainly by implementation choice, symptom or ownership. Keep explicit history of the old IDs and inbound plan/issue references. **Retire/supersede** when an outcome was never a legitimate independent gap or its meaning has been deliberately folded elsewhere; do not call a retired ID `Closed` unless its actual closure evidence passed.

**Keep** an existing ID when its underlying outcome persists through refinement. Every material creation, retirement, redefinition or relationship change still uses the established [first-principles boundary receipt](../../../scripts/check_gap_boundaries.py), with the source links and independent closure proof. A historical issue may stay closed without proving the broader gap.

## Closure evidence contract

For a proposed gap, a reviewer should be able to answer the following without inferring the result from the implementation:

- **Positive:** a real person or supported agent follows a named creator/contributor journey, obtains the claimed editable/durable/reusable/observable result, and its essential boundary survives restart, repetition, collaboration or transfer *when relevant*.
- **Negative:** one or more realistic adverse cases (failure, interruption, invalid authority, unavailable input, stale state, unexpected version) produce the documented safe failure/recovery behavior rather than falsely appearing successful.
- **Provenance:** source revision/contract, platform/environment, version and test identity or product evidence, actual result and limits. A prior release pin is historical evidence, not proof of the current candidate.
- **Independence:** explain what can remain unfinished in adjacent gaps while this one closes.
- **Falsifiability:** name a concrete observation which would overturn a “Closed” claim.

This is not a mandate to run expensive GPU or product tests during gap-definition work. GD-2 designs the evidence criteria; later projects or releases supply their own authorized proof.

## Calibration examples (not holdout verdicts)

These examples deliberately do **not** predetermine the full-catalogue outcome. Each is from the [GD-3 proposed calibration pool](calibration-2026-11-20.md); GD-4 must challenge them against full sources and independent classifications.

| Example | Tentative application of the tests | Nearest alternative / unresolved boundary |
| --- | --- | --- |
| [#966](https://github.com/banodoco/astrid-dev/issues/966) saved indicator and an unpublished draft, [#842](https://github.com/banodoco/astrid-dev/issues/842) old timeline edit refusal | Evidence for a meaningful outcome such as reliably preserving and revising existing creative work, **not** a gap titled “fix save race” | Compare against F-002 ownership and F-003 general creative execution; separate persistence, authorization and historic-compatibility causes before deciding whether there is one independent outcome |
| [#890](https://github.com/banodoco/astrid-dev/issues/890) H3 audio/video references | Missing source-control possibilities may be evidence of creator-directed multimodal generation; a particular H3 input key is a technical implementation, not a gap | Compare with F-003 and model-independent control outcomes. One provider's lack of support is insufficient to assert all Astrid modes fail |
| [#644](https://github.com/banodoco/astrid-dev/issues/644) newline-wrapped base64 in reviewer intake | Usually a focused contributor-workflow bug. A successful fix belongs to its issue/PR, not automatically a new gap | It may inform the *current state* of a broader parallel-contribution/review outcome only if the pattern materially blocks it |
| [#907](https://github.com/banodoco/astrid-dev/issues/907) duration-dependent speed-meter false positive | An inaccurate gate is not evidence that real user latency exceeds the agreed threshold | Fix the measurement or investigate further; compare user-visible latency data before changing a speed-related gap |
| [CA-002](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/vision/gaps/CA-002-contributor-ownership.md) contributor ownership | A meaningful long-horizon contributor outcome can be a legitimate gap despite few issue reports | Require its own concrete legal/governance/participant evidence; do not make issue volume an eligibility condition |
| [Plan 55](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/55-local-speed/plan.md) local speed, [Plan 39](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/plans/39-green-mains/plan.md) green mains | A project is an independently useful delivery route, not itself a gap by default | Ask whether speed/reliability is genuinely a distinct missing user outcome versus a subpart of an existing gap, and whether its closure is individually provable |

## Why v1 differs from the evaluated v0

This amendment is **based on the two CAL evaluations**, not on HOLD results. The first-pass manager assessment was merged in [PR #1097](https://github.com/banodoco/astrid-dev/pull/1097), the separately authored second source assessment and comparison in [PR #1100](https://github.com/banodoco/astrid-dev/pull/1100). The second author's CAL verdicts were committed at `1e7c18b572c6424ba89dd085b31ed11c47067290` before they read the manager's first pass; the comparison is at merge `cfa8d3db3374988e8ceb97efafaa314ace03e5a2`. The two assessments are calibration evidence, **not** independent RS1 approval. No new gap is proposed or auto-created here.

| Tested ambiguity | v1 decision rule / explicit counterexample | What still needs a reviewer |
| --- | --- | --- |
| **Only evidence is absent** | First request a named discriminating check or honestly mark `Needs recheck` on the nearest existing outcome. Lack of a test alone does not establish a missing capability. **Counterexample:** CAL-07's false speed meter proves only a meter failure, not slow creative work. | Can one legitimately identify a necessary gap top-down without issue reports (e.g., CA-002) while avoiding arbitrary test-status gaps? |
| **One goal, two genuine outcomes** | Do not merge automatically when two outcomes share a goal or provider. **Counterexample:** F-005 local-authoritative delegated execution and F-006 hosted-authoritative durable workspace have different independent positive/negative custody proof. | Can each gap close while the other remains observably open? Does the rubric reject an artificial split by API or cloud provider? |
| **Many causes, possibly one recipient result** | Never create gaps by counting issues or shared implementation causes. **Counterexample:** CAL-01 save publication and CAL-02 historical-validator refusals differ technically; they may both prevent *durable revision*, but only independent creator closure can decide. | Which named goal best anchors the outcome? Can revision durability close without closing AA-001/F-002/F-003? |
| **Creative controls below the north star** | Small artistic outcomes can merit gaps if a real creator journey is valuable, closes independently, and differs from existing F-003/AA-001/LS-004 proof. **Counterexamples:** CAL-04 controlled identity/voice references and CAL-12 named reusable retime-safe spatial regions. | Are these distinct source-supported outcomes, a shared missing creative-direction capability, or useful feature/project steps rather than gaps? |
| **Local responsiveness versus portability** | A per-interval meter failure alone is a measurement issue (CAL-07). **A measured creator latency shortfall**, if independently actionable and closeable, may justify a separate responsive-iteration outcome rather than expanding F-008 by technology association (CAL-16). | No user-observed latency suite has yet been qualified as the defining baseline, so do not assert or create this candidate. |

**Version/holdout discipline:** v0 was tested by two author-separated CAL case passes. This v1 is a **new proposal**, not retroactively “the version that passed” those evaluations. A qualified independent reviewer should first challenge v1 on the existing source-linked CAL cases, record accepted/rejected differences and a clearly pinned v1 SHA, **then** recommend the exact frozen rubric commit SHA for a possible once-only test of the preselected HOLD-01–10. The accountable manager must verify the exact freeze, independent review and remaining run-level review authority, then obtain separate run-level authorization identifying the frozen SHA and designated evaluator **before** that evaluator may open any holdout source. **Without that authorization, HOLD-01–10 remain sealed and may not be opened or classified.** With valid authorization for that exact SHA, only the designated evaluator may conduct the single controlled holdout assessment; a failed holdout remains evidence against the version actually tested and may not be reused to qualify a revision. Opening or tuning to HOLD evidence before that review would corrupt the intended holdout. If v1 fails, preserve that failure and draw a new unseen holdout for a later version. Neither GD-4, RS1 nor GD-5 is complete at this point.

## Reviewer protocol for GD-4 and RS1

- Two independent evaluations should each record **candidate type**, **goal**, **closest existing gap**, **why this level**, **disposition**, **positive/negative closure idea**, **evidence strength** and **uncertainty** for the same calibration cases. Do not simply ask a reviewer whether this draft “looks good.”
- Record actual disagreement by case and field, not only percentage agreement; resolve substantive conflicts by checking the original issue and vision source, not by majority vote or editing the source to fit the rubric.
- Freeze this draft's exact commit **before** opening the ten preselected holdout sources from [GD-3](calibration-2026-11-20.md). An unseen holdout verdict is never prefilled from this document. If the holdout reveals a substantive weakness, record failure of the exact frozen version **actually tested** (v1 for this proposal, not the earlier CAL-tested v0), retain the adverse verdict, and use a new untouched holdout for any revised version; never re-label the failed holdout as training success.
- An independent reviewer must challenge the five tests for excessive fragmentation, too-broad “north star” outcomes, technology-specific names, missing governance/privacy effects and ambiguous closure. Authors cannot certify their own independent review.
- A completed RS1 and the owner's explicit acceptance at GD-5 are separate gates. This draft, a passing Markdown check and a manager's agreement do not satisfy either.

## Known limits and placement decision

The existing [individual Gap workstream](https://github.com/banodoco/astrid-dev/blob/4b3e3841af3921d9846389a4cd744f027c1db0b3/skills/shared/workstreams/astrid-dev-gap/SKILL.md) and template remain the intended canonical consumers; no `astrid-dev-gap-review` skill, scheduler or recurring review state is introduced. The **Plan 73** Markdown-first skills migration has active writers to the workstream's eventual `agent/shared/workstreams/gap.md` home, while **Plan 53** has an open Goals source/consumer migration. Do not edit either owner's shared files from GD-2 until their accepted contracts land or ownership is explicitly coordinated. Keeping this draft under Plan 71 evidence avoids overlapping writes; its acceptance must later be reflected in the *canonical* authoring rule, with only links elsewhere.

**GD-2 progress:** a substantive draft exists for test and review. It is **not yet marked complete**: independent calibration/review and any resulting canonical placement decision are still pending, so no unverified completion checkmark is warranted.
