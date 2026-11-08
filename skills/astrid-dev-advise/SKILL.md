---
name: astrid-dev-advise
description: Answer one bounded question when an Astrid planner, manager or working agent is genuinely blocked, faces conflicting evidence, or must make a consequential judgment; return one concrete next action; also runs owner-requested check-ins on a run. Use only when asked.
---

# Advise on an Astrid blocker

Planners and managers are administrators; this is where their high-judgment work goes. Use it only when a planner, manager or working agent asks, for a genuine blocker, conflicting evidence, or a consequential judgment the accepted plan cannot settle. It is not routine per-task approval. Follow the [run contract](../astrid-dev-shared/run-contract.md), and answer the bounded question you were given.

**Between questions and check-ins, stay idle.** Don't follow the run, answer progress updates or relay them to the owner. Progress lives in the plan's `tasks.md`, and the next check-in reads it there.

- **Refresh the facts first:** the exact candidate, source and donor identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Question the question.** Ask why it reached you: missing evidence, an unclear task card, or a gap in a skill or the plan. Sometimes the right answer is a different question.
- **Leave the asker better equipped.** Say how they could have settled it themselves (which file, check or evidence), and fix that gap at its source: the task card, the plan, or a skill (through a PR). If you can't fix it now, add it to the [process ledger](../../docs/process-ledger.md). The aim is to be asked less over time.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a concrete challenge against over-engineering.
- **Require the previously failing check** to run on the repaired candidate.
- **Don't:**
  - waive failures, widen scope, reset counters, add a review stage, or authorize execution or publication;
  - invent model IDs, or claim a run happened without evidence.

## Check-ins (only when the owner asks)

When the owner asks for regular check-ins on a run, take the cadence and end condition from that request and record them as `checkin` in the run's `run.yaml`. Schedule them from your own session. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
- **Progress record (every check-in):** check that the plan's `tasks.md` matches reality. Merged PRs should be ticked, and open and blocked tasks should show their state. If it lags, the nudge is to bring it up to date. Report progress from it, not from memory.
- **Moving:** tasks finished or candidates landed since last time.
- **Stuck:** the same failure twice, the same open question, or idle agents.
- **Blocked:** waiting on a person, an event or a dependency, and for how long.
- **Drifting:** work outside its scope, or something undoing a recorded decision.
- **Wasteful:** reruns with nothing changed, or a costlier route than the task needs.

Then do exactly one thing:
- **On track:** note one line; send the manager nothing.
- **Needs a nudge:** send the manager one next action to unblock or improve the run.
- **Needs the owner:** bring one decision with your recommendation.

**Improve astrid-dev as you go.** When the run hits friction in astrid-dev itself (an unclear skill, a missing template field, a slow check), add a row to the [process ledger](../../docs/process-ledger.md). If the fix is small and touches only astrid-dev docs or skills, open the fixing PR in the same check-in and add a `fix` row pointing to it. Friction specific to this one run goes in its [decisions ledger](../astrid-dev-shared/templates/decisions-ledger.md) instead.

After three check-ins in a row with nothing to report, tell the owner, then slow down or stop. A check-in never starts, resumes or authorizes work.

**Cancel them when the project is done.** When the project is complete, cancel every check-in you scheduled. Do the same when its end condition is met or the owner says stop. A project is complete when its completion PR merges. Confirm none remain, and tell the owner they have stopped.
