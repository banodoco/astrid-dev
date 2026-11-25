# Inputs — Extensible project templates

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Cancelled on 24 November 2026 before any scope was approved: the owner absorbed this plan into [Plan 95](../95-composable-agentic-workspaces/plan.md) as its template seam. Earlier record: the owner selected standard and loop as templates of one project. Next: none here; Plan 95's scope PR carries the template decision.

**Prior art:** [Plan 48](../48-one-record-model/plan.md), [pack_shape.py](../../scripts/pack_shape.py), [test_pack_shape.py](../../scripts/test_pack_shape.py), [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), [its task list](../77-saving-holds-on-a-heavy-timeline/tasks.md) and [Plan 89 task list](../89-heavy-saves-in-seconds/tasks.md) inspected at 83ab5c0ec2842023f9227451fbb0d71adfee428c. Shape currently derives headings, labels and the first task-table header from one pack template; the registry calls it only for new packs. Plan 77 explicitly declares loop; 89 does not. Plan 73 changes workstream paths; consume landed layout.

**Approach:** Extend template-derived shape validation with a tiny local type manifest and additional Markdown files; preserve the common record and check registry. One template selection also routes to the authored procedure. Compare the actual differing loop rules, not a new generic workflow language.

**Challenge:** Pending — This changes shared contracts and checks and needs a fresh high-judgment source-capable reviewer before scope greenlight. Next: challenge the necessity of each addition, removals and migration risks against the actual integrated prerequisite tree; record findings and owner dispositions. This drafting session is not independent review.

**Proof and limits:** Positive/negative fixture tests of both current templates, a fresh third template and migration parity; readiness and completion evidence are distinct. A heading cannot prove a measurement occurred; local review checks the actual receipts. No tests were run during proposal drafting.

**Review rounds:** Pending — Recommend one RS1 after the load-bearing design and one final R, with independent reviewer bindings. Next: owner agrees the review budget; no extra round is automatic.

**Run start:** Pending — Planning only. Next: record owner-authorized run, accountable session, advisor, exact source/destination, permitted actions and limits after prerequisite handoff and scope approval.

### Alternatives and boundary

Copy all three documents into every type (duplicates common rules); subclass project entities (duplicates status, task and graph machinery); embed stop/count logic in a workflow DSL (unneeded and wrong for differing loop policies); use one base plus additive docs/requirements and workstream (recommended). Existing projects already differ in how they run; classification should not treat every reference to iteration as a type. Keep task IDs, proof and review semantics intact.

The [planning rule](../../agent/shared/workstreams/plan.md) and [glossary](../../agent/shared/glossary.md) already distinguish loop projects. New type-specific semantics belong in local workstreams/checks rather than extra fields in the shared record. A new template need not define its own lifecycle. Proposed type filenames, manifest syntax and route selection are subject to RS1; no decision requires a new external dependency.

## Owner decisions

- **D1 (direction selected, 24 Nov):** standard and loop are templates of one project; addition should be discoverable without core code.
- **D2 (open):** canonical Template field, manifest and extra-file/standing-task reference contract; prefer one additive template level and existing Markdown parser.
- **D3 (open):** migration timing and treatment of active/archived projects, explicit legacy classification and template-change approval. Recommend finish at safe handoff, preserve run pins and receipts.
- **D4 (open):** review budget and dev-only execution authority; settle with critique.

## Source identities

Planning snapshot: banodoco/astrid-dev main 83ab5c0ec2842023f9227451fbb0d71adfee428c (24 November 2026). Prior proposal [PR #1868, original head 6f1dfd829d21103b477da8ad12add8f49cbcb3e3](https://github.com/banodoco/astrid-dev/tree/6f1dfd829d21103b477da8ad12add8f49cbcb3e3) is planning history, not execution authority. At dispatch record final accepted prerequisite commits, actual overlapping writers, base/ref/dirty state, destination, protected CI and named run authority. Re-read moved paths after Plan 73. For release-linked work use the authorized release/plan branch route; an astrid-dev-only run requires explicit owner authorization. No new repository, run, merge or release is authorized by this pack.

## References

[Plan 48](../48-one-record-model/plan.md) · [Plan 51](../51-astrid-dev-clean-up/plan.md) · [Planning skill](../../agent/shared/workstreams/plan.md) · [Run contract](../../agent/shared/run-contract.md) · [Design principles](../../docs/contribution-design-principles.md).
