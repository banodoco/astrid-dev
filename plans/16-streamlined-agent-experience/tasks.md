# Tasks: Streamlined agent setup and execution

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

## Draft task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| T1 — Scope current flows and extension contract | TBD | Verified source and retained work | Draft |
| T2 — Implement setup, readiness, execution, and representative extension | TBD | T1 | Draft |
| T3 — Prove selected journeys and compatibility | TBD | T2; integrated candidate | Draft |

These are organizing work areas only. Executable task breakdown, route/difficulty, dependencies, selectors, and review-round limits remain to be scoped after source inspection. Do not treat them as assigned or start-ready.

## Intended work and proof

- **T1:** Map choose-agent → connect-account → ready → run using the existing catalog and bridge. Identify first-increment providers and what “path runs” means. Distinguish provider/agent sign-in from connecting the local Astrid Runtime. Design one authoritative extension that supplies adapter, setup/sign-in, capabilities, model, and readiness information through existing contracts.
- **T2:** Reuse supported sign-in and credential storage; never expose secrets in UI or logs. Show missing installation, disconnected account, expired login, unavailable model, and retry after correction. Keep one normal agent execution path over existing pack/capability invocation, while preserving direct pack runs and alternative agents. Prove a representative addition through the extension point after generic consumer plumbing is established.
- **T3:** Define focused UI/bridge checks for successful setup, failed or cancelled sign-in, reconnect, one agent task, one pack invocation, and stopping a run. Cover the sandbox path with [Plan 15](../15-openshell-safe-execution/plan.md) where applicable. Preserve existing-agent compatibility and verify on the integrated candidate.

## Predecessor and authority

Use [PR #112](https://github.com/banodoco/astrid-agent/pull/112) to trace the Octop integration, not as proof that its files or behavior match current source. Preserve useful coverage; raw file-count reduction is not the goal. Check selectors and commands during task setup; do not invent them or run broad/automatic suites. Keep the project's existing review and publication authority under the [shared run contract](../../skills/astrid-dev-shared/run-contract.md).
