# Near-instant commits: review of the draft plan

18 Nov 2026. Read-only. Six Haiku readers gathered facts; I re-read the load-bearing code myself (Runtime `519b404`, Agent `22ff36923`, App `b38e29d06`). Nothing was run. "Reported" marks a reader's finding I did not open. "Inferred" marks a conclusion from reading code that no one has measured.

## Verdict

**The plan removes the right two costs but stops one level short of the root, and three of its eight items need changing.** R1 is sound and is the single largest win. R3's "same set" claim is not provable as written. A1 already exists in the Runtime, so the 400's trigger is still unknown. Under 1 s is not shown by the numbers: the plan gets from ~187 s to low seconds, and nobody has measured the residue.

Top changes:

1. **R1: keep, tighten.** Reuse the Runtime's existing verify-once-per-file-identity map; it must survive memo clears; bound the stat cost too.
2. **R3: change.** Don't write a second resolver and call it equivalent. Make it the kernel's one collect pass, gated by the same delta helper as R5 and R6, with the old probe kept as a test oracle.
3. **A1: drop.** Same-key requests already wait. Return the "inputs changed" condition as retryable, and log what changed.
4. **R2: change.** The scan is O(history) for every commit that creates something. Memoising within a commit leaves that.
5. **R5 + R6: merge** into one rule: every whole-head check reports findings through `split_findings`, and readers never raise.
6. **Proof: add scaling counts** (same counts at 3 and 30 history entries) and "a refusal or an unrelated write causes no re-hash".

## A. Root

**Deepest cause I can support: an accepted head is not treated as a fact.** Every request re-proves the already-accepted base from scratch against today's code, and each layer does it its own way.

- **Runtime.** Bytes it verified a moment ago are re-read and re-hashed at every read scope. `history_read_scope` runs three full passes, all `final=True` (`timeline_commit_store.py:587-590`), over every object the process has consumed (`:438`), which includes whole media files (`:1509`, via `cas.read`, which hashes once itself at `cas.py:188-193`, then `_confirm_object` hashes again). The SQLite side is already trusted on a stat tuple plus `data_version` (`:285-301`, `:364-380`). CAS is the only part re-proved by content each time.
- **Agent.** `_load` has no memo (`commit.py:432-440`). `_check_reservations` walks the whole ancestry and loads each revision about three times (`:1012`, `:1013`, `:1017`, `:1021`): 3N+1 loads for N history entries. N was 3 in the profile, hence 10. It runs only when the commit creates an identity (`:762-763`), so a drop or split pays it and a move does not. **The plan's "history length is not the cause" is wrong for the future: this term grows by three closure loads per edit.**
- **Legacy probes.** `_legacy_declaration_is_resolvable` re-proves, per declaration and per commit, a fact about the base alone (`_commit_timing_validation.py:262-265` passes `baseline`; nothing from the candidate enters).
- **Whole-head rules (R5, R6).** The same habit as correctness, not cost: the rule re-judges what was already accepted.

On the candidate root in the brief: "once per revision, not per load" is right but not enough for the probes. **Each commit creates a new base revision, so a cache keyed by base revision misses on every ordinary edit.** It helps only retries, refused commits and dry-run-then-accept. The probes need fewer passes, not a cache.

**One change that removes most of the time: R1.** About 190 of 280 profiled seconds, plus the 8 s history GET and the mutex hold behind it. No single change removes the rest; the probes are a separate 80 s.

**Addendum (R6).** Yes, it belongs with R5. `registry_selections` is a reader that raises (`native_media_admission.py:37-39`) and is called on the unchanged base (`publish.py:42`, `authoring_commit.py:145`, `native_media_admission.py:107`). The one place already exists: `_preexisting.split_findings`, whose docstring states the contract ("the signature is everything the finding depends on"). Two rules prevent the next one:

- a whole-head rule reports `{key: signature}` and only *introduced* findings block;
- a function that reads the base never raises on its content.

The corpus invariant from my 17 Nov review ("every corpus head accepts an unrelated one-field commit and a duplicate") is the test that enforces both. Add a half association and a `gap_after_s` clip to the corpus.

## Deeper issue

**Yes. All five are one cause seen from different sides: nothing in the stack treats "accepted" as settled.** The stack has no notion of a fact that was proved once and can be relied on, so each layer re-derives it, and when a re-derivation disagrees there is no outcome except refusal.

| Symptom | How it follows |
|---|---|
| 3-minute commits | Bytes, closures, history and legacy proofs are re-proved per read, per load and per declaration |
| Whole-head refusals (R5, R6, #842's four rules) | Rules re-judge the accepted head against today's code |
| Equality bridge (#839) | The editor re-derives the result and demands it equal the UI's, instead of adopting the accepted head |
| Stuck conflict and retry states | A disagreement, even a transient one, is recorded as a permanent `rejected` that nothing removes (`commitOutbox.ts:519-526`; `resolveRejected` is reached only for `too_large`, `localSaveSession.ts:160-175`) |
| Half catalog association | A writer admitted it; a reader later refuses it on every read |

It got through for the reason I gave on 17 Nov, extended by one clause: **no test holds a document with a history, and none holds one with size.**

**Is it logged?** In pieces, never as one cause.

| Where | What it says | Covers |
|---|---|---|
| astrid-dev #842 (closed) | "A commit or duplicate is refused only for problems it introduces or touches." | The validation side, as a principle. Closed after four rules; R5 and R6 show the principle did not become a mechanism. |
| #852 (open) | "The editor sends the intent and adopts the head that comes back." Proposed home: Plan 18. | The editor side. |
| #826 (open) | "A commit pays for the whole history." Also: "Every database write clears the cross-request verification cache." | The cost side, partly. It covers history paging, not the reservation scan, the probes or per-scope re-hashing. |
| #846 (open) | "every commit refusal clears the replay memo" | Cost after a refusal. |
| #732 (open, blocked on the owner) | "A rejected timeline save … leaves the editor stuck with no way out." | The stuck state. |
| #847 (open) | First start fails with "accepted commit inputs changed during verification"; cause not identified. | The same 400, a second trigger. |
| Plan 54, `plan.md:47` | "Verify at a trust boundary once; inside a job, carry the digest." | The exact principle, written for generation jobs. Not applied to timelines. |
| Plan 18 | Queued, unowned, "Waiting on: scope agreement". Goal: "reliable timeline editing primitives". | Nothing yet. It is the nominal home. |
| Plans 39, 55, 62; vision gaps | Reported: no timeline commit budget, no baseline rule, no document corpus. | Miss. |
| `releases/12/decisions.md:100-103` | A refusal blocked every later save; decided "No sticky `captureFailure`". Per-change rejection rejected "as too large". | The stuck state, fixed once at one site. |

Not found anywhere: the half association, a per-commit cost expectation, the two-tab clash, the legacy probes' cost.

**Recommendation: both of the first two options, no new plan.**

- **Fix now, in Release 14's Plan 59 branches:** the time (R1, R2, R3), the delta gate (R5 + R6), the retryable condition and the dischargeable rejection. These unblock the owner's timeline.
- **Extend Plan 18** with a first phase, because it is waiting on scope, #852 already points there, and a third home would split one cause again. Scope paragraph:

> **Phase 0, the commit contract.** An accepted head is a fact. (1) A commit's work is bounded by the change plus one pass over the document, and is independent of history length; stated as counts and held by a test. (2) Every rule that reads the whole head reports findings through one delta gate; reading the base never refuses. (3) The editor sends intent and adopts the accepted head (#852). (4) A refusal applies to one change and can always be discharged (#732). (5) One corpus of real long-lived documents, in astrid-agent, runs the invariant: every head accepts an unrelated one-field commit and a duplicate, at the stated counts. Closes #826, #846, #852, #732; reopens #842 as the mechanism.

## B. Elegance, item by item

| Item | Call | Why |
|---|---|---|
| R1 | **Keep, tighten** | The Runtime already has this: `service.py:6031-6036` keeps `_verified_cas_objects[digest] = file_identity(...)`, "Verify once per immutable file identity". Use that one map, not a second. It must not be cleared by `clear_replay_memo`, or every write and every refusal makes it cold again (#826, #846). |
| R2 | **Change** | A per-ref memo cannot share bundles: `scan` mutates the loaded state (`commit.py:928-984`, reported). Memoise the verified document and build a fresh bundle per use. That still leaves N+1 loads. The real fix is to keep the reserved-identity set per publication, extended by one entry per accept, since ancestry is immutable. |
| R3 | **Change** | See C. |
| R4 | **Drop for now** | Identity-keyed memoisation is defeated by the deep copies around it. Most digests go with R2 and R3. Re-profile first. |
| R5 | **Merge with R6** | One rule, one helper. Signing by the declaration's own value matches the helper's contract: the kernel never evaluates `gap_after_s`, so the finding depends on nothing else. |
| A1 | **Drop** | Already built: `CommitExecutionCoordinator._execution` holds a lock per `(scope, idempotency_key)` and the waiter returns the replay (`timeline_commit_execution.py:462-485`, `:529-543`). The App's outbox also sends one request at a time with one key (`commitOutbox.ts:465-484`, reported). |
| A2 | **Split** | Classification belongs in the Runtime (below). Keep the App half: a rejected head must be dischargeable. |
| A3 | **Keep, simplify** | Timing fields already commit through `onValueCommitted` (`ClipPanelBody.tsx:350-405`); Position X only has `onChange` (`:437-439`). Use the one existing path. No new debounce. |

**The second path that should be one.** The plan treats the 400 as an App classification problem, matched on a message string. The condition is "the store moved while I was reading", which is a retryable busy state, not a protocol violation (`ProtocolError` is status 400, `errors.py:83-85`). The App already retries `head_busy` and `runtime_unavailable` (`client.ts:324`). So: the Runtime returns this condition with that retryable reason, and the App needs no new rule.

**Trigger still unproven.** With A1 already in place, the plan's story for the 400 ("an overlapping same-key verification") cannot be right. Within one scope the store mutex is held, so an in-process request cannot interleave. Candidates are a second writer (the owner's tab, a media import on the mutex-exempt binary route) or a WAL stat change. Log which component of the version tuple moved at each raise site (`:200`, `:433`, `:592`). #847 is the same error at first start.

## C. Safety

**R1 is sound, with four conditions.**

- **Key on `file_identity`** (`cas.py:19-20`: dev, inode, size, `mtime_ns`, `ctime_ns`), taken by `fstat` before and after hashing, as `_verify_open_stream` does (`cas.py:122-134`). `ctime` cannot be set back by an ordinary user, so an in-place rewrite with a restored `mtime` is still caught.
- **Objects are never replaced by the store.** Publication is a no-replace hard link (`cas.py:164`); a replaced file has a new inode.
- **What is given up:** silent on-disk corruption that changes no metadata is found at first verification per process, not on every read. That matches how the database itself is trusted, so it is not the weakest link.
- **What the re-hash guarded:** the commit messages name cache-baseline races and "an external writer cannot be absorbed into the baseline" (`09a27ef`, `6a9a98f`, reported). None names tampering or partial writes. A stat compare at every scope boundary keeps the external-writer guarantee.

**R3 is not shown to be equivalent, and cannot be by construction.**

- The probe's answer is the outcome of a full `validate_candidate_timing` on the base with one declaration set, classified by error-message markers (`:181-191`, `:228-231`) with a physical-context retry (`:232-242`). A declaration's resolved start feeds the dependency graph and whole-document checks such as "clip starts before its occurrence". "Resolve each declaration against a compiled context" is a second implementation of that rule. This is the pattern my 17 Nov review named.
- **Possible existing fault, inferred, not run.** The probe passes no baseline, so `_drop_preexisting_unsupported` does nothing. On a base that carries `gap_after_s` (Almost Ready does), each probe would raise "unsupported timing declaration" (`_timing_evaluators.py:515-517`), which has no marker, so the probe returns "resolvable". If so, the 68 full probes on this timeline compute a constant and grant no exemptions. Test this before designing R3; it changes what "same set" means.
- **Recommended shape.** Give `evaluate` a collect mode that reports each legacy declaration that fails, for the base and the candidate (two passes), then let `split_findings` decide which are pre-existing. That is one mechanism for R3, R5 and R6. Keep the old probe in the tests as an oracle on the corpus. Where the sets differ, that is an owner decision, not a silent change.
- **Safe now:** memoise the probe by (base revision id, key, field, value). It changes nothing semantically and stops a refused commit paying 85 s again.

**R5 and R6 do not weaken validation** provided the key and signature follow the helper's contract. A new or changed declaration or association still blocks.

## D. "Near instant"

From the profiled add-media commit (280 s, about 1.5× real):

| Cost | Profiled | After the plan |
|---|---|---|
| CAS re-verification | ~190 s | Hashing goes. What stays: 59 passes × ~1,100 objects of open plus `fstat`. `cas.open` makes about 15 `open` calls per object (16,620 for 1,108, history profile), about 0.25 s a pass. **Up to ~15 s profiled unless the confirm is one cheap stat or the pass count falls** (inferred). |
| Legacy probes | ~80 s | One or two passes, about 1.4 s profiled each (81.6 − 80.1) |
| Loads | in the above | Each `_load` still deep-copies, re-digests and re-opens the bundle: about 0.16 s profiled, × (N+1) |
| Accept, writes, the rest | ~10–18 s | Unmeasured. Partly CAS. |

- **Plausible after the plan as drafted: low seconds.** Under 1 s is not supported by any number in the profile.
- **Needed for under 1 s:** the cheap confirm; the reservation set per publication; one validation pass; then re-profile and remove whole-document deep copies and digests in what remains.
- **Two floors outside the Runtime.** The editor debounces saves by 500 ms (`useTimelinePersistence.ts:47`, reported), so "well under a second" must be defined as the acknowledgement after the POST. A cold Runtime still hashes every media object once, about 8 s on this timeline, growing with media bytes.
- **Polling** should not stay "filed". Each GET holds the store mutex; after R1 it is cheap, but #826's "every database write clears the verification cache" means a polling tab can keep the Runtime cold. Verify with the count test below.

## E. Proof

The count-based proofs are the right kind and are not yet sufficient. Add:

1. **Scaling, without a clock.** Run the same commit on the corpus at 3 and at 30 history entries, and with one and with two timelines loaded. Loads, hashes, opens and timing passes must be equal. This is the test that would have caught all of it.
2. **Count opens and stats, not only hashes**, or R1 passes while 15 s remains.
3. **Persistence of trust.** After a refused commit and after an unrelated database write, the next commit performs zero re-hashes.
4. **R1 negatives.** Same-size rewrite, replaced file and restored `mtime` are each re-hashed and refused.
5. **R3 differential.** New exemption set equals the old probe's on every corpus head, with the `gap_after_s` case stated explicitly.
6. **App.** A rejected head can be discarded and the next edit saves, including after a reload.

Live wall time recorded as evidence, not as a gate, is right.

## Recommended plan

| # | Repo | Change | Ships |
|---|---|---|---|
| 1 | Runtime | CAS confirm by file identity through the existing `_verified_cas_objects` map; survives memo clears; one cheap stat per confirm; non-outermost scopes pass `final=False` | First |
| 2 | Agent | Memoise probe results per base revision now. Test the `gap_after_s` probe fault. Then the collect pass plus `split_findings` | First (memo, test); then |
| 3 | Agent | One delta gate: unsupported declarations signed by value (R5), associations (R6), readers never raise; corpus gains both cases | First |
| 4 | Agent | Verified-document memo per commit; reserved set per publication | First (memo); then |
| 5 | Runtime | "Inputs changed" returned with a retryable reason; log the moved component | First |
| 6 | App | Rejected head is dischargeable from both buttons (#732); Position fields use `onValueCommitted` | Second |
| 7 | All | Proofs 1–6; re-profile; then decide R4 and the last second | With each |
| 8 | astrid-dev | Extend Plan 18 with Phase 0; link #826, #846, #852, #732, #847; reopen #842 | Now |

Dropped: A1 (exists), R4 (until re-profiled), the message-string classification in A2.

## Not checked

- No change was prototyped or measured. Every "after" figure is arithmetic on the profile.
- How the conflict card opens after a `rejected` outcome: the reader could not trace it (the card is set only by `handleConflictExhausted`). The plan's App fix should start by reproducing it.
- The 707 pull requests in astrid-dev were not searched, only the 161 issues.
- The history commits behind the probe after `2ad707b7a` (`89c700ade`, `6d190daec`) were not diffed.
