# The local App path: a first-principles sense-check

Read-only review, 9 Nov 2026. "Local App" means the App served from a checkout on the user's machine by `npm run dev:local` (the fully local launcher and the dev workspace are the same script), including Pinokio's "Install fully local", plus `npm run update` and the in-page Update now that drives it.

**Sources (fetched heads, read with `git archive`, not working trees):**

| Repo | Ref | SHA |
|---|---|---|
| App | `int/29-update-and-release` (= main, Release 10) | `1db36e66` |
| App | `ur-15b-app-copy` (#223) | `6da57d9e` |
| App | `ur-15k-live-update` (#224, contains #223) | `a1ce3d6c` |
| Agent | `int/29-update-and-release` (contains #319, UR-15/15a) | `97abb707` |
| Agent | `ur-15f-failure-copy`, `ur-15k-live-update-journey`, `ur-15c-journey-leg` | `39ddf6ab`, `37f788b9`, `eded78cc` |
| Runtime | `int/29-update-and-release` | `21df9bfb` |
| Runtime | `ur-15b-diagnostics` (#43) | `091e4505` |
| astrid-dev | `origin/main`; review on `advisor/plan29-field-failure-review` | `1864f8f`; `f81b37b` |

Line numbers are on those SHAs: App files on `a1ce3d6c` when they changed there, otherwise `1db36e66` (none of the UR-15 App branches touches `scripts/` or `config/vite/localUpdate*.ts`, **verified** by `diff -rq`). Tags: **[verified]** read in code, **[inferred]** follows from verified code but not run, **[unverified]**.

---

## Verdict

The local path is **sound inside one update transaction, and unsound everywhere around it**.

- **What is good.** One local update is a real transaction with a real end check. The Agent's `local_update.py` runs the same C2 journal as the installer. It checks the live Runtime's identity against the target (`local_update.py:337-373`). The launcher then checks that the restarted editor serves the target build and that the Runtime release matches (`dev-local-workspace.mjs:932-948`). A local "updated" is therefore rarely a lie. **[verified]**
- **What is wrong.** The local path keeps its **own copy of every source of truth**: what is installed, what is latest, where the data lives, how a run ended, and what each failure is called. None of the UR-15 work reaches it:
  - The local status calls the **App checkout's** release "installed", and never looks at the Runtime.
  - The launcher finds the data root with its own JS reader, which ignores a storage handoff that has not been normalised. On Windows it reads a path the Agent deletes.
  - `local_update.py` neither settles nor writes `last-run.json`. It does not normalise a finished handoff, and it does not run the second-Runtime check.
  - The page's live update display and "didn't install anything" card are switched off when `local` is set.
  - Failures reach the person as "Check diagnostics", and the diagnostics hold nothing about the App-side steps.
- **The honest-failure test.** The local path passes "exit 0 only if true" for a normal update. It fails it for `recovered`, where `npm run update` exits 0. It fails "descriptive failure" and "points to the full story" almost everywhere. It fails "both agent and manual steps": the agent brief and the manual command update the Runtime, not the local editor. It also has two dead ends with no defined transition: a Runtime newer than the editor, and an editor current but a Runtime behind.

---

## 1. The path, traced

### 1.1 Sources of truth, side by side

| Question | Hosted (astrid.haus) | Local (dev:local) | Agree? |
|---|---|---|---|
| **Installed release** | Live Runtime health `release` (`updateStatus.ts:36`, `installedReleaseOf`) | The **App checkout's** `public/install-manifest.json` `release` (`localUpdateStatus.ts:163`, wired at `vite.config.ts:153`) | **No.** Local never asks the Runtime. **[verified]** |
| **Latest release** | Same-origin `/install-manifest.json` (served by astrid.haus) | `https://astrid.haus/build.json` + `install-manifest.json` fetched by the Vite plugin (`localUpdateStatus.ts:132,148`) | Same values, different code. **[verified]** |
| **"Behind"** | `installed < served` (`updateStatus.ts:47`) | `served > checkout` **or** served App SHA is not an ancestor of HEAD (`localUpdateStatus.ts:49-51`) | **No.** A developer on a feature branch is "behind" for ever. **[verified]**; consequence **[inferred]** |
| **Can it update itself** | Runtime `/v1/update/status` `self_update` + `reason` enum | Env flag `ASTRID_LOCAL_SELF_UPDATE`, fixed when the launcher starts (`dev-local-workspace.mjs:662-677`). Reason is always `source` when false, Pinokio included (`localUpdateStatus.ts:168`) | **No.** A second, static mechanism. **[verified]** |
| **Where the data lives** | Agent `Installation.resolve` (`installation.py:145-200`) | JS `resolveRuntimeDataRoot` reads `astrid-install.json` `data_root` (`dev-local-workspace-options.mjs:235-253`) | **No.** See 1.2. **[verified]** |
| **Which backend is installed** | Agent `current(program_root)` | JS `installedBackend` walks up from the Python path looking for `install.json` + `current` (`local-update-backend.mjs:28-51`) | Second parser. **[verified]** |
| **Is an update pending** | Agent `pending_transaction`, `TERMINAL_STEPS` (`core.py:107-115`) | JS `readUpdateJournal` / `journalSettled` (`local-update-backend.mjs:17-25`) | Same rule today, second copy. **[verified]** |
| **How the last run ended** | `last-run.json` (Agent `outcome.py`), shown in diagnostics and in the App's "didn't install anything" card | Launcher's in-memory result message. `local_update.py` writes no receipt (grep: no `settle`/`write_record` outside `cli.py`) | **No.** **[verified]** |
| **Failure vocabulary** | `outcome.REASONS` (Agent), `INSTALLER_UPDATE_REASON_MESSAGES` (App) | `LOCAL_PAGE_REFUSAL_MESSAGES` (3 entries) + a generic failure line (`updateOperation.ts:236-242, 300-304`), launcher strings, runner strings | **No.** Four tables. **[verified]** |

### 1.2 The data-root reader disagrees with the Agent's resolver

- **macOS and Linux.**
  - Both sides read `~/.local/share/astrid-install.json` (or `$XDG_DATA_HOME`). **[verified]**
  - The launcher takes `data_root` as written. Before normalisation, a finished R0→R1 handoff still has `data_root = R0` (review §0), so the launcher attaches to, or starts, a Runtime **at the R0 data root**. **[inferred]**
  - Line 510-515 then swaps in the program root's `current` Python, which is the R1-era version. **[inferred]**
  - That is a candidate for what restarted R0 on Hannah's Mac. The review left that **[unverified]**, and so do I.
  - After UR-15 normalisation (`boundary_handoff.py:86-87`) the two sides agree again. Only a CLI `install`/`--update` normalises (`cli.py:644`). **[verified]**
- **Windows.**
  - The Agent moves the selection to `%LOCALAPPDATA%\Astrid Installer\astrid-install.json` and **deletes** the legacy `%LOCALAPPDATA%\astrid-install.json` (`service.py:128-178`). **[verified]**
  - The App still reads the legacy path (`dev-local-workspace-options.mjs:238-241`), so it falls back to `%LOCALAPPDATA%\Astrid Runtime`. **[verified]**
  - So a Windows install with a custom data root, or one after a handoff (R1 = `…-r1`, `boundary_handoff.py:299`), is not found by the launcher, even after normalisation. **[inferred]**

### 1.3 Journeys

| Journey | What happens today (user action → visible result) | Source of truth | Agrees with hosted / resolver / receipt? |
|---|---|---|---|
| **First local install** | The in-App setup offers manual steps (`copy.ts` `localSetupSteps`) **and** an agent brief (`localSetupInstructions`): official installer, then `git clone` + `npx -y npm@11 ci`, then `npm run dev:local`. The installer step is the hosted CLI, so it settles and writes `last-run.json`. If the Runtime is missing, `dev:local` prints "Astrid isn't set up on this computer yet. Install guide: …" (`dev-local-workspace.mjs:41-42`). **[verified]** | CLI receipt for the Runtime. Nothing for the editor. | The Runtime half agrees. The editor half has no receipt. The terminal offers only a URL, with no agent line. |
| **Start** (`npm run dev:local`) | Resolves the data root (1.2), reads discovery, validates the credential, catalog, health, handshake and realm (`:376-492`), starts the Runtime with `runtime up` if none is live, then prints "Open http://127.0.0.1:5180/tools/video-editor". Each failure is one friendly line plus one `Details:` line (`:79-84`). Good shape. **[verified]** Exception: a schema mismatch prints one long technical line (`:440`). A pending local-update journal is recovered **silently** before start (`:508-576`). **[verified]** | JS data-root reader. Discovery at that root. | The reader can disagree (1.2). A recovery at start leaves no trace in the terminal or in a receipt. |
| **Update available** | Settings shows "Update available: Release N" with **Update now** (when `ASTRID_LOCAL_SELF_UPDATE=1`) and **Copy instructions for your agent** (`resolveUpdate.ts:76`, a1ce3d6c). Update now posts to the launcher (`updateOperation.ts` `LocalPageUpdate`). The launcher runs `runner.update()`: recover, select target, preflight, prepare, then `local_update` (hooks stop/move/start/verify editor). The CLI path is `npm run update` (`local-update.mjs`). **[verified]** | Installed = **App checkout** release. Latest = astrid.haus. | **No.** "Installed" is the editor, not the Runtime. The agent brief is the hosted `curl … --update`, which updates the **Runtime only** and leaves the editor behind (`UpdateResolutionActions.tsx:73`, `copy.ts` `agentInstructions('update', …, localBuild)`). It also tells the agent to "confirm Astrid shows Connected" on astrid.haus. The App never shows `npm run update`, and a test asserts it never does (`FullyLocalUpdate.test.tsx:50-60`). **[verified]** |
| **Update finishes** | On `done`, `updateLocally` reloads the page itself (`UpdateResolutionActions.tsx:54-58`). The launcher prints "Astrid is updated and running." (`dev-local-workspace.mjs:968`). **[verified]** Vite restarts the dev server mid-update, and Vite's client reloads the page as soon as the server comes back, which can be before the POST answers. That drops the in-memory result. **[inferred]** (standard Vite 5 client behaviour; not run here). After the reload no "Astrid updated: Release N → M" is shown: `noteRelease` runs only in `UpdateOperation.refresh`, and `useInstallerUpdate` is disabled when `local` (`useInstallerUpdate.ts:35,40` a1ce3d6c). **[verified]** | In-memory `LocalPageUpdate` state. | **No.** UR-15k's live display never runs locally. |
| **Update failure** | Page: "The update did not complete. Check diagnostics before trying again." (`updateOperation.ts:302`) for every non-refusal failure. The step, code and message the launcher returns are discarded. The launcher's own terminal prints **nothing** on a page-started failure (`dev-local-workspace.mjs:967-969` logs only success; `local-update-control.mjs:237-241` does not log). `npm run update` prints "Astrid update failed at <step>: <message>". That message can embed up to 16 KB of updater stderr (`local-update-backend.mjs:65,90`) or the full `npm ci` stderr (`local-update-checkout.mjs:253,293`). **[verified]** The App-side steps (git, npm ci, build) are logged nowhere (grep: no log file in `local-update-*.mjs`). **[verified absence]** | None durable for the App half. `install.log` for the Agent half. | **No.** "Check diagnostics" points at a report that has no App-side story. Nothing is written to `last-run.json`. |
| **Interrupted update** | At the next start the launcher recovers it silently (above). `npm run update` / Update now recover it first and return `recovered`. The page says "The update did not finish. Astrid was restored to its previous version." (honest). `npm run update` **exits 0** (`local-update.mjs:3-6`). **[verified]** | C2 journal `update-transaction.json`. | **Exit 0 contradicts** the receipt contract: a recovery-only update is `not-updated`, exit 3 (`outcome.py:20-31`). |
| **Repair** | Undefined. The repair row needs `installType === 'installer'` (`AstridUpdatesSection.tsx:159`). Plan 29 says "Fully local repair isn't defined in this plan" (tasks.md:120). Launcher errors name `astrid-runtime up/restart --profile astrid`, not the official repair line. **[verified]** | — | No repair transition exists. |
| **Editor behind the Runtime** (Runtime updated from astrid.haus, or by `curl --update`) | Same session: the page may show the schema card. Its fully-local action is Update now, and `local_update` runs as a repair of the Runtime while it moves the editor, so it converges. **[inferred]** At the next start, `dev:local` checks the Runtime's schema digest against the editor's accepted list. A newer digest prints the "incompatible … update your checkouts; restart: <python -m …>" line and exits 1 (`dev-local-workspace.mjs:435-452`). `npm run update` needs a **running** launcher ("Start Astrid with npm run dev:local, then run npm run update", `local-update-control.mjs:281`). **Dead end:** the updater needs the launcher, and the launcher refuses until updated. **[verified]** | Digest list `runtime-update-contract.mjs:5-20`. | No defined transition. The only exit is a manual `git pull`, which the message does not say. |
| **Runtime behind the editor** (e.g. the person ran `git pull`, the agent brief's own recipe, `copy.ts:169`) | The local status compares only the editor with astrid.haus, so it says "Astrid is up to date (Release N)". The runner returns `up-to-date` from the App's git ancestry alone (`local-update-checkout.mjs:144`, `local-update-runner.mjs:110`). `local_update` refuses an App with no change ("The local launcher has no App update to apply.", `local_update.py:155-156`). Nothing updates the Runtime from the local page. The launcher starts if the old digest is in the legacy list. **[verified]** | App checkout only. | **Silent.** The page says up to date while the Runtime is older. |

---

## 2. Root problems, from first principles

| # | Problem | Kind | Evidence | Missing invariant |
|---|---|---|---|---|
| **P1** | **"Installed" means the editor checkout locally and the Runtime when hosted.** No local surface compares the Runtime with the editor or with astrid.haus. | Duplicated resolver; silent success | `localUpdateStatus.ts:163-166`; `local-update-checkout.mjs:144`; `local_update.py:155` | **L1.** Installed = the *pair* {live Runtime release, editor release}. "Up to date" only when both equal the served release. |
| **P2** | **Three JS readers of Agent state**: data root (`dev-local-workspace-options.mjs:235`), backend (`local-update-backend.mjs:28`), journal (`:17-25`), plus the static `self_update` env flag. They ignore the handoff journal, `r1_data_root` and Windows' private selection. | Duplicated resolver/parser | §1.2 | **L2.** Only the Agent resolver says where Astrid lives (review I2, extended to the App's local launcher). |
| **P3** | **The local update writes no receipt and has its own exit codes.** `local_update.main` returns 0/1. `npm run update` exits 0 for `recovered`. Diagnostics' "Last update" and the App's "didn't install anything" card can show a stale CLI receipt next to a fresh local result. | Silent success; duplicated outcome | `local_update.py:578-598`; `local-update.mjs`; `local-update-runner.mjs:108` | **L3.** Every run that can change the installation, CLI or local, settles once and writes `last-run.json` (review I1). |
| **P4** | **The un-normalised handoff trap is back on the local path.** `local_update._backend` only *adopts* an already-normalised handoff (`local_update.py:203-207` → `installation.py:226-238`). `_selection` takes `data_root` from the marker, which is R0 before normalisation (`local_update.py:213-218`). The realm check compares R0 with R0 and passes (`:237-240`). So a local update on such a machine runs backup, migrate and start against the **R0 data root**, the exact trap review §0 warns about. | State with no defined transition | as cited | **L4.** No update path, local included, operates a handed-off install before normalising it. |
| **P5** | **No second-Runtime check locally.** `retire_r0_leftover` / `other-runtime-running` run only in `cli.py:762-769`. | Missing post-condition | grep | Review I5. Already **UR-15i**. |
| **P6** | **The page never sees the Runtime's update status.** `useInstallerUpdate` is gated `!local` (`:35,40`). So UR-15k's live display, `self_update`, the reason codes, the reconciliation kind and the `self-update-too-old` copy (`resolveUpdate.ts:83-85` requires `installer`) are all off. `loadPageUpdateStatus` is fetched once per page load (`pageUpdateStatus.ts:11-27`). | Missing live display; parallel copy | as cited | **L5.** One status shape and one page operation for every install type. Install type changes the action, never the facts. |
| **P7** | **The agent brief and the manual step do not update what the button updates.** Update now updates the editor and Runtime together. "Copy instructions for your agent" and "Run it yourself" give `curl … --update`, which updates the Runtime only (`copy.ts` `agentInstructions`). The fully-local brief also says to `git pull` main (`copy.ts:169`), a third recipe that can put the editor ahead of the served build. | Missing next step; duplicated copy | `resolveUpdate.ts:76`; `UpdateResolutionActions.tsx:73`; `FullyLocalUpdate.test.tsx:50-60` | **L6.** Each install type has exactly one update recipe, and the button, the agent brief and the manual line all name it. |
| **P8** | **Failures don't say what happened or where to look.** One generic page line. Silence in the launcher terminal on page failures. Multi-KB stderr dumped into `npm run update` output. No App-side log. "Update another way" for refusals without naming the way. The status-check 503 drops its `stage` and says "Check your connection" even for a local Git failure (`AstridUpdatesSection.tsx:114`). | Dump of detail; missing next step | §1.3 | **L7.** Every local failure is one plain line, a "Why", and a pointer to Download diagnostics and the log path. The log holds the whole story, App half included. |
| **P9** | **Dead ends between editor and Runtime versions.** A newer Runtime blocks the launcher, which blocks the updater. A current editor with an older Runtime has no update path from the page. | States with no defined transition | §1.3 | **L8.** Every {editor, Runtime} skew has a defined transition, enumerated and tested (review I3, extended to the pair). |
| **P10** | **Smaller lies.** (a) Diagnostics' App header "Latest available" fetches `/install-manifest.json` relative to the page, which is the **checkout's own** manifest when local (`diagnosticsDownload.ts:6-16,35`). (b) `--preview` mode offers Update now, but the page endpoint is registered only for the dev server (`localUpdatePage.ts:30`, no `configurePreviewServer`), so the click fails with "The update launcher is not available". (c) The launcher reports `reason: 'source'` for Pinokio too (`localUpdateStatus.ts:168` + `dev-local-workspace.mjs:663`). (d) The Agent resolver's `fully-local` kind means "a local-update journal is mid-flight" (`installation.py:177-178`), not "a fully local install". | Never lie | as cited, **[verified]** in code. (b)'s click result **[inferred]**: page-route tests run only in dev mode (`local-update-launcher.test.mjs:578-640`). | L5, L6 |

The **strength worth keeping**: the local transaction already has an observed post-condition (`editor.verify` + `_verify_selected_identity`). It just doesn't record it where everything else reads.

---

## 3. Does the UR-15 work cover the local path?

| UR-15 guarantee | Hosted after UR-15 | Local after UR-15 | Evidence |
|---|---|---|---|
| One resolver + normalising a finished handoff (agent `installation.py`) | `cli.py:644` normalises; `update_job`/`maintenance` adopt | **Not used.** The launcher has its own JS readers (P2). `local_update` adopts but never normalises (P4). | `local_update.py:203-207`; `dev-local-workspace-options.mjs:235-253` **[verified]** |
| Receipt `last-run.json`, exit 0 only if live = target, 3 = not updated, 2 = consent | `cli.py:16,375-386,471` | **Not written** by `local_update`. `npm run update` exits 0/1 only, and 0 on `recovered`. The launcher reads no receipt and no exit code. It reads the updater's JSON line (`local-update-backend.mjs:61-91`). | grep; `local-update.mjs` **[verified]** |
| Second-Runtime refusal | `cli.py:762-769` | Absent. Scoped as **UR-15i** (tasks.md:52, "not release 11"). | **[verified]** |
| Diagnostics headline (runtime #43) | Reads `last-run.json` and the storage-move state (`diagnostics.py:113-136,180-195,299`) | Runs, but for a local update it says "no installer run recorded" or shows a **stale** CLI receipt. "Latest" comes from `receipt.target` (`:252-254`), so it is unknown or stale locally. The App header above it shows the checkout's own release as "Latest available" (P10a). | `diagnostics.py:252-254`; `diagnosticsDownload.ts:6-16` **[verified]** |
| Reason copy (app #223) | `installerUpdateReasons.ts`; `self-update-too-old`; "didn't install anything" card | `self-update-too-old` requires `installType === 'installer'` (`resolveUpdate.ts:84`). The "didn't install anything" card compares the **checkout's** release with served (`AstridUpdatesSection.tsx:186`) and offers `curl … --update` (`:208`), which won't move the editor. Local failures keep the old generic line (`updateOperation.ts:302`). | **[verified]** |
| Live update display (app #224) | `UpdateOperation.refresh` → `noteRelease` (`updateOperation.ts:159-163`) + auto-reload on restart (`RuntimeConnectionPill.tsx`) | `refresh` never runs locally (`useInstallerUpdate.ts:35,40`), so the notice never fires. The pill's auto-reload may still fire, because it follows the connection's restart state. **[inferred]** | **[verified]** gate |
| Proof | Hosted journey legs, every-state test | No UR-15 test sets `VITE_ASTRID_LOCAL_UPDATE_STATUS` (grep count 0 in `LiveUpdate.test.tsx`, `liveUpdate.test.ts`, `updateReasons.test.ts`). The local canary is "written, not run" (`docs/fully-local-update.md:69`). | **[verified]** |

**What breaks or stays silent locally after UR-15 lands:**
1. **A local update on an un-normalised handed-off machine targets the R0 data root** (P4). UR-15 made the CLI safe and left this door open. **[inferred]** from verified code.
2. **A local `recovered` run exits 0 and leaves no receipt.** Diagnostics keep showing whatever the last CLI run wrote. **[verified]**
3. **The launcher on Windows ignores normalisation**, because it reads the legacy selection path. **[inferred]**
4. **"Astrid updated: Release N → M" never appears on a local page**, and an update run from a terminal is never noticed by an open local page. **[verified]** gate
5. **"The last update didn't install anything"** locally mixes a CLI receipt with the editor's release, and its "try again" command doesn't touch the editor. **[verified]** code; user-visible effect **[inferred]**.
6. **Every local failure still reads "Check diagnostics before trying again."**, and diagnostics hold no App-side story. **[verified]**

---

## 4. The elegant shape

Three mechanisms. All of them already exist for the hosted path. The local path should call them instead of copying them.

1. **The Agent owns "what is installed", and the launcher asks it.**
   - Add a read-only entry point: `python -I -m astrid.installer.installation --json`. It prints `State` with `kind`, `program_root`, `active_data_root`, `selected_version` (python, profile, release), `live_identity`, `live_runtimes`, `pending` and `phase`.
   - The launcher already needs one Python to start. It calls this once at start and once before each update.
   - Fix `kind`: `fully-local` should mean "an installer backend used by a local launcher", and a pending local journal should be `pending-transaction`.
   - **Delete:**
     - `resolveRuntimeDataRoot` (`dev-local-workspace-options.mjs:235-253`) and the selection read;
     - `installedBackend`'s walk-up (`local-update-backend.mjs:28-51`);
     - `readUpdateJournal`/`journalSettled` (`:17-25`) and their uses in `dev-local-workspace.mjs:516-517` and `local-update-runner.mjs:7,134-136`;
     - `launcherCanSelfUpdate` and `ASTRID_LOCAL_SELF_UPDATE` (`dev-local-workspace.mjs:662-677`, `localUpdateStatus.ts:183`).
2. **One receipt for every run.**
   - `local_update.main` calls the same `settle(Request("update", target=manifest release), before, Installation.resolve)` and `write_record` as `cli.py`.
   - Its JSON reply carries the `Outcome` record, and `npm run update`'s exit code is `outcome.exit_code`. The page and the launcher terminal render `outcome.headline()` and `reason_line`.
   - **Delete:** the runner's message strings (`local-update-runner.mjs:108,110,130`, `dev-local-workspace.mjs:960`), the page's own result/failure lines (`updateOperation.ts:300-304`), and the "must include Astrid's local updater" guess (`local-update-backend.mjs:90`).
   - The App half's steps (select, preflight, prepare, move) write to the same `install.log` through the hook protocol, or to a sibling `local-update.log` that diagnostics tail.
3. **One status shape and one page operation.**
   - The local status endpoint returns the hosted shape: `installedRelease` = live Runtime release; `appRelease`/`app` = checkout; `servedRelease`; `self_update` + `reason` from the Agent's resolver and the reason enum; `lastRun` = the receipt.
   - The page runs the same `UpdateOperation` (refresh, `noteRelease`, didNothing) for local. Only the *action* differs: Update now posts to the launcher, and the recipe is `npm run update`.
   - **Delete:** the `!local` gates (`useInstallerUpdate.ts:35,40`), `checkLocalUpdate`'s special parser (`updateStatus.ts:59-77`), the per-load cache for local (`pageUpdateStatus.ts:11-27`), and the regex read of the receipt out of diagnostics text (`lastRun.ts:19`), which becomes a typed field. Plan 30 UR-16b's update-status schema is the natural home.

**Copy follows from these.** One reason table, `outcome.REASONS`, exported as JSON for the App. The App keeps lines only for Runtime-only refusal codes. `LOCAL_PAGE_REFUSAL_MESSAGES` becomes three more reasons in the same table (`local-edits-conflict`, `private-commits`, `not-fast-forward`). Net effect: the local path gets smaller. Roughly −200 lines of JS readers, parsers and strings, against about +60 lines of Agent entry point and receipt wiring.

---

## 5. Triage

### (a) Small fixes for Release 11: they make UR-15's guarantees hold on the local path

| # | Fix | Where | Size | Proof |
|---|---|---|---|---|
| a1 | **Close the R0 trap locally.** Inside the installer lock, before `_selection`, run the same `normalise_completed(backend)` the CLI runs (`cli.py:644`). If a handoff journal is present but not `complete`, refuse with reason `needs-repair` ("Run the install line once to finish an earlier storage move"). | agent `local_update.py:531-575` | ~15 lines + 1 test | Field fixture `handed-off-release1-r0-live-disk-full` with a local `update` action: `_selection` data root is R1 and the journal is archived; un-normalised mid-phase → refusal. Fails on `97abb707` first. |
| a2 | **Settle and write the receipt from `local_update`.** Wrap `execute` in `settle(...)`/`write_record(log_dir/last-run.json)`. `recovered` → `not-updated` (`recovered-previous-version`). Reply `{"result": …, "outcome": record}`. | agent `local_update.py:578-598`, reuse `outcome.py` | ~30 lines + 2 tests | Updated → receipt `updated`, exit field 0; recovery-only → `not-updated`, exit 3. Diagnostics headline reflects a local run. |
| a3 | **`npm run update` exit codes follow the receipt**: 0 updated/already-current, 3 recovered/not-updated, 1 failed. Print the headline lines, not `result.message`. | app `scripts/local-update.mjs`, `local-update-runner.mjs:108` | ~10 lines + test | `local-update-runner.test.mjs` asserts exit 3 on `recovered`. |
| a4 | **Local failures say what happened and where.** Page: map `code`/`step` to a reason line, plus "Details: Download diagnostics · <install log path>". Launcher terminal: print one line plus `Details:` on page-started failure. Cap the updater stderr in messages to its last line; the rest goes to `install.log`. | app `updateOperation.ts:236-242,300-304`; `dev-local-workspace.mjs:953-970`; `local-update-backend.mjs:90`; `local-update-checkout.mjs:253` | ~35 lines + tests | Vitest: a 422 `private_commits` renders its own line and both pointers. Node test: launcher stdout has one failure line. |
| a5 | **Agent brief and manual line match the button** (needs an owner decision: Plan 29 UR-9 chose "Secondary: the normal install command", tasks.md:143-151). The fully-local update brief names `npm run update` in this checkout, and the installer only as a Runtime fallback. Manual line: "In a second terminal in this folder, run `npm run update`." Flip `FullyLocalUpdate.test.tsx:50-60` and `AstridUpdatesSection.test.tsx:140`. | app `copy.ts` (new `localUpdateInstructions`), `UpdateResolutionActions.tsx:73` | ~40 lines + tests | Fully-local card shows Update now, agent brief containing `npm run update`, and manual line. Hosted card unchanged. |
| a6 | **Diagnostics header never mislabels "Latest available"**: in local mode, take it from the local status's `servedRelease`, or write "unknown". | app `diagnosticsDownload.ts:6-16,35` | ~8 lines + test | Local fixture: header shows served 11 while the checkout is 10. |
| a7 | **No Update now in `--preview` mode** unless the page route exists. Register `configurePreviewServer` in `localUpdatePage.ts` with `preview.port`, mirroring `localUpdateStatus.ts:186-189`. | app `config/vite/localUpdatePage.ts` | ~8 lines + test | `local-update-launcher.test.mjs` page-route test parametrised over dev and preview. |
| a8 | **Live result on a local page.** After `checkLocalUpdate`, call `noteRelease(app, release)` and publish the transition through the page's `UpdateOperation` (constructor already shows a carried transition, `updateOperation.ts:123-127`). The reload after a local update then shows "Astrid updated: Release N → M". | app `pageUpdateStatus.ts`, `updateOperation.ts` (expose `showUpdated`) | ~20 lines + vitest | Vitest: local status 10 then 11 with a new App SHA shows the updated line with no click. |
| a9 | **Start-time recovery says so.** One line when the launcher restores an interrupted update before start. | app `dev-local-workspace.mjs:526-575` | ~3 lines | Node test asserts the line. |

These total about 170 lines of product code, plus tests. a1 and a2 are the two that make UR-15's invariants true locally. a3–a9 make rules 1–5 true there.

### (b) Larger jobs: task cards

| Card | Route | Depends on | Scope | Focused proof |
|---|---|---|---|---|
| **LA-1 The launcher asks the Agent where Astrid lives** (mechanism 1) | X | UR-15, a1 | agent `installation.py` (`--json` entry, `kind` fix); app `dev-local-workspace-options.mjs` (delete `resolveRuntimeDataRoot`), `local-update-backend.mjs` (delete `installedBackend`, `readUpdateJournal`, `journalSettled`), `dev-local-workspace.mjs`, `localUpdateStatus.ts` (`self_update` from the resolver) | Fixtures: un-normalised handoff (macOS) → the launcher attaches to R1; Windows private selection with a custom data root → found. A lint/grep test fails if App code reads `astrid-install.json` or `update-transaction.json`. |
| **LA-2 One status shape and one page operation for local** (mechanism 3) | X | LA-1, a2, Plan 30 UR-16b | app `localUpdateStatus.ts`, `updateStatus.ts`, `pageUpdateStatus.ts`, `useInstallerUpdate.ts` (drop `!local`), `resolveUpdate.ts`, `AstridUpdatesSection.tsx`, `lastRun.ts` (typed field, no regex) | Vitest: Runtime 10 / editor 11 shows the engine line; Runtime 11 / editor 10 shows the editor line. A terminal `npm run update` is shown live on an open page within 30 s with no click. The didNothing card uses the receipt and the Runtime release. |
| **LA-3 Every editor/Runtime skew has a transition** (L8) | S | LA-1, LA-2 | app `local-update-control.mjs` (`requestLocalUpdate` runs the updater in-process when no launcher is live), `dev-local-workspace.mjs:435-452` (a newer Runtime starts the update path instead of exiting), `local-update-checkout.mjs:144` + agent `local_update.py:155-156` (Runtime-only repair when the editor is current) | A table test over {editor < = > Runtime} × {Runtime < = served}: each cell ends `updated`, `already-current` or a named refusal, never exit 0 with skew. The Runtime-newer fixture recovers with `npm run update` alone. |
| **LA-4 One reason table across Agent and App** | X | a2, Plan 30 UR-16b/UR-17 | agent `outcome.py` (export `REASONS` as JSON with a schema); app `installerUpdateReasons.ts`, `LOCAL_PAGE_REFUSAL_MESSAGES` → generated | A schema test fails when a reason exists on one side only. The App has no hand-written copy of an Agent reason. |
| **LA-5 Hosted Update now vs a running local launcher** | X | LA-1 | runtime `update.py` status (a local launcher receipt present → reason `local-launcher`, with the `npm run update` line); app `resolveUpdate.ts` | With dev:local running, astrid.haus shows "This Astrid is updated from your local editor" and no Update now, instead of updating the Runtime under the editor. |
| **LA-6 Define local repair** | N | LA-1 | app `AstridUpdatesSection.tsx:159`, `copy.ts`; launcher error copy (`dev-local-workspace.mjs:61-73`) | A degraded Runtime under dev:local shows one repair line (the plain install line, then restart dev:local), an agent brief and a log pointer. Launcher errors name the same line. |
| **LA-7 App-half update log** | N | a4 | app `local-update-checkout.mjs`, `local-update-runner.mjs`; runtime `diagnostics.py` (tail `local-update.log`) | A failed `npm ci` in prepare appears in Download diagnostics under its own label, with the command and the last lines. |

### (c) Already scoped elsewhere

| Item | Where | Note |
|---|---|---|
| Fully local update proof | Plan 30 `tasks.md:14` (UR-18b); `plan.md:14,43` | A dev:local page-driven test already exists with a **fake** backend (`local-update-launcher.test.mjs:636`). Re-aim UR-18b at a real installed backend plus the a2 receipt, so it proves the post-condition rather than the plumbing. |
| Update-status schema | Plan 30 `tasks.md:11` (UR-16b) | LA-2's local shape should be this schema, not a second one. |
| Refusal rule | Plan 30 `tasks.md:12` (UR-17) | LA-4 feeds it. |
| Second-Runtime check in `local_update` | Plan 29 `tasks.md:52` (UR-15i, "not release 11") | Keep it as scoped. a1 removes the more dangerous R0-data case without it. |
| UX pass over every path | Plan 29 `tasks.md:53` (UR-15j) | Its scope says "installer terminal". Add the **dev:local terminal, `npm run update`, and the local Settings card** explicitly, or the local path stays outside the pass. |
| Live update display | Plan 29 `tasks.md:54` (UR-15k) | Scoped to astrid.haus pages. a8 is the minimal local extension; LA-2 is the real one. |
| Fully local repair | Plan 29 `tasks.md:120` ("isn't defined in this plan") | LA-6. |
| Pinokio and fully local "proven through the actions people press" | Plan 30 `plan.md:14` | Covers proof, not the truth-sharing in LA-1/LA-2. |

---

## 6. Copy: proposed exact lines for the local path

Rules applied: what happened, with numbers; whether work is safe; one next action; a pointer, not a dump; both an agent brief and a manual line. "Editor" means the local App, "Astrid" the Runtime and agent. These are the two words a local user already sees in the launcher.

### 6a. Settings › Updates (local)

| State | Status line / title | Body | Actions |
|---|---|---|---|
| Up to date (editor = Runtime = served) | **Astrid is up to date (Release 11)** | — | Check for updates |
| Update available, can update here | **Release 11 is ready** | You have Release 10. Updating takes a few minutes and keeps your projects and your local edits. The editor restarts, then this page reloads. | **Update now** · Copy instructions for your agent |
| ↳ manual line under the actions | | Or, in a second terminal in this folder, run `npm run update`. | |
| Updating | **Updating Astrid…** | The editor restarts during the update; this page reloads by itself. | — |
| Just updated (8 s, live) | **Astrid updated: Release 10 → Release 11** | — | — |
| Already current after a click | **Astrid is already up to date (Release 11)** | Nothing was changed. | — |
| Interrupted, restored (`not-updated`, `recovered-previous-version`) | **The update didn't finish** | Astrid went back to Release 10 and is running. Your projects and edits are unchanged. | **Try again** · Download diagnostics · Copy instructions for your agent |
| Failed (`failed`/`rolled-back`) | **Astrid did not update** | It is still Release 10. Why: {reason line}. Your projects and edits are unchanged. Details: Download diagnostics, or see {install log path}. | **Try again** · Download diagnostics · Copy instructions for your agent |
| Refused: overlapping edits | **Astrid did not update: your edits overlap this update** | {n} files you changed are also changed by Release 11. Nothing was changed. Commit or move those edits, then try again. | Try again · Copy instructions for your agent |
| Refused: commits not on main | **Astrid did not update: this folder has commits that aren't on main** | Nothing was changed. Push them, or move them to another branch, then try again. | Try again · Copy instructions for your agent |
| Busy | **Another update is running** | Wait for it to finish; this page shows the result. | Update now (disabled) |
| Launcher not answering | **Astrid can't update from this page right now** | The terminal running `npm run dev:local` isn't answering. Start it again, then try again. | Copy the start command · Copy instructions for your agent |
| Preview mode | **Release 11 is ready** | This editor was started in preview mode, so it can't update from this page. In a terminal in this folder, run `npm run update`. | Copy the command · Copy instructions for your agent |
| Editor older than Astrid | **Your editor is older than Astrid** | The editor is Release 10 and Astrid is Release 11. Updating the editor keeps your projects and edits. | **Update now** · Copy instructions for your agent |
| Astrid older than the editor | **Astrid is older than this editor** | Astrid is Release 10 and the editor is Release 11. Update now brings Astrid to Release 11 and keeps your projects. | **Update now** · Copy instructions for your agent |
| Source checkouts (no installed Astrid) | **Release 11 is ready** | This Astrid runs from source checkouts, so update those to main and restart `npm run dev:local`. | Copy instructions for your agent |
| Check failed (by stage) | **Couldn't check for updates** | `upstream_fetch`: astrid.haus didn't answer. `served_manifest_validation`: astrid.haus sent release information this editor can't read. `local_git_ancestry_lookup`: Git couldn't read this folder. | Check again · Download diagnostics |
| Last run installed nothing (receipt) | **The last update didn't install anything** | Astrid is still Release 10; Release 11 is available. Why: {reason line}. Your projects are safe. | **Try again** · Download diagnostics · Copy instructions for your agent |

### 6b. Terminal: `npm run update`

```
Astrid updated: Release 10 → Release 11.
The editor restarted. Your projects and edits were kept.
```
exit 0
```
Astrid is already up to date (Release 11). Nothing was changed.
```
exit 0
```
Astrid did NOT update. An earlier update was interrupted, so Astrid restored Release 10.
Your projects and edits are unchanged.
Next: run npm run update again.
Details: ~/Library/Logs/Astrid Runtime/install.log
```
exit 3
```
Astrid did NOT update. It is still Release 10; Release 11 is available.
Why: {reason line}
Your projects and edits are unchanged.
Next: {one action}. If it fails twice, open Settings › Updates › Download diagnostics.
Details: ~/Library/Logs/Astrid Runtime/install.log
```
exit 1 (failed) or 3 (refused before any change)
```
Astrid did NOT update: Astrid isn't running in this folder.
Next: run npm run dev:local in another terminal, then run npm run update again.
```
exit 1

### 6c. Terminal: `npm run dev:local`

- Interrupted update restored at start:
  ```
  Astrid: An earlier update was interrupted. Astrid restored Release 10 and is starting it.
  Next: run npm run update to try again.
  ```
- Astrid newer than the editor. Interim wording until LA-3:
  ```
  Astrid: This editor is older than Astrid (editor Release 10, Astrid Release 11), so it can't start.
  Next: git pull --ff-only origin main, then npx -y npm@11 ci, then npm run dev:local.
  Details: Runtime schema sha256:… is not one this editor accepts.
  ```
- Update started from the page failed:
  ```
  Astrid did NOT update from the page: {reason line}
  Details: ~/Library/Logs/Astrid Runtime/install.log
  ```

### 6d. Agent brief: "Copy instructions for your agent" (fully local, update)

```
Please update my fully local Astrid on this computer. Do the work yourself and verify the result.

Astrid's editor runs from the checkout at {checkout path} with `npm run dev:local`, and uses the installed Astrid Runtime. Keep my projects, media, credentials, agent instructions and any uncommitted edits in that checkout.

1. Make sure `npm run dev:local` is running in that checkout; start it in its own terminal if it isn't.
2. In a second terminal in the same checkout, run `npm run update`. It updates the editor and Astrid together, then restarts the editor.
3. Exit code 0 means it worked: the first line names the release, for example "Astrid updated: Release 10 → Release 11". Exit code 3 means nothing was updated, and exit code 1 means it failed. In both cases read the "Why:" line, and the log named on the "Details:" line, then fix the cause before retrying. Don't retry more than twice.
4. If it says local edits overlap the update, or the checkout has commits that aren't on main, tell me. Don't discard or reset them.
5. Check the result: open http://127.0.0.1:5180/tools/video-editor. Settings › Updates should say "Astrid is up to date (Release {served})". Tell me the actual result; don't claim success if a check couldn't be run.
6. If it still fails, save the diagnostics (Settings › Updates › Download diagnostics, or run `astrid-runtime doctor > astrid-diagnostics.txt`) and tell me what they say.
```

---

## Flags (not derailing)

- `dev-local-workspace.mjs` is 1,006 lines, and `main()` alone is about 820. That is far over the 300-line guide. Recovery, the updater editor and the start path are three concerns in one function.
- `local-update-launcher.test.mjs` exercises the launcher only against a fake Agent updater. The native canary legs are "written, not run" (`docs/fully-local-update.md:69`). No local update has a receipt from a real machine. The release-11 field-receipt rule (review §3.4) should name the local path if Release 11 claims it.
- `localUpdateBehind` treats "served SHA not an ancestor of HEAD" as behind. For the dev-workspace audience on feature branches, that is a permanent "Update available" whose button fails with `private_commits`. LA-2 should base "behind" on releases, and show branch state as its own line.
