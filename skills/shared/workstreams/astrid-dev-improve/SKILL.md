---
name: astrid-dev-improve
description: Change astrid-dev itself, whether a rule, term, skill, template, check or generated page: start from a recorded failure, change the one home, prove it and record the fix.
---

# Improve astrid-dev

## Workstream contract

**Outcome:** A demonstrated Astrid Dev process or documentation failure corrected at its canonical source with regression proof.
**When to use:** When changing an Astrid Dev rule, term, skill, template, check or generated document.
**Inputs:** The recorded failure or need, one authoritative source, neighboring references, existing tests and permission to change the machinery.
**Procedure:** Identify the owning source, make the smallest coherent change, run the relevant checks and record the fix without duplicating policy.
**Completion:** Documentation and generated views remain consistent, original regressions are covered and the change's proof is recorded.

Enter through [astrid-dev](../../../astrid-dev/SKILL.md). Words follow the [glossary](../../glossary.md).

## Where things go

| Kind of thing | Its one home | Enforced by |
| --- | --- | --- |
| A run rule: [routes and families](../../run-contract.md#routing-and-bindings); [taste tasks](../../run-contract.md#who-answers-for-a-run); [stopping thresholds](../../run-contract.md#cheapest-model-first); [authority, Run start, merges of progress PRs](../../run-contract.md#who-answers-for-a-run); [commits only, credentials, rented machines](../../run-contract.md#scope-source-identity-and-state); [no test edited to pass](../../run-contract.md#checks-and-failure-repair); [merge-case test scope, check before commit](../../run-contract.md#when-a-test-run-is-load-bearing); [blocking findings, review rounds](../../run-contract.md#review-and-promotion-boundaries) | [run contract](../../run-contract.md) | judgment |
| A role's own steps and selected workstreams: a [Release Lead](../../../roles/astrid-dev-lead/SKILL.md) and its [multi-manager workstream](../../../roles/astrid-dev-lead/workstreams/multi-manager-release.md); a manager's [progress](../../../roles/astrid-dev-manage/SKILL.md#the-answer), [plan branch and worker cards](../../../roles/astrid-dev-manage/SKILL.md#steps) (including `AskUserQuestion`); an orchestrator's [workstreams](../../../roles/astrid-dev-orchestrate/SKILL.md#workstreams) and [closing](../../../roles/astrid-dev-orchestrate/SKILL.md#path-4-close) | that role's skill and `workstreams/` | judgment |
| Running Codex from a Claude session: workers are the default; a Codex manager's check-in | [Codex-in-Claude workstream](../../../roles/astrid-dev-orchestrate/workstreams/codex-in-claude-cloud.md#use-codex-from-claude-cloud) | judgment |
| Reading CI results, getting them complete, using GitHub Actions for tests | [green skill](../astrid-dev-green/SKILL.md) | judgment |
| Installing skills for Codex | the guide for that environment: [Claude cloud](../../../roles/astrid-dev-orchestrate/workstreams/codex-in-claude-cloud/README.md) or [Codex cloud](../../../roles/astrid-dev-orchestrate/workstreams/codex-cloud/README.md) | judgment |
| Vision wording: an element, an goal, its lists | [contribution workflow](../../../../docs/contribution-workflow.md#write-or-improve-documentation) | `subjects`, owner review |
| Release rationale, scope and contributions | the [release brief](../../../../releases/TEMPLATE.md) | `release-documents` |
| Version and major-version decisions, with generated release material | [strategy](../../../../strategy.md); [hierarchy](../../../../docs/contribution-workflow.md#review-the-strategy) | `strategy-consistency`, `generated-views` |
| A term | [glossary](../../glossary.md) | judgment |
| A record of decisions | the glossary names three: a manager's [decision log](../../../roles/astrid-dev-manage/SKILL.md#decide), the [decisions ledger](../../run-contract.md#decisions-ledger-when-the-owner-is-unavailable), `inputs.md` Owner decisions | judgment |
| A pack's shape; what a card holds | the [plan](../../../../templates/project/plan.md), [inputs](../../../../templates/project/inputs.md) and [tasks](../../../../templates/project/tasks.md) templates | `pack-shape` |
| A project fact: name, goal, status, owner, estimate, waiting | the six lines of its `plan.md` | `plan-catalog` |
| Priority | [`plans/priority.md`](../../../../plans/priority.md) | `plan-catalog` |
| Claiming, proposing or finishing a project | the [contribution workflow](../../../../docs/contribution-workflow.md#claim-a-project) | the claim bot, `completion-assessment` |
| A check | `scripts/checks.py`; how: [extending guide](../../../../docs/extending.md#add-a-check) | its tests, `list` |
| A generated page | `scripts/views.py`; how: [extending guide](../../../../docs/extending.md#add-a-generated-view) | `generated-views` |
| Who owns a project; who merges; accountability, not permission | principle 5 in the [principles](../../../../docs/contribution-design-principles.md#the-principles); the [glossary](../../glossary.md)'s project owner | `catalog-paths`, judgment |
| A principle | the [principles](../../../../docs/contribution-design-principles.md#the-principles) | judgment |
| A question, bug, observation or idea about Astrid | the [Issues section](../../../../docs/contribution-workflow.md#issues) and each type's [form](../../../../.github/ISSUE_TEMPLATE) | GitHub's forms, judgment |
| Friction | the [process ledger](../../../../docs/ledger/README.md) | `ledger` |

## Steps

1. Start from a recorded failure: a process ledger entry, an issue or an accepted card. No failure, no change.
2. Find the home in the table. Change it and nothing else; replace any copy with a link to the home's heading.
3. If you add words, cut as many.
4. Change what a check accepts, or add a check, in a separate, announced change: list every pinned test, fixture and `scripts/fixtures/golden.txt` line it makes untrue, and how each changes. The run contract [bars editing one to get a pass](../../run-contract.md#checks-and-failure-repair).
5. Prove it. Run `python3 scripts/astrid_dev.py check`; the tests of what you touched (`python3 -m unittest discover -s scripts -p "test_<file>.py"`); and `sync` if a generated page changed. `check` confirms that a linked file exists and (`link-anchors`) that a `#heading` link into a skill, template or top-level doc names an existing heading. A pull request is checked with `check --base <base commit> --body-file /dev/null`.
6. Add a `fix` entry to the process ledger that ends `Follows: <entry it resolves>`.

## Audit

Run it when a process ledger entry from a run names friction in the skills, or the owner asks; never on a schedule. `N` helpers each map one area read-only: a skill, a guide, the templates. One high-judgment critic then verifies their claims against the code and judges them. The output is ledger entries and at most one proposal, not edits.
