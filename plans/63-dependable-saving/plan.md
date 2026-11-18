# 63 — Dependable saving

**Project:** Dependable saving

**Goal:** The owner edits a long-lived timeline for a week with no stuck state, every change to a timeline, from the editor or from an agent, ends in one of four outcomes the server names, and an edit costs the change.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 34 engineering days (about 12 elapsed with parallel workers), in two independent tracks: the App about 12.5 (critical path about 11.5: CC-4, CC-5b, CC-10, R0), the Agent and Runtime about 20, review 2. The lean form of an independent check on 18 November 2026 was about 31.5 (the first draft said 37); the agent-edits check added about 2.5 for the Agent track.

**Waiting on:** the owner's choice of release (D9, open; recommended Release 15) and a go to start, because it is queued in no release brief; then the owner's answer on D15 before CC-5b starts (the only decision on the critical path); D14 (persisting verified trust) and D10 (the corpus data) in [inputs.md](inputs.md#owner-decisions).

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones. **To begin once the owner has chosen the release and said go:** read [tasks.md](tasks.md#start-here) (prerequisites, repositories, commands), then take CC-5a (the model test, first), CC-4 and CC-7 and CC-1 beside it (CC-4 starts the App critical path, CC-7 the server one).

**Vision gaps:** [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

**Dependable saving.** Created on 18 November 2026 by moving Plan 18's Phase 0 (the commit contract) here, with the deltas of the save-category design applied, and then cut to its lean form by an independent check the same day. The owner asked whether stability should come before extensibility ("SO DO WE HAVE A STABILITY PROJECT? … SO IT CAN BUILD ON TOP"); the answer was that the two are separable, and stability goes first. The owner then said to record it in astrid-dev and not do it yet: it is queued, in no release brief, and which release carries it is [D9](inputs.md#owner-decisions), open. [Plan 18](../18-timeline-editing/plan.md) (one command layer) starts on this plan's base.

**The end state.** The owner edits a long-lived timeline ("Almost Ready") for a week and meets no stuck state. It is two ideas, one on each side of the wire, with no dependency between them:

- **Idea A, on the App: one home and four outcomes.** An unsettled change has one home (one queue row per timeline), a reply has one of four meanings named by the server, and the screen is a function of the home. The four meanings are one rule for **both kinds of writer**: the editor and any agent send one commit to the one commit route and read the reply the same way ([statements.md](statements.md)); the Agent's own client, which has its own file-backed queue, reads `outcome` too (CC-4b).
- **Idea B, on the Agent and Runtime: a settled head.** An accepted head is a fact. A check judges only what a change introduces, and a commit costs the change, whatever the history.

**The root cause.** Two things, one for each idea.
- *Server:* nothing in the stack treats an accepted head as settled. Every request re-proves the accepted base from scratch against today's code, and when that disagrees the only outcome is a refusal. That produced commits that took 3 minutes, whole-head refusals ([#842](https://github.com/banodoco/astrid-dev/issues/842)), writers that stored what readers later refuse, and states nothing could discharge ([#732](https://github.com/banodoco/astrid-dev/issues/732)).
- *Editor:* nothing gives an unsettled change one home. A change can be in an outbox owner, a session copy, a draft slot and six React flags at once, and a reply can be classed nine ways by status code. Each of the sixteen incidents on one timeline ([inputs.md](inputs.md#planning-evidence)) is a path through that space nobody designed. Release 14 has not built this centre: the draft database, the owners, the six inputs to the bar and the edit-blocking throws are all still in the code.

No test held a document with a history or with size, so each slipped through.

**The five invariants** are the plan's statements (the plain-language form is [statements.md](statements.md)). Each is held by the type, the model test or a named count, nothing more. Invariants 1 to 3 are idea A; 4 and the computation third of 5 are idea B.

1. **One queue is the only home of unsaved work.** One ordered queue of change records per timeline, in IndexedDB: the existing outbox, one row per timeline. A record is `{id, key, basis, label, payload}` and **the payload is opaque to the queue**, so Plan 18's TL-5 only swaps the payload (a document patch for `{op, select, args}`). The document on screen is the accepted head with the queue applied. The badge, the bar and what a reload shows are one pure function of that row. One gesture is one record; a field edit commits when the edit ends.
2. **Every reply to a change is one of four outcomes, for every writer, and the server says which.** `accepted` (adopt the head, drop the record), `moved` (apply the same change to the new head and send it), `refused` (these bytes will never be accepted; invariant 3), `unavailable` (nothing was decided; send the same bytes again, same key). The commit and import routes carry the outcome as a field, **set where each reply is built: by the Runtime for the errors it builds, and by the Agent's `failure()` (where most commit refusals are built) through one mapping table kept beside the reasons**: `conflict` and `stale_head` are `moved`; `head_busy` and a 503 are `unavailable` (**for every client**: today the editor retries it and the Agent files it as a refused pending change); `invalid` and every other `refused` are `refused`. Reasons are for people and never decide behaviour. One decoder, total, in `send(request): Promise<Outcome>`, the only function in the save modules that sees an HTTP status. Against a Runtime that sends no `outcome`, the decoder falls back to the present status table collapsed to four values, private to `send`. 401, 403, 408 and 429 are `unavailable`, so an expired session never takes edits off the timeline.
3. **A refusal parks itself, and nothing ever blocks an edit.** On `refused`, that record and everything queued behind it are parked together as one entry in the same row. The document returns to the head plus what is left. The bar keeps its two buttons for every state: **Try again** (queue the parked entry on the current head) and **Discard**. A record waiting on `unavailable` stays and retries, with the same two buttons. Adding to the queue has no precondition, and any unsaved change can be discarded, in any state, before and after a reload. ([D15](inputs.md#owner-decisions): this lean form is the recommendation; it is still the owner's decision.)
4. **A check is signed by what it reads, and refuses only what the change introduces.** The delta gate, and a guard on a change's inputs signed the same way: a selection by identity and bytes, not the whole head. One writer admits what readers will accept.
5. **An edit costs the change.** Computation: a commit is the change plus one pass over the document, independent of history length, stated as counts at 3 and 30 history entries. A reply is not lost to a socket error (N5), a read does not wait behind a commit's lock (N10), and an import does not wait behind a commit (Release 14 Runtime #62 and #65; this plan's proof re-measures it).

**What is in scope.** CC-1 to CC-7, CC-4b, CC-9, CC-10, CC-11, CC-12 and R0; CC-4 and CC-5 are rewritten and CC-8 is cut. The CC ids from Plan 18's Phase 0 are kept so references stay valid. What is deleted is listed in [inputs.md](inputs.md#what-gets-deleted); nothing is added except the `outcome` field, the parked entry, the one bar's row function and a write-time admission function, the Agent client's reading of `outcome`, one fixture of replies and one paragraph of guidance.

**What stays in Plan 18** (one home per fact): the closed reason list with headlines and its sync script (TL-4 and TL-2), TL-1 to TL-3, TL-5 and TL-5b (the document as the head plus the queue replayed), TL-6 to TL-9, TL-10 (a drop is a named command, **and the durable form of an upload record**), TL-11 to TL-15 and phase 2. TL-1 inherits the refusal rule decided here (park the refused change and its tail) for queued previews.

**What Release 14 already ships, and what this plan adds.** The save fixes already merged on Release 14 carry the behaviour. This plan builds on them (N1 to N12, the `_reference_basis` fix, Runtime #61 to #63 and #65, App #299 to #300, `release/14/save-recovery-2`, and the seed of the model test in `localSaveSession.discard.test.ts`) and does not redo them. N1 to N12 are listed in [inputs.md](inputs.md#what-release-14-already-ships); three are stopgaps with a named replacement here: N8 (CC-5b deletes its throws), N12 (CC-10's retry owns the placeholder) and N6, whose fetch-once behaviour is kept and tested by CC-9. What Release 14 does not give: a guarantee that the category cannot come back. Until this plan lands, a new status or surface can be added without a test failing.

**Release.** None yet: the plan is queued and in no release brief. Which release carries it is [D9](inputs.md#owner-decisions), open; the recommendation is **Release 15** (per the stability sequencing note, because the structure changes what is stored in the browser and what goes over the wire, and Release 14 already carries the behaviour). Nothing here starts, and no branches are cut, until the owner chooses and says go. Plan branches then follow the rule: `release/<NN>/plan-63` in astrid-app, astrid-runtime and astrid-agent, cut from `release/<NN>/main`.

**Deferred or out of scope, and what the lean form gives up:**
- an upload interrupted by a reload or a closed tab is not resumed: the person drops the file again, and the file is still on their disk (the durable record is Plan 18's TL-10);
- an unrelated edit made just behind a refused one is parked with it, and Try again brings it back;
- no structural guard against a new media fetcher, only the GET-count test; one object reader is filed as an issue, not built;
- no ratchet file outside the Agent, and no ratchet on the equality bridge (the old CC-8; Plan 18 may add a two-line scan);
- the closed reason list arrives with Plan 18, so until then reasons are free text shown to people;
- a server reply under one second (the invariants bound work; they do not make whole-document validation cheap, and with invariant 3 the wait no longer blocks or breaks anything);
- **what agents get from Plan 18, not here:** the one command verb for any batch, the generated MCP tool and `timelines ops --json`, the refusal envelope with a stable code and a headline, bundle and checkout publishes as commands (or their retirement), narrow reads for function commits (so an agent's function does not clash with every concurrent edit), one vocabulary for parked work across the CLI and the editor, and the authoring writer (bundle publishes), which has no outbox and keeps nothing if a reply is lost: it is better solved by sending bundles through the one verb than by a third queue, so here it only raises the same four cases (CC-4b);
- merging the editor's and the Agent's queue implementations (they share a contract, not code);
- the editor sending intent for every gesture (Plan 18); a redesign of the timeline UI; anything in Release 14 or Plan 59.

Deferred items with reasons are in [inputs.md](inputs.md#deferred).

## Existing work and decision

We build on what Release 14 lands, on `discardOversized` (which already parks one kind of refusal and becomes the only refusal path), on the existing outbox (it becomes the one row), on the import's stable key and one replay (`recoverMediaImportAfterLostAck`, which becomes the save's backoff loop), and on the Agent's `split_findings` and the uniform baseline rule from #842 (they become the registry's gate). The smallest sound approach is to delete the parallel homes for an unsaved change rather than add a mechanism to reconcile them, and to keep the closed reason list, durable uploads and per-clip dependents out until the command layer gives them a shape. The evidence, the alternatives, the independent check, the challenge and the owner's decision are in [inputs.md](inputs.md#planning-evidence); this draft is not accepted.

## Sequence and readiness

**Two tracks, no dependency between them; this plan goes first, and Plan 18's phase 1 starts on its base.** It starts when the owner chooses the release (D9) and says go, on `release/<NN>/plan-63` cut from that release's main. **The first task is the model test (CC-5a), grown from the seed;** every later case is added as the outcomes (CC-4) and D15 land.

- **App (what the owner feels; ship first):** CC-5a, CC-4, then CC-5b, then CC-10 and CC-9. Critical path CC-4, CC-5b, CC-10, R0 (about 11.5 days). CC-5b waits for D15.
- **Agent and Runtime (what Plan 18's TL-1 waits on):** CC-7, then CC-1 then CC-2, and CC-7 then CC-3 then CC-6; CC-11 after CC-1; CC-4b (the Agent's side of the four outcomes, with the one reply fixture) then CC-12 (the guidance), which also feed the App's CC-4 test.

Plan 18's TL-1 (a design task that writes findings, not product code) waits for CC-3, CC-4 and CC-7; Plan 18's RS1, and with it every task that changes product code, waits for R0, this plan's end-state checks **and** a week of the owner editing "Almost Ready" without a stuck state (the week is evidence for the owner's call, not a gate on the code). The order and day counts are in [tasks.md](tasks.md#critical-path-and-estimates).

## Interfaces and handoff

**Consumes:** `release/<NN>/main` of each product repository at the cut (identified by SHA at CC-1, in [inputs.md](inputs.md#source-identities)), including N1 to N12, the `_reference_basis` fix, Runtime #61 to #63 and #65, App #299 to #300, `release/14/save-recovery-2`, the model-test seed and the Agent's baseline rule from #842.

**Produces,** for Plan 18 and for every later gesture: (1) the counting harness and the scaling test (Agent and Runtime); (2) the rule registry (names carry an owner prefix, `core.<rule>`; `findings(document)` is a pure function of the document, so a pack's rule can run in the Runtime provider process under the same gate) and the generated rules-by-legacy-shapes grid; (3) `outcome` on the commit and import replies (set by the Runtime and by the Agent's `failure()` through one table), the App's one decoder, `send(): Outcome`, the Agent client's reading of it (the `--json` envelope carries `outcome`, so MCP gets it through the bridge), and **one fixture of canned replies with the expected outcome each, kept in the Agent and pinned by the App, which both clients must decode identically**; `sendIntent` in Plan 18 is `send` with a command payload, not a second send function; (4) the one queue row with its opaque payload, the parked entry, and the model test, which speaks only of rows and outcomes, never of `doc.patch` shapes; (5) one write-time admission function for registry and catalog entries; (6) the corpus and its manifest; (7) immutable accepted history; (8) **the guidance paragraph for agents**, in the Agent's timeline skill and linked from the other skills and astrid-dev's. Limits: Runtime schema bumps still need a paired App pin.

## Completion

Done when each of these is true, each guarded by a named test that fails if it stops being true (the full list with test names is in [tasks.md](tasks.md#end-state-checks)):

1. **The model test passes.** A scripted `send` plays every outcome at every queue position, a lost reply, a reload between any two steps, a second tab, a Runtime that sends no `outcome`, and unsaved work already stored in the old shape. After each step: adding an edit never throws; the screen equals the function of the row; every record is accepted, parked, or waiting; Discard leaves a saved state and the next edit saves. It includes a drop while the head moves (I-3).
2. **The counts hold at 3 and at 30 history entries:** identical computation counters; adding one object causes GETs for that object only.
3. **The end-state checks P0-1 to P0-6 are true,** including `outcome` on every error reply of the commit and import routes and the `ENOBUFS` writer test.
4. **As evidence, not a gate:** the commit timing line on "Almost Ready", the import re-measured while a commit runs, and a week of the owner's editing with no stuck state.

Negative cases: a same-size rewrite of a CAS object, a refused commit followed by an unrelated edit, a new rule added without a registry row, a half association written, a refusal then a reload, a lost reply, two tabs, a reply with no `outcome` and an attempted update of an accepted history row. Limits: this proves the save path is bounded and consistent on the corpus and under the model test, not on every document a creator can make or every browser; a server reply under one second is not promised. Integration and publication follow the [run contract](../../skills/shared/run-contract.md); this plan authorizes neither.
