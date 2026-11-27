# Large local media

> **Planning revision — 27 November 2026, under review.** This is the proposed Release 16 execution contract, replacing conflicting original and appended dispatch wording. Accepted owner decisions remain in [inputs.md](inputs.md#owner-decisions). This revision authorizes no implementation, integration or publication and claims no new product proof.

**Project:** Large local media

**Goal:** A creator or agent imports supported local media up to the Runtime's configured per-object limit, places it once, and can save, reopen and use it without changing the original file.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 6–9 implementation person-days plus 2–3 integration, installed-qualification and review days; 8–12 remaining in total, excluding venue wait and unrelated release repairs

**Waiting on:** Lead dispatch and exact R16 base/pin selection; only affected consumers wait for the LM-1 stream/metadata contract, P63 placement handoff and P29/P35 custody interfaces. P77 and P88 are landed predecessors, not whole-plan start gates.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six fields above feed the generated [catalog](../index.md); do not edit the catalog directly.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Retain one managed-copy import path. The Runtime owns the size decision; 5 GiB is its current default ceiling, and configuration can lower it. The limit applies to each object, not to the aggregate project. Supported formats remain locally decodable within existing decoder safeguards. Astrid reads the original without moving, editing or deleting it.

The first-release blockers are bounded Agent streaming; truthful configured-cap refusal; exact catalog selection and intrinsic metadata; ordinary image/audio/video placement; and custody across interrupted import, pending placement and reload. Keep these within LM-1–5, followed by LM-6 and the existing final review.

The Runtime already stages and hashes streams, publishes managed objects, settles catalog pairs and looks up import operations. P77 supplies parked-drop UX and concurrent drop tracking; P88 supplies media swap/verified-edit behavior; the App already has a shared reload guard. Reuse these mechanisms. None by itself completes an LM task. The source facts and merged/unmerged credits are in [inputs.md](inputs.md#verified-baseline-and-reconciliation).

**Included:**

- Sized streaming through the existing generated client and every promised Agent add, replacement, cached/batch and detached-authoring route; bounded memory and stable source identity throughout probe, hash and send.
- Runtime-only size policy, with a consistent refusal naming its configured limit; no duplicate Agent/App byte ceiling. Keep authentication, format, decoder and path restrictions.
- Intrinsic dimensions/duration derived or validated from the same staged bytes through existing Runtime admission; carry those facts and the exact catalog selection through native image/audio/video placement.
- Handle placement with exact zero/one/many catalog behavior, unchanged `astrid media import` output, and no guessed selection or cross-project access.
- Recovery using the existing import operation and P63 placement custody; completed import is reused, placement retry does not upload again, and unknown outcomes remain visible.
- D4's browser warning and explicit reselect/discard after lost in-memory bytes, with the existing App reload/update gate covering the entire import-to-placement lifetime.

**Deferred or excluded:** P80 clones and external path links, new upload endpoints or stores, giant browser-byte persistence, resumable byte-offset infrastructure, proxies, a general quota/reservation system, new metadata schemas, generated-media limits and remote-machine uploads. An inability to satisfy the existing interface is a concrete decision to escalate, not permission to introduce a parallel mechanism.

## Sequence and readiness

1. LM-1 can begin on an authorized base: existing Runtime client streaming and bounded intrinsic-metadata admission. The separately reviewed Agent pin follows D5.
2. LM-2 consumes that client/pin. LM-3 catalog/handle inventory can begin independently; its affected stream consumer lands after LM-1/2.
3. LM-4 App producer and LM-5 guard work can begin independently. Agree the actual shared handoff/guard functions with P63/P29/P35 before their affected landings; sharing a file alone does not serialize work.
4. Exercise one early import → placement → lost-ACK recovery → undo → reopen → short-render witness on an explicit interim tuple. LM-6 revalidates affected evidence on the final frozen tuple, then R reviews the combined result.

All product changes belong to the Lead-selected Release 16 branches and tuple. Record actual branch heads and Runtime/Agent pin transitions at dispatch. Historical R15 branch names are not current instructions. This planning revision neither starts a run nor assigns an existing active branch to a second writer.

## Interfaces and handoff

Use the [P63 shared import and placement contract](../63-dependable-saving/plan.md#shared-import-and-placement-contract) as the single cross-project lifecycle definition. P79 owns the import operation, bounded recovery metadata, source identity, catalog receipt and producer. P63 owns captured placement intent, exact commit-attempt key/bytes, outbox, save outcomes and undo. P29 supplies the existing reload/update guard; P35 owns recovery-state location and migration. CC-10 judges their integration rather than building another importer or queue.

The existing `POST /v1/projects/<id>/media-imports` and operation lookup remain the transport and recovery boundary. A completed import is reusable without retransmission. A pending object/catalog operation may require the original bound metadata and bytes under the same key; do not promise zero-transfer settlement or restore a missing browser `File`. Preserve accepted objects and existing operation replay compatibility. If the original placement target disappears, retain the imported media and ask for a new location.

Browser recovery retains the original request options and subsequently learned Runtime content identity. No browser prehash is required. Replay preserves the original presence or absence of `expectedDigest`: adding it after learning the receipt digest would change the existing replay fingerprint. A reselected file with identical name/type/size but different bytes must fail Runtime's existing content binding. Without a content-bound receipt or the original bytes after forced close, preserve the unresolved operation and report the recovery limit; do not falsely claim an exact reselect.

P87 owns rendering/projection correctness; P79 supplies verified media facts and one actual output witness. P85 supplies existing measurement tools. P63/P04 supply independently judged saving/concurrency acceptance using the shared imported-media witness. Their implementation effort is not counted again here.

## Completion

- **Source implementation:** LM-1–5 preserve existing accepted behavior and focused negative tests, exact catalog/digest identity and original file bytes/path/modified time. Detached apply still checks all inputs before the first mutation; a later upload failure causes no timeline commit. Earlier accepted catalog imports may remain visible and reusable, without claiming all-or-nothing catalog publication.
- **Installed use:** a real playable file larger than 1 GiB is imported by CLI and editor drop, saved, reopened and played on the exact installed tuple. Include supported audio and a non-square/portrait video with correct duration, geometry and source offsets, plus handle placement and a short render that actually uses the imported media after the original is unavailable.
- **Memory:** absolute Agent peak resident memory stays below 256 MiB for both the 300 MiB focused case and the greater-than-1 GiB CLI witness. Record baseline/incremental memory, probe-process and Runtime/App peaks, elapsed time and allocated temporary disk as diagnostics; do not substitute them for the absolute gates.
- **Refusal and failure:** real HTTP checks at a lowered configured cap cover below/at/above the boundary and truthful size errors. The Runtime refuses declared oversize before reading the body; do not promise that clients send no bytes. Source mutation/truncation, short body, digest mismatch and disk exhaustion fail safely, preserve originals/accepted work and clean only owned partial stages.
- **Recovery and reload:** cover interruption before acceptance, object accepted/catalog pending, completed catalog with lost reply and placement with lost commit reply. Lookup precedes retry; no duplicate catalog/placement, blind fresh import, false Saved or loss of unrelated edits. Panel/drop active and parked states share the guard. Forced browser reload/crash shows the recoverable receipt or truthful exact reselect/discard; browser warnings can be overridden.
- **Qualification ownership:** retain one primary OS for P79's full large-media witness. Existing [R16 qualification](../../releases/16.md#proposed-support-and-negative-acceptance) supplies targeted Windows/macOS/Linux coverage and shared P63/P04/P87 receipts. A source check or one-OS result is not an all-platform pass. The P88 large-shots fixture issue #1916 is a predecessor only if that fixture is selected; no new full-film harness is required here.

One final independent review remains accepted. D1/D4/D5 remain decided; D2's unmerged interim donor and any conditional need for a new interface are recorded in [inputs.md](inputs.md#remaining-decisions-and-limits). No acceptance gate is waived by an estimate or by source presence.
