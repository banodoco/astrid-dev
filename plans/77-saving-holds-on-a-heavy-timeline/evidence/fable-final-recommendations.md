# Final recommendations on Plans 63, 64, 65 and 18

18 November 2026. Read only; nothing was run and nothing was changed except this file.

**Sources.**
- Plans on astrid-dev `origin/plan/63-dependable-saving` (PR #880): the four `plan.md` files and Plan 18's `statements.md` read in full; the estimate tables, the owner decisions and the deciding task rows of each `tasks.md` read (CC-3, CC-4b, CC-5b, CC-5c, FS-1 to FS-5, CC-2, ET-1 to ET-6, TL-1, TL-2, TL-3r, TL-5, TL-5b, TL-13b, TL-15a, EX-2). The `inputs.md` files were not read.
- Review A (`fable-commit-proof-fit.md`) and Review B (`fable-end-state-review.md`) read in full. `fable-gap-method.md` and `fable-diagnosis-check.md` read; `fable-four-questions.md` and `fable-dependable-saving-check.md` skimmed by heading.
- Code: `release-src/runtime-src` at `9be54d5` and `agent-src` at `6468e38f3` (branch `task/plan59-shot-trim`), App worktree `wt-app-quick-edits` at `ff34621e9`. These are not the exact commits the two reviews read.

**Labels.** **[mine]** I read it. **[Haiku]** reported by one of four Haiku readers, not re-read. **[review]** taken from Review A or B. **[inferred]** my reasoning, not run.

---

## Verdict in brief

1. **The two reviews agree on the fault and differ only on how far to go. Both are right: A is the first step and B is the destination.** A's four tasks go into Plan 63. B's "the Runtime applies, it does not compare" goes into Plan 64 as one more task, sized by a one-day experiment.
2. **One design serves all four goals:** every change is a command the Agent runs on the current head to produce an effect list in a closed set of kinds; one acceptor per timeline applies and stores it. The effect list is the patch, the write set, the read set, the inverse and the history record.
3. **The authenticator question has an answer in outline.** Of its 340 refusal sites, about 158 are identity and binding work, about 91 re-check the provider's answer, 63 check shape and 28 are ordering and coverage [Haiku]. So "apply, don't compare" removes about a quarter of the sites and a third of the code. It is neither a pure deletion nor a rewrite, and the identity half stays.
4. **Keep four plan numbers; move tasks between them and re-phase Plan 18.** The agent and pack surface changes no App code, so it need not wait for the App track or the owner's week.
5. **Totals:** Plan 63 about 30 becomes about 39.5. Plan 64 about 20 becomes about 24.5 unconditional plus 2 conditional. Plan 65 about 11.5 becomes about 12. Plan 18 about 69 becomes about 62, plus 8.5 optional. The sum is 130.5 before and about 138 committed after, with 10.5 conditional or optional.
6. **The bisection's first result settles Plan 64's shape.** The same nudge costs 3.74 s on Almost Ready and 0.22 s on a one-clip timeline, and `validate_final_candidate` alone is about 2.2 s [coordinator-reported, measured, run 1]. The cost is the document, and most of it is one stage. So validating only what the effects touch is no longer a conditional stage 2: it is the main task, and the stage 1 and stage 2 split goes.

---

## 1. One design, not four plans

### The architecture

A change is a **command**. The Agent runs it on the current head and the run produces an **effect list**: ordered writes of `(address, before, after)` in a closed set of kinds. The Runtime's **one acceptor per timeline**, one commit at a time, checks one **proof rule**, applies the list, stores it with the new head and the head's findings. Everything else reads that stored list.

| Need | How the effect list serves it |
| --- | --- |
| The patch | Apply the writes in order |
| What the change wrote and relied on | The addresses written, plus the addresses the recorder saw read |
| A clash | Intersect those addresses with the stored lists of the commits since the head the writer named. No document is loaded |
| Undo | Swap `before` and `after`. `timeline.inverse` already does this from recorded `before` values [Haiku, `_doc_patch.py:537-564`, `inverse.py:1074`] |
| "Who changed what" | The label, author and addresses of the commits since a head |
| History | The list is the record. The store already keeps `records_json` and the canonical document per accepted commit [mine, `timeline_commit_store.py:787`] |

### Where the goals pull, and how the design resolves each

| Tension | Resolution |
| --- | --- |
| **Speed against per-commit proof** | The proof is the effect list plus the findings the change introduces. Both are the size of the edit. The head is settled (immutable history, stored findings), so nothing about it is proved again. What stays proportional to the document is one serialise and hash of the changed revision |
| **Extensibility against a closed set of effect kinds** | Ops are open and effects are closed. A handler can only write through the recorder, so a pack's op can only emit the closed kinds. The closed set is what lets the Runtime, undo, clash detection and the "who and what" line work for an op they have never heard of |
| **Agent edits against human edits on one head** | One serial acceptor and one clash rule for every writer. The only place the two kinds of writer differ is what the client does with `moved`: an agent runs again, a person's change parks |
| **Dependability against speed** | The batch (one save in flight, one waiting) bounds a burst at any commit cost. Speed then decides only how soon work is safe and how long an agent's change takes to show |
| **Extensibility against speed** | A pack op has no editor preview, so nothing shows until the accept. At 4 s that looks broken. Pack ops therefore need the fast acceptor, which the plans do not say [review B] |

---

## 2. The two pressure tests

### Review B's "closed set of effect kinds": it enables extensibility, with two conditions

**The code is already nearly this shape.**
- Every handler has the signature `handler(ctx: Recording, command)` and writes through one primitive, `Recording.assign`, which records `{ref, path, before, after}`; a clear is a write whose `after` is absent [Haiku, `_recording.py:121-132`].
- `doc.patch` goes through the same primitive [Haiku, `_doc_patch.py:240-268`]. So a raw patch is already "the identity command", as Review B wants.
- The kinds are few: write, `created`, `derived_writes`, and the list forms at the patch level (`set`, `remove`, `list.insert`, `list.remove`, `list.move`).

**So a pack op compiles down to the closed set by construction.** The set is the stable substrate: a pack adds meaning (ops) and data (new addresses), never a new way to change a document.

**Two conditions, neither met today:**

1. **The set must really be closed.** Binding keys and dependency kinds are open strings, and the Runtime authenticates bindings by key prefix [Haiku, `timeline_commit_auth.py:529-548`]. At least one handler path writes the bundle without a record (`_recording.py:206` sets `_created` directly) [Haiku; the `native_*` handlers were not audited]. Closing these is a small task (TL-3e below).
2. **The address space must be open.** A pack must be able to write its own fields and its own collections without a new kind. The Runtime knows collections by ref family (`clip`, `track`, `occurrence`, `asset`, `text-binding`, `collection`) [Haiku, `:121-131`]. Whether a pack-owned collection passes was not checked. The pack-op proof (EX-P below) must include it.

**What blocks extensibility today is the opposite of a closed set.** The Runtime branches on eight op names (`doc.patch`, `timeline.inverse`, `track.create`, `list.move`, `occurrence.fork`, `occurrence.swap-media` and two prefixes) at about 25 lines [Haiku]. A pack op that needs what those branches give cannot get it. Review A's rule 3 ("the Runtime never branches on an op name") is the fix.

**There is no registry yet.** `register_operation` does not exist outside tests; the 35 ops are a dict literal whose docstring says the extensible registry "belongs to M2" [Haiku, `commands.py:29-118`]. Plan 18's TL-3r builds it. That is the real start of agent extensibility, and it is an Agent-only change.

### Review A's "proof derived in the Agent": compatible with fast saving, and it is the cheap part

- **Deriving the proof is the run itself.** A handler's execution is milliseconds [inferred, `fable-gap-method.md`'s floor table]. The 4 s is not derivation.
- **The 4 s is whole-document work repeated.** Twelve commits of the same nudge cost 4,086 to 4,399 ms, a 7% spread [`fable-diagnosis-check.md`, read there]. The older profile showed many whole-document passes per commit: deep copies, serialisation, digests, compiles [Haiku, from `sonnet-commit-profile-r14.md`]. `validate_final_candidate` runs on every one of up to three attempts [Haiku, `commit.py:1343`, `:1406-1417`].
- **A proof proportional to the edit needs five things, all in the plans or in this review:**

| Part of a commit | Proportional to the edit when | Where |
| --- | --- | --- |
| Run the command, record effects | Already | Existing |
| Clash check | Address intersection over stored effect lists, not document loads | FS-4, simpler once the effect list is the record |
| Rules | The head's findings are stored; only rules that read what changed run. **This is the measured hotspot** | FS-3a (stored findings), FS-3b (read-scoped rules) |
| Runtime's check of the answer | It applies the list; it does not re-project and compare | FS-6 (new) |
| Store | One durable write; one serialise and hash of the changed revision | CC-2 |

- **The bisection's first result** [coordinator-reported, measured on an APFS realm clone at the Release 14 pins, median of warm one-clip nudges; run 2 is in progress]:

| Measure | Value | What it means |
| --- | --- | --- |
| Almost Ready | 3.74 s | |
| A one-clip timeline, same stack | 0.22 s | The fixed cost of a commit is already under 300 ms. About 3.5 s is proportional to the document |
| `validate_final_candidate` | about 2.2 s, about 60% | One stage holds most of it. This is a hotspot, not many equal passes |
| Everything else that follows the document | about 1.3 s [my subtraction] | Load and verify the base, build and digest the document, the reader check, the records, the Runtime's own checks. Not yet split |

- **Is 300 ms reachable? Yes in principle, and only by proof proportional to the edit.** The 0.22 s is the measured floor: it is what a commit costs when the document is small enough not to matter. Reaching it on a large document takes two things, in this order:
  1. **Validate only what the effects touch, against the head's stored findings (FS-3a and FS-3b).** This is aimed at the 2.2 s. If it works fully, a commit is about 1.5 s [my arithmetic, not measured]. That is not under a second by itself.
  2. **Make the remaining 1.3 s follow the edit:** keep the verified base by immutable revision id (CC-2), let the Runtime apply the effect list in place of re-projecting and comparing (FS-6), and build the reader check from the delta. Only then does the total approach the 0.22 s floor plus one serialise and hash of the changed revision.
- **What this does to Plan 64's stages.** Plan 64 put "validate what the change touches" in a conditional stage 2, to start "only on stage 1's numbers", and its own honest limit said stage 1 reaches 1.5 to 2 s. The number that was to start stage 2 now exists. Trimming repeats cannot reach a second when one stage is 2.2 s and it runs once. **FS-3 moves to the front of the plan, and the two-stage structure is dropped.**
- **Caution.** Run 2 (no history, dry run, skipping the validator and the reader check, a cProfile run) is not in. Until it is, "60%" is one measurement, and the split of the other 1.3 s is unknown. If run 2 shows that most of the 2.2 s is one repeat inside the validator (for example the baseline validated again on each commit, or a validator built per clip), a small fix may take a large share before FS-3b is built. FS-3a, storing the head's findings, is the version of that fix that is also the end state.
- **The browser will be the larger share at that point.** One edit stores about three whole documents on the named-command path and about five on the document-patch path, and every append reads, clones and rewrites the whole row [Haiku, `commitOutbox.ts:308-318`, `localSaveSession.ts:25-36`]. Plan 63's CC-5b fixes the shape; it needs a real-browser measure of its own.

---

## 3. The open rules, settled

### Clashes: one server rule, park for a person, run again for an agent

**Recommendation.** A change is accepted if and only if nothing it relied on or wrote was changed by another writer between the head it named and the current head, and it introduces no new finding. Otherwise the reply is `moved` and names the addresses and the commits that changed them.

- **An agent** reads again and runs again, at most three times, then reports.
- **A person's change parks**, with everything queued behind it, in the one bar: "The agent changed this clip first." **Try again** sends it on the current head, where it now lands. That is the person overwriting on purpose. **Discard** drops it.

**This is D15 applied to a clash, and it cuts Plan 18's automatic re-apply.** Reasons:

- Plan 65 says "nobody overwrites without being asked". Plan 18's TL-5 re-applies a person's change on a same-field clash without asking. Both cannot stand [review B].
- Parking needs no new mechanism: it is the same entry, bar and buttons as a refusal.
- The window is short. Once the editor notices a foreign head in seconds and a commit is fast, a same-address clash needs both writers to touch one field within about a second.
- **"A delete beats an edit" goes too.** The delete parks with "The agent edited this clip; Try again deletes it". One rule, no exception list.

**Where I differ from Review B.** B suggests a command re-run on the current head simply wins and the line shows what it replaced. That is silent overwrite with a notice afterwards. It also makes a command's proof differ from a snapshot's. Counting written addresses as relied on keeps one proof rule for every payload kind.

**One thing to settle in TL-1:** a writer's own earlier queued records must not count as "another writer". Plan 63's `basis: {after: id}` already carries that.

### Undo: `timeline.inverse` of the person's own record; no local snapshots

**Recommendation.** Undo is a command like any other.

| Case | Rule |
| --- | --- |
| The edit is still queued and unsent | Remove it from the queue |
| The edit is in flight or accepted | Append `timeline.inverse` naming it; it goes through the same queue, proof rule and four outcomes |
| Someone changed the same address since | `moved`, so the undo parks: "The agent changed this since; Try again undoes it anyway" |
| A foreign head is adopted | The undo list is a list of the person's own records, so it survives |
| Undo an agent's change | The same command, from the "who and what" line |

**Most of this exists.** In the Runtime-backed editor, undo already appends a `timeline.inverse` command through the outbox, with targets taken from server history filtered to this actor [Haiku, `timelineLocalSaveHandoff.ts:346-365`, `:1040-1085`]. The snapshot stacks (100 whole-document entries, cleared on any foreign head) are the fallback path for an editor with no Runtime save [Haiku, `useTimelineHistory.ts:205-223`, `:308-323`]. The server refuses an inverse of a field someone has since changed (`inverse_conflict`) and leaves unrelated newer work alone [Haiku, `inverse.py:1117-1119`].

So the rule is mostly a deletion: remove the snapshot stacks on the Runtime-backed path (TL-1 item 10 leaves this open; decide it now), and map `inverse_conflict` to `moved`.

### What an agent's edit relies on

**Recommendation: derived, never declared, with one opt-in.**

- **A named command:** the addresses the handler read through the recorder, plus the addresses it wrote. Already recorded [Haiku, `_recording.py:93-99`].
- **A function commit:** the union of its commands' recorded reads and writes. Today it defaults to the whole timeline, `merge="atomic"` [Haiku, `commit_session.py:765-775`], which is why unrelated edits clash. `reads="timeline"` stays as the one opt-in, for a ripple or "tighten the intro".
- **A document publish:** the addresses in its diff, derived on the server.
- **The editor's document patch:** the addresses it writes, derived on the server; the values it sends are ignored (CC-16).

**When a person edits underneath an agent:**

| The person changed | Result |
| --- | --- |
| Nothing the agent's change read or wrote | Both land |
| Something it read or wrote | The agent gets `moved`, re-reads and runs again |
| The thing it targets was deleted | The re-run is refused with a code; the agent reports "that clip was deleted in the editor; skipped" |

**The accepted risk.** A function that reads widely, writes narrowly and does not opt in can land on a head where its premise changed. The rule gate still refuses an invalid result. What gets through is a valid edit made on slightly old information. The answer is the "who and what" line with one-click undo of the agent's commit, which I promote from nice-to-have to a must (ET-4b).

---

## 4. Duplicated truths that remain

After these recommendations, every fact still held in two places:

| # | Fact | Held by | Why it stays |
| --- | --- | --- | --- |
| 1 | What an edit means | The Agent's handler; the editor's preview | Instant feedback. The preview cannot refuse and snaps to the result |
| 2 | How an effect is applied | The Agent's recorder (as it runs); the Runtime's applier | Two implementations of a handful of kinds. Held together by one test: applier(effects, base) equals the provider's document, on every matrix row |
| 3 | Bindings and identities | The provider proposes them; the Runtime checks them against stored objects | About 158 sites [Haiku]. It ends only if the Runtime allocates identities itself, which no plan proposes. **The largest remaining one** |
| 4 | The inverse | The stored `before` values; the Runtime's inverse-stage code, 1,114 lines and 114 sites [Haiku] | Review A leaves it alone and so do I. A candidate once FS-6 is proven |
| 5 | The outcome of a reply | The App's decoder; the Agent's client | One pinned fixture |
| 6 | Old-Runtime fallbacks | A status table in `send`; `details.status` in the Agent client | Give both an end date |
| 7 | The command schema | The Agent's registry; generated App types and constants | One direction, generated. The Runtime copy is cut |
| 8 | The queue | The editor's outbox; the Agent's pending record | One contract, two implementations, by the plans' choice |
| 9 | The head's findings | Stored with the head; recomputable from the document | A cache. It must be keyed by rule-set version |
| 10 | A `before` value in a raw patch | The writer's copy; the server's base | A value the writer saw. Treated as an address only (CC-16). Gone from the App with Plan 18; it stays for agents' raw patches |
| 11 | Edit kinds | `EDIT_KINDS` in the App; the Agent's registry | Until TL-5 generates one from the other |

---

## 5. Final recommendations

### 5.1 The target architecture

1. **Effect list** (Agent produces, Runtime stores): the one representation of an edit; closed kinds; a read is an address, never a value.
2. **Command** (Agent's registry): a named function from head, selector and arguments to an effect list. A raw patch is the identity command. Packs register commands here.
3. **Acceptor** (Runtime): one commit at a time per timeline. It applies the effect list and compares nothing the provider already computed.
4. **Proof rule** (stated once, checked in the Agent): nothing relied on or written was changed by another writer since the named head, and no new finding.
5. **Head** (Runtime): immutable history; the head's findings stored with it.
6. **Identity and binding** (Runtime): ids, revisions, object digests, keys. The only thing the Runtime checks about a provider's answer.
7. **Rule registry** (Agent): pure `findings(document)`, under the delta gate. Packs register rules here.
8. **Outbox** (each writer): ordered records with an opaque payload, sent as a batch; parked entries live in the same row.
9. **Four outcomes** (set where each reply is built): the only thing a client branches on.
10. **Client policy on `moved`** (each client): an agent runs again; a person's change parks with Try again and Discard.
11. **Undo** (a command): `timeline.inverse` of the writer's own record.
12. **Preview** (App): a disposable local picture of a gesture; never a judge.

### 5.2 Plan by plan

#### The split

**Keep the four numbers. Change two cut lines.**

- **Plan 64 is "one acceptor", not only "fast".** Serial commits, stored findings and "apply, don't compare" are simplifications that also make it fast. They belong together and should not wait on stage 1's numbers.
- **Plan 18 is re-phased: agents and packs first, editor gestures second, the alternate view optional.** The owner's goal names extensibility for agents. The registry, the CLI verb, the MCP tool and the pack-op proof change no App code, so they do not need the App track's R0 or the owner's week.

#### Plan 63, Dependable saving: about 30 becomes about 39.5

| Task | Call | Days |
| --- | --- | --- |
| CC-5a, CC-4, CC-5c, CC-10, CC-7, CC-3, CC-6, CC-12, R0 | **Keep** | as planned |
| CC-4b | **Change:** `outcome` is a required argument of every failure constructor. No reason-to-outcome table [review B] | 2.5, unchanged |
| CC-5b | **Change:** a record holds a patch, never a document; an append costs the edit, not the row. Acceptance adds a real-browser measure on a real-size document against the 50 ms "kept" budget | 7 becomes 7.5 |
| CC-5a | **Change:** add undo rows (undo of a queued edit, of an edit in flight, of an accepted edit) | within its 2 |
| **CC-13** every edit kind is accepted, through the real Runtime route, from one `EDIT_KINDS` list [review A] | **New.** Day one. This becomes the one harness: CC-5c's first check, TL-15a and ET-6's server rows reuse it | 3.5 |
| **CC-14** close what CC-13 shows red [review A] | **New** | 2 (1 to 4) |
| **CC-15** one record shape per effect kind [review A] | **New** | 1.5 |
| **CC-16** a read is an address [review A] | **New, re-scoped.** The declared value is compared with the writer's base on the first pass and with the current head after a rebase [Haiku, `commit.py:1338`, `:1383`]. So on a replay it is the clash check. CC-16 must replace that with the base-to-head address comparison, not only delete it. Review A flagged this as unchecked | 2 (was 1.5) |
| New end-state check P0-7 [review A], plus one line: `invalid_records` is unreachable from any matrix row | **New** | 0 |

- **Order:** CC-13, CC-5a and CC-7 on day one. CC-14, CC-15 and CC-16 follow CC-13. The App critical path stays about 16 days.
- **Statement to add:** "the server derives; nobody compares" as invariant 6, with the proof rule in one sentence.

#### Plan 64, Fast saving: about 20 becomes about 24.5 unconditional plus about 2 conditional

| Task | Call | Days |
| --- | --- | --- |
| **FS-0** permanent stage spans and size fields on the provider's timing line (`fable-gap-method.md` section 4), and the bisection read off them | **New.** Half is in flight now | 0.5 |
| FS-1, CC-1, CC-11, CC-9, FS-2 | **Keep** | 7 |
| CC-2 | **Keep,** and prefer deleting a re-check to caching its answer once CC-11 makes history immutable [review B] | 4 |
| **FS-3a** store the head's findings with the head | **Split from FS-3; unconditional, and first after FS-0.** It removes any validation of the base on a commit | 1.5 |
| **FS-3b** validate only what the effects touch: a rule declares what it reads, and only rules whose inputs the effect list touched run | **Unconditional, moved to the front.** It is aimed at the measured 2.2 s. Needs Plan 63's CC-3 (the registry), so CC-3 is now on Plan 64's critical path | 4.5 |
| **FS-5** one commit at a time per timeline | **Promote to unconditional.** It deletes three attempts and `head_busy`. First half-day: check lock order, because the provider's reads take the store-wide `store._mutex` and no per-timeline lock exists today [Haiku, `timeline_commit_execution.py:462-483`, `store.py:1087`] | 2 (was 1.5) |
| **FS-6** the Runtime applies the effect list and re-compares nothing | **New.** Removes the re-check class: about 91 sites and 940 lines [Haiku]. Needs CC-13 and CC-15 first, and the shadow-applier experiment (section 5.5) | 5 (3 to 8) |
| **FS-4** replay against the net difference | **Conditional.** Smaller once clashes are address intersections | 2 |

- **Drop the stage 1 and stage 2 split.** One plan, one target: 300 ms at the median from gesture end to accept on Almost Ready, with under 1 s as the first recorded milestone. FS-4 is the only conditional task left.
- **Order:** FS-0 and FS-1 first; then FS-3a and FS-3b (the hotspot) as soon as CC-3 lands; CC-1 then CC-2 for the other 1.3 s; FS-5 and CC-11 beside them; FS-6 after Plan 63's CC-13 and CC-15.
- **Each task states a prediction first:** "this stage costs X ms; after, the total will be Y" (`fable-gap-method.md`, section 5). FS-0's spans make that a log read.

#### Plan 65, Editing together: about 11.5 becomes about 12

| Task | Call | Days |
| --- | --- | --- |
| **ET-0** state the clash rule and the undo rule; the `moved` reply names the addresses and commits | **New** | 0.5 |
| ET-1 narrow reads | **Change.** Cut the editor half: the editor declares nothing new, the server derives written addresses. Keep the Agent half: function commits default to their commands' recorded addresses, a publish derives its diff, and the survey of intents that need `reads="timeline"` | 3 becomes 2 |
| ET-2 notice a foreign head | **Keep, with a first check.** A `timelines-updated` event listener already exists [Haiku, `useTimelineRealtime.ts:13-22`]. If it fires for an agent's commit, relax the gating and add no 2 s check | 1 |
| ET-3 adopting keeps the person's place | **Change.** Undo already goes by `timeline.inverse` per actor. Delete the snapshot stacks on the Runtime-backed path; keep selection, playhead and scroll | 2 |
| ET-4 who and what | **Keep** | 1.5 |
| **ET-4b** undo the agent's change from the line | **Promote** from nice-to-have. It is the safety valve for narrow default reads. Unverified: that the server lets one actor invert another's commit | 1 |
| ET-5, ET-6 | **Keep** | 4 |

- **Cut from the deferred list:** "Keep mine" on a clash (Try again is it) and "delete beats edit".

#### Plan 18, Extensible editing: about 69 becomes about 62, plus 8.5 optional

**Phase A, agents and packs (about 18 days; Agent and Runtime only).** Starts after Plan 63's server track (CC-3, CC-4b, CC-13, CC-15, CC-16), not after R0 and the owner's week.

| Task | Call | Days |
| --- | --- | --- |
| TL-1 | **Change.** Item 5 becomes a decision: the command payload is opaque to the Runtime, and the provider discovers pack ops and rules when it loads. Item 4 inherits the clash rule. Item 10 inherits the undo rule | 4 |
| RS1 | **Keep,** gated for Phase A on Plan 63's server checks only | 1 |
| TL-2 | **Change.** Cut the Runtime's schema copy, its sync script and the command half of the digest handshake; the Runtime validates the envelope only [review B]. Keep the generated App constants and the lock check | 2 becomes 1.5 |
| TL-3r registry | **Keep** | 1.5 |
| **TL-3e** close the set: enumerate binding and dependency kinds, remove direct bundle writes, and remove the Runtime's op-name branches that a generic effect covers | **New** | 1.5 |
| TL-13a two tiers, one door | **Keep,** worded as "a raw patch is the identity command" | 3.5 |
| TL-13b agents send ops | **Change.** Cut selector-declared reads | 3 becomes 2.5 |
| **EX-P** the pack-op proof: a pack op with its own handler, its own data address and its own rule, accepted by an unmodified Runtime and App, as rows in the CC-13 harness | **New.** Replaces phase 2 as the proof of extensibility [review B] | 2.5 |

**Phase B, editor gestures as commands (about 44 days).** After Plan 63's R0 and the owner's week, as planned.

| Task | Call | Days |
| --- | --- | --- |
| TL-3a to TL-3d, TL-4, TL-5b, TL-6 to TL-12, TL-15b, R | **Keep** | 41 |
| TL-5 | **Change.** Cut automatic re-apply and "delete beats edit" | 2.5 becomes 2 |
| TL-15a | **Change.** Rows end at the Runtime's commit route through the CC-13 harness, not at `validate_final_candidate` [review A] | 3 becomes 2 |

- TL-4's reason list needs no Runtime copy either: a reason never decides behaviour.

**Phase C, the alternate view (about 8.5 days): optional.** It is a product feature, not the proof. The owner decides (D5).

#### Order and dependencies

```
Release 14 stop-gap (now)
        │
Plan 63 App track ───────────────► R0, the owner's week ─► Plan 18 Phase B (editor)
Plan 63 server track ─► CC-13..16 ─┬► Plan 64 FS-6
        │                          └► Plan 18 Phase A (agents and packs) ─► Plan 65 ET-1 (agent half)
Plan 64 FS-0, FS-1, CC-1, CC-2, FS-5, CC-11 (from day one); FS-3a, FS-3b after Plan 63's CC-3
Plan 65 editor half: after Plan 63's CC-4, CC-4b, CC-5b
```

### 5.3 Release 14, the stop-gap, now: about 3 to 4 days

| Piece | Days |
| --- | --- |
| Runtime #66 and App #308, each with its own regression case | landed |
| A one-off sweep of every edit kind on a sandbox timeline on the staging stack; list every refusal [review A] | 1 |
| Fix what an ordinary session hits; the rest become named gaps | 1 to 2 |
| Finish the speed bisection (run 2), with the stage spans left in as a diagnostic | 0.5 |
| The condition is now met: `validate_final_candidate` is about 60%. **If run 2's profile shows one removable repeat inside it** (the base validated again, or a validator built per clip), fix that one, with a predicted before and after. If the time is spread across the rules, do nothing here: that is FS-3b, in Plan 64 | 1 to 2, conditional on run 2 |

**Not in Release 14:** anything that changes what the browser stores or what goes over the wire (the batch, the queue shape, a read as an address, serial commits).

### 5.4 Decisions only the owner can make

| ID | Decision | Recommendation |
| --- | --- | --- |
| D9 | Which release carries the plans | **Release 15.** Release 14 gets only section 5.3 |
| D15 | What a refused change looks like | **Park it with everything behind it; Try again and Discard** |
| New | Does a clash follow the same rule as a refusal? | **Yes.** A person's clashing change parks and is never re-applied automatically; Try again is "keep mine". This cuts Plan 18's automatic re-apply and "delete beats edit" |
| New | What an agent's function relies on by default | **Only what its commands read and wrote;** the whole timeline is opt-in. The accepted risk is a valid edit made on slightly old information, shown in the "who and what" line with one-click undo |
| New | Plan 18's order | **Agents and packs first, without waiting for the week of editing;** editor gestures after it |
| D5 | The alternate view | **Defer.** The pack-op proof replaces it as the proof |
| New | The speed target, and Plan 64's shape | **300 ms, with under 1 s as the first milestone, and no conditional stage 2.** The bisection shows the cost follows the document and 60% is one stage, so validating only what a change touches is the plan, not an option. It adds about 4.5 committed days |
| D10 | Corpus data | **Synthetic,** as recommended. The shadow-applier experiment reads a local copy of real history and commits none of it |

### 5.5 Risks, and the first experiment

| # | Risk | What reduces it |
| --- | --- | --- |
| 1 | **FS-6 turns into a rewrite.** The four largest authenticator functions mix identity checks with re-checks, and 30 to 40 of the per-site labels are judgment calls [Haiku] | The shadow applier, below |
| 2 | **The speed target.** Run 1 shows the cost is the document and 60% is the validator; the other 1.3 s is not split, and FS-3b's saving is predicted, not measured | Run 2 of the bisection; then a half-day spike before FS-3b: skip every rule that reads nothing the nudge touched and time the commit |
| 3 | **The closed set is not closed.** Open binding and dependency kinds; at least one unrecorded write | TL-3e; the shadow applier finds unrecorded writes as mismatches |
| 4 | **Serial commits deadlock or stall** on `store._mutex` | FS-5's first half-day |
| 5 | **CC-16 removes a clash check by accident** | Its re-scope above; a matrix row with a foreign commit between base and head |
| 6 | **Narrow default reads land a stale-premise edit** | The opt-in, the survey in ET-1, and ET-4b |
| 7 | **Proof machinery outgrows the product** [review B] | One harness (CC-13) reused by CC-5c, TL-15a and ET-6 |
| 8 | **The browser becomes the bottleneck** once the server is fast | CC-5b's real-browser measure |
| 9 | **Estimates are judgment,** mine included | Re-estimate CC-14 from the sweep and FS-6 from the experiment |

**The first experiment: a shadow applier over real accepted history. About one day, read only, offline.**

- **What.** On a copy of a realm database, for each accepted commit, take the stored records and the previous canonical document, apply the recorded writes with a generic applier of about 200 lines, and compare the result with the stored canonical document.
- **Why it is cheap.** Both halves are already stored per commit [mine, `records_json` and `result_json` in `timeline_commit_store.py`]. Almost Ready's history is a corpus of hundreds of real commits.
- **What it decides.**
  - **Share equal, by op.** Near 100% means the effect list is a sufficient record and FS-6 is a deletion of the re-check class. A low share for some ops names exactly which ones carry meaning outside their effects (shot materialisation and occurrence forks are the likely ones).
  - **Every mismatch is an unrecorded write or an open kind,** which is risk 3's list.
  - **The time to apply** is the floor for the Runtime's share of a commit.
- **Run it beside the bisection's run 2.** The bisection has answered "is the cost the document" (yes). The applier answers how much of the authenticator is comparison that can go, and run 2 says how much of the remaining 1.3 s that comparison costs.

---

## 6. Where I side with each review

| Point | A | B | Mine |
| --- | --- | --- | --- |
| The hole is the Agent to Runtime proof boundary | Yes | Yes | Yes |
| Reads are addresses, not values | Yes | Adopted from A | Yes; and the replay path needs a replacement check (CC-16) |
| How far the Runtime goes | Projects and compares, with fewer shapes | Applies, compares nothing | A's tasks first in Plan 63; B's as FS-6 in Plan 64, sized by the experiment. The identity half stays |
| The matrix | Specified (CC-13) | Endorsed | Adopt A's, and make it the one harness |
| Serial commits and stored findings unconditional | Not addressed | Yes | Yes, with the lock-order check |
| Command payload opaque to the Runtime | Implied | Yes | Yes |
| Same-thing clash | Not addressed | The later gesture wins, with a notice | Park, by D15; one proof rule for every payload |
| Undo | In the matrix rows | `timeline.inverse`; queue removal | Same as B; most of it already exists |
| Phase 2 | Not addressed | Change what it proves | Replace with EX-P in Phase A; the view is optional |

---

## Not checked

- **Nothing was run.** No request was sent, no experiment was performed and no time was measured by me.
- **The authenticator classification** is one Haiku reader's, over the whole file. I did not re-read the sites. Its own note says 30 to 40 labels in four mixed functions could swap between identity and re-check. Its count is 340 sites in 3,411 lines; the reviews counted 344 in 3,432, on a different commit.
- **The Agent facts** (one write primitive, the open binding kinds, the bypass at `_recording.py:206`, the lock chain, the retry loop, the inverse construction) are one Haiku reader's. I checked only that the store keeps records and the canonical document per commit.
- **The App facts** (undo by `timeline.inverse`, the snapshot stacks as fallback, document copies per record, the `timelines-updated` listener) are one Haiku reader's, from `wt-app-quick-edits`, not the Release 14 tip.
- **Whether a pack-owned collection passes the Runtime's ref families,** and whether one actor may invert another's commit. Both are named as first checks.
- **Whether the shadow applier can use stored records as they are.** I saw the two columns, not their full shape; derived writes and materialised shots may need more than a generic apply.
- **The speed figures.** The bisection's run 1 (3.74 s, 0.22 s, about 2.2 s in the validator) was reported to me by the coordinator while I wrote; I did not see the run. The 1.3 s remainder and the 1.5 s after FS-3 are my subtraction. The 4 to 5 s and 95% are from `fable-diagnosis-check.md` and the brief; the older profile files give 8.6 to 9.3 s.
- **The `inputs.md` files** of the four plans, and most task rows outside those listed under Sources.
- **Day counts** are judgment on the plans' own figures and the two reviews', not bottom-up.
