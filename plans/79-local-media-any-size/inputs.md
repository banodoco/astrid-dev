# Inputs — Large local media

> **Planning revision — 27 November 2026, under review.** The owner authorized reconciliation of planning records and one documentation PR, not product implementation or merge. Proposed amendments below do not create execution authority or retrospectively accept scope changes.

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner authorized this planning reconciliation, preserving accepted D1/D2/D4/D5. Next: review the canonical correction and D2 disposition; no implementation is dispatched here.

**Prior art:** On 21 November 2026 the owner requested the project and accepted managed-copy streaming, the revised scope/estimate and D1/D2/D4/D5 in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG). The complete prior rationale, alternatives, independent critique and owner wording are preserved in [inputs at 2b43946a](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/79-local-media-any-size/inputs.md); prior [plan](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/79-local-media-any-size/plan.md) and [tasks](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/79-local-media-any-size/tasks.md) preserve original acceptance and progress.

**Challenge:** Reviewed — [observation #2059](https://github.com/banodoco/astrid-dev/issues/2059), [SC-79](https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md), [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md), current records and [R16 scope](../../releases/16.md) were independently checked against source. Principal gaps were already identified by SC-79. Metadata-admission, swallowed-persistence and receipt-selection findings refine existing tasks rather than create workstreams.

**Approach:** Managed-copy streaming through existing Runtime import/settlement. In-place references and clone-first storage remain P80; existing native placement, outbox, guard and measurement mechanisms remain their owners' implementations. Deliver reliable import/placement/recovery without a new media architecture.

**Proof and limits:** The [verified baseline](#verified-baseline-and-reconciliation) credits source and merged work only. No product tests or installed witnesses were run here; LM-6 retains real large-media, memory, recovery and output qualification.

## Verified baseline and reconciliation

Source/PR checks on 27 November used Agent R16 `4a2bad187f12e7b0d1ba5bd1164b4a076787516a`, Runtime R16 `55a541a7ab904873e63510e581a60742e1b83fb8`, App main `cc1d48f016fde55ad6b0609c619d8a4bcec56823` and Dev main `2b43946a85f63a0a114023e271baf4952ed209c2`. These are inspection identities, not an installed/served release tuple. No product tests, uploads or native proof were run for this revision; bounded open-PR search is not exhaustive execution inventory.

| Finding / evidence | Planning consequence |
| --- | --- |
| Runtime [template](https://github.com/banodoco/astrid-runtime/blob/55a541a7ab904873e63510e581a60742e1b83fb8/generators/python_client_template.py#L1185-L1212) has sized object streaming but `import_project_media` still calls `bytes(data)`. Existing staging/CAS/import operation remains. | Keep LM-1 at `python_client_template.py`, not stale `generate.py`; regenerate, preserve bytes compatibility and pin separately. No replacement uploader/store. |
| Agent [_metadata](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/authoring_media.py#L108-L143) still applies 64 MiB and reads whole bytes; [detached apply](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/authoring_media.py#L580-L652) holds all payloads. [Handle selection](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/timeline/media_add.py#L38-L85) refuses zero/many catalog matches. | LM-2/3 remain. Preserve all-input validation, distinguish timeline atomicity from independently accepted catalog imports, and use exact selection/retry rather than deduplication by digest alone. |
| Open draft [Agent #475](https://github.com/banodoco/astrid-agent/pull/475), head `3f79b2c537776b7e5c44d9a9c146a5a9c4c4307e`, contains the [1 GiB constant](https://github.com/banodoco/astrid-agent/blob/3f79b2c537776b7e5c44d9a9c146a5a9c4c4307e/astrid/sdk/authoring_media.py#L20-L33); it is unmerged. | D2 is authored elsewhere, not delivered. No competing stopgap assignment or wholesale merge of the broad donor. |
| Runtime [request/probe/settlement](https://github.com/banodoco/astrid-runtime/blob/55a541a7ab904873e63510e581a60742e1b83fb8/runtime_protocol/service.py#L5918-L6200) validates numeric caller metadata and decodability but does not carry probe facts into catalog settlement. | Correct the old claim that only callers fall short. LM-1 derives/validates intrinsic facts inside existing admission; LM-4 propagates them. Existing fields and operation replay remain compatible; no new schema or retroactive accepted-history rewrite. |
| App [preparation](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L1411-L1498) creates a key per call and suppresses native selection for `prepareAsset`; [recovery](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L1753-L1802) swallows persistence failure, recovers completed receipt, or retransmits pending bytes. | LM-4/5 retain one import operation and truthful bounded metadata custody. Completed receipt reuse differs from pending settlement; no promise to restore browser bytes. Duplicate-import risk is source-supported, not newly reproduced. |
| [Drop](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/lib/external-drop-utils.ts#L465-L570) retries upload-and-place; audio lacks exact selection and [handoff](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts#L746-L766) still guards ordinary non-image placement out. | LM-4 needs producer plus bounded native handoff repair, not merely removal of an image predicate. P63 owns shared placement custody. |
| [App #309](https://github.com/banodoco/astrid-app/pull/309) merged `2ffc0a300009f38b5eca6cbc0f5cedf0d6a86e87`; [#326](https://github.com/banodoco/astrid-app/pull/326) merged `cc57a53cbf60bec343f21dfd38cf410e152f31ef`; existing [reload guard](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/shared/lib/updates/draftSafeReload.ts#L4-L81) retains dirty owners and validates mutations. | Credit parked/Discard UX, concurrent-drop tracking and shared guard. Extend their lifetime/receipt integration; do not rebuild them or infer large-media qualification from historical focused tests. |
| [Agent #612](https://github.com/banodoco/astrid-agent/pull/612) merged `514499debc902643a03aee3f0ed68b710c5d3ead`; its render-backed qualification remained deferred. [#526](https://github.com/banodoco/astrid-agent/pull/526) is an unmerged older swap donor. | Reuse P88 same-kind swap/verified edit work; do not duplicate it. Source implementation and final render/installed acceptance remain separate. |

**Independent assessment:** accept necessary streaming, metadata, selection and custody amendments. Keep one LM task set and the [P63 shared contract](../63-dependable-saving/plan.md#shared-import-and-placement-contract). Do not turn exhaustive format exploration, aggregate project size, a new fixture framework or every fault point into separate work. Accepted memory/original-integrity/recovery guarantees and final supported-route qualification remain gates. No LM row is complete on this evidence.

**Recovery clarification from source:** Runtime's existing [`_ingest_transfer`](https://github.com/banodoco/astrid-runtime/blob/55a541a7ab904873e63510e581a60742e1b83fb8/runtime_protocol/service.py#L5800-L5885) binds actual staged digest and original request options, including an absent `expected_digest`, to the stable object-ingest key. A pending receipt can supply content identity for browser recovery without mandatory prehashing. Preserve the original options on replay; newly adding the learned digest as a header can break a correct retry. These are LM-4/5 regression cases, not another recovery mechanism or estimate increment.

## Owner decisions

The following decisions remain accepted from 21 November 2026; the [original record](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/79-local-media-any-size/inputs.md#owner-decisions) retains alternatives and the exact owner response.

- **D1 — Runtime-only limit: option (a).** Runtime refuses by declared size. Agent/App do not impose an independent byte ceiling. Option (c), reporting the configured limit through a new interface, was not approved; it remains conditional on evidence that existing refusal cannot provide truthful client behavior.
- **D2 — 1 GiB interim cap: option (b).** Approved because P79 waited behind P77. The authorized donor exists in open #475; inspected release source remains 64 MiB. Proposed supersession is explicit below, not a claim this decision was revoked or delivered.
- **D3 — use in place.** Separate [Plan 80](../80-use-media-in-place/plan.md); managed-copy streaming remains this plan's approach.
- **D4 — warning at reload: option (a).** Use the shared guard; browser warning and reselect/discard are the boundary. Persistent browser upload bytes/resumption were not approved. App-controlled reload/update must respect pending custody; native warning cannot prevent an overridden reload or crash.
- **D5 — Runtime pin.** Approved in advance as its own commit once LM-1 passes review. No unrelated pin movement or publication authority follows from this approval.

**Review rounds:** one final independent round, as agreed 21 November 2026. Preserve the existing review contract and bounded findings process.

## Remaining decisions and limits

**D2 recommendation for review:** if streaming is promptly dispatched, absorb the interim need into LM-2 and do not land a separate whole-file-memory cap increase. If the Lead still needs the stopgap first, reuse the already authorized narrow donor after exact-base review. Do not create another assignment or treat the entire #475 PR as approved. This proposed disposition awaits acceptance of the planning correction.

**Conditional interface decision:** first prove actual configured-cap refusal and handle/pending recovery through existing interfaces. If truthful client errors or exact stored-object settlement cannot be implemented within that boundary, bring the smallest concrete interface amendment, evidence and alternative to the owner. A new limit handshake or recovery endpoint is not pre-authorized by this revision.

**Qualification limits:** the original primary live witness is one OS, with absolute Agent RSS below 256 MiB for a real greater-than-1-GiB file; the task also retains the 300 MiB absolute gate. Broader supported-platform checks belong to the existing R16 matrix. Windows long paths and network/removable drives are not proven by source review. No expensive full-film rerender is required to establish import correctness. P88 #1916 is relevant only when its large-shots fixture is selected; P87 owns output repair.

**Estimate:** 6–9 implementation person-days plus 2–3 integration/installed-qualification/review days, 8–12 total. Existing P63/P87 work is not counted twice. Hardware availability and unrelated release repair remain separate uncertainty.

## Source identities and run start

**Run start:** Pending. This assignment permits planning-record corrections only; no P79 implementation run is authorized here. At dispatch the Lead records accountable sessions, exact product bases, overlapping function owners, focused proof commands and the Runtime/Agent pin before and after LM-1. Use the current approved `release/16/main` lineage and actual plan branches; do not follow preserved historical R15 branch instructions.

**Final handoff:** one exact integrated source/installed/served tuple with LM-6 evidence and separate P63 saving, P04 concurrency and P87 output verdicts. A merged predecessor, source presence, mocked size or historical small-file run is not final P79 qualification.

## References

- Existing incidents: [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1237](https://github.com/banodoco/astrid-dev/issues/1237), [App #252](https://github.com/banodoco/astrid-app/issues/252), [App #255](https://github.com/banodoco/astrid-app/issues/255). Keep their evidence; no duplicate observation is needed.
- Adjacent ownership: [P63](../63-dependable-saving/plan.md), [P04](../04-concurrent-edits/plan.md), [P35](../35-one-home-for-user-state/plan.md), [P29](../29-update-and-release/plan.md), [P77](../77-saving-holds-on-a-heavy-timeline/plan.md), [P87](../87-render-works/plan.md), [P88](../88-timeline-edits-land/plan.md), [P85](../85-one-place-to-measure/plan.md).
