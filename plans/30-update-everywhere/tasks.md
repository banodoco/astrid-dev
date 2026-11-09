# Tasks — Update everywhere: remaining setups

[Plan](plan.md) · [Inputs](inputs.md)

Routes: **N** = normal, **X** = very hard, **S** = super hard (see the [run contract](../../skills/astrid-dev-shared/run-contract.md)). X and S tasks delegate research, reading, mechanical edits and checks to N helpers, and keep the judgment and the final change.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| UR-15 Remove the systemd 254 floor | S | Plan 29 | agent `update_job*.py`, journey matrix; contract update helper | On systemd 249, the Linux worker runs from an owner-only file with no `$` or `%` expansion. An update started before the change still reconciles. An Ubuntu 22.04 row passes | [ ] |
| UR-16a Helper-protocol schema owned by the Runtime | X | Plan 29 UR-10 | runtime helper-protocol schema; agent helper tests | A JSON Schema (Python on both sides) under `astrid_runtime/`, outside `contract/`; both repos test against it | [ ] |
| UR-16b Update-status schema, kept outside the versioned contract | N | Plan 29 UR-11 | app `client.ts`; update-status schema | The App validates against it, and `schema_digest` is unchanged | [ ] |
| UR-17 Refusal rule | N | Plan 29 UR-1 | app `CopyRefusedInstructions.tsx`, `RuntimeConnectionPanel.tsx`, `RuntimeConnectionPill.tsx`, `copy.ts` | A separate `resolveRefusal`; refused cards show update wording only when the installed release is behind | [ ] |
| UR-18a Pinokio update proof | N | — | agent `scripts/pinokio_row_driver.py` (coordinate with Plan 10) | The Pinokio row runs the launcher's own Update action (`update.js`), not a direct installer re-run | [ ] |
| UR-18b Fully local update proof | X | Plan 29 UR-9 | app local-update control tests | A dev:local test drives the in-page updater (no new hosted row) | [ ] |
| LA-1 The launcher asks the Agent where Astrid lives (local review mechanism 1) | X | Plan 29 UR-15, a1 | agent `installation.py` (`--json` entry), app `dev-local-workspace-options.mjs`, `local-update-backend.mjs` | One resolver answers the launcher; the launcher's own path logic is deleted | [ ] not started (Plan 30) |
| LA-2 One status shape and one page operation for local pages (local review mechanism 3) | X | LA-1, UR-15l-2, Plan 30 UR-16b | app `localUpdateStatus.ts`, `updateStatus.ts`, `pageUpdateStatus.ts`, `useInstallerUpdate.ts`, `resolveUpdate.ts` | One status schema for hosted and local; "behind" based on releases, not commit ancestry | [ ] not started (Plan 30) |
| LA-3 Every editor/Runtime skew has a transition (local review L8) | S | LA-1, LA-2 | app `local-update-control.mjs`, `dev-local-workspace.mjs:435-452` | Each editor/Runtime skew state has a defined update transition, tested | [ ] not started (Plan 30) |
| LA-4 One reason table across the Agent and the App (local review) | X | UR-15l-2, Plan 30 UR-16b/UR-17 | agent `outcome.py` (export REASONS as JSON with a schema), app `installerUpdateReasons.ts` | A schema test fails when a reason is added in one place only | [ ] not started (Plan 30) |
| LA-5 Hosted Update now vs a running local launcher | X | LA-1 | runtime `update.py` status (local launcher reason `local-launcher`), app `resolveUpdate.ts` | With dev:local running, astrid.haus shows the local-launcher reason and the `npm run update` line | [ ] not started (Plan 30) |
| LA-6 Define local repair | N | LA-1 | app `AstridUpdatesSection.tsx:159`, `copy.ts`, `dev-local-workspace.mjs:61-73` | A degraded Runtime under dev:local shows one repair line, then restart dev:local | [ ] not started (Plan 30) |
| LA-7 App-half update log | N | UR-15l-2 | app `local-update-checkout.mjs`, `local-update-runner.mjs`, runtime `diagnostics.py` | A failed `npm ci` in prepare appears in Download diagnostics under its own label | [ ] not started (Plan 30) |
| UR-19 Prune retained R0 copy after the first successful update; rollback offered only before it (owner decision 19, 9 Nov 2026) | S | Plan 29 UR-15, UR-15d, UR-15e (decided by decision 19) | agent `installation.py`, `cli.py` (`--rollback`); runtime retained-R0 plist and version handling | Acceptance tests (to write): `test_rollback_offered_only_before_first_successful_update`, `test_prune_retained_r0_after_first_successful_update` (R0 copy, plist and version removed), `test_rollback_refused_after_prune` | [ ] not started (Plan 30) |
| UR-20 In-app update preserves autostart-off: launch outside the job's kill domain, then delete the guard | TBD | TBD | agent `update_job*.py`, `update_job_platform.py`; runtime `update.py` (guard) | With autostart off, an in-app update leaves autostart off after the job's end; the guard is deleted only after the new launch is confirmed | [ ] not started (Plan 30) |
| UR-21 One `launch_plan` resolver, reported in the Runtime status and rendered by both the terminal and the App | TBD | TBD | runtime `update.py` (status); agent `cli.py` and installer terminal; app `resolveUpdate.ts`, `UpdateResolutionActions.tsx` | The same plan comes back from the Runtime status, the terminal and the App for each fixture; no surface computes its own plan | [ ] not started (Plan 30) |
| UR-22 Table-driven tests over autostart × service manager × OS × managed_by × situation | TBD | UR-21 | agent and runtime update tests; app decision tests | One table covers every combination the resolver reads; a new value that is not in the table fails the test | [ ] not started (Plan 30) |
| UR-23 Rewrite the agent brief for weak models (`copy.ts` ~:294–332): bounded inspect step, bounded "diagnose", observable "Connected" check | TBD | — | app `copy.ts` (~:294–332) | The brief names a fixed, short sequence of steps; each step has an observable result; no open-ended inspect and no unbounded diagnose; "Connected" is checked by a status field, not by the agent's judgement | [ ] not started (Plan 30) |
| UR-24 Print the "start later" line in the terminal for autostart off | TBD | UR-21 | agent `cli.py` (~:203 and ~:220) | With autostart off, the terminal prints the "start later" line on both paths, and the line matches the App's copy | [ ] not started (Plan 30) |
| UR-25 Windows upgrade path | TBD | TBD | agent installer Windows update path; journey `windows_update_journey.py` | The Windows upgrade row passes its hosted receipt on the candidate; the autostart-off case is covered | [ ] not started (Plan 30) |
| UR-26 Installer is step 1 in the local "Run it yourself" list (`copy.ts` ~:137–157) | TBD | TBD | app `copy.ts` (~:137–157) | The local "Run it yourself" list starts with the installer step; copy test asserts the order | [ ] not started (Plan 30) |
| UR-27 Hosted setup screen polls after install (`WelcomeFlow.tsx` ~:54–56) | TBD | TBD | app `WelcomeFlow.tsx` (~:54–56) | After the install finishes, the setup screen advances without a reload; a test drives the poll | [ ] not started (Plan 30) |
| UR-28 Weak-agent wording: "click Connect" becomes "tell me to click Connect" (`copy.ts` ~:331); EmptyWorkspaceGuidance step 4 gets a concrete check | TBD | TBD | app `copy.ts` (~:331), `EmptyWorkspaceGuidance` | The copy reads "tell me to click Connect"; step 4 names one observable check; copy test asserts both | [ ] not started (Plan 30) |
| UR-29 VibeComfy-specific "isn't installed; run the install line" message in generate list and doctor; catch narrowed to `ModuleNotFoundError` for vibecomfy (Plan 33's `entries.py` restore is silent) | TBD | TBD | agent generate list and doctor; `entries.py` (Plan 33's restore) | With VibeComfy missing, generate list and doctor show the message; any other import error still raises; a test covers both | [ ] not started (Plan 30) |
| UR-30 Install-time check of the VibeComfy pin against the manifest | TBD | TBD | agent installer; app `public/install-manifest.json` | At install, a VibeComfy pin that differs from the manifest fails or warns with the mismatch named; a test covers a mismatched pin | [ ] not started (Plan 30) |
| UR-31 CI job for the pack-build tests that Plan 33 moved to a manual lane (`backend.py` ~:1220–1226 has no CI coverage) | TBD | TBD | agent CI workflow; `backend.py` (~:1220–1226) | A CI job runs the pack-build tests on pull requests; it is green on the candidate | [ ] not started (Plan 30) |
| UR-R Up to two independent reviews before closing | S | UR-15–UR-18b | all Plan 30 scopes (read-only review) | Same review rounds as [Plan 29](../29-update-and-release/tasks.md#ur-r-review-rounds); findings become rows `UR-R<round>.<n>` directly below this one, done before the next round | [ ] |

## Task details

### UR-15 systemd floor
- **Why the floor exists:** it is there only for `systemd-run --expand-environment=no` (`update_job_platform.py:222`).
- **The fix:** use Windows' approach (`_worker_command`, `update_job.py:1341-1381`). The Linux argv becomes `python -B -X utf8 -I <owner-only job file>`.
- **Effect on in-flight updates:** the worker digest changes, so an update that started before the change must still reconcile (`update_job.py:623, 693, 1279`).
- **Before adding the 22.04 row:** it needs owner approval after a probe.

### UR-16 Contracts
`/v1/update/status` is not in `contract/` today. Adding it there would change `SCHEMA_DIGEST` and switch off `supportsFullV2Commit` in the App (`contract-metadata.ts:22-27`). Keep both schemas outside `contract/`.

