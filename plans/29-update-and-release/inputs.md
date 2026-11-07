# Inputs — One update path and release

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:**
- **Draft.** The owner asked for this project on 7 Nov 2026: one elegant update path, as simple as possible, with root-cause fixes, and the release process designed together with it.
- **Owner decisions** recorded below. The end state still needs the owner's selection on the pending decisions.
- **Next:** owner review of this draft.

**Prior art:**
- Seven read-only maps of the current state, at App `915bfa84`, Agent `709492fa`, Runtime `61e2c301`, launcher `d15c58b5` and astrid-dev `dd87b92`. The maps covered:
  - the App surfaces;
  - Settings and the decision logic;
  - the Plan 01 consent model;
  - the Runtime identity and update API;
  - installer install types;
  - Pinokio, fully local and source;
  - recorded decisions and docs.
- Key findings:
  - **Update now has never worked on a published install.** The Runtime and Agent disagree on the helper's first action (`reconcile`). No gate pressed the button, because hosted rows update through the CLI.
  - **The App works out install type from about 17 signals,** and has no unknown value.
  - **About 15 Runtime refusals return no reason.**
  - **`pin.mjs` and `release-check.mjs` make the release number count manifest edits.** The check runs only on push, and App `main` is unprotected. Release went from 1 to 9 in one merge, and the tuple changed several times under "Release 1".
  - **Plan 01's SetupBlock is shown on update and repair surfaces,** although its own ruling says existing installs get no choice flags.
  - **Fully-local pages can't use the in-app update,** because update routes are browser-door only.
  - **Docs describe three or four fully-local update paths,** and two of them are unused.

**Approach:** reuse and correct the existing pieces (`identity`, `resolveUpdate`, the status `reason`, `release-check.mjs`, the canary). Don't add new fields, a new resolver, a publish script or new CI rows.

**Challenge:** an independent high-judgment review of the first draft was accepted almost entirely. It contributed these items:
- **Cuts:** the new status fields, the new resolver, the publish script and new check, and the "main only moves by release" rule.
- **Corrections:**
  - releases 0–9 can never update in-app;
  - the `reconcile` handler exists unmerged;
  - repair is the plain install line, not Update now;
  - fully local needs its own path.
- **Gaps added:** systemd below 254 on Ubuntu 22.04 and Debian 12; the 501 status in Pinokio fully-local preview; bootstrap files as release bytes; downgrade via `--update`.
- **Rejected:** the review's deferrals and its release-number constant. The owner asked for a proper fix with no stopgaps, so the systemd floor, the Pinokio preview status and typed contracts are in scope, and a Runtime capability replaces the "release 9 or earlier" constant.

**Proof and limits:** see [plan.md](plan.md#completion). Existing installs on releases 9 and earlier keep the command path once; the button works only for installs from release 10.

## Owner decisions

From the owner, 7 Nov 2026 (session chat):
- **One path, no duplicates.** Updates follow the same path everywhere.
- **"Astrid on this computer" is status only.** Updates is the one place to act.
- **Pinokio users get only Update in Pinokio.**
- **Each install type sees only its own path.**
- **The primary action is Update now or Update in Pinokio,** with no middle ground. A manual command or agent instructions may remain as a secondary option.
- **Fix issues at their root,** and keep it as simple as possible.
- **The release process is part of this project.** Release 9, currently live, is kept; the next release is 10.

## Pending decisions

1. **Fully local:** planned as Update now through the existing in-page updater, following "Update now or Pinokio, no middle ground". Confirm.
2. **Pinokio fresh install consent.** Pinokio's terminal currently shows Plan 01's setup questions. Should Pinokio ask them, or accept the recommended choices, given that Pinokio manages start itself?
3. **Branch protection on App `main`.** This needs a repository admin.

## Source identities

Record exact base and donor SHAs at task start. Known donor: Agent `b97c43db8` (`reconcile` handler, unmerged).

## References

The maps and the review are working notes from the planning session. Their findings are summarised above, and each task card names the code it changes.
