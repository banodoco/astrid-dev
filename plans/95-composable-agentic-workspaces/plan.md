# Otto — an importable framework for Markdown-first organisations

**Project:** Otto — an importable framework for Markdown-first organisations

**Goal:** A person or agent can pin Otto in a Markdown-first workspace, declare its records, relations, pipelines, project templates and skills in a few small files, follow Otto's guidance to stand up an organisation, and have `otto check` prove the workspace keeps to its declared pipelines, without changing Otto or another workspace.

**Status:** active

**Owner:** The orchestrator, Claude session `session_011EzfW1Urc5P4hpm2SvVy5d` (accountable), with ChatGPT manager `p95-manager-1` dispatching fresh packet sessions; owner-authorized 25 November 2026

**Estimate:** About 12 engineering days (10–14) after Plans 71–73 land: pipelines about 2.5, organisation guidance about 3, project templates about 1.5, extraction and config about 3, Dev migration about 2, reviews about 1. The critical path to the tagged Otto v0.1.0 that Plan 96 waits on is about 7 days of elapsed work.

**Waiting on:** the acting Lead finishing OT-19 part d and then the adopted path on the [run board](run.md#now-28-nov-2026); the owner's own sign-off on OT-18's before and after; astrid-dev `main` merges of the project branch need the owner's go at the end (OT-24).

**Run route:** astrid-dev-only

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — moves the organisation's shared coordination, validation and guidance into Otto, with Astrid Dev and Astrid Marketing as independent consumers; it does not itself close CA-005 or CA-003.

## Outcome and scope

**Otto** (O-T-T-O) is a small Python package and CLI that any Markdown-first workspace pins by git tag. It is not an Astrid product and not a mandatory process. Astrid Dev is its first consumer; Astrid Marketing ([Plan 96](../96-astrid-marketing-organisation/plan.md)) is the driving second consumer, and every seam below is justified by what Marketing needs or by keeping Dev unchanged. Otto v0 contains:

1. **Package and repository.** A public `banodoco/otto` repository with a `pyproject` package `otto` (standard library only, Python 3.11 or later) and an `otto` command: `otto check`, `otto views generate`, `otto skills build|check|install`, `otto pipeline list|show`. Workspaces pin a git tag; no PyPI at first. Creating the repository is owner decision [D2](inputs.md#owner-decisions).
2. **Workspace config, `otto.toml`.** The workspace name, its skill namespace prefix (Dev keeps `astrid-dev-`), its paths (record folders, agent source root, common pack templates) and an ID policy per record kind: Dev uses `NN-slug` for projects and `XX-NNN` for gaps, Marketing uses slugs. One resolver maps IDs to paths both ways. This replaces [Plan 98](../98-project-identity-and-vocabulary/plan.md)'s resolver card.
3. **Record and relation kinds as data.** [Plan 72](../72-composable-project-delivery/plan.md)'s `RECORD_KINDS` and `RELATION_KINDS` literals and its cardinality rules become workspace-declared data. Otto ships generic Markdown readers (frontmatter, bold header fields, headings, tables) built on `scripts/document_structure.py`. Bespoke kinds, such as Dev's gaps and releases, stay as workspace-local Python adapters that `otto.toml` registers. Workspace code is as trusted as its repository; there is no extension sandbox.
4. **Declarative pipelines.** A workspace may declare several named pipelines, one small file each (proposed `pipelines/<id>.toml`). A pipeline is an ordered chain of stages (record kinds) joined by declared relation kinds, with basic constraints:
   - **cardinality per link,** at each end: exactly one, at most one, one or more, or any;
   - **required or optional stages** (optional relaxes that link's lower bound to zero; a declaration that is both optional and "exactly one" is rejected);
   - **primary and supporting role rules** (for example, exactly one primary, any supporting);
   - **allowed source and target kinds** per stage (a stage may accept more than one kind);
   - **allowed statuses** per stage, optionally.

   `otto check` runs a conformance check for every declared pipeline and reports each violation with its source file and line. `otto pipeline list` and `otto pipeline show <id> <record-id>` traverse read-only, in a deterministic order, and terminate on cycles. Each constraint type has a planted-violation fixture that proves it is caught. One record may take part in several pipelines, with no duplicated record or owner, and deleting a pipeline file deletes no record. This is **not an execution engine**: no scheduler, no automatic transitions, no state machine, and no language beyond this small declaration. Dev declares exactly Plan 72's two compositions as `delivery` (goal → gap → project → release) and `issue` (issue → release), with byte-identical public output. Marketing declares at least `strategy` (goal → project → campaign, campaign optional) and `intake` (issue or idea → project). Plan 72 excluded a generic pipeline DSL from its own scope; that boundary was Plan 72's. Otto now owns this small declarative layer, at the owner's request ([D1](inputs.md#owner-decisions)), and Plan 72's code is not reopened.
5. **Project templates (absorbs [Plan 97](../97-extensible-project-templates/plan.md)).** One project entity. The header field `**Template:**` selects a template, and a missing field means `standard`. Otto ships `standard` and `loop`; each has a manifest (proposed `templates/<name>/template.toml`) naming its extra documents, their required headings and its execution workstream. A workspace may add its own templates, and names its own common pack templates or uses Otto's generic ones: one additive level, no inheritance. In Dev only real loop plans opt in: [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) (`**Plan type:** a loop plan`, with `rounds.md`) and [Plan 94](../94-dependable-environment-setup-and-recovery/plan.md) (a draft loop plan). [Plan 89](../89-heavy-saves-in-seconds/plan.md) runs a measure-and-fix loop under Release 15's pinned instructions and opts in only if that release's Lead agrees. [Plans 87](../87-render-works/plan.md) and [88](../88-timeline-edits-land/plan.md) are standard plans whose loop is one bounded phase. Every other pack is untouched.
6. **Checks and views.** [Plan 48](../48-one-record-model/plan.md)'s check runner and view engine move to Otto. The workspace registers its own checks and views (`main(..., registry=...)` is already injectable). Otto ships generic checks: links and anchors, pack shape and templates, relationship validity, pipeline conformance, skill packages current, and generated views current.
7. **Skills.** Plan 73's document reader, builder and installer, with the namespace and source root from `otto.toml`. Plan 73's completion card MSC-2 already puts the prefix and root in one constant each. Two namespaces install side by side, and each retires only its own packages.
8. **Organisation guidance.** Otto ships `guidance/` as Markdown with `skill: true`, built as `otto-*` skills:
   - a **stand-up playbook** for a new organisation or workspace, as a checklist: config, strategy document, record kinds, pipelines, templates, roles, boards, first project;
   - the **generic run-contract core**: routes `N`/`X`/`S`/`T` and their model families, cheapest model first, one accountable agent, authority only from the owner's own message, the decisions ledger, load-bearing tests, review rounds and the last-round rule, and provenance;
   - **generic roles** (leader, orchestrator, manager, worker) and **generic workstreams** (plan, iterate, merge, improve, review, fresh-session ChatGPT packet dispatch, and the boards and mailbox protocol).

   Workspaces keep overlays. Dev's release, GPU and product-repository specifics stay in astrid-dev `agent/` and link to the pinned Otto guidance. Marketing writes its own overlay (campaigns, publication authority) in Plan 96. The split is proved by a rule-preservation map from Dev's documents to Otto core plus Dev overlay, with zero lost rules.
9. **Dev migration.** astrid-dev pins Otto and swaps its generic modules to `otto` imports, deleting its copies so each mechanism has one home. Dev's existing golden fixtures and full unit suite are the parity check, and the public vision JSON is byte-identical at a fixed revision. There is no physical rename of `plans/` or of projects.
10. **Marketing pilot inside Otto's tests.** A synthetic, minimal Marketing fixture workspace proves the second consumer before Plan 96 builds the real one. It has two pipelines, an optional campaign, a standard and a loop project, and a blank workspace with no pipelines beside it.

Proposed shapes, which OT-4 fixes and RS1 reviews:

```toml
# otto.toml (Dev)
[workspace]
name = "astrid-dev"
skill_namespace = "astrid-dev-"
[paths]
projects = "plans"
agent = "agent"
pack_templates = "templates/project"
[ids]
project = "NN-slug"
gap = "XX-NNN"
[adapters]
module = "scripts/otto_dev.py"
```

```toml
# pipelines/strategy.toml (Marketing)
id = "strategy"
stages = ["goal", "project", "campaign"]
[[links]]
relation = "serves"      # project -> goal
from = "project"
to = "goal"
per_source = "one-or-more"
per_target = "any"
[[links]]
relation = "includes"    # campaign -> project
from = "campaign"
to = "project"
per_source = "one-or-more"
per_target = "any"
optional = true
```

**Not included:** the physical rename `plans/` → `projects/` in Dev (Plan 98, optional and later), a scheduler or any automation, a visual builder, a central database or graph store, template inheritance, sandboxing of trusted workspace extensions, PyPI publishing, generalising Dev's release, gap, public-feed, claim, review or auto-merge machinery, issue-intake code (Marketing uses issue forms), and rewriting active run instructions or historical receipts.

## Existing work and decision

Otto lifts working code, not a new design. [Plan 48](../48-one-record-model/plan.md) (done) supplies the check registry, view engine, pack shape and lifecycle. Plan 72 supplies `RelationshipIndex`, which uses only the standard library and is ready to lift, and the two read-only compositions that become Dev's pipelines. Plan 73 supplies the `agent/` Markdown sources with `skill: true`, the builder and the installer, and its MSC-4 rule-preservation audit, which seeds the guidance split. Plans 72 and 73 finish under their own completion runs; this plan adds nothing to them. Plan 97 is cancelled and absorbed here as the template seam. Plan 98 is cut down to an optional later Dev rename.

On 24 November 2026 the owner chose Otto, its two consumers, and multiple pipelines per workspace with basic constraints and tests that the workspace keeps to them ([inputs](inputs.md#owner-direction-24-november-2026)). An independent direction review the same day judged the end state right but the order backwards and the guidance under-specified. The owner accepted its sequence, its absorption of Plan 97 and cut-down of Plan 98, its distribution and trust recommendations, and its guidance layer. The owner overruled its advice to defer declarative pipelines. Dispositions are in [inputs](inputs.md#planning-evidence). The scope stays pending until the owner merges this scope PR.

## Sequence and readiness

1. Plans 71, 72 and 73 land on `main` under their own runs. OT-1 records the integrated baseline and the parity oracles.
2. The owner settles D2 (repository) and D3 (run route); the orchestrator creates the repository (OT-2).
3. The contract design (OT-4) and the mechanical lifts (OT-3, OT-5, OT-6) run in parallel; the guidance map (OT-15) starts at the same time. RS1 reviews the config, record, relation, pipeline and template contract, before any card builds on it.
4. Config, relations, pipelines, templates and `otto check` (OT-7 to OT-13) are built on the reviewed contract. The Marketing fixture (OT-14) and the guidance documents (OT-16 to OT-18) are written alongside.
5. Dev migrates on its project branch (OT-19 to OT-21), and OT-22 proves parity. OT-23 tags Otto v0.1.0, which unblocks Plan 96. Then the final review R and the completion PR (OT-24) follow.

The run uses the fresh-session ChatGPT packet workstream: an orchestrator, a manager for this plan, and packets in High, Extra High or Pro by route. [Tasks](tasks.md) marks which cards are orchestrator-lane (proofs, repository and branch operations, migrations needing clones or network, reviews) and which are packet-able (code and document writing). Recording this plan authorizes no run.

## Interfaces and handoff

**Consumes:** astrid-dev `main` after Plans 71–73 land, at the SHA OT-1 records: Plan 48's check and view engines, Plan 72's `relationships.py` and `project_delivery.py`, Plan 73's `agent_documents.py`, `skill_builder.py`, `skill_installer.py`, its `agent/` tree and its rule-preservation audit. Earlier candidate SHAs in [inputs](inputs.md#source-identities) are observations, not bases.

**Produces:** the `banodoco/otto` repository at tag `v0.1.0`; the `otto.toml`, pipeline and template-manifest contract (`docs/contract.md`); generic checks; `otto-*` guidance skills; Otto's synthetic Marketing and blank fixture workspaces; and astrid-dev pinned to that tag, with its two pipelines declared, loop plans declared and its `agent/` overlay linking Otto guidance.

**Handoff to Plan 96:** the tag, the contract, the Marketing fixture as a starting example (not a pilot), the stand-up playbook and the guidance to overlay. A missing primitive found by Marketing becomes an Otto issue and a patch tag, not a fork. **Handoff to Plan 98:** Dev paths are configuration, so a rename, if the owner wants one, is a config change plus a move and its consumers.

## Completion

1. astrid-dev and the Marketing fixture use the same pinned Otto. On Dev, the full unit suite and golden fixtures pass unchanged except import lines; the public vision JSON at a fixed revision, `project_delivery.py` outputs and the `astrid-dev-*` skill tree are byte-identical to the OT-1 baseline; hosted `documentation` and `vision-consumer-contract` pass.
2. `otto pipeline list` shows Dev's `delivery` and `issue` pipelines and the fixture's `strategy` and `intake` pipelines. One project appears in two pipelines with one task list. A blank workspace with no pipelines passes `otto check`.
3. Every constraint type, and every malformed declaration, has a planted fixture that `otto check` rejects with file and line. Plan 72's planted negatives still fail on Dev with their messages.
4. A fixture adds a third template (`research`) with no Otto code change. A Dev loop plan validates against the loop template, and every non-loop pack is unchanged.
5. `otto-*` and `astrid-dev-*` skills install side by side into one temporary destination, and removing one namespace leaves the other. The rule-preservation map assigns every consequential rule in Dev's guidance to Otto core or Dev overlay, with none lost.
6. Limits: proof covers two workspaces, one real and one synthetic. It is not a claim of generality to every organisation, of agent safety, or of Marketing's success. No Astrid product release, product repository or publication is involved.
