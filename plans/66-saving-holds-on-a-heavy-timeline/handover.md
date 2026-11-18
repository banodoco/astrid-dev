# Handover — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Rounds](rounds.md)

Written on 18 November 2026 for whoever runs this plan next, on another machine. It is a dated snapshot: re-read branch heads with `git ls-remote` before acting. Claim sources: **verified** means read from a file or command on 18 November; **reported** means an earlier agent said so and nothing re-checked it.

## First actions on a new machine

1. **Clone the repositories** (all under `banodoco` on GitHub): `astrid-dev`, `astrid-app`, `astrid-agent`, `astrid-runtime`. Free disk first: 40 GB, and never below 15 GB during a run (the disk filled twice on 18 November from headless browser profiles and stack copies). Needs macOS (the release script uses APFS clones and launchd), Node 20, ffmpeg and Playwright.
2. **Check out the branches** (all on origin, cut from `release/14/plan-59`): `release/14/plan-66` in each of astrid-app, astrid-agent and astrid-runtime, and `plan/66-live-loop` in astrid-dev (this pack). Use one worktree per branch; keep the main clones clean.
3. **Fix astrid-dev PR #880** (branch `plan/63-dependable-saving`, Plans 63, 64, 65 and 18, for Release 15). It is open and its `documentation` check fails: `ERROR project-planning-evidence: … missing 'Approach' planning evidence` for 63, 64 and 65 (reported on head `3dc1b4ed`). Main has since used numbers 64 and 65 for two H3 plans, so renumber #880's 64 and 65 to 67 and 68 (directory names, titles, every link, the catalog row, `priority.md` if listed), and write each plan's `**Approach:**` line in its `inputs.md` ([template](../../templates/project/inputs.md)). Then run the docs check below and push. The PR body should say "about 35" (reported). Later, the plan deltas from [rounds.md](rounds.md) go into these plans.
4. **Build the stack** ([below](#build-the-stack)).
5. **Build the fixture** (SL-0): `scripts/save-loop/build-fixture.*` in astrid-app, not written yet.
6. **Run round 1** ([live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round)). The first run of the seeded sweep on the new fixture should reproduce 3 saved and 11 refused; if it does not, say why before fixing anything.

Checks for every astrid-dev PR here: `python3 scripts/astrid_dev.py check` and `python3 -m unittest discover -s scripts -p "test_*.py"`. For a PR add `--base <base commit> --body-file /dev/null` to the check.

## Where everything is

- **This pack:** astrid-dev `plan/66-live-loop`, `plans/66-saving-holds-on-a-heavy-timeline/`. Evidence copies (the originals were in a folder not under git): [evidence/](evidence/). Start with `handover-facts-20261118.md`, then `sonnet-commit-profile-r14.md`, `fable-final-recommendations.md`, `fable-commit-proof-fit.md`, `fable-end-state-review.md` and `QUEUE.md`.
- **Seeded harness:** astrid-app `release/14/plan-66`, `scripts/save-loop/` (`sweep.mjs`, `lib.mjs`, `sweep.b64`; head `36d2b8258`). Read its header for the flags and `SAVE_LOOP_*` environment variables. Row ids and pixel coordinates are still hard-coded for a 1700 by 1500 viewport. The profiler helpers `prof_run.py` and `wall_run.py` were not found on disk; `scripts/perf/measure-editor.mjs` already exists in astrid-app.
- **Crash work, pushed to origin as wip branches** (inventory taken on 18 November; verified from `git ls-remote`):

| Repository | Branch | SHA | What it holds |
| --- | --- | --- | --- |
| astrid-app | `release/14/plan-66-wip/wt-app-concurrent-drops-registry` | `2402b1d97` | concurrent drops refusing each other (four files: `timelineLocalSaveHandoff(.test).ts`, `useAssetManagement.ts`, `useTimelineCommit.ts`) |
| astrid-agent | `release/14/plan-66-wip/wt-r14-validate-trim` | `2bb8c1095` | the speed trim of `validate_final_candidate`, barely started, with a golden test |
| astrid-runtime | `release/14/plan-66-wip/wt-rt-media-digest` | `a3acdc5fc` | the media digest diagnostic log |
| astrid-app, astrid-agent, astrid-runtime | `…/wt-shot-trim`, `…/agent-src-main-clone`, `…/runtime-src-main-clone`, `…/wt-r14-agentbase` | app `11ee51c1e`, agent `15ca752d1` and `ed0c6c6e4`, runtime `1b3f36083` | a separate shot-trim task. **Out of scope; only listed.** |

  Other branches reported done and merged into `release/14/plan-59` earlier: Runtime #66, #67; App #308 and #309 (drop-error parks).
- **Release 14 stack run on 18 November:** under `~/astrid-release/release-14-plan-59` on the first machine; stopped. It holds a copy of the owner's data and is not part of this plan.

## Build the stack

The real route is `scripts/astrid-release/astrid-release release/14/plan-66` in astrid-app (it also has `status`, `stop` and `update <branch>`). It builds an isolated root and ports under `~/astrid-release/release-14-plan-66`, refuses the live ports (17340, 2222, 17336, 17391) and never writes the live install. **Known limit (read, not run):** it always snapshot-copies the machine's live realm, so on a machine with no live Astrid it stops; SL-1 decides the smallest empty-realm option. Moving a built stack to newer commits is not supported without losing data (issue #825): to test new commits stop it, keep `data/`, delete the root and run it again. After a Runtime fix, run `scripts/regenerate_runtime_pins.py` in astrid-agent before rebuilding (reported).

## Known broken or open

- **Sweep:** 14 edit kinds on the loaded timeline: 3 saved (a move, its undo, a cross-track move), 11 refused. Clip edits show "Local edits preceded the original verified read; draft retained"; audio edits show "The save has not been confirmed. Your changes are kept." Both with Try again and Discard. The run crashed when the disk filled, so the result needs a rerun. The Library drag ended "Not saved" with the same first message (reported).
- **Drops:** "conflict: selected media catalog digest changed" on repeated drags (not reproduced; the likely trigger is dragging one library item several times); a failed drop deletes its placeholder (`external-drop-utils.ts:531`); three quick drops refuse each other ("would alter more than the asset you picked"); a same-file double drop is refused.
- **Speed:** save on the real timeline 3.74 s median, 0.22 s on one clip; `validate_final_candidate` about 57%, a doubled legacy-declaration pass inside (reported from the profile). Target here about 2 s.
- **Other open items on the crash day** (reported, in [QUEUE.md](evidence/QUEUE.md)): a recovered draft from an old realm loops on Try again with a "Saved" badge; Discard left 37 old-realm outbox rows; an 11 s "Dirty" delay before the first send; the `direct-journey` check fails on plan-59 PRs, suspected pin skew.
- **Fixture mismatch:** the copied timeline has 8 clips and 140 KB, while the profile says 616 clips and 2.6 MB; see [inputs](inputs.md#heavy-timeline-shape).
- **Hygiene:** the harness profiles and stack copies are what filled the disk; delete each profile after its run.
