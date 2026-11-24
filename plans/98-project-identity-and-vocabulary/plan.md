# One project vocabulary and identity

**Project:** One project vocabulary and identity

**Goal:** A contributor or agent encounters one canonical project concept and path, with stable identities, intact release and issue relationships and truthful historical evidence.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 3–6 engineering days provisional; re-estimate after inventory of active references, external URLs, generated feeds and protected CI.

**Waiting on:** [Plan 97](../97-extensible-project-templates/plan.md) accepted and integrated; Plans 71–73 and goal contract handed off; owner-approved safe migration window and independent critique; named manager.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six fields above define the catalog row. Leave [priority](../priority.md), release membership and run authority unchanged until separately decided.

**Vision role:** Foundational enabler — removes duplicate plan/project terminology and isolates Dev-specific identity conventions before extraction to Otto.

## Outcome and scope

Call the unit of work a **project** everywhere in new authored structure. A plan is an approach within a project, not a second entity. Preserve the project's numeric identity in Astrid Dev (Project 77 stays 77); remove the shared machinery's assumption that every workspace must use numbered folders. Marketing may use stable slugs. Title changes do not change identity. Preserve current project data, classifications and template selections.

Proposed Dev canonical paths: projects/<NN-slug>/project.md, inputs.md, tasks.md and existing supporting docs; common authoring template project.md, project catalog/priority, project links in new release briefs and skills. Keep existing GitHub repository name and all stable numeric IDs. Consolidate the resolver used by readers, checks, labels, branch and release membership, paths and views; don't add an ID database or infer identity from display title. Make an explicit per-workspace identity/path policy that Otto can later accept without rewriting this migration. Do not introduce a permanent second authoritative directory or separate plan entity.

**Migration boundary and scope:** inventory every consumer on the actual integrated tree, including project/goal/gap relationships, project catalog, release briefs, strategy, public feed schema, planning/pack-shape/completion/boundary tests, claim/review/intake/auto-merge scripts and workflows, role/workstream references, tool paths, CI required check names, active run/mailbox instructions, .otto state location and pinned receipts. Update new authored paths and names coherently with the parser/check/automation cutover; do not change the protected workflow trust model or bypass. Preserve old branch names, issue IDs, published release records and exact historical evidence at original revisions. Do not rename live branches or mutate live state in place. Pin old-source links when they are historical; use bounded, documented read-only compatibility for existing old release links, label aliases or externally published URLs where necessary. Keep public wire schema and stable IDs compatible; explicitly enumerate allowed path/link-only output deltas rather than demand byte identity after intentional moves. Never silently rewrite a finalized release or interpret a renamed file as a new project.

A transition strategy may keep read-only support for old plan:NN labels and active run references while new authored references use project:NN; migrate labels only with explicit scope and proof, not by bulk API mutation from this plan. Choose whether externally used old main paths need generated link-only redirects or pinned links after evidence; no alias becomes another editable source. New Marketing workspaces need no numeric label/branch compatibility burden.

**Out of scope:** renumbering projects, rebasing or renaming historical branches, changing product release authority, modifying accepted tasks/goal or status, rewriting historical receipts, changing product code except an explicitly authorized consumer-compatibility adjustment if genuinely unavoidable, generic workflow engine or Otto package extraction. If existing App consumer needs a behavior change, isolate and obtain its owner decision rather than silently break its contract.

## Existing work and decision

[Glossary](../../skills/shared/glossary.md) equates plan and project; [project-format](../../docs/project-format.md) and [Plan 48](../48-one-record-model/plan.md) already treat the project as the record. [project_contract.py](../../scripts/project_contract.py), [records.py](../../scripts/records.py), release/issue scripts and [docs CI](../../.github/workflows/docs.yml) embed current paths, regexes and consumer assumptions. Plan 51's one-word/one-home principle supports the rename. Plan 97 formalises templates before this mechanical migration. Plan 72's graph, Plan 73's agent paths, Plan 52 issue intake, Plan 53 Goals and Plans 31/58 release/strategy are domain owners, not things to rewrite as part of a rename. See [inputs](inputs.md#planning-evidence).

## Sequence and readiness

Inventory actual source and cross-repo readers, active writers and historical refs. RS1 accepts ID/path resolution and rollback/cutover strategy before moving records. Implement the canonical resolver and compatibility read boundary; stage consumer updates and authored moves together or in a reviewed compatible sequence. Rehearse full migration and rollback on an isolated candidate; land at owner-approved safe boundary only after native docs, public consumer and protected automation proofs. No new framework distribution until the migration handoff is accepted. [Tasks](tasks.md).

## Interfaces and handoff

**Consumes:** accepted Plan 97 template system, Plans 48/71–73/53 current contracts, actual Dev records, App consumer schema and GitHub routing/permissions at named revisions.

**Produces:** canonical project vocabulary and source path, stable identity resolver with explicit local convention, migrated authored active records and templates, consumer/compatibility mapping and exact parity proof. Plan 95 uses this as Otto's first consumer and does not repeat the rename. Existing external/legacy cases and removal conditions are documented with tested fixtures; no second source of project facts.

## Completion

1. A new Dev project is authored, discovered, displayed and linked as one project at the canonical path, with the same numeric identity rules and selected template as before. Existing canonical records map one-to-one; no status, owner, task or relationship changes merely due to rename.
2. Old historical links and finalized release/issue records remain accurate; any needed old URL/label compatibility resolves read-only to the canonical identity without duplicate enumeration. Stable IDs and public feed schema/consumer behavior hold; enumerate approved link/text changes.
3. New authoring, catalog, completion, gap routes, release membership, issue intake and privileged workflows work through the new resolver. Tests cover old/new references, ambiguous/colliding IDs, unknown IDs, path traversal, duplicate facts, rename vs new pack, unapproved privileged action; preserve existing negative oracles and required check names.
4. Active runs and published release records remain pinned; no unapproved branch/label/state mutation. Rehearse rollback; record actual source/base/candidate and CI proof, including App vision consumer. Independent review accepts a single authoritative structure and bounded compatibility, not two parallel systems.
