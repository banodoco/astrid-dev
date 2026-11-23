---
description: Launch and steer one Claude-hosted orchestrator per lane, each running a Codex manager through a carded plan, with the Lead as strategist and gatekeeper rather than dispatcher.
---

# Workstream: lane orchestrators in Claude cloud

## Workstream contract

**Outcome:** Each lane runs end to end in its own session (orchestrator, one manager, workers by card route) and comes to the Lead only at anchor points; the Lead's time goes to strategy, gates and cross-lane links.
**When to use:** When the Lead starts or restarts a lane in Claude cloud, including replacing a lane whose session has drifted (fresh context on the same base).
**Inputs:** A carded plan on astrid-dev `main` (each card with route, scope, dependencies, focused proof), its `Run start` line, the base SHAs, the owner's go, and a session with working Codex.
**Procedure:** The four steps below, then strategy checks.
**Completion:** The plan's cards are ticked in `tasks.md`, its landings confirmed by the Lead, its check-ins cancelled, and the session retired or handed its next plan.

The [Lead responsibilities](../SKILL.md) continue to apply. Lessons from Release 15 (23 November 2026) are the reason for each step; see the [process ledger](../../../../docs/ledger/2026-11-23-lane-launch-lessons.md).

## 1. Card the plan on main first

The orchestrator reads its plan from `main`, so record everything before the launch message: the cards in `tasks.md` sized to the [run contract's routes](../../../shared/run-contract.md#routing-and-bindings) (most cards `N`; `X` only for the one subtle change; `S` only where a wrong call silently accepts a bad result; reviews by the high-judgment role), the test inventory, and the `Run start` line in `inputs.md` naming the session, what it may do without asking, the owner's limits, the advisor and any lane it must coordinate with. Merge that PR before the owner pastes the launch message; an unmerged `Run start` reads as "Pending" and a careful orchestrator stops.

A plan that grows mid-run gets its own plan number rather than cards bolted onto a different plan (Plan 89 split from Plan 75, 23 November 2026).

## 2. Make the session

- **Fresh or reused.** Prefer a fresh session on the same base when a lane has been going round in circles or used about half its context; reuse a session only at a breakpoint (its current work landed). Never hand over mid-card.
- **Create it with a short placeholder prompt** ("You will be the orchestrator for Plan NN. Wait for the owner's launch message"). Never pass shell syntax as the prompt; it is sent literally.
- **Codex.** Codex logins are per container, and usage limits are per account. Before assigning Codex work, the session runs `codex exec --skip-git-repo-check -s read-only 'Reply ok.'` once. A session on an account at its limit runs its cards on Claude subagents by the same routes, or the owner signs it in with another account. Test each session; never infer one session's account from another's.

## 3. The owner pastes the launch message

A message sent from the Lead's session arrives as peer data, not as the owner's go, so the orchestrator rightly refuses outward actions on it. Draft the message for the owner to paste:

```text
You are the orchestrator for Plan <NN>, <one-line outcome>, in Release <N> of Astrid, and you answer for it finishing.

Start here. Attach <repos>. Follow the astrid-dev-orchestrate skill, its lane-orchestrator workstream and its Codex-in-Claude workstream. Your run and its limits are the Run start line in plans/<NN>-<name>/inputs.md on astrid-dev main, and your work is cards <ids> in plans/<NN>-<name>/tasks.md, each with its route, scope and proof.

Host one Codex manager on Terra (route X, effort high) that follows the astrid-dev-manage skill and works through those cards. It dispatches each card on its named route (Luna for N, Terra for X, Sol for S, Astra for reviews), runs only the tests the cards name, and ticks Progress in tasks.md as each card merges. <Checkpoints, e.g. "RN-13: report and start nothing further until the Lead and I decide.">

Check in on the manager every hour with a scheduled task and send the Release <N> Lead (<lead session>) one short report each hour; otherwise follow the lane-orchestrator workstream's rules (anchor points only, decide and record, keep-awake). <Coordination: "X touches the same code as <lane>: agree the order directly with <session>.">

Speed over bureaucracy: keep real correctness and every existing test unchanged, and prove the result <by a real render / an installed measurement> before any hosted CI.

You may, without asking me: run Codex with full access here (Claude subagents if Codex refuses); attach any banodoco repo you need; cut and push release/<N>/plan-<NN> from release/<N>/main; open PRs; merge them once the Release <N> Lead confirms the gate; and dispatch hosted CI when the Lead gives you the slot. Trust the Release <N> Lead on every direction and design decision. Come to me only for publishing a release, anything paid, rented machines, live installs on my machine, or my own media.
```

Ask the owner to do the Codex device sign-in in the session first if the check in step 2 failed.

## 4. The orchestrator's rules live in its own workstream

The lane's side (Codex check, anchor points only, decide and record, hourly reports, proof before CI, direct coordination, keep-awake, merging its own records) is the orchestrate role's [lane workstream](../../astrid-dev-orchestrate/workstreams/lane-orchestrator.md). The launch message points there; send the Lead's rulings as they come, and when a lane asks what it could decide, add the missing rule to that workstream or to its plan once rather than answering again.

## The Lead's check-ins: strategy, not dispatch

Every two to three hours, per lane: is it on the biggest measured win; is anything still unexplained after two tries (send the one cheapest experiment that makes the cause visible); what will block it next (disk, fixture, Codex limit, CI slot, review) and arrange it ahead; is it asking things it could decide (write the rule once); do two lanes share code or a root cause (connect them directly). Pre-decide a lane's "least sure" item in your reply so it does not wait on you.

**Gates.** Confirm a landing only after your own by-id comparison of its hosted unit run against the release baseline (a subagent fetches each job's full log and extracts `FAILED`/`ERROR` ids; record the comparison under `releases/<N>/evidence/`), with each new id either in a recorded moving group or ruled with evidence (base and head run locally, or the source unchanged). Two Agent CI runs may run in parallel; after a landing whose tree equals the gated head, cancel the push-triggered runs on the release branch.

**Speed findings** go in [docs/speed.md](../../../../docs/speed.md) through the lanes' evidence PRs.
