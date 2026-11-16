# Into the Minkhole proof point

**Project:** Into the Minkhole proof point

**Goal:** A creator finishes Into the Minkhole in Astrid, and a weaker agent can repeat the editing workflow on another timeline.

**Status:** active

**Owner:** Hannah

**Estimate:** TBD; the work advances one creative task at a time.

**Waiting on:** Owner decisions recorded under D3: whether `release/14/plan-59` in timeline-composition becomes `main`, the missing license field, and which stray branches and copies the owner deletes.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary); [F-008 — Portable generation](../../vision/gaps/F-008-portable-generation.md) (supporting).

## Outcome and scope

What done looks like:

1. You open Into the Minkhole and the Matrix shots fill the frame edge to edge, with no black bars.
2. That frame looks the same in the editor, in an export, and in the picture an agent pulls from the CLI, because all three read from one place.
3. On any clip you can see and change Fit/Fill and crop, and changing one never moves the other.
4. One command gives an agent a single clean frame of any moment, and it never reports success while handing back nothing.
5. The archive you handed over imports on the release build with one command.
6. Morpheus says the new lines in his own voice with his mouth matching, using a technique you chose after hearing real attempts side by side.
7. An agent asks "what is said in this clip, and when?" and gets words with timestamps, for source footage and for anything generated.
8. An agent says "change the mouth in this shot" and gets a mask without painting one.
9. A generated take arrives next to the shot it's for; you compare takes, pick one, and it's on the timeline.
10. A cheaper agent, given a different timeline, a script and only the skill, makes a comparable edit and stops only to ask you taste questions.

## Existing work and decision

Extend Astrid's existing timeline, rendering, transcription and H3 tools as each creative task needs them. The live sequence and blocker record are in [tasks.md](tasks.md); concise prior-art and source evidence are in [inputs.md](inputs.md#planning-evidence). This work is through Astrid's own tools: fix a blocker at its cause, or file an issue when useful work is too large for now. No workarounds.

## Sequence and readiness

Use the loop in [tasks.md](tasks.md): take the next creative task, attempt it with Astrid, diagnose and properly fix blockers (or file an issue), return to the creative task, and record what was learned for the skill. Later tasks are expected to change as the work teaches us. Owner taste decisions return to Hannah. Keep the $25 RunPod ceiling and its split in [inputs.md](inputs.md#owner-decisions). The owner decided on 16 November 2026 to include this work in Release 14; adding it to the release's Included plans list is the release manager's step.

## Interfaces and handoff

Consume the supplied timeline-v1 archives and the actual Release 14 source heads recorded at dispatch. Produce a finished edit in Astrid and a skill/runbook that lets a weaker agent repeat it on another timeline. Record exact revisions, artifacts and proof in the live task record as they become available. The composition source has been recovered and its owning repository builds the package; owner decisions and consumer adoption remain open.

## Completion

Complete the ten outcomes above through Astrid, with the owner reviewing creative choices and the final result. Then have a fresh weaker agent use only the skill on a different timeline, stopping only for taste questions. The task log records evidence and remaining limits; a finished plan does not itself merge or publish the work. Release 14 inclusion is recorded by the release manager in [releases/14.md](../../releases/14.md).
