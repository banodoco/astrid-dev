# F-001 — Reliability across supported environments

**Applies to:** [Local-first, cloud-capable](../principles.md#local-first-cloud-capable) · [In the creator's control](../principles.md#in-the-creators-control) · **Assessment:** Partially evidenced (2026-11-06; source is existing plan/queue evidence, not a new qualification).

## Desired state

On each **declared supported** OS, device and deployment mode, people can reliably install, start, use, stop, update, roll back, repair and remove Astrid without losing work or being stranded by unexplained state. Support claims are backed by a maintained matrix of real-path evidence.

## Current state

[Plan 08](../../plans/08-release1-install-update/plan.md) records a completed five-row hosted R1 installation/update gate, proving that *specific* paths worked on *specific* candidates. The [project queue](../../README.md) records Plan 07 as active with indicative Pinokio evidence and existing CI failures, while Plans 09/10 target broader routes and native qualification. This is **not** proof that all devices, browser variants or real engines are covered.

## Gap

Real supported-environment coverage, failure/recovery paths, launcher and engine lifecycle, update/rollback qualification and current source/version coherence need broader and ongoing verification.

## Closure evidence

A declared OS/browser/device/deployment matrix, including realistic new-install and update journeys, managed task/engine start and safe stop, recovery after interrupted operation, rollback/uninstall, preservation of project data, and meaningful negative controls. Exact candidate/source and platform evidence are attached. Unsupported cells remain explicit; do not claim "all devices" without defining the matrix.

## Sources and reassessment

[Plan 08](../../plans/08-release1-install-update/plan.md) · [Current queue](../../README.md) · [Gap model](../gaps.md). Reassess on shipped versions, new supported platforms, incident reports or finished evidence—not solely when a CI job turns green.
