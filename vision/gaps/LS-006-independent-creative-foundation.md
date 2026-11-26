# LS-006 — The creative foundation is not yet independent of its clients and creative environments

**Aspiration:** [A small, dependable foundation](../pillars/liquid-software.md#a-small-dependable-foundation) (primary) · [Shared human–agent work](../pillars/liquid-software.md#shared-humanagent-work) (supporting) · [Dependable execution and recovery](../principles/eliminate-needless-technical-wrangling.md#dependable-execution-and-recovery) (supporting) · **Assessment:** Open; source-observed implementation coupling, 2026-11-26; product journey not yet qualified.

## Desired state

A creator can open, inspect, edit and preserve the same authoritative workspace through a browser, local application, CLI or independent agent, without the foundation depending on any particular interface, agent provider or creative-language environment. When a managed environment or agent breaks, the creator can still access their work, see what happened, repair or replace the failed component and continue unrelated work. Independent contributors can implement a client or capability against documented contracts without importing the core's private implementation, with consistent editing semantics and permission boundaries.

## Current state

Observed in source reviewed 2026-11-26 (the published-main source identities are historical observations, not release qualification): the [Runtime protocol](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/contract/README.md) already defines generated clients, authoritative tasks, state, idempotency and version checks. However, the [Agent generic host](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/execution/generic_host.py) imports Runtime implementation modules; the [Runtime timeline provider](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_provider.py) dynamically imports a synchronous Python authoring provider. The [bootstrap](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install) provisions Python before the installer can run; the [Agent installer](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/installer/runtime_lifecycle.py) and [App development launcher](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/scripts/dev-local-workspace.mjs) share lifecycle responsibilities with Runtime. The current Python Runtime is itself dependent on an interpreter; its pyproject also declares schema-validation dependencies. This is positive evidence of architectural dependence, not evidence that every supported current journey fails. Existing release branches may already resolve some of the reported duplication; re-inventory before code.

## Gap

The foundation cannot yet be independently started, operated and recovered with the same creative semantics while replaceable client, provider or managed-language environments are absent, failed or independently implemented. F-001 measures the reliability of supported installation transitions, F-004 pack lifecycle, LS-003 frontend/backend extension composition and LS-004 modality ecosystem breadth; those can improve without establishing an independent core, and this gap can close without qualifying every pack, GPU, modality or hosted service.

## Closure evidence

- E1 — A separately implemented client and worker use documented, versioned contracts without private implementation imports, and read the same project and task receipts as the supported SDKs; unknown versions, stale writes and unauthorized operations are refused.
- E2 — On declared Windows, Linux and macOS installations, the same workspace is accessible through the supported hosted and bundled local React interfaces, native shell and CLI. After intentionally breaking the managed Python or Node environment, the native recovery path diagnoses and repairs it without losing work or creating a second owner. External managers are respected; offline local editing does not need the hosted site.
- E3 — The same edit command corpus from Python, TypeScript and browser preview yields equivalent timeline semantics, with canonical commits, history, rendering inputs and undo preserved. Concurrent incompatible edits, stale head, invalid commands and crash/retry have documented outcomes; a preview cannot bypass commit authority.
- E4 — A native, headless workspace starts and reads/edits existing projects, handles state, media and task admission without Python, Node, an agent or UI. A verified migration preserves data and provenance; interrupted writes, backup/restore, rollback eligibility, permissions and duplicate-owner refusal are exercised.
- E5 — An agent provider is killed or replaced during a real creative task: already admitted work continues or safely settles, the next authorized agent resumes from inspectable durable context/receipts, and unrelated work is unaffected. No provider-private reasoning or credentials are silently transferred.
- E6 — The same versioned core and task/worker contract work in local and isolated headless remote deployments. The same capability executes with explicit placement and scoped inputs; disconnect, retry and revoke preserve custody, avoid duplicate settlement and do not silently spend or upload. Fully hosted account service and all cloud routes remain separate outcomes.

## Closure approach

Use the existing product and its in-flight reliability/performance work as the behavioural reference. First make the actual boundaries independent of implementation, including installer/worker custody and the timeline authoring seam. In parallel where ownership is clear, qualify a native application and a single deterministic timeline engine; keep React and Python creative tooling extensible. Build the native authoritative workspace against the same behavioural contracts, with one active writer and verified data migration, before replacing the Python daemon. Agent and remote execution can then use the common boundary without making the core depend on either. Prefer deleting old ownership paths after parity over keeping two indefinitely. The proposed design and alternatives are in [native foundation architecture](../../plans/100-language-independent-foundation/architecture.md); the umbrella decision is [issue #2038](https://github.com/banodoco/astrid-dev/issues/2038).

## Route to closure

| Step | Plan | Contributes (closure evidence it delivers) | Milestone |
|---|---|---|---|
| 1 | [Plan 100](../../plans/100-language-independent-foundation/plan.md) | E1: independent client/worker contract and behavioural reference | A: one boundary |
| 2 | [Plan 101](../../plans/101-native-astrid-application/plan.md) ∥ [Plan 102](../../plans/102-one-timeline-engine/plan.md) | E2: independent installation and interfaces; E3: one timeline semantics | B: native app and shared editing |
| 3 | [Plan 103](../../plans/103-native-workspace-runtime/plan.md) | E4: headless authoritative native workspace and migration | C: independent core |
| 4 | [Plan 104](../../plans/104-provider-independent-agents/plan.md) ∥ [Plan 105](../../plans/105-one-local-cloud-runtime/plan.md) | E5: provider-independent recovery; E6: local/remote deployment parity | D: replaceable providers and placement |

Critical path: contract and reference proof → timeline and workspace integration → qualified native workspace cutover → integrated provider/deployment proof. Native application work may run alongside the early contract and timeline slices, but it must not create another installation owner. The route and numbers are a draft scope proposal; no release or implementation is authorized.

## Sources and reassessment

Source links above; [architecture and evidence](../../plans/100-language-independent-foundation/architecture.md), [strategy](../../strategy.md), [gap definition](../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap). Reassess against exact integrated revisions and the six journeys, with both positive and negative cases. An inability to recover work independently, differing authoritative edits, or a second writer overturns closure. Do not close on language adoption, a plan status or compilation alone.
