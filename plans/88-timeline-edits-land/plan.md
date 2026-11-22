# Timeline edits land and hold

**Project:** Timeline edits land and hold

**Goal:** An agent can make the edits a real film needed on a heavy timeline (swap a clip's media, move word-anchored clips, remove and restore clips) on a build of `release/15/main`, and each edit is confirmed by reading it back and by a render.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 6 engineering days: 1 to land the two sound fixes, 2 for the word-anchored retime rule, 3 for the edit loop on the test timeline.

**Waiting on:** [Plan 87](../87-render-works/plan.md) reaching a working render (its RN-1); decisions T1 and T2 in [inputs.md](inputs.md#owner-decisions); agreement with the managers of Plans 69 and 77 on the boundary; a claimed run.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog is generated.

**Vision role:** Foundational enabler — an agent that cannot change a clip on a real timeline cannot finish a film. [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) owns how saves are built, [Plan 76](../76-editing-together/plan.md) agents editing together, [Plan 69](../69-project-elements/plan.md) project elements; this plan lands three existing fixes and proves real edits end to end.

## Outcome and scope

On 22 November 2026 a session made about twenty edits to a film timeline of 621 clips. Simple parameter edits landed. Three kinds did not: replacing the media on an existing shot clip, moving clips that are anchored to spoken words, and undoing its own additions. The session worked around them (overlay clips, a skipped edit) and wrote three fixes. Two are sound; one must be replaced before it ships.

**In scope**

1. Land the media-swap fix and the legacy-overrun fix on Release 15 with their missing tests.
2. Replace the word-provenance exemption with the narrower rule both reviews asked for.
3. Run an edit loop on a test timeline: make each kind of edit that failed, confirm it by read-back and by a render from Plan 87's stack, and fix what breaks if it belongs here.
4. Convert the film's workarounds back: the overlay clips become in-place media swaps, and the skipped pause edit is made.

**Not in scope**

- Edits that fold unrelated rewrites into a commit ([#1401](https://github.com/banodoco/astrid-dev/issues/1401)): Plan 77.
- The shared outbox and sessions blocking each other ([#1402](https://github.com/banodoco/astrid-dev/issues/1402)): Plan 76.
- Full authenticated word binding for shot clips: [Plan 18](../18-timeline-editing/plan.md) phase A. This plan lands only the bounded rule in TE-3.
- Restoring a removed clip or reverting a range ([#1430](https://github.com/banodoco/astrid-dev/issues/1430)), the delete guard ([#1406](https://github.com/banodoco/astrid-dev/issues/1406)), item-scoped list removal ([#1409](https://github.com/banodoco/astrid-dev/issues/1409)), unreadable outgoing changes ([#1431](https://github.com/banodoco/astrid-dev/issues/1431)): issues. The loop records how far each blocks real work and adds that evidence to the issue.
- Anything about rendering: Plan 87.

## Existing work and decision

**What exists.** Three commits on astrid-agent [`release/14/r6-fixes`](https://github.com/banodoco/astrid-agent/tree/release/14/r6-fixes), cut from a commit already in `release/15/main`:

| Change | Commit | Verdict | Here |
| --- | --- | --- | --- |
| Media swap keeps shot clips: footage elements accepted, legacy entries without pins handled, new media admitted by the Runtime, one route for SDK, CLI and document publisher | `24740fdf` | Sound in two reviews; cherry-picks cleanly onto Release 15 | TE-1 |
| An unchanged legacy overrun survives a pure start shift | `ad10ff6d` | Ship after one review and three tests | TE-2 |
| A word-anchored shot clip may change its interval | `d4bf28e4` | Replace. It lets a clip move without proof that the narration moved with it; a later reflow can snap the clip back | TE-3 |

Reviews: [code review](../87-render-works/evidence/review/ASTRA-530.md), [verdicts](../87-render-works/evidence/shipplan/VERDICTS.md). Defect write-ups: [media swap and word binding](../87-render-works/evidence/occ/bug-evidence-pack.md), [write-path defects](../87-render-works/evidence/edits/DEFECTS.md). All evidence lives with Plan 87.

**The fixes were never exercised live.** The Runtime loads these guards from its installed Agent at start-up, and the session's stack could not be updated in place. Tests pass; no real edit has gone through them.

**The decision.** Land what is sound, replace what is not, then prove it by doing the real edits. The loop is the acceptance test, as in Plan 87. Where the loop hits a defect that Plan 77, 76 or 69 owns, it stops on that edit, records the evidence on the owner's issue, and moves to the next edit.

## Sequence and readiness

**Branch.** `release/15/plan-88` in astrid-agent, cut from `release/15/plan-87` once Plan 87's RN-1 is done, so the loop has a stack that can render. It lands on `release/15/main` after Plan 87 through the Release 15 Lead.

1. TE-1 and TE-2: cherry-pick, add tests, confirm on the stack with one real swap.
2. TE-3: the retime rule, behind decision T1.
3. TE-4: the edit loop on the test timeline.
4. TE-5: the film's workarounds converted back, as the last real use.

**Blocked on a decision:** TE-3 on T1; TE-4's timeline on T2.

**Risks**

- Plans 69 and 77 are active in the same files (`_commit_timing_validation.py`, `commit_session.py`). Agree the boundary before TE-1; rebase often.
- TE-3's rule needs the product's own word resolver to be callable at commit time. If it is not, TE-3 becomes a refusal with a supported alternative and the ripple edit waits for Plan 18.
- The loop may mostly produce evidence for other plans. That is an acceptable outcome; the plan still lands TE-1 to TE-3.

## Interfaces and handoff

**Consumes:** Plan 87's branch and stack; the three donor commits; the test timeline; the film project with its overlay clips and their undo list ([overlay evidence](../87-render-works/evidence/overlay/FRICTION.md)).

**Produces:** media replacement on shot-owned footage clips through one route; a retime rule that cannot leave a clip disagreeing with its word; a recorded edit loop with each edit's result.

**Handoff:** the branch, the loop log, and evidence comments on the issues owned by Plans 69, 76 and 77.

## Completion

- On a build of the plan branch, each edit in the loop either lands and reads back exactly as intended, with a render showing it, or is stopped by a defect with an issue number.
- Media swap and ripple retime both land on word-anchored shot clips of the test timeline, and a dry-run reflow afterwards moves no clip.
- The film's eleven overlay clips are gone, replaced by in-place swaps; the pause after "two million" is tightened; the film renders whole on Plan 87's stack.
- Limits: one test timeline and one film; agents editing at the same time are not covered.
