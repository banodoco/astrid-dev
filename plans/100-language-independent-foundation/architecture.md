# Native creative foundation — architecture proposal

[Plan 100](plan.md) · [Gap LS-006](../../vision/gaps/LS-006-independent-creative-foundation.md) · [Owner discussion / umbrella issue #2038](https://github.com/banodoco/astrid-dev/issues/2038)

**Disposition:** Direction agreed in owner conversation, 26 November 2026; this document and six project scopes are draft proposals pending independent critique and scope/release decisions. No product execution, spend or cutover is authorized.

## Why this matters

Astrid is not trying to be a fixed video editor. It is a creative environment in which people and agents continually add, compose and change tools. A fragile foundation multiplies the cost of every new modality, agent, provider and installation. A reliable, small and independently recoverable foundation makes the layers above it liquid. Rust is a proposed implementation choice because compiled native distribution removes interpreter bootstrap dependence, ownership and types can encode invariants, and native concurrency and efficient memory representation help CPU-heavy paths. Rust does not fix incorrect protocols, duplicated state, filesystem semantics, GPU drivers, cloud latency, or costly algorithms by itself. The user-facing goal survives choosing a different implementation.

## Source observations and their implications

Reviewed 2026-11-26 via GitHub source inspection. Observed snapshots (not the live release-16 integration tuple): Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`; Dev `890f8acafa2cd5b5e0b68dbc2d1576e0f7856202`. Reconfirm pins and branch status at each scope/run start. No runtime benchmark, native install, GPU or cross-platform test was run for this proposal.

| Observed source / historical report | Why it matters / design response |
|---|---|
| [Runtime contracts](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/contract/README.md) define language-neutral HTTP, generated Python/TS clients, handshake, idempotency, CAS and optimistic concurrency | Retain wire contracts, state authority and fixtures; make behaviour—not Python class names—the migration oracle. |
| [Agent generic host](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/execution/generic_host.py) imports runtime_protocol.platform, dirfd, errors, storage, verified_host_launch and external_pack_sources; [worker](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/execution/generic_host_worker.py) accesses verified source/custody | A wire-compatible Rust server is insufficient. Separate public worker ABI and any local platform-support library from private authority. Preserve verified source, native handles, lease/fence and scoped grants. |
| [Timeline provider](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_provider.py) imports astrid.sdk.timeline.commit.create_runtime_commit_service; [commit port](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_port.py) mediates scoped store access; [Agent semantics](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/commit.py) consume it | Extract pure deterministic editing rules and batch immutable context; avoid chatty per-leaf IPC or a second database writer. Runtime remains the sole commit authority. |
| [Shell bootstrap](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install), [Agent installer](https://github.com/banodoco/astrid-agent/tree/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/installer), [Runtime bootstrap](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/astrid_runtime/bootstrap.py), [local Vite launcher](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/scripts/dev-local-workspace.mjs) divide machine lifecycle; [profile services](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/docs/profile-services.md) currently bind a selected Python interpreter | Native bootstrap must be able to repair its managed dependencies independently, and one controller must own installation/version selection. Reuse current transactions via delegation during transition; transfer ownership atomically, never layer competing managers. |
| [Portability](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/docs/runtime-portability-testing.md) documents Linux pidfds, macOS audit-token custody, Windows Job Objects/handles and ACL/reparse-point rules | Preserve specific native guarantees; cross-platform libraries are not evidence of safe process termination or file custody. |
| Runtime tree has 103 Python implementation files under astrid_runtime/ and runtime_protocol/ (~3.98 MB source), ~400 Python/JS/TS test files (~6.4 MB); Agent installer ~0.91 MB; service.py ~660 KB, store.py ~486 KB, generic_host.py ~18,818 lines | A rewrite is not a small launcher change; split into cohesive crates, characterize behaviour before porting, avoid reproducing giant files. Counts are rough source inventory, not complexity or effort measurements. |
| [Plans 35](../35-one-home-for-user-state/plan.md), [38](../38-one-process-identity/plan.md), [62](../62-one-manifest-one-stack/plan.md), [29](../29-update-and-release/plan.md), [83](../83-execution-host-in-modules/plan.md), [94](../94-dependable-environment-setup-and-recovery/plan.md) document state drift, process identity duplication, version selection, update and worker decomposition issues | Reuse their landed results and test evidence. Never create another state store, install mechanism or source of version truth. Historical plans do not prove defects remain on the current release. |
| [Plan 81](../81-once-per-command/plan.md) reported 3.5–3.8 s timeline commands despite each Runtime request under 100 ms; [82](../82-reuse-across-commands/plan.md) identified repeated discovery/workflow work; [89](../89-heavy-saves-in-seconds/plan.md) measured 72–76% Python copy/compare on one candidate | Profile current integrated baseline. Remove repeated work and history-sized copies irrespective of language; native code must prove real installed end-to-end improvement. |

## Target design

```text
Hosted React | local bundled React | desktop shell | CLI | Python/TS SDKs | agents
                     authenticated versioned API + events
                                      |
               Rust workspace runtime (one authoritative writer)
               project/storage, edit commits, task/lease, grants, events
                   |             |               |
          native timeline     worker ABI      agent-session control
          pure Rust library   local/remote    provider adapters
                   |             |               |
          WASM preview        Python/Node/    Claude/Codex/custom
          (not authority)      native packs     agents/models
                                     
      independent Rust bootstrap/controller: manifest, environment,
      launch/attach, health, update, recovery, static UI, OS integration
```

A single user installation can ship several executables/crates: recovery/bootstrap must survive a broken core update; the core can run headless without any shell. Keep package management external where appropriate (uv, pinned artifacts, user-managed ComfyUI); don't build a package manager or inference engine. Managed services can own their own descendants within declared custody, not install/version authority. One native controller owns selected program versions, lifecycle and recovery; a workspace runtime owns durable project/task state. Credential grants, process identity and recovery transactions have explicit authorities, not shared mutable side files. External managers such as Pinokio keep their own exclusive installation ownership; delegate/attach or explicitly transfer, never silently adopt.

### Interfaces and timeline

React remains the extensible frontend. Production build static assets are served locally; hosted astrid.haus still connects through a separately qualified local connection/permission route. A desktop shell (Tauri vs Electron/other remains a choice after media/webview evaluation) displays the same React build, not a second product. Developers and agents can opt into Vite/HMR and independent UI/pack updates without compiling Rust. Node may still be required for builds, agents or Remotion, not for serving static production UI or workspace authority. Browser/desktop sessions keep per-client transient UI state while canonical project selection/preferences follow approved state ownership. Loopback binding, exact origin/handshake, least privilege, CSRF/local-network permission and remote pairing remain explicit; a same-origin local UI must not expose privileged credentials to web content.

Agents call the same generated Python SDK, CLI or MCP adapter; e.g. an illustrative batch trim/move/add operation becomes typed commands with project/timeline IDs, expected revision, idempotency key and permission context. The native authority validates, computes and atomically publishes one revision/receipt/event. The editor and agent receive the same outcome and conflict/refusal. Rust pure editing kernel defines frame/time/rational rounding, nested composition, command validation, dependency changes, undo and deterministic projections; Python/TS remain ergonomic clients. WASM or PyO3 bindings are optional for measured pure local preview/calculation, never direct persistence or an alternate authority. Preserve Remotion and custom elements as extension/rendering capabilities and define independent domain contracts so a future music/image/3D engine need not become a video-timeline fork. Rendering parity includes custom elements, time mapping, audio and readback, not only JSON equality.

### Agent and execution

The core owns durable session identity, scoped project/context references, admitted tasks, receipts, observable checkpoints, permissions and coordination. Provider-specific prompts, conversation formats and reasoning are owned by adapters; no automatic reconstruction of hidden state. A provider replacement explicitly resumes from supported checkpoint/project/receipt data, not a promise that all provider sessions are portable. Existing ACP/CLI/skills remain valid. Existing ComfyUI and Python tool ecosystems remain outside the native core, under declared capability and worker contracts. Reuse lease/fence, cancellation, idempotency and verified source identity, with real failure/expiry/cleanup proof. Agents do not get unrestricted shell/network/credential rights by being first-class. Resource budgets, sandbox policy and approval remain explicit.

### Local and remote

Same runtime source and public contract for local and headless deployment, with platform-specific packaging/adapters and explicit workspace custody. A local authority may delegate scoped execution to a remote worker; a fully hosted workspace is a different selected authority, not a hidden replica. No multi-master sync or transparent failover promise. Remote workers authenticate, use bounded input transfer, return verified results, reconcile interrupted execution, and enforce spend consent. Existing Plans 25/26 own actual cloud product journeys; Plan 32 owns placement and F-008 generation portability. Plan 105 proves shared core/worker deployment, not a second hosted product or scheduler.

## Requirements shared by all six projects

1. One canonical authority per resource and installation; make ownership transfer, startup, shutdown and recovery explicit; delete redundant paths after qualified cutover.
2. Existing user data, credentials, project identity, revisions, media CAS bytes, receipts and backups survive supported migrations; never downgrade schema silently, share simultaneous DB writers or erase data for compatibility.
3. Preserve public operations and negative guarantees; version changes deliberately, generate clients, and distinguish supported version matrix from internal implementation.
4. Native bootstrap/core starts with Python and Node missing/broken; managed dependencies provision with visible consent, verified sources, progress, cancellation, resume and safe rollback. Do not bundle GPU stacks gratuitously.
5. One UI codebase; browser/desktop/local/headless are access modes, not divergent features. Keep pack/React iteration live. Respect offline limitations of optional providers.
6. Explicit security model: process custody, grants, secret storage, filesystem boundary, origin and remote authentication; never weaken proofs to get parity.
7. Qualify supported Windows/Linux/macOS distributions, architectures and hardware explicitly; don't claim universal GPU support. Include Pinokio/external ownership where selected.
8. Separate black-box conformance from implementation unit tests. Run against pinned Python and Rust candidates in isolated roots with deterministic fixtures, actual installed journeys, negative/adversarial cases and performance baselines. Changes to expected behaviour require independent review, not wholesale golden regeneration.
9. The old implementation is a behavioral reference, not an architectural template. Modular crate boundaries, explicit domain separation and measurable invariants; don't reproduce service.py or generic_host.py as a single native monolith.
10. No GPU spend, production deployment or release promotion by planning alone. Cross-repo integration uses exact manifests, native artifact provenance/signing, rollback eligibility and reviewed evidence.

## Alternatives and sequencing

- Keep Python entirely: lowest disruption; optimize algorithms and process reuse, but recovery foundation still depends on a managed interpreter and private imports remain unless fixed.
- Only native launcher: useful independently and appropriate early; doesn't solve workspace authority or semantic duplication. Do not present it as full native core.
- Big-bang Rust translation: reject; high integration and regression risk, accumulated behavioural knowledge lost, no independently useful intermediate states.
- New modular native implementation behind existing contracts: recommended end state. Start with independent boundary proof (100), native distribution (101) and deterministic timeline engine (102); workspace authority cutover (103) requires their accepted interfaces and migration proof. Agent infrastructure (104) and local/remote parity (105) build on the shared core, with early adapters allowed against the reference contract. Parallel work must coordinate ownership and exact source pins.

Existing releases 15–18 remain the reference and active delivery path. Proposed 0.3 extensible-foundations target, after 0.1 dependability and alongside 0.2 performance work, before broad modality expansion; no committed deadline or release slot. Initial earlier conversational estimates (3–5 engineer-days audit, 5–10 launcher prototype, 15–30 production distribution, 15–30 boundary decoupling, 80–180+ runtime parity) were rough and overlapping, not scoped commitments. Re-estimate from an actual slice and test inventory; all new plans retain TBD until scope review. Infinite implementation capacity does not remove integration, hardware qualification or review dependencies.

## Review decisions still open

Independent advisor to challenge: whether LS-006 is distinct; whether the six scopes are independently useful or should be merged into existing plans; Rust core boundaries and pure timeline algorithm location; desktop renderer/media compatibility; process/custody and IPC design; data/rollback migration strategy; provider session semantics; local/cloud authority and reuse. Owner confirms per-plan scope and sequencing after review. No independent review or product proof has occurred in this planning conversation.
