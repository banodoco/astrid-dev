---
description: Run declared agent tests: a cheap actor plays a role from its starting message, a judge checks the report against the case, and the owner reviews what the session would do.
skill: true
---

# Run agent tests

## When to use

When a covered document, brief or start message changes, before a lane launches, or when a new workstream, role or brief needs its first case.

## Outcome

Each selected case has a recorded result for the current documents, every miss is fixed at its home or put to the owner, and the owner has read what the session would do.

## Inputs

The cases in `agent-tests/cases/`, a checkout of the documents under test, the actor route each case names, and the high-judgment role for the judge.

## Procedure

Pick the cases, give each actor only its prompt, judge its report, fix document gaps at their home, re-run, record results and bring the owner the walkthrough and questions.

## Completion

Every selected case is `pass` in `agent-test status`, or its remaining misses are owner questions recorded on the PR; the results are committed with the change.

The format and rules are in [agent-tests/README.md](../../../agent-tests/README.md). Expectations come from the [golden path](../../../agent-tests/golden-path.md).

## Steps

1. **Pick the cases.** `python3 scripts/astrid_dev.py agent-test status` and `coverage`. Run every case that covers a changed file, and every case after it in a chain.
2. **Prepare a checkout** of the documents under test, at the PR's head. The actor reads only that.
3. **Run the actor.** `agent-test prompt <case> --checkout <path>` prints its prompt. Give that text, unchanged, to a fresh subagent on the case's route (N: Haiku), read-only. Never show the actor the case file, its Expect lines or an earlier report. For a chained case, pass the upstream actor's text with `--upstream <file>`.
4. **Judge.** `agent-test judge <case> --report <file>` prints the judge's prompt. Give it to a separate high-judgment session ([routing](../run-contract.md#routing-and-bindings)), never the author of the change.
5. **Fix and re-run.** A doc-gap is fixed at its home through [improve](improve.md). Re-run the actor on the fixed documents until the case passes or only owner questions remain. Don't edit a case's Expect lines to get a pass; a wrong expectation is fixed in the [golden path](../../../agent-tests/golden-path.md) first, with its source.
6. **Record.** `agent-test record <case> --verdict <file> --actor-model <model> --judge-model <model>` writes `agent-tests/results/<case>.md`. Commit it with the change.
7. **Owner.** Post each case's walkthrough and its Ask-the-owner questions on the PR, and record the answers where they belong.

Run independent cases side by side; run a chain in order.
