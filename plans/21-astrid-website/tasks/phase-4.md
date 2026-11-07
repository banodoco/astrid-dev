# Astrid Homepage Journey — Phase 4: finale, navigation, accessibility, E2E Tasks

← [Task index](../tasks.md#task-index) · [Phase 3](phase-3.md)

##### Task T22

| Field | Accepted value |
|---|---|
| Tier | TASTE-HIGH |
| Goal · files | The finale: shared reveal module (its extraction is a NORMAL sub-step inside this brief), the mink at the horizon, look-up at progress ≥ .98 · `J/PublicAstridJourneyFinale.tsx`, CSS |
| Deps | T6, T21, M1 |
| Done when | Signs off `finale-D` and `-P` at the peak and the look-up frame against `../mockups/*/05-finale` at 2×; one Vision link |

##### Task T23

| Field | Accepted value |
|---|---|
| Tier | XHARD |
| Goal · files | Navigation, lifecycle and hash restore |
| Deps | T3, T5, T22 |
| Done when | Repeated Vision/back restores exact scroll, hash and section (checked on the LAN preview in real Safari); hidden work stops; same-page hashes don't start room transitions |

##### Task T24

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | Semantics and keyboard: headings, the tab control's keys, Replay and "Show the steps"/"Pause" focus, inertness |
| Deps | T3, T11, T14, T17, T19, T28 |
| Done when | a11y tests pass; `s4-demo-P-rm` shows the stepped story with opacity changes only; keyboard order checked in a recording |

##### Task T26

| Field | Accepted value |
|---|---|
| Tier | NORMAL |
| Goal · files | The journey E2E spec with `page.clock` (forward, flick, back, Replay, Vision, RM, phone project); CI installs WebKit or the spec pins to what CI can launch |
| Deps | T23, T24 |
| Done when | The default projects pass locally and in CI |

[Back to task index](../tasks.md#task-index)
