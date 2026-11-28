---
id: improve-changes-workstream
role: session asked by the owner to change one line in agent/roles/worker.md
covers:
  - agent/shared/workstreams/improve.md
  - agent/roles/worker.md
host: claude-cloud
actor: N
---

# Changing one line of the worker role through the improve workstream

## Given

```text
Follow the astrid-dev-improve skill (install the skills with python3 scripts/astrid_dev.py skills install from a banodoco/astrid-dev checkout). Change one line in agent/roles/worker.md on banodoco/astrid-dev main so that a worker sets no hourly check-in and posts only milestones. The failure is recorded in docs/ledger/2026-11-28-agent-path-dry-runs.md.
```

## Fixture

- `docs/ledger/2026-11-28-agent-path-dry-runs.md` is open: its `Resolved by:` line reads `—`. It records that workers were told both to set an hourly task and to post only milestones.
- `agent/roles/worker.md` has no check-in rule today.

## Expect

- Reads the recorded failure first, and names its ledger entry, before it edits anything ([improve, step 1](../../agent/shared/workstreams/improve.md#steps)).
- Finds the one home for a worker's check-in, and changes only that line in `agent/roles/worker.md` ([improve, where things go](../../agent/shared/workstreams/improve.md#where-things-go); [improve, step 2](../../agent/shared/workstreams/improve.md#steps)).
- Replaces any copy of the rule elsewhere with a link to its home, rather than restating it ([improve, step 2](../../agent/shared/workstreams/improve.md#steps)).
- Reports that [run contract, coordination item 7](../../agent/shared/run-contract.md#coordination-boards-and-check-ins) says every Claude role sets an hourly check-in, which conflicts with the worker rule in the [golden path](../golden-path.md#the-four-rules).
- Runs `python3 scripts/astrid_dev.py check`, and the unit tests of the files it touched ([improve, step 5](../../agent/shared/workstreams/improve.md#steps)).
- Runs `agent-test status`, then every case that covers `worker.md`, and commits their results with the change ([improve, agent tests](../../agent/shared/workstreams/improve.md#agent-tests)).
- Where a case misses, groups the misses by cause and names one parent idea per group before any fix ([improve, synthesize, don't react](../../agent/shared/workstreams/improve.md#synthesize-dont-react)).
- Adds a `fix` entry to `docs/ledger/` that ends `Follows: 2026-11-28-agent-path-dry-runs` ([improve, step 6](../../agent/shared/workstreams/improve.md#steps); [ledger README](../../docs/ledger/README.md)).

## Must not

- Edit any file other than `agent/roles/worker.md`, its fix entry, and its case results ([improve, step 2](../../agent/shared/workstreams/improve.md#steps)).
- Edit or delete the open ledger entry, except to fill its `Resolved by:` line ([ledger README](../../docs/ledger/README.md)).
- Change a case's Expect lines to make a run pass ([improve, step 5](../../agent/shared/workstreams/improve.md#steps)).
- Patch each miss separately ([improve, synthesize, don't react](../../agent/shared/workstreams/improve.md#synthesize-dont-react)).

## Ask the owner

- Is `agent/roles/worker.md` the one home for a worker's check-in? Or should run contract coordination item 7, which says every Claude role sets one, be narrowed to managers and orchestrators?
