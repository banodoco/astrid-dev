# Astrid Homepage Journey — Phase 2: §2 and §4 in parallel, the sky, the mink Tasks

← [Task index](../tasks.md#task-index) · [Phase 1](phase-1.md) · [Phase 3](phase-3.md)

##### Task T6

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | Section layouts: headers (eyebrow types on; headline and sub never animate), section scroll lengths, the composition of every section at D, P, N and S, including phones · `J/PublicAstridJourney.css`, section wrappers |
| Deps | T5, H0 |
| Done when | `pull-app-D-1320` and `-P-1320`: header readable and sticky beside the settled stack; no title or spine collision at D, P, N, S |

##### Task T8

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | The pull-apart and its reverse, from App and Agent, at D and P, plus the RM dip (owns the phone stack) · pose CSS, `J/PublicAstridExtendStack.tsx` |
| Deps | S2, T6, H0 |
| Done when | Signs off `pull-app-D-0/240/600/1320`, `pull-agent-D-0/300/600/1320`, `pull-app-P-1320`, `back-2-1-D`, `pull-app-D-rm` against `../mockups/night/02a` and `day/02b` at 2×: the hero coming apart, not a cut to a new scene |

##### Task T11

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Section spines with chip slot, pending ellipsis, reserved height · `J/PublicAstridJourneySpine.tsx` |
| Deps | T1, T3, T28 |
| Done when | Carry-over exact; chips attach to the right reply; replay makes no duplicate turns; `s4-demo-P` shows no spinner and no layout shift |

##### Task T12

| Field | Accepted value |
|---|---|
| Tier | TASTE-LOW |
| Goal · files | The look of every primitive: stamp, lit layer, chip and flood, typed line and check, History row, tabs, Replay, Departure Mono 11 px |
| Deps | T11, T28, H0 |
| Done when | `s2-demo-D` at the stamp peak, `s4-demo-D` at the flood, and `-P` equivalents legible in both palettes; highlight is text plus dot |

##### Task T13

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Three.js structure view (plumbing; lazy import, dispose, still-frame fallback captured from the scene) · `J/structure-view.ts`, `J/PublicAstridStructureView.tsx` |
| Deps | T1, T8 |
| Done when | No three.js request at hero load; planes match the snapshot; code panel shows the real module; repeated entry doesn't grow canvases; fallback works at D and P |

##### Task T14

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | §2 example states and tabs: the first cycle, then T0's ambient cycling with live activity in each example; a click pins one example, progress line, pillar conduits, the cable from an anchor measured once · `J/extendExamples.ts`, `J/PublicAstridExtendExamples.tsx` |
| Deps | T3, T8, T28 |
| Done when | `s2-demo-D` plays the first cycle and `rest-2-D` shows it still alive 20 s later; leaving gives the LTX handoff; resize re-anchors the cable once; keyboard tests pass |

##### Task T15

| Field | Accepted value |
|---|---|
| Tier | TASTE-LOW |
| Goal · files | Example panels, **including the 3D view's look** (camera, framing, material, sway), the workflow card, waveform reveal, install log, tab-swap motion, cause → light → stamp order |
| Deps | T12, T13, T14 |
| Done when | `s2-demo-D` and `-P`, one still per tab at +2600, against `../mockups/*/02a`, `02b`, `02c` at 2× |

##### Task T19

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | §4 mechanics: cursor states, History append/shift/tint and phone ticker, the ambient exchanges from T0's pool (snapshot publishes at beat boundaries), beat markers, flash rectangles, wedge/level/dimension strokes · `J/PublicAstridJourneyHistory.tsx`, edit cues |
| Deps | T1, T3, T9, T10, T11, T28 |
| Done when | Each History row matches its snapshot in `s4-demo-D`/`-P`; the ticker shows one row at a time; `V2` unchanged |

##### Task T20

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | The grow and the §4 beats (starts right after the foundation; the grow is finished after T18's fold exists) |
| Deps | T9, T19 |
| Done when | Signs off `grow-D-0/420/840`, `s4-demo-D` stills (trim, mid-carry, 2nd snip, flood, mid-retime, end) and `s4-demo-P` against `../mockups/*/04a`, `04b`, `04c` at 2× |

##### Task T21

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Sky in the journey: progress from the scroll reader, quantised steps, held palette with the 720 ms boundary transition, quiet field gated to the hero, RM stepping · sky session/geometry, `J/useJourneySky.ts` |
| Deps | S4, T3, T5 |
| Done when | `finale-D` shows visible steps and no colour pop at boundaries; `finale-D-rm` steps per section; Vision return deterministic |

##### Task M1

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | Every mink cue and glyph ([design.md](../design.md#106-the-mink)): placement, frame choice and holding back at D and P, on the A5a placeholders |
| Deps | T10, A5a; cue slots from T15, T18, T20 |
| Done when | One still per cue in `s2/s3/s4-demo-D`/`-P` and `finale-D`: charming, never covering a label, chip or cursor; "!" and the sparkle appear once each across the full recordings |

[Phase 3 →](phase-3.md) · [Back to task index](../tasks.md#task-index)
