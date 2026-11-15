# Inputs — Strategy from releases

[Plan](plan.md) · [Tasks](tasks.md) · [Review](review.md)

## Planning evidence

**Scope decision:** Accepted — the owner asked for this on 15 November 2026 in the planning session (https://claude.ai/code/session_011EzfW1ptd55F1pnWRTb25F); her words are under [What the owner said](#what-the-owner-said). She chose a plan of its own, done before Plan 31: "the existing plan is one that basically makes releases happen based on these docs but I'd like to get this all done first. And of course fix the documentation. And merge the plan to main." She decided D1 to D12 the same day.

**Prior art:** Five read-only readings of astrid-dev `main` at `a398525a526a2bfe0eb2cccac47732c3491c467d` on 15 November 2026, one each on the checks and fixtures, the release system and Plan 31, issue intake and Plan 52, every plan header, and the rules for changing astrid-dev; and two reads of astrid-dev's open issues on GitHub the same day.

*The strategy page and its checks.*
- [`strategy.md`](../../strategy.md) repeats each release brief's state, highlight and plan list in its Sequence table, and `strategy_errors` in [`scripts/check_docs.py`](../../scripts/check_docs.py) compares the copies. It then builds its version rules from the table's rows, so a copy is read back as a source.
- Which release belongs to which version is written only on the strategy page. No release brief and no plan says it.
- A generated region already exists for the plan catalog ([`scripts/views.py`](../../scripts/views.py), [extending](../../docs/extending.md#add-a-generated-view)). One view owns one region; several views may share a file. A registered region view whose markers are missing raises, and `sync` does not catch it.
- Every pull request runs `sync` and then the always-on checks. A generated page is compared with its sources only when the pull request touched it; otherwise the refresh job commits it on `main` after merge. That job is live: it committed refreshed views on 13 and 15 November 2026.
- A plan completion must change `strategy.md` (`check_completion.py:strategy_errors`). No check reads the completion form's `Strategy:` line, though a test requires the form to have exactly one.
- [Plan 48](../48-one-record-model/plan.md) recorded the hand copy and deferred "generating the strategy release table" to Plan 31.
- Pinned today: 352 unit tests pass; five `strategy-*` and four release fixture folders and their lines in `scripts/fixtures/golden.txt`; eight tests in `scripts/test_check_docs.py` call `strategy_errors`.

*Releases.*
- [`releases/TEMPLATE.md`](../../releases/TEMPLATE.md) and `release_errors` give every release brief a number, a state, a one-line highlight, an intent, an approach, at least one linked plan and a publication section. Each included plan has a sentence saying what it contributes.
- All six release briefs say `State: Draft`. Release 12 was published on 12 November 2026 ([decision log](../../releases/12/decisions.md)); its App, Agent and Runtime commits are only in its [gate record](../../releases/12/gate-record.md), which does not hold the other five keys a Final payload needs. Release 13 has no gate record. The [release log](../releases.md) has rows for Releases 9 and 10. Releases 12 and 13 have no version in the repository.
- Versions follow [Plan 29](../29-update-and-release/inputs.md) decision 7: `major.minor.patch` worked out from the release number, "patch by default, minor or major only when the owner declares it". Plan 31 writes `version` and `kind` into a release brief only when it becomes Final. The strategy page writes 0.1 as a step of its own, while Release 17 is titled "Version 0.1, the stable release": one numbering, described in two places.
- The [Release skill](../../skills/astrid-dev-release/SKILL.md) uses "Patch release" for a small fix-only release, a second sense of the word. A patch release takes the next number and renumbers a release in flight, so a draft's number can change.
- "A standing lane for fixes" appears in release briefs 14 to 17 and on the strategy page and is defined nowhere. `## Included pull requests` is the only list a release brief has besides its plans; none uses it.
- In Release 12, known issues were kept in more than one place and the lists differ; in Release 13, each tester run was one GitHub issue with an improvised `r13-tester` label.
- [Plan 31](../31-releases-from-astrid-dev/plan.md) is queued and unassigned with no task done. It plans the final record, the release contract, publishing and versions on screen, and one legacy record it validates against the served manifest. It plans checks that the strategy page agrees with the release briefs, not generation, and no issue list. It would make the owner the code owner of all of `releases/`.

*Issues.*
- [The issue rules](../../docs/contribution-workflow.md#issues): four types, six states, labels `plan:NN` and `gap:ID`, a closed list of triage actions, and "an issue becomes work only through a task row".
- Plan 52's [first triage](../52-issue-intake/evidence/triage-first-run.md): "No task row in any plan cites an open issue."
- On GitHub on 15 November 2026, at the planning read: 60 open issues; 43 carry a `plan:NN` label and 17 carry none; none is `planned`; Plans 39, 50 and 40, which Release 15 includes, have 35 between them. Later the same day 76 were open, 23 with no type label and five with more than one `plan:` label.
- The issues endpoint is reachable from a cloud session through `contribution_api.request`; it also returns pull requests.
- [Plan 52](../52-issue-intake/plan.md) excluded "a copy of issues in the repository, a generated page of issues, or any check that calls GitHub". Only the last has a stated reason: "a check must give the same result on a laptop and in CI". Most of its decisions were made by the orchestrator under delegation and are the owner's to reverse. Its II-13 row, on the same Issues section, is open.
- The issue bot only labels ([`scripts/issue_intake.py`](../../scripts/issue_intake.py)).

*Plans.*
- All 56 plans have the six header fields. 36 goals are longer than 160 characters and one is 611. The release briefs' contribution sentences are short and say what lands in that release.
- Plans 29 and 40 are each in two releases. 27 open plans are in no release and no candidate list.

*Rules for the change.*
- [Principles](../../docs/contribution-design-principles.md) 2 (one home per fact; generate into a marked region never read back), 7 (checks see structure; people decide), 8 (change only for a recorded failure) and 9 (one word per thing) bear on it. None needs changing.
- [Planning auto-merge](../../scripts/auto_merge.py) merges a member's pull request that touches only `plans/`, `releases/`, `vision/`, `docs/`, `strategy.md` or `README.md` once checks pass, unless it is a draft, has the `hold` label or says `Owner decision needed`. The files JSON it reads carries each file's patch.

**Approach:** see [plan.md](plan.md#existing-work-and-decision). Alternatives considered:
- *Leave it to Plan 31.* Plan 31 is 12.5 days, has not started and waits on Plan 29; the page stays hand-copied until then, and Plan 31 would publish from release briefs that are wrong today. The owner chose to do this first.
- *Keep the hand copy and its checks.* This is today's state and the recorded complaint.
- *Generate the whole page.* The aim, each version's sentence and paragraph, the candidates and the decisions are judgment and have no other home; they stay hand-written.
- *One generated region below the hand-written version text.* It needs no thought about markers, and it separates a version's words from its releases, which is the complaint. Nine static views keep them together with no change to the view machinery.
- *A `Toward` line naming the version.* It is a second fact beside the kind, which Plan 29 and Plan 31 already have; kind alone gives the version each release leads to.
- *Pull each plan's goal.* 36 goals are too long for a list, and a goal is wrong for a plan that ships across two releases. The release brief's sentence fits (D1).
- *Copy the patches' plans and issues into the minor release's brief.* The same plan and issue would be recorded in two releases; the page rolls them up instead.
- *Pull issue titles into the release brief.* Anyone can write a title, and agents read release briefs; the owner chose linked numbers (D2).
- *A GitHub milestone per release.* It puts the list outside the repository, where no check sees it and no pull request reviews it.
- *A bot that writes the issue list.* It needs write access to `main` and a view whose source is not in the repository. A command a person or agent runs needs neither (D3).
- *A catalog column for each plan's release, a strategy template, a rule that a final release brief ships something.* Dropped on the critique: no requirement or recorded failure asks for them.

Chosen: the release brief as the structured source; generated parts on the strategy page; a pulled issue block, checked for shape and frozen before Final.

**Challenge:** Reviewed — an independent critique of the first draft against the code, recorded in [review.md](./review.md). Accepted: all four blocking findings (one change for the view, checks and page; nine static views; issue rows that stay and a freeze the release manager edits; finalising Releases 12 and 13 taken out of the task list) and every other finding, including dropping the catalog column, the strategy template and two rules, merging two tasks, and delivering the owner's guard in auto-merge. Left to the owner, and since decided: D5 and D12. Rejected: none.

**Proof and limits:** Completion and its limits are in [plan.md](plan.md#completion). Not verified while planning: branch protection and code owners on GitHub; whether Plan 52's II-13 has landed; the line numbers and test names in the cards beyond the critique's reading, which the cards say to re-check. The `Kind` line and the roll-up came after the critique and are covered by the final review round.

**Review rounds:** Agreed — one final review round, confirmed by the owner in the run-start message on 15 November 2026. No review stop. Findings become task rows and the integration merge waits for their resolution.

**Run start:** Authorized on 15 November 2026 by the owner's message in this ChatGPT conversation: "This message is my go for the run." Covers SR-1 to SR-7 and the one final review round. Accountable agent and project owner: the Plan 58 manager, ChatGPT `/root`, session/workspace `3417d5f77996`; advisor: none assigned (a separate high-judgment advisor may be consulted if needed). The manager may create branches and pull requests on astrid-dev, merge task pull requests into `int/58-strategy-from-releases`, merge its own progress pull requests, run the repository's checks and tests, and read astrid-dev issues for SR-4. The owner's go is required for merging the integration branch into `main`, any scope or decision change, the SR-3 wording (which the owner rewrites), and anything touching a product repository or publishing a release. A refused command is brought to the owner without retrying it. One pull request per task; a draft integration pull request opens as soon as the first task lands and stays current; after all tasks and review, the manager opens the completion pull request from the completion template. The owner is notified when the draft is open, when the SR-3 draft is ready and when the completion pull request is open.

## What the owner said

In the planning session on 15 November 2026 (dictated or typed; spelling tidied, words unchanged):

- On the page today: "It feels pretty flat in terms of understanding." And: "How should that be populated? By the release docs which each have structured data that then feeds into it?"
- "This should be a 'Path to V.1' and … each major release should be able to have a description to start with no plans, based on the release docs."
- "I think we should have them associated with kind of plans, but then we should also just have them associated with releases, like an assorted tickets kind of thing associated with release."
- "We have releases which talk about all the stuff related to stuff released, then we have plans, and then the basically strategy thing. If it pulls this stuff from that, includes the context, like the one-line sentence from each of them, then includes in the strategy doc some for each of the kind of big initiatives like 0.1 to 0.2, overarching context as well … just like a paragraph usually on an overall initiative and what it's trying to achieve."
- "Each release can contain like obviously plans and also assorted bug releases … in the release you can say for whatever 46 different issues at the bottom of that release that's pulled … to actually decide which are actually included in it when we're actually shipping."
- "These strategy documents should be kind of by, like major version, so this one's all the way up to 1.0 basically. And then from there, we'll probably like start new documents … we probably need to have … a one-line summary of the overall strategy, maybe like a few paragraphs in."
- "The existing plan is one that basically makes releases happen based on these docs but I'd like to get this all done first. And of course fix the documentation. And merge the plan to main."
- "See the way we have major releases, minor, and patches? Should we mark that in the release already? And only show greater than minor in the strategy.md? (they're the ones that'll go from 0.1 to 0.2 once we have that set up)"
- "Should it include all the plans and issues done in patches before too? Or what's a nice way to do this?"

## Owner decisions

All decided by the owner on 15 November 2026 in the planning session.

- **D1 The line shown for each plan under a release.** (a) The plan's name and the release brief's sentence on what it contributes. (b) The plan's goal. **Decided: (a), "Yes, we should also make sure templates cover and include this."** The release template says what that sentence is for (SR-1).
- **D2 Issue titles in a release brief.** **Decided: "Probably should just include hyperlinked issue number."** The block holds each issue's linked number with its type, its state and the label that brought it in, which are our own words, and no text from the issue.
- **D3 Who pulls the list.** A command run by a person or agent, committed by pull request. **Decided: "Yes, but it can be populated earlier, e.g. when we're figuring out the strategy for the release. And probably should be."**
- **D4 The words for versions.** **Decided: "It should probably be based on the released."** Read with D10 as one numbering: a version on the strategy page is the version its minor release ships as. Superseded in detail by D10.
- **D5 Releases 12 and 13.** She first decided "Yes, release": finalise their release briefs here. The critique then found facts she did not have: Release 13 has no gate record; Release 12's holds three of the eight payload keys and the rest would mean reading product repositories; a Final record cannot be corrected once Plan 31's rule is on; and Plan 31 expects to validate one legacy record itself. Recommendation then: leave both to Plan 31 (RL-1a), and let the hand-written "Focus now" say they are out. **Decided, with those facts: Plan 31 ("Yes to all 4!").**
- **D6 How the owner's decisions are kept from merging by themselves.** **Decided: as recommended,** which was a check for the phrase `Owner decision needed`. The critique showed that inverts the phrase, which marks a decision still open. Delivered instead in auto-merge, which reads the patch and refuses a change to a `Kind` or `State` line (SR-6). Her intent is unchanged; she may object to the mechanism.
- **D7 Who may apply `release:NN`.** Triage, as a candidate only. **Decided: as recommended.**
- **D8 The words at the top of the page.** The lead drafts; the owner rewrites. **Decided: as recommended.**
- **D9 Order.** **Decided: this plan is done before Plan 31.** It is placed directly above Plan 31 in [priority.md](../priority.md); she may move it.
- **D10 Mark the kind in the release brief.** She asked: "Should we mark that in the release already?" **Decided: yes, as recommended ("Yes to all 4!").** `**Kind:** patch`, `minor` or `major`, optional, absent meaning patch. It records early the declaration Plan 29's decision 7 gives her, and the version each release leads to follows from it, so no second line is needed. Consequence: Releases 12 and 13, as patches before the first minor, appear on 0.1's "on the way" line. The Release skill's "Patch release" is renamed for its lane so the word has one sense.
- **D11 What the strategy page shows.** She asked: "only show greater than minor?" and "Should it include all the plans and issues done in patches before too?" **Decided: the roll-up, as recommended ("Yes to all 4!"):** each version shows its minor release in full; the patches on the way as one line of linked titles; the plans of all of them, each once; and a count of issues for each frozen list. A minor release's own brief lists only its own plans and issues. The alternative, hiding patches from the page entirely, was not chosen.
- **D12 Under what authority an assorted ticket is worked.** The rules say an issue becomes work only through a task row, and an assorted ticket has no plan. **Decided, as recommended ("Yes to all 4!"):** its row in a release brief's issue list counts, worked under that release's run; the label alone still commits nothing.

## Estimate

| Task | Days |
| --- | --- |
| SR-1 | 0.7 |
| SR-2 | 1.5 |
| SR-3 | 0.3 |
| SR-4 | 0.7 |
| SR-5 | 0.15 |
| SR-6 | 0.2 |
| SR-7 | 0.6 |
| Review and its fixes | 0.5 |
| **Total** | **about 4.5 to 5** |

The owner's replies on SR-3 and on the open decisions come on top.

## Source identities

astrid-dev `main` at `a398525a526a2bfe0eb2cccac47732c3491c467d` (15 November 2026) for every reading above; the critique read the draft at `ed0171cfd5b53e1cdb57b08715f68581c6b09282`. No product repository is read or changed. The run starts from astrid-dev `main` at `1e1c646ea428bfd022adc024bbc25bc08078ef93`, the generated-view refresh immediately after the owner's plan reference `91035254b96342ce811afb2711631f300969572d`; the four plan documents are unchanged between them. The new clone was clean at the start. Implementation lands on `int/58-strategy-from-releases`; progress-only pull requests keep `tasks.md` current on `main` under the management skill.

## References

- Ledger: [the strategy page is hand-copied](../../docs/ledger/2026-11-15-strategy-hand-copied-from-briefs.md); [a published release still reads as a draft](../../docs/ledger/2026-11-15-published-release-still-draft.md); [issues never reach a release](../../docs/ledger/2026-11-15-issues-never-reach-a-release.md).
- [Plan 31](../31-releases-from-astrid-dev/plan.md), [Plan 48](../48-one-record-model/plan.md), [Plan 52](../52-issue-intake/plan.md).
- [Contribution design principles](../../docs/contribution-design-principles.md); [Improve](../../skills/astrid-dev-improve/SKILL.md).
