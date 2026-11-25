# Review — Strategy from releases

[Plan](plan.md) · [Inputs](inputs.md) · [Tasks](tasks.md)

## Independent critique of the first draft, 15 November 2026

A fresh agent with no stake in the draft read the pack at commit `ed0171cfd5b53e1cdb57b08715f68581c6b09282` against the code, briefed by the [planning skill](../../agent/shared/workstreams/plan.md) to build as little as possible and to verify claims in code. It ran the repository check (passes), the pull-request check (only the two expected Challenge errors) and the 352 unit tests (pass). Verdict: accept with changes, four of them blocking. Its findings are numbered as it gave them.

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

### Left to the owner, and decided by her on 15 November 2026

| # | Finding | Decision |
| --- | --- | --- |
| 4 | Whether Releases 12 and 13 are finalised here | D5: left to Plan 31 |
| 34 | Under what authority an assorted ticket is worked, since an issue becomes work only through a task row | D12: its row in a release brief's issue list, under that release's run |
| 46 | The planning skill leaves `plans/priority.md` to the owner or orchestrator, and the draft added its own line | Kept, on the owner's words "I'd like to get this all done first" (D9); she may move or remove it |

### Rejected

None.

### After the critique

The owner asked, the same day, whether a release brief should mark its kind (patch, minor or major) and whether the strategy page should show only minor releases and above. That replaced the critique's optional `Toward` line with an optional `Kind` line and gave the page its roll-up for each version. The critic did not see that change; the one final review round covers it.

## Final review, 15 November 2026 — round 1 of 1

A fresh completion reviewer, independent of the implementation workers and manager, reviewed `eb79504c93fa02f619bd17408f7f7a0da658e711..7aae8cc18bf5faa727b8b6da0db68b8da6b80130` (candidate tree `cd43b7f01c99f1dab39010e9504e6da7ae379062`). The brief supplied the accepted plan, D1–D15, exact sources and proof, and questions about the contract and negative cases. It did not supply a manager verdict. Route S used the configured Astra judgment override.

The candidate combined all seven task PRs with `main` at `eb79504c93fa02f619bd17408f7f7a0da658e711`. Before review, normal and base-relative checks and all 220 tests in the accepted inventory passed. The reviewer independently checked source identity, the implementation and test changes, the exact owner-accepted wording, and the live issue snapshot replay.

### Findings and fix verification

| Finding | Evidence and disposition | Fix and verification |
| --- | --- | --- |
| **R1.1 — high, blocking:** a field spelling accepted by the release reader could bypass the owner-decision auto-merge guard | `**Kind :** minor` parsed as `kind=minor` and passed release validation, but its added patch line returned no eligibility refusal. D6 protects the meaning of the field, including accepted whitespace. Accepted and fixed by sharing `records.key_value_lines` normalization in the guard. | [PR 708](https://github.com/banodoco/astrid-dev/pull/708), merge `48d1f2c521f6f869b2ed349d88faae4175fb6556`, tree `9c0d3672c49cc5adab8e6b2f41c5d19ac27a34f3` (identical to local fix `6e8e2ebf013ec2669a38e2ec39f7fc4a0f56169d`). Six files-JSON whitespace subcases failed before the fix and passed afterward. Worker and manager each passed 73 focused tests and both repository checks. The reviewer reread the two-file diff, reproduced the original probe now being refused, and ran two CLI regression tests successfully. **Cleared within this round.** |
| **R1.2 — low:** the plan's current decision summary still said SR-3 awaited the owner | The paragraph stopped at D14 and contradicted D15's acceptance of the draft unchanged. Accepted and corrected; historical waits in the append-only rulings remain explicitly superseded. Private recovery state was refreshed separately and is not acceptance evidence. | [PR 710](https://github.com/banodoco/astrid-dev/pull/710), merge `1c28a173dd8cfb3f471c64b0418758ca104a72b7`, tree `2d34d76ee18b6280910759cdcde42be981f54f8a` (identical to local correction `153b996d6a4c1847d586b37f3e4a31af2eec8a48`). Worker and manager checks passed. The reviewer verified the one-line correction records D15, completes D8, and retains the separate owner go for main. **Cleared within this round.** |

**Final reviewer verdict:** no unresolved findings. Both fixes were verified in the single agreed round; no second round was opened.

### What the reviewer verified

- The release reader, strict plan bullets and optional/default Kind rules; ten version regions, the nine-minor limit and final-major boundary; post-0.9 patches, grouped plan contributions and frozen-only issue counts; and separation of authored and generated text.
- Issue retention, state refresh, pagination, pull-request exclusion, controlled fields, unchanged dates, assembly before writing and refusal to refresh frozen blocks. Replaying the sanitized snapshot of 76 issues and 13 pull requests produced byte-identical Release 14–17 blocks with 0, 35, 2 and 0 rows.
- The removed tests and oracle lines match SR-2's accepted migration; completion-body validation remains. The obsolete-wording search has no matches.
- Approved SR-3 commit `5ba1efd7ff96a5ee829f4b0cdea4c8f71b45da14` differs from the reviewed strategy only in the acceptance-status sentence. The authored proposal is unchanged.
- Documentation gives the hierarchy one home, preserves D5 and D12, and hands the shared reader, frozen issue record and Final-transition approval to Plan 31.

### Final joined proof and limits

After the fixes, the manager joined `main` at `a9dc8fb4197ead24d73b8207dbf1403651900be0` into candidate `64aaf557cf845f74d23c241aa005393926ba8145`, tree `4328d950523b72a6be5f76e8433ade83518a20f0`. That join adds only Plan 55 and Plan 58 progress already on main. The accepted inventory passed **221 tests in 28.879 seconds**, both repository checks passed, and `sync` reported that views were current. The [baseline comparison](evidence/tests/astrid-dev/64aaf557/summary.md) records the run-start baseline, candidate IDs, authorized retired IDs and raw logs.

Remote commit `a9d79f65e359ee021c902dc3a763a0ef4f58a324` has the identical full tree and is retained as the completion-record commit's parent. The tests ran on the local candidate; tree identity connects that proof to the remote source. Subsequent closure edits contain only this report, evidence, the plan's done status and its generated catalog row. That was true when the manager closed the run; the owner's later check added the fixes recorded under "After completion" below.

Hosted full-suite CI is a separate pre-main gate; the local inventory and this review do not substitute for it. The completion PR reports its current result. Direct shell-authenticated GitHub REST was not exercised: live issue data came from the authenticated connector and was replayed through the real CLI entry point with injected read-only transport. The four lists remain unfrozen candidates. Releases 12 and 13 are still finalized by Plan 31. No product code or release publication changed, and integration-to-main still requires the owner's go.

## After completion: the owner's check, 15 November 2026

After the manager marked the plan done, the owner asked the planning session to check the integration branch before it merged. Four reviewers read the integrated work at `a7c2f4861d80fe05f1f7c4d2fcc5de92635966d5`, and one further reviewer then read the whole merge candidate against the plan. Their findings were fixed on `claude/nice-hopper-x1ifrw`, on top of the integration branch joined with `main`, and merged into the integration branch before it went to `main`.

| Finding | Fix |
| --- | --- |
| An open issue with two type labels, or a listed issue closed with no reason, stopped the issue command for every release | `af6c0524`: only issues in the list or matching its labels are validated; a closure with no reason reads as done; a missing token gives a clear message; the release brief is replaced in one step |
| The auto-merge rule failed open on a hidden line break, an empty patch and a renamed release brief | `dfff896f`, and the commit that adds this section: each is refused |
| The glossary gave `version` two meanings; a ledger entry was marked resolved by an entry that said it was not; the release template carried a real plan link and a real issue row | `a726888b` |
| A plan in two releases rendered a full stop before a semicolon; `sync` printed a traceback for a missing marker; four unused names remained | `00457e98` |
| A unit test pinned the wording, kind and plans of Releases 12 to 17, so an ordinary edit to a release brief failed CI | The commit that adds this section: the test checks shape only |
| A frozen issue count would have rendered inside the last plan bullet, and a link in a highlight was not re-based | The commit that adds this section |

**Proof on the final tree:** `python3 scripts/astrid_dev.py check`, the base check against `main`, `sync` (views current) and the whole unit suite, 387 tests, all passing.

**Left as they are, and known:**
- Before the freeze a row removed by hand returns at the next run; the cut is made after the freeze.
- A listed issue that is deleted or transferred stops the command until its row is removed by hand.
- Adding or removing a `## ` heading above a `**Kind:**` or `**State:**` line changes what the reader takes from a release brief without changing that line, and auto-merge does not see it. Plan 31's approval of the Final transition is the proper guard.
- A patch release's highlight and state are not shown on the strategy page, only its title.
- Hand-written lines on the strategy page that the owner may want to revisit: version 0.1 is described as Releases 14 to 17 while the generated part also lists Releases 12 and 13 on the way; the candidates paragraph says none is assigned while Plans 20 and 32 appear under 0.1; and the decision that says the sentence for 1.0 was proposed by the advisor predates the accepted aim.
