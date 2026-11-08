# Releases defined and published from astrid-dev

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

A release becomes one reviewed file in astrid-dev, and merging it is what publishes the release:

- **Definition.** Each release is a record at `releases/<N>.json`. It holds:
  - the number, version and kind (patch, minor or major);
  - whether the update is required, with a reason;
  - why it ships, and the plans it ships;
  - full commits for App, Agent and Runtime, plus the schema digest and tool versions.
- **Gate.** CI checks that the record is complete and consistent with the pinned commits before it can merge.
- **Protection.** Only the owner can approve a release, and publishing fails closed if that approval or the branch protection is missing.
- **Publish.** Merging writes one generated install manifest to a generated-only branch, the same way the vision feed is published.
- **App copy.** An App workflow syncs that manifest and the pinned install scripts into the App's one generated copy, which deploys. There is no App PR per release, and nobody edits those files by hand.
- **On screen.** Users see versions, such as "Astrid 0.0.10", and never release numbers.

**Not changed:** the Agent, Runtime and Pinokio. The integer `release` stays the ordering key on the wire and on users' disks. The installer URLs stay the same.

**Not building:**
- runtime proxying of the manifest by astrid.haus;
- signatures;
- a separate go-check bot;
- version arithmetic in the App;
- a markdown release log, since the record files are the log.

## Existing work and decision

The design reuses the vision pipeline (`vision-consumer-contract`, `publish-vision`), the App's existing manifest check and canary, and astrid-dev's fail-closed protection precedent (the claim bot). It takes over [Plan 29](../29-update-and-release/plan.md)'s UR-8b, UR-8c and UR-8d, and replaces UR-8's tuple guard. The evidence, alternatives and both independent reviews are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Phase 1, releases defined and published from astrid-dev:
1. **RL-0:** a worker setup script for the App, so workers can run its checks.
2. **RL-1a–RL-1d:** release records and their checks, the `release-contract` job across repositories, the fail-closed `publish-release` gate, and the Release skill publishing through records. RL-1a records the release live at start (expected 10) and proves its rendered manifest matches the served one.
3. **RL-2a–RL-2d:** a typed manifest schema shared by every App reader, the bootstrap move, the App's generated copy and sync (deleting `release-guard` and `pin.mjs` write mode in the same change), and the canary comparing with `release-published`. Syncing the legacy record changes only metadata.
4. **Review rounds (RL-R),** then **go live (RL-G)** through the Release skill, in a fixed order with the owner's settings changes between steps.

Phase 2, on screen: **RL-3**, users see versions. It ships with the next record after its own review round.

All work lands on `int/31-releases-from-astrid-dev` in astrid-dev and the App. Only the Release skill moves either branch to `main`.

This plan starts after [Plan 29](../29-update-and-release/plan.md) publishes Release 10 and the owner gives the go (owner, 8 Nov 2026). Its first record is the release live at that point, expected to be Release 10 = `0.0.10`. The next release is the first one published through this path. The owner turns on astrid-dev `main` protection before the first publish. The details are in [tasks.md](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

- **Consumes:**
  - the App's manifest checker (`checkManifest`, behind RL-2a's typed schema and `manifest-check`);
  - the served-manifest canary;
  - the Agent's `tools.validate_manifest`;
  - each product's `main` history.
- **Produces:**
  - `releases/<N>.json`, the record format and the release log;
  - the `release-published` branch, with one generated `install-manifest.json`;
  - the App's generated `public/install*` copy;
  - the release skill's publishing steps.

## Completion

The proof is these observable results:
- **Phase 1:**
  - The first release after this plan is published by merging an owner-approved `releases/<N>.json`, with no App PR, and the canary confirms the deployed manifest matches it.
  - A record that is incomplete, inconsistent or unapproved can't merge or publish. That includes a commit that isn't on its repository's `main`.
  - A hand edit to the App's generated files fails its PR.
- **Phase 2:** the hosted App and the local launcher show versions, such as "Astrid is up to date (0.0.11)", and never a release number.

Limits: the trust root becomes astrid-dev `main`, so its protection is a prerequisite. Releases go live within one sync interval plus a deploy.
