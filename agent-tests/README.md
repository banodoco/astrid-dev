# Agent tests

Programmatic tests check what code does. Agent tests check what a fresh session does when it is given a role's documents and one starting message: whether it finds the right skill and brief, takes the right first steps, sets its check-in, posts in the right place, pushes only what it should, runs the right tests, and hands the right text to the next session.

A test is a **case**. Each case is declared in one file, and names the documents it covers and the brief it runs under. A **cheap actor** plays the role from the starting message alone and reports what it would do. A **judge** compares the report with the case's expectations. The **owner** reads a short account of what the session would do and answers the case's questions. The procedure is in [improve](../agent/shared/workstreams/improve.md#agent-tests).

## Where things live

| What | Where |
| --- | --- |
| One case | `agent-tests/cases/<id>.md` |
| A case's latest result | `agent-tests/results/<id>.md`, written by `agent-test record` |
| The golden path the cases encode | [golden-path.md](golden-path.md) |
| The runner | `python3 scripts/astrid_dev.py agent-test list \| status \| coverage \| prompt \| judge \| record` |
| The structure check | `agent-tests` in `python3 scripts/astrid_dev.py check` |

Cases live here, not next to the documents under `agent/`. Two reasons: a skill's text is what the actor reads, so expectations beside it would hand the actor the answers; and many cases cover a path across several documents (an orchestrator's launch line becomes a manager's input), so a case belongs to the path, not to one file. Each case declares what it covers; `agent-test coverage` gives the view from each document's side.

## A case

```markdown
---
id: lane-orchestrator-start
role: lane orchestrator, launched by the owner
covers:
  - agent/roles/orchestrator.md
  - agent/roles/orchestrator/lane-orchestrator.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: N
---

# A lane orchestrator's first two hours

## Given

The exact first message, as the role receives it.

## Fixture

- State the actor may assume: board contents, branches that exist.

## Expect

- One observable behaviour per line, phrased so a report can show it.

## Must not

- One forbidden behaviour per line.

## Ask the owner

- A question only the owner can answer: does this make sense?
```

| Field | Meaning |
| --- | --- |
| `id` | The file name, lowercase kebab-case. |
| `role` | Who the session is, and who started it. |
| `covers` | The documents whose instructions the case tests. A changed covered file makes the result stale. |
| `brief` | The brief the session works under, if any (a lane brief, a plan's `tasks.md`). Also part of the result's fingerprint. |
| `host` | `claude-cloud`, `claude-subagent`, `codex-app`, `codex-in-claude` or `chatgpt-web`. Sets the role-play line. |
| `actor` | The route that plays the role. Default `N`, the cheapest: if the cheapest model follows the documents, they are clear. |
| `after` | A chained case: its Given contains `{upstream}`, filled with the text the upstream case's actor produced (for example the manager launch an orchestrator posted). Chains test hand-offs. Pass only the text the upstream session would hand over, not its whole report. |

**Writing expectations.** Take each one from [the golden path](golden-path.md), which names the document line it rests on. A behaviour the documents don't state is not an expectation yet: fix the document first, through [improve](../agent/shared/workstreams/improve.md). Phrase each line so the report can show it, for example "posts its first STATUS on `board: lane h3`", not "communicates well".

## Results

A result records the date, verdict, the actor's and judge's models, the commit, and a digest of every covered file and the brief. `agent-test status` reports each case as `never run`, `stale` (a covered file changed since), `fail` or `pass`.

The person running the tests does not fix misses one by one: they group them by cause, name the parent idea behind each group, and fix that ([synthesize, don't react](../agent/shared/workstreams/improve.md#synthesize-dont-react)). A miss has one of three causes, which the judge names:
- **doc-gap:** the documents are missing, wrong or contradictory. Fix the document, then re-run.
- **actor-error:** the documents were clear. Note it; re-run once on the next route up if it repeats.
- **ambiguity:** only the owner can decide. Ask, record the answer in its one home, then re-run.

## When cases run

- **Changing a covered document:** run every case that covers it, and record the results in the same PR ([improve](../agent/shared/workstreams/improve.md), step 5).
- **Before a lane launches:** run the cases that name its brief.
- **Adding a workstream, role or brief:** add at least one case for it.

The check validates structure only: fields, sections, covered files, chains and result files. It runs no models.

## Depths

- **Cold read** (this runner): the actor describes what it would do. It works for every host, including the Codex app and ChatGPT chats, which cannot run a harness.
- **Mocked act** (later, Claude hosts only): the same case run through `claude plugin eval`, with GitHub and remote-session tools mocked, so the grader sees the tools actually called.
