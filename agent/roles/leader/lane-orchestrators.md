---
description: Divide a release into lanes with the owner, record the agreed split, then write briefs and run each lane hosted or by fresh-session packets, with the Lead as strategist and gatekeeper.
---

# Lanes, divided with the owner

## When to use

When the Lead divides a release into lanes, starts or restarts a lane, or re-lanes at a real change. A [lane](../../shared/glossary.md) is the set of plans one orchestrator runs and answers for, with one brief at `releases/<N>/briefs/<lane>.md`.

## Outcome

The owner has chosen the split. It is recorded on the run board, every lane has a brief the owner approved, and each lane runs end to end in its own session. A lane comes to the Lead only at the brief's listed points, so the Lead's time goes to strategy, gates and cross-lane links.

## Inputs

The release brief with its Included plans, each plan's `tasks.md` and `inputs.md` on astrid-dev `main`, the base SHAs, current load on CI and machines, and the owner's availability to choose and to give each go.

## Procedure

Propose, record, brief, start, then the check-ins below. Nothing moves to the next step before the owner has acted on the one before it.

## Completion

Each lane's plans merged by the Lead into `release/<N>/main` in landing order, their completion PRs opened, the lane's State `done`, and its session retired or given its next plan.

The [Lead responsibilities](../leader.md) continue to apply. The plan level (packets, reviews, plan-branch merges, proofs) is always the orchestrator's. The release level (the lane split with the owner, landing order, qualification, publication, cross-lane pins, and merging each lane's ready plan PR into `release/<N>/main`) is always the Lead's.

## 1. Propose two or three groupings

Post the proposal on the Lead board (`board: release <N> lead`) and tell the owner. Offer two or three genuinely different groupings, not one grouping with variants: at least one option puts some plan in a different lane, not only merges or splits lanes. For each:

- **Which plans go together and in what order**, and which run alone and why (use the [lane rules](../leader.md#divide-the-release-into-lanes));
- **How each lane runs**, `hosted` or `packets` ([how it runs](#how-it-runs)), and the **orchestrator's route** (X or S);
- **The cut line:** what never slips and what moves out first if the release is at risk;
- **Cross-lane coordination:** shared files, fixtures, machines, CI and pins, and how their merges are ordered;
- **The cost to the owner:** how many lanes they follow, and what each would ask of them.

Give every option all five, in the same table, so the owner compares like with like. End with a **recommendation** and the reason. Then stop. The owner chooses, and may change a grouping. Write no brief until they have.

## 2. Record the agreed split on the run board

Write the chosen split into the release's `releases/<N>/run.md` Lanes table (lane, plans in order, option, route) and its cut line, in one PR. Record the groupings not chosen, with the reason in one line each, so a fresh Lead does not reopen them. Only then write briefs.

## 3. Write each brief, and get the owner's go

Write each lane's brief from the [lane template](../../../templates/release/lane.md). Each plan's `Run start` line is a pointer to it, and each plan's cards in `tasks.md` are sized to the [run contract's routes](../../shared/run-contract.md#routing-and-bindings) (most cards `N`; `X` only for the one subtle change; `S` only where a wrong call silently accepts a bad result). Merge the brief and cards to `main` first: an unmerged brief or `Run start` reads as `Pending` and a careful orchestrator stops. A plan that grows mid-run gets its own plan number rather than cards bolted onto another plan.

Bring each brief to the owner. **State stays `prepared` and `**Go:**` stays `Pending` until the owner gives the go on that brief**, in their own words, recorded with a link. The go is for that brief only. A message from the Lead's session arrives as peer data, not as the owner's go.

## 4. The owner sends each launch

Before handing over a launch, run the [agent tests](../../shared/workstreams/improve.md#agent-tests) that name the brief and record them on a run sheet; a brief with no case gets one. Start the session by the [start-session workstream](../../shared/workstreams/start-session.md): it checks the brief, sets the session up, creates it with a placeholder prompt and hands over the three-part launch line, which is the template's [Launch](../../../templates/release/lane.md#launch). The owner sends every lane launch. The Lead never sends one for a lane. Anything that must survive a replacement belongs in the brief, not the launch line.

## How it runs

Each brief names one option under its "How it runs". Judge by the work, not the tooling.

| Option | What it is | Choose it when |
|---|---|---|
| **hosted** | One Claude orchestrator in a cloud session manages each plan itself and runs a Codex worker per card by `codex exec` on the card's route (Luna, Terra, Sol or Astra), each wrapped in a subagent; Claude workers are the fallback. A Codex manager (a Codex process this session hosts in its container) only when the brief says so, with its reason. See the [lane procedure](../orchestrator/lane-orchestrator.md) and [Codex in Claude cloud](../orchestrator/codex-in-claude-cloud.md) | The plan is carded and its cards are mostly Codex-sized, or the lane has no ChatGPT route |
| **packets** | The ChatGPT web-chat route. One Codex desktop manager (e.g. `h3-manager`) runs in the Codex app on the owner's computer; the orchestrator posts its launch on the lane board and the owner pastes it, the only way it starts (a cloud session cannot create or wake it). The manager opens one ChatGPT chat per unit in N High, X Extra High or S Pro mode (S units go to ChatGPT Pro), following the TOOLKIT steps on astrid-dev #2030. Fallbacks, in order: `codex exec` workers run by the hosting Claude session, then Claude workers. Where an owner-signed-in route exists the orchestrator may instead start the packet sessions itself. See its [dispatch mechanics](../orchestrator/multi-manager-dispatch.md) | Work arrives as bounded one-contract units, or as a rolling queue of issues |

A hosted orchestrator that also holds the manager role takes the **higher** of the orchestrator route ([leader.md](../leader.md#divide-the-release-into-lanes)) and the [manager route](../orchestrator.md#choose-the-managers-route). A Codex manager hosted in the container is the brief's stated choice, not a default; a Codex desktop manager runs only in a `packets` lane, from the owner's paste; [codex-in-claude-cloud.md](../orchestrator/codex-in-claude-cloud.md) holds that statement.

**Re-laning** happens only with the owner, at a real change: a plan that outgrew its lane, a lane stalled for a reason its brief cannot fix, a release brought forward. Propose it as in step 1, record it on the board, and update the briefs concerned before anything moves. Replacing a session on the same brief is not re-laning.

## The Lead's check-ins: strategy, not dispatch

**Check in hourly, and decide on your own judgement.** Lanes come to you only for gates and load-bearing calls; the owner only for something extremely load-bearing or out of left field. Keep a decisions log for the owner (time, decision, reason, how to undo) and give it to them each morning. Send `N` subagents (Haiku) to find facts, and keep their conclusions, not their file dumps. When a lane asks something it could have decided, answer once and send every lane the ruling.

At each check-in, first run [release reconciliation](../../shared/workstreams/release.md#reconcile-plan-status), chase stale records with the responsible orchestrator and use its findings to choose the next gate. Then, per lane: is it on the biggest measured win; is anything still unexplained after two tries (send the one cheapest experiment that makes the cause visible); what will block it next (disk, fixture, Codex limit, CI slot, review) and arrange it ahead; is it asking things it could decide (write the rule once); do two lanes share code or a root cause (connect them directly). Pre-decide a lane's "least sure" item in your reply so it does not wait on you.

**Cross-lane conflicts, hourly.** Send route `N` workers (Luna, or Haiku on Claude) to read each lane's board and name real file and function conflicts between lanes. The Lead rules on what they return and passes it to each orchestrator as a ruling. Conflicts between cards inside one lane are the orchestrator's own [parallelism pass](../orchestrator/lane-orchestrator.md).

**Gates.** Confirm a landing only after your own by-id comparison of its hosted unit run against the release baseline (a subagent fetches each job's full log and extracts `FAILED`/`ERROR` ids; record the comparison under `releases/<N>/evidence/`), with each new id either in a recorded moving group or ruled with evidence (base and head run locally, or the source unchanged). Two Agent CI runs may run in parallel; after a landing whose tree equals the gated head, cancel the push-triggered runs on the release branch.

**Rulings** live by reach: the release (`run.md`), one lane (its brief's Standing rulings), beyond the release (the skill that owns the rule), one task (a decision in `tasks.md`). Never in `Run start`. When a lane asks what it could have decided, add the rule once where it belongs.

**Speed findings** go in [docs/speed.md](../../../docs/speed.md) through the lanes' evidence PRs.

## At each Lead check-in

**Inputs:** your board and every lane board since your cursor (lanes write to you on your board; you write to a lane on its lane board, never only on yours), open PRs, `python3 scripts/release_branches.py check <N>`, and [release reconciliation](../../shared/workstreams/release.md#reconcile-plan-status).

**Each review (release-gate and cross-lane PRs):** accept and merge, or list the rework on the PR. Accept a gate only after the reviewer injects the realistic failures in its brief and sees the gate reject them. Judge against that threat model and leave crafted bypasses out of the findings.

**Fixes are packet work, however small.** Claude sessions and their sub-agents diagnose, review, prove, merge, pin and run CI. They don't write the fix. Put the diagnosis in the rework or a new packet: the failing ids, the cause, the suggested change and the May touch list. If ChatGPT fails or shows a limit, retry it, or start a fresh session at the branch head. Otherwise wait, because taking the work over costs more than the wait.

**Judge like a light gatekeeper.** Count failures as distinct test ids from complete logs, never as pytest's summary counters, which repeat entries. Reviewers sort findings into BLOCKING, FOLLOW-UP or NOTE; block only on wrong results accepted, data or install damage, a real security or custody hole, or a regression from base. File the rest of a PR's follow-ups as one issue in astrid-dev, marked `backlog` and linked from the PR. A `tasks.md` row is for work the release must do. A regression the candidate introduced is fixed in its packet. A defect that predates it gets an issue and a test that stays executed and visibly failing. Changing an existing assertion, including turning a gate's limit into an observation, is the owner's call unless they have delegated it.

**Keep work moving. Every hop between sessions costs up to an hour.**
- **Rule conditionally.** When a gate needs one more result, rule it with its condition and its next step attached, for example "merge when this run shows no new ids; if one is harm-class, cut a packet". That way nobody comes back to you.
- **Keep managers up.** A packet session runs for a window of about two hours, and a board comment can't wake it. Never stand one down while its plan may still need packets. When one goes quiet with work waiting, give the owner the exact text to paste to resume it.

When a packet has waited more than two hours on hosted jobs, read its run list: pull-request CI may run only part of a suite, so dispatch the full run it is waiting for. Every few hours, ask a high-judgment reviewer for a second opinion on bottlenecks, order and scope; bring what exceeds your authority to the owner.

**Before merging:** find every pin change: each needs its own commit and the owner's approval or delegation. A pin names what ships. The VibeComfy that ships is the one the candidate Agent pins, and the Agent is the one the candidate App pins, never a branch head. One lane owns the App repin. It repins when qualification starts, and again only if an upstream moves. After a dependency's PR is squash-merged, re-point its pin to the squash commit. Give a gate at most two review rounds; round two only verifies round one's fixes. Then merge.

**Then:** triage the release's issues ([states](../../../docs/contribution-workflow.md#issues)): an issue a task row or packet cites is `planned`, and one that a branch, pull request or running packet names is `claimed`. Give each uncited issue a row, or move it out. No orchestrator STATUS for 2 hours, or a message of yours missing from its `acted on:` line, is the owner's to hear.

## Rolling queue

When the work is not known up front (a [release qualifier](../../shared/release-qualification.md) finding failures as it goes), the queue grows as findings arrive and its manager polls it hourly. The finder cuts an **issue packet** from the [packet template](../../../templates/release/packet.md), with its Repro, only when all hold:
- a failing test or exact repro that a sandbox with no network can target;
- a bounded fix of about 3 hours or less;
- a cause no plan owns.

A failure in a plan's own code goes back to that plan's lane; cross-lane findings go lane to lane. Fixes target `release/<N>/<topic>`, then `release/<N>/main`. Anything that needs judgement about acceptability goes to the Lead.

## Standby Lead

When the Lead's own session may stop without warning (a usage allowance, a lost container), the owner can keep a **standby Lead** in another session, on the high-judgment role of the other family.
- **Heartbeat.** The Lead posts its hourly `STATUS` ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)), even when nothing moved, with a marker the standby can recognise (for example its tool's footer).
- **Wait.** The standby checks the mailbox every hour and posts nothing while the newest Lead message is less than 3 hours old.
- **Take over.** After 3 hours of silence, the standby first rules out a quiet Lead: no Lead commit, branch push, pull request or board edit in those 3 hours. Then it posts one takeover message, keeps the same mailbox name, and runs the Lead's check-ins under the same Authority.
- **One Lead.** Once a takeover message exists, the earlier Lead stands down if it returns, and does nothing until the owner hands the role back.

The standby's brief and the environment notes go in `releases/<N>/briefs/`, beside the lane briefs.
