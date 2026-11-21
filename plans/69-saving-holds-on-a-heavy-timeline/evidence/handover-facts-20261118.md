# Handover facts, 18 Nov 2026 (read-only gathering)

Gathered by a read-only agent on 18 Nov 2026 (about 15:56 CET). Nothing was started, stopped, changed or tested.
Labels: **verified** = seen in a file or command output by this agent; **reported** = said by an earlier agent (transcript), not re-checked.
The `gh` CLI is not on this shell's PATH, so PR states below are reported or inferred from local git history, not read from GitHub.

---

## 1. Agent jobs (from transcripts)

Transcripts: `~/.claude/projects/-Users-<user>/89e96a59-5dfa-43fb-8013-1fe9d0216757/subagents/agent-<id>.jsonl`
(the `tasks/` folder under /private/tmp only holds three 0-135 byte stubs written at 15:56; the real records are the subagent transcripts). **verified**

| Job (meta description) | Agent id | Model | Last write | Status at crash |
|---|---|---|---|---|
| R14 sweep: every edit kind must save | a24089746a5039372 | sonnet | 14:54 | Crashed mid-run (disk full). No final report. |
| Fix: media catalog digest conflict on repeated drags | a9e1355a0384ea80f | sonnet | 15:44 | Stopped by ENOSPC. No final report, no PR. |
| R14 speed trim + revert #62 retention | abc0598004064b547 | sonnet | 15:23 | Waiting on background golden run b5nf5l1gp. No report. |
| Profile a commit on the fixed code | a4c57d6358986ba29 | sonnet | 14:10 | Finished. Report written. |
| Find profile harness (child of the profiler) | ab30ed08c86cbf820 | haiku | 10:13 | Finished. |
| Merge runtime #62 and app #300 | aba88026016a53baf | haiku | 10:47 | Finished. Both merged. |
| Merge astrid-dev #880 to main | ac4a7c6261580621f | haiku | 12:12 | Finished. Not merged. |

### 1.1 R14 sweep (every edit kind must save)
- **Status:** crashed. The last log lines are `Target page, context or browser has been closed` and a Node uncaught exception from `lib.mjs:42`. **verified** (`r14-sweep/sweep-loaded.log`, 15:32).
- **Where it wrote:** `~/Developer/astrid-release-src/r14-sweep/`
  - `sweep.mjs` (5786 bytes, 14:53), `lib.mjs` (5022 bytes, 14:53), `probe.mjs`, `t*.mjs`
  - `results.jsonl` (3293 bytes, 15:12): 14 rows, one per edit kind. **verified**
  - `results-run1-invalid.jsonl` (4698 bytes, 14:53): earlier run, marked invalid.
  - `sweep-loaded.log` (5164 bytes, 15:32): the loaded run, which crashed.
  - Screenshots `a.png`, `b.png`, `probe.png`.
- **Edit kinds and outcome (results.jsonl, verified).** These are the "[loaded]" rows, on clip-2 and the music-song audio clip:

| Edit | Outcome | ms |
|---|---|---|
| move clip-2 same track (drag +120px) | saved | 19560 |
| same, then UNDO | saved | 31323 |
| move clip-2 cross-track to Fx (drag) | saved | 3623 |
| move clip-2 onto shot track Picture (drag) | not saved | 11832 |
| keyboard move clip-2 track ArrowDown | not saved | 10948 |
| keyboard nudge clip-2 Alt+Right | not saved | 7418 |
| trim clip-2 right edge (drag -40px) | not saved | 18187 |
| trim clip-2 left edge (drag +30px) | not saved | 7767 |
| split clip-2 at playhead ('s') | not saved | 6778 |
| mute clip-2 ('m') | not saved | 12364 |
| delete clip-2 (Delete key) | not saved | 13886 |
| move audio music-song (drag +60px) | not saved | 42255 |
| trim audio music-song right edge (-30px) | not saved | 39110 |
| mute audio music-song ('m') | not saved | 56498 |

- **Refusal reasons (verified, toast text):**
  - Clip edits: "Local edits preceded the original verified read; draft retained" with Try again / Discard.
  - Audio edits: "The save has not been confirmed. Your changes are kept." with Try again / Discard.
- **Later rows in sweep-loaded.log** (after the crash cascade began) are `ROWERR` lines: a missing number input in the inspector, `connectOverCDP ECONNREFUSED 127.0.0.1:9540`, then `Target page ... has been closed` for every remaining row (track add, rename, reorder, shot move/trim, redo).
- **Agent's own summary (reported):** the Library drag (`application/x-generation`) ended "Not saved" with the same "preceded the original verified read" refusal. Three quick moves of one clip saved fine (commit 200). No digest conflict was seen. The agent called the refusal "a generic second-capture problem", not file-specific.
- **Not a check on the list:** the sweep covered 14 kinds. It did not cover shot-timeline or repeated-drop variants beyond the rows above.

### 1.2 Repeated-drag digest conflict (the external-drop-utils vanish)
- **Status:** stopped by disk-full (reported: free space fell to about 144 MiB, then commands returned ENOSPC). No final report, no PR, no commit. The agent said the three App fixes and the Runtime instrumentation had not landed. **reported**
- **Code locations (reported, quoted from the transcript; not re-read here):**
  - `astrid-app/src/tools/video-editor/.../external-drop-utils.ts:531-534`: the catch calls `onAssetDropError(error)` and `removeSkeleton()`.
  - `:526-529`: `if (!placed) removeSkeleton()`.
  - Skeleton removal around `:445-455`. `abandonDrop` at `:458-461`: "The timeline changed while this file uploaded; drop it again."
  - Key scoping at `:404-412`.
- **Message seen repeatedly (reported; 8 occurrences in its transcript):** "This media change would alter more than the asset you picked. Try adding it again." It appears on repeated drags and on a duplicate-file drop.
- **Diagnostic:** the Runtime side was to log the App's pin against the Runtime's recomputed digest for one failing drop. Not run.
- **Branches and worktrees (verified by git status/log):**
  - `wt-app-drop-error-parks`: `release/14/drop-error-parks` at `6976b017c`, clean. Its PR is reported as #309.
  - `wt-app-concurrent-drops-registry`: `release/14/concurrent-drops-registry` at `2ffc0a300`, 4 dirty files. Its history holds the merge of #309.
  - `wt-app-same-file-drop`: `release/14/same-file-drop` at `90e464039`, clean. Its history holds the merge of #308 ("gesture-registry-read").
  - `wt-rt-media-digest`: `release/14/media-digest-diagnostic` at `ee235d3`, **8 dirty files** (uncommitted instrumentation). Its history holds the merge of Runtime #67 (revert-62-retention).
  - `wt-rt-media-base`: detached at `ee235d3`, 6 dirty files.
- **Delete candidates the agent noted (reported):** `01M7QDNVQVTAB3RH14ACQPZA62` (spare duplicate project, archived). Its keep candidate `01M7QDJTM60WEK60JDXZPHGBRK` is the "Digest drop repro (Claude) 18 Nov" project.

### 1.3 Speed trim and #62 revert
- **Status:** no final report. Last narration (verified): "Waiting on the background golden generation (task b5nf5l1gp); it will notify on completion." The task output file is not in the tasks folder. Treat as unfinished.
- **Revert of #62 (verified in git):** Runtime branch `release/14/revert-62-retention` at `05d1ad8` in worktree `~/Developer/astrid-release-src/wt-r14-revert62`. Top commit: `Revert "Keep verified history across unrelated writes so an import never forces a re-walk"`. It has 6 dirty files.
- **Merged (verified in the local log of `wt-rt-media-digest`):** "Merge pull request #67 from banodoco/release/14/revert-62-retention".
- **Speed trim (reported only):** the `release/14/validate-trim` worktree `wt-r14-validate-trim` is at `ec758a9b8` with 3 dirty files. Its top commit merges `origin/release/14/plan-59` into `p59/recast-rubric`. This is the only trim-related branch found; whether it is the speed-trim work is unverified.

### 1.4 Profiler (sonnet-commit-profile-r14)
- **Status:** finished. Report is at `~/Developer/astrid-release-src/plan-review/sonnet-commit-profile-r14.md` (16509 bytes, 14:09). **verified** (file exists; contents from the agent's final message, **reported**).
- **Build profiled (reported):** Agent `458d9d51`, Runtime `d725811`. Almost Ready: 616 clips, 2.6 MB.
- **Findings (reported):**
  - `validate_final_candidate` is 56-59% of wall time. Skipping it takes a commit from 3.74 s to 1.63 s.
  - The timing validation runs the legacy-declaration pass twice (`_commit_timing_validation.py:387` and `:374`).
  - Top cost (cProfile): `validation.py:667` `validate_final_candidate` about 2.1 s; `commit.py:302` `document_from_bundle` about 0.54 s; `commands.py` `execute` about 0.45 s; `_check_readers` about 0.38 s.
  - Absorb vs discard for the history retention: "Discard wins" on this timeline (absorb costs about 1,450 extra statements per import and saves nothing on the next commit). The 5-7 s import wait is mostly gone in both modes.
  - Clip count does not matter on its own: a one-clip timeline commits in 0.22 s, the duplicate with no history in 3.54 s.
- **Harness status:** `pr_harness.py` does not exist. **verified**: `find /private/tmp/claude-501 ~/Developer/astrid-release-src -name pr_harness.py` returned nothing.
  - The profiler's helper scripts are `prof_run.py` (lines 18-19 and 14) and `wall_run.py` (lines 20-21), named by the "Find profile harness" agent (**reported**). Its scratch clone (`scratchpad/data`) was deleted per its own doc. Not re-checked.
- **Earlier profile:** `sonnet-commit-profile.md` (02:47) found 187 s for one add-media commit on Almost Ready, with 67% in `_legacy_exemptions` -> `_reference_basis`. **reported**, from the file.

### 1.5 Plan PR #880 (astrid-dev, "Dependable saving", plan 63)
- **Status:** NOT merged. Reported by the merge agent (finished 12:12): the required `documentation` check failed on head `3dc1b4ed`.
  - Error lines: `ERROR project-planning-evidence: 63-dependable-saving: missing 'Approach' planning evidence`, and the same for 64-fast-saving and 65-editing-together.
  - `mergeable_state` is `blocked`. The fix belongs in the plan docs, so the PR needs a new push. The agent did not force or bypass anything.
- **Local branch (reported in QUEUE.md):** `plan/63-dependable-saving` at `fe8e09dd` (worktree `scratchpad/wt63b`; the ref is in `~/Developer/astrid-dev/.git`), with the PR body to change to "about 35". This push was **blocked** after the reboot: the GitHub keychain item was gone (QUEUE: BLOCKED 11:45). The token is in `~/.github_token` (memory note); not read here.
- **Four plan commits on astrid-dev `3dc1b4ed` (reported):** 63 Dependable saving (about 30 days), 64 Fast saving (about 11 days plus a conditional 9), 65 Editing together (about 11.5 days), 18 extensible. All queued in no release.

### 1.6 Other merges by the same period (reported; check before relying)
- Runtime #62 merged to `release/14/plan-59` as `1af7ed60d693fc...` (verified: the SHA exists in `~/Developer/astrid-release-src/runtime-src`).
- App #300 merged to `release/14/plan-59` as `48202a7acc661a7cc2a4e678d3135103963d9d02` (verified: the SHA exists in `~/Developer/astrid-release-src/astrid-app`).
- The `direct-journey` check failed on App #300 when GitHub accepted the merge. Its cause is not known. Required checks did not include it.

---

## 2. plan-review folder

Path: `~/Developer/astrid-release-src/plan-review/`. Sizes and mtimes (**verified**, local time, 18 Nov unless noted):

| File | Bytes | Modified |
|---|---|---|
| QUEUE.md | 20168 | 18 Nov 12:16 |
| fable-agent-edits.md | 21257 | 11:34 |
| fable-commit-proof-fit.md | 20987 | 13:39 |
| fable-dependable-saving-check.md | 23195 | 11:18 |
| fable-diagnosis-check.md | 6946 | 12:36 |
| fable-edit-refusals-deeper.md | 7072 | 17 Nov 23:48 |
| fable-end-state-review.md | 28574 | 13:41 |
| fable-final-recommendations.md | 37282 | 13:53 |
| fable-four-questions.md | 36764 | 11:51 |
| fable-gap-method.md | 10194 | 12:39 |
| fable-getting-it-running.md | 7742 | 17 Nov 21:29 |
| fable-live-blockers.md | 11675 | 03:31 |
| fable-near-instant-review.md | 18317 | 02:59 |
| fable-program-dir-blocker.md | 8081 | 17 Nov 19:40 |
| fable-properly-now.md | 11060 | 17 Nov 22:25 |
| fable-quick-edits.md | 14159 | 11:38 |
| fable-realm-copy-refuses.md | 9695 | 17 Nov 21:49 |
| fable-realm-start-blocker.md | 7956 | 17 Nov 20:32 |
| fable-reattach-blocker.md | 8804 | 17 Nov 20:12 |
| fable-save-category-design.md | 26003 | 10:30 |
| fable-sense-check.md | 23748 | 17 Nov 20:28 |
| fable-stability-sequencing.md | 11206 | 10:49 |
| fable-still-slow-review.md | 17472 | 10:21 |
| fable-two-paths.md | 20969 | 17 Nov 19:02 |
| fable-update-autostart-off.md | 10819 | 17 Nov 19:20 |
| first-start-trace.log | 52671 | 17 Nov 22:27 |
| live-check-almost-ready.md | 19112 | 02:23 |
| near-instant-facts.md | 14639 | 03:06 |
| opus-396-review.md | 15746 | 04:54 |
| opus-phase0-review.md | 21703 | 03:28 |
| opus-r14-save-fixes-review.md | 19494 | 11:10 |
| opus-r14-set-review.md | 22224 | 04:14 |
| opus-review-agent-387.md | 26833 | 00:47 |
| opus-review-app-285-probes/ | 192 (dir) | 01:15 |
| opus-review-app-285.md | 36452 | 01:17 |
| opus-review-app-286-probes/ | 96 (dir) | 01:26 |
| opus-review-app-286.md | 14524 | 01:31 |
| opus-runpod-edits.md | 10008 | 17 Nov 18:52 |
| plan-near-instant-commits.md | 9305 | 03:01 |
| r14-slow-save-evidence.md | 11255 | 10:14 |
| save-failures-evidence-pack.md | 31283 | 10:27 |
| save-state-map.md | 13929 | 10:22 |
| sonnet-commit-profile-r14.md | 16509 | 14:09 |
| sonnet-commit-profile.md | 13798 | 02:47 |
| sonnet-finder-drop-unconfirmed.md | 5632 | 02:00 |
| sonnet-unnamed-edits-on-shot-timelines.md | 7881 | 01:11 |

### 2.1 QUEUE.md open items (verified read; statuses are as written in the file at 12:16)
1. **Release 14 :2400 stack:** the Agent's pin must be bumped with `regenerate_runtime_pins.py`, then :2400 rebuilt and browser-tested (drop, drop during save, stop/start Runtime during save, reload, Discard).
2. **App #299** (`release/14/save-recovery`, commit `c0750f500`): "merging" at 12:16. State after that not known.
3. **Agent #400** into `release/14/main`, then `main` into plan-59. Agent #402 (oracle frozen, 33 cases identical): ready, held.
4. **Runtime #61** (`release/14/selection-digest`): the retained reader keeps the old digest behind `retained=True`; the v33 "affected" test is being re-seeded.
5. **Runtime transport** (`release/14/transport`, N5/N10/N11): PR pending.
6. **Runtime #65** (`release/14/commit-hook`): held pending the A/B measurement. The profile favours discard, so the plan is to revert #62 retention (done as #67) and use SQLite immutability triggers for Plan 63.
7. **Opus must-fixes:** App 1, 2, 3 and 5-10 on `release/14/save-recovery-2` (Sonnet); Runtime 4 on #65. Status not recorded in the file.
8. **Live-fix bugs** sent to `release/14/live-fixes`: Try again on a recovered draft from an old realm loops silently with a "Saved" badge; Discard left 37 old-realm outbox rows; an 11 s "Dirty" delay before the first send.
9. **Blocked pushes (credential gone after reboot, since 11:45):** agent `release/14/runtime-pin-r14b` at `ae9c3bb44`; astrid-dev `plan/63-dependable-saving` at `fe8e09dd` (-> #880); app `release/14/quick-edits` at `ff34621e9`.
10. **#880 documentation check:** the Approach planning evidence is missing for plans 63-65.
11. **`direct-journey` fails on plan-59 PRs** (#299 and #300): suspected App pin skew (App lock pins Runtime `2d490617`). Fix at release freeze with `regenerate_runtime_pins.py --app-checkout <App>`. Does not block :2400.
12. **Release 15:** `release/15/main` was cut (App `358dd0157` #301, Runtime `3a609a6f2` #64, Agent `1ad6160a9` #401). Still to do: forward-merge after the pin bump and #61; fill the cut SHAs into `releases/15.md`.
13. **Owner decisions open:** D15 (refusal: remove-and-list or leave visible), D9 (Release 15 recommended), D10 (synthetic corpus), D14 (persist `file_identity`).
14. **Plan 18 Phase 0** PR into astrid-dev `main`, after the Opus review.
15. **Almost Ready animation edits** must go live on the owner's real timeline ("done only when live").

### 2.2 Fable and Sonnet reports, one line each (verified read of each file's verdict section)
- fable-agent-edits: Every live timeline write goes to one commit route with one validator, but the clients and the guidance do not agree; asks for one consistent approach for editor and agent edits.
- fable-commit-proof-fit: The "edit refused by commit authentication" fix is three small tasks on the Agent and Runtime track of Plan 63; the proof should be derived in the Agent.
- fable-dependable-saving-check: "Proceed lean": the design centre is right and close to minimal; Release 14 has not built it.
- fable-diagnosis-check: Claim table; provider_commit dominates the save time, but the cause is not identified.
- fable-edit-refusals-deeper: Refusals come from several decision points with no single owner of what an edit means (17 Nov).
- fable-end-state-review: Editor end state is elegant; the Agent-Runtime layer is an unaddressed structural hole in the plans.
- fable-final-recommendations: Merge two reviews into one design; A's four tasks go into Plan 63, B's rule into Plan 64.
- fable-four-questions: Fast edits are possible: one save in flight, later edits queue as the next commit, the server document reaches the screen only when nothing is outstanding.
- fable-gap-method: Method for the 4-5 s to near-instant gap; bisection plan, nothing measured.
- fable-getting-it-running: Stack was running on the installer's empty realm on 17 Nov 21:28; the next blocker is the copied realm start.
- fable-live-blockers: Almost Ready edits can only go live through an App deploy from product main, so a publication is needed; Agent fix #393 should ride it.
- fable-near-instant-review: The draft removes the right two costs but stops one level short; three of its eight items need changing.
- fable-program-dir-blocker: "The program directory contains files Astrid does not own" was a tool check; the fix is already in the tool; keep it.
- fable-properly-now: Ranked list of what to do now for astrid-release (trace the first-start failure first, then `workspace attach`).
- fable-quick-edits: Approach: while anything is queued the screen keeps the person's edits; an accepted save only moves the base. Mostly built; not yet in Plan 63.
- fable-realm-copy-refuses: Cause not proven; the copied realm is healthy and the Runtime starts on it outside the stack (8 of 8); one traced start will settle it.
- fable-realm-start-blocker: The error "discovery realm root does not match" comes from a stale record that carried the old realm root.
- fable-reattach-blocker: "Retained Runtime source configuration cannot be verified": root cause in the kept-data source config (read).
- fable-save-category-design: One home and four outcomes for every change; seven small changes make :2400 dependable now.
- fable-sense-check: Claim that the tool never writes or restarts live is sound, but too strong in four places; no evidence live was changed.
- fable-stability-sequencing: Stability is separable and goes first; Phase 0 becomes its own project, Release 15 (D9).
- fable-still-slow-review: The remaining problem is bulk media traffic every drop starts (every audio source re-downloaded), not the commit algorithm; ENOBUFS on loopback.
- fable-two-paths: Keep Plan 61's manifest idea; five places drift from the installer (rollback, branch-keyed stack, etc.).
- fable-update-autostart-off: `--update` on an autostart-off stack fails because of a global launchd label collision; design options given.
- sonnet-commit-profile-r14: Validation is the hotspot (56-59%); legacy pass runs twice; discard beats absorb on Almost Ready.
- sonnet-commit-profile: One 616-clip add-media commit took 187 s uncontended; cProfile 280 s; the hotspot is `_legacy_exemptions` / `_reference_basis`.
- sonnet-finder-drop-unconfirmed: Ranked candidates for "save never got a confirmation" on a Finder drop (shallow clone limits history checks).
- sonnet-unnamed-edits-on-shot-timelines: Unnamed edits on shot timelines are refused at `hooks/timelineLocalSaveHandoff.ts:318` and `:651`; smallest safe fix for Release 14 vs Plan 18 given.

---

## 3. The stack (~/astrid-release)

### 3.1 Logs
- `start-pre66.log` (mtime 13:38), `rebuild-pre66.log` (13:11), `update-run-123205.log` (12:32). All **verified** (read).
- Ports: editor 2400, proxy 17500, door 17501.
- Realm copy: `<owner-realm>`. Copied from the owner's data: 558 media files, 279 byte-compared, 2211654876 bytes. Stack selects it. Timelines listed through the stack: 8 (start log) and 7 (update log). **verified**
- Live runtime (`haus.astrid.runtime`) was left untouched by the runs (plist mtime unchanged). **verified**

### 3.2 Pinned SHAs (verified from start-pre66 / rebuild-pre66)
- App: `release/14/plan-59` at `9f548b34def6` (rebuild log).
- Agent: `ca3f830feffb103791b0e5358a81a9c8f6eefda6`.
- Runtime: `4c18af59d233a...` (`4c18af59d233da7cd1c6a13657823ca2b71e37ac`).
- Manifest sha256: `9c9e746eb5138f5e92baf5bcd87e8598c6aa92597c92083956b24517c4071923`.
- Lock pins: vibecomfy `79143f24ee4d`; runpod-lifecycle `9f88ef7640bc`.
- Not running (verified): runpod-lifecycle tip `93beec314171` is not what the stack installs (its lock needs a bump on the Agent branch). timeline-composition tip `e628744bf9e6` is never built in (the App and Agent each bundle their own tarball).
- Installer result: "updated (current program: f8413e63b423)". The log also says "Astrid installed: Release 13 (build ca3f830f)". Odd label; not explained in the log.
- **Conflict to note:** QUEUE.md says :2400 was rebuilt at 12:0x on App `f236327ca`, Agent `2829f180`, Runtime `e6f4d5c2`. The logs above are later (13:11 and 13:38) and show App `9f548b34` / Agent `ca3f830f` / Runtime `4c18af59`. The logs are the newer record. Which pins :2400 runs now has not been checked (the stack was not queried).

### 3.3 Commands (verified from the log's "To launch / Status / Stop" lines)
Let `ASTRID=~/Developer/astrid-release-src/astrid-app/scripts/astrid-release/astrid-release`.
- Start (after stop or reboot): `$ASTRID release/14/plan-59`
- Open: `http://127.0.0.1:2400/tools/video-editor?connect=1`
- Update (pull newer code, keeps data): `$ASTRID update release/14/plan-59`
- Status: `$ASTRID status release/14/plan-59`
- Stop: `$ASTRID stop release/14/plan-59`
- CLI for this stack: `HOME=~/astrid-release/release-14-plan-59/home ~/astrid-release/release-14-plan-59/program/run-astrid`

### 3.4 Folders and sizes (`du -sh`, verified, run 15:5x)
| Folder | Size |
|---|---|
| `release-14-plan-59/` (live stack) | 7.6G |
| `release-14-plan-59.root-pre66/` | 7.6G |
| `release-14-plan-59.data-20261118-0138/` | 2.1G |
| `release-14-plan-59.data-20261118-0147/` | 2.1G |
| `release-14-plan-59.data-20261118-0258/` | 2.1G |
| `release-14-plan-59.data-20261118-0904/` | 2.1G |
| `release-14-plan-59.data-20261118-100141/` | 2.1G |
| `release-14-plan-59.data-20261118-1204/` | 1.6G |
| `release-14-plan-59.data-20261118-1232/` | 1.6G |
| `release-14-plan-59.data-20261118-1250/` | 1.6G |
| `release-14-plan-59.data-pre66-1307/` | 1.6G |
| `realm-fresh-copy-pre66/` | 1.6G |

Inside `release-14-plan-59/`: `program` 3.8G, `home` 1.4G, `data` 1.7G, `editor` 727M, `logs` 596K, `state` 276K.
Total of the folders above is roughly 35 GB. Each `.data-*` is a backup of the realm data; the 2026-11-18 "data-*" folders are the owner's backups and are not to be deleted without a decision (QUEUE: owner decision on the 6.9 GB folder and older backups).

### 3.5 Disk now
`df -h /`: 15Gi free, 42% used (**verified** at 15:56). The disk was 155 MiB free at the time of the crash (reported).

---

## 4. Tools that already exist for heavy timelines, benchmarks, and drag/save harnesses

Grep was run over the three clones (`~/Developer/astrid-release-src/{astrid-app,agent-src,runtime-src}`), excluding node_modules, .git, dist and build. Purposes below are from file names and header comments only, unless marked "header" (read).

### 4.1 Editor performance and latency
- `astrid-app/scripts/perf/measure-editor.mjs`: editor load, 60 s idle network and CPU, playback, scrub latency, memory. Requires a running App and Runtime; uses installed Chrome (`PLAYWRIGHT_CHANNEL`). Read-only mode. **header read**
- `astrid-app/scripts/perf/compare-editor-measure.mjs`: compares two outputs of the above. **name only**
- `astrid-app/tests/e2e/timeline/extension-performance-budget.spec.ts`: extension performance budget. **name only**
- `astrid-app/tests/e2e/timeline/preview-scrub-evidence.spec.ts`: scrub evidence. **name only**
- `astrid-app/tests/e2e/local/support/measure.ts`: measurement helper for the local tests. **name only**

### 4.2 Runtime and Agent commit tests and helpers (candidates for a synthetic heavy timeline)
- `runtime-src/tests/helpers/p2_commit_phase_capture.py`: captures commit phases. **name only**
- `runtime-src/tests/test_timeline_commit_baseline.py` and `runtime-src/tests/test_timeline_commit_acceptance.py`: commit baseline and acceptance. **name only**
- `runtime-src/tests/baseline_fixture.py`, `runtime-src/tests/precut_realm_fixture.py`, `runtime-src/tests/project_isolation_fixture.py`, `runtime-src/tests/historical_audio_fixture.py`: realm and project fixtures. **name only**
- `agent-src/tests/editing_conformance/test_commit_runtime_parent_media.py` and `..._swap.py`: commit with parent media. **name only**
- `agent-src/tests/sdk/test_timeline_commit_provider_runtime.py`, `agent-src/tests/sdk/test_workspace_client_timeline_commit.py`: commit provider and client. **name only**
- `agent-src/scripts/acceptance/timeline_transfer.py`: timeline transfer acceptance. **name only**
- Nothing found by grep with a clear name for "synthetic" or "large timeline" generators. The 616-clip timeline was reached by copying the owner's realm (not by a generator).

### 4.3 Profiling harness (from the profiler's child agent; **reported**)
- `prof_run.py` (cProfile runs, lines 14, 18-19) and `wall_run.py` (wall-clock runs, lines 20-21). Both were in the profiler's scratch clone `scratchpad/data`, which the doc says was deleted. Not re-checked. The profile interpreter was `fdbff077811b/py/bin/python`.
- No `pr_harness.py` exists anywhere (verified).

### 4.4 Browser and Playwright harnesses that drive editor drag, drop and save
- `astrid-app/playwright*.config.ts` (about 12 configs, e.g. `playwright.direct.config.ts`, `playwright.three-products.config.ts`). **name only**
- `astrid-app/tests/e2e/timeline/support.ts`: timeline test support. **name only**
- `astrid-app/tests/e2e/video-editor-workflow-parity.spec.ts`, `video-editor-processes.spec.ts`, `video-editor-instance-lifecycle.spec.ts`: editor workflow specs. **name only**
- `astrid-app/tests/e2e/local/timeline-transfer.spec.ts` (**name only**), `tests/e2e/local/three-products.*.spec.ts` (grep matched drag/drop/`mouse.move`/`DataTransfer` in these specs; the matches were in the "local" tests and `tests/e2e/local/support/app.ts`).
- `astrid-app/tests/e2e/direct-journey.spec.ts` and `tests/e2e/support/app.ts` (the failing `direct-journey` check, from QUEUE): name only.
- The agent-built harness: `~/Developer/astrid-release-src/r14-sweep/sweep.mjs` and `lib.mjs`. They attach to Chrome over CDP on port 9540 (`browserType.connectOverCDP`), and their profile names are shared with the sweep (per the drag agent). Use with care; the sweep crashed on the disk-full error.

### 4.5 Plans 54 and 55 (checked, not the same problem)
- `~/Developer/astrid-dev/plans/54-warm-latency/` and `plans/55-local-speed/`: their goals are **generation** speed (a model's warm generation time and Astrid's overhead on a rented or local machine). They do not cover editor save latency. Not a benchmark for this problem.
  - 54 files: `inputs.md`, `plan.md`, `tasks.md`.
  - 55 files: `developer-handoff.md`, `evidence/`, `github-publication.md`, `handover.md`, `inputs.md`, `plan.md`, `review.md`, `tasks.md`.

---

## 5. Gaps and cautions for the receiving machine

- **GitHub credential:** the keychain item was lost at reboot (QUEUE, 11:45). Re-seed it before any push. The token file is `~/.github_token` (memory note). Do not print it.
- **Disk:** the crash was a full disk from runs leaving headless Chromes and /tmp profiles, plus the scratchpad `r14m` folder. The folder is reported at 5.9 GB (`frozen` 3.8 GB, `data1` 2.1 GB), last written 14:49. **verified absent now:** the scratchpad of this session lists only `inv.sh`, `inventory.txt`, `tail.py`, `texts.py`.
- **Uncommitted work:** `wt-rt-media-digest` (8 files), `wt-r14-revert62` (6), `wt-rt-media-base` (6), `wt-app-concurrent-drops-registry` (4), `wt-r14-validate-trim` (3). These are not in any branch.
- **Unfinished work with no report:** the repeated-drag fix, the speed trim, and the sweep. Restart each from its worktree and its last narration, and check each claim before reuse.
- **Mismatch in pins:** see 3.2. Read the stack's own status before assuming which build :2400 runs.
- **Owner data:** do not delete `release-14-plan-59.data-*` or the owner's backups without a decision.
