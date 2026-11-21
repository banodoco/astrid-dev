# Inputs — Use media in place

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked for this plan on 21 November 2026, in the Release 15 Lead session (`session_011EzfW1gtAhRQwk8pgJMzhG`): "another plan for just like being able to use any [media] on the machine without importing it", after asking "what's stopping us from just running it from anywhere?" She has not yet read this end state or answered D1 to D6. Next: she confirms or changes them.

**Prior art:** Read on 21 November 2026 at astrid-agent `release/15/main` `aac1ceb6`, astrid-runtime `release/15/main` `1758a6df` and astrid-app `release/15/main`, by an exploration with four read-only helpers. Lines marked † were re-read by the planner; the rest are the exploration's and are re-checked in LK-1.

- **Media identity is its content.** A selection records the object id, size, media type and variant id, and each commit that uses it re-checks the stored bytes (`runtime_protocol/timeline_commit_port.py:1040-1066`, `service.py:6614`).
- **"Verify once" assumes nobody else writes.** The Runtime skips re-hashing while a stored file's device, inode, size and times are unchanged (`runtime_protocol/cas.py:200-215`). [#1222](https://github.com/banodoco/astrid-dev/issues/1222) asks about the same rule.
- **Readers assume the store.** Preview reads through Runtime object routes (`server.py:548-582`); the Agent's media views refuse anything not stored (`astrid/.../media_views.py:16-53`); the renderer reads only its workspace and listed extra folders (`rendering.py:665-692`); export and recovery pack from the store (`timeline_export.py:425`, `timeline_recovery.py:76-87`); rented machines are given object ids and digests (`remote_worker_deployment.py:183-203`).
- **Today's copy is not destructive.** † The Runtime stages the request body and stores it (`runtime_protocol/server.py:1129`); it deletes only its own staging files. The user's file is only read.
- **The editor cannot know a path.** It is a browser app with no desktop shell. A leftover start exists: saved Chromium file handles (`localHandleStore.ts`) and a "local" storage mode that plays them as `blob:` URLs (`localMediaResolver.ts:1-60`), but turning them into project media is stubbed as unavailable (`materializeLocalGeneration.ts:23-34`), and the Agent accepts only the `managed_local` realm (`astrid/sdk/remote.py:1813-1823`).
- **Negative finding:** #1235 says a "path-backed realm" was removed once. Why was not found; LK-1 must find out before repeating it.

**Approach:** Compared with doing less.

| Option | What the creator gets | Days | Verdict |
| --- | --- | --- | --- |
| Plan 79 only | Any size, still copied | about 5 | Already proposed for Release 15 |
| Plan 79 plus a copy-on-write clone | No upload and no extra disk on file systems that support clones (APFS, Btrfs, XFS, ReFS); a plain copy elsewhere (ext4, NTFS, across drives) | 4–6 more | The cheap alternative: D6 |
| **This plan** | A true link on every file system, with changed and missing states | about 22 | Proposed; the owner asked for it |
| Always link, never copy | — | — | Not viable: export, rented machines and recovery need owned bytes |

**Challenge:** Pending — an independent critique is required before greenlight: this changes a cross-repository contract, user data and a flow every creator uses, and exceeds five days. Next: brief the critic to build as little as possible, to test whether D6's clone gives most of the value, and to check the claims above in code; record findings here.

**Proof and limits:** The completion cases in [plan.md](plan.md#completion). Not proven here: network and removable drives beyond "missing", Windows long paths, and portability without copying in.

**Review rounds:** Recommended: a review stop (RS1) after the contract, because every later task builds on it and a late finding would redo them, and two rounds at the end, because the change reaches user data. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the phase it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — the release.** (a) Release 15. (b) The release after the saving plans land. Recommendation: (b). This plan changes media identity on the commit path Plans 63, 75 and 77 are stabilising, and at about 22 days it would be the second-largest plan in Release 15. Pending.
- **D2 — the default when adding a file by path.** (a) Copy stays the default; linking is a choice. (b) Link by default. Recommendation: (a) until the changed and missing states have been lived with. Pending.
- **D3 — what Astrid may read.** (a) Only folders the creator has linked. (b) Any path the creator's own session names. Recommendation: (a); the Runtime is a local server, and (b) lets anything that can reach it read any file. Pending.
- **D4 — a file that changed.** (a) Flag the clip and refuse new uses until the creator accepts or relinks. (b) Quietly use the new content. Recommendation: (a); (b) changes finished work without anyone choosing it. Pending.
- **D5 — adding from the editor.** (a) Browse linked folders through the Runtime. (b) A desktop shell that knows file paths. (c) SDK and CLI only; the editor only displays links. Recommendation: (a). Pending.
- **D6 — the cheaper clone first.** Should the copy-on-write clone (4–6 days on top of Plan 79) come first, with this plan waiting to see whether it is still wanted? Recommendation: decide after the critique; the clone does nothing on NTFS or ext4, which covers most Windows and many Linux installs. Pending.

## Source identities

Pending — no code work has started. At run start record, for each repository: the plan branch `release/<NN>/plan-80` cut from that release's branch (the release is D1), the commit it was cut at, and the commits of Plan 79 and Plan 63 it builds on.

## References

- [Plan 79](../79-local-media-any-size/plan.md): the copy path, and the answer to "what stops Astrid using the file where it is".
- [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1222](https://github.com/banodoco/astrid-dev/issues/1222).
- [Plan 63](../63-dependable-saving/plan.md), [Plan 75](../75-fast-saving/plan.md), [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md): the commit path this plan adds a refusal to.
- [Plan 25](../25-cloud-assist-v1/plan.md): local files with cloud work, which meets linked media at "copy in when owned bytes are needed".
