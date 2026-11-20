---
name: astrid-dev
description: One entrypoint for people and agents contributing to Astrid; locate existing work, choose the smallest outcome, prove it and integrate safely.
---

# Contribute to Astrid

**Start here for any Astrid contribution.** For creating art *with* Astrid, use its creative tools instead. You need not understand every repository first: identify the person's goal, then find the existing issue, project and code.

## Choose the right work

| Work | Where it goes |
| --- | --- |
| Bug, small fix, docs or maintenance | [Issue](../../docs/contribution-workflow.md#issues) and focused PR. [Bug fixing](../shared/workstreams/astrid-dev-bugfix/SKILL.md) handles incidents; [Iterate](../shared/workstreams/astrid-dev-iterate/SKILL.md) handles scoped repairs |
| Noticed something, or have a question | [Issues](../../docs/contribution-workflow.md#issues): file it, search first |
| Assigned one bounded task as a worker | [Worker](../roles/astrid-dev-worker/SKILL.md): follow the task card and invoke [Iterate](../shared/workstreams/astrid-dev-iterate/SKILL.md) for code |
| Task in a claimed project | Existing [plan, inputs and tasks](../../docs/project-format.md); inherit accepted decisions and permissions |
| New independent outcome | Check [catalog](../../plans/index.md) and [gaps](../../vision/README.md), then use [Plan](../shared/workstreams/astrid-dev-plan/SKILL.md). A difficult bug still needn't become a project |
| What we're doing now, next and later | [Strategy](../../strategy.md): read it first for release and version direction; see [the hierarchy](../../docs/contribution-workflow.md#review-the-strategy) |
| A gap, or the strategy across several plans | [Gap](../shared/workstreams/astrid-dev-gap/SKILL.md): define or reassess the outcome, write its closure approach and route to closure |
| Planning a new project | [Planner](../shared/workstreams/astrid-dev-plan/SKILL.md): define the accepted scope and tasks |
| Leading release delivery, including setting up a Codex orchestrator to farm tasks out to ChatGPT managers | [Lead](../roles/astrid-dev-lead/SKILL.md): own the overall outcome; select the [multi-manager workstream](../roles/astrid-dev-lead/workstreams/multi-manager-release.md) when applicable |
| Supervising managers or dispatching work sessions | [Orchestrate](../roles/astrid-dev-orchestrate/SKILL.md): keep manager runs and handoffs moving, advise and check in |
| Running one accepted project | [Manage](../roles/astrid-dev-manage/SKILL.md); ask the advisor ([Orchestrate](../roles/astrid-dev-orchestrate/SKILL.md)) for a genuine blocker or consequential choice |
| Someone else's pull request, usually an outside contributor's | [Merge](../shared/workstreams/astrid-dev-merge/SKILL.md): a lead critic and a few cheap helpers review it, then merge it, send it back or bring it to the owner |
| Test results: is a candidate worse than its baseline, or why is a `main` red | [Get to green](../shared/workstreams/astrid-dev-green/SKILL.md): measure completely, then gate on no new failures or retire old red by cause |
| Work that ships in a release: a plan's task or a fix | A release is one branch per repository that its plans and fixes merge into, tested as a whole and published on the owner's go; your pull request goes into a plan or fix branch `release/<NN>/…`: [How a release runs](../shared/workstreams/astrid-dev-release/SKILL.md#how-a-release-runs) |
| Integration, release or publication | [Release](../shared/workstreams/astrid-dev-release/SKILL.md), with explicit current authorization; start at [How a release runs](../shared/workstreams/astrid-dev-release/SKILL.md#how-a-release-runs) |
| Real-GPU proof of generation ("run full GPU validation") | [GPU validate](../shared/workstreams/astrid-dev-gpu-validate/SKILL.md), within the owner's standing budget |
| Changing astrid-dev itself: a rule, term, skill, template, check or generated page | [Improve](../shared/workstreams/astrid-dev-improve/SKILL.md): find the rule's one home, change only that, prove it |

**Skill structure:** [Roles](../shared/workstreams.md) define who is accountable; shared workstreams are independently callable procedures; role-specific workstreams are operating variants. [Shared run rules](../shared/run-contract.md) govern every invocation. Standalone skills retain `astrid-dev-*` names.

## One path, proportionate depth

1. **Orient:** Learn what the contributor wants; consult the [domain map](references/domains.md) for the relevant code and specialists.
2. **Investigate:** Trace actual behavior and prior work before changing it. Search issues and projects; confirm source revision, dependencies and relevant proof.
3. **Decide:** Agree the smallest complete result and test of success. Reuse accepted scope; challenge consequential designs without creating a mandatory second planning ritual.
4. **Build:** Work on the authorized source using [Iterate](../shared/workstreams/astrid-dev-iterate/SKILL.md); protect existing work and respect the current run's constraints.
5. **Prove:** Record proof as the [run contract](../shared/run-contract.md#checks-and-failure-repair) and its [route provenance](../shared/run-contract.md#actual-route-provenance) say. A green wrapper is not product proof.
6. **Land:** Link issue/project and implementation PRs, merged into the plan branch of the release they ship in (a fix goes to its fix branch); use ordinary review and [Release](../shared/workstreams/astrid-dev-release/SKILL.md) for cross-repo integration and separately authorized promotion.

Start at the first stage **not already established by evidence**; a fact-finding task can end after investigation, and a known small fix needn't revisit architectural planning.

## Make contributing easy

If a person has a goal, find the closest issue or existing task first. Otherwise offer 2–3 bounded choices from the [issues](https://github.com/banodoco/astrid-dev/issues) and [project catalog](../../plans/index.md), accounting for time, hardware and interests.

Use the [GitHub contributor guide](../../docs/contribution-workflow.md) to **claim, propose, request a start decision, ask a question, submit multiple product PRs or finish a project**. Claiming is ownership, not authorization. No mandatory project conversation hub is created. The concise completion PR is an index of real evidence, not another database. When astrid-dev itself gets in your way, add an entry file to the add-only [process ledger](../../docs/ledger/README.md).

**Authority:** Follow the [shared run contract](../shared/run-contract.md), [contribution design principles](../../docs/contribution-design-principles.md), and the active product repository's instructions. This skill routes the work; it does not grant execution, integration or release permission. Never install skills or change a contributor's machine merely to orient them.
