# GD-5 — Owner decision brief (prepared, not decided)

**Decision status:** `NOT READY / OWNER DECISION PENDING`. This is the concrete decision the owner will be asked to make *after* a qualified independent RS1 review and the guarded HOLD-01–10 evaluation. Preparing it now does not satisfy GD-5 or authorize GD-6, changes to gap records, Plans 53/73, or a final project merge.

## Exact proposal to decide

**Version to prepare for decision:** [GD-2 v1 candidate on PR #1102](https://github.com/banodoco/astrid-dev/pull/1102), last verified observed HEAD `04573347bfc1f5d34df7c18e39b4c4c97878f5e8`, rubric blob `ee8889bc8c8e07ffe0156960f47703d775b1f3b9`. This corrects an **earlier stale PR-head pin**: the original content commit `6c1eca653659bd765a99cd810c33410b0a0622d5` and escrow-integrated head `958422a1e3af2ae868d439519bb5ebe0f3956360` both contained **identical** rubric blob `5e5dd8877defac45579ac261bfd4b43d493e8b63`; the newer `04573347…` changes only the holdout failure/version sentence, not the rubric's five boundary tests. **The final owner decision must name the exact *reviewed* head and content blob as reverified at decision time**, never simply “v1.” Original v0 remains at `e03d09caf7ff84f2361de7b92eee9a00621bc3b5`. See the [RS1 reviewer packet](rs1-exact-head-review-packet-2026-11-21.md) and source escrow, GD-4 CAL source comparison, and any actual holdout verdicts once legitimately obtained.

**Proposed principle:** A gap is a meaningful, independently assessable shortfall from **one primary vision goal** in a creator/contributor outcome, substantiated by dated observations of missing or unreliable capability and separated from an issue, implementation plan, technology choice or release gate. An unverified capability triggers honest `Needs recheck` and a specific discriminating proof request, **not** automatically a new gap. A legitimate new gap has a distinct recipient/outcome, nearest-boundary analysis and positive/negative closure evidence that can succeed while neighboring gaps remain open. Two gaps may share one goal when data custody or other independent user journeys differ (e.g. F-005 vs F-006).

**Do not silently accept:** the two GD-4 evaluations broadly agree in their immediate decisions but do **not** settle whether durability/revision, source-directed creative controls, reusable spatial regions or measured local responsiveness merit independent gap boundaries. A frozen rubric alone cannot claim these candidates belong in the revised catalogue.

**Review decision is not yet ready:** the source escrow was supplied for reviewers who cannot reach live GitHub issue bodies, but no qualified independent reviewer has returned a source-grounded verdict on the *current exact candidate*. The supplementary observation about stale SHA and the v0/v1 typo is useful editorial evidence, **not RS1 clearance or a holdout classification**. Preserve GD-5 as `NOT READY` until native CI, independent review and authorized guarded holdout proof are obtained; separately preserve GD-9 as owner-controlled after later full-corpus reconciliation.

## Required evidence before asking for approval

| Gate | Present proof | What is still missing |
| --- | --- | --- |
| Authored draft | v0 and v1 linked to exact commits; v1 docs + vision-consumer + review-intake CI green | The final reviewed wording after findings, if any |
| Source examples | 16 CAL issue/goal/gap/project cases, two separately authored assessments, documented comparison | A qualified independent RS1 challenge of the exact version and each unresolved substantive boundary |
| Holdout integrity | Ten preselected HOLD IDs sealed and not classified | One authorized, source-custodied evaluation after a reviewer-accepted freeze; log failing and passing cases without tuning to them |
| Canonical home and owner | Existing individual Gap skill/template, contribution workflow, first-principles boundary check identified by GD-1 | Confirm current landed Plan 53 Goals schema and Plan 73 Markdown-first skill path; agree one canonical destination, not a duplicate rule |
| Reviewer provenance | Explicit request on PR #1102; no completed review falsely asserted | Distinct qualified reviewer with authored verdict, sources/commit identity and resolved blockers |

## Owner choices — request only when the gates above are met

1. **Accept the exact independently reviewed definition** at a new final SHA, subject to any recorded limits. This authorizes **GD-6's read-only full gap/project/issue baseline census and GD-7/8's proposed catalogue**, not immediate creation/retirement of gap IDs or an approved migration.
2. **Require another bounded revision/holdout proof.** Name the specific boundary or negative evidence missing, return to GD-2/GD-4 and preserve the failed version's original outcome; do not replay the same holdout as an unseen test.
3. **Reject the approach or change the abstraction.** Record which basic premise is wrong (e.g., the necessity of one primary goal or independence test), update the accepted plan scope through the usual review process, and do not run GD-6 under an unaccepted definition.

**Provisional manager recommendation:** only *conditional option 1* if RS1 and held-out evidence confirm a coherent distinction between missing/user-unreliable capability, merely unverified implementation and an isolated issue. The project should prefer `keep or refine` over new gaps until the complete issue/project corpus justifies a separate user outcome. This is advice, not the owner's response.

## Consequence of an actual GD-5 acceptance

- Freeze the accepted wording, source SHA, limitations, review-round use and holdout result.
- Align the **one** canonical gap authoring procedure once Plan 53/73 shared-surface ownership allows; do not silently change their active branches.
- Begin GD-6: enumerate every original gap and project at exact revisions plus all relevant issues, open and closed, using complete pagination and honest exclusion reasons.
- Preserve **GD-9** as a second explicit owner decision on the *whole proposed old-to-new catalogue mapping* after GD-7/GD-8 and RS2. GD-5 never grants blanket permission for gap merges, closures, source ID changes, issue relabeling, or product deployment.

## Deferred work

Phases 6–7 are out of the current execution scope. No `astrid-dev-gap-review` workstream, weekly scheduler, bot, recurring index or permanent checkpoint is authorized by any option above.
