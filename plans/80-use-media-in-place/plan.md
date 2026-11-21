# Use media in place

**Project:** Use media in place

**Goal:** A creator or agent uses media already on the computer without uploading it or paying for a second copy on disk: first by an instant clone where the file system allows, and later, if the owner still wants it, by linking to the file where it is.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Phase 1, the clone, 4 to 6 engineering days. Phase 2, true links for agents, more than the 22 days first drafted; it is re-estimated by its contract task (LK-1). Phase 3, the editor and automatic copy-in, is deferred and not estimated.

**Waiting on:** the owner's decisions D1 to D7 in [inputs.md](inputs.md#owner-decisions), above all D6 (the clone first) and D7 (reversing an earlier decision); [Plan 79](../79-local-media-any-size/plan.md), whose streaming copy is the fallback; and, for phase 2 only, the saving plans ([63](../63-dependable-saving/plan.md), [75](../75-fast-saving/plan.md), [77](../77-saving-holds-on-a-heavy-timeline/plan.md)) landing first.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [F-003 — Creative execution isn't yet dependable end to end](../../vision/gaps/F-003-creative-execution.md) (primary): a creator's footage is usable where it already lives. [F-002 — User control and recovery aren't fully proven](../../vision/gaps/F-002-safe-user-control.md) (supporting): the creator decides what Astrid may read. Neither route names this plan, so there is no `Contributes to closure` line.

## Outcome and scope

Today every clip is copied into Astrid's store before it can be used. The copy is safe, but it doubles the disk space, takes time for large footage, and is the step where size limits and lost uploads appear.

**Phase 1 — the clone.** When an agent or the CLI adds a file that is on the same volume as Astrid's store, and the file system can clone (APFS on macOS, Btrfs and reflink-enabled XFS on Linux, ReFS on Windows), the Runtime clones it into the store instead of receiving its bytes. A clone is instant and uses no extra disk until one of the two files changes. Astrid's copy is a snapshot: later edits to the original do not reach it. Everywhere else it falls back to Plan 79's streaming copy. Nothing about a clip's identity, saving, preview, render or export changes.

**Phase 2 — true links, for agents.** A file is linked by its path and read where it is, with one folder the creator grants, changed and missing states, relink, and an explicit copy-in command. This reverses an earlier decision (D7) and changes what a clip's identity means, so it starts with a written contract and a review stop.

**Phase 3 — deferred.** The editor's states, relink and folder browser, and automatic copy-in for export and rented machines.

**Not included:** watching folders for new files, proxies or transcoding of linked media, links on rented or remote machines, and network-drive reliability beyond showing "missing".

## Existing work and decision

Astrid had this once. A storage mode called `external_local` kept paths to the user's files, with relocation and fingerprint checks, and it was retired on purpose: a saved path gave the application continuing authority to read that location, so local execution was narrowed to bytes the Runtime owns. No data-loss incident was found behind that decision. Phase 2 brings the authority back in a narrower form, and the owner should decide that knowingly (D7).

The independent critique recommended building the clone first. It gives most of the disk and time saving on eligible volumes, keeps every guarantee the saving plans rely on, and the Runtime already has a clone helper. The findings, the options and the critique are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

1. **Phase 1: LK-0,** after Plan 79's streaming import exists. It measures the disk used, the time taken and that editing the original leaves Astrid's copy unchanged.
2. **The owner decides** whether phase 2 is still wanted, having used the clone (D6).
3. **Phase 2: LK-1, the contract, then RS1,** a review stop. Then one granted folder (LK-2), link and read (LK-3), commit rules (LK-4), the CLI and SDK (LK-5), preview and render (LK-6), and an explicit copy-in command (LK-7).
4. **LK-8, the live proof, then R.**

**Real dependencies:** Plan 79 for LK-0. For phase 2, Plan 63's outcomes: LK-4 needs two new ones, "temporarily unavailable" and "stale selection", and must not slow the commit path that Plans 75 and 77 are measuring.

**Unresolved:** D1 to D7. Recording this plan authorizes no implementation. Task details are in [tasks.md](tasks.md).

## Interfaces and handoff

**Consumes:** the Runtime's import validation and catalog publication, its clone helper (`runtime_protocol/fsclone.py`), and Plan 79's streaming import. For phase 2, the media selection and commit contract as Plan 63 leaves it. Exact commits are recorded at run start.

**Produces:** phase 1, a same-host import that clones, with no new record type. Phase 2, a linked-media record and its rules in the Runtime's `contract/` folder, with an executable schema, and commands to link, relink and copy in. **Compatibility limits, published before any link is accepted:** a project with linked media is not portable until its files are copied in; a linked file larger than the Runtime's object limit, or deleted or overwritten, cannot later be exported, recovered or sent to a rented machine. Older Agents and editors must refuse a linked selection clearly.

## Completion

**Phase 1:**

- **Works:** on an eligible volume, a multi-gigabyte file is added from the CLI in seconds; the store's allocated space grows by far less than the file's size; the clip plays and renders.
- **Snapshot:** the original is edited afterwards; Astrid's clip is unchanged.
- **Fallback:** on a volume that cannot clone, or across volumes, the same command succeeds by streaming, and says which it did.
- **Untouched original:** Astrid never writes to, moves or deletes the source file.

**Phase 2, to be made exact by LK-1:**

- **Works:** a file in the granted folder is linked and placed from the CLI, plays and renders, and the store has not grown by its size.
- **Changed and missing:** each is flagged; a timeline with a missing link still opens and saves; accepting new content makes a new revision that undo can reverse.
- **Boundary:** a path outside the granted folder, through a symlink or a case alias, is refused.
- **Negative case:** a file swapped or edited in place is never rendered as the original.

**Limits of the proof:** one operating system per phase unless the owner asks for more, so cross-platform behaviour is not priced here. Landing and publishing remain the owner's.
