# Releases defined and published from astrid-dev

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

A release starts **in advance** as one living strategy document in astrid-dev, `releases/<N>.md`. That *same file* becomes the permanent, immutable release record when published; there is no parallel planning document or handwritten release log.

- **Plan the release.** Start from [`releases/TEMPLATE.md`](../../releases/TEMPLATE.md). A draft has a short, memorable **highlight**, a longer **intent/outcome**, the **approach and trade-offs**, and a list of included [plans](../../plans/index.md) with one-line reasons. Identify dependencies and boundaries; adjust scope as evidence comes in, before freezing. It can be created and revised on `main` without publishing anything. An unassigned plan stays unassigned rather than being silently promised to a release.
- **Release-led strategy.** [`strategy.md`](../../strategy.md) is a compact, ordered summary of the planned and published releases, linking to their documents and included plans. The release file owns its rationale and scope; the strategy page explains the sequence, not a second set of project descriptions. The catalog still owns project status, priority, estimates and ownership; gaps still own closure evidence.
- **Finalize the same file.** A ready-to-publish record keeps the strategy sections and adds the pinned publication payload: release integer, version and kind, optional required-update reason, full App/Agent/Runtime SHAs, schema digest, tool versions and any informational Pinokio pin. The final transition is owner-approved; after publication the file is append-only history (no editing or deleting the released record).
- **Gate.** CI validates draft structure, plan links and consistency with the strategy summary without demanding pins for drafts. Only an explicit draft-to-final transition with a complete, coherent payload can trigger publication; it checks the pinned commits, monotonic release number and owner approval. A draft edit, a strategy edit, or the presence of future planned releases **must never publish an installer**.
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
- a second Markdown release log or a separate release-planning document, since the release files themselves are both living plans and the eventual ledger.

## Existing work and decision

The design reuses the vision pipeline (`vision-consumer-contract`, `publish-vision`), the App's existing manifest check and canary, and astrid-dev's fail-closed protection precedent (the claim bot). It takes over [Plan 29](../29-update-and-release/plan.md)'s UR-8b, UR-8c and UR-8d, and replaces UR-8's tuple guard. The evidence, alternatives and both independent reviews are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Phase 1, releases defined and published from astrid-dev:
1. **RL-0:** a worker setup script for the App, so workers can run its checks.
2. **RL-1a–RL-1d:** a release-file template, draft/strategy checks, final-record checks, the `release-contract` job across repositories, the fail-closed `publish-release` gate, and the Release skill publishing through final records. RL-1a also imports the release live at start as a historical record and proves its rendered manifest matches the served one. Earlier published releases are backfilled only from real receipts, never invented.
3. **RL-2a–RL-2d:** a typed manifest schema shared by every App reader, the bootstrap move, the App's generated copy and sync (deleting `release-guard` and `pin.mjs` write mode in the same change), and the canary comparing with `release-published`. Syncing the legacy record changes only metadata.
4. **Review rounds (RL-R),** then **go live (RL-G)** through the Release skill, in a fixed order with the owner's settings changes between steps.

Phase 2, on screen: **RL-3**, users see versions. It ships with the next record after its own review round.

All work lands on `int/31-releases-from-astrid-dev` in astrid-dev and the App. Only the Release skill moves either branch to `main`.

This plan was sequenced after [Plan 29](../29-update-and-release/plan.md) and the owner's go (decision recorded 8 Nov 2026). The initial legacy record must describe **whichever release is actually live when implementation starts**; the earlier estimate that it would be Release 10 is historical, not an instruction to overwrite the newer releases. The next new release is the first one published through this path. The owner turns on astrid-dev `main` protection before the first publish. The details are in [tasks.md](tasks.md). Recording this plan does not authorize implementation.

## Interfaces and handoff

- **Consumes:**
  - the App's manifest checker (`checkManifest`, behind RL-2a's typed schema and `manifest-check`);
  - the served-manifest canary;
  - the Agent's `tools.validate_manifest`;
  - each product's `main` history.
- **Produces:**
  - `releases/<N>.md` (draft strategy → final release ledger), its template, CI structure/strategy checks and publishable record format;
  - the `release-published` branch, with one generated `install-manifest.json`;
  - the App's generated `public/install*` copy;
  - the release skill's publishing steps.

## Completion

The proof is these observable results:
- **Phase 1:**
  - A future release can be drafted, revised and linked from `strategy.md` without a manifest change, installer publication or required full SHAs; CI rejects missing required sections, broken plan links and a strategy row that diverges from the release document.
  - The first release after this plan is published by an owner-approved transition of its existing draft `releases/<N>.md` to final, with no App PR, and the canary confirms the deployed manifest matches it.
  - A final record that is incomplete, inconsistent or unapproved can't merge or publish. That includes a commit that isn't on its repository's `main`. A published release document cannot be silently rewritten or removed.
  - A hand edit to the App's generated files fails its PR.
- **Phase 2:** the hosted App and the local launcher show versions, such as "Astrid is up to date (0.0.11)", and never a release number.

Limits: the trust root becomes astrid-dev `main`, so its protection is a prerequisite. Releases go live within one sync interval plus a deploy.
