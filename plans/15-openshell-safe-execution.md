# 15 — Sandboxed execution with OpenShell

**Draft scope — not yet fully specified.** Current status and owner are in the [README queue](../README.md).

## Goal

Give users a straightforward way to run Astrid and its agents in an isolated environment with explicit permissions for files, network access, accounts, and connected services.

## Existing work to reuse

- [Agent PR #109 — OpenShell sandbox, MCP server and sandbox process control](https://github.com/banodoco/astrid-agent/pull/109): open at inspection on 2026-11-05; head `20530b07d7f225f85b2be5bb51c83325db810aed`. Includes `scripts/openshell/`, MCP integration, installer changes, and process-control propagation. Reconcile the actual current base and reusable changes before implementation.
- Its [sandbox setup document](https://github.com/matlowai/astrid-agent/blob/20530b07d7f225f85b2be5bb51c83325db810aed/docs/setup/openshell-sandbox.md) describes the Linux path, policy checks, account login, and service permissions. Treat its platform claims as historical evidence, not current qualification.
- Dependencies [Runtime #8](https://github.com/banodoco/astrid-runtime/pull/8) and [VibeComfy #160](https://github.com/banodoco/VibeComfy/pull/160) are merged; related [Runtime #9](https://github.com/banodoco/astrid-runtime/pull/9) is also merged. Check whether the candidate uses those merged changes rather than stale fork pins.

## Intended work and focused proof

- Reuse and streamline the existing sandbox setup, start/stop, account connection, and permission controls rather than building another launcher.
- Define the supported platform and isolation contract. Default to restricted access; users explicitly choose permitted services and file access. Document residual risks rather than promising absolute safety.
- Verify effective enforcement with explicit negative checks: forbidden host files, credentials, network destinations, and unapproved services stay inaccessible. Also prove permitted agent/pack operations, cancellation, and restart work.
- Inspect host-folder sharing and host ComfyUI access in particular: the existing document says these can weaken isolation. Keep stronger isolation usable without enabling those exceptions; disclose any exceptions at the point of selection.
- Coordinate UI account setup with [Plan 16](16-streamlined-agent-experience.md). Keep provider spend and external-service side effects visible; isolation does not prevent all actions inside an allowed service.

## Completion

A user can set up and run the supported sandbox path, understand its granted access, and stop it reliably. Focused positive and negative checks demonstrate the stated boundary on the exact integrated candidate. Unsupported platforms and remaining limitations are explicit. Historical full-suite results in the PR are evidence to assess, not instructions to rerun broad suites.

## Before implementation

Confirm current repositories, base branches and SHAs, existing work to preserve, verified predecessor inputs, a fresh candidate branch, and the intended `pre-main` destination. Break the work into bounded tasks with difficulty levels and explicit focused checks after inspecting those inputs. Links to other projects provide context, not blanket scheduling gates. No broad suites or automatic test discovery.
