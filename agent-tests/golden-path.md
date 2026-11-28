# The golden path

The parent rules that [agent tests](README.md) check. Each is written once, in its home; this page only lists them, so a case's Expect lines can cite the document line and the rule it rests on. A behaviour that rests on neither is not an expectation yet: fix the document first, through [improve](../agent/shared/workstreams/improve.md).

They came from three read-only inventories on 28 November 2026, which found about thirty contradictions and gaps, and from the runs recorded in [runs/](runs/).

## Governing thought

**A session takes its authority, its hand-off and its clock from its run's brief, does only what its host can do, and closes what it runs.** Role documents give defaults. The brief says what this run changes. The run contract's safety, proof and permission rules bind everyone.

## The rules

1. **Authority: a brief changes defaults, and says so.** Home: the run contract's [Who answers for a run](../agent/shared/run-contract.md#who-answers-for-a-run).
2. **Hand-off: one start message per edge, and one way back.** Each start message names what the child reads and at which ref, its base SHA, its branch, which kind of worker it is, what it pushes, how it returns and whom it answers to. Home: [start-session](../agent/shared/workstreams/start-session.md#procedure), step 7, and a lane brief's Start messages.
3. **Clock: long-running roles check in; one-shot roles report.** A check-in belongs to the session that set it, which names its end, never sets a second, and cancels it. Liveness is one clock: nudge at 2 hours, act at 3. Home: the run contract's [coordination rules](../agent/shared/run-contract.md#coordination-boards-and-check-ins), items 5, 7 and 8.
4. **Host: what a session can do decides where work runs.** A session that can't build doesn't run proofs, so CI on the PR is the proof. A subagent runs on its creator's machine, so its creator runs its focused tests. Home: start-session step 7 and the brief's Proof.
5. **Progress: whoever merges a task ticks it.** `tasks.md` holds state, changed only when state changes, in one PR at a check-in. Home: the run contract's merge rule and the [whole-project manager](../agent/roles/manager/whole-project.md#progress-is-always-current).
6. **Close: whoever runs it closes it.** A task is closed by its merger, a plan by its accountable agent's completion PR, and a lane by its orchestrator once the Lead has merged each plan into `release/<N>/main`. The release is closed by the Lead. Each `done` needs the level below. Home: [who does what](../docs/lifecycle.md), generated from `scripts/lifecycle.py`, and the `lane-briefs` check.
7. **Reading path: a rule a role needs is on that role's own pages,** or linked from them.
