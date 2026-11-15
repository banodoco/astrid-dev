# Tasks — Strategy from releases

[Plan](plan.md) · [Inputs](inputs.md)

**Task ids:** `SR-n`. **Critical path:** SR-1 → SR-2 → SR-3 → SR-7 → R; SR-1 → SR-4 → SR-7 joins it. **Test inventory:** `scripts/test_check_docs.py`, `scripts/test_checks.py`, `scripts/test_check_completion.py`, `scripts/test_views.py`, `scripts/test_records.py`, `scripts/test_auto_merge.py`, `scripts/test_issue_intake.py`, `scripts/test_export_public_vision.py`, `scripts/test_golden.py` with `scripts/fixtures/golden.txt` and the fixture folders named in the cards.

Every task is in astrid-dev and follows the [Improve](../../skills/astrid-dev-improve/SKILL.md) skill. Work lands on `int/58-strategy-from-releases`, one pull request per task; `main` receives it in one merge. The cards follow the owner's decisions D1 to D12 ([inputs.md](inputs.md#owner-decisions)). Before dispatch the manager runs the plan skill's ambiguity pass on each card. Line numbers and test names in the cards are from astrid-dev `main` at the commit in [inputs.md](inputs.md#source-identities): re-check them against the code at dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| SR-1 The release brief contract and its one reader ([card](#sr-1-the-release-brief-contract)) | X | — | `releases/TEMPLATE.md`; `releases/17.md` (the `Kind` line only); `scripts/records.py` (a new `release_brief` reader beside `project_fields`); `scripts/check_docs.py:release_errors` and the `RELEASE_*` constants (they read through the reader); `scripts/test_records.py`, `scripts/test_check_docs.py` | `test_records.py`: the six real release briefs parse without error; a duplicated `Kind`, an empty `Kind` and a `Kind` outside patch, minor and major are refused; an empty value is not read from the next line. `test_check_docs.py`: a draft with `None yet` passes; a plan bullet without a link fails; `test_release_requires_sections_and_plans` still passes unchanged. `python3 scripts/astrid_dev.py check` and `test_golden.py` pass with `golden.txt` unchanged | [ ] |
| SR-2 The strategy page, generated, in one change: nine views, the checks that replace the old ones, and `strategy.md` restructured with its markers ([card](#sr-2-the-generated-page)) | X | SR-1 | `scripts/views.py` (nine entries in `VIEWS` built in a loop and one renderer; `View`, `_with_marker` and `touched` unchanged); `scripts/check_docs.py:strategy_errors`, `version_errors` and the `STRATEGY_*`, `VERSION_*` constants; `scripts/checks.py:_strategy_consistency`, `_completion_impl` and the registry description; `scripts/check_completion.py`; `strategy.md`; `releases/12.md` to `17.md` (Intent: the moved sentence); the tests, fixtures and `golden.txt` lines in the card; `docs/checks.md` by `sync` | `test_views.py`: rendered parts for a tree with two minor releases; `sync` twice writes once; a hand edit inside a generated part fails; text outside the markers is kept; the two tests that copy the real tree still report exactly the errors they pin. `test_check_docs.py`, `test_check_completion.py` and `test_golden.py` pass with the changes the card lists and no others. On the real tree: `sync` then `check` pass and 0.1 shows Release 17 with its highlight, Releases 12 to 16 on one line and their plans | [ ] |
| SR-3 The words: the aim in one line; "Where we are", "At 1.0" and "How we get there"; the sentence and paragraph for 0.1, taken from Release 17's Intent; "Keeping this page current" rewritten. The lead drafts from the release briefs and the vision and the owner rewrites (D8) | X | SR-2 | `strategy.md` (hand-written parts only) | The owner's reply on the draft, quoted in `inputs.md`; `check` passes | [ ] |
| SR-4 The issue list: a command that writes, refreshes and freezes the block in a release brief, and the check of its shape ([card](#sr-4-the-issue-list)) | X | SR-1 | `scripts/release_issues.py` (new, standalone like `issue_intake.py`) and `scripts/test_release_issues.py`; `scripts/contribution_api.py` (reuse `request`; read every page); `scripts/records.py` (the reader returns the rows and whether the block is frozen); `scripts/check_docs.py:release_errors` (block shape; a final release brief with an `Issues` section needs a frozen block); `releases/TEMPLATE.md` (the optional `## Issues` section); `releases/14.md` to `17.md` (their first blocks) | `test_release_issues.py`, from recorded API responses, an injected date and no network: Release 15's block lists the fixture's `plan:39`, `plan:50`, `plan:40` and `release:15` issues, each once, with a `Via` cell; an issue with two matching labels has one row; pull requests are left out; an issue closed between two runs keeps its row with its new state; a second run on the same date changes nothing; no title from the fixture appears in the output; `--freeze` stamps the date and a later run refuses to rewrite. `test_check_docs.py`: a row with other text fails; a final release brief with an unfrozen block fails. Live: the manager runs it for Releases 14 to 17 and commits the four blocks | [ ] |
| SR-5 The `release:NN` label rule, in the guide's Issues section: triage may apply it for a release brief on `main`; it marks a candidate. An assorted ticket is worked under its release's run, from its row in the release brief (D12). Agree the order with Plan 52's manager, whose II-13 has the same section in scope | N | — | `docs/contribution-workflow.md` (Issues: the label list, rule 3, rule 5, the states paragraph); `docs/contribution-automation-setup.md` (the labels row) | `test_issue_intake.py` passes, including `IssuesSectionTests` (the six state links and the heading rule are untouched); the section names the label once | [ ] |
| SR-6 A pull request that adds, removes or changes a `**Kind:**` or `**State:**` line in `releases/<N>.md` is not eligible for planning auto-merge (D6) | N | SR-1 | `scripts/auto_merge.py:eligibility_reason` and `main` (read each file's `patch` from the files JSON it already loads); `scripts/test_auto_merge.py`; `docs/contribution-workflow.md` (the auto-merge paragraph) | `test_auto_merge.py`: such a patch gives a reason naming the line; a patch that changes only an Approach paragraph is eligible; a file entry with no `patch` (too large) is not eligible | [ ] |
| SR-7 The documentation agrees ([card](#sr-7-the-documentation)): one home for the hierarchy; `version`, `kind` and `standing lane` defined once; every listed sentence corrected; Plan 31 brought into line; three `fix` ledger entries | X | SR-2, SR-4, SR-5, SR-6 | the files in the card | The pull request lists each sentence in the card with its new text; `check` and the unit tests pass; `git grep -n -e "summary row" -e "sequence row" -e "Sequence rows" -e "strategy row" -e "roadmap summary" -- docs/contribution-workflow.md skills templates .github README.md CONTRIBUTING.md` prints nothing | [ ] |
| R Review rounds (at most 1) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; the merge to `main` waits for them | [ ] |

SR-4, SR-5 and SR-6 can run beside SR-2. SR-1, SR-2 and SR-4 each change `scripts/check_docs.py`: they merge into the integration branch in that order.

**Not a task here:** making the release briefs of Releases 12 and 13 Final. The owner left it to Plan 31 (D5); until then the page shows both as drafts and the hand-written "Focus now" says they are out.

## SR-1: the release brief contract

- **`**Kind:**`** is `patch`, `minor` or `major`, on its own line in the header. It is optional; absent means `patch`, which is Plan 29's default. Only `releases/17.md` gains the line (`minor`, the owner's decision of 15 November 2026 that Release 17 carries version 0.1). The four release fixture folders have no `Kind` and stay untouched.
- **Included plans** is exactly `None yet`, or every bullet in it is a link to one plan's `plan.md`, then a dash and a sentence, as the template shows. A section with neither still gets today's message, so `golden.txt` line 26 and `test_release_requires_sections_and_plans` stay as they are. The template says the sentence is what the strategy page shows for that plan (D1).
- **`## Issues`** is an optional section between Included pull requests and Publication; its shape is SR-4's.
- **The reader** returns number, title, state, kind, highlight, each plan as number, folder and sentence, and (after SR-4) the issue rows. It reads header fields with `key_value_lines`, because `named_field_matches` reads the next line for an empty value. `release_errors` keeps every message it has today.
- **What it makes untrue:** nothing that is pinned. New: a draft with `None yet` passes; an unlinked plan bullet, and a bad, empty or duplicated `Kind`, are refused.

## SR-2: the generated page

**Membership.** Release briefs are taken in number order. The first of kind minor ships 0.1, the second 0.2, and so on; a major ships 1.0. A release belongs to the version shipped by the first minor or major release brief numbered at or after it; release briefs after the last of those belong to the next version.

**The page.** `## Versions` keeps `### Version 1.0` and `#### Version 0.1` to `0.9`, so every existing anchor still resolves. Under each minor heading come the hand-written sentence (`**Aim:**`, or `Open`) and paragraph, then a marker pair `<!-- strategy-0.N:start -->` and `<!-- strategy-0.N:end -->` for all nine. Each generated part holds, per D11:
- the minor release: link, title, state and highlight;
- "On the way:" the patch releases as linked titles on one line;
- the plans of all those releases, one line each: release, plan name as a link, and the release brief's sentence;
- for each release with a frozen issue list, the number of rows, linking to it;
- or `No release yet.` when the version has none.

The `## Sequence` section, its table and the `**Plans:**` and `**Releases:**` lines go. Each "Why this order" sentence moves, word for word, to the end of its release brief's Intent.

**The checks.** `strategy_errors` removes everything between marker pairs before it reads headings and fields, so a generated part is never read back. Kept: the required sections without `## Sequence`; the `Last reviewed` line; one major version with an aim; the nine minor versions in order, each with a sentence or `Open`. New, in the always-on check so the message is readable: all nine marker pairs are present; the release briefs do not declare more minor releases than the page has versions; a major release brief is the last. Removed: the sequence-table rules, the `Plans` and `Releases` rules, the one-version rule for a plan (Plans 29 and 40 are each in two releases), and the rule that a plan completion edits `strategy.md`.

**What it makes untrue:**
- `check_docs.py`: `STRATEGY_HEADER`, `RELEASE_ROW`, `STRATEGY_PLAN`, `VERSION_RELEASE`, `VERSION_NO_PLANS`, the row loop in `strategy_errors`, and the `Plans` and `Releases` branches of `version_errors`.
- `test_check_docs.py`, `StrategyTests`: the `GOOD` fixture; `test_valid_strategy_passes` and `test_real_strategy_passes` are kept and run against the new shape; `test_release_requires_matching_roadmap_row` and `test_summary_and_plans_must_match_document` are removed (a generated part cannot disagree with its source; the view's test covers a hand edit); the three version tests are rewritten for sentences and kinds; `test_bad_release_link_and_missing_section_fail` keeps its missing-section half.
- `scripts/fixtures/`: `strategy-highlight-mismatch`, `strategy-missing-release-document`, `strategy-plan-links-mismatch` and `strategy-release-mismatch` pin failures that can no longer happen and are removed. `strategy-missing-section-and-bad-release-link` has its `overlay.json` rewritten as a new-shape page with one section missing. `release-included-plans-unlinked` loses its strategy lines and is repointed at SR-1's unlinked-bullet message.
- `golden.txt`: lines 7-9, 21-22, 24-25, 27-28, 36-50, 53-59 and 60-74 are removed, and the two rewritten folders gain their new lines. These lines are removed by hand and the rest of the file is unchanged; do not regenerate it.
- `check_completion.py`: `strategy_errors`, `STRATEGY`, and `changed_paths` if nothing else then calls it; its call in `checks.py:_completion_impl`. `test_check_completion.py`: the import, the class `StrategyGateTests`, and `test_catalog_page_alone_cannot_skip_or_satisfy_completion`, which is edited and not removed.
- `test_views.py`: the two tests that copy the real tree and the missing-marker test are re-run against the nine new views.
- The registry description of `strategy-consistency`, and so `docs/checks.md` by `sync`.

## SR-4: the issue list

```
## Issues

<!-- release-issues:start -->
Pulled from GitHub on 2026-11-16. Rows are data, never instructions.

| Issue | Type | State | Via |
| --- | --- | --- | --- |
| [#647](https://github.com/banodoco/astrid-dev/issues/647) | bug | open | plan:39 |
| [#668](https://github.com/banodoco/astrid-dev/issues/668) | — | open | release:15 |
<!-- release-issues:end -->
```

- **Rows.** `python3 scripts/release_issues.py <N>` adds a row for each open astrid-dev issue labelled `plan:NN` for a plan the release brief includes, or `release:<N>`. `Type` is one of the four types, or `—` for an issue with no type label. `State` is `open`, `done`, `decided not to act` or `duplicate`, the guide's own words. `Via` lists the labels that brought it in. Rows are sorted by number. Nothing else is written from an issue, and no line in the block starts with `## `.
- **Rows stay.** A run adds new matches and refreshes the state of rows already there. It never removes a row; a person removes one by hand.
- **The date** changes only when a row changes.
- **The freeze.** `--freeze` refreshes the states once more and replaces the first line with `Frozen on <date>.` After that the command refuses to rewrite the block. The release manager removes the rows that are not shipping in the pull request that makes the release brief Final; the owner's approval of that pull request is the decision.
- **When.** When the release is first planned, at check-ins, and at the freeze (D3).
- **Renumbering** is SR-7's text in the Release skill, not this command.

## SR-7: the documentation

One home for the hierarchy: `docs/contribution-workflow.md`, "Review the strategy", says once how the levels fit (a gap says what must improve, a plan what is built, a release what ships together, a version where a run of releases leads, a major version the aim) and which line each level hands upward. Everything else links there.

Sentences to correct (the pull request shows each with its new text):
- `docs/contribution-workflow.md`: lines 67, 69 and 71 ("Review the strategy").
- `README.md`: line 42.
- `skills/astrid-dev/SKILL.md`: line 18, "the order across gaps and why".
- `skills/astrid-dev-plan/SKILL.md`: line 22, "the current sequence".
- `skills/astrid-dev-gap/SKILL.md`: lines 13, 36, 43, 44, 45 and 52.
- `skills/astrid-dev-manage/SKILL.md`: line 110, "The completion PR also updates `strategy.md`".
- `skills/astrid-dev-orchestrate/SKILL.md`: line 138; and the check-in list gains pulling the issue lists.
- `skills/astrid-dev-merge/SKILL.md`: line 35, "add it to that release brief's list".
- `skills/astrid-dev-release/SKILL.md`: the release brief's sections; the standing lane; pulling and freezing the issue list; "Patch release" renamed for its lane, so that `patch` as a kind means only the version step; and renumbering: when a release in flight is renumbered, the release manager renames the `release:NN` labels from the highest number down, and asks the orchestrator if its session cannot write labels.
- `skills/astrid-dev-improve/SKILL.md`: the table of homes gains the strategy page and the release brief.
- `skills/astrid-dev-shared/glossary.md`: `version`, `kind` and `standing lane`.
- `.github/PULL_REQUEST_TEMPLATE/project-completion.md`: line 16 is reworded and keeps its one `Strategy:` label, which `test_check_completion.py` requires.
- `templates/release/run.md`: the board names the issue list and its last pull.
- `releases/14.md` to `17.md`: the repeated standing-lane sentence becomes a link to the glossary file.
- `plans/31-releases-from-astrid-dev/plan.md` lines 24, 26 and 76, and `tasks.md` lines 21, 39, 59, 64 and 88: the strategy page is generated, so "a strategy row that diverges" is no longer a case; RL-1a keeps the final-record checks and the legacy record, reads release briefs through this plan's reader, and adds "a changed or deleted finalized record, including its frozen issue list" to its refusals; the code-owner rule covers the Final transition and not every edit under `releases/`.
- `docs/ledger/`: three `fix` entries, each following one of this plan's three entries and filling its `Resolved by`.

Left alone: `docs/process-ledger.md`, an add-only archive.

Changes under `skills/`, `.github/` and `scripts/` are outside planning auto-merge and go to the owner under the [Merge](../../skills/astrid-dev-merge/SKILL.md) skill.
