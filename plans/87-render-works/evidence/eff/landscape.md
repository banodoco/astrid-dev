# Release and plan landscape

`5d3f9e4` (2026-11-22).

## Releases

- **14:** Final; frozen/published 2026-11-22 ~13:50 UTC. Lead `session_011EzfW3Zy19ncNecpQnKb7D`; highlight “dependably” (`releases/14.md:1-11,166,444`). Agent/App/Runtime main == release/14/main: `c0ad6b54`, `e0da794a`, `5120462d` (`releases/14.md:287-299`).
- **15:** Draft/open; no date. Lead `session_011EzfW1gtAhRQwk8pgJMzhG`; “Generation is tested for real” (`releases/15.md:1-11,55-59`).
- **R14 rule:** only the Lead merges accepted plan/fix branches (`releases/14/run.md:40`); no unexplained failures; targeted/importing tests (`releases/14.md:448-452).

## Plans

- **(a) #1401:** P77 *Saving holds on a heavy timeline* — active/Codex manager/R15; “about 2 s or better” (`plans/77-saving-holds-on-a-heavy-timeline/plan.md:7-9,23-34`; `releases/15.md:36`). P63 *Dependable saving* — queued/unassigned/R15 (`plans/63-dependable-saving/plan.md:7-13`). P18 *Extensible timeline editing* — queued/unassigned/R15; commit contract moved to P63 (`plans/18-timeline-editing/plan.md:7-25`).
- **(b) #1402:** P76 *Editing together* — queued/unassigned/R15; “unrelated changes both land” (`plans/76-editing-together/plan.md:1,7-13,25-29`).
- **(c) #1403:** P69 *Editing a real clip: project elements and practical fixes* — active/Codex manager/R15; `clip.set-element` “refuses unbound clips” (`plans/69-project-elements/plan.md:1,7-13,23-28`).
- **(d) Render:** P27 *Complete video rendering and export options* — queued/unassigned/no release; export should “produce” a playable file (`plans/27-video-render-options/plan.md:1,7-13,19-27`).
- **(e) Custody:** P83 *Execution host in modules* — queued/unassigned/no release; “process custody” (`plans/index.md:87`; `plans/83-execution-host-in-modules/plan.md:1,55`). P38 *One process identity* — queued/unassigned (`plans/index.md:23`). PROCLIFE/process-lifecycle not found.
- **(f) Motion:** P78 *Live custom-element editing* — active/Plan 78 manager/R15; fresh-install pin awaits owner (`plans/78-live-custom-element-editing/plan.md:1,7-13`; `plans/78-live-custom-element-editing/inputs.md:7,16`). P69: `astrid_motion` moved to `poms_packs`; unpinned (`plans/69-project-elements/inputs.md:16`).
- **(g) CI journeys:** P39 *All three mains green* — active/Release 14 Lead; remainder R15 (`plans/39-green-mains/plan.md:1,7-13`; `releases/15.md:31`). Windows journey `plans/39-green-mains/tasks.md:79`; `journey.yml` receipts are Release-skill-owned (`plans/39-green-mains/plan.md:36; plans/39-green-mains/tasks.md:154`).
- P84 *A living planet on the vision page* is active; P85–86 exist (`plans/index.md:88-90`); next free: **87**.

## Issues

All issues open/unassigned; —=not found.

| # | Title | Labels | Plan |
|---|---|---|---|
|1246|bug: a failed timeline commit can leave the timeline stuck with no supported way to clear it|bug|—|
|1253|bug: every timeline render is refused on an installed release|bug|—|
|1320|observation: timelines visualize fails with "renderer lease channel closed" after about 57 seconds from source in a container|observation, plan:81|81|
|748|Composed timeline visualization fails installed registry discovery while inputs mode works|plan:59|59|
|759|Source Runtime: identity mismatch after source changes, and a stale pack-host registration after restart|none|59 (body)|
|1238|bug: timelines visualize fails the whole timeline on one stale asset|bug|—|
|1397|observation: an action failure prints the one useful line under three copies of a traceback|observation|—|
|1398|idea: run an SDK script in an install's own Python|idea|—|
|1413|bug: a Runtime timeout is reported as a failed identity check with "run the Astrid install line again"|bug|—|
|1430|Restore removed clips or revert a time range to an earlier revision|bug|—|
|1469|bug: editor preview and render use different revisions of the same element pack|bug|—|
|1470|bug: the render bundler cannot resolve elements from collection packs|bug|—|
|1471|bug: collection pack elements cannot import shared rendering contracts|bug|—|
|1472|bug: long renders lose the execution lease while the Runtime is unresponsive|bug|—|
|1473|bug: custody cleanup aborts a live render when descendant capture fails|bug|—|
|1474|bug: a failed render leaves the managed session slot occupied|bug|—|
|1475|bug: failed render scratch is not reclaimed and blocks the next admission|bug|—|
|1476|bug: render failures and frame progress are invisible outside the invoking command|bug|—|
|1477|bug: the render export hint uses an unsupported --to option|bug|—|
