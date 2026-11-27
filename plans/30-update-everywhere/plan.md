# Update everywhere: remaining setups

**Project:** Update everywhere: remaining setups

**Goal:** Finish Plan 29 for less common setups: Linux with systemd below 254, typed update contracts, refused cards, and update proof for Pinokio and fully local.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Historical residual estimate 7–9 engineering days; re-size remaining supported-route gaps before dispatch

**Waiting on:** Reuse P29's landed updater; [SC-30](https://github.com/banodoco/astrid-dev/blob/75d69e848eaa0760993e7be3a7c13c5fa7a0f19c/plans/30-update-everywhere/evidence/release-16-scoping/SC-30.md) identifies older systemd worker lifecycle, normalized status/refusal, fully-local skew and genuine Pinokio update proof. Coordinate P09/P10/P29; task rows remain unchecked.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

[Plan 29](../29-update-and-release/plan.md) gives normal installs a working Update now from Release 10. This plan finishes the setups it leaves:

- **Linux with systemd below 254** (Ubuntu 22.04, Debian 12). Update now works there too.
- **Contracts.** Typed contracts guard the boundaries that broke.
- **Refused cards.** The "refused" cards follow one rule.
- **Pinokio and fully local.** Updates are proven through the actions people actually press.

This plan is committed: it is part of the owner's "no stopgaps" decision on 7 Nov 2026, not optional polish.

## Existing work and decision

The scope, evidence and reviews are in [Plan 29's inputs](../29-update-and-release/inputs.md#planning-evidence). This plan has its own catalog row so it can be prioritised separately.

## Sequence and readiness

Start after Plan 29's Release 10. The tasks are independent of each other, and the details are in [tasks.md](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

- **Consumes:** Plan 29's `self_update` status, its reasons, and the hosted button-path rows.
- **Produces:**
  - a Runtime-owned helper-protocol schema;
  - an update-status schema that sits outside the versioned contract, so the schema digest stays unchanged;
  - a refusal rule;
  - proof rows.

## Completion

The proof is these observable results:
- An Ubuntu 22.04 hosted row updates through the button.
- An update that started before the systemd change is still reconciled.
- Schema tests on both boundaries fail when either side drifts.
- "Refused" shows update wording only when the installed release is behind.
- The Pinokio row runs the launcher's own Update action.
- A dev:local test updates through the in-page updater.


## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

Independent work starts on existing typed action/status interfaces; only affected landings join the P29 contract. Keep old Linux systemd, fully-local pairing and actual Pinokio. One resolver, no parallel refusal system.
