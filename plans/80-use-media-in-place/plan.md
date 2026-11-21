# Use media in place

**Project:** Use media in place

**Goal:** A creator or agent uses any media file already on the computer in a timeline without importing it: Astrid links to the file where it is, takes no second copy, and says plainly when the file has changed or gone.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 22 engineering days (15 to 25), in two phases: phase A, agents and the Runtime, about 13; phase B, the editor, about 9. Provisional until the independent critique and the contract task.

**Waiting on:** the owner's decisions D1 to D6 in [inputs.md](inputs.md#owner-decisions); the independent critique; [Plan 79](../79-local-media-any-size/plan.md), whose streaming copy is this plan's fallback; and the saving plans ([63](../63-dependable-saving/plan.md), [75](../75-fast-saving/plan.md), [77](../77-saving-holds-on-a-heavy-timeline/plan.md)) landing first, because this plan changes what a clip's identity means.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary): a creator's footage is usable where it already lives. [F-002 — User control and recovery aren't fully proven](../../vision/gaps/F-002-safe-user-control.md) (supporting): the creator decides which folders Astrid may read. Neither route names this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Today every clip is copied into Astrid's store before it can be used. The copy is safe, but it doubles the disk space, takes time for large footage, and is the step where size limits and lost uploads appear. This plan adds a second way to use a file: a **link**.

**Included:**

- **Linked media.** A file is linked by its path. Astrid records its size, times and content digest, and reads it where it is. Nothing is copied, moved or changed.
- **Linked folders.** The creator names the folders Astrid may read. A path outside them is refused.
- **Honest states.** A linked file is shown as available, changed, or missing. A changed or missing file never silently alters a timeline: existing clips are flagged, and new uses are refused until the creator relinks or accepts the new content.
- **Relink.** A missing or moved file is pointed at its new place, and accepted only if the content matches, or the creator says to accept the difference.
- **Copy in when owned bytes are needed.** Export, a rented machine and recovery copy the file into the store at that moment, using Plan 79's streaming import.
- **From the editor too.** The editor adds media by browsing the linked folders through the Runtime, since a browser never learns a dropped file's path.

**Copying stays, and stays the default** unless the owner decides otherwise (D2). Drag and drop into the editor still copies.

**Not included:** watching folders for new files, proxies or transcoding of linked media, links on rented or remote machines, and network-drive reliability beyond showing "missing".

## Existing work and decision

The Runtime's store identifies media by content digest and skips re-hashing because nothing else can write to it. Preview, the renderer, export, recovery and rented machines all read from that store. A link breaks the assumption all of them rest on, so the load-bearing part of this plan is one written contract for linked media (LK-1), reviewed before any code. There is a leftover start in the editor (saved browser file handles and a "local" storage mode) that is stubbed out; LK-1 decides whether any of it is reused. The findings, the options and the cheaper alternative (a copy-on-write clone, D6) are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **LK-1, the contract, then RS1,** a review stop. Everything else builds on it.
2. **Phase A (agents and the Runtime):** linked folders (LK-2), linking and reading (LK-3), commit rules (LK-4), the SDK and CLI (LK-5), copy in (LK-6), preview and render (LK-7). An agent can then use a linked file end to end.
3. **Phase B (the editor):** states and relink (LK-8), adding by browsing (LK-9), wording (LK-10).
4. **LK-11, the live proof, then R.**

**Real dependencies:** Plan 79 for LK-6. The saving plans for LK-4, which adds a refusal to the commit path they are stabilising; starting LK-4 before Plan 63's four outcomes exist would mean writing it twice.

**Unresolved:** D1 to D6, and whether D6's cheaper clone delivers enough that this plan should wait. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's media selection and verification contract and its commit refusals, as Plan 63 leaves them; Plan 79's streaming import. Exact commits are recorded at run start.

**Produces:** a linked-media record and its rules in the Runtime's `contract/` folder; SDK and CLI commands to link, relink and copy in; editor states for linked media. **Compatibility limit:** a project with linked media is not portable until its files are copied in; export does that. Older Agents and editors must refuse a linked selection clearly, never misread it.

## Completion

- **Works:** a multi-gigabyte file in a linked folder is placed on a timeline from the CLI and from the editor, plays and renders, and Astrid's store has not grown by the file's size.
- **Changed file:** the file is edited outside Astrid; the clip is flagged as changed, a new use is refused naming the file, and the creator can accept the new content or relink.
- **Missing file:** the file is moved; the clip is flagged as missing, the timeline still opens and saves, and relinking to the moved file restores it.
- **Boundary:** a path outside the linked folders is refused, from the SDK, the CLI and the editor.
- **Owned bytes:** export, and a job on a rented machine, succeed with linked media by copying in, and say that they did.
- **Negative case:** a file swapped for a different one at the same path is never rendered as the original.
- **Untouched original:** Astrid never writes to, moves or deletes a linked file.
- **Limits of the proof:** one operating system for the live run unless the owner asks for more; removable and network drives are proven only as far as "missing". Landing and publishing remain the owner's.
