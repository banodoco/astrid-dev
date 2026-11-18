# Handover — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Rounds](rounds.md)

Written on 18 November 2026 for whoever runs this plan next, on another machine. It is a dated snapshot: re-read branch heads with `git ls-remote` before acting. Claim sources: **verified** means read from a file or command on 18 November; **reported** means an earlier agent said so and nothing re-checked it.

## First actions on a new machine

1. **Clone the repositories** (all under `banodoco` on GitHub): `astrid-dev`, `astrid-app`, `astrid-agent`, `astrid-runtime`. Free disk first: 40 GB, and never below 15 GB during a run (the disk filled twice on 18 November from headless browser profiles and stack copies). Needs macOS (the release script uses APFS clones and launchd), Node 20, ffmpeg and Playwright.
2. **Check out the branches** (all on origin, cut from `release/14/plan-59`): `release/14/plan-66` in each of astrid-app, astrid-agent and astrid-runtime, and `plan/66-live-loop` in astrid-dev (this pack, until it is merged). One worktree per branch; keep the main clones clean. Record your session id in the `Owner` line of [plan.md](plan.md) ([authority](inputs.md#planning-evidence)).
3. **Create `run.yaml`** ([below](#runyaml)).
4. **Build the stack** (SL-1, [below](#build-the-stack)).
5. **Build the fixture** (SL-0): `scripts/save-loop/build-fixture.*` in astrid-app, not written yet.
6. **Run round 1** ([live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round)), once SL-2 has retargeted the harness. SL-3 (recover the lost work) and SL-5 (astrid-dev PR #880) run beside these and do not block round 1.

Checks for every astrid-dev PR here: `python3 scripts/astrid_dev.py check` and `python3 -m unittest discover -s scripts -p "test_*.py"` (Python 3.10 or later). For a PR add `--base <base commit> --body-file /dev/null` to the check.

## run.yaml

`.otto/` is gitignored, so create the run's `run.yaml` on the new machine from [`skills/shared/templates/run.yaml`](../../skills/shared/templates/run.yaml), under `plans/66-saving-holds-on-a-heavy-timeline/.otto/runs/<run-id>/`.

- **Bindings:** bind `N`, `X`, the advisor and the reviewer from the owner's own delegation table (in their global agent instructions: normal, hard and sense-check tiers on Codex). If that table is not on the machine, ask the owner. Do not guess model IDs.
- **If Codex is unavailable** (on the first machine its usage limit was exhausted until 20 November 00:00), run the same routes on the Claude families in the [run contract's routing table](../../skills/shared/run-contract.md#routing-and-bindings), record `--override`, and carry on. Do not wait.
- The advisor is a role, not route `S`: it gives the strategy each round; the reviewer runs the final review.

## How to work

- The coordinator keeps the judgment and delegates the doing.
- Scenarios only ever use the sandbox fixture, never the owner's timelines.
- No arbitrary time limits in tests; only a hang fails.
- Treat the advisor's advice as evidence, and ask it what to remove first.
- After a Runtime fix, regenerate the Agent's Runtime pins (`scripts/regenerate_runtime_pins.py` in astrid-agent) before rebuilding the stack.
- Tag claims as verified or reported.

## Where everything is

- **This pack:** astrid-dev `plan/66-live-loop`, `plans/66-saving-holds-on-a-heavy-timeline/`. Evidence copies (the originals were in a folder not under git): [evidence/](evidence/). Start with `handover-facts-20261118.md`, then `sonnet-commit-profile-r14.md`, `fable-final-recommendations.md`, `fable-commit-proof-fit.md`, `fable-end-state-review.md` and `QUEUE.md`.
- **Seeded harness:** astrid-app `release/14/plan-66`, `scripts/save-loop/` (`sweep.mjs`, `lib.mjs`, `sweep.b64`; head `36d2b8258`). Read its header for the flags and `SAVE_LOOP_*` environment variables. It attaches over CDP to an existing browser at `127.0.0.1:9540` and targets the owner's `clip-2` and `music-song` at a 1700 by 1500 viewport; SL-2 retargets it. Row ids and pixel coordinates are hard-coded. The profiler helpers `prof_run.py` and `wall_run.py` were not found on disk; `scripts/perf/measure-editor.mjs` already exists in astrid-app.
- **Crash work, pushed as wip branches** (verified by GitHub compare on 18 November):

| Repository | Branch under `release/14/plan-66-wip/` | Head | Base | What it holds |
| --- | --- | --- | --- | --- |
| astrid-app | `wt-app-concurrent-drops-registry` | `2402b1d97` | `2ffc0a300` (plan-59 tip, the plan-66 cut), 1 commit | concurrent drops refusing each other (`timelineLocalSaveHandoff(.test).ts`, `useAssetManagement.ts`, `useTimelineCommit.ts`) |
| astrid-agent | `wt-r14-validate-trim` | `2bb8c1095` | `ec758a9b8`, 1 commit | the speed trim of `validate_final_candidate`, barely started, with a golden test |
| astrid-runtime | `wt-rt-media-digest` | `a3acdc5fc` | `ee235d39d`, 1 commit | the media digest diagnostic log |
| astrid-agent | `wt-r14-agentbase` | `ed0c6c6e4` | `ec758a9b8`, 1 commit | its only changed file on 18 November was the same golden test (reported inventory); check before ignoring it |
| astrid-app | `wt-shot-trim` | `11ee51c1e` | `4eb6fb3`, 7 ahead, 74 behind plan-66 | a separate shot-trim task: **out of scope, only listed** |
| astrid-agent | `agent-src-main-clone` | `15ca752d1` | `f9642bd`, 6 ahead, 68 behind | same shot-trim task, out of scope |
| astrid-runtime | `runtime-src-main-clone` | `1b3f36083` | `519b404`, 2 ahead, 16 behind | same shot-trim task, out of scope |

  **Already contained in `release/14/plan-66`** (GitHub compare, ahead 0): App `release/14/same-file-drop`, App `release/14/quick-edits`, Agent `release/14/runtime-pin-r14b`. Merged into plan-59 before the cut (reported): Runtime #66, #67; App #308, #309.
- **Release 14 stack run on 18 November:** under `~/astrid-release/release-14-plan-59` on the first machine; stopped. It holds a copy of the owner's data and is not part of this plan.

## Build the stack

The real route is `scripts/astrid-release/astrid-release release/14/plan-66` in astrid-app (it also has `status`, `stop` and `update <branch>`). It builds an isolated root under `~/astrid-release/release-14-plan-66` (the branch name with `/` as `-`), refuses the live ports (17340, 2222, 17336, 17391) and never writes the live install. **Known limit (read, not run):** it stops at its start when the machine has no live install or realm, so SL-1 adds an empty-realm option; ports and the editor URL are in SL-1 and SL-1 records the real ones here. Moving a built stack to newer commits is not supported without losing data (issue #825): to test new commits stop it, keep `data/`, delete the root and run it again.

## Known broken or open

- **Sweep:** the 14 kinds are the scenarios that completed on the loaded timeline: 3 saved (a move, its undo, a cross-track move), 11 refused. Ten more rows failed with ROWERR (12 ROWERR lines in the log). Clip edits show "Local edits preceded the original verified read; draft retained"; audio edits show "The save has not been confirmed. Your changes are kept." Both with Try again and Discard. The run ended with "Target page, context or browser has been closed" after `connectOverCDP ECONNREFUSED 127.0.0.1:9540`, not a disk error; the disk was nearly full at the time (reported). It needs a rerun. The Library drag ended "Not saved" with the same first message (reported).
- **Drops:** "conflict: selected media catalog digest changed" on repeated drags (not reproduced; the likely trigger is dragging one library item several times); a failed drop deletes its placeholder (`external-drop-utils.ts:531`); three quick drops refuse each other ("would alter more than the asset you picked"); a same-file double drop is refused.
- **Speed (the profile's own numbers):** a commit on the heavy timeline was 3.74 s median, 0.22 s on one clip, as a warm commit median through the Runtime from the CLI, not editor time to Saved. `validate_final_candidate` is about 59% of it; the legacy-declaration pass inside is about 57%; skipping validation saves about 56% (2.11 s). Target here about 2 s; 300 ms is Plan 64's.
- **Other open items on the crash day** (reported, in [QUEUE.md](evidence/QUEUE.md)): a recovered draft from an old realm loops on Try again with a "Saved" badge; Discard left 37 old-realm outbox rows; an 11 s "Dirty" delay before the first send; the `direct-journey` check fails on plan-59 PRs, suspected pin skew.
- **Fixture discrepancy:** the copied timeline has 8 clips and 140 KB, while the profile says 616 clips and 2.6 MB. The profile names "Almost Ready (trial v2)", so the copy probably read a different timeline. The fixture targets the profile; see [inputs](inputs.md#heavy-timeline-shape).
- **Hygiene:** headless profiles and stack copies filled the disk; delete each profile after its run.
