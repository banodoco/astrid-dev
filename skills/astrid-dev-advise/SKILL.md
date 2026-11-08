---
name: astrid-dev-advise
description: Answer one bounded question when an Astrid planner, manager or working agent is genuinely blocked, faces conflicting evidence, or must make a consequential judgment; return one concrete next action; also runs owner-requested check-ins on a run. Use only when asked.
---

# Advise on an Astrid blocker

Planners and managers are administrators; this is where their high-judgment work goes. Use it only when a planner, manager or working agent asks, for a genuine blocker, conflicting evidence, or a consequential judgment the accepted plan cannot settle. It is not routine per-task approval. Follow the [run contract](../astrid-dev-shared/run-contract.md), and answer the bounded question you were given.

- **Refresh the facts first:** the exact candidate, source and donor identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a concrete challenge against over-engineering.
- **Require the previously failing check** to run on the repaired candidate.
- **Don't:**
  - waive failures, widen scope, reset counters, add a review stage, or authorize execution or publication;
  - invent model IDs, or claim a run happened without evidence.

## Check-ins (only when the owner asks)

When the owner asks for regular check-ins on a run, take the cadence and end condition from that request and record them as `checkin` in the run's `run.yaml`. Schedule them from your own session, and remove the schedule when the run ends or the owner says stop. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
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
