# Refining H3_AV

**Project:** Refining H3_AV

**Goal:** A creator or an agent can continue a clip, change a region of a shot or generate from references with H3 by asking for the edit, on real footage, guided by skills.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 7 engineering days, excluding time waiting on a GPU.

**Waiting on:** The owner's decisions D1–D6 in [inputs](inputs.md#owner-decisions) and an independent critique of this plan.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

## Outcome and scope

What done looks like:

1. You point H3 at a clip on your timeline, at any frame rate and size, and it runs; nobody converts a file by hand.
2. There is one command and one request shape for the three things H3 does: continue a clip, change a region, generate from references.
3. The result of any other Astrid workflow (a mask, an earlier take) goes into an H3 request by its handle, never as a copied file.
4. Nothing in the pack is unreachable, advertised but unimplemented, or documented but absent.
5. An agent that has never used H3 reads one short skill, chooses the right operation and the right cut point, and knows when to stop and ask.
6. Morpheus says a new line in Into the Minkhole, made through exactly this path, and the owner has heard it.
7. A different person's similar shot goes through the same path from the skills alone.

In scope: the H3_AV pack's request, source preparation, entry point, removals and documentation, and the cross-pack skill that tells an agent how to do an audiovisual edit. Out of scope, and consumed from elsewhere: transcription, automatic masks, the transcript structure, placing and comparing takes, and renting the GPU ([inputs](inputs.md#planning-evidence) says where each belongs). Deferred until evidence asks for it: regenerating sound inside existing footage, and longer voice context.

## Existing work and decision

Keep the pack's working spine: one contributed entry (`astrid generate video --entry h3`), the prepare → compile → run → compose → verify stages, the packaged continuation graph, the native masked edit and the reference generation. Remove what no request can reach or what always errors, document one request shape, and let the pack prepare real footage itself. Solve choices with skills and mechanics with the smallest code. The evidence, the alternatives considered and the removal list are in [inputs](inputs.md#planning-evidence). This plan is drafted at the owner's request; its scope is not yet accepted.

## Sequence and readiness

Five steps in [tasks](tasks.md), the first one detailed: H3 accepts real footage by handle and range; the Morpheus shot on a GPU; remove what is not the product; write the skills; a fresh agent repeats it on a different shot. Step 1 unblocks the pilot that is refused today. Steps 3 and 4 do not wait for the GPU. GPU spend comes from the Plan 59 budget the owner set (at most $2 an hour; $3 for the pilot, $6 for experiments, $3 for the fresh-agent trial), not a new one. Recording this plan authorizes no implementation.

## Interfaces and handoff

Consumes: astrid-agent and VibeComfy at their `release/14/main` heads, plus whatever [Plan 59](https://github.com/banodoco/astrid-dev/tree/release/14/plan-59/plans/59-into-the-minkhole-proof-point)'s H3 pilot track has landed on its `p59/h3-*` branches (re-checked at dispatch); Astrid's existing media handles, timeline edit commands and RunPod pack; the Into the Minkhole rough cut and Matrix reference timelines. Produces: an H3_AV pack whose request accepts a media handle with a source range and a stated fit; one documented request shape; a pack with the removal list applied; an `audiovisual-editing` skill and a one-screen H3_AV skill with tested examples; an owner-reviewed Morpheus take with its request and receipts. Plan 59 consumes all of these for its dialogue shots and its final fresh-agent test. Link implementation pull requests and the completion pull request here when they exist.

## Completion

On the integrated branch: the pinned Morpheus request, naming its source by handle and range, is admitted and runs on a GPU without any hand-prepared file, and the owner has reviewed the take; every example in the skills is admitted by a dry run in a test; no test, document or manifest names a removed route; a fresh agent given a different clip and only the skills produces an admitted request and one generation, with its actions and stumbles recorded. Negative cases: footage whose picture shape differs from 16:9 is never stretched; a request for something H3 cannot do (sound regenerated inside existing footage, a voice reference on a continuation) is refused with the reason and the supported alternative. This proves those clips on that GPU setup, not every clip or model. Merging into `release/14/main` and release remain the owner's and the release manager's steps.
