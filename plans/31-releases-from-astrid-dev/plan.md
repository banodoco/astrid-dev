# Releases defined and published from astrid-dev

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

A release starts **in advance** as one living strategy document in astrid-dev, `releases/<N>.md`. That *same file* becomes the permanent release record when the owner approves it; there is no parallel planning document or handwritten release log.

- **Plan the release.** Start from [`releases/TEMPLATE.md`](../../releases/TEMPLATE.md). A draft has a short, memorable **highlight**, a longer **intent**, the **approach and trade-offs**, a list of included [plans](../../plans/index.md) with one-line reasons, and optionally the included pull requests that belong to no plan. It can be created and revised on `main` without publishing anything. An unassigned plan stays unassigned rather than being silently promised to a release. *This part is on `main` already.*
- **Release-led strategy.** [`strategy.md`](../../strategy.md) is a compact, ordered summary of the planned and published releases. The release file owns its rationale and scope; the catalog still owns project status, priority, estimates and ownership; gaps still own closure evidence. *Also on `main` already.*
- **Decide: finalize the same file.** A Final record keeps the strategy sections and adds the pinned payload: version and kind, an optional required-update reason, full App, Agent and Runtime SHAs, the schema digest, the tool, VibeComfy and lifecycle pins, and an informational Pinokio pin. The release number comes from the file. A CI job in astrid-dev runs the App's own checker on the proposed record: the payload's shape, that every commit is on its repository's `main`, and that the App's manifest check accepts what it renders.
- **Approve.** The owner's go is her GitHub approval on the pull request that turns the record Final, from an account no agent can act as. A script in the App, the *gate*, verifies that approval on that exact change, and that the record has not changed since. Changing a Final record un-approves it. astrid-dev itself gains no code-owner review, so draft briefs and progress pull requests stay as free as today.
- **Publish: a checked copy.** One App command renders the record into the App's `public/install*` files, and that goes to App `main` as a pull request. A required check, run from App code the owner reviews, accepts a change to those files only if it equals, byte for byte, the newest Final record's render and the gate passes. A hand edit, an older release, an unapproved record, a draft, and a different installer under an unchanged number all fail it. A draft edit, a strategy edit or the presence of future planned releases **can never publish an installer**.
- **On screen.** Users see versions, such as "Astrid 0.0.13", and never release numbers.

**Not changed:** the Agent, Runtime and Pinokio. The integer `release` stays the ordering key on the wire and on users' disks. The installer URLs stay the same. Draft briefs stay freely editable, and astrid-dev gains no required check, script or review rule: only one advisory workflow job, the Release skill's steps and the records themselves.

**Not building:**
- a generated `release-published` branch, a scheduled job with write access to App `main`, or any new credential (proposed cut, owner decision D2);
- runtime proxying of the manifest by astrid.haus;
- signatures;
- a separate go-check bot;
- version arithmetic in the App;
- a shared typed schema for every App manifest reader;
- a second Markdown release log or a separate release-planning document.

## Existing work and decision

The draft half of this plan landed between 8 and 11 Nov 2026: the template, the Release 12 brief, and the `release-documents` and `strategy-consistency` checks. [Plan 48](../48-one-record-model/plan.md)'s Phase 1 then moved those checks into one registry; this plan leaves them as they are and adds none. The code that reads, renders and verifies a Final record lives in the App, where the last write happens, and astrid-dev runs it in a job, as `vision-consumer-contract` already does for the vision feed. In the App it reuses `checkManifest`, the bootstrap and manifest tests and the served-manifest canary; it deletes `release-guard` and `pin.mjs`'s write mode. It takes over [Plan 29](../29-update-and-release/plan.md)'s UR-8b, UR-8c and UR-8d, and replaces UR-8's tuple guard.

The scope is **not yet accepted**. The 11 Nov 2026 re-read against current code kept astrid-dev as the source and changed how a decided release reaches the App, because the earlier transport could be written by anyone with push access. The evidence, alternatives, what the code settled, the reviews and the open owner decisions are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

**Starts after** [Plan 29](../29-update-and-release/plan.md) is on App `main`, Release 12 is published, [Plan 48](../48-one-record-model/plan.md)'s Phase 2 has landed (the owner's order of 11 Nov 2026), the owner has answered D1 to D7, and a `Run start` line names the accountable session. Release 12 is in its gate and still a Draft today. The first record is whichever release is live when the run starts.

Phase 1, the record and the checked copy:
1. **Contracts first.** Two tasks write tests before any code: what a Final record is, what it renders to and when the App accepts a copy (RL-3), and every way a record can be Final without the owner's approval (RL-4). A review stop (RS1) reads them. Beside them: the App worker setup (RL-0), one manifest check command (RL-1) and the bootstrap move (RL-2).
2. **Build to the tests:** the record reader and render (RL-5), the gate (RL-6), the copy guard with `CODEOWNERS` and the old pin path deleted (RL-7), the canary step (RL-8), astrid-dev's `release-contract` job (RL-9), the Release skill (RL-10), the live release prepared as the first record (RL-11), and the wording (RL-12t, RL-13t).
3. **Review** (R, at most two rounds), then **go live** (RL-G) through the Release skill, in a fixed order with the owner's settings change on the App between steps. Its last step re-publishes the live release from its record, which changes nothing users install.

Phase 2: users see versions (RL-14, RL-14t), and the temporary parts are deleted (RL-15).

All work lands on `int/31-releases-from-astrid-dev` in astrid-dev and the App. Only the Release skill moves either branch to `main`. Codex writes most of the work; the Claude session hosting it manages the run, commits, reviews and runs go-live ([dispatch notes](tasks.md#dispatch-notes)). Sizes are in [tasks.md](tasks.md#size). Recording this plan does not authorize implementation.

## Interfaces and handoff

- **Consumes:**
  - `releases/<N>.md` and the landed draft checks, at the revision each task records;
  - the App's `checkManifest` and its served-manifest canary;
  - the Agent's `tools.validate_manifest`, by git at each record's Agent commit;
  - each product's `main` history, for ancestry.
- **Produces:**
  - `releases/<N>.md` as a Final record with a pinned payload;
  - in the App: `scripts/installer/install-copy.mjs render | check-record | verify | write`, `scripts/installer/release-approval.mjs` (the one answer to "is this release approved?", which the guard and the Release skill both call), `scripts/installer/manifest-check.mjs`, the required `install-copy-guard` check in its own workflow, `CODEOWNERS`, and bootstrap sources under `scripts/installer/bootstrap/`;
  - the advisory `release-contract` job on astrid-dev;
  - an install manifest with three added keys, `version`, `versions` and `app`, that older Apps and Agents ignore;
  - the Release skill's eight publishing steps.
- **Limits:** the hosted App's code reaches `main`, and deploys, before the installer it was qualified with is published; a candidate is qualified on a copy written from its proposed payload, and the published copy must have the same SHA-256; the Agent's `regenerate_runtime_pins.py` still edits an App checkout's manifest, and its output is not what ships.

## Completion

The proof is these observable results:
- **Phase 1:**
  - A future release can be drafted, revised and linked from `strategy.md` without a manifest change, an installer publication or any SHA. *True today;* it stays true.
  - The first release after this plan is published by an owner-approved change of its existing draft to Final, then one generated App pull request whose check passes, and the canary confirms the deployed copy matches the record.
  - Each of these fails, shown by a test and, where marked in [tasks.md](tasks.md), live: a Final record with a commit that is not on its repository's `main`; a Final record with no approval from a release approver on its final head; a Final record changed after approval, or merged with content the approved head did not have; a hand edit to the App's generated files; a copy of anything but the newest Final record; a changed installer under an unchanged release number.
- **Phase 2:** the hosted App and the local launcher show versions, such as "Astrid is up to date (0.0.13)", and never a release number.

**Limits.** The approval is only as strong as the approving account's separation from the agents, the agents' account having no way around App `main`'s rules (D1), and those rules (O-1). The plan protects the installer files, the workflows that check them and the two files that serve them; it does not stop someone who controls the hosted App's deployment or serves the installer by another route, though the canary would report different bytes within a day. Without D3 a it does not stop a deliberate change to the guard itself. The gate's positive path first runs at go-live, on a release that is already live.
