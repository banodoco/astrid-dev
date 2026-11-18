# Four questions about timeline saving: fast edits, an agent on a human, fast saving, and the split

18 Nov 2026. Read-only: no code, plan or install was changed, and nothing was built or run.

**Read:** `fable-quick-edits.md`, `fable-agent-edits.md`, `fable-save-category-design.md` (section 2), `fable-stability-sequencing.md`, `fable-dependable-saving-check.md` and `sonnet-commit-profile-r14.md` in full; the headings of `save-failures-evidence-pack.md`; Plan 63 (`plan.md`, `statements.md`, the task list) and Plan 18 (`plan.md`, the task list) at `fe8e09dd`; and code at astrid-app `2ce3c44fa`, astrid-agent `46db5ef3d` and astrid-runtime `e6f4d5c` (all `origin/release/14/plan-59`). Four Haiku readers traced the edit path, the merge, the commit's costs and the Agent's handling of a moved head; I re-read the lines the answer rests on.

**Labels.** **Verified** = I read the code or text. **Reported** = from a Haiku reader, not re-read by me. **Measured** = a number in `sonnet-commit-profile-r14.md`. **Inferred** = reasoned, not observed.

## The four answers in brief

1. **Fast edits.** Yes: *the screen is the person's document; one save is in flight and everything edited meanwhile goes as the next commit; the server's document reaches the screen only when nothing is outstanding.* The first half is Plan 63's rule and a ten-line Release 14 fix. The second half (the batch) is new, about 3 days, and is what makes it hold at any rate.
2. **An agent on a person.** The server already merges by address, down to a field. It fails today because most agent edits, and some editor edits, claim the whole timeline, so unrelated changes clash. One rule for every writer: *send what you changed, the head you read, a key, and what you relied on.* The new must-haves are about 11.5 days and need no command layer.
3. **Really fast.** A commit was measured at 9 s; the fix for 67% of it has landed and is unmeasured (about 3 s, inferred). Under a second is about 11 days of removing repeated whole-document work. 200 ms needs validation that follows the change, about 9 more days, and should be decided on measurement.
4. **The split.** Four projects, cut slightly differently: **A** Dependable saving (which includes the person's own quick edits; they cannot be separated), **B** Fast saving (parallel, fully separable), **C** Editing together (small, on A), **D** Extensible editing (Plan 18, after A). Robustness does not need the intent model: the server replays changes, and the editor never does until Plan 18.

## 1. Fast edits

### The property

A scripted test, at two levels (the model test with a scripted `send`, and one run on the staging stack):

> **For N from 1 to 20 edits a second, for 30 seconds, mixed (drag, nudge, drop, trim, field), with each save taking anything from 0 to 10 s and accepts, a lost reply and one foreign commit landing at any point in the burst:**
> 1. **None refused or undone.** Adding an edit never throws and never declines.
> 2. **No jumps.** After every step the screen equals the person's own edits applied in order. It changes for only two reasons: the person edited, or the queue was empty and the head had moved.
> 3. **All saved, in order.** When the burst ends and the queue drains, the Runtime's head equals the starting head plus the N edits in order (plus any foreign change), and equals the screen.
> 4. **Bounded.** At most one save is in flight and one is waiting, whatever N is. The number of commits sent is at most (burst length ÷ save time) + 2, not N.
> 5. **Soon.** The last edit is accepted within two save times of the gesture ending.

Lines 1 to 3 are the failures the owner sees today. Lines 4 and 5 are what makes it hold at *any* rate; without them a fast enough person outruns the saves and the queue grows without limit (at 5 edits a second and 3 s a commit, 30 seconds of editing takes 7.5 minutes to drain).

### The one model

> **The screen is the person's document. One save is in flight; everything edited meanwhile waits as one batch and goes as the next commit, each edit still its own step. An accept moves only the base. The server's document reaches the screen only when nothing is in flight or waiting.**

It has two halves, and they differ in cost.

**Half 1: the screen keeps the person's edits (Plan 63, invariant 1; `fable-quick-edits.md`).** Verified in code at `2ce3c44fa`: at every accept, `pump` installs the server's document and sets `replaying` when records are still queued (`localSaveSession.ts:247-257`); `append` then throws `LocalSaveDeclined` (`:415`), and before that the handoff's `checkHead` and same-document check refuse. Removing the install-at-each-accept removes all three. Plan 63 already states the rule; the Release 14 version is about ten lines.

**Half 2: one in flight, one waiting (new; not in Plan 63).** Today each edit is its own commit, sent one at a time (verified: `pump` sends `record.intents[0]`, one request per record). Half 1 alone makes ten quick edits ten background saves, which is correct but not bounded. The batch needs no new wire format:
- a commit request already carries a list of `commands` and a list of `steps`, each step naming its own command ordinals (verified: `localSaveSession.ts:262-275`; Agent `_commit_patch.py:54-63`, `:371-377`, where a later step reads an earlier step's output);
- undo is per step, not per commit (verified that `_step_undo.py` and `undo_steps` exist; **not verified** that a batch of the editor's chained `doc.patch` records undoes one step at a time, which is the half-day spike that decides this).

So a batch of k waiting edits is one commit with k steps. Nothing is merged or lost, one undo step per gesture is kept, and no timer or coalescing rule is needed: the batch is simply "whatever arrived while the last save was out". At a slow edit rate every batch has one edit and the behaviour is today's.

### What it deletes

| Deleted | Where | Why it can go |
|---|---|---|
| Installing the server's document at each accept; `replaying`; the "Wait for retained dependent saves" refusal | `localSaveSession.ts:247-257`, `:415` | half 1 |
| `checkHead` and the same-document check when capturing an edit; "original verified authoring head is unavailable" | `timelineLocalSaveHandoff.ts:254-270`, `:483-494` | half 1: nothing compares a new edit with the head |
| `before` in each record, and the `same(save.before, document)` throw | `localSaveSession.ts:25-34`, `:420` | the queue's order is the chain |
| The 500 ms save debounce and the watchdog's dependence on it | `useTimelinePersistence.ts:47`, `:76-77`, `:1292` | half 2: send at once when idle, batch when not |
| The same-field coalescing rule proposed in `fable-quick-edits.md` | (Plan 63, CC-5b) | half 2 bounds the queue without it; do not build it |
| The per-edit whole-document recovery snapshot | `useTimelinePersistence.ts:1123-1132` (`writeRecoverySnapshot`) | already deleted by Plan 63 (the draft database) |

### The cost

| Piece | Size | Where |
|---|---|---|
| Half 1 on Release 14: install the server's document only when the queue is empty | 1 to 1.5 days, about ten lines plus tests | now, as `fable-quick-edits.md` section 3 |
| Half 1 in full (the handoff's checks, `before`, the reload path) | already in Plan 63 CC-5b (7 days) | Plan 63 |
| Half 2: the spike (do k chained steps commit and undo one by one?) | 0.5 day | Plan 63, before CC-5b |
| Half 2: build the batch at send time; the burst cases in the model test | about 2 days | Plan 63 CC-5b and CC-5a |
| A refused batch: resend its steps one at a time, once, so only the bad edit and what follows it are parked | 0.5 day | Plan 63 CC-5b |
| The exact form (the screen is the accepted head plus the queue replayed, so a foreign change shows mid-burst) | Plan 18 TL-5 | not needed for the property |

**What it does not cost:** the command layer. The property above holds with document patches. Half 2 also makes the exact form matter less: with at most two saves outstanding, "when the queue is empty" is at most two save times after the person pauses.

**One trade.** A batch is validated as one commit, so one bad edit refuses the whole batch on the first try. The single retry step by step (row 5) brings that back to today's blast radius.

## 2. An agent on top of a human

### What the machinery is today

- **One route, and the merge is by address.** Every writer posts to the one commit route with the head it read. If the head has moved, the Agent's provider (running inside the Runtime) replays the request on the new head, up to three times, and then answers `head_busy` (verified, Agent `commit.py:1427-1557`; one Haiku reader reported that a moved head becomes a 500, which is wrong: the provider catches `StaleHead` at `:1552`).
- **A clash is an overlap of addresses.** Each writer's guards are (thing, path) pairs; each intervening commit's writes are (thing, path) sites. They clash when the thing is the same and one path is a prefix of the other, or when either side names the whole timeline (verified, `_commit_patch.py:976-999`). So field-level merge already exists on the server. A Runtime test pins the simple case: two moves of different clips merge, two moves of one clip clash (reported, `test_timeline_commit_integration.py:475`).
- **But many writers name the whole timeline.** A `doc.patch` with no declared reads is forced to `atomic` (reported, Runtime `timeline_commit_store.py:86-103`; the editor's own default agrees, verified `localSaveSession.ts:269`). The editor declares reads only for split, trim, move, transition clear, a media drop, an element edit and a track label, and an element edit is sent `atomic` anyway (verified, `timelineLocalSaveHandoff.ts:565`, `:957`). An agent's function commit is `atomic` over the whole timeline unless it declares reads (verified earlier, `commit_session.py:771-778`), and a document publish (`timelines commit --file`, the MCP publish tool) is `atomic` (reported, `timeline_document.py:327`).
- **The editor hears of someone else's commit two ways.** In the reply to its own next save, or from a poll of the timeline every 30 seconds that is skipped while anything is unsaved or a gesture is active (verified, `useTimelineQueries.ts:8`; gating reported, `usePollSync.ts`). There is no push. Adopting the document clears the undo and redo stacks (verified, `useTimelineHistory.ts:308-322`) and shows no notice (reported).
- **"Try again" cannot win a real clash.** It resends the same change on the latest head; if the clash is real it is refused again (verified, the comment and code at `localSaveSession.ts:199-206`). So today the only way out of a real clash is Discard.

### The five cases

| Case | Today | Should |
|---|---|---|
| **(a) Different clips** | **Lands, if both writers declared what they read.** A drag, trim, split or drop beside an agent's fixed list merges. It does **not** merge when either side is `atomic`: an element or parameter edit in the editor, any agent function, any document publish. Then the second writer gets a clash although nothing overlapped: the person gets the bar and (until Plan 63 CC-5b) cannot edit; the agent's function is run again up to three times. The person sees the agent's work at their next accept or up to 30 s later, with their undo history cleared and no notice | **Always lands, both ways, silently.** Narrow reads are the default for every writer; the whole timeline is something a writer asks for. The change appears within about a second of the person pausing, in place, with one quiet line saying who and what |
| **(b) The same clip or field** | The second writer gets a clash. **Person second:** the screen is reset to the head, the bar shows, the whole queue is held, and Try again cannot succeed. **Agent second:** a function is run again on the new head (so it decides again knowing the person's value); a list is saved as a pending change with "you both changed: …" | **The second writer gets `moved`, and nobody is blocked.** The person's change is parked with the clip named ("The agent changed this clip first"); the screen shows the agent's value; they keep editing and can redo it in one gesture. The agent's function runs again; a list is parked. Nobody overwrites silently. A "keep mine" button is a nice-to-have |
| **(c) A big agent bundle while the person has queued edits** | The bundle's base is the head pinned when the agent checked out, possibly minutes earlier (reported, `authoring_commit.py:24-38`). Every edit the person saved since must be replayed over, one history entry at a time, each loading two whole documents (verified, `_commit_patch.py:885-887`). If the bundle is `atomic` or touches anything the person touched, it is refused once; the writer keeps no copy of the request (reported, `authoring_bundle.py:1923`), so the agent must build and send again. Meanwhile each of the person's quick saves is another head change for the bundle to lose to: a commit takes about 9 s (measured), so three attempts can all lose, giving `head_busy`, which the Agent files as "refused" (verified earlier). If the bundle lands first, each of the person's queued edits is replayed by the server, and the first that overlaps parks the chain | **The bundle is an addition with narrow reads:** it relies only on what it attaches to, so it lands under any amount of unrelated editing. If it is `moved`, the agent re-reads and re-attaches without generating anything again, and it keeps its request and key until it has an answer. The person's batch (at most one waiting) is replayed once. The person sees "Agent added 12 animations" when they pause. Fast commits and batching (sections 1 and 3) are what stop the agent losing three times |
| **(d) The person deletes what the agent edits** | **Delete first, agent second:** the agent's change no longer finds its clip and clashes; a function runs again and sees the clip gone, a list is parked. This is right already, apart from the words. **Agent first, delete second:** the delete's guards cover the clip, the agent's write is under it, so the person gets the bar for a delete (inferred from the prefix rule; not run) | **Delete first:** `moved`; the agent reports "that clip was deleted in the editor; skipped". **Delete second: the delete lands.** Deleting needs no agreement about what the thing looked like. With document patches that is a special case; with a `clip.delete` command chosen by identity it is free, so this half waits for Plan 18 and until then is a parked change |
| **(e) The person is offline** (the tab cannot reach the Runtime: it stopped, the laptop slept, or the hosted path dropped) | Edits are kept in IndexedDB and retried with the same key, from 1 s up to every 30 s (reported). The agent, which talks to the Runtime directly, keeps committing. On return the queue is sent one edit at a time; the server replays the first over everything the agent did. Disjoint edits land. At the first clash the screen is reset to the head, so the offline work leaves the screen, and the rest of the queue waits behind the bar | **The same rule, no special mode.** The offline queue is sent as one batch. Steps that merge land; a clashing step and what follows it are parked and listed by name; the screen keeps the person's edits until the queue is empty, then takes the head. Long absences are bounded by section 3 (replay cost should follow the difference, not the number of commits missed) |

### The one rule for every writer

> **Read the head, change your own copy, and send what you changed with the head you read, a key you keep, and what you relied on.** The Runtime lands it if nothing you relied on has changed, wherever the head is by then. If something has, the answer is `moved`: a person's change is parked and shown, an agent reads again and runs again (at most three times). Nobody waits for anybody, nobody's screen is taken from them, and nobody overwrites without being asked.

This is Plan 63's statement with five words added: **"and what you relied on"**. Narrow by default, the whole timeline on request. Without that clause, case (a) fails for most agent edits, and case (a) is the common one.

### What the person sees when an agent's change lands

- **During a gesture, or while their own saves are out: nothing.** The screen is theirs (section 1).
- **Within about a second of pausing:** the change appears in place. Selection, playhead, scroll and undo history are kept. One quiet line for a few seconds: "Agent · Added 12 animations". No bar.
- **Only if their own change clashed:** the one bar, naming the clip and the other writer.

### Must-haves and nice-to-haves

| | What | Size | Home |
|---|---|---|---|
| **Must** | A clash parks the change and never blocks editing | in Plan 63 (CC-5b) | Plan 63 |
| **Must** | Four outcomes for both writers; `head_busy` means "send again" to the Agent too | in Plan 63 (CC-4, CC-4b) | Plan 63 |
| **Must** | **Narrow reads by default.** Editor: every record declares the addresses its patch writes; `atomic` only where a gesture truly needs it. Agent: a function commit's default reads are the things its commands touch; `reads="timeline"` is opt-in; a document publish declares its diff | 3 days | new |
| **Must** | **The editor notices a foreign head in seconds, not 30.** A head-only check every 2 s while idle (the history read is 0.07 to 0.2 s, measured) | 1 day | new |
| **Must** | **Adopting keeps the person's place:** undo and redo survive (undo by inverse of their own steps already exists on the server, reported `test_real_inverse_preserves_newer_disjoint_work…`), selection and playhead kept | 2 days, unverified | new |
| **Must** | **Who and what:** the quiet line, from the commit's `label`, `source.via` and publisher (all already stored, reported `sync.py:1036-1046`) | 1.5 days | new |
| **Must** | **A bundle publish survives `moved`:** keeps its request and key, re-attaches without generating again | 2 days | new (Plan 63's CC-4b only makes it raise the four cases) |
| **Must** | **A test with both writers on a real stack:** a burst in the editor, an agent function and a bundle on one timeline; cases (a) to (e) as rows | 2 days | new (Plan 63 has the model-test rows) |
| Nice | Push in place of the 2 s check (a head event) | 3 days | later |
| Nice | The agent's change visible in the middle of a burst | Plan 18 TL-5 | Plan 18 |
| Nice | A table test of finer merges (two fields of one clip, an add beside a reorder), and narrowing patch paths where it fails | 1 day, plus what it finds | later |
| Nice | "Keep mine" on a real clash (resend with guards taken from the new head, for the touched fields only) | 2 days | later |
| Nice | Delete beats edit | free with commands | Plan 18 |
| Nice | Undo the agent's change from the line; highlight what changed; "an agent is working here" | 2 + 3 + 2 days | later |

**The musts that are new come to about 11.5 days.** None needs the command layer.

## 3. Really fast saving

### The target, and what it is for

There are three different moments, and only one of them should ever be felt.

| Moment | Target | Scales with |
|---|---|---|
| **On screen** | The same frame as the gesture ends. Never waits for anything | nothing (section 1) |
| **Kept** (on disk in the browser; survives a reload or a crash) | Within 50 ms of the gesture ending | the change |
| **Accepted** (the Runtime's head includes it) | **Stage 1: under 1 s. Stage 2: 200 ms at the median and 500 ms at the 95th percentile**, for a one-clip edit on "Almost Ready", the same at 3 and at 300 history entries and while an import runs | the change |

With section 1 in place the person never waits for an accept, so a slow accept no longer costs them an edit. What a fast accept still buys: how soon work is safe outside the browser, how long an agent's change waits to appear (two save times), and how often two writers lose a race and validate again. **Under a second buys nearly all of that.** 200 ms is worth having only if it comes from the principled change below, not from tuning.

### What is measured and what is not

- **Measured** (`sonnet-commit-profile-r14.md`; Agent `458d9d51`, Runtime `d725811`; the CLI, not the editor; a loaded machine): a commit takes 8.6 to 9.3 s inside the Runtime, the same at about 8 and about 28 history entries; 67% of it is the legacy-declaration pass; an import waited 5.0 to 6.7 s behind a commit; a commit that overlaps an import took 22 to 26 s; SQLite's 2,190 statements took 0.06 to 0.08 s in total.
- **Landed since, not measured:** the legacy pass now builds its bases once (Agent #400, `6b8780669`, on the branch at `46db5ef3d`; verified in the log). Runtime #62 ("keep verified history across unrelated writes so an import never forces a re-walk") and #63 ("one reply writer, health off the mutex, commit timing at INFO") are on the branch at `e6f4d5c` (verified in the log; their effect is not measured).
- **Inferred:** "about 3 s now" is 33% of 9 s. The stage estimates below scale profiled seconds by 9 ÷ 28.8, which is rough, because a profiler slows call-heavy code more than the rest.
- **Never measured by anyone:** the time from a gesture ending in the editor to the accept; the browser's write per edit; the size of the document and of the reply.

### Step by step: what each costs today, and what makes it cost the change

| Step | Scales with today | What makes it cost the change | State | Size |
|---|---|---|---|---|
| **Wait before sending** | A fixed 500 ms, plus every earlier edit's commit, one at a time (verified, `useTimelinePersistence.ts:47`) | Send at once when idle; one batch waiting (section 1) | project A | in A |
| **The browser's record** | About three whole documents per edit: `before`, `after` and a display basis, plus a whole-document recovery snapshot in a second database (reported; `localSaveSession.ts:25-36` verified) | The record is the patch. One display copy per timeline, not per edit. That copy is the last document-sized write per edit until Plan 18's TL-5 removes it; measure it before doing more | Plan 63 CC-5b | in A |
| **The request** | The change: one `doc.patch` and the base ids (verified, `localSaveSession.ts:262-290`) | already so | done | 0 |
| **The legacy timing pass** | The document times the number of declarations: 400 deep-copying calls, 67% (measured) | Built once per bundle. The pass itself still runs on every commit (reported) | **landed** (#400), unmeasured | re-measure |
| **Timing compile and evaluate** | The whole document, once per commit: 15% of the old profile, perhaps 1.3 s (inferred) | Stage 1: find why 204 rule evaluations cost this much (`lookup.py:332`, not read). Stage 2: **validate what the change touches.** An accepted head is a fact, so its results are kept by revision; a rule declares what it reads; only rules whose inputs the change touched run again | new; builds on CC-3 (rules signed by what they read) and CC-11 (accepted history cannot change) | stage 2, 6 days |
| **Serialising and hashing** | The document, many times: 9,585 `json.dumps` calls (9%) and 1,797 digests (measured) | Once per commit; an unchanged child keeps its digest | Plan 63 CC-2 | in B |
| **The history check** | The history: the ancestry walk under `_check_reservations` (6% at 8 entries, measured; suspected to grow as the square on long histories, not constructed) | Accepted history is immutable, so the head is trusted and nothing is walked | partly landed (#62); CC-2, CC-11 | in B |
| **Replay over a moved head** | The number of commits since the writer's base, two whole-document loads each (verified, `_commit_patch.py:885-887`; not measured) | Replay against the net difference between the base and the head | new | stage 2, 2 days |
| **Losing the race at accept** | The whole validation again, up to three times (verified, `commit.py:1427`, `:1552`) | Stage 1 makes it rare. Then **one commit at a time per timeline**, in arrival order: the three attempts and `head_busy` are deleted | new, only after stage 1 | stage 2, 1.5 days |
| **The store's writes** | The document (a new revision row holds the whole payload, and the receipt holds the canonical document; reported) | Leave it. All of SQLite is under 0.1 s (measured) | — | 0 |
| **Steps that follow the history or the number of commits** (all reported, none measured): a count of all the timeline's events on every publish (Runtime `timeline_commit_store.py:2275`); a cold head read that hashes every timeline event (`:1174-1206`); receipts that keep each commit's whole result for 24 hours; a reference projection whose table is never pruned (`reference_projection.py:140-175`); a legacy-media check that walks the whole head on every commit (`service.py:3061-3080`) | history, or document times commits | Each becomes a counter in CC-1's test at 300 entries; fix only the ones that go red | new counters | inside CC-1 and CC-2 |
| **The reply** | The document: every reply carries the canonical document (verified, `localSaveSession.ts:297`) | The reply is ids and a digest. The editor fetches the document only when it is about to show it: the queue is empty and the head is not the one it expects | new | stage 1, 1.5 days |
| **Waiting on a lock** | An import waited the length of the commit's history walk (measured, 5 to 7 s) | Reads and imports do not take the commit's lock | landed (#62, #63), unmeasured | CC-9, 1 day |
| **The editor on receipt** | The document: it rebuilds and installs the whole display at every accept (verified, `localSaveSession.ts:247-257`) | Only when the queue is empty (section 1) | Release 14 fix, then A | in A |

### What has landed, and what remains

**Landed on Release 14:** the two earlier cost fixes (187 s to 9 s, measured); the legacy basis fix (9 s to about 3 s, inferred); imports and health reads off the commit's path (unmeasured); a commit timing line in the Runtime's log.

**Stage 1, under a second (about 11 days; project B):**

| Task | Size |
|---|---|
| Measure from the editor: a mark at the gesture's end and at the accept, next to the Runtime's timing line. **First, because every number above is from the CLI** | 1 day |
| CC-1: counters and the scaling test, at 3, 30 and now 300 history entries | 2 days |
| CC-2: close what is red: repeated serialising and digests, the history walk, the lock hold, and the evaluate cost | 4 days |
| CC-11: accepted history is immutable | 1.5 days |
| CC-9: the two transport tests; the import re-measured while a commit runs | 1 day |
| The reply without the document | 1.5 days |

Arithmetic, not a promise: removing the repeats leaves compile, evaluate and one pass of the rest, about 1.5 to 2 s on the old profile's shares. Under a second needs the evaluate cost to fall too, and that is unread code. **If stage 1 measures above a second, that is the finding that starts stage 2.**

**Stage 2, 200 ms (about 9 days; started only on stage 1's numbers):** validate what the change touches (6); replay against the net difference (2); one commit at a time per timeline (1.5).

**Not on the list:** a faster language, a second process, an "accept now, validate later" reply (a refusal must stay an answer to the request), or shrinking what SQLite stores.

## 4. The split

### Separable or tied?

**Four projects is right, but not cut quite where the owner drew the lines.** "Multi-edit robustness" is two different things, and they belong in different places.

| The owner's four | Verdict |
|---|---|
| **Stability and elegance of the raw approach** | A project. It is Plan 63's editor half plus the four outcomes and the rule gate |
| **Multi-edit robustness, the person's own quick edits** | **Tied to the one above. Not a project.** The rule that makes any edit rate safe ("the screen is the person's document; an accept moves only the base") *is* the raw approach's first invariant. Building one without the other means building the queue twice |
| **Multi-edit robustness, an agent beside a person** | A project, small, on top of the first. Its must-haves need no command layer |
| **Speed** | A project, and the most separable of all: other repositories, other people, and a different kind of proof (numbers against a budget, not a model test) |
| **Extensibility** | A project, after the first. Nothing in the other three needs it |

### The dependency graph

```
Release 14, now:  install the server's document only when the queue is empty   (1 to 1.5 days)

   A. Dependable saving ───────────────►  C. Editing together  ─ ─ ─►  exact forms arrive with D
        │   (the queue, four outcomes,          (narrow reads, notice,
        │    batch, rule gate)                   bundle survives `moved`)
        │                                              ▲
        │                                              ┆ helps: an agent stops losing three times
        ▼                                              ┆
   D. Extensible editing              B. Fast saving ──┘   (parallel with A from day one;
        (Plan 18, unchanged)                                shares only the test corpus)
```

Solid arrows are "cannot start product code before". Dotted are "is better with".

- **A needs nothing.**
- **B needs nothing from A.** They share one task, the corpus of long-lived documents (CC-7), which goes first and both use. B makes line 5 of the fast-edit property ("soon") tight and stops agents starving in C, but neither A nor C is blocked on it.
- **C needs A's** four outcomes and the parked change (CC-4, CC-4b, CC-5b). Its server half (narrow reads) can start at once.
- **D needs A's** review round and end-state checks, as Plan 18 already says. It needs nothing from B or C.

### The honest tie: does robustness need the intent model?

**Only for exactness, and it can be cut cleanly.** Robustness needs one ability: take a change made on one head and apply it to another. There are two places that can live.

- **On the server, by address.** This exists. `rebase_patch` replays a document patch over the commits that landed since, and refuses only where addresses overlap (verified, section 2). It needs every writer to declare what it relied on, which is project C's one real change.
- **In the editor, by meaning.** This does not exist: the editor cannot apply a queued edit to a different document, because the code that knows what an edit means is in the Agent (verified, the comment at `localSaveSession.ts:248-249`). That is what Plan 18's command layer builds (`sendIntent`, TL-5).

**The cut: the server replays; the editor never does, until Plan 18.** The editor only needs to keep its own screen until its queue is empty (section 1), and with one save in flight and one waiting, that is at most two save times. What this gives up until Plan 18, all visible only when two writers touch the same thing or the person never pauses:
- an agent's change does not appear in the middle of a burst, only at the next pause;
- a clash on the same field parks the person's change; it is not re-applied for them;
- a delete after an agent's edit to the same clip is a parked change, not a delete.

**What to shape now so Plan 18 only swaps a payload** (all free, all already compatible):
- the queue record's payload is opaque to the queue (already in Plan 63);
- a save is a batch of steps (section 1), which is what a batch of named commands will be;
- every record declares its reads (project C), which a command with a selector does by construction.

One thing moves from Plan 18's list to project C: "narrow reads for function commits", in its plain default form. The selector-declared form stays in Plan 18.

### The recommended structure

| | Name | End state | Comes from | Size | Order |
|---|---|---|---|---|---|
| **A** | **Dependable saving** | The owner edits "Almost Ready" for a week with no stuck state, and the fast-edit property of section 1 passes in the model test and on the staging stack. One queue row per timeline; the screen is the person's; one save in flight and one batch waiting; four outcomes named by the server for every writer; a refusal parks itself; a new rule cannot refuse an old document | **Plan 63, kept:** CC-5a, CC-4, CC-4b, CC-12, CC-5b (with the batch, +3 days), CC-10, CC-7, CC-3, CC-6, R0 | about 30 days; the editor critical path about 15.5 | First. Starts on the owner's go and D15 |
| **B** | **Fast saving** | A one-clip edit on "Almost Ready" is accepted in under 1 s (stage 1), then 200 ms at the median (stage 2), the same at 3 and at 300 history entries, measured from the editor and failing a test when it stops being true. An import never waits on a commit | **Carved out of Plan 63:** CC-1, CC-2, CC-11, CC-9 (8.5 days), plus the new work in section 3 | stage 1 about 11 days; stage 2 about 9, started only if stage 1's numbers call for it | Beside A from the first day (Agent and Runtime; other people) |
| **C** | **Editing together** | A person and an agent edit one timeline: cases (a) to (e) of section 2 behave as the "should" column, proven by one test with both writers on a real stack. The person sees who changed what, within seconds, and never loses their place | **New.** One item from Plan 18's deferred list (narrow reads); the rest is in no plan | about 11.5 days | After A's CC-4 and CC-5b; the Agent half can start at once |
| **D** | **Extensible editing** | Plan 18 as written: every gesture a named command, anyone can add one. It also delivers the exact forms above | **Plan 18, unchanged** | about 60 days, then 9 | After A's R0 and the owner's week |

**Total before extensibility: about 52 days of work; about three weeks elapsed with A and B in parallel and C following.** (Plan 63 today is 35; the difference is the batch, +3; section 3's new speed work, +2.5 in stage 1; and project C, +11.5. Stage 2 of B is a further 9, decided on measurement.)

### The minimum that keeps it elegant

- **Three sentences carry the whole design.** *The screen is the person's; one save in flight, one waiting* (A). *Every reply is one of four outcomes; say what you relied on* (A and C). *A commit costs the change* (B). If a task serves none of the three, it is not in these projects.
- **No new mechanism in A or C.** The batch uses the request's existing list of steps; the merge uses the server's existing address rule; the notice uses fields the commit already stores. Each project deletes more than it adds.
- **Do not build:** the same-field coalescing rule (the batch replaces it); a replay of edits in the editor before Plan 18; a third queue for bundles; push events before the 2 s check has been found wanting; stage 2 of B before stage 1 has been measured.
- **One plan per project, not one plan with tracks.** Plan 63 already says its two tracks have no dependency between them; that is the definition of two projects, and it lets A ship what the owner feels without waiting for the server work to close.

## Not checked

- **Nothing was built or run.** No burst, co-editing case or timing was reproduced. Every "should" is a design statement.
- **The batch.** That k chained `doc.patch` records can go as k steps of one commit, with their reads combined and each step undone on its own. The request and the Agent's step code have the shape for it; the half-day spike in section 1 is what proves it.
- **How fine the merge is in practice.** The rule is by address with prefix overlap (read). Whether two different fields of one clip merge depends on how narrow each writer's patch paths are, which I did not read; only "different clips merge, the same clip clashes" is pinned by a test (reported).
- **Case (d), delete second,** is inferred from the prefix rule, not run.
- **Whether narrowing a function commit's default reads is safe** for intents that depend on things they do not change (a ripple, "tighten the intro"). The proposal keeps `reads="timeline"` for those; which built-in intents need it was not surveyed.
- **Which path clears undo on a foreign head** in the Runtime-backed editor. The local stacks are cleared (read); the editor also sends server-side undo (`timeline.inverse`), and how the two relate was not traced.
- **Whether `/v1/events` can carry a head change** (reported as unverified), so "push" is sized as new work.
- **`lookup.py:332` and the evaluate cost**, the remaining server time after the landed fixes, and the browser's write time per edit: all unmeasured.
- **The four Haiku reports** are used above as "reported" where I did not re-read the line. One claim in them (a moved head becomes a 500) was wrong and is corrected in section 2; treat the other reported lines as leads of the same quality.
- **The sizes** are my judgment on top of Plan 63's own figures, not a bottom-up estimate.
