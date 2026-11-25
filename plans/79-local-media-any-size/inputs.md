# Inputs — Local media of any size

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner asked for this project and its release on 21 November 2026, in the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) (`session_011EzfW1gtAhRQwk8pgJMzhG`): "Let's add a project to do this right and add it to release 15, please." After the critique she was given the revised end state (about 8 days; the Runtime refuses by size; a Runtime client change and a pin) with the recommended answers to D1, D2, D4 and D5, and replied: "Yes, I agree with your recommendations."

**Prior art:** Read on 21 November 2026 at astrid-agent [`release/15/main` `aac1ceb6`](https://github.com/banodoco/astrid-agent/tree/aac1ceb6) and astrid-runtime [`release/15/main` `1758a6df`](https://github.com/banodoco/astrid-runtime/tree/1758a6df), by an exploration with four read-only helpers, with the lines below re-read by the planner.

- **The limit is the Agent's.** `astrid/sdk/authoring_media.py:27` sets `_MAX_BYTES = 64 * 1024 * 1024`. `_metadata` refuses above it and calls it "Runtime's 64 MiB limit" (lines 111 and 141). The Runtime's object limit is 5 GiB (`runtime_protocol/cas.py:16`).
- **The file is read whole, more than once.** `_metadata` calls `path.read_bytes()` to hash it (line 139); `astrid/sdk/timeline/media_add.py:55` reads it again and passes the bytes to `import_project_media`; detached authoring reads every file again (`authoring_media.py:592`).
- **The Runtime already streams.** `runtime_protocol/server.py:1129` handles `POST …/media-imports` by staging the request body in chunks with the expected digest, then recording the catalog entry.
- **The editor already sends large files** on that route, with a 5 GiB limit of its own (`AssetResolver.ts:57`, reported by the exploration, not re-read).
- **`astrid media import` uses a different route.** It streams to the project objects route (`astrid/sdk/workspace_client.py:837`) and records a managed object. Its digest can be placed only when exactly one catalog entry matches it (see Challenge).
- **Nothing is moved or deleted.** Every route reads the user's file. The Runtime deletes only its own staging files (`runtime_protocol/cas.py`, reported by the exploration).
- **Negative finding:** an earlier "path-backed realm" is mentioned in #1235 as removed. Why was not found.

**Approach:** Four options were compared.

| Option | What it is | Days | Verdict |
| --- | --- | --- | --- |
| A | Keep Astrid's private copy; remove the Agent's limit; stream | about 8 | **Chosen.** No wire, schema or store change; one Runtime client change and a pin; closes #1235 and #1237 |
| B | Reference the file in place, check before each use, copy only when needed | 15–25 | Its own plan: [Plan 80](../80-use-media-in-place/plan.md) |
| C | Copy-on-write clone into the store where the file system allows, else copy | 4–6 on top of A | A possible later step: Plan 80's D6 |
| D | Always reference in place | — | Not viable |

**What stops Astrid using the file where it is.** Recorded because the owner asked.

- **The editor cannot.** It is a browser app and never learns a dropped file's path.
- **A clip's identity is its content.** Every commit records the media's digest and the Runtime re-checks it; the Runtime skips re-hashing only because nothing else can write to its store. A user's file can change, move or vanish at any time.
- **Everything downstream reads the store:** preview, the renderer, export, recovery and rented machines.
- **So in-place use needs** missing-media and relink screens, a copy on export and for rented machines, and a media identity that can change under the saving plans' checks (Plans 63, 75 and 77), which are being stabilised now.

**Challenge:** Reviewed — commissioned from the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) on 21 November 2026 and done by an independent Codex critic (on the high-judgment role, high effort, read-only brief, no stake in the draft), which checked the draft's claims in the three repositories. It ran no tests or uploads. Findings and what the planner did with each:

- **Accepted — the Agent cannot learn the limit.** 5 GiB is a ceiling that `RUNTIME_MAX_OBJECT_BYTES` can lower, and neither health nor handshake reports it (`runtime_protocol/service.py:561`, `:858`, `:905`). The draft promised a refusal "before any bytes are sent". Now: the Agent declares the size and the Runtime refuses before reading the body. Reporting the limit in the handshake is a protocol change, left as D1's option (c).
- **Accepted — streaming needs a Runtime client change and a pin.** The route stages chunks, but the generated client calls `bytes(data)` (`astrid_runtime_client/generated.py:1185-1212`; generator at astrid-runtime `generators/generate.py:23`; pin at astrid-agent `runtime.lock.json:15`). Now LM-1, with the pin as D5.
- **Accepted — the editor proof has a blocker.** On `release/15/main` the save handoff refuses an ordinary dropped video (`timelineLocalSaveHandoff.ts:705-720`), and the App's 5 GiB test only changes a tiny file's reported size (`mediaImport.test.ts:228`). Now LM-4, and the proof reopens the saved timeline.
- **Accepted — the handle diagnosis was conditional.** A digest handle already works when exactly one catalog entry matches; none and several give the same refusal (`astrid/sdk/timeline/media_add.py:72-85`). The narrower fix catalogs the stored object on first placement and leaves `media import` and its output alone. Now LM-3; the draft's D5 is withdrawn.
- **Accepted — other callers read whole files:** SDK add and replacement (`astrid/sdk/timeline/commit_session.py:277`, `:383`) and detached apply, which holds every payload before its first change (`authoring_media.py:591`). Now in LM-2, keeping the check-everything-first guarantee with bounded staging.
- **Accepted — smaller points:** measure resident memory, not `tracemalloc`; translate the Runtime's digest mismatch into the promised message; test a slow acknowledgement (the client's socket timeout is 30 s, 300 s on Plan 77); LM-1 and LM-2 of the draft merged into one `X` task; the wording folded into it; the reload guard separated and built on the App's shared guard (`draftSafeReload.ts`).
- **Noted:** no Agent test pins 64 MiB for local authoring. "The Runtime deletes only its staging files" holds for import clean-up; it removes stored objects elsewhere, by design.
- **Estimate:** 5 days was optimistic; now about 8.

**Proof and limits:** The four completion cases in [plan.md](plan.md#completion). Not proven here: Windows long paths, network and removable drives, and files above 5 GiB.

**Review rounds:** One round at the end, because the change crosses three repositories and a flow every creator uses. Agreed by the owner on 21 November 2026 in the Release 15 Lead session: "Yeah, I agree with your recommendations".

**Run start:** Pending — No run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking and what still needs the owner's go.

## Owner decisions

- **D1 — the limit.** (a) The Runtime's limit is the only limit, and the Runtime refuses by the declared size. (b) The Agent keeps a lower limit of its own. (c) As (a), and the Runtime also reports its limit in the handshake so clients can refuse earlier; this is a protocol change. Recommendation: (a); a second number is how #1237 happened, and (c) can follow if the late refusal proves annoying. **Decided 21 November 2026: (a).** The owner agreed with the Lead's recommendation in the Release 15 Lead session (`session_011EzfW1gtAhRQwk8pgJMzhG`): "Yes, I agree with your recommendations."
- **D2 — a stopgap first.** (a) No stopgap; this plan starts soon. (b) Raise the Agent's constant to 1 GiB now as a one-line fix, and let this plan replace it. Recommendation: (b) only if this plan waits more than a few days behind Plan 77; a 1 GiB file then uses about 1 GiB of memory. **Decided 21 November 2026: (b),** raise the constant to 1 GiB now, because this plan waits behind Plan 77. Same source as D1.
- **D3 — using the file in place.** Now its own plan: [Plan 80](../80-use-media-in-place/plan.md). Nothing to decide here.
- **D4 — an upload in flight at reload (astrid-app #255).** (a) Warn before the page closes while an upload is running, using the App's shared reload guard. (b) Save pending uploads and resume them. Recommendation: (a); (b) is a design of its own. **Decided 21 November 2026: (a),** the warning. Same source as D1.
- **D5 — the Runtime pin.** LM-1 changes the Runtime's generated client, and the Agent must pin the Runtime commit that has it. A pin change is the owner's to approve. Recommendation: approve it as its own commit once LM-1 has passed review. **Decided 21 November 2026: approved in advance,** as its own commit once LM-1 has passed review. Same source as D1.

## Source identities

Pending — no code work has started. At run start record, for astrid-runtime, astrid-agent and astrid-app: `release/15/plan-79`, cut from that repository's `release/15/main` after Plan 77 has landed there, the commit it was cut at, and the Runtime commit the Agent pins before and after LM-1. Intended destination: `release/15/main`.

## References

- [#1235](https://github.com/banodoco/astrid-dev/issues/1235), [#1237](https://github.com/banodoco/astrid-dev/issues/1237), [astrid-app #255](https://github.com/banodoco/astrid-app/issues/255), [astrid-app #252](https://github.com/banodoco/astrid-app/issues/252).
- [#1222](https://github.com/banodoco/astrid-dev/issues/1222): the Runtime's verify-once rule, which in-place reference would break.
- [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md), [Plan 63](../63-dependable-saving/plan.md) and [Plan 75](../75-fast-saving/plan.md): the saving plans this must not disturb.

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

bind configured cap, source-change detection, scratch/disk/memory accounting, zero/one/many handle cases, accepted import versus pending placement and D4 crash/reselect policy. Distinguish source-supported duplicate-import risk from a reproduced incident.
