---
description: Prepare and lead fresh-session packet delivery across accepted release work without delegating the Lead's review or integration authority.
---

# fresh-session ChatGPT packet dispatch

## When to use

When the Lead coordinates accepted release work through fresh ChatGPT manager sessions rather than a single long-lived manager.

## Outcome

Lead-prepared, authorized release packets with one durable dispatch queue and review-ready task evidence.

## Inputs

An approved release brief, current plan task records, packet scope and dependencies, owner authorization, branch destinations and evidence requirements.

## Procedure

Prepare bounded packets and the coordination boards, run Lead check-ins, review delivered task PRs and integrate only authorized work using the sections below.

## Completion

The queue and task records reflect every packet, its evidence and disposition, with review/integration decisions owned by the Lead.

Use when the Lead prepares accepted plan work for an Orchestrator to assign to **a fresh ChatGPT manager session per packet**. The [Lead responsibilities](../leader.md) continue to apply.

**A lane can be the Lead for its own plan.** In a release run by [lane orchestrators](lane-orchestrators.md), a lane's orchestrator may take the Lead's part here for its own plan: it writes and reviews packets, merges into its plan branch and runs the proofs needing an installed stack or the network. It gets its own dispatch manager and mailbox; the release Lead keeps only the gate into `release/<N>/main` (Release 15, Plans 87 and 89).

## Set up once

1. **Prepare packets.** Start from what exists: bring each plan's `tasks.md` up to date, and ask any earlier manager to push its work, write a handover and stop; its open drafts become packet inputs. Use ready task IDs from **one plan**; ~**three human engineering days** is the outer cap for a brief, not permission to bundle cards (the tighter dispatch rule below applies). An **issue packet** groups issues from the brief's list instead; its fix branches `release/<N>/<topic>` target `release/<N>/main`, per [Release](../../shared/workstreams/release.md). Give each packet the Route of its hardest card, honestly: it sets the session's mode ([ChatGPT session modes](../../shared/run-contract.md#chatgpt-session-modes)). Put them at `releases/<N>/packets/<id>.md` using [the packet template](../../../templates/release/packet.md). Link, never copy, tasks, dependencies and proof; split oversized tasks first. Order the queue by priority; cap Running plus Review at what you can review. A meter, gate or check brief states which realistic ways to get to green it must catch: skips, xfails and deselection through markers, `-k`, `-m`, config or `PYTEST_ADDOPTS`. Fail closed if a registry, baseline or ceiling approves itself or grows, if a PR changes the gate without approval or runs its own gate code, or if results are missing, truncated or show zero tests. Leave crafted bypasses (shadowing the standard library, patching runner internals, packaging or build hooks, deliberately malformed results) and code the candidate runs inside the job to path protection and human review.
**Write each packet to finish in one run** (Release 15, Plans 56, 87, 89, 82: [ledger](../../../docs/ledger/2026-11-24-dispatch-lessons.md)).

- **One contract per packet, aimed at about 3 hours.** Never bundle cards; split a big card at its seams.
- **Rule before dispatch.** Run a local baseline on the plan branch and write into the packet its exact focused selectors, the ids that already fail, the tests that must pass unchanged, and both **May touch** (files and functions) and **Must not touch**; a packet without both is not Ready. See the [packet workstream](../manager/chatgpt-packet.md).
- **Orchestrator-run, never the packet's:** network clones and builds, the UI model or mode selector (the manager confirms it), timings and installed measurements, anything needing a real ComfyUI, GPU, installed build or generated catalog, and the proof itself. The packet ends with `READY-PROOF <repo> <PR> <head> <selectors>`. A cache or speed packet emits its counters (hit, miss, recompute); the lane reads them before trusting a timing and measures the numeric gate on the exact head.
- **A sweep carries its count:** every site found and every site changed, in the PR before review. Audit it against a count you take yourself.

2. **Prepare one queue.** List each packet in `releases/<N>/run.md` with its handoff state, session and next action. A packet is **Ready** only when every PR or packet it depends on has merged into its destination; otherwise **Blocked**, the dependency named in its row. `tasks.md` stays the record of progress.
3. **Own plan-level completion.** For plans assigned through this workstream, record the **Lead as the accountable agent** on its `inputs.md` Run start, with the owner's authorization; there is **no separate plan manager**. You review and land accepted task PRs, keep `tasks.md` current on `main`, and do the plan manager's [Release](../../shared/workstreams/release.md#how-a-release-runs) steps: merging `release/<N>/main` into plan branches, and landing them. Review stops (RS1, R) are yours: commission an independent reviewer, not a packet.
4. **Prepare the boards.** Reuse the release's existing boards, or create them ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)) by their titles; no packet issues, no labels.
5. **Hand off to the owner** with queue and mailbox links, ready/blocked packets, missing authorization and the Orchestrator launch message, filled in from the [run board template](../../../templates/release/run.md#orchestrator-launch-message). The board's startup checks verify access, session creation, resume, the hour and the mailbox; describe any manual steps.

## At each Lead check-in

**Inputs:** your boards since your cursor, including every packet the Orchestrator's STATUS marks Review; open packet PRs; and `python3 scripts/release_branches.py check <N>`.

**Each Review:** accept, merge, open the `tasks.md` progress PR and post DONE; or list the rework on the PR and post a DECISION. Accept a gate only after the reviewer injects the realistic failures in its brief and sees the gate reject them. Judge against that threat model and leave crafted bypasses out of the findings. Route each reviewer by the run contract:

See [routing and bindings](../../shared/run-contract.md#routing-and-bindings) in the run contract.

**Fixes are packet work, however small** (owner, Release 15). Claude sessions and their sub-agents diagnose, review, prove, merge, pin and run CI. They don't write the fix. Put the diagnosis in the rework or a new packet: the failing ids, the cause, the suggested change, and the May touch list. If ChatGPT fails or shows a limit, retry it, or start a fresh session at the branch head. Otherwise wait, because taking the work over costs more than the wait.

**Judge like a light gatekeeper.** Count failures as distinct test ids from complete logs, never as pytest's summary counters, which repeat entries. Reviewers sort findings into BLOCKING, FOLLOW-UP or NOTE; block only on wrong results accepted, data or install damage, a real security or custody hole, or a regression from base. File the rest of a PR's follow-ups as one issue in astrid-dev, marked `backlog` and linked from the PR. A `tasks.md` row is for work the release must do. A regression the candidate introduced is fixed in its packet. A defect that predates it gets an issue and a test that stays executed and visibly failing, and the packet does not fix it. Changing an existing assertion, including turning a gate's limit into an observation, is the owner's call unless she has delegated it. An Orchestrator acting on her direct instructions needs her confirmation in its own chat.

**Keep work moving. Every hop between sessions costs up to an hour.**
- **Rule conditionally.** When a gate needs one more result, rule it with its condition and its next step attached, for example "merge when this run shows no new ids; if one is harm-class, cut a packet". That way nobody comes back to you.
- **Manager cadence.** Managers check every 20 minutes while a packet is Running or in Review, and hourly when idle.
- **Keep managers up.** A ChatGPT manager runs for a window of about two hours, and a board comment can't wake it. Never stand one down while its plan may still need packets. When one goes quiet with work waiting, give the owner the exact text to paste to resume it.

When a packet has waited more than two hours on hosted jobs, read its run list: pull-request CI may run only part of a suite, so dispatch the full run it is waiting for. Every few hours, ask a high-judgment reviewer for a second opinion on bottlenecks, order and scope; bring what exceeds your authority to the owner.

**Before merging:** find every pin change: each needs its own commit and the owner's approval or delegation. A pin names what ships. The VibeComfy that ships is the one the candidate Agent pins, and the Agent is the one the candidate App pins, never a branch head. One lane owns the App repin. It repins when qualification starts, and again only if an upstream moves. After a dependency's PR is squash-merged, re-point its pin to the squash commit. Give a gate at most two review rounds; round two only verifies round one's fixes. Then merge.

**Rulings:** when a ruling will recur, add it to the board's Standing rulings (`releases/<N>/run.md`), so that a fresh Lead, Orchestrator or packet session finds it without reading the mailbox. A ruling that holds beyond the release goes into its skill instead, and the board links it.

**Then:** triage the release's issues ([states](../../../docs/contribution-workflow.md#issues)): an issue a task row or packet cites is `planned`, and one that a branch, pull request or running packet names is `claimed`, whoever started it. Give each uncited issue a row, or move it out. Move unblocked packets to Ready, write the next, copy the Orchestrator's STATUS into the board and refresh Now and Waiting on the owner. No Orchestrator STATUS for 2 hours, or a message of yours missing from its `acted on:` line, is the owner's to hear. Schedule your own check-ins with a scheduler that outlives your machine, re-armed each time; else say which nudge the owner gives.

## Rolling queue

When the work is not known up front (a [release qualifier](../../shared/release-qualification.md) finding failures as it goes), the queue grows as findings arrive and the manager polls it hourly. The finder cuts an **issue packet** from the packet template, with its Repro, only when all hold:
- a failing test or exact repro that a sandbox with no network can target;
- a bounded fix of about 3 hours or less;
- a cause no plan owns.

A failure in a plan's own code goes back to that plan's lane; cross-lane findings go lane to lane. Fixes target `release/<N>/<topic>` → `release/<N>/main`. Anything that needs judgement about acceptability goes to the Lead.

## Standby Lead

When the Lead's own session may stop without warning (a usage allowance, a lost container), the owner can keep a **standby Lead** in another session, on the high-judgment role of the other family.
- **Heartbeat.** The Lead posts its hourly `STATUS` ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)), even when nothing moved, with a marker the standby can recognise (for example its tool's footer).
- **Wait.** The standby checks the mailbox every hour and posts nothing while the newest Lead message is less than 3 hours old.
- **Take over.** After 3 hours of silence, the standby first rules out a quiet Lead: no Lead commit, branch push, pull request or board edit in those 3 hours. Then it posts one takeover message, keeps the same mailbox name, and runs the Lead's check-ins under the same Authority.
- **One Lead.** Once a takeover message exists, the earlier Lead stands down if it returns, and does nothing until the owner hands the role back.

The release keeps the standby's brief and the environment notes beside its run board, under `releases/<N>/lead/`.
