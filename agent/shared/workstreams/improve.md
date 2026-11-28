---
description: Change astrid-dev itself, whether a rule, term, skill, template, check or generated page: start from a recorded failure, change the one home, prove it with checks and agent tests, and record the fix.
skill: true
---

# Improve astrid-dev

## When to use

When changing an Astrid Dev rule, term, skill, template, check or generated document; when auditing them; or when testing that a role's documents make a fresh session do the right thing.

## Outcome

A demonstrated Astrid Dev process or documentation failure corrected at its canonical source with regression proof.

## Inputs

The recorded failure or need, one authoritative source, neighboring references, existing tests and permission to change the machinery.

## Procedure

Identify the owning source, make the smallest coherent change, run the relevant checks and record the fix without duplicating policy.

## Completion

Documentation and generated views remain consistent, original regressions are covered and the change's proof is recorded.

Enter through [astrid-dev](../../start.md). Words follow the [glossary](../glossary.md).

## Where things go

| Kind of thing | Its one home | Enforced by |
| --- | --- | --- |
| A run rule: [routes and families](../run-contract.md#routing-and-bindings); [taste tasks](../run-contract.md#who-answers-for-a-run); [stopping thresholds](../run-contract.md#cheapest-model-first); [authority, Run start, merges of progress PRs](../run-contract.md#who-answers-for-a-run); [commits only, credentials, rented machines](../run-contract.md#scope-source-identity-and-state); [no test edited to pass](../run-contract.md#checks-and-failure-repair); [merge-case test scope, check before commit](../run-contract.md#when-a-test-run-is-load-bearing); [blocking findings, review rounds](../run-contract.md#review-and-promotion-boundaries); [boards, who checks in, milestones, liveness](../run-contract.md#coordination-boards-and-check-ins) | [run contract](../run-contract.md) | judgment |
| A role's own steps and selected workstreams: a [Release Lead](../../roles/leader.md) and its [lane workstream](../../roles/leader/lane-orchestrators.md); a manager's [progress](../../roles/manager.md#the-answer), [plan branch and worker cards](../../roles/manager.md#steps) (including `AskUserQuestion`); an orchestrator's [workstreams](../../roles/orchestrator.md#workstreams) and [closing](../../roles/orchestrator.md#path-4-close) | that role's skill and `workstreams/` | judgment |
| Running Codex from a Claude session: workers are the default; a Codex manager's check-in | [Codex-in-Claude workstream](../../roles/orchestrator/codex-in-claude-cloud.md#use-codex-from-claude-cloud) | judgment |
| Reading CI results, getting them complete, using GitHub Actions for tests | [green skill](green.md) | judgment |
| Installing skills for Codex | the guide for that environment: [Claude cloud](../../guides/codex-in-claude-cloud/README.md) or [Codex cloud](../../guides/codex-cloud/README.md) | judgment |
| Vision wording: an element, an aspiration, its lists | [contribution workflow](../../../docs/contribution-workflow.md#write-or-improve-documentation) | `subjects`, owner review |
| Release rationale, scope and contributions | the [release brief](../../../releases/TEMPLATE.md) | `release-documents` |
| Version and major-version decisions, with generated release material | [strategy](../../../strategy.md); [hierarchy](../../../docs/contribution-workflow.md#review-the-strategy) | `strategy-consistency`, `generated-views` |
| A term | [glossary](../glossary.md) | judgment |
| A record of decisions | the glossary names three: a manager's [decision log](../../roles/manager.md#decide), the [decisions ledger](../run-contract.md#decisions-ledger-when-the-owner-is-unavailable), `inputs.md` Owner decisions | judgment |
| A pack's shape; what a card holds | the [plan](../../../templates/project/plan.md), [inputs](../../../templates/project/inputs.md) and [tasks](../../../templates/project/tasks.md) templates | `pack-shape` |
| A project fact: name, goal, status, owner, estimate, waiting | the six lines of its `plan.md` | `plan-catalog` |
| Priority | [`plans/priority.md`](../../../plans/priority.md) | `plan-catalog` |
| Claiming, proposing or finishing a project | the [contribution workflow](../../../docs/contribution-workflow.md#claim-a-project) | the claim bot, `completion-assessment` |
| A check | `scripts/checks.py`; how: [extending guide](../../../docs/extending.md#add-a-check) | its tests, `list` |
| A generated page | `scripts/views.py`; how: [extending guide](../../../docs/extending.md#add-a-generated-view) | `generated-views` |
| Who owns a project; who merges; accountability, not permission | principle 5 in the [principles](../../../docs/contribution-design-principles.md#the-principles); the [glossary](../glossary.md)'s project owner | `catalog-paths`, judgment |
| A principle | the [principles](../../../docs/contribution-design-principles.md#the-principles) | judgment |
| A question, bug, observation or idea about Astrid | the [Issues section](../../../docs/contribution-workflow.md#issues) and each type's [form](../../../.github/ISSUE_TEMPLATE) | GitHub's forms, judgment |
| Friction | the [process ledger](../../../docs/ledger/README.md) | `ledger` |

## Steps

1. Start from a recorded failure: a process ledger entry, an issue or an accepted card. No failure, no change.
2. Find the home in the table. Change it and nothing else; replace any copy with a link to the home's heading.
3. If you add words, cut as many. Write the change as an [explainer](../../README.md#write-it-as-an-explainer): the parent rule, not another case.
4. Change what a check accepts, or add a check, in a separate, announced change: list every pinned test, fixture and `scripts/fixtures/golden.txt` line it makes untrue, and how each changes. The run contract [bars editing one to get a pass](../run-contract.md#checks-and-failure-repair).
5. Prove it. Run `python3 scripts/astrid_dev.py check`; the tests of what you touched (`python3 -m unittest discover -s scripts -p "test_<file>.py"`); `sync` if a generated page changed; and `skills build` then `skills check` if a skill changed. `check` confirms that a linked file exists and (`link-anchors`) that a `#heading` link into a skill, template or top-level doc names an existing heading. A pull request is checked with `check --base <base commit> --body-file /dev/null`.
   For a change to a role, workstream, start message or brief, also run the [agent tests](#agent-tests) that cover it (`agent-test status` lists them) and commit the run sheet; a changed document with no case gets one.
6. Add a `fix` entry to the process ledger that ends `Follows: <entry it resolves>`.

## Audit

Run it when a process ledger entry from a run names friction in the skills, or the owner asks; never on a schedule. `N` helpers each map one area read-only: a skill, a guide, the templates. One high-judgment critic then verifies their claims against the code and judges them. The output is ledger entries and at most one proposal, not edits.

## Agent tests

An agent test checks that a fresh session, given a role's documents and one starting message, does what the [golden path](../../../agent-tests/golden-path.md) says. The format is in [agent-tests/README.md](../../../agent-tests/README.md). Run them when a covered document, brief or start message changes, before a lane launches, and as an audit. An audit's inventories feed the golden path.

1. **Open a run sheet** from [the template](../../../agent-tests/runs/TEMPLATE.md), and fill it in as you go. **Pick the cases.** `python3 scripts/astrid_dev.py agent-test status` and `coverage`. Run every case that covers a changed file, and every case after it in a chain.
2. **Prepare a checkout** of the documents under test: `agent-test checkout <dest>` exports the head with the cases, results and golden path withheld. The actor reads only that.
3. **Run the actor.** `agent-test prompt <case> --checkout <path>` prints its prompt. Give that text, unchanged, to a fresh read-only subagent on `N` (Haiku), with no tool that acts on another session where the host allows it. If every miss is an actor-error, run the same prompt once more on the case's `actor` route ([when a case passes](../../../agent-tests/README.md#run-sheets)). Never show the actor the case file, its Expect lines or an earlier report. For a chained case, pass the upstream actor's report with `--upstream-report <file>`; its tagged hand-over block is used ([hand-offs](../../../agent-tests/README.md#hand-offs)).
4. **Judge.** `agent-test judge <case> --report <file>` prints the judge's prompt. Give it to a separate high-judgment session ([routing](../run-contract.md#routing-and-bindings)), never the author of the change.
5. **Synthesize before fixing** ([below](#synthesize-dont-react)). Then **fix and re-run.** Each parent fix lands at its home through the [steps](#steps) above. Re-run the actor on the fixed documents until the case passes or only owner questions remain. Don't edit a case's Expect lines to get a pass; a wrong expectation is fixed in the [golden path](../../../agent-tests/golden-path.md) first, with its source.
6. **Record** each round's verdicts, the synthesis and the changes on the run sheet, and commit it with the change, or on its own PR when the run changed nothing.
7. **Owner.** Post each case's walkthrough and its Ask-the-owner questions on the PR, and record the answers where they belong.

Run independent cases side by side; run a chain in order.

### Synthesize, don't react

A run's findings are evidence about the documents, not a to-do list. Thirty misses answered one by one become thirty patches and a longer, less coherent skill. The person running the tests reads them for causes:

1. **Group by cause, not by symptom.** Gather the misses from every case and every level before fixing any. Misses in different roles often share one cause.
2. **Name each group's kind.**
   - **Structural:** a fact has two homes, or none.
   - **Precedence:** two documents both apply and neither says which wins.
   - **Missing parent idea:** many specific rules exist because one general rule was never written.
   - **Sequence or priority:** the right steps, in an order or with a weight that misleads.
   - **Wording:** one document, unclear.
3. **State the parent idea for each group,** as one sentence a fresh session could apply to cases nobody listed. Prefer the parent that lets you delete specific rules ([subtract before adding](../../../docs/contribution-design-principles.md#the-principles)).
4. **Write it as a pyramid.** Lead with the governing thought. Under it, the few parent ideas, ranked by consequence times likelihood. Under each, only the findings it settles, as evidence. A finding no parent explains is the only kind fixed on its own.
5. **Fix the parents, then re-run.** A parent fix is right when re-running the same cases clears its whole group. Misses that survive point to a different parent.
6. **Bring the owner the pyramid,** not the list: the governing thought, the parent ideas with the choice each needs, and what each removes.
