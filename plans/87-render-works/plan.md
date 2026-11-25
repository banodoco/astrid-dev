# The renderer works end to end

**Project:** The renderer works end to end

**Goal:** A heavy real timeline renders from first frame to last in one product render on a build of `release/15/main` with no local patches, and the file matches what the editor shows.

**Status:** active

**Owner:** Orchestrator session `session_011EzfW2YgL2GSmbJMr9r9SG`, hosting one manager

**Estimate:** Provisional, about 9 engineering days: 1 to port the sound fixes, 5 for the proper fixes, 2 for the render loop on the heavy timeline, 1 for the CI check. Re-estimate after the lease measurement and the first whole-fixture attempt.

**Waiting on:** Recorded core and staged follow-ups landed in Release 15; RN-0 and R still have open Progress rows. Reconcile their exact proof and the remaining rendering scope with the Lead against frozen-candidate qualification and the Release 16 handoff #1938.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog is generated.

**Vision role:** Foundational enabler — rendering is how finished work leaves Astrid. [Plan 27](../27-video-render-options/plan.md) keeps export choices; [Plan 88](../88-timeline-edits-land/plan.md) lands the timeline-editing fixes found in the same session; everything else found that day is an issue, listed in [inputs.md](inputs.md#moved-to-issues).

## Outcome and scope

We want one thing: the renderer works, proven on a heavy timeline, with the fixes in the proper code.

On 22 November 2026 a film project could not be rendered on a Release 14 test stack. Sixteen changes later it rendered, in four ranges joined outside the product. Seven of those changes are reviewed fixes; nine are stopgaps that prove what is needed but cannot ship as written. Every defect site is still present on today's `release/15/main` ([head check](evidence/eff/heads.md)).

**In scope**

1. Carry the six sound render changes onto `release/15/main`, resolving their conflicts once.
2. Write the remaining fixes properly, using the session's stopgaps as the description of what each has to achieve.
3. Render the heavy test timeline end to end, debugging what breaks. The owner named it: the generated heavy fixture built by the App's [`scripts/save-loop/build-fixture.mjs`](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/build-fixture.mjs) ([how to run it](https://github.com/banodoco/astrid-app/blob/release/15/plan-77/scripts/save-loop/README.md)), in both its standard and `large-shots` variants. A break in the render path is fixed here; anything else becomes an issue.
4. One real render check in CI, built on the test that already executes `rendering.render` against a real Runtime and pack host.

**Not in scope, and where it went**

- Timeline editing fixes (media swap on shot clips, moving word-anchored clips, the legacy overrun): [Plan 88](../88-timeline-edits-land/plan.md).
- Cancel, lease-loss recovery, the poisoned session slot, scratch left by failed renders, tasks stuck as active: [#1514](https://github.com/banodoco/astrid-dev/issues/1514) and the issues it links. During this plan a stuck stack is restarted.
- Render progress and failure visibility ([#1476](https://github.com/banodoco/astrid-dev/issues/1476)), resumable renders ([#1515](https://github.com/banodoco/astrid-dev/issues/1515)), the export hint ([#1477](https://github.com/banodoco/astrid-dev/issues/1477)), late range validation ([#1504](https://github.com/banodoco/astrid-dev/issues/1504)).
- Saving, agents editing together and write-path defects: Plans [77](../77-saving-holds-on-a-heavy-timeline/plan.md) and [76](../76-editing-together/plan.md) and their issues.
- Editor preview defects, generation gaps, Windows, render speed.
- Release 14. It was published on 22 November and takes changes only through its Lead ([landscape](evidence/eff/landscape.md)).

The full list of what was moved, with issue numbers, is in [inputs.md](inputs.md#moved-to-issues).

## Existing work and decision

**What exists.** Two branches in astrid-agent, both cut from `83d5f8fe`, a commit already contained in `release/15/main` ([inventory](evidence/eff/inventory.md)):

- [`release/14/r6-fixes`](https://github.com/banodoco/astrid-agent/tree/release/14/r6-fixes) (draft [PR #530](https://github.com/banodoco/astrid-agent/pull/530)): seven commits, reviewed twice ([code review](evidence/review/ASTRA-530.md), [verdicts](evidence/shipplan/VERDICTS.md)).
- [`release/14/r6-render-stopgaps`](https://github.com/banodoco/astrid-agent/tree/release/14/r6-render-stopgaps): nine more commits, each marked `STOPGAP (do not merge)`. The render that finished ran on these.

Nothing else on the test stack's branches is missing from Release 15: the stack's Agent, App and Runtime lines are all fully contained in it. So "what we did" is these sixteen commits.

**Why rendering had never worked.** Each layer failed and hid the next: asset admission, worker environment check, bundler resolution, composition, lease, process custody. No test ran the real path with a collection-pack element through a command worker, so nothing caught any of it ([root-cause picture](evidence/shipplan/PLAN.md)).

**The decision: port what is sound, write the rest properly, and render at every step.** The earlier draft ordered the work as separately designed fixes, each with its own new tests, across two release lines. We chose a shorter route:

1. Cherry-pick the six sound render changes onto a plan branch cut from `release/15/main`. The two conflicting files are known (`generic_host.py`, `remotion_runtime.py`) and are resolved once.
2. Carry the lease and custody stopgaps as two tracked experiments, because nothing long can render without them and their proper fixes need measurement first.
3. Write the pack-root, pack-revision and animation fixes directly. Their stopgaps are not ported: porting code that is about to be replaced costs a second conflict resolution, and a render that depends on an override or a suppressed error is not a trustworthy reference.
4. After each fix, run a short real render. Render the film-shaped fixture variant (621 clips at the film's scale; see Decisions in tasks.md) whole at three milestones. Compare with the editor, never with an earlier render.
5. Nothing merges to `release/15/main` while an experiment remains.

A first version of this plan ported all sixteen commits before fixing anything. A second opinion showed that sixteen cherry-picks would not reproduce the session's stack anyway (the animation patch lived outside the repository and the pack override needed a machine-local setting), so we changed it ([opinion](evidence/astra-plans/OPINION.md), [what we took and left](inputs.md#second-opinion)).

**The sixteen changes and what happens to each**

| Change | Commit | In this plan |
| --- | --- | --- |
| Drop the editor's own-object route before the managed render check | `7bf7d908` | Keep, add tests (RN-2) |
| Thumbnail metadata and redundant locators projected out | `cb90a4b9` | Keep, add tests (RN-2) |
| Mismatch error names the differing fields | `7332e03d` | Keep, show values for path fields (RN-3) |
| Launch validation matches worker contexts | `0f6aea92` | Keep, fold into one environment builder (RN-3) |
| Command workers use the command readiness rule | `f4f5a321` stopgap | Ported with the four above; correct as written (RN-3) |
| Empty pack path equals unset | `f84c80be` stopgap | Ported with the four above; correct as written (RN-3) |
| Worker pack roots; bundler roots via parent mapping; relative shared-import alias | `90380578`, `fa3b6df1`, `54e605c6` stopgaps | Not ported. One proper fix (RN-4) |
| Render uses the App-vendored motion pack | `007c40d3` stopgap | Not ported. One pinned revision for preview and render (RN-5) |
| Fade with an easing no longer fails the render | `221e5003` stopgap | Not ported. The `fade` element declares its easing support (RN-6) |
| Two-hour lease requested on every heartbeat | `b051e8cc` stopgap | Carried as a tracked experiment; replaced after the cause is measured (RN-7, RN-8) |
| Wait before the custody retry | `7265aa5d` stopgap | Carried as a tracked experiment; replaced by a bounded retry that keeps every custody check (RN-9) |
| Media swap on shot clips; word-provenance exemption; legacy overrun | `24740fdf`, `d4bf28e4`, `ad10ff6d` | Not render fixes and not on this branch. [Plan 88](../88-timeline-edits-land/plan.md) lands them |

**Judgement calls made in this reshaping** are recorded with their reasons in [inputs.md](inputs.md#judgement-calls).

## Sequence and readiness

**Branch.** `release/15/plan-87` in astrid-agent, cut from the `release/15/main` head on the day; the same name in astrid-runtime and astrid-app only if a task changes them. It lands on `release/15/main` through the Release 15 Lead.

**Phase 1: a render on Release 15 (RN-0, RN-1).** Stand up a source-launched stack and an installed-profile stack on the plan branch, and record the exact versions of everything in them. Record the first failing stage on the unmodified head. Write the reset procedure for a stack left stuck by a failed render. Then port the six sound changes.

**Phase 2: proper fixes (RN-2 to RN-9).** In the order of the table in [tasks.md](tasks.md). RN-3 and RN-4 are the critical path. RN-7 and the short contract render (RN-11) start on day 1.

**Phase 3: the heavy timeline (RN-10).** The loop:

1. Build the heavy fixture in the plan stack with the App's save-loop builder: the standard variant (616 parent clips, 46 shot occurrences, a 2.6 MB document) and then `large-shots` (three 480-second shots of 32 child clips each, on 90-second generated video and audio sources). It needs no owner media and no GPU. Render a short range from the densest part, then the whole timeline in one render.
2. On failure, read the first real error. If the cause is in the render path (admission, worker launch, bundling, composition, lease, custody, encode, output), fix it on the plan branch with a focused test and render again.
3. If the cause is elsewhere, file or update an issue, note the workaround, and continue.
4. On completion, compare frames against the editor at chosen times and check the audio. A mismatch is a failure.
5. Stop when one render of each variant completes and matches, twice in a row, with no stopgap on the branch. The heavy fixture proves scale and long duration; the film-shaped fixture variant proves custom elements, word-anchored and shot-owned clips at the film's scale. Both must pass. No proof depends on the owner's own film.

**Phase 4: keep it working (RN-11).** Extend the existing real-render integration test and run it in the lane that already installs Remotion and a browser.

**Decisions:** none open. P1 to P3 were taken on 23 November 2026.

**Risks**

- The heartbeat renewal stop has no known cause. RN-7 may not find it quickly. P3 covers that case.
- Inputs and outputs are read whole into memory, and an attempt has a one-hour default deadline. The heavy fixture may meet both; RN-10 measures them on every run.
- A failed render can leave the stack refusing work. RN-0's reset procedure is the only recovery this plan provides; if resets start to dominate the loop, the smallest missing clean-up comes back in from [#1514](https://github.com/banodoco/astrid-dev/issues/1514).
- `generic_host.py` is large and changed on Release 15; RN-1 and RN-3 conflict there. Keep RN-3 to the builder and its callers.
- The standard and large-shots variants are far larger than the film-shaped variant (616 clips and 480-second shots against 621 clips at the film's 3 minutes 16 seconds). Phase 3 has no fixed end; the estimate assumes two days.
- The fixture builder asks for 25 GiB of free disk and stops below 15 GiB. The session's Mac had under 10. Phase 3 needs a machine with room.
- The motion pack's install pin is also an open decision in [Plan 78](../78-live-custom-element-editing/plan.md). P2 settles it for rendering; Plan 78's manager should be told before RN-5 starts.

## Interfaces and handoff

**Consumes:** `release/15/main` heads of astrid-agent, astrid-runtime and astrid-app at cut time; the Runtime pin; the motion pack revision vendored by the App; the two donor branches above; the App's save-loop fixture builder (on `release/15/plan-77` at filing; use the copy on `release/15/main` or `main` if it has landed by then).

**Produces:** one function that builds a worker's environment for both launch validation and dispatch; one source of pack roots for the bundler; one motion pack revision for preview and render; a Runtime log line for slow requests and a host log line for each failed heartbeat; a real render check in CI.

**Handoff:** the plan branch with its render receipts, the frame comparison, and the list of issues filed during the loop. Plan 88 starts from this branch's stack.

## Completion

- The heavy fixture, standard and `large-shots`, renders whole, in one product render each, twice in a row, through to the Runtime's completion receipt and a registered output, on a build of the plan branch with no experiment commit and no local patch.
- Sampled frames match the editor and the audio matches the timeline.
- The film-shaped fixture variant renders whole in one render on the same build, on the source stack and the installed stack.
- The CI render check is green on the plan branch and fails when any one of RN-2 to RN-6 is reverted.
- After the branch lands, the same three renders complete on a build of `release/15/main` (RN-12). Only then is the goal met.
- Every defect met during the loop that was not fixed here has an issue.
- Limits: one machine class, macOS and Linux; Windows and render speed are not covered.
