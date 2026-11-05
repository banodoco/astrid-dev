# 12 — Add multiple inference routes through shared generation

**Draft scope — not yet fully specified.** Current project status is in the README queue.

## Goal

Provide one shared generation route for VibeComfy (primary) and Wan2GP (additional), with both integrations represented as packs. The same task lifecycle applies to either backend: claim the task and required compute resources, load and unload models, execute, handle cancellation, and release resources on success, failure, or cancellation. Reuse existing ownership, custody, and lease primitives first; make the smallest platform change only if those primitives cannot support the lifecycle. Explicitly selected external inference remains supported.

## Owner

See the root [README queue](../README.md) for ownership.

## Scope

- Included: inspect and reuse existing installation/setup and instance-connection infrastructure where applicable; make the full setup path for VibeComfy and Wan2GP understandable and usable; support inference through the shared lifecycle; prove both a full Wan2GP installation path and connection to an existing Wan2GP instance. Distinguish attaching to an external server from owning its process or GPU: never stop or kill a user's server or unload models the route did not load/own.
- Deferred: additional inference backends and provider-specific capabilities not needed to establish these routes.

## Inputs and source identity

The user-provided starting premise is that VibeComfy is the existing primary route, some reusable setup/connection infrastructure already exists, and Wan2GP should be added as another route. These are planning inputs, not verified claims about current code. At execution start, identify the actual repositories, refs and SHAs, dirty work to preserve, current generation interfaces, pack entry points, and existing installation and instance-connection mechanisms. Define the hardware, model availability, and environment for actual inference proof during scoping; do not reduce acceptance to mocks alone.

| Input | Why it matters | Link or evidence |
|---|---|---|
| Shared generation behavior | Defines the common user-facing route and existing setup/execution/results contract. | [Consistent generation plan](02-consistent-generation/plan.md) and its [task details](02-consistent-generation/tasks.md); verify current state at start. |
| Pack implementation and composition | Reuse current native pack conventions and boundaries. | [Plan 06 — Packs](06-packs.md); verify current source at start. |
| Wan2GP install and connection paths | Distinguishes full installation from attaching to an existing instance. | Establish exact code paths, supported environments, and focused proof during execution scoping. |

## Intended work and focused proof

- Map existing generation, setup, instance-connection, ownership/custody, and lease code; reuse it instead of introducing a parallel framework.
- Expose VibeComfy and Wan2GP as packs through the shared generation path, preserving VibeComfy as the primary route.
- Demonstrate Wan2GP installation and connection to an existing instance separately, including actual inference through each path. Also demonstrate actual VibeComfy inference. Exercise normal completion, failure, cancellation, cleanup/release, and compute contention for each shared lifecycle; mocks can supplement, but cannot replace actual inference evidence.
- Confirm VibeComfy still generates successfully and external inference remains usable when explicitly selected. Use focused route and pack checks; do not invent selectors before inspecting the current code.

Define executable tasks, difficulty levels, and exact test selectors after inspecting the existing code. Before implementation, record the actual base branch and SHA, reusable work and verified predecessor inputs, a fresh candidate branch, and the verified `pre-main` destination. These linked plans are context, not blanket scheduling gates.

## Completion

Complete when both packs use the shared lifecycle, VibeComfy remains primary, the Wan2GP full-install and existing-instance paths are demonstrated, actual inference succeeds through both backends, and focused lifecycle checks prove failure, cancellation, cleanup, and contention behavior. Controlled failures may use fixtures; successful inference evidence must be real. Existing external instances and unrelated loaded models remain untouched. Record unsupported hardware, model, or environment combinations explicitly.

## Scoping questions

- Which hardware, models, and environment can be used for actual inference proof?
- How should VibeComfy and Wan2GP packs be installed or included by default? This policy is still to be decided and is separate from Plan 11's requirement that Three.js remain included by default.
- Which existing installation and instance-connection mechanisms are reusable, and what is the smallest supported Wan2GP installation path?
