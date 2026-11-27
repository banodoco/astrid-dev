# Releases defined and published from astrid-dev

**Project:** Releases defined and published from astrid-dev

**Goal:** Each release starts as a living strategy brief linked from the release-led roadmap, then becomes one owner-approved immutable record whose finalization publishes the checked product tuple, with versions shown to users.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD — residual only; prior whole-plan estimate 12.5 (9.5–18) engineering days

**Waiting on:** [Plan 58](../58-strategy-from-releases/plan.md) is done; reuse the existing release briefs, parser and strategy view. [SC-31](https://github.com/banodoco/astrid-dev/blob/25ced2a35b4677532911aaa61127fc9452be59b7/plans/31-releases-from-astrid-dev/evidence/release-16-scoping/SC-31.md) identifies remaining semantic-version display, protected exact-tuple finalization, generated manifest/bootstrap cutover and served readback. Await owner controls, scoped dispatch and P29 status seam; no separate publication.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

A release starts **in advance** as one living strategy document in astrid-dev, `releases/<N>.md`. That *same file* becomes the permanent, immutable release record when published; there is no parallel planning document or handwritten release log.

- **Plan the release.** Start from [`releases/TEMPLATE.md`](../../releases/TEMPLATE.md). A draft has a short, memorable **highlight**, a longer **intent/outcome**, the **approach and trade-offs**, and a list of included [plans](../../plans/index.md) with one-line reasons. Identify dependencies and boundaries; adjust scope as evidence comes in, before freezing. It can be created and revised on `main` without publishing anything. An unassigned plan stays unassigned rather than being silently promised to a release.
- **Release-led strategy.** [`strategy.md`](../../strategy.md) draws its repeated release material from release briefs; the release file owns rationale and scope. The catalog owns project status, priority, estimates and ownership; gaps own closure evidence ([hierarchy](../../docs/contribution-workflow.md#review-the-strategy)).
- **Prepare a tentative testing build.** A contributor or their coding agent can discover the designated active testing release (or specify a release or recorded snapshot), resolve its latest coherent release-branch tuple, and locally generate and validate its manifest and matching Windows/Linux installers without a maintainer, pre-created bundle, write credential or Final transition. Derive dependency pins from their owners; do not combine independent floating heads. Freeze the full source identities, artifact hashes and qualification status per session; fresh sessions resolve again and resumed sessions reuse their receipt. Multiple snapshots may share a release integer. Keep tentative use opt-in and separate from production publication. Update the existing [tester brief](../../releases/15/tester-run/tester-brief.md) and [technical matrix](../../releases/15/tester-run/test-matrix.md) into a permanent reusable testing entrypoint with platform adapters and release-specific focus, using platform-neutral filenames and preserving consent/reporting safeguards. Support full-stack testing of the exact compatible App commit through its local editor route, with real browser connection, timeline edits/save/reopen, agent setup and first project-aware chat, alongside installed-side generation; explicitly separate served App from pinned App evidence. See RL-1e.
- **Finalize the same file.** A ready-to-publish record keeps the strategy sections and adds the pinned publication payload: release integer, version and kind, optional required-update reason, full App/Agent/Runtime SHAs, schema digest, tool versions and any informational Pinokio pin. The final transition is owner-approved; after publication the file is append-only history (no editing or deleting the released record).
- **Gate.** CI validates draft structure and plan links without demanding pins; strategy material is generated from briefs. Only an explicit draft-to-final transition with a complete, coherent payload can trigger publication; it checks the pinned commits, monotonic release number and owner approval. A draft edit, a strategy edit, or the presence of future planned releases **must never publish an installer**.
- **Protection.** Only the owner can approve a release, and publishing fails closed if that approval or the branch protection is missing.
- **Publish.** Merging writes one generated install manifest to a generated-only branch, the same way the vision feed is published.
- **App copy.** An App workflow syncs that manifest and the pinned install scripts into the App's one generated copy, which deploys. There is no App PR per release, and nobody edits those files by hand.
- **On screen.** Users see versions, such as "Astrid 0.0.10", and never release numbers.

**Not changed by the publication pipeline:** the Agent, Runtime and Pinokio. If a same-release tentative snapshot update exposes an installer defect, route the smallest supported repair to Plans 09/29/30; never fake a release number or bypass update safety. The integer `release` stays the ordering key on the wire and on users' disks. The installer URLs stay the same.

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
4. **RL-1e:** self-service tentative build preparation and the permanent tester guide, using the same manifest renderer and validation logic before retiring the old pin writer.
5. **Review rounds (RL-R),** then **go live (RL-G)** through the Release skill, in a fixed order with the owner's settings changes between steps.

Phase 2, on screen: **RL-3**, users see versions. It ships with the next record after its own review round.

All work lands on `int/31-releases-from-astrid-dev` in astrid-dev and the App. Only the Release skill moves either branch to `main`.

**Plan 58 contract.** Plan 58 provides the release template, draft checks, `records.release_brief`, generated strategy and issue lists. RL-1a uses that reader, keeps final-record checks and the legacy record, and refuses changed or deleted finalized records, including frozen issues. Releases 12 and 13 remain to be made Final here (D5). Owner review gates Final; ordinary draft issue pulls remain unblocked.

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
  - the release skill's publishing steps;
  - a permanent tester entrypoint and read-only tentative-build preparation with reproducible manifest/installer receipts.

## Completion

The proof is these observable results:
- **Phase 1:**
  - A future release can be drafted, revised and linked from `strategy.md` without a manifest change, installer publication or required full SHAs; CI rejects missing required sections, broken plan links and invalid generated strategy structure.
  - The first release after this plan is published by an owner-approved transition of its existing draft `releases/<N>.md` to final, with no App PR, and the canary confirms the deployed manifest matches it.
  - A final record that is incomplete, inconsistent or unapproved can't merge or publish. That includes a commit that isn't on its repository's `main`. A published release document cannot be silently rewritten or removed.
  - A hand edit to the App's generated files fails its PR.
  - A Windows and a Linux tester independently prepare and install an unpublished coherent snapshot without repository write access or a pre-made bundle, verify the active identities, produce a first result and report it. Both platforms also open the exact local App with that tuple, perform a real edit and save/reopen, and exercise a supported agent setup/chat journey (credentials and spending only with consent); report blocked/skipped cases separately, never substitute a fake backend. A fresh session resolves newer coherent inputs; replay reproduces the old snapshot. A same-release-number update succeeds through the supported route or reports an explicit routed blocker. Wrong release, ambiguous discovery, missing/stale/mixed pins and invalid tools fail clearly. Tentative preparation cannot change the public manifest, update feed, required policy or publication gate; production still requires main ancestry and owner approval.
- **Phase 2:** the hosted App and the local launcher show versions, such as "Astrid is up to date (0.0.11)", and never a release number.

Limits: the trust root becomes astrid-dev `main`, so its protection is a prerequisite. Releases go live within one sync interval plus a deploy.


## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

deliver first-minor publication and visible version inside R16; reuse P58. Replace obsolete `int/31`/whole-P29-on-main sequencing with approved release branches and row-level joins. Proposed D-SYN-1 would reconcile green-gate language only after explicit owner agreement; never call a ceiling full green.
