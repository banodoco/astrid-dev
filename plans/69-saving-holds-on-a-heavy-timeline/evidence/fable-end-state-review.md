# End-state review: saving and editing after Plans 63, 64, 65 and 18

18 November 2026. Read-only review of the destination, not the sequencing or the effort.

**Sources.** Plans on astrid-dev `origin/plan/63-dependable-saving` (PR #880): each plan's `plan.md` and `statements.md` read in full by me; `tasks.md` and `inputs.md` inventoried by four Haiku agents, with the deciding task rows (CC-3, CC-4, CC-4b, CC-5c, CC-6, TL-1, TL-5, TL-5b) read by me. Code: `release/14/plan-59` in `runtime-src` and `agent-src`.

**Claim labels.** *[mine]* I read the code or plan text myself. *[Haiku]* reported by a subagent, not re-checked. *[inferred]* my reasoning, not run.

---

## Verdict

**Nearly, with one structural hole.** In the editor and on the wire the end state is elegant and close to minimal: one queue, four outcomes, one command vocabulary, one rule gate, and it deletes far more than it adds. Between the Agent and the Runtime it is not: the plans leave in place, and never mention, the layer that produced today's refusals. The destination has one edit representation for clients and still three for the server, compared against each other on every commit.

The whole review reduces to one principle the plans apply on the App side and not on the server side: **derive, don't compare.** Wherever one fact is held in two forms and checked for agreement, every disagreement in *form* becomes a refusal of a valid edit. Plan 18 removes that pattern from the App (the expected-diff blocks). Nothing removes it from the Runtime.

---

## 1. The end state, in my words

1. A person's gesture shows on screen at once, is kept in the browser within 50 ms, and is never refused at the moment of editing.
2. Every unsaved change lives in one ordered queue per timeline; the screen is the accepted head with that queue applied.
3. A gesture, an agent's edit and an extension's edit are the same thing: a named command `{op, select, args}` sent to one route with the head read and a key kept.
4. The reply is one of four outcomes named by the server: accepted, moved, refused, unavailable. A refusal carries a code and a plain headline, parks the change, and never blocks further editing.
5. Changes to different things by a person and an agent both land; the person sees who changed what within seconds and keeps their place.
6. A commit costs what it changes, not the history: under a second on a long-lived timeline.
7. A document rule can refuse only what a change introduces, and nothing can be stored that is later refused.
8. A pack can add a command and gets validation, atomicity, undo and coded refusals without an App change.

**Is it the right end state?** Yes. Each line answers an observed failure, and together they are what a local-first editor shared with agents should promise.

**Essential and missing:**

- **One proof rule between the Agent and the Runtime** (section 3). The end state says who decides the *meaning* of an edit (the Agent) and never says what the Runtime may demand of the Agent's answer. That gap is today's bug class.
- **One notion of undo.** The App keeps local undo stacks, the server has `timeline.inverse`, and how they relate "was not traced" (Plan 65 inputs *[Haiku]*); Plan 18 leaves local undo snapshots to "the TL-1 decision (delete, or named as a second path)" *[mine]*. Undo of a queued edit, of an accepted edit, and across a foreign change are three cases with no stated rule.
- **One rule for a same-thing clash.** Plan 65 says a person's clashing change "is parked and shown" and "nobody overwrites without being asked". Plan 18's TL-5 delivers "re-applying a person's change automatically on a same-field clash" *[mine]*, which is the person overwriting the agent without being asked. Both cannot be the destination.

**Included and not needed for the end state:**

- Plan 64 stage 2 as a separate conditional tier (its pieces sort into "part of the minimum" and "cache", see section 2).
- Plan 18's phase 2 alternate view as a product deliverable. It is a proof of line 8, and a weaker one than it looks (section 3.4).
- The integer-millisecond rename of existing ops. Worth doing; not part of this end state.

---

## 2. The minimum, from first principles

### The minimal concept set

| # | Concept | Definition |
| --- | --- | --- |
| 1 | **Effect list** | The one edit representation at acceptance: an ordered list of `(address, before, after)`, produced by the server running the change. It is at once the patch, the write set, the narrow read set (the addresses written), the inverse (swap the two) and the history record. Extra reads, for a change that depends on things it does not write, are addresses in the same address space. A writer never sends a value it saw: a read is an address at a named head, and the server looks the value up. |
| 2 | **Command** | A named function from `(head, select, args)` to an effect list, held in one registry in the Agent. A raw patch is the identity command, not a second tier. |
| 3 | **One acceptor** | The Runtime's commit route, one commit at a time per timeline: look up the key, run the command on the *current* head, apply the effects, run the rules on the result, append the revision. |
| 4 | **One proof rule** | A change is accepted if and only if the addresses it relied on are unchanged between the head it named and the current head, and it introduces no new finding. Nothing else is proved by anyone. The Runtime *applies* the effect list to get the new document; it does not receive a document and compare. |
| 5 | **One head** | Only the Runtime has one. A client holds the last head it adopted and its queue; its screen is `preview(head, queue)`. Rebase happens in one place: the acceptor running the command on the current head. |
| 6 | **One outbox per writer** | Ordered records `{id, key, payload}`, payload opaque, sent as a batch; parked entries are records in the same row. |
| 7 | **Four outcomes** | Set where each reply is built; the only thing a client branches on. |
| 8 | **One rule registry under a delta gate** | `findings(document)` pure; the head's findings are stored with the head, so the gate is `findings(candidate) − findings(head)`. |

Two consequences follow without extra mechanism *[inferred]*:

- **`moved` is rare.** A command re-run on the current head either applies or is refused with a code ("that clip was deleted"). `moved` is only for a writer whose change was computed from a snapshot: an agent's function commit, a document publish, a raw patch.
- **No race loop.** With one commit at a time per timeline there is no "replay up to three times" and no `head_busy`.

### Component by component

| Minimum | What the four plans build | Match |
| --- | --- | --- |
| Effect list as the one representation | Clients send commands (18). The Agent provider returns three things, a patch per step, recorder records (writes, reads, bindings) and a canonical document, and the Runtime's `timeline_commit_auth.py` re-projects each effect from the records and requires all three agree *[mine]*. No plan changes this. | **No** |
| Command registry | `register_operation` in the Agent, schema and listing generated (18 TL-3r). | Yes |
| Raw patch is the identity command | "Two tiers through one door": `doc.patch` kept as tier 2, both through `validate_final_candidate` (18). Same idea, worded as two tiers. | Nearly |
| One acceptor, serial per timeline | One commit route (63). Serial commits are FS-5, **conditional stage 2** of 64; until then the Agent replays on a moved head up to three times, then `head_busy`. | Partly |
| One proof rule | Rules: yes (63 CC-3, the delta gate). Reads and effects: checked in the Agent (`_commit_patch.py:332`, "declared field read does not match") **and** again in the Runtime (`timeline_commit_auth.py:252`, "declared field read differs from its input boundary") *[mine]*; not addressed. | **No** |
| One head, one rebase | Screen is head plus queue replayed (18 TL-5; 63 keeps one stored `after` until then). Server rebases by address. Good. | Yes |
| One outbox per writer | One row per timeline, opaque payload (63 CC-5b); the Agent keeps its own pending record, same contract (63, 65). | Yes |
| Four outcomes | 63 CC-4, CC-4b. | Yes |
| One rule registry, delta gate | 63 CC-3. Head findings stored: only as FS-3, conditional stage 2. | Nearly |

### Every mechanism beyond the minimum

| Mechanism | Plan | Why it is there | Call |
| --- | --- | --- | --- |
| The Runtime's authentication of provider records (`timeline_commit_auth.py`, 3,432 lines, 344 `require` sites, all `invalid_records` 422) | none (existing, untouched) | The "neutral" Runtime does not trust the provider it imports in-process as "the one trusted provider" *[mine]* | **Cut to a generic effect applier.** See section 5, change 1. |
| Batch: one save in flight, one waiting, k steps in one commit | 63 CC-5c | A person edits faster than a commit lands | **Keep.** It is the outbox's send rule, and it stays needed even at one second a commit. |
| Refused batch resent step by step, once | 63 CC-5c | A commit is all-or-nothing, so one bad step refuses the batch | **Merge** into the reply: name the refused step and accept the prefix. Cheap as written, so fine as an interim. |
| `basis: {after: id}` on each record | 63 CC-5b | Continuity of chained document patches | **Cut with 18.** Order in the queue is the continuity once payloads are commands. |
| One stored display `after` copy | 63 | No replay in the editor before commands | **Cut with 18** (TL-5 says so). |
| Parked entry, Try again and Discard | 63 CC-5b | The home of `refused` | **Keep.** |
| Web Lock for the sending tab | 63 CC-5b | Two tabs share one row | **Keep.** |
| Migration of old browser state | 63 CC-5b | Unsaved work in the old shape | **Keep**, once. |
| Status-code fallback in `send`, and `details.status` fallback in the Agent client | 63 CC-4, CC-4b | A hosted editor may meet an older Runtime | **Keep with an end date.** Two fallbacks for one fact; delete both when old Runtimes are unsupported. |
| Reason-to-outcome mapping table in the Agent's `failure()`, beside the Runtime's own setting | 63 CC-4b | Most refusals are built in the Agent | **Merge.** Make `outcome` a required argument of every failure constructor. A table from reason to outcome contradicts "reasons never decide behaviour". |
| Reply fixture pinned by hash across App and Agent | 63 CC-4b | Proves two decoders agree | **Keep.** A test, and the right one. |
| `admit_registry_entry`, `admit_catalog_association`, write scan | 63 CC-6 | Writers stored what readers refuse | **Keep**, as rules in the one gate. If the predicate is a registered rule, the write scan is the only extra. |
| `SHAPE_PRECONDITIONS`, `rule-error:<rule>` findings | 63 CC-3 | Make the gate total | **Keep.** |
| Corpus, generated grid, ratchets, model test, burst property | 63 | Proof | **Keep.** Proof mechanisms, not product concepts. |
| In-memory upload retry, then a durable upload record | 63 CC-10, 18 TL-10 | An upload is an unsaved change | **Merge** to the end form: an upload is a queue record. One mechanism, built once. |
| Accepted history immutable by trigger | 64 CC-11 | "A settled head" needs the database to agree | **Keep.** It is what lets everything else stop re-proving. |
| Replay memo, verification cache, persisted `file_identity` | 64 CC-2, D14 | The Runtime re-verifies history and stored bytes on reads and writes | **Keep as caches**, but they patch re-proving. With immutable history most of the re-proving has nothing left to find; prefer deleting the check to caching its answer. |
| Reply holds ids and a digest, not the document | 64 FS-2 | The reply repeated megabytes | **Keep.** See the composition note in 3.4. |
| Rules declare reads; results kept by revision | 64 FS-3 (conditional) | The delta gate runs every rule twice | **Split.** Storing the head's findings is part of the minimum (concept 8) and should be unconditional. Read-scoped evaluation is an optimization; conditional is right. |
| Replay against the net difference | 64 FS-4 (conditional) | A base 20 commits behind replays 20 entries | **Keep conditional.** |
| One commit at a time per timeline | 64 FS-5 (conditional) | Removes three attempts and `head_busy` | **Promote to unconditional.** It deletes a mechanism and is part of concept 3. |
| Narrow reads declared by each writer, `reads="timeline"` opt-in | 65 ET-1 | Most writers claim the whole timeline | **Merge** into derivation: reads are a change's `before` values plus what the recorder saw. Keep `reads="timeline"` as the one opt-in. Nobody else declares. |
| Selector-declared reads for function commits | 18 TL-13b | Same, for agent code | **Merge** as above: a third way to say what was relied on. |
| Head check every 2 s while idle | 65 ET-2 | A 30 s poll is too slow | **Keep.** It replaces the poll, so the count of ways to learn the head stays at one. |
| Adoption keeps selection, playhead, undo | 65 ET-3 | Adopting a head reset the editor | **Keep**; needs the undo rule (section 1). |
| "Who and what" line | 65 ET-4 | The person should know | **Keep.** Reads stored fields. |
| Bundle keeps request and key | 65 ET-5 | The authoring writer has no outbox | **Merge** into the Agent's one sending path (18 TL-13b says the same). |
| `GESTURE_OPS` table of encoders | 18 TL-5 | Gesture to command | **Keep.** |
| Editor preview per gesture | 18 (existing local edit, demoted) | Instant feedback | **Keep.** An unavoidable second description, correctly made unable to refuse. |
| Runtime copy of `edit-command.schema.json`, sync script, CI drift check, generated App constants | 18 TL-2 | Three repos must agree on command shapes | **Cut the Runtime copy.** Make the command payload opaque to the Runtime, as it is to the queue. See section 5, change 3. |
| CLI verb, generated MCP tool, `timelines ops --json` | 18 TL-13b | Agents send commands | **Keep.** One generated surface. |
| Closed reason list with headlines, uncoded-error ratchet | 18 TL-4 | A refusal says why | **Keep.** |
| Gesture matrix, generator, manifest | 18 TL-15 | Proof | **Keep**, sized to what it finds. |
| Phase 2 alternate view | 18 | Proof that a pack can add an op | **Keep as proof**, but change what it proves (section 3.4). |

---

## 3. Elegance and engineering

### 3.1 Duplicated truths left in the end state

| Fact | Where it is held | Plans' answer |
| --- | --- | --- |
| **What a commit did** | The step's patch, the recorder's writes and reads, and the canonical document, all from the provider; a fourth projection built by the Runtime *[mine]* | None |
| **Whether a declared read still holds** | Agent `_commit_patch.py:332`; Runtime `timeline_commit_auth.py:252` *[mine]*; and the Agent compares a client's submitted reads with its own capture, `commands.py:280-301`, `capture_mismatch` *[Haiku]* | Plan 18 removes the client's copy. The Agent and Runtime pair stays. |
| **Which ops exist** | The Agent registry; op names inside the Runtime's authentication (`doc.patch`, `timeline.inverse`, `list.move`, `list.remove`, `track.create`, `occurrence.fork`, `occurrence.swap-media`) *[mine]*; the Runtime's schema copy | Schema copy generated (18). Authentication untouched. |
| **The command schema** | Agent, Runtime copy, App constants, plus a digest handshake when the provider loads *[mine]* | One owner, two generated copies, drift check. Sound, but three copies of a fact the Runtime need not read. |
| **What an edit means** | Agent handler; editor preview | Preview demoted to disposable. Right. |
| **Undo** | App local stacks; server `timeline.inverse` | Open. |
| **What a writer relied on** | Client-declared reads (65), selector-declared reads (18), recorder-observed reads (existing) | Three forms. Should be one, derived. |
| **The outcome of a failure** | Runtime, where it builds an error; Agent mapping table | Cross-checked by a fixture. Acceptable. |
| **An unsaved upload** | In-memory retry (63), then a queue record (18) | Converges. |

### 3.2 Concepts that exist only to patch other concepts

- **Provider authentication patches a trust boundary that is not there.** The provider is loaded in-process, behind an explicit "trusted `astrid` profile" *[mine]*. The module's own comment says "List operations are Agent semantics. The recorder supplies the complete resulting collection; Runtime only projects that value", and the fix for clip deletion (Runtime #66, `5f74064`) adds a 16-line special case teaching the Runtime one more shape the Agent may record *[mine]*. Each new effect shape needs another.
- **Step-by-step resend** patches all-or-nothing batches.
- **Results kept by revision (FS-3)** patches the delta gate's doubled cost.
- **Replay memo and verification cache** patch re-proving a history that CC-11 makes immutable.
- **Three attempts and `head_busy`** patch validating outside the lock; FS-5 removes the cause.
- **The reply fixture and the fallback decoders** patch two decoders and old Runtimes. Honest, and cheap.

### 3.3 Where App, Agent and Runtime re-derive or re-check the same thing

After all four plans *[mine, from the plan text and the code]*:

- **App:** nothing. No App file builds `reads`, `expect` or `selections`; no encoder can refuse. This is the plans' best result.
- **Agent:** executes the command, records reads and writes, detects clashes by address, runs the rule gate. One place. Good.
- **Runtime:** still validates the command against its schema copy, still re-checks each declared read, still re-projects every effect from the recorder's records, still compares the result with the provider's document, and still knows some ops by name.

So the destination has two layers that hold an idea of what an edit must prove, down from three. Today's evidence came from the pair that remains: "provider list effect lacks a full collection observation" is the Runtime disagreeing with the Agent about the *form* of a correct deletion.

### 3.4 Does Plan 18 compose with 63, 64 and 65?

**With the App side: cleanly.** The queue payload is opaque, so TL-5 swaps a patch for a command and touches nothing else; `sendIntent` is `send`; the parked rule is inherited; rules and ops share one loading question. This is good design.

**With the Runtime: it fights, in three places.**

1. **A pack's op with a new effect shape meets the authentication layer.** Plan 18 states the Runtime "keeps no op table of its own" *[Haiku, from inputs]*. That is true of handlers and false of effects *[mine]*. A composite op built from existing handlers emits only known shapes, so phase 1's proof (`clip.ripple-delete`) passes without touching the hard case, and so can phase 2's.
2. **A pack's op meets the Runtime's schema copy.** The copy is generated at build time and checked for drift in CI (TL-2); a pack registers at run time. TL-1 lists "how the Runtime provider loads pack-registered ops" as an open finding "with a fallback if it cannot" *[mine]*. The central extensibility claim rests on an unsettled question.
3. **Editing together is specified twice.** Plan 65 builds declared narrow reads in the App for element and parameter edits; Plan 18 then forbids any App file from building reads. And the clash rule differs (section 1).

**With Plan 64: a hidden dependency.** A command with no editor preview (any pack op) shows nothing until it is accepted. At four seconds that reads as broken; at under a second it is fine. The plans say Plan 18 "needs nothing from B". For pack ops it needs B.

**A composition the plans miss.** FS-2 (a reply without the document), ET-2 (notice a foreign head), ET-4 (who and what) and TL-5 (adopt the head) all ask the same question: "what changed since the head I hold?" The effect list answers it. One read, "changes since head X", returning each commit's label, author and effects, would serve all four, and the editor would apply effects where it now fetches a whole document. Optional; it is where one representation would pay twice.

---

## 4. Over- and under-engineering

**Over:**

1. **Proof machinery outgrowing the product.** Corpus, generated grid, gesture matrix (12 documents × every gesture × every track), ratchets, AST counts, scans, lints, pinned fixtures, a contract page. Each is defensible. Together they are a second system to maintain, and they prove agreement between layers that a derived design would not need to check.
2. **Plan 18's breadth.** One command layer, plus a unit rename, plus a CLI verb, plus a generated MCP tool, plus an extension SDK rewrite, plus an alternate view. Only the first is the end state; the rest are consumers of it.
3. **Caches in Plan 64** (memo, verification cache, file identity, findings by revision) added where the cheaper move is to stop re-proving what immutable history has settled.

**Under:**

1. **The Agent–Runtime proof boundary is left as it is.** The biggest risk in the set. The end state can pass every one of its own checks and still refuse a valid edit with `invalid_records`, because no check, corpus row or model test in the four plans names that path.
2. **Extensibility is proved only on the easy case.** Composite ops and an App-free view do not show that a pack's own handler, with its own effect shape and schema, is accepted by a Runtime that was not rebuilt.
3. **Undo and the same-thing clash have no single rule.** Both surface exactly when a person and an agent share a timeline, which is the product's premise.

---

## 5. The smallest changes that would make it elegant and minimal

Ranked by impact. All are changes to the stated end state, not new plans.

1. **Add a sixth invariant to Plan 63: the Runtime derives, it does not compare.** The provider returns one thing, an effect list in a closed set of effect kinds, one shape each. The Runtime applies it with a generic applier and stores it as the record; a read is an address, never a value. `step_output`'s per-shape projection, the second read check and the op names in the Runtime go. What the Runtime keeps is what only it can know: identity allocation, revisions, history, keys. Add corpus rows that drive every op through the *Runtime* route, so the grid covers this path. This is the change that closes today's bug class; without it the plans fix the neighbours of the bug.
2. **Make one commit at a time per timeline unconditional** (FS-5 out of stage 2), and store the head's findings with the head (the storing half of FS-3). Both delete mechanism: three attempts, `head_busy` as a race answer, and the doubled rule pass.
3. **Make the command payload opaque to the Runtime.** The Runtime validates the envelope (key, head, command list); the provider validates commands. The Runtime's schema copy, its sync script and the command part of the digest handshake go, and a pack's op needs no Runtime change. This turns Plan 18's open TL-1 finding into a decision.
4. **Reads are derived, never declared.** A change's reads are its `before` values plus what the recorder observed; `reads="timeline"` is the one opt-in. ET-1 becomes "the Agent derives narrow reads for every writer", and the App part of ET-1 and the selector form in Plan 18 are not built.
5. **State one clash rule and one undo rule.** Suggested: a command is re-run on the current head, so a person's later gesture wins and the "who and what" line shows what it replaced; `moved` is for snapshot writers only. Undo of a queued edit removes it from the queue; undo of an accepted edit is `timeline.inverse` of that commit.
6. **Change what phase 2 must prove:** a pack op with its own handler and a new effect shape, accepted by an unmodified Runtime and App. Then the alternate view is optional.

With 1 to 4 the server side matches the App side, and the eight concepts in section 2 are the whole design.

---

## 6. Comparison with the earlier reviews

Read after sections 1 to 5 were written. One wording change was made afterwards and is marked below.

### `fable-commit-proof-fit.md`

**Same hole, found independently.** It also reports that no plan names `timeline_commit_auth.py`, and counts the same 3,432 lines and 344 sites. I agree with its three rules: one record shape per effect kind, reads are addresses and not values, and the Runtime never branches on an op name ("ops are open; effects are closed"). Its "reads are addresses" is sharper than my first wording ("`before` values hold on the head"), and I changed concepts 1 and 4 and change 1 to match: a value a writer saw is a second copy that can only add a way to fail.

**Where I disagree: how far the end state should go.**

- It keeps the three-way comparison and narrows it: the Runtime "projects each effect onto its own base and compares", and the inverse-stage code (about 2,000 lines) is explicitly left alone. That is the right three-day step for Plan 63. It is not the destination. As long as the provider returns a patch, records and a document, and the Runtime checks that they agree, each of the remaining `require` sites can still refuse a valid edit. The end state should say the Runtime applies effects and compares nothing.
- It keeps `invalid_records` as `refused` with "our fault" wording. I agree for now. In the end state that reason should be unreachable from a valid edit, and a test should say so.
- It rejects "the Runtime derives the proof from the op". So do I. My change 1 is per effect kind, not per op, and is the same boundary it draws.

**What it has that I lacked:** the edit-kind matrix sent through the real Runtime route with a pinned request file (its CC-13). That is the proof my change 1 needs, and better specified than my "corpus rows through the Runtime route".

**What I add:** an opaque command payload for the Runtime (change 3), which its "the Runtime checks effects, never ops" implies and does not state; and the observation that pack ops meet both the authenticator and the schema copy.

### `fable-four-questions.md`

- **"Send what you relied on", declared by every writer.** I disagree, as `fable-commit-proof-fit.md` already does. What a writer relied on should be derived by running the change. Declaring is the pattern that failed.
- **One commit at a time per timeline "only after stage 1".** I disagree on placement. It sorts FS-5 as speed work. It is a simplification that deletes the retry loop and `head_busy` as a race answer, and it belongs in the end state whatever stage 1 measures. *[inferred; I did not check what else holds the lock]*
- **"Robustness does not need the intent model."** Agree. But its conclusion that Plan 18 is then "unchanged" misses that Plan 18's re-apply rule and Plan 65's park rule differ for the same clash.
- **The split into four, and the three sentences.** Agree. I would add a fourth sentence: *the server derives, nobody compares.*

### `fable-dependable-saving-check.md`

- **"The centre is right and close to minimal."** Agree for idea A, the editor's.
- **Idea B, "an accepted head is settled", judged sound.** Agree as far as it goes. It settles the head for document rules and for cost. It does not settle what the Agent must hand the Runtime, so idea B is half stated.
- **Drop the ratchets, keep the type and the model test.** Agree, and section 4 extends the same worry to Plan 18's proof machinery.
- **Opaque queue payload as the cheap shaping for extensibility.** Agree; change 3 applies the same idea one layer down.

### `fable-gap-method.md`

No disagreement. It is about finding where the time goes, not about the destination. Its caution that "96% in the provider" includes Runtime port reads called from inside the provider is a reason not to assume the authenticator is free; I did not measure it.

---

## Not checked

- **Nothing was run.**
- **Whether change 1 is feasible as stated.** I read the head of `timeline_commit_auth.py`, `validate_read`, the start of `step_output`, `validate` and the #66 diff, not all 3,432 lines. Part of that module does work only the Runtime can do (physical identities, bindings, materialized shot revisions). How much is that, and how much is comparison, decides whether "apply, don't compare" is a rewrite or a deletion.
- **Whether the Runtime's schema validation would refuse an unknown op today.** I saw the schema copy and per-op argument types; I did not trace the refusal.
- **Serial commits.** That nothing else relies on validating outside the lock.
- **Plan `tasks.md` and `inputs.md` files** were inventoried by Haiku agents; I read the deciding rows only.
- **App code.** Not read by me; the App facts are from the plans and one Haiku pass.
