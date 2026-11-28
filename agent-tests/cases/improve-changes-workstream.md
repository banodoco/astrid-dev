---
id: improve-changes-workstream
role: session asked by the owner to fix a contradictory worker rule
covers:
  - agent/shared/workstreams/improve.md
  - agent/roles/worker.md
host: claude-cloud
actor: X
---

# Changing one line of the worker role through the improve workstream

## Given

```text
Follow the astrid-dev-improve skill (install the skills from a banodoco/astrid-dev checkout: mkdir -p ~/.claude/skills && python3 scripts/astrid_dev.py skills install --destination ~/.claude/skills). Workers are being told both to set an hourly check-in and to post only milestones; the failure is recorded in docs/ledger/2026-11-28-agent-path-dry-runs.md. Fix it on banodoco/astrid-dev main.
```

## Fixture

- Stand-ins: treat `agent/shared/workstreams/start-session.md` step 5 as reading, unscoped, "**Set the check-in.** The new session sets its own hourly check-in with its host's scheduler…", even where the checkout differs.
- `docs/ledger/2026-11-28-agent-path-dry-runs.md` is open: its `Resolved by:` line reads `—`.

## Expect

- Reads the recorded failure first, and names its ledger entry, before it edits anything ([improve, step 1](../../agent/shared/workstreams/improve.md#steps)).
- Finds the rule's one home, the run contract's coordination items 5 and 7, and the copy that contradicts it, start-session step 5 ([improve, where things go](../../agent/shared/workstreams/improve.md#where-things-go)).
- Changes the copy to defer to the home with a link, rather than adding a rule anywhere else ([improve, step 2](../../agent/shared/workstreams/improve.md#steps); [write it as an explainer](../../agent/README.md#write-it-as-an-explainer)).
- Runs `python3 scripts/astrid_dev.py check`, and the skill build, since start-session is a skill ([improve, step 5](../../agent/shared/workstreams/improve.md#steps)).
- Runs `agent-test status`, runs every case that covers the changed file, and commits a run sheet with the change ([improve, agent tests](../../agent/shared/workstreams/improve.md#agent-tests)).
- Groups any misses by cause and names a parent idea before fixing them ([improve, synthesize, don't react](../../agent/shared/workstreams/improve.md#synthesize-dont-react)).
- Adds a `fix` entry to `docs/ledger/` that ends `Follows: 2026-11-28-agent-path-dry-runs` ([improve, step 6](../../agent/shared/workstreams/improve.md#steps)).

## Must not

- Add a check-in rule to `agent/roles/worker.md` that restates the run contract.
- Edit or delete the open ledger entry, except to fill its `Resolved by:` line ([ledger README](../../docs/ledger/README.md)).

## Ask the owner

- Is linking the copy to its home, rather than deleting it, the right weight for a step every role reads?
