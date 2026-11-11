# Sandboxed execution with OpenShell

**Vision gaps:** [F-007 — First-class full-stack sandboxing](../../vision/gaps/F-007-first-class-sandbox.md) (primary); [F-002 — trustworthy user control](../../vision/gaps/F-002-safe-user-control.md) (supporting). The sandbox outcome is independently testable; broader consent and recovery require separate evidence.

**Contributing:** [Astrid development skill](../../skills/astrid-dev/SKILL.md).

Offer an onboarding path to run the full Astrid stack—app/frontend, Runtime, and Agent backend—in OpenShell with clear, user-selected permissions. This is a draft; supported platforms and the isolation contract remain to be scoped against current source.

## Goal and scope

- Included: reuse the existing OpenShell setup, start/stop, account connection, and permission controls; define the actual sandbox and client boundaries; support explicitly authorized external inference; prove the stated boundary with focused checks.
- Deferred: implementation assignments and platform qualification until current repositories and retained work are inspected.

## What we build on

Agent PR #109 contains an OpenShell setup path, MCP integration, installer changes, and process-control propagation. Runtime #8, Runtime #9, and VibeComfy #160 are merged dependencies to reconcile against the candidate. See [inputs](inputs.md) for historical identities and limits.

## Sequence

Inspect and reconcile inputs, then scope executable tasks and selectors. Define which app and backend processes run inside the sandbox and which clients remain outside; specify supported platforms, default restrictions, and disclosed exceptions for host-folder sharing or host ComfyUI access. Coordinate first use with [onboarding](../20-zero-to-first-image/plan.md), [agent setup](../16-streamlined-agent-experience/plan.md), and [inference routing](../12-multiple-inference-routes/plan.md). The task outline is in [tasks](tasks.md).

## Completion

Users can choose, configure, run, and reliably stop the supported full-stack sandbox, understanding its granted access, outside client boundary, external inference data flow, and residual risks. Focused positive and negative checks establish the claims on the integrated candidate. This does not prove absolute safety or qualify unsupported platforms. Integration is subject to the existing `pre-main` destination and publication authority in the [shared run contract](../../skills/astrid-dev-shared/run-contract.md).

## Read next

- [tasks.md](tasks.md): draft work outline and scoping needed before dispatch.
- [inputs.md](inputs.md): historical work, dependencies, and source identity requirements.
