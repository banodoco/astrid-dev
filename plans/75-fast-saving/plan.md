# 75 — One acceptor (fast saving)

**Project:** One acceptor (fast saving)

**Goal:** A one-clip edit on a long-lived timeline is accepted by the Runtime in 300 ms at the median (under 1 s as the first milestone), the same at 3 and at 300 history entries and while an import runs, because the Runtime has one acceptor per timeline that applies what a change wrote and checks only what it introduced, and a commit costs the change and not the history.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 24.5 engineering days committed, plus about 2 conditional (FS-4); no stage 2. On 23 November 2026 [Plan 89](../89-heavy-saves-in-seconds/plan.md) took on FS-0, FS-1, a narrow CC-1 (copy and compare counts at 3, 30 and 300 entries) and CC-11, and Plan 77's save run the verified-base part of CC-2; re-estimate the rest from Plan 89's final measurement.

**Waiting on:** the final installed measurement of [Plan 89](../89-heavy-saves-in-seconds/plan.md), which decides what is left; then a release (the Release 15 Lead proposes it as the lead item of Release 16). The owner took this plan out of Release 15 on 22 November 2026; on 23 November she had the cheap parts done as their own plan, Plan 89, instead. [Plan 81](../81-once-per-command/plan.md) and [Plan 82](../82-reuse-across-commands/plan.md) remain the command half.

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once the owner has said go:** read [tasks.md](tasks.md#start-here), then take FS-0 (permanent stage spans) and FS-1 (measure from the editor) first.

**Vision gaps:** [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

**One acceptor.** One of four plans cut from the save work on 18 November 2026 and settled by the final recommendations, which the owner accepted ([Plan 63](../63-dependable-saving/plan.md) is first and states the **target architecture once**: effect list, command, **acceptor**, proof rule, head, identity and binding, and the rest; this plan is its Runtime half and does not copy it). It was "Fast saving" with two stages; the bisection settled its shape and the owner chose **300 ms with no conditional stage** ([D19](../63-dependable-saving/inputs.md#owner-decisions)). It is queued, in Release 15, and starts on the owner's go.

**The four plans and their order** (solid arrows: cannot start product code before; this plan needs only Plan 63's corpus first, then CC-3 for FS-3b and CC-13 and CC-15 for FS-6):

```
A. Plan 63 Dependable saving ────► C. Plan 76 Editing together
      │  (queue, outcomes, batch, the proof)       (agent beside a person)
      ├────────────────────────────────┐
      ▼                                ▼
D. Plan 18 Extensible editing     B. Plan 75 One acceptor (this plan; parallel with A from day one)
   phase A: agents and packs (after A's server track); phase B: editor gestures (after A's R0 and the week)
```

**The bisection that shaped the plan** (measured by the coordinator, on an APFS realm clone at the Release 14 pins, median of warm one-clip nudges; run 1; run 2 is in progress): **the same nudge costs 3.74 s on Almost Ready and 0.22 s on a one-clip timeline, and `validate_final_candidate` alone is about 2.2 s (about 60%).** So the fixed cost of a commit is already under 300 ms; about 3.5 s is proportional to the document; and one stage holds most of it. The remaining about 1.3 s (load and verify the base, build and digest the document, the reader check, the records, the Runtime's own checks) is my subtraction and not yet split. Trimming repeats cannot reach a second when one stage is 2.2 s and it runs once, so **validating only what the effects touch is the plan, not an option**, and the stage 1 and stage 2 split is dropped.

**The end state.** On "Almost Ready", a one-clip edit is accepted in **300 ms at the median** (under 1 s as the first recorded milestone), the same at 3 and at 300 history entries and while an import runs, **measured from the editor**, and a test fails when it stops being true. The one idea is **a commit costs the change**, by one design: every change is a command the Agent runs on the current head to produce an effect list; **one acceptor per timeline**, one commit at a time, applies it and stores it; the head is settled (immutable history, stored findings), so nothing about it is proved again. What stays proportional to the document is one serialise and hash of the changed revision.

**Three moments, and only one should be felt.** *On screen:* the same frame as the gesture ends (Plan 63). *Kept* (on disk in the browser): within 50 ms of the gesture ending (Plan 63's CC-5b measures it). *Accepted* (the Runtime's head includes it): this plan. With Plan 63 in place the person never waits for an accept; what a fast accept buys is how soon the work is safe outside the browser, how long an agent's change waits to appear, how often two writers lose a race, and that **a pack op, which has no editor preview, shows nothing until the accept, so at 4 s it looks broken** (pack ops therefore need this plan).

**What is in scope.** The tasks moved from Plan 63, with their ids: CC-1 (counters and the scaling test, at 3, 30 and 300 entries), CC-2 (close what is red), CC-9 (two transport tests) and CC-11 (accepted history is immutable); and new work: **FS-0** (permanent stage spans and size fields on the provider's timing line), **FS-1** (measure from the editor), **FS-2** (the reply without the document), **FS-3a** (store the head's findings with the head), **FS-3b** (validate only what the effects touch), **FS-5** (one commit at a time per timeline; it deletes the three attempts and `head_busy`), **FS-6** (the Runtime applies the effect list and re-compares nothing; its first task is the one-day shadow applier experiment) and, conditionally, FS-4 (replay against the net difference). FS-3a, FS-3b and FS-5 are unconditional.

**What is measured and what is not** ([inputs.md](inputs.md#planning-evidence)). **Measured** on the CLI, on a loaded machine: a commit took 8.6 to 9.3 s inside the Runtime in the older profile, the same at 8 and 28 history entries; 67% of it was the legacy-declaration pass; an import waited 5.0 to 6.7 s behind a commit. **Landed since, not measured:** Agent #400, Runtime #62 and #63. **Never measured by anyone:** the time from a gesture ending in the editor to the accept, the browser's write per edit, and the size of the document and of the reply (FS-1).

**Honest limit.** The 300 ms target is reachable only by a proof proportional to the edit: the 0.22 s is the measured floor, what a commit costs when the document is small enough not to matter. Validating only what the effects touch is aimed at the 2.2 s and, if it works fully, leaves a commit of about 1.5 s (my arithmetic, not measured); the remaining 1.3 s needs the verified base kept by immutable revision id (CC-2), the Runtime applying the effect list in place of re-projecting and comparing (FS-6), and the reader check built from the delta. **Each task states its prediction first** ("this stage costs X ms; after, the total will be Y"); FS-0's spans make that a log read. **Run 2 of the bisection is read before FS-3a:** if one removable repeat holds most of the 2.2 s, a small fix may take a large share first.

**Deferred or out of scope:** a faster language, a second process, an "accept now, validate later" reply (a refusal must stay an answer to the request), shrinking what SQLite stores (all of it is under 0.1 s, measured); one object reader as a refactor (filed as an issue); push events instead of polling (Plan 76's nice-to-have); the per-revision snapshot size; the Runtime allocating identities itself (the largest remaining duplication; no plan proposes it). Deferred items with reasons are in [inputs.md](inputs.md#deferred).

## Existing work and decision

We build on the Release 14 cost fixes (Agent #400, Runtime #62 and #63, and the earlier two that took a commit from 187 s to 9 s), on the Runtime's `timeline_commit_timing` line (N11), on Plan 63's rule registry (CC-3: a rule declares what it reads), corpus (CC-7) and edit-kind harness (CC-13), and on the fact that the Runtime's store already keeps `records_json` and the canonical document per accepted commit (so the effect list is already stored, and the shadow applier can test it against real history). The smallest sound approach is to measure first, then make the proof follow the edit: stored findings, read-scoped rules, one commit at a time, the Runtime applying and not comparing. The evidence, the alternatives and the independent checks are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

**Parallel with Plan 63 from day one, other repositories and other people, and a different kind of proof (numbers against a budget, not a model test).** Order: FS-0 and FS-1 first; then FS-3a and FS-3b (the hotspot) as soon as Plan 63's CC-3 lands; CC-1 then CC-2 for the other 1.3 s; FS-5 and CC-11 beside them; FS-6 after Plan 63's CC-13 and CC-15, its shadow-applier experiment (read only) can start earlier. FS-2 builds on Plan 63's CC-4 and CC-5b. FS-4 is the only conditional task. The order and day counts are in [tasks.md](tasks.md#critical-path-and-estimates).

## Interfaces and handoff

**Consumes:** `release/15/main` of each product repository at the cut (identified by SHA at FS-0, in [inputs.md](inputs.md#source-identities)), including Agent #400, Runtime #62 and #63, N5, N6, N10 and N11; Plan 63's corpus and manifest (CC-7), its rule registry (CC-3), and its edit-kind harness and one record shape per effect kind (CC-13, CC-15).

**Produces:** (1) permanent stage spans and a baseline table, and the editor's own timing marks; (2) the counting harness and the scaling test at 3, 30 and 300 entries (Agent and Runtime); (3) accepted history that the database refuses to change; (4) the head's findings stored with it, and validation that follows the effects; (5) one commit at a time per timeline, with no `head_busy`; (6) an acceptor that applies the effect list and compares nothing the provider already computed; (7) a reply that holds ids and a digest, not the document.

## Completion

Done when each of these is true, each guarded by a named test or a recorded measurement (the full list is in [tasks.md](tasks.md#end-state-checks)):

1. **The counts hold at 3, 30 and 300 history entries:** identical computation counters; adding one object causes GETs for that object only; accepted history cannot be updated or deleted.
2. **Commits are serial and the acceptor applies:** two writers on one head land in arrival order with no retry and no `head_busy`; applier(effects, base) equals the provider's document on every matrix row.
3. **The transport proof:** an `ENOBUFS` reply is written in full; an import does not wait behind a commit (re-measured). **The reply holds no document.**
4. **Evidence, recorded and repeated:** the editor-to-accept time on "Almost Ready", at 3 and at 300 entries and during an import, against the target (300 ms at the median; under 1 s as the first milestone).

Negative cases: a same-size rewrite of a CAS object, an `UPDATE` of an accepted history row, a new whole-document copy per commit. Limits: this proves the commit costs the change on the corpus, not a number on the owner's machine; the bisection's arithmetic after FS-3b reaches about 1.5 s and the rest depends on CC-2 and FS-6; FS-6 may be larger than 5 days (3 to 8). Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
