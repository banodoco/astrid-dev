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
| Timeline: Plan 69, then Plan 77 (a loop plan) | Claude orchestrator `session_011EzfW1FXS3o7GFnNSB7cZS`, hosting a Codex manager | [briefs/plans-69-77.md](briefs/plans-69-77.md) | Plan 69 landed. Plan 77’s exact first cut reopened a persisted local selection in 4.074 and 4.506 s and confirmed one legal save in 34.254 s. The first previously unset workspace selection for the actor in the realm still cost a 17.146 s reopen. Stock and candidate both refused the default direct restart. The owner chose to land with that limit stated ([#1521](https://github.com/banodoco/astrid-dev/issues/1521)). The local compatibility repeat passed. The first-cut Runtime PR includes landed Plan 81 and a reviewed fix for the duplicate diagnostic emitter. The unchanged macOS watchdog failed one isolated diagnostic iteration on the exact Runtime base. The Lead recorded inherited fragility in [#1621](https://github.com/banodoco/astrid-dev/issues/1621) and landed Runtime at `737843e9`. The Agent topic contains landed Plan 40 and pins that Runtime. The Lead cleared the exact hosted gate and [Agent PR #555](https://github.com/banodoco/astrid-agent/pull/555) landed at `b324d7c1`. The App has regenerated both release 15 pins and is qualifying two local source repairs for the standing local suite before the hosted App gate. [Runtime PR](https://github.com/banodoco/astrid-runtime/pull/102) The separate startup slice is parked in unmerged branches. Its local synthetic probe crossed 135 s pending on both routes. A later two-save profile on 300 clips confirmed 57.498 and 19.712 s to Saved. The fresh save run uses those profiles. [Parked source and verdicts](../../plans/77-saving-holds-on-a-heavy-timeline/tasks.md#first-cut-gate-and-parked-work-23-november-2026) [Save profile](https://github.com/banodoco/astrid-dev/pull/1638) [Grown startup proof](../../plans/77-saving-holds-on-a-heavy-timeline/rounds.md#grown-300-clip-startup-development) [Installed requalification](../../plans/77-saving-holds-on-a-heavy-timeline/evidence/2026-11-22-release-15/first-cut-installed-requalification/RESULT.md) |
| Commands: Plan 81, with Plan 13 | Claude orchestrator `session_011EzfW2Ut856AFGZS8ZamHU`, hosting Codex managers on route X | [Plan 81 handover](../../plans/81-once-per-command/handover.md) | Plan 13 landed. Plan 81: gain measured, review failed, fixes in progress on a frozen scope; then one installed re-measurement and the reviewer's check |
| Vision page: Plan 84 (a taste plan) | Claude orchestrator `session_011EzfW1Df4SCkBoafGdR1di`, which hosted a Codex manager on route T | start message from the owner, 22 November | Paused: the owner stopped the first run on 22 November after PL-0 and PL-1. PL-1 is on `release/15/plan-84` (astrid-app #371); PL-2 is nearly done on its own branch; an entry repair is open as astrid-app #372. A second run waits on her go ([plan](../../plans/84-living-planet-on-the-vision-page/plan.md)) |
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

### Waiting on the owner

- **The cut line and the headline.** The release is named for every platform and rented machines; what is running is speed and editing. The Lead recommends naming it for what will ship and moving Plans 63, 76, 18 and 39 to the next release.
- **Plan 56: a standby Lead.** A Lead whose session stops is not covered for Release 15 yet; name a standby Lead session (the other model family) under `releases/15/lead/` ([how](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md#standby-lead)), or accept that the owner restarts the Lead by hand.
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

## Plan 56 dispatch

Added 23 November 2026 at the owner's request. The Lead rewrites this section at each check-in. Packets are in [packets/](packets/); the plan's `tasks.md` stays the record of progress.

### Authority

On 23 November 2026 the owner, in an orchestrating session (`session_011EzfW4BJ221kXBNRB4xQcG`), asked for Plan 56 to be set up for the [fresh ChatGPT packet workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md).

- **Accountable agent** for Plan 56: the Release 15 Lead, `session_011EzfW2ePdUMAHRAcAm3nur`; there is no separate plan manager. It writes and orders packets, reviews packet PRs, merges accepted ones into `release/15/plan-56`, merges `release/15/main` into it, keeps `tasks.md` current, runs the review stops (RS1 after WS-7b and LE-2b, and R, up to two rounds) with Codex Astra, and may move the Agent's VibeComfy pin on `release/15/plan-56` with `scripts/vibecomfy_pin.py`. It confirms the landing gate before anything goes into `release/15/main`, and gives hosted CI slots.
- **Sessions in use (23 November 2026):** the Lead runs in `session_011EzfW2ePdUMAHRAcAm3nur` (the owner's brief and the Run start named `session_011EzfW1gtAhRQwk8pgJMzhG`; the role and the mailbox name `r15-lead` are unchanged). The Orchestrator is the Codex session `01a20a4e-a34d-7a51-ab59-536b6cfa6869`, posting as `r15-orchestrator-1`. On the owner's override the Orchestrator dispatched P56-01 at 21:44 UTC, before this board reached `main`.
- **The Orchestrator** acts in the owner's ChatGPT account at her request, so its start messages are hers. It may start, resume, stop and replace packet sessions and comment on the mailbox; it does not edit the repository.
- **A packet session may:** push to the branches its packet's PR destination names, open pull requests to that destination, and comment on the mailbox. It never merges, never edits `tasks.md`, never rebases a shared branch, never dispatches hosted CI and never takes a second packet.
- **Session mode follows the packet's Route:** N High, X Extra High, S Pro ([run contract](../../skills/shared/run-contract.md#chatgpt-session-modes)).
- **Bases:** astrid-agent `release/15/plan-56` from `release/15/main` (`045064b6`); VibeComfy `release/15/plan-56` from `c0e910ca`, the commit the Agent pins, which contains VibeComfy `release/15/main` (`48b5fa9e`), so both branches carry the current `release/15/main`. When `release/15/main` moves, the Lead merges it into `release/15/plan-56`; a packet never does.
- **Needs the owner:** the live SAM run (WS-L, after R), publishing, anything paid or touching her install or media, and decisions D10–D12 before landing (build to the recommendations meanwhile).

### Standing rulings (Plan 56)

1. **Different functions in one file are not a conflict** between packets; the same function or the same new test table is. The holder is the task branch, not the packet: a function is free for the next packet once the last task that writes it has merged. (Proposed by the owner and confirmed by the Lead, 23 November 2026.)
2. **Cross-repo packets never move a pin:** they post `READY-PIN <VibeComfy head>` and the Lead adds the pin commit.
3. **RS1 and R are commissioned by the Lead,** each by Codex Astra.
4. **The Plan 56 bases include `release/15/main` of both repositories** (the owner, 23 November 2026, through the Orchestrator); the Lead records each base's head and ancestry in `releases/15.md` Branches.
5. **A packet's dependants wait only for the cards they depend on,** not for the whole packet (Lead, 23 November 2026).
6. **Proof runs where the network is.** ChatGPT packet sandboxes cannot reach `github.com`. Packet sessions publish through the connector and post `READY-PROOF <repo> <PR> <head> <selectors>`. The Lead runs the Agent proofs, the VibeComfy fast suite by id, and the requalification of integrated heads; the Orchestrator may run VibeComfy focused proofs on the owner's computer (Lead, 23 November 2026).
7. **Hosted CI.** VibeComfy's `ci` runs no unit tests (astrid-dev #1768), so the Lead's local fast suite, compared by id, replaces it (baseline at `c0e910ca`: 758 passed, 9 failed, 9 skipped). Agent `ci.yml` does not trigger on `release/*/plan-*`; the Lead dispatches it on `release/15/plan-56` after each batch and compares it by id with `agent-ci-baseline-8807f820` (Lead, 23 November 2026).
8. **Batch integration.** The Lead merges accepted VibeComfy PRs with `--no-ff`, tests the integrated tree, pushes that exact tree, and adds one cumulative Agent pin per batch (Lead, 23 November 2026).

### Mailbox

[astrid-dev #1757](https://github.com/banodoco/astrid-dev/issues/1757), run `r15-dispatch`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Lead | `r15-lead` | `session_011EzfW2ePdUMAHRAcAm3nur` | 7116279618 |
| Orchestrator | `r15-orchestrator-1` | `01a20a4e-a34d-7a51-ab59-536b6cfa6869` (Codex) | 7114811678 |
| Packet session | `r15-<packet>-<n>`, for example `r15-P56-01-1` | from the Orchestrator's STATUS | — |

Cadence and time limits are those of [multi-manager dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md): the Orchestrator reads the mailbox and checks every open packet each hour; a Running packet with no commit or STATUS for 3 hours is resumed; one that will not load, does not reply 30 minutes after a resume, or is quiet for 6 hours is replaced from its branch head (never two writers on one branch); a Review unanswered for 4 hours is a REQUEST to the Lead and a note to the owner.

### When a session goes quiet

A branch, not a chat, shows health: look at the packet's branch and pull requests before judging a session. Work that has not moved is blocked by the work or by the environment (a session that cannot push, start or resume; a missing permission; CI capacity): fix an environment cause where it lives, or bring the owner the exact step, and never dispatch into the same wall again.

| Who is quiet | At 2 hours | At 3 hours | At 6 hours |
|---|---|---|---|
| A packet session (no commit or STATUS) | The Orchestrator checks its branch and PRs and marks it "quiet" in its hourly STATUS with the last evidence; it takes no other action yet | The Orchestrator resumes the session and posts the resume on the mailbox | If the chat will not load after one reload, or gives no reply 30 minutes after the resume, or is still quiet: broken. If its branch moved in the last 30 minutes, wait. Otherwise the Orchestrator replaces it (`r15-<packet>-<n+1>`) from the branch head and last STATUS, naming that head in the first message; never two writers on one branch |
| The Orchestrator (no STATUS on the mailbox) | The Lead checks that the Orchestrator's hourly reminder is still running and, if the session is reachable, nudges it; if not, the Lead tells the owner at once and names the manual step (open the session and say "continue") | The Lead tells the owner again, and starts no new packet itself | The Lead asks the owner to start a fresh Orchestrator from the board, which holds every session and state |
| The Lead (no STATUS or DECISION; the Lead posts a heartbeat STATUS at least every 90 minutes) | The Orchestrator keeps its running packets going and starts nothing new that needs a Lead ruling; it tells the owner | The Orchestrator sends the owner the list of Review packets waiting and the exact REQUESTs outstanding | The owner hands the role to a standby Lead (none is named yet: see Waiting on the owner), which takes over under the same mailbox name `r15-lead` after ruling out a quiet Lead (no commit, push, PR or board edit in those hours) |
| A Review (a submitted packet, unanswered by the Lead) | The Orchestrator tells the Lead it is waiting | At 4 hours: the Orchestrator sends a REQUEST and tells the owner | — |

A message is not ACKed after two cycles: the sender sends it again. A silent mailbox is never fixed by starting a duplicate session.

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
9. **A packet session can run the tests:** it can build the Agent environment with astrid-agent's in-repo `scripts/worker-env/agent-setup.sh` (VibeComfy at the Agent's pin) and run one focused test, for example `tests/core/generation/test_entries.py`; for VibeComfy, which has no in-repo copy, astrid-dev `env/vc-setup.sh` and `env/vc-pytest.sh`.

### Dispatch queue (Plan 56)

Cap: at most **four** packets in Running or Review at once (the Lead may lower or raise it). P56-01 alone first; P56-02 to P56-04 after its early STATUS shows a session can push, open a draft PR and comment, in that order if the account allows fewer. Dispatch the next as slots free and dependencies merge.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| [R15-P56-01](packets/R15-P56-01.md) The contracts | LE-1a, WS-7a, LE-2a, WS-6a | Done | `r15-P56-01-1` (ChatGPT Pro) | Merged 23 November 2026: Agent #570 (`c3d8ee2d`), VibeComfy #187. Pro |
| [R15-P56-02](packets/R15-P56-02.md) Phase 0, agent side | WS-0a, WS-0b, WS-0d, WS-0g, LE-15 | Running | `r15-P56-02-1` (Extra High) | WS-0d VibeComfy half merged (#190); Agent #581 open; WS-0a next. Extra High |
| [R15-P56-03](packets/R15-P56-03.md) Phase 0, catalog and alignment | WS-0c, WS-0e | Running | `r15-P56-03-1` (High) | WS-0c VibeComfy half merged (#188); Agent #573, #574 open; WS-0e fail-closed guard approved. High |
| [R15-P56-04](packets/R15-P56-04.md) Lookup repair and the doctor check | LE-4, WS-5, LE-6 | Running | `r15-P56-04-1` (Extra High) | LE-4 (#189), WS-5 (#191) and LE-6's VibeComfy half (#192) merged; Agent #577 open. Extra High |
| [R15-P56-05](packets/R15-P56-05.md) Recipe installed | WS-7b | Ready | — | Dependencies met (WS-7a, WS-0c merged); start first. Pro |
| [R15-P56-06](packets/R15-P56-06.md) Next-step mappings and `--add` | LE-1b, LE-3, LE-12 | Blocked | — | After P56-01, 02, 03. Extra High |
| [R15-P56-07](packets/R15-P56-07.md) Consent enforced | LE-2b | Blocked | — | After P56-01 and 05; then the Lead's RS1. Pro |
| [R15-P56-08](packets/R15-P56-08.md) Lookup suggestions, several packs, models | LE-5, LE-16, LE-9 | Blocked | — | After P56-04 and 06. High |
| [R15-P56-09](packets/R15-P56-09.md) Target honesty | LE-8, LE-10, LE-14, LE-17 | Blocked | — | After P56-04, 07 and RS1; its LE-14 after P56-10. Extra High |
| [R15-P56-10](packets/R15-P56-10.md) Recipe for an unlisted pack | LE-13 | Blocked | — | After P56-05, 06, 07 and RS1. Extra High |
| [R15-P56-11](packets/R15-P56-11.md) Renderer, wording, skill proof | LE-18b, LE-11, WS-6b | Blocked | — | After every other packet. Extra High |
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

Added 23 November 2026 at the owner's request. It works like [Plan 56 dispatch](#plan-56-dispatch) above, with one difference: each plan's **lane orchestrator acts as the Lead for its own plan** (it writes packets, reviews them, merges them into its plan branch, runs the live proofs and requests the landing gate). A separate **dispatch manager** starts and minds a fresh ChatGPT session for each packet. The Release 15 Lead gates only the landing into `release/15/main`. Packets live in [packets/](packets/), and each plan's `tasks.md` stays the record of progress.

### Authority

On 23 November 2026, in the Release 15 Lead's session (`session_011EzfW1gtAhRQwk8pgJMzhG`), the owner asked for Plans 87 and 89 to farm their remaining tasks out this way, and for Plan 88 to finish as it runs now.

- **Lane Leads.** For Plan 87, its lane orchestrator `session_011EzfW2YgL2GSmbJMr9r9SG` (mailbox `r15-p87-lead`); for Plan 89, `session_011EzfW2o5WfJcvHwr8fSDzC` (`r15-p89-lead`). Each is the accountable agent for its plan, as in the [Lead's packet workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md): it writes and orders packets, has each submission reviewed on the run contract's routes, applies the fix-it-yourself rule, merges accepted PRs into `release/<15>/plan-<P>`, merges `release/15/main` into the plan branch, keeps `tasks.md` true, runs every proof that needs an installed stack or the network, dispatches hosted CI under the standing rulings, and asks the Release 15 Lead for the landing gate. Its Codex manager finishes its current card, pushes, writes a handover and stops. The lane keeps Claude subagents for reviews and live proofs.
- **Dispatch managers.** `r15-p87-manager-1` and `r15-p89-manager-1`, one per plan, each started by the owner the same way as Plan 56's Orchestrator and acting in her ChatGPT account at her request. A manager may start, resume, stop and replace its own plan's packet sessions and comment on its mailbox. It does not edit the repository, merge, approve or dispatch hosted CI. It follows [multi-manager dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md), with its lane Lead as "the Lead".
- **Packet sessions** may push to the branches their packet's PR destination names, open pull requests there and comment on their plan's mailbox. They never merge, never edit `tasks.md`, never rebase a shared branch, never dispatch hosted CI and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro.
- **What stays in the lane:** real renders, installed save measurements, fixture builds and anything else that needs an installed stack. A packet's proof is its focused tests. Its acceptance proof is the lane's (Plan 56 ruling 6: packet sandboxes cannot reach `github.com`).
- **Needs the owner:** publishing, anything paid, her install or media, and changing an existing test's assertion.

### Standing rulings (Plans 87 and 89)

1. Plan 56 rulings 1 (functions, not files, conflict), 2 (packets never move a pin; post `READY-PIN`), 5 (dependants wait only for their own cards) and 6 (proof runs where the network is; post `READY-PROOF <repo> <PR> <head> <selectors>`) apply as written.
2. The lane Lead runs reviews itself on the run contract's routes (high-judgment for S cards, integrity or contract changes, or code already judged unsound; one final round otherwise). It never commissions a packet to review.
3. The release-wide rulings in [the lane orchestrator workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/lane-orchestrator.md) bind the lane Leads: free CI slots, the by-id comparison with each gate request, pin witnesses, fixtures shrink, cross-lane findings go lane to lane.
4. Cap: at most **four** packets in Running or Review per plan; the lane Lead may lower it. The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.

### Mailboxes

| Plan | Mailbox | Run | Lane Lead | Dispatch manager |
|---|---|---|---|---|
| 87 | [astrid-dev #1776](https://github.com/banodoco/astrid-dev/issues/1776) | `r15-p87-dispatch` | `r15-p87-lead` | `r15-p87-manager-1` |
| 89 | [astrid-dev #1777](https://github.com/banodoco/astrid-dev/issues/1777) | `r15-p89-dispatch` | `r15-p89-lead` | `r15-p89-manager-1` |

Cadence, quiet sessions and replacement follow [Plan 56's table](#when-a-session-goes-quiet), with "Lead" read as the lane Lead. The lane Lead posts a heartbeat STATUS on its mailbox at least every 90 minutes.

### Manager startup checks

These are [Plan 56's checks](#orchestrator-startup-checks) 1, 3, 4, 5, 7, 8 and 9, run against the plan's own mailbox. Check 2 becomes: `release/15/plan-<P>` exists in each repository the plan's packets name, and no `p<P>/*` branch exists that the board does not list. Check 6 becomes: a packet session can push a `p<P>/<task id>` branch, open a draft PR and comment on the mailbox, in each repository the packets name (Plan 87: astrid-agent, astrid-runtime, astrid-app; Plan 89: astrid-runtime, astrid-agent, astrid-app). The manager posts one STATUS with each result and dispatches nothing until its lane Lead's DECISION answers it.

### Dispatch queue (Plan 87)

The lane Lead writes the packets at its next break point and lists them here. Candidates from [tasks](../../plans/87-render-works/tasks.md): RN-5 (pin and revision report, X), RN-8 and RN-9 (S, Pro), RN-11 (CI render check, X), RN-14 (D2, the motion pack on a fresh install, X). RN-10, RN-12 and RN-13 are renders, so they stay in the lane.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| — | — | — | — | The lane Lead writes the first packets |

### Dispatch queue (Plan 89)

The lane Lead writes the packets at its next break point and lists them here. Candidates from [tasks](../../plans/89-heavy-saves-in-seconds/tasks.md): SV-L2 (editor timing marks), SV-L3 (copy counters), SV-L5 (immutable accepted history, X), SV-L7 (burst coalescing, once sized), SV-L8 (commit schema validation). Installed measurements stay in the lane.

| Packet brief | Source plan/tasks | Handoff | Session | Next action / evidence |
|---|---|---|---|---|
| — | — | — | — | The lane Lead writes the first packets |
