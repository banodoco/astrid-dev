# 16 — Streamlined agent setup and execution

**Start here:** read [AGENTS.md](../../AGENTS.md), choose a workflow in the [skills guide](../../skills/README.md), follow the [run contract](../../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../../docs/glossary.md).

Make Astrid's own agent the simple default way to get work done, with clear agent selection, account connection, readiness, and execution. Preserve supported alternative agents and pack execution. Status, owner, and estimate remain in the [project queue](../../README.md).

## Goal and scope

- Included: a simple choose → connect account → ready → run path; useful setup and recovery information; one authoritative agent extension point; existing agent choices and direct pack runs.
- Deferred: a new agent framework and assumptions that every provider uses the same authentication method.
- Still undecided: first-increment providers and the meaning of “path runs.” Keep existing execution routes until clarified.

## What we build on

The app already has an agent catalog/readiness model, ACP connection routes, and onboarding flows. The agent repository has a local-agent host/ACP bridge plus skills and capability execution. PR #112 is the closest integration example: trace its scattered edits and distinguish generated output and useful coverage from duplicated handwritten work. See [inputs](inputs.md) for identities and [tasks](tasks.md) for the draft work areas.

## Sequence

Recover and verify current source and retained work; map the shortest setup and execution journey, including the difference between provider sign-in and connecting the local Astrid Runtime. Then define one owned extension consumed by onboarding, the app, and execution host; prove a representative agent through it; finish with focused compatibility checks. Coordinate with [execution host refactor](../13-execution-host-refactor/plan.md) and [repository cleanup](../14-repository-cleanup/plan.md) only at demonstrated shared boundaries.

## Completion

Users can connect a supported account and complete work through Astrid's agent with clear setup and recovery, while other agents and pack execution remain available. A representative agent uses the single extension point without scattered provider-specific consumer edits. Selected journeys and existing-agent compatibility have explicit focused evidence on the integrated candidate. Destination and publication authority follow verified input and shared run policy; this draft does not authorize implementation.

## Read next

- [Tasks](tasks.md): intended work and what remains to scope.
- [Inputs](inputs.md): source identities, precedent, and evidence limits.
