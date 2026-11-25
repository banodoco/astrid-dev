# The timeline feels fast

**Project:** The timeline feels fast

**Goal:** On a heavy timeline in the compiled editor, the things a person does every minute (open, scrub, play, drag, save) each meet a stated time, shown by a measurement anyone can repeat, and the costs that measurement ranks highest are fixed.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 6 engineering days for the measuring half, starting with moving the playhead. The fixing half is written and estimated only once the measurement has ranked the costs; no figure is set for it in advance.

**Waiting on:** [Plan 85](../85-one-place-to-measure/plan.md) for the method and the shape of a result; the heavy project from [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md); the owner's decision D1 in [inputs.md](inputs.md#owner-decisions); a release.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary): a person edits by feel, and an editor that takes seconds to show a frame or minutes to settle breaks that long before anything fails. F-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Two plans already cover part of timeline speed. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), in Release 15, is about a heavy timeline opening and ordinary edits saving. [Plan 75](../75-fast-saving/plan.md), in no release, is about the Runtime accepting an edit in 300 ms. Neither looks at what a person feels between saves: moving the playhead, playing, dragging, zooming. This plan measures it, starting with the owner's own example (move the playhead to an arbitrary point: how long until the picture shows), then fixes what the measurement puts first.

**It starts from what already exists.** The App has an editor benchmark (`npm run perf:editor`) that was run on a real 286-clip film in October 2026 and already probes idle cost, playback and scrubbing, and a test that checks the frame shown after a seek against a reference picture. Plan 77's harness already has the gestures for moving a clip, dropping a file and undoing. This plan reuses all three; it does not build a fourth harness.

**The scenarios** (each gets an exact start and stop in TF-1):

| A person | What is timed |
| --- | --- |
| opens a project | until it can be used, and until the editor is actually quiet |
| moves the playhead to an arbitrary point | until the right frame is shown, the first time and again |
| presses play | the delay before it starts; how often playback holds over ten seconds; the offset between sound and picture events across a cut |
| drags a clip | how many times the editor redraws and how long each takes; the time until it says Saved, which is Plan 77's and is listed here from its result |
| zooms or scrolls the timeline | how smooth it is |
| adds a file | until it appears; until its thumbnail and waveform show |
| undoes and redoes | until it takes effect |
| starts an export | until the first frame; frames per second, for the renderer, codec and machine tested |
| leaves the editor open for ten minutes of editing | whether memory keeps growing |

**Measured as [Plan 85](../85-one-place-to-measure/plan.md)'s method says:** the compiled editor on current code, a quiet machine, the heavy project built once and restored, a small project beside it as the control, each result listed with its setting. Elapsed time and processor time are kept as separate clocks: on 22 November 2026 an opening took 23.0 s of elapsed time during which the Runtime used 19.9 s and the browser 6.3 s of processor time, overlapping, so shares of one do not add up to the other.

**What a headless browser can and cannot tell us.** Time to a frame, counts of redraws and requests, playback holds and the timing of sound and picture events can be measured there, and compared between two builds. How smooth playback or a drag feels, and whether sound is audibly in step, cannot: those need a person's kind of computer, and the plan says so where it reports a stand-in figure.

**Two halves.** First measure, on a harness made fit for it. Then the owner sets the times (D1) from real numbers, and the fixing tasks are written from the ranking, as [Plan 13](../13-execution-host-refactor/plan.md) did with its re-estimate. No fix is chosen before the measurement.

**Not included:** what Plan 77 and Plan 75 already own (the save holding on a heavy timeline; the Runtime's acceptance time), which are scenarios here only so that their numbers sit in the same table; generation speed; export quality; anything on a GPU.

## Existing work and decision

- **The harness exists and found real things:** the App's `scripts/save-loop/` separates Runtime time from browser time, records each request and where a clip is on screen. Pointed at one edit it located a refusal in a single run.
- **What it lacks is known, and mostly Plan 77's to add:** it rebuilds the project every run by design, it defaults to the development server, and it has no way to run one scenario alone (the sweep does keep the rows it finished, and stops when a clean-up fails). Restoring a saved project and opening the compiled editor are part of Plan 77's own remaining work (its SL-7); this plan takes them from there and adds only what is still missing. Its manager's account is in [evidence/what-the-harness-needs.md](evidence/what-the-harness-needs.md).
- **What is already known on a 300-clip project, compiled, on the older save path** (22 November 2026; to be re-taken on current code by Plan 77): opening about 23 s with about 20 s of it Runtime processing; the background history load 344 s before the Runtime is quiet; a one-clip edit saved in about a second.
- **Something is known about scrubbing and playback, from October 2026:** on the 286-clip film, on warm development builds, playback ran at between 0.46 and 0.998 of real time on the same build under different load, and 373 moves of the ruler caused 802 redraws of the editor (App `docs/quality/editor-efficiency-2026-10.md`). That was a development build and a different measure, so it is a pointer, not a baseline. The benchmark's comparison script also counts playback holds wrongly (it counts the entries of an object, so none and ten can look the same), which TF-0 fixes before any ranking leans on it.
- **Nothing is known** on a compiled build and a heavy project about time to a frame after a seek, redraws during a drag, zooming, adding a file, or the start of an export.

## Sequence and readiness

1. **TF-0,** what exists made usable: the editor benchmark's counting fault fixed, and one scenario runnable alone on a restored project and the compiled editor, taking Plan 77's work for the latter.
2. **TF-1,** moving the playhead: time to the right frame, first and repeated, on the heavy project.
3. **TF-2,** the other scenarios, each as a real measure or a named stand-in.
4. **TF-3,** the first measurement of all of them.
5. **TF-4,** the evidence put to the owner, her times, and the fixing tasks written and estimated.
6. **The fixes,** as TF-4 writes them.
7. **TF-5,** measured again.
8. **R,** one review round.

**Real dependencies:** Plan 85's method; Plan 77's restore and compiled-opening work and its re-measurement on current code, so the two plans do not build or measure the same thing twice; the heavy project and its backup (a 300-clip one restores today; the 616-clip one is being built once). **Unresolved:** D1, a release. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** Plan 85's method, runner and result shape; the heavy project; Plan 77's and Plan 75's findings. **Produces:** the scenarios as part of the App's harness; rows in the shared results table; fixes in whichever of the App, Agent and Runtime the ranking points at. **Compatibility:** the measuring half changes only the App's harness, not the product.

## Completion

- **Each scenario has a result** on the heavy project and on a small control, on the compiled editor and current code, taken five times, with elapsed time and the Runtime's and the browser's processor time kept separately; where only a stand-in can be measured, the result says what it stands in for.
- **The owner has set a time for each,** and the table says which are met.
- **The costs ranked highest are fixed,** each shown by the same scenario before and after.
- **Kept:** the scenarios and their results are listed in [Plan 85](../85-one-place-to-measure/plan.md)'s home, so the next measurement starts from them.
- **Limits of the proof:** a headless browser on a CPU machine stands in for a person's computer, and says so; smoothness figures there are comparisons between builds, not promises about any one machine. Landing remains the owner's.
