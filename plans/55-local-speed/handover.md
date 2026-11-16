# Handover — Local speed

[Plan](plan.md) · [Tasks](tasks.md) · [Inputs](inputs.md) · [Release 14](../../releases/14.md)

Written by the Release 14 release manager on 16 November 2026, about 21:00 UTC, from the branches, pull requests and CI results as they stood then. It is a dated snapshot for the manager who takes this plan next. The run's own records are on the astrid-dev branch `release/14/plan-55`: its `decisions.md` and `evidence/continuation-20261116/approved-implementation-followup.md` are newer than anything on `main`. The run `2026-11-15-local-speed` was still active when this was written.

## Where it stands

One of seventeen task rows is done (LS-11). The fast lane itself has not started: there is no design note, so nothing after it on the critical path can begin. A day of work went into measuring and into records. The measurements are useful, and one of them contradicts a target.

On the critical path, LS-1 → LS-3 → RS1 → LS-8 → LS-15 → LS-9 → LS-14 → R, the work is partway through the first step. The estimate of two to three days no longer holds.

## What has been measured

| What | Result | Read it as |
| --- | --- | --- |
| The floor: a script that only submits to a real ComfyUI on CPU and collects the result. Hosted runners, 20 samples a cell, one-megapixel image (run 43858887774) | Median overhead on Linux 41 ms in one cell and 179 ms in the other; on Windows 226 ms and 284 ms. Transport alone 5 ms. | The least Astrid could add. Not the installed Agent. The two Linux cells differ fourfold and the record does not say why. |
| Today's path through the meter, Linux, one sample (run 43918996289) | SDK 22.3 s, command line 16.8 s; 13 requests to ComfyUI; 3 emissions; 8 and 9 process starts | A baseline, on a 16-pixel image. The plan's inputs said one child process; the meter counted eight. |
| Today's path, Windows, one observation each (run 43942960060) | SDK 66.7 s, command line 32.2 s | Baseline samples, "not medians". The native counts have no result: converting the trace timed out. |
| A GPU machine, or a tester's Windows machine | Nothing | No spend. |

**The Windows floor is above the target.** D1 sets under 0.1 s for a connected caller on Windows, "confirmed by measurement", and the plan estimated 25 to 120 ms. A hosted Windows runner measured 226 to 284 ms for the floor alone. Either a real machine is much faster than a hosted runner, or the Windows target has to move. That is the owner's, and LS-3 has to say which.

## Task by task

| Task | State | What is proven |
| --- | --- | --- |
| LS-1 floor | Partly | CPU only, image only. No video, no native command line, no virus-scanner cell, no GPU. Recorded on draft astrid-dev #756, not on the plan branch. |
| LS-2 meter | Partly | Counts on Linux match the baseline; the budget is not certified; Windows pending. Drafts Agent #359 and #355. |
| LS-3 design | Not started | No `design.md` on any branch. |
| RS1 review | Not started | Waits for LS-3. |
| LS-4 prepared workflow | Not started | |
| LS-5 held connection | Partly | VibeComfy transport merged (#167, #169); Agent attempt custody merged (#352). The approved pin `7fde33e2` is on draft Agent #371 only. The Agent's held-connection code is not in any repository (below). |
| LS-6 output once | Partly | Agent #351 merged; its own description says duplicate hashing and the synchronous preview remain. |
| LS-7 Runtime hand-off | Not started | No Runtime plan branch exists. |
| LS-8 resident sessions | Not started | |
| LS-9 leaving the fast lane | Partly | Cancel by job only, 23 local cases (draft #355); its Windows check failed. Six of eight cases absent. |
| LS-10 thin callers | Not started | |
| LS-11 inputs by content | Done | Merged into the Agent plan branch. Its row in `tasks.md` is still empty. |
| LS-12 first job | Code, no proof | Draft Agent #361, no checks run. |
| LS-13 Windows | Partly | Hosted Windows only. No tester. |
| LS-14 live proof | No result | Needs paid GPU time. |
| LS-15 pack session | Not started | |
| R final review | Not started | |

## What exists but has not landed

- **Agent drafts into the plan branch:** #353, #355, #359, #361, #371. **Branches with no pull request:** `p55/windows-trace-decode-20261116` (nine commits), `p55/current-meter-diagnostic-20261116`, `p55/cpu-followthrough-20261116`, `p55/decision-record-check-20261116`.
- **Integration drafts:** Agent #358, VibeComfy #172, astrid-dev #753 (in conflict with `main`).
- **astrid-dev drafts into the plan branch:** #756, #729, #719.
- The Agent plan branch was cut from `9814193a` and is 548 commits behind `release/14/main`. It merges without conflict.

## At risk of being lost

- **The held-connection code for LS-5.** It passed 21 loopback cases and exists only in a chat workspace, `/mnt/data/plan55-owner-approved-eadow7h3`, whose local execution then failed. The record says not to rebuild it from a summary and call it the tested code. Recover those bytes and push them, or rewrite and re-prove.
- **Hosted artifacts** that hold the floor and meter results expire. The numbers above are in astrid-dev #756; land it.
- The manager lost the ability to run code locally during 16 November. Hosted CI and GitHub still worked, so later proof ran on hosted CI only.

## Waiting on the owner

- **The Windows target**, given the measured floor.
- **Paid GPU time** for the live floor and LS-14, and **a Windows tester** for LS-13. Neither holds LS-3: the record says "GPU cells do not hold unrelated implementation".
- **Runtime pins** for LS-7, when it has something to pin.

D10 to D13 (the VibeComfy pin, LS-6's scope, the Windows fixture repair, progress pull requests to `main`) are approved and recorded in `decisions.md`.

## For the next manager, in order

1. Read the [Manage skill](../../skills/astrid-dev-manage/SKILL.md), then `decisions.md` and the follow-up on the plan branch. You answer for this plan finishing.
2. Save what could be lost: the LS-5 code, and #756.
3. Make the record true. `tasks.md` shows seventeen empty rows and a "Now" block dated 15 November. D13 lets you merge a pull request to `main` that changes only that file.
4. Merge `release/14/main` into the Agent plan branch. Merge or close each draft: a draft that is right goes in, one that is superseded is closed with a line saying why.
5. **Write LS-3 now**, from the numbers in hand. It needs the fast-lane key, what ends the fast lane, the resident helper, the Runtime hand-off, and an answer on Windows. Then the one review round, RS1.
6. After RS1, LS-4, LS-7 and LS-8 at the same time, then LS-15, with LS-10 beside LS-9. Cut the Runtime plan branch for LS-7. LS-8 arrives as a module of its own beside the host ([Plan 13](../13-execution-host-refactor/plan.md#release-14-scope)).
7. Keep the meter to what the budget test needs: process starts, waits, requests, hash passes, forced writes. The native Windows trace work belongs with LS-13.
8. Four issues joined this plan on 16 November and sit on the same path: [#724](https://github.com/banodoco/astrid-dev/issues/724), [#583](https://github.com/banodoco/astrid-dev/issues/583), [#733](https://github.com/banodoco/astrid-dev/issues/733), [#610](https://github.com/banodoco/astrid-dev/issues/610).

## What this run taught

- **Measuring became the project.** The plan says measure first, then design. Nothing said when measuring was enough. It is enough when it can change the design; the floor and one baseline did that on the first day.
- **Everything stayed a draft.** Eleven pull requests are open, all drafts, so each new branch is built on unmerged work.
- **Approval was asked for what a manager decides.** Four requests went to the owner on 16 November. The Manage skill's "Decide" section lets a manager make most such calls and log the ruling.
- **Work lived outside the repositories.** A workspace failed and took tested code with it. Push a branch before proving anything on it.
- **The records disagree with each other.** `tasks.md`, `decisions.md`, the follow-up and the pull request descriptions give different states, heads and tester baselines. One progress record, on `main`.
