# Composable agentic workspaces

**Project:** Composable agentic workspaces

**Goal:** A person or agent can establish and evolve an independent Markdown-first workspace with its own record types, relationships, roles, skills and views using the same versioned machinery as Astrid Dev, without changing that machinery or another workspace.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Provisionally 10–15 engineering days after Plans 71, 72 and 73 are accepted and landed; phase 1 about 1, phase 2 2–3, phase 3 2–3, phase 4 1–2, phase 5 2–3, phase 6 2–3. Re-estimate against the integrated source and migration inventory; excludes full marketing operations.

**Waiting on:** [Plan 71](../71-gap-definition-reconciliation/plan.md), [Plan 72](../72-composable-project-delivery/plan.md) and [Plan 73](../73-markdown-first-agent-skills/plan.md) accepted and landed; verify the integrated Plan 53 goal contract; independent scope critique, owner decisions, named accountable manager and an authorized integration/cutover boundary.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six fields above define the catalog row; leave [priority](../priority.md) and release membership unchanged until the owner decides.

**Vision role:** Foundational enabler — makes the organisation's existing source-driven coordination and extension mechanisms reusable for a second independently operated workspace; supports CA-005 and CA-003 without satisfying their real concurrent-contributor or public evidence-trail closure criteria.

## Outcome and scope

Make the existing development workspace one consumer of a small shared framework, rather than the definition of the framework. Astrid Dev remains a working organisation with its own records, skills and product rules. A minimal Astrid Marketing workspace is the second, deliberately different real consumer. A blank starting template is also supported. Full operational marketing belongs to [Plan 96](../96-astrid-marketing-organisation/plan.md).

**Three layers, one direction of dependency:** (1) shared versioned standard-library-oriented tooling and a small common operating contract; (2) reusable starting templates (initially the Dev method, minimal Marketing and a blank start); (3) workspace-owned documents, registrations, rules, integrations and data. The framework never imports a particular workspace's business logic except through an explicit trusted registration interface. Templates are initial scaffolds, not ongoing authoritative copies; upgrading the framework does not overwrite authored workspace content. The actual Dev configuration is the reference development template, not a permanent special case. Do not ship Astrid's historical plans, private data or active releases in a reusable template.

**Included:**

- Explicit workspace identity, root, repository, skill namespace, pinned framework identity and registered extensions. Commands resolve the intended workspace or refuse ambiguity; root is not inferred from the installed framework's source directory. A checkout and a GitHub-only agent can both discover the canonical entrypoint and applicable rules.
- Shared Markdown parsing and record discovery/registration. Each workspace owns record kinds, stable identity rules, source paths (including nested headings and externally sourced records where justified), required fields and authoring templates. Prefer existing readers and small Python registrations over a universal schema language. An agent can add a new kind with local code/docs only.
- Generalise Plan 72's typed links, provenance, deterministic traversal, endpoint/role/cardinality validation and duplicate/conflict checks. Move the Dev-specific kinds, primary/supporting and foundational-enabler semantics to Dev's registration. Separate relationship composition (what facts connect), workstreams (how agents act), and record lifecycle (what state changes mean); none automatically grants execution authority. Local and workspace-qualified external references cannot collide; cross-workspace references include repository, exact source/revision and trust/availability limits. Do not silently infer membership, closure or shipment.
- Separate Plan 48's check runner and view engine from local registrations. Common checks cover structural integrity, references, declared output ownership and skill packages; local policy owns allowed states and transition evidence, checks, triggers and projections. Preserve current Dev verdicts and public feed bytes at a fixed source. A valid empty/blank workspace is not mistaken for a broken one; an omitted or failed required registration is never silently a pass. Generated views remain outputs, deterministic and safely bounded to owned paths/regions.
- Generalise Plan 73's Markdown-first compiler/discovery/install: explicit namespace, workspace-aware ownership markers, collision and foreign-link refusal, deterministic packaging and reference resolution, clean retirement of owned entries only, support for both workspaces installed concurrently. Roles and workstreams remain ordinary Markdown, opt in with skill metadata; avoid another manual registry for discovery. Preserve the existing Dev skill identities and GitHub-only source navigation, including pinned historical links.
- Extract only genuinely common operating guidance: scoped authority, accountability, bounded delegation, source and decision provenance, proportionate proof and independent review, recovery and learning. Each workspace controls roles, cadence, routing, workstreams, evidence, review and lifecycle policies; Dev retains release, branch, pin, qualification, CI and product-specific practices. No requirement to create a project pack for a small activity or to run a four-layer hierarchy. Keep instructions readable at the point of action, one home per rule.
- Provide a minimal reproducible bootstrap and version pin (distribution method subject to critique); expose the existing check, view and skill operations via one shared CLI and retain Dev's supported command entrypoints. A framework upgrade and rollback must be explicit and independently selectable by each consumer. Shared guidance is either pinned and accessible or deliberately materialized as generated, provenance-labelled text; no mutable duplicate source. Keep the GitHub-only path usable without a package install.
- Separate trusted read-only validation from privileged automation. Move or retain Dev-specific bots, auto-merge, claim/review intake, vision-feed publication, protected generated writeback, release/GPU steps and qualification in their existing domain. New workspaces default to no publication, paid actions, merge bypass or inherited secrets. Never load untrusted PR extensions under write credentials. Bind authority to workspace, actor, exact approved action and artifact, not merely a skill, status or merged document.
- Prove two independently configured workspaces on the same framework revision and an independent upgrade/rollback trial. The minimal Marketing consumer uses objectives, campaigns, content and results (or a smaller reviewed equivalent), a different lifecycle, a local check/view and Markdown skill; completes a real bounded marketing work item through review and evidence. External publication is not required for framework proof and may occur only under separate authority. A fresh agent adds one new record type, relation, check/view and skill without editing framework or Dev, and both remain usable.

**Not included:** a pipeline DSL or execution/scheduling engine, new hosted agent service, database or graph store, template inheritance/merge engine, central metrics or evidence database, automatic cross-repository synchronization, generalising every product release action, marketing integrations or full campaign strategy, product release publication, rewriting prior evidence, changing unrelated product code, or altering live manager/packet instructions mid-run.

## Existing work and decision

[Plan 48](../48-one-record-model/plan.md) delivered common record helpers, registered checks and generated views. [Plan 71](../71-gap-definition-reconciliation/plan.md) calibrates gap assessment; retain its methodology in the Dev template rather than requiring a gap stage elsewhere. Plan 72 adds a read-only relationship model; its current candidate hardcodes five kinds, relations and project-specific exceptions. Plan 73 adds Markdown-first skill compilation; its candidate hardcodes the Astrid Dev namespace and ownership/discovery layout. [Plan 53](../53-vision-aspirations/plan.md) owns the goal authoring contract and remains a local domain contract. See [inputs](inputs.md#planning-evidence) for exact inspected sources, concrete coupling and alternatives.

The requester selected the direction on 24 November 2026: one foundational plan building on the three prerequisites, plus a separate marketing organisation plan; the pipeline stages and skills may differ and today's Dev configuration is a template. The detailed architecture, repository name, distribution approach and migration boundary remain proposed; no independent critique or implementation go is recorded. Prefer extracting the proven mechanisms and moving registrations over rewriting the system or cloning it.

## Sequence and readiness

1. After the prerequisite plans land, freeze actual source/consumer revisions and Dev baseline, inventory path/identity/authority assumptions and overlap with ongoing work, agree a minimal Marketing example and interface/ownership map. RS1 protects all downstream extraction.
2. Extract workspace discovery, record registrations and the relationship core. Reuse the final Plan 72 rather than preserve an obsolete candidate contract.
3. Extract check/view execution and lifecycle declarations; move Dev registrations, keeping oracles unchanged except expressly reviewed diagnostics. In parallel where interfaces are disjoint, extract compiler/install and bootstrap; split common guidance from local operating procedures.
4. Assemble the shared framework and two fixtures; RS2 protects the live cutover, testing authority, ownership, versioning and negative cases. Migrate Dev at an agreed safe boundary, preserving old active run pins, required checks and deployed feed contract. Bootstrap the minimal Marketing workspace and run a representative work item. Final independent review R and separately authorized integration.
5. Hand off exact revisions, limitations and the operational starting point to Plan 96.

See [tasks](tasks.md) for task scopes, routes and proof. Recheck final prerequisite paths, test names and base choices before dispatch. No framework or marketing repository creation, product testing, release assignment, change to active run instructions or implementation is authorized by this planning pack.

## Interfaces and handoff

**Consumes:** the accepted integrated output of Plans 71–73 and Plan 48, Plan 53's actual integrated goal contract, Dev Markdown/registrations, current documentation and vision-consumer CI, source and authority contracts and the relevant release/issue automation. Capture exact commit SHAs and consumer versions at execution start; candidate revisions in inputs are prior art only.

**Produces:** a versioned common package/CLI and small common operating contract, a Dev starting template stripped of live data, a blank initializer, a minimal Marketing configuration and documented local extension interface. Dev and Marketing each pin the package independently. The design must state exact repository/manifest/extension paths, source and generated ownership, supported host/agent environments and explicit non-support. Source-only agents get an accessible pinned entrypoint; local skill packages are a convenience. No public framework publication is required to establish the contract; separately authorize repository creation, visibility, package release and integration.

**Handoff to [Plan 96](../96-astrid-marketing-organisation/plan.md):** exact accepted framework and Marketing workspace revisions, local record and relationship definitions, extension guide, skill entrypoint, permissions and remaining gaps. No full marketing strategy, real account access or publication authority implied.

## Completion

At exact reviewed candidate revisions, demonstrate:

1. Existing Dev source identities, project classifications, lifecycle/authority rules, plan/release views and fixed-revision public vision output retain their approved semantics; existing golden and negative fixtures retain verdicts, required CI including the App consumer contract passes, and no active run is silently switched. Any intentional migration difference is enumerated, owner-reviewed and proved; historical evidence links preserve actual source revisions.
2. A minimal Marketing workspace has a non-Dev record graph and lifecycle, local check and view, roles/skills, and an actual bounded work item carried through draft, independent review and evidence. No Dev project, gap, release or GPU check is required there. A blank workspace can start without inventing a project.
3. A fresh agent with only the workspace and extension guide registers another marketing record type, relation/cardinality, check or view and Markdown skill. It does not edit framework code, Dev, disable a check or invent a second authoritative store. Removing the new skill retires only the owned package.
4. Dev and Marketing are discoverable by a GitHub-only agent and coexist in one supported local skill environment; install/reinstall is idempotent. Wrong-root, duplicate namespace, foreign skill, path/symlink escape, dangling/missing reference, invalid endpoint/cardinality, stale generated view, failed required registration, unauthorized state transition and unauthorized publishing/privileged extension cases fail clearly without damaging either workspace.
5. One workspace upgrades/rolls back while the other remains pinned and unchanged; an incompatible version refuses or has an explicit reviewed migration. A cross-workspace release reference identifies source and revision, cannot be mistaken for a local record, and unverified source cannot imply shipment. No synchronization service required.
6. Record actual native commands, revision pairs, raw results and limits; prove reuse with the same unchanged core and compare Dev on original and migrated trees. Independent architecture and final review accept that the shared core is smaller than two copied systems. Integration/promotion and any external marketing action are separately authorized.

The proof establishes reuse and isolation, not full marketing effectiveness, universal portability, gap closure, or arbitrary agent execution safety.
