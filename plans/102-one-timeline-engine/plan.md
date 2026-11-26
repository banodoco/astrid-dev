# One native timeline engine

**Project:** One native timeline engine

**Goal:** People and agents can make the same timeline edits through the editor, Python SDK or CLI with identical authoritative semantics, responsive previews and dependable history.

**Status:** queued

**Owner:** Unassigned

**Target milestone:** 0.3

**Estimate:** Provisional 30–60 engineering days; re-estimate against exact accepted command corpus and reference.

**Waiting on:** Plan 100's reviewed authoring seam; independent scope and release placement; pin accepted Plans 63/75/76/77/89 and Plan 88 reference.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting) · [Sustained creative work](../../vision/gaps/AA-001-sustained-creative-work.md) (supporting)

**Contributes to closure:** LS-006: E3: one deterministic timeline semantics and canonical commits.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Extract deterministic timeline operations into a cohesive Rust library, separate from storage, rendering, provider calls and UI. Establish a versioned typed command corpus for trim/move/split/insert, nested composition, time/frame/rational rounding, edit validation, dependency updates, inverse operations, history/revisions and deterministic projections. Preserve existing schemas and open extension payloads, media identity, custom elements and renderer inputs. Do not require future modalities to inherit video semantics. Timeline is the first substantial domain of Plan 100's common creative-resource contract. Expose typed operations and resource/view bindings to both SDKs and the Plan 24/45/46 workspace; a timeline engine must not own window layout, generic component mounting or the data model for canvas, 3D, writing or audio. The thin second-domain witness may proceed with Plan 100; do not fold full canvas implementation into this plan.

Python SDK/CLI/MCP and React/TS SDK submit the same typed batch (project/timeline IDs, expected revision, idempotency and authority context). The authoritative Runtime admits, checks permission/conflict, computes or verifies the result, atomically commits one revision and emits a receipt/event. During transition the Python runtime may call the pure Rust kernel via a bounded binding; explicit immutable input/output or in-process native binding avoids per-leaf IPC. WASM/PyO3 pure previews/calculations are optional where measured useful; a preview never writes canonical state. Browser optimistically updates and reconciles authoritative outcomes, not a separate implementation of editing rules.

Reuse Plans 63/75/76/77/88/89 and Plan 18 behavior and timings. Preserve approved conflict/undo semantics and never weaken copy/compare bounds; profile current candidate and measure real commands/saves. Retire duplicate deterministic rules only after parity; leave Remotion, FFmpeg and dynamic custom rendering in their appropriate services.

Out: all workspace DB authority (Plan 103), a new video renderer, full new editor, rewriting every creative pack, generic timeline semantics for music/3D before requirements exist.

## Existing work and decision

Runtime dynamically loads astrid.sdk.timeline.commit.create_runtime_commit_service; RequestCommitPort mediates in-process Python access, Agent commit.py implements renderer-independent editing. Existing contract/commit-v2 and schemas record rich acceptance/undo/closure semantics. Plan 89 reported copy/compare costs on a historical candidate; Plan 81 found fast individual runtime requests but slow total commands. Optimize algorithms and process reuse independently of language; see [architecture](../100-language-independent-foundation/architecture.md). See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

Pin actual supported command/commit schemas and accepted reference, capture deterministic vectors and heavy timeline fixture; isolate pure rules and review semantics/rounding and transaction boundary; implement Rust kernel and adapters in bounded slices; differential test before swapping the reference provider. Plan 103 consumes the proven kernel for authoritative Rust commits; no independent DB writes from bindings. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes Plan 100 authoring boundary, pinned Agent edit-command schema, Runtime timeline-commit contract, timeline-schema package and corpus from Plans 63/75/76/77/88/89. Produces native pure library/ABI, deterministic cross-language fixtures, Python/TS clients and optional WASM preview, reference-provider parity receipts and installed save/preview/render evidence. Plan 103 consumes exact crate version and commit coordinator contract.

## Completion

- Python SDK, React editor and direct typed client apply identical command corpus against independent roots; compare authoritative projection, revision, inverse/undo, frame/time rounding, nested composition, extension preservation and renderer input/readback. Include real representative timeline edits and render evidence.
- Invalid/stale/conflicting edits return documented outcomes; permission denied, crash during commit, retry with same key and concurrent disjoint writes preserve existing guarantees. Preview has no authority to commit.
- Heavy timeline benchmark records current baseline and candidate, median/tail end-to-end edit/save plus CPU/memory and history growth; no regression against accepted Plans 75/86/89 gates. Do not promise a speedup solely from Rust.
- Cross-language fixtures catch planted rounding or validation drift; verify no duplicate authoritative edit path after cutover. Existing undo/restore/custody tests remain meaningfully covered.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
