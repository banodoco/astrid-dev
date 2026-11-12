---
name: astrid-dev-improve
description: Change astrid-dev itself, whether a rule, term, skill, template, check or generated page: start from a recorded failure, change the one home, prove it and record the fix.
---

# Improve astrid-dev

Enter through [astrid-dev](../astrid-dev/SKILL.md). Words follow the [glossary](../astrid-dev-shared/glossary.md).

## Where things go

| Kind of thing | Its one home | Enforced by |
| --- | --- | --- |
| A run rule: [routes, families, taste](../astrid-dev-shared/run-contract.md#routing-and-bindings); [stopping thresholds](../astrid-dev-shared/run-contract.md#cheapest-model-first); [authority, Run start, merges of progress PRs](../astrid-dev-shared/run-contract.md#who-answers-for-a-run); [commits only, credentials, rented machines](../astrid-dev-shared/run-contract.md#scope-source-identity-and-state); [no test edited to pass](../astrid-dev-shared/run-contract.md#checks-and-failure-repair); [merge-case test scope, check before commit](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing); [blocking findings, review rounds](../astrid-dev-shared/run-contract.md#review-and-promotion-boundaries) | [run contract](../astrid-dev-shared/run-contract.md) | judgment |
| A role's own steps: a manager's [progress](../astrid-dev-manage/SKILL.md#the-answer), [integration branch and worker cards](../astrid-dev-manage/SKILL.md#steps) (including `AskUserQuestion`); an orchestrator [closing](../astrid-dev-orchestrate/SKILL.md#path-4-close) | that role's skill | judgment |
| Running Codex from a Claude session: workers are the default; a Codex manager's check-in | [orchestrate skill](../astrid-dev-orchestrate/SKILL.md#use-codex-from-claude-cloud) | judgment |
| Installing skills for Codex | the guide for that environment: [Claude cloud](../astrid-dev-orchestrate/codex-in-claude-cloud/README.md) or [Codex cloud](../astrid-dev-orchestrate/codex-cloud/README.md) | judgment |
| A term | [glossary](../astrid-dev-shared/glossary.md) | judgment |
| A record of decisions | the glossary names three: a manager's [decision log](../astrid-dev-manage/SKILL.md#decide), the [decisions ledger](../astrid-dev-shared/run-contract.md#decisions-ledger-when-the-owner-is-unavailable), `inputs.md` Owner decisions | judgment |
| A pack's shape; what a card holds | the [plan](../../templates/project/plan.md), [inputs](../../templates/project/inputs.md) and [tasks](../../templates/project/tasks.md) templates | `pack-shape` |
| A project fact: name, goal, status, owner, estimate, waiting | the six lines of its `plan.md` | `plan-catalog` |
| Priority | [`plans/priority.md`](../../plans/priority.md) | `plan-catalog` |
| Claiming, proposing or finishing a project | the [contribution workflow](../../docs/contribution-workflow.md#claim-a-project) | the claim bot, `completion-assessment` |
| A check | `scripts/checks.py`; how: [extending guide](../../docs/extending.md#add-a-check) | its tests, `list` |
| A generated page | `scripts/views.py`; how: [extending guide](../../docs/extending.md#add-a-generated-view) | `generated-views` |
| Who owns a project; who merges; accountability, not permission | principle 5 in the [principles](../../docs/contribution-design-principles.md#the-principles); the [glossary](../astrid-dev-shared/glossary.md)'s project owner | `catalog-paths`, judgment |
| A principle | the [principles](../../docs/contribution-design-principles.md#the-principles) | judgment |
| Friction | the [process ledger](../../docs/ledger/README.md) | `ledger` |

## Steps

1. Start from a recorded failure: a process ledger entry or an issue. No failure, no change.
2. Find the home in the table. Change it and nothing else; replace any copy with a link to the home's heading.
3. If you add words, cut as many.
4. Change what a check accepts in a separate, announced change: list every pinned test, fixture and `scripts/fixtures/golden.txt` line it makes untrue, and how each changes. The run contract [bars editing one to get a pass](../astrid-dev-shared/run-contract.md#checks-and-failure-repair).
5. Prove it. Run `python3 scripts/astrid_dev.py check`; the tests of what you touched (`python3 -m unittest discover -s scripts -p "test_<file>.py"`); and `sync` if a generated page changed. `check` confirms that a linked file exists, not the heading after `#`: open the target and read its heading. GitHub's anchor is the heading in lowercase, punctuation dropped except hyphens and underscores, spaces turned into hyphens.
6. Add a `fix` entry to the process ledger that ends `Follows: <entry it resolves>`.

## Audit

Run it when a run's ledger entry names friction in the skills, or the owner asks; never on a schedule. `N` helpers each map one area read-only: a skill, a guide, the templates. One high-judgment critic then verifies their claims against the code and judges them. The output is ledger entries and at most one proposal, not edits.
