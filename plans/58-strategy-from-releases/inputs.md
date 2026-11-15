# Inputs — Strategy from releases

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner asked for this on 15 November 2026 in the planning session, recorded on the [strategy page](../../strategy.md#decisions); her words are under [What the owner said](#what-the-owner-said). She chose a plan of its own, done before Plan 31: "the existing plan is one that basically makes releases happen based on these docs but I'd like to get this all done first. And of course fix the documentation. And merge the plan to main." D1 to D8 below are still hers to make.

**Prior art:** Five read-only readings of astrid-dev `main` at `a398525a526a2bfe0eb2cccac47732c3491c467d` on 15 November 2026, one each on the checks and fixtures, the release system and Plan 31, issue intake and Plan 52, every plan header, and the rules for changing astrid-dev; and one read of astrid-dev's open issues on GitHub the same day.

*The strategy page and its checks.*
- [`strategy.md`](../../strategy.md) repeats each brief's state, highlight and plan list in its Sequence table, and `strategy_errors` in [`scripts/check_docs.py`](../../scripts/check_docs.py) compares the copies. It then builds its version rules from the table's rows, so a copy is read back as a source.
- Which release belongs to which version is written only on the strategy page. No brief and no plan says it.
- A generated region already exists for the plan catalog ([`scripts/views.py`](../../scripts/views.py), [extending](../../docs/extending.md#add-a-generated-view)). One view owns one region; several views may share a file.
- A pull request's generated page is compared with its sources only when the pull request touched that page; otherwise `main` refreshes it after merge. The generated pages were current on the planning commit.
- A plan completion must change `strategy.md` (`check_completion.py:strategy_errors`); the completion form's `Strategy:` line is read by nothing.
- [Plan 48](../48-one-record-model/plan.md) recorded the hand copy and deferred "generating the strategy release table" to Plan 31.
- Pinned today: 352 unit tests pass; five `strategy-*` and four release fixture folders and their lines in `scripts/fixtures/golden.txt`; eight tests in `scripts/test_check_docs.py`.

*Releases.*
- [`releases/TEMPLATE.md`](../../releases/TEMPLATE.md) and `release_errors` give every brief a number, a state, a one-line highlight, an intent, an approach, at least one linked plan and a publication section. Each included plan has a sentence saying what it contributes.
- All six briefs say `State: Draft`. Release 12 was published on 12 November 2026 ([decision log](../../releases/12/decisions.md)); its shipped commits are only in its [gate record](../../releases/12/gate-record.md). The [release log](../releases.md) has rows for Releases 9 and 10. Releases 12 and 13 have no release version in the repository.
- Release versions follow [Plan 29](../29-update-and-release/inputs.md) decision 7: `major.minor.patch` worked out from the release number, "patch by default, minor or major only when the owner declares it". The strategy page's 0.1 is a different thing with the same word, and Release 17 is titled "Version 0.1, the stable release".
- A patch release takes the next number and renumbers a release in flight ([Release skill](../../skills/astrid-dev-release/SKILL.md)), so a draft's number can change.
- "A standing lane for fixes" appears in briefs 14 to 17 and on the strategy page and is defined nowhere. `## Included pull requests` is the only list a brief has besides its plans; no brief uses it.
- In Release 12, known issues were kept in three places that differ; in Release 13, each tester run was one GitHub issue with an improvised `r13-tester` label.
- [Plan 31](../31-releases-from-astrid-dev/plan.md) is queued and unassigned with no task done. It plans the final record, the release contract, publishing and release versions on screen. It plans checks that the strategy page agrees with the briefs, not generation, and no issue list.

*Issues.*
- [The issue rules](../../docs/contribution-workflow.md#issues): four types, six states, labels `plan:NN` and `gap:ID`, a closed list of triage actions, and "an issue becomes work only through a task row".
- Plan 52's [first triage](../52-issue-intake/evidence/triage-first-run.md): "No task row in any plan cites an open issue."
- On GitHub on 15 November 2026: 60 open issues; 43 carry a `plan:NN` label and 17 carry none; none is `planned`. Plans 39, 50 and 40, which Release 15 includes, have 35 between them.
- [Plan 52](../52-issue-intake/plan.md) excluded "a copy of issues in the repository, a generated page of issues, or any check that calls GitHub". Only the last has a stated reason: "a check must give the same result on a laptop and in CI". Most of its decisions were made by the orchestrator under delegation and are the owner's to reverse.
- The issue bot only labels ([`scripts/issue_intake.py`](../../scripts/issue_intake.py)); it has `issues: write` and `contents: read`.

*Plans.*
- All 56 plans have the six header fields. 36 goals are longer than 160 characters and one is 611. The briefs' contribution sentences are short and say what lands in that release.
- Plans 29 and 40 are each in two releases. 27 open plans are in no release and no candidate list.

*Rules for the change.*
- [Principles](../../docs/contribution-design-principles.md) 2 (one home per fact; generate into a marked region never read back), 7 (checks see structure; people decide), 8 (change only for a recorded failure) and 9 (one word per thing) bear on it.
- [Planning auto-merge](../../scripts/auto_merge.py) merges a member's pull request that touches only `plans/`, `releases/`, `vision/`, `docs/`, `strategy.md` or `README.md` once checks pass, unless it is a draft, has the `hold` label or says `Owner decision needed`.

**Approach:** see [plan.md](plan.md#existing-work-and-decision). Alternatives considered:
- *Leave it to Plan 31.* Plan 31 is 12.5 days, has not started and waits on Plan 29; the page stays hand-copied until then, and Plan 31 would publish from briefs that are wrong today. The owner chose to do this first.
- *Keep the hand copy and its checks.* This is today's state and the recorded complaint.
- *Generate the whole page.* The aim, each version's sentence and paragraph, the candidates and the decisions are judgment and have no other home; they stay hand-written.
- *Pull each plan's goal.* 36 goals are too long for a list, and a goal is wrong for a plan that ships across two releases. The brief's sentence fits (D1).
- *A GitHub milestone per release.* It puts the list outside the repository, where no check sees it and no pull request reviews it.
- *A bot that writes the issue list.* It needs write access to `main` and a view whose source is not in the repository. A command a person or agent runs needs neither (D3).
- *Hand-written fix lines in the brief.* The owner asked for the list to be pulled; Release 15 alone would need about 35 lines.
- *A list of unplaced plans on the strategy page.* The catalog already lists every plan; one `Release` column there shows the same thing without a second list.

Chosen: the brief as the structured source; generated parts on the strategy page; a pulled, checked-for-shape issue block frozen at finalisation.

**Challenge:** Pending — an independent critique of this draft against the code is required because the plan changes astrid-dev's own checks. Next: run it and record the findings in review.md.

**Proof and limits:** Completion is in [plan.md](plan.md#completion). Not verified while planning: whether the App that refreshes generated pages on `main` is configured (the pages were current, which suggests it is); the live label list; whether `gh api` reaches the issues endpoint from every session that will run the command (the issue rules already file through it). The frozen list records each issue's state on a date and does not prove a fix is in the pinned commits. Whether the page is clearer is the owner's to judge on reading it.

**Review rounds:** Pending — recommended: one final round, because the plan rewrites checks other plans rely on and puts text anyone can write into files agents read. No review stop: the estimate is under five days and the brief contract is covered by its own tests. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, and the advisor session.

## What the owner said

In the planning session on 15 November 2026 (dictated; spelling tidied, words unchanged):

- On the page today: "It feels pretty flat in terms of understanding." And: "How should that be populated? By the release docs which each have structured data that then feeds into it?"
- "This should be a 'Path to V.1' and … each major release should be able to have a description to start with no plans, based on the release docs."
- "I think we should have them associated with kind of plans, but then we should also just have them associated with releases, like an assorted tickets kind of thing associated with release."
- "We have releases which talk about all the stuff related to stuff released, then we have plans, and then the basically strategy thing. If it pulls this stuff from that, includes the context, like the one-line sentence from each of them, then includes in the strategy doc some for each of the kind of big initiatives like 0.1 to 0.2, overarching context as well … just like a paragraph usually on an overall initiative and what it's trying to achieve."
- "Each release can contain like obviously plans and also assorted bug releases … in the release you can say for whatever 46 different issues at the bottom of that release that's pulled … to actually decide which are actually included in it when we're actually shipping."
- "These strategy documents should be kind of by, like major version, so this one's all the way up to 1.0 basically. And then from there, we'll probably like start new documents … we probably need to have … a one-line summary of the overall strategy, maybe like a few paragraphs in."
- "The existing plan is one that basically makes releases happen based on these docs but I'd like to get this all done first. And of course fix the documentation. And merge the plan to main."

## Owner decisions

- **D1 The line shown for each plan under a release.** (a) The plan's name and the brief's sentence on what it contributes to that release. (b) The plan's goal. Recommendation: (a); it is short, already written and right for a plan in two releases.
- **D2 Issue titles in a brief.** Anyone can write a title, and agents read briefs; the issue rules say issue text is never pasted into a brief. (a) Titles reduced to plain text, in a block marked as data, as the one exception to that rule. (b) Numbers, types and states only. (c) A sentence in our own words for each, by hand. Recommendation: (a); 35 bare numbers cannot be read, and 35 hand-written sentences will not be kept up.
- **D3 Who pulls the list.** (a) A command run by the release manager or the orchestrator at check-ins and at the freeze, committed by pull request. (b) A workflow that writes to `main`. Recommendation: (a).
- **D4 The words.** `**Toward:** 0.1` on a brief. "Version" means a step on the strategy page (0.1 to 1.0). "Release version" means what users see (0.0.14). The release that completes a version is the one the owner declares a minor release version under Plan 29's decision 7, so Release 17 would be release version 0.1.0. Recommendation: accept, or name other words.
- **D5 Releases 12 and 13.** (a) Finalise their briefs in this plan from their gate records, with the owner's go for each (SR-11). (b) Leave them as drafts for Plan 31; until then the page shows them as drafts and the hand-written "Focus now" says they are out. Recommendation: (a) for Release 12, and for Release 13 once its record is complete.
- **D6 How the owner's decisions are kept from merging by themselves.** (a) A check that fails a pull request changing a `Toward` line, a `State` line or a frozen list unless its body says `Owner decision needed`, which is the phrase that already holds auto-merge. (b) Teach auto-merge to read the diff. Recommendation: (a); it reuses the existing hold.
- **D7 Who may apply `release:NN`.** (a) Triage, as a candidate only. (b) Only the release manager or the owner. Recommendation: (a); the commitment is the freeze, which is the owner's.
- **D8 The words at the top of the page.** The planner drafts the three paragraphs from the briefs and the vision; the owner rewrites them. The aim for 1.0 was proposed by the advisor on 15 November 2026 and is still hers to change. Recommendation: draft, then her edit.
- **D9 Order.** Decided 15 November 2026 (the owner): this plan is done before Plan 31. It is placed directly above Plan 31 in [priority.md](../priority.md); she may move it.

## Source identities

astrid-dev `main` at `a398525a526a2bfe0eb2cccac47732c3491c467d` (15 November 2026) for every reading above. No product repository is read or changed. The run starts from astrid-dev `main` at its start and records that commit here.

## References

- Ledger: [the strategy page is hand-copied](../../docs/ledger/2026-11-15-strategy-hand-copied-from-briefs.md); [a published release still reads as a draft](../../docs/ledger/2026-11-15-published-release-still-draft.md); [issues never reach a release](../../docs/ledger/2026-11-15-issues-never-reach-a-release.md).
- [Plan 31](../31-releases-from-astrid-dev/plan.md), [Plan 48](../48-one-record-model/plan.md), [Plan 52](../52-issue-intake/plan.md).
- [Contribution design principles](../../docs/contribution-design-principles.md); [Improve](../../skills/astrid-dev-improve/SKILL.md).
