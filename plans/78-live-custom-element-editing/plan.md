# Live custom-element editing

**Project:** Live custom-element editing

**Goal:** The editor's own agent writes a custom element and applies it with the rest of an edit in one commit, with no restart, no outside script and no page reload.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 4–6 engineering days, one phase.

**Waiting on:** nothing for its base: [Plan 69](../69-project-elements/plan.md)'s product work is on `release/15/plan-69` in all three repositories since 21 November 2026; cut `release/15/plan-78` in astrid-agent from it at run start.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md).

**Vision gaps:** [F-004 — Pack lifecycle](../../vision/gaps/F-004-pack-lifecycle.md) (primary).

**Contributes to closure:** F-004: a real project uses a pinned, locally authored frontend rendering contribution after admission, including failed admission and preserved project references; this is only a portion of its demanding-pack evidence.

## Outcome and scope

A creator asks the editor's agent for an animation change. The agent edits the project pack's files, admits them, and makes **one** timeline commit that points every affected clip at the new element and carries the parameter, text and timing edits with it. The open editor shows the result without a reload, and a pack installed while Astrid is running works on the next command.

Included, all in the Agent:

- **One commit for a mixed edit.** A placement becomes something a `Timeline.commit` function can do alongside its other edits, so seven placements and their edits are one receipt and one undo.
- **No restart after a pack install.** The running Runtime rediscovers elements when a lookup misses, and the install message stops telling people to restart.
- **The skills teach that flow.** The rendering guide's per-clip `place-element` recipe gives way to "admit, then one commit".
- **A live proof** through the editor's chat agent of the four representative edits.

Decided boundaries:

- **Local project-pack code is trusted as the creator's own.** The code already says so (`_check_imports`: "Pack code is trusted build source"). This plan adds no sandbox, provenance check or trust tier, and removes ceremony rather than checks.
- **What stays is integrity, not policing:** compile at admission, the digest-pinned snapshot, the exact revision on each clip, and the editor's digest check before it imports a module. They are what keeps an old timeline rendering the code it was made with.
- **The import rule stays** (React, Remotion and declared files in the pack). It is what makes the snapshot complete; widening it to arbitrary packages is a dependency feature nobody has asked for.
- **Admission and the timeline commit stay two calls.** A wrapper command that merges them would hide which one failed and buys nothing once the commit is a single call.

Left out: hosted or shared-pack isolation, cheaper saves on heavy timelines ([plans 75 and 77](inputs.md#planning-evidence) own that), and the separate defects listed as proposed issues in [inputs](inputs.md#planning-evidence). This plan does not promise a speed number: one commit instead of eight removes seven whole-timeline validations, and the proof records what remains.

## Existing work and decision

Almost everything exists. `Timeline.commit` already takes many edits as one commit, and `place_element` is that same commit with exactly one `clip.set-element` in it. The open editor already reloads admitted elements when a commit changes the element refs it renders. The pack host already picks up a newly installed pack while idle. Two things are missing: a way to stage a placement inside a commit function, and a cache clear when the Runtime's element lookup misses. The plan adds those two, corrects the skills and proves the flow; it builds no new pack, command surface or publishing path. Sources, the critique of the first draft and the alternatives are in [inputs](inputs.md#planning-evidence). The owner set the direction; the specific scope is not yet greenlit.

## Sequence and readiness

LE-1 (batch) and LE-2 (no restart) are independent and run in parallel. LE-4 (the live proof) needs both. One review at the end. The work builds on the plan-69 changes in all three repositories, so it starts once those are on a release line, or from the plan-69 branches if the owner starts it sooner. See [tasks](tasks.md). Recording this plan authorizes no run, release or change to a live stack.

## Interfaces and handoff

Consumes the plan-69 Agent, Runtime and App work (project-pack compile and admission, Runtime serving, the App loader) at the revisions recorded at run start; the donor heads observed while planning are in [inputs](inputs.md#source-identities). Produces one public Agent interface, a placement staged inside `Timeline.commit`, plus corrected skills, and a recorded live proof bound to exact commits. The existing `place_element` call and CLI keep working unchanged. Expected-head, idempotency, conflict and retry behaviour are the existing commit's, not new ones. No release is assigned.

## Completion

On a disposable copy of a heavy project, the editor's chat agent is asked for the four edits and delivers them with one timeline receipt and one history row: seven clips retargeted to two forked elements, their parameter edits, and six added text clips. The open editor shows them without a reload. A pack installed after the Runtime started resolves on the next commit without a restart. No SQL, outside script or detached publish is used.

The record holds the source pins, the prompt, the resulting head, stills of the four edits compared with the intent, and the elapsed time for admission, commit and visible result. Negative cases: a stale head, a wrong or unadmitted revision, a failed compile and a failed commit after a good admission each leave the timeline unchanged and say which step failed. If the exact word-bound timing of the new text clips cannot be committed, the proof uses numeric timing and says so. The proof is local; it shows nothing about hosted isolation or about every project size.
