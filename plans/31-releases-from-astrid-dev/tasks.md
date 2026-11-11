# Tasks — Releases defined and published from astrid-dev

[Plan](plan.md) · [Inputs](inputs.md)

**Not authorized to run.** The owner asked on 11 Nov 2026 for this plan to be brought up to date and made ready to execute; that is an instruction to prepare, not a go. The scope decision and owner decisions D1 to D7 in [inputs.md](inputs.md#owner-decisions) are open. These cards are written for the recommended answers (D1 a, D2 a, D3 a); [what changes under the other answers](#if-the-owner-decides-otherwise) is at the end.

Routes: **N**, **X**, **S**, **T** per the [run contract](../../skills/astrid-dev-shared/run-contract.md). X and S tasks delegate reading, mechanical edits and checks to N helpers. An N task that misses the same acceptance check twice re-routes to X with the worker's notes.

**Task ids:** `RL-<n>`. This re-plan (11 Nov 2026) renumbers the 8 Nov cards; [the old-to-new map](#what-changed-from-the-8-nov-cards) is below.

**Where work lands.** Every task lands by pull request on `int/31-releases-from-astrid-dev`, in astrid-dev and in the App, cut from each `main` when the run starts (after Plan 29 is on App `main` and Release 12 is published). Record each task's base SHA when it starts. Only the [Release skill](../../skills/astrid-dev-release/SKILL.md) moves either branch to `main` (RL-G). One exception: RL-1g's record change is prepared on its own branch and opens against astrid-dev `main` during RL-G, because it has to be a separately approved pull request.

**Phases.** Phase 1 is every row down to RL-G: a release is a record in astrid-dev, and the App can only carry a checked copy of it. Phase 2 is RL-3a, RL-3t and RL-9: users see versions, and the temporary parts are deleted.

**Critical path:** RL-1a → RL-1c → RS1 → RL-1d → RL-2d → R → RL-G. RL-2c runs beside RL-1c and joins at RS1. Everything else hangs off that chain and runs in parallel: RL-0, RL-2a and RL-2b start at once; RL-1b after RL-1a; RL-1e after RL-1b and RL-2a; RL-1g after RL-1b. Shortest elapsed time is about six working days.

**Test inventory.**

- *astrid-dev* (standard-library `unittest`, the whole inventory runs in under a minute, so by the run contract's cost exception all of it runs at every load-bearing moment). New: `scripts/test_release_record.py`, `scripts/test_release_gate.py`. Added to, never edited: `scripts/fixtures/golden.txt` (new lines for new fixtures only), `scripts/test_checks.py` (only if it lists check ids). Affected and must pass unedited: `scripts/test_golden.py`, `scripts/test_check_docs.py`, `scripts/test_views.py`, `scripts/test_checks.py`. Every other `scripts/test_*.py` must stay green.
- *App, phase 1* (`node --test`). New: `scripts/installer/manifest-check.test.mjs`, `scripts/installer/install-copy.test.mjs`. Affected: `scripts/installer/release.test.mjs` (the guard and pin cases are deleted in RL-2d; the served-canary case stays), `scripts/installer/bootstrap.test.mjs`, `scripts/installer/bootstrap-powershell.test.mjs` (hosted Windows only), `scripts/installer/manifest.test.mjs`, `config/vite/installerAssets.test.ts`. Not affected, must stay green: `scripts/installer/local-update-canary.test.mjs`.
- *App, phase 2* (`vitest`): `src/shared/lib/updates/updateStatus.test.ts`, `config/vite/localUpdateStatus.test.ts`, `src/shared/components/SettingsModal/sections/AstridUpdatesSection.test.tsx`, and in `src/shared/components/RuntimeConnection/`: `QuietUpdateNotice.test.tsx`, `FullyLocalUpdate.test.tsx`, `InstallerUpdateCallers.test.tsx`, `SourceCheckoutUpdateSurface.test.tsx`. Each asserts a `Release <n>` string today.

**Load-bearing test moments.** Before the first task: both inventories on the starting SHAs (the App's after RL-0, which the [manage skill](../../skills/astrid-dev-manage/SKILL.md) allows to run first). After each task: its own focused proof. Before others build on a shared part: RL-1a's tests before RL-1b, RL-1c and RL-2c start; RL-1c's and RL-2c's tests at RS1. Before R: the full workflows once per repository on the integrated heads, on CI.

**Checks a worker can run.**

```text
# astrid-dev (no setup; standard library only)
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p "test_*.py"
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py check
PYTHONDONTWRITEBYTECODE=1 python3 scripts/astrid_dev.py sync

# App (after RL-0; from the checkout root, literal paths, no cd)
bash scripts/worker-env/app-setup.sh
node --test scripts/installer/<file>.test.mjs
npx vitest run --config config/testing/vitest.config.ts <files>
```

Another repository's files come from public git at a pinned commit (`git clone --filter=blob:none https://github.com/banodoco/<repo>`), never from an archive download. `checkManifest` in the App reads `raw.githubusercontent.com`; a network failure there is an environment problem (exit 3), never a test result, and every proof that needs it is labelled *hosted*.

**Proof labels.** *Local* runs in the task's worktree at its candidate. *Hosted* is the named CI job on the task's pull request into `int/31-releases-from-astrid-dev`, judged by its inner step, and is run by the hosting session.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Owner** | | | | | |
| O-0 Answer D1 to D7 and the scope decision; create the approving identity D1 names | owner | — | [inputs.md](inputs.md#owner-decisions) | Each decision carries a date and the owner's choice; the approving account exists and is not one an agent session can act as | [ ] |
| O-1 astrid-dev `main` ruleset: add code-owner review, dismiss stale approvals, and require `release-contract` beside the two checks required today | owner | RL-G step 3 | astrid-dev repository settings | `GET /repos/banodoco/astrid-dev/rules/branches/main` shows `require_code_owner_review: true`, `dismiss_stale_reviews_on_push: true` and the three checks | [ ] |
| O-2 App `main` ruleset: require a pull request and the `install-copy-guard` check (it replaces `release-guard` if Plan 29's owner row made that required); with D3 a, also code-owner review | owner | RL-G step 1 | App repository settings | The App's branch rules show the pull-request rule, `install-copy-guard` required, `release-guard` gone and, with D3 a, code-owner review | [ ] |
| **Build: worker environment** | | | | | |
| RL-0 App worker setup script | N | — | astrid-dev `env/app-setup.sh` (new), `env/smoke.sh` (`app` mode), `env/README.md` (table row and the call list); App `scripts/worker-env/app-setup.sh`, `scripts/worker-env/smoke.sh` (new, byte copies) | Local, App worktree: `bash scripts/worker-env/smoke.sh app scripts/installer/release.test.mjs` prints `ENV-PASS` and runs that one file; with a Node other than 20.19.x first on `PATH` it exits 3. `cmp` of each App copy with its `env/` source is silent | [ ] |
| **Build: the record (astrid-dev)** | | | | | |
| RL-1a The final-record contract, tests first. What a Final record's payload holds, what `check` refuses, what `render` writes, and the command lines, as failing tests | X | — | astrid-dev `scripts/test_release_record.py` (new), `scripts/release_record.py` (new: signatures and docstrings only), `scripts/fixtures/final-record-clean/overlay.json`, `scripts/fixtures/final-record-bad-pin/overlay.json` (new) | Local: `test_release_record.py` exists and fails only on the cases RL-1b implements; the rest of the inventory passes; `golden.txt` is unchanged (the new fixtures print nothing until RL-1b registers the check) | [ ] |
| RL-1b Record check and render against RL-1a's tests; register the checks | N | RL-1a | astrid-dev `scripts/release_record.py`; `scripts/checks.py` (two thin wrappers and two `REGISTRY` entries, nothing else); `docs/checks.md` (regenerated by `astrid_dev.py sync`); `scripts/fixtures/golden.txt` (added lines only); `scripts/test_checks.py` (added lines only, if it lists ids) | Local: the whole astrid-dev inventory passes with no existing test or golden line edited; `astrid_dev.py list` shows `release-records always` and `release-immutable pr`; `astrid_dev.py check` passes on the real tree; `python3 scripts/release_record.py render --release <a Draft's number>` exits non-zero and says the record is a Draft | [ ] |
| RL-1c The approval gate's contract, tests first. Every way a Final record can be on `main` without the owner's approval, as failing tests over recorded API responses | S | RL-1a | astrid-dev `scripts/test_release_gate.py` (new), `scripts/release_gate.py` (new: signatures only), `scripts/fixtures/gate/*.json` (new: recorded responses) | Local: `test_release_gate.py` exists and fails only on the cases RL-1d implements; its cases cover [the refusal list](#rl-1c-and-rl-1d-the-approval-gate) one for one. The S lead returns that list with one line per refusal saying which test holds it | [ ] |
| RS1 Review stop after the trust root's contracts (rounds at most 1). Protects RL-1d, RL-2d and RL-G: a hole found at the final review would mean redoing both implementations, and one found after go-live would have let an unapproved installer through | S | RL-1a, RL-1c, RL-2c | read-only: the three tests-first tasks and RL-1b if landed | Same protocol as R, on `int/31` in both repositories; the reviewer is briefed "find what would let an unapproved installer publish, in code, not in the cards". Findings become rows `RS1.<n>`; RL-1d and RL-2d depend on this row | [ ] |
| RL-1d The gate, and `CODEOWNERS` | N | RS1, RL-1b | astrid-dev `scripts/release_gate.py`; `.github/CODEOWNERS` (new) | Local: the whole astrid-dev inventory passes. Local, live public API, read-only: `python3 scripts/release_gate.py --repo banodoco/astrid-dev --commit 12a54b6d8baa220fbe3d3a48e3a04f48b0511c07` exits non-zero and names both "main does not require code-owner review" (true until O-1) and "no approval from a release approver on the final head". The positive path first runs in RL-G step 5 | [ ] |
| RL-1e `release-contract` job: the newest Final record against the real consumers | N | RL-1b, RL-2a | astrid-dev `.github/workflows/release.yml` (new); `scripts/release_record.py:ancestry` and its tests in `scripts/test_release_record.py` | Local: the `ancestry` tests pass on temporary repositories. Hosted (hosting session, once RL-1g's branch exists): on a draft pull request from `rel/31-live-record` into `int/31`, kept open and never merged there, `release-contract` PASSES; on one throwaway pull request, closed unmerged, whose record names an Agent commit that exists but is not on Agent `main`, it FAILS at the ancestry step; on a pull request that touches no release file, its steps skip and the job is green | [ ] |
| RL-1f The Release skill plans, finalizes and publishes through records | N | RL-1d, RL-2d | astrid-dev `skills/astrid-dev-release/SKILL.md` ("Agent/Runtime installer tuple" lane, "One publisher at a time", "Publishing an installer release", the "Installer tuple" runbook line); `releases/TEMPLATE.md` (the paragraph under `## Publication` only) | Local: `astrid_dev.py check` passes; `grep -n -e "release-guard" -e "release guard" -e "pin.mjs <" skills/astrid-dev-release/SKILL.md` prints nothing; the skill holds [the eight steps](#rl-1f-release-skill) in order, names draft, decided, published and live, and still has "Take stock of open pull requests" unchanged; the template still has `## Included pull requests` | [ ] |
| RL-1g The live release as the first record, prepared and not merged | N | RL-1b | astrid-dev, on branch `rel/31-live-record` cut from `int/31`: `releases/<live>.md` (State, Publication), `strategy.md` (that row's state word), every `scripts/fixtures/*/overlay.json` that carries `releases/<live>.md` or `strategy.md` (refreshed so each still shows only its one defect), `plans/releases.md` (a closing line), `scripts/fixtures/final-record-clean/overlay.json` (the same payload) | Local: `python3 scripts/release_record.py render --release <live>` equals the served manifest saved at run start as parsed JSON, once `version`, `versions` and `app` are removed from the render; the whole inventory passes with `golden.txt` byte-identical to `int/31`. The pull request to `main` opens in RL-G step 5 | [ ] |
| RL-1t Words people read in astrid-dev: every refusal and error line of `release_record.py` and `release_gate.py`, and the Release skill's new steps | T | RL-1b, RL-1d, RL-1f | astrid-dev `scripts/release_record.py`, `scripts/release_gate.py` (message strings only); `skills/astrid-dev-release/SKILL.md` (wording of RL-1f's text only); `scripts/fixtures/golden.txt` (only the lines RL-1b added) | Before and after for every string, in the pull request. Rules: plain words; each refusal says what is wrong, in which file or pull request, and the one next step; never implies a release happened. The inventory passes; no line from before this plan changes | [ ] |
| **Build: the App's checked copy** | | | | | |
| RL-2a One manifest check command | N | RL-0 | App `scripts/installer/manifest-check.mjs`, `scripts/installer/manifest-check.test.mjs` (new); `package.json` (`test:node` file list) | Local: `node --test scripts/installer/manifest-check.test.mjs` passes: with `--offline`, today's `public/install-manifest.json` and `public/` bootstraps are accepted; a manifest with `version`, `versions` and `app.sha` is accepted; a `versions` map that lacks the manifest's own release, a short `app.sha`, and a uv pin that differs from `install` are each refused. Hosted: without `--offline` it prints `checkManifest`'s line for `main`'s manifest | [ ] |
| RL-2b Bootstrap source moves out of `public/` | N | RL-0 | App `public/install`, `public/install.sh`, `public/install.ps1` → `scripts/installer/bootstrap/` (`public/` keeps byte-identical copies); `scripts/installer/bootstrap.test.mjs`, `scripts/installer/bootstrap-powershell.test.mjs`, `scripts/installer/fixture.mjs` (paths) | Local: `node --test scripts/installer/bootstrap.test.mjs` passes against the moved source; `cmp` of each source with its `public/` copy is silent; `scripts/installer/manifest.test.mjs` and `config/vite/installerAssets.test.ts` are unchanged and pass. Hosted: `Windows installer` runs on the task pull request and its test step passes | [ ] |
| RL-2c The copy guard's contract, tests first. When a change to `public/install*` is allowed, as failing tests over temporary repositories and stubbed `render` and gate commands | X | RL-1a, RL-2a | App `scripts/installer/install-copy.test.mjs` (new), `scripts/installer/install-copy.mjs` (new: exports and usage text only) | Local: the test file exists and fails only on the cases RL-2d implements; its cases cover [rules G1 to G12](#rl-2c-and-rl-2d-the-copy-guard) one for one | [ ] |
| RL-2d The guard, the write command, and the old pin path deleted | N | RS1, RL-2b, RL-2c, RL-1b, RL-1d | App `scripts/installer/install-copy.mjs`; `.github/workflows/test.yml` (job `install-copy-guard` replaces job `release-guard`); deleted: `scripts/installer/release-guard.mjs`, its cases and the `applyRequiredPin` case in `scripts/installer/release.test.mjs`; `scripts/installer/pin.mjs:pin`, `applyRequiredPin`, `main` (write mode goes, `--print` arrives, `--check` and `checkManifest` stay); `README.md` (the pin line); `package.json` (`test:node` file list); with D3 a, `.github/CODEOWNERS` (new: `/.github/` and `/scripts/installer/`) | Local: `node --test scripts/installer/install-copy.test.mjs scripts/installer/release.test.mjs scripts/installer/manifest.test.mjs` passes. Local, with astrid-dev `int/31` cloned beside it: `node scripts/installer/install-copy.mjs write --candidate <RL-1g payload file> --release <live> --astrid-dev <dir>` changes only `version`, `versions` and `app` in `public/install-manifest.json` and no bootstrap byte. `git grep -n -e release-guard -e applyRequiredPin` prints nothing. Hosted (hosting session): on a throwaway pull request that edits `public/install.sh`, `install-copy-guard` FAILS; on the task pull request it passes | [ ] |
| RL-2e The canary also checks the deployed copy against its record | N | RL-2d | App `.github/workflows/served-manifest-canary.yml` (one step in job `canary`); `scripts/installer/install-copy.mjs:verifyDeployed` and its cases in `scripts/installer/install-copy.test.mjs` | Local: the added cases pass: a copy that matches its record passes; a copy with one changed byte fails; a manifest with no `version` (a copy from before the first record) is skipped with a line that says so. The live run is RL-G step 6 | [ ] |
| RL-2t Words people read in the App's guard: every refusal of `install-copy.mjs` and `manifest-check.mjs` | T | RL-2a, RL-2d | App `scripts/installer/install-copy.mjs`, `scripts/installer/manifest-check.mjs` (message strings only), and the same strings in their two test files | Before and after for every string, in the pull request, under RL-1t's rules; a refusal on a hand edit says the file is generated and names the record to change instead. Both test files pass | [ ] |
| **Review: before anything reaches `main`** | | | | | |
| R Review rounds on the integrated pipeline (at most 2, pending the owner) | S | every row above except O-1, O-2 | read-only: all Plan 31 scopes in both repositories | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md), after the full workflows have run once per repository on the integrated heads. Findings become rows `R<round>.<n>` directly below this one, each with route, scope, dependencies and proof; RL-G waits for them | [ ] |
| **Publish** | | | | | |
| RL-G Go live through the Release skill (owner's go, in the publishing session) | release | R, O-0 | App and astrid-dev `main` (Release skill only) | [The six steps](#rl-g-go-live) in order, each with its receipt. It ends when the canary passes for a deployed App commit whose copy was written from the live record. Plan completion is separate: the first new release published this way | [ ] |
| **Phase 2: on screen, and clean up** (lands on `int/31` after RL-G; RL-3a and RL-3t ship as an ordinary hosted App deploy, with no review round beyond pull-request review) | | | | | |
| RL-3a Users see versions, not release numbers | N | RL-G; RL-1b (the manifest's `version` and `versions`); Plan 30's LA-2 if it has started | App `src/shared/lib/updates/updateStatus.ts` (`UpdateStatus`, `checkHostedUpdate`, `checkLocalUpdate`); `config/vite/localUpdateStatus.ts` (the status body); `src/shared/components/SettingsModal/sections/AstridUpdatesSection.tsx` (the status line and the Installed value); `src/shared/components/RuntimeConnection/QuietUpdateNotice.tsx` (the notice line); the seven phase 2 test files | Local: `npx vitest run --config config/testing/vitest.config.ts` on the seven phase 2 test files passes, showing a version where the manifest names one and no name where it does not, hosted and local launcher. Each test feeds a manifest written by `release_record.py render`, not hand-written fields. `git grep -n -e 'Release ${' -e 'Release {' -- src config` prints nothing | [ ] |
| RL-3t The update lines themselves | T | RL-3a | App: the strings RL-3a touched, plus `resolveUpdate.ts` ("A newer release of Astrid is available."), `AstridUpdatesSection.tsx` ("Connect to Astrid before checking its release.") and `updateStatus.ts` ("Release information was invalid"), and the same strings in their tests | Before and after for every string, shown to the owner. Rules: plain words; a version, never a release number; never names a version the manifest did not give; every line that reports a problem has a next step. The seven test files pass | [ ] |
| RL-9 Delete what was temporary | N | the first new release published after RL-G | App `scripts/installer/install-copy.mjs` (the `public/` fallback for a record whose `app` predates RL-2b, and `verifyDeployed`'s skip for a copy with no `version`) and their cases; the throwaway branches and pull requests RL-1e and RL-2d opened; `rel/31-live-record`; `int/31-releases-from-astrid-dev` in both repositories once fast-forwarded | Local: `node --test scripts/installer/install-copy.test.mjs` passes with the two cases removed; `git grep -n "predates" -- scripts/installer` prints nothing; `git ls-remote --heads` shows none of the named branches | [ ] |

Add task details beneath the index only when useful. Scope names the paths, and any shared surface or contract, the task may change (a path includes its own tests, wherever they live); tasks with overlapping scopes need a dependency.

## Size

Days are one agent's working time, not elapsed time. The catalog holds the plan's total.

| Task | Days | Task | Days |
| --- | --- | --- | --- |
| RL-0 | 0.5 | RL-2a | 0.5 |
| RL-1a | 1 | RL-2b | 0.5 |
| RL-1b | 0.75 | RL-2c | 0.75 |
| RL-1c | 0.75 | RL-2d | 1 |
| RS1, with its findings | 0.75 | RL-2e | 0.25 |
| RL-1d | 0.5 | RL-2t | 0.25 |
| RL-1e | 0.75 | R, with its findings | 1.5 |
| RL-1f | 0.5 | RL-G | 0.5 |
| RL-1g | 0.5 | RL-3a | 0.75 |
| RL-1t | 0.25 | RL-3t, RL-9 | 0.25 each |

Phase 1 (every row to RL-G) is 11.5 days; phase 2 is 1.25.

By route: N 6.75 days (12 tasks), X 1.75 (2), S 3 (RL-1c 0.75, RS1 0.75, R 1.5), T 0.75 (3), release 0.5. Total 12.75, range 10 to 16: the range is the hosted proofs in RL-1e and RL-2d, which repeat slowly when wrong, and review findings.

## Who runs each task

Codex does the writing wherever a Codex model can; the hosting Claude session does what Codex cannot. Codex routes are the run contract's: N → Luna, X → Terra, S → Sol.

| Task | Writes it | The hosting session does |
| --- | --- | --- |
| RL-0, RL-1b, RL-1d, RL-1f, RL-1g, RL-2a, RL-2e, RL-3a, RL-9 | Codex, Luna | Commits, opens and merges the task pull request. For RL-1g it first saves the served manifest into the run folder; for RL-9 it deletes the remote branches |
| RL-1e, RL-2b, RL-2d | Codex, Luna | The same, plus the hosted proof: it opens the throwaway pull requests, reads the job's inner step, and closes them |
| RL-1a, RL-2c | Codex, Terra | Commits and opens the pull request; runs the tests once to see they fail only where the card says |
| RL-1c | Codex, Sol | The same |
| RL-1t, RL-2t, RL-3t | Hosting session, a named sub-agent on the high-judgment role | All of it. RL-3t's before and after goes to the owner |
| RS1, R | Hosting session, a named reviewer on the high-judgment role, with no part in the build | All of it; findings come back as cards Codex can take |
| RL-G | Hosting session with the owner | All of it: it needs the owner's go in that session, her settings changes and her approval |
| O-0, O-1, O-2 | Owner | Brings her each one with the exact setting to change |

**Codex's share:** 15 of the 21 build, review and publish rows and 9.25 of the 12.75 days (about 73%). X is needed only for the two contracts that are written as tests before any code exists: what a record is, and when the App accepts a copy. S is needed only for the gate's refusal list, which is security and cannot run end to end before go-live. Everything else is N because the tests exist first and the cards name every file.

## Dispatch notes

**Recommended manager route: S,** by the [orchestrate skill's table](../../skills/astrid-dev-orchestrate/SKILL.md#choose-the-managers-route): this is a release, across two repositories, with a security boundary, and one wrong call (merging a guard that passes too much) reaches every user.

**Recommended shape: the hosting Claude session manages; Codex executes.** A Codex sandbox cannot commit or push ([Plan 48's run note](../../docs/ledger/2026-11-11-plan48-phase1-run.md)), so it cannot integrate, and a manager that cannot integrate is a worker. The hosting session is the run's [accountable agent](../../skills/astrid-dev-shared/run-contract.md#who-answers-for-a-run) and its manager; it starts one Codex run per wave from [`manager-brief.md`](../../skills/astrid-dev-orchestrate/codex-in-claude-cloud/manager-brief.md), briefed as a lead that dispatches cards to sub-agents by route and never integrates.

- **Waves.** 1: RL-0, RL-1a, RL-2b. 2: RL-1b, RL-1c, RL-2a, then RL-2c. 3 (after RS1): RL-1d, RL-1e, RL-1g, RL-2d. 4: RL-1f, RL-2e. The T rows follow their inputs. Phase 2 is one small wave after RL-G.
- **Workspace.** Partial clones `astrid-dev/` and `astrid-app/` at `int/31-releases-from-astrid-dev`, `astrid-agent/` at `main` for reading only, and `run/`. One `git worktree add` path per card (`wt/<task id>`) with its own `<worktree>.env`; only the lead touches the base clones.
- **Hand-over of each card.** The sub-agent leaves its change uncommitted in its worktree, runs the card's focused proof, and the lead writes `READY: <task id> <worktree path>` to the mailbox with the proof's command and output. The hosting session checks that the changed files are inside the card's scope, re-runs the proof once, commits (one commit per card, commits added and never rewritten), pushes a fresh branch `task/31-<task id>`, opens the pull request into `int/31-releases-from-astrid-dev` and merges it.
- **First step of the run:** one sub-agent tries `git commit` in a scratch worktree. If it works in this layout, sub-agents commit locally and the hosting session only pushes and opens pull requests; record which in `run.yaml`.
- **`READY:` tasks the hosting session runs itself,** as soon as their inputs land, without waiting to be asked: RL-1t, RL-2t, RL-3t, RS1, R, RL-G, the hosted proofs of RL-1e, RL-2b and RL-2d, and saving the served manifest for RL-1g.
- **App worker environment.** RL-0 lands first in the App. Every App card then starts with `bash scripts/worker-env/app-setup.sh` from its worktree root; Node 20.19.x must be on `PATH` in the hosting container before the run starts (the App's `.nvmrc` is 20.19.4). The App has no committed `.claude/settings.json`, which matters only if a Claude worker session is ever attached to it; a Codex sub-agent needs none.
- **Batches.** A push to an App `int/**` branch starts the App's full workflows, so App task merges land several per push. astrid-dev merges are not batched. Progress on this file lands as its own pull request, which now waits for the two required checks before it merges.
- **Never,** in any card: push to `main`; change `public/install*` on a branch that will merge to App `main` other than through `install-copy.mjs write`; edit an existing line of `golden.txt` or an existing test to get green; put a model identifier in a commit, pull request or file.
- **Every sub-agent brief names** the card, its scope, its base SHA, its worktree, the exact proof command, and "leave the change uncommitted; do not ask the owner anything; write questions to the lead".

## Task details

### What is already on `main`

Part of the 8 Nov card RL-1a landed before this re-plan, at astrid-dev `12a54b6`:

- `releases/TEMPLATE.md`, including the optional `## Included pull requests` section (added 11 Nov);
- `releases/12.md`, a living Draft brief, with its row in `strategy.md`;
- the draft rules, as the registered checks `release-documents` and `strategy-consistency` (`scripts/check_docs.py:release_errors`, `strategy_errors`): number, title, state word, the five sections, a one-line highlight, linked and unduplicated plans, "Not pinned." in a Draft, and the strategy row agreeing with the document;
- one final rule: a Final record needs a JSON block holding `version`, `kind`, `required`, `app`, `agent`, `runtime`, `runtime_schema_digest` and `tools`;
- eleven golden fixtures for those rules, and their cases in `scripts/test_check_docs.py`.

Not built: `scripts/release_record.py`, any other final rule, `render`, the live record, and everything in RL-1c to RL-2e. None of the landed code is edited by this plan: new rules go in the new module and are registered beside the old ones.

### What changed from the 8 Nov cards

| 8 Nov card | Now |
| --- | --- |
| RL-0 | RL-0, unchanged except that its smoke test is a file that needs no network |
| RL-1a records, checks, legacy record | The landed part is reused. The rest is RL-1a (contract, tests first), RL-1b (implementation) and RL-1g (the live record) |
| RL-1b `release-contract` (X) | RL-1e (N): the ancestry rule is unit-tested locally, the Agent install steps are named, and one hosted negative case replaces five |
| RL-1c `publish-release` and gate (S) | RL-1c (S, the refusal list as tests) and RL-1d (N). The publish job and the `release-published` branch are cut ([D2](inputs.md#owner-decisions)) |
| RL-1d Release skill | RL-1f, with the steps written out |
| RL-2a typed schema for every reader (X) | RL-2a (N): one check command. The hand-written readers are left alone ([alternatives](inputs.md#alternatives)) |
| RL-2b bootstrap move | RL-2b, with every test file named |
| RL-2c `release-sync` and the copy guard (X) | RL-2c (X, the guard's rules as tests) and RL-2d (N). The scheduled writer is cut ([D2](inputs.md#owner-decisions)) |
| RL-2d canary compares with `release-published` | RL-2e: the canary checks the deployed copy against its record |
| RL-R, RL-G | RS1, R and RL-G |
| RL-3 | RL-3a (N) and RL-3t (T) |
| — | RL-1t, RL-2t (words), RL-9 (deleting the temporary parts) |

### RL-0 App worker setup

- `app-setup.sh`, from the App checkout root: fails with exit 3 unless `node --version` is `v20.19.*` and `package-lock.json` exists; then `npm ci --legacy-peer-deps`. No other repository, no network beyond the npm registry.
- `smoke.sh app <file>`: runs the setup, then `node --test <file>`; prints `ENV-PASS app <file>` or `ENV-FAIL` with the failing step. The three existing modes are unchanged.
- The App copies are byte copies under `scripts/worker-env/`, as in the Agent.

### RL-1a and RL-1b The record

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

**`check` refuses,** each with its own test in RL-1a: a payload that is not one JSON object; a missing key; a key not in the table; a malformed SHA, digest or version; an unknown `kind`; `legacy` on any record but the lowest Final; a version that is not the previous Final record's version stepped once by `kind`; an empty `required` reason; a gap in the Final records' numbers; a Draft numbered below a Final record. Registered as `release-records` (`always`).

**`release-immutable`** (`pr`, reads the base revision as the existing `pr` checks do): a record that is Final at the base is, at the head, either byte-identical or no longer Final; it is never deleted. Turning a record back to Draft is the one way to correct a mistaken Final, and making it Final again needs a fresh approval, which the gate checks. This check is early warning; the gate, not this check, is what refuses a changed record.

**One diagnostic per failure.** `release-records` skips any record that `check_docs.release_errors` already rejects, so a Final record with no payload still prints only today's line. This is the rule the [Plan 48 run](../../docs/ledger/2026-11-11-plan48-worker-recovery.md) asked to be stated before dispatch.

**Dropped from the 8 Nov list:** "a final record whose pins disagree with its included plans". Nothing in a plan file names a commit, so no check can decide it.

**`render --release N [--payload-file F] [--output F]`** writes the App's manifest: `schema_version` 1, `release` N, `version`, `versions`, `app.sha`, `agent.sha`, `runtime.sha` and `runtime.schema_digest`, `tools`, `vibecomfy`, `lifecycle`, and `required` only when a floor exists. Keys in that order, two-space indent, one trailing newline.

- `versions` maps every release from 1 to N: the legacy record's `legacy_versions`, then each Final record's own `version`.
- `required` is `{release, reason}` of the highest Final record at or below N whose `required` is not null, so a floor stays in force until a later record sets a new one.
- A Draft does not render. `--payload-file` renders a *candidate*: the same function over a payload that is not yet in a record, for release N one above the newest Final. That is what lets a candidate be qualified on the exact bytes that will ship.
- The 8 Nov design also rendered `source`, the astrid-dev commit. It is cut: the render is then a pure function of the records, so a candidate's bytes and the published bytes are the same.

**Standard library only.** `release_record.py` and `release_gate.py` import nothing from this repository except each other; a test reads their imports and fails otherwise. They are the only scripts whose output decides what users install, so they must not depend on a file the owner does not review.

**Golden file.** Two new fixtures only, `final-record-clean` (no lines) and `final-record-bad-pin` (its lines); every other rule is a unit test over strings, because each fixture overlays whole real files and so has to be refreshed when the live brief changes (see RL-1g).

### RL-1c and RL-1d The approval gate

`python3 scripts/release_gate.py --repo banodoco/astrid-dev --release N` answers one question: did a release approver approve the exact change that made record N Final, and has the record stayed as approved? It reads a git checkout and the public REST API (with `GITHUB_TOKEN` if set, for the rate limit) and writes nothing. It exits non-zero unless every line below holds, and on any API error, missing field or shape it does not recognize.

**The refusal list (RL-1c writes one test for each; RL-1d makes them pass):**

1. `main` has no active rule requiring a pull request with code-owner review and stale approvals dismissed (`GET /repos/{repo}/rules/branches/main`).
2. `.github/CODEOWNERS` at the first parent of the finalizing commit has no line for `/scripts/release_gate.py`, or that line names a team or nobody. **The release approvers are the code owners of the gate itself,** read from the commit *before* the change, so a pull request cannot add its own approver.
3. No commit on `main`'s first-parent history turns `releases/N.md` from absent or Draft to Final. The most recent one that does is the *finalizing commit*.
4. `releases/N.md` at the tip differs from the same file at the finalizing commit.
5. The finalizing commit is not the merge commit of exactly one merged pull request into `main` (`GET /repos/{repo}/commits/{sha}/pulls`); a direct push fails here, and so does a rebase merge, so the finalizing pull request is merged by merge commit or squash.
6. That pull request has no review in state `APPROVED` from a release approver whose `commit_id` is the pull request's final head, or that approver's latest review is not the approval (changes requested later, or dismissed).
7. The approver is the pull request's author.
8. A lower-numbered Final record fails any line above (a release cannot be approved on top of an unapproved one), except records at or below the legacy record.

`--commit <sha>` runs lines 1, 2 and 5 to 7 against a named commit; it exists for the live negative proof.

**`CODEOWNERS` (RL-1d) covers exactly four paths:** `/.github/CODEOWNERS`, `/.github/workflows/release.yml`, `/scripts/release_record.py`, `/scripts/release_gate.py`. It does **not** cover `releases/`: Release 12's Draft brief was changed by 24 commits in two days, by managers, and a Draft must stay that free. The approval that matters is checked by the gate on the one pull request that makes a record Final. With only those four paths owned, no other plan's progress pull request waits for the owner once code-owner review is on.

**Why S and then N.** The list is the security boundary and cannot run end to end until RL-G, so writing it is S and it is reviewed at RS1 before any code exists. Once the tests exist, making them pass is ordinary work over recorded responses.

### RL-1e `release-contract`

A new workflow file, so the owned path is one file and `docs.yml` (which Plan 48 also edits) stays free. One job, `release-contract`, on every pull request and on push to `main`; it must report on every pull request because it will be a required check, so the job always runs and its steps skip unless the change touches `releases/*.md`, `scripts/release_record.py`, `scripts/release_gate.py` or the workflow itself.

For the newest Final record N, in this order:

1. `python3 scripts/release_record.py check`, then `render --release N`.
2. **Ancestry, before any other repository's code runs:** partial clones of the App, Agent and Runtime; `python3 scripts/release_record.py ancestry` requires each of `app`, `agent`, `runtime` to be an ancestor of that repository's `origin/main`. Reachable is not enough: GitHub serves fork and pull-request commits through the parent repository.
3. **The App's checker:** check out the App at the branch named like the pull request's base if it exists there, else `main`; `node scripts/installer/manifest-check.mjs <rendered> --bootstrap-dir <dir>` with the bootstraps taken from the record's `app` (`scripts/installer/bootstrap/`, or `public/` when that commit predates RL-2b).
4. **The Agent's validator,** from the record's `agent` and from the previous Final record's `agent`: Python 3.11, `python -m pip install -e '.[dev]'`, `python scripts/ci_install_runtime.py` (the Agent's own CI steps), then `astrid.installer.tools.validate_manifest` on the rendered manifest.

Read by code at Agent `a105de3`, `709492fa` and `6e9c4f9c` (Releases 11, 9 and 10): `validate_manifest` has no closed set of top-level keys, so the added `version`, `versions` and `app` do not break an installed Agent's update.

### RL-1f Release skill

The "Publishing an installer release" list becomes these steps; steps 0 and 1 of today's list stay as they are.

1. **Candidate.** Freeze the Agent, Runtime and App candidates. Get the derived pins with `node scripts/installer/pin.mjs --print <agent sha>` and write the payload file. Write the candidate copy on the App candidate branch with `install-copy.mjs write --candidate`; qualify on it. Record the manifest's SHA-256.
2. **Owner's go, in this session,** on the exact SHAs.
3. **Merge code:** Agent, then Runtime, then the App's code candidate *without* the candidate copy commit. The hosted App deploys; that is not a release.
4. **Decide:** open the pull request that turns `releases/<N>.md` Final with that payload and sets the strategy row to `final`. `release-contract` must pass. The owner approves it on GitHub from the approving account; that approval is the durable go. Merge. `release_gate.py --release N` passes: the release is *decided*.
5. **Publish:** in an App checkout of `main`, `install-copy.mjs write`, open the pull request, `install-copy-guard` passes, merge: *published*. The manifest's SHA-256 equals the one qualified in step 1, or stop.
6. **Live:** wait for the deploy and the canary, then confirm the served manifest.
7. Bring integration branches up to `main`.
8. Close the project.

"One publisher at a time" keeps its rule and loses its mechanism: the guard refuses a copy that is not the newest Final record, so two projects cannot both publish a number. "Take stock of open pull requests" is not touched.

### RL-1g The live record

- **Which release:** the `release` in `https://astrid.haus/install-manifest.json` when the run starts, saved to the run folder by the hosting session. Release 12 is expected; if it is, `releases/12.md` already exists as a Draft and this task flips it. If the live release has no brief, write one from its publish receipts only, with one honest sentence per section.
- **Payload:** copied from the served manifest; `app` is the deployed App commit the canary last passed for; `kind` is `legacy`; `version` and `legacy_versions` follow [D5](inputs.md#owner-decisions).
- **Why its own branch:** the gate reads the approvers from `CODEOWNERS` as it stood before the finalizing pull request, so the record cannot become Final in the same pull request that first adds `CODEOWNERS`.
- **Fixtures:** every golden fixture overlays whole copies of `releases/12.md` or `strategy.md`. When the real brief turns Final they must be refreshed so each still differs from the real tree by its one defect; `golden.txt` must come out byte-identical. If a line would change, stop and ask.
- **`plans/releases.md`** gets one closing line: later releases are the files in `releases/`. Its two rows stay; astrid-dev pull request #82, still open, closes unmerged.

### RL-2a Manifest check

`node scripts/installer/manifest-check.mjs <manifest> --bootstrap-dir <dir> [--offline]`: the added keys' shape (all three optional; if `versions` is present it names the manifest's own release); every tool asset has one HTTPS URL and one real SHA-256 per download (today's first case in `manifest.test.mjs`, as a function); uv and Python pins agree with `<dir>/install` and `<dir>/install.ps1`; and, unless `--offline`, `checkManifest`. No dependency beyond Node: astrid-dev's job and the App's guard run it without `npm ci`.

The 8 Nov card also moved `updateStatus.ts` and `localUpdateStatus.ts` onto a shared Zod schema. That is cut: both readers already ignore keys they do not know (read at App `6545f13`), so nothing in phase 1 needs them changed.

### RL-2b Bootstrap move

After this, a bootstrap is edited under `scripts/installer/bootstrap/` and reaches users only when a record names an App commit that contains it. `public/install*` is then only ever a generated copy. `config/vite/installerAssets.ts`, the `Dockerfile`, `scripts/local-update-checkout.mjs` and the Agent's journeys keep reading `public/`, so none of them change.

### RL-2c and RL-2d The copy guard

`node scripts/installer/install-copy.mjs verify --base <sha> [--head <sha>] --astrid-dev <dir>` decides whether a change may touch the four generated files: `public/install`, `public/install.sh`, `public/install.ps1`, `public/install-manifest.json`. It runs astrid-dev's `release_record.py render` and `release_gate.py` from `<dir>` as child processes; RL-2c's tests stub both.

| Rule | Case |
| --- | --- |
| G1 | The four files are unchanged between base and head: pass, without reading astrid-dev |
| G2 | They equal the render of the newest Final record N and the bootstraps at that record's `app`, and the gate passes for N: pass |
| G3 | The manifest differs from the render by any byte: refuse |
| G4 | A bootstrap differs from the record's `app` by any byte: refuse |
| G5 | The head's `release` is below the base's: refuse |
| G6 | The head's `release` names a Final record that is not the newest: refuse |
| G7 | Record N is missing or a Draft: refuse |
| G8 | The gate exits non-zero: refuse, and print its lines |
| G9 | The record's `app` is not an ancestor of App `main`: refuse |
| G10 | `manifest-check` refuses the result: refuse |
| G11 | Any other path under `public/` whose name starts with `install` is added or changed: refuse |
| G12 | The astrid-dev directory, `python3` or either command is missing or errors: refuse |

- **`write --astrid-dev <dir>`** computes the same bytes and writes them. **`write --candidate <payload> --release N`** writes a candidate copy for qualification; it never passes the guard, because no Final record matches it.
- **The job** `install-copy-guard` in `test.yml` runs on pull requests to `main` and on push to `main`, with `contents: read`; it clones astrid-dev `main` and runs `verify`. On push it is the alarm for a write that went around the rules.
- **`pin.mjs`** keeps `checkManifest` and `--check`, and gains `--print <agent sha>`, which prints `runtime`, `runtime_schema_digest`, `vibecomfy` and `lifecycle` for a payload. It stops writing the manifest. Plan 29 already removed `release-check.mjs` and `update-manifest.mjs` (absent at App `6545f13`).
- **Temporary, deleted in RL-9:** a record whose `app` predates RL-2b takes its bootstraps from `public/` at that commit. Only the live record needs it.
- **App pull request #208** (the version helper) closes unmerged; nothing from it is used. Its state could not be read from the planning session.

### RL-G Go live

Each step is the Release skill's, with the owner's go in the publishing session; her settings changes fall between steps.

1. **App `int/31` → `main`.** The four generated files are unchanged, so nothing users install changes. **O-2.** Then one throwaway pull request that edits `public/install.sh` shows `install-copy-guard` failing as a required check; close it.
2. **astrid-dev `int/31` → `main`,** by merge commit: the scripts, `CODEOWNERS`, `release.yml` and the skill. No record is Final yet.
3. **O-1.**
4. **Negative proof, live:** `release_gate.py --commit <step 2's merge commit>` refuses, naming the missing approval and nothing about the ruleset.
5. **The live record:** open `rel/31-live-record` against `main`. `release-contract` passes. The owner approves from the approving account. Merge. `release_gate.py --release <live>` passes: the gate's first positive run, on a release that is already live.
6. **The first copy:** `install-copy.mjs write` in the App, pull request, guard green, merge. The diff touches only `version`, `versions` and `app` in the manifest. Deploy; the canary passes, including RL-2e's step.

The next release is then published by the eight steps in RL-1f; that is the plan's completion, and it is the first time a tuple changes through this path.

### RL-3a and RL-3t Versions on screen

- **Hosted:** `checkHostedUpdate` reads `version` and `versions` from the manifest it already loads; `UpdateStatus` gains `version` (the installed release's, from `versions`) and `servedVersion`, both optional.
- **Local launcher:** `localUpdateStatus.ts` already fetches the served manifest for the required floor; it adds the same two fields to its reply, and `checkLocalUpdate` reads them.
- **No name without a version.** If the manifest gives no version for a release, the line names none ("Astrid is up to date", "Update available"); it never falls back to a release number. RL-3t decides the exact words.
- **Kind** is not shown.
- **Order against Plan 30:** its LA-2 changes `localUpdateStatus.ts` and `updateStatus.ts`. Whichever starts second starts from the other's result.

### If the owner decides otherwise

- **D1 b (no separate approving account):** RL-1c, RL-1d and the guard's rule G8 have nothing to verify. The plan then delivers records, the contract job and a byte-exact copy, and says plainly that it does not control who publishes. RS1 and one review round go.
- **D2 b (the 8 Nov transport: a `release-published` branch and a scheduled job that pushes to App `main`):** add a `publish-release` job and its superseded-run guard; a ruleset on `release-published`; a write credential for App `main` kept as an environment secret that only `main`'s workflows can use, with a ruleset bypass; the `release-sync` workflow and its off switch. RL-2c and RL-2d are re-planned, the writer becomes an S task, and phase 1 grows by two to three days. The guard's rules G1 to G12 are still needed, because the branch can be written by anyone with push access.
- **D3 b (no code-owner review on App `main`):** nothing in the cards changes; the [limit](plan.md#completion) is stated in the plan.

**Overlap with other projects:**

- **[Plan 48](../48-one-record-model/plan.md) Phase 1 is on `main`,** and these cards are written against it: checks are registered in `scripts/checks.py`; `golden.txt` gains lines and never loses or changes one; the `documentation` job is not renamed or edited; `docs/checks.md` is regenerated, not hand-edited.
- **Plan 48 Phase 2** moves status and owner into each `plan.md` and makes `plans/index.md` a generated view; its PM-10 deletes `check_docs.py`. This plan imports one function from it (`release_errors`, for the one-diagnostic rule). Whichever starts second re-reads the other's result; if PM-10 has landed, RL-1b imports that function from wherever it moved.
- **Plan 29** changes the same App files (the guard RL-2d deletes, the update screens RL-3a edits), so this plan starts after Plan 29 is on App `main` and Release 12 is published.
- **Plan 30** (queued): LA-2 and UR-17 touch the update status readers and cards; see RL-3a.
- **The Release skill** is edited by RL-1f and by Plan 29's post-publish pull request (re-syncing `runtime.lock.json`). Start RL-1f from whichever has landed.
