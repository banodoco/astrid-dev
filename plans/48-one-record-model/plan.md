# One model for astrid-dev's records, checks and generated pages

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [CA-003 — Our vision and execution aren't yet fully connected](../../vision/gaps/CA-003-vision-experiments-progress.md) (primary).

## Outcome and scope

A contributor or agent can answer four questions about astrid-dev from one place each, and they stay true with a hundred plans in flight:

1. **What kinds of record exist, and what shape is each?** (project, gap, release, ledger entry, review form.)
2. **What is checked, and when?** One command lists every check and runs them the same way locally and in CI.
3. **Which files are written by hand and which are generated?** Every fact has one source; every other appearance is a generated view, marked as such.
4. **How do I add a check, a view, a field or a stage?** One documented place, one entry, and the forms, checks and pages that depend on it follow.

**Included, in four phases:**

- **Phase 1: one model, one command.** One Markdown record parser, a registry of checks behind one command, and one standard way to generate a page or a marked region. The existing vision README, root summary and public feed move onto it. No rule changes: what passes today passes after, and the public feed is byte-identical.
- **Phase 2: plans define the list.** Status, owner, estimate and waiting-on move into each project's own `plan.md`. `plans/index.md` and the strategy release table become generated views. Priority gets its own small ordered file. The claim and review-intake bots read the project file. Project numbers are checked unique.
- **Phase 3: one pack shape, a declared lifecycle, generated forms.** The plan, inputs and tasks shapes are declared and checked for new and changed packs. Statuses, transitions and what each transition requires are declared once; the three PR gates become transition checks. PR templates are generated from the same form definitions the checks read.
- **Phase 4: one evidence shape.** One envelope (claim, exact candidate, command, environment, result, receipt, limits, route) used by the implementation and completion forms and the GPU validation record.

**Boundaries:**

- No new record types, statuses, approvals or roles. This consolidates what exists ([principle 8](../../docs/contribution-design-principles.md)).
- No dependencies beyond the Python standard library, and no new file format: fields stay in the two syntaxes the repository already uses.
- CI still checks structure, links and transitions only. Whether evidence proves a claim stays a reviewer's judgment ([principle 7](../../docs/contribution-design-principles.md)).
- Product repositories are not changed. The public feed's shape is not changed.
- Packs of projects with a live run (Plans 20, 29, 32, 40 today) are not reshaped until their run ends.

**Deferred:** a public evidence trail on the vision page ([Plan 44](../44-vision-execution-trail/plan.md) owns it and can consume Phase 4's envelope); moving raw logs out of the repository; allocating project numbers automatically.

## Existing work and decision

This grows from three things already in the repository, not from a new design:

- **Shared parsers, partly done.** `scripts/project_contract.py` calls itself "the one interpretation used by validation, completion and publishing"; `vision_subject.py`, `gap_relationships.py`, `catalog_rows` and `contribution_api.py` are each shared by several scripts. The rest of the parsing is repeated per script.
- **One generated-page pipeline.** `scripts/export_public_vision.py` generates `vision/README.md`, the root README summary and the public feed, with a stale check in CI and a publish step on `main`. It is specific to the vision and cannot be reused for a second page.
- **[Plan 31](../31-releases-from-astrid-dev/plan.md)** designs a typed release record, a draft-to-final gate and a second generated-only branch. That is this project's lifecycle and view ideas for one record type.

The smallest sound approach is to finish the shared layer those three imply, then move the catalog onto it. The findings, alternatives, critique and open owner decisions are in [inputs.md](inputs.md#planning-evidence). This is a draft: the scope is not accepted.

## Sequence and readiness

Phases run in order; each leaves the repository working and is useful if later phases never start. Phase 1 carries most of the value for contributors adding checks or pages; Phase 2 removes the shared file every plan change edits today.

1. **Phase 1** (PM-1 to PM-5, then review stop RS1). Behaviour-preserving, so it can land while other plans run.
2. **Phase 2** (PM-6 to PM-10). Changes how a project is claimed and where status is edited, so it lands in one coordinated change with the skills and workflow docs.
3. **Phase 3** (PM-11 to PM-13).
4. **Phase 4** (PM-14), then review rounds (R).

**Readiness and constraints:**

- **Release 12** managers depend on the current checks daily. Nothing here starts before Release 12 is published, and Phase 1 must not change any check's result.
- **Plan 31** adds its own checker and publisher to the same scripts. Sequence Phase 1 before Plan 31's RL-1a to RL-1c so Plan 31 registers checks and views instead of adding a fourth one-off (owner decision D5).
- **Phase 2's refresh on `main`** needs `main` protected and a bot identity allowed to commit generated files, the same owner settings Plan 31 and the claim bot already wait on (D3).
- Open owner decisions D1 to D6 are in [inputs.md](inputs.md#owner-decisions).

Tasks, routes, scopes and proofs are in [tasks.md](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** the current scripts, workflows, templates and skills at the astrid-dev revision recorded when each task starts; the App's `vision:check` parser through the existing `vision-consumer-contract` job.

**Produces, for other projects to build on:**

- `python3 scripts/astrid_dev.py check | list | sync`: the one entry point CI and contributors run.
- A record model other scripts import (record types, fields, statuses, transitions, forms).
- A view mechanism Plan 31 can use for its release manifest and Plan 44 for its trail.
- An evidence envelope Plan 44 and the GPU validation skill can cite.
- `docs/checks.md` and `docs/extending.md`: the generated list of every check and view, and the one page on adding a check, view, field or stage.

**Limits:** the public feed (`vision.json`) keeps `schemaVersion: 1` and its exact shape; any change there is out of scope and would need the App's agreement.

## Completion

Shown on the integrated astrid-dev candidate, with exact SHAs:

- **Listable:** `astrid_dev.py list` prints every check and view with its trigger; `docs/checks.md` is generated from it and CI fails if it is stale.
- **Same everywhere:** the documentation workflow runs only `astrid_dev.py check`; the same command on a clean checkout of the same commit gives the same result.
- **One source per fact:** no check compares two hand-written copies of a fact. The catalog, the strategy release table, the vision README and every PR template are generated, and each generated file or region carries the standard marker.
- **Plans define the list:** a PR adding only a valid `plans/NN-name/` folder appears in the generated catalog with no edit to any shared file; two such PRs opened from the same base both merge without conflict.
- **Extensible in one place:** adding a new check, a new view, a new project field and a new lifecycle stage are each demonstrated as a change to one file plus its test, following `docs/extending.md`.
- **Negative cases:** a hand edit to a generated file fails; a duplicate project number fails; a claim for another person's handle, or one that changes any other field, is refused; a status change without its transition's form fails.
- **Unchanged:** the public feed is byte-identical before and after Phases 1 and 2 for the same sources, and the App's parser accepts it.

**Limits of this proof:** it shows structure, not that contributors find it clearer. One fresh agent adding a check and a view from `docs/extending.md` alone, with its confusions recorded, is the only readability evidence. Completion does not close CA-003: that gap needs a maintained public trail for three decisions, which this project enables and does not deliver.
