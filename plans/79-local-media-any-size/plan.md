# Local media of any size

**Project:** Local media of any size

**Goal:** A creator or agent adds a clip from their own computer at any size the Runtime accepts, with one limit, one message and no extra step, and the original file is never touched.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 8 engineering days (7 to 9): the Runtime's client and the Agent's pin about 1, the Agent about 4, the App about 1.5, the live proof and review about 1.5. The critique of 21 November 2026 raised it from 5.

**Waiting on:** the owner's decisions D1, D2, D4 and D5 in [inputs.md](inputs.md#owner-decisions), a manager, and Plan 77 landing in `release/15/main`: it edits the same Agent and App files, and the editor half needs its drop handling ([sequence](#sequence-and-readiness)).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary): a creator who cannot put their own footage on a timeline cannot start. F-003's route does not name this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Today a local file over 64 MiB cannot be placed on a timeline from the SDK or the CLI ([#1235](https://github.com/banodoco/astrid-dev/issues/1235)), although the Runtime accepts 5 GiB and the editor already sends files that large. Four routes have four limits, and the error names the wrong owner of the limit ([#1237](https://github.com/banodoco/astrid-dev/issues/1237)).

**Included:**

- **One limit, declared once.** The Runtime's object limit is the only size limit on local media, and the Runtime is the one that refuses. The Agent keeps no number of its own for it.
- **Streaming.** Every SDK path that places or replaces local media hashes and sends the file in chunks. Memory use does not grow with the file.
- **One import that the timeline can use.** A handle from `astrid media import` can be placed on a timeline. The command and what it returns do not change.
- **One message.** Every refusal for size names the real limit and its owner, and the docs agree.
- **The editor does not lose an upload silently** when the page is reloaded mid-upload ([astrid-app #255](https://github.com/banodoco/astrid-app/issues/255)).

**Astrid keeps its private copy.** The original file is read and never moved, changed or deleted, as today.

**Not included, deliberately:** using the file in place at its own path. The owner asked what stops that; the answer is in [inputs.md](inputs.md#planning-evidence), and it is now its own plan, [Plan 80](../80-use-media-in-place/plan.md). Also not included: Runtime store changes, the saving plans' digest work, generated-media limits and remote-machine uploads.

## Existing work and decision

The Runtime already does the hard part: its `media-imports` route streams the request body into a staging file, checks the digest and stores it, up to 5 GiB. Only the callers fall short. The Agent's SDK reads the whole file into memory and applies its own 64 MiB constant, and the Runtime's generated Python client turns the body into bytes before sending. So this plan changes the callers, not the store: no wire, schema or store change. It does need one change in astrid-runtime, to the client generator, and a new Runtime pin in the Agent, which is the owner's to approve (D5). The source findings, the options compared, the critique and the owner's request are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **LM-1** (astrid-runtime): the generated client can send a sized file stream on `media-imports`. Then the Agent's pin moves to it.
2. **LM-2** (the Agent): no limit of its own, and streaming on every path that reads local media.
3. **LM-3** (the Agent), in parallel once LM-2's streaming call exists: the import handle.
4. **LM-4 and LM-5** (the editor), once Plan 77 has landed in `release/15/main`: a large dropped clip is placed and stays placed, and a reload cannot silently lose an upload.
5. **LM-6, the live proof,** on the combined result, then **R**.

**Real dependencies:** `release/15/plan-77` edits `astrid/sdk/timeline/media_add.py` and the client's timeout in the Agent, and the drop handling in the App. This plan's branches are cut from `release/15/main` after Plan 77 lands there; the manager records the commits in [inputs.md](inputs.md#source-identities). On `release/15/main` today the editor's save handoff refuses an ordinary dropped video ([astrid-app #252](https://github.com/banodoco/astrid-app/issues/252)), so the editor half cannot be proven until that is fixed, by Plan 77 or by LM-4.

**Must not disturb:** Plan 63's import outcomes and replay, Plan 75's concurrent-commit timing and Plan 77's parked-drop retry.

**Unresolved:** decisions D1, D2, D4 and D5. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's `POST /v1/projects/<id>/media-imports` route and its object limit, unchanged. The limit can be lowered by `RUNTIME_MAX_OBJECT_BYTES` and is not reported by the Runtime's health or handshake, so the Agent cannot know it in advance: it declares the file's size, and the Runtime refuses before reading the body.

**Produces:** in astrid-runtime, a generated Python client whose `import_project_media` accepts a sized file stream as well as bytes; in the Agent, the pin to it, an SDK and CLI path that places local media of any accepted size, and a `media import` handle the timeline accepts. Plans 63, 75 and 77 are unaffected in design: media identity stays the content digest of bytes the Runtime owns.

## Completion

- **Works:** a real clip larger than 1 GiB is placed on a timeline from the CLI and by dropping it in the editor, on a real stack; the saved timeline is reopened and the clip plays. The Agent process's peak resident memory during the CLI import stays under 256 MiB.
- **Refuses correctly:** a file over the Runtime's limit is refused by the Runtime before it reads the body, and the message names the limit and the Runtime as its owner.
- **Negative case:** a file that changes while it is being imported is refused with the existing "changed during import" message, and nothing is added to the timeline.
- **The handle:** a handle from `astrid media import` is placed on a timeline; two catalog entries for one digest are still refused as ambiguous.
- **Untouched original:** after each case the source file's bytes, path and modified time are unchanged.
- **Limits of the proof:** one operating system for the live run unless the owner asks for more; Windows long paths and network drives are not proven here. Landing in `release/15/main` and publishing remain the owner's.
