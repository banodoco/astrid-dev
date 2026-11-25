# Tasks — Releases defined and published from astrid-dev

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change. An N task that misses the same acceptance check twice re-routes to X.

**Where work lands (proposed R16):** use the existing Lead-approved release branches and record each actual base SHA. Prepare independent work against the current producer; land consumers after the specific reviewed Plan 29 status/manifest seam. Only the authorized release process and owner may promote publicly at RL-G.

**R16 sequencing (proposed):** RL-3 version display lands and is independently reviewed before the first R16 Final. Early legacy adoption and nonpublishing rehearsal precede RL-G; RL-G is the single final owner-authorized transition. Retain the new RL-1e tester workflow and its dependencies. Estimates remain in the [catalog](../index.md).

**Proof labels.** *Local* runs in a single-repository worker session at the task's candidate SHA. *Hosted* is the named CI job on the task's PR into `int/31`, judged by its inner step, not the run's status. Proof that needs another repository's files fetches them by git at a pinned commit; nothing reads `raw.githubusercontent.com` from a worker session.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner** | | | | | |
| Protect astrid-dev `main` (code-owner review, stale approvals dismissed, `release-contract` required) and `release-published` (no force-push or deletion) | owner | — | astrid-dev repository settings | Settings show both rulesets | [ ] |
| O-2 App publication controls | owner | RL-2c | App repository settings and generated sync | Verify effective protections and an exact generated-only writer satisfying all required checks; retain the old guard until the replacement is effective. No blanket bypass; owner explicitly resolves any alternative and deployment interval | [ ] |
| **Build: worker environment** | | | | | |
| RL-0 App worker setup script | N | — | astrid-dev `env/app-setup.sh` (new), `env/smoke.sh` (`app` mode), `env/README.md` table; App `scripts/worker-env/{app-setup.sh,smoke.sh}` (copies) | Local, App worker on `int/31`: `bash scripts/worker-env/smoke.sh app scripts/installer/manifest.test.mjs` exits 0 and runs that one file; with a Node other than 20.19.x first on `PATH` it exits 3. `cmp env/app-setup.sh <App>/scripts/worker-env/app-setup.sh` is silent | [ ] |
| **Build: astrid-dev records and publishing** | | | | | |
| RL-1a Living release briefs, draft checks, final record checks and the legacy record | N | — | astrid-dev `releases/TEMPLATE.md`, `releases/<N>.md` (living drafts → final records), `scripts/records.py:release_brief` (reader), `scripts/release_record.py` (`check`, `render`), `scripts/test_release_record.py`; import the actually live legacy record at start; closes astrid-dev PR #82 unmerged (its cases move here) | Local: `python3 scripts/astrid_dev.py check` and `python3 -m unittest discover -s scripts -p test_release_record.py` pass. A draft with no SHAs is accepted and cannot render or publish. Negative cases refuse a missing highlight/intent/approach, invalid plan link, duplicate plan, wrong release number, malformed final payload, a gap in finalized numbers, wrong version step for kind, non-40-character SHA, required update without a reason, a changed or deleted finalized record including its frozen issue list, and a final record whose pins disagree with its included plans. The actual live legacy final record renders a manifest matching the served one, apart from the four intentionally added metadata fields | [ ] |
| RL-1b `release-contract` job: the record against the real consumers | X | RL-1a, RL-2a | astrid-dev `.github/workflows/docs.yml` (`release-contract`), `scripts/release_record.py` (`ancestry`) and its test | Hosted, `release-contract` on the task PR: PASS for the legacy record. Hosted, one throwaway draft PR into `int/31` per case, closed unmerged, each FAIL with its reason: an `app`, `agent` or `runtime` SHA that exists but is not an ancestor of that repository's `main` (a real open-PR head commit); a `runtime` that differs from the Agent's `runtime.lock.json`; a wrong `runtime_schema_digest`; bootstraps at `app` whose uv or Python pin differs from `tools`; `tools` that the record's Agent or the previous record's Agent `tools.validate_manifest` rejects (Node `20.19.5`) | [ ] |
| RL-1c `publish-release` finalization and fail-closed gate | S | RL-1b | astrid-dev `.github/CODEOWNERS` (new), `.github/workflows/docs.yml` (`publish-release`), `scripts/release_gate.py` and `scripts/test_release_gate.py` (new) | Local: `python3 -m unittest discover -s scripts -p test_release_gate.py` covers refusals from recorded API response shapes, including a Draft or strategy-only PR causing no publication, a Final without owner approval, and attempts to edit a previously finalized release. Local, live public API, read-only: `python3 scripts/release_gate.py --repo banodoco/astrid-dev --check-only --commit <a merged main commit with no code-owner approval>` exits non-zero and names both "main has no code-owner ruleset" (today) and "no code-owner approval on the final head". The positive path first runs in RL-G | [ ] |
| RL-1d Release skill plans, finalizes and publishes through release documents | N | RL-1c, RL-2c | astrid-dev `skills/capabilities/astrid-dev-release/SKILL.md` (installer-tuple lane and publish steps) | Local: `python3 scripts/check_docs.py` passes; `grep -n -e pin.mjs -e release-guard -e "release guard" skills/capabilities/astrid-dev-release/SKILL.md` prints nothing; the skill names draft, final/decided, published and live, the sync as its own step, and the RL-G order; drafting never implies a release | [ ] |
| **Build: App generated copy** | | | | | |
| RL-2a Typed install-manifest schema and one check CLI | X | RL-0 | App `scripts/installer/manifest-schema.mjs` and `scripts/installer/manifest-check.mjs` (new) and their test; `scripts/installer/pin.mjs` (`--check` CLI removed, `checkManifest` kept); `scripts/installer/manifest.test.mjs`; `src/shared/lib/updates/updateStatus.ts` (`readManifest`); `config/vite/localUpdateStatus.ts` (manifest parsing) | Local: `node --test scripts/installer/manifest-schema.test.mjs scripts/installer/manifest.test.mjs` passes, accepting App `main`'s served manifest unchanged and the RL-1a rendered manifest, and rejecting a bad `versions` entry, a non-integer `release` and a short `app.sha`. Local: `npx vitest run --config config/testing/vitest.config.ts src/shared/lib/updates/updateStatus.test.ts config/vite/localUpdateStatus.test.ts` passes. `git grep -n -e "--check" -- scripts/installer/pin.mjs scripts/installer/manifest.test.mjs` prints nothing | [ ] |
| RL-2b Bootstrap source moves out of `public/` | N | RL-0 | App `public/{install,install.sh,install.ps1}` → `scripts/installer/bootstrap/` (`public/` keeps identical copies until the first sync); `scripts/installer/{fixture.mjs,bootstrap.test.mjs,bootstrap-powershell.test.mjs,manifest.test.mjs}` paths | Local: `node --test scripts/installer/bootstrap.test.mjs` passes against the moved source, and `cmp` of each source with its `public/` copy is silent. Hosted: `Windows installer` runs on the task PR (its `scripts/installer/**` filter) and its test step passes | [ ] |
| RL-1e Self-service tentative builds and reusable tester guide | X | RL-1a, RL-1b, RL-2a, RL-2b | astrid-dev shared renderer/contract, read-only preparation command, existing tester brief and technical matrix migrated to a permanent cross-platform entrypoint; App/Agent installer interfaces | Local/hosted: discover active or explicit release, resolve exact coherent release-branch inputs, render and validate both platform artifacts, receipt and hashes without writes; replay old snapshot and resolve a newer one; refuse wrong release, mixed/missing pins, ambiguous discovery and invalid tools. Real Windows and Linux: install/update with consent, verify active identity, first creation, pinned local App connect/edit/save/reopen and real agent setup/chat (with consent), issue and cleanup; exercise two same-number snapshots, route any supported-update blocker. Tentative output never changes production artifacts or approval/ancestry gates | [ ] |
| RL-2c `release-sync`, the copy guard, and the old pin path deleted | X | RL-1a, RL-2a, RL-2b, RL-1e | App `.github/workflows/release-sync.yml` and `scripts/installer/release-sync.mjs` and its test (new); `.github/workflows/test.yml` (`install-copy-guard` replaces `release-guard`); deletes `scripts/installer/release-guard.mjs`, its cases in `release.test.mjs`, `pin.mjs` write mode (`pin`, `applyRequiredPin`, CLI) and the `README.md` pin line | Local: `node --test scripts/installer/release-sync.test.mjs` passes. It syncs the RL-1a rendered legacy manifest into a temp clone of App `int/31`, and the diff touches only `version`, `versions`, `app` and `source`. Each of these refuses to commit: a `source` that is not an ancestor of astrid-dev `main`; a `source` with no Final record for `release`; an `app` that is not an ancestor of App `main`; a manifest that fails `manifest-check`. Local: `node scripts/installer/release-sync.mjs` with `RELEASE_SYNC_ENABLED` unset exits 0 and writes nothing. Hosted: on a throwaway draft PR that edits `public/install.sh`, `install-copy-guard` FAILs; on the task PR it passes. `git grep -n -e release-guard -e applyRequiredPin` prints nothing | [ ] |
| RL-2d Canary also compares with `release-published` | N | RL-2c | App `scripts/installer/served-manifest.mjs`, its case in `release.test.mjs`, `.github/workflows/served-manifest-canary.yml` | Local: `node --test scripts/installer/release.test.mjs` passes, with a case where the served manifest matches the deployed copy but not `release-published`, which fails. The live run is in RL-G | [ ] |
| **Review: before the first release through this path** | | | | | |
| RL-R Independent reviews of the integrated pipeline | S | RL-0 to RL-2d, RL-1e, RL-3 | all Plan 31 scopes (read-only review) | At most the owner's agreed number of rounds (see [inputs](inputs.md#planning-evidence)). Findings become rows `RL-R<round>.<n>` directly below this one, done before the next round | [ ] |
| **Publish** | | | | | |
| RL-G Go live through the Release skill (owner's go) | release | RL-R, RL-3, both owner rows, accepted product gates and exact owner approval | App and astrid-dev authorized release paths | Rehearse legacy adoption without publication; verify effective controls, exact approved source and evidence, coherent deployment interval and generated-only sync before the Final transition. Owner explicitly authorizes go; verify all served manifest and bootstrap bytes and deployment identity after publication | [ ] |
| **Version display for the first R16 minor** (proposed to land before RL-R and RL-G) | | | | | |
| RL-3 Users see versions, not release numbers | N | RL-1a, RL-2a and settled status seam | App `src/shared/lib/updates/updateStatus.ts`, `src/shared/components/SettingsModal/sections/AstridUpdatesSection.tsx`, `src/shared/components/RuntimeConnection/QuietUpdateNotice.tsx`, `config/vite/localUpdateStatus.ts`, and their tests | Local: `npx vitest run --config config/testing/vitest.config.ts src/shared/lib/updates/updateStatus.test.ts src/shared/components/SettingsModal/sections/AstridUpdatesSection.test.tsx src/shared/components/RuntimeConnection/QuietUpdateNotice.test.tsx config/vite/localUpdateStatus.test.ts` passes, showing "Astrid is up to date (0.0.10)", "Update available: Astrid 0.0.11" and "Installed 0.0.9", hosted and local launcher. Each test feeds the manifest RL-1a renders, not hand-written fields. `git grep -n -e 'Release ${' -e 'Release {' -- src` prints nothing | [ ] |

**Overlap with other projects:**
- **[Plan 48](../48-one-record-model/plan.md) Phase 1 is on `main` (11 Nov 2026), so re-plan these cards against it before the run starts:**
  - *Checks are registered.* Draft structure and generated strategy checks already exist; RL-1a reads `records.release_brief` and registers its final-record rules in `scripts/checks.py`. Its local proof is `python3 scripts/astrid_dev.py check`.
  - *The golden file pins every check's output.* A new rule adds its own fixture and lines to `scripts/fixtures/golden.txt`; no existing line or test is edited to get green.
  - *The `documentation` job runs only `astrid_dev.py check`,* and its name is a required check on `main`. RL-1b and RL-1c add their own jobs beside it and don't rename it.
  - *`main` is protected already,* but not as the owner row needs: a pull request and the `documentation` and `vision-consumer-contract` checks are required, with no approval and no code-owner review. Managers auto-merge progress PRs under that rule, so when code-owner review is turned on, `CODEOWNERS` must cover only the paths RL-1c names, or every plan's progress PR starts waiting for the owner.
  - *The release template has an optional `## Included pull requests` section* that the Release skill fills when it takes stock of open pull requests. RL-1a's template and draft checks keep it, and RL-1d keeps that step.
  - *Plan 48's Phase 2 moves status and owner out of the catalog into each `plan.md`.* Whichever of that phase and this plan starts second re-reads the other's result first, because the release and strategy checks read the catalog.
  - *Before a manager starts,* the pack needs what the templates now ask for: a test inventory in this file, a `Run start` line naming the accountable session, and the manager's route (S by the orchestrate skill's table: a release, two repositories and a trust-root task).
- RL-2 and RL-3 change App files that Plan 29 also changes (UR-8's guard, UR-1 and UR-3's update screens), so this plan starts after Plan 29 is on `main`.
- RL-1d edits the Release skill, which the green-mains rule also edits after Release 10. Start RL-1d from whichever lands first.
- Plan 30 touches the update screens (UR-17). Check its scope at start; if it touches `QuietUpdateNotice.tsx` or `localUpdateStatus.ts`, sequence RL-3 against it.

## Task details

### RL-0 App worker setup
- `app-setup.sh` checks Node 20.19.x and runs `npm ci --legacy-peer-deps` in the checkout. It exits 3 on an environment problem, like the other scripts in `env/`.
- `smoke.sh app <file>` runs setup and then `node --test <file>`.
- The App copies live in `scripts/worker-env/`, the same as the Agent's.

### RL-1a Records
- **One Markdown document, two phases:**
  - Draft: `Release` number, `State: Draft`, optional `Kind`, title, `Highlight`, `Intent`, `Approach`, `Included plans` (linked plan files with contributions, or `None yet`), optional pull requests and issues, and `Publication: Not pinned.`. The strategy generator pulls repeated material from the brief. Drafts may change on `main` and never enter publish output.
  - Final: the same sections, `State: Final` and a publication JSON block with `version`, `kind`, `required` (null or a reason), full SHAs for `app`, `agent`, `runtime`, `runtime_schema_digest`, `tools` and optional informational `pinokio`. The release number, strategic `why` and `plans` are derived from the document, not duplicated in a second hand-edited record. The render output is the existing App-compatible manifest. CI refuses invalid or missing pins and changes to an already finalized record.

  The owner's go is the GitHub approval on the PR, not a field.
- **Legacy record:** the release actually live when this plan starts, without assuming the old expected number 10 is still current. `app` is the deployed App commit the canary last passed for. `versions` maps 1 to N as `0.0.<n>`, so every install that exists today has a version to show (owner to confirm, see inputs).
- **Checks:** draft structure and generated strategy validation belong to documentation CI; final-record shape and refusal of changed or deleted finalized records, including frozen issue lists, belong to `check`. Coherence across repositories (Runtime against Agent lock, digest, ancestry, tools) belongs to RL-1b, through the App's own checker, so no digest code is copied into Python. Finalization is a distinct transition; regular documentation merges never publish.
- **`render`** writes today's manifest shape plus `version`, `versions`, `app.sha`, `required.release` and `source`. It takes `source` as an argument.

### RL-1b `release-contract`
- **Shape:** the same as `vision-consumer-contract`, and it needs `documentation`.
- **The App ref follows the PR base:**
  - a PR into `main` checks against App `main`;
  - a PR into `int/<project>` checks against App `int/<project>` when that branch exists, and App `main` otherwise.

  This lets the contract be proven before Release, and it is why Release merges App first.
- **What it runs:**
  - App `manifest-check` (RL-2a) on the rendered manifest, with the bootstraps from the record's `app`;
  - `astrid.installer.tools.validate_manifest` from the record's Agent and from the previous record's Agent, each fetched by git at its SHA and installed like `env/agent-setup.sh`.
- **Ancestry:** "reachable" is not enough, because GitHub serves fork and PR commits through the parent repository. Each SHA must be an ancestor of its repository's `main` (`git merge-base --is-ancestor` on a `--filter=blob:none` fetch).
- **Route note (X, not N):** it spans three repositories and its proof is hosted-only, so a guess repeats slowly. With a fully specified card it could be N. Keep X unless the ambiguity pass removes every open choice.

### RL-1e Self-service tentative builds
- One renderer and contract checker; separate preview input resolution/release-branch ancestry from production Final authorization/main ancestry. Discover the active testing release from existing release records and live/active release state; do not pick the highest planned number or maintain a second release list. If multiple targets are plausible, ask for explicit selection. Support explicit release and recorded snapshot.
- Resolve immutable App and Agent sources, derive Runtime, VibeComfy, lifecycle and other pins from owning locks, and validate tool/pack and installer compatibility. Prefer the latest coherent integrated snapshot; if the App lags, disclose it and distinguish an explicitly selected installed-side-only exploratory build from full-stack evidence. Never silently combine floating heads. No write access or pre-existing preview bundle required.
- Save the manifest, matching bootstrap(s), SHA-256 hashes, exact tuple, qualification status and test scope as a session receipt. Fresh sessions resolve again; resumed sessions replay. Prove same-release snapshot updates through the supported path, routing missing behavior to Plans 09/29/30 without changing release integers or weakening verification.
- Update the [current tester brief](../../releases/15/tester-run/windows-tester-brief.md) and [technical matrix](../../releases/15/tester-run/windows-test-matrix.md) into the standing Windows/Linux methodology; preserve existing links. Reuse the [interim preparation route](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/releases/15/tester-run/prepare-build.md), existing setup/generation skills and issue intake. Include standing and release-specific checks, free-form use, consent, exact evidence, cleanup and rollback. Use the App's supported fully-local launcher for the exact compatible App SHA; no hosted-source fallback or fake backend. See the [Release 15 frontend cases](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/releases/15/tester-run/frontend-testing.md). Make UI connection, timeline persistence and agent setup/chat testable on both Windows and Linux; separately record served-App observations and native full-stack evidence. Keep public update policy, publication authority and production output unchanged.

### RL-1c `publish-release`
- **Base:** copy `publish-vision`, including the superseded-run guard. Publish only when a new, owner-approved Final record has been merged to `main`; drafts and strategy changes are ignored, even when they are newer by release number. A push that leaves published bytes unchanged writes nothing.
- **Gate:** fail closed like the claim bot, using only reads a public repository allows. The gate checks:
  - an active ruleset on `main` requires a pull request with code-owner review, with stale approvals dismissed (`GET /repos/{repo}/rules/branches/main`);
  - the commit that transitioned the intended record to Final belongs to a merged PR;
  - that PR has an `APPROVED` review from the owner authorized for the Final transition, whose `commit_id` is the PR's final head.

  The gate checks the PR that finalized the record, not whatever push triggered the run.
- **Owner review:** protect the Final transition with owner review without requiring owner review for every edit under `releases/`; ordinary draft issue-list pulls remain unblocked. The owner also owns `.github/CODEOWNERS`, `.github/workflows/docs.yml`, `scripts/release_record.py` and `scripts/release_gate.py`, which decide what gets published. Implement and prove a transition-specific gate, rather than making the owner code owner of all release drafts.
- **States:**
  - draft: the unpinned strategy document can evolve on `main` without publishing;
  - decided: the owner-approved Final record is on `main`;
  - published: `release-published` has the finalized record;
  - live: the canary passes for a deployed commit with that release.

  The release skill reads these. There is no new state file.
- **Route note (S):** this is the trust root for code that users run, and it can't run end to end before RL-G. The claim bot is a working precedent, so X is arguable, but a wrong gate publishes unapproved installers to every user.

### RL-2a Manifest schema
- **Why:** the published manifest crosses astrid-dev → App → Agent installers, and today each reader parses it by hand.
- **One Zod schema:** it holds today's fields plus optional `version`, `versions`, `app.sha` and `source`. It is `passthrough`, so that a field added later doesn't break an App that is already deployed.
- **`manifest-check <file> [--bootstrap-dir <dir>]`:** runs the schema, then `checkManifest`, then the uv and Python pin agreement with the bootstraps that `manifest.test.mjs` checks today.
- **Burn down:** `updateStatus.ts` and `localUpdateStatus.ts` parse through the schema, and their hand-written checks are deleted in the same change.
- **Route note (X):** the strictness of a contract that old and new Apps both read, with two parsers to replace.

### RL-2b Bootstrap move
- **Why:** after the move, `public/install*` is only ever the generated copy.
- **What is unchanged:** `config/vite/installerAssets.ts` and the `Dockerfile` serve from `public/`, so they stay as they are.

### RL-2c `release-sync`
- **Why a copy:** at least six consumers read `public/install-manifest.json` from an App checkout or image, among them Docker, `build.json`, fully local, the local-update checkout and Pinokio. Keeping one generated copy means none of them change.
- **What it does:** it runs every 30 minutes and can be started by hand. Its code comes from App `main`, and it does nothing unless `vars.RELEASE_SYNC_ENABLED == 'true'`, like the claim bot's switch. It:
  - fetches `release-published`;
  - checks that `source` is an ancestor of astrid-dev `main` and holds `releases/<release>.md`;
  - runs `manifest-check`;
  - copies the bootstraps from `app` (from `scripts/installer/bootstrap/`, or `public/` for a SHA from before RL-2b, which only the legacy record has);
  - commits only `public/install*` and pushes.
- **Checks on its own pushes:** a push made with the workflow token starts no other workflow, so the sync runs the App's manifest and bootstrap checks itself before pushing. The canary checks the deployed result.
- **`install-copy-guard`** fails any PR that changes `public/install*`. The sync never opens a PR.
- **Burn down:** the sync replaces `pin.mjs` write mode and `release-guard`, so they're deleted in this same change. Plan 29 already deleted `release-check.mjs`, `update-manifest.mjs`, the release-0 and baseline files and `check-public-updater-candidate.*`. Confirm that against App `main` at start.
- **App PR #208** (version helper) closes unmerged. Nothing from it is needed.
- **Route note (X, could be S):** this job writes installer code to App `main`. The gate in RL-1c is the trust root, and the review round covers this job. Raise it to S if the push identity needs a new credential (see inputs, open decision 1).

### RL-3 Versions on screen
- **Hosted:** reads `version` and `versions` from the manifest the App already loads, through RL-2a's schema.
- **Local launcher:** `localUpdateStatus.ts` returns the served `versions` alongside the release numbers.
- **Unknown release:** a release with no entry in `versions` shows "an earlier version", never "Release N".
- **Kind** isn't displayed.


## Proposed Release 16 scope reconciliation (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

Build, review and go remain unchecked. The first owner row is unnumbered; the proposed label O-1 refers to that existing row, while O-2 already exists.

| Existing task | Exact proposed outcome/dependency change |
| --- | --- |
| RL-0 | Retain App worker setup, copied-script parity and focused setup/smoke acceptance; reuse and revalidate existing scripts. Put publisher/control inventory under RL-1a/RL-2c and run prerequisites, without reopening completed P58. |
| RL-1a | Extend existing release-brief record/validation/generation/view, adopt one verified actually served legacy anchor; no invented Final records or public versions for every numbered candidate. |
| RL-1b | Validate complete full-SHA tuple, schema/lock and platform/bootstrap/pack identities, predecessor/candidate compatibility and approved publication ancestry. Candidate need not be on public main to qualify. Product producer and proof-only pin commits are distinct. |
| RL-1c | Authenticated protected owner Final transition bound to exact head/evidence; stale/wrong actor/replay/race reject, legitimate retry idempotent. Draft/strategy changes cannot publish. |
| RL-1d | Current branch and draft/decided/published/live procedure, owner-only public promotion and immutable receipts. |
| RL-2a | Preserve every existing manifest field and integer behavior while adding validated version metadata; consume one P29/P30 status/parser contract. |
| RL-2b/c | Canonical bootstrap source and deterministic generated-only sync; retain old served bytes/guard until coherent replacement is effective, then retire old authority once. Prefer exact generated diff through a protected bot PR. O-2 bypass plus self-check is not equivalent enforcement. |
| RL-2d | Compare complete actual served manifest and three bootstraps to approved generated bytes; verify deployment identity separately. Source SHA, sync commit and deployment UUID are different; no future self-referential commit in its own manifest. |
| RL-3 | **Remove final RL-G dependency.** Depends on RL-1a/RL-2a and settled status seam; implement Settings/notice for hosted/local 0.1.0 and true rollback identity before final review. |
| RL-R | Add RL-3 and negative publication/compatibility cases to existing RL-0–2d review. Final review includes exact release proof/ledger, not a hypothetical record. |
| RL-G | Keep one stable row but distinguish early nonpublishing rehearsal/legacy adoption from final go. Final action depends on RL-R, RL-3, effective owner controls, all accepted product gates and exact owner approval. |
| Unnumbered owner row / O-2 | Verify effective controls on each actual write/deploy boundary, stale approval invalidation and allowed actors. Hold auto-deploy or prove compatible interval. No new broad bypass or weakening required checks. |

The comparator correction belongs to this bounded gate work, using existing `env/baseline-diff.py`/inventory machinery, not a second CI programme. A previously failing missing test must not disappear from the candidate inventory. Namespace repository/job-family/OS/config/full ID, combine all shards within family, retain subtests/removals and collection success. Evidence: [SC-31](../../releases/16/evidence/scoping/README.md#receipts), [INV-01](../../releases/16/evidence/scoping/README.md#receipts), [INV-06](../../releases/16/evidence/scoping/README.md#receipts), [AUD-01](../../releases/16/evidence/scoping/README.md#receipts), [source adjudication](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md#9-refreshed-identities-primary-source-adjudication-and-limits).
