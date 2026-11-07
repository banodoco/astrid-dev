# Tasks — Agent-powered liquid workspace

[Plan](plan.md) · [Inputs](inputs.md). **Draft only.** Scope and task routes/acceptance selectors are to be frozen with the actual App/Agent/Runtime base; do not execute from this document alone.

| ID | Outcome | Dependency | Focused evidence |
| --- | --- | --- | --- |
| LW-1 | Audit real video editor component contracts, state, touch/pointer/drag behavior and extension boundaries | None | Current App source and reproduction notes for mounting constraints |
| LW-2 | Declarative 2D workspace geometry, layout persistence and reversible `open/place/attach/focus/float` ops with deterministic IDs | LW-1 | Dock/float/maximize/restore real preview, timeline and inspector without state loss |
| LW-3 | Reusable component definition/instance/binding contract and adaptive container sizing | LW-2 | Correct scoped playback and selection with two views/instances; gallery or transcript pilot |
| LW-4 | Host-owned typed extension points via existing contribution lifecycle | LW-3 | One new component defines a specialized extension without modifying the editor shell |
| LW-5 | Agent workspace manipulation API with authorization, inverse operations and separate semantic binding | LW-2, LW-3 | Direct UI and agent make equivalent layout changes; accidental proximity never silently binds |
| LW-6 | Music-aware editing preset using real `music.beats`/timeline capabilities and optional typed beat lane | LW-3, LW-4, LW-5; reconcile Plans 04/06/18 | Real result read, source/time mapping, edit proposal, concurrent correction and stateful restoration |
| LW-7 | Evidence review of second-domain generality, performance and input isolation | LW-6 | Focused browser and domain tests on exact candidate, including compact/mobile case |

Do not substitute a mock shell or static picture for proof against the existing editor. Native 3D workspace placement is a separate follow-on once model and lifecycle constraints are stable.
