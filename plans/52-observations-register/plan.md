# Observations register

> **DRAFT, 12 Nov 2026. Not accepted, not in the catalog, no run authorized.** `queued` below is the only status the catalog accepts for a plan that has not started; the owner decisions in [inputs.md](inputs.md#owner-decisions) are all open. The project number 52 is the next free one today and may change.

**Project:** Observations register

**Goal:** Anyone, person or agent, can log something they saw in Astrid in one small file and move on, and every planner sees the open observations about their plan and gap before writing tasks.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 1–1.5

**Waiting on:** the owner's decisions D1–D6; merge order with Plan 51's skill and script edits

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary): what one run sees reaches the next planner without a conversation. CA-005's route does not name this plan yet, so there is no `Contributes to closure` line; adding one is a [Gap](../../skills/astrid-dev-gap/SKILL.md) step if the plan is accepted.

## Outcome and scope

Astrid-dev has a home for every stage of work except the first one. A missing outcome is a gap, a scoped project is a plan, a user's failure is a bug issue, and friction in astrid-dev itself is a process-ledger entry. Something merely *seen* in the product (a smell, a suspected bug, a slow path, a usability trip), not certain and not worth specifying yet, has nowhere to go. On 12 Nov it went into three files in a working folder outside the repository (`smells.md`, `usability-log.md`, a failures catalogue) and into a release decision log.

When this is done:

1. **Logging is one file write.** A file `observations/YYYY-MM-DD-<slug>.md` with four header lines (`Date`, `Source`, `About`, `Outcome`) and one paragraph. No number to allocate, no form, no approval. One file per observation, so PRs never conflict.
2. **Each observation points at what it bears on.** `About` names gap IDs and plans, or `—`. `Outcome` is `open` until it is `folded:` into a named plan task, `fixed:`, turned into an `issue:`, or `dropped:` with a reason.
3. **One check keeps the links true.** `python3 scripts/astrid_dev.py check` verifies the name, the four fields, that every gap and plan in `About` exists, and that a `folded:` outcome names a real `tasks.md` containing that task id.
4. **One generated page shows what is open.** `observations/index.md`: open observations, oldest first, listed under each gap and each plan, with the count. Nobody maintains it by hand.
5. **Planners, gap assessors and release closers read it.** One sentence each in the plan, gap, manage, orchestrate and release skills, and one row in the contribution route table.

**Included:** the record definition, the check, the generated page, the skill and guide sentences, and adopting the interim files already in `observations/` unchanged.

**Not included:**
- a status workflow, assignees, priorities, severities or labels;
- an expiry timer or a check that fails on age (D3);
- generated regions inside gap or plan files;
- a command that writes the file (D4);
- moving the process ledger into this folder (D2);
- publishing observations on the public vision page (D6).

**Deferred:** per-gap counts on the vision page ([Plan 44](../44-vision-execution-trail/plan.md) can read the same files); a product-side command so an agent in a product checkout can log without an astrid-dev checkout.

## Existing work and decision

The [process ledger](../../docs/ledger/README.md) already is this mechanism for one subject: one file per entry, plain `Key: value` header, add-only, checked by `ledger_entry_errors` (`scripts/check_docs.py:114`) and registered as the `ledger` check (`scripts/checks.py:465`). It excludes product observations by rule ("Product bugs go to their repository's issues instead"). This plan reuses its shape and its parser for a second folder with a different field list, so there is still one way to write an entry file.

Alternatives considered, with the evidence, are in [inputs.md](inputs.md#planning-evidence): GitHub issues with a label, stub plans, an observations section in each gap, and widening the process ledger. This draft is not accepted; the owner has decided none of D1–D6.

## Sequence and readiness

1. **OB-1** defines the record and the check, tests first, and proves the 22 interim files pass unchanged.
2. **OB-2** adds the generated page. It needs OB-1's reader.
3. **OB-3** adds the sentences to the skills and guides. It needs the folder name (D1) and nothing from the code.

Critical path: OB-1 → OB-2. OB-3 runs beside them.

**Real dependencies:**
- [Plan 51](../51-astrid-dev-clean-up/plan.md) is active and rewrites the manage and orchestrate skills (CU-6, CU-7) and, in its Part 2, the shared guard in `scripts/checks.py` (CU-12). OB-3 and OB-1 change the same files, so each needs a merge order with those cards, agreed with Plan 51's manager.
- [Plan 48](../48-one-record-model/plan.md) lists astrid-dev's record kinds (`plan.md`, outcome 1). This plan adds one kind and must add it to that list's home, [extending.md](../../docs/extending.md).

No budget, no product repository, no paid service. Tasks are in [tasks.md](tasks.md); recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** the entry-file reader and check registry as they stand on astrid-dev `main` at the run's base (to be recorded in [inputs.md](inputs.md#source-identities)); the gap IDs in `vision/gaps/` and the plan folders in `plans/`.

**Produces:**
- the record: `observations/*.md` with the four fields, defined in `observations/README.md`;
- `check_docs.observation_errors(root)` and the `observations` check;
- the `observations-index` view writing `observations/index.md`;
- a reader other scripts can call for the open observations about a gap or a plan.

**Limits:** the check proves an observation's links resolve, never that the observation is true or that a `folded:` task really covers it; a reviewer judges that.

## Completion

- A fresh agent, given only the contributor skill and one sentence describing something it saw, adds a valid observation file without reading any script, and `astrid_dev.py check` passes.
- The 22 interim files pass the check unchanged.
- **Negative cases**, each a failing check with a message that names the file and the fix: a missing field; an unknown gap ID; a plan folder that does not exist; `folded:` naming a task id absent from that `tasks.md`; an `Outcome` outside the five forms.
- `observations/index.md` lists every open observation under each gap and plan it names, oldest first, and a hand edit to it fails `generated-views`.
- The plan, gap, manage, orchestrate and release skills each say when to read or write an observation, in one sentence, and link the README rather than restate the format.

**Limit of this proof:** it shows the mechanism works, not that people use it. The real test is the next release: whether its run notes hold loose lists of findings, or files in `observations/`.
