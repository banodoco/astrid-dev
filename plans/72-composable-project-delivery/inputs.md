# Inputs — Composable project-delivery relationships

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner said to proceed after [scope PR #1064](https://github.com/banodoco/astrid-dev/pull/1064), and approved proceeding with the proposed Release 15 placement on 20 November 2026. This authorizes preparation and the release-scoping PR, **not** a claim that the plan skill’s required independent critique was performed. Next: obtain and record a fresh high-judgment architectural critique, then record the accepted scope decision with a traceable review before an implementation merge.

**Prior art:** Inspected against astrid-dev main `6d174521e6f3996349044e393d51b9fa06dbc625` (20 November 2026): [Plan 48](../48-one-record-model/plan.md) delivered the standard-library record helper, check registry and view infrastructure; [Plan 53](../53-vision-aspirations/plan.md) owns goal authoring and gap references, with a further [goal terminology PR](https://github.com/banodoco/astrid-dev/pull/1059) under review; [Plan 44](../44-vision-execution-trail/plan.md) proposes the actual public evidence narrative; [Plan 31](../31-releases-from-astrid-dev/plan.md) owns publishing; [Plan 52](../52-issue-intake/plan.md) owns GitHub issue intake. Current code: [records.py](../../scripts/records.py), [vision_subject.py](../../scripts/vision_subject.py), [gap_relationships.py](../../scripts/gap_relationships.py), [project_contract.py](../../scripts/project_contract.py), [export_public_vision.py](../../scripts/export_public_vision.py), [checks.py](../../scripts/checks.py), [views.py](../../scripts/views.py) and [check_docs.py](../../scripts/check_docs.py). `scripts/relationships.py` did not exist at that source. This is targeted source reading, not a comprehensive call-site inventory; PD-0 rechecks the live base.

**Approach:** Proposed — keep current files and domain rules as canonical, add only a standard-library typed-reference/link foundation and one concrete delivery composition, and consolidate repeated relationship interpretation after proving behavior. Alternatives: (a) do nothing, leaving scattered interpretations and no reusable traversal; (b) extend only each existing domain parser, cheapest now but still without a shared cross-domain representation; (c) build a universal pipeline engine, graph store or YAML DSL, rejected as speculation with no second real execution consumer; (d) fold everything into `records.py`, rejected provisionally because parsing and cross-domain relationship semantics have different responsibilities. The independent critique must challenge whether the new module and separate composition file each earn their existence.

**Challenge:** Pending — this changes astrid-dev's shared checks and exported data interpretation, so the [plan workstream](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) requires a fresh independent high-judgment critique against the code before greenlight. Next: obtain critique covering whether existing readers already suffice; exact record identity and provenance; goals-versus-aspirations alias; issue authority; which consumers to leave alone; regression cost and deletion opportunities, then record blocking findings and accepted cuts here. The planner's own review is not a substitute.

**Proof and limits:** Same fixed-SHA public feed bytes, unchanged primary classifications, preserved old checks/negative cases, one connected real/fixture delivery traversal and one distinct frozen issue-to-release traversal with unknown/refusal controls. No claim of real multi-contributor scale, actual gap closure, new delivery UI, comprehensive evidence indexing, release publication or automatic action. Native source/code proof is required at the integrated head; planning cannot supply it.

**Review rounds:** Pending — recommend **RS1 one independent review of the typed contract and adapted reader boundary** before checker/view migrations (late changes would require widespread rework), and **R one independent final integrated review** before completion. Each recommended review has one round with blocking findings made into task rows. Next: owner confirms the count at run start; review is not waived by CI.

**Run start:** Pending — planning only; no implementation, release, publication or reviewer identity was authorized. Next: owner chooses the accountable session, authorized scope, release/destination and exact current base; record those with model routes and reviewer before dispatch.

## Owner decisions

- **D1 — distinct project or extend Plan 48/44?** Recommend a new foundational-enabler project: Plan 48 is completed and has a different record/check/view outcome; Plan 44 owns a public evidence trail, not the internal reusable relationship mechanism. Alternative: extend Plan 44 and risk binding its public UX delivery to a new internal contract. **Pending:** scope PR acceptance.
- **D2 — actual shared primitive contract?** Recommend a minimal immutable `RecordRef(type, id)` and `Relationship(source, kind, target)` plus provenance and deterministic queries, retaining domain rules in their reader. Alternative: an even smaller function-only adapter if critique shows it suffices. Do not freeze exact public API names from a chat sketch. **Pending:** RS1 design decision following independent critique.
- **D3 — scope of the second path and evidence?** Recommend frozen, locally authored release issue membership only as the read-only reuse proof; no live GitHub queries, new evidence envelope, inferred shipment or Plan 44 implementation. **Pending:** scope PR acceptance.
- **D4 — catalog priority and release?** Recommend leaving the new plan absent from `plans/priority.md`, `queued` and `Unassigned` until separately owned and scheduled, and leaving all release briefs unchanged. **Decided, 20 November 2026:** the requester gave a go-ahead after Release 15 was proposed. Leave the project out of the priority file and Release 15 publication/merge authority untouched.
- **D5 — review gates?** Recommend one RS1 contract stop and one integrated R, each one round. **Pending:** owner confirmation on run start.

## Source identities

**PD-0 source and CI baseline (20 Nov 2026):** [Exact code/reader ownership and native GitHub Actions receipts](evidence/tests/astrid-dev/4b3e384/summary.md) compare the original pre-candidate `4b3e3841...` main (450/450) with core (456/456), reader (463/463) and guide (463/463) candidates. The current release-scoping merge is `ae9e105d...`; Release 15 integration and independent review remain open. This is evidence from existing runs, not a newly launched or independently reviewed qualification.


**Planning source:** `banodoco/astrid-dev` `main` at `6d174521e6f3996349044e393d51b9fa06dbc625`, inspected 20 November 2026. Relevant other work includes [PR 1059](https://github.com/banodoco/astrid-dev/pull/1059); do not assume its result is installed or accepted.

**Execution source:** Pending — before any code work, re-read live main, check other writers touching the same scripts, pin exact base/donor SHA, active review and release destination. For a Release 14+ implementation the owner's selected `release/<NN>/main` is the source of `release/<NN>/plan-72`, per the [release workflow](../../skills/shared/workstreams/astrid-dev-release/SKILL.md). This scope PR targets `main` for planning only; it is not an implementation branch.

## References

[Project templates](../../templates/project/) · [Plan skill](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) · [Contribution principles](../../docs/contribution-design-principles.md) · [Extending astrid-dev](../../docs/extending.md) · [CA-003](../../vision/gaps/CA-003-vision-experiments-progress.md) · [CA-005](../../vision/gaps/CA-005-parallel-contribution.md).

The requester asked for this pack directly in a 20 November 2026 planning conversation. That conversation is not used as a GitHub approval record; the scope PR is the explicit review/decision boundary.


### 2026-11-20 execution placement

Requested by the owner in this ChatGPT conversation: proceed without another release question. **Chosen destination:** Release 15 (proposed plan row in the release brief), not active Release 14. The Release 15 manager is not named and its `release/15/main` branch was not present at this inspection; therefore **do not invent/cut its release branch on behalf of a nonexistent manager**. Isolated implementation candidate work may be prepared and validated, but can enter `release/15/plan-72` only after Release's branch owner cuts the release branch. For any code work, recheck latest base SHA and sole writer. The independent high-judgment design critique remains pending and will not be claimed as performed by this manager.
