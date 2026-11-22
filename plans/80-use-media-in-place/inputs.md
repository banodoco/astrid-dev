# Inputs — Use media in place

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — phase 1 only. The owner asked for this plan on 21 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) (`session_011EzfW1gtAhRQwk8pgJMzhG`): "another plan for just like being able to use any [media] on the machine without importing it". After the critique she was given the three phases and the recommendations to build the clone first, to put it in Release 15 only if Plan 79 lands with time to spare, and to decide on true links after using the clone, and replied: "Yes, I agree with your recommendations." Phase 2 is not accepted: it waits on D7. D2 to D5 were not put to her and stay pending.

**Prior art:** Read on 21 November 2026 at astrid-agent [`release/15/main` `aac1ceb6`](https://github.com/banodoco/astrid-agent/tree/aac1ceb6), astrid-runtime [`release/15/main` `1758a6df`](https://github.com/banodoco/astrid-runtime/tree/1758a6df) and astrid-app [`release/15/main` `2ef94b4c`](https://github.com/banodoco/astrid-app/tree/2ef94b4c), by an exploration and then by the independent critic, whose corrections are included.

- **Astrid had in-place media and retired it.** The `external_local` realm kept paths to the user's files, with relocation and fingerprint checks. It was removed because a saved path gave the application continuing authority to read that location; local execution was narrowed to bytes the Runtime owns (astrid-agent commits `a5f46d4e` and `17bfe373`). The critic found an architectural decision, and no evidence of a data-loss incident.
- **Media identity is its content.** The wire selection has five identity fields; size and media type are resolved metadata (astrid-runtime `contract/schemas/timeline-commit.json:1452`). Consumed selections get byte checks (`runtime_protocol/timeline_commit_port.py:1054`), and closure validation separately requires managed project objects (`timeline_commit_store.py:1625`).
- **"Verify once" assumes nobody else writes.** The Runtime skips re-hashing while a stored file's device, inode, size and times are unchanged (`runtime_protocol/cas.py:200-215`). [#1222](https://github.com/banodoco/astrid-dev/issues/1222) already questions whether some reads inherit verification they never performed. External files must never inherit that trust.
- **Readers.** The Agent's `media_views` is an optional fast path for stored objects (`astrid/sdk/media_views.py:16`). The renderer rejects locator fields and reads host-materialized files into memory to verify them (`astrid/core/rendering/assets.py:235`, `:264`), so adding folders to its sandbox is not enough. Export, recovery and rented machines need owned, immutable bytes (`timeline_export.py:345`, `timeline_recovery.py:47`, `remote_worker_deployment.py:184`).
- **The editor cannot know a path,** but saved browser file handles already support gallery playback and permission recovery (`localMediaResolver.ts:145`); turning them into project media is stubbed (`materializeLocalGeneration.ts:29`).
- **The Runtime already has a clone helper** (`runtime_protocol/fsclone.py:16`). Its import receives HTTP bytes (`server.py:1129`, `service.py:5696`), so a clone needs a local handoff of the path.
- **Access.** The Runtime already requires scoped bearer credentials (`server.py:272`) and has directory-handle helpers (`dirfd.py:671`).

**Approach:** Compared with doing less.

| Option | What the creator gets | Days | Verdict |
| --- | --- | --- | --- |
| Plan 79 only | Any size, still copied | about 8 | Proposed for Release 15 |
| **Clone first (phase 1)** | No upload and no extra disk where the file system clones and the file is on the store's volume; a snapshot that survives edits to the original; a plain copy elsewhere | 4–6 | **Recommended first**, by the critic and the planner |
| True links (phase 2) | A link on every file system, tracking the live file, with changed and missing states | more than 22 | Only if still wanted after phase 1 |
| Always link, never copy | — | — | Not viable: export, rented machines and recovery need owned bytes |

**Where a clone works,** from the critic, with sources, not tested here: macOS on APFS (`clonefileat`); Linux on Btrfs and reflink-enabled XFS (`FICLONE`, exposed by Python 3.12); Windows on ReFS (block cloning, in ranges below 4 GB per call). Ordinary ext4, NTFS and any transfer across volumes need a copy. `shutil.copyfile` does not guarantee a clone.

**Challenge:** Reviewed — commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 21 November 2026 and done by an independent Codex critic (on the high-judgment role, high effort, read-only brief, no stake in the draft), which read code and history in the three repositories. It did not run the stack, benchmark hashing, test file systems or measure how often creators keep footage and the store on one volume. Its recommendation: **build the clone first.** Findings and what the planner did with each:

- **Accepted — the earlier removal was deliberate** (above). Now D7, and LK-1 must answer it.
- **Accepted — a folder list and a freshness check cannot guarantee the bytes rendered.** The contract must say who grants and revokes, open files relative to a held directory handle (symlinks, Windows reparse points, case aliases), and define how each range and render gets verified bytes; coarse timestamps, same-size edits and Windows sharing violations must be tested; the first digest reads every byte. Now in LK-1, LK-2 and LK-3, re-routed to `S`.
- **Accepted — commit rules reach accepted history.** Availability stays outside accepted revisions; accepting replacement bytes makes a new revision and keeps undo; Plan 63 needs distinct outcomes for "temporarily unavailable" and "stale selection"; re-checking unrelated files would threaten Plan 75's 300 ms and Plan 77's two seconds. Now in LK-1 and LK-4.
- **Accepted — "copy in later" can fail for good:** a file over the Runtime's limit, deleted or overwritten. The limits are published before a link is accepted, and copy-in is an explicit command (LK-7); automatic copy-in is deferred.
- **Accepted — the reader inventory was wrong** in the draft (above), and derived thumbnails, transcripts and proxies must be keyed by source digest. Now LK-6, re-routed to `X`.
- **Accepted — 22 days was too optimistic** for the stated guarantees, and one operating system's proof cannot price the others. Phase 2 is re-estimated by LK-1; the editor work is deferred to phase 3; the wording task is folded into delivery.
- **Accepted — start with one useful slice:** the clone, for the SDK and CLI on one host, on APFS first. Now LK-0 and phase 1.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Not proven here: other operating systems than the one each phase is run on, network and removable drives beyond "missing", and portability without copying in.

**Review rounds:** None for phase 1 beyond its focused proof and a bounded-fix check, because it adds no record type; for phase 2, a review stop (RS1) after the contract and two rounds at the end, because the change reaches user data and accepted history. Agreed by the owner on 21 November 2026 in the Release 15 Lead session: "Yeah, I agree with your recommendations".

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the phase it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — the release.** (a) Phase 1 in Release 15, after Plan 79. (b) Phase 1 in the next release. Phase 2 in neither until D6 is answered again. Recommendation: (a) if Plan 79 lands with time to spare, since phase 1 is 4 to 6 days and changes no contract; otherwise (b). **Decided 21 November 2026:** phase 1 goes into Release 15 only if Plan 79 lands with time to spare; otherwise the next release. It is in no release brief until then. Source as D6.
- **D2 — the default when adding a file by path.** (a) Clone when possible, copy otherwise, automatically. (b) Ask. For phase 2, linking stays an explicit choice. Recommendation: (a). Pending.
- **D3 — what Astrid may read.** Phase 1: only a path the creator's own session names, read once at import. Phase 2: (a) one folder the creator grants; (b) any path. Recommendation: (a). Pending.
- **D4 — a linked file that changed (phase 2).** (a) Flag the clip and refuse new uses until the creator accepts or relinks. (b) Quietly use the new content. Recommendation: (a). Pending.
- **D5 — the editor (phase 3).** (a) Browse the granted folder through the Runtime. (b) A desktop shell that knows file paths. (c) Build on the saved browser file handles. Recommendation: decide when phase 3 is planned. Pending.
- **D6 — the clone first.** (a) Build phase 1, use it, then decide whether phase 2 is still wanted. (b) Go straight to true links. Recommendation: (a), as the critic recommends. On a Mac with footage and Astrid on the same disk, the clone already means no upload and no second copy; what it does not give is a clip that follows later edits to the original. **Decided 21 November 2026: (a),** the clone first. The owner agreed with the Lead's recommendation in the Release 15 Lead session (`session_011EzfW1gtAhRQwk8pgJMzhG`): "Yes, I agree with your recommendations."
- **D7 — bring back a saved path's authority (phase 2).** Astrid removed in-place media so that it never keeps standing permission to read the user's folders. Phase 2 reverses that for one granted folder. (a) Accept that, with the grant visible and revocable. (b) Keep the earlier decision; phase 2 is not built. Recommendation: decide after phase 1. **Deferred by the owner on 21 November 2026** until she has used the clone. Source as D6. Pending.

## Source identities

Pending — no code work has started. At run start record, for each repository: the plan branch `release/<NN>/plan-80` cut from that release's branch (the release is D1), the commit it was cut at, and the commits of Plan 79 and, for phase 2, Plan 63 it builds on.

## References

- [Plan 79](../79-local-media-any-size/plan.md): the copy path and the fallback.
- [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1222](https://github.com/banodoco/astrid-dev/issues/1222).
- [Plan 63](../63-dependable-saving/plan.md), [Plan 75](../75-fast-saving/plan.md), [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): the commit path phase 2 adds refusals to.
- Clone support: [Apple `clonefile`](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/man/man2/clonefile.2), [Linux `FICLONE`](https://man7.org/linux/man-pages/man2/FICLONE.2const.html), [Python `fcntl`](https://docs.python.org/3/library/fcntl.html), [Windows ReFS block cloning](https://learn.microsoft.com/en-us/windows-server/storage/refs/block-cloning).
