# Where the "edit refused by commit authentication" fix belongs, and its shape

18 Nov 2026. Read only; nothing was run and nothing was changed except this file.

**Sources.**
- Plans: astrid-dev `origin/plan/63-dependable-saving` at `da5c3265` (Plans 63, 64, 65, 18).
- Code: Runtime `4c18af5` (`release/14/plan-59`, with #66), App `36c3c6f6a` (`release/14/plan-59`), Agent `e2a500072`.
- Labels: **read** = I checked it in the code or plan myself. **reader** = reported by a Haiku reader, not re-read. **unverified** = inferred.
- Case 2's diagnosis came from the coordinator while this was being written. I re-read the Agent check it names and the App fix's file list; the rest of that diagnosis is **peer-reported**.

## Verdict in brief

1. **It fits Plan 63, as three small tasks on the Agent and Runtime track. It is not its own plan, not Plan 18's, and only a slice is Release 14's.**
2. **The proof should be derived in one place, and that place is the Agent, by running the change. It is not the Runtime, and it is not the App.**
   - the Agent alone says what was written, in one record shape per effect kind;
   - a read is an address at a named head, never a value the writer saw; the server looks the value up;
   - the Runtime checks effects, never ops;
   - the App declares no values now, and no reads at all once Plan 18's TL-5 lands.
3. **The matrix is the right test, with a different unit and home than drafted.** Its unit is what the shipped save path sends for a gesture. It is a pinned request file with two tests, one in the App and one in the Runtime, plus one run on a real stack.
4. **Release 14** gets the two fixes (both landed), a one-off sweep of every edit kind on a sandbox timeline, and fixes for what an ordinary session hits (about 2 to 3 days).
5. **Plan 63 goes from about 30 to about 38 days; Plan 65 drops by about 1.** The App critical path stays at 15.5. Nothing is pulled forward from Plan 18; one small piece moves from Plan 65.

## What the code shows

- **No plan names the Runtime's authenticator (read).** `timeline_commit_auth.py` appears zero times in the plan, tasks and inputs files of Plans 63, 64, 65 and 18. It is 3,432 lines with 344 `require(` sites.
- **Every one of those sites refuses with one reason, `invalid_records`, status 422 (read, `:18-21`).** Under Plan 63's four outcomes that is `refused`, so a disagreement between our own layers is shown to the person as their edit being refused.
- **The Runtime does not run edits, by design (read, module docstring):** "it never executes submitted edits. Command execution, conflict detection and inverse construction belong to Agent."
- **Case 1 is two record shapes for one effect kind (read, `:901-915`, `:957-965`).** For a `list.*` effect the Runtime wanted the whole resulting collection. The Agent began recording a removal as one row's clear. #66 added a second accepted shape; it did not replace the first.
- **Case 2 is the App declaring a value the server does not hold.**
  - The Agent raises "declared field read does not match" in `CommitPatch.capture` when a declared field's `state` differs from the value it finds (read, `_commit_patch.py:330-333`, kind `previous_value_mismatch`).
  - A clip move declared the whole asset registry entry as the App held it. The server stores that entry thinner, without `file` or `metadata` (peer-reported).
  - App #308 (`90e4640`) declares only the entry's `duration` (read: the merge title and its four files).
- **The same comparison exists a second time, in the Runtime (read, `:251-252`):** "declared field read differs from its input boundary". So a value the App saw is checked by two layers against two copies of the base.
- **The App hand-builds those reads per gesture, with the value it saw (read).** `hooks/timelineLocalSaveHandoff.ts:558-954` has about a dozen sites that build `{kind: 'field', …, state}` or `{kind: 'collection', …, members, order}`.
- **The Agent already derives reads by running, for named ops (reader).** A handler reads through the recording context (`_recording.py:93-112`), which notes each read. Only the `doc.patch` route needs the writer to declare anything, because the App worked out the result itself.
- **The Runtime holds two views of a list effect (reader, agreeing with what I read).** For a member removal and an occurrence move it works the result out itself. For every other `list.*` it takes the Agent's whole resulting collection as given.
- **The authenticator's own tests use hand-built records (reader).** `_member_removal_case` in `tests/test_timeline_commit_authentication.py:1390-1421` builds Python dicts. None is shaped like an editor request.
- **The App has no list of edit kinds (reader).** `EditCommand.op` is a plain `string`. About 22 op names are written as literals across about 20 files, plus `doc.patch` with five change kinds (`set`, `remove`, `list.insert`, `list.remove`, `list.move`).
- **One gesture has two encodings, and the tested one is not the one that failed.**
  - `tests/e2e/local/clip-delete-command.spec.ts` drives a real Runtime and expects `clip.delete` to be accepted (read).
  - The failing deletion was a `list.remove` effect, which is the `doc.patch` route (unverified: inferred from the message and from `d7efe3c49` touching `_doc_patch.py`).
  - That spec is in neither `playwright.direct.config.ts` nor `playwright.n4-direct.config.ts` (read). I did not check `e2e.yml`.
- **The plumbing for a cross-repository fixture already exists (read).**
  - The App pins Runtime conformance files by hash in `runtime.lock.json`.
  - The Runtime pins an Agent checkout in `tests/astrid-agent.pin`, and `tests/test_timeline_commit_integration.py` commits through the real provider.
  - The App's `direct-journey.yml` starts a real Runtime and Agent at the App's pins.

## 1. Where it fits

**Plan 63.** Three reasons.

- **It is Plan 63's own promise.** The goal line says "nothing is refused or undone". A deletion that can never save breaks it as surely as a burst does.
- **Plan 63's proof is blind to it by design.** The model test uses a scripted `send` and "speaks only of rows and outcomes" (read, CC-5a). That is right for the queue, and it means no Plan 63 test ever sends a real request to a real authenticator. The grid (CC-3, CC-6) runs Agent rules on documents; it does not pass through the Runtime's authenticator either.
- **It reuses Plan 63's machinery.** The pinned fixture is CC-4b's pattern, the documents are CC-7's corpus, and the review is R0.

**Why not the others.**

| Home | Verdict | Why |
| --- | --- | --- |
| Its own plan | No | About 6 days, with no decision of its own and no end state separate from Plan 63's |
| Plan 18 | No | It starts after Plan 63's R0 and the owner's week. TL-15a as written replays Agent ops through `commands.execute` and `validate_final_candidate`, so it would miss this class too |
| Plan 65 | One wording change only | ET-1 is where the reads side is cured (section 2) |
| Plan 64 | No | It is about cost, not agreement |
| Release 14 | A slice | The fixes and a sweep. The structure changes the wire and needs paired pins |

## 2. The shape

### Why not "the Runtime derives the proof from the op"

- **It makes a second implementation of every op.** The Runtime would need each op's meaning to derive what it reads and writes. Two implementations of one meaning is the disease, moved.
- **It closes the door Plan 18 opens.** TL-1 item 5 has packs register ops that run in the provider. A Runtime that derives proofs per op must learn every pack's op.
- **TL-1 does not say it.** TL-1 item 3 is about the App's encoders: they build no `reads`, `expect` or `selections`. It does not move derivation into the Runtime.

### The two cases are the same fault from opposite sides

| | Case 1 | Case 2 |
| --- | --- | --- |
| Who was wrong | The Runtime, too strict | The App, declared too much |
| The fact in dispute | What a removal wrote | What a move read |
| How many layers held their own idea of it | Two (Agent, Runtime) | Three (App, Agent, Runtime) |
| The fix that landed | Add a second accepted shape | Narrow one gesture's declared value |

Both fixes are correct and both leave the cause in place: the next gesture can over-declare, and the next recorder change can miss a shape.

### Should the App declare reads at all?

**No values, ever. No reads at all in the end state.**

- **A declared value can only add a way to fail.** The server holds the document at the head the writer named. A value sent beside the address is a second copy, and the App's copy is not the server's: it is thicker where the App has added local fields. A mismatch at the writer's own base is never a real clash. It is always a misstatement.
- **A real clash needs no value from the writer.** The server compares the address at the writer's base with the same address at the current head. Both are its own.
- **For written fields the patch already says what was relied on.** Every `doc.patch` change carries `before` or `order_before` (reader, `_doc_patch.py:379-400`).
- **So what is left for the App is small:** addresses it relied on and did not write, such as an asset's `duration` for a move. Over-declaring an address costs at most a `moved`; it cannot refuse.
- **In Plan 18 even that goes.** The App sends `{op, select, args}`, the handler runs in the Agent, and the recording context notes what it read.

**This can be done on the server alone.** The Agent and the Runtime stop comparing a declared `state` and treat a read as its address. An older App that still sends `state` is unaffected, so there is no paired pin and no compatibility case. The App's builders are deleted later, by TL-5 and TL-12 as already planned.

### The single contract: one author per fact

**Ops are open; effects are closed.** Anyone may add an op. Every op, whatever it means, is recorded as a list of five effect kinds. The Runtime knows the five and nothing else.

| Fact | One author | The others |
| --- | --- | --- |
| **What was written** | The Agent's recorder, because it runs the op | The Runtime projects each effect onto its own base and compares. The App carries nothing |
| **What was relied on** | The Agent, by running the change (named ops). For `doc.patch`, the patch's own `before` values plus any addresses the writer adds | The server looks up the values at the named head. Nobody sends a value they saw |
| **Whether the document is valid** | The Agent's rule registry (CC-3) | Unchanged |

Three rules follow.

1. **One record shape per effect kind.** A `list.remove` is `{id, before, order_before}` and nothing else is accepted. Today the Runtime accepts two shapes for it (read), and `list.move` on occurrences has its own branch (read, `:948-955`). Each fix in this class must remove a shape, not add a branch.
2. **Reads are addresses, not values.** Case 2 is this rule broken. Two copies can disagree for reasons that are nobody's edit: fields the App adds locally, path normalisation, the `config` mirror, materialised shots. Without the value there is nothing to mismatch.
3. **The Runtime never branches on an op name.** It may branch on an effect kind and on a collection's identity key.

### Does it conflict with anything?

- **The settled head (Plan 63, invariant 4): no.** An effect's `before` is checked against the base, which is delta-shaped already.
- **CC-3's registry: no, and keep them apart.** The registry is the home of document rules. The authenticator checks that a record matches a base. Do not register its 344 sites as rules; the cure for them is fewer shapes, not a registry.
- **ET-1 (Plan 65): it pulls the other way as written, and should be reworded.** ET-1 has the editor declare more ("every record declares the addresses its patch writes", read). More declaring by the App is how case 2 happened. Reword it: the written addresses are derived from the patch on the server, and the editor adds only addresses it relied on and did not write, with no values. The server half of that (a read is an address) moves to Plan 63 as CC-16, because it is a dependability fault today, not a co-editing nicety. ET-1 keeps the narrow default reads for agent function commits and the `atomic` clean-up.
- **TL-1 and TL-5 (Plan 18): it is their first half.** Once reads are derived from the patch, TL-5's check that "no file constructs `reads`" is nearly true before TL-5 starts. A selector resolves to addresses in the Agent, through the same function.

### What stays out

- No fifth outcome. `invalid_records` stays `refused`, so it parks and can be discarded.
- No registry or ratchet for the authenticator's `require` sites.
- No rewrite of the authenticator's inverse-stage code (about 2,000 lines). If rule 1 cannot be met without touching it, stop and leave that to Plan 18's TL-3r.

## 3. The matrix

**Right test, with three changes to the draft.**

### The unit

**A gesture kind × a target kind, encoded by the shipped save path.** Not an op, because one gesture has two encodings and only the untested one failed (above).

- **Gesture kinds:** every entry point the editor has: delete, move, trim, split, duplicate, add media, swap media, set a field, set params, set an element, track create, track label, shot set, the occurrence edits, undo.
- **Target kinds:** a parent clip, a clip inside a shot, a track, a shot occurrence, an element or text clip.
- **Each row asserts three things:**
  1. the commit is accepted;
  2. the accepted document equals the App's own `after` (accepted but different makes the screen snap);
  3. undo is accepted and restores the start.
- **Starting states, because of case 2:** the document as the App holds it, not a raw seed. Two states at least: freshly loaded through the App's real loader, and just after adding media in the same session (when the App's copy of an asset is thickest).
- **Documents:** two seed documents at first, one plain and one with shots. Later, CC-7's corpus heads.
- **Size:** about 40 to 60 rows (my estimate from the reader's op list).

### The home

**One pinned request file, two tests, one live run.** Each repository then catches its own break in its own CI.

| Piece | Repository | What it does |
| --- | --- | --- |
| The list `EDIT_KINDS` and a generator | App | Drives the real handoff (`timelineLocalSaveHandoff` then `localSaveSession`) on the seed document for every row and writes the requests |
| The request file | Runtime `conformance/requests/` | Its home. The App pins it by hash in `runtime.lock.json`, which is the existing mechanism |
| App test | App | The generator's output equals the pinned file. A changed request shape fails here |
| Runtime test | Runtime | Each request, sent through the real pinned Agent provider and the real store, is accepted, matches and undoes. A changed authenticator fails here; a changed Agent recorder fails here at the pin bump |
| The whole list on a real stack, nightly | App `direct-journey` (it already has a nightly schedule and takes a Runtime and an Agent ref) | Every row in a browser against a real Runtime. This is the only run that sees what the App really holds after loading and uploading, which is what case 2 turned on |

- **Why not only a full-stack job in the App:** it is slow, needs tokens for two private repositories, and catches an Agent or Runtime change only when the App's pins move.
- **A known wrinkle (unverified):** requests carry the base head pair. If seeding does not give stable ids, the Runtime test substitutes them at replay. The head pair is not what the test is about.

### Staying complete

- **One list.** `EDIT_KINDS` is a typed table in the App. `EditCommand.op` becomes a union instead of `string`, so a new op literal with no row is a compile error. A scan covers the five `doc.patch` change kinds for each collection the diff mapper can emit.
- **Plan 18 inherits it.** `EDIT_KINDS` is keyed by gesture kind, which is the key set of TL-5's `GESTURE_OPS`. TL-5 adds the encoder column to the same table. TL-15a's manifest already "must contain every key of `GESTURE_OPS`".
- **TL-15a needs one amendment:** its rows end at "accepted by the Runtime's commit route", using this harness, not at `validate_final_candidate`.
- **The batch joins it.** CC-5c's first check (k chained steps in one commit) runs through this harness, with one row of two kinds batched.

## 4. Release 14

**Land now (about 2 to 3 days beyond the diagnosis in flight):**

1. **Runtime #66 and App #308, both landed,** each with its own regression case.
2. **A one-off sweep, about 1 day.** Script every edit kind once on the Release 14 staging stack, on a sandbox timeline, never the timeline the owner views. List every refusal. This is the seed of the matrix, as `localSaveSession.discard.test.ts` was the seed of the model test.
3. **Fix what an ordinary editing session hits, about 1 to 2 days.** The count is unknown until the sweep. The rest become named gaps, by the owner's light-testing rule.

**Already there:** a refused change can be discarded (N3, N4), so this class is survivable today.

**Waits for Plan 63:** the CI matrix and the pinned file, one shape per effect kind, the `op` union, and the server treating a read as an address. The last is server-only and small, but it touches the capture and replay paths I have not read in full, so it should not go into a release under light testing.

## 5. Estimates, and the effect on Plan 63

| Piece | Where | Days | Note |
| --- | --- | --- | --- |
| Sweep and urgent fixes | Release 14 | 2 to 3 | Not in Plan 63's total |
| **CC-13** every edit kind is accepted (list, generator from the App's real loaded state, pinned file, two tests, the nightly run) | Plan 63, Agent and Runtime track | 3.5 | First, beside CC-5a and CC-7. Needs nothing |
| **CC-14** close what CC-13 shows red | Plan 63 | 2 (1 to 4) | Lower if Release 14's sweep ran first. Re-estimate from the red count |
| **CC-15** one record shape per effect kind | Plan 63 | 1.5 | Half a day first to check the inverse-stage code does not depend on the second shape; stop if it does |
| `invalid_records` gets a named row in the outcome table and a plain "our fault, not your edit" wording | Inside CC-4 and CC-4b | 0 | A row, not a task |
| **CC-16** a read is an address: the Agent's capture and the Runtime's `validate_read` stop comparing a declared value | Plan 63, moved from ET-1 | 1.5 | Half a day first on chained records and the sequential capture; server only, no paired pin |
| ET-1, reworded | Plan 65 | 2 (was 3) | Its server half is CC-16 |
| TL-15a reuses the harness; TL-5 extends the list | Plan 18 | about 1 less | |

- **Plan 63: about 30 becomes about 38** (37 to 40): 3.5 + 2 + 1.5 + 1.5. The Agent and Runtime track goes from 12.5 to about 21. The App critical path stays 15.5, and the tracks still do not depend on each other.
- **Plan 65: about 11.5 becomes about 10.5.**
- **Order:** CC-13 starts on day one with CC-5a and CC-7. CC-14, CC-15 and CC-16 follow it. R0 gains two negatives: a new op literal with no row fails, and a request whose declared value is wrong is still accepted.
- **New end-state check P0-7:** every row of the edit-kind matrix is accepted, matches and undoes; one accepted record shape per effect kind; no refusal anywhere compares a value the writer declared.

**Against the main thread's draft.**

| Draft | Judgment |
| --- | --- |
| (a) matrix, 2 to 3 days | Agree at 3, with the unit and home above |
| (b) fixes, 2 to 4 days | Agree; split between Release 14 and CC-14 |
| (c) pull "the Runtime derives the proof from the op" into Plan 63, 5 to 8 days | **Half right.** Right that the proof must be derived in one place. Wrong place: the Agent derives it by running the change, and the Runtime checks. That costs 3 days here (CC-15 and CC-16), not 5 to 8. TL-1 and TL-5 stay in Plan 18 at their size |

## Not checked

- **Nothing was run.** No request was sent and no fix was tried.
- **Case 2's detail.** That the server's registry entry is thinner, and that the move declared the whole entry, are peer-reported. I read the Agent check and the App fix's title and file list only.
- **Which head the Agent's check compares against.** I read the comparison, not the code that picks the boundary. If it also runs against the current head on a replay, it doubles as clash detection there, and CC-16 must replace that with the base-to-head comparison rather than only delete it.
- **That dropping the declared value is safe in every path.** Chained records and the sequential capture (`validate_sequential_capture`, about 300 lines) were not read. CC-16 has a half-day first check for this.
- **Whether one member-scoped shape works for `list.insert` and non-occurrence `list.move`.** CC-15's first check.
- **Whether the owner's deletion took the `doc.patch` route.** Inferred, not traced.
- **Whether `e2e.yml` runs `clip-delete-command.spec.ts`.**
- **The day counts** are judgment on the plans' own figures, not bottom-up.
