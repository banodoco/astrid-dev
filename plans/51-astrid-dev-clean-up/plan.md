# astrid-dev clean-up

**Project:** astrid-dev clean-up

**Goal:** Contributors and their agents meet one word for each thing, one home for each rule and one skill for changing astrid-dev itself, in fewer words and fewer script lines than today.

**Status:** done

**Owner:** Plan 51 manager

**Estimate:** 0

**Waiting on:** —

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each, then run `python3 scripts/astrid_dev.py sync`. Its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary).

**Contributes to closure:** CA-005: each rule and each term has one source, and a fresh agent changes astrid-dev from one skill and the guide it links, with its confusions recorded and resolved. The gap's route names this plan as step 2 (task CU-0).

## Outcome and scope

astrid-dev is the repository that holds Astrid's plans, skills, templates and checks. This project cleans astrid-dev itself. It changes no product repository.

When it is done:

1. **One home per rule.** Each rule that is written in several skills today is written once. Every other mention is a link to it.
2. **One word per thing.** One glossary defines every role and every unit of work. The skills stop defining terms.
3. **Principles that come from failures.** The contribution principles are decided again from the failures people have hit. Each one names an example in this repository and, where a machine can check it, the check that does.
4. **One skill for changing astrid-dev.** It says where a new rule, term, check, page or field goes, and how to prove the change.
5. **The conflicts are settled.** Five places where two skills say opposite things are made to agree. The one that could cost money, about rented GPU machines, goes first.
6. **Less, not more.** The skills end with fewer words and the scripts with fewer lines than they started with.

**Included, in two parts:**

- **Part 1, words.** It starts on the owner's go. It touches no file under `scripts/`, no workflow, and none of the files Plan 48's open refresh change edits. Tasks CU-0 to CU-9, with two review stops.
- **Part 2, scripts and one check.** It starts only after Plan 48's refresh job is live on `main` (Plan 48's task C-2). Tasks CU-11 to CU-16 and the final review.

*Owner decisions, 12 Nov 2026:* the completion-form change is taken and joins Part 2 (D9.1); the older packs' sentence is left (D7); the other two check changes stay proposed.

**Proposed, not committed** (owner decisions D7 and D9): correcting one sentence in five older packs; making the unfilled completion form fail the completion check; letting ten checks report while a plan's header is broken; and a check that asks for a reason when a pull request adds words to the skills. Nobody has hit a failure from the first three, and the fourth adds a step for every author.

**Boundaries:**

- No new role, status, record type or approval.
- No check changes its verdict, trigger or message without a task that says so. One check is added and one check changes when it fails; [tasks.md](tasks.md) says exactly how.
- The release skill and the GPU-validation skill are not edited while Releases 12 and 13 are running.
- No pack with a live run is edited (Plans 20, 29, 32, 40 and 48 today), except one note in Plan 48's task list that its owner merges.
- Files that belong to Releases 12 and 13 are reported to the owner, never edited.
- No workflow file changes.

**Deferred or cut, with the reason in [inputs.md](inputs.md#alternatives-including-doing-less):** one parser for every script; one helper for finding changed files; a generated completion form; one evidence form; a lock on who may edit a pack; a check for model names; a fixed word budget for the skills; a list of every rule in every skill.

## Existing work and decision

This builds on what is already here:

- **The run contract** already calls itself the single owner of run policy. Most duplicated rules move there.
- **The three project templates** are already the one definition of a pack, and a check enforces it. The same idea is applied to rules and terms.
- **[Plan 48](../48-one-record-model/plan.md)** built the one command, the check list, the generated pages and the oracle that pins the verdicts of the always-run checks. Part 2 uses them and adds no new mechanism.
- **[The extending guide](../../docs/extending.md)** already shows how to add a check, a page and a field. The new skill points to it and does not copy it.
- **The process ledger** records what went wrong in recent runs. Each task here starts from one of those records or from a verified finding.

Seven fact-finders read the repository on 12 Nov 2026. The planner checked each finding in the code. Fourteen were wrong, weaker than reported or already handled, and were dropped. An independent critic then read this pack against the code; one design was dropped and most of its seventeen findings changed a card or a claim. The smallest sound approach is to fix what has caused a real failure and cut the rest. The findings, the alternatives, the critique and the open decisions are in [inputs.md](inputs.md#planning-evidence).

The owner asked for this project on 12 Nov 2026 and accepted its scope the same day (decision D1 in [inputs.md](inputs.md#owner-decisions)).

## Sequence and readiness

Part 1 has one short chain and then four tasks side by side:

1. Count and list what exists (CU-1). Fix the rented-machine conflict (CU-2).
2. Decide the principles (CU-3). Write the glossary, the table of homes and the new skill (CU-4). Review both (RS1).
3. Apply them to the skills, three workers at once (CU-5, CU-6, CU-7), while a fourth polishes the three new documents (CU-8).
4. Small stale fixes (CU-9) run beside all of this.
5. Review the whole of Part 1 (RS2) and land it.

Part 2 waits for Plan 48's refresh job. It removes dead script code, stops a generated page being its own source, sweeps the contributor docs and adds one check.

**Constraints:**

- While Part 1 runs, other sessions keep changing the skills. The manager merges `main` in each day. A rule added elsewhere during the run is placed by the table of homes before Part 1 lands.
- Part 1 can land and be useful if Part 2 never starts.

**Unresolved:** owner decisions D1 to D11 in [inputs.md](inputs.md#owner-decisions). Task details are in [tasks.md](tasks.md). Recording this plan does not authorize any work.

## Interfaces and handoff

**Consumes:**

- astrid-dev `main`. This plan was written against `1826336201f4ec631399d2169b210b1bc22aebe8`.
- For Part 2, Plan 48's refresh change as merged (draft pull request 544 today; its branch has moved since this plan read it at `29779a5`). The manager records the merge commit when Part 2 starts and re-checks Part 2's cards against it.

**Produces:**

- `skills/astrid-dev-shared/glossary.md`, the one home for role and work-unit terms.
- `skills/astrid-dev-improve/SKILL.md`, the skill for changing astrid-dev, with its table of homes.
- A rewritten `docs/contribution-design-principles.md`.
- One check in the one check list: `link-anchors`.
- `plans/51-astrid-dev-clean-up/evidence/baseline.md`, the starting word count, the terms and the duplicated rules.

**Limits:** principles are cited by number in three older plans. After the rewrite those numbers may point to a different principle. The rewrite gives each principle a short name, and new text cites the name.

## Completion

The project is complete when all of these hold on `main`:

- **Fewer words.** This prints less than 29,156, the count at the starting commit, with the new glossary and skill counted:

  ```text
  LC_ALL=C find skills docs/contribution-design-principles.md docs/extending.md docs/project-format.md docs/contribution-workflow.md docs/contribution-automation-setup.md -type f -name '*.md' -print0 | LC_ALL=C xargs -0 cat | LC_ALL=C wc -w
  ```

  The planner expects several hundred fewer and has not proven it: the additions are certain (up to about 1,250 words) and the cuts in the two longest skills stop early if a rule would be lost.
- **Fewer script lines.** `ls scripts/*.py | grep -v /test_ | xargs cat | wc -l` prints less than it did on the commit where Part 2 started. The margin is small, about twenty lines: about fifty go and the new check adds about thirty. It was 2,948 at this plan's commit, before Plan 48's refresh change.
- **No rule lost.** Every card that deleted a sentence listed it with the home of its rule. The review of Part 1 samples twenty against the diff and looks for deletions no list mentions.
- **One definition per term.** No skill but the glossary has a `## Terms` section.
- **The skill works.** A fresh worker on the cheapest route, given the new skill, the extending guide it links and its task card, adds the `link-anchors` check. Each question it asks becomes a fix to the skill or the guide.
- **Nothing changed by accident.** `scripts/fixtures/golden.txt` is byte-identical to its state when Part 2 started, and `python3 scripts/astrid_dev.py check` passes.
- **Negative cases.** A link to a heading that does not exist in a skill fails `link-anchors`. Swapping two principle headings in the generated vision page no longer changes the public feed.

**Limits of this proof:** counts show size, not clarity. Whether the skills read better is the reviewers' and the owner's judgment. After the project, only the new skill's rule and an occasional audit keep the skills short, unless the owner takes the proposed check. Nothing here is proven with many contributors at once. Merging to `main` needs the owner's go; this plan grants none.
