# Inputs — astrid-dev clean-up

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

Short names used below: RC is `skills/astrid-dev-shared/run-contract.md`; MGR, ORCH, PLAN, ITER, REL and GPU are the `SKILL.md` of the manage, orchestrate, plan, iterate, release and gpu-validate skills; CCR is `skills/astrid-dev-orchestrate/codex-in-claude-cloud/README.md`, BRIEF is `manager-brief.md` beside it, and CCX is `skills/astrid-dev-orchestrate/codex-cloud/README.md`. Line numbers are at `1826336`.

**Scope decision:** Pending — The owner asked for this project in the orchestrator's session on 12 Nov 2026: "a little project", an astrid-dev clean-up, so that "everything is really nice in terms of how astrid-dev works". She has not seen or accepted the scope written here. Next: the owner reads the [ten statements](#ten-vivid-statements) and decides D1 to D9.

**Prior art:** Seven read-only fact-finders read `main` at `1826336` on 12 Nov 2026. The planner checked every finding a task relies on against the code on this branch; see [what was verified](#prior-art-what-was-verified) and [what was wrong](#findings-that-were-wrong-or-already-handled). Reused: the [run contract](../../skills/astrid-dev-shared/run-contract.md) as the home of run rules, the [templates](../../templates/project/tasks.md) as the home of shapes, [Plan 48](../48-one-record-model/plan.md)'s check list, oracle and generated pages, the [extending guide](../../docs/extending.md) and the [process ledger](../../docs/ledger/README.md).

**Approach:** A new pack, because no existing plan fits: [Plan 14](../14-repository-cleanup/plan.md) cleans the product repositories and has no agreed scope, and Plan 48 is about records and checks, not rules and words. The work is cut to what has caused a real failure. Part 1 is words only and starts now; Part 2 is scripts and waits for Plan 48's refresh job. See [alternatives](#alternatives-including-doing-less).

**Challenge:** Pending — The planning skill requires an independent critique here, because the plan changes astrid-dev's own checks and skills and exceeds five days. Next: a fresh critic reads the written pack against the code; its findings and what was accepted are recorded under [Critique](#critique).

**Proof and limits:** Two counts taken before and after (words in the skills and five docs; lines in the non-test scripts), a rule list in which every rule is accounted for, the oracle file unchanged, a fresh worker adding a check from the new skill alone, and three negative cases. Counts show size, not clarity; clarity is judged in review. See [plan.md](plan.md#completion).

**Review rounds:** Recommend one round at each of three points, all on the S route by a fresh high-judgment sub-agent ([guide](../../skills/astrid-dev-shared/run-contract.md#review-and-promotion-boundaries)): a review stop after the principles, glossary and table of homes (RS1), because three workers then build on them; a review stop on the whole of Part 1 before it lands (RS2), because every agent reads these skills and a lost rule would only show up in a later run; and the final review on Part 2 (R), because it adds two checks. The owner has not confirmed.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the part or tasks it covers, the accountable session ([who that is](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run)), what it may do without asking, what still needs the owner's go, and the advisor session if there is one. The recommended setup is in the [dispatch notes](tasks.md#dispatch-notes).

### What the owner said

All on 12 Nov 2026, to the orchestrator's session. The orchestrator relayed them to the planner, so this record is second-hand.

- Make this "a little project", an astrid-dev clean-up, so that "everything is really nice in terms of how astrid-dev works". Follow the plan skill "to make sure that it captures everything and it's all as clean as possible". "There's obviously a lot of things that mean different things here that are going to cause issues."
- Ship the work already in flight first: Plan 48's refresh job (its task C-2, draft pull request 544). So anything here that edits `scripts/` or the workflows starts only after C-2 has merged. The words work does not have to wait.
- Rethink the principles from first principles, "as if you didn't even know that was there".
- Capture how astrid-dev is used, not only how it is built. She suggested a skill for improving astrid-dev itself, "astrid-dev-improve" or similar, possibly taking in the extending guide.
- Then make everything follow, "so that the actual code base of astrid-dev is as elegant as possible".
- Use cheap models for fact-finding and mechanical work, and stronger ones for the harder work.
- She asked whether it is right that every project has one owner, declared once, and nobody else can edit it meanwhile. She has not chosen how that is enforced (D2).

### Prior art: what was verified

Each line was checked in the code or by running it on this branch.

- **Rules are copied.** "Never rebase or force-push" is in MGR, ORCH's Codex guides, the merge and release skills, and not in RC. The route meanings are in RC:7, RC:13-16, PLAN:63, MGR:14, ORCH:58-63 and CCR:7-12. "Authority comes only from the owner's own message" is in RC:45, ORCH:76 and :96, MGR:81 and others.
- **Skills contradict each other.** Verified: C1, C3, C5, C6 and C7 below. C2 and C4 are weaker than reported (see the next section).
  - C1: CCR:22 installs the skills with `rm -rf ~/.agents/skills`; CCX:9-17 says never remove existing skills.
  - C3: CCR:12 and RC:16 map taste work to a Codex family; CCR:28 says taste work stays on Claude sub-agents.
  - C5: `codex-runner.sh:55` tells a pausing manager to "release or keep pods as is safe"; GPU:31 says "Release every pod this run made, whatever happened".
  - C6: RC:104 sends a blocking finding left after the last round "to the owner"; MGR:108 says "to the owner through the advisor".
  - C7: MGR:28 has the manager merge its own progress pull requests with auto-merge; ORCH:97 says the session needs the owner's go for merges.
  - Two stopping thresholds are never said to be different actions: ITER:23 (a worker stops after three attempts or 45 minutes) and RC:25 (a manager moves a task up a route after two misses or 20 minutes).
  - Model names: RC:53 bans exact model IDs in the repository; `docs/contribution-workflow.md:126` and `templates/product-pr/review.md:13` allow "a specific model name"; RC:13-16, CCR:7-12 and BRIEF:25-30 each carry a table of family names.
- **Words mean several things.** "Advisor" is the orchestrator (MGR:13) or a fresh sub-agent (PLAN:13). "Principle 7" in MGR:109 and BRIEF:55 means the manage skill's own seventh rule, not the seventh contribution principle. "Pack" is a plan's three files and also a product pack. Only PLAN and MGR have a `## Terms` section, and they define "owner" differently. Orchestrator, worker, lead, host, card, phase and track are used and never defined.
- **The skills are long.** 24,205 words in 17 files under `skills/`. MGR is 4,002 words and ORCH 3,450.
- **A generated page is still its own source.** `scripts/export_public_vision.py:89-92` and `:115` read the principle list from `vision/README.md`, which is generated. Swapping two principle headings there passes the checks and changes the public feed. Plan 48's review raised this twice and left it.
- **Dead and repeated code.** `records.py:109` `field_matches` has no caller. `check_docs.py:20` `STATUSES` has no reader. `check_completion.py` imports `json` and `subprocess` and uses neither; `check_gap_boundaries.py` imports `json` and does not use it. In `scripts/checks.py` eleven checks repeat the same seven-line guard, and in ten of them the `rows = projects(root)` call cannot do anything the line before it has not already done.
- **Bytecode is tracked.** Three `.pyc` files under `scripts/__pycache__/` are in git and `.gitignore` has no rule for them, so every task card has to carry a clean-up command. The first comment in `.gitignore` names another project.
- **Stale sentences.** `strategy.md:5` and `releases/TEMPLATE.md:22` say the catalog owns status, priority, estimate and owner. `docs/contribution-workflow.md:36` and `vision/gaps/F-001-platform-reliability.md:26` link to a heading whose name carries an old gap count. `env/README.md:20` says the setup installs three commands; `env/cloud-setup.sh` installs four. Twelve `plan.md` files still say status lives only in the catalog (the finding said sixteen).
- **The template misleads.** `templates/project/plan.md:17` shows `**Vision role: Foundational enabler**` with the colon inside the bold. `scripts/project_contract.py:9` needs `**Vision role:**` at the start of its own line, and counts the literal `(primary)`, which the template never shows.
- **The completion form passes half-filled.** Run on this branch: with only the plan number filled in, the form fails on two fields and passes on five hint lines. `Implementation PRs: None — TBD` passes, because the dash is not stripped before the placeholder test (`check_completion.py:75`). No recorded failure came from this, so it is proposed only (D9).
- **Two experiments, run in a scratch copy on 12 Nov 2026.** Removing the guard from ten checks leaves the oracle output byte-identical. No link in the repository points to a missing heading in `skills/`, `templates/` or a top-level `docs/` file, so a check for that starts with no errors; 25 links elsewhere are broken, all pointing into plan packs, release files, the root README or the generated vision page.

### Findings that were wrong or already handled

- **"The gap outcome words are declared twice and differ."** Wrong. `export_public_vision.py:22` lists a gap's states; `check_completion.py:17` lists what a completion may say about a gap. They are two lists for two things.
- **"`plans/02-consistent-generation/env/` is an orphan with diverged copies."** Wrong. `env/README.md:62` says those copies are frozen on purpose for Plan 02's recorded proof, and Plan 06 links them.
- **"An unedited inputs template passes the planning check."** True and intended: a draft keeps the template's `Pending — … Next: …` lines.
- **"The default pull request form lacks the two intake lines."** It tells the author to add them, which the setup guide allows.
- **"Two generators and two repair commands for the vision page", "the docs recommend `--sync-readme`", "the claim form asks for two files and the bot accepts one".** True on `main`, and all three are already fixed by Plan 48's open refresh change (pull request 544). Left to Plan 48.
- **"Three checks go silent when the catalog check fails."** It is eleven, and it is deliberate: `scripts/test_checks.py:204` pins it for Plan 48. Changing it is a verdict change, so it is proposed only (D9).
- **"The wake-up interval contradicts itself" (C4).** ORCH:117 and CCR:82 are about keeping a hosted Codex manager alive; MGR:62 is about a manager's own wake-up. Two timers, not one rule stated twice. They still get one sentence each in one home.
- **"The test scope contradicts itself" (C2).** MGR:61 is a stated special case for merges. It needs one clause in the run contract, not a ruling.
- **"BRIEF:57 says 'process-ledger entry'."** That is the ledger's name. Not stale.
- **"`env/README.md:47` has a machine-local path."** It is the fixed path of every cloud session, quoted in a test result.
- **"The `codex-in-cloud` symlink is clutter."** Plans 29 and 38 link through it and have live runs. Left.
- **The brief's "the oracle pins every verdict".** It pins the always-run checks on the real tree and thirty fixtures. Checks that need a pull request's base are pinned by unit tests only. The tasks say which proof applies.
- **The brief's "words work does not have to wait".** One exception: pull request 544 edits `docs/contribution-workflow.md`, `CONTRIBUTING.md`, two pull request forms and the preambles of `plans/index.md` and `plans/priority.md`. The sweep of those files (CU-14) waits for C-2 so the two changes do not collide.

### Overlap with Plan 48

| Plan 48 item | This project |
| --- | --- |
| The refresh job (PM-8, C-2) | Leaves it. Part 2 waits for it |
| The principle list read from a generated page (raised at its review R2, "not done in Phase 2") | Takes it over as CU-13a and CU-13b. CU-0 adds a note to Plan 48's task list saying so |
| `strategy.md:5` (raised at R2, left to "the owner or the next strategy edit") | Takes it over in CU-9 |
| Track C, the generated completion form (PM-13a, PM-13b, PM-13t; unscheduled) | Leaves it unscheduled. D9 proposes only the smallest part: hints that no longer pass unfilled. If D9 is accepted, CU-0's note says PM-13a's "unfilled form fails" case is done here |
| Phase 4, the evidence envelope (unscheduled) | Leaves it |
| `docs/extending.md` (PM-10e) | Keeps the file where it is; the new skill links to it (D8) |

### Alternatives, including doing less

1. **Do nothing.** The skills keep growing: about fifteen skill changes in two days each added a paragraph where its author was working, and one rule ("Codex workers are the default") was written into four entry points. A run already started a manager layer the owner did not want. Rejected.
2. **Fix only the contradictions and the stale sentences** (CU-2, CU-9, and the settled list from CU-4; about one day). Cheap and safe. It does not stop the next fifteen changes from doing the same thing again. This is the fallback if the owner wants less (D1, option c).
3. **Part 1 only.** Words, glossary, principles and the new skill, with no script change and no new check. Most of the value. Without the word budget check, nothing but habit keeps the skills short (D1, option b).
4. **Parts 1 and 2 as written.** Recommended (D1, option a).
5. **Extend Plan 48 instead of a new pack.** Rejected: Plan 48 has an active run, its own manager and 140 KB of task history, and its subject is records and checks.

Cut from the orchestrator's expected shape, each because nobody has hit a failure it would prevent:

- **One parser.** About 85 regular-expression calls sit in 13 scripts outside `records.py`. Most match content (a release row, a link), not record structure. Moving them is a rewrite with a real risk of changing a verdict.
- **One way to find changed files.** The three callers differ on purpose in two cases (untracked files; renames).
- **A check for "no status word outside the declaration"** and one for "no Markdown parsing outside the record helper". The first would fail on ordinary prose; the second needs the parser rewrite.
- **A generated completion form and an evidence envelope.** Plan 48 holds both unscheduled after two critiques said to wait for a failure.
- **A lock on packs** (D2).
- **Removing a check for the four principle file names** (`canonical-principles`). `scripts/test_checks.py:215` pins its id, and it costs nothing.

### Ambiguity pass

Resolved from the code, no owner decision needed:

- **Which files count as "the skills".** Every `*.md` under `skills/`, not following the `codex-in-cloud` symlink: 17 files, 24,205 words. The five docs counted with them (4,951 words) are the ones a rule could be moved into, so moving words between the two sets cannot fake a cut.
- **Which lines count as "the scripts".** Non-test `scripts/*.py`: 2,948 lines at `1826336`. Tests are proof and are not counted. The baseline is taken again when Part 2 starts, because Plan 48's refresh change alters three scripts first.
- **Where the glossary lives.** Under `skills/`, because the Codex setup copies only that folder, so a glossary in `docs/` would be missing for those workers.
- **Where the table of homes lives.** In the new skill. It is the skill's main content.
- **What "no rule lost" means.** CU-1 lists every rule sentence in the six longest files before any cut. Each later task marks each rule kept, linked or removed as a copy.
- **Whether the principles keep their file.** Yes: 3 skills and docs and 3 plan packs link `docs/contribution-design-principles.md`.
- **Whether a route row for this plan in CA-005 trips the gap boundary check.** No: `check_gap_boundaries.py:boundary_signature` reads the title, the relationships and three sections, not the route table.
- **Whether editing an old pack's `plan.md` re-runs the planning check on it.** Yes, when its `inputs.md` has a `## Planning evidence` section. CU-10 says what to do then.
- **Whether the word "phase" may be used here.** The glossary will define it; this pack says "Part" to avoid leaning on an undefined term.

The eight principles the orchestrator derived were tested against the repository as a proposal:

- "A generated page is never its own source" is true per marked region, not per file: `README.md` and `plans/index.md` mix hand text and generated regions. The principle must say "region".
- "The same command runs every rule locally and in CI" is not true today: the workflows also run the unit tests, a merge-commit guard, the App's parser and the vision publish, and `astrid_dev.py list` shows none of them. The principle must say what is listed, or name the exception.
- "Only its owner changes its pack while it is active" contradicts the catalog's "Owner is accountability, not permission" and cannot be checked while every agent commits as one account (D2).
- "One path through the work" is already principle 1.
- The rest stand. CU-3 keeps a principle only if a recorded failure stands behind it, so the final count may be below eight.

### Estimates

Engineering days, by track:

| Track | Tasks | Days |
| --- | --- | --- |
| Baseline, bookkeeping, the rented-machine fix | CU-0, CU-1, CU-2 | 0.45 |
| Principles | CU-3 | 0.5 |
| Glossary, table of homes, new skill | CU-4, RS1 | 1.0 |
| Applying them to the skills | CU-5, CU-6, CU-7, CU-8 | 2.25 |
| Stale sentences and old packs | CU-9, CU-10 | 0.4 |
| Review of Part 1 | RS2 | 0.4 |
| Script clean-up | CU-11, CU-12 | 0.5 |
| The principle list | CU-13a, CU-13b | 0.9 |
| Docs sweep after C-2 | CU-14 | 0.5 |
| Two checks and their words | CU-15, CU-16, CU-17 | 1.25 |
| Final review | R | 0.4 |
| **Total** | | **8.55** |

Part 1 is 5.0 days and about two and a half elapsed with three workers. Part 2 is 3.55 days and about two elapsed. The proposed tasks under D9 would add 1.0.

### Ten vivid statements

Each is true of the plan as written.

1. Now, a rule lives wherever its author was working. After, each rule has one home and every other mention is a link.
2. Now, "advisor", "owner" and "pack" each mean two or three things. After, one glossary defines every role and unit of work, and no skill has its own Terms section.
3. The eight contribution principles are rewritten from failures people actually hit. A principle with no recorded failure behind it is cut, so there may be fewer than eight.
4. One new skill, `astrid-dev-improve`, is the door for changing astrid-dev itself: start from a recorded failure, find the one home, prove the change, write it in the ledger.
5. The project ends with fewer words in the skills and fewer lines in the scripts than it began with. From then on, whoever adds words to a skill must cut as many or raise one number in the same pull request, where a reviewer sees it.
6. A project still has one owner, and nobody is locked out. Ownership stays a written convention with no lock and no new check (D2, as recommended).
7. A rented GPU machine is always released when a run pauses. This is the first thing fixed, because it is the one contradiction that costs money.
8. Nothing under `scripts/` and no workflow is touched until Plan 48's refresh job is live. The words work starts first.
9. We do not build one parser, one changed-files helper, a generated completion form or an evidence form. Nobody has hit a failure they would prevent.
10. The release skill, the GPU-validation skill, the files of Releases 12 and 13 and every pack with a live run are left exactly as they are. What is wrong in them is reported to the owner, not fixed.

### Critique

Pending. See the Challenge line above.

## Owner decisions

**D1. The scope.** Options: (a) Parts 1 and 2 as written, about 8.5 days; (b) Part 1 only, about 5 days, with no new check; (c) only the contradictions and stale sentences, about 1 day. Recommendation: (a). Part 1 can start at once under any option.

**D2. How project ownership is enforced.** Today: one owner per project, declared once on the plan's `**Owner:**` line. Exclusive editing is not enforced, and the catalog says "Owner is accountability, not permission". 37 of 49 plans are Unassigned, 6 name the shared agent account and 6 name a role. Every agent commits as one shared GitHub account. Options: (a) convention only, written once in the principles and the glossary: while a project is active, others propose changes to its pack by pull request and its owner or the manager running it merges them; (b) the convention plus an advisory check that prints a notice when a pull request edits the pack of an active project it does not name; (c) a real lock, with a generated CODEOWNERS file and required code-owner review. Recommendation: (a). A lock enforces nothing until owners are distinct accounts, and (b) adds a check that cannot tell who is editing. Revisit (c) when owners have their own accounts.

**D3. Rented machines when a run pauses.** Options: (a) the GPU-validation skill's rule wins everywhere: release every pod the run made before pausing, with no exception; (b) keep "release or keep as is safe", and say who decides. Recommendation: (a). A kept pod bills while nobody watches.

**D4. Who merges a manager's progress pull requests.** These change only one plan's `tasks.md`. Options: (a) the manager merges its own, with auto-merge, as a standing rule in the run contract; every other merge still needs the owner's go; (b) every merge needs the owner's standing go, recorded on the `Run start` line. Recommendation: (a). It is what the manage skill already says and what runs do.

**D5. Where a blocking review finding goes after the last agreed round.** Options: (a) straight to the owner, with the manager's recommendation; (b) to the owner through the advisor. Recommendation: (a). The manager answers for the run, and a relay adds a step without adding authority.

**D6. Model family names in the repository.** Exact model IDs are already banned. Options: (a) family names appear in one table only, in the run contract; the copies in the Codex guides become links, and "a specific model name" in the workflow guide and review form becomes "a family name, never an exact ID"; (b) no family names at all: the run contract's table describes each route in words and the mapping lives only in each run's local `run.yaml`; (c) leave as is. Recommendation: (a).

**D7. The false sentence in older packs.** Twelve `plan.md` files say status, owner, priority and estimate live only in the catalog. Options: (a) fix that one sentence in the five open packs with no live run and no place in a running release (Plans 30, 31, 37, 38, 39) and leave the rest until their runs end; (b) fix all twelve now; (c) leave all. Recommendation: (a).

**D8. The extending guide.** Options: (a) keep `docs/extending.md` at its path as the code recipes, trimmed of stale lines; the new skill is the entry point and links to it; (b) move its content into the new skill and delete the file. Recommendation: (a). Plan 48's pack and the gap's closure evidence both link the file, and deleting it means editing a pack with a live run.

**D9. Two proposed changes to what checks accept.** Neither has caused a recorded failure. (1) The completion form's hint text no longer passes the completion check, and `None — TBD` no longer counts as a reason (two tasks, 0.75 days). (2) Ten checks report even when a plan's header is broken, instead of staying silent until it is fixed (one task, 0.25 days; it reverses a behaviour Plan 48 pinned on purpose). Options for each: take it or leave it. Recommendation: take (1), because the completion check is the last gate before a project is called done; leave (2).

**D10. Where this plan sits in the priority order.** It is added last among the open rows, as the planning skill requires. Recommendation: move it above the queued product plans that have no agreed scope, since it changes how every later run reads its instructions. Moving it is the owner's call.

## Source identities

- **Repository:** `banodoco/astrid-dev`. Only this repository changes.
- **Planned against:** `main` at `1826336201f4ec631399d2169b210b1bc22aebe8`, read on 12 Nov 2026.
- **Also read:** Plan 48's refresh change, `int/48-refresh` at `29779a564c40e49a41e232a59d6128c446368bb3` (draft pull request 544). It is not a donor: Part 2 starts from `main` after it has merged.
- **Integration destination:** `int/51-astrid-dev-clean-up`, cut from `main` when a run starts; one pull request to `main` per part.
- **Dirty state:** none. This branch adds only this folder, one line in `plans/priority.md` and what `sync` regenerates.

## References

- [Plan 48's plan, inputs and tasks](../48-one-record-model/tasks.md), for what is already scheduled there.
- [The Plan 48 Phase 2 and 3 run](../../docs/ledger/2026-11-12-plan48-phase2-3-run.md) and [its fix entry](../../docs/ledger/2026-11-12-run-lessons-into-skills.md): what stopped workers last time.
- [Gap CA-005](../../vision/gaps/CA-005-parallel-contribution.md).
- The fact-finders' summary of 12 Nov 2026 was a working file in the orchestrator's session and is not in the repository. Everything a task relies on from it is restated under [what was verified](#prior-art-what-was-verified).

**To report to the owner, not to edit:** `releases/12/decisions.md` and `releases/13/decisions.md` hold model identifiers, a session id and local paths; `releases/13/generation.md` links to headings in `releases/12.md` that no longer exist; Release 12's state differs between `releases/12.md`, its gate record and `releases/13.md`; `docs/proposals/2026-11-05-stopping-early-and-guess-work.md` cites evidence in a private repository; `docs/process-ledger.md` reuses row numbers 43, 44, 47 and 48; `plans/releases.md` has rows for Releases 9 and 10 only; the root README says "four guiding principles" where the vision page says "driving".
