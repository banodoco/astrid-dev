# Handover — Saving holds on a heavy timeline

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Rounds](rounds.md)

Written on 18 November 2026 for whoever runs this plan next, on another machine. It is a dated snapshot: re-read branch heads with `git ls-remote` before acting. Claim sources: **verified** means read from a file or command on 18 November; **reported** means an earlier agent said so and nothing re-checked it.

## First actions on a new machine

1. **Clone the repositories** (all under `banodoco` on GitHub): `astrid-dev`, `astrid-app`, `astrid-agent`, `astrid-runtime`. Free disk first: 25 GB (a stack is about 10 GB by the release script's README, on top of the 15 GB floor), and never below 15 GB during a run (the disk filled twice on 18 November from headless browser profiles and stack copies). Delete the old stack root before each rebuild; the fixture is rebuilt, so no data copy is kept. Needs Node 20, ffmpeg and Playwright. The release script needs macOS and a live install (APFS clones and launchd); any other machine uses the direct route in [SL-1](tasks.md).
2. **Check out the branches** (all on origin, cut from `release/14/plan-59`): `release/14/plan-77` in each of astrid-app, astrid-agent and astrid-runtime, and astrid-dev `main` (this pack). **Check first with `git ls-remote`:** on 21 November only the Runtime had the `plan-77` names; the App and Agent still had `release/14/plan-66` and `release/14/plan-66-wip/...`. The owner asked for this rename on 21 November: if it is not done, push the same commits under the new names if you can, or stop and ask: a stack built from a missing branch name silently falls back to `release/14/main`. One worktree per branch; keep the main clones clean. Record your session id in the `Owner` line of [plan.md](plan.md) ([authority](inputs.md#planning-evidence)).
3. **Create `run.yaml`** ([below](#runyaml)).
4. **Build the stack** (SL-1, [below](#build-the-stack)).
5. **Build the fixture** (SL-0) on that stack: `scripts/save-loop/build-fixture.*` in astrid-app, not written yet.
6. **Run round 1** once SL-2 has retargeted the harness, then keep looping ([a round, step by step](#a-round-step-by-step)). SL-3 (recover the lost work) runs beside these and does not block round 1.

Checks for every astrid-dev PR here: `python3 scripts/astrid_dev.py check` and `python3 -m unittest discover -s scripts -p "test_*.py"` (Python 3.10 or later). For a PR add `--base <base commit> --body-file /dev/null` to the check.

## run.yaml

`.otto/` is gitignored, so create the run's `run.yaml` on the new machine from [`skills/shared/templates/run.yaml`](../../skills/shared/templates/run.yaml), under `plans/77-saving-holds-on-a-heavy-timeline/.otto/runs/<run-id>/`.

**Bindings.** These follow the [run contract's routing table](../../skills/shared/run-contract.md#routing-and-bindings) (`N` Luna, `X` Terra, `S` Sol, `T` Astra; reviews, plan judgment and advice on Astra) with the newest IDs a ChatGPT-login Codex accepted on 21 November 2026, each answering a one-line `codex exec` with that effort. Fill them in as below; if the owner gives other bindings, theirs win. Before dispatch, re-check each with `codex exec -m <id> -c model_reasoning_effort='"<effort>"' --skip-git-repo-check -s read-only "Reply with just OK." < /dev/null`, and set `availability: verified` only for those that answer. Refused on that login: `gpt-6.2-luna`, `gpt-6.1-luna`, `gpt-6.2-terra`, `gpt-6-terra`, `gpt-6.1-astra`.

```yaml
models:
  normal:              {class: Luna/Haiku-class,      model_id: gpt-6-luna,    reasoning_effort: medium}
  very_hard:           {class: Terra/Sonnet-class,    model_id: gpt-6.1-terra, reasoning_effort: high}
  super_hard:          {class: Sol/Opus-class,        model_id: gpt-6.2-sol,   reasoning_effort: high}
  taste:               {class: Astra/Opus-class,      model_id: gpt-6.2-astra, reasoning_effort: medium}
  plan_judgment:       {class: Astra/Opus/Fable-class, model_id: gpt-6.2-astra, reasoning_effort: high}
  advisor:             {class: Astra/Opus/Fable-class, model_id: gpt-6.2-astra, reasoning_effort: high}
  completion_reviewer: {class: Astra/Opus/Fable-class, model_id: gpt-6.2-astra, reasoning_effort: high}
```

**If Codex is unavailable** (on the first machine its usage limit was exhausted until 20 November 00:00), run the same routes on the Claude families in the routing table (`N` Haiku, `X` Sonnet, `S` Opus; judgment on Opus or Fable, newest of each), record `--override`, and carry on. Do not wait.

### Who runs what

| Work | Runs on | Notes |
| --- | --- | --- |
| The coordinator (this plan's manager) | the session the plan is handed to | Keeps every judgment: picks fixes, checks each result against its diff and proof, writes `rounds.md`, merges into the plan branches. Never delegates a decision down. Best on a high-judgment model. |
| SL-0 fixture, SL-1 stack, SL-3a and SL-3b recovery | `N` | One worktree each, background `codex exec -s workspace-write` (command in the [workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#roles)). |
| SL-2 harness, SL-3c validation trim | `X` | Writes its `N` split first and runs the helpers in parallel, then merges their work ([tasks](tasks.md)). |
| A round's fix | `N` by default; `X` when the cause is coupled or unclear | The coordinator tags it when picking. |
| The strategist, once per round | `advisor`, read-only | Gets the round tables, not the coordinator's conclusion; asked what to remove first. Evidence, not a verdict. |
| R, the final review | `completion_reviewer` | Up to five rounds after the loop stops. |
| Fact-finding for anyone (status, logs, diffs) | `N` | Never gives a verdict. |

**Moving up a tier** follows the contract's [cheapest model first](../../skills/shared/run-contract.md#cheapest-model-first): move `N` to `X` after two misses or 20 minutes without progress, or when the work is wrong in a way a better brief would not fix, and `X` to `S` on the same test; pass the previous attempt's diff, output and best guess up; drop back to `N` once the cause is known. A worker stops after three attempts or 45 minutes on one failure and hands back what it has.

## How to work

- The coordinator keeps the judgment and delegates the doing.
- Scenarios only ever use the sandbox fixture, never the owner's timelines.
- No arbitrary time limits in tests; only a hang fails.
- Treat the advisor's advice as evidence, and ask it what to remove first.
- After a Runtime fix, regenerate the Agent's Runtime pins (`scripts/regenerate_runtime_pins.py` in astrid-agent) before rebuilding the stack.
- Tag claims as verified or reported.

## A round, step by step

The [live-loop workstream](../../skills/roles/astrid-dev-manage/workstreams/live-loop.md#the-round) is the rule; this is the order on the machine.

1. **Disk:** `df -h`; stop below 15 GB. Delete leftover browser profiles.
2. **Stack:** if the last round merged an Agent or Runtime fix (after a Runtime fix, regenerate the Agent's pins first), delete the stack root and install fresh by SL-1's route; if it merged only App fixes, check out the new App head and restart the editor. Confirm the stack's App and Agent commits are the plan branch heads.
3. **Fixture:** run SL-0's `build-fixture` script; it writes the manifest the harness reads.
4. **Matrix:** run SL-2's harness against the editor port; it prints the round table and writes one JSON row per scenario run.
5. **Record:** add the round's section to [rounds.md](rounds.md) (versions, the table, timings split into editor wait, commit and badge) and its one line under the loop card in [tasks.md](tasks.md).
6. **Strategist:** give the advisor binding the new round and the earlier ones, read-only (`codex exec ... -s read-only`, command in the workstream), and ask what to remove first. Paste its advice into the round as evidence.
7. **Pick and fix:** the coordinator picks the smallest fixes (one failing scenario, one cause, one change) and dispatches each as `N` or `X` in its own worktree; each lands as a PR into `release/14/plan-77` with the failed scenario as its red test. Write the round's plan deltas for Plans 63, 75, 76 and 18.
8. **Stop or repeat:** check the stop rules on the [loop card](tasks.md); otherwise go to step 1.

## Where everything is

- **This pack:** astrid-dev `main`, `plans/77-saving-holds-on-a-heavy-timeline/`. Evidence copies (the originals were in a folder not under git): [evidence/](evidence/). Start with `handover-facts-20261118.md`, then `sonnet-commit-profile-r14.md`, `fable-final-recommendations.md`, `fable-commit-proof-fit.md`, `fable-end-state-review.md` and `QUEUE.md`.
- **Seeded harness:** astrid-app `release/14/plan-77`, `scripts/save-loop/` (`sweep.mjs`, `lib.mjs`, `sweep.b64`; head `36d2b8258`). Read its header for the flags and `SAVE_LOOP_*` environment variables. It starts its own headless Chrome on a random port from 9300 with a fresh profile, deleted on close (checked 21 November in `lib.mjs`; 9540 in the crash log was one such port). It defaults to the owner's `clip-2` and `music-song` at a 1700 by 1500 viewport; SL-2 retargets it. Row ids and pixel coordinates are hard-coded, and its timer cannot judge 2 s (see SL-2). The profiler helpers `prof_run.py` and `wall_run.py` were not found on disk; `scripts/perf/measure-editor.mjs` already exists in astrid-app.
- **Crash work, pushed as wip branches** (verified by GitHub compare on 18 November):

| Repository | Branch under `release/14/plan-77-wip/` | Head | Base | What it holds |
| --- | --- | --- | --- | --- |
| astrid-app | `wt-app-concurrent-drops-registry` | `2402b1d97` | `2ffc0a300` (plan-59 tip, the plan-77 cut), 1 commit | concurrent drops refusing each other (`timelineLocalSaveHandoff(.test).ts`, `useAssetManagement.ts`, `useTimelineCommit.ts`) |
| astrid-agent | `wt-r14-validate-trim` | `2bb8c1095` | `ec758a9b8`, 1 commit | the speed trim of `validate_final_candidate`, barely started, with a golden test |
| astrid-runtime | `wt-rt-media-digest` | `a3acdc5fc` | `ee235d39d`, 1 commit | the media digest diagnostic log |
| astrid-agent | `wt-r14-agentbase` | `ed0c6c6e4` | `ec758a9b8`, 1 commit | its only changed file on 18 November was the same golden test (reported inventory); check before ignoring it |
| astrid-app | `wt-shot-trim` | `11ee51c1e` | `4eb6fb3`, 7 ahead, 74 behind plan-77 | a separate shot-trim task: **out of scope, only listed** |
| astrid-agent | `agent-src-main-clone` | `15ca752d1` | `f9642bd`, 6 ahead, 68 behind | same shot-trim task, out of scope |
| astrid-runtime | `runtime-src-main-clone` | `1b3f36083` | `519b404`, 2 ahead, 16 behind | same shot-trim task, out of scope |

  **Already contained in `release/14/plan-77`** (GitHub compare, ahead 0): App `release/14/same-file-drop`, App `release/14/quick-edits`, Agent `release/14/runtime-pin-r14b`. Merged into plan-59 before the cut (reported): Runtime #66, #67; App #308, #309.
- **Release 14 stack run on 18 November:** under `~/astrid-release/release-14-plan-59` on the first machine; stopped. It holds a copy of the owner's data and is not part of this plan.

## Build the stack

**Where the script is (checked 21 November):** `scripts/astrid-release/` reached astrid-app `release/14/main` with Plan 61 on 20 November (App #320) but is not on `release/14/plan-77`, which was cut from plan-59 before it. Run it from a `release/14/main` checkout (it clones the branches it builds by name). The real route is `scripts/astrid-release/astrid-release release/14/plan-77` in astrid-app (it also has `status`, `stop` and `update <branch>`). It builds an isolated root under `~/astrid-release/release-14-plan-77` (the branch name with `/` as `-`), refuses the live ports (17340, 2222, 17336, 17391) and never writes the live install. **Known limit (read, not run):** it is macOS-only and stops at its start when the machine has no live install, so on any other machine SL-1 runs the steps it wraps by hand (the direct route in [SL-1](tasks.md)) and leaves the script alone; `release/14/main` then need not be merged into the plan branch. Ports and the editor URL are in SL-1 and SL-1 records the real ones here. The Runtime in a stack is the one the Agent's `runtime.lock.json` pins. Moving a built stack to newer commits is not supported without losing data (issue #825): to test new commits stop it, keep `data/`, delete the root and run it again.

## Known broken or open

- **Sweep:** the 14 kinds are the scenarios that completed on the loaded timeline: 3 saved (a move, its undo, a cross-track move), 11 refused. Ten more rows failed with ROWERR (12 ROWERR lines in the log). Clip edits show "Local edits preceded the original verified read; draft retained"; audio edits show "The save has not been confirmed. Your changes are kept." Both with Try again and Discard. The run ended with "Target page, context or browser has been closed" after `connectOverCDP ECONNREFUSED 127.0.0.1:9540`, not a disk error; the disk was nearly full at the time (reported). It needs a rerun. The Library drag ended "Not saved" with the same first message (reported).
- **Drops:** "conflict: selected media catalog digest changed" on repeated drags (not reproduced; the likely trigger is dragging one library item several times); a failed drop deletes its placeholder (`external-drop-utils.ts:531`); three quick drops refuse each other ("would alter more than the asset you picked"); a same-file double drop is refused.
- **Speed (the profile's own numbers):** a commit on the heavy timeline was 3.74 s median, 0.22 s on one clip, as a warm commit median through the Runtime from the CLI, not editor time to Saved. `validate_final_candidate` is about 59% of it; the legacy-declaration pass inside is about 57%; skipping validation saves about 56% (2.11 s), leaving 1.63 s. The pass that runs twice runs on the candidate and on the baseline, so it is not a plain duplicate. Target here about 2 s to Saved in the editor, which has not been measured; 300 ms is Plan 75's.
- **Other open items on the crash day** (reported, in [QUEUE.md](evidence/QUEUE.md)): a recovered draft from an old realm loops on Try again with a "Saved" badge; Discard left 37 old-realm outbox rows; an 11 s "Dirty" delay before the first send; the `direct-journey` check fails on plan-59 PRs, suspected pin skew.
- **Fixture discrepancy:** the copied timeline has 8 clips and 140 KB, while the profile says 616 clips and 2.6 MB. The profile names "Almost Ready (trial v2)", so the copy probably read a different timeline. The fixture targets the profile; see [inputs](inputs.md#heavy-timeline-shape).
- **Hygiene:** headless profiles and stack copies filled the disk; delete each profile after its run.
