# F-007 — Running Astrid in a sandbox isn't yet a first-class option

**Applies to:** [In the creator's control](../principles/in-the-creators-control.md) (primary) · [Eliminate needless technical wrangling](../principles/eliminate-needless-technical-wrangling.md) (supporting) · **Assessment:** Open; sandbox foundations exist, but an integrated, qualified user-facing full-stack path has not been demonstrated (2026-11-07).

## Desired state

People can choose to run Astrid's creative environment—App, Agent, Runtime and permitted tools—in an isolated sandbox as a normal, understandable setup option. They can grant and revoke access to host files, credentials, network destinations, external inference services and compute resources without needing to manage low-level containment themselves. They can work, stop and recover predictably, and understand any integrations that cross the isolation boundary.

## Current state

There is relevant ongoing work: [Astrid Agent PR #109](https://github.com/banodoco/astrid-agent/pull/109) contains OpenShell sandbox setup and controls, and [Plan 15](../../plans/15-openshell-safe-execution/plan.md) covers an integrated full-stack option. Current Agent sources include sandbox scripts, but their existence does not demonstrate a supported, first-class end-to-end user experience or verified isolation across the App, Agent and Runtime. The PR was open when checked on 2026-11-07; environment and platform qualification remain to be established.

## Gap

There is no proven, user-friendly path for selecting, starting and using a **fully isolated Astrid workspace** with understandable permissions and boundaries. The outcome is independent of a particular sandbox technology: OpenShell is one possible implementation, not the definition of the gap.

## Closure evidence

On a declared supported platform, a user can choose the sandbox mode, start the required stack, perform an approved creative job, stop and restart, and recover their project. Show positive and negative checks for permissions to host files/credentials, network and external inference, including denied actions, cancellation and safe teardown. Document what runs inside versus outside, any opted-in host integration, and residual risks. This proves a bounded supported isolation option, not universal security or a complete answer to [the broader user-control gap F-002](F-002-safe-user-control.md).

## Sources and reassessment

[Plan 15](../../plans/15-openshell-safe-execution/plan.md) · [Agent PR #109](https://github.com/banodoco/astrid-agent/pull/109) · [Plan 15 source assessment](../../plans/15-openshell-safe-execution/inputs.md) · [F-002 — safe user control](F-002-safe-user-control.md). Reassess only against integrated, version-pinned evidence; do not treat a proposed sandbox, available script or a green test suite by itself as proof of this outcome.
