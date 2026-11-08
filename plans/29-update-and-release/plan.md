# One update path and release

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary). [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting).

## Outcome and scope

People see one clear way to update Astrid, and it works:
- **Update now** for a normal install;
- **Update in Pinokio** for Pinokio;
- the command or agent instructions only as a secondary option, or where the button can't work.

Every screen agrees, because each one shows what the installed Astrid says rather than guessing. A release number means a real release: it changes only when what users install changes, and only by a deliberate merge.

- **Included:**
  - fix "Update now" at its root (it has never worked on any published install);
  - say why whenever it can't run;
  - one decision table for every update surface;
  - remove setup and consent UI from update surfaces;
  - a release number that moves only with the installed tuple, guarded by a small required check;
  - protected App `main`.
- **Also included:** a Runtime `self_update` capability; update status for Pinokio fully local (its preview server answers 501 today); fully local Update now through the existing in-page updater.
- **Committed in [Plan 30](../30-update-everywhere/plan.md):** removing the systemd 254 floor, typed contracts at both broken boundaries, the refused cards, and Pinokio and fully local update proof.

  This plan takes over [Plan 09](../09-install-and-update-confidence/plan.md) IU-5 (in-app route). Plan 09 keeps IU-1 transaction consolidation.
- **Not building:**
  - new status fields;
  - a new resolver;
  - a publish script;
  - new CI rows;
  - a "main only moves by release" rule. App `main` also deploys the hosted editor, so that rule would make every UI fix a release.

## Existing work and decision

The current state was mapped by seven read-only reviews, then a draft design was challenged by an independent reviewer whose cuts were accepted. Both are summarised in [inputs.md](inputs.md#planning-evidence).

The approach reuses what exists:
- the installed Astrid's own `identity` (`managed_by`, `release`);
- the existing `resolveUpdate`, the update status `reason`, `release-check.mjs` and the served-manifest canary.

Each is fixed where it is wrong, rather than replaced.

The owner's decisions (7 Nov 2026) are recorded in [inputs.md](inputs.md#owner-decisions) and are the source of truth that the decision table test enforces.

## Sequence and readiness

This plan (about 13.5–15.5 engineer-days) gives every normal install a working, honest Update now from Release 10, and a release number that only moves when a release is published, named as a version (`0.0.10` first) and recorded in an astrid-dev release log. The less common setups follow in [Plan 30](../30-update-everywhere/plan.md) (about 7–9 days), which is committed, not optional.

**Phase 1a: App and release versions, deployable this week (about 5.5–6 days).**
- Show Update now only when the installed Astrid's update status reports it can update itself. No Runtime reports it yet, so the button that has never worked disappears for everyone today, and turns on by itself with Release 10. Everyone else sees the reason and the command.
- Show the real refusal reason.
- Remove SetupBlock from the four update surfaces and from "Astrid on this computer".
- Move the chat update cards onto the shared decision (`resolveUpdate`, which already drives every other Update now button).
- Pinokio memory reads the Runtime's own identity; Pinokio fully local serves its update status instead of 501.
- `release-check.mjs` becomes one rule, run on pull requests and on push to `main`; `pin.mjs` stops changing `release`.

**Phase 1b: fully local Update now (about 1.5 days).** Re-enable the existing in-page updater the owner hid in `f2eca0bd5`, after a short spike to confirm it works.

**Phase 1c: Release 10 (about 6.5–7.5 days).**
- Merge the existing five-commit `reconcile` lane (Agent `b97c43db8` and its tests), with one Agent test that drives the Runtime's real update request through the real helper.
- The Runtime reports the capability and a reason on `GET /v1/update/status` (not in health `identity`, which would change the schema digest).
- A narrow test-only seam lets a hosted row update to a stand-in release through the in-app request; one such row per OS for a normal install.
- Freeze `public/install*` while 10 is qualified; publish 10 without marking it required.
- **Owner step:** turn on branch protection with the release check required on App `main`.

**Then:** [Plan 30](../30-update-everywhere/plan.md) finishes the remaining setups.

Owner decisions are recorded in [inputs.md](inputs.md#decisions-recorded-7-nov-2026). Recording this plan does not authorize implementation. Task cards: [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:**
  - Runtime `GET /v1/health` `identity` and `GET`/`POST /v1/update/status`;
  - the Agent update helper (`update_job.main` actions);
  - the App manifest `public/install-manifest.json` and bootstrap `public/install*`.
- **Produces:**
  - one update decision table in the App;
  - a Runtime↔Agent helper contract test;
  - a release guard in which a tuple or bootstrap change means release +1, and anything else leaves the release unchanged.

## Completion

Before publishing, up to three independent review rounds turn findings into routed tasks and complete them ([UR-R](tasks.md#ur-r-review-rounds)).

On the published release 10 tuple:
- a hosted row on every OS, Linux included without the systemd floor, updates from the installed candidate to a stand-in 11 through the in-app request, for a normal install, a fully local install and Pinokio;
- the decision table test passes for every install type × situation;
- `release-guard` is required on App `main`;
- an App-only merge leaves `release` unchanged, and a re-pin without a bump is refused.

**Negative cases:**
- releases 9 and earlier never show an enabled Update now;
- Pinokio never sees the installer command;
- "Astrid on this computer" has no actions;
- an installed version newer than astrid.haus shows no command.
