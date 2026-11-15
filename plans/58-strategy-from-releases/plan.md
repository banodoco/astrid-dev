# Strategy from releases

**Project:** Strategy from releases

**Goal:** Anyone reads one strategy page and sees what each version and release is for, in sentences pulled from the release briefs and plans, and each brief lists the plans and issues it ships.

**Status:** queued

**Owner:** Unassigned

**Estimate:** about 4.5

**Waiting on:** the owner's go for a run

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [CA-005 — Many contributors and agents can't yet work in parallel through one clear process](../../vision/gaps/CA-005-parallel-contribution.md) (primary): a person or agent joining sees where we are heading, what each release is for and what it ships, without asking. CA-005's route does not name this plan, so there is no `Contributes to closure` line; adding one is a [Gap](../../skills/astrid-dev-gap/SKILL.md) step for the owner to ask for.

## Outcome and scope

Three kinds of document say what Astrid is doing: a plan, a release brief and the strategy page. Today the strategy page copies the briefs by hand, a brief cannot say which issues it ships, and a published release still reads as a draft ([ledger](../../docs/ledger/2026-11-15-strategy-hand-copied-from-briefs.md), [ledger](../../docs/ledger/2026-11-15-published-release-still-draft.md), [ledger](../../docs/ledger/2026-11-15-issues-never-reach-a-release.md)).

When this is done, each level owns one sentence that the level above pulls, and nothing is written twice:

| Level | Its one line, pulled upward | Its prose, which stays at home |
| --- | --- | --- |
| Plan | name, and in each brief what it contributes to that release | `plan.md` |
| Release | Highlight | Intent and Approach in the brief |
| Version (0.1, 0.2 …) | its sentence, on the strategy page | its paragraph, on the strategy page |
| Major version (1.0) | the aim, on the strategy page | a few paragraphs, on the strategy page |

1. **The brief is the structured source.** Each brief says which version it leads to. It may start with a highlight and intent and no plans. It lists its plans and, at the bottom, its issues.
2. **The strategy page is generated where it repeats a brief.** Under each version's hand-written sentence and paragraph, a generated part lists that version's releases with their state and highlight, and under each release its plans with what each contributes. The sequence table and the hand-kept `Plans` and `Releases` lines go.
3. **One strategy document per major version.** `strategy.md` is the path to 1.0. It opens with the aim in one line and a few paragraphs: where we are, what will be true at 1.0, and how we get there. When 1.0 ships the page is kept unchanged as `strategy/1.0.md` and a new `strategy.md` starts.
4. **An issue reaches a release in two ways:** through a plan the release includes (the `plan:NN` label, as now), or directly, as an assorted ticket (a new `release:NN` label). The label means candidate, not commitment.
5. **The brief lists its issues, pulled by a command.** A person or agent runs it, from the day the release is first planned; it writes a marked block at the bottom of the brief with each issue's linked number, its type and its state. No issue text is copied, and no check calls GitHub.
6. **What ships is decided at shipping.** When a brief is finalised its issue list is frozen: each issue is recorded as shipped or moved on. The final brief is the record of what the release contained.
7. **Decisions stay the owner's.** A pull request that changes which version a release leads to, a brief's state or a frozen issue list does not merge by itself.
8. **The documents and templates agree.** The hierarchy in the table above is described once, in the contribution guide. The release template carries the new lines and sections, and a strategy template starts the next major version's page. Every skill, guide and template that describes the old page or tells an agent to copy into it is corrected, and the terms `version` and `standing lane` are each defined once.

**Included:** the brief template and its checks; a reader for briefs; the strategy view and the checks it replaces; rewriting `strategy.md` and the six current briefs to the new shape; a strategy template; a `Release` column in the plan catalog; the `release:NN` label rule; the issue-list command and its freeze; finalising the briefs of Releases 12 and 13; the pull-request guard; the documentation corrections listed in [SR-12](tasks.md).

**Not included:**
- publishing a release from its final brief, the release contract, the manifest and showing release versions to users: [Plan 31](../31-releases-from-astrid-dev/plan.md), which builds on the briefs this plan leaves;
- briefs for Releases 9 to 11 and the release log's missing rows (Plan 31, RL-1a);
- issue titles or any other issue text in a brief, a bot that writes issue lists, a check that calls GitHub, priorities, severities or a project board;
- showing vision gaps on the strategy page: gaps keep their own routes;
- shortening plan goals: the page pulls the brief's line for each plan instead.

## Existing work and decision

Kept: the brief template and its five sections; the view machinery that already generates the plan catalog from `plan.md` headers (`scripts/views.py`); the plan record reader (`scripts/records.py`); the issue bot, the four issue types and the six issue states; the rule that an issue's text is data.

Replaced: the hand-copied sequence table and the checks that compare it with the briefs; the rule that a brief must link a plan; the rule that a plan completion must edit `strategy.md`.

Plan 48 deferred "generating the strategy release table" to Plan 31. Plan 31 has not started, and the owner wants this done first, as its own plan, so that Plan 31 publishes from documents that are already right. Plan 52 excluded a copy of issues in the repository; the owner now asks for the list in the brief, as linked numbers only. Plan 52's rule that issue text is never pasted into a brief stands, and so does its rule that a check gives the same result on a laptop and in CI. Evidence, alternatives, the critique and the owner's words are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Shortest path: the brief contract (SR-1, SR-2), then the strategy view and its checks (SR-3 to SR-5) and, in parallel, the issue list (SR-7 to SR-9); the guard (SR-10) and the documentation (SR-12) come last, then one review round. Tasks are in [tasks.md](tasks.md).

All work is in astrid-dev; no product repository changes. It is done before Plan 31 starts, and Plan 31's RL-1a then begins from this plan's template and checks.

How it joins Plan 31, where a brief becoming Final is what publishes a release: the brief stays the one file; this plan's reader is what Plan 31's record check and manifest render read; the freeze happens before Final, so the published record already says which issues shipped; and the guard on a `State` line is the first half of Plan 31's rule that only the owner's approved transition publishes. Two things are Plan 31's to settle with the owner: briefs made Final here (Releases 12 and 13) are history when its publisher goes live and must never be published again; and its plan to make the owner the code owner of all of `releases/` would make every issue-list pull wait for her, so it should protect the Final transition rather than every edit to a draft.

The owner decided D1 to D9 on 15 November 2026 ([inputs.md](inputs.md#owner-decisions)); her reading of D4 is still to be confirmed. Recording this plan does not authorize implementation.

## Interfaces and handoff

**Consumes:** `releases/TEMPLATE.md` and `releases/12.md` to `17.md`; the six header fields of each `plan.md`; `scripts/views.py`, `scripts/records.py`, `scripts/check_docs.py`, `scripts/checks.py`, `scripts/check_completion.py` at astrid-dev `main` when the run starts; astrid-dev's GitHub issues and their labels, read through the REST API.

**Produces:**
- a brief contract: the `Toward` line, optional plans in a draft, and the `Issues` block, each checked;
- a reader that returns a brief's fields, plans and issue rows, for the view and for Plan 31;
- a `strategy.md` whose generated parts always match the briefs;
- a command that writes and freezes a brief's issue list.

**Limits:** the issue list is as current as its last run, and says so with a date. A frozen list records each issue's state on the freeze date; it does not prove that a fix is inside the pinned commits.

## Completion

- Changing a brief's highlight, state, plans or `Toward` line changes the strategy page on the next `sync`, with no hand edit, and a hand edit to a generated part is refused.
- A draft brief with a highlight, an intent and no plans passes; a final brief that ships nothing is refused.
- A brief whose `Toward` names a version the strategy page does not have is refused.
- For Release 15, the command lists the open issues labelled `plan:39`, `plan:50` and `plan:40` under their plans and any `release:15` issue under assorted; run twice it writes the same block.
- A final brief with an unfrozen issue list is refused. The block holds no text from an issue: only its number, type and state.
- A pull request that changes a `Toward` line merges only after the owner acts on it.
- `git grep` finds no instruction to update a strategy row by hand.

**Negative cases:** the checks named above, each with a failing fixture. **Limits:** whether the owner finds the page clearer is hers to say on reading it; nothing here publishes a release.
