# Local media of any size

**Project:** Local media of any size

**Goal:** A creator or agent adds a clip from their own computer at any size the Runtime accepts, with one limit, one message and no extra step, and the original file is never touched.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 5 engineering days: the Agent about 3, the App about 1, the live proof and review about 1.

**Waiting on:** the owner's decisions D1 to D5 in [inputs.md](inputs.md#owner-decisions), a manager, and Plan 77's branch for the two files it also edits ([sequence](#sequence-and-readiness)).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary): a creator who cannot put their own footage on a timeline cannot start. F-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Today a local file over 64 MiB cannot be placed on a timeline from the SDK or the CLI ([#1235](https://github.com/banodoco/astrid-dev/issues/1235)), although the Runtime accepts 5 GiB and the editor already sends files that large. Four routes have four limits, and the error names the wrong owner of the limit ([#1237](https://github.com/banodoco/astrid-dev/issues/1237)).

**Included:**

- **One limit, declared once.** The Runtime's object limit is the only size limit on local media. The Agent keeps no number of its own for it.
- **Streaming.** Placing local media hashes and sends the file in chunks. Memory use does not grow with the file.
- **One import that the timeline can use.** `astrid media import` returns a handle that can be placed on a timeline.
- **One message.** Every refusal for size names the real limit and its owner, and the docs agree.
- **The editor does not lose an upload silently** when the page is reloaded mid-upload ([astrid-app #255](https://github.com/banodoco/astrid-app/issues/255)).

**Astrid keeps its private copy.** The original file is read and never moved, changed or deleted, as today.

**Not included, deliberately:** using the file in place at its own path. The owner asked what stops that; the answer and its cost are in [inputs.md](inputs.md#planning-evidence), and whether it becomes a later project is decision D3. Also not included: Runtime store changes, the saving plans' digest work, generated-media limits and remote-machine uploads.

## Existing work and decision

The Runtime already does the hard part: its `media-imports` route streams the request body into a staging file, checks the digest and stores it, up to 5 GiB. The editor already uses that route. Only the Agent's SDK path reads the whole file into memory and applies its own 64 MiB constant. So this plan changes the caller, not the store: no schema, protocol or Runtime store change is expected. The source findings, the four options compared and the owner's request are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **LM-1 and LM-2 together** (the Agent): remove the Agent's own limit and stream the file. They change the same functions, so one worker does both in order.
2. **LM-3 and LM-4** in parallel with those: the import handle, then the wording.
3. **LM-5** (the editor) once Plan 77 has landed in `release/15/main`, because `release/15/plan-77` edits the same drop code.
4. **LM-6, the live proof,** on the combined result, then **R**.

**Real dependencies:** `release/15/plan-77` edits `astrid/sdk/timeline/media_add.py` in the Agent and `external-drop-utils.ts` in the App. This plan's branches are cut from `release/15/main` after Plan 77 lands there, or LM-2 and LM-5 merge `release/15/plan-77` first; the manager chooses at run start and records it in [inputs.md](inputs.md#source-identities).

**Unresolved:** decisions D1 to D5. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's `POST /v1/projects/<id>/media-imports` route and its object limit, at the Runtime commit the Agent's `release/15/main` pins. LM-2's first step confirms the generated Runtime client can send a stream on that route; if it cannot, that client change is the one cross-repository edit, and it is recorded before any code.

**Produces:** an SDK and CLI path that places local media of any accepted size, and a `media import` handle the timeline accepts. Plans 63, 75 and 77 are unaffected: media identity stays the content digest of bytes the Runtime owns.

## Completion

- **Works:** a real clip larger than 1 GiB is placed on a timeline from the CLI and by dropping it in the editor, on a real stack, and plays. The Agent process's peak memory during the CLI import stays under 256 MiB.
- **Refuses correctly:** a file over the Runtime's limit is refused before any bytes are sent, and the message names the limit and the Runtime as its owner.
- **Negative case:** a file that changes while it is being imported is refused with the existing "changed during import" message, and nothing is added to the timeline.
- **Untouched original:** after each case the source file's bytes, path and modified time are unchanged.
- **Limits of the proof:** one operating system for the live run unless the owner asks for more; Windows long paths and network drives are not proven here. Landing in `release/15/main` and publishing remain the owner's.
