# Tasks — Releases defined and published from astrid-dev

[Plan](plan.md) · [Inputs](inputs.md)

**Not authorized to run.** The owner asked on 11 Nov 2026 for this plan to be brought up to date and made ready to execute; that is an instruction to prepare, not a go. The scope decision and owner decisions D1 to D7 in [inputs.md](inputs.md#owner-decisions) are open. These cards are written for the recommended answers (D1 a, D2 a, D3 a); [what changes under the other answers](#if-the-owner-decides-otherwise) is at the end.

Routes: **N**, **X**, **S**, **T** per the [run contract](../../skills/astrid-dev-shared/run-contract.md). X and S tasks delegate reading, mechanical edits and checks to N helpers. An N task that misses the same acceptance check twice re-routes to X with the worker's notes.

**Task ids:** `RL-<n>`. This re-plan (11 Nov 2026) renumbers the 8 Nov cards; [the old-to-new map](#what-changed-from-the-8-nov-cards) is below.

**Where work lands.** Every task lands by pull request on `int/31-releases-from-astrid-dev`, in astrid-dev and in the App, cut from each `main` when the run starts. Record each task's base SHA when it starts. Only the [Release skill](../../skills/astrid-dev-release/SKILL.md) moves either branch to `main` (RL-G). One exception: RL-11's record change is prepared on its own branch and opens against astrid-dev `main` during RL-G, because it has to be a separately approved pull request.

**Phases.** Phase 1 is every row down to RL-G: a release is a record in astrid-dev, and the App can only carry a checked copy of it. Phase 2 is RL-14, RL-14t and RL-15: users see versions, and the temporary parts are deleted.

**Critical path:** RL-1 → RL-3 → RS1 → RL-5 → RL-7 → RL-8 → RL-12t → R → RL-G, about seven working days end to end. RL-4 runs beside RL-1 and RL-3 and joins at RS1; RL-6 runs beside RL-5. RL-0 and RL-2 start at once; RL-9, RL-10 and RL-11 hang off RL-5 and RL-7 and run in parallel.

**Test inventory.**

- *App, phase 1* (`node --test`). New: `scripts/installer/manifest-check.test.mjs`, `scripts/installer/install-copy.test.mjs`, `scripts/installer/release-approval.test.mjs`. Affected: `scripts/installer/release.test.mjs` (its guard and pin cases are deleted in RL-7; the served-canary case and the `test.yml` concurrency case stay), `scripts/installer/bootstrap.test.mjs`, `scripts/installer/bootstrap-powershell.test.mjs` (hosted Windows only), `scripts/installer/manifest.test.mjs`, `config/vite/installerAssets.test.ts`. Not affected, must stay green: `scripts/installer/local-update-canary.test.mjs`.
- *App, phase 2* (`vitest`): `src/shared/lib/updates/updateStatus.test.ts`, `config/vite/localUpdateStatus.test.ts`, `src/shared/components/SettingsModal/sections/AstridUpdatesSection.test.tsx`, and in `src/shared/components/RuntimeConnection/`: `QuietUpdateNotice.test.tsx`, `FullyLocalUpdate.test.tsx`, `InstallerUpdateCallers.test.tsx`, `SourceCheckoutUpdateSurface.test.tsx`. Each asserts a `Release <n>` string today.
- *astrid-dev* (standard-library `unittest`; the whole inventory runs in under a minute, so by the run contract's cost exception all of it runs at every load-bearing moment). No new test file: this plan adds no Python. Affected and must pass unedited: `scripts/test_golden.py` and `scripts/test_check_docs.py` (RL-11 changes the real release file and strategy row they read), `scripts/test_views.py`. Every other `scripts/test_*.py` must stay green. `scripts/fixtures/golden.txt` must stay byte-identical.

**Load-bearing test moments.** Before the first task: both inventories on the starting SHAs (the App's after RL-0, which the [manage skill](../../skills/astrid-dev-manage/SKILL.md) allows to run first). After each task: its own focused proof. Before others build on a shared part: RL-3's and RL-4's tests at RS1, before RL-5, RL-6 and RL-7 start. Before R: the full workflows once per repository on the integrated heads, on CI.

**Checks a worker can run.**

```text
# App (from the checkout root, literal paths, no cd)
node --test scripts/installer/<file>.test.mjs          # needs only Node 20.19.x
bash scripts/worker-env/app-setup.sh                   # RL-0; only before a vitest run
npx vitest run --config config/testing/vitest.config.ts <files>

# astrid-dev (no setup; standard library only)
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_*.py"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py check
```

Another repository's files come from public git at a pinned commit (`git clone --filter=blob:none https://github.com/banodoco/<repo>`), never from an archive download. `checkManifest` in the App reads `raw.githubusercontent.com`; a network failure there is an environment problem (exit 3), never a test result, and every proof that needs it is labelled *hosted*.

**Proof labels.** *Local* runs in the task's worktree at its candidate. *Hosted* is the named CI job on the task's pull request into `int/31-releases-from-astrid-dev`, judged by its inner step, and is run by the hosting session.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner** | | | | | |
| O-0 Answer D1 to D7 and the scope decision. Create the approving account D1 names, with write access to astrid-dev and the App (a code owner without write access is ignored). Confirm the agents' account is not an admin of the App and is on no bypass list there. Approve, from the approving account, the astrid-dev pull request that records this plan's `Run start` line: that gives RL-4 one real approved pull request to record | owner | — | [inputs.md](inputs.md#owner-decisions); App and astrid-dev collaborator settings | Each decision carries a date and the owner's choice; the `Run start` pull request shows an `APPROVED` review from the approving account on its final head | [ ] |
| O-1 App `main` ruleset: require a pull request; require the `install-copy-guard` check with GitHub Actions as its source, so a commit status of the same name cannot stand in for it (it replaces `release-guard` if Plan 29's owner row made that required); no bypass actors; with D3 a, code-owner review with stale approvals dismissed | owner | RL-G step 1 | App repository settings | `GET /repos/banodoco/astrid-app/rules/branches/main` shows the pull-request rule, `install-copy-guard` with an `integration_id`, no `release-guard` and, with D3 a, `require_code_owner_review: true` and `dismiss_stale_reviews_on_push: true`; `GET /repos/banodoco/astrid-app/codeowners/errors` is empty | [ ] |
| **Build: worker environment** | | | | | |
| RL-0 App worker setup script | N | — | astrid-dev `env/app-setup.sh` (new), `env/smoke.sh` (`app` mode), `env/README.md` (table row and the call list); App `scripts/worker-env/app-setup.sh`, `scripts/worker-env/smoke.sh` (new, byte copies) | Local, App worktree: `bash scripts/worker-env/smoke.sh app scripts/installer/release.test.mjs` prints `ENV-PASS` and runs that one file; with a Node other than 20.19.x first on `PATH` it exits 3. `cmp` of each App copy with its `env/` source is silent | [ ] |
| **Build: the App reads, checks and copies a record** | | | | | |
| RL-1 One manifest check command | N | — | App `scripts/installer/manifest-check.mjs`, `scripts/installer/manifest-check.test.mjs` (new) | Local: `node --test scripts/installer/manifest-check.test.mjs` passes: with `--offline`, today's `public/install-manifest.json` and `public/` bootstraps are accepted; a manifest with `version`, `versions` and `app.sha` is accepted; a `versions` map that lacks the manifest's own release, a short `app.sha`, and a uv pin that differs from `install` are each refused. Hosted: without `--offline` it prints `checkManifest`'s line for `main`'s manifest | [ ] |
| RL-2 Bootstrap source moves out of `public/` | N | RL-0 | App `public/install`, `public/install.sh`, `public/install.ps1` → `scripts/installer/bootstrap/` (`public/` keeps byte-identical copies); `scripts/installer/bootstrap.test.mjs`, `scripts/installer/bootstrap-powershell.test.mjs`, `scripts/installer/fixture.mjs` (paths) | Local: `node --test scripts/installer/bootstrap.test.mjs` passes against the moved source; `cmp` of each source with its `public/` copy is silent; `scripts/installer/manifest.test.mjs` and `config/vite/installerAssets.test.ts` are unchanged and pass. Hosted: `Windows installer` runs on the task pull request and its test step passes | [ ] |
| RL-3 The record, the render and the copy rules, tests first. What a Final record holds, what it renders to, and when a change to `public/install*` is allowed, as failing tests over fixture record folders and temporary repositories | X | RL-1 | App `scripts/installer/install-copy.test.mjs` (new), `scripts/installer/install-copy.mjs` (new: exports and usage text only), `scripts/installer/fixtures/records/` (new: small record folders) | Local: the test file exists and fails only on the cases RL-5 and RL-7 implement; its cases cover [the payload rules, the render and rules G1 to G13](#rl-3-rl-5-and-rl-7-record-render-and-copy-guard) one for one. The X lead returns that list with the test that holds each line | [ ] |
| RL-4 The approval gate's contract, tests first. Every way a Final record can be on astrid-dev `main` without the owner's approval, as failing tests over API responses the hosting session records from the real API (the approved `Run start` pull request from O-0, and unapproved #521) and temporary repositories | S | O-0 | App `scripts/installer/release-approval.test.mjs` (new), `scripts/installer/release-approval.mjs` (new: exports and usage text only), `scripts/installer/fixtures/approval/` (new: recorded responses) | Local: the test file exists and fails only on the cases RL-6 implements; its cases cover [the refusal list](#rl-4-and-rl-6-the-approval-gate) one for one. The S lead returns that list with the test that holds each line, and any refusal it found that the list lacks | [ ] |
| RS1 Review stop after the trust root's contracts (rounds at most 1). Protects RL-5, RL-6, RL-7 and RL-G: a hole found at the final review would mean redoing the implementations, and one found after go-live would have let an unapproved installer through | S | RL-3, RL-4 | read-only: RL-3 and RL-4 as landed on App `int/31` | Same protocol as R. The reviewer is briefed "find what would let an unapproved installer publish; read the tests and the code, not the cards". Findings become rows `RS1.<n>`; RL-5, RL-6 and RL-7 depend on this row | [ ] |
| RL-5 Record reader and render, against RL-3's tests | N | RS1 | App `scripts/installer/install-copy.mjs` (`readRecords`, `render`, command `check-record`) | Local: the record and render cases in `install-copy.test.mjs` pass; the copy-rule cases still fail. With astrid-dev cloned beside it, `node scripts/installer/install-copy.mjs render --records <astrid-dev>/releases --release <a Draft's number>` exits non-zero and says the record is a Draft | [ ] |
| RL-6 The gate, against RL-4's tests | N | RS1 | App `scripts/installer/release-approval.mjs` | Local: `node --test scripts/installer/release-approval.test.mjs` passes. Local, live public API, read-only, with astrid-dev cloned beside it and `--approvers-at` pointing at a local scratch commit that carries the planned `CODEOWNERS`: `--commit <the Run start pull request's merge commit>` passes, and `--commit 12a54b6d8baa220fbe3d3a48e3a04f48b0511c07` (pull request #521, never approved) refuses, naming the missing approval | [ ] |
| RL-7 The guard, the write command, `CODEOWNERS`, and the old pin path deleted | N | RL-2, RL-5, RL-6 | App `scripts/installer/install-copy.mjs` (`verify`, `write`); `.github/workflows/install-copy-guard.yml` (new); `.github/workflows/test.yml` (job `release-guard` removed, nothing else); `.github/CODEOWNERS` (new: `/.github/`, `/scripts/installer/`, `/config/vite/installerAssets.ts`, `/Dockerfile`); `package.json` (`test:node` gains the three new test files); deleted: `scripts/installer/release-guard.mjs`, its cases and the `applyRequiredPin` case in `scripts/installer/release.test.mjs`; `scripts/installer/pin.mjs:pin`, `applyRequiredPin`, `main` (write mode goes, `--print` arrives, `--check` and `checkManifest` stay) and the two `checkManifest` messages that say "run pin.mjs"; `README.md` (the pin line) | Local: `node --test scripts/installer/install-copy.test.mjs scripts/installer/release.test.mjs scripts/installer/manifest.test.mjs` passes. Local: `node scripts/installer/install-copy.mjs write --candidate <a payload file made from the served manifest saved at run start, with `app` set to this task's base commit> --release <live> --records <dir>` changes only `version`, `versions` and `app` in `public/install-manifest.json` and no bootstrap byte. `git grep -n -e release-guard -e applyRequiredPin` prints nothing. Hosted (hosting session): two draft pull requests into App `main`, both closed unmerged: from the task branch, `install-copy-guard` passes; from a throwaway branch that also edits `public/install.sh`, it FAILS | [ ] |
| RL-8 The canary compares what is served with the record | N | RL-7 | App `.github/workflows/served-manifest-canary.yml` (one step in job `canary`); `scripts/installer/install-copy.mjs:verifyServed` and its cases in `scripts/installer/install-copy.test.mjs` | Local: the added cases pass: a served manifest and three bootstraps that equal, byte for byte, the render and bootstraps of the approved record for the served `release` pass; one changed byte in any of the four fails; a record the gate refuses fails; a served manifest with no `version` (from before the first record) is skipped with a line that says so. The live run is RL-G step 5 | [ ] |
| RL-12t Words people read from the App's commands: every refusal of `install-copy.mjs`, `release-approval.mjs` and `manifest-check.mjs` | T | RL-1, RL-5, RL-6, RL-7 | App: those three files (message strings only), and the same strings in their three test files | Before and after for every string, in the pull request. Rules: plain words; each refusal says what is wrong, in which file or pull request, and the one next step; a refusal on a hand edit says the file is generated and names the record to change instead; nothing implies a release happened. The three test files pass | [ ] |
| **Build: astrid-dev** | | | | | |
| RL-9 `release-contract` job: a proposed Final record against the App's checker, before the owner approves it. Not a required check | N | RL-5 | astrid-dev `.github/workflows/release.yml` (new) | Hosted (hosting session): on one throwaway pull request into `int/31`, closed unmerged, whose record is Final and names an Agent commit that exists but is not on Agent `main`, `release-contract` FAILS at the ancestry step; on a pull request that changes no Final record, its steps skip and the job is green. Its first PASS is RL-G step 4. Local: `astrid_dev.py check` passes | [ ] |
| RL-10 The Release skill plans, decides and publishes through records | N | RL-7 | astrid-dev `skills/astrid-dev-release/SKILL.md` ("Agent/Runtime installer tuple" lane, "One publisher at a time", "Publishing an installer release", the "Installer tuple" runbook line); `releases/TEMPLATE.md` (the paragraph under `## Publication` only) | Local: `astrid_dev.py check` passes; `grep -n -e "release-guard" -e "release guard" -e "pin.mjs <" skills/astrid-dev-release/SKILL.md` prints nothing; the skill holds [the eight steps](#rl-10-release-skill) in order, names draft, decided, published and live, and still has "Take stock of open pull requests" unchanged; the template still has `## Included pull requests` | [ ] |
| RL-11 The live release as the first record, prepared and not merged | N | RL-5 | astrid-dev, on branch `rel/31-live-record` cut from `int/31`: `releases/<live>.md` (State, Publication, with `app` left as the placeholder `0000000000000000000000000000000000000031` until RL-G step 4), `strategy.md` (that row's state word), every `scripts/fixtures/*/overlay.json` that carries `releases/<live>.md` or `strategy.md` (refreshed so each still shows only its one defect), `plans/releases.md` (a closing line) | Local, with the App at `int/31` cloned beside it: `node <app>/scripts/installer/install-copy.mjs render --records releases --release <live>` equals the served manifest saved at run start as parsed JSON, once `version`, `versions` and `app` are removed from the render. The whole astrid-dev inventory passes with `golden.txt` byte-identical to `int/31`. The pull request to `main` opens in RL-G step 4, after the hosting session replaces the placeholder in the record and in each refreshed overlay | [ ] |
| RL-13t The Release skill's new steps, as a skill reads | T | RL-10 | astrid-dev `skills/astrid-dev-release/SKILL.md` (wording of RL-10's text only) | Before and after, in the pull request. Rules: the skill's existing voice; each step one action with its command; says what is decided, published and live without implying a go. `astrid_dev.py check` passes | [ ] |
| **Review: before anything reaches `main`** | | | | | |
| R Review rounds on the integrated pipeline (at most 2, pending the owner) | S | every row above except O-1 | read-only: all Plan 31 scopes in both repositories | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md), after the full workflows have run once per repository on the integrated heads. Findings become rows `R<round>.<n>` directly below this one, each with route, scope, dependencies and proof; RL-G waits for them | [ ] |
| **Publish** | | | | | |
| RL-G Go live through the Release skill (owner's go, in the publishing session) | release | R | App and astrid-dev `main` (Release skill only) | [The five steps](#rl-g-go-live) in order, each with its receipt. It ends when the canary passes for a deployed App commit whose copy was written from the live record. Plan completion is separate: the first new release published this way | [ ] |
| **Phase 2: on screen, and clean up** (lands on `int/31` after RL-G; RL-14 and RL-14t ship as an ordinary hosted App deploy, with no review round beyond pull-request review) | | | | | |
| RL-14 Users see versions, not release numbers | N | RL-G; RL-5 (the manifest's `version` and `versions`); Plan 30's LA-2 if it has started | App `src/shared/lib/updates/updateStatus.ts` (`UpdateStatus`, `checkHostedUpdate`, `checkLocalUpdate`); `config/vite/localUpdateStatus.ts` (the status body); `src/shared/components/SettingsModal/sections/AstridUpdatesSection.tsx` (the status line and the Installed value); `src/shared/components/RuntimeConnection/QuietUpdateNotice.tsx` (the notice line); the seven phase 2 test files | Local: `npx vitest run --config config/testing/vitest.config.ts` on the seven phase 2 test files passes, showing a version where the manifest names one and no name where it does not, hosted and local launcher. Each test feeds a manifest written by `install-copy.mjs render`, not hand-written fields. `git grep -n -e 'Release ${' -e 'Release {' -- src config` prints nothing | [ ] |
| RL-14t The update lines themselves | T | RL-14 | App: the strings RL-14 touched, plus `resolveUpdate.ts` ("A newer release of Astrid is available."), `AstridUpdatesSection.tsx` ("Connect to Astrid before checking its release.") and `updateStatus.ts` ("Release information was invalid"), and the same strings in their tests | Before and after for every string, shown to the owner. Rules: plain words; a version, never a release number; never names a version the manifest did not give; every line that reports a problem has a next step. The seven test files pass | [ ] |
| RL-15 Delete what was temporary | N | the first new release published after RL-G | App `scripts/installer/install-copy.mjs:verifyServed` (the skip for a served manifest with no `version`) and its case; the throwaway branches and pull requests RL-7 and RL-9 opened; `rel/31-live-record`; `int/31-releases-from-astrid-dev` in both repositories once fast-forwarded | Local: `node --test scripts/installer/install-copy.test.mjs` passes with that case removed; `git grep -n "before the first record" -- scripts/installer` prints nothing; `git ls-remote --heads` shows none of the named branches | [ ] |

Add task details beneath the index only when useful. Scope names the paths, and any shared surface or contract, the task may change (a path includes its own tests, wherever they live); tasks with overlapping scopes need a dependency.

## Size

Days are one agent's working time, not elapsed time. The catalog holds the plan's total.

| Task | Days | Task | Days |
| --- | --- | --- | --- |
| RL-0 | 0.5 | RL-9 | 0.5 |
| RL-1 | 0.5 | RL-10 | 0.5 |
| RL-2 | 0.5 | RL-11 | 0.5 |
| RL-3 | 1.25 | RL-12t | 0.25 |
| RL-4 | 0.75 | RL-13t | 0.25 |
| RS1, with its findings | 0.75 | R, with its findings | 1.5 |
| RL-5 | 0.75 | RL-G | 0.5 |
| RL-6 | 0.5 | RL-14 | 0.75 |
| RL-7 | 1 | RL-14t | 0.25 |
| RL-8 | 0.5 | RL-15 | 0.25 |

Phase 1 (every row to RL-G) is 11 days; phase 2 is 1.25. By route: N 6.75 days (12 tasks), X 1.25 (1), S 3 (RL-4 0.75, RS1 0.75, R 1.5), T 0.75 (3), release 0.5. Total 12.25, range 10 to 15.5: the range is the hosted proofs in RL-7 and RL-9, which repeat slowly when wrong, and review findings. RL-0, RL-9, RL-10, RL-11 and RL-13t are off the critical path.

## Who runs each task

Codex does the writing wherever a Codex model can; the hosting Claude session does what Codex cannot. Codex routes are the [run contract's Codex column](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings); the family names below repeat it only so each row reads on its own.

| Task | Writes it | The hosting session does |
| --- | --- | --- |
| RL-0, RL-1, RL-5, RL-6, RL-8, RL-10, RL-11, RL-14, RL-15 | Codex, Luna | Commits, opens and merges the task pull request. For RL-11 it first saves the served manifest into the run folder; for RL-15 it deletes the remote branches |
| RL-2, RL-7, RL-9 | Codex, Luna | The same, plus the hosted proof: it opens the draft and throwaway pull requests, reads the job's inner step, and closes them |
| RL-3 | Codex, Terra | Commits and opens the pull request; runs the tests once to see they fail only where the card says |
| RL-4 | Codex, Sol | The same, and before it starts, records the real API responses the tests use |
| RL-12t, RL-13t, RL-14t | Hosting session, a named sub-agent on the high-judgment role (the contract also gives Codex a T route; these stay with the host because it holds the review of the same strings) | All of it. RL-14t's before and after goes to the owner |
| RS1, R | Hosting session, a named reviewer on the high-judgment role, with no part in the build | All of it; findings come back as cards Codex can take |
| RL-G | Hosting session with the owner | All of it: it needs the owner's go in that session, her settings changes and her approval |
| O-0, O-1 | Owner | Brings her each one with the exact setting to change |

**Codex's share:** 14 of the 20 build, review and publish rows and 8.75 of the 12.25 days (about 71%). X is needed once, for the contract written as tests before any code exists: what a record is, what it renders to, and when the App accepts a copy. S is needed once, for the gate's refusal list, which is the security boundary and cannot run end to end before go-live. Everything else is N because the tests exist first and the cards name every file. No task was left on X or S for being long.

## Dispatch notes

**Recommended manager route: S,** by the [orchestrate skill's table](../../skills/astrid-dev-orchestrate/SKILL.md#choose-the-managers-route): this is a release, across two repositories, with a security boundary, and one wrong call (merging a guard that passes too much) reaches every user.

**Recommended shape: the hosting Claude session manages; Codex executes.** A Codex sandbox cannot commit or push ([Plan 48's run note](../../docs/ledger/2026-11-11-plan48-phase1-run.md)), so it cannot integrate, and a manager that cannot integrate is a worker. The hosting session is the run's [accountable agent](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run) and its manager; it starts one Codex run per wave from [`manager-brief.md`](../../skills/astrid-dev-orchestrate/codex-in-claude-cloud/manager-brief.md), briefed as a lead that dispatches cards to sub-agents by route and never integrates.

- **Waves.** 1: RL-0, RL-1, RL-4, then RL-2. 2: RL-3. After RS1, 3: RL-5, RL-6. 4: RL-7, RL-9, RL-11. 5: RL-8, RL-10. The T rows follow their inputs. Phase 2 is one small wave after RL-G.
- **Workspace.** Partial clones `astrid-app/` and `astrid-dev/` at `int/31-releases-from-astrid-dev`, `astrid-agent/` at `main` for reading only, and `run/`. One `git worktree add` path per card (`wt/<task id>`) with its own `<worktree>.env`; only the lead touches the base clones.
- **Hand-over of each card.** The sub-agent leaves its change uncommitted in its worktree, runs the card's focused proof, and the lead writes `READY: <task id> <worktree path>` to the mailbox with the proof's command and output. The hosting session checks that the changed files are inside the card's scope, re-runs the proof once, commits (one commit per card, commits added and never rewritten), pushes a fresh branch `task/31-<task id>`, opens the pull request into `int/31-releases-from-astrid-dev` and merges it.
- **First step of the run:** one sub-agent tries `git commit` in a scratch worktree. If it works in this layout, sub-agents commit locally and the hosting session only pushes and opens pull requests; record which in `run.yaml`.
- **`READY:` tasks the hosting session runs itself,** as soon as their inputs land, without waiting to be asked: RL-12t, RL-13t, RL-14t, RS1, R, RL-G, the hosted proofs of RL-2, RL-7 and RL-9, recording the API responses for RL-4, and saving the served manifest for RL-11.
- **App worker environment.** Node 20.19.x must be on `PATH` in the hosting container before the run starts (the App's `.nvmrc` is 20.19.4). The cards for `scripts/installer/` use only Node itself and need no setup. RL-0's script (`npm ci`) is for the cards that run `vitest`: RL-2's unchanged `installerAssets.test.ts` and phase 2. The App has no committed `.claude/settings.json`, which matters only if a Claude worker session is ever attached to it; a Codex sub-agent needs none.
- **Batches.** A push to an App `int/**` branch starts the App's full workflows, so App task merges land several per push. Progress on this file lands as its own astrid-dev pull request, which now waits for the two required checks before it merges.
- **Never,** in any card: push to `main`; change `public/install*` on a branch that will merge to App `main` other than through `install-copy.mjs write`; edit an existing line of `golden.txt` or an existing test to get green; import anything outside `scripts/installer/` and Node into the three trusted scripts; put a model identifier in a commit, pull request or file.
- **Every sub-agent brief names** the card, its scope, its base SHA, its worktree, the exact proof command, and "leave the change uncommitted; do not ask the owner anything; write questions to the lead".

## Task details

### What is already on `main`

Part of the 8 Nov card RL-1a landed before this re-plan, at astrid-dev `12a54b6`:

- `releases/TEMPLATE.md`, including the optional `## Included pull requests` section (added 11 Nov);
- `releases/12.md`, a living Draft brief, with its row in `strategy.md`;
- the draft rules, as the registered checks `release-documents` and `strategy-consistency` (`scripts/check_docs.py:release_errors`, `strategy_errors`): number, title, state word, the five sections, a one-line highlight, linked and unduplicated plans, "Not pinned." in a Draft, and the strategy row agreeing with the document;
- one final rule: a Final record needs a JSON block holding `version`, `kind`, `required`, `app`, `agent`, `runtime`, `runtime_schema_digest` and `tools`;
- nine golden fixtures for those rules, and their cases in `scripts/test_check_docs.py`.

Not built: any reader of the payload, any other final rule, a render, the live record, any approval check, and everything in the App. None of the landed code is edited by this plan.

### Where the trusted code lives, and why

Three scripts decide what users install: `install-copy.mjs`, `release-approval.mjs` and `manifest-check.mjs`. All three live in the App, under `scripts/installer/`, for three reasons read from the repositories on 11 Nov 2026:

- **astrid-dev `main` is about to get an identity that bypasses its pull-request rule** ([Plan 48 D3](../48-one-record-model/inputs.md#owner-decisions), decided 11 Nov), and its managers merge their own progress pull requests with no approval. Code there cannot be the thing the installer trusts without slowing every other plan.
- **The App is where the last write happens,** so the App has to verify whatever it is given; anything verified only upstream can be skipped by writing to the App directly.
- **astrid-dev already checks its content with the App's own code:** the `vision-consumer-contract` job runs the App's parser on the proposed feed. `release-contract` (RL-9) does the same with a proposed record.

So astrid-dev holds data (the records) and a job that runs the App's checker early; the App holds the reader, the render, the gate and the guard, and executes no astrid-dev code. A test asserts the three scripts import only Node and files under `scripts/installer/`, so no unreviewed file can change their result. This is why the plan adds no Python and registers no new check: [Plan 48](../48-one-record-model/plan.md)'s registry, golden file and Phase 2 are untouched except by RL-11's fixture refresh.

### What changed from the 8 Nov cards

| 8 Nov card | Now |
| --- | --- |
| RL-0 | RL-0, with a smoke test that needs no other repository; no longer a dependency of the installer cards |
| RL-1a records, checks, legacy record | The draft part landed. Final rules and the render are RL-3 (tests) and RL-5, in the App; the live record is RL-11 |
| RL-1b `release-contract` (X) | RL-9 (N): it runs the App's `check-record` and is not a required check; the Agent validator step is cut, because a candidate is already qualified on the same bytes; one hosted negative case replaces five |
| RL-1c `publish-release` and gate (S) | RL-4 (S, the refusal list as tests) and RL-6 (N), in the App. The publish job and the `release-published` branch are cut ([D2](inputs.md#owner-decisions)) |
| RL-1d Release skill | RL-10, with the steps written out, and RL-13t |
| RL-2a typed schema for every reader (X) | RL-1 (N): one check command. The hand-written readers are left alone ([alternatives](inputs.md#alternatives)) |
| RL-2b bootstrap move | RL-2, with every test file named |
| RL-2c `release-sync` and the copy guard (X) | RL-3 (X, the rules as tests) and RL-7 (N). The scheduled writer is cut ([D2](inputs.md#owner-decisions)) |
| RL-2d canary compares with `release-published` | RL-8: the canary compares what is served, whole, with the approved record |
| RL-R, RL-G | RS1, R and RL-G |
| RL-3 | RL-14 (N) and RL-14t (T) |
| — | RL-12t (words), RL-15 (deleting the temporary parts) |

### RL-0 App worker setup

- `app-setup.sh`, from the App checkout root: fails with exit 3 unless `node --version` is `v20.19.*` and `package-lock.json` exists; then `npm ci --legacy-peer-deps`. No other repository, no network beyond the npm registry.
- `smoke.sh app <file>`: runs the setup, then `node --test <file>` (the file named in the card's proof needs no other repository); prints `ENV-PASS app <file>` or `ENV-FAIL` with the failing step. The three existing modes are unchanged.
- The App copies are byte copies under `scripts/worker-env/`, as in the Agent.

### RL-1 Manifest check

`node scripts/installer/manifest-check.mjs <manifest> --bootstrap-dir <dir> [--offline]`: the added keys' shape (all three optional; if `versions` is present it names the manifest's own release); every tool asset has one HTTPS URL and one real SHA-256 per download (today's first case in `manifest.test.mjs`, as a function); uv and Python pins agree with `<dir>/install` and `<dir>/install.ps1`; and, unless `--offline`, `checkManifest`. No dependency beyond Node, so astrid-dev's job and the App's guard run it without `npm ci`.

The 8 Nov card also moved `updateStatus.ts` and `localUpdateStatus.ts` onto a shared Zod schema. That is cut: both readers already ignore keys they do not know (read at App `6545f13`), so nothing in phase 1 needs them changed.

### RL-2 Bootstrap move

After this, a bootstrap is edited under `scripts/installer/bootstrap/` and reaches users only when a record names an App commit that contains it. `public/install*` is then only ever a generated copy. `config/vite/installerAssets.ts`, the `Dockerfile`, `scripts/local-update-checkout.mjs` and the Agent's journeys keep reading `public/`, so none of them change.

### RL-3, RL-5 and RL-7 Record, render and copy guard

**One Markdown file, two states.** Nothing about a Draft changes. A Final record is the same file with `**State:** Final` and, under `## Publication`, exactly one fenced `json` block:

| Key | Value |
| --- | --- |
| `version` | `major.minor.patch` |
| `kind` | `patch`, `minor`, `major`, or `legacy` (only the lowest-numbered Final record) |
| `required` | `null`, or the reason as a non-empty string |
| `app`, `agent`, `runtime` | 40 lowercase hex characters each |
| `runtime_schema_digest` | `sha256:` and 64 hex characters |
| `tools` | the manifest's `tools` object, verbatim |
| `vibecomfy`, `lifecycle` | the manifest's blocks, verbatim (the App's `checkManifest` requires both since Release 11) |
| `pinokio` | optional, 40 hex; informational, never rendered |
| `legacy_versions` | only with `kind: legacy`: the versions of every earlier release, keyed by release number ([D5](inputs.md#owner-decisions)) |

**`readRecords(dir)` refuses,** each with its own test: a Final record with more or fewer than one `## Publication` section, or more or fewer than one fenced `json` block in it; a payload that is not one JSON object; a missing key; a key not in the table; a malformed SHA, digest or version; an unknown `kind`; `legacy` on any record but the lowest Final; a version that is not the previous Final record's version stepped once by `kind`; an empty `required` reason; a gap in the Final records' numbers; a Draft numbered below a Final record. A Draft's body is never parsed beyond its number and state.

**Dropped from the 8 Nov list:** "a final record whose pins disagree with its included plans". Nothing in a plan file names a commit, so no check can decide it.

**`render --records <dir> --release N [--payload-file F]`** writes the manifest: `schema_version` 1, `release` N, `version`, `versions`, `app.sha`, `agent.sha`, `runtime.sha` and `runtime.schema_digest`, `tools`, `vibecomfy`, `lifecycle`, and `required` only when a floor exists; two-space indent and one trailing newline, as `pin.mjs` writes today.

- `versions` maps every release from 1 to N: the legacy record's `legacy_versions`, then each Final record's own `version`.
- `required` is `{release, reason}` of the highest Final record at or below N whose `required` is not null, so a floor stays in force until a later record sets a new one, as it does today.
- A Draft does not render. `--payload-file` renders a *candidate*: the same function over a payload that is not yet in a record, for the number one above the newest Final. That lets a candidate be qualified on the exact bytes that will ship.
- The 8 Nov design also rendered `source`, the astrid-dev commit. It is cut: the render is then a pure function of the records, so a candidate's bytes and the published bytes are the same.

**`check-record --records <dir> --release N [--payload-file F] --app-dir A --agent-dir G --runtime-dir R`** is everything except the approval: render; each of `app`, `agent`, `runtime` is an ancestor of `origin/main` in its clone (reachable is not enough: GitHub serves fork and pull-request commits through the parent repository); then `manifest-check` on the render, with the bootstraps from the record's `app`.

**`verify --base <sha> [--head <sha>] --astrid-dev <dir>`** decides whether a change may touch the four generated files: `public/install`, `public/install.sh`, `public/install.ps1`, `public/install-manifest.json`.

| Rule | Case |
| --- | --- |
| G1 | The four files are unchanged between base and head: pass, without reading astrid-dev |
| G2 | They equal the render of the newest Final record N and the bootstraps at that record's `app`, `check-record` passes, and the gate passes for N: pass |
| G3 | The manifest differs from the render by any byte: refuse |
| G4 | A bootstrap differs from the record's `app` by any byte: refuse |
| G5 | The head's `release` is below the base's: refuse |
| G6 | The head's `release` names a Final record that is not the newest: refuse |
| G7 | Record N is missing or a Draft: refuse |
| G8 | The gate refuses: refuse, and print its lines |
| G9 | `app`, `agent` or `runtime` is not an ancestor of its repository's `main`: refuse |
| G10 | `manifest-check` refuses the result: refuse |
| G11 | Any other path under `public/` whose name starts with `install` is added or changed: refuse |
| G12 | The astrid-dev directory, a clone, git or the network is missing or errors: refuse |
| G13 | Anything but `version`, `versions` and `app` differs between the base's and the head's manifest, or any bootstrap byte differs, and the head's `release` is not above the base's: refuse. This keeps the rule `release-guard` enforces today: a different installer always has a higher number |

- **`write --astrid-dev <dir>`** computes the same bytes and writes them. **`write --candidate <payload> --release N --records <dir>`** writes a candidate copy for qualification; it can never pass the guard, because no Final record matches it.
- **The job** `install-copy-guard` lives alone in its own workflow file, triggered only by pull requests to `main`, with no job-level `if`, `contents: read` and no `npm ci`; it clones astrid-dev `main`, and the Agent and Runtime, and runs `verify`. A job of that name in a workflow with other triggers could be skipped on a push or a manual run and leave a passing-looking check on the same commit, which is why it leaves `test.yml`; a case in `install-copy.test.mjs` fails if any other workflow file defines a job with that name. The alarm for a write that went around the rules is the canary (RL-8), which runs on every deployment.
- **`.github/CODEOWNERS`** names the approving account (D1, D4) for `/.github/`, `/scripts/installer/`, and the two files that decide which bytes are served at the installer URLs, `/config/vite/installerAssets.ts` and `/Dockerfile`. Its `/scripts/installer/` line is both the App's review rule (D3 a) and the list of release approvers the gate reads.
- **`pin.mjs`** keeps `checkManifest` and `--check`, and gains `--print <agent sha>`, which prints `runtime`, `runtime_schema_digest`, `vibecomfy` and `lifecycle` for a payload. It stops writing the manifest. Plan 29 already removed `release-check.mjs` and `update-manifest.mjs` (absent at App `6545f13`).
- **No fallback for old App commits.** A record's `app` must contain `scripts/installer/bootstrap/`. The live record's `app` is therefore the commit that lands RL-2 on App `main` (RL-G step 1), whose bootstraps are byte-identical to what is served.
- **App pull request #208** (the version helper) closes unmerged; nothing from it is used. Its state could not be read from the planning session.

### RL-4 and RL-6 The approval gate

`node scripts/installer/release-approval.mjs --astrid-dev <dir> --release N [--approvers-at <App sha>]` answers one question: did a release approver approve the exact change that made record N Final, and has the record stayed as approved? It reads a git checkout of astrid-dev, the App's `CODEOWNERS`, and the public REST API (with `GITHUB_TOKEN` if set, for the rate limit). It writes nothing. It refuses unless every line below holds, and on any API error, missing field or shape it does not recognize.

**The refusal list (RL-4 writes one test for each; RL-6 makes them pass):**

1. The App's `.github/CODEOWNERS`, read at the pull request's *base* (or at `--approvers-at`), has no line for `/scripts/installer/`, or that line names a team or nobody. **The release approvers are the code owners of the App's installer code,** read from before the change, so a pull request cannot add its own approver.
2. No commit on astrid-dev `main`'s first-parent history turns `releases/N.md` from absent or Draft to Final. The most recent one that does is the *finalizing commit*.
3. `releases/N.md` at the tip differs from the same file at the finalizing commit.
4. The finalizing commit is not the merge commit of exactly one merged pull request into `main` (`GET /repos/banodoco/astrid-dev/commits/{sha}/pulls`). A direct push fails here, including one by an identity that bypasses the pull-request rule; so does a rebase merge, so the finalizing pull request is merged by merge commit or squash.
5. That pull request has no review in state `APPROVED` from a release approver whose `commit_id` is the pull request's final head, or that approver's latest review is not the approval (changes requested later, or dismissed).
6. `releases/N.md` at the finalizing commit differs from the same file at that approved head. This binds the approval to the bytes that landed: without it, a second pull request merged in between could add to the record what the owner never saw.
7. Any lower-numbered Final record fails lines 2 to 6. A release cannot be approved on top of an unapproved one, because `versions` and the required floor are read from them.

`--commit <sha>` runs lines 1, 4 and 5 against a named astrid-dev commit; it exists for the live proofs.

Two checks the first draft had are cut: that the approver is not the author (GitHub already refuses a self-approval), and that App `main`'s ruleset requires code-owner review (if it does not, this check is not required either, so it cannot fail closed; O-1's proof shows the rule instead).

**No `CODEOWNERS` and no code-owner review in astrid-dev.** Release 12's Draft brief was changed by 24 commits in two days, by managers, and a Draft must stay that free. Turning a Final record back to Draft is the one way to correct a mistaken one; making it Final again needs a fresh approval, because the finalizing commit is then the new one.

**Why S and then N.** The list is the security boundary and cannot run end to end until RL-G, so writing it is S and it is reviewed at RS1 before any code exists. Once the tests exist, making them pass is ordinary work over recorded responses.

### RL-9 `release-contract`

A new workflow file in astrid-dev, so `docs.yml` (which Plan 48 also edits) stays as it is. One job, `release-contract`, on pull requests and on push to `main`. It is **not a required check**: draft briefs change many times a day, and a job that reads three other repositories must never be able to block them. Its steps run only when the change makes or alters a Final record.

1. Check out the App at the branch named like the pull request's base if it exists there, else `main` (this is what lets the job be proven on `int/31` before Release). Clone the Agent and the Runtime.
2. `node <app>/scripts/installer/install-copy.mjs check-record --records releases --release N ...` for the newest Final record: render, ancestry, `manifest-check`. Ancestry comes first.

It does not check the approval: the pull request it runs on is the one being approved. It is early warning for the owner before she approves. What protects users is the App's guard, which runs the same `check-record` again, from reviewed code, before any copy lands.

**Cut from the 8 Nov card:** running the Agent's `validate_manifest` from the record's Agent and the previous one. A candidate is qualified by the Agent's journeys on a copy with the same bytes (`journey.yml` reads `public/install*` from the App checkout), including the update rows from earlier releases, so a manifest an Agent refuses fails there first. Read by code at Agent `a105de3`, `709492fa` and `6e9c4f9c` (Releases 11, 9 and 10): `validate_manifest` has no closed set of top-level keys, so the added `version`, `versions` and `app` do not break an installed Agent's update.

### RL-10 Release skill

The "Publishing an installer release" list becomes these steps. Today's step 0 (cover real install states) stays in front of them unchanged; today's step 1 is step 2 here.

1. **Candidate.** Freeze the Agent, Runtime and App candidates. Get the derived pins with `node scripts/installer/pin.mjs --print <agent sha>` and write the payload file. Write the candidate copy on the App candidate branch with `install-copy.mjs write --candidate`; qualify on it. Record the manifest's SHA-256.
2. **Owner's go, in this session,** on the exact SHAs.
3. **Merge code:** Agent, then Runtime, then the App's code candidate *without* the candidate copy commit. The hosted App deploys; that is not a release.
4. **Decide:** open the astrid-dev pull request that turns `releases/<N>.md` Final with that payload and sets the strategy row to `final`. `release-contract` must pass. The owner approves it on GitHub from the approving account; that approval is the durable go. Merge by merge commit or squash. `release-approval.mjs --release N` passes: the release is *decided*.
5. **Publish:** in an App checkout of `main`, `install-copy.mjs write`, open the pull request, `install-copy-guard` passes, merge: *published*. The manifest's SHA-256 equals the one qualified in step 1, or stop.
6. **Live:** wait for the deploy and the canary, then confirm the served manifest.
7. Bring integration branches up to `main`.
8. Close the project.

**Withdrawing a decided release:** close its App copy pull request first, then turn the record back to Draft. A green check on an open copy pull request is not re-run when astrid-dev changes.

"One publisher at a time" keeps its rule and loses its mechanism: the guard refuses a copy that is not the newest Final record, so two projects cannot both publish a number. "Take stock of open pull requests" is not touched.

### RL-11 The live record

- **Which release:** the `release` in `https://astrid.haus/install-manifest.json` when the run starts, saved to the run folder by the hosting session. Release 12 is expected; if it is, `releases/12.md` already exists as a Draft and this task flips it. If the live release has no brief, write one from its publish receipts only, with one honest sentence per section.
- **Payload:** copied from the served manifest; `app` is the App `main` commit that lands RL-2 (RL-G step 1), a placeholder until then; `kind` is `legacy`; `version` and `legacy_versions` follow [D5](inputs.md#owner-decisions).
- **Why its own branch:** the approval has to be on a pull request that does one thing, and the App's approver list has to be on App `main` first.
- **Fixtures:** every golden fixture overlays whole copies of `releases/12.md` or `strategy.md`. When the real brief turns Final they must be refreshed so each still differs from the real tree by its one defect; `golden.txt` must come out byte-identical. If a line would change, stop and ask. If Plan 48's Phase 2 has changed how fixtures are stored, follow what it left.
- **`plans/releases.md`** gets one closing line: later releases are the files in `releases/`. Its two rows stay; astrid-dev pull request #82, still open, closes unmerged.

### RL-G Go live

Each step is the Release skill's, with the owner's go in the publishing session; her settings changes fall between steps.

1. **App `int/31` → `main`.** The four generated files are unchanged, so nothing users install changes; `CODEOWNERS` and the guard's workflow arrive. **O-1.** Then one throwaway pull request into `main` that edits `public/install.sh` shows `install-copy-guard` failing as a required check; close it.
2. **astrid-dev `int/31` → `main`:** `release.yml`, the skill, the template paragraph and `env/`. No record is Final yet.
3. **Negative proof, live:** `release-approval.mjs --commit <step 2's merge commit>` refuses, naming the missing approval.
4. **The live record:** set `app` in `rel/31-live-record` to step 1's merge commit, in the record and in each refreshed overlay, and run the astrid-dev inventory. Open the pull request against astrid-dev `main`. `release-contract` passes, its first PASS. The owner approves from the approving account. Merge. `release-approval.mjs --release <live>` passes: the gate's first run on a real record, on a release that is already live.
5. **The first copy:** `install-copy.mjs write` in the App, pull request, guard green, merge. The diff touches only `version`, `versions` and `app` in the manifest and no bootstrap byte. Deploy; the canary passes, including RL-8's step.

The next release is then published by the eight steps in RL-10; that is the plan's completion, and it is the first time a tuple changes through this path.

### RL-14 and RL-14t Versions on screen

- **Hosted:** `checkHostedUpdate` reads `version` and `versions` from the manifest it already loads; `UpdateStatus` gains `version` (the installed release's, from `versions`) and `servedVersion`, both optional.
- **Local launcher:** `localUpdateStatus.ts` already fetches the served manifest for the required floor; it adds the same two fields to its reply, and `checkLocalUpdate` reads them.
- **No name without a version.** If the manifest gives no version for a release, the line names none ("Astrid is up to date", "Update available"); it never falls back to a release number. RL-14t decides the exact words.
- **Kind** is not shown.
- **Order against Plan 30:** its LA-2 changes `localUpdateStatus.ts` and `updateStatus.ts`. Whichever starts second starts from the other's result.

### If the owner decides otherwise

- **D1 b (no separate approving account):** RL-4, RL-6, rule G8 and O-0's approval have nothing to verify. The plan then delivers records, the contract job and a byte-exact copy, and says plainly that it does not control who publishes. RS1 and one review round go.
- **D2 b (the 8 Nov transport: a `release-published` branch and a scheduled job that pushes to App `main`):** add a `publish-release` job and its superseded-run guard in astrid-dev; a ruleset on `release-published`; a write credential for App `main` kept as an environment secret that only `main`'s workflows can use, with a ruleset bypass; the `release-sync` workflow and its off switch. RL-7 is re-planned, the writer becomes an S task, and phase 1 grows by two to three days. Rules G1 to G13 are still needed, because the branch can be written by anyone with push access.
- **D3 b (no code-owner review on App `main`):** no card changes; `CODEOWNERS` is then only the approver list, which any merged pull request can edit; the [limit](plan.md#completion) is stated in the plan.

**Overlap with other projects:**

- **[Plan 48](../48-one-record-model/plan.md).** Phase 1 is on `main`. The owner said on 11 Nov 2026 that this plan is queued after Plan 48's Phase 2 ([its D6](../48-one-record-model/inputs.md#owner-decisions)), which moves status and owner into each `plan.md`, generates `plans/index.md`, deletes `check_docs.py` and gives a bot a bypass on `main`. This plan adds no check and no Python, so the only places they meet are RL-11 (the golden fixtures and `strategy.md`) and this pack's own header fields; re-read both against Phase 2's result before the run starts. The bot's bypass is why the gate refuses a record made Final by a direct push.
- **Plan 29** changes the same App files (the guard RL-7 deletes, the update screens RL-14 edits), so this plan starts after Plan 29 is on App `main` and Release 12 is published.
- **Plan 30** (queued): LA-2 and UR-17 touch the update status readers and cards; see RL-14.
- **The Release skill** is edited by RL-10 and by Plan 29's post-publish pull request (re-syncing `runtime.lock.json`). Start RL-10 from whichever has landed.
