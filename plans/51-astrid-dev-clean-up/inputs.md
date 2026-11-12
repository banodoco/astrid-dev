# Inputs — astrid-dev clean-up

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

Short names used below: RC is `skills/astrid-dev-shared/run-contract.md`; MGR, ORCH, PLAN, ITER, REL and GPU are the `SKILL.md` of the manage, orchestrate, plan, iterate, release and gpu-validate skills; CCR is `skills/astrid-dev-orchestrate/codex-in-claude-cloud/README.md`, BRIEF is `manager-brief.md` beside it, and CCX is `skills/astrid-dev-orchestrate/codex-cloud/README.md`. Line numbers are at `1826336`.

**Scope decision:** Accepted — Parts 1 and 2, with the completion-form change (D9.1). The owner asked for this project in the [orchestrator's session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF) on 12 Nov 2026 and, shown this scope and its eleven decisions the same day, answered each one ([Owner decisions](#owner-decisions)) and asked for it to go to the manager to farm out.

**Prior art:** Seven read-only fact-finders read `main` at `1826336` on 12 Nov 2026. The planner checked every finding a task relies on against the code on this branch; see [what was verified](#prior-art-what-was-verified) and [what was wrong](#findings-that-were-wrong-or-already-handled). Reused: the [run contract](../../skills/astrid-dev-shared/run-contract.md) as the home of run rules, the [templates](../../templates/project/tasks.md) as the home of shapes, [Plan 48](../48-one-record-model/plan.md)'s check list, oracle and generated pages, the [extending guide](../../docs/extending.md) and the [process ledger](../../docs/ledger/README.md).

**Approach:** A new pack, because no existing plan fits: [Plan 14](../14-repository-cleanup/plan.md) cleans the product repositories and has no agreed scope, and Plan 48 is about records and checks, not rules and words. The work is cut to what has caused a real failure. Part 1 is words only and starts now; Part 2 is scripts and waits for Plan 48's refresh job. See [alternatives](#alternatives-including-doing-less).

**Challenge:** Reviewed — one round on 12 Nov 2026 at commit `e76cdfd7` of this pack's branch ([session](https://claude.ai/code/session_011EzfW38XJUpUFewfUM9MxF)). It was required, because the plan changes astrid-dev's own checks and skills and exceeds five days. One round, 12 Nov 2026: a fresh critic session with no stake in the draft read the pack at commit `e76cdfd` against the code and returned ACCEPT WITH CHANGES, with one blocking finding. The findings and what was accepted are under [Critique](#critique). The revised pack has not had a second round.

**Proof and limits:** A word count taken before and after; a script line count taken before and after Part 2; every deleted sentence listed with the home of its rule and sampled in review; the oracle file unchanged; a fresh worker adding a check from the new skill; and two negative cases. Counts show size, not clarity; clarity is judged in review. The word cut is expected and not proven. See [plan.md](plan.md#completion).

**Review rounds:** Recommend one round at each of three points, all on the S route by a fresh high-judgment sub-agent ([guide](../../skills/astrid-dev-shared/run-contract.md#review-and-promotion-boundaries)): a review stop after the principles, glossary and table of homes (RS1), because three workers then build on them; a review stop on the whole of Part 1 before it lands (RS2), because every agent reads these skills and a lost rule would only show up in a later run; and the final review on Part 2 (R), because it adds a check and changes when another fails. The owner has not confirmed.

**Run start:** 12 Nov 2026. The owner asked for the project to be given to the manager once Plan 48's refresh job was on `main`; it merged that day (`e7c42d9`), so both parts may run, Part 1 first. **Accountable session:** `session_011EzfW3FH6dvD1UHyzGnajf`, the manager ([who answers for a run](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run)). **Manager's route:** X. **Workers:** Claude sub-agents on each card's route, not Codex, as the dispatch notes say; taste and review cards go to a fresh high-judgment sub-agent. **Without asking:** every card, landing on this plan's integration branch, and its own progress updates to `tasks.md`. **Needs a go:** each part's pull request to `main`, merged by the orchestrator under the owner's delegation after its review has no blocking finding and the required checks pass. **Advisor:** the orchestrator, `session_011EzfW38XJUpUFewfUM9MxF`, which also receives a blocking finding left after the last round (D5). **Check-ins:** every three hours from the orchestrator until the project is done or the owner says stop.

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

- **Rules are copied.** "Never rebase or force-push" is in MGR, ORCH, BRIEF and the release skill, and not in RC. The route meanings are in RC:7, RC:13-16, PLAN:63, MGR:14, ORCH:58-63 and CCR:7-12. "Authority comes only from the owner's own message" is in RC:45, ORCH:76 and :96, MGR:81 and others. "Codex workers are the default" is in ORCH:107-114, RC:39-40, CCR:3 and :24, BRIEF:3 and MGR:65-66.
- **Skills conflict in five places.**
  - Rented machines: `codex-runner.sh:55` tells a pausing manager to "release or keep pods as is safe"; GPU:31 says "Release every pod this run made, whatever happened".
  - Merging: MGR:28 has the manager merge its own progress pull requests with auto-merge; ORCH:97 says the session needs the owner's go for merges.
  - A blocking finding left after the last round: RC:104 sends it "to the owner"; MGR:108 says "to the owner through the advisor".
  - Model names: RC:53 bans exact model IDs in the repository; `docs/contribution-workflow.md:126` and `templates/product-pr/review.md:13` allow "a specific model name"; RC:13-16, CCR:7-12 and BRIEF:25-30 each carry a table of family names.
  - Taste work under Codex workers: CCR:12 and RC:16 map it to a Codex family; CCR:28 says it stays on Claude sub-agents.
- **Two thresholds are never said to be different actions.** ITER:23: a worker stops after three attempts or 45 minutes. RC:25: a manager moves a task up a route after two misses or 20 minutes.
- **Words mean several things.**
  - "Advisor" is the orchestrator (MGR:13) or a fresh sub-agent (PLAN:13).
  - "Principle 7" in MGR:109 and BRIEF:55 means the manage skill's own seventh rule, not the seventh contribution principle.
  - "Pack" is a plan's three files and also a product pack.
  - A record of decisions has three names for three things that are never told apart: MGR:41 "decision log" (or a "Rulings" section), RC:71 "decisions ledger", and the inputs template's "Owner decisions".
  - T is a small editorial task in RC:47 and also a manager's route in ORCH:63 ("a project whose outcome is copy").
  - Only PLAN and MGR have a `## Terms` section, and they define "owner" differently. Orchestrator, worker, lead, host, card, phase and track are used and never defined.
- **The skills are long.** 24,205 words in 17 files under `skills/`. MGR is 4,002 words and ORCH 3,450.
- **A generated page is still its own source.** `scripts/export_public_vision.py:89-92` and `:115` read the principle list from `vision/README.md`, which is generated. Swapping two principle headings there passes the checks and changes the public feed. Plan 48's review raised this twice and left it.
- **Dead and repeated code.** `records.py:109` `field_matches` has no caller. `check_docs.py:20` `STATUSES` has no reader. `check_completion.py` imports `json` and `subprocess` and uses neither; `check_gap_boundaries.py` imports `json` and does not use it. In `scripts/checks.py` eleven checks repeat the same seven-line guard, and in ten of them the `rows = projects(root)` call cannot do anything the line before it has not already done.
- **Bytecode is tracked.** Three `.pyc` files under `scripts/__pycache__/` are in git and `.gitignore` has no rule for them, so every task card has to carry a clean-up command. The first comment in `.gitignore` names another project.
- **Stale sentences.** `strategy.md:5` and `releases/TEMPLATE.md:22` say the catalog owns status, priority, estimate and owner. `docs/contribution-workflow.md:36` and `vision/gaps/F-001-platform-reliability.md:26` link to a heading whose name carries an old gap count. `env/README.md:20` says the setup installs three commands; `env/cloud-setup.sh` installs four. Twelve `plan.md` files still say status lives only in the catalog (the finding said sixteen).
- **The template misleads.** `templates/project/plan.md:17` shows `**Vision role: Foundational enabler**` with the colon inside the bold. `scripts/project_contract.py:9` needs `**Vision role:**` at the start of its own line, and counts the literal `(primary)`, which the template never shows.
- **The completion form passes half-filled.** Run on this branch: with only the plan number filled in, the form fails on two fields and passes on five hint lines. `Implementation PRs: None — TBD` passes, because the dash is not stripped before the placeholder test (`check_completion.py:75`). No recorded failure came from this, so it is proposed only (D9).
- **`check` does not look at the part of a link after `#`.** `scripts/check_docs.py:local_links` checks that the file exists. A rough script found no link pointing to a missing heading in `skills/`, `templates/` or a top-level `docs/` file, and about two dozen broken ones elsewhere, all pointing into plan packs, release files, the root README or the generated vision page.
- **An experiment, run in a scratch copy on 12 Nov 2026.** Removing the guard from ten checks leaves the oracle output byte-identical. The critic repeated it with the same result.

### Findings that were wrong or already handled

- **"The gap outcome words are declared twice and differ."** Wrong. `export_public_vision.py:22` lists a gap's states; `check_completion.py:17` lists what a completion may say about a gap. They are two lists for two things.
- **"`plans/02-consistent-generation/env/` is an orphan with diverged copies."** Wrong. `env/README.md:62` says those copies are frozen on purpose for Plan 02's recorded proof, and Plan 06 links them.
- **"An unedited inputs template passes the planning check."** True and intended: a draft keeps the template's `Pending — … Next: …` lines.
- **"The default pull request form lacks the two intake lines."** It tells the author to add them, which the setup guide allows.
- **"Two generators and two repair commands for the vision page", "the docs recommend `--sync-readme`", "the claim form asks for two files and the bot accepts one".** True on `main`, and all three are already fixed by Plan 48's open refresh change (pull request 544). Left to Plan 48.
- **"Three checks go silent when the catalog check fails."** It is eleven, and it is deliberate: `scripts/test_checks.py:204` pins it for Plan 48. Changing it is a verdict change, so it is proposed only (D9).
- **"Installing skills for Codex contradicts itself."** CCR:22 deletes and copies; CCX:9-17 says never remove existing skills. They are for two environments: a fresh Claude cloud container, and a Codex Cloud workspace that persists. Each guide gets one line saying which it is for.
- **"The wake-up interval contradicts itself."** ORCH:117 and CCR:82 are about keeping a hosted Codex manager alive; MGR:62 is about a manager's own wake-up. Two timers.
- **"The test scope contradicts itself."** MGR:61 is a stated special case for merges. It needs one clause in the run contract, not a ruling.
- **"BRIEF:57 says 'process-ledger entry'."** That is the ledger's name. Not stale.
- **"`env/README.md:47` has a machine-local path."** It is the fixed path of every cloud session, quoted in a test result.
- **"The `codex-in-cloud` symlink is clutter."** Plans 29 and 38 link through it, and Plan 29 has a live run. Left.
- **The brief's "the oracle pins every verdict".** It pins the always-run checks on the real tree and thirty fixtures. Checks that need a pull request's base are pinned by unit tests only. The tasks say which proof applies.
- **The brief's "words work does not have to wait".** One exception: pull request 544 edits `docs/contribution-workflow.md`, `CONTRIBUTING.md`, two pull request forms and the preambles of `plans/index.md` and `plans/priority.md`. The sweep of those files (CU-14) waits for C-2 so the two changes do not collide.

### Overlap with Plan 48

| Plan 48 item | This project |
| --- | --- |
| The refresh job (PM-8, C-2) | Leaves it. Part 2 waits for it |
| The principle list read from a generated page (raised at its review R2 and noted twice in its task list as not done) | Takes it over as CU-13a and CU-13b. CU-0 adds a sentence to both notes in Plan 48's task list |
| `strategy.md:5` (raised at R2, left to "the owner or the next strategy edit") | Takes it over in CU-9 |
| Track C, the generated completion form (PM-13a, PM-13b, PM-13t; unscheduled) | Leaves it unscheduled. D9 proposes only the smallest part: hints that no longer pass unfilled. If that is taken, CU-0's note says PM-13a's "unfilled form fails" case is done here |
| Phase 4, the evidence envelope (unscheduled) | Leaves it |
| `docs/extending.md` (PM-10e) | Keeps the file where it is and brings it up to date; the new skill links to it (D8) |

### Alternatives, including doing less

1. **Do nothing.** The skills keep growing: about fifteen skill changes in two days each added a paragraph where its author was working (the orchestrator's own count, not re-checked), and one rule, "Codex workers are the default", is written in five files. A run already started a manager layer the owner did not want ([ledger](../../docs/ledger/2026-11-12-plan48-phase2-3-run.md)). Rejected.
2. **Fix only the conflicts and the stale sentences** (CU-2, CU-9, and the settled list from CU-4; about one day). Cheap and safe. It does not stop the next fifteen changes from doing the same thing again. This is the fallback if the owner wants less (D1, option c).
3. **Part 1 only.** Words, glossary, principles and the new skill, with no script change and no new check. Most of the value (D1, option b).
4. **Parts 1 and 2 as written.** Recommended (D1, option a).
5. **Extend Plan 48 instead of a new pack.** Rejected: Plan 48 has an active run, its own manager and 140 KB of task history, and its subject is records and checks.

Cut from the orchestrator's expected shape, each because nobody has hit a failure it would prevent or because it adds more than it removes:

- **One parser.** About 85 regular-expression calls sit in 13 scripts outside `records.py`. Most match content (a release row, a link), not record structure. Moving them is a rewrite with a real risk of changing a verdict.
- **One way to find changed files.** The three callers differ on purpose in two cases (untracked files; renames).
- **A check for "no status word outside the declaration"** and one for "no Markdown parsing outside the record helper". The first would fail on ordinary prose; the second needs the parser rewrite.
- **A generated completion form and an evidence envelope.** Plan 48 holds both unscheduled after two critiques said to wait for a failure.
- **A lock on packs** (D2).
- **A fixed word budget for the skills,** checked on every run. Dropped at the critique: two pull requests that each pass can together break `main` for everyone. A smaller form is proposed under D9.
- **A list of every rule in every skill.** Several hundred rows written by cheap workers would be the largest thing the project makes, and a rule missing from the list could be lost while the proof still passed. Each sweep lists what it deletes instead.
- **Removing the check for the four principle file names** (`canonical-principles`). `scripts/test_checks.py:215` pins its id, and it costs nothing.

### Ambiguity pass

Resolved from the code, no owner decision needed:

- **Which files count as "the skills".** Every `*.md` under `skills/`, not following the `codex-in-cloud` symlink: 17 files, 24,205 words. The five docs counted with them (4,951 words) are the ones a rule could be moved into, so moving words between the two sets cannot fake a cut. The count is taken with `LC_ALL=C`; another locale gives 29,208 for the same files.
- **Which lines count as "the scripts".** Non-test `scripts/*.py`: 2,948 lines at `1826336`. Tests are proof and are not counted. The baseline is taken again when Part 2 starts, because Plan 48's refresh change alters three scripts first.
- **Where the glossary lives.** Under `skills/`, because the Codex setup copies only that folder, so a glossary in `docs/` would be missing for those workers.
- **Where the table of homes lives.** In the new skill. It is the skill's main content.
- **What "no rule lost" means.** Each card that deletes or moves a sentence lists it with the home of its rule. The review of Part 1 samples the lists against the diff and looks for deletions no list mentions.
- **How a card proves it broke no heading link before the new check exists.** A thirty-line script in the [dispatch notes](tasks.md#dispatch-notes), run from outside the repository.
- **Whether the principles keep their file.** Yes: the entry skill, the root README, the workflow guide, gap CA-005 and three plan files link `docs/contribution-design-principles.md`.
- **Whether a route row for this plan in CA-005 trips the gap boundary check.** No: `check_gap_boundaries.py:boundary_signature` reads the title, the relationships and three sections, not the route table.
- **Whether a registered check's generated page must be committed after C-2.** It may be: C-2 lets a pull request carry a correctly regenerated page. The cards run `sync` and commit `docs/checks.md`.
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
| Baseline, bookkeeping, the rented-machine fix | CU-0, CU-1, CU-2 | 0.4 |
| Principles | CU-3 | 0.5 |
| Glossary, table of homes, new skill | CU-4, RS1 | 1.0 |
| Applying them to the skills | CU-5, CU-6, CU-7, CU-8 | 2.25 |
| Stale sentences | CU-9 | 0.15 |
| Review of Part 1 | RS2 | 0.4 |
| Script clean-up | CU-11, CU-12 | 0.5 |
| The principle list | CU-13a, CU-13b | 0.9 |
| Docs sweep after C-2 | CU-14 | 0.5 |
| One check and its words | CU-15, CU-16 | 0.65 |
| Final review | R | 0.4 |
| **Total** | | **7.65** |

Part 1 is 4.7 days and about two and a half elapsed with four workers. Part 2 is 2.95 days and about two elapsed. The proposed cards under D7 and D9 would add 1.75.

### Ten vivid statements

Each is true of the plan as written.

1. Now, a rule lives wherever its author was working. After, each rule has one home and every other mention is a link.
2. Now, "advisor", "owner" and "pack" each mean two or three things. After, one glossary defines every role and unit of work, and no skill has its own Terms section.
3. The eight contribution principles are decided again from failures people actually hit. A principle with no recorded failure behind it is cut, so there may be fewer than eight.
4. One new skill, `astrid-dev-improve`, is the door for changing astrid-dev itself: start from a recorded failure, find the one home, prove the change, write it in the ledger.
5. The project must end with fewer words in the skills than it began with, and that is expected, not proven: the new glossary and skill add about a thousand words before any cut is made.
6. After the project, nothing but the new skill's rule and an occasional audit stops the skills growing back. A check that would ask for a reason is proposed, not committed.
7. A project still has one owner, and nobody is locked out. Ownership stays a written convention with no lock and no new check (D2, as recommended).
8. A rented GPU machine is always released when a run pauses. This is the first thing fixed, because it is the one conflict that costs money (D3, as recommended).
9. One new check arrives, and it bites other people's packs: renaming a heading in a skill fails `check` until every link to it is fixed, wherever the link is.
10. We do not build one parser, a generated completion form or an evidence form, and we do not touch the release skill, the GPU-validation skill, the files of Releases 12 and 13 or any pack with a live run. What is wrong there is reported to the owner, not fixed.

### Critique

One round, 12 Nov 2026. A fresh session, started with no context but its brief, read the three files at commit `e76cdfd` and checked them against the code, running the checks, the 250 tests and its own prototypes in a scratch copy. Its brief: build as little as possible; verify claims in the code, not in the summary; find any card that would change a check's verdict unannounced, any card a cheap worker cannot run, and anything that adds more than it removes. Verdict: **ACCEPT WITH CHANGES.**

| Finding | Severity | What was done |
| --- | --- | --- |
| 1. A word budget checked on every run lets two passing pull requests together turn `main` red, applies to the release skills mid-release, and makes every skill edit touch one script | blocking | Accepted. The check is out of the committed scope. A smaller form that compares a pull request with its own base is proposed under D9 (CU-19). The fresh-worker proof moved to `link-anchors` |
| 2. The principle-list cards change when `public-vision-content` fails, not only one message | should-fix | Accepted. CU-13a lists all three changes and widens the tests a worker must look for |
| 3. A "byte-identical to today's" test has no stored snapshot to compare with | should-fix | Accepted. The test is dropped; CU-13b's feed comparison covers it |
| 4. CU-7 was told to edit the run contract, which is outside its scope | should-fix | Accepted. That edit moved to CU-4; the manage skill's copy moved to CU-6 |
| 5. "Settling must not change what a rule requires" cannot hold for a real conflict; two items in the settled list were not in this file | should-fix | Accepted. CU-4 now carries a ruling for each conflict, the two items are restated above with file and line, and taste work under Codex became D11 |
| 6. Deciding the set of principles is not a T task; a T card may not set a number or edit a skill's content | should-fix | Accepted. CU-3 is an S card; wording moved to CU-8; CU-16 is words only |
| 7. Changing `codex-runner.sh:71` would tell a continuing run to release machines it is using | should-fix | Accepted. CU-2 edits line 55 only |
| 8. "At least 1,500 fewer words" rested on cuts with escape hatches against certain additions | should-fix | Accepted. The requirement is "fewer than today"; the plan says the margin is expected, not proven; the three guides got a number |
| 9. "Fewer script lines" holds by about twenty lines; "at least 60 fewer" invites squeezing code | should-fix | Accepted. The 60 is gone, the margin is stated, and the review looks for squeezed code |
| 10. A list of every rule is the largest thing the project writes and does not prove completeness | should-fix | Accepted. CU-1 lists only terms and duplicated rules; each sweep lists what it deletes |
| 11. `check` does not validate the part of a link after `#`, and the greps in three cards missed real links | should-fix | Accepted. A script in the dispatch notes is the proof in every Part 1 card that touches a skill, and in RS2 |
| 12. The word count depends on the locale | should-fix | Accepted. The command carries `LC_ALL=C` |
| 13. The cards that register a check ignored the generated check page, and the fresh worker would get a stale guide | should-fix | Accepted. `docs/checks.md` is in scope; CU-15 depends on CU-14, which brings the guide up to date |
| 14. Four claims here were off: the Codex install "contradiction" is two environments; Plan 38 has no live run; the broken-link count; the refresh branch's head | note | Accepted. All four corrected |
| 15. Plan 48 states the principle-list follow-up twice; CU-10 copies a sentence that C-2 makes partly unnecessary | note | Accepted. CU-0 edits both notes. CU-10 is now proposed only |
| 16. The `Contributes to closure` line is written before the gap's route names the plan; the second table repeated route and dependencies; RS2 named a card that does not depend on it; CU-8 spanned twelve files; "only the new skill" was not what the card gives the worker | note | Mostly accepted. The second table lost the repeated columns; RS2, CU-8 and the completion text are corrected. The `Contributes to closure` line is kept and now says plainly that the route row is still to be added (CU-0): the planner was told to change no gap file |
| 17. Nobody has hit a failure from the stale sentence in five older packs | note | Accepted. CU-10 is proposed only and D7 now recommends leaving them |

The critic also suggested that `link-anchors` as a permanent check is optional, since the script covers the cuts. It is kept: after this project many more links point at headings, nothing else notices when one breaks, and two such links are already broken. That is the planner's call and the owner can cut it under D1.

**What the critic confirmed in the code:** the counts; that removing the guard leaves the oracle unchanged; the dead code; that a prototype `link-anchors` gives no error on the real tree or any fixture; that adding a section to the intro changes neither the feed nor the generated page; that Part 1 touches no file pull request 544 edits; and the line references it sampled. **What it did not check:** the completion-form claims behind CU-17; the regular-expression count; whether the word targets for the two long skills are reachable; the workflow on the refresh branch.

## Owner decisions

**D1. The scope.** Options: (a) Parts 1 and 2 as written, about 7.5 days; (b) Part 1 only, about 4.7 days, with no script change and no new check; (c) only the conflicts and stale sentences, about 1 day. Recommendation: (a). Part 1 can start at once under any option. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** (a), both parts. She asked the orchestrator whether it agreed with both; it did, and she asked for the project to go to the manager.

**D2. How project ownership is enforced.** Today: one owner per project, declared once on the plan's `**Owner:**` line. Exclusive editing is not enforced, and the catalog says "Owner is accountability, not permission". 37 of 49 plans are Unassigned, 6 name the shared agent account and 6 name a role. Every agent commits as one shared GitHub account. Options: (a) convention only, written once in the principles and the glossary: while a project is active, others propose changes to its pack by pull request and its owner or the manager running it merges them; (b) the convention plus an advisory check that prints a notice when a pull request edits the pack of an active project it does not name; (c) a real lock, with a generated CODEOWNERS file and required code-owner review. Recommendation: (a). A lock enforces nothing until owners are distinct accounts, and (b) adds a check that cannot tell who is editing. Revisit (c) when owners have their own accounts. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** convention only, for now.

**D3. Rented machines when a run pauses.** Options: (a) the GPU-validation skill's rule wins everywhere: release every pod the run made before pausing, with no exception; (b) keep "release or keep as is safe", and say who decides. Recommendation: (a). A kept pod bills while nobody watches. **Decided, 12 Nov 2026, by the orchestrator under the owner's delegation:** (a), always release. The owner asked what a rented pod is and did not choose; (a) is the option that cannot cost money, and she may reverse it.

**D4. Who merges a manager's progress pull requests.** These change only one plan's `tasks.md`. Options: (a) the manager merges its own, with auto-merge, as a standing rule in the run contract; every other merge still needs the owner's go; (b) every merge needs the owner's standing go, recorded on the `Run start` line. Recommendation: (a). It is what the manage skill already says and what runs do. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** (a). The manager merges its own progress updates; the owners decide how a project's result goes into a release.

**D5. Where a blocking review finding goes after the last agreed round.** Options: (a) straight to the owner, with the manager's recommendation; (b) to the owner through the advisor. Recommendation: (a). The manager answers for the run, and a relay adds a step without adding authority. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** neither option as written: a blocking finding after the last round goes straight to the orchestrator, who rules under the owner's delegation or takes it to her. Where a run has no orchestrator, it goes to the owner.

**D6. Model family names in the repository.** Exact model IDs are already banned. Options: (a) family names appear in one table only, in the run contract; the copies in the Codex guides become links, and "a specific model name" in the workflow guide and review form becomes "a family name, never an exact ID"; (b) no family names at all: the run contract's table describes each route in words and the mapping lives only in each run's local `run.yaml`; (c) leave as is. Recommendation: (a). **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** (a).

**D7. The false sentence in older packs.** Twelve `plan.md` files say status, owner, priority and estimate live only in the catalog. Options: (a) fix that one sentence in the five open packs with no live run and no place in a running release (Plans 30, 31, 37, 38, 39) and leave the rest until their runs end (CU-10); (b) fix all twelve now; (c) leave all. Recommendation: (c). Nobody has hit a failure from it, a hand edit to the catalog already fails with a message naming the real source, and each edit re-runs the planning check on an old pack. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** as recommended: leave the older packs. CU-10 is not taken.

**D8. The extending guide.** Options: (a) keep `docs/extending.md` at its path as the code recipes, brought up to date; the new skill is the entry point and links to it; (b) move its content into the new skill and delete the file. Recommendation: (a). Plan 48's pack and the gap's closure evidence both link the file, and deleting it means editing a pack with a live run. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** (a), on condition that the guide is up to date and is linked from every place that should point to it. CU-14 carries that condition.

**D9. Three proposed changes to what checks accept.** None answers a recorded failure of a check.

1. The completion form's hint text no longer passes the completion check, and `None — TBD` no longer counts as a reason (CU-17a and CU-17b, 0.75 days).
2. Ten checks report even when a plan's header is broken, instead of staying silent until it is fixed (CU-18, 0.25 days). It reverses a behaviour Plan 48 pinned on purpose.
3. A check that asks for a one-line reason in the pull request description when a pull request adds words to the skills (CU-19, 0.5 days). It adds a step for every author who lengthens a skill.

Options for each: take it or leave it. Recommendation: take (1), because the completion check is the last gate before a project is called done; leave (2); take (3) only if the skills grow again after Part 1 lands, since its design has not been through a critique. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** as recommended: take (1), so CU-17a and CU-17b join Part 2; leave (2); (3) only if the skills grow back.

**D10. Where this plan sits in the priority order.** It is added last among the open rows, as the planning skill requires. Recommendation: move it above the queued product plans that have no agreed scope, since it changes how every later run reads its instructions. Moving it is the owner's call. **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** as recommended. Its line in `plans/priority.md` sits directly above `11-threejs-pack`, the first of the queued plans without an agreed scope.

**D11. Taste work when a run's workers are on Codex.** Options: (a) it stays on Claude sub-agents at the high-judgment tier, as CCR:28 says and as Plan 48's runs did; the Codex column for T in the run contract's table then applies only when a Codex manager runs the project, and the table says so; (b) it goes to the Codex family the table names, and CCR:28 is removed. Recommendation: (a). **Decided, 12 Nov 2026 (the owner, in the orchestrator's session):** taste work may run on the Codex taste family, and Claude is recommended.

## Source identities

- **Repository:** `banodoco/astrid-dev`. Only this repository changes.
- **Planned against:** `main` at `1826336201f4ec631399d2169b210b1bc22aebe8`, read on 12 Nov 2026.
- **Also read:** Plan 48's refresh change, `int/48-refresh` at `29779a564c40e49a41e232a59d6128c446368bb3` (draft pull request 544). The branch has moved since. It is not a donor: Part 2 starts from `main` after it has merged.
- **Integration destination:** `int/51-astrid-dev-clean-up`, cut from `main` when a run starts; one pull request to `main` per part.
- **Dirty state:** none. This branch adds this folder and one line in `plans/priority.md`, and carries what `sync` regenerates: `plans/index.md` and the project count in the root `README.md`.

## References

- [Plan 48's plan, inputs and tasks](../48-one-record-model/tasks.md), for what is already scheduled there.
- [The Plan 48 Phase 2 and 3 run](../../docs/ledger/2026-11-12-plan48-phase2-3-run.md) and [its fix entry](../../docs/ledger/2026-11-12-run-lessons-into-skills.md): what stopped workers last time.
- [Gap CA-005](../../vision/gaps/CA-005-parallel-contribution.md).
- The fact-finders' summary of 12 Nov 2026 was a working file in the orchestrator's session and is not in the repository. Everything a task relies on from it is restated under [what was verified](#prior-art-what-was-verified).
- The critique was the final message of a separate read-only session on 12 Nov 2026; its findings are restated in full under [Critique](#critique).

**To report to the owner, not to edit.** Reported by the fact-finders; only the first two were re-checked here.

- `docs/process-ledger.md` reuses row numbers 43, 44, 47 and 48.
- The root README says "four guiding principles" where the vision page says "driving"; a test pins the wording.
- `releases/12/decisions.md` and `releases/13/decisions.md` hold model identifiers, a session id and local paths.
- `releases/13/generation.md` links to headings in `releases/12.md` that no longer exist.
- Release 12's state differs between `releases/12.md`, its gate record and `releases/13.md`.
- `docs/proposals/2026-11-05-stopping-early-and-guess-work.md` cites evidence in a private repository.
- `plans/releases.md` has rows for Releases 9 and 10 only.
