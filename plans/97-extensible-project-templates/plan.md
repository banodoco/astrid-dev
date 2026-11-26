# Extensible project templates

> **Cancelled on 24 November 2026: absorbed into [Plan 95](../95-composable-agentic-workspaces/plan.md).** The owner chose to build the template seam once, in Otto, instead of in astrid-dev first and then extracting it ([Plan 95 inputs](../95-composable-agentic-workspaces/inputs.md#owner-direction-24-november-2026)). Plan 95's OT-11 and OT-12 carry this design: the `**Template:**` field (absent means `standard`), `template.toml` manifests, `standard` and `loop`, and a third template with no code change. Only real loop plans opt in. Everything below is kept as history; dispatch nothing from it.

**Project:** Extensible project templates

**Goal:** A person or agent chooses a project template that supplies its extra documents and execution workstream, and can introduce a new template without changing the common project machinery.

**Status:** cancelled

**Owner:** Unassigned

**Estimate:** None; cancelled.

**Waiting on:** —

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six fields above define the catalog row. Leave [priority](../priority.md), release membership and run authority unchanged until separately decided.

**Vision role:** Foundational enabler — formalises the existing project execution variants for later reuse by Otto; no claim of CA-005 concurrent-contributor closure.

## Outcome and scope

One project entity, one identity/status/owner/task list and one common pack. Standard and loop are templates for the same entity, not separate record types, pipelines, statuses or duplicate implementations. A standard project has a defined outcome and broadly known tasks; a loop project has a defined outcome but discovers the next work from evidence. An ordinary project may include a bounded iterative task without choosing the loop template.

Retain Plan 48's existing template-as-declaration principle. Keep the common plan, inputs and tasks Markdown templates in one home; a discoverable flat type directory supplies a small manifest (proposed template.toml), extra Markdown templates and a reference to a valid authored execution workstream. One canonical header field (proposed **Template:** standard or loop) selects it. A common parser reads that field once, and pack validation selects the common requirements plus the type-specific files, headings and any minimal additional structural requirement. A template can be added through local documents and metadata, without modifying validator code for ordinary cases; unusual semantic checks use the existing check registry. No template inheritance hierarchy, DSL, registry duplicated from directories, project state machine or new orchestration service.

**Standard:** common three-document pack, existing task and acceptance procedure. **Loop:** common pack plus round-history document and an explicit reference to one standing loop task in the same task list (use the project's actual stable task ID, not a required magic name). Define baseline or its setup task, comparable measurement method, how evidence selects next tasks, success/stop/escalation conditions, and append-only round receipts/decisions with links to new ordinary task rows. Keep goal and completion in the common record. Plan 77's two successful rounds and Plan 89's marginal-benefit/freeze stop are examples of local rules, not a universal hardcoded stop count. Actual loop procedure remains with the live-loop workstream; extract only common structure. A draft may legitimately have a pending baseline and no rounds; readiness needs an executable measurement/stop method, completion needs real evidence and a recorded disposition under the agreed rule. Do not manufacture a successful round or mark a project done merely because the loop stopped.

Extend current pack-shape/check machinery, not a second validator. Validate newly created packs and explicitly migrated packs when their template-sensitive files or template declaration change; when a template changes, check affected adopters or require an explicit compatible migration. Preserve existing pre-adoption grandfathering and current planning/completion gates, but reject removal of a required document, unapproved template switching or deleting the declaration as a bypass. Template discovery rejects missing/unknown/duplicate IDs, broken workstream references, unsafe paths and conflicting definitions. Generation/check output is deterministic and must not mutate authored records. The same selected template drives scaffolding/author guidance and validation.

**Migration:** inventory all existing canonical project records, identify actual execution mode rather than searching for the word loop (Plan 77 is explicit; Plan 89 uses a measure-and-fund loop without that field; Plans 87/88 contain live loops but require human disposition). Use one explicit classification and evidence for each. Preserve existing task IDs, scope, evidence, status, ownership and live run policy. Add declaration and genuinely needed loop records at an owner-approved boundary; historical rounds stay truthful, link existing evidence instead of fabricating or duplicating it. Where a live run cannot safely adopt new rules, keep its pinned instructions and defer that record's adoption until authorized handoff; do not silently reclassify. Record exceptions and finish the agreed migration before completion. Do not rename project paths in this plan: that is [Plan 98](../98-project-identity-and-vocabulary/plan.md).

**Out of scope:** Otto extraction, campaign/release changes, new project types beyond standard/loop in production, compulsory new project packs for simple issues, auto-execution, universal stop rules, a global rewrite of existing project acceptance criteria.

## Existing work and decision

[Plan 48](../48-one-record-model/plan.md) completed the common record and pack-shape mechanism. [pack_shape.py](../../scripts/pack_shape.py) reads the current three templates but assumes one shape and checks new packs only. [document_structure.py](https://github.com/banodoco/otto/blob/223086a92e9ce0dc8c01d02278f84b08330df243/otto/markdown.py) already parses real headings/frontmatter. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) explicitly declares a loop, uses a standing task and [rounds](../77-saving-holds-on-a-heavy-timeline/rounds.md); [Plan 89](../89-heavy-saves-in-seconds/plan.md) uses a different stop policy. [Whole project](../../agent/roles/manager/whole-project.md) and [live loop](../../agent/roles/manager/live-loop.md) already define the execution alternatives. Keep their substance; Plan 73 will move the source paths. The owner chose the direction on 24 Nov: projects use different templates, but remain one entity. See [inputs](inputs.md#planning-evidence) for open details and independent critique requirement.

## Sequence and readiness

After Plans 71–73 land, inventory all project records, exact test baseline, final Markdown agent layout and execution rules. Review a minimal common/type contract (RS1). Implement discovery/selection, extend existing shape checks and scaffold/route from the same source, formalise standard and loop, then migrate the classified existing records at the approved boundary. Prove a third template in a temporary workspace (not a new mandatory production type); final review and separately approved integration. Design for the path migration in Plan 98 but do not perform it here. [Tasks](tasks.md).

## Interfaces and handoff

**Consumes:** accepted Plan 48 pack-shape, checks, templates and project metadata; final Plan 73 authored workstreams; final Plan 71/72/53 contracts at exact recorded revisions.

**Produces:** one common template and discoverable standard/loop extensions, one selection parser, existing-validator extension, source-owned routing/authoring guidance, classification and migration evidence, exact tests and extension example. Handoff to [Plan 98](../98-project-identity-and-vocabulary/plan.md) for naming/path migration and [Plan 95](../95-composable-agentic-workspaces/plan.md) for extraction into Otto, with the actual API and no speculative generic infrastructure.

## Completion

1. New standard and loop packs both validate through the same command and catalog; selected workstream is discoverable in native and source-only agent paths. Existing scope, evidence, ownership, lifecycle, tasks and reviews remain one source.
2. Missing loop document/standing task/stop method, broken reference, unknown/duplicate template, path escape, declaration in a fenced example, unapproved template switch/removal, and template edit that invalidates an adopted pack fail at the appropriate gate; standard does not require loop files. Draft/no baseline is allowed, false completion is not.
3. Existing project inventory is classified and adopted under the agreed migration boundary, with no rewritten historical receipts, lost task IDs or active-run surprise. Preserve all legacy negative/positive checks not deliberately reviewed.
4. A fresh agent creates a research template with an extra findings document and workstream in a fixture; discovery, scaffold and validation work with no core code change, and removal or malformed additions fail appropriately. No third production template required.
5. Native focused and full existing docs/consumer CI on exact candidate; independent final review accepts minimality and negative evidence.
