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
- **Deferred:**
  - dropping the systemd 254 floor on Linux;
  - update status for Pinokio fully local (its preview server answers 501);
  - a typed status contract;
  - [Plan 09](../09-install-and-update-confidence/plan.md) IU-1 transaction consolidation.

  This plan takes over Plan 09 IU-5 (in-app route).
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

Three slices, in order.

1. **App only, no release.** Stop showing a button that always fails, and stop silent re-pin releases.
   - Releases 9 and earlier show the command, with one line explaining it.
   - Show the real refusal reason.
   - Remove the setup block from update surfaces and from "Astrid on this computer".
   - Fully-local pages show their own command.
   - The Pinokio memory reads `identity`.
   - Add the decision table test, plus a required `release-guard` check and branch protection.
2. **Release 10.** Make the button work.
   - Merge the existing Agent `reconcile` handler, with a test that drives the Runtime's real update request through the real Agent helper.
   - The Runtime always gives a reason when an update is not available.
   - Hosted rows update through the button path.
   - `pin.mjs` stops changing `release`.
   - Remove the second pin tool and stale release files.
   - Publish 10.
3. **Deferred items** (see scope), each when needed.

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
- a hosted row per OS updates from the installed candidate to a stand-in 11 through the in-app request;
- the decision table test passes for every install type × situation;
- `release-guard` is required on App `main`;
- an App-only merge leaves `release` unchanged, and a re-pin without a bump is refused.

**Negative cases:**
- releases 9 and earlier never show an enabled Update now;
- Pinokio never sees the installer command;
- "Astrid on this computer" has no actions;
- an installed version newer than astrid.haus shows no command.
