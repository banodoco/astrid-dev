# Release 15 — run board

The live state of the Release 15 run, rewritten at each check-in by the release manager. The [brief](../15.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Now (19:50 UTC, Sun 22 Nov)

Two lanes are running, a third has its brief, and a fourth is proposed. [Release 14](../14.md) published on 22 November and is forwarded into `release/15/main` in all three product repositories (astrid-app `e3dbad64`, astrid-agent `8807f820`, astrid-runtime `23310dc8`). How lanes are divided, and how capable each orchestrator must be, is in the [Lead skill](../../skills/roles/astrid-dev-lead/SKILL.md#divide-the-release-into-lanes).

- **Speed of one command (Plan 81) has a measured gain that is not yet landed.** `generate image` went from about 15 s to under 6 s on an installed build; about 42% of the saving is in the Agent and Runtime and about 58% in VibeComfy. Its review failed on correctness, the fixes are in progress on a frozen scope, and the installed re-measurement follows them.
- **The heavy timeline (Plan 77) has its cause and no fix yet.** Opening a 300-clip project takes about five minutes the first time after the Runtime starts, because the Runtime re-reads and re-verifies the timeline's whole history; the same read stopped a 616-clip build at 432 clips and stops a 432-clip backup from being restored and started. The nine earlier Runtime commits are dropped. Round 7, a cheap verified read of the current head and no long hold on the store lock, is approved by the owner and not yet built.
- **Plans 69 and 13 have landed.** Plan 13's Release 15 part is complete; the further extraction is Plan 83, in no release.
- **The release's headline has no lane.** Generation tested for real on three systems rests on issues #678 to #683 and Plan 39; neither has an owner in this release yet.
- **This board was rewritten from the lanes' reports and records.** CI on the three release heads was not re-read for this rewrite.

### Timeline to publish

Not set. The cut line is still the first decision owed: about 150 engineering days of the listed plans have not started.

### Lanes

| Lane | Session and routes | Brief | State |
| --- | --- | --- | --- |
| Timeline: Plan 69, then Plan 77 (a loop plan) | Claude orchestrator `session_011EzfW1FXS3o7GFnNSB7cZS`, hosting a Codex manager | [briefs/plans-69-77.md](briefs/plans-69-77.md) | Plan 69 landed. Plan 77’s exact first cut reopened a persisted local selection in 4.074 and 4.506 s and confirmed one legal save in 34.254 s. The first previously unset workspace selection for the actor in the realm still cost a 17.146 s reopen. Stock and candidate both refused the default direct restart. The owner chose to land with that limit stated ([#1521](https://github.com/banodoco/astrid-dev/issues/1521)). The local compatibility repeat passed. The first-cut Runtime source `b89cd48b` includes landed Plan 81 and matches the rehearsal tree and test results. Agent and App predecessor landings and the hosted gate remain pending. A separate local Runtime startup foundation passed the independent review and paired protected checks. The 300-clip development probe crossed 135 s on native startup. The managed proof of that threshold is still open. [Installed requalification](../../plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/first-cut-installed-requalification/RESULT.md) |
| Commands: Plan 81, with Plan 13 | Claude orchestrator `session_011EzfW2Ut856AFGZS8ZamHU`, hosting Codex managers on route X | [Plan 81 handover](../../plans/81-once-per-command/handover.md) | Plan 13 landed. Plan 81: gain measured, review failed, fixes in progress on a frozen scope; then one installed re-measurement and the reviewer's check |
| Vision page: Plan 84 (a taste plan) | Claude orchestrator `session_011EzfW1Df4SCkBoafGdR1di`, which hosted a Codex manager on route T | start message from the owner, 22 November | Paused: the owner stopped the first run on 22 November after PL-0 and PL-1. PL-1 is on `release/15/plan-84` (astrid-app #371); PL-2 is nearly done on its own branch; an entry repair is open as astrid-app #372. A second run waits on her go ([plan](../../plans/84-living-planet-on-the-vision-page/plan.md)) |
| Small Agent plans: Plan 78 and Plan 40, side by side | Claude orchestrator `session_011EzfVz6RTgoXjxNDgJP47L` on route X, hosting two Codex managers, Plan 78 on X and Plan 40 on S | start message from the owner, 22 November | Running since 22 November. Plan 40: local proofs done; it waits on Plan 81 landing, then a merge and one hosted run. Plan 78: its independent review found nine findings, seven blocking; fixes in progress, then a second round; its live proof runs last, on the candidate that includes Plan 77's first cut |
| Build machine for Plan 77's large project | the Release 15 Lead's own session, with a Codex manager per run | — | Holds the only project past 300 clips (432 clips) and its signed backup. It runs commands for the timeline lane on request and is lost if the session's machine is reclaimed |
| Easy wins (issue packet) | Release 15 Lead, with Codex workers | — | Nine fixes in [astrid-agent #475](https://github.com/banodoco/astrid-agent/pull/475) (draft). Waiting on the owner's go to land |
| Plan 79 (local media of any size) | not started | — | Queued; starts after Plan 77 lands |
| Plans 63, 76, 18 (the saving plans) | not started | — | Held: Plan 77's evidence rewrites them, and its finding is in the commit history they build on |
| Plans 39, 50 and the cross-platform tests (#678 to #683) | not started | — | The release's named theme. Plan 50 waits on its scope decision (D1); Plan 39 competes with Plan 81 for CI runners until that lands |
| Plans 52, 53 | waiting on the owner | — | Plan 52: her issue transfers and approval of the reporting rules. Plan 53: her mark-up |
| Plan 72 (project delivery) | its own manager, not yet accepted by the Lead | — | Hold, until the owner decides its scope |

### Forwards from Release 14

Release 14 is published. Its last state is in `release/15/main` in all three repositories: astrid-runtime by #86 and #100, astrid-agent by #482 and #523, astrid-app by #369. Nothing is waiting.

### Waiting on the owner

- **The cut line and the headline.** The release is named for every platform and rented machines; what is running is speed and editing. The Lead recommends naming it for what will ship and moving Plans 63, 76, 18 and 39 to the next release.
- **Starting the two new lanes:** Plan 84, and Plans 78 with 40.
- **Plan 84's D1:** her statement that the mock-up is hers to publish, before it lands.
- **Plan 81:** whether its new short check of the speed guard becomes a required check, when its orchestrator brings the measured duration.
- **The go to land** [astrid-agent #475](https://github.com/banodoco/astrid-agent/pull/475) in `release/15/main`.
- **Plan 50's scope decision (D1),** before it can join a lane.
- **Releases for Plans 82, 85 and 86,** which are in none.
- **The VibeComfy `root-clean` gate** ([astrid-dev #1311](https://github.com/banodoco/astrid-dev/issues/1311)): add three entries to its allow list (recommended) or move the files.
- **Branch protection on `release/15/main`** in each product repository.
- **Plan 72's scope decision,** then its go or hold.

## Standing rulings

- Fixes flow forward: `release/14/main` is merged into `release/15/main`, never the reverse, and never by rebase or force-push.
- A forward that conflicts on the save path waits for the Release 14 Lead's own combination rather than resolving it twice.
- The owner approved Codex with full access in the Lead's session on 21 November 2026, and asked for Codex Luna workers wherever the work allows. The Lead reads every diff and re-runs every proof before pushing.
- A fix that would change an existing test's assertion goes to the owner first, by name.
- **Lanes land their own plans.** On 22 November 2026 the owner told the Lead: "they do the merges themselves, but you're making sure that they're doing everything in the right way", and told each lane in its own session: "You may merge your plan into release/15/main yourself, pins included, once the Release 15 Lead confirms its landing gate is met. ... Publishing a release still needs my own go." The Lead confirms a gate in writing to the lane; product decisions inside a gate, such as accepting what a change no longer checks, stay the owner's.
- **The landing gate,** the same for every lane, met on one frozen set of commits: `release/15/main` merged into the plan branch before the final proof; the review passed, by a reviewer that did none of the work; one hosted CI run per repository, with the Agent's compared test by test against [the baseline](evidence/agent-ci-baseline-8807f820/README.md) and no new failures; the plan's headline measurement re-taken on those commits; pins produced by the generators, with their witness tests and the pin check; `tasks.md` true and the record pull request merged, quoting every owner decision the landing relies on; the landing pull requests open, one per repository, naming their order.
- **Landing order:** Plan 81, then Plan 40, then Plan 77's first cut, then Plan 78. One Agent CI run at a time across the release; a lane tells the Lead before it dispatches.
- **Pins and the hosted run (Lead, 23 November 2026, the owner having delegated direction to the Lead overnight).** A repository's final pins can only name its upstream's merge commit after that upstream has landed, so the order is: the Runtime's pull request lands; the Agent's pull request then carries its source plus one generator-only pin commit; then the App's. The lane's one full hosted run for a repository is dispatched on the head that lands, pin commit included; opening a landing pull request runs only a cheap subset, so the full Agent run is a manual dispatch of `ci.yml` and `lanes.yml` on the Lead's written slot. The Runtime pin lives in exactly four Agent files (`runtime.lock.json`, `astrid/resources/runtime.lock.json`, and the literals at `tests/test_vendor_lock.py:76` and `tests/test_windows_path_budget.py:23`); all four move in the pin commit, to the value the generator wrote, and nothing else in either test file changes, as every earlier repin did (`ffe659dd5`). Plan 81 is the one exception to "the head that lands is the head that ran": its full run was already under way on the pre-pin source, so that run stands and the next full Agent run on the release branch (Plan 40's) is the backstop for its pin.
- **The App's pins and its `release` number (Lead, 23 November 2026; this replaces a ruling of the same morning that allowed only one App pin, made at the freeze, which rested on running the guard against the release branch).** The App's release guard (`scripts/installer/release-guard.mjs`) is run by `test.yml` only for pull requests into `main` and pushes to `main`; the workflow says the install tuple may change more than once inside a release branch, and "+1 exactly" is checked against what is published. So a lane pins the App after its Agent has landed, as the pin sequence above says. The first pin on `release/15/main` raises `release` from 14 to 15 and every later pin leaves it at 15. The check to run and quote is the guard against the published `main`, which must accept 15; pointed at the release branch it asks for 16, and that message does not apply. `required`, the forced-update floor, is a publication decision and stays the owner's. Plan 78's `packs` entry for the motion pack lands with that plan's App patch.
- **A test that fails only on a busy runner** is recorded in [the baseline](evidence/agent-ci-baseline-8807f820/README.md) with its symptom once it has been reproduced on the unchanged base, and then does not hold a landing.
