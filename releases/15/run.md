# Release 15 — run board

The live state of the Release 15 run, rewritten at each check-in by the release manager. The [brief](../15.md) holds intent, included plans, branches and issues; each plan's `tasks.md` holds its progress.

## Now (19:50 UTC, Sun 22 Nov)

Two lanes are running, a third has its brief, and a fourth is proposed. [Release 14](../14.md) published on 22 November and is forwarded into `release/15/main` in all three product repositories (astrid-app `e3dbad64`, astrid-agent `8807f820`, astrid-runtime `23310dc8`). How lanes are divided, and how capable each orchestrator must be, is in the [Lead skill](../../skills/roles/astrid-dev-lead/SKILL.md#divide-the-release-into-lanes).

- **Speed of one command (Plan 81) has a measured gain that is not yet landed.** `generate image` went from about 15 s to under 6 s on an installed build; about 42% of the saving is in the Agent and Runtime and about 58% in VibeComfy. Its review failed on correctness, the fixes are in progress on a frozen scope, and the installed re-measurement follows them.
- **The heavy timeline (Plan 77) has its cause and no fix yet.** Opening a 300-clip project takes about five minutes the first time after the Runtime starts, because the Runtime re-reads and re-verifies the timeline's whole history; the same read stopped a 616-clip build at 432 clips and stops a 432-clip backup from being restored and started. The nine earlier Runtime commits are dropped. Round 7, a cheap verified read of the current head and no long hold on the store lock, is approved by the owner and not yet built.
- **Plans 69 and 13 have landed.** Plan 13's Release 15 part is complete; the further extraction is Plan 83, in no release.
- **The release's headline has no lane.** Generation tested for real on three systems rests on issues #678 to #683 and Plan 39; neither has an owner in this release yet.
- **This board was rewritten from the lanes' reports and records.** CI on the three release heads was not re-read for this rewrite.

### Boards

The Lead board is `board: release 15 lead`; each plan's is `board: release 15 plan <P>` ([rules](../../skills/shared/run-contract.md#coordination-boards-and-check-ins)); [list them](https://github.com/banodoco/astrid-dev/issues?q=is%3Aissue+is%3Aopen+in%3Atitle+%22board%3A+release+15%22).

### Timeline to publish

Not set. The cut line is still the first decision owed: about 150 engineering days of the listed plans have not started.

### Lanes

| Lane | Session and routes | Brief | State |
| --- | --- | --- | --- |
| Timeline: Plan 69, then Plan 77 (a loop plan) | Claude orchestrator `session_011EzfW1FXS3o7GFnNSB7cZS`, hosting a Codex manager | [briefs/plans-69-77.md](briefs/plans-69-77.md) | Plan 69 landed. Plan 77’s exact first cut reopened a persisted local selection in 4.074 and 4.506 s and confirmed one legal save in 34.254 s. The first previously unset workspace selection for the actor in the realm still cost a 17.146 s reopen. Stock and candidate both refused the default direct restart. The owner chose to land with that limit stated ([#1521](https://github.com/banodoco/astrid-dev/issues/1521)). The local compatibility repeat passed. The first-cut Runtime PR includes landed Plan 81 and a reviewed fix for the duplicate diagnostic emitter. The unchanged macOS watchdog failed one isolated diagnostic iteration on the exact Runtime base. The Lead recorded inherited fragility in [#1621](https://github.com/banodoco/astrid-dev/issues/1621) and landed Runtime at `737843e9`. The Agent topic contains landed Plan 40 and pins that Runtime. The Lead cleared the exact hosted gate and [Agent PR #555](https://github.com/banodoco/astrid-agent/pull/555) landed at `b324d7c1`. The App has regenerated both release 15 pins and is qualifying two local source repairs for the standing local suite before the hosted App gate. [Runtime PR](https://github.com/banodoco/astrid-runtime/pull/102) The separate startup slice is parked in unmerged branches. Its local synthetic probe crossed 135 s pending on both routes. A later two-save profile on 300 clips confirmed 57.498 and 19.712 s to Saved. The fresh save run uses those profiles. [Parked source and verdicts](../../plans/77-saving-holds-on-a-heavy-timeline/tasks.md#first-cut-gate-and-parked-work-23-november-2026) [Save profile](https://github.com/banodoco/astrid-dev/pull/1638) [Grown startup proof](../../plans/77-saving-holds-on-a-heavy-timeline/rounds.md#grown-300-clip-startup-development) [Installed requalification](../../plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/first-cut-installed-requalification/RESULT.md) |
| Commands: Plan 81, with Plan 13 | Claude orchestrator `session_011EzfW2Ut856AFGZS8ZamHU`, hosting Codex managers on route X | [Plan 81 handover](../../plans/81-once-per-command/handover.md) | Plan 13 landed. Plan 81: gain measured, review failed, fixes in progress on a frozen scope; then one installed re-measurement and the reviewer's check |
| Vision page: Plan 84 | Unassigned for fresh project run | Owner's 24 November direction | Queued: time-linked 3D world with eight individually directed scenes, four flying concepts and two cinematic transitions; first vignette style lock and complete-world taste gates. [Plan](../../plans/84-living-planet-on-the-vision-page/plan.md); fresh owner go required. |
| Small Agent plans: Plan 78 and Plan 40, side by side | Claude orchestrator `session_011EzfVz6RTgoXjxNDgJP47L` on route X, hosting two Codex managers, Plan 78 on X and Plan 40 on S | start message from the owner, 22 November | Running since 22 November. Plan 40: local proofs done; it waits on Plan 81 landing, then a merge and one hosted run. Plan 78: its independent review found nine findings, seven blocking; fixes in progress, then a second round; its live proof runs last, on the candidate that includes Plan 77's first cut |
| Build machine for Plan 77's large project | the Release 15 Lead's own session, with a Codex manager per run | — | Holds the only project past 300 clips (432 clips) and its signed backup. It runs commands for the timeline lane on request and is lost if the session's machine is reclaimed |
| Easy wins (issue packet) | Release 15 Lead, with Codex workers | — | Nine fixes in [astrid-agent #475](https://github.com/banodoco/astrid-agent/pull/475) (draft). Waiting on the owner's go to land |
| Workflow set-up: Plan 56 (any workflow runs or stops with a named next step) | Packet dispatch: the Release 15 Lead is accountable; Orchestrator `session_011EzfW2WBWyoHTBJggpfEDm` starts one fresh ChatGPT session per packet, in the mode its Route sets | [Dispatch queue](#dispatch-queue-plan-56) | Set up 23 November; waiting on the owner to paste the Orchestrator launch message and on the Lead's startup-check DECISION |
| Plan 79 (local media of any size) | not started | — | Queued; starts after Plan 77 lands |
| Plans 63, 76, 18 (the saving plans) | not started | — | Held: Plan 77's evidence rewrites them, and its finding is in the commit history they build on |
| Plans 39, 50 and the cross-platform tests (#678 to #683) | not started | — | The release's named theme. Plan 50 waits on its scope decision (D1); Plan 39 competes with Plan 81 for CI runners until that lands |
| Plans 52, 53 | waiting on the owner | — | Plan 52: her issue transfers and approval of the reporting rules. Plan 53: her mark-up |
| Plan 72 (project delivery) | its own manager, not yet accepted by the Lead | — | Hold, until the owner decides its scope |

### Forwards from Release 14

Release 14 is published. Its last state is in `release/15/main` in all three repositories: astrid-runtime by #86 and #100, astrid-agent by #482 and #523, astrid-app by #369. Nothing is waiting.

### Owner decisions, 24 November 2026

The owner accepted all of the Release 15 Lead's recommendations, in the Lead's session (`session_011EzfW1gtAhRQwk8pgJMzhG`):

- **Cut and freeze:** freeze in about two days, about 26 November, once Plan 87's core lands in `release/15/main`. What isn't on `release/15/main` by then ships in Release 16. Publishing still needs her own go.
- **Plan 87's RN-15** (long renders lose their outputs when a process id is reused) is a **release blocker**.
- **Plan 87's RN-14** (the motion pack on a fresh install, D2) moves to Release 16.
- **Plan 82: go**, with its D2 (trust a shipped install) decided yes; it runs as a packet dispatch ([Plan 82 dispatch](#plan-82-dispatch)). **Plan 92: go** for Release 16, after Plan 82.
- **VibeComfy `release/15/main`** may be fast-forwarded to `c0e910ca` (Plan 56's head; the current tip is its ancestor).
- **Plans 13, 79 and 72** move to [Release 16](../16.md); none had started in Release 15.
- **The Release 7 branches** may be tagged and deleted.

### Waiting on the owner

- **The cut line and the headline.** The release is named for every platform and rented machines; what is running is speed and editing. The Lead recommends naming it for what will ship and moving Plans 63, 76, 18 and 39 to the next release.
- **Plan 56: a standby Lead.** A Lead whose session stops is not covered for Release 15 yet; name a standby Lead session (the other model family) under `releases/15/lead/` ([how](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#standby-lead)), or accept that the owner restarts the Lead by hand.
- **Starting the two new lanes:** Plan 84, and Plans 78 with 40.
- **Plan 84:** appoint a delivery owner and confirm the release window and site sky-session interface before work; live 3D with clock-coupled horizontal rotation is the selected medium. Make no product integration without a fresh go.
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
- **Release-wide rulings** (Lead's DECISION, [#1836](https://github.com/banodoco/astrid-dev/issues/1836), 24 November 2026): the freeze is about 26 November, once Plan 87's core lands. Gates compare whole runs by id from full job logs, never shard against shard. Never edit a pinned schema in place; prefer an additive field to changing an existing assertion. Answer each READY-PROOF within 45 minutes, running proofs in parallel. A staged landing is allowed when the slice is reviewed, coherent alone and fully gated.
- **CI:** At most two plan gate pairs (`ci.yml` + `lanes.yml`) at once across Releases 15 and 16, plus the `release/*/main` push runs; a third waits until both running pairs' jobs have started; the running runs are the slot table; landing gates first; never cancel a release/*/main run; name your run ids in your STATUS (Lead, 24 November 2026: GitHub-hosted runners, no shared resource; [#1836](https://github.com/banodoco/astrid-dev/issues/1836) r15-lead-0006).
- **Lanes land their own plans.** On 22 November 2026 the owner told the Lead: "they do the merges themselves, but you're making sure that they're doing everything in the right way", and told each lane in its own session: "You may merge your plan into release/15/main yourself, pins included, once the Release 15 Lead confirms its landing gate is met. ... Publishing a release still needs my own go." The Lead confirms a gate in writing to the lane; product decisions inside a gate, such as accepting what a change no longer checks, stay the owner's.
- **The landing gate,** the same for every lane, met on one frozen set of commits: `release/15/main` merged into the plan branch before the final proof; the review passed, by a reviewer that did none of the work; focused proofs of every touched area on the landing head, compared by id with the base (since 24 November 2026, with the owner's go: no plan-branch full run; the `release/15/main` push run after the merge is the full check, compared test by test against [the baseline](evidence/agent-ci-baseline-8807f820/README.md) by the Lead; a new failure is fixed forward within 2 hours or reverted; an integrity-critical change may still ask for a plan-branch full run first; [#1836](https://github.com/banodoco/astrid-dev/issues/1836) r15-lead-0008); the plan's headline measurement re-taken on those commits; pins produced by the generators, with their witness tests and the pin check; `tasks.md` true and the record pull request merged, quoting every owner decision the landing relies on; the landing pull requests open, one per repository, naming their order.
- **Landing order:** Plan 81, then Plan 40, then Plan 77's first cut, then Plan 78. A lane tells the Lead before it dispatches.
- **Pins and the hosted run (Lead, 23 November 2026, the owner having delegated direction to the Lead overnight).** A repository's final pins can only name its upstream's merge commit after that upstream has landed, so the order is: the Runtime's pull request lands; the Agent's pull request then carries its source plus one generator-only pin commit; then the App's. The lane's one full hosted run for a repository is dispatched on the head that lands, pin commit included; opening a landing pull request runs only a cheap subset, so the full Agent run is a manual dispatch of `ci.yml` and `lanes.yml` on the Lead's written slot. The Runtime pin lives in exactly four Agent files (`runtime.lock.json`, `astrid/resources/runtime.lock.json`, and the literals at `tests/test_vendor_lock.py:76` and `tests/test_windows_path_budget.py:23`); all four move in the pin commit, to the value the generator wrote, and nothing else in either test file changes, as every earlier repin did (`ffe659dd5`). Plan 81 is the one exception to "the head that lands is the head that ran": its full run was already under way on the pre-pin source, so that run stands and the next full Agent run on the release branch (Plan 40's) is the backstop for its pin.
- **The App's pins and its `release` number (Lead, 23 November 2026; this replaces a ruling of the same morning that allowed only one App pin, made at the freeze, which rested on running the guard against the release branch).** The App's release guard (`scripts/installer/release-guard.mjs`) is run by `test.yml` only for pull requests into `main` and pushes to `main`; the workflow says the install tuple may change more than once inside a release branch, and "+1 exactly" is checked against what is published. So a lane pins the App after its Agent has landed, as the pin sequence above says. The first pin on `release/15/main` raises `release` from 14 to 15 and every later pin leaves it at 15. The check to run and quote is the guard against the published `main`, which must accept 15; pointed at the release branch it asks for 16, and that message does not apply. `required`, the forced-update floor, is a publication decision and stays the owner's. Plan 78's `packs` entry for the motion pack lands with that plan's App patch.
- **Fixes are ChatGPT packet work** (owner, 24 November 2026; [#1836](https://github.com/banodoco/astrid-dev/issues/1836) r15-lead-0015). Claude orchestrators and their subagents diagnose, review, prove, merge, pin and run CI. They never write the fix. When ChatGPT fails, retry the session, start a fresh one, or wait. A manager is never stood down while its plan may still need packets.
- **Ship as soon as it is safe** (owner, 25 November 2026; r15-lead-0016). Only harm-class findings block shipping: lost or corrupted work; a broken install, update or rollback; wrong output on a real path; a project that can't open or save; or a broken Release 15 promise. Anything else becomes an astrid-dev issue marked as a Release 15 known issue.
- **Freeze** (Lead, 25 November 2026, about 02:45 UTC; r15-lead-0017). Plan 87's core landed (Runtime `686ca695`, Agent `89768ef9`, App `2e57fd92`), and Release 15 is frozen.
  - Only these may still land: Plan 89's App half (astrid-app #400); Plan 56's stage 1, if its gate passes by 25 November 18:00 UTC; P87-07, if gated before the candidate is named; and fixes for harm-class findings.
  - Everything else is Release 16.
  - The candidate's SHAs are named on #1836 once those items land or drop out.
- **A test that fails only on a busy runner** is recorded in [the baseline](evidence/agent-ci-baseline-8807f820/README.md) with its symptom once it has been reproduced on the unchanged base, and then does not hold a landing.

## Plan 56 dispatch

Added 23 November 2026 at the owner's request. The Lead rewrites this section at each check-in. Packets are in [packets/](packets/); the plan's `tasks.md` stays the record of progress.

### Authority

On 23 November 2026 the owner, in an orchestrating session (`session_011EzfW4BJ221kXBNRB4xQcG`), asked for Plan 56 to be set up for the [fresh ChatGPT packet workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md).

- **Accountable agent** for Plan 56: `session_011EzfW2ePdUMAHRAcAm3nur`, acting for the Release 15 Lead (`session_011EzfW1gtAhRQwk8pgJMzhG`); there is no separate plan manager. It writes and orders packets, reviews packet PRs, merges accepted ones into `release/15/plan-56`, merges `release/15/main` into it, keeps `tasks.md` current, runs the review stops (RS1 after WS-7b and LE-2b, and R, up to two rounds) with Codex Astra, and may move the Agent's VibeComfy pin on `release/15/plan-56` with `scripts/vibecomfy_pin.py`. It confirms the landing gate before anything goes into `release/15/main`, and gives hosted CI slots.
- **Sessions in use (23 November 2026):** the Release 15 Lead is `session_011EzfW1gtAhRQwk8pgJMzhG`. Plan 56's accountable agent, delegated by the owner, is `session_011EzfW2ePdUMAHRAcAm3nur`. On mailbox #1757 only, it posts under the name `r15-lead`, and the Orchestrator addresses it so. The Orchestrator is the Codex session `01a20a4e-a34d-7a51-ab59-536b6cfa6869`, posting as `r15-orchestrator-1`. On the owner's override, the Orchestrator dispatched P56-01 at 21:44 UTC, before this board reached `main`.
- **The Orchestrator** acts in the owner's ChatGPT account at her request, so its start messages are hers. It may start, resume, stop and replace packet sessions and comment on the mailbox; it does not edit the repository.
- **A packet session may:** push to the branches its packet's PR destination names, open pull requests to that destination, and comment on the mailbox. It never merges, never edits `tasks.md`, never rebases a shared branch, never dispatches hosted CI and never takes a second packet.
- **Bases:** astrid-agent `release/15/plan-56` from `release/15/main` (`045064b6`); VibeComfy `release/15/plan-56` from `c0e910ca`, the commit the Agent pins, which contains VibeComfy `release/15/main` (`48b5fa9e`), so both branches carry the current `release/15/main`. When `release/15/main` moves, the Lead merges it into `release/15/plan-56`; a packet never does.
- **Heads (24 November 2026):** astrid-agent `release/15/plan-56` = `7fa92be1` (after #621); astrid-agent `p56/landing-s1` = `46f5b945` (or later); VibeComfy `release/15/plan-56` = `42819e14`; VibeComfy `p56/landing-s1` = `033473ff`.
- **Needs the owner:** the live SAM run (WS-L, after R), publishing, and anything paid or touching her machine, install or media. On 24 November 2026 she delegated every other Plan 56 blocker, owner decisions included, to Plan 56's accountable agent, which records each one on the mailbox.

### Standing rulings (Plan 56)

1. **Different functions in one file are not a conflict** between packets; the same function or the same new test table is. The holder is the task branch, not the packet: a function is free for the next packet once the last task that writes it has merged. (Proposed by the owner and confirmed by the Lead, 23 November 2026.)
2. **Cross-repo packets never move a pin:** they post `READY-PIN <VibeComfy head>` and the Lead adds the pin commit.
3. **RS1 and R are commissioned by the Lead,** each by Codex Astra.
4. **The Plan 56 bases include `release/15/main` of both repositories** (the owner, 23 November 2026, through the Orchestrator); the Lead records each base's head and ancestry in `releases/15.md` Branches.
5. **A packet's dependants wait only for the cards they depend on,** not for the whole packet (Lead, 23 November 2026).
6. **Proof runs where the network is.** Packet sessions end with `READY-PROOF` ([workstream](../../skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md)). The Lead runs the Agent proofs, the VibeComfy fast suite by id, and the requalification of integrated heads; the Orchestrator may run VibeComfy focused proofs on the owner's computer (Lead, 23 November 2026).
7. **Hosted CI.** VibeComfy's `ci` runs no unit tests (astrid-dev #1768), so the Lead's local fast suite, compared by id, replaces it (baseline at `c0e910ca`: 758 passed, 9 failed, 9 skipped). Agent `ci.yml` does not trigger on `release/*/plan-*`; the Lead dispatches it on `release/15/plan-56` after each batch and compares it by id with `agent-ci-baseline-8807f820` (Lead, 23 November 2026).
8. **Batch integration.** The Lead merges accepted VibeComfy PRs with `--no-ff`, tests the integrated tree, pushes that exact tree, and adds one cumulative Agent pin per batch (Lead, 23 November 2026).
9. **Code-quality audit before every packet merge:** duplication across repos, silent fallbacks, broad `except`, hard-coded cases, test-only seams, dead or duplicate paths. A silent fallback, or a second code path left as an end state, is must-fix (mailbox a0bb99b6; follow-ups in astrid-dev #1772).
10. Agent CI capacity: see the CI rule in [Standing rulings](#standing-rulings).
11. **Owner decisions are delegated (24 November 2026)** to Plan 56's accountable agent, except the reserved items under Authority. An assertion change that implements an accepted plan outcome is decided by that agent and recorded with its reason (mailbox 9c75f07b).
12. **Stage 1 lands from snapshots.** P56-01 to -05 and -07 land into `release/15/main` from `p56/landing-s1` in each repo (VibeComfy `033473ff` as a fast-forward; Agent `3956bc41` + merge of `release/15/main` + pin), never from the moving plan-56 tip. Only the `release/15/main` merge, the pin, the coherence fixes and the RS1 fix packets go on the snapshot, each covered by a focused fresh RS1. The gate request carries the three-dot diff comparison command and output. Release Lead decision of 24 Nov; RS1 fresh pass due by 25 Nov 18:00 UTC or Plan 56 goes to Release 16 whole.
13. **Release-wide rulings live on astrid-dev #1836** (read to the last page hourly). Release ruling 11: never cancel a `release/*/main` CI run. Hourly reports go as a STATUS on #1757 `to: r15-release-lead`.

### Mailbox

[astrid-dev #1757](https://github.com/banodoco/astrid-dev/issues/1757), run `r15-dispatch`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Plan 56 accountable agent (`r15-lead`) | `r15-lead` | `session_011EzfW2ePdUMAHRAcAm3nur` | 7130458784 |
| Orchestrator | `r15-orchestrator-1` | `01a20a4e-a34d-7a51-ab59-536b6cfa6869` (Codex) | 7114811678 |
| Packet session | `r15-<packet>-<n>`, for example `r15-P56-01-1` | from the Orchestrator's STATUS | — |

Cadence and time limits: [multi-manager dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md) and the [liveness rule](../../skills/shared/run-contract.md#coordination-boards-and-check-ins).

### When a session goes quiet

A branch, not a chat, shows health ([liveness](../../skills/shared/run-contract.md#coordination-boards-and-check-ins)). Work that has not moved is blocked by the work or the environment: fix an environment cause where it lives, or bring the owner the exact step, and never dispatch into the same wall again.

- **A packet session:** resumed and replaced as in the [dispatch workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md); the replacement is `r15-<packet>-<n+1>`.
- **The Orchestrator** quiet: the Lead checks its scheduled task and nudges it; at 3 hours the owner is told and starts a fresh one from the board.
- **The Lead** quiet: the Orchestrator keeps its running packets going, starts nothing needing a ruling and tells the owner; at 6 hours the owner hands the role to a standby Lead (none named: see Waiting on the owner), under the same mailbox name `r15-lead`, after ruling out a quiet Lead.
- **A Review** unanswered for 4 hours: the Orchestrator sends the Lead a REQUEST and tells the owner.

### Orchestrator startup checks

The Orchestrator does these first, posts one STATUS with each as passed or failed, and dispatches nothing until the Lead's DECISION answers it. A failure is a manual step for the owner, written here.

1. **Mailbox both ways:** read #1757, post one non-sensitive ACK, see the Lead's reply.
2. **Branches:** confirm `release/15/plan-56` exists in astrid-agent and VibeComfy at the bases recorded in `releases/15.md` Branches, and that no `p56/*` branch exists yet.
3. **A fresh ChatGPT session** in the mode the first packet's Route sets, with nothing from an earlier chat.
4. **Resume:** reopen that session later and continue it.
5. **The hour:** a reminder that fires every hour, verified by one firing.
6. **GitHub from a packet session:** the session can push a `p56/<task id>` branch, open a draft pull request and comment on #1757, in astrid-agent, VibeComfy and astrid-dev.
7. **GitHub for the Orchestrator:** it can read pull requests, commits and workflow runs in those repositories, and comment on #1757.
8. **How many ChatGPT sessions the account can run at once.** Tell the Lead if that is below the cap below, and whether Extra High and Pro are offered.
9. **The Orchestrator can run the tests, on a network-capable machine; never a packet startup check:** it builds the Agent environment (`scripts/worker-env/agent-setup.sh`; VibeComfy: astrid-dev `env/vc-setup.sh`, `env/vc-pytest.sh`) and runs one focused test, such as `tests/core/generation/test_entries.py`.

### Dispatch queue (Plan 56)

Cap: at most **four** packets in Running or Review at once (the Lead may lower or raise it). P56-01 alone first; P56-02 to P56-04 after its early STATUS shows a session can push, open a draft PR and comment, in that order if the account allows fewer. Dispatch the next as slots free and dependencies merge.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R15-P56-01](packets/R15-P56-01.md) The contracts | LE-1a, WS-7a, LE-2a, WS-6a | Done | `r15-P56-01-1` (ChatGPT Pro) | Merged 23 November 2026: Agent #570 (`c3d8ee2d`), VibeComfy #187. Pro |
| [R15-P56-02](packets/R15-P56-02.md) Phase 0, agent side | WS-0a, WS-0b, WS-0d, WS-0g, LE-15 | Done | `r15-P56-02-1` (Extra High) | WS-0a/b/d, LE-15 and WS-0g complete (Agent #591 merged). Extra High |
| [R15-P56-03](packets/R15-P56-03.md) Phase 0, catalog and alignment | WS-0c, WS-0e | Done | `r15-P56-03-1` (High) | Merged 24 Nov 2026: WS-0c (#188, #193, #573), WS-0e (#574). High |
| [R15-P56-04](packets/R15-P56-04.md) Lookup repair and the doctor check | LE-4, WS-5, LE-6 | Done | `r15-P56-04-1` (Extra High) | Merged 24 Nov 2026: LE-4 (#189 + #199 speed fix), WS-5 (#191), LE-6 (#192, #197, #577). Extra High |
| [R15-P56-05](packets/R15-P56-05.md) Recipe installed | WS-7b | Done | — | Merged 24 Nov 2026: WS-7b (#196). Pro |
| [R15-P56-06](packets/R15-P56-06.md) Next-step mappings and `--add` | LE-1b, LE-3, LE-12 | Running | `r15-P56-06-1` (Extra High) | LE-3 and LE-12 VibeComfy halves merged (#200, #201); Agent halves after #599; LE-1b after WS-0g. Extra High |
| [R15-P56-07](packets/R15-P56-07.md) Consent enforced | LE-2b | Done | `r15-P56-07-1` (Pro) | LE-2b complete: VibeComfy #198 and Agent #599 merged (3956bc41); LE-2b fix #621 merged (7fa92be1). RS1 FAIL 3150d425; fixes in P56-12 to -16. Pro |
| [R15-P56-08](packets/R15-P56-08.md) Lookup suggestions, several packs, models | LE-5, LE-16, LE-9 | Blocked | — | After P56-04 and 06. High |
| [R15-P56-09](packets/R15-P56-09.md) Target honesty | LE-8, LE-10, LE-14, LE-17 | Running | `r15-P56-09-1` (Extra High) | LE-10 then LE-8; target_schema after #591; LE-14 after P56-10; LE-17 after RS1. Extra High |
| [R15-P56-10](packets/R15-P56-10.md) Recipe for an unlisted pack | LE-13 | Blocked | — | On hold until the fresh RS1 passes (RS1 failed 11:00Z, 3150d425). Extra High |
| [R15-P56-11](packets/R15-P56-11.md) Renderer, wording, skill proof | LE-18b, LE-11, WS-6b | Blocked | — | After every other packet. Extra High |
| [R15-P56-12](packets/R15-P56-12.md) Restore checkout (F1) | RS1.2, RS1.4 | Ready | — | Extra High. Base: `p56/landing-s1` in each repo. |
| [R15-P56-13](packets/R15-P56-13.md) Lock trust (F2) | RS1.3, RS1.5, RS1.11 | Ready | — | Extra High. Merges after P56-12. |
| R15-P56-14 Selection keeps the authored recipe (F3) | RS1.6 | Done | — | VibeComfy #211 merged into `p56/landing-s1`. Extra High. |
| R15-P56-15 Pip boundary (F4) | RS1.7, RS1.8, RS1.9, RS1.1 if it fits | Done | — | VibeComfy #212 merged into `p56/landing-s1`. Pro. |
| [R15-P56-16](packets/R15-P56-16.md) Publish only after approvals (F5) | RS1.10 | Ready | — | Extra High; Agent and VibeComfy. |
| Conflicts (one task branch at a time writes each) | — | — | — | `cli.py:_workflow_command`: P56-02 (WS-0d, WS-0a), 06, 07, 08, 10; P56-07 goes first of 06, 07, 08 and 10 (critical path) and starts once P56-02's WS-0a has merged. `entries.py:target_schema`: P56-02 (WS-0g), 06 (LE-1b), 08, 09. VibeComfy `_install.py` in the order P56-03, 05, 07, 10, then P56-09's LE-14. `managed_preparation.py:native_failure_diagnostic`: P56-04 (LE-6), then P56-09 (LE-14). P56-01 and P56-04 share `comfyui_engine.py` and `managed_preparation.py` in different functions and may run together (ruling 1). |
| RS1 and R | Review stops | Lead | — | Codex Astra, commissioned by the Lead: RS1 after P56-07; R after P56-11 (up to two rounds) |

### Orchestrator launch message

The owner pastes this into the Orchestrator's own session (`session_011EzfW2WBWyoHTBJggpfEDm`).

```text
You are the Orchestrator for Release 15 Plan 56, reporting to the Lead (mailbox name r15-lead, session_011EzfW2ePdUMAHRAcAm3nur).
Follow skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md in banodoco/astrid-dev.
Read releases/15/run.md at main, section "Plan 56 dispatch", then on main at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1757, format in its first post. Your mailbox name: r15-orchestrator-1.
First do the Orchestrator startup checks and post one STATUS with each result; dispatch nothing until the Lead's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session in the mode its packet's Route sets (N High, X Extra High, S Pro), with the workstream's packet start message. Dispatch P56-01 alone first. Every hour: read the mailbox, check every open packet, run the parallelism pass (start every Ready packet that has no unmet dependency and no file conflict with a Running packet, up to the cap), resume or replace stalled sessions, pass submissions to the Lead, and post one STATUS.
You may start, resume, stop and replace packet sessions and comment on the mailbox. Never dispatch hosted CI: relay a packet's READY-CI to the Lead. You may not merge, edit the repository or approve anything. Send anything reserved to the owner to the Lead.
If a check fails, say which manual step the owner must do instead of promising automation.
```

## Plans 87 and 89 dispatch

Added 23 November 2026 at the owner's request. It works like [Plan 56 dispatch](#plan-56-dispatch) above, with these names:

- **Orchestrator:** each plan's Claude lane session. It takes the Lead's part of the [packet workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md) for its own plan: it writes packets, reviews them, merges them into its plan branch, runs the live proofs and requests the landing gate.
- **Manager:** a separate session that starts and minds a fresh ChatGPT session for each packet. It takes the Orchestrator's part of [multi-manager dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md), with its plan's orchestrator as "the Lead".
- **Release 15 Lead:** above both, in `session_011EzfW1gtAhRQwk8pgJMzhG`, posting as `r15-release-lead`. Packets live in [packets/](packets/), and each plan's `tasks.md` stays the record of progress.

### Authority

On 23 November 2026, in the Release 15 Lead's session (`session_011EzfW1gtAhRQwk8pgJMzhG`), the owner asked for Plans 87 and 89 to farm their remaining tasks out this way, and for Plan 88 to finish as it runs now.

- **Release 15 Lead.** It addresses the orchestrators ([chain](../../skills/shared/run-contract.md#coordination-boards-and-check-ins)). A DECISION from `r15-release-lead` binds all of them and overrides an orchestrator's, within this Authority and the owner's reserved items. A comment still grants nothing beyond this section. Its own gate covers only the landing into `release/15/main`; otherwise it steers and rules.
- **Orchestrators.** For Plan 87, `session_011EzfW2YgL2GSmbJMr9r9SG` (mailbox `r15-p87-orchestrator`); for Plan 89, `session_011EzfW2o5WfJcvHwr8fSDzC` (`r15-p89-orchestrator`). Each is the accountable agent for its plan, as in the [Lead's packet workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md): it writes and orders packets, has each submission reviewed on the run contract's routes, applies the fix-it-yourself rule, merges accepted PRs into `release/<15>/plan-<P>`, merges `release/15/main` into the plan branch, keeps `tasks.md` true, runs every proof that needs an installed stack or the network, dispatches hosted CI under the standing rulings, and asks the Release 15 Lead for the landing gate. Its Codex manager finishes its current card, pushes, writes a handover and stops. The lane keeps Claude subagents for reviews and live proofs.
- **Managers.** `r15-p87-manager-1` and `r15-p89-manager-1`, one per plan, each started by the owner the same way as Plan 56's Orchestrator and acting in her ChatGPT account at her request. A manager may start, resume, stop and replace its own plan's packet sessions and comment on its mailbox. It does not edit the repository, merge, approve or dispatch hosted CI. It reports to its plan's orchestrator and follows the Release 15 Lead's DECISIONs.
- **Packet sessions** may push to the branches their packet's PR destination names, open pull requests there and comment on their plan's mailbox. They never merge, never edit `tasks.md`, never rebase a shared branch, never dispatch hosted CI and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro.
- **What stays in the lane:** see the [packet rules](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#set-up-once).
- **Needs the owner:** publishing, anything paid, her install or media, and changing an existing test's assertion.

### Standing rulings (Plans 87 and 89)

1. Plan 56 rulings 1 (functions, not files, conflict), 2 (packets never move a pin; post `READY-PIN`), 5 (dependants wait only for their own cards) and 6 (proof runs where the network is; post `READY-PROOF <repo> <PR> <head> <selectors>`) apply as written.
2. The orchestrator runs reviews itself on the run contract's routes (high-judgment for S cards, integrity or contract changes, or code already judged unsound; one final round otherwise). It never commissions a packet to review.
3. The release-wide rulings in [the lane orchestrator workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/lane-orchestrator.md) bind the orchestrators: free CI slots, the by-id comparison with each gate request, pin witnesses, fixtures shrink, cross-lane findings go lane to lane.
4. Cap: at most **four** packets in Running or Review per plan; the orchestrator may lower it. The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.
5. Packet sessions run in a normal ChatGPT Chat, not Work (owner, 24 November 2026); the Route sets the mode (N High, X Extra High, S Pro). One writer per branch: replace a stopped session only after its branch has been still for 30 minutes.
6. A test's forging step (direct writes that craft a corrupt or legacy state in setup) may change to a shared helper when a new integrity rule refuses it, if every assertion line stays byte-identical, the helper restores the rule in the same transaction and a test proves it is back (Release 15 Lead, 24 November 2026, for Plan 89's SV-L5).

### Mailboxes

| Plan | Mailbox | Run | Orchestrator | Manager |
|---|---|---|---|---|
| 87 | [astrid-dev #1776](https://github.com/banodoco/astrid-dev/issues/1776) | `r15-p87-dispatch` | `r15-p87-orchestrator` | `r15-p87-manager-1` |
| 89 | [astrid-dev #1777](https://github.com/banodoco/astrid-dev/issues/1777) | `r15-p89-dispatch` | `r15-p89-orchestrator` | `r15-p89-manager-1` |

Cadence, quiet sessions and replacement follow [Plan 56's table](#when-a-session-goes-quiet), with "Lead" read as the plan's orchestrator.

### Manager startup checks

These are [Plan 56's checks](#orchestrator-startup-checks) 1, 3, 4, 5, 7, 8 and 9 (9 for the orchestrator only), run against the plan's own mailbox. Check 2 becomes: `release/15/plan-<P>` exists in each repository the plan's packets name, and no `p<P>/*` branch exists that the board does not list. Check 6 becomes: a packet session can push a `p<P>/<task id>` branch, open a draft PR and comment on the mailbox, in each repository the packets name (Plan 87: astrid-agent, astrid-runtime, astrid-app; Plan 89: astrid-runtime, astrid-agent, astrid-app). The manager posts one STATUS with each result and dispatches nothing until its orchestrator's DECISION answers it.

### Dispatch queue (Plan 87)

The orchestrator writes the packets at its next break point and lists them here. Candidates from [tasks](../../plans/87-render-works/tasks.md): RN-5 (pin and revision report, X), RN-8 and RN-9 (S, Pro), RN-11 (CI render check, X), RN-14 (D2, the motion pack on a fresh install, X). RN-10, RN-12 and RN-13 are renders, so they stay in the lane.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R15-P87-01](packets/R15-P87-01.md) | RN-11 (X): CI render check | Ready (first, alone) | — | Continues `p87/rn11-contract` in astrid-agent; pack-element cases wait for RN-4 |
| [R15-P87-02](packets/R15-P87-02.md) | RN-9 (S): custody retry | Ready (second, after P87-01's early STATUS) | — | Continues `p87/rn9-custody`; high-judgment review (S) |
| [R15-P87-03](packets/R15-P87-03.md) | RN-5 (X): one pinned pack revision | Blocked on RN-4 (orchestrator's lane) | — | Continues the three `p87/rn5-*` branches; `READY-PIN` for the pin |
| [R15-P87-04](packets/R15-P87-04.md) | RN-8 (S): lease through a long render | Blocked on the orchestrator's long-render measurement (`READY-MEASURE`) | — | RN-7 logs are on the plan branch; high-judgment review (S) |
| [R15-P87-05](packets/R15-P87-05.md) | RN-14 (X): motion pack on a fresh install | Blocked on RN-5's pin; sized first | — | Over one day moves to Release 16 |
| [R15-P87-06](packets/R15-P87-06.md) | RN-15 (S): long renders die on a recycled process id | Ready (top priority; Lead DECISION 24 November 2026) | — | New branch `p87/rn15-pid-wrap`; high-judgment review (S); the outputs policy is a separate commit |
| [R15-P87-07](packets/R15-P87-07.md) | `clip.move` and `placement.move` write integer `at_ms` (S) | Ready (dispatch route pending: Lead to confirm manager) | — | New branch `p87/clip-move-int-ms`; Lead DECISION `r15-lead-p87-0004`; branches from the head named at dispatch |
| [R15-P87-08](packets/R15-P87-08.md) | Remove the redundant parent/config clip check P87-07 added to `runtimeGraphToContract` (N) | Ready | — | New branch `p87/graph-clips-check-app` in astrid-app from `release/15/main`; fixes five App vitest failures from P87-07 (Lead ruling `r15-lead-p87-0012`); PR into `release/15/main` |

Stays in the orchestrator's lane: RN-1 to RN-3 (draft astrid-agent#567, awaiting RN-2's real own-object render), RN-4 (`p87/rn4-roots-clean`, review and installed proof), RN-6 and RN-7 (merged), RN-10, RN-12, RN-13 and every real render.

### Dispatch queue (Plan 89)

The orchestrator writes the packets at its next break point and lists them here. Candidates from [tasks](../../plans/89-heavy-saves-in-seconds/tasks.md): SV-L2 (editor timing marks), SV-L3 (copy counters), SV-L5 (immutable accepted history, X), SV-L7 (burst coalescing, once sized), SV-L8 (commit schema validation). Installed measurements stay in the lane.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| R15-P89-01 (withdrawn) | SV-L2 (N): editor timing marks | Done as astrid-app [#377](https://github.com/banodoco/astrid-app/pull/377), in the orchestrator's lane | — | Head `7705ebd4`; the lane runs the focused tests and proves the four marks on an installed drag save |
| [R15-P89-02](packets/R15-P89-02.md) | SV-L5 (X): accepted history immutable | Ready (first, alone) | — | astrid-runtime `p89/SV-L5`; integrity change, high-judgment review |
| [R15-P89-03](packets/R15-P89-03.md) | SV-L8 (N): attribute the 1.7 s of schema validation | Ready (second, after P89-02's early STATUS) | — | Investigation note only; an implementation packet follows on the orchestrator's DECISION |
| [R15-P89-04](packets/R15-P89-04.md) | SV-L3 (N): history-growth counters | Blocked on SV-L6 (Runtime draft #113 merging) | — | Priority after SV-4; evidence: [Plan 88's history-growth lines](../../plans/89-heavy-saves-in-seconds/evidence/2026-11-24-p88-history-growth/README.md) |
| [R15-P89-05](packets/R15-P89-05.md) | SV-L9a (X): a slow startup scan no longer locks a healthy store out | Blocked on SV-L5 (P89-02) merging | — | astrid-runtime `p89/SV-L9a`; #1793; high-judgment review; the watermark (SV-L9b) is Release 16 |
| [R15-P89-06](packets/R15-P89-06.md) | SV-L5 rollback hook (X): installer rollback removes the history guard layer before the older Runtime starts | Ready (second, in parallel with P89-02's rework; uses #115's `remove-history-guards`) | — | astrid-agent `p89/SV-L5-rollback`; Lead's condition: one day or less, else SV-L5 and this hook go to Release 16; lane proves it with both previous Runtimes |
| [R15-P89-07](packets/R15-P89-07.md) | SV-L10 (X): validate the unchanged clips once | Ready (design first; I review the design before code) | — | astrid-runtime `p89/SV-L10`; evidence: Plan 89's counters (894 KB `PreparedCommit`, 1.91 s instrumented); acceptance change, high-judgment review |
| [R15-P89-08](packets/R15-P89-08.md) | SV-L13 (X): editor gesture end to POST, and response to Saved | Ready (funded by the Lead's DECISION 7130359113; design STATUS first) | — | astrid-app `p89/SV-L13`; installed gesture-end-to-Saved measurement on the exact head is the gate; burst test must not get worse |
| [R15-P89-09](packets/R15-P89-09.md) | SV-L11 (X): fewer owned-snapshot copies (`detached`, Agent snapshots) | Ready (count first, then design gate; runs in parallel with SV-L10) | — | astrid-runtime `p89/SV-L11` (Agent only if justified); stop if under about 0.3 s projected; high-judgment review |

Stays in the orchestrator's lane: SV-L1 (merged), SV-L4 (burst test, a measurement), SV-L6 (Runtime covers index, X; the Codex manager's draft #113), SV-L7 (burst coalescing: sized at 4 to 6 App days, awaiting the Release 15 Lead's go), and every installed measurement.

## Plan 82 dispatch

Added 24 November 2026, when the owner gave her go for [Plan 82](../../plans/82-reuse-across-commands/plan.md) (the `astrid generate` caches) and decided its D2 (yes). It works exactly like [Plans 87 and 89 dispatch](#plans-87-and-89-dispatch): the same roles, Authority, standing rulings, manager startup checks and cadence, with these names.

| Plan | Mailbox | Run | Orchestrator | Manager |
|---|---|---|---|---|
| 82 | [astrid-dev #1824](https://github.com/banodoco/astrid-dev/issues/1824) | `r15-p82-dispatch` | `r15-p82-orchestrator`, Claude session `session_011EzfW1e1nGMfuKEg7z7nKN` | `r15-p82-manager-1` |

Plan branches: `release/15/plan-82` in astrid-agent, astrid-runtime and VibeComfy, cut by the orchestrator from each `release/15/main` before the first packet. The manager's check 6 covers those three repositories.

### Rulings for Plan 82

The packet and dispatch rules from Plans 56, 87 and 89 are in the [Lead's packet workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#set-up-once) and [dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md#every-hour). Plan-specific: split RA-2 (S) into the prepared-template contract and key, the approval compile split, then the 53-template differential. RA-0a and every installed timing are the lane's.

**Order:** RA-6 first (it gates every cache); RA-1b in parallel; RA-0b after RA-6, RA-0a and Plan 87's RN-4 on `release/15/main` (until then RA-0b may be built against RN-4's commit on `release/15/plan-87`, cherry-picked under the standing rulings); the RA-2 packets after RA-6; R last, in the lane.

### Dispatch queue (Plan 82)

The orchestrator writes the packets after its startup baseline, lists them here and answers the manager's startup STATUS with a DECISION. Candidates from [tasks](../../plans/82-reuse-across-commands/tasks.md): RA-6 (X), RA-1b (X), RA-0b (X), RA-2 split in up to three (S). RA-0a and R stay in the lane.

Cap: at most **four** packets in Running or Review at once. P82-01 goes alone first; P82-02, P82-03 (design STATUS only) and P82-06 follow once its early STATUS shows a session can push, open a draft PR and comment. **Staged landing (Release 15 Lead, 24 November 2026):** stage 1 is RA-6, RA-1b and RA-0b (none depends on RA-2); stage 2 is RA-2a/b/c and R, in Release 15 only if it makes the freeze, else Release 16. Cache packets emit counters through `cache_event` (astrid-agent #617, merged on `release/15/plan-82` at `69c34457`).

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R15-P82-01](packets/R15-P82-01.md) | RA-6 (X): receipt and companion checked against the admitted bytes | Ready (first, alone) | — | astrid-agent `p82/RA-6`; design STATUS first; high-judgment review (integrity). Host-side check (worker, before `_approve_live`; Lead ruling 24 November 2026): it also stops a direct POST, proved by a test; a Runtime validator seam is Release 16 |
| [R15-P82-02](packets/R15-P82-02.md) | RA-1b (X): lazy imports | Ready (second, after P82-01's early STATUS) | — | astrid-agent `p82/RA-1b`; the lane's import profile is its first STATUS |
| [R15-P82-03](packets/R15-P82-03.md) | RA-2 part 1 (S): prepared-template contract and key | Ready for the design STATUS only (after P82-01's early STATUS); code Blocked on P82-01 merged | — | astrid-agent and VibeComfy `p82/RA-2a`; design STATUS first; high-judgment review; the Lead allowed the design alongside RA-6 |
| [R15-P82-04](packets/R15-P82-04.md) | RA-2 part 2 (S): approval compile split | Blocked on P82-03 | — | VibeComfy and astrid-agent `p82/RA-2b`; same functions as P82-03 (`workflow_bundle.py`, `local_server_engine.py`), so after it; high-judgment review |
| [R15-P82-05](packets/R15-P82-05.md) | RA-2 part 3 (S): the 53-template differential | Blocked on P82-03 and P82-04 | — | VibeComfy `p82/RA-2c`; the four mutation checks are the proof |
| [R15-P82-06](packets/R15-P82-06.md) | RA-0b part 1 (X): install stamp, read-only installed files | Ready (after P82-01's early STATUS; RA-0a is recorded) | — | astrid-agent `p82/RA-0b-stamp`; installer only, no conflict with P82-01; stage 1 of the staged landing |
| [R15-P82-07](packets/R15-P82-07.md) | RA-0b part 2 (X): shipped discovery and registry caches | Blocked on P82-06 and RN-4 | — | astrid-agent `p82/RA-0b-cache`; PB-7c's two refusals against a warm cache first; high-judgment review |

Stays in the orchestrator's lane: RA-0a (the measurements, including the real import profile P82-02 starts from), every installed timing, and R (the final high-judgment review).

## Qualification dispatch

Added 24 November 2026 by the Release 15 Qualifier (`r15-qualifier`, `session_011EzfW1Lc24EARJQsmbgNfo`) under the Lead's instruction. The bar is [qualification.md](qualification.md). Mailbox: [astrid-dev #1834](https://github.com/banodoco/astrid-dev/issues/1834), run `r15-qual-dispatch`. Manager: `r15-qual-manager-1`, which starts one fresh ChatGPT session per packet (`r15-Q-NN-<n>`); the Qualifier is the packet workstream's Lead for this queue, and the Release 15 Lead keeps the gate into `release/15/main`.

### Rules for qualification packets

1. **Issue packets only** ([rolling queue](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#rolling-queue)): a failing test id or an exact repro that a sandbox with no network can target, a fix of about 3 hours or less, one contract, no owning lane. A failure in a plan's own code goes to that plan's orchestrator.
2. **Never packet work:** anything needing an installed build, a GPU, a render, a real timing or hosted CI to reproduce.
3. **Each packet carries** its exact selectors, the failing ids, the tests that must pass unchanged, and "no existing assertion changes".
4. **PR destination:** `p15q/<packet id>` → `release/15/q-<topic>` (a topic branch the Qualifier cuts from `release/15/main`), then `release/15/q-<topic>` → `release/15/main` through the Lead's gate.
5. **Proof:** a packet ends with `READY-PROOF`; the Qualifier answers within 45 minutes, in parallel. Packets never merge, edit `tasks.md` or dispatch hosted CI.
6. **Cap:** at most **three** packets in Running or Review at once. None starts before the Lead's DECISION answers the manager's startup STATUS and the Qualifier posts its own.

### Dispatch queue (qualification)

| Packet brief | Source failure | Handoff | Session | Next action / evidence |
| --- | --- | --- | --- | --- |
| [R15-Q-01](packets/R15-Q-01.md) | Agent writes must open in the editor (qualification row 5; Lead DECISION r15-lead-qual-0004): parser contract harness | Ready (first, alone; after its early STATUS, up to three at once) | — | astrid-agent `p15q/R15-Q-01` → `release/15/q-agent-writes`; Route X; phase 1 is the parser, R15-Q-03 (loader, fractional `start_ms`) follows; the Qualifier records the selectors' baseline in the PR body |
| [R15-Q-03](packets/R15-Q-03.md) | Agent writes keep every `_ms` field a whole number the editor accepts (Plan 87 fixed one instance; this checks the class) | Ready (second, after R15-Q-01's early STATUS) | — | astrid-agent `p15q/R15-Q-03` → `release/15/q-agent-writes`; Route X; builds on R15-Q-01's harness files if present; proof merges Plan 87's `2efd174a` into the topic branch |
