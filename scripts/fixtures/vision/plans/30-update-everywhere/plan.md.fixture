# Update everywhere: remaining setups

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

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
