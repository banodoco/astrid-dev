# Lane brief — <lane>

**Lane:** <lane>
**Releases:** <N>, continuing in <M>
**State:** <prepared, running, paused or done>; <one line of note>
**Go:** <Pending while prepared; otherwise the owner's go: date, the owner, and a link to where the owner gave it>
**Orchestrator:** route <X or S>; session <session id, once started>
**Reviewer:** <the high-judgment binding and its brief>
**Board:** `board: lane <lane>`, linked once opened

This is the one home for how the <lane> lane runs. Its plans, order, rulings and limits live here; the release brief and each plan's `tasks.md` link to it and never copy it.

## Outcome

<The end state for this lane, in a few sentences.>

## Plans and order

| Plan | Release | Starts when | Branches |
| --- | --- | --- | --- |
| <PP> <title>, `plans/<PP>-<slug>/plan.md` | <N> | <Now, or the joins: the units that must merge first> | <repository and branch `release/<N>/plan-<PP>`, at `<SHA>`, with its base> |

## Queue

The execution-units tables in each plan's `tasks.md` are the queue. Link each plan's `tasks.md` here, one link per plan (`plans/<PP>-<slug>/tasks.md`); never copy its table.

## How it runs

**Option:** <hosted or packets>

`hosted`: a Claude orchestrator runs a Codex worker per card by `codex exec` (Claude workers as fallback), or a Codex manager it hosts when this brief says so. `packets` is the ChatGPT web-chat route: one Codex desktop manager (name it, e.g. `h3-manager`) runs in the Codex app on the owner's computer, the orchestrator posts its launch on the lane board and the owner pastes it, and it opens one ChatGPT chat per unit (N High, X Extra High, S Pro) by the TOOLKIT steps on astrid-dev #2030. Fallbacks, in order: `codex exec` workers run by the orchestrator's Claude session, then Claude workers.

- **Start.** Open the lane board first, then post one STATUS. <The startup checks, each posted as one STATUS line: passed or failed.>
- **Dispatch.** <The in-flight cap, whether the first unit runs alone, and the route and mode for each unit. Replacement rules. The hourly cadence.>
- **Proof.** <Who runs the focused proof, where it runs, and what counts as evidence. Hosted CI as the final check.>
- **Reviews.** <Which stops need the reviewer's ACCEPT, which units merge on green CI and shown proof, and how findings return.>
- **Merges.** <What the orchestrator merges on green. Each ready plan goes to the Lead as a PR into `release/<N>/main`, and the Lead merges it.>
- **Check-ins.** <One STATUS on the lane board per check-in, and what it holds.>

## Roles

- **Orchestrator:** <accountable for every plan in this lane, and answers to the owner. Signs its comments `<lane>-orchestrator`. What it may do without asking.>
- **Manager or packet sessions:** <bounded delegates: what each may do and may never do.>
- **Reviewer:** <the high-judgment binding, and when it is started.>
- **Advisor:** <the chain: delegates ask the orchestrator; the orchestrator asks the release Lead for release-level questions, and the reviewer for technical judgment.>
- **Owner:** <see Owner only.>

## Standing rulings

Dated and append-only; this is the one home for this lane's rulings. Each entry gives its date and who ruled.

- <date> (<who ruled>): <ruling>, with its reason and link.

## Context

- **Decisions and their reasons:** <each with a link to its issue, plan or record.>
- **Skills:** <hand-written guides this lane's work follows, and which pack or plan writes each.>

## Cut line and coordination

- **Never slips:** <what this lane must ship.>
- **Slips first:** <what moves out first if the release is at risk.>
- **Other lanes:** <lanes that touch the same code or fixtures, and how the merges are ordered.>
- **CI:** <how CI capacity is shared, and with which lanes.>

## Owner only

- <What the orchestrator must bring to the owner: scope changes, spending, publication, and anything else reserved.>

## Launch

The owner sends this one line to a new orchestrator session:

```text
Follow the astrid-dev-orchestrator skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). Your brief is releases/<N>/briefs/<lane>.md on banodoco/astrid-dev main. Created by session <creator session id>, signing <creator sign-off>.
```

## Status

Read `python3 scripts/astrid_dev.py release status <N>` and this lane's board. Do not keep a second copy here.
