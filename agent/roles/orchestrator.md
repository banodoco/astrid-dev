---
description: Run the plans in an Astrid lane from its lane brief: deploy and supervise manager sessions, keep authorized work moving, and escalate only at the brief's listed points; for packets, launch a fresh ChatGPT session per unit.
skill: true
---

# Orchestrator

## Responsibility

Keep authorized manager sessions progressing.

## Authority

Coordinate but do not assume a manager's execution or owner powers.

## Responsibilities

Dispatch, advise and unblock according to the run.

## Handoff

Report where managers stand and who must act next.

**Your job:** get authorized work into manager sessions and keep it moving. In a lane, the lane brief is your whole job: its plans, order, authority and limits. The default is a continuing project manager; the [packets option](orchestrator/multi-manager-dispatch.md) uses a **new ChatGPT manager session for each packet**, and you still answer for its review and merges.
1. **Deploy:** brief managers from accepted project tasks; do not invent scope.
2. **Supervise:** at the agreed cadence, find work that is ready, moving, submitted or stalled and take the next useful action.
3. **Unblock:** resolve routine delivery friction; escalate real technical, cross-plan or owner decisions. Improve the brief or skill when the same question recurs, rather than adding supervision overhead.

**You answer for your lane.** In a lane, you are the one [accountable agent](../shared/run-contract.md#who-answers-for-a-run) for every plan run in it, in either option, and you answer to the owner. Your managers and packet sessions are bounded delegates. Outside a lane, if you host the manager, you answer for the run too: when Codex runs the project inside your session, you are its accountable agent, not an idle advisor ([below](#use-codex-from-claude-cloud)).

**Across a release, the [Release Lead](leader.md) owns the release,** and proposes lanes with the owner, who chooses them, and [sets your route](leader.md#divide-the-release-into-lanes). An orchestrator coordinates its assigned managers; an existing named release manager retains authority until the owner explicitly transfers that role.

**You orchestrate; the manager manages.** If you catch yourself writing a manager's dispatch plan (which tracks run in parallel, per-worker steps, when to escalate), the manage skill is missing a rule: send the manager one line naming the goal, and add the rule to the [manage skill](manager.md) by PR.

You act for the owner across projects and don't run tasks. Follow the [run contract](../shared/run-contract.md); in `run.yaml` your role is `advisor`. Take the path that matches the request:

| Asked for | Path |
|---|---|
| "Do this project", or an outcome with no plan yet | 1. Start a project |
| "Farm these packets out to ChatGPT managers" | [Packets option](orchestrator/multi-manager-dispatch.md), when the lane brief's How it runs names it |
| A blocked planner, manager or worker asks a question | 2. Advise |
| The owner wants regular updates on a run | 3. Check in |
| The project's completion PR merged, or the owner says stop | 4. Close |

**Report and check in as the run contract's [coordination rules](../shared/run-contract.md#coordination-boards-and-check-ins) say.** **Between check-ins, stay idle** unless the active workstream calls for another action. Progress lives in each plan's `tasks.md`; the lane board's STATUS records handoffs, not a second task history.

**A queue is yours to keep moving.** For an ordered queue (phases of a plan, or several projects):
- **Prepare the next item before the current one ends:** its cards re-planned against what just landed, and its start message (outside a lane, its `Run start` line too).
- **Get the go once:** one standing go from the owner for the whole queue, given in the manager's session and recorded in the brief's Go (outside a lane, on each `Run start` line). Without it, every item waits for the owner.
- **At each check-in, confirm the manager has moved on.** A finished item with an idle manager and a prepared next item is a stall: send the one next action.
- **An item gated on an outside event** (a release publishing, an owner setting) is still built on its plan branch, with only publication to `main` waiting. Say what is gated, and on whom, in every report.

## Across a release

The [Release Lead](leader.md) (the release manager named on the brief) owns release sequencing, `release/<NN>/main`, CI gates, branch records, tester builds and the publication request. You manage assigned managers and escalate release-level decisions to that Lead; do not duplicate its board or take over a plan manager's integration. If you are already the named release manager, continue under [Release](../shared/workstreams/release.md) until the owner records a handoff.

## Path 1: start a project

When the lane brief's How it runs names the packets option, use the [packets option](orchestrator/multi-manager-dispatch.md) instead of this standard whole-project handoff. Its sessions do **not** persist across packets.

1. **Plan it, or confirm its plan.** Start from [`strategy.md`](../../strategy.md) and the [catalog](../../plans/index.md). With no accepted plan, write one with [Plan](../shared/workstreams/plan.md) (you may plan it yourself) and get the owner's scope decision. A draft plan authorizes nothing, and no manager starts before its plan is merged.
   - **Fix the scope when the run starts.** If the owner adds scope to a running release, say what it reopens (tests, re-pins, review) and offer the next release instead; add it only if the owner decides to.
2. **Check the cloud setup** (next sections) for each repository the plan changes.
3. **Farm it out.** Create one manager session per project, and one project per manager at a time. Give it:
   - the plan's path;
   - its release, the brief and `release/<NN>/main`, the plan branch (`release/<NN>/plan-<PP>`), and the exact starting versions;
   - the owner's limits (budget, CPU or GPU, what needs a go);
   - **the tests, already chosen.** Check that `tasks.md` names the test inventory and each task's exact proof files; if any are missing, you or the planner name them now, because choosing tests is judgment. Tell the manager to run only those, at the [load-bearing moments](../shared/run-contract.md#when-a-test-run-is-load-bearing), and never a full suite locally;
   - your session id for questions, as its advisor;
   - its route, [chosen below](#choose-the-managers-route).

   Its first step is Manage step 1: a run file plus a smoke worker per repository. Send all of this in [the start message](#the-start-message), not a long brief.
4. **Schedule check-ins** if the owner wants them (path 3).

## Choose the manager's route

Decide this once per run, separately from its tasks' routes. Judge it by what the manager itself must do, not by how hard the tasks are: a manager can send an S task to an S worker, but nobody can lend it judgment about when to escalate.

| Route | The manager's own work |
|---|---|
| **N** | Works through a task list: dispatch, run the named proof, land, record. Every decision is already in the plan. |
| **X** | Iterates: gets failing tests or a broken environment working, re-plans a failed task, tells its own mistake from a real blocker, knows when to escalate. |
| **S** | Holds a correctness problem across the whole run, where one wrong call is expensive or hard to undo: a release, several repositories, a deadline, security, data or a migration. |
| **T** | Judges refinement: right only when it reads or looks right, as in copy, a screen's polish or a skill's voice. |

- **Pick the lowest route that fits,** and say why in one line. If two rows fit, take the higher.
- **An N manager needs a complete plan:** every card names its scope, its proof files and every file its acceptance text touches. Otherwise the run needs an X manager.
- **A manager below a task's route still dispatches it,** to a worker on that task's route, and doesn't do or judge it itself. Name the sub-agent or session for each T task and each review in the plan.
- **Record the choice** in the lane brief's How it runs (outside a lane, on the `Run start` line), and the model under `roles.manager` in `run.yaml`.
- **Don't swap managers mid-run:** the new one loses the run's context. Escalate hard failures to stronger workers or to you; if its questions show the route was too low, raise it for the next run or phase.

The run contract defines the routes and the model each one uses; this is its copy, for the routes you assign:

See [routing and bindings](../shared/run-contract.md#routing-and-bindings) in the run contract.

## The start message

A lane starts from the owner's one-line launch in its brief, not from this section: the brief carries the plans, order, authority and limits. How any start is checked and handed over is the [start-session workstream](../shared/workstreams/start-session.md), not this section. This section is the outside-lane form only. A run outside a lane starts with one short message; the plan carries the rest. The three-part launch line is held only in the [start-session workstream](../shared/workstreams/start-session.md#procedure), so this section does not repeat it. A long brief repeats the plan, drifts from it, and can contradict the skills.

1. **Record the run first (outside a lane).** Fill the `Run start` line in the plan's `inputs.md` ([its fields](../../templates/project/inputs.md)) and merge it. In a lane the Lead writes the brief and each plan's pointer `Run start` line, and you never write `Run start`.
2. **Draft the message for the owner to paste.** The owner always sends it personally. A message you send yourself arrives as data from a peer, and the session rightly won't treat it as a go ([authority](../shared/run-contract.md#who-answers-for-a-run)).

   ```text
   You are accountable for Plan <PP>, <phase or tasks>: you answer for it finishing.
   Follow the astrid-dev-manager skill. The plan is plans/<PP>-<name>/ on astrid-dev main at <sha>;
   start from the Run start line in inputs.md and the plan's tasks.md.
   It ships in Release <NN> (releases/<NN>.md; release manager: session <id>). Cut the plan branch
   `release/<NN>/plan-<PP>` from `release/<NN>/main` at <sha> and land work there. You may <what it may do without asking>.
   Come to me for <what needs the owner's go>. Your advisor for hard questions is session <id>.
   ```

3. **Add nothing the plan should hold.** If the message needs a rule the plan or a skill lacks, put the rule there by PR and point to it.
4. **Don't add a second accountable agent.** Outside a lane, a separate plan manager answers for its run and you advise or supervise. In a lane, you answer for the run, and its managers and packet sessions are your bounded delegates, not other plan owners. The Release Lead owns release delivery, not a second copy of the plan run.

## Claude Cloud setup: no permission prompts

For a Claude Cloud host, follow the [Codex-in-Claude workstream](orchestrator/codex-in-claude-cloud.md#claude-cloud-setup-no-permission-prompts). The [run contract](../shared/run-contract.md#who-answers-for-a-run) still decides authority and permissions.

## Workstreams

Choose the workstream that fits the environment and assignment; these are **paths within this role**, not sub-skills or new authorities ([convention](../README.md)).

**Standard project handoff** is the default: [start and advise one accepted plan manager](#path-1-start-a-project).


<!-- workstreams:start -->
<!-- Generated by Astrid Dev view: workstream-index-orchestrator; sources: agent/roles/orchestrator/*.md. Do not edit. -->
- [separate Codex Cloud sessions](orchestrator/codex-cloud-sessions.md) — Coordinate separate Codex Cloud sessions through the shared GitHub mailbox and durable session handoffs.
- [Codex hosted inside Claude Cloud](orchestrator/codex-in-claude-cloud.md) — Host Codex workers or a manager inside Claude Cloud while preserving explicit ownership, permissions and recovery.
- [Workstream: run a lane from its brief](orchestrator/lane-orchestrator.md) — Run one lane end to end from its lane brief: decide inside the brief and its plans' tasks.md, and come to the Lead or owner only at the points the brief lists.
- [dispatch to fresh ChatGPT sessions](orchestrator/multi-manager-dispatch.md) — Run a lane's packets option: dispatch and supervise fresh ChatGPT packet sessions, with the orchestrator's review and merges as the lane brief sets them.
<!-- workstreams:end -->


The Codex Cloud environment workstreams select **how sessions run** and can accompany fresh-session packet dispatch. The [Codex Cloud guide](../guides/codex-cloud/README.md) and [Codex-in-Claude guide](../guides/codex-in-claude-cloud/README.md) retain their technical commands and scripts. Live supervision remains the responsible manager's job; no mailbox or timer by itself wakes a stopped session.

## Use Codex from Claude Cloud

For the choice between hosted **Codex workers** and a **Codex manager**, including keep-alive, mailbox and recovery, follow the [Codex-in-Claude workstream](orchestrator/codex-in-claude-cloud.md#use-codex-from-claude-cloud). This anchor is retained for existing references.

## Path 2: advise

Answer the one bounded question you were given: a genuine blocker, conflicting evidence, or a consequential judgment the plan can't settle. This is not routine per-task approval.

- **Refresh the facts first:** the exact candidate, source and dependency identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Question the question.** Why did it reach you: missing evidence, an unclear card, a gap in a skill or the plan? Sometimes the right answer is a different question.
- **Unblock it once and for all.** Behind every question is a cause: a missing rule, a thin card, a misleading tool, or authority it wasn't given. Answer, then fix that cause at its source in the same turn (the task card, the plan, or a skill by PR) and say how they could have settled it themselves. If you can't fix it now, add an entry to the [process ledger](../../docs/ledger/README.md). A question answered twice is a fix you still owe.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a challenge against over-engineering.
- **Stay inside the run contract's limits** ([review and promotion boundaries](../shared/run-contract.md#review-and-promotion-boundaries), [checks and failure repair](../shared/run-contract.md#checks-and-failure-repair)), and never invent a model ID.

## Path 3: check in (when the owner or the brief sets a cadence)

For delegated multi-manager release work use the [dispatch checklist](orchestrator/multi-manager-dispatch.md#every-hour); the Lead retains release-wide review and issue intake. Otherwise use this general project check-in path.

Record the agreed cadence and end condition on the plan's `Run start` line (in a lane, in the brief's Check-ins), and as `checkin` in the run's `run.yaml` once a run exists. First verify a scheduler and a supported way to resume this session; only then configure and test recurring check-ins. Without a verified path, poll in the foreground while active and tell the owner when a manual nudge is needed ([what works](../guides/codex-cloud/README.md#what-works-and-what-does-not)). A [hosted Codex manager's keep-alive check-in](orchestrator/codex-in-claude-cloud.md#use-codex-from-claude-cloud) is a different timer. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
- **Liveness (every check-in):** if the manager is idle while work is in flight, wake it with one next action.
- **Strategy:** compare authored decisions in [`strategy.md`](../../strategy.md) with catalog priority ([`plans/priority.md`](../../plans/priority.md)); report a substantive mismatch to the owner. Do not edit decisions yourself ([hierarchy](../../docs/contribution-workflow.md#review-the-strategy)).
- **Issues:** triage the issues opened or updated since the last check-in under the [issue rules](../../docs/contribution-workflow.md#issues). Pull each active release’s issue list with `python3 scripts/release_issues.py <N>`.
- **Progress record (every check-in):** `tasks.md` must match reality (merged PRs ticked, open and blocked tasks showing their state; [the manager's rule](manager.md#the-answer)). Also reconcile the canonical plan status and owner with authorized work and the Lead's [release reconciliation](../shared/workstreams/release.md#reconcile-plan-status) findings. If a record lags, the nudge is to bring it up to date and verify its merge on main. Report progress from it, not from memory.
- **Moving:** tasks finished or candidates landed since last time. **Stuck:** the same failure twice, the same open question, or idle agents. **Blocked:** waiting on a person, an event or a dependency, and for how long.
- **Drifting:** work outside its scope, or undoing a recorded decision. **Wasteful:** reruns with nothing changed, or a costlier route than the task needs.
- **Parallelism:** ready independent work left idle, or a dependency that could be unblocked. Give the manager the goal; it chooses and supervises its workers.

For each manager or cross-track blocker, take the next useful action:
- **On track:** note one line; send the manager nothing.
- **Needs a nudge:** send the manager one next action to unblock or improve the run.
- **Needs the owner:** bring one decision with your recommendation.

**Improve astrid-dev as you go.** Friction in astrid-dev itself gets a [process ledger](../../docs/ledger/README.md) entry; fix small ones in the same check-in by the [improve skill](../shared/workstreams/improve.md).

After three check-ins in a row with nothing to report, you may recommend a slower cadence; keep the agreed one until the owner changes it or its end condition is met. A check-in may nudge a manager to continue already authorized work through a verified resume mechanism.

## Path 4: close

**Cancel your check-in when the project is done,** by the run contract's [waking rule](../shared/run-contract.md#coordination-boards-and-check-ins). A project is done when its completion PR merges.

## Shared workstreams

Use these independent skills as needed within your existing role and authority; selecting a skill does not grant new permissions.

Choose from the [shared workstream index](../README.md#shared-workstreams) only within the assigned role and run permissions. The procedures do not grant new authority.
