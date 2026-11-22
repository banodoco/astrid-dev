# Inputs — The timeline feels fast

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — The owner asked on 22 November 2026 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): "is there other stuff we should check on the timeline? For example, like imagine if you just scrub to an arbitrary part of the thing and how long it takes the image to show and stuff like that", and then: "let's create another plan for the more kind of robust ... timeline speed stuff". She has not chosen its release.

**Prior art:** Read on astrid-dev `main` at [`3db0fc91`](https://github.com/banodoco/astrid-dev/tree/3db0fc91) and astrid-app `release/15/main` at `e3dbad64`.

- **No plan covers what happens between saves.** [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) (active, Release 15) covers opening and saving on a heavy timeline; [Plan 75](../75-fast-saving/plan.md) (queued, no release) covers the Runtime's acceptance time; [Plan 18](../18-timeline-editing/plan.md) is about what an edit means, not how fast it is. Scrubbing, playback, drag smoothness, zooming, adding a file, undo and export start are in none of them.
- **The harness:** astrid-app `scripts/save-loop/`, with its README. What it lacks, confirmed by Plan 77's manager on 22 November 2026: the project is rebuilt every run by design; the development server by default; no single-scenario run ([evidence](evidence/what-the-harness-needs.md)).
- **The editor benchmark:** astrid-app `scripts/perf/measure-editor.mjs` and `compare-editor-measure.mjs`, `npm run perf:editor`, with October 2026's results in `docs/quality/editor-efficiency-2026-10.md`: a real 286-clip film on warm development builds; playback between 0.46 and 0.998 of real time on one build under different load; 802 redraws across 373 moves of the ruler. Its comparison counts the entries of the holds object, not the holds (`compare-editor-measure.mjs` near 32).
- **A test that already checks the frame after a seek:** astrid-app `tests/e2e/timeline/preview-scrub-evidence.spec.ts`, cold and repeated, against reference pictures.
- **What Plan 77 measured that day,** on a restored 300-clip project and the compiled editor, on a build that predates Release 14's save work: opening 22.994 s, 19.89 s of it Runtime processing and 6.26 s the browser's; several history and object reads of about 17.8 s each; the deferred history taking 344 s to install; a one-clip edit saved in about 1.0 s. On the development build an empty timeline opened in 19.9 s, compiled in 1.585 s.
- **A refused edit that looked like a slow save** ([astrid-dev #1427](https://github.com/banodoco/astrid-dev/issues/1427)): the reason a scenario must say what it expects to happen, not only how long it took.

**Approach:** Measure first, then choose.

| Option | For | Against |
| --- | --- | --- |
| Measure every scenario, then write the fixes from the ranking (chosen) | Effort goes where the time is; Plan 77 and Plan 81 both showed that the guessed cause was not the measured one | The fixing half cannot be estimated until the measuring half is done |
| Write fixes now for the likely causes (history load, frame decoding, list virtualising) | Starts sooner | Three plans on 22 November 2026 were aimed at causes that measurement then moved |
| Add the scenarios to Plan 77 | One plan | Plan 77 is in Release 15 and still owes its own measurements; a plan sits wholly in one release |

**Challenge:** Reviewed — an independent Codex critic (`gpt-6.2-astra`, high effort, read-only, no part in the draft) was commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 22 November 2026 and read this plan and Plan 85 against the repositories; its report is [Plan 85's critique.txt](../85-one-place-to-measure/evidence/critique.txt). It ran no benchmarks and did not check playback on a real machine. The owner has asked that such critiques be weighed, not adopted wholesale; what the planner did with each finding on this plan:

- **Accepted — the App already has an editor benchmark.** `npm run perf:editor` (`scripts/perf/measure-editor.mjs`) was run on a real 286-clip film in October 2026 and probes load, playback, scrubbing and memory. The draft said nothing was known about scrubbing or playback; that was wrong. The plan now reuses it and corrects the fault in its comparison script first.
- **Accepted — start with the owner's own example.** Moving the playhead is TF-1, built on the existing test that matches the preview to a reference picture, with its 100 ms polling stated as an upper bound and a frame-numbered clip where the claim is exact.
- **Accepted — say what a headless browser cannot tell.** The draft asked for a number and a Runtime and browser share everywhere, and also allowed "cannot be measured". Scenarios are now either a measure or a named stand-in, and elapsed time and processor time are kept as separate clocks.
- **Accepted — do not rebuild what Plan 77 owns.** Restoring a project and opening the compiled editor are Plan 77's SL-7; its gestures for moving, dropping and undoing are reused; opening and saving are listed from its results. The draft's claim that an early failure loses the rest of a sweep was wrong: the sweep keeps finished rows.
- **Accepted — no figure for the fixing half, and no pre-numbered fix slots.** TF-4 puts the evidence to the owner first, then her times, then the tasks and their estimate.
- **Accepted — two proofs replaced.** "A slowed step moves the right number and no other" and a throwaway release are replaced by one seek delayed on purpose, and recorded pairs that are slower and unchanged.
- **Kept — two plans, not one.** The critic agreed.

The [Plan 77 manager's account](evidence/what-the-harness-needs.md) of what the harness needs agrees with the weaknesses as now stated.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Limits: a headless browser on a CPU machine; smoothness there compares builds and does not promise a figure on a person's computer.

**Review rounds:** Recommended: the stop at TF-3, where the owner sets the times and the fixes are written, and one round at the end. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — the time each scenario must meet.** Set at TF-3 from real numbers, not now. As a starting point for her to change: usable within 3 s of opening; the right frame within 0.3 s of moving the playhead to a point already seen and 1 s to one not yet loaded; playback starting within 0.3 s and dropping no more than one frame in a hundred; a drag that keeps up with the pointer; Saved within 2 s. Pending.

## Source identities

No work has started. Read on 22 November 2026: astrid-app `release/15/main` at `e3dbad64d402724ac5a35fb6447f18e432c64b78`; astrid-agent `release/15/main` at `8807f820eb47d6018db723511e024a0a123fbe95`; astrid-runtime `release/15/main` at `23310dc828765293a2ab39f637f28b948e780d94`. At run start record the release, the plan branch and the commits it was cut at.

## References

- [Plan 85](../85-one-place-to-measure/plan.md): the method, the runner and the table.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), [Plan 75](../75-fast-saving/plan.md): opening, saving and the Runtime's acceptance time.
- [astrid-dev #1427](https://github.com/banodoco/astrid-dev/issues/1427): the refused edit.
