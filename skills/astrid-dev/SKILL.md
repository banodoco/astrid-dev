---
name: astrid-dev
description: One entrypoint for people and agents contributing to Astrid; locate existing work, choose the smallest outcome, prove it and integrate safely.
---

# Contribute to Astrid

**Start here for any Astrid contribution.** For creating art *with* Astrid, use its creative tools instead. You need not understand every repository first: identify the person's goal, then find the existing issue, project and code.

## Choose the right work

| Work | Where it goes |
| --- | --- |
| Bug, small fix, docs or maintenance | [Issue](https://github.com/banodoco/astrid-dev/issues) and focused PR. [Bug fixing](../astrid-dev-bugfix/SKILL.md) handles incidents; [Iterate](../astrid-dev-iterate/SKILL.md) handles scoped repairs |
| Task in a claimed project | Existing [plan, inputs and tasks](../../docs/project-format.md); inherit accepted decisions and permissions |
| New independent outcome | Check [catalog](../../plans/index.md) and [gaps](../../vision/README.md), then use [Plan](../astrid-dev-plan/SKILL.md). A difficult bug still needn't become a project |
| What we're doing now, next and later | [Strategy](../../strategy.md): read it first; the order across gaps and why |
| A gap, or the strategy across several plans | [Gap](../astrid-dev-gap/SKILL.md): define or reassess the outcome, write its closure approach and route to closure |
| Handing off a project, or overseeing several | [Orchestrate](../astrid-dev-orchestrate/SKILL.md): plan it, farm it out to a manager set up for cloud sessions, advise and check in |
| Running one accepted project | [Manage](../astrid-dev-manage/SKILL.md); ask the advisor ([Orchestrate](../astrid-dev-orchestrate/SKILL.md)) for a genuine blocker or consequential choice |
| Someone else's pull request, usually an outside contributor's | [Merge](../astrid-dev-merge/SKILL.md): a lead critic and a few cheap helpers review it, then merge it, send it back or bring it to the owner |
| Integration, release or publication | [Release](../astrid-dev-release/SKILL.md), with explicit current authorization |
| Real-GPU proof of generation ("run full GPU validation") | [GPU validate](../astrid-dev-gpu-validate/SKILL.md), within the owner's standing budget |
| Changing astrid-dev itself: a rule, term, skill, template, check or generated page | [Improve](../astrid-dev-improve/SKILL.md): find the rule's one home, change only that, prove it |

## One path, proportionate depth

1. **Orient:** Learn what the contributor wants; consult the [domain map](references/domains.md) for the relevant code and specialists.
2. **Investigate:** Trace actual behavior and prior work before changing it. Search issues and projects; confirm source revision, dependencies and relevant proof.
3. **Decide:** Agree the smallest complete result and test of success. Reuse accepted scope; challenge consequential designs without creating a mandatory second planning ritual.
4. **Build:** Work on the authorized source using [Iterate](../astrid-dev-iterate/SKILL.md); protect existing work and respect the current run's constraints.
5. **Prove:** Record proof as the [run contract](../astrid-dev-shared/run-contract.md#checks-and-failure-repair) and its [route provenance](../astrid-dev-shared/run-contract.md#actual-route-provenance) say. A green wrapper is not product proof.
6. **Land:** Link issue/project and implementation PRs; use ordinary review and [Release](../astrid-dev-release/SKILL.md) for cross-repo integration and separately authorized promotion.

Start at the first stage **not already established by evidence**; a fact-finding task can end after investigation, and a known small fix needn't revisit architectural planning.

## Make contributing easy

If a person has a goal, find the closest issue or existing task first. Otherwise offer 2–3 bounded choices from the [issues](https://github.com/banodoco/astrid-dev/issues) and [project catalog](../../plans/index.md), accounting for time, hardware and interests.

Use the [GitHub contributor guide](../../docs/contribution-workflow.md) to **claim, propose, request a start decision, ask a question, submit multiple product PRs or finish a project**. Claiming is ownership, not authorization. No mandatory project conversation hub is created. The concise completion PR is an index of real evidence, not another database. When astrid-dev itself gets in your way, add an entry file to the add-only [process ledger](../../docs/ledger/README.md).

**Authority:** Follow the [shared run contract](../astrid-dev-shared/run-contract.md), [contribution design principles](../../docs/contribution-design-principles.md), and the active product repository's instructions. This skill routes the work; it does not grant execution, integration or release permission. Never install skills or change a contributor's machine merely to orient them.
