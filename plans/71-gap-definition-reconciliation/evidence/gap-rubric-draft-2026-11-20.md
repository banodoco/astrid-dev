# GD-2 — Candidate standard for an Astrid vision gap

**Status:** Draft for calibration and independent RS1 review; **not** an accepted change to Astrid's canonical gap definition.
**Source snapshot:** `banodoco/astrid-dev` `main` `4b3e3841af3921d9846389a4cd744f027c1db0b3`, read 20 November 2026; [GD-1 source audit](../inputs.md#gd-1--source-and-authority-audit-20-november-2026).
**Future canonical home:** [Define or reassess a vision gap](../../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap), consumed by the existing [Gap workstream](../../../skills/shared/workstreams/astrid-dev-gap/SKILL.md) and [gap template](../../../templates/gap.md). This draft does not create a competing policy, a new record type or a workstream.

## Definition

A **vision gap** is an independently assessable *missing, unreliable, or materially unproven outcome* needed to reach one specific authored Astrid **vision goal**, supported by dated evidence of today's capability and framed so that a different implementation could close it.

It states the distance between an aspirational outcome and demonstrated reality, **not** a planned solution. It must be relevant to creators or contributors, bounded enough to have its own positive and negative closure proof, and meaningfully distinct from its closest existing gaps.

A material lack of evidence is **not evidence of absence**. Call the observed capability *unverified* and say which test or journey would settle it; create or expand a gap only if a distinct, necessary outcome remains unresolved after comparing existing boundaries. If the proposed outcome is simply “run these tests,” it is normally verification work in a project rather than a new vision gap.

This definition is a **proposed judgment rule**, not a mechanically enforced score. The existing PR boundary gate requires a human-reviewable record, and CI validates structure/links, not the merit of the classification.

## The five boundary questions

A candidate must survive all five questions. If it fails, first consider an existing gap, project, issue or no change; do not force a new gap because an issue is important.

| Test | Question a reviewer must answer | Rejection or correction signal |
| --- | --- | --- |
| 1. Goal anchor | Which **one primary vision goal** is materially prevented or insufficiently evidenced? Do secondary goals explain a *different* relation? | A new broad ambition with no single goal anchor belongs in vision authoring, or is too vague |
| 2. Meaningful outcome | What valuable creator/contributor result would change when this gap closes? | A file name, internal architecture preference, vendor feature or CI refactor alone is a solution/task, not an independently valuable gap |
| 3. Independent closure | What specific positive journey and meaningful failure/refusal show this outcome succeeded, even if nearby gaps stay open? | “Everything works,” “creative work is possible,” or success only after an entire multi-project vision succeeds is too broad; a one-test repair may be too narrow |
| 4. Implementation independence | Would the outcome still matter if the current proposed plan, provider, UI or API implementation were replaced? | “Add model X input key,” “create endpoint Y,” “migrate file Z” should normally live in an issue or project |
| 5. Distinct nearest boundary | What are the closest one to three existing gaps and why can they *not* cover this outcome with a clearer statement or closure item? | Shared closure and the same recipient outcome suggests refining or merging instead of adding; related causes alone do not justify a split |

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

## Reviewer protocol for GD-4 and RS1

- Two independent evaluations should each record **candidate type**, **goal**, **closest existing gap**, **why this level**, **disposition**, **positive/negative closure idea**, **evidence strength** and **uncertainty** for the same calibration cases. Do not simply ask a reviewer whether this draft “looks good.”
- Record actual disagreement by case and field, not only percentage agreement; resolve substantive conflicts by checking the original issue and vision source, not by majority vote or editing the source to fit the rubric.
- Freeze this draft's exact commit **before** opening the ten preselected holdout sources from [GD-3](calibration-2026-11-20.md). An unseen holdout verdict is never prefilled from this document. If the holdout reveals a substantive weakness, record the failed v0 and produce a new version with a fresh untouched holdout.
- An independent reviewer must challenge the five tests for excessive fragmentation, too-broad “north star” outcomes, technology-specific names, missing governance/privacy effects and ambiguous closure. Authors cannot certify their own independent review.
- A completed RS1 and the owner's explicit acceptance at GD-5 are separate gates. This draft, a passing Markdown check and a manager's agreement do not satisfy either.

## Known limits and placement decision

The existing [individual Gap workstream](../../../skills/shared/workstreams/astrid-dev-gap/SKILL.md) and template remain the intended canonical consumers; no `astrid-dev-gap-review` skill, scheduler or recurring review state is introduced. The **Plan 73** Markdown-first skills migration has active writers to the workstream's eventual `agent/shared/workstreams/gap.md` home, while **Plan 53** has an open Goals source/consumer migration. Do not edit either owner's shared files from GD-2 until their accepted contracts land or ownership is explicitly coordinated. Keeping this draft under Plan 71 evidence avoids overlapping writes; its acceptance must later be reflected in the *canonical* authoring rule, with only links elsewhere.

**GD-2 progress:** a substantive draft exists for test and review. It is **not yet marked complete**: independent calibration/review and any resulting canonical placement decision are still pending, so no unverified completion checkmark is warranted.
