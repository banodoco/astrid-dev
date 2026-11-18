# 64 — Fast saving

**Project:** Fast saving

**Goal:** A one-clip edit on a long-lived timeline is accepted by the Runtime in under a second (then 200 ms if that is worth it), the same at 3 and at 300 history entries and while an import runs, because a commit costs the change and not the history.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Stage 1 (under 1 s) about 11 engineering days; stage 2 (200 ms) about 9 more, **conditional on stage 1's numbers**. Runs in parallel with Plan 63 from day one.

**Waiting on:** the owner's choice of release (open, see [Plan 63's D9](../63-dependable-saving/inputs.md#owner-decisions); recommended with Plan 63) and a go to start, because it is queued in no release brief; it needs only Plan 63's corpus (CC-7), which goes first; stage 2 waits on stage 1's measurements.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once the owner has chosen the release and said go:** read [tasks.md](tasks.md#start-here), then take FS-1 (measure from the editor) first.

**Vision gaps:** [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

**Fast saving.** One of four plans cut from the save work on 18 November 2026 (the owner asked whether to split it into stability, speed, multi-edit robustness and extensibility; the structure is from the independent four-questions check, accepted by the main thread). The owner then said to add the work to astrid-dev and not do it yet: all four are queued, in no release, with the release open.

**The four plans and their order** (solid arrows: cannot start product code before; this plan needs nothing from the others except Plan 63's corpus, a first task they share):

```
A. Plan 63 Dependable saving ─────► C. Plan 65 Editing together
        │  (the queue, four outcomes,          (narrow reads, notice,
        │   batch, rule gate)                   bundle survives `moved`)
        ▼
D. Plan 18 Extensible editing          B. Plan 64 Fast saving   (this plan; parallel with A from day one;
        (after A's R0 and the owner's week)                       makes agents stop losing three times in C)
```

**The end state.** On "Almost Ready", a one-clip edit is **accepted in under 1 s (stage 1)**, then **200 ms at the median and 500 ms at the 95th percentile (stage 2, if worth it)**, the same at 3 and at 300 history entries and while an import runs, **measured from the editor**, and a test fails when it stops being true. The one idea is **a commit costs the change**: in computation (a settled head: an accepted head is a fact, so it is not re-proved), in transport and in waiting (an import never waits on a commit).

**Three moments, and only one should be felt.** *On screen:* the same frame as the gesture ends; never waits for anything (Plan 63's rule). *Kept* (on disk in the browser): within 50 ms of the gesture ending (Plan 63). *Accepted* (the Runtime's head includes it): this plan. With Plan 63 in place the person never waits for an accept, so a slow accept no longer costs them an edit. What a fast accept still buys: how soon the work is safe outside the browser, how long an agent's change waits to appear (two save times), and how often two writers lose a race and validate again. Under a second buys nearly all of that.

**What is in scope.** The tasks moved from Plan 63, with their ids: CC-1 (counters and the scaling test, now also at 300 entries), CC-2 (close what is red), CC-9 (two transport tests) and CC-11 (accepted history is immutable); and new work: FS-1 (measure from the editor, first), FS-2 (the reply without the document) and, conditionally, stage 2: FS-3 (validate what the change touches), FS-4 (replay against the net difference) and FS-5 (one commit at a time per timeline).

**What is measured and what is not** ([inputs.md](inputs.md#planning-evidence)). **Measured** on the CLI, on a loaded machine: a commit took 8.6 to 9.3 s inside the Runtime, the same at 8 and 28 history entries; 67% of it was the legacy-declaration pass; an import waited 5.0 to 6.7 s behind a commit. **Landed since, not measured:** Agent #400 (the legacy pass builds its bases once; about 3 s inferred, which is 33% of 9 s), Runtime #62 (verified history kept across unrelated writes, so an import never forces a re-walk) and #63 (one reply writer, health off the mutex, commit timing at INFO). **Never measured by anyone:** the time from a gesture ending in the editor to the accept, the browser's write per edit, and the size of the document and of the reply. That is FS-1.

**Honest limit.** Stage 1's arithmetic (removing the repeats leaves compile, evaluate and one pass of the rest) reaches about **1.5 to 2 s**, not under a second. Under a second needs the evaluate cost (204 rule evaluations, `lookup.py:332`, unread code) to fall too. **If stage 1 measures above a second, that is the finding that starts stage 2**; stage 2 is written as conditional for that reason.

**Deferred or out of scope:** a faster language, a second process, an "accept now, validate later" reply (a refusal must stay an answer to the request), shrinking what SQLite stores (all of it is under 0.1 s, measured); one object reader as a refactor (filed as an issue); push events instead of polling (Plan 65's nice-to-have); the per-revision snapshot size (a storage-format question). Deferred items with reasons are in [inputs.md](inputs.md#deferred).

## Existing work and decision

We build on the Release 14 cost fixes (Agent #400, Runtime #62 and #63, and the earlier two that took a commit from 187 s to 9 s), on the Runtime's `timeline_commit_timing` line (N11) and on Plan 63's rule registry (CC-3: a rule declares what it reads) and corpus (CC-7). The smallest sound approach is to measure first, remove repeated whole-document work (stage 1), and only then make validation follow the change (stage 2), because stage 2 is the principled change and tuning is not. The evidence, the alternatives and the independent check are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

**Parallel with Plan 63 from day one, other repositories and other people, and a different kind of proof (numbers against a budget, not a model test).** Order inside the plan: FS-1 first (it sets the baseline and decides stage 2); CC-1 then CC-2 (the critical path, about 7 days); CC-11, CC-9 and FS-2 beside them; FS-2 builds on Plan 63's CC-4 and CC-5b. Stage 2 (FS-3, FS-4, FS-5) starts only on stage 1's numbers. The order and day counts are in [tasks.md](tasks.md#critical-path-and-estimates).

## Interfaces and handoff

**Consumes:** `release/<NN>/main` of each product repository at the cut (identified by SHA at FS-1, in [inputs.md](inputs.md#source-identities)), including Agent #400, Runtime #62 and #63, N5, N6, N10 and N11; Plan 63's corpus and manifest (CC-7) and, for stage 2, its rule registry (CC-3).

**Produces:** (1) the editor's own timing marks and a baseline table; (2) the counting harness and the scaling test at 3, 30 and 300 entries (Agent and Runtime); (3) accepted history that the database refuses to change; (4) a reply that holds ids and a digest, not the document; (5) if stage 2 runs, validation that follows the change.

## Completion

Done when each of these is true, each guarded by a named test or a recorded measurement (the full list is in [tasks.md](tasks.md#end-state-checks)):

1. **The counts hold at 3, 30 and 300 history entries:** identical computation counters; adding one object causes GETs for that object only; accepted history cannot be updated or deleted.
2. **The transport proof:** an `ENOBUFS` reply is written in full; an import does not wait behind a commit (re-measured).
3. **The reply holds no document.**
4. **Evidence, recorded and repeated:** the editor-to-accept time on "Almost Ready", at 3 and at 300 entries and during an import, against the stage's target.

Negative cases: a same-size rewrite of a CAS object, an `UPDATE` of an accepted history row, a new whole-document copy per commit. Limits: this proves the commit costs the change on the corpus, not a number on the owner's machine, and stage 1's arithmetic reaches only 1.5 to 2 s; stage 2 is not promised. Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
