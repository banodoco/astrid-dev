# Refining H3_AV

**Project:** Refining H3_AV

**Goal:** For giving a character a new line, by continuing the shot or with the picture kept, there is one skill an agent can follow from a clip and an intended result to a reviewed take, on real footage, with nothing else.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 13 engineering days for the two dialogue task skills and their tools, part of it provisional, under the assumptions in [inputs](inputs.md#planning-evidence), excluding time waiting on a GPU.

**Waiting on:** The run start and the pilot's measurement of what one GPU run costs, which informs the D8 ceiling reset.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

## Outcome and scope

What done looks like:

1. Each of the two kinds of dialogue edit has one skill document, and a fresh agent given only that skill, the clip and the intended result finishes the edit on a rented GPU without help. The two kinds of picture edit have an outlined skill, run the same way when the edit reaches them.
2. Morpheus says his three new lines in Into the Minkhole, each made by such an agent, and the owner has accepted each take.
3. Where the owner wants the words changed and the picture kept exactly, there is a skill for that too, and she has accepted one of its takes.
4. You point H3 at a clip on your timeline, at any frame rate, size and shape, and it runs; nobody converts a file by hand and nothing is stretched.
5. There is one command and one documented request shape for the three things H3 does: continue a clip, change a region, generate from references. The character swap is the one exception, documented separately as experimental.
6. The result of any other Astrid workflow (a mask, an earlier take) goes into an H3 request by its handle, never as a copied file.
7. Nothing in the pack is unreachable, advertised but unimplemented, or documented but absent.
8. Every tool change in this plan exists because one of those skills needed it.

In scope: the task skills for the Minkhole edit's H3 work and the shared skills above them; and, pulled by those skills, the H3_AV pack's request, source preparation, canvas, sound-inside-footage route, entry point and removals. Four task skills are listed: a new line by continuing the shot (three Morpheus clips), new words with the picture kept, a change inside the picture, and a still becoming a moving shot. The first two are detailed and are this plan's completion; the last two are outlined and run when the edit reaches them and the money allows. This plan does not qualify the still-heavy majority of the cut: six of the nine shots are stills, three of them multi-image sequences. Out of scope, and used from elsewhere: word-level transcription, automatic masks, the transcript structure, comparing takes side by side, and renting the GPU ([inputs](inputs.md#planning-evidence) says where each belongs and [the coverage table](inputs.md#coverage) shows what nothing covers yet). Deferred until a take shows the need: longer voice context, and a voice reference separate from the start clip.

## Existing work and decision

Keep the pack's working spine: one contributed entry (`astrid generate video --entry h3`), the prepare → compile → run → compose → verify stages, the packaged continuation graph, the native masked edit and the reference generation, on the node packs already pinned. Remove what no request can reach or what always errors, document one request shape, and let the pack prepare real footage itself. Solve choices with skills and mechanics with the smallest code, and build a tool only when a task skill needs it. The evidence, the alternatives considered and the removal list are in [inputs](inputs.md#planning-evidence). This plan is drafted at the owner's request; its scope is not yet accepted.

## Sequence and readiness

[Tasks](tasks.md) lists the task skills in order with one loop for all of them: write the skill; give it, the clip and the intended result to a fresh agent; the agent rents a GPU through Astrid and does the edit end to end; record where it stalled; fix the tool or the skill there; repeat with a fresh agent until one finishes unaided; the owner reviews the take. Before each paid trial a fresh agent passes a rehearsal that rents nothing. No rental starts until the RunPod creation-time lifetime bound has independent review; each rental must carry a creation-time deadline and the existing pod watchdog, and an unacknowledged self-stop is refused. First the new line by continuing the shot, on clips 02c, 01 and 04; then new words with the picture kept, which starts after the first accepted take. Under each sits the tool work it needs: real footage of any size by handle and range (automatic source conform exists on Plan 59 task branch `p59/h3-conform`; RH-1 must recheck and integrate it), a short review of that contract before any paid trial builds on it, the placement method rehearsed at no GPU cost, and only those removals that would mislead a trial agent, for the first; sound regenerated inside a time span for the second. The wider removals run in parallel and are required before the final review. Words are checked by listening and masks are supplied by the caller; neither transcription nor a mask workflow is a dependency. GPU spend is the owner's one $25 for all of this work and Plan 59's, with caps set after the pilot measures the cost of a run (D8). Recording this plan authorizes no implementation.

## Interfaces and handoff

Consumes: astrid-agent and VibeComfy at their `release/14/main` heads, plus whatever [Plan 59](https://github.com/banodoco/astrid-dev/tree/release/14/plan-59/plans/59-into-the-minkhole-proof-point)'s H3 pilot track has landed on its `p59/h3-*` branches (re-checked at dispatch); Astrid's existing media handles, timeline edit commands and RunPod pack; the Into the Minkhole rough cut and Matrix reference timelines. Produces: task skills under an `audiovisual-editing` skill, each with the log of the trials that proved it; an H3_AV pack whose request accepts a media handle with a source range, a stated fit and a chosen canvas, and can regenerate sound inside a time span; one documented request shape; a pack with the removal list applied; owner-reviewed takes for the Morpheus lines with their requests and receipts. Plan 59 places those takes in its edit and reuses the skills for its final fresh-agent test on a different timeline. Link implementation pull requests and the completion pull request here when they exist.

## Completion

Task skills RH-2 and RH-5 are complete when, on the integrated branch, a fresh agent given only the synced skills, the clip and the intended result has done each edit end to end on a rented GPU without help, the take is on the timeline by the stated placement method with the target line audible in it, and the owner has accepted it: for RH-2 on clips 02c, 01 and 04; for RH-5 on one Morpheus line, where the picture-kept take proves the mechanics (the picture equals the prepared baseline, the joins are clean) and the owner accepts one take, with or without the mouth region, as new words on that footage. A rejected take, or the money running out first, leaves the project unfinished and is recorded that way. Every example in the skills is admitted by a dry run in a test. No live code path, manifest, packaging declaration or agent-facing document names a removed route; historical records and the tests that guard against a removed route may. Only RH-2 and RH-5 must complete for this plan; RH-7 and RH-8 are outlined, and are either run the same way when the edit reaches them or handed on by the owner with their outlines. Negative cases: footage whose shape differs from the canvas is never stretched; a mask that does not match the prepared clip is refused; a handle from another project is refused before anything is rented; a canvas that is not on the model's grid or is over the budget is refused with the nearest valid size; a request for something H3 cannot do (a voice reference on a continuation, an audio-only request) is refused with the reason and the supported alternative. This proves those clips on that GPU setup, not every clip or model; whether the skills carry to a different film is Plan 59's final test. Merging into `release/14/main` and release remain the owner's and the release manager's steps.
