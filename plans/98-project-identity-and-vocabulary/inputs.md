# Inputs — One project vocabulary and identity

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Owner asked to rename plans to projects and make the common system usable for Marketing; 24 Nov 2026. Next: review canonical path, stable IDs and migration choices; record durable scope approval.

**Prior art:** [Plan 48](../48-one-record-model/plan.md), [Plan 51](../51-astrid-dev-clean-up/plan.md), [glossary](../../skills/shared/glossary.md), [project-format](../../docs/project-format.md), [project_contract.py](../../scripts/project_contract.py), [records.py](../../scripts/records.py), [pack_shape.py](../../scripts/pack_shape.py), [views.py](../../scripts/views.py), [issue_intake.py](../../scripts/issue_intake.py), [release_branches.py](../../scripts/release_branches.py), [docs CI](../../.github/workflows/docs.yml) inspected at 83ab5c0ec2842023f9227451fbb0d71adfee428c. Current path/ID assumptions extend beyond prose; public feed and privileged actions are coupled.

**Approach:** One canonical project path and reader, retain Dev numeric identity and existing historical refs, keep compatibility at a narrow read boundary. Avoid renaming active branches or forcing the same numeric policy on Marketing. Stage and qualify the change separately from Otto extraction.

**Challenge:** Pending — This changes shared contracts and checks and needs a fresh high-judgment source-capable reviewer before scope greenlight. Next: challenge the necessity of each addition, removals and migration risks against the actual integrated prerequisite tree; record findings and owner dispositions. This drafting session is not independent review.

**Proof and limits:** Exact source inventory, mapping, pre/post semantic and negative parity, consumer-contract CI, active-run and rollback rehearsal. External links and legacy records are explicit risks; no guarantee all historical external references can be discovered. No implementation/CI run yet.

**Review rounds:** Pending — Recommend one RS1 after the load-bearing design and one final R, with independent reviewer bindings. Next: owner agrees the review budget; no extra round is automatic.

**Run start:** Pending — Planning only. Next: record owner-authorized run, accountable session, advisor, exact source/destination, permitted actions and limits after prerequisite handoff and scope approval.

### Actual coupling and alternatives

- project_contract.py derives numeric identity from numbered plan folder and recognizes relative gap links. records.py fixes project fields, release plan links and release branch/repository semantics. checks.py, planning/pack-shape/completion/boundary checks and views use paths and IDs; check catalog and golden fixtures are affected.
- release_issues.py, boards.py, release_branches.py, issue/review intake, claim_project.py and auto_merge.py route by plan number/path/label, with security-sensitive trusted-main and ruleset boundaries. Existing branches and frozen issue/release receipts are facts, not rename targets.
- export_public_vision.py and App consumer depend on stable schema and paths; strategy and generated view markers reference current source paths. Record intended diff and keep schema/IDs, not merely cosmetic feed parity.
- Run state in plans/<project>/.otto/runs and instructions in active release packets may reference original paths. Preserve their custody and revision-pinned paths; do not repoint active runs.
- Terminology-only change (lowest cost but leaves confusing path/ID coupling); mass search/replace (unsafe and loses semantics/history); separate source resolver plus one coordinated move (recommended). If external compatibility or active writers make the physical rename unreasonably risky, record the narrower alternative and bring it to the owner rather than silently force it.

Coordinate with Plan 97 (base); Plan 71/72/73/53 (consume accepted results); Plan 52 (issue intake), Plan 31/58 (release/strategy) and Plan 44 (evidence) for current and future source ownership. Recheck actual overlap, choose wait/stack/separate at dispatch; do not demand completion of unrelated future product release work just for naming.

## Owner decisions

- **D1 (direction selected, 24 Nov):** use project as the entity, with plan as ordinary approach; preserve existing project identities. Marketing can use slugs.
- **D2 (open):** approve canonical physical paths and compatibility for old URLs/labels/public consumers. Recommend projects/<existing-id-slug>/project.md, no renumbering, narrow read aliases only as needed.
- **D3 (open):** safe integration boundary, treatment of active state/old branches/finalized records, permissions for any consumer/label migration; recommend no active branch rename or automatic label writes.
- **D4 (open):** review budget and authorized Dev run; re-estimate after inventory.

## Source identities

Planning snapshot: banodoco/astrid-dev main 83ab5c0ec2842023f9227451fbb0d71adfee428c (24 November 2026). Prior proposal [PR #1868, original head 6f1dfd829d21103b477da8ad12add8f49cbcb3e3](https://github.com/banodoco/astrid-dev/tree/6f1dfd829d21103b477da8ad12add8f49cbcb3e3) is planning history, not execution authority. At dispatch record final accepted prerequisite commits, actual overlapping writers, base/ref/dirty state, destination, protected CI and named run authority. Re-read moved paths after Plan 73. For release-linked work use the authorized release/plan branch route; an astrid-dev-only run requires explicit owner authorization. No new repository, run, merge or release is authorized by this pack.

## References

[Plan 48](../48-one-record-model/plan.md) · [Plan 51](../51-astrid-dev-clean-up/plan.md) · [Planning skill](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) · [Run contract](../../skills/shared/run-contract.md) · [Design principles](../../docs/contribution-design-principles.md).
