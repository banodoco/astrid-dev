---
name: astrid-dev-improve
description: Change astrid-dev itself, whether a rule, term, skill, template, check or generated page: start from a recorded failure, change the one home, prove it and record the fix.
---

# Improve astrid-dev

Enter through [astrid-dev](../astrid-dev/SKILL.md). Words follow the [glossary](../astrid-dev-shared/glossary.md).

## Where things go

| Kind of thing | Its one home | Enforced by |
| --- | --- | --- |
| A run rule: routes and model families, authority, who answers and the `Run start` line, stopping, commits only, merges, review rounds and blocking findings, rented machines, credentials, `check` before a commit, no test edited to pass | [run contract](../astrid-dev-shared/run-contract.md) | judgment |
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
| A principle | the [principles](../../docs/contribution-design-principles.md#the-principles) | judgment |
| Friction | the [process ledger](../../docs/ledger/README.md) | `ledger` |

## Steps

1. Start from a recorded failure: a process ledger entry or an issue. No failure, no change.
2. Find the home in the table. Change it and nothing else; replace any copy with a link to the home's heading.
3. If you add words, cut as many.
4. A change to what a check accepts is its own announced change: list every pinned test, fixture and `scripts/fixtures/golden.txt` line it makes untrue, and how each changes. Never edit one to get a pass; if your card did not list it, stop and report the lines.
5. Prove it. Run `python3 scripts/astrid_dev.py check`; the tests of what you touched (`python3 -m unittest discover -s scripts -p "test_<file>.py"`); and `sync` if a generated page changed. `check` confirms that a linked file exists, not the heading after `#`: open the target and read its heading. GitHub's anchor is the heading in lowercase, punctuation dropped except hyphens and underscores, spaces turned into hyphens.
6. Add a `fix` entry to the process ledger that follows the entry it resolves.

## Audit

Run it when a run's ledger entry names friction in the skills, or the owner asks; never on a schedule. `N` helpers each map one area read-only: a skill, a guide, the templates. One high-judgment critic then checks their claims in the code and judges them. The output is ledger entries and at most one proposal, not edits.
