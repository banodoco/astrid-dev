# Project: <name>

**Start here:** read [AGENTS.md](../AGENTS.md), choose a workflow in the [skills guide](../skills/README.md), follow the [run contract](../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../docs/glossary.md).

## Prerequisites

| Item | Record |
|---|---|
| Hardware | Operating systems, architecture, disk or other machine needs for the checks, or `none` |
| Access | Repository push rights, accounts or approved spend needed, or `none` |
| Predecessors | Plans or landed work that must exist first, with links, or `none` |
| Authorization | Queued plans start only on the owner's explicit go ([AGENTS.md](../AGENTS.md)) |

## Can start?

List the tasks a contributor can begin today and what each one waits on. Say plainly which tasks are blocked and by what.

## Goal

What useful result will users get? Include important behavior that must remain.

## Owner

Set the accountable person, team, or coordinating role in the root [README queue](../README.md). Use `Unassigned` until a current owner is known; this field does not grant work authorization. Keep the queue as the only owner record.

## Scope

- Included:
- Deferred:

## Inputs

List the plan, code, decisions, or other evidence needed to do the work. Link portable sources; confirm changing source details when work starts.

| Input | Why it matters | Link or evidence |
|---|---|---|
| | | |

## Starting code

Record these before changing source code. Freeze actual identities; do not assume a branch exists.

| Field | Record |
|---|---|
| Product repository | Repository URL or local identity |
| Starting branch and commit | Actual branch and SHA at the start |
| Existing work to preserve | Exact commits and unfinished local changes |
| Predecessor output | Link to verified output, or `none` |
| Working candidate branch | Fresh branch name, recorded at start |
| Intended merge destination | `pre-main` for this initiative; verify the branch exists |

## Tasks

Break the goal into outcomes. For each, record its route, dependency, and focused acceptance evidence. The route is `N` by default, including ordinary hard work; `X` only for very hard work; `S` only for super-hard work. Name the route, not the model; see the [routing table](../skills/astrid-dev-shared/run-contract.md#routing-and-bindings).

| Outcome | Route | Depends on | How to check | Done |
|---|---|---|---|---|
| | | | | |

Example: “Preserve the current export format” could use route `N`, no dependency, and a focused export check on a sample project.

## Completion

State what evidence shows the goal is met, what remains unresolved, and where the accepted result should go. When done or cancelled, move the project from the root README queue to [ARCHIVE.md](../ARCHIVE.md); keep this plan at its stable path.
