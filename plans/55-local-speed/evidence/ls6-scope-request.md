# LS-6 implementation scope request

**State:** proposed, not approved. The accepted outcome and D1–D8 stay unchanged. This note records the additional code boundaries found during implementation; it does not replace LS-3 or consume RS1.

## Why the listed files are insufficient

The current partial change carries the harvester's expected digest through host upload so the Runtime rejects changed bytes. It is in [Agent #351](https://github.com/banodoco/astrid-agent/pull/351), with focused proof in [tests/README.md](tests/README.md). Remaining output hashes occur in the manifest, pack result and VibeComfy result paths outside LS-6's listed files. Public client upload/download methods buffer entire objects. The existing thumbnail backfill is on demand; the generation worker lacks task-admission and project-write authority. Giving it those permissions is not proposed.

The Runtime's current object GET also cannot replace caller verification. `service.py::open_object` verifies a held file descriptor before `server.py::_send_file` reads it again for transmission. A held descriptor keeps the inode, not its contents. A digest header and correct length cannot establish that later transmitted bytes are the verified bytes. Caller hashing stays until a narrowly defined verified-transfer contract is implemented and reviewed.

## Requested additional scope

| Repository / paths | Necessary change |
| --- | --- |
| Agent `core/generation/backends/comfy_target.py`, `core/_shared/result_manifest.py`, `core/contracts/managed_generation_result.py`, `packs/vibecomfy/actions/run/run.py` | Carry the original fetch digest and byte count as an expected identity through the actual result path, preserving attribution, declared-output, path and fence checks; Runtime remains the authority on received bytes. |
| VibeComfy `runtime/run.py`, `runtime/session.py` | Carry the retrieval receipt through managed-result emission; retain existing verification for other producers and for hooks that transform bytes. |
| Runtime `generators/python_client_template.py`; regenerated Agent `astrid_runtime_client/generated.py`; Agent `sdk/workspace_client.py` | Add bounded streaming methods over existing object routes with the current attempt-bound upload proof and project-scoped read authorization. Do not hand-edit generated code alone. |
| Runtime `runtime_protocol/server.py` and the necessary `service.py`/CAS verification seam | Make optimized full-object export verify the actual transmitted chunks and withhold complete response framing until digest/size verification succeeds, or provide an equivalently strong bounded transfer. Keep range and unrelated file responses on their existing contract. This is a proposed design to examine at RS1, not an approved protocol. |
| Agent `core/execution/thumbnail_backfill.py`, `sdk/invocation.py`, and the already in-scope host; Runtime task/settlement code only if required for atomic follow-up admission | Reuse ordinary Runtime-backed thumbnail work and existing authority. Do not use an untracked background thread. The design must handle caller disconnection and the settlement-to-thumbnail-admission window explicitly. |

## Boundaries and review

The requested outcome remains one Agent output-content hash, necessary Runtime integrity checks, bounded transfers, an independent caller copy and a reply that does not wait for thumbnail extraction. It does not mean one physical read across every file and process. Success still means stored and recorded; every caller still goes through the Runtime. No writable CAS path, broader worker permission, speculative execution framework or automatic resubmission is introduced.

The protocol and thumbnail admission details belong in LS-3 and its existing RS1 stop before implementation of those changes. Tests must cover changed bytes after fetch/verification, mutation during streaming, exact-length corruption, truncation without destination replacement, final response completion withheld on failure, attempt/lease/fence isolation, and durable thumbnail work after caller exit. A new dependency pin remains a separate owner approval on exact commits.

**Recommendation:** approve these bounded additional file/repository paths to deliver the existing LS-6 outcome; retain the current protections until the reviewed replacements pass. No extension has been implemented.

Evidence was read at Agent `9814193a73f606719e81883a8be197d27dd361d4`, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, and VibeComfy `dba38f8644c46f652376f2cd5112ea161e40f09b`. The engineering advice and manager cross-check were read-only and consumed neither RS1 nor the final review.
