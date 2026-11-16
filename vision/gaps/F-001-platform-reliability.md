# F-001 — Reliability isn't proven across supported setups

**Aspiration:** [Dependable execution and recovery](../principles/eliminate-needless-technical-wrangling.md#dependable-execution-and-recovery) (primary) · [Approachable, reversible choices](../principles/in-the-creators-control.md#approachable-reversible-choices) (supporting) · **Assessment:** Partially evidenced (2026-11-06; source is existing plan/queue evidence, not a new qualification).

## Desired state

On each declared supported operating system, device and deployment route, people can reliably install, launch, stop, update, roll back, repair and remove Astrid without losing projects or becoming stranded in an unexplained state. This concerns the application's **operational lifecycle**, not whether every creative workflow succeeds.

## Current state

[Plan 29](../../plans/29-update-and-release/plan.md) is reopened: Release 10 (0.0.10) is published, but `install --update` on a machine that already completed the Release 1 storage handoff exits 0 and installs nothing. Less common setups remain in [Plan 30](../../plans/30-update-everywhere/plan.md).


[Plan 08](../../plans/08-release1-install-update/plan.md) records a completed five-row hosted R1 installation/update gate, proving that *specific* paths worked on *specific* candidates. The [project queue](../../README.md) records Plan 07 as active with indicative Pinokio evidence and existing CI failures, while Plans 09/10 target broader routes and native qualification. This is **not** proof that all devices, browser variants or real engines are covered.

## Gap

Supported installation, launcher and engine lifecycle transitions—especially updates, failures, rollback, cleanup and recovery—still lack sufficiently broad, current and reproducible qualification. Creative job correctness belongs to F-003; authority over agent actions belongs to F-002.

## Closure evidence

A declared and version-pinned OS/device/deployment matrix demonstrates clean installation, launch, stop, update, interruption recovery, rollback and removal with preserved work and meaningful negative tests. This qualifies supported operational paths, not creative inference accuracy or permission policy.

## Sources and reassessment

[Plan 08](../../plans/08-release1-install-update/plan.md) · [Current queue](../../README.md) · [Vision gaps](../README.md). Reassess on shipped versions, new supported platforms, incident reports or finished evidence—not solely when a CI job turns green.
