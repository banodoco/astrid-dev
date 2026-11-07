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
- **Also included, not deferred:**
  - a Runtime capability that says the installed Astrid can update itself;
  - removing the systemd 254 floor so Linux updates in-app like Windows;
  - update status for Pinokio fully local (its preview server answers 501 today);
  - fully local Update now through the existing in-page updater;
  - typed contracts with tests at both broken boundaries: Runtime↔Agent helper actions, and Runtime update status↔App.

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

One coherent release, Release 10, with the App part allowed to ship first as permanent code:

1. **App.** Offer Update now only when the installed Astrid reports it can update itself (installs on 9 and earlier can't, and are told once why, with the command). Show the real refusal reason. Remove the setup block from update surfaces and "Astrid on this computer". Fully local uses the in-page updater. The Pinokio memory reads `identity`. Add the decision table test, a required `release-guard` check, and branch protection.
2. **Agent and Runtime.** Merge the existing `reconcile` handler. Add the capability and a reason whenever an update is not available. Remove the systemd 254 floor. Serve update status in Pinokio fully local. Add both contracts with tests.
3. **Release.** `pin.mjs` stops changing `release`; remove the second pin tool and stale release files; hosted rows on every OS update through the button path; publish 10.

Pending owner decisions are listed in [inputs.md](inputs.md#pending-decisions). Recording this plan does not authorize implementation. Task cards: [tasks.md](tasks.md).

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
