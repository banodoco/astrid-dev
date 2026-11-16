# Tasks — astrid-dev clean-up

[Plan](plan.md) · [Inputs](inputs.md)

**Run started 12 Nov 2026** (see the `Run start` line in [inputs.md](inputs.md#planning-evidence)); progress is ticked below as cards land on `int/51-astrid-dev-clean-up` (Part 1) and `int/51-part2` (Part 2). The cards are written ready to dispatch. Line numbers are at `main` `1826336`; every card that names a line, a grep or a pinned test is **re-checked against the code at dispatch**.

Routes are **N**, **X**, **S** and **T** per the [run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings). Only astrid-dev changes. Short names (RC, MGR, ORCH, PLAN, ITER, CCR, BRIEF, CCX) are spelled out at the top of [inputs.md](inputs.md#planning-evidence).

**Task ids:** `CU-1`, `CU-2`, …; review stops `RS1`, `RS2`; final review `R`. **Critical path:** Part 1: CU-3 → CU-4 → RS1 → CU-6 → RS2 (CU-7 is the same length as CU-6). Part 2: Plan 48's C-2 → CU-11 → CU-14 → CU-15 → CU-16 → R. **Test inventory:** all nineteen `scripts/test_*.py` files (250 tests, about 50 seconds at `1826336`). Added to: `test_checks.py` (CU-15) and `test_export_public_vision.py` (CU-13a). Possibly re-aimed, each test listed first: `test_views.py` (CU-13a). Must pass unedited in every card: `test_golden.py` and the other fifteen.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Part 1: words. Starts on the owner's go. Touches nothing under `scripts/`, no workflow, and no file that pull request 544 edits** | | | | | |
| CU-0 The gap's route names this plan, and Plan 48's task list says which of its open items moved here | N | D1 | `vision/gaps/CA-005-parallel-contribution.md` (one route row, the critical-path sentence); `plans/48-one-record-model/tasks.md` (one sentence in each of two notes, in a pull request its owner merges) | `check --base` passes; [details](#cu-0) | [x] 12 Nov: the gap route (CU-0a) merged with Part 1; the Plan 48 sentences (CU-0b) merged as PR 561 |
| CU-1 The baseline: the word count, the list of terms, and the rules that are written in more than one place | N | — | `plans/51-astrid-dev-clean-up/evidence/baseline.md` (new); read-only elsewhere | The count reproduces with the command; the manager checks five term rows and five rule rows against the files; [details](#cu-1) | [x] 12 Nov: baseline.md and baseline-rules.md on `int/51-astrid-dev-clean-up` (merges 0a09051, 989369a); 29,410 words at `195586c` |
| CU-2 A pausing run always releases its rented machines | N | D3 | `skills/astrid-dev-orchestrate/codex-in-claude-cloud/codex-runner.sh` (the prompt text at line 55 only) | `bash -n` on the file; `grep -rn "keep pods" skills` prints nothing; before and after in the pull request; [details](#cu-2) | [x] 12 Nov: merged on `int/51-astrid-dev-clean-up` (21a9f9a); the sentence is now at codex-runner.sh:57 |
| CU-3 The contribution principles, decided again from the failures people hit | S | — | `docs/contribution-design-principles.md` | Before and after to the owner; a table of principle, failure, example and check id; at most 600 words; `check` and the anchor proof pass; [details](#cu-3) | [x] 12 Nov: merged on `int/51-astrid-dev-clean-up` (98b747a); ten principles, 599 words after RS1 and CU-8 |
| CU-4 One glossary, one table of homes, the new skill, and the conflicts settled as this card rules | X | CU-1, CU-3; D3 to D6 and D11 for the five rules that are the owner's | `skills/astrid-dev-shared/glossary.md` (new); `skills/astrid-dev-improve/SKILL.md` (new); `skills/astrid-dev/SKILL.md` (one table row); `skills/astrid-dev-shared/run-contract.md` (added sentences, each listed; lines 39-40) | Every term and every duplicated rule in the baseline has exactly one home; the settled list with before and after; word limits; `check` and the anchor proof pass; [details](#cu-4) | [x] 12 Nov: merged (e9081de); glossary 450 words, improve skill 557 |
| RS1 Review stop after the principles, the glossary and the table of homes (rounds at most 1). It protects CU-5, CU-6 and CU-7: a wrong home found later means redoing three sweeps | S | CU-3, CU-4 | read-only | Same protocol as R, on those two cards' integrated result; findings become rows `RS1.<n>`; CU-5, CU-6 and CU-7 depend on this row; [what it looks for](#review-rows) | [x] 12 Nov: 2 blocking, 10 should-fix, notes; all applied or ruled, rows below |
| RS1.1 to RS1.13, RS1.16 Findings of the review stop: the owner entry had two senses (blocking); the run-rule row had no headings (blocking); principle 5's check, principle 2's exception, principle 7's failure pointer, the plan, check and advisor terms, the model-family sentence, the worker-stop home, a second home for the no-edit rule, the D11 wording | X | RS1 | the five CU-3/CU-4 files and one baseline row | Fixed on `int/51-astrid-dev-clean-up` (task/51-rs1fix, 927dc79); anchor proof, `check` and the inventory pass; [details](#review-rows) | [x] 12 Nov: merged (ad4e527). RULING: advisor = the orchestrator, or where there is none a fresh high-judgment sub-agent. Open: the owner's question on restoring "drafts can be incomplete; templates ask only what helps the next agent act" (the reviewer recommends leaving it out). RS1.14 to RS1.17 were notes for CU-5 and CU-15/16, applied there or left |
| CU-5 The short skills use the glossary and link to each rule's home | N | RS1 | `skills/astrid-dev-plan/SKILL.md`, `skills/astrid-dev-iterate/SKILL.md`, `skills/astrid-dev/SKILL.md`, `skills/astrid-dev-gap/SKILL.md`, `skills/astrid-dev-bugfix/SKILL.md`, `skills/astrid-dev-merge/SKILL.md` | No `## Terms` heading left in them; every deleted sentence listed with its home; the word count is lower than before the card; `check` and the anchor proof pass; [details](#cu-5) | [x] 12 Nov: merged (3cef655); six-file words 5,847 to 5,424; bugfix skill needed no change |
| CU-6 The manage skill, cut toward 3,200 words with no rule lost | X | RS1; D4, D5 | `skills/astrid-dev-manage/SKILL.md` | Every deleted or moved sentence listed with its home; the word count; `check` and the anchor proof pass; [details](#cu-6) | [x] 12 Nov: merged (593ef1d); manage skill 4,016 to 3,383 words, floor listed in the report (aim 3,200 not reached) |
| CU-7 The orchestrate skill and its three guides, cut, with one model table and one statement of the default | X | RS1; D6, D11 | `skills/astrid-dev-orchestrate/SKILL.md`; `codex-in-claude-cloud/README.md` and `manager-brief.md`; `codex-cloud/README.md`. No `.sh` file | As CU-6, with the orchestrate skill toward 2,900 words and the three guides together below 4,578; [details](#cu-7) | [x] 12 Nov: merged (3931b58); orchestrate skill 3,450 to 2,965 (aim 2,900 not reached), three guides 4,812 to 4,523 |
| CU-8 The wording of the three new or rewritten documents | T | CU-3, CU-4, RS1 | `docs/contribution-design-principles.md`; `skills/astrid-dev-shared/glossary.md`; `skills/astrid-dev-improve/SKILL.md` | Before and after for each sentence; no rule, definition or home changes; the word count is not higher than before the card; `check` and the anchor proof pass; [details](#cu-8) | [x] 12 Nov: merged (b6ce669) |
| CU-9 Four stale sentences and the template's misleading example | N | — | `strategy.md` (line 5); `releases/TEMPLATE.md` (line 22); `vision/gaps/F-001-platform-reliability.md` (line 26); `env/README.md` (line 20 and the script table); `templates/project/plan.md` (the `**Vision gaps:**` line) | `check --base` passes; the whole inventory passes; the template's two example lines are accepted by `plan_gap_ids`; [details](#cu-9) | [x] 12 Nov: merged on `int/51-astrid-dev-clean-up` (de55dd7); the Vision role form has the colon inside the bold, as the check requires |
| CU-20 The root README leads with what Astrid is, in the owner's words | T | — | `README.md` (hand-written text only: the title, the opening line, the order of the sections and the sentences of "What we're building"; not the `vision-summary` region, not the agent prompt block or its heading) | Before and after shown to the owner; the fenced agent prompt and the heading `## Want to contribute? Give this to your agent.` are byte-identical; `check` passes; the public feed is byte-identical; `sync` reports the views current; the word count of `README.md` outside the generated region is not higher; [details](#cu-20) | [x] 12 Nov: merged with Part 1 (PR 565); the tagline carries the owner's new words; the title is still "Astrid development workspace" (her choice open) |
| CU-21 The vision statement in the owner's new words, changed at its source | N | — | `vision/intro.md` (line 1, the title after `# Astrid — `); `README.md` (the bold line under `## What we're building`). Not `vision/README.md`: the refresh job regenerates it. Not the fixtures under `scripts/fixtures/` or `scripts/test_export_public_vision.py`, which pin a fixture title, not the live one | The title reads "A tool to unlock the artistic potential of the open-source AI community" in both files; `check --base` passes; the whole inventory passes with no test edited; the public feed differs from the base in the `title` value only (show the diff); after the part merges, the job's commit changes `vision/README.md` line 3 and nothing else in it; [details](#cu-21) | [x] 12 Nov: merged with Part 1 (PR 565); the feed's `title` is the only change |
| CU-22 The README's statement line is generated, so the statement has one home | N | CU-21; C-2 (Part 2) | `scripts/export_public_vision.py:render_root_readme` (the region gains the bold statement line, read from `vision/intro.md`); `README.md` (the hand-written bold line is removed; the region regenerated); `scripts/test_export_public_vision.py` and `scripts/test_views.py` (added cases only); the README fixtures under `scripts/fixtures/` if the region's shape is pinned there, each listed | A test that changing the title in `vision/intro.md` changes the README region after `sync` and that the hand-written copy is gone; `golden.txt` changes only where the README region's content is pinned, each line listed before and after; the public feed is byte-identical to CU-21's; if it needs more than about twenty changed script lines, stop and tell the orchestrator; [details](#cu-21) | [x] 12 Nov: the statement line is its own generated region (`root-vision-statement`, 18 non-test script lines), with the hand-written "Astrid pairs..." sentence under it, as the owner asked; one fixture input changed (`broken-local-link/overlay.json`), `golden.txt` not |
| RS2 Review stop on the whole of Part 1 before it lands (rounds at most 1). It protects every later run that reads these skills, and CU-14 and CU-15, which build on the table of homes and the new skill | S | CU-0 to CU-9, CU-20, CU-21 | read-only | Same protocol as R, on the integrated head of `int/51-astrid-dev-clean-up` after `main` is merged in and the inventory, `check` and the anchor proof pass; findings become rows `RS2.<n>`; then one pull request to `main`, merged on the owner's go; [what it looks for](#review-rows) | [x] 12 Nov: 2 blocking, should-fix items all applied; the second round was not run (the plan allows one) |
| **Part 2: scripts and one check. Starts only when Plan 48's C-2 is on `main`** | | | | | |
| CU-11 Bytecode is no longer tracked | N | C-2 | `scripts/__pycache__/` (three files leave the index); `.gitignore` | `git ls-files "*.pyc"` prints nothing; the inventory run without `PYTHONDONTWRITEBYTECODE` leaves `git status --porcelain` empty; [details](#cu-11) | [x] 12 Nov: merged on `int/51-part2` (d73b71e) |
| CU-12 Dead code goes, and the guard that eleven checks repeat is written once | N | C-2 | `scripts/checks.py` (the eleven guarded checks and one new helper); `scripts/records.py:field_matches`; `scripts/check_docs.py:STATUSES`; the unused imports in `scripts/check_completion.py` and `scripts/check_gap_boundaries.py` | The inventory passes with no test edited; `golden.txt` unchanged; `list` prints the same lines as the base; fewer non-test lines than the base; [details](#cu-12) | [x] 12 Nov: merged on `int/51-part2` (9d3d5d5); non-test script lines 3005 to 2954 |
| CU-13a The principle-list contract, tests first: the public feed takes the principle names and order from the hand-written intro, never from the generated page | X | C-2 | `scripts/test_export_public_vision.py` (added tests); the intro file under `scripts/fixtures/vision/` (one added section); `scripts/test_views.py` (only tests the card lists as made untrue) | The added tests fail only on cases that need CU-13b; everything else passes; [details and what it makes untrue](#cu-13a-and-cu-13b) | [x] 12 Nov: merged on `int/51-part2`; the deletion test became a garbled-page test, because pillar documents link to `../README.md#four-driving-principles` |
| CU-13b Pass the principle-list contract | N | CU-13a | `scripts/export_public_vision.py:build` and the comment at line 215; `vision/intro.md` (one added section) | CU-13a's tests pass unedited; the feed is byte-identical to the base; `sync` reports nothing to update; `golden.txt` unchanged; [details](#cu-13a-and-cu-13b) | [x] 12 Nov: merged on `int/51-part2` (30c8386); the regenerated `vision/README.md` header comment is committed with it |
| CU-14 The contributor docs use the glossary and link to each rule's home; the extending guide is brought up to date | N | RS2, C-2, CU-11; D6, D8 | `docs/contribution-workflow.md`, `docs/project-format.md`, `docs/contribution-automation-setup.md`, `docs/extending.md`, `CONTRIBUTING.md`, `README.md` (outside the marked regions), `templates/product-pr/review.md`, the hand text of the four forms in `.github/` | Every deleted sentence listed with its home; the word count is lower than before the card; `check --base` and the anchor proof pass; `test_review_intake.py` and `test_check_completion.py` pass unedited; [details](#cu-14) | [x] 12 Nov: merged on `int/51-part2` (e1dfe4c); words 29,024 to 29,000; the claim and review forms changed in hint text only |
| CU-15 A new check, `link-anchors`, added by a fresh worker from the new skill and the extending guide: a link to a heading in a skill, a template or a top-level doc must name a heading that exists | N | RS2 landed on `main`, C-2, CU-14 | `scripts/checks.py` (one function, one `REGISTRY` entry); `scripts/test_checks.py` (added tests); `docs/checks.md` (as `sync` writes it) | The added tests pass; `list` shows the check; `golden.txt` unchanged; `check --base` passes on the real tree; the worker's questions are listed in the pull request; [details](#cu-15) | [x] 12 Nov: merged on `int/51-part2`; written first by a fresh worker (56 lines), then cut to 25 lines (ATX headings only; no percent-decoding or query strings: none occur in the checked files); the worker's 18 questions are CU-15.1 to CU-15.7 in `docs/extending.md` and the improve skill, the rest were out of the brief's reach; a `fix` ledger entry was not written |
| CU-16 Closing words: the new check's description and message, and its id in the principles | T | CU-15 | `scripts/checks.py` (the new check's two strings); `scripts/test_checks.py` (only assertions that pin an edited string, each listed); `docs/checks.md` (as `sync` writes it); `docs/contribution-design-principles.md` (one line) | Before and after for every string; the inventory passes; `golden.txt` unchanged; `check --base` passes; [details](#cu-16) | [x] 12 Nov: merged on `int/51-part2`; the description now reads "Validate links to headings..."; the message gives one next step; principle 2 names the id (one word trimmed from principle 3 to stay at 600; not in the card) |
| R Review rounds (at most 1), on Part 2's integrated head | S | all other tasks in Part 2 | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R1.<n>` added directly below this one, each with route, scope, dependencies and proof; the pull request to `main` and the completion wait for them; [what it looks for](#review-rows) | [x] 12 Nov: no blocking finding; R1.1 (a garbled line in principle 2, fixed), R1.2 (the missing rows for CU-17c, CU-22b and CU-23, added here), R1.3 (the guide's file-list rule, fixed), R1.4 (CU-16's extra line, recorded above); R1.5 to R1.9 notes |
| **Not taken (owner decision D7, 12 Nov 2026): older packs are left as they are** | | | | | |
| CU-10 Five older packs stop saying that status lives only in the catalog | N | D7 (a) | `plans/30-update-everywhere/plan.md`, `plans/31-releases-from-astrid-dev/plan.md`, `plans/37-generate-time-destination/plan.md`, `plans/38-one-process-identity/plan.md`, `plans/39-green-mains/plan.md` (one sentence each) | The grep lists only the packs left on purpose; `check --base` passes; [details](#proposed-cards) | [ ] |
| **Taken by the owner (decision D9.1, 12 Nov 2026): part of Part 2** | | | | | |
| CU-17a The completion form contract, tests first: with only the plan number filled in, every field whose rule can tell an answer from a hint fails; `None — TBD` is not a reason | X | D9 (1); C-2 | `scripts/test_check_completion.py` (added tests) | The added tests fail only on cases that need CU-17b; the rest pass unedited; [details](#proposed-cards) | [x] 12 Nov: merged on `int/51-part2` |
| CU-17b Pass the completion form contract | N | CU-17a | `.github/PULL_REQUEST_TEMPLATE/project-completion.md` (hint text); `scripts/check_completion.py:assess_completion` (line 75) | CU-17a's tests pass unedited; `test_review_intake.py` passes unedited; [details](#proposed-cards) | [x] 12 Nov: merged on `int/51-part2`; the colon form (`None: TBD`) is also covered, as a follow-up (6b19b06) |
| CU-17c The colon form of the completion contract: `None: TBD` fails as `None — TBD` does | X | CU-17b | `scripts/test_check_completion.py` (added tests); `scripts/check_completion.py` (one line: the separators stripped before the placeholder test) | The added tests fail on the base for the colon only, then pass; the inventory passes | [x] 12 Nov: merged on `int/51-part2` (6b19b06), added at the orchestrator's instruction |
| CU-22b The statement line gets its own generated region, so the hand-written sentence sits directly under it | X | CU-22 | `scripts/views.py` (one view and its render function); `scripts/export_public_vision.py` (back to the summary only); `README.md`; CU-22's added tests; `scripts/fixtures/vision/README.md.fixture` and `scripts/fixtures/broken-local-link/overlay.json` (inputs) | Feed byte-identical; `golden.txt` unchanged; at most about twenty changed script lines | [x] 12 Nov: merged on `int/51-part2` (c7700f3); 18 lines |
| CU-23 Review intake can label a pull request: the workflow token gains `pull-requests: write`, and a refused call names itself | N | — | `.github/workflows/review-intake.yml` (one permission; the only workflow change of the plan); `docs/contribution-automation-setup.md` (one table cell); `scripts/review_intake.py` (docstring); `scripts/contribution_api.py` (the error carries the method and path); `scripts/test_review_intake.py` (two added tests) | Both tests fail before and pass after; reproduced and fixed first in a scratch repository (runs 43257544607, 43258020722 fail; 43258458758 succeeds); the inventory passes | [x] 12 Nov: merged on `int/51-part2` (89e2b6f); cause: adding a label to a pull request returned 403 `Resource not accessible by integration` with `pull-requests: read`; the orchestrator asked for it |
| **Proposed only, not taken (decisions D9.2 and D9.3)** | | | | | |
| CU-18 Ten checks report even when a plan's header is broken | N | D9 (2); CU-12 | `scripts/checks.py` (the helper from CU-12); `scripts/test_checks.py:test_every_other_documentation_rule_skips_a_bad_record` (re-aimed, before and after shown) | [details](#proposed-cards) | [ ] |
| CU-19 A check that asks for a reason when a pull request adds words to the skills | N | D9 (3); RS2 landed on `main`, C-2 | `scripts/checks.py` (one function, one `REGISTRY` entry); `scripts/test_checks.py` (added tests); `docs/checks.md` (as `sync` writes it) | [details](#proposed-cards) | [ ] |

## Sizes and who runs each card

Engineering days. A "cheap worker" is a Claude sub-agent on the N route; an "X worker" is one on the X route; the high-judgment sub-agent is a fresh one that has not seen the cards being built. Route and dependencies are in the table above and are not repeated here.

| Card | Run by | Waits for C-2 | Days |
| --- | --- | --- | --- |
| CU-0 | cheap worker | no | 0.1 |
| CU-1 | two cheap workers, one file group each | no | 0.2 |
| CU-2 | cheap worker | no | 0.1 |
| CU-3 | high-judgment sub-agent | no | 0.5 |
| CU-4 | X worker with N helpers | no | 0.75 |
| RS1 | high-judgment sub-agent | no | 0.25 |
| CU-5 | cheap worker | no | 0.5 |
| CU-6 | X worker with N helpers | no | 0.75 |
| CU-7 | X worker with N helpers | no | 0.75 |
| CU-8 | high-judgment sub-agent | no | 0.25 |
| CU-9 | cheap worker | no | 0.15 |
| CU-20 | high-judgment sub-agent | no | 0.15 |
| CU-21 | cheap worker | no | 0.05 |
| CU-22 | cheap worker | yes | 0.25 |
| RS2 | high-judgment sub-agent | no | 0.4 |
| CU-11 | cheap worker | yes | 0.1 |
| CU-12 | cheap worker | yes | 0.4 |
| CU-13a | X worker | yes | 0.5 |
| CU-13b | cheap worker | yes | 0.4 |
| CU-14 | cheap worker | yes | 0.5 |
| CU-15 | a fresh cheap worker | yes | 0.5 |
| CU-16 | high-judgment sub-agent | yes | 0.15 |
| R | high-judgment sub-agent | yes | 0.4 |

**Totals by route:** N 2.95 days (39%), X 2.75 (36%), S 1.55 (20%), T 0.4 (5%); 7.65 in all, 4.7 in Part 1 and 2.95 in Part 2. Cheap and mid-tier workers do 75% of it. The proposed cards would add 1.75: CU-10 0.25, CU-17a 0.5, CU-17b 0.25, CU-18 0.25, CU-19 0.5.

## Dispatch notes

**Recommended manager route: X.** The manager keeps three tracks moving, rules on whether a cut lost a rule, and rules at once when a card meets a pinned test; that is judgment an N manager cannot borrow, and nothing here is deep enough for S.

**The setup, for the `Run start` line.** One Claude session manages and is the accountable agent. It sends each N and X card to a Claude sub-agent on that card's route, as the run contract's table maps it. The owner asked on 12 Nov 2026 for the cheap family on N work and the middle one on X work, so this run does not use Codex workers; say so on the `Run start` line, because Codex workers are otherwise the default. The manager does not do or judge S and T cards: CU-3, CU-8, CU-16, RS1, RS2 and R each go to a fresh high-judgment sub-agent.

**Where work lands.** `int/51-astrid-dev-clean-up`, cut from `main` when the run starts; record the commit on the `Run start` line. Each card has its own task branch and worktree, cut from the integration branch and merged back into it. Part 1 goes to `main` as one pull request after RS2. Part 2 starts from `main` after C-2: merge `main` into the integration branch, record that commit as Part 2's base, and take the script line count on it.

**Order.**

- Start CU-1, CU-3 and CU-9 at once. CU-0 and CU-2 start as soon as their decision is made.
- CU-4 follows CU-1 and CU-3. RS1 follows CU-4.
- After RS1, run CU-5, CU-6, CU-7 and CU-8 side by side. They change different files.
- RS2, then the pull request.
- In Part 2, CU-11, CU-12 and CU-13a start together. CU-14 follows CU-11. CU-15 follows CU-14. CU-12 and CU-15 both edit `scripts/checks.py` in different places; that is a merge order, not a dependency: whichever merges second merges the branch in and re-runs its proof.

**How to tell C-2 has landed.** On `main`, `python3 scripts/astrid_dev.py list` prints `generated-views pr …` (today it prints `generated-views always …`), and `scripts/export_public_vision.py` has no `--sync-readme` option. If C-2 is late, land Part 1, set this plan's `**Waiting on:**` line, and leave Part 2 queued. Plan 48's refresh branch has moved since this plan read it; read it again before Part 2 starts and re-check every Part 2 card against it.

**For every card.**

- Record the card's base commit when it starts. Add commits only.
- The card's brief carries the manager line and the "never use AskUserQuestion" line that the [manage skill](../../skills/astrid-dev-manage/SKILL.md) requires.
- A worker never edits a test or `scripts/fixtures/golden.txt` to get a pass. If its card would make a pinned test, a fixture or an oracle line untrue and the card does not list it, the worker stops and reports the exact lines, and the manager rules at once.
- **No rule lost.** A card that deletes or moves a sentence from a skill or doc lists, in its pull request, each such sentence with its file and line and where the rule now lives. If removing a copy would lose something its home does not say, the worker stops and reports the sentence. It does not decide.
- Until CU-11 lands, prefix Python commands with `PYTHONDONTWRITEBYTECODE=1`. If tracked bytecode still changes: `git clean -fdq -- env/__pycache__ scripts/__pycache__; git checkout -q -- scripts/__pycache__`.
- Generated pages: before C-2, run `sync` and commit what it writes. After C-2 a pull request may still carry a correctly regenerated page, so a card that registers a check runs `sync` and commits `docs/checks.md`.

**Commands.**

- One test file: `python3 -m unittest discover -s scripts -p "<file>"`. The whole inventory: the same with `"test_*.py"`.
- The checks: `python3 scripts/astrid_dev.py check`. With a base: `python3 scripts/astrid_dev.py check --base <base commit> --body-file /dev/null`. Also `list` and `sync`.
- The oracle: `test_golden.py` passes, and `git diff --stat <base commit> -- scripts/fixtures/golden.txt` prints nothing.
- The same feed: `python3 scripts/export_public_vision.py --revision 0000000000000000000000000000000000000000 --output <file>` on the base and on the candidate, compared with `cmp`.
- Words: the `LC_ALL=C find … | LC_ALL=C xargs -0 cat | LC_ALL=C wc -w` command in [plan.md](plan.md#completion). The locale matters: another one counts 52 more. Script lines: `ls scripts/*.py | grep -v /test_ | xargs cat | wc -l`.
- The anchor proof: save the script below outside the repository and run it from the repository root. It must print nothing.

**The anchor proof.** `check` validates that a link's file exists. It does not look at the part after `#`. Until CU-15 lands, this script is how a card proves it broke no link to a heading in a skill, a template or a top-level doc, including links inside the same file. It printed nothing at `1826336`.

```python
import re, sys
from pathlib import Path

root = Path(".").resolve()
link = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)")


def anchors(path):
    seen, out = {}, set()
    for h in re.findall(r"^#{1,6}\s+(.+?)\s*$", path.read_text(encoding="utf-8"), re.M):
        h = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", h).replace("`", "")
        s = re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-")
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def checked(path):
    parts = path.relative_to(root).parts
    return parts[0] in ("skills", "templates") or (parts[0] == "docs" and len(parts) == 2)


bad = 0
for src in sorted(root.rglob("*.md")):
    if ".git" in src.parts:
        continue
    for target in link.findall(src.read_text(encoding="utf-8", errors="replace")):
        if "#" not in target or re.match(r"[a-z][a-z0-9+.-]*:|//", target, re.I):
            continue
        name, _, fragment = target.partition("#")
        dest = (src.parent / name).resolve() if name else src
        if (dest.suffix == ".md" and dest.is_file() and dest.is_relative_to(root)
                and checked(dest) and fragment not in anchors(dest)):
            print(f"{src.relative_to(root)}: {target}")
            bad += 1
sys.exit(bool(bad))
```

**Load-bearing test moments.** The inventory runs in under a minute, so by the run contract's cost exception the manager runs all of it at each of these: once on the first commit of the integration branch; after each card that touches `scripts/` or a file a test reads (`templates/`, `vision/`, `strategy.md`, the forms); on the integrated head before RS2 and before R; and CI on each pull request to `main`. A card that changes only skills runs `check`, the anchor proof and its own proof.

**Other sessions keep editing the skills.** Merge `main` into the integration branch daily during Part 1. For each skill change that arrived, place its rule by the table of homes before RS2. If a change conflicts with a cut, keep the rule and redo the cut.

## Review rows

Each review follows the run contract's protocol: independent of the authors, read-only, on an exact commit range, briefed with the range and these questions and not with the manager's conclusions.

- **RS1** reads CU-3 and CU-4. It looks first for: a principle that is not true of the repository; a principle with no real failure behind it; a term left with two senses; a rule with no home or two; a conflict settled differently from the rulings in CU-4 or the owner's decisions; and anything added that could have been a link.
- **RS2** reads the whole of Part 1. It looks first for: a rule lost (it samples twenty deleted sentences from the cards' lists and from the diff itself against the homes they name, and looks for deletions no list mentions); a link where the reader now needs three hops to learn one rule; an edit to the release or GPU-validation skill, to a pack with a live run, or to a Release 12 or 13 file; and a word count that is not lower than the baseline. If the count is not lower, the cut cards get another pass before Part 1 lands.
- **R** reads Part 2. It looks first for: a check whose verdict, trigger or message changed with no card saying so (`golden.txt` must be byte-identical to Part 2's base); a test edited that no card lists; non-test script lines not below Part 2's base; code squeezed to meet that count; and a question from CU-15's worker that changed nothing.

## Card details

### CU-0

Add to the route table in `vision/gaps/CA-005-parallel-contribution.md`, after step 1: step 2, a link to this plan written as `[Plan 51](../../plans/51-astrid-dev-clean-up/plan.md)`, the contribution "each rule and term has one source; a fresh agent changes astrid-dev from one skill alone", and a milestone name. Use no status word in the row (`queued`, `active`, `blocked`, `paused`, `done`, `cancelled`): the `gap-structure` check refuses them. Update the critical-path sentence under the table. The gap boundary check does not read the route table.

Plan 48's task list states the principle-list follow-up in two places: the note that begins "Raised at R2 (12 Nov 2026) and not done in Phase 2" (line 186) and the paragraph that begins "Still open from the Phase 2 review, and not in this queue" (line 247). Add one sentence to each saying Plan 51 takes it as CU-13, and to the first that Plan 51's CU-9 takes the `strategy.md` sentence. If D9 (1) is taken, add to the PM-13a row that Plan 51's CU-17 covers the unfilled-form case. Plan 48 has a live run, so this goes as its own small pull request that Plan 48's accountable session merges.

### CU-1

One file, `plans/51-astrid-dev-clean-up/evidence/baseline.md`, with three short parts. It is not a list of every rule.

1. **The count,** with the commit, the word command and its output, and the word count of each file under `skills/`.
2. **Terms.** Each role and unit-of-work word (owner, maintainer, contributor, orchestrator, advisor, manager, host, accountable agent, lead, worker, helper, reviewer; project, plan, pack, phase, track, task, card, run, route, candidate, check, gate, view, round, stop, release, brief), with each file and line that defines it or uses it in a different sense.
3. **Rules written more than once.** Start from the list in [inputs.md](inputs.md#prior-art-what-was-verified) and search for more. One row per rule: the rule in at most fifteen words, and every file and line that states it.

Split across two workers: the terms; the duplicated rules. The release and GPU-validation skills are read for copies and are never edited.

### CU-2

Under D3 option (a), the sentence at `codex-runner.sh:55` becomes: append the question, release every pod this run made and say which, then end with `RUN-STATUS: WAITING`. Change no shell logic. Leave line 71 alone: it speaks to a run that was interrupted and is about to continue, and it already says to release only what is not in use. If D3 is decided as (b), the card instead adds who decides and where that is recorded; ask the manager for the wording.

### CU-3

An S card, run by a fresh high-judgment sub-agent. It decides which principles exist. It is not a wording task; CU-8 polishes the words afterwards.

- **Surface:** `docs/contribution-design-principles.md`, 505 words today, eight principles.
- **Intent:** someone who arrives with no context can act correctly, because each principle names a failure that has happened here and the rule that prevents it.
- **Starting material:** today's eight; the orchestrator's eight and the four corrections to them in the [ambiguity pass](inputs.md#ambiguity-pass); the [process ledger](../../docs/ledger/README.md). Treat both lists as proposals. Derive the set again from the failures.
- **Rules:**
  1. No failure, no principle. For each one, name the failure with a pointer: a ledger entry, a line in `inputs.md`, or a file and line.
  2. Each principle has a short name of two to four words, one sentence of rule, one example path in this repository, and either the id of a check from `python3 scripts/astrid_dev.py list` or the word "judgment".
  3. Each is true of the repository when Part 1 lands, or names its exception.
  4. The ownership sentence follows D2. Until D2 is decided, write what is true today: one owner per project, declared once; accountability, not permission.
  5. At most 600 words in the file.
  6. Keep the file's two `## ` headings as they are, or run the anchor proof to show nothing links to a heading you rename.
- **Proof:** the exact before and after, shown to the owner, because she decides what the principles are; a table in the pull request with principle, failure pointer, example path and check id or "judgment"; `check` and the anchor proof pass.
- **Note:** three older plans cite principles by number. Do not edit them. New text cites a principle by name.

### CU-4

An X card. The worker keeps the judgment and sends reading and mechanical edits to N helpers.

**The glossary,** `skills/astrid-dev-shared/glossary.md`, at most 450 words. One line per term in CU-1's list. Each definition is the sense most used today. Where two senses are both needed, they become two terms (for example "project pack" and "product pack"; "task route" and "manager's route"). A term that is not needed is listed in the pull request as dropped, with the word that replaces it.

**The new skill,** `skills/astrid-dev-improve/SKILL.md`, at most 600 words, with the same front matter as the other skills:

- **Where things go:** a table of kind of thing, its one home, and what enforces it. At least: a run rule (the run contract); a role's own steps (that role's skill); a term (the glossary); a pack's shape and what a task card holds (the three templates, enforced by `pack-shape`); a check (`scripts/checks.py`, how in `docs/extending.md`); a generated page (`scripts/views.py`); a project fact (the six lines of its `plan.md`); priority (`plans/priority.md`); a principle (the principles doc); friction (the ledger).
- **Steps:** start from a recorded failure (a ledger entry or an issue); find the home in the table; change the home and nothing else; if you add words, cut as many; a change to what a check accepts is its own announced change, with every pinned test, fixture and oracle line it makes untrue listed; prove it with the commands; add a `fix` entry to the ledger.
- **Audit:** at most 120 words. When: a run's ledger entry names friction in the skills, or the owner asks. How: cheap helpers each map one area read-only, then one high-judgment critic checks their claims in the code and judges. Output: ledger entries and at most one proposal. No standing schedule.

**The entry skill** gets one row in its routing table for the new skill.

**The run contract** gains one canonical sentence for each rule that has copies and no home there. At least: add commits only, never rebase or force-push; the merge case where the test scope is every test file that touches a changed module (MGR:61); the two stopping thresholds, named as different actions (a worker stops after three attempts or 45 minutes, ITER:23; a manager moves a task up a route after two misses or 20 minutes, RC:25). Its lines 39-40 keep the table row and link to the one statement that Codex workers are the default (see CU-7). List each added sentence in the pull request.

**The settled list.** Apply these rulings and no others. Where two texts conflict and no ruling here or owner decision covers it, stop and report.

| Conflict | Ruling |
| --- | --- |
| Rented machines on pause (`codex-runner.sh:55` against GPU:31) | D3. CU-2 applies it; here only the run contract's sentence |
| Who merges progress pull requests (MGR:28 against ORCH:97) | D4 |
| Where a blocking finding goes after the last round (RC:104 against MGR:108) | D5 |
| Model names (RC:53 against `docs/contribution-workflow.md:126`, and three family tables) | D6 |
| Taste work when workers are on Codex (CCR:28 against RC:16 and CCR:12) | D11 |
| Installing skills for Codex (CCR:22 against CCX:9-17) | Not a conflict: two environments. Each guide says in its first line which environment it is for. No rule changes |
| Wake-up interval (ORCH:117 and CCR:82 against MGR:62) | Not a conflict: two timers. Each sentence names its timer. No rule changes |
| Three names for a record of decisions (MGR:41 "decision log"; RC:71 "decisions ledger"; the inputs template's "Owner decisions") | Three things. The glossary defines each: a manager's running list of its own rulings; calls made while the owner is away, for her to accept or revert; what the owner must decide |
| "Principle 7" (MGR:109, BRIEF:55) | It means the manage skill's own rule 7. Cite it by its name, "Progress is always current" |
| T as a manager's route (ORCH:63) and T as a small task (RC:47) | Two terms in the glossary: "task route" and "manager's route". Neither text changes |

If one of D3 to D6 or D11 is not yet decided, leave that rule as it is and say so in the pull request; the manager adds a row when she decides.

**Proof:** every term in the baseline is in the glossary or on the dropped list; every duplicated rule in the baseline appears in exactly one row of the table of homes; the word limits hold; the pull request shows before and after for each row of the settled list; `check` and the anchor proof pass.

### CU-5

For each of the six files: replace every copy of a rule whose home is elsewhere with a link to that home, using the heading link the table of homes gives; replace a `## Terms` section with one line linking the glossary; change nothing else. List each deleted sentence with its home in the pull request.

Proof: `grep -c "^## Terms"` on each of the six files prints 0; the word command prints less than before the card; `check` and the anchor proof pass.

### CU-6

An X card. For each rule in the manage skill: a run rule becomes a link to the run contract; a rule about a hosted Codex manager becomes a link to that guide; a manage step stays and is shortened. Split the four longest paragraphs (lines 28, 62, 86 and 87) into one bullet per action. Remove the `## Terms` section. Replace "principle 7" as CU-4 rules. Apply D4 and D5. The copy of "Codex workers are the default" at lines 65-66 becomes a link to the orchestrate skill's section "Use Codex from Claude Cloud".

The aim is 3,200 words or fewer (4,002 today). No rule may be lost to reach it: if the count stops higher, say which rules set the floor. List every deleted or moved sentence with its home in the pull request.

Proof: that list; the word count; `check` and the anchor proof pass (the skill links to its own `#decide` heading, and other files link to its headings).

### CU-7

An X card, as CU-6, for four files.

- The orchestrate skill: 2,900 words or fewer (3,450 today), on the same terms as CU-6. Line 147's "catalog order" becomes the priority order.
- The three guides together (4,578 words today) end lower.
- The route-to-model tables at CCR:7-12 and BRIEF:25-30 become links to the run contract's table, per D6. BRIEF keeps its fill-in lines for a run's own copy.
- "Codex workers are the default" is stated once, in the orchestrate skill's section "Use Codex from Claude Cloud". Its copies at CCR:3 and :24 and BRIEF:3 become links. The copies in the run contract and the manage skill belong to CU-4 and CU-6.
- The rulings in CU-4's settled list that touch these files are applied here.

Proof: the list of deleted or moved sentences with their homes; the word counts; `check` and the anchor proof pass. Many plan packs link to headings in these files, and the guides link to each other's headings; the anchor proof covers all of them.

### CU-8

A T card, run by a fresh high-judgment sub-agent, on three documents: the principles, the glossary and the new skill. Intent: a newcomer understands each principle, definition and step without opening another file. Taste rules: plain words; short sentences; one word for one thing, as the glossary has it. It changes no principle, definition, home or step; if a sentence cannot be made clear without changing one, it reports the sentence. It returns the exact before and after for each sentence.

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

### CU-20

The owner asked for this on 12 Nov 2026, after reading the page: lead with what Astrid is, then how to contribute. It is a small edit and a little rewriting, not a new page.

- **Order.** The title; the opening line that says what Astrid Dev is for (today's "Astrid Dev connects our creative ambition to practical contributions"); then `## What we're building`; then `## Want to contribute? Give this to your agent.`; then the rest as it is.
- **What we're building, in her words.** The line becomes "A tool to unlock the artistic potential of the open-source AI community." (CU-21 changes the statement at its source; this card uses the same words.) Follow it with one sentence saying what Astrid consists of: an adaptable front end, linked to [astrid.haus](https://astrid.haus), alongside an agent equipped with tools for creative work and open-source AI. The generated `vision-summary` region stays directly below, untouched.
- **The title.** She called the page "Astrid Dev Workspace"; offer that beside today's "Astrid development workspace" in the before and after and let her choose.
- **What must not change.** `scripts/export_public_vision.py` finds the agent prompt by the exact heading `Want to contribute? Give this to your agent.` and requires exactly one fenced block under it, and it publishes that block in the public feed. So the heading and the block are moved as a unit and not edited. The marker pair of the `vision-summary` region is not edited either.
- **Taste rules.** Plain words, short sentences, no claim the product does not yet meet, every link resolves, and nothing a newcomer would have to look up.

### CU-21

On 12 Nov 2026 the owner changed the vision statement itself: "A tool to unlock the artistic potential of the open-source AI community", in place of "A tool to unlock the collective artistic ambition of the open-source AI community". Her reason: "collective artistic ambition" is already implied by "community", so the shorter line is more elegant. She asked whether the README's line is the one that reaches the vision page. It is not: the statement's source is the title of `vision/intro.md`, which the exporter publishes as the feed's `title` and the vision page shows; the README carries a second, hand-written copy.

- **CU-21** changes both copies together, so they agree the day it lands. The published feed's `title` changes on purpose; nothing else in the feed does.
- **CU-22** then removes the second copy: the README's line is generated into the `vision-summary` region from `vision/intro.md`, so the next change is one edit. It is Part 2 because it changes a script.
- **Not changed:** Pillar 1 keeps its name, "A Tool for Artistic Ambition". Whether the product's own site states the old line anywhere outside the feed was not checked; it is in another repository.

### CU-11

`git rm --cached` the three files under `scripts/__pycache__/`. Add `__pycache__/` and `*.pyc` to `.gitignore`, and reword its first comment so it describes `.otto/` without naming another project. Do not touch the workflow, which sets `PYTHONDONTWRITEBYTECODE` on its own.

### CU-12

No behaviour changes in this card. If any test or any line of `golden.txt` would need an edit, stop and report.

- Remove `records.py:field_matches` (no caller), `check_docs.py:STATUSES` (no reader), and the unused imports: `json` and `subprocess` in `check_completion.py`, `json` in `check_gap_boundaries.py`. Confirm each with a grep at dispatch.
- In `scripts/checks.py`, eleven checks begin with the same guard: return nothing if the catalog check has errors, then call `projects(root)`. In ten of them `rows` is never read, and the call cannot raise once the catalog check has passed. Remove those ten calls and the imports only they used. `_catalog_paths` keeps its call, because it reads `rows`.
- Write the guard once, as one helper the eleven checks use. `scripts/test_checks.py:test_every_other_documentation_rule_skips_a_bad_record` pins the guard's behaviour and must pass unedited.

Proof: the inventory passes with no test edited; `golden.txt` unchanged; `python3 scripts/astrid_dev.py list` prints the same lines as on the base; the script line count is lower than on the base. Do not squeeze code to lower the count: the saving comes from the removed calls and the repeated guard, about fifty lines.

### CU-13a and CU-13b

Today `export_public_vision.py:build` reads the principle names, order and links from `vision/README.md` (lines 89-92 and 115), which is generated. The pillars are already read from the hand-written `vision/intro.md`.

**CU-13a, tests first.** Add to `test_export_public_vision.py`:

1. `build` reads the principles from a `## Four driving principles` section of the intro file, written as the pillars are in that file: one third-level heading per principle, holding a link from its name to its file under `principles/`.
2. In a temporary copy of the fixture tree, swapping two principle headings in the generated vision page, or deleting that page, gives the same `build` result.
3. Swapping two entries in the intro file changes the order in the result.
4. A principle file whose heading differs from the intro raises an error that names the intro.

Add the section to the intro file under `scripts/fixtures/vision/`.

**What it makes untrue.** This changes when `public-vision-content` fails, in three ways:

- A missing or garbled `vision/README.md` no longer fails it. `build` stops reading that file.
- An intro file with no `## Four driving principles` section now fails it.
- One error message changes: "principle heading must match README" becomes "principle heading must match the intro".

No line of `golden.txt` holds any of these at `1826336`; confirm on Part 2's base. At dispatch, list every test in `test_export_public_vision.py` and `test_views.py` that builds a vision tree with its own intro file, removes or damages a vision README, or edits a principle heading there; show each before and after in the pull request. If there are none, say so. Read Plan 48's refresh change first: it re-aimed tests in `test_views.py` that this card may meet.

**CU-13b.** Make `build` read the intro's section; add the section to the real `vision/intro.md` with the four principles in today's order; correct the comment at line 215. The card touches no test.

Proof: CU-13a's tests pass unedited; the feed is byte-identical to the base; `sync` reports nothing to update for `vision/README.md`; `golden.txt` unchanged; `check` passes.

The `canonical-principles` check, which holds the four file names in `scripts/checks.py`, stays as it is.

### CU-14

As CU-5, for the contributor docs, once C-2 has merged its own edits to them.

- Copies of homed rules become links; terms follow the glossary.
- `docs/contribution-workflow.md:36`: the link `../vision/README.md#gaps--16-assessed-outcomes` becomes `../vision/README.md`.
- `docs/contribution-workflow.md:126` and `templates/product-pr/review.md:13`: "a specific model name" follows D6.
- `docs/extending.md`, under D8 option (a): fix the stale check description at line 11; drop the `PYTHONDONTWRITEBYTECODE=1` prefixes (CU-11 makes them unnecessary); replace "In this branch" with plain present tense; and make its sentence about `docs/checks.md` true after C-2 (run `sync` and commit the page with the change; the page also refreshes on `main`). Keep its three recipes.
- Add no link with a `#fragment` into `docs/project-format.md`: an oracle fixture, `obsolete-project-path`, replaces that file, and once CU-15 lands such a link would add a line to `golden.txt`.
- In the four forms under `.github/`, change only hint text. Never change a line a check reads: `Project:`, `Review request:`, and every label in the completion form.

Proof: the list of deleted sentences with their homes; the word command prints less than before the card; `check --base` and the anchor proof pass; `test_review_intake.py` and `test_check_completion.py` pass unedited.

### CU-15

This card is also the proof that the new skill works. Give a fresh N worker `skills/astrid-dev-improve/SKILL.md`, `docs/extending.md` (which the skill links) and this card, and nothing else. Record every question it asks. Each question becomes a row `CU-15.<n>` that fixes the skill or the guide, so the next worker does not need to ask.

**The check.** `link-anchors`, trigger `always`. For every Markdown file that `markdown-links` walks, take each local link that has a `#fragment` and whose target is a `.md` file under `skills/` or `templates/`, or directly in `docs/`. A link that is only `#fragment` counts when its own file is in that set. The fragment must be the anchor of a heading in the target. Links into `plans/`, `releases/`, `vision/`, `docs/ledger/`, `docs/handoffs/` and the root files are not checked: about two dozen are broken there today, in files this project may not edit.

**The anchor rule,** as GitHub renders it: take the heading text without Markdown link syntax or backticks; lowercase it; drop every character that is not a letter, a digit, a space, a hyphen or an underscore; turn each space into a hyphen. A heading that repeats in one file gets `-1`, `-2` and so on. The script in the [dispatch notes](#dispatch-notes) is a working version of the rule.

**Message:** `<file>: link to <target>#<fragment> names no heading there; fix the link or restore the heading`.

**Tests,** added to `test_checks.py`: registered with trigger `always`; a good link passes; a missing heading fails with that message; a repeated heading's `-1` form passes; a heading that holds a link or backticks resolves; a bad fragment into `plans/` is not reported.

**A new verdict, announced.** From the day this reaches `main`, renaming a heading in a skill, a template or a top-level doc fails `check` until every link to it is fixed, in whichever pack holds the link. It cannot fail for someone who changed nothing: a link breaks only when its target heading or the link itself changes.

**The oracle.** The check runs on the real tree and on every fixture. One fixture, `obsolete-project-path`, replaces `docs/project-format.md` with other text; no link carries a fragment into that file today, so `golden.txt` gains no line. A prototype gave no error on the real tree and on all thirty fixtures at `1826336`. Re-check at dispatch. If the real tree has errors, fix the links that are in this plan's scope and report the rest.

**The generated page.** Registering a check changes `docs/checks.md`. Run `sync` and commit it with the change.

Proof: the added tests pass; `list` shows the check; `golden.txt` unchanged; `check --base` passes on the real tree.

### CU-16

A T card, run by a fresh high-judgment sub-agent.

- **Surfaces:** the description and the error message of `link-anchors`; in the principles doc, the one principle the check enforces now names its id.
- **Intent:** the message says what is wrong, where, and the one next step.
- **What it makes untrue:** only test assertions that pin a string it rewords. List each, before and after. Run `sync` and commit `docs/checks.md` if the description changed.

### Proposed cards

Not part of a run unless the owner takes them under D7 or D9.

**CU-10.** In each of the five packs, the sentence "Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md)." becomes the template's current sentence beginning "The six lines above are this project's row". At dispatch, check again which plans have a live run or sit in a running release, and skip those. Proof: `grep -ln "live \*\*only\*\* in the" plans/*/plan.md` lists only the packs left on purpose (20, 29, 32, 33, 34, 40 and 48 today); `check --base` passes. Editing a `plan.md` re-runs the planning check on a pack whose `inputs.md` has a `## Planning evidence` section. If it fails for a reason older than this edit, revert that pack and list it.

**CU-17a and CU-17b.** Run on `1826336`: the completion form with only its plan number filled in fails on two fields (`Integrated candidate`, and the `Gap` line's placeholder id) and passes on five hint lines. `Implementation PRs: None — TBD` passes, because `check_completion.py:75` tests the text after "None" with its dash still attached.

- CU-17a adds tests to `test_check_completion.py`: the form file itself, with only the plan number set, fails on `Evidence`, `Completion`, `Implementation PRs`, `Integrated candidate`, `Routes used` and the `Gap` line; `Unproven` is the listed exception, because its rule cannot tell an answer from a hint; `None — TBD` and `None — todo` fail for `Implementation PRs` and `Integrated candidate`; `None — Communication-only project.` still passes. The test that fills each hint with an example (added by Plan 48's PM-13h) must still pass unedited.
- CU-17b rewrites the hints so none satisfies its rule (no example link, no "Yes —", no route letter), and strips the dash before the placeholder test.
- **What it makes untrue:** a completion that passed with `None — TBD` now fails. At dispatch, list every test in `test_check_completion.py` and every line in `scripts/fixtures/` that holds "None —" followed by a placeholder word; at `1826336` there are none.
- The generated form (Plan 48's PM-13b) stays with Plan 48.

**CU-18.** Remove the guard from the ten checks that do not read the catalog rows. In a scratch copy at `1826336` this left the oracle output byte-identical. It makes one test untrue on purpose: `test_checks.py:test_every_other_documentation_rule_skips_a_bad_record`, which Plan 48 wrote to pin the guard. Re-aim it to say that only `catalog-paths` stays silent; show it before and after. In a nearly empty tree several of these checks will now report missing files, so the re-aimed test builds a tree that is whole apart from one broken plan header.

**CU-19.** A `pr` check, `skill-words`. It compares the words in every `*.md` file under `skills/` (files with identical content counted once, because copies of the tree turn the `codex-in-cloud` symlink into a second folder) between the merge base and the working tree. When the count went up, it fails unless the pull request's description has a line `Skill words: <reason>`. It never runs on `main` and compares each pull request with its own base, so two pull requests cannot together turn `main` red, and no shared number has to be edited. It adds one line that an author types and about twenty-five lines of script; that is why it is proposed and not committed. An earlier design, a fixed budget checked on every run, was dropped at the critique: two passing pull requests could together break `main` for everyone.
