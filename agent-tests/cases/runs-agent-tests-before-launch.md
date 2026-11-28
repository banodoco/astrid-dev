---
id: runs-agent-tests-before-launch
role: a fresh session asked by the owner to run a lane's agent tests before its launch
covers:
  - agent/shared/workstreams/improve.md
  - agent-tests/README.md
  - agent/roles/leader/lane-orchestrators.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: X
---

# Running the H3 lane's agent tests from the documents alone

## Given

```text
Follow the astrid-dev-improve skill. Before the H3 lane launches, run its agent tests on banodoco/astrid-dev main and bring me the result.
```

## Fixture

- The actor checkout withholds `agent-tests/cases/`. Assume `agent-test status` lists ten cases naming `releases/16/briefs/h3.md`, among them the chain `h3-orchestrator-start` → `h3-codex-manager-start` → `h3-chat-unit`, all `stale`.

## Expect

- Opens a run sheet from `agent-tests/runs/TEMPLATE.md` before running anything.
- Picks the cases with `agent-test status` and `coverage`, including every case after a stale one in a chain.
- Exports the actor checkout with `agent-test checkout`, and never shows an actor a case file.
- Gives each actor only its `agent-test prompt` text, as a fresh read-only subagent on `N`, with no tool that acts on another session.
- Runs a chain in order, feeding each case its upstream's hand-over with `--upstream-report`.
- Judges each report in a separate high-judgment session with `agent-test judge`.
- Applies the pass bar: re-runs a case on its own route only when every miss is an actor-error.
- Groups the misses by cause and names parent ideas before fixing anything.
- Commits the run sheet, and brings the owner the governing finding, the parent ideas and the owner questions.

## Must not

- Edit a case's Expect lines to get a pass.
- Fix misses one by one without a synthesis.
- Judge its own actors' reports in the same session.
