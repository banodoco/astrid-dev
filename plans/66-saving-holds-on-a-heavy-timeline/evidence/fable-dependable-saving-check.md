# Dependable saving: is it minimal, is it elegant, does it fit extensibility?

18 Nov 2026. Read-only: no code, plan or install was changed. I did not write the design under review.

**Read:** `fable-save-category-design.md`, `fable-stability-sequencing.md`, `save-failures-evidence-pack.md`, `sonnet-commit-profile-r14.md`, Plan 18 on astrid-dev `main`, Plan 63 as drafted on `origin/plan/63-dependable-saving` (`e54499c3`), astrid-app `origin/release/14/plan-59` (`816f88da9`) and astrid-runtime `origin/release/14/plan-59` (`e6f4d5c2`).

**Labels.** **Verified** = I read the code or plan text. **Reported** = from one of three Haiku readers, not re-read. **Inferred** = reasoned, not measured. Nothing was built or run.

## Verdict

**Proceed lean.** The centre of the design is right and is close to minimal: one queue row per timeline, four outcomes named by the server, a refusal that parks itself, and a model test that compares the screen with the row. That centre is what stops the owner's incident class, and Release 14 has not built it: the draft database, the owners, the six inputs to the bar and the edit-blocking throws are all still in the code. Around that centre the plan has picked up about nine days of work that prevents no incident in the pack or belongs to Plan 18, and it is about three days short where the real risk sits (the stored-shape change). Build it as two independent tracks at about 30 days, not 37, with the App track's critical path at about 11 days, not 16. Cut CC-10 to an in-memory retry, cut CC-9 to its tests, cut CC-8 and the ratchet machinery, move the closed reason list to Plan 18, and simplify D15 to "park the refused change and everything queued behind it". Add three things the plan lacks: a rule for old Runtimes that send no `outcome`, a rule for unsaved work already stored in browsers, and the three other writers that share the outbox.

## What the code has today

After N1 to N12, on the App branch above:

| What | Today | Source |
|---|---|---|
| IndexedDB homes for unsaved work | 2: `astrid.command-outbox` and `astrid.timeline-drafts` | reported; the draft module and its five importing files verified |
| Outbox rows per timeline | Unbounded: one per owner, a new random owner per session | verified (`commitOutbox.ts:153-157`, `localSaveSession.ts:389-392`) |
| Inputs to the one bar | 6: session state, recovery draft, conflict exhausted, schema incompatible, watchdog, save error | verified (`hooks/saveBar.ts`, `SaveBarSources`) |
| Session statuses | 8 | verified (`localSaveSession.ts:30`) |
| Throws that refuse a new edit for an earlier state | 2 in `append`, kept as a named stopgap | verified |
| Failure kinds | 9, classified by status code, with the `>= 500` prelude copied at 3 call sites | verified (`client.ts:307-348`) |
| What the session does with the 9 kinds | Collapses them to 3: accepted, retry, rejected (with `conflict` as the rebase case) | verified (`localSaveSession.ts:291-294`) |
| Runtime replies on the commit route | 8 statuses and about 20 reason strings; no `outcome` field | reported; the `refused()` helper verified |
| Idempotency | Every mutating client call already carries a key; the commit route requires one | verified in `client.ts`; Runtime side reported |
| Writers that create their own save session | 3: the editor, `placementService.ts:308`, `shotTimelineDataProvider.ts:1341` | verified |

Two readings follow. The four outcomes are not a new idea imposed on the client: the session already behaves as accepted, retry, rejected and rebase, and what is missing is the server saying which. And the structure the plan deletes is real and still present, so the plan is not redoing Release 14.

## 1. Minimal?

### The five invariants

| Invariant | Needed? | Why |
|---|---|---|
| 1. One queue row is the only home | **Yes.** | Classes C and D appear in 9 of 16 incidents each. Two stores, owners and six flags are still in the code |
| 2. Four server-named outcomes | **Yes, and four is right.** | See below |
| 3. A refusal leaves the queue; nothing blocks an edit | **Yes, in a simpler form.** | See D15 below |
| 4. A check is signed by what it reads | **Yes, but it is a different idea** (the server's), and its incidents are mostly already fixed: I-7 by N1, I-11 by Agent #394, I-12's reader side by #393. What remains is the mechanism (CC-3) and the writer side (CC-6) | It prevents the next whole-head refusal, not this week's |
| 5. An edit costs the change | **Partly.** Computation: yes (CC-1, CC-2). Transport and waiting are landed fixes (N5, N6, N10) plus tests. They do not need to be an invariant or carry eight days | See CC-9 and CC-10 |

**Four outcomes versus fewer.** Three failure outcomes map to three different actions: send the same bytes again (`unavailable`), send again on a new head (`moved`), never send these bytes (`refused`). Folding `moved` into `refused` would park every head race. Folding it into `unavailable` would resend stale bytes for ever, which is I-7. Keep four.

### Task by task

| Task | Plan | Call | Lean | Reason |
|---|---|---|---|---|
| CC-5a model test | 2 | **Keep** | 2 | The one enforcement that fails when someone adds a state or a surface. Make it assert on the row and on outcomes only, never on `doc.patch` shapes, so Plan 18 does not rewrite it |
| CC-4 four outcomes | 4 | **Narrow** | 2.5 | Below |
| CC-5b one queue, one bar | 4 | **Keep, simplify D15, add what is missing** | 6 | Below. This is the under-estimated task |
| CC-7 corpus | 3 | Keep | 3 | Everything on the server track stands on it |
| CC-1 counters and ratchets | 3 | **Trim** | 2 | Keep the counters and the scaling test. Drop the ratchet machinery outside the Agent |
| CC-2 close what is red | 4 | Keep, add one item | 4 | Below |
| CC-3 registry and delta gate | 4 | Keep, re-estimate | 5 | Plan 18 said 5 days; Plan 63 added the input guards and says 4. It moves 65 `_fail` sites in the Agent's validator and is the riskiest server change |
| CC-6 writers | 2 | Keep | 2 | I-12's writer is still open (`shot-group-pack-commands.ts:189-190`, reported) |
| CC-8 ratchet on the equality bridge | 1 | **Cut** | 0 | It guards Plan 18's statement (c) for the few weeks before Plan 18 deletes the bridge. If wanted, it is a two-line scan inside Plan 18 |
| CC-9 bounded transport | 4 | **Cut to its tests** | 1 | Below |
| CC-10 uploads as queue records | 4 | **Replace with an in-memory retry; durable form to Plan 18 TL-10** | 1 | Below |
| R0 | 2 | Keep | 2 | |
| **Total** | **37** | | **about 30** | |

Cut or deferred: about 8 days. Moved to Plan 18: about 1.5. Added where the estimate is thin: about 3.

### The items I was asked to look at hard

**The typed boundary.** Keep `send(): Promise<Outcome>`. It is the cheapest strong guard in the plan: once the type has four members, a fifth state cannot be written without changing it. Two parts are wider than the incidents need.
- *"Every mutating route."* The client has about 20 mutating calls (create project, user state, mark viewed and so on). The incidents involve two: the commit and the media import. Put `outcome` on those two. The route table test then covers two routes that are already idempotent. Saves about 1 day.
- *The lint's reach.* "No `ApiError` or `.status` anywhere under `tools/video-editor/`" hits 15 non-test files (verified count), including the page, the placement requester and history. Scope it to the save modules.

**The closed reason list and its sync script.** Under invariant 2, a reason never decides behaviour. So closing the reason list, giving it one wording home in the Agent, generating the Runtime copy and requiring a pin bump for each new reason no longer serve dependable saving. They serve headlines, which is Plan 18's TL-4, and the script is the one TL-2 needs for the schema. On the Runtime the outcome can be set where the errors are built (`refused()`, `reject()`, `HeadBusyError`, `CommitUnavailable` and the generic handler), with one test: every error reply from the two routes carries an `outcome`. Move the list and the script to TL-4 and TL-2. This is a move of about 1.5 days, not a saving, and it puts the code list where TL-1 designs it, so it is designed once.

**The ratchet counts.** A ratchet earns its place for a count that falls over months. Most of the counts here are at zero when the plan ends: the three scans (save state outside the queue module, a throw reachable from adding to the queue, an object fetch outside the reader). A count held at zero is a lint or a test, and needs no `ratchets.json`, no `check_ratchets.py` and no merge-base comparison. Object GETs per gesture is an assertion in one test. That leaves the Agent's `_fail` count (65) as the only real ratchet in this plan. The two others the file was meant to hold (68 `refuse(` sites, 240 uncoded errors) are Plan 18's. Build the ratchet step in the Agent only, or let Plan 18 build it when it has three users.

**"Signed checks" (invariant 4).** Needed as a rule; not needed as part of the same idea. One inconsistency: the design credits it with preventing I-3 (a drop refused because the head moved), and CC-3's text includes "a drop guard signed by the track and shot it lands on". But the drop guard is App code (`useAssetManagement.ts:330`), CC-3's scope is the Agent and the Runtime, and Plan 63 leaves that guard in Plan 18's TL-10. As scoped, Plan 63 does not close I-3. Either say so, or add the one-line guard change to CC-5b.

**CC-9, bounded transport.** The Runtime half has landed (N5, N10, N11). N6 already fetches each media file once. What CC-9 adds is a refactor of three fetchers and four URL builders into one reader, with a scan. That is tidy code; no incident in the pack needs it. The 503s on `/objects/` are themselves unproven (pack, open question 4). Keep two tests: the `ENOBUFS` writer test, and "adding one object causes GETs for that object only". File the single reader as an issue. Saves about 3 days. Gives up: a fourth fetcher written later could bring the bulk download back, and only the GET-count test would catch it.

**CC-10, uploads as queue records.** This is the clearest over-build.
- It stores the dropped `File` in IndexedDB. Video sources are large; this doubles their bytes in browser storage, meets quota limits, and the plan itself opens with "confirm it survives a reload in every browser".
- The cause of I-8 was a cut connection, removed by N5 and N6 and by commits that are 20 times shorter. The residue the plan names is "a cut upload is lost if its one replay fails".
- Plan 18's TL-10 then turns the drop into a command in the same queue. An upload record built before that command exists is a guess at its shape. This is the largest rework risk between the two plans.

Lean form: the import already has a stable key and one replay (`recoverMediaImportAfterLostAck`, verified). Make that replay the same backoff loop the save uses, for as long as the tab is open, with the placeholder clip as the pending state and the same bar. About 1 day. Gives up: an upload interrupted by a reload or a closed tab is not resumed; the person drops the file again, and the file is still on their disk. The durable form goes to TL-10, where the command is defined.

**D15, remove-and-list on refusal.** The direction is right: a refused change must stop blocking. The proposed form is heavier than it needs to be.
- *Dependents "by clip or track id".* Today every queued record is chained to its predecessor (`OutboxBasis {after: id}`) and most are whole-document patches. Working out which later records are independent of a refused one is the job of named commands with selectors, which is Plan 18. Today's `discardOversized` removes the refused change and everything queued behind it. Keep that rule: the refused record and the tail behind it are parked together, as one entry.
- *Restore and Dismiss.* N4 gave the bar two buttons for every state: Try again and Discard. Restore is Try again (queue the parked entry on the current head, which `rebaseOntoLatest` does now), and Dismiss is Discard. Adding a second pair gives one bar two vocabularies and four buttons to test. Keep two.

So D15 becomes a smaller question for the owner: "a refused change, and anything queued behind it, comes off the timeline and waits in the bar with Try again and Discard; meanwhile you can keep editing." Gives up: an unrelated edit made in the second or two behind a refused one is parked with it, and one press brings it back. Saves about 1 day inside CC-5b and removes a mechanism Plan 18 would replace.

**The 37 days.** The sequencing note says it is task arithmetic on Plan 18's figures, not a bottom-up estimate, and it shows. The periphery is over-scoped by about 9 days. The core is light: CC-5b has 4 days for a new stored shape, the deletion of the draft database, owners, seven throws, six flags and five surfaces, and a new refusal path. It omits migration and three other writers (below). I would give it 6. CC-3 lost a day while gaining scope. And CC-2 carries its own note that 4 days is not enough if Release 14's cost branches did not all land; CC-1 must settle that first.

### What is missing

1. **A Runtime that sends no `outcome`.** The decoder's rule is "any reply it cannot read is `refused`". Astrid's hosted editor talks to local Runtimes of whatever version the person has installed (inferred from the hosted Runtime path). Against a Runtime older than this plan, every `head_busy` and `runtime_unavailable` reply would decode as `refused` and park the person's work. The decoder needs a stated fallback for a reply with no `outcome`: the present status table, collapsed to four values, private to `send`. So the nine-kind classifier is folded in, not deleted, until old Runtimes are no longer supported. Also name 401, 403, 408 and 429 as `unavailable` on the server; by the default they would be `refused`, and an expired session should not take edits off the timeline.
2. **Unsaved work already in browsers.** One row per timeline changes the stored shape. Testers and the owner hold owners with retained work and draft slots today. The sequencing note rates this change "High" risk; no task says what happens to that data on first open. The smallest rule: each old owner with work becomes one parked entry in the new row, oldest first, and a draft is dropped when the outbox holds the same work. The model test needs that case.
3. **The other users of the outbox and the draft database.** CC-5b names four editor files. Also in the code: `placementService.ts` and `shotTimelineDataProvider.ts` each create their own save session, the latter also reads and writes the draft database (reported), `bootstrapInitialization.ts` creates timelines through the outbox, and the outbox record carries placement continuations and their capture state (verified, `commitOutbox.ts:420-476`). "One row per timeline, nothing else" must say where each of those lives, or the draft database cannot be deleted.
4. **The two-tab rule, written down.** "Two tabs read the same row, and one of them sends" is the whole specification. Before CC-5b: which tab sends, what the other tab shows while the first has queued edits, and what happens when the sender closes. The lean answer: appends are IndexedDB transactions on the one row, the Web Lock decides only who sends, and each tab redraws when the row or the head changes. Live mirroring of the other tab's unsent edits is not required.
5. **An import waits behind a commit.** The profile measured a media import waiting 5.0 to 6.7 s on `store._mutex` behind a commit, and a commit taking 22 to 26 s when an import overlaps it. CC-9 quotes that figure but only takes object and health *reads* off the lock. The profile's second fix (hold the mutex less in the ancestry walk) is not named in any task. Add it to CC-2's split.
6. **The `_reference_basis` fix as a precondition.** It is 67% of the 9 s commit. Plan 63 lists it as landed; the task list still says "if it has not landed". CC-1's first step should record which.

## 2. Elegant?

**It is two ideas and a tidy-up, presented as five invariants.** Plan 63's own root cause says so: "two things, one on each side of the wire".

- **Idea A, the editor's.** An unsettled change has one home, a reply has one of four meanings, and the screen is a function of the home. Invariants 1, 2 and 3 are this one idea, and it is a good one: a person or an agent changing the save path next has one record to read and one type to satisfy.
- **Idea B, the server's.** An accepted head is settled, so a check judges only what a change introduces and a commit costs the change. Invariant 4 and the computation third of invariant 5. This is Plan 18's original Phase 0, and it is also sound.
- **The tidy-up.** Transport and waiting. Invariant 5 joins three unrelated things (validation cost, repeated downloads, a socket error) under one slogan. They share a sentence, not a mechanism.

For the people and agents who change this code next:
- **Good.** The deletions are the design. After CC-5b a newcomer reads one row shape, one decoder and one function from row to screen, where today there are about 2,900 lines across the session, the outbox, the draft store and two hooks. The model test is a specification that runs.
- **Good.** `send` as the only reader of a status is a rule an agent can follow without reading history.
- **Stacked.** The enforcement has four layers for one property: a type, a lint, a model test and ratchet counts. The type and the model test carry it. The lint is cheap. The ratchets are the layer to drop.
- **Stacked.** The plan's text carries the history of its own edits: statements (a) to (g) beside invariants 1 to 5 beside checks P0-1 to P0-7, with CC ids kept from another plan. Three numberings for one contract is a cost to every reader. Once the scope settles, keep the invariants and the checks and drop the lettered statements.
- **Awkward.** A bar with Try again and Discard for one state and Restore and Dismiss for another.

Stated as "Idea A on the App, Idea B on the Agent and Runtime, two tracks with no dependency between them", the end state is clean and is what the task graph already shows.

## 3. Fit with extensibility

**It fits. The dependency runs one way, and nothing in Idea A or B is thrown away by Phases 1 and 2.** There are four places to watch.

| Touch point | Fit | What to do |
|---|---|---|
| **TL-1** waits for CC-3, CC-4, CC-7 | Good; unchanged by any cut above | If the reason list moves, TL-4 creates it and TL-2 creates the sync script. Plan 18 on the branch still says "`retryable` derived from `status`" in TL-1 item 9 and "each list entry declares its own `retryable`" in TL-13a and `plan.md`: stale against the four outcomes, fix before it merges |
| **TL-5** (document = head plus queue; `sendIntent`) | Good, if the row is shaped for it now | Make the queue record's payload opaque to the queue: `{id, key, basis, label, payload}`. TL-5 then changes the payload from a document patch to `{op, select, args}` and touches nothing else. Say that `sendIntent` is `send` with a command payload, so there are not two send functions |
| **TL-1 item 4 and D15** | **They overlap.** TL-1 is to decide what a refusal does to queued previews ("replays or drops"); D15 decides the same thing for queued saves | Decide once, here, in the simple form (park the refused change and its tail). TL-1 inherits it. The per-clip dependents rule, if ever wanted, arrives with commands that have selectors |
| **TL-10's command half and CC-10** | **This is where they would fight.** An upload record in the queue is built before the drop command that consumes it | Defer the durable upload record to TL-10 (the cut above). The in-memory retry is not rework: it sits inside the import call |
| **CC-3's `register_rule`** | Good. Built-ins only now, packs through the same function later, under the same gate | Two cheap decisions now, because rule names end up in finding keys and in the generated grid: reserve an owner prefix in the name (`core.<rule>`), and require `findings(document)` to be a pure function of the document, so a pack's rule can run in the Runtime's provider process |
| **The command layer and Phase 2** | No conflict. `outcome` rides on the commit reply, whatever the command | Because it is in the Runtime's reply, the CLI and MCP get it too. TL-13a's envelope should say so |

**Waste, all small:**
- the one display copy the row keeps until TL-5 (unavoidable);
- the rebase of whole-document patch chains, deleted at TL-12;
- CC-8, replaced at TL-12 (cut above);
- the per-clip dependents and the upload record, if built as planned (cut above).

**What Phase 1 would redo if stability were built as written:** the upload record (TL-10), the refusal rule (TL-1 item 4), and any model-test case that asserts on patch shapes. All three are avoided by the lean version.

**What extensibility needs that is cheap to shape now:** the opaque record payload, the rule name prefix and purity, one refusal rule, and a model test that speaks only of rows and outcomes.

## The lean version

Two tracks, no dependency between them.

| Track | Tasks | Days |
|---|---|---|
| **App: one home, four outcomes** | Model test 2; `outcome` on commit and import, one decoder with the old-Runtime fallback 2.5; one row, no drafts, no blocking throws, park-on-refusal, migration, the three other writers, the two-tab rule 6; upload retry 1; two transport tests 1 | about 12.5 |
| **Agent and Runtime: a settled head** | Corpus 3; counters and scaling test 2; close what is red, with the mutex hold 4; registry and delta gate 5; writers 2 | about 16 |
| Review | R0 | 2 |
| **Total** | | **about 30** (critical path about 11 on the App) |

**What it gives up:**
- an upload interrupted by a reload is dropped again by hand, until TL-10;
- an unrelated edit queued just behind a refused one is parked with it;
- no structural guard against a new media fetcher, only a GET-count test;
- no ratchet file outside the Agent;
- the closed reason list arrives with Plan 18, so until then reasons are free text shown to people (they already cannot decide behaviour).

**What it keeps:** every invariant in the form the owner can observe, the model test, the typed boundary, and all of Idea B.

**Order.** The App track is what the owner feels and can ship first. The server track is what Plan 18's TL-1 waits on. D15, in its smaller form, is still the one decision on the critical path.

## Not checked

- Nothing was built or run. The lean day counts are my judgment on the plan's own figures, no more bottom-up than the 37.
- Whether old Runtimes really meet a new hosted editor in practice; if pins always pair them, the fallback in item 1 shrinks to a test.
- The Runtime's moved-head path for a non-restore commit: one Haiku reader suspected `StaleHead` could surface as a 503. I read the raise and re-raise sites but not the Agent provider that handles it. Unverified.
- Line numbers from the Haiku readers differ by a few lines from the design's; I did not reconcile them.
- Whether `shotTimelineDataProvider.ts` and `placementService.ts` are reachable in the shipped editor.
