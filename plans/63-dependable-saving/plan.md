# 63 — Dependable saving

**Project:** Dependable saving

**Goal:** The owner edits a long-lived timeline for a week with no stuck state, every save ends in one of four outcomes the server names, and an edit costs the change.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 37 engineering days (about 15 elapsed with parallel workers); about 33 once the N-items already merged on Release 14 are counted off CC-4, CC-5 and CC-9. The critical path is CC-4, CC-5, CC-10, R0 (about 16 days, all on the App).

**Waiting on:** the owner's choice of release (D9, open; recommended Release 15) and a go to start, because it is queued in no release brief; then the owner's answer on D15 before CC-5 starts (the only decision on the critical path); D14 (persisting verified trust) and D10 (the corpus data) in [inputs.md](inputs.md#owner-decisions).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once the owner has chosen the release and said go:** read [tasks.md](tasks.md#start-here) (prerequisites, repositories, commands), then take CC-5a (the model test, first), CC-7 and CC-1, and CC-4 beside them (CC-4 starts the critical path).

**Vision gaps:** [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

**Dependable saving.** Created on 18 November 2026 by moving Plan 18's Phase 0 (the commit contract) here, with the deltas of the save-category design applied. The owner asked whether stability should come before extensibility ("SO DO WE HAVE A STABILITY PROJECT? … SO IT CAN BUILD ON TOP"); the answer was that the two are separable, and stability goes first. The owner then said not to do it yet, only to record it here: it is queued, in no release brief, and which release carries it is [D9](inputs.md#owner-decisions), open. [Plan 18](../18-timeline-editing/plan.md) (one command layer) starts on this plan's base.

**The end state.** The owner edits a long-lived timeline ("Almost Ready") for a week and meets no stuck state. Every reply to a change is one of four outcomes, named by the server. An edit costs the change, in computation, in transport and in waiting.

**The root cause.** Two things, one on each side of the wire.
- *Server:* nothing in the stack treats an accepted head as settled. Every request re-proves the accepted base from scratch against today's code, and when that disagrees the only outcome is a refusal. That produced commits that took 3 minutes, whole-head refusals ([#842](https://github.com/banodoco/astrid-dev/issues/842)), writers that stored what readers later refuse, and states nothing could discharge ([#732](https://github.com/banodoco/astrid-dev/issues/732)).
- *Editor:* nothing gives an unsettled change one home. A change can be in an outbox owner, a session copy, a draft slot and six React flags at once, and a reply can be classed nine ways by status code. Each of the sixteen incidents on one timeline ([inputs.md](inputs.md#planning-evidence)) is a path through that space nobody designed. Transport had no owner at all: the same object was fetched by three readers, and an accepted commit could lose its reply to a socket error.

No test held a document with a history or with size, so each slipped through.

**The five invariants** are the plan's statements (the plain-language form is [statements.md](statements.md)). Each is held by a named test:

1. **One queue is the only home of unsaved work.** One ordered queue of change records per timeline, in IndexedDB: the existing outbox, one row per timeline. The document on screen is the accepted head with the queue applied. The badge, the bar and what a reload shows are one pure function of that row. Two tabs read the same row, and one of them sends. One gesture is one record; a field edit commits when the edit ends.
2. **Every reply is one of four outcomes, and the server says which.** `accepted` (adopt the head, drop the record), `moved` (apply the same change to the new head and send it), `refused` (these bytes will never be accepted; rule 3), `unavailable` (nothing was decided; send the same bytes again, same key). The reply carries the outcome as a field. Reasons are for people; they never decide behaviour. One decoder, total: no reply or a 5xx is `unavailable`; any reply it cannot read is `refused`. Every request that changes anything carries an idempotency key, so a lost reply is an ordinary `unavailable`. This holds for every mutation the editor makes, uploads included, because all of them go through one `send`.
3. **A refusal leaves the queue, and nothing ever blocks an edit.** On `refused`, that record and the records that depend on it move into a "not saved" list in the same row. The document returns to the head plus what is left. One bar says what and why, with **Restore** and **Dismiss**. A record waiting on `unavailable` stays and retries; the same bar shows it, with Discard. Adding to the queue has no precondition. Any unsaved change can be discarded, in any state, before and after a reload. (The exact form of "leaves the queue" is [D15](inputs.md#owner-decisions), open.)
4. **A check is signed by what it reads, and refuses only what the change introduces.** The delta gate of statement (b), extended to guards on a change's inputs: a selection is signed by identity and bytes, a drop by the track and shot it lands on, not by the whole head. One writer admits what readers will accept.
5. **An edit costs the change: in computation, in transport and in waiting.** Computation: statement (a). Transport: an immutable object's bytes are fetched once per session, through one reader; adding one object reads that object. Waiting: a reply is written by one writer that survives a transient socket error, and a read does not wait behind a commit's lock.

**The contract, in seven statements,** each held by a named test (the full list is in [tasks.md](tasks.md#end-state-checks)). They are Plan 18's Phase 0 statements (a) to (f), with (d) rewritten, (b) extended and (g) new; the lettering is kept so references stay valid.

- **(a) Bounded work.** A commit's work is the change plus one pass over the document, independent of history length. It is stated as counts (closure loads, CAS hashes, opens and stats, timing passes) and held by a scaling test at 3 and at 30 history entries and at one and two timelines. Trust persists: a refused commit or an unrelated write causes no re-hash. No test uses a wall-clock limit.
- **(b) One delta gate.** The registry is the one home of every document invariant (`validate_final_candidate` runs the registered rules; no second list), through `register_rule` for the built-in rules; how packs register rules is Plan 18's TL-1, through the same function and under the same gate. Every rule that reads the whole head reports `{key: signature}` findings through `_preexisting.split_findings`, and only introduced findings block. A function that reads the base never raises on its content. The gate is total (a rule's exception is a finding; the inline `_fail(` calls become rules or named shape preconditions), the grid is generated from the registry and the corpus manifest, and a count of the remaining raise sites only falls. **A guard on a change's inputs is signed the same way: by what it reads.**
- **(c) The editor sends intent and adopts the head (held here by a ratchet; delivered in Plan 18)** ([#852](https://github.com/banodoco/astrid-dev/issues/852)). This plan states it and holds it with a ratchet (no new expected-diff refusal site, CC-8); [Plan 18](../18-timeline-editing/plan.md) delivers it. The shot start and end command ([#838](https://github.com/banodoco/astrid-dev/issues/838)) is Plan 59's, by the owner's decision of 17 November.
- **(d) Every reply is one of four outcomes (accepted, moved, refused, unavailable), named by the server.** A refusal leaves the queue with its dependents and its reason. Unsaved work has one home, one row per timeline, and the screen is drawn from it. Any unsaved change can be discarded, in any state, before and after a reload ([#732](https://github.com/banodoco/astrid-dev/issues/732)).
- **(e) Writers cannot store what readers refuse.** Registry and catalog entries are validated at write time, in one place, both ids or neither; a closure test applies every writer to every corpus head and checks the result cold.
- **(f) One corpus.** Long-lived documents, synthetic or anonymised real shapes, in astrid-agent, run the invariant: every head accepts an unrelated one-field commit and a duplicate, at the stated counts. Two shapes beyond the original set: a selection whose lifecycle advanced, and a head with many audio sources.
- **(g) Bounded transport.** An edit causes transport proportional to the change. An immutable object is fetched once per session through one reader. Every mutating request is idempotent by key, so a lost reply is a retry. A reply is not lost to a transient socket error.

**What is in scope.** CC-1 to CC-8 (CC-4 and CC-5 rewritten), CC-9 (bounded transport, new), CC-10 (new: TL-10's upload half moved in, so a dropped file is a queue record, sent again if cut) and R0. The CC-n ids are kept. What is deleted is listed in [inputs.md](inputs.md#what-gets-deleted); nothing is added except the `outcome` field, `discardScope`, the one bar, the one object reader and the one reply writer.

**What stays in Plan 18** (one home per fact): TL-1 to TL-3, TL-4's headlines, TL-5 and TL-5b (the document as the head plus the queue replayed: the end form of invariant 1, which removes one stored copy and nothing the owner would notice), TL-6 to TL-9, TL-10's command half (a drop is a named command), TL-11 to TL-15 and phase 2.

**What Release 14 already ships, and what this plan adds.** The save fixes already merged on Release 14 carry the behaviour; this plan carries the structure. It builds on what is already merged on `release/14/main` (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63 and App #299 to #300, and the seed of the model test in `localSaveSession.discard.test.ts`) and does not redo it:

- **N1 to N12**, the save-recovery fixes (identities and where each is in the code are in [inputs.md](inputs.md#what-release-14-ships)): the selected-media guard signs identity and bytes only (N1); no 409 is re-sent without the server saying so (N2); Discard is total, through `discardScope` (N3); one bar (N4); one reply writer that survives `ENOBUFS` (N5); each object URL warmed once per session (N6); position fields commit at the end of the edit (N7); the replay throw declined by the bar (N8); an unavailable save retries with backoff (N9); health served without the store mutex (N10); the commit timing line (N11); a failed upload removes its placeholder (N12).
- **The `_reference_basis` fix** (measured as 67% of the 9 s commit on Release 14; [profile](inputs.md#what-release-14-ships)).
- **The seed of the model test:** the scripted `send` with the cases that are true today (Discard, reload, two retained owners, the next edit saves).

Three of those are stopgaps with a named replacement here: N6 (CC-9's reader), N8 (CC-5's deleted throws) and N12 (CC-10). What Release 14 does not give: a guarantee that the category cannot come back. Until this plan lands, a new status or surface can be added without a test failing, an import can still wait behind a commit's lock for as long as the commit runs, and a cut upload is lost if its one replay fails.

**Release.** None yet: the plan is queued and in no release brief. Which release carries it is [D9](inputs.md#owner-decisions), open; the recommendation is **Release 15** (per the stability sequencing note, because the structure changes what is stored in the browser and what goes over the wire, and Release 14 already carries the behaviour). Nothing here starts, and no branches are cut, until the owner chooses and says go. Plan branches then follow the rule: `release/<NN>/plan-63` in astrid-app, astrid-runtime and astrid-agent, cut from `release/<NN>/main`.

**Deferred or out of scope:** the editor moving to send intent for every gesture (Plan 18); a server reply under one second (the invariants bound work; they do not make whole-document validation cheap, and with rule 3 the wait no longer blocks or breaks anything); a redesign of the timeline UI; anything in Release 14 or Plan 59. The deferred items with reasons are in [inputs.md](inputs.md#deferred).

## Existing work and decision

We build on what Release 14 lands, on `discardOversized` (which already moves one kind of refusal out of the queue and becomes the only refusal path), on the existing outbox (it becomes the one row), and on the Agent's `split_findings` and the uniform baseline rule from #842 (they become the registry's gate). The smallest sound approach is to delete the parallel homes for an unsaved change rather than add a mechanism to reconcile them. The evidence, the alternatives, the challenge and the owner's decision are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

**This plan goes first, and Plan 18's phase 1 starts on its base.** It starts when the owner chooses the release (D9) and says go, on `release/<NN>/plan-63` cut from that release's main. **The first task is the model test (CC-5a), grown from the seed;** it starts at once and every later case is added as the outcomes (CC-4) and D15 land. The critical path is CC-4, then CC-5, then CC-10, then R0 (about 16 days). Three lines run beside it: CC-7, then CC-1, then CC-2 (Agent and Runtime); CC-7, then CC-3, then CC-6; and CC-9 alone. CC-8 has no dependency. CC-5 waits on D15. The order and the day counts are in [tasks.md](tasks.md#critical-path-and-estimates). Plan 18's TL-1 (a design task that writes findings, not product code) waits for CC-3, CC-4 and CC-7; Plan 18's RS1, and with it every task that changes product code, waits for R0, this plan's end-state checks **and** a week of the owner editing "Almost Ready" without a stuck state (the week is evidence for the owner's call, not a gate on the code).

## Interfaces and handoff

**Consumes:** `release/<NN>/main` of each product repository at the cut (identified by SHA at CC-1, in [inputs.md](inputs.md#source-identities)), including N1 to N12, the `_reference_basis` fix, Runtime #61 to #63, App #299 to #300, the model-test seed and the Agent's baseline rule from #842.

**Produces,** for Plan 18 and for every later gesture: (1) the counting harness and the scaling test (Agent and Runtime), whose golden counts may only fall; (2) the rule registry and the generated rules-by-legacy-shapes grid; (3) the four-outcome reply and the App's one decoder, `send(): Outcome`; (4) the one queue row, the one bar and the model test; (5) one write-time admission function for registry and catalog entries; (6) the corpus and its manifest; (7) the one object reader and the idempotent route table; (8) uploads as queue records. Limits: Runtime schema bumps still need a paired App pin; whether a `File` stored in the queue row survives a reload in every supported browser is confirmed by CC-10 before uploads move.

## Completion

Done when each of these is true, each guarded by a named test that fails if it stops being true (the full list with test names is in [tasks.md](tasks.md#end-state-checks)):

1. **The model test passes.** A scripted `send` plays every outcome at every queue position, a lost reply, a cut upload, a reload between any two steps and a second tab. After each step: adding an edit never throws; the screen equals the function of the row; every record is accepted, listed as not saved, or waiting; Discard and Dismiss leave a saved state.
2. **The ratchet counts hold at 3 and at 30 history entries:** identical computation counters; adding one object causes object GETs for that object only; the three scans are at zero.
3. **The end-state checks P0-1 to P0-7 are true,** including the route table (every mutating route sent twice with one key has one effect) and the `ENOBUFS` writer test.
4. **As evidence, not a gate:** the commit timing line on "Almost Ready", and a week of the owner's editing with no stuck state.

Negative cases: a same-size rewrite of a CAS object, a refused commit followed by an unrelated edit, a new rule added without a registry row, a half association written, a refusal then a reload, a lost reply, a cut upload and two tabs. Limits: this proves the save path is bounded and consistent on the corpus and under the model test, not on every document a creator can make or every browser; a server reply under one second is not promised. Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
