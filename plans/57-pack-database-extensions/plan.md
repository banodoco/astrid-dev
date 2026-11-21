# Packs extend the database

**Project:** Packs extend the database

**Goal:** A pack can add its own tables and rows to a project's database, freely, while Astrid's own fields stay protected, updates keep working, and a pack cannot destroy what is not its own.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** version 0.1 ([Strategy](../../strategy.md#versions)); the prior-art read and the owner's scope decision

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each, then run `python3 scripts/astrid_dev.py sync`. Its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [Frontend and backend extension composition](../../vision/gaps/LS-003-full-stack-contributions.md) (primary): a contribution that needs its own data today has nowhere sanctioned to keep it. [Pack lifecycle under load](../../vision/gaps/F-004-pack-lifecycle.md) (supporting): what a pack stores must survive install, update, rollback and removal.

**Draft; not ready for execution.** This records the owner's direction of 15 November 2026 so it is not lost. It is for after version 0.1.

## Outcome and scope

The owner's direction, in her words where quoted:

- Packs should be able to "add tables and add rows", and in general "extend the database in whatever way they want".
- "We should obviously have some protected fields in the database": what Astrid itself owns is not a pack's to change.
- "We need to have a way to accommodate for that in updates and everything": a pack's tables must survive Astrid's updates and the pack's own updates, rollback and removal.
- We need "to test for it and protect against them doing destructive actions".
- Some things Astrid does in core today should become packs once this exists, installed by default: "for example, references, how we deal with references, and possibly some others".

Not yet decided: which store this means (the Runtime's project database, the App's, or both), what counts as protected, how far "whatever way they want" goes for changing existing tables, and which core features move first.

## Existing work and decision

Pending. See [inputs.md](inputs.md#planning-evidence). Nothing has been read for this plan yet. Related: [Plan 06](../06-packs/plan.md) (packs), [Plan 35](../35-one-home-for-user-state/plan.md) (one home for user state), [Plan 47](../47-pack-stress-tests/plan.md) (proving demanding packs), [Plan 17](../17-vibecomfy-extensibility/plan.md) (pack extension points).

## Sequence and readiness

After version 0.1. First step when taken up: read how the Runtime and App store and migrate data today and how packs are installed and updated, then put real options to the owner. Recording this plan authorizes no work.

## Interfaces and handoff

Pending the prior-art read.

## Completion

Pending. At least: a pack adds a table and rows, and they survive an Astrid update, a pack update, a rollback and a removal with an explicit choice about its data; a pack's attempt to change or delete what it does not own is refused; a feature that is core today (references is the owner's example) runs as a default-installed pack with no loss of existing data.
