# Tasks — Releases defined and published from astrid-dev

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner** | | | | | |
| Protect astrid-dev `main` (code-owner review, stale approvals dismissed, `release-contract` required) and `release-published` (no force-push or deletion) | owner | — | astrid-dev repository settings | Settings show both rulesets | [ ] |
| **Build** | | | | | |
| RL-1 Release records, checks and publishing | N | Plan 29 | astrid-dev `releases/` (new), `.github/CODEOWNERS` (new), `scripts/release_record.py` and its test, `.github/workflows/docs.yml` (`release-contract`, `publish-release`), `skills/astrid-dev-release/SKILL.md`; App `pin.mjs` check mode (read-only use) | Each of these fails: a gap in numbers, a wrong version step, a short or unreachable SHA, a Runtime that differs from the Agent's lock, a digest mismatch, a bootstrap/tools mismatch, `required` without a reason, an edited old record, a broken plan link, a missing or stale owner approval, unprotected `main`. the legacy record for the release live at the start (expected `releases/10.json`, `0.0.10`) passes, and its generated manifest equals the served tuple | [ ] |
| RL-2 App generated copy and sync | X | RL-1 | app bootstrap move to `scripts/installer/bootstrap/` (and the tests and workflow paths that name it), `.github/workflows/release-sync.yml` and its script (new), a PR guard on `public/install*`, the served-manifest canary; deletes `pin.mjs` write mode, `release-check.mjs`, `update-manifest.mjs`, the release-0 and baseline files, `check-public-updater-candidate.*` and UR-8's tuple guard | Syncing the legacy record changes only metadata fields. A forged `source`, a bootstrap that isn't on App `main`, or a bad digest each refuse to commit. A PR that edits `public/install*` fails. The canary also compares with `release-published` | [ ] |
| RL-3 Users see versions, not release numbers | N | RL-2 | app `src/shared/lib/updates/updateStatus.ts`, `SettingsModal/sections/AstridUpdatesSection.tsx` | Shows "Astrid is up to date (0.0.10)", "Update available: Astrid 0.0.11" and "Installed 0.0.9" from the manifest's `version` and `versions`; no screen shows "Release N" | [ ] |
| **Review — before the first release through this path** | | | | | |
| RL-R Independent reviews of the integrated pipeline | S | RL-1–RL-3 | all Plan 31 scopes (read-only review) | At most the owner's agreed number of rounds (see [inputs](inputs.md#planning-evidence)); findings become rows `RL-R<round>.<n>` directly below this one, done before the next round | [ ] |

**Overlap with other projects:** RL-2 and RL-3 change App files that Plan 29 also changes (UR-8's guard, UR-1 and UR-3's update screens), so this plan starts after Plan 29 is on `main`.

## Task details

### RL-1 Records and publishing
- **Record:**
  - `release`, `version` and `kind`;
  - `required`: null, or a reason;
  - `why`;
  - `plans`: links to plan files;
  - full SHAs for `app`, `agent`, `runtime`, plus `runtime_schema_digest` and `tools`;
  - `pinokio`, optional and informational.

  The owner's go is the GitHub approval on the PR, not a field.
- **`release-contract`** has the shape of `vision-consumer-contract`. It runs App `main`'s `checkManifest` on the generated manifest, and the previous release's Agent `tools.validate_manifest`. Every repository is public, so no token is needed.
- **`publish-release`** copies `publish-vision`, including the superseded-run guard. Before writing, it checks through the API that the merged PR has a code-owner approval on its final head, and that `main` is protected. It fails closed otherwise, like the claim bot.
- **Published manifest:** today's shape, plus `version`, `versions` (release number to version), `app.sha`, `required.release` and `source` (the astrid-dev commit).
- **States:**
  - decided: the record is on `main`;
  - published: `release-published` has it;
  - live: the canary passes for a deployed commit with that release.

  The release skill reads these. There is no new state file.
- **Reuse:** rework astrid-dev PR #82. Keep its check test cases, and drop its markdown table.

### RL-2 App copy
- **Why a copy:** at least six consumers read `public/install-manifest.json` from an App checkout or image, among them Docker, `build.json`, fully local, the local-update checkout and Pinokio. Keeping one generated copy means none of them change.
- **`release-sync`** runs every 30 minutes and can be started by hand. Its code comes from App `main`. It:
  - fetches the published manifest;
  - checks that `source` is on astrid-dev `main` and has the record;
  - runs `checkManifest`;
  - copies the bootstrap scripts from the pinned `app.sha`;
  - commits the generated `public/install*` files and pushes.
- **Once App `main` is protected,** the sync needs a bypass.
- **App PR #208** (version helper) closes unmerged. Nothing from it is needed.

### RL-3 Versions on screen
- Reads `version` and `versions` from the manifest the App already loads. The kind isn't displayed.
