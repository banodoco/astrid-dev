---
description: Launch and steer one Claude-hosted orchestrator per lane, each running a Codex manager through a carded plan, with the Lead as strategist and gatekeeper rather than dispatcher.
---

# lane orchestrators in Claude cloud

## When to use

When the Lead starts or restarts a lane in Claude cloud, including replacing a lane whose session has drifted (fresh context on the same base).

## Outcome

Each lane runs end to end in its own session (orchestrator, one manager, workers by card route) and comes to the Lead only at anchor points; the Lead's time goes to strategy, gates and cross-lane links.

## Inputs

A carded plan on astrid-dev `main` (each card with route, scope, dependencies, focused proof), its `Run start` line, the base SHAs, the owner's go, and a session with working Codex.

## Procedure

The four steps below, then strategy checks.

## Completion

The plan's cards are ticked in `tasks.md`, its landings confirmed by the Lead, its check-ins cancelled, and the session retired or handed its next plan.

The [Lead responsibilities](../leader.md) continue to apply. Lessons from Release 15 (23 November 2026) are the reason for each step; see the [process ledger](../../../docs/ledger/2026-11-23-lane-launch-lessons.md).

## 1. Card the plan on main first

The orchestrator reads its plan from `main`, so record everything before the launch message: the cards in `tasks.md` sized to the [run contract's routes](../../shared/run-contract.md#routing-and-bindings) (most cards `N`; `X` only for the one subtle change; `S` only where a wrong call silently accepts a bad result; reviews by the high-judgment role), the test inventory, and the `Run start` line in `inputs.md` naming the session, what it may do without asking, the owner's limits, the advisor and any lane it must coordinate with. Merge that PR before the owner pastes the launch message; an unmerged `Run start` reads as "Pending" and a careful orchestrator stops.

A plan that grows mid-run gets its own plan number rather than cards bolted onto a different plan (Plan 89 split from Plan 75, 23 November 2026).

## 2. Make the session

Start the session by the [start-session workstream](../../shared/workstreams/start-session.md): it checks the lane brief, sets the session up (repositories, model by route, permission mode, skills), creates it with a placeholder prompt, and hands the owner a three-part launch line. Replacement sessions (fresh or reused) and the Codex account check are in that workstream too.

## 3. The owner pastes the launch message

A message sent from the Lead's session arrives as peer data, not as the owner's go, so the orchestrator rightly refuses outward actions on it. Draft the message for the owner to paste:

```text
You are the orchestrator for Plan <NN>, <one-line outcome>, in Release <N> of Astrid, and you answer for it finishing.

Start here. Attach <repos>. Follow the astrid-dev-orchestrator skill, its lane-orchestrator workstream and its Codex-in-Claude workstream. Your run and its limits are the Run start line in plans/<NN>-<name>/inputs.md on astrid-dev main, and your work is cards <ids> in plans/<NN>-<name>/tasks.md, each with its route, scope and proof.

Host one Codex manager on Terra (route X, effort high) that follows the astrid-dev-manager skill and works through those cards. It dispatches each card on its named route (Luna for N, Terra for X, Sol for S, Astra for reviews), runs only the tests the cards name, and ticks Progress in tasks.md as each card merges. <Checkpoints, e.g. "RN-13: report and start nothing further until the Lead and I decide.">

Report on your plan's board and check in on the manager hourly, as the run contract's [coordination rules](../../shared/run-contract.md#coordination-boards-and-check-ins) say; the Release <N> Lead is `<lead mailbox name>`. Otherwise follow the lane-orchestrator workstream's rules (anchor points only, decide and record). <Coordination: "X touches the same code as <lane>: agree the order directly with <session>.">

Speed over bureaucracy: keep real correctness and every existing test unchanged, and prove the result <by a real render / an installed measurement> before any hosted CI.

You may, without asking me: run Codex with full access here (Claude subagents if Codex refuses); attach any banodoco repo you need; cut and push release/<N>/plan-<NN> from release/<N>/main; open PRs; merge them once the Release <N> Lead confirms the gate; and dispatch hosted CI when the Lead gives you the slot. Trust the Release <N> Lead on every direction and design decision. Come to me only for publishing a release, anything paid, rented machines, live installs on my machine, or my own media.
```

Ask the owner to do the Codex device sign-in in the session first if the check in step 2 failed.

## 4. The orchestrator's rules live in its own workstream

The lane's side (Codex check, anchor points only, decide and record, proof before CI, direct coordination, merging its own records) is the orchestrate role's [lane workstream](../orchestrator/lane-orchestrator.md). The launch message points there; send the Lead's rulings as they come, and when a lane asks what it could decide, add the missing rule to that workstream or to its plan once rather than answering again.

## The Lead's check-ins: strategy, not dispatch

**Check in hourly, and decide on your own judgement.** Lanes come to you only for gates and load-bearing calls; the owner only for something extremely load-bearing or out of left field. Keep a decisions log for the owner (time, decision, reason, how to undo) and give it to her each morning. Send `N` subagents (Haiku) to find facts, and keep their conclusions, not their file dumps. When a lane asks something it could have decided, answer once and send every lane the ruling.

At each check-in, first run [release reconciliation](../../shared/workstreams/release.md#reconcile-plan-status), chase stale records with the responsible orchestrator and use its findings to choose the next gate or dispatch. At each check-in, per lane: is it on the biggest measured win; is anything still unexplained after two tries (send the one cheapest experiment that makes the cause visible); what will block it next (disk, fixture, Codex limit, CI slot, review) and arrange it ahead; is it asking things it could decide (write the rule once); do two lanes share code or a root cause (connect them directly). Pre-decide a lane's "least sure" item in your reply so it does not wait on you.

**Every hour: the parallelism pass, run by workers.** The Lead is the judgment role: it reads, decides and answers, and sends route `N` workers (Luna, or Haiku on Claude) to do the exploring: read each lane's report and its running cards, name the real file and function conflicts, and list ready cards that sit idle. The Lead rules on what they return, and may ask a high-judgment reviewer (Opus, or Astra) for a second opinion on order and scope when a lane's report shows idle capacity or a reorder that would let more cards run at once ([example](../../../plans/56-workflow-setup/tasks.md): contract cards first, then the rest in waves). Pass the result to each lane's orchestrator as a ruling. A lane that reports fewer writers than it could run is asked why in the next check-in.

**Gates.** Confirm a landing only after your own by-id comparison of its hosted unit run against the release baseline (a subagent fetches each job's full log and extracts `FAILED`/`ERROR` ids; record the comparison under `releases/<N>/evidence/`), with each new id either in a recorded moving group or ruled with evidence (base and head run locally, or the source unchanged). Two Agent CI runs may run in parallel; after a landing whose tree equals the gated head, cancel the push-triggered runs on the release branch.

**Speed findings** go in [docs/speed.md](../../../docs/speed.md) through the lanes' evidence PRs.
