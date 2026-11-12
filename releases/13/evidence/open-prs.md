# Release 13: open pull requests, triage

Taken Thu 12 Nov 2026, about 22:40 to 23:30 UTC. This was read-only: nothing was commented on, reviewed, labelled, merged or pushed.

**Candidate refs:**
- Agent `r13/compose` `520803167`, which is 665 files ahead of `main`.
- VibeComfy `r13/cells-vc` `b3f20f33`, pinned in `astrid/packs/runpod/pins.json`.
- Runtime stays at `42ae24aff` (G5).
- The lifecycle pin is `f2948817`.

**Count:** 57 open PRs across the 8 repositories. Agent 21, Runtime 5, App 11, VibeComfy 3, Pinokio 3, runpod-lifecycle 2, poms_packs 1, astrid-dev 11.

**How each PR was checked:**
- **Metadata:** REST API, plus check runs and reviews on the head SHA. **No open PR in any of the 8 repositories has a review.**
- **Containment:** `git merge-base --is-ancestor` and `git cherry` against `main` and the candidate.
- **Conflicts:** `git merge-tree --write-tree` against `r13/compose` (or `r13/cells-vc`).
- **Overlap:** the PR's files intersected with `git diff --name-only origin/main...origin/r13/compose`.

The diffs of the PRs marked IN were read in full. No tests were run locally: there was 2.8 GB of free disk, no venv in the worktree, and the brief limits managers to focused proofs.

**Not done as asked:** no Agent tool was available in this session, so there were no haiku helpers. I collected every fact myself by script.

**Legend:**
- **Lane:** E engine, M machines, C cells, T test lane, RM release manager.
- **Conflict:** the risk against R13. *none* means it merges cleanly and touches no R13 file.

## astrid-agent (21)

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#293](https://github.com/banodoco/astrid-agent/pull/293) | Fix: return whole invoke results and skill descriptions over MCP | matlowai (outside) | 5d | **IN** | **MCP fix**, +27/−2. Drops the `[:20000]` cut on `invoke` text (it produced invalid JSON) and the `[:1000]` cut on skill descriptions. Has 2 regression tests. Merges cleanly onto `r13/compose`, which touched only line 267 of `mcp_server.py`. No R13 skill description is over 1000 characters, so that half changes nothing today. CI never ran because it comes from a fork | E (owns the MCP generation tools), about 30 min | low: same file, different hunk |
| [#346](https://github.com/banodoco/astrid-agent/pull/346) | Preserve existing media alternatives when importing timelines | peteromallet | 0d (22:22 today) | **AFTER** (owner may pull in) | A real import-refusal fix, +126/−3, tested and reviewed by Astra per its body. But it is timeline persistence, not generation, and timeline persistence is a protected invariant. Red checks are only the Windows task-host journey, which is already red on `main` (Plan 39 AT4) | T, about 1 h if pulled in | none: merges cleanly, 0 R13 files |
| [#341](https://github.com/banodoco/astrid-agent/pull/341) | Plan 20: guide setup through Connected (draft) | AstridPseudon | 2d | **IN (already composed)** | Its head is an ancestor of `r13/compose`, so it is already in the candidate. Nothing to land; it closes when R13 reaches `main` | RM, 0 | none |
| [#329](https://github.com/banodoco/astrid-agent/pull/329) | Pin recovery-only --update exits to 3 (UR-15a) | AstridPseudon | 3d | **NOT** (already landed) | Its head is already in `main` (R11/R12). Stale open PR; close | — | — |
| [#327](https://github.com/banodoco/astrid-agent/pull/327) | Settle a completed app update on its release | AstridPseudon | 3d | **NOT** (already landed) | Its head is in `main`; close | — | — |
| [#326](https://github.com/banodoco/astrid-agent/pull/326) | Report windows-upgrade-unsupported (UR-15j) | AstridPseudon | 3d | **NOT** (already landed) | Its head is in `main`; close | — | — |
| [#325](https://github.com/banodoco/astrid-agent/pull/325) | UR-15j: run receipt says only what is true | AstridPseudon | 3d | **NOT** (already landed) | Its head is in `main`; close | — | — |
| [#324](https://github.com/banodoco/astrid-agent/pull/324) | Settle the local update through the installer's receipt | AstridPseudon | 3d | **NOT** (already landed) | Its head is in `main`; close | — | — |
| [#321](https://github.com/banodoco/astrid-agent/pull/321) | End every non-zero installer outcome with Next and Details | AstridPseudon | 3d | **NOT** (already landed) | Its head is in `main`; close | — | — |
| [#186](https://github.com/banodoco/astrid-agent/pull/186) | Land lane/M-QUAL/user-quit-delete-1503 | AstridPseudon | 8d | **NOT** (already landed) | Its only commit is patch-equivalent to one in `r13/compose`; base `int/r1` is retired; close | — | — |
| [#264](https://github.com/banodoco/astrid-agent/pull/264) | Land lane/M-QUAL/fabae98-reassess-0553 | AstridPseudon | 7d | **NOT** | Automated lane-land PR into the retired `int/r1`. Adds CI journey evidence tooling (`ci_journey.py`). A near-duplicate of #255. If the tooling is wanted, it goes to Plan 39 | T | none |
| [#256](https://github.com/banodoco/astrid-agent/pull/256) | Land lane/M-QUAL/fb55feb-current-0434 | AstridPseudon | 7d | **NOT** | Same pattern: Windows SDK journey evidence, into `int/r1` | T | none |
| [#255](https://github.com/banodoco/astrid-agent/pull/255) | Land lane/M-QUAL/fabae98-current-0434 | AstridPseudon | 7d | **NOT** | Duplicate of #264 with a different tip, into `int/r1` | T | none |
| [#292](https://github.com/banodoco/astrid-agent/pull/292) | Consolidate installer, generation and Packs candidates (draft) | matlowai (outside) | 5d | **NOT** | 868 files, +55k/−93k, into `pre-main`, and dirty. A contributor's consolidation snapshot that R12 and R13 have overtaken | — | high |
| [#109](https://github.com/banodoco/astrid-agent/pull/109) | OpenShell sandbox, MCP server and sandbox process control | matlowai (outside) | 18d | **NOT** as it stands (superseded) | Maintainers said on the PR that they would split it and close it. 35 of its 39 commits are already patch-equivalent in R13. The 4 left are sandbox process control and installer JSON parsing, not MCP. Merging conflicts in `generic_host.py`, `gpu_environment.py`, `mcp_server.py` and 11 more files. Close it; route the 4 commits to a sandbox follow-up | — | high (R13 hot files) |
| [#115](https://github.com/banodoco/astrid-agent/pull/115) | Recover interrupted Windows installs without old-host rollback (draft) | peteromallet | 16d | **NOT** as it stands | Draft, CI red (8 failures), touches 5 R13 files and pins an old Runtime. It is installer recovery, and that scope is now being re-planned in astrid-dev #625 (Plan 09) | — | medium |
| [#312](https://github.com/banodoco/astrid-agent/pull/312) | Allow worker sessions to run setup and test commands (draft) | AstridPseudon | 4d | **AFTER** | `.claude/settings.json` allowlist. It does not ship. It widens worker permissions, and its body says to merge after Plan 33. Land it after publish | RM | none |
| [#289](https://github.com/banodoco/astrid-agent/pull/289) | docs: PR submission template | peteromallet | 5d | **AFTER** | Only `.github/pull_request_template.md`. Harmless, but it goes onto `main` during the gate; land it after publish | RM, 2 min | none |
| [#112](https://github.com/banodoco/astrid-agent/pull/112) | feat(chat): Octop local agent integration | sirjoonas (outside) | 17d | **AFTER** | New chat-agent feature. Conflicts with R13 in `chat/service.mjs` and `skills/cli.py`. Needs a rebase. Pairs with App #127 | — | medium |
| [#110](https://github.com/banodoco/astrid-agent/pull/110) | Add DeepSeek Harness as a local chat agent | stierma1 (outside) | 18d | **AFTER** | New feature, plus an installer launchd fix. Conflicts in `installer/backend.py`, `installer/service.py` and `chat/service.mjs`. Pairs with App #126 | — | medium |
| [#111](https://github.com/banodoco/astrid-agent/pull/111) | Document connecting DeepSeek Harness to chat | stierma1 (outside) | 17d | **AFTER** | Docs only; merges cleanly. It documents #110, so it lands with #110 | — | none |

## astrid-runtime (5)

R13 keeps Runtime at `42ae24aff` (G5), so any Runtime change would reopen the pin.

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#47](https://github.com/banodoco/astrid-runtime/pull/47) | Fix landing regressions in Windows, sandbox, darwin and macOS CI | AstridPseudon | 3d | **NOT** (already landed) | Its head is in Runtime `main`; close | — | — |
| [#33](https://github.com/banodoco/astrid-runtime/pull/33) | Consolidate Runtime shutdown and pack custody/admission (draft) | matlowai (outside) | 5d | **NOT** (already landed) | Its head is in Runtime `main`; close | — | — |
| [#11](https://github.com/banodoco/astrid-runtime/pull/11) | Retry drained service cleanup receipts (draft) | peteromallet | 16d | **NOT** (already landed) | Both commits are patch-equivalent in `main`; close | — | — |
| [#38](https://github.com/banodoco/astrid-runtime/pull/38) | Allow worker sessions to run setup and test commands (draft) | AstridPseudon | 4d | **AFTER** | Same allowlist as Agent #312 | RM | none |
| [#32](https://github.com/banodoco/astrid-runtime/pull/32) | docs: PR submission template | peteromallet | 5d | **AFTER** | Same as Agent #289. Doc-only; its red checks are unrelated to the change | RM | none |

## astrid-app (11)

R13 touches App only to re-pin it on Saturday.

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#229](https://github.com/banodoco/astrid-app/pull/229) | Merge origin/main into int/29 (R11 candidate) | AstridPseudon | 3d | **NOT** (already landed) | Its head is in App `main`; close | — | — |
| [#228](https://github.com/banodoco/astrid-app/pull/228) | R11 cards 7, 8: install.ps1 receipt; dev:local line | AstridPseudon | 3d | **NOT** (already landed) | Its head is in App `main`; close | — | — |
| [#227](https://github.com/banodoco/astrid-app/pull/227) | UR-15j: small UX fixes (App) | AstridPseudon | 3d | **NOT** (already landed) | Its head is in App `main`; close | — | — |
| [#248](https://github.com/banodoco/astrid-app/pull/248) | Fit the mobile homepage to one screen (draft) | peteromallet | 1d | **AFTER** | Marketing or homepage UI work, a draft, and dirty against `main`. Not generation | — | n/a |
| [#220](https://github.com/banodoco/astrid-app/pull/220) | Allow worker sessions to run setup and test commands (draft) | AstridPseudon | 4d | **AFTER** | Same allowlist as Agent #312 | RM | none |
| [#194](https://github.com/banodoco/astrid-app/pull/194) | Compose installer candidate with pack live effects (draft) | matlowai (outside) | 5d | **NOT** | Into `pre-main`, dirty, +4.5k/−1.5k. A consolidation snapshot that has been overtaken | — | high |
| [#158](https://github.com/banodoco/astrid-app/pull/158) | Fix Runtime installer update response handling | peteromallet | 10d | **NOT** | Into the retired `int/r1`, on an App history `main` no longer shares. If any of it is still needed, re-raise it against `main` after R13 | — | n/a |
| [#154](https://github.com/banodoco/astrid-app/pull/154) | I-AP-18-R2: migrate direct-journey writes to /commit (test only) | AstridPseudon | 10d | **NOT** | Into `int/r1` on the old history; stale | — | n/a |
| [#130](https://github.com/banodoco/astrid-app/pull/130) | Asset provenance view (Do not Merge, mockup) | stierma1 (outside) | 15d | **NOT** | The author marked it a mockup, not for merge. Design input for a later plan | — | n/a |
| [#127](https://github.com/banodoco/astrid-app/pull/127) | Octop local agent in setup card | sirjoonas (outside) | 17d | **AFTER** | The App half of Agent #112; it lands with it | — | n/a |
| [#126](https://github.com/banodoco/astrid-app/pull/126) | Offer DeepSeek Harness in agent setup card | stierma1 (outside) | 18d | **AFTER** | The App half of Agent #110; it lands with it | — | n/a |

## VibeComfy (3)

The candidate is `r13/cells-vc` `b3f20f33`. Red CI matches VibeComfy `main`, which is red too (Plan 39 evidence `release-12-vibecomfy-ci.md`).

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#166](https://github.com/banodoco/VibeComfy/pull/166) | Reconcile model picker paths with declared custody | AstridPseudon | 2d | **IN (already composed)** | Its head is an ancestor of `r13/cells-vc`, which is pinned. Nothing to land; it closes when cells-vc reaches VibeComfy `main` | C, 0 | none |
| [#165](https://github.com/banodoco/VibeComfy/pull/165) | Remove Foley template region notices | AstridPseudon | 2d | **IN (already composed)** | Its head is an ancestor of `r13/cells-vc`. Same as #166 | C, 0 | none |
| [#164](https://github.com/banodoco/VibeComfy/pull/164) | Allow worker sessions to run setup and test commands (draft) | AstridPseudon | 4d | **AFTER** | Same allowlist as Agent #312. It is not in cells-vc and must not join the pin | RM | low (`Makefile`) |

## astrid-pinokio (3)

R13 does not change Pinokio.

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#1](https://github.com/banodoco/astrid-pinokio/pull/1) | fix(windows): sanitize PSMODULEPATH | theCosmicCrafter (outside) | 15d | **AFTER** | A plausible fix (+8, `environment.js`) for PowerShell 7 module collisions. No test, and CI never ran on the fork. Needs a unit case in `tests/environment.test.mjs` and a native Windows run. Not generation | — | none |
| [#2](https://github.com/banodoco/astrid-pinokio/pull/2) | fix(windows): sanitize PSMODULEPATH… | theCosmicCrafter (outside) | 15d | **NOT** | Exact duplicate of #1 (same SHA `f09bb1b`, opened from the fork's `main`); close in favour of #1 | — | — |
| [#3](https://github.com/banodoco/astrid-pinokio/pull/3) | Integrate Astrid updater changes | peteromallet | 14d | **NOT** as it stands | 14 commits, +2.5k. Smoke is red on macOS and Ubuntu. Its own plan said to reconcile with latest `main` after a hotfix, and that never happened. Probably overtaken by the R11/R12 updater work; needs the author to re-check | — | n/a |

## runpod-lifecycle (2)

The R13 pin is `f2948817`. Any bump reopens G4 (pins) and the full GPU gate.

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#2](https://github.com/banodoco/runpod-lifecycle/pull/2) | Make ship_and_run primitives safe for concurrent pod fan-out | protereus (outside) | 113d | **AFTER**, not as is | Merges cleanly; 9 tests. **Money and custody note:** `ship_and_run_detached` now catches every exception into `result.error` and returns `returncode=-1` instead of raising. The Agent's two callers (`packs/runpod/shared/common.py:1292` and `:1661`) rely on the raise, turning it into an `AstridError` with a recovery command. With this PR the failure cause is silently dropped, which works against R13's failure-receipt goal. Teardown is unchanged. To land it later, the Agent callers must call `raise_if_error()` in the same pin bump | M (after R13) | none in the repo; behavioural for the Agent |
| [#4](https://github.com/banodoco/runpod-lifecycle/pull/4) | Allow worker sessions to run setup and test commands (draft) | AstridPseudon | 4d | **AFTER** | Same allowlist as Agent #312 | RM | none |

## poms_packs (1)

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#1](https://github.com/banodoco/poms_packs/pull/1) | Stage the 19-pack migration and external installation tests (draft) | matlowai (outside) | 5d | **NOT** | Draft, 488 files, +101k, into the lane branch `lane/M-GPU/packs-M3-10`. Packs are not pinned by R13 | — | n/a |

## astrid-dev (11)

None of these is part of the shipped tuple, so none reopens qualification.

| PR | Title | Author | Age | Verdict | Reason | Lane | Conflict |
|---|---|---|---|---|---|---|---|
| [#602](https://github.com/banodoco/astrid-dev/pull/602) | Release skill: one home for each release record | AstridPseudon | 0d | **IN** (records) | +43. Codifies the `run.md`, `decisions.md` and `tests.md` layout R13 already uses, plus the run-board template. Merges cleanly; checks green | RM, 5 min | none |
| [#604](https://github.com/banodoco/astrid-dev/pull/604) | Plan 39: record that the mypy total gate is dropped | AstridPseudon | 0d | **IN** (records) | One line recording the owner's 12 Nov decision. Merges cleanly; checks green | RM, 2 min | none |
| [#625](https://github.com/banodoco/astrid-dev/pull/625) | Plan legacy-to-standalone installation conversion (draft) | peteromallet | 0d | **AFTER** | A paused, proposed Plan 09 extension. Not R13 | — | none |
| [#439](https://github.com/banodoco/astrid-dev/pull/439) | Design retained owner-selected observer contract (draft) | AstridPseudon | 1d | **NOT** as it stands | Built on an astrid-dev history `main` no longer shares (no merge base). Re-raise on `main` if still wanted | — | n/a |
| [#276](https://github.com/banodoco/astrid-dev/pull/276) | Plan 32 completion evidence (draft) | AstridPseudon | 2d | **NOT** as it stands | Orphaned history; its evidence is on pre-R13 heads | — | n/a |
| [#260](https://github.com/banodoco/astrid-dev/pull/260) | Record Plan 34 first GPU validation (draft) | AstridPseudon | 2d | **NOT** as it stands | Orphaned history. A historical 10 Nov run, not frozen-tuple evidence. Port the record only if Plan 34 wants the history (T, 15 min) | T | n/a |
| [#178](https://github.com/banodoco/astrid-dev/pull/178) | Plan 29: record R11 and the R12 candidate | AstridPseudon | 3d | **NOT** as it stands | Orphaned history, and `main` has since diverged on the same files | — | n/a |
| [#163](https://github.com/banodoco/astrid-dev/pull/163) | Plan 29 UR-15c: same record shapes | AstridPseudon | 3d | **NOT** as it stands | Orphaned history | — | n/a |
| [#122](https://github.com/banodoco/astrid-dev/pull/122) | Record the Windows discovery.json race (UR-13) | AstridPseudon | 4d | **NOT** as it stands | Orphaned history | — | n/a |
| [#82](https://github.com/banodoco/astrid-dev/pull/82) | Add the release log and its check (UR-8c) | AstridPseudon | 4d | **NOT** as it stands | Orphaned history | — | n/a |
| [#39](https://github.com/banodoco/astrid-dev/pull/39) | plans/02: fix P2 setup and P3 ordering text | AstridPseudon | 5d | **NOT** as it stands | Orphaned history | — | n/a |

## The IN set, in landing order

1. **Already composed, nothing to land:**
   - VibeComfy #166 and #165, inside the pinned `r13/cells-vc` `b3f20f33`.
   - Agent #341 (Plan 20), inside `r13/compose`.
   - **Reopens:** nothing. List them under `## Included pull requests` in `releases/13.md`, and close them once the R13 branches reach each `main` after publish.
2. **Agent #293 (MCP whole results):** cherry-pick the single commit `6aad6a46` onto `r13/compose` before the Fri 18:00 cut.
   - **Lane:** engine, about 30 min.
   - **Proof:** `tests/test_mcp_server.py` and `tests/test_mcp_generation_parity.py` on the merged head. The fork's CI never ran, so this is its first CI.
   - **Reopens:** only the Agent CI comparison at the next freeze, which is already scheduled. No pins, no GPU cell, no catalog change (no description is over 1000 characters).
   - **Money and custody:** none. It changes only how a reply is formatted; `structuredContent` was already whole, so no new data leaves the process.
   - **Review:** a two-line change, read here in full. The manager's diff read is enough; no Astra round is needed.
3. **astrid-dev #602, then #604:** process records, mergeable at any time, release manager, about 5 min.
   - **Reopens:** nothing in the tuple.

## Needs the owner

- **Agent #346 (Peter's timeline-import fix):** recommend AFTER.
  - **Why:** it is sound and small, but it is not generation. It changes a protected invariant (timeline persistence) a day before the cut.
  - **If she wants it in:** the test lane lands it before Sat 06:00. App Tests and Direct Journey already run on the frozen tuple, so this adds risk, not extra runs.
- **runpod-lifecycle #2:** confirm AFTER. It changes failure semantics under the Agent's RunPod callers, and any lifecycle bump reopens pins and the GPU gate.
- **The five worker-permission PRs (Agent #312, Runtime #38, App #220, VibeComfy #164, lifecycle #4):** permission changes, approved by the owner on 8 Nov but held. Land them after publish, and keep them out of the cells-vc pin.
- **Housekeeping:** closing stale PRs is a maintainer's job; I closed nothing.
  - Already landed: Agent #321, #324, #325, #326, #327, #329 and #186; Runtime #11, #33 and #47; App #227, #228 and #229.
  - Superseded: Agent #109, App #194, Agent #292 and Pinokio #2.
  - The skill says each deferred outside contributor should be told on the PR which release will consider their work: matlowai, sirjoonas, stierma1, theCosmicCrafter and protereus.
