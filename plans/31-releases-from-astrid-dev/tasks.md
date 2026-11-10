# Tasks — Releases defined and published from astrid-dev

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change. An N task that misses the same acceptance check twice re-routes to X.

**Where work lands.** Every task lands by PR on `int/31-releases-from-astrid-dev`, in astrid-dev and in the App, cut from each `main` when the run starts (after Plan 29 is on App `main`). Only the [Release skill](../../skills/astrid-dev-release/SKILL.md) moves either branch to `main` (RL-G). Record each task's base SHA when it starts.

**Phases.** Phase 1 is every row down to RL-G: releases are defined, checked and published from astrid-dev. Phase 2 is RL-3: users see versions. Per-phase estimates are in the [catalog](../index.md).

**Proof labels.** *Local* runs in a single-repository worker session at the task's candidate SHA. *Hosted* is the named CI job on the task's PR into `int/31`, judged by its inner step, not the run's status. Proof that needs another repository's files fetches them by git at a pinned commit; nothing reads `raw.githubusercontent.com` from a worker session.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner** | | | | | |
| Protect astrid-dev `main` (code-owner review, stale approvals dismissed, `release-contract` required) and `release-published` (no force-push or deletion) | owner | — | astrid-dev repository settings | Settings show both rulesets | [ ] |
| O-2 App `main`: swap the required check `release-guard` (Plan 29) for `install-copy-guard`, and give the sync's push identity a bypass that only it holds | owner | RL-2c | App repository settings | Settings show `install-copy-guard` required and `release-guard` gone; the bypass list names only the sync identity. Done in RL-G, between App `int/31` merging and the first sync | [ ] |
| **Build: worker environment** | | | | | |
| RL-0 App worker setup script | N | — | astrid-dev `env/app-setup.sh` (new), `env/smoke.sh` (`app` mode), `env/README.md` table; App `scripts/worker-env/{app-setup.sh,smoke.sh}` (copies) | Local, App worker on `int/31`: `bash scripts/worker-env/smoke.sh app scripts/installer/manifest.test.mjs` exits 0 and runs that one file; with a Node other than 20.19.x first on `PATH` it exits 3. `cmp env/app-setup.sh <App>/scripts/worker-env/app-setup.sh` is silent | [ ] |
| **Build: astrid-dev records and publishing** | | | | | |
| RL-1a Living release briefs, draft/strategy checks, final record checks and the legacy record | N | — | astrid-dev `releases/TEMPLATE.md`, `releases/<N>.md` (living drafts → final records), `strategy.md`, `scripts/check_docs.py` (draft/overview validation), `scripts/release_record.py` (`check`, `render`), `scripts/test_release_record.py`; import the actually live legacy record at start; closes astrid-dev PR #82 unmerged (its cases move here) | Local: `python3 scripts/check_docs.py` and `python3 -m unittest discover -s scripts -p test_release_record.py` pass. A draft with no SHAs is accepted and cannot render or publish. Negative cases refuse a missing highlight/intent/approach, invalid plan link, mismatched strategy summary, duplicate plan, wrong release number, malformed final payload, a gap in finalized numbers, wrong version step for kind, non-40-character SHA, required update without a reason, a changed/deleted finalized record, and a final record whose pins disagree with its included plans. The actual live legacy final record renders a manifest matching the served one, apart from the four intentionally added metadata fields | [ ] |
| RL-1b `release-contract` job: the record against the real consumers | X | RL-1a, RL-2a | astrid-dev `.github/workflows/docs.yml` (`release-contract`), `scripts/release_record.py` (`ancestry`) and its test | Hosted, `release-contract` on the task PR: PASS for the legacy record. Hosted, one throwaway draft PR into `int/31` per case, closed unmerged, each FAIL with its reason: an `app`, `agent` or `runtime` SHA that exists but is not an ancestor of that repository's `main` (a real open-PR head commit); a `runtime` that differs from the Agent's `runtime.lock.json`; a wrong `runtime_schema_digest`; bootstraps at `app` whose uv or Python pin differs from `tools`; `tools` that the record's Agent or the previous record's Agent `tools.validate_manifest` rejects (Node `20.19.5`) | [ ] |
| RL-1c `publish-release` finalization and fail-closed gate | S | RL-1b | astrid-dev `.github/CODEOWNERS` (new), `.github/workflows/docs.yml` (`publish-release`), `scripts/release_gate.py` and `scripts/test_release_gate.py` (new) | Local: `python3 -m unittest discover -s scripts -p test_release_gate.py` covers refusals from recorded API response shapes, including a Draft or strategy-only PR causing no publication, a Final without owner approval, and attempts to edit a previously finalized release. Local, live public API, read-only: `python3 scripts/release_gate.py --repo banodoco/astrid-dev --check-only --commit <a merged main commit with no code-owner approval>` exits non-zero and names both "main has no code-owner ruleset" (today) and "no code-owner approval on the final head". The positive path first runs in RL-G | [ ] |
| RL-1d Release skill plans, finalizes and publishes through release documents | N | RL-1c, RL-2c | astrid-dev `skills/astrid-dev-release/SKILL.md` (installer-tuple lane and publish steps) | Local: `python3 scripts/check_docs.py` passes; `grep -n -e pin.mjs -e release-guard -e "release guard" skills/astrid-dev-release/SKILL.md` prints nothing; the skill names draft, final/decided, published and live, the sync as its own step, and the RL-G order; drafting never implies a release | [ ] |
| **Build: App generated copy** | | | | | |
| RL-2a Typed install-manifest schema and one check CLI | X | RL-0 | App `scripts/installer/manifest-schema.mjs` and `scripts/installer/manifest-check.mjs` (new) and their test; `scripts/installer/pin.mjs` (`--check` CLI removed, `checkManifest` kept); `scripts/installer/manifest.test.mjs`; `src/shared/lib/updates/updateStatus.ts` (`readManifest`); `config/vite/localUpdateStatus.ts` (manifest parsing) | Local: `node --test scripts/installer/manifest-schema.test.mjs scripts/installer/manifest.test.mjs` passes, accepting App `main`'s served manifest unchanged and the RL-1a rendered manifest, and rejecting a bad `versions` entry, a non-integer `release` and a short `app.sha`. Local: `npx vitest run --config config/testing/vitest.config.ts src/shared/lib/updates/updateStatus.test.ts config/vite/localUpdateStatus.test.ts` passes. `git grep -n -e "--check" -- scripts/installer/pin.mjs scripts/installer/manifest.test.mjs` prints nothing | [ ] |
| RL-2b Bootstrap source moves out of `public/` | N | RL-0 | App `public/{install,install.sh,install.ps1}` → `scripts/installer/bootstrap/` (`public/` keeps identical copies until the first sync); `scripts/installer/{fixture.mjs,bootstrap.test.mjs,bootstrap-powershell.test.mjs,manifest.test.mjs}` paths | Local: `node --test scripts/installer/bootstrap.test.mjs` passes against the moved source, and `cmp` of each source with its `public/` copy is silent. Hosted: `Windows installer` runs on the task PR (its `scripts/installer/**` filter) and its test step passes | [ ] |
| RL-2c `release-sync`, the copy guard, and the old pin path deleted | X | RL-1a, RL-2a, RL-2b | App `.github/workflows/release-sync.yml` and `scripts/installer/release-sync.mjs` and its test (new); `.github/workflows/test.yml` (`install-copy-guard` replaces `release-guard`); deletes `scripts/installer/release-guard.mjs`, its cases in `release.test.mjs`, `pin.mjs` write mode (`pin`, `applyRequiredPin`, CLI) and the `README.md` pin line | Local: `node --test scripts/installer/release-sync.test.mjs` passes. It syncs the RL-1a rendered legacy manifest into a temp clone of App `int/31`, and the diff touches only `version`, `versions`, `app` and `source`. Each of these refuses to commit: a `source` that is not an ancestor of astrid-dev `main`; a `source` with no Final record for `release`; an `app` that is not an ancestor of App `main`; a manifest that fails `manifest-check`. Local: `node scripts/installer/release-sync.mjs` with `RELEASE_SYNC_ENABLED` unset exits 0 and writes nothing. Hosted: on a throwaway draft PR that edits `public/install.sh`, `install-copy-guard` FAILs; on the task PR it passes. `git grep -n -e release-guard -e applyRequiredPin` prints nothing | [ ] |
| RL-2d Canary also compares with `release-published` | N | RL-2c | App `scripts/installer/served-manifest.mjs`, its case in `release.test.mjs`, `.github/workflows/served-manifest-canary.yml` | Local: `node --test scripts/installer/release.test.mjs` passes, with a case where the served manifest matches the deployed copy but not `release-published`, which fails. The live run is in RL-G | [ ] |
| **Review: before the first release through this path** | | | | | |
| RL-R Independent reviews of the integrated pipeline | S | RL-0 to RL-2d | all Plan 31 scopes (read-only review) | At most the owner's agreed number of rounds (see [inputs](inputs.md#planning-evidence)). Findings become rows `RL-R<round>.<n>` directly below this one, done before the next round | [ ] |
| **Publish** | | | | | |
| RL-G Go live through the Release skill (owner's go) | release | RL-R, both owner rows | App and astrid-dev `main` (Release skill only); owner sets App variable `RELEASE_SYNC_ENABLED` | In order: App `int/31` → `main` with the sync disabled, and the canary passes; O-2; astrid-dev `int/31` → `main`, and `publish-release` writes `release-published` for the legacy record; the owner enables the sync, its first commit to App `main` touches only the four metadata keys, and the canary passes for that deployment. Then the first new draft becomes Final in an owner-approved merge with no App PR, and the canary confirms it (plan completion) | [ ] |
| **Phase 2: on screen** (lands on `int/31` after RL-G; ships through the Release skill with the next record, after one review round of its own) | | | | | |
| RL-3 Users see versions, not release numbers | N | RL-1a, RL-2a, RL-G | App `src/shared/lib/updates/updateStatus.ts`, `src/shared/components/SettingsModal/sections/AstridUpdatesSection.tsx`, `src/shared/components/RuntimeConnection/QuietUpdateNotice.tsx`, `config/vite/localUpdateStatus.ts`, and their tests | Local: `npx vitest run --config config/testing/vitest.config.ts src/shared/lib/updates/updateStatus.test.ts src/shared/components/SettingsModal/sections/AstridUpdatesSection.test.tsx src/shared/components/RuntimeConnection/QuietUpdateNotice.test.tsx config/vite/localUpdateStatus.test.ts` passes, showing "Astrid is up to date (0.0.10)", "Update available: Astrid 0.0.11" and "Installed 0.0.9", hosted and local launcher. Each test feeds the manifest RL-1a renders, not hand-written fields. `git grep -n -e 'Release ${' -e 'Release {' -- src` prints nothing | [ ] |

**Overlap with other projects:**
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
  - Draft: `Release` number, `State: Draft`, title, one-line `Highlight`, multi-paragraph `Intent`, `Approach`, `Included plans` (linked plan files, each with a short reason) and `Publication: Not pinned.`. Existing docs CI ensures the row in `strategy.md` matches the highlight, release number, stage and plan set. Drafts may be changed on `main` and must never enter the publish output.
  - Final: the same sections, `State: Final` and a publication JSON block with `version`, `kind`, `required` (null or a reason), full SHAs for `app`, `agent`, `runtime`, `runtime_schema_digest`, `tools` and optional informational `pinokio`. The release number, strategic `why` and `plans` are derived from the document, not duplicated in a second hand-edited record. The render output is the existing App-compatible manifest. CI refuses invalid or missing pins and changes to an already finalized record.

  The owner's go is the GitHub approval on the PR, not a field.
- **Legacy record:** the release actually live when this plan starts, without assuming the old expected number 10 is still current. `app` is the deployed App commit the canary last passed for. `versions` maps 1 to N as `0.0.<n>`, so every install that exists today has a version to show (owner to confirm, see inputs).
- **Checks:** draft structure and release↔strategy consistency belong to documentation CI; final-record shape belongs to `check`. Coherence across repositories (Runtime against Agent lock, digest, ancestry, tools) belongs to RL-1b, through the App's own checker, so no digest code is copied into Python. Finalization is a distinct transition; regular documentation merges never publish.
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

### RL-1c `publish-release`
- **Base:** copy `publish-vision`, including the superseded-run guard. Publish only when a new, owner-approved Final record has been merged to `main`; drafts and strategy changes are ignored, even when they are newer by release number. A push that leaves published bytes unchanged writes nothing.
- **Gate:** fail closed like the claim bot, using only reads a public repository allows. The gate checks:
  - an active ruleset on `main` requires a pull request with code-owner review, with stale approvals dismissed (`GET /repos/{repo}/rules/branches/main`);
  - the commit that transitioned the intended record to Final belongs to a merged PR;
  - that PR has an `APPROVED` review from a code owner of `releases/`, whose `commit_id` is the PR's final head.

  The gate checks the PR that finalized the record, not whatever push triggered the run.
- **`CODEOWNERS`:** the owner owns `releases/`. The owner also owns everything that decides what gets published: `.github/CODEOWNERS`, `.github/workflows/docs.yml`, `scripts/release_record.py` and `scripts/release_gate.py`. Otherwise a maintainer could change the publisher without the owner.
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
