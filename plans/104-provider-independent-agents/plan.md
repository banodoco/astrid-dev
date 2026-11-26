# Provider-independent agent infrastructure

**Project:** Provider-independent agent infrastructure

**Goal:** A creator can recover and continue creative work with another authorized agent after a provider or agent process fails, without losing admitted work or changing project authority.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** Plan 100 agent/worker contracts and Plan 103 native authority for final proof; independent scope/release review; preserve current ACP and skill integrations.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Agent-managed tools](../../vision/gaps/LS-005-agent-managed-tools.md) (supporting) · [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting)

**Contributes to closure:** LS-006: E5: provider-independent agent recovery and durable work.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Give the common runtime durable agent-session identity, actor grants, project/context references, task/receipt linkage, user-visible checkpoints, cancellation and lifecycle coordination. External agents (Claude Code, Codex, local/custom) use provider adapters, CLI/SDK/MCP and the same capability discovery and typed operations. Keep provider-specific prompts, conversation data, reasoning and tool-loop implementation in adapters where appropriate. Explicitly distinguish portable project/task/checkpoint state from nonportable provider sessions or hidden reasoning. Do not promise transparent resume of arbitrary provider internals.

Define recoverable agent tasks and handoff semantics: an admitted independent task can continue or safely settle according to its contract; a replacement inspects durable facts, reuses idempotency/receipts, obtains fresh scoped permission and resumes only supported work. Avoid duplicate requests/settlement, silent credential transfers or unrestricted shell access. Preserve existing ACP chat, project chat, skills and extension development; native coordination does not require rewriting model adapters in Rust. Runtime owns authoritative context/records and agent orchestration primitives, not every prompt or intelligence provider. For presentation, route agent requests to the existing Plan 46 workspace operations with explicit target client/session, actor grant and actual frontend acknowledgement. Do not let headless agents claim they opened a window, or create provider-specific UI control paths; Plan 24/45/46 own component and layout semantics.

Out: developing an LLM, mandatory centralized agent harness, cross-provider hidden transcript migration, broad orchestration product, unapproved paid provider calls or OS sandbox replacement. Plan 15/F-007 owns sandbox qualification; Plan 41 owns agent-managed tool authoring.

## Existing work and decision

Agent astrid/chat has Node/TypeScript ACP process host, project chat, shared sessions, adapter and runtime client; the runtime profile-services supervisor declares chat readiness and custody. Existing plans 16, 41, 46, 15 and 36 address agent experience, tool management, workspace ops, sandbox and credentials. Reuse current behavior and contracts; see [architecture](../100-language-independent-foundation/architecture.md). See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

Inventory current chat/session/provider authority and durable versus ephemeral state; design a portable checkpoint and scoped capability contract with Plan 100; prove a CPU fake adapter and real local/reference agent where available. Integrate with Plan 103's authoritative native state; run provider termination/replacement and task settlement journeys. Do not change provider UX or add a duplicate chat store without review. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes Plan 100 contract, existing ACP adapters and session behavior, Plan 103 native workspace/task authority, scoped credential and permission contracts from existing plans. Produces provider adapter/session/checkpoint contract, durable recoverable session records, portable receipt-based handoff, and positive/negative integrated proof. Plan 105 may consume headless agent service, not provider-private state.

## Completion

- Two distinct authorized adapters operate on the same real project and typed capability surface; editor observes both operations and receipts. Include an independent local/CPU test adapter and at least one supported real provider path with appropriate authorization.
- Kill an agent during admitted work: worker completes or settles safely, user-visible checkpoint and receipt remain, replacement continues a supported step without duplicate effects; unrelated edit continues.
- Deny/revoke a grant, restart runtime, expire a session, lose connection and replay a request; verify no secret disclosure, unauthorized access, duplicate settlement or invented provider reasoning.
- Confirm supported provider-specific features and explicitly report nonportable session data. Existing ACP and external CLI integration remains usable; no mandatory new harness.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
