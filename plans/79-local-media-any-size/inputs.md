# Inputs — Local media of any size

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked for this project and its release on 21 November 2026, in the Release 15 Lead session (`session_011EzfW1gtAhRQwk8pgJMzhG`): "Let's add a project to do this right and add it to release 15, please." That followed the Lead's finding that a one-line raise of the 64 MiB constant would unblock ordinary clips but load each whole file into memory. She has not yet read this end state or answered D1 to D5. Next: she confirms or changes them.

**Prior art:** Read on 21 November 2026 at astrid-agent `release/15/main` `aac1ceb6` and astrid-runtime `release/15/main` `1758a6df`, by an exploration with four read-only helpers, with the lines below re-read by the planner.

- **The limit is the Agent's.** `astrid/sdk/authoring_media.py:27` sets `_MAX_BYTES = 64 * 1024 * 1024`. `_metadata` refuses above it and calls it "Runtime's 64 MiB limit" (lines 111 and 141). The Runtime's object limit is 5 GiB (`runtime_protocol/cas.py:16`).
- **The file is read whole, more than once.** `_metadata` calls `path.read_bytes()` to hash it (line 139); `astrid/sdk/timeline/media_add.py:55` reads it again and passes the bytes to `import_project_media`; detached authoring reads every file again (`authoring_media.py:592`).
- **The Runtime already streams.** `runtime_protocol/server.py:1129` handles `POST …/media-imports` by staging the request body in chunks with the expected digest, then recording the catalog entry.
- **The editor already sends large files** on that route, with a 5 GiB limit of its own (`AssetResolver.ts:57`, reported by the exploration, not re-read).
- **`astrid media import` uses a different route.** It streams to the project objects route (`astrid/sdk/workspace_client.py:837`) and, as the exploration reports, records a store object without a catalog entry, which is why the handle in #1235 cannot be placed. Re-check at dispatch.
- **Nothing is moved or deleted.** Every route reads the user's file. The Runtime deletes only its own staging files (`runtime_protocol/cas.py`, reported by the exploration).
- **Negative finding:** an earlier "path-backed realm" is mentioned in #1235 as removed. Why was not found.

**Approach:** Four options were compared.

| Option | What it is | Days | Verdict |
| --- | --- | --- | --- |
| A | Keep Astrid's private copy; remove the Agent's limit; stream | about 5 | **Chosen.** No schema or protocol change expected; closes #1235 and #1237 |
| B | Reference the file in place, check before each use, copy only when needed | 15–25 | Not now: see below |
| C | Copy-on-write clone into the store where the file system allows, else copy | 4–6 on top of A | A possible later step (D3) |
| D | Always reference in place | — | Not viable |

**What stops Astrid using the file where it is.** Recorded because the owner asked.

- **The editor cannot.** It is a browser app and never learns a dropped file's path.
- **A clip's identity is its content.** Every commit records the media's digest and the Runtime re-checks it; the Runtime skips re-hashing only because nothing else can write to its store. A user's file can change, move or vanish at any time.
- **Everything downstream reads the store:** preview, the renderer, export, recovery and rented machines.
- **So in-place use needs** missing-media and relink screens, a copy on export and for rented machines, and a media identity that can change under the saving plans' checks (Plans 63, 75 and 77), which are being stabilised now.

**Challenge:** Pending — an independent critique of this plan and its tasks is required before greenlight, because it changes a user-visible flow. Next: record the critique's findings here, with what was accepted and rejected.

**Proof and limits:** The four completion cases in [plan.md](plan.md#completion). Not proven here: Windows long paths, network and removable drives, and files above 5 GiB.

**Review rounds:** Recommended: one round at the end, because the change crosses two repositories and a flow every creator uses. Pending — the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — the limit.** (a) The Runtime's limit, 5 GiB, is the only limit. (b) The Agent keeps a lower limit of its own. Recommendation: (a); a second number is how #1237 happened. Pending.
- **D2 — a stopgap first.** (a) No stopgap; this plan starts soon. (b) Raise the Agent's constant to 1 GiB now as a one-line fix, and let this plan replace it. Recommendation: (b) only if this plan waits more than a few days behind Plan 77; a 1 GiB file then uses about 1 GiB of memory. Pending.
- **D3 — using the file in place, later.** (a) Not a goal. (b) A later project for option C, which avoids the second copy on disk where the file system allows. (c) A later project for option B. Recommendation: (b), considered after the saving plans land. Pending.
- **D4 — an upload in flight at reload (astrid-app #255).** (a) Warn before the page closes while an upload is running. (b) Save pending uploads and resume them. Recommendation: (a); (b) is a design of its own. Pending.
- **D5 — `astrid media import`.** May it record a catalog entry, so its handle can be placed on a timeline? This changes what an existing command writes. Recommendation: yes. Pending.

## Source identities

Pending — no code work has started. At run start record, for each repository: `release/15/plan-79`, cut from that repository's `release/15/main`, the commit it was cut at, whether Plan 77 had landed, and the Runtime commit the Agent pins. Intended destination: `release/15/main`.

## References

- [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1237](https://github.com/banodoco/astrid-dev/issues/1237), [astrid-app #255](https://github.com/banodoco/astrid-app/issues/255), [astrid-app #252](https://github.com/banodoco/astrid-app/issues/252).
- [#1222](https://github.com/banodoco/astrid-dev/issues/1222): the Runtime's verify-once rule, which in-place reference would break.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), [Plan 63](../63-dependable-saving/plan.md) and [Plan 75](../75-fast-saving/plan.md): the saving plans this must not disturb.
