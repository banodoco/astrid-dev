# Astrid Homepage Journey — Phase 1: foundation Tasks

← [Task index](../tasks.md#task-index) · [Phase 0](phase-0.md) · [Phase 2](phase-2.md)

##### Task T1

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Scripts, snapshots and registry to T0's numbers · `L/journey-script.ts`, `journey-snapshots.ts`, `journey-media.ts` |
| Deps | S1, T0, A1, A2 |
| Done when | Every snapshot validates; projections follow design.md §3.2; §4 never changes `V2`; copy numbers come from the same constants |

##### Task T2

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Session-owned publisher and adoption bridge · `J/publicAstridJourneyData.ts`, `H/PublicAstridEditorProvider.tsx`, `H/PublicAstridMountedEditor.tsx` |
| Deps | S1, T1 |
| Done when | Publish, replay and race tests pass; one provider instance; hero bundle immutable |

##### Task T3

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Scroll reader, pure director, projections and clock (trigger lines, retarget-never-queue, 120 ms floor, fast-forward, "Show the steps" mode, and an **ambient phase** after each demo that plays T0's ambient beats with variation, pauses off-screen or when hidden, and is skipped under reduced motion) · `J/publicAstridDirector.ts`, `J/usePublicAstridDirector.ts`, `J/publicAstridScrollReader.ts`, tests |
| Deps | T0, T1, T2 |
| Done when | Every design.md §3.4 row is a passing test; initial `#edit`, scrollbar jumps and boundary oscillation pick the right section without flicker; `flick-D`/`flick-P` show no stack, tray or label flash |

##### Task T5

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Sticky showcase in the tall grid (or the recorded fallback), per-section sticky left columns, leave-hero beat (vacuum retract, tilt eased to 0 before unmount, preview playing at rest), frame dissolve/re-form hooks, phone pin-and-scale · `J/PublicAstridJourney.tsx`, `H/PublicAstridSite.tsx`, Shell mount points, CSS |
| Deps | S2, T3 |
| Done when | One editor; no doubled scroll height; sticky ends before the finale; `pull-app-P` shows no jump of stage or text; between 10% and the trigger the hero rests, still playing |

##### Task T9

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Fit controller and hero zoom restore · `J/useJourneyTimelineFit.ts` |
| Deps | T2, T5 |
| Done when | D/P/N fits use the real gutter; stable on resize; clamped; hero zoom restored; `V1+A1+V2` fits at 320 px |

##### Task T10

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Flat overlay layer with computed positions + `PixelSprite` (part W6) · `J/JourneyOverlay.tsx`, `J/PixelSprite.tsx` |
| Deps | T0, T5, A5a |
| Done when | `s4-demo-D`/`-P` stills at DPR 2: every sprite pixel is a uniform k×k block in the mink palette (pixel check); the mink stays with a gliding clip |

##### Task T28

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Shared motion primitives reading only tokens: typed line, stamp, chip receipt, flash, History row, pixel ellipsis, Replay, the reduced-motion slideshow · `J/motion/*` |
| Deps | T0 |
| Done when | Unit tests for step counts, timings and reduced-motion paths |

[Phase 2 →](phase-2.md) · [Back to task index](../tasks.md#task-index)
