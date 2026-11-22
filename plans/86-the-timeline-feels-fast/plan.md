# The timeline feels fast

**Project:** The timeline feels fast

**Goal:** On a heavy timeline in the compiled editor, the things a person does every minute (open, scrub, play, drag, save) each meet a stated time, shown by a measurement anyone can repeat, and the costs that measurement ranks highest are fixed.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 6 engineering days for the measuring half. The fixing half is written and estimated from what the measuring finds; an allowance of 10 to 15 days.

**Waiting on:** [Plan 85](../85-one-place-to-measure/plan.md) for the method and the shape of a result; the heavy project from [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md); the owner's decision D1 in [inputs.md](inputs.md#owner-decisions); a release.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary): a person edits by feel, and an editor that takes seconds to show a frame or minutes to settle breaks that long before anything fails. F-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Two plans already cover part of timeline speed. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), in Release 15, is about a heavy timeline opening and ordinary edits saving. [Plan 75](../75-fast-saving/plan.md), in no release, is about the Runtime accepting an edit in 300 ms. Neither looks at what a person feels between saves: moving the playhead, playing, dragging, zooming. This plan measures all of it as one set of scenarios, then fixes what the measurement puts first.

**The scenarios** (each gets an exact start and stop in TF-1):

| A person | What is timed |
| --- | --- |
| opens a project | until it can be used, and until the editor is actually quiet |
| moves the playhead to an arbitrary point | until the right frame is shown, the first time and again |
| presses play | the delay before it starts; frames dropped over ten seconds; sound and picture staying together across a cut |
| drags a clip | how smooth the drag is; the time until it says Saved |
| zooms or scrolls the timeline | how smooth it is |
| adds a file | until it appears; until its thumbnail and waveform show |
| undoes and redoes | until it takes effect |
| starts an export | until the first frame; frames per second |
| leaves the editor open for ten minutes of editing | whether memory keeps growing |

**Measured as [Plan 85](../85-one-place-to-measure/plan.md)'s method says:** the compiled editor on current code, a quiet machine, the heavy project built once and restored, a one-clip project beside it as the control, the time split between the Runtime and the browser, results in the shared shape.

**Two halves.** First measure, on a harness made fit for it. Then the owner sets the times (D1) from real numbers, and the fixing tasks are written from the ranking, as [Plan 13](../13-execution-host-refactor/plan.md) did with its re-estimate. No fix is chosen before the measurement.

**Not included:** what Plan 77 and Plan 75 already own (the save holding on a heavy timeline; the Runtime's acceptance time), which are scenarios here only so that their numbers sit in the same table; generation speed; export quality; anything on a GPU.

## Existing work and decision

- **The harness exists and found real things:** the App's `scripts/save-loop/` separates Runtime time from browser time, records each request and where a clip is on screen. Pointed at one edit it located a refusal in a single run.
- **Its four weaknesses cost Plan 77 a day,** and are this plan's first task: it rebuilds the project every run by design; it runs as one long sweep, so an early failure loses the rest; it defaults to the development server; it has no way to run one scenario alone.
- **What is already known on a 300-clip project, compiled, on the older save path** (22 November 2026; to be re-taken on current code by Plan 77): opening about 23 s with about 20 s of it Runtime processing; the background history load 344 s before the Runtime is quiet; a one-clip edit saved in about a second.
- **Nothing is known** about scrubbing, playback, drag smoothness, zooming, adding a file, undo or export start on a heavy timeline. Nobody has measured them.

## Sequence and readiness

1. **TF-0,** the harness made fit: restore, one scenario at a time, the compiled editor, independent results.
2. **TF-1,** the scenarios written and built.
3. **TF-2,** the first measurement.
4. **TF-3,** the ranking, the owner's times, and the fixing tasks written.
5. **TF-4 onward,** the fixes, in ranked order.
6. **TF-9,** measured again, and held.
7. **R,** one review round.

**Real dependencies:** Plan 85's method and result shape (TF-0 can start on the method alone); the heavy project and its backup; Plan 77's re-measurement on current code, so the two plans do not measure the same thing twice. **Unresolved:** D1, a release. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 85's method, runner and result shape; the heavy project; Plan 77's and Plan 75's findings. **Produces:** the scenarios as part of the App's harness; rows in the shared results table; fixes in whichever of the App, Agent and Runtime the ranking points at. **Compatibility:** the measuring half changes only the App's harness, not the product.

## Completion

- **Each scenario has a number** on the heavy project and on the one-clip control, on the compiled editor and current code, taken five times, with the Runtime's and the browser's share, in the shared table.
- **The owner has set a time for each,** and the table says which are met.
- **The costs ranked highest are fixed,** each shown by the same scenario before and after.
- **Held:** the scenarios are in the release comparison, so a release that makes one slower shows it.
- **Limits of the proof:** a headless browser on a CPU machine stands in for a person's computer, and says so; smoothness figures there are comparisons between builds, not promises about any one machine. Landing remains the owner's.
