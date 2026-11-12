# Tasks — astrid-dev clean-up

[Plan](plan.md) · [Inputs](inputs.md)

**Not authorized to run.** The owner asked for this project and has not accepted this scope; no `Run start` is recorded in [inputs.md](inputs.md#planning-evidence). The cards are written ready to dispatch. Line numbers are at `main` `1826336`; every card that names a line, a grep or a pinned test is **re-checked against the code at dispatch**.

Routes are **N**, **X**, **S** and **T** per the [run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings). Only astrid-dev changes. Short names (RC, MGR, ORCH, PLAN, ITER, CCR, BRIEF, CCX) are spelled out at the top of [inputs.md](inputs.md#planning-evidence).

**Task ids:** `CU-1`, `CU-2`, …; review stops `RS1`, `RS2`; final review `R`. **Critical path:** Part 1: CU-3 → CU-4 → RS1 → CU-6 → CU-8 → RS2 (CU-7 is the same length as CU-6). Part 2: Plan 48's C-2 → CU-13a → CU-13b → R, with CU-15 → CU-17 → R beside it. **Test inventory:** all nineteen `scripts/test_*.py` files (250 tests, about 50 seconds at `1826336`). Edited or added to: `test_checks.py` (CU-15, CU-16), `test_export_public_vision.py` and possibly `test_views.py` (CU-13a). Must pass unedited in every card: `test_golden.py` and the other fifteen.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Part 1: words. Starts on the owner's go. Touches nothing under `scripts/`, no workflow, and no file that pull request 544 edits** | | | | | |
| CU-0 The gap's route names this plan, and Plan 48's task list says which of its open items moved here | N | D1 | `vision/gaps/CA-005-parallel-contribution.md` (one route row, the critical-path sentence); `plans/48-one-record-model/tasks.md` (two sentences, in a pull request its owner merges) | `check --base` passes; [details](#cu-0) | [ ] |
| CU-1 The baseline: both counts, the list of every rule in the files to be cut, and the list of terms | N | — | `plans/51-astrid-dev-clean-up/evidence/baseline.md` (new); read-only elsewhere | The counts reproduce with the two commands; the manager checks ten rule rows and five term rows against the files; [details](#cu-1) | [ ] |
| CU-2 A pausing run always releases its rented machines | N | D3 | `skills/astrid-dev-orchestrate/codex-in-claude-cloud/codex-runner.sh` (the prompt text at lines 55 and 71 only) | `bash -n` on the file; `grep -rn "keep pods" skills` prints nothing; before and after in the pull request; [details](#cu-2) | [ ] |
| CU-3 The contribution principles, rewritten from the failures people hit | T | — | `docs/contribution-design-principles.md` | Before and after to the owner; a table of principle, failure, example and check id; at most 600 words; `check` passes; [details](#cu-3) | [ ] |
| CU-4 One glossary, one table of homes, the new skill, and the contradictions settled | X | CU-1, CU-3; D3 to D6 for the four rules that are the owner's | `skills/astrid-dev-shared/glossary.md` (new); `skills/astrid-dev-improve/SKILL.md` (new); `skills/astrid-dev/SKILL.md` (one table row); `skills/astrid-dev-shared/run-contract.md` (added sentences, each listed) | Every term and every duplicated rule in the baseline has exactly one home; the settled list with before and after; word limits; `check` passes; [details](#cu-4) | [ ] |
| RS1 Review stop after the principles, the glossary and the table of homes (rounds at most 1). It protects CU-5, CU-6 and CU-7: a wrong home found later means redoing three sweeps | S | CU-3, CU-4 | read-only | Same protocol as R, on those two cards' integrated result; findings become rows `RS1.<n>`; CU-5, CU-6 and CU-7 depend on this row; [what it looks for](#review-rows) | [ ] |
| CU-5 The short skills use the glossary and link to each rule's home | N | RS1 | `skills/astrid-dev-plan/SKILL.md`, `skills/astrid-dev-iterate/SKILL.md`, `skills/astrid-dev/SKILL.md`, `skills/astrid-dev-gap/SKILL.md`, `skills/astrid-dev-bugfix/SKILL.md`, `skills/astrid-dev-merge/SKILL.md`; `evidence/baseline.md` (the status column) | No `## Terms` heading left in them; each baseline rule from these files is marked; the word count is lower than before the card; `check` passes; [details](#cu-5) | [ ] |
| CU-6 The manage skill, cut to at most 3,200 words with no rule lost | X | RS1; D4, D5 | `skills/astrid-dev-manage/SKILL.md`; `evidence/baseline.md` (the status column) | Every baseline rule from this file is marked; the word count; every heading other files link to still exists; `check` passes; [details](#cu-6) | [ ] |
| CU-7 The orchestrate skill and its three guides, cut, with one model table and one statement of the default | X | RS1; D6 | `skills/astrid-dev-orchestrate/SKILL.md`; `codex-in-claude-cloud/README.md` and `manager-brief.md`; `codex-cloud/README.md`; `evidence/baseline.md` (the status column). No `.sh` file | As CU-6, with the orchestrate skill at most 2,900 words; [details](#cu-7) | [ ] |
| CU-8 The wording of the glossary, the new skill and the reworded paragraphs | T | CU-5, CU-6, CU-7 | `skills/astrid-dev-shared/glossary.md`; `skills/astrid-dev-improve/SKILL.md`; in the files of CU-5 to CU-7, only sentences those cards marked "reworded" | Before and after for each sentence; no rule changes meaning; the word count is not higher than before the card; `check` passes; [details](#cu-8) | [ ] |
| CU-9 Five stale sentences and the template's misleading example | N | — | `strategy.md` (line 5); `releases/TEMPLATE.md` (line 22); `vision/gaps/F-001-platform-reliability.md` (line 26); `env/README.md` (line 20 and the script table); `templates/project/plan.md` (the `**Vision gaps:**` line) | `check --base` passes; the whole inventory passes; the template's two example lines are accepted by `plan_gap_ids`; [details](#cu-9) | [ ] |
| CU-10 Five older packs stop saying that status lives only in the catalog | N | D7 | `plans/30-update-everywhere/plan.md`, `plans/31-releases-from-astrid-dev/plan.md`, `plans/37-generate-time-destination/plan.md`, `plans/38-one-process-identity/plan.md`, `plans/39-green-mains/plan.md` (one sentence each) | The grep lists only the packs left on purpose; `check --base` passes; [details](#cu-10) | [ ] |
| RS2 Review stop on the whole of Part 1 before it lands (rounds at most 1). It protects every later run that reads these skills, and CU-14 to CU-17, which build on the table of homes | S | CU-0 to CU-10 | read-only | Same protocol as R, on the integrated head of `int/51-astrid-dev-clean-up` after `main` is merged in and the inventory and `check` pass on CI; findings become rows `RS2.<n>`; then one pull request to `main`, merged on the owner's go; [what it looks for](#review-rows) | [ ] |
| **Part 2: scripts and checks. Starts only when Plan 48's C-2 is on `main`** | | | | | |
| CU-11 Bytecode is no longer tracked | N | C-2 | `scripts/__pycache__/` (three files leave the index); `.gitignore` | `git ls-files "*.pyc"` prints nothing; the inventory run without `PYTHONDONTWRITEBYTECODE` leaves `git status --porcelain` empty; [details](#cu-11) | [ ] |
| CU-12 Dead code goes, and the guard that eleven checks repeat is written once | N | C-2 | `scripts/checks.py` (the eleven guarded checks and one new helper); `scripts/records.py:field_matches`; `scripts/check_docs.py:STATUSES`; the unused imports in `scripts/check_completion.py` and `scripts/check_gap_boundaries.py` | The inventory passes with no test edited; `golden.txt` unchanged; `list` prints the same lines as the base; at least 60 fewer non-test lines; [details](#cu-12) | [ ] |
| CU-13a The principle-list contract, tests first: the public feed takes the principle names and order from the hand-written intro, never from the generated page | X | C-2 | `scripts/test_export_public_vision.py` (added tests); the intro file under `scripts/fixtures/vision/` (one added section); `scripts/test_views.py` (only tests the card lists as made untrue) | The added tests fail only on cases that need CU-13b; everything else passes; [details and what it makes untrue](#cu-13a-and-cu-13b) | [ ] |
| CU-13b Pass the principle-list contract | N | CU-13a | `scripts/export_public_vision.py:build` and the comment at line 215; `vision/intro.md` (one added section) | CU-13a's tests pass unedited; the feed is byte-identical to the base; `sync` reports nothing to update; `golden.txt` unchanged; [details](#cu-13a-and-cu-13b) | [ ] |
| CU-14 The contributor docs use the glossary and link to each rule's home | N | RS2, C-2, CU-11; D6, D8 | `docs/contribution-workflow.md`, `docs/project-format.md`, `docs/contribution-automation-setup.md`, `docs/extending.md`, `CONTRIBUTING.md`, `README.md` (outside the marked regions), `templates/product-pr/review.md`, the hand text of the four forms in `.github/` | Each baseline rule from these files is marked; the word count is lower than before the card; `check --base` passes; `test_review_intake.py` and `test_check_completion.py` pass unedited; [details](#cu-14) | [ ] |
| CU-15 A new check, `skill-words`, added by a fresh worker from the new skill alone | N | RS2 landed on `main`, C-2 | `scripts/checks.py` (one function, one constant, one `REGISTRY` entry); `scripts/test_checks.py` (added tests) | The added tests pass; `list` shows the check; `golden.txt` unchanged; the worker's questions are listed in the pull request; [details](#cu-15) | [ ] |
| CU-16 A new check, `link-anchors`: a link to a heading in a skill, a template or a top-level doc must name a heading that exists | N | C-2 | `scripts/checks.py` (one function, one `REGISTRY` entry); `scripts/test_checks.py` (added tests) | The added tests pass; `list` shows the check; `golden.txt` unchanged; `check` passes on the real tree; [details](#cu-16) | [ ] |
| CU-17 Closing words: the two checks' messages, the check ids in the principles, the skill's fixes from CU-15, and the final budget number | T | CU-15, CU-16 | `scripts/checks.py` (the two checks' strings and the one constant); `scripts/test_checks.py` (only assertions that pin an edited string, each listed); `docs/contribution-design-principles.md`; `skills/astrid-dev-improve/SKILL.md`; `docs/extending.md` | Before and after for every string; the inventory passes; `golden.txt` unchanged; `check` passes; [details](#cu-17) | [ ] |
| R Review rounds (at most 1), on Part 2's integrated head | S | all other tasks in Part 2 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; the pull request to `main` and the completion wait for them; [what it looks for](#review-rows) | [ ] |
| **Proposed only (owner decision D9). Not part of a run unless she takes them** | | | | | |
| CU-18a The completion form contract, tests first: with only the plan number filled in, every field whose rule can tell an answer from a hint fails; `None — TBD` is not a reason | X | D9 (1); C-2 | `scripts/test_check_completion.py` (added tests) | The added tests fail only on cases that need CU-18b; the rest pass unedited; [details](#proposed-cards) | [ ] |
| CU-18b Pass the completion form contract | N | CU-18a | `.github/PULL_REQUEST_TEMPLATE/project-completion.md` (hint text); `scripts/check_completion.py:assess_completion` (line 75) | CU-18a's tests pass unedited; `test_review_intake.py` passes unedited; [details](#proposed-cards) | [ ] |
| CU-19 Ten checks report even when a plan's header is broken | N | D9 (2); CU-12 | `scripts/checks.py` (the helper from CU-12); `scripts/test_checks.py:test_every_other_documentation_rule_skips_a_bad_record` (re-aimed, before and after shown) | [details](#proposed-cards) | [ ] |

## Sizes and who runs each card

Engineering days. "Cheap worker" is a Claude sub-agent on the card's route; the high-judgment sub-agent is a fresh one that has not seen the cards being built.

| Card | In one line | Route | Run by | Depends on | Waits for C-2 | Days |
| --- | --- | --- | --- | --- | --- | --- |
| CU-0 | Gap route row and the note in Plan 48 | N | cheap worker | D1 | no | 0.1 |
| CU-1 | Counts, rule list, term list | N | three cheap workers, one file group each | — | no | 0.25 |
| CU-2 | Rented machines released on pause | N | cheap worker | D3 | no | 0.1 |
| CU-3 | Principles rewritten | T | high-judgment sub-agent | — | no | 0.5 |
| CU-4 | Glossary, table of homes, new skill, settled list | X | X worker with N helpers | CU-1, CU-3 | no | 0.75 |
| RS1 | Review stop on CU-3 and CU-4 | S | high-judgment sub-agent | CU-3, CU-4 | no | 0.25 |
| CU-5 | Short skills swept | N | cheap worker | RS1 | no | 0.5 |
| CU-6 | Manage skill cut | X | X worker with N helpers | RS1 | no | 0.75 |
| CU-7 | Orchestrate skill and guides cut | X | X worker with N helpers | RS1 | no | 0.75 |
| CU-8 | Wording pass | T | high-judgment sub-agent | CU-5, CU-6, CU-7 | no | 0.25 |
| CU-9 | Stale sentences and the template example | N | cheap worker | — | no | 0.15 |
| CU-10 | Five older packs | N | cheap worker | D7 | no | 0.25 |
| RS2 | Review stop on Part 1, then its pull request | S | high-judgment sub-agent | CU-0 to CU-10 | no | 0.4 |
| CU-11 | Bytecode untracked | N | cheap worker | — | yes | 0.1 |
| CU-12 | Dead code and one guard | N | cheap worker | — | yes | 0.4 |
| CU-13a | Principle-list tests | X | X worker | — | yes | 0.5 |
| CU-13b | Principle list passes | N | cheap worker | CU-13a | yes | 0.4 |
| CU-14 | Contributor docs swept | N | cheap worker | RS2, CU-11 | yes | 0.5 |
| CU-15 | `skill-words`, from the skill alone | N | a fresh cheap worker | RS2 on `main` | yes | 0.5 |
| CU-16 | `link-anchors` | N | cheap worker | — | yes | 0.5 |
| CU-17 | Closing words | T | high-judgment sub-agent | CU-15, CU-16 | yes | 0.25 |
| R | Final review, then the pull request | S | high-judgment sub-agent | all of Part 2 | yes | 0.4 |

**Totals by route:** N 3.75 days (44%), X 2.75 (32%), T 1.0 (12%), S 1.05 (12%); 8.55 in all. Cheap and mid-tier workers do 76% of it. The proposed cards would add X 0.5 and N 0.5.

## Dispatch notes

**Recommended manager route: X.** The manager keeps three tracks moving, rules on whether a cut lost a rule, and rules at once when a card meets a pinned test; that is judgment an N manager cannot borrow, and nothing here is deep enough for S.

**The setup, for the `Run start` line.** One Claude session manages and is the accountable agent. It sends each N and X card to a Claude sub-agent on that card's route, as the run contract's table maps it. The owner asked on 12 Nov 2026 for the cheap family on N work and the middle one on X work, so this run does not use Codex workers; say so on the `Run start` line, because Codex workers are otherwise the default. The manager does not do or judge T cards or reviews: CU-3, CU-8, CU-17, RS1, RS2 and R each go to a fresh high-judgment sub-agent.

**Where work lands.** `int/51-astrid-dev-clean-up`, cut from `main` when the run starts; record the commit on the `Run start` line. Each card has its own task branch and worktree, cut from the integration branch and merged back into it. Part 1 goes to `main` as one pull request after RS2. Part 2 starts from `main` after C-2: merge `main` into the integration branch, record that commit as Part 2's base, and take the script line count on it.

**Order.**

- Start CU-1, CU-3 and CU-9 at once. CU-2 and CU-10 start as soon as their decision is made.
- CU-4 follows CU-1 and CU-3. RS1 follows CU-4.
- After RS1, run CU-5, CU-6 and CU-7 side by side. They change different files. Each also marks rows in `evidence/baseline.md`; merge them one at a time and let the later ones merge the integration branch in first.
- CU-8, then RS2, then the pull request.
- In Part 2, CU-11, CU-12, CU-13a and CU-16 start together. CU-12, CU-15 and CU-16 all edit `scripts/checks.py` in different places (the guarded checks; two new functions; the `REGISTRY` tuple). Sharing the tuple is a merge order, not a dependency: whichever merges second merges the branch in and re-runs its proof.

**How to tell C-2 has landed.** On `main`, `python3 scripts/astrid_dev.py list` prints `generated-views pr …` (today it prints `generated-views always …`), and `scripts/export_public_vision.py` has no `--sync-readme` option. If C-2 is late, land Part 1, set this plan's `**Waiting on:**` line, and leave Part 2 queued.

**For every card.**

- Record the card's base commit when it starts. Add commits only.
- The card's brief carries the manager line and the "never use AskUserQuestion" line that the [manage skill](../../skills/astrid-dev-manage/SKILL.md) requires.
- A worker never edits a test or `scripts/fixtures/golden.txt` to get a pass. If its card would make a pinned test, a fixture or an oracle line untrue and the card does not list it, the worker stops and reports the exact lines, and the manager rules at once.
- In a sweep, if removing a copy would lose something its home does not say, the worker stops and reports the sentence. It does not decide.
- Until CU-11 lands, prefix Python commands with `PYTHONDONTWRITEBYTECODE=1`. If tracked bytecode still changes: `git clean -fdq -- env/__pycache__ scripts/__pycache__; git checkout -q -- scripts/__pycache__`.
- Generated pages: before C-2, run `sync` and commit what it writes. After C-2, follow the workflow guide as it then stands; a page refreshes itself on `main`.

**Commands.**

- One test file: `python3 -m unittest discover -s scripts -p "<file>"`. The whole inventory: the same with `"test_*.py"`.
- The checks: `python3 scripts/astrid_dev.py check`. With a base: `python3 scripts/astrid_dev.py check --base <base commit> --body-file /dev/null`. Also `list` and `sync`.
- The oracle: `test_golden.py` passes, and `git diff --stat <base commit> -- scripts/fixtures/golden.txt` prints nothing.
- The same feed: `python3 scripts/export_public_vision.py --revision 0000000000000000000000000000000000000000 --output <file>` on the base and on the candidate, compared with `cmp`.
- Words: the `find … | xargs -0 cat | wc -w` command in [plan.md](plan.md#completion). Script lines: `ls scripts/*.py | grep -v /test_ | xargs cat | wc -l`.

**Load-bearing test moments.** The inventory runs in under a minute, so by the run contract's cost exception the manager runs all of it at each of these: once on the first commit of the integration branch; after each card that touches `scripts/` or a file a test reads (`templates/`, `vision/`, `strategy.md`, the forms); on the integrated head before RS2 and before R; and CI on each pull request to `main`. A card that changes only skills runs `check` and its own proof.

**Other sessions keep editing the skills.** Merge `main` into the integration branch daily during Part 1. For each skill change that arrived, place its rule by the table of homes before RS2. If a change conflicts with a cut, keep the rule and redo the cut.

## Review rows

Each review follows the run contract's protocol: independent of the authors, read-only, on an exact commit range, briefed with the range and these questions and not with the manager's conclusions.

- **RS1** reads CU-3 and CU-4. It looks first for: a principle that is not true of the repository; a principle with no real failure behind it; a term left with two senses; a rule with no home or two; a contradiction "settled" by changing what a rule requires without the settled list saying so; and anything added that could have been a link.
- **RS2** reads the whole of Part 1. It looks first for: a rule lost (it samples twenty rows of `evidence/baseline.md` against the cut files); a link where the reader now needs three hops to learn one rule; a heading that other files link to and that no longer exists; an edit to the release or GPU-validation skill, to a pack with a live run, or to a Release 12 or 13 file; and a word count that went up.
- **R** reads Part 2. It looks first for: a check whose verdict changed with no card saying so (`golden.txt` must be byte-identical to Part 2's base); a test edited that no card lists; non-test script lines above Part 2's base; a question from CU-15's worker that changed nothing; and a `skill-words` budget set looser than the next hundred above the real count.

## Card details

### CU-0

Add to the route table in `vision/gaps/CA-005-parallel-contribution.md`, after step 1: step 2, a link to this plan written as `[Plan 51](../../plans/51-astrid-dev-clean-up/plan.md)`, the contribution "each rule and term has one source; a fresh agent changes astrid-dev from one skill alone", and a milestone name. Use no status word in the row (`queued`, `active`, `blocked`, `paused`, `done`, `cancelled`): the `gap-structure` check refuses them. Update the critical-path sentence under the table. The gap boundary check does not read the route table.

In `plans/48-one-record-model/tasks.md`, add to the note that begins "Raised at R2 (12 Nov 2026) and not done in Phase 2" one sentence saying Plan 51 takes both items (its CU-9 and CU-13). If D9 (1) is taken, add to the PM-13a row that Plan 51's CU-18 covers the unfilled-form case. Plan 48 has a live run, so this goes as its own small pull request that Plan 48's accountable session merges.

### CU-1

One file, `plans/51-astrid-dev-clean-up/evidence/baseline.md`, with three parts.

1. **Counts,** with the commit, the two commands and their output, and `wc -w` for each file under `skills/`.
2. **Rules.** One row for each rule sentence in MGR, ORCH, CCR, BRIEF, CCX and RC, and for each copy of those rules found in PLAN, ITER, the entry, gap, bugfix and merge skills and the five docs counted in the word command. Columns: an id, the file and line, the rule in at most fifteen words, the ids of its copies, and an empty status column that later cards fill with `kept`, `linked to <home>` or `removed, copy of <id>`.
3. **Terms.** Each role and unit-of-work word (owner, maintainer, contributor, orchestrator, advisor, manager, host, accountable agent, lead, worker, helper, reviewer; project, plan, pack, phase, track, task, card, run, route, candidate, check, gate, view, round, stop, release, brief), with each file and line that defines it or uses it in a different sense.

Split by file group across three workers: MGR; ORCH with its three guides; RC and the rest. The release and GPU-validation skills are read for copies and never listed for cutting.

### CU-2

Under D3 option (a), the sentence at `codex-runner.sh:55` becomes: append the question, release every pod this run made and say which, then end with `RUN-STATUS: WAITING`. Line 71 already says to release anything not in use; make it say the same thing in the same words. Change no shell logic. If D3 is decided as (b), the card instead adds who decides and where it is recorded; ask the manager for the wording.

### CU-3

A T card, run by a fresh high-judgment sub-agent.

- **Surface:** `docs/contribution-design-principles.md`, 505 words today, eight principles.
- **Intent:** someone who arrives with no context can act correctly, because each principle names a failure that has happened here and the rule that prevents it.
- **Starting material:** today's eight; the orchestrator's eight in the findings; the four corrections in the [ambiguity pass](inputs.md#ambiguity-pass); the [process ledger](../../docs/ledger/README.md). Treat both lists as proposals. Derive the set again from the failures.
- **Rules:**
  1. No failure, no principle. For each one, name the failure with a pointer: a ledger entry, a line in `inputs.md`, or a file and line.
  2. Each principle has a short name of two to four words, one sentence of rule, one example path in this repository, and either the id of a check from `python3 scripts/astrid_dev.py list` or the word "judgment".
  3. Each is true of the repository when Part 1 lands, or names its exception.
  4. The ownership sentence follows D2. Until D2 is decided, write what is true today: one owner per project, declared once; accountability, not permission.
  5. Plain words, short sentences, at most 600 words in the file.
  6. Keep the last section as a short pointer to where the principles are applied; it will link the new skill.
- **Proof:** the exact before and after, shown to the owner, because her taste decides; a table in the pull request with principle, failure pointer, example path and check id or "judgment"; `check` passes.
- **Note:** three older plans cite principles by number. Do not edit them. New text cites a principle by name.

### CU-4

An X card. The worker keeps the judgment and sends reading and mechanical edits to N helpers.

**The glossary,** `skills/astrid-dev-shared/glossary.md`, at most 450 words. One line per term in CU-1's list. Each definition is the sense most used today. Where two senses are both needed, they become two terms (for example "project pack" and "product pack"; "task route" and "manager's route"). A term that is not needed is listed in the pull request as dropped, with the word that replaces it.

**The new skill,** `skills/astrid-dev-improve/SKILL.md`, at most 600 words, with the same front matter as the other skills:

- **Where things go:** a table of kind of thing, its one home, and what enforces it. At least: a run rule (the run contract); a role's own steps (that role's skill); a term (the glossary); a pack's shape and what a task card holds (the three templates, enforced by `pack-shape`); a check (`scripts/checks.py`, how in `docs/extending.md`); a generated page (`scripts/views.py`); a project fact (the six lines of its `plan.md`); priority (`plans/priority.md`); a principle (the principles doc); friction (the ledger).
- **Steps:** start from a recorded failure (a ledger entry or an issue); find the home in the table; change the home and nothing else; if you add words, cut as many; a change to what a check accepts is its own announced change, with every pinned test, fixture and oracle line it makes untrue listed; prove it with the commands; add a `fix` entry to the ledger.
- **Audit:** at most 120 words. When: a run's ledger entry names friction in the skills, or the owner asks. How: cheap helpers each map one area read-only, then one high-judgment critic checks their claims in the code and judges. Output: ledger entries and at most one proposal. No standing schedule.

**The entry skill** gets one row in its routing table for the new skill.

**The run contract** gains one canonical sentence for each rule that has copies and no home there. At least: add commits only, never rebase or force-push; the merge case where the test scope is every file that touches a changed module (C2); the two timers (C4); the two stopping thresholds, named as different actions; and the outcomes of D3 to D6 once decided. List each added sentence in the pull request. If D3 to D6 are not yet decided, leave those four rules as they are and say so; the manager adds a row when she decides.

**The settled list,** in the pull request body: for C1, C2, C3, C4, the thresholds, the three names for a record of decisions, "principle 7" and T as a manager's route, the before, the after and one line of reason. Settling must not change what any rule requires; if it would, stop and report.

**Proof:** every term in the baseline is in the glossary or on the dropped list; every duplicated rule in the baseline appears in exactly one row of the table; the word limits hold; `check` passes.

### CU-5

For each of the six files: replace every copy of a rule whose home is elsewhere with a link to that home, using the heading link the table of homes gives; replace a `## Terms` section with one line linking the glossary; change nothing else. Mark each affected row in `evidence/baseline.md`. If a copy says something its home does not, stop and report the sentence.

Proof: `grep -c "^## Terms" skills/*/SKILL.md` prints 0 for these files; the word command prints less than before the card; `check` passes (it validates every link target).

### CU-6

An X card. A helper lists the manage skill's rows from the baseline. For each: a run rule becomes a link to the run contract; a rule about a hosted Codex manager becomes a link to that guide; a manage step stays and is shortened. Split the four longest paragraphs (lines 28, 62, 86 and 87) into one bullet per action. Remove the `## Terms` section. Replace "principle 7" with the rule's name. Apply D4 and D5.

Keep every heading that another file links to. At dispatch, run `grep -rn "astrid-dev-manage/SKILL.md#" --include=*.md .` and keep each fragment it shows (`#decide` today).

The target is at most 3,200 words (4,002 today). If a rule would be lost below some higher count, stop there and say which rules set the floor. Mark the reworded sentences for CU-8.

### CU-7

An X card, as CU-6, for four files.

- The orchestrate skill: at most 2,900 words (3,450 today). Line 147's "catalog order" becomes the priority order.
- The route-to-model tables at CCR:7-12 and BRIEF:25-30 become links to the run contract's table, per D6. BRIEF keeps its fill-in lines for a run's own copy.
- "Codex workers are the default" is stated once, in the orchestrate skill's section "Use Codex from Claude Cloud". Its copies at RC:39-40, CCR:3 and :24, BRIEF:3 and MGR:65-66 become links. MGR is CU-6's file: leave that copy to CU-6 and tell the manager.
- C1, C3 and C7 are applied as CU-4 settled them.

Keep every heading other files link to. Many plan packs link into these files; at dispatch, run `grep -rno "astrid-dev-orchestrate/[A-Za-z/.-]*#[a-z0-9-]*" --include=*.md .` and keep each fragment.

### CU-8

A T card, run by a fresh high-judgment sub-agent. Intent: a newcomer understands each definition and each step without opening another file. Taste rules: plain words; short sentences; one word for one thing, as the glossary has it; never change what a rule requires. Return the exact before and after for each sentence.

### CU-9

Exact edits.

- `strategy.md:5`: the sentence that says the catalog alone owns status, priority, estimate and owner becomes: each plan's own `plan.md` holds its status, owner and estimate, `plans/priority.md` holds the order, and the catalog is generated from them. Keep the links.
- `releases/TEMPLATE.md:22`: the same correction to its last sentence.
- `vision/gaps/F-001-platform-reliability.md:26`: the link `../README.md#gaps--15-assessed-outcomes` becomes `../README.md`. The heading it named carries a count that changes.
- `env/README.md:20`: "three commands" becomes the four that `env/cloud-setup.sh` installs, and the script table names every script in `env/` or says which are internal.
- `templates/project/plan.md`, the `**Vision gaps:**` line: show the two exact forms the check accepts. For a gap: a link to the gap file followed by the literal `(primary)`. For no gap: replace the line with `**Vision role:** Foundational enabler — <reason>`, the colon outside the bold, on its own line. Keep it one line, and keep the sentence about small fixes.

Proof: `check --base` passes; the whole inventory passes (some tests read the live tree); and this prints two lists and no error, with each of the template's two example lines pasted in turn as `<line>`:

```text
python3 -c "import sys; sys.path.insert(0,'scripts'); import project_contract as p; print(p.plan_gap_ids('''<line>'''))"
```

### CU-10

In each of the five packs, the sentence "Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md)." becomes the template's current sentence beginning "The six lines above are this project's row". At dispatch, check again which plans have a live run or sit in a running release, and skip those.

Proof: `grep -ln "live \*\*only\*\* in the" plans/*/plan.md` lists only the packs left on purpose (20, 29, 32, 33, 34, 40 and 48 today); `check --base` passes. Editing a `plan.md` re-runs the planning check on a pack whose `inputs.md` has a `## Planning evidence` section. If it fails for a reason older than this edit, revert that pack and list it.

### CU-11

`git rm --cached` the three files under `scripts/__pycache__/`. Add `__pycache__/` and `*.pyc` to `.gitignore`, and reword its first comment so it describes `.otto/` without naming another project. Do not touch the workflow, which sets `PYTHONDONTWRITEBYTECODE` on its own.

### CU-12

No behaviour changes in this card. If any test or any line of `golden.txt` would need an edit, stop and report.

- Remove `records.py:field_matches` (no caller), `check_docs.py:STATUSES` (no reader), and the unused imports: `json` and `subprocess` in `check_completion.py`, `json` in `check_gap_boundaries.py`. Confirm each with a grep at dispatch.
- In `scripts/checks.py`, eleven checks begin with the same guard: return nothing if the catalog check has errors, then call `projects(root)`. In ten of them `rows` is never read, and the call cannot raise once the catalog check has passed. Remove those ten calls and the imports only they used. `_catalog_paths` keeps its call, because it reads `rows`.
- Write the guard once, as one helper the eleven checks use. `scripts/test_checks.py:test_every_other_documentation_rule_skips_a_bad_record` pins the guard's behaviour and must pass unedited.

Proof: the inventory passes with no test edited; `golden.txt` unchanged; `python3 scripts/astrid_dev.py list` prints the same lines as on the base; the script line count is at least 60 lower than on the base.

### CU-13a and CU-13b

Today `export_public_vision.py:build` reads the principle names, order and links from `vision/README.md` (lines 89-92 and 115), which is generated. The pillars are already read from the hand-written `vision/intro.md`.

**CU-13a, tests first.** Add to `test_export_public_vision.py`:

1. `build` reads the principles from a `## Four driving principles` section of the intro file, written as the pillars are in that file: one third-level heading per principle, holding a link from its name to its file under `principles/`.
2. In a temporary copy of the fixture tree, swapping two principle headings in the generated vision page, or deleting that page, gives the same `build` result.
3. Swapping two entries in the intro file changes the order in the result.
4. A principle file whose heading differs from the intro raises an error that names the intro.
5. `render_readme` for the fixture tree is byte-identical to today's.

Add the section to the intro file under `scripts/fixtures/vision/`.

**What it makes untrue.** One error message changes: "principle heading must match README" becomes "principle heading must match the intro". No line of `golden.txt` holds it. At dispatch, list every test in `test_export_public_vision.py` and `test_views.py` that edits a principle heading in a vision README and expects an error or a changed feed; show each before and after in the pull request. If there are none, say so.

**CU-13b.** Make `build` read the intro's section; add the section to the real `vision/intro.md` with the four principles in today's order; correct the comment at line 215. The card touches no test.

Proof: CU-13a's tests pass unedited; the feed is byte-identical to the base; `sync` reports nothing to update for `vision/README.md`; `golden.txt` unchanged; `check` passes.

The `canonical-principles` check, which holds the four file names in `scripts/checks.py`, stays as it is.

### CU-14

As CU-5, for the contributor docs, once C-2 has merged its own edits to them.

- Copies of homed rules become links; terms follow the glossary.
- `docs/contribution-workflow.md:36`: the link `../vision/README.md#gaps--16-assessed-outcomes` becomes `../vision/README.md`.
- `docs/contribution-workflow.md:126` and `templates/product-pr/review.md:13`: "a specific model name" follows D6.
- `docs/extending.md`, under D8 option (a): fix the stale check description at line 11, drop the `PYTHONDONTWRITEBYTECODE=1` prefixes (CU-11 makes them unnecessary), and replace "In this branch" with plain present tense. Keep its three recipes.
- In the four forms under `.github/`, change only hint text. Never change a line a check reads: `Project:`, `Review request:`, and every label in the completion form.

Proof: each baseline rule from these files is marked; the word command prints less than before the card; `check --base` passes; `test_review_intake.py` and `test_check_completion.py` pass unedited.

### CU-15

This card is also the proof that the new skill works. Give a fresh N worker only `skills/astrid-dev-improve/SKILL.md`, `docs/extending.md` and this card. Record every question it asks; each becomes an edit in CU-17.

**The check.** `skill-words`, trigger `always`. It adds up the words (split on white space, as `wc -w` does) of every `*.md` file under `skills/`, counting files with identical content once. It fails when the total is above `SKILL_WORD_BUDGET`, a constant beside it, set to the count on `main` after Part 1 rounded up to the next hundred.

**Why identical files count once.** `skills/astrid-dev-orchestrate/codex-in-cloud` is a symlink to a sibling folder. The oracle and several tests copy the repository with `shutil.copytree`, which turns the link into a second real folder. Counting by content gives the same total in the real tree and in a copy, so `golden.txt` does not change.

**Tests,** added to `test_checks.py`: the check is registered with trigger `always`; a small tree at the budget passes; one word over fails with one error; a tree with no `skills/` folder gives no error; a file copied under a second name is counted once.

**A new verdict, announced.** From the day this reaches `main`, a pull request that takes the skills over the budget fails until it cuts words or raises the constant in the same pull request.

Proof: the added tests pass; `list` shows the check; `golden.txt` unchanged; `check` passes on the real tree.

### CU-16

**The check.** `link-anchors`, trigger `always`. For every Markdown file that `markdown-links` walks, take each local link that has a `#fragment` and whose target is a `.md` file under `skills/` or `templates/`, or directly in `docs/`. A link that is only `#fragment` counts when its own file is in that set. The fragment must be the anchor of a heading in the target. Links into `plans/`, `releases/`, `vision/`, `docs/ledger/`, `docs/handoffs/` and the root files are not checked: 25 are broken there today, in files this project may not edit.

**The anchor rule,** as GitHub renders it: take the heading text without Markdown link syntax or backticks; lowercase it; drop every character that is not a letter, a digit, a space, a hyphen or an underscore; turn each space into a hyphen. A heading that repeats in one file gets `-1`, `-2` and so on.

**Message:** `<file>: link to <target>#<fragment> names no heading there; fix the link or restore the heading`.

**Tests,** added to `test_checks.py`: registered with trigger `always`; a good link passes; a missing heading fails with that message; a repeated heading's `-1` form passes; a heading that holds a link or backticks resolves; a bad fragment into `plans/` is not reported.

**A new verdict, announced.** Renaming a heading in a skill, a template or a top-level doc fails until every link to it is fixed, in whichever pack holds the link.

The planner ran a rough version on `1826336` and found no error in the checked set. Re-check at dispatch. If the real tree has errors, fix the links that are in this plan's scope and report the rest.

Proof: the added tests pass; `list` shows the check; `golden.txt` unchanged; `check` passes on the real tree.

### CU-17

A T card, run by a fresh high-judgment sub-agent.

- **Surfaces:** the description and error message of `skill-words` and of `link-anchors`; the principles doc, where a principle that one of them enforces now names its id; the new skill and `docs/extending.md`, edited for each question CU-15's worker asked.
- **Intent:** each message says what is wrong, where, and the one next step.
- **Also:** set `SKILL_WORD_BUDGET` to the real count on this branch rounded up to the next hundred.
- **What it makes untrue:** only test assertions that pin a string it rewords. List each, before and after.

### Proposed cards

Not part of a run unless the owner takes them under D9.

**CU-18a and CU-18b.** Run on `1826336`: the completion form with only its plan number filled in fails on two fields (`Integrated candidate`, and the `Gap` line's placeholder id) and passes on five hint lines. `Implementation PRs: None — TBD` passes, because `check_completion.py:75` tests the text after "None" with its dash still attached.

- CU-18a adds tests to `test_check_completion.py`: the form file itself, with only the plan number set, fails on `Evidence`, `Completion`, `Implementation PRs`, `Integrated candidate`, `Routes used` and the `Gap` line; `Unproven` is the listed exception, because its rule cannot tell an answer from a hint; `None — TBD` and `None — todo` fail for `Implementation PRs` and `Integrated candidate`; `None — Communication-only project.` still passes. The test that fills each hint with an example (added by Plan 48's PM-13h) must still pass unedited.
- CU-18b rewrites the hints so none satisfies its rule (no example link, no "Yes —", no route letter), and strips the dash before the placeholder test.
- **What it makes untrue:** a completion that passed with `None — TBD` now fails. At dispatch, list every test in `test_check_completion.py` and every line in `scripts/fixtures/` that holds "None —" followed by a placeholder word; at `1826336` there are none.
- The generated form (Plan 48's PM-13b) stays with Plan 48.

**CU-19.** Remove the guard from the ten checks that do not read the catalog rows. In a scratch copy at `1826336` this left the oracle output byte-identical. It makes one test untrue on purpose: `test_checks.py:test_every_other_documentation_rule_skips_a_bad_record`, which Plan 48 wrote to pin the guard. Re-aim it to say that only `catalog-paths` stays silent; show it before and after. In a nearly empty tree several of these checks will now report missing files, so the re-aimed test builds a tree that is whole apart from one broken plan header.
