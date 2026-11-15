# Strategy from releases

**Project:** Strategy from releases

**Goal:** Anyone reads one strategy page and sees what each version and release is for, in sentences pulled from the release briefs and plans, and each release brief lists the plans and issues it ships.

**Status:** active

**Owner:** Plan 58 manager (ChatGPT session 3417d5f77996)

**Estimate:** about 4.5

**Waiting on:** —

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary): a person or agent joining sees where we are heading, what each release is for and what it ships, without asking. CA-005's route does not name this plan, so there is no `Contributes to closure` line; adding one is a [Gap](../../skills/astrid-dev-gap/SKILL.md) step for the owner to ask for.

## Outcome and scope

Three kinds of document say what Astrid is doing: a plan, a release brief and the strategy page. Today the strategy page copies the release briefs by hand, a release brief cannot say which issues it ships, and a published release still reads as a draft ([ledger](../../docs/ledger/2026-11-15-strategy-hand-copied-from-briefs.md), [ledger](../../docs/ledger/2026-11-15-published-release-still-draft.md), [ledger](../../docs/ledger/2026-11-15-issues-never-reach-a-release.md)).

When this is done, each level owns one sentence that the level above pulls, and nothing is written twice:

| Level | Its one line, pulled upward | Its prose, which stays at home |
| --- | --- | --- |
| Plan | name, and in each release brief what it contributes to that release | `plan.md` |
| Release | Highlight | Intent and Approach in the release brief |
| Version (0.1, 0.2 …) | its sentence, on the strategy page | its paragraph, on the strategy page |
| Major version (1.0) | the aim, on the strategy page | a few paragraphs, on the strategy page |

1. **The release brief is the structured source.** It says what kind of release it is: a patch, a minor or a major (D10). It may start with a highlight and intent and no plans. It lists its own plans and, at the bottom, its own issues, and never another release's.
2. **The strategy page is generated where it repeats a release brief.** Under each version's hand-written sentence and paragraph, a generated part rolls up everything since the previous minor release: the minor or major release that ships the version, with its state and highlight; the patch releases on the way to it, as one line of linked titles; the plans those releases include, each once with its release and what it contributes; and, for each release whose issue list is frozen, how many issues it shipped (D11). The nine minor regions are followed in the model by a generated 1.0 region under the major aim; pending patches after 0.9 belong there (D13). The sequence table and the hand-kept `Plans` and `Releases` lines go.
3. **One strategy document per major version.** `strategy.md` is the path to 1.0. It opens with the aim in one line and a few paragraphs: where we are, what will be true at 1.0, and how we get there. When 1.0 ships the page is kept as `strategy-1.0.md` beside it and a new `strategy.md` starts.
4. **An issue reaches a release in two ways:** through a plan the release includes (the `plan:NN` label, as now), or directly, as an assorted ticket (a new `release:NN` label). The label means candidate, not commitment.
5. **The release brief lists its issues, pulled by a command.** A person or agent runs it, from the day the release is first planned; it writes a marked block at the bottom of the release brief with each issue's linked number, its type, its state and how it came in. No issue text is copied, and no check calls GitHub.
6. **What ships is decided at shipping.** The freeze stamps each row with its state on that date; the release manager then edits the list in the pull request that makes the release brief Final, and the owner approves that pull request. The final release brief is the record of what the release contained.
7. **Decisions stay the owner's.** A pull request that changes a release brief's kind or state is not merged automatically.
8. **The documents and templates agree.** The hierarchy in the table above is described once, in the contribution guide. The release template carries the new line and section. Every skill, guide and template that describes the old page or tells an agent to copy into it is corrected, and `version`, `kind` and `standing lane` are each defined once.

**Included:** the release template, its checks and one reader for release briefs; the strategy views, the checks they replace and the rewritten `strategy.md`; the `release:NN` label rule; the issue-list command and its freeze; the auto-merge rule for kind and state; the documentation corrections in [SR-7](tasks.md).

**Not included:**
- publishing a release from its final release brief, the release contract, the manifest and showing versions to users: [Plan 31](../31-releases-from-astrid-dev/plan.md), which builds on the release briefs this plan leaves;
- making the release briefs of Releases 12 and 13 Final: Plan 31 (D5);
- release briefs for Releases 9 to 11 and the release log's missing rows: no plan covers these today, and this one does not add them;
- issue titles or any other issue text in a release brief, a bot that writes issue lists, a check that calls GitHub, priorities, severities or a project board;
- a list of plans that are in no release: the catalog lists every plan;
- showing vision gaps on the strategy page: gaps keep their own routes;
- shortening plan goals: the page pulls the release brief's line for each plan instead.

## Existing work and decision

Kept: the release template and its five sections; the view machinery that already generates the plan catalog from `plan.md` headers (`scripts/views.py`), unchanged; the plan record reader (`scripts/records.py`); the issue bot, the four issue types and the six issue states; the rule that an issue's text is data and is never pasted into a release brief.

Replaced: the hand-copied sequence table and the checks that compare it with the release briefs; the rule that a draft release brief must link a plan; the rule that a plan completion must edit `strategy.md`.

Plan 48 deferred "generating the strategy release table" to Plan 31. Plan 31 has not started, and the owner wants this done first, as its own plan, so that Plan 31 publishes from documents that are already right. Plan 52 excluded a copy of issues in the repository; the owner now asks for the list in the release brief, as linked numbers only, and Plan 52's rule that a check gives the same result on a laptop and in CI stands. Evidence, alternatives and the owner's words are in [inputs.md](inputs.md#planning-evidence); the independent critique and what was done with each finding are in [review.md](review.md).

## Sequence and readiness

Shortest path: the release brief contract (SR-1), then the generated page in one change (SR-2); beside it the issue list (SR-4, SR-5); then the words (SR-3), the auto-merge rule (SR-6) and the documentation (SR-7), and one review round. Tasks are in [tasks.md](tasks.md).

All work is in astrid-dev; no product repository is read or changed. Work lands on `int/58-strategy-from-releases`, one pull request per task, and reaches `main` in one merge with the owner's go: a registered view without its markers on the page breaks `sync` for every pull request, so the parts cannot reach `main` separately.

**How it joins Plan 31,** where a release brief becoming Final is what publishes a release: the release brief stays the one file; this plan's reader is what Plan 31's record check and manifest render read; the freeze happens before Final, so the published record already says which issues shipped; and kind is declared in the release brief from the draft, so Plan 31's version step has its source. Plan 31's approval of the Final transition (a code owner's review) replaces this plan's auto-merge rule for `State` when it lands. Releases 12 and 13 are made Final in Plan 31, not here (D5). One thing is Plan 31's to settle with the owner: its plan to make her the code owner of all of `releases/` would make every issue-list pull wait for her, so it should protect the Final transition and not every edit to a draft.

The owner decided D1 to D12 in planning and D13 to D14 during this run on 15 November 2026 ([inputs.md](inputs.md#owner-decisions), [run decisions](inputs.md#run-decisions)). The recorded Run start authorizes implementation within its limits; D8 still requires the owner's wording for SR-3.

## Interfaces and handoff

**Consumes:** `releases/TEMPLATE.md` and `releases/12.md` to `17.md`; the six header fields of each `plan.md`; `scripts/views.py`, `scripts/records.py`, `scripts/check_docs.py`, `scripts/checks.py`, `scripts/check_completion.py` and `scripts/auto_merge.py` at astrid-dev `main` when the run starts; astrid-dev's GitHub issues and their labels, read through the REST API.

**Produces:**
- a release brief contract: the `Kind` line, `None yet` for a draft without plans, and the `Issues` block, each checked;
- a reader that returns a release brief's fields, plans and issue rows, for the views and for Plan 31;
- a `strategy.md` whose generated parts match the release briefs;
- a command that writes and freezes a release brief's issue list.

**Limits:**
- After a release brief changes, the strategy page on `main` is stale until the refresh job commits it (one CI run); a pull request compares a generated part only if it touched it.
- The issue list is as current as its last run and says when that was.
- A frozen list records each issue's state on the freeze date. It does not prove a fix is inside the pinned commits, and a fix merged only to an integration branch still reads as open; the release manager corrects the list by hand before Final.
- The auto-merge rule keeps a change from merging by itself; it does not stop a person with merge rights.

## Completion

- Changing a release brief's highlight, state, kind or plans changes the strategy page on the next `sync`, with no hand edit, and a hand edit to a generated part is refused.
- A draft release brief with a highlight, an intent and `None yet` for its plans passes; a plan line without a link is refused.
- With Release 17 marked minor, the page shows it under 0.1 with its highlight, the earlier releases on one line, and their plans, each once; marking a later release minor fills 0.2 with no edit to the page.
- A major release appears in full in the generated 1.0 region with its preceding patches, plan contributions and frozen counts; patches after 0.9 appear there while awaiting it. More than nine minors and releases after a major are refused.
- For Release 15, the command lists the issues labelled `plan:39`, `plan:50` and `plan:40` and any labelled `release:15`, each once; an issue closed between two runs keeps its row; a second run on the same day changes nothing.
- The block holds no text from an issue. A final release brief with an unfrozen block is refused.
- A pull request that adds or changes a `Kind` or `State` line is not eligible for auto-merge; one that changes only an Approach is.
- No skill, guide or template tells an agent to update a strategy row by hand ([SR-7](tasks.md) lists each sentence).

**Negative cases:** the refusals named above, each with a failing test. **Limits:** whether the owner finds the page clearer is hers to say on reading it; nothing here publishes a release.
