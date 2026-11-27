# Machine lifetime controls

**Project:** Machine lifetime controls

**Goal:** A person with a rented RunPod machine sees when it will stop (release time, minutes left, cost so far, hourly rate) and can keep it longer or until they release it, always within a spend cap they set and with fresh paid consent.

**Status:** done

**Owner:** Plan 40 manager

**Estimate:** 0

**Waiting on:** —

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../index.md).

**Vision gaps:** [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (primary): a person sees when a rented machine will stop and can keep it, within a spend cap they set. [Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting): warm machines between jobs make RunPod usable for a working session.

## Outcome and scope

A person with a rented RunPod machine can see, and change, when it stops:

1. **See it.** `astrid machines` shows, for each live machine, when it will be released (the earlier of its idle expiry and its paid limit), the minutes left, the cost so far and its hourly rate. This works whether the machine is busy or idle.
2. **Keep it longer.** `astrid machines keep <id> --for <duration> --max-usd <cap>` extends a live machine's paid limit with fresh paid consent. It can be repeated.
3. **Keep it until released.** `astrid machines keep <id> --until-release --max-usd <cap>` turns off idle release, so the machine stays up until `astrid machines release <id>` or until the cap runs out. The cap is required ([D1](inputs.md#owner-decisions)).

**Not included:** a session-level keep (one setting that holds a machine across many jobs and tools), better default output names and folders, a provider-side or pod-side cap that works with no host running, and changes to how reuse treats paid limits. These are follow-ups ([inputs.md](inputs.md#deferred)).

## Existing work and decision

Everything needed is already in Plan 32's lease owner and journal; this plan adds one owner operation and a CLI over it. The journal already records `hourly_usd`, `estimated_cost_usd`, `accounted_at`, `paid_expires_at` and `idle_expires_at`, so (1) is a display change. Reuse deliberately refuses to extend a paid limit, and that rule stays: an explicit keep with fresh consent is the one sanctioned way to extend. Release is fired only by timers inside the running host, so a keep must refuse when no host owns the machine, and the CLI must say that release needs a running host. Details, the critic's findings and what was accepted are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Planned as four tasks (T1 to T4), it grew to T1 to T9 (T5 to T8 are GPU choice, waiting for capacity, setup and claim; T9 keeps the machine after a failed job). The review round is used and its four repairs, R1.1 to R1.4, are the last open work: see [tasks.md](tasks.md).

The plan was built on Plan 32's integration branch, `int/32-one-generation-path`, and its machines work shipped in the Release 13 line as the redesign in [D14](inputs.md#owner-decisions). It now ships in [Release 15](../../releases/15.md), on `release/15/plan-40` in astrid-agent, cut from `release/15/main`; the old `int/40-machine-lifetime` and `plan40/staging-int40` branches are not merged (they diverge by hundreds of commits and predate the redesign). There are no live GPU tests here: Plan 34 owns live runs.

## Interfaces and handoff

**Consumes:** Plan 32's `RunPodLeaseOwner` (`astrid/packs/runpod/worker_owner.py`), its lease journal rows (`astrid/packs/runpod/machine.py` `lease_row`), `PaidRunConsent.validate` (`astrid/packs/runpod/target_selection.py`) and the release task path, at the int/32 revision recorded in [inputs.md](inputs.md#source-identities).

**Produces:** the `astrid machines` table and its `--json` fields `release_at`, `minutes_left`, `cost_usd` (accrued to now) and `hourly_usd`; a `runpod.keep` host operation; and `astrid machines keep`. Plan 34 can use them to watch spend; a later session-level keep builds on the operation.

## Completion

On CPU fakes, through the real CLI and host operation:

- the table shows the right release time for an idle and for an active machine, and a cost that grows with time;
- `keep --for` moves the release time out, and only with fresh consent;
- `keep --until-release` removes idle release, and the machine is still released when the cap runs out;
- a keep with no live owner, on a machine the owner did not create, while a release is in flight, or with replayed consent is refused, and the machine is unchanged;
- reuse still cannot extend a paid limit.

The proof's limit: it runs on fakes, so a real pod is not kept or released here; Plan 34 can do that in its next run.

## Completion reconciliation — 26 November 2026

All 17 recorded task rows are complete. [Agent #554](https://github.com/banodoco/astrid-agent/pull/554) records the Lead's 23 November gate, 42 R1 and 17 headline cases passing with CPU fakes, and hosted comparison runs 45127057649 and 45127061949 (no new failures after the recorded baseline rulings). Merge `8fdf6615082785f5a8458abf614a9323092e0bc6` is an ancestor of the published Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, verified via GitHub compare. The scoped completion proof is CPU-fake proof, not a live paid RunPod session; no claim about real provider behavior or spend is made.

Release 15 was [qualified](https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7172606069) under the owner's approved conditional gate and [published](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7174076695) on 25 November. The [Lead's stand-down](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7179900972) confirms delivery is over. The owner's long-lived-install check and formal release finalization remain separate; no release status or gap is closed by this metadata reconciliation.
