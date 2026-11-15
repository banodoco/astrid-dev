# Review — Strategy from releases

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md)

## Independent critique of the first draft, 15 November 2026

A fresh agent with no stake in the draft read the pack at commit `ed0171cfd5b53e1cdb57b08715f68581c6b09282` against the code, briefed by the [planning skill](../../skills/astrid-dev-plan/SKILL.md) to build as little as possible and to verify claims in code. It ran the repository check (passes), the pull-request check (only the two expected Challenge errors) and the 352 unit tests (pass). Verdict: accept with changes, four of them blocking. Its findings are numbered as it gave them.

### Blocking, all accepted

| # | Finding | What changed |
| --- | --- | --- |
| 1 | The view, the new checks and the rewritten page could not each pass alone: a registered view without its markers breaks `sync` on every pull request, and two tests copy the real tree | One task, SR-2, makes all three changes; the plan lands on an integration branch and reaches `main` in one merge |
| 2 | One view owns one region, and the card left the design open | Nine static views built in a loop, a marker pair under every version heading, and no change to the view machinery; an empty version says "No release yet." |
| 3 | The issue list's membership and freeze did not work: a closed issue dropped out, a re-query by label would claim every issue ever closed, "closed as completed" is wrong in four ways, and 23 of 76 open issues have no type | Rows stay once added and only their state is refreshed; states use the guide's own words; the freeze stamps states and the release manager edits the list in the finalising pull request; an untyped row is allowed |
| 4 | Finalising Releases 12 and 13 could not run from its card: Release 13 has no gate record, Release 12's has three of the eight payload keys, the rest would mean reading product repositories, and Plan 31 expects one legacy record it validates itself | Removed from the task list. D5 is reopened for the owner with the recommendation changed to Plan 31; the conditions for keeping it here are written in tasks.md |

### Accepted

| # | Finding | What changed |
| --- | --- | --- |
| 5 | No Plan 31 task backfills Releases 9 to 11 or the release log | The plan says no plan covers these |
| 6, 7, 15 | The owner's phrase in a pull request body is a weak and inverted guard, and proves only that auto-merge is off | D6 is delivered in `auto_merge.py`, which reads each file's patch (SR-6); the plan claims only "not merged automatically"; Plan 31's code-owner approval replaces it for `State` |
| 8 | The completion form's `Strategy:` line is required by a test | SR-7 rewords the line and keeps its label |
| 9, 26 | Every pull request also runs `sync`; after a release brief changes, `main` is stale for one CI run and nothing on `main` reports it | Stated under Limits; the rules that would otherwise fail as a traceback are in the always-on check |
| 10, 21 | `strategy/1.0.md` and a strategy template one folder down cannot keep working relative links | The archived page is `strategy-1.0.md` at the root; the strategy template is dropped and the live page is the model |
| 11 | "Line numbers below" with none in the cards | The sentence now covers the line numbers the cards do carry |
| 12, 13 | The refresh App is live and the REST route works from a cloud session; the open count rose from 60 to 76 during the day | inputs.md updated |
| 14 | The catalog `Release` column has no owner requirement and changes a pinned view | Dropped |
| 16, 17 | A separate reader task and a separate freeze task are not warranted | Merged into SR-1 and SR-4 |
| 18 | The version line should be optional, so old release briefs and four fixtures stay untouched | `Kind` is optional and absent means patch; only Release 17 gains the line |
| 19 | With the strategy comparison gone, an unlinked plan line would be dropped silently | Included plans is `None yet` or every bullet is a linked plan with its sentence |
| 20 | "A final release brief ships something" has no recorded failure | Dropped |
| 22 | An issue count on the strategy page rewrites it at every pull | A count is shown only for a frozen list, which does not change |
| 23, 24, 31, 32 | Five issues carry two plan labels; a network command does not belong in the check runner; no block line may start with `## `; the date fights idempotence | A flat list with a `Via` cell; a standalone script; both rules in the SR-4 card |
| 25 | The check must never read generated lines | `strategy_errors` removes marked parts before reading |
| 27 | "A plan in one version" would fail Plans 29 and 40 | The rule is dropped |
| 30 | Renumbering a release needs the labels renamed in descending order, and a manager's session may not be able to write labels | Written into SR-7's text for the Release skill |
| 33 | No task committed a first block into Releases 14 to 17 | Added to SR-4 |
| 35 to 38 | The contract cards missed tests, fixture files and exact `golden.txt` lines; SR-12 had no card and its `grep` could not pass | The SR-2 and SR-7 cards carry the critique's lists; the proof is a per-sentence list |
| 39, 40 | What Plan 31's RL-1a should say afterwards, and its code-owner rule | In SR-7's card, and in a note on Plan 31 |
| 41 | Plan 52's II-13 has the same Issues section in scope | SR-5 agrees the order with that plan's manager |
| 42 to 45 | Dependencies, the critical path, a landing rule, the test inventory, the ambiguity pass, routes for the prose and the documentation, a link to a heading that does not exist, a proof with no command | tasks.md rewritten; headings on the strategy page keep their names so every anchor still resolves |
| 46 | No `fix` ledger entries; "brief" used for "release brief"; `Waiting on` hid an open decision; the Scope decision cited a line this draft added | SR-7 writes the entries; the pack says "release brief"; `Waiting on` names the open decisions; the Scope decision links the session |
| 47, 48 | 4.5 days was too low for the drafted scope; one final round suits the reduced scope | A per-task estimate is in inputs.md; with the cuts it is about 4.5 |

### Left to the owner

| # | Finding | Decision |
| --- | --- | --- |
| 4 | Whether Releases 12 and 13 are finalised here | D5, reopened |
| 34 | Under what authority an assorted ticket is worked, since an issue becomes work only through a task row | D12 |
| 46 | The planning skill leaves `plans/priority.md` to the owner or orchestrator, and the draft added its own line | Kept, on the owner's words "I'd like to get this all done first" (D9); she may move or remove it |

### Rejected

None.

### After the critique

The owner asked, the same day, whether a release brief should mark its kind (patch, minor or major) and whether the strategy page should show only minor releases and above. That replaced the critique's optional `Toward` line with an optional `Kind` line and gave the page its roll-up for each version. The critic did not see that change; the one final review round covers it.
