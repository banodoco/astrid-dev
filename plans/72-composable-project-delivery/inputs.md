# Inputs — Composable project-delivery relationships

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 20 November 2026 the requester asked to set up a project for the previously discussed intermediate state: one working project-delivery composition over reusable primitives, with no generic execution engine. This pack records that intent, but no traceable maintainer greenlight or run authorization exists in the repository. Next: owner reviews the scope PR after the independent critique and records acceptance or changes there.

**Prior art:** Inspected against astrid-dev main `6d174521e6f3996349044e393d51b9fa06dbc625` (20 November 2026): [Plan 48](../48-one-record-model/plan.md) delivered the standard-library record helper, check registry and view infrastructure; [Plan 53](../53-vision-aspirations/plan.md) owns goal authoring and gap references, with a further [goal terminology PR](https://github.com/banodoco/astrid-dev/pull/1059) under review; [Plan 44](../44-vision-execution-trail/plan.md) proposes the actual public evidence narrative; [Plan 31](../31-releases-from-astrid-dev/plan.md) owns publishing; [Plan 52](../52-issue-intake/plan.md) owns GitHub issue intake. Current code: [records.py](../../scripts/records.py), [vision_subject.py](../../scripts/vision_subject.py), [gap_relationships.py](../../scripts/gap_relationships.py), [project_contract.py](../../scripts/project_contract.py), [export_public_vision.py](../../scripts/export_public_vision.py), [checks.py](../../scripts/checks.py), [views.py](../../scripts/views.py) and [check_docs.py](../../scripts/check_docs.py). `scripts/relationships.py` did not exist at that source. This is targeted source reading, not a comprehensive call-site inventory; PD-0 rechecks the live base.

**Approach:** Proposed — keep current files and domain rules as canonical, add only a standard-library typed-reference/link foundation and one concrete delivery composition, and consolidate repeated relationship interpretation after proving behavior. Alternatives: (a) do nothing, leaving scattered interpretations and no reusable traversal; (b) extend only each existing domain parser, cheapest now but still without a shared cross-domain representation; (c) build a universal pipeline engine, graph store or YAML DSL, rejected as speculation with no second real execution consumer; (d) fold everything into `records.py`, rejected provisionally because parsing and cross-domain relationship semantics have different responsibilities. The independent critique must challenge whether the new module and separate composition file each earn their existence.

**Challenge:** Pending — this changes astrid-dev's shared checks and exported data interpretation, so the [plan workstream](../../agent/shared/workstreams/plan.md) requires a fresh independent high-judgment critique against the code before greenlight. Next: obtain critique covering whether existing readers already suffice; exact record identity and provenance; goals-versus-aspirations alias; issue authority; which consumers to leave alone; regression cost and deletion opportunities, then record blocking findings and accepted cuts here. The planner's own review is not a substitute.

**Proof and limits:** Same fixed-SHA public feed bytes, unchanged primary classifications, preserved old checks/negative cases, one connected real/fixture delivery traversal and one distinct frozen issue-to-release traversal with unknown/refusal controls. No claim of real multi-contributor scale, actual gap closure, new delivery UI, comprehensive evidence indexing, release publication or automatic action. Native source/code proof is required at the integrated head; planning cannot supply it.

**Review rounds:** Pending — recommend **RS1 one independent review of the typed contract and adapted reader boundary** before checker/view migrations (late changes would require widespread rework), and **R one independent final integrated review** before completion. Each recommended review has one round with blocking findings made into task rows. Next: owner confirms the count at run start; review is not waived by CI.

**Run start:** Pending — planning only; no implementation, release, publication or reviewer identity was authorized. Next: owner chooses the accountable session, authorized scope, release/destination and exact current base; record those with model routes and reviewer before dispatch.

## Owner decisions

- **D1 — distinct project or extend Plan 48/44?** Recommend a new foundational-enabler project: Plan 48 is completed and has a different record/check/view outcome; Plan 44 owns a public evidence trail, not the internal reusable relationship mechanism. Alternative: extend Plan 44 and risk binding its public UX delivery to a new internal contract. **Pending:** scope PR acceptance.
- **D2 — actual shared primitive contract?** Recommend a minimal immutable `RecordRef(type, id)` and `Relationship(source, kind, target)` plus provenance and deterministic queries, retaining domain rules in their reader. Alternative: an even smaller function-only adapter if critique shows it suffices. Do not freeze exact public API names from a chat sketch. **Pending:** RS1 design decision following independent critique.
- **D3 — scope of the second path and evidence?** Recommend frozen, locally authored release issue membership only as the read-only reuse proof; no live GitHub queries, new evidence envelope, inferred shipment or Plan 44 implementation. **Pending:** scope PR acceptance.
- **D4 — catalog priority and release?** Recommend leaving the new plan absent from `plans/priority.md`, `queued` and `Unassigned` until separately owned and scheduled, and leaving all release briefs unchanged. **Pending:** owner prioritization and execution authorization.
- **D5 — review gates?** Recommend one RS1 contract stop and one integrated R, each one round. **Pending:** owner confirmation on run start.

## Source identities

**Planning source:** `banodoco/astrid-dev` `main` at `6d174521e6f3996349044e393d51b9fa06dbc625`, inspected 20 November 2026. Relevant other work includes [PR 1059](https://github.com/banodoco/astrid-dev/pull/1059); do not assume its result is installed or accepted.

**Execution source:** Pending — before any code work, re-read live main, check other writers touching the same scripts, pin exact base/donor SHA, active review and release destination. For a Release 14+ implementation the owner's selected `release/<NN>/main` is the source of `release/<NN>/plan-72`, per the [release workflow](../../agent/shared/workstreams/release.md). This scope PR targets `main` for planning only; it is not an implementation branch.

## References

[Project templates](../../templates/project/) · [Plan skill](../../agent/shared/workstreams/plan.md) · [Contribution principles](../../docs/contribution-design-principles.md) · [Extending astrid-dev](../../docs/extending.md) · [CA-003](../../vision/gaps/CA-003-vision-experiments-progress.md) · [CA-005](../../vision/gaps/CA-005-parallel-contribution.md).

The requester asked for this pack directly in a 20 November 2026 planning conversation. That conversation is not used as a GitHub approval record; the scope PR is the explicit review/decision boundary.
