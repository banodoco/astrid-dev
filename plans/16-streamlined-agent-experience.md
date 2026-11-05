# 16 — Streamlined agent setup and execution

**Start here:** read [AGENTS.md](../AGENTS.md), choose a workflow in the [skills guide](../skills/README.md), follow the [run contract](../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../docs/glossary.md).

**Draft scope — not yet fully specified.** Current status and owner are in the [README queue](../README.md).

## Goal

Make Astrid's own agent the simple default way to get work done, with clear in-app agent selection, account connection, readiness, and execution, while preserving supported alternative agents and pack execution.

## Existing work to reuse

A read-only local inspection found these existing surfaces. Agent snapshot: `2958bacea3e3c7961788fa9c625dd9db0be282de`; App snapshot: `d38edf434a575f3aed941c516fe2a5338135820b`. Recheck current source before scoping tasks.

- App: `src/integrations/astrid/localAgents.ts` models agent choices, readiness, sign-in, and models; `src/integrations/astrid/acpRoutes.ts` provides connection/session APIs.
- App: `src/app/onboarding/WelcomeLocalSetup.tsx` and `WelcomeConnection.tsx` own existing setup and Runtime connection flows.
- Agent: `astrid/chat/` owns the local-agent host/ACP bridge; `astrid/mcp_server.py` and `astrid/omp_invoke.py` expose skills and capability execution. [PR #109](https://github.com/banodoco/astrid-agent/pull/109) also provides sandbox account/service integration.

The best matching example found is [Agent PR #112 — add Octop local agent integration](https://github.com/banodoco/astrid-agent/pull/112), inspected at head `c7444ad3be79569715fe5d36d6b7cce0f801b4c0`. It changes 18 files: eight implementation/build files and ten test or smoke files. Integration spans agent identity/catalog metadata, discovery and sign-in probing, launch routing, skills sync/harness registration, and a rebuilt bundle. Distinguish generated output and useful test coverage from duplicated handwritten integration work; reducing the raw file count is not the goal.

## One place to add an agent

Make adding a supported agent an extension implemented in one authoritative location in one repository. It should declare or provide the adapter, setup/sign-in behavior, capabilities, and model/readiness information through existing contracts. The app, onboarding, and execution host consume that same definition instead of maintaining parallel agent lists and provider-specific switch statements. “One place” means one owned extension, not a demand to put unrelated code in one giant file.

Use PR #112 to trace today's scattered edits, then prove a representative addition through the new extension path. Permit generic consumer plumbing changes while establishing the contract; afterwards, adding the representative agent must not require handwritten provider-specific changes across multiple repositories. Preserve existing agents and pack execution. Coordinate with the [execution host refactor](13-execution-host-refactor.md) and [repository cleanup](14-repository-cleanup.md) only at demonstrated shared boundaries.

## Intended work and focused proof

- Map the shortest choose-agent → connect-account → ready → run flow using the existing catalog and bridge. Clearly distinguish provider/agent sign-in from connecting the local Astrid Runtime.
- Put useful readiness and recovery information in the interface: missing installation, disconnected account, expired login, unavailable model, and retry after correction.
- Reuse supported sign-in flows and credential storage. Never expose account secrets in UI output, logs, or project files.
- Keep one normal agent execution path and reuse existing pack/capability invocation underneath it; preserve supported direct pack runs and other agent choices.
- Define focused UI/bridge checks for successful setup, failed/cancelled sign-in, reconnect, one agent task, one pack invocation, and stopping a run. Cover the sandbox path with [Plan 15](15-openshell-safe-execution.md) where applicable.

## Scope still to settle

Confirm which account/provider flows are in the first increment and what the user's “path runs” phrase denotes; preserve existing execution routes until that is clear. Do not turn this into a new agent framework or assume every provider supports the same authentication method.

## Completion

Users can connect a supported account and complete work through Astrid's agent with clear setup and recovery, while alternative agents and pack execution remain available. A representative agent can be added through the single owned extension path, without scattered provider-specific consumer edits. The selected journeys and existing-agent compatibility pass explicit focused checks on the integrated candidate.

## Before implementation

Confirm current repositories, base branches and SHAs, existing work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. Break the work into bounded tasks with difficulty levels and explicit focused checks after inspecting those inputs. Links to other projects provide context, not blanket scheduling gates. No broad suites or automatic test discovery.
