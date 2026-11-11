# One model for astrid-dev's records, checks and generated pages

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary).

**Contributes to closure:** CA-005: one command lists every check and generated page; a project lands by adding only its own folder; one source per fact; a fresh agent extends it from the guide; refusals work.

## Outcome and scope

A contributor or agent can answer four questions about astrid-dev from one place each, and they stay true with a hundred plans in flight:

1. **What kinds of record exist, and what shape is each?** (project, gap, release, ledger entry, review form.)
2. **What is checked, and when?** One command lists every check and runs them the same way locally and in CI.
3. **Which files are written by hand and which are generated?** A project's facts live in the project; the catalog is generated from the plans, and every generated file is marked.
4. **How do I add a check, a view or a field?** One documented place, one entry.

**Committed, in two phases:**

- **Phase 1: one model, one command.** One shared record helper, a registry of checks behind one command, and one standard way to generate a page or a marked region. The existing vision README and root summary move onto it. One rule changes on purpose (PR checks read the working tree, so local and CI agree); every other verdict stays the same and the public feed is byte-identical.
- **Phase 2: plans define the list.** Status, owner, estimate and waiting-on move into each project's own `plan.md`, and `plans/index.md` becomes a generated view. Priority gets its own small ordered file. The completion gate, review intake and the claim bot read the project file. Project numbers are checked unique.

**Proposed, not committed (owner decision D7):**

*Owner decision, 11 Nov 2026 (D7, D9):* queued to run after Phase 2: the one-line form fix (PM-13h), Phase 3's pack-shape track and its lifecycle track without the status gate, and one review round. Phase 3's form track and all of Phase 4 stay proposed and unscheduled. No run is authorized yet.

- **Phase 3: one pack shape, a declared lifecycle, generated review forms.** Three tracks that do not depend on each other:
  - **A, pack shape.** The three templates are the declaration. A new pack must match them. Existing packs are never checked.
  - **B, lifecycle.** The six statuses and what entering each requires are declared in one file that every reader uses. As a separate, droppable step, the allowed moves between them are declared too and any other move fails.
  - **C, the completion form.** It is generated from a definition, and the completion gate takes its labels from the same definition. The gate's rules stay as they are.
- **Phase 4: one evidence shape.** One envelope (claim, exact candidate, command, environment, result, receipt, limits, routes) in the implementation review form and in the GPU validation record. CI confirms it is complete, never that it is true. The completion assessment keeps its own lines.

Both phases are specified to task level in [tasks.md](tasks.md) at the owner's request of 11 Nov 2026; that request is not acceptance. Two independent critiques recommend cutting most of this until a recorded failure asks for it, keeping at most a one-line fix to the completion form and the pack-shape check; see [the first](inputs.md#critique) and [the second](inputs.md#second-critique).

**Boundaries:**

- No new record types, statuses, approvals or roles. This consolidates what exists ([principle 8](../../docs/contribution-design-principles.md)).
- No dependencies beyond the Python standard library, and no new file format: fields stay in the two syntaxes the repository already uses.
- CI still checks structure, links and transitions only. Whether evidence proves a claim stays a reviewer's judgment ([principle 7](../../docs/contribution-design-principles.md)).
- Product repositories are not changed. The public feed's shape is not changed.
- Phase 2 moves four header fields in every pack in one change. Nothing else in a pack with a live run (Plans 20, 29, 32 and 40-machine-lifetime-controls today) is touched until its run ends.
- The strategy release table stays with [Plan 31](../31-releases-from-astrid-dev/plan.md), which already owns `strategy.md` and the release template.

**Deferred:** generating the strategy release table (Plan 31); a public evidence trail on the vision page ([Plan 44](../44-vision-execution-trail/plan.md) owns it and can consume Phase 4's envelope); moving raw logs out of the repository; allocating project numbers automatically.

## Existing work and decision

This grows from three things already in the repository, not from a new design:

- **Shared parsers, partly done.** `scripts/project_contract.py` calls itself "the one interpretation used by validation, completion and publishing"; `vision_subject.py`, `gap_relationships.py`, `catalog_rows` and `contribution_api.py` are each shared by several scripts. The rest of the parsing is repeated per script.
- **One generated-page pipeline.** `scripts/export_public_vision.py` generates `vision/README.md`, the root README summary and the public feed, with a stale check in CI and a publish step on `main`. It is specific to the vision and cannot be reused for a second page.
- **[Plan 31](../31-releases-from-astrid-dev/plan.md)** designs a typed release record, a draft-to-final gate and a second generated-only branch. That is this project's lifecycle and view ideas for one record type.

The smallest sound approach is to finish the shared layer those three imply, then move the catalog onto it. The findings, alternatives, critique and open owner decisions are in [inputs.md](inputs.md#planning-evidence). Phase 1's scope is accepted; the rest is not.

## Sequence and readiness

Phases run in order; each leaves the repository working and is useful if later phases never start. Phase 1 carries most of the value for contributors adding checks or pages; Phase 2 removes the shared file every plan change edits today.

1. **Phase 1** (PM-0 to PM-5t, then one review round, R1). Accepted and authorized.
2. **Phase 2** (PM-6 to PM-10). Not yet accepted. Changes how a project is claimed and where status is edited, so the migration, the gates that read status and the docs land together.
3. **One review round** (R) closes the committed scope.
4. **Phases 3 and 4** (PM-11a to R4) only if D7 accepts them, each closed by its own review round (R3, R4). Only Phase 3's lifecycle track needs Phase 2; the pack-shape and form tracks need only Phase 1 on `main`, so the owner may take either earlier (D9). Phase 4 needs the form track. The one-line form fix (PM-13h) needs nothing.

**Readiness and constraints:**

- **Release 12** managers depend on the current checks daily. Phase 1 starts now on the owner's go, lands on its integration branch, keeps the old check commands working, and reaches `main` in one PR on the owner's go. Phase 2 waits for Release 12 to publish.
- **Plan 31** adds its own checker and publisher to the same scripts. Sequence Phase 1 before Plan 31's RL-1a to RL-1c so Plan 31 registers checks and views instead of adding a fourth one-off (owner decision D5). Whichever lands second re-plans its task cards against the other's result.
- **Phase 2's refresh on `main`** needs `main` protected and a bot identity allowed to commit generated files, the same owner settings Plan 31 and the claim bot already wait on (D3).
- Open owner decisions D1 to D8 are in [inputs.md](inputs.md#owner-decisions).

Tasks, routes, scopes and proofs are in [tasks.md](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** the current scripts, workflows, templates and skills at the astrid-dev revision recorded when each task starts; the App's `vision:check` parser through the existing `vision-consumer-contract` job.

**Produces, for other projects to build on:**

- `python3 scripts/astrid_dev.py check | list | sync`: the one entry point CI and contributors run.
- A record helper other scripts import (sections, fields, tables, project records).
- A view mechanism Plan 31 can use for its release manifest and strategy table, and Plan 44 for its trail.
- If Phase 3 is accepted: `scripts/pack_shape.py` (the shape read from the templates), `scripts/lifecycle.py` (statuses, what each requires and, if kept, the allowed moves) and `scripts/forms.py` (the completion form).
- If Phase 4 is accepted: `scripts/evidence.py`, whose `parse` returns the envelopes in a text, for Plan 44 and the GPU validation skill to cite.
- `docs/checks.md` and `docs/extending.md`: the generated list of every check and view, and the one page on adding a check, view or field.

**Limits:** the public feed (`vision.json`) keeps `schemaVersion: 1` and its exact shape; any change there is out of scope and would need the App's agreement.

## Completion

Shown on the integrated astrid-dev candidate, with exact SHAs:

- **Listable:** `astrid_dev.py list` prints every check and view with its trigger; `docs/checks.md` is generated from it and CI fails if it is stale.
- **Same everywhere:** the documentation workflow runs only `astrid_dev.py check`; the same command on a clean checkout of the same commit gives the same result.
- **One source per fact:** the catalog and the vision README are generated, no generated file is its own source, and each generated file or region carries the standard marker.
- **Plans define the list:** a PR adding only a valid `plans/NN-name/` folder appears in the generated catalog with no edit to any shared file; two such PRs opened from the same base both merge without conflict.
- **Gates still bite:** a PR that changes a project's status to `done` in its `plan.md` without a completion assessment fails, exactly as an index edit does today.
- **Extensible in one place:** adding a new check, a new view and a new project field are each demonstrated as a change to one file plus its test, following `docs/extending.md`.
- **Negative cases:** a hand edit to a generated file fails; a duplicate project number fails; a claim for another person's handle, or one that changes any other line, is refused.
- **Unchanged:** the public feed is byte-identical before and after Phase 1, and after Phase 2 differs only by the one renumbered project's id; the App's parser accepts it.

**If Phases 3 and 4 are accepted,** also shown on their integrated candidates:

- **Shape:** a new pack copied from the templates passes; the same pack with one template heading removed fails, naming the file and the heading; a changed or renamed old pack is never failed.
- **Lifecycle:** adding a status is one entry in `scripts/lifecycle.py`, shown by a test that adds one; a move to `done` without a completion assessment still fails; if PM-12c is kept, a status change the declaration does not allow fails.
- **Form:** editing the generated completion form by hand fails; it holds every label its gate asks for; with only its plan number filled in, it fails on every field whose rule can tell an answer from a hint.
- **Envelope:** an incomplete envelope fails in an implementation review request and in a new GPU record; a complete envelope that is false passes, and the form and the skill say so.
- **Unchanged:** no verdict that existed before either phase changes. For the completion gate that is shown by exact output over a pinned set of descriptions, before and after.

**Limits of this proof:** it shows structure, not that contributors find it clearer. One fresh agent adding a check and a view from `docs/extending.md` alone, with its confusions recorded, is the only readability evidence. Completion does not close CA-005: that also needs reassessment after a real period of many contributors working at once.
