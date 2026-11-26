# A language-independent foundation

**Project:** A language-independent foundation

**Goal:** A separately built client and worker can use Astrid's real workspace and task operations through documented contracts without depending on the core's private implementation.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Provisional 20–40 engineering days, including a thin second-domain witness and the first investigation slice (8–12 days within this allowance); re-estimate after source inventory and independent scope review.

**Waiting on:** Independent architecture and gap-boundary review, owner scope decision and release placement; pin the current integrated reference and coordinate Plans 38 and 83.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Full-stack contributions](../../vision/gaps/LS-003-full-stack-contributions.md) (supporting) · [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting)

**Contributes to closure:** LS-006: E1: independent client/worker contract and behavioural reference.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Make the real product boundaries language-independent, not merely the public HTTP surface. Inventory and classify every private Runtime import from Agent, dynamic authoring-provider callback, OS custody handoff, installed source identity, worker/session protocol and lifecycle/manifest assumption. Include App and Pinokio entry points where they depend on implementation detail. Reuse workspace.v1, generated Python/TypeScript clients, current schemas, service declarations, scoped credentials, process identity and worker lease/fence invariants. Split genuine local platform support from authoritative Runtime operations; preserve retained native handles and pre-import source verification.

Deliver one versioned client/worker contract, a separately implemented client and simple worker that exercise real state/task/receipt operations, and a differential conformance harness usable against Python and a later Rust implementation. Define observable contract errors, idempotency, canonical serialization/digests, opaque revisions, permission scopes, cancellation, events and crash/expiry behavior. Characterize the timeline provider seam and design a batched immutable-input/pure-result boundary for Plan 102; do not port timeline semantics here. Define machine-level ownership and handoff contract with Plan 101; no competing launch or update path.

Define a minimal shared creative-resource and operation envelope from real timeline behavior and one bounded, genuinely different resource witness (canvas layers or structured 3D scene). Resource identity, revision/receipt, grants, storage and events are shared; each domain owns data representation, validation, edit and undo/conflict rules, renderer and extension capabilities. A separately implemented Python/TypeScript service or pack must be able to register a domain with no core fork or Rust requirement. Coordinate Plans 43, 45 and 57; no universal timeline model, generic graph platform or full non-video editor. Plan 46 owns agent workspace commands over Plan 24 component instances and Plan 45 bindings; expose the common target/authority contract without implementing those layout operations here. The common domain contract must support multiple interchangeable views, including an independent pack-authored React tool or alternative view over the same canonical resource; never require Rust or core-private imports for frontend authoring. Plan 41 owns the agent authoring/maintenance journey and Plan 47 the pack qualification. See [agent-authored tools](architecture.md#agent-authored-tools-and-replaceable-default-interfaces). See the [multimodal and workspace design](architecture.md#creative-domains-one-resource-contract-separate-engines).

Out: replacing the workspace store, building an inference engine, generic IPC for its own sake, rewriting the editor or deleting Python worker support. Keep implementation-specific unit tests and add public behavioural fixtures; do not weaken current required gates.

## Existing work and decision

The current Runtime already owns the public protocol and generated clients, but Agent generic_host directly imports runtime_protocol.platform, dirfd, errors, storage, verified_host_launch and external_pack_sources; Runtime loads the Agent's synchronous timeline commit provider. Plans 38 and 83 consolidate process identity and decompose host behavior; use their qualified work, not another implementation. Plan 50's recorded boundaries and Plans 39/91's green gates provide reusable evidence. The [shared architecture rationale](architecture.md) records concrete source identities and alternatives. See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

Start with the [bounded architectural investigation](investigation.md) (NF-1a–NF-1j): source-backed traces of the SDK, default tools, contribution/operation discovery, state, trust, rendering and deployment; independent-tool and non-video witness design; explicit keep/reuse/remove dispositions and independent critique. Pin the real integrated tuple first. The investigation is read-only by default and is a prerequisite to the contract and conformance design; no product implementation or tests without the appropriate recorded authority. Then agree the contract and the independent conformance harness; then remove private authority imports in small parity-proven slices, preserving the current product. Deliver an independent consumer and worker before declaring the seam ready. Plan 101 may prototype its bootstrap in parallel, but ownership transfer depends on the accepted lifecycle contract; Plan 102 consumes the reviewed timeline seam. Plan 103 consumes the complete conformance baseline. Review migration scope before any code starts. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes a frozen integrated Runtime/Agent/App tuple, current workspace.v1 artifacts, Plan 38's identity/custody contracts, Plan 83's characterization and the recorded boundary fixtures as available. Produces a dependency/ownership inventory, public client and worker ABI, lifecycle and timeline-boundary design, executable black-box suite with negative fixtures, exact versioned contracts and independent consumer/worker receipts. Plan 103 must run the same suite, not a rewritten weaker version.

## Completion

- A clean independent consumer with no private Python Runtime imports creates/reads an actual project, submits a typed capability task, reads the same output and receipt through a second client and exercises event delivery.
- Independent worker claims, settles, cancels and recovers a task; stale fence, unauthorized grant, duplicate receipt and incompatible version are rejected or reconciled exactly as the reference specifies.
- Static import and process-boundary checks catch planted private-authority dependencies; genuine platform support is explicitly allowlisted and tested, not moved into a second authority.
- Characterize current reference and preserve native custody checks on the supported three OSes; report unqualified paths, not a blanket compatibility claim.
- A bounded non-video domain witness and the timeline both use the same resource identity, authorization, revision and event path; invalid/stale edits refuse, an independent contributor can implement the witness without changing core, and it does not inherit timeline-specific semantics. No full image/3D product proof.
- An independent reviewer accepts the contract, ownership table and parity corpus. No Rust server parity or new install route is claimed yet.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
