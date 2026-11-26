# Investigation — an elegant, independently extensible Astrid foundation

[Plan 106](plan.md) · [Task index](tasks.md) · [Plan 100](../100-language-independent-foundation/plan.md) · [Proposed architecture](../100-language-independent-foundation/architecture.md) · [Inputs](inputs.md) · [Idea #2038](https://github.com/banodoco/astrid-dev/issues/2038)

**Purpose:** Before implementing new foundation abstractions or committing to a Rust rewrite, establish what makes Astrid difficult to extend today, what can be retained or removed, and the smallest architecture that lets a creator or an independent agent build, change, replace and share real creative tools. This is a standalone investigation project and a prerequisite for Plan 100's contract work, not another extension framework.

**Direction:** Owner requested this investigation on 26 November 2026 following agreement on the native foundation direction, then explicitly directed that it be its own plan. Detailed design, run, release, test-environment and review authority remain pending. No product changes, hardware rental, new trust grants, deployment or migration authorized by this document.

## The result we want

A small public vocabulary should explain nearly all creative contributions. Candidate nouns: resources (editable work), operations (typed intent and edits), views (interchangeable presentation), capabilities (compute and processing), packs (discoverable contributions). This is a hypothesis, not a demand for five new classes, registries or services. Existing concepts may already be better; require a real caller for each abstraction and remove redundant vocabulary where possible.

A contributor should be able to add a complete tool by describing what it provides, writing its actual creative code and interface, and teaching agents how to use it. Storage, permission enforcement, task execution, identity, revision/undo infrastructure, discovery, hosting and recovery should come from existing shared contracts. A built-in tool and an independent contribution should access the same supported creative operations; the core can retain genuinely privileged recovery, trust and authority functions. Native performance, correct data, and fault containment are requirements, not excuses for duplicate implementations.

The first domain is video, not a universal timeline-shaped data model. Test the abstraction against a layer/mask canvas or structured 3D scene. No claim that all domains share every edit semantic, renderer or interaction clock.

## Baseline, scope and method

Start with FI-1: resolve the currently shipped manifest, actual App deployment and candidate release tuple, verify source identities for Runtime, Agent, App and Pinokio, and identify retained branches that materially change the investigated path. Record differences instead of conflating main, installed and candidate code. Prior observations below are from Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, and Dev `97d6fbe7142168363446c52ed459e6bfb5e3aff9` (reviewed 26 November 2026). These are not the run pins. Follow a real source path rather than counting grep matches; include relevant VibeComfy, packs, timeline-schema and external providers only when a traced boundary requires them.

For each workstream trace creator or agent intent → public entrypoint → discovery/admission → owner/implementation → persistence or effect → receipt/event → observed UI/agent result → failure/recovery. Identify the exact caller, source path/symbol/line range and revision, contract/schema, resource/operation identity, state owner and trust boundary. Include a normal and adverse path. State what is verified by source, what is recorded historical evidence, what was actually run, and what remains hypothesis/unverified. A large file, many registries, multiple representations or an internal import are clues, not by themselves defects.

Use existing test inventories, fixtures and documentation to select the smallest discriminating check. This is a source investigation: product tests and isolated disposable prototypes are allowed only if a separately recorded run explicitly authorizes their environment and bounds. Do not change tracked product files, weaken assertions, open sealed holdouts, use user projects or secrets, execute arbitrary pack code outside approved isolation, rent GPUs, use paid providers or start any implementation task. Where a check cannot run, specify exact proposed input, command/route, observable oracle, and reason not run; distinguish an evidence deficit from a missing capability.

## Investigation lanes

The lane cards below elaborate FI-1–FI-8 in [tasks.md](tasks.md); that table alone owns progress and dependencies. Paths are starting points, not pre-approved change scopes. Assign focused read-only work in parallel after the baseline; the coordinator reconciles overlaps. No lane may turn into a broad refactor proposal without a specific user/contributor journey and decision it changes.

### A — Canonical identities, documents and operations (FI-2)

**Question:** Can a new creative domain share infrastructure without inheriting video semantics or inventing another store, transaction system or agent API?

- Read [Runtime document schema](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/contract/schemas/document.json), [canonical SQLite schema](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/canonical_schema.py), timeline commit provider/port/store, App dataProvider and operationHost, Agent SDK timeline and authoring rules.
- Trace one UI trim and one SDK/CLI trim through admission, preview, conflict, commit, undo, revision/event and reopen. Identify shared invariants vs video-specific rules, duplicated transformations, time/frame rounding, direct write alternatives, exact replay and dependency projection. Use [Plan 18](../18-timeline-editing/plan.md) as the existing command-layer owner; distinguish its accepted phase A from optional/deferred alternate view and gesture work.
- Trace one generic project document edit and a 3D package or canvas-like layer edit. Check opaque content vs typed schema/version, multi-resource atomicity, reference pin/follow semantics, extension-owned data and migrations (Plan 57), unknown types, schema changes and deletion/backup/restore. Do not assert arbitrary pack SQL or general transactions are supported merely because generic documents exist.
- **Deliver:** state and operation authority table, domain/core boundary, candidate smallest resource/operation contract, exact keep/adapt/remove candidates and safe migration constraints. Select a second-domain witness that can falsify a timeline-only abstraction. Explicitly name unresolved multi-resource semantics; no universal graph or generic CRDT unless real evidence requires one.

### B — App shell, views and the public SDK (FI-3)

**Question:** Can an independent tool do what a default view can do without importing or mounting the entire video editor?

- Inspect [SDK context](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/sdk/context.ts), [manifest](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/sdk/manifest.ts), [contribution kinds](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/sdk/video/families/contributionKinds.ts), [TimelineEditorShellCore](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/components/TimelineEditorShellCore.tsx), VideoEditorProvider, EditorRuntimeProvider, shared editorRuntimeAssembly, panesStore, selection and keyboard/focus routing, component registry and UI/theme primitives.
- Map direct built-in imports and hooks against supported extension surfaces: project/timeline context, selection and playback, resource binding, tool opening, menus/keybindings, drag/drop, clipboard, file pickers, viewport, modal/focus, styling, undo and diagnostics. Separate portable view primitives, video-domain services, privileged shell and device-local behavior. Identify genuinely shared provider assembly already present; do not copy it.
- Trace installed whole-tool and existing extension slot from manifest to mounted React component. Distinguish component definition/instance, domain resource, tool selection, presentation and runtime session. Verify whether a default component can be swapped using public hooks and what private dependency blocks it.
- **Deliver:** public-vs-private capability matrix for default and third-party views; proposed minimum portable host/SDK and video-specific module boundary; one alternative timeline view witness and one non-video view witness; what can be deleted or reused. Route layout/bind/open/focus to Plans 24/45/46, not a second framework.

### C — One contribution declaration and one operation vocabulary (FI-4)

**Question:** What must a contributor declare more than once, and can every caller discover the same typed action without handwritten adapters?

- Read [Agent pack v3 schema](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/pack/schemas/v3/pack.json), [agent index](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/pack/agent_index.py), discovery/registry/canonical/loader, [MCP server](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/mcp_server.py), CLI/SDK schemas and App extension manifest, agentToolRegistry, agentToolInvocationService/Adapters, family registries and runtime capability admission.
- Inventory by *fact*, not registry count: pack/action ID, version, input/output schema, permissions/effects, documentation, operation handler, UI contribution, available target/engine, lifecycle and dependency identity. Trace one built-in operation, one pack-defined backend action and one frontend/session-dependent tool across React, Python SDK, CLI, MCP and agent discovery. Note when a transport is intentionally different (e.g. UI target requires active session) but should project the same definition. Determine actual supported versus reserved/deferred paths.
- **Deliver:** declaration→projection map, example minimal pack using actual current public format, duplicate-definition and drift inventory with owners, minimal changes and deletion list. Choose one canonical source for each fact; generate projections where justified. Retain specialized indexes and caches when derivative and invalidatable; don't consolidate all registries into a god object. Keep Plan 18 pack-op semantics and Plan 06 lifecycle.

### D — Durable state, UI targeting and recovery (FI-5)

**Question:** Does changing a tool, browser, session, machine or agent leave creative work and explicit preferences intact?

- Inspect [extension state repository](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/runtime/extensionStateRepository.ts), IndexedDB/provider variants, SDK settings services, settingsStore, timelineStore, commitOutbox, project selection and view/session stores. Trace Agent project config/side files, Runtime documents/app-state/selections, cache and credential paths. Use [Plan 35](../35-one-home-for-user-state/plan.md) and [Plan 36](../36-one-credential-path/plan.md) as ownership inputs; verify live implementation before proposing change.
- Classify every load-bearing value: authoritative creative resource, saved workspace/layout/binding, user preference, per-device bootstrap, per-client transient focus/playback/selection, durable pending outbox/draft, cache, secret or receipt. For each, specify owner, lifetime, version, replication or invalidation, backup and recovery. Never silently delete unsent edits or state just because another copy exists.
- Trace agent open/bind/arrange/focus with explicit target session/client, active component mount acknowledgement, stale/disconnected/headless behavior and human conflict. Distinguish open existing vs create resource vs run a capability vs activate new code.
- **Deliver:** state ownership and lifecycle matrix, side-store removal/migration list, reconnect and live-swap failure cases; identify what Plan 35/46/63/76 already owns. No new global browser store or shadow database.

### E — Extension execution, live authoring and trust (FI-6)

**Question:** Can agents create and update useful software while artists work without giving arbitrary code uncontrolled authority?

- Read [App trust/security](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/docs/extensions/trust-and-security.md), [extension loader](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/runtime/extensionLoader.ts), dynamic registry, activation transaction/lifecycle/disposal, package build and module delivery, React singleton/shared imports, Agent pack install/permissions/transaction, worker source verification/custody, [Plan 78](../78-live-custom-element-editing/plan.md), [Plan 15](../15-openshell-safe-execution/plan.md).
- Trace source edit → dependency resolution → compile → artifact identity/admission → mounted view → action/worker → hot update → failure → fallback. Compare hosted, local and dev routes; inspect native IPC exposure, origin/CSP/CORS, token access, per-extension network/DOM/storage, install scripts, backend child/process/file access and permissions/revocation. Existing trust docs explicitly say extension modules share the App browser realm; same-origin code admission and error boundaries do not equal sandboxing. Distinguish the world-preview iframe from normal extensions; preserve trusted personal project-pack behavior and exact pinned render references.
- **Deliver:** trust/authority and fault containment map, practical authoring flow, supported vs unverified security claims, smallest isolation and artifact-hosting alternatives with performance/ergonomics tradeoffs, bad build/mount/update/rollback and denied-grant probes. Reuse Plans 06/41/47/78 and 15; do not add another extension manager or grant model. Security review is mandatory before later implementation.

### F — Rendering, media, playback and interactive performance (FI-7)

**Question:** Can creative domains and alternative views share reliable media identity and result reproduction without forcing a common renderer or slow interactive path?

- Inspect [Agent rendering contracts](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/rendering/contracts.py), Remotion runtime, rendering schemas/provenance/replay, [Three.js authoring](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/rendering/ui/threejs-live-editor/authoring.ts), App preview/playback/asset adapters, shaders/effects/clip renderers, frame/sample/time mappings, Runtime CAS and range/linked-media/verified snapshots. Check existing Plan 27, 69, 75, 79/80, 85–89, 99 proposal if it exists at the pinned source; do not assume an unmerged plan is assigned or available.
- Trace a custom element and a 3D scene into a timeline preview and offline render, including asset/renderer versions, time mapping, live-vs-pinned dependency, GPU/CPU placement, cancellation, provenance and old revisions. Examine cache invalidation, memory copies, binary formats, large assets, seeking, brush/viewport input cadence, audio device clocks and backpressure. Separate transient high-rate preview from meaningful committed edit; no RPC per frame, pointer sample or audio callback.
- **Deliver:** contract and renderer/clock ownership map, reusable media primitives vs domain-specific ones, real performance discriminators and failure probes, preview/final render parity acceptance, no speculative performance numbers. Keep specialized GPU and native libraries; Rust alone does not fix algorithmic duplication or browser media limitations.

### G — Process, installation, local/cloud and provider boundary (FI-8)

**Question:** Can the foundation genuinely survive the loss of its optional environments and expose the same capabilities on different machines?

- Trace App bootstrap/development launcher, Agent installer and lifecycle bridge, Runtime bootstrap/daemon/services/door/local+remote worker composition, process custody, release manifests/locks and Pinokio ownership. Inspect Agent ACP/chat lifecycle and Runtime callbacks; use [architecture](../100-language-independent-foundation/architecture.md) pinned findings. Identify every private Runtime import and in-process semantic provider crossing with owner and minimal public contract. Include Node/Python dependency assumptions, OS handles, platform filesystem and credential protection, reconnect, runtime recovery and source identity.
- Trace same task through local and remote workers and a hosted/local client. Distinguish workspace authority from scoped worker, provider-specific session state, explicit grants and spend/transfer. Check state, versions, packaging, update/recovery and permission changes with a failed Python/Node environment or closed UI. Reuse Plan 29/38/62/83/93/94 and 25/26/32; never replace a user-managed install silently.
- **Deliver:** cross-repo dependency and lifecycle ownership graph; retain/reuse/move/remove disposition per boundary; smallest independent bootstrap/worker/agent handoff probes; migration and rollback constraints for Plans 101/103–105. Do not reimplement platform security or start Rust merely to prove a design.

## Independent-tool and second-domain test design (FI-9)

Use a fresh contributor or coding-agent session with only the documented public pack/SDK interfaces and a pinned isolated test workspace, not core source or privileged helper imports. First attempt a small useful tool (e.g. lighting controls for a scene or image-layer inspector), then an alternative timeline/other-domain view, or a separate lightweight canvas/scene resource if supported. The investigator knows the product; the independent author must not be coached around a failing API.

| Journey | Acceptance oracle (design now; execute only if authorized) |
|---|---|
| Discover and open existing resource | Stable project/resource ID, correct active view and actual mount acknowledgement, no private imports or duplicate project model |
| Extend an existing view and create a whole React tool | Public pack/SDK only, supported typed action visible to human and external agent with declared permission/effect |
| Apply a real edit or task | Same authority, receipt, event, revision, undo and readback as default path; reject invalid/stale/unauthorized inputs |
| Swap view and return to default | Same data, history, in-flight state and compatible layout, no migration or special privilege |
| Change tool source while in use | Verified revision and live update or explicit refusal; bad build/mount retains last working state; old render pins unchanged |
| Reuse on second workspace or route | Same pack identity/artifact and declared deps, qualified local/hosted path; no core rebuild or bespoke glue, no private data upload |
| Try different domain | No timeline-shaped data or video-only public imports for independent operation and view; explicit domain semantics |
| Failure and scope | Broken dependency, disconnected/wrong session, denied grant, incompatible version, absent optional service produce truthful outcomes and no data loss |

Measure rather than optimize vanity counts: number of handwritten source/config files *needed for the actual tool*, duplicate declarations of the same fact, integration-only code and concepts/API families learned, private imports, core modifications, separately maintained adapters, clean-build/activation/reload and rollback steps, first-use time, and relevant interaction/commit latency where measured. Record tool-specific creative code separately from glue; report baseline and proposed comparison with exact definitions. Do not use arbitrary LOC, file-count or performance thresholds as a reason to weaken security or behavior. A failure is valuable evidence; record the smallest missing public affordance and how to reproduce it instead of repairing product during this investigation.

## Required evidence and decision pack (FI-10)

Publish a compact, reviewable evidence pack under this project when the run is authorized, with separate lane notes only where useful and one integrated conclusion. Every recommendation must link exact source evidence or an actual probe; no broad survey with no decision.

1. Exact source/contract/installed matrix, investigated caller paths, supported/deferred/unverified classification and evidence limits.
2. One map of concepts and authority (public and internal), one contributor journey map, and actual current-vs-proposed dependency/registration paths. Show how the same operation reaches React, Python, CLI/MCP and worker; label legitimate platform/session differences.
3. Findings table: finding ID, observed/derived/hypothesis classification, source SHA/path/symbol/line or run receipt, concrete effect, affected users, current owner, risk, smallest discriminating check, and proposed disposition.
4. Consolidation ledger: keep as-is, reuse existing work, extract/generalize, replace, delete, or defer; name each redundant owner/declaration/route/file and what takes over, prerequisite, preserved invariant and removal proof. Do not keep a duplicate indefinitely under a new adapter name. Count *authoritative* declarations and concepts, not all derivative indexes.
5. Compare at least (a) retain/refactor current implementation, (b) native bootstrap plus contract extraction, (c) parallel modular Rust replacement after parity; compare small domain seam vs generalized engine, default view substitution vs privileged host and actual trust alternatives. State what would falsify each preference; choose the least complex sound approach, not the most Rust.
6. Independent-tool test specification, exact evidence baseline, smallest second-domain witness and reusable behavioral/negative corpus for Plan 100's NF-2/NF-3.
7. Dependency and work routing table linking existing projects 18/24/35/38/41/43/45/46/47/57/62/63/75/78/83/94 and proposed 100–105, as applicable: which work is already accepted, which is reused, which needs a new scope decision or genuinely new task. Re-estimate in engineering days, identify critical path and parallel lanes, avoid charging prior accepted work twice.
8. Owner decision brief: no more than ten consequential decisions, recommended alternative with tradeoffs, what is deliberately not built, concrete elegance test, migration order, unresolved blockers and which vision/gap closure evidence should be refined (not closed). No automatic project/release assignment.

Use the independent reviewer specified in the shared run contract, not the investigating author, to examine evidence and challenge unnecessary abstractions, missing security/authority boundaries, accidental video special cases, misleading performance assumptions and duplicated implementation. Review actual sources and proposed removals rather than just the synthesis. Reconcile rejected/accepted findings and keep open decisions explicit. Plan 100's NF-2/NF-3 may consume the accepted investigation baseline only after Plan 106's independent review and owner disposition; Plan 100 still has its own contract review RS1.

## Effort and stop rule

Planning allowance: **8–12 engineering days** for read-only pin/trace, seven bounded lanes, independent-tool test design, synthesis and independent critique; parallelizable once the source tuple is pinned. This effort was previously included within Plan 100's provisional 20–40 days. Separating it into Plan 106 leaves Plan 100 at 12–28 days provisionally (8–12 plus 12–28 = 20–40); re-estimate both from evidence, without double counting. Re-estimate after FI-1; actual separately authorized product probes may change effort. Stop when the high-risk decisions are source-backed or explicitly blocked with a discriminating next check; do not audit every file or build a new framework to resolve uncertainty. No product implementation, new project/vision-gap scope or release allocation follows automatically.

## Planning references

[Vision — Agent-Powered Liquid Software](../../vision/pillars/liquid-software.md) · [Open by design](../../vision/principles/open-by-design.md) · [LS-003](../../vision/gaps/LS-003-full-stack-contributions.md) · [LS-004](../../vision/gaps/LS-004-cross-modal-foundations.md) · [LS-005](../../vision/gaps/LS-005-agent-managed-tools.md) · [LS-006](../../vision/gaps/LS-006-independent-creative-foundation.md) · [Planning workstream](../../agent/shared/workstreams/plan.md) · [Shared run contract](../../agent/shared/run-contract.md).

No product proof or independent critique is claimed by creating this plan. Update the existing vision/gaps with evidence and a boundary assessment only after investigation; avoid a separate "elegance" gap if the existing creator/contributor outcomes can be refined.
