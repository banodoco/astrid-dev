# Plan 18 Phase 0 (the commit contract): independent review

18 Nov 2026. Read-only. Reviewed the astrid-dev branch `plan/18-phase-0-commit-contract` at **`35f26b2b`**, which is `8e1ce0f3`, then `1b4e654e`, then `35f26b2b`, on top of `bd535a5d`. I read all five files in `plans/18-timeline-editing/` at that head, the five evidence files in this folder, and the code:

- Agent `6468e38f3` (`task/plan59-shot-trim`).
- Runtime `9be54d5`.
- App `36c3c6f6a`, plus `release/14/rejected-discharge` at `88045a78c`.
- The in-flight Release 14 worktrees `wt-commit-loads`, `wt-legacy-probes` and `runtime-commit-cost`. Their changes are uncommitted; I read the diffs.

Three Haiku readers did the legwork: a CC task list, a CC/TL overlap check, and a citation sample. I re-read every claim I use below. GitHub issue states could not be checked because the API was rate-limited.

## Verdict

**Merge with edits.** The diagnosis is right, and most of the contract is the right shape:

- one delta gate, which already exists as `split_findings`;
- counts, not clocks;
- one corpus in the Agent;
- typed reasons;
- writers checked against readers.

But three of the six mechanisms still depend on discipline at exactly the place the next instance will appear:

- The rule gate is enforced by a function-name scan, while 65 inline `_fail(` sites sit in `validate_final_candidate`.
- The bounded-work test has only a history axis, and the 80 s probe cost was per declaration, not per history entry.
- Every "only falls" or "cannot shrink" number can be raised by editing it.

Of the three latest edits:

- **Edit 5:** keep it, but it needs a boundary to be true.
- **Edit 6:** strike it. It reaches into phase 1.
- **Edit 7:** keep it, but it contradicts the code on `retryable`.

CC-5's smaller outbox records also carry an unstated dependency on phase 1's adopt model.

## Elegance first

| Question | Answer |
| --- | --- |
| One rule per concept, one path? | Mostly. There is one gate, one corpus and one reason list. Exceptions: (1) five separate hand-rolled ratchets (CC-1 golden, CC-7 manifest, CC-8, TL-4's uncoded `CommandError(`, TL-15a manifest) with no shared mechanism; (2) edit 6 merges two concepts, rules and ops, into a third one, a door that takes a kind; (3) CC-4 builds a Runtime copy "generated from the Agent checkout" one phase before TL-2 builds the schema sync, so there would be two sync scripts. |
| Deletes more than it adds? | Not yet, though it could. These deletions are available and not claimed: the "Resolve retained local saves" throw (`localSaveSession.ts:364` on `rejected-discharge`); "Outbox has a rejected prefix" (`commitOutbox.ts:496`); the `before` document and its equality check (`localSaveSession.ts:371`, an equality bridge inside the outbox); `registry_selections`' raise (`native_media_admission.py:39`); the four hand-built heads. Name them as deletions, not as states that tests prove unreachable. |
| Generated, not hand-listed? | Partly. The source scan matches names and keeps a hand-written exemption list. The grid speaks of "rows" to add. CC-8 keeps a per-site table with line numbers that will move. Each of these can be generated from the registry and the manifest instead. |
| Would an agent extending Astrid do the right thing? | **No, for the most likely extension.** An agent adding an invariant will copy what it sees. `validation.py` has 65 `_fail(` calls and 6 `_check_*`/`_validate_*` functions, so the agent writes a 66th inline `_fail`. The name scan does not see it, and the next whole-head refusal is born. Required edit 2 fixes this. |

**Edit 5: the registry is `validate_final_candidate`'s one rule home. Keep it.** It is the right unification, and it makes TL-13a's "every invariant lives once" concrete. As written, though, "no second list" is false on day one: `validate_final_candidate` (`validation.py:713` onward) is an imperative run of `_fail` calls. Some are shape checks; others judge legacy content directly, for example `config.registry` "does not match parent.registry" and `config.clips` "does not match parent.clips". The plan must say which `_fail` sites stay as shape preconditions and turn the rest into rules (edit 2).

**Edit 6: one `_registry.py` `register(kind=rule|op)` door that TL-3r calls. Strike it.** Four reasons:

- Rules and ops are two concepts with different shapes: `findings(document) -> {key: signature}` against `(name, parameters, handler, intent, singleton)`. A kind-discriminated door does not remove either concept; it adds a third.
- In phase 0 the `op` kind has no caller, so it is speculative code.
- It fixes `register_operation`'s shape before TL-1 item 5 ("the registry design") and RS1 have decided it.
- It invites pack-registered rules before anyone knows whether the Runtime provider process loads pack registrations. TL-1 item 5 is open on exactly this point, and it applies to rules as much as to ops. A pack rule the Runtime does not load means the single writer validates with a different rule set from the CLI's dry run: two meanings of "valid".

Phase 0 needs built-in rules only. The rule for packs belongs in TL-1.

**Edit 7: one closed refusal list, owned by the Agent, with the Runtime copy generated. Keep it, and fix three things.**

- Making the Agent the owner matches TL-2, and the Runtime already pins the Agent. State the cost: a new Runtime store reason now needs an Agent change and a pin bump.
- **"`retryable` derives from `status`" is false for the Runtime's members.** `refused()` (`timeline_commit_port.py:89-92`) gives every store refusal `details.status: "refused"`. Release 14's in-flight `HeadBusyError` (`runtime-commit-cost`, `errors.py`) is also `"refused"`, and it is the one reason a client retries. `stale_head` is `"refused"` and rebases; `too_large` is `"refused"` and final. So each entry in the list must declare its own `retryable`.
- `inputs_changed` would be a second name for one condition. The in-flight `commit-cost` work already answers "inputs changed" as `head_busy` (its contract text: "the one refusal a client retries").

## 1. Root: does Phase 0 remove the cause?

It turns the cause into mechanisms for (a), (d) and (f), and partly for (b) and (e). (c) is honestly held only by a ratchet until phase 1. These would still get through:

1. **A new invariant written as an inline `_fail(` in `validate_final_candidate`, or a raise in an op handler that reads the base.** The scan matches only `_check_*`/`validate_*` function names. `_timing_evaluators.py` has 54 raise sites of its own.
2. **A legacy shape that is not in the corpus.** The grid tests only known shapes. Nothing makes "a function that reads the base never raises" true by construction.
3. **A per-declaration or per-shot loop.** The legacy probes were O(declarations × document): 268 probes and 69 compiles, with only 3 history entries. Their cost does not change between 3 and 30 history entries, so P0-1's equality passes them. Only the golden would catch them, and a golden can be raised.
4. **A new CAS read path that hashes or opens outside the counted function.** If the counters are hooks at today's call sites, a new path bypasses them.
5. **A pull request that raises a golden or drops a manifest shape.** "May only fall" has no enforcement.
6. **A Runtime refusal raised outside the list.** Today "accepted commit object changed during verification" (`timeline_commit_store.py:459`) is a bare `ProtocolError` 400. Nothing in CC-4 forces every commit-path raise through a list member.
7. **A writer that bypasses `admit_*`.** CC-6 says the function is "the only way" but has no check that it is.

Required edits 2 to 5 and 8 close all seven.

## 2. Over-engineering and duplication

- **Edit 6's shared door:** above.
- **CC-8:** the per-site table, with each site's retiring task, rots as Release 14 and TL-1 move lines; TL-1 re-inventories anyway. Keep two counts (`refuse(` calls; `reads`/`expect`/`selections` constructions) and drop the table.
- **CC-7's App pin subset check** conflicts with TL-15a ("no App copy of the matrix, no digest sync"). The App tests that read that pin (`p1FeasibilityCorpus.test.ts`, `p1RawHandoffCorpus.test.ts`) are deleted in TL-12. Drop CC-7's App half.
- **CC-6's own every-op × every-head closure test** is the CC-3 grid harness with ops varied. Use one harness and one test file.
- **Counters as production "hooks"** (`commit.py`, counter hooks only): test spies on the lowest primitive need no production code, and cannot be bypassed by a new call site (edit 3).
- **Duplication with Release 14 that the table misses:**
  - `release/14/rejected-discharge` `88045a78c` already does two things: "stale_head … rebase the retained chain onto the latest head and resend it (bounded)" and "Recover several retained owners in turn instead of refusing when more than one has work". So CC-4 part (3) and CC-5's two-session bullet are build work that is already done.
  - `release/14/save-rejections` (#720, merged `ba20e7da`) is not in the table.
  - Agent `release/14/edit-refusals` (#842 uniform baseline, open, `d5f90a4b`) is not in the table, yet CC-3 builds directly on it.
  - CC-1 says what did not land "moves into CC-2", but the App items belong in CC-4 and CC-5.
- **Release 14's state:** on 18 Nov, `release/14/commit-cost`, `commit-loads` and `legacy-probes` have no commits beyond their cut points; the work is uncommitted in worktrees. CC-2's 4 days assumes they land. State the contingency: if they do not, CC-2 takes on the whole of near-instant Rev 2.

## 3. Missing items and the deferrals

- **Outbox whole documents (now in CC-5).** The direction is right, but the plan does not say what replaces the stored documents. In the code (`rejected-discharge`):
  - `LocalSave` carries `before` and `after` (`localSaveSession.ts:18-19`);
  - `:371` refuses an append unless `save.before` equals the session document;
  - on reload, `:335` rebuilds the display from the last intent's `after`.

  Without documents, reload recovery has to show the head, re-send and adopt. That is TL-5's model arriving early. Decide it in CC-5 (edit 6).
- **Two sessions on one origin.** Already on `rejected-discharge`; CC-4 and CC-5 should only test it. **The two-tab draft slot deferral** leaves statement P3 ("you can always get out") possibly false until phase 1: the live check said two tabs "block each other". I did not trace how the slot is keyed after `88045a78c`. Edit 6 makes this a test in CC-5, with a small fix if it fails, rather than a deferral.
- **Cold-start hashing.** The deferral reason is weaker than written. Trust persisted against the full `file_identity` (dev, inode, size, `mtime_ns`, `ctime_ns`) gives up only corruption that changes no metadata, across restarts. Within a process that is already given up (the 18 Nov review, section C). It is a trust-model choice, so the owner decides, but it needs a D-number with a recommendation, not "file an issue". It can also be bounded by count now. #847 (first start) lives here (edit 10).
- **Polling.** Deferring the rate is justified. But P0-1 tests only "zero hashes", and the residue the review measured was opens and stats: about 15 `open` calls per object, up to about 15 s. plan.md promises the mutex hold is "counted, history-independent"; no check holds it (edit 3).
- **Snapshot size:** deferral fine.

## 4. Tests

The count-based approach is the right kind and complies with the owner's no-clock rule. The 3-against-30 equality and the one-against-two-timelines equality compare the code with itself, so editing a number cannot game them. That is the strongest test in the plan. It is not sufficient:

- It has no axis for declarations or shots (gap 3 above).
- The goldens and manifests hold over time only if something compares them with the base branch.
- Counters at call sites can be bypassed.
- `_check_history_objects` iterates `_history_state["objects"]`, a set that grows with process lifetime. Both history depths must be built in the same kind of process as the measured commit.

Edits 3 and 4 close these gaps. Prefer absolute formulas, such as "closure loads per attempt ≤ 2", to golden numbers wherever the target is known. A formula is the contract itself and needs no ratchet.

## 5. Could a newcomer start CC-7 and CC-1?

Nearly. Missing pieces:

- **History depth is a harness property, not a fixture.** In the Agent it comes from `DetachedRealm`/`DetachedPort` in `tests/sdk/test_timeline_commit_provider.py:68`/`:114`, calling `realm.call` N times. In the Runtime it comes from `commit(service, body, key=…)` N times (`tests/test_timeline_commit_closure_growth.py`). "One built at 3 and at 30 history entries" reads like a fixture property.
- **How the Runtime reads the corpus:** through its pinned Agent checkout (`tests/astrid-agent.pin`). This is not stated.
- **Generator name:** "under `scripts/`" names no file.
- **The golden:** where it lives and who sets its first value (CC-1).
- **What "an unrelated database write" is:** for example, a media ingest on another timeline.
- **Small fixes:**
  - CC-2's "the R1 negatives above" refers to a name used only in the private Rev 2 plan.
  - `timeline_duplicate.py` is at `astrid/sdk/timeline_duplicate.py`, not under `astrid/sdk/timeline/`.
  - `_rules.py` is not marked new.
  - The handoff has 68 `refuse(` calls on App `36c3c6f6a`, not 69 (TL-1 re-counts anyway).
- **Ordering contradicts itself.** "These six are true before phase 1 starts" and the critical path "CC-7, CC-3, R0, then TL-1" disagree with TL-1's Depends cell (CC-3, CC-4, CC-7). CC-4 depends on CC-1 but uses no counter. With that dependency the real critical path is CC-7, CC-1, CC-4, CC-5, R0, which is 13 days. Without it, the path is CC-7, CC-1, CC-2, R0, which is 11 days. Either way it is not 9.

## Required edits

1. **Strike edit 6's shared door.**
   - **CC-3:** replace the sentences from "It is also the one extension surface" to "TL-3r builds no parallel mechanism" with: "Rules register through `register_rule(name, findings)` in `_rules.py` (new). In phase 0 only built-in rules register; there is no pack hook. How a pack registers rules, and whether rules and ops share an owner namespace, is TL-1 item 5, under one constraint: a pack's rules run under this gate and in the Runtime provider process, or not at all."
   - **TL-3r:** delete the "thin caller of the shared registry CC-3 builds (`_registry.py`)" clause.
   - **TL-1 item 5:** add "and pack-registered rules (the same loading question)".
   - **plan.md (b):** delete "and the one door through which ops and rules register (TL-3r is a caller)".
   - **D13:** amend to match.
2. **Make edit 5 true, with a gate that is total and a scan that does not depend on names (CC-3, P0-2).** Add to CC-3:
   - "`validate_final_candidate` keeps as direct `_fail` calls only the shape preconditions named in `_rules.SHAPE_PRECONDITIONS` (the candidate or a required container is not an object; not finite JSON). Every other `_fail`/`raise` reachable from it becomes a registered rule's finding."
   - "The gate runs each rule on base and candidate. An exception from a rule becomes a finding keyed `rule-error:<rule>`, signed by exception type and path, so a failure already present in the base cannot block. The grid asserts zero rule errors on the corpus."
   - "Replace the `_check_*`/`validate_*` name scan with an AST count of `_fail(` and `raise` sites in the validation modules outside registered rules and `SHAPE_PRECONDITIONS`. It is a ratchet (edit 4): 65 `_fail(` in `validation.py` at Agent `6468e38f3`."
   - "The grid is generated as registry × manifest; there are no rows to add."
3. **Give bounded work a second axis, primitive counters and polling counts (CC-1, CC-2, P0-1).**
   - Add the axis: "on heads with 5 and 50 legacy declarations and with 7 and 30 shots, timing passes, closure loads, whole-document copies and whole-document digests are equal."
   - Add counters `document_copies` and `document_digests`.
   - State the known targets as formulas in the test: closure loads per attempt ≤ 2; timing passes ≤ 2; CAS hashes on a warm store = objects newly written; CAS opens ≤ 1 per object read.
   - Counters are test spies on the single primitive, not production hooks: the port's `revision_closure`, `compile_timing`, bundle `deepcopy`/`_digest`, `os.open`/`os.stat` under the CAS root, and `hashlib.sha256` in the CAS read path. Add a scan that the Runtime hashes CAS bytes in one function only.
   - Extend P0-1 and `test_timeline_polling_costs.py`: per-GET opens and stats are equal at 3 and 30 entries.
4. **One ratchet mechanism.** Every "only falls" or "cannot shrink" value in the plan lives in one `ratchets.json` per repository: CC-1 golden (if any remains after edit 3), CC-3 site count, CC-7 manifest set, CC-8 counts, TL-4 uncoded `CommandError(`, TL-15a manifest. One CI step fails if any value rises, or a set loses a member, against the merge-base's file. No test hand-checks its own ratchet. Add this to CC-1 and reference it from the other rows.
5. **Fix edit 7 (CC-4, TL-4, TL-13a, inputs ruling 7 and G7).**
   - Replace "`retryable` derives from `status`" with "each list entry declares `{reason, status, retryable}`; Runtime store refusals are all `details.status: "refused"` (`timeline_commit_port.py:89-92`), so status cannot carry it."
   - Replace `inputs_changed` with Release 14's `head_busy`.
   - Add the integrity refusal ("accepted commit object changed during verification", `timeline_commit_store.py:459`) as a non-retryable member.
   - Add a test that every refusal raised on the commit path names a list member.
   - One sync script: CC-4 creates the Runtime's `scripts/sync-from-agent.py` and its CI check; TL-2 adds the schema to that same script.
6. **CC-5 says what replaces the stored documents, and deletes rather than proves unreachable.**
   - "Delete `LocalSave.before` and the `:371` equality check; continuity is by intent basis (`OutboxBasis {after: id}`). Keep at most one `after` per owner, for the reload display; TL-5 deletes it."
   - "Delete the 'Resolve retained local saves' and 'Outbox has a rejected prefix' throws."
   - Proof: "whole documents stored per owner ≤ 1, independent of the number of pending intents."
   - Add "two tabs on one timeline" to the refuse–edit–discard–reload table. If they still block each other, key the draft slot by owner id in CC-5, and remove the two-tab row from Deferred.
7. **Cite what Release 14 already does.**
   - CC-4 part (3) and CC-5's two-session bullet become "landed by `rejected-discharge` `88045a78c`; CC-4/CC-5 add the tests only".
   - Add `release/14/save-rejections` (`ba20e7da`, #720) and Agent `release/14/edit-refusals` (`d5f90a4b`, #842; CC-3 builds on it) to the plan.md table.
   - CC-1: "moves into the CC task in the table's third column", not "into CC-2".
   - State CC-2's contingency if the three uncommitted Release 14 branches do not land.
8. **CC-6: a proof that holds, and enforcement.**
   - Replace "validated with `baseline=None`, introduced findings only", which is contradictory on legacy heads, with: "through CC-3's grid harness, for every op in `commands.operations()` plus the duplicate path on every corpus head, findings(result) − findings(head) is empty; on the clean heads, validation without a baseline is clean."
   - Add "a scan fails on a write to the parent registry or a catalog association outside `admit_*`".
   - Correct "one function" to "two functions in one module".
   - Delete `test_writers_pass_readers.py` as a separate harness.
9. **Ordering.**
   - TL-1 (design only) keeps CC-3, CC-4 and CC-7. Add R0 to RS1's Depends.
   - Change "true before phase 1 starts" to "true before RS1 closes".
   - Change CC-4's dependency from CC-1 to "Release 14 published".
   - Restate the critical path. With CC-4 unblocked it is CC-7, CC-1, CC-2, R0 = 11 days, not "CC-7, CC-3, R0 = 9". Make the header and the table agree (23 or 23.5).
10. **Cold start becomes owner decision D14**, not "file an issue". Recommended: persist verified `file_identity` in the store database. What is given up is metadata-preserving corruption across restarts, which a process already gives up. Meanwhile, CC-2 bounds it by count: a cold start hashes each object of the requested closure once, and only those objects. Link #847.
11. **CC-7 startable and Agent-only.**
    - Name the generator `scripts/gen_long_lived_corpus.py`.
    - Say that history depth is applied by the harnesses (`DetachedRealm.call` ×N; Runtime `commit(...)` ×N), and that the Runtime reads the corpus through its pinned Agent checkout.
    - Drop the App pin subset check, and make P0-6 Agent-only.
    - Fix the `timeline_duplicate.py` path, mark `_rules.py` new, and change CC-2's "R1 negatives above" to "CC-1's negatives".
12. **CC-8: counts only.** Keep the two counts under edit 4. Drop the per-site table with retiring tasks; TL-1 owns that inventory.

## Optional suggestions

- **Generated signatures.** A rule declares the fields it reads, and the gate derives the signature from them. This makes the whole-row-signature bug (#387's `gap_after_s`) impossible to write rather than something a test catches.
- **A state-exit test for the outbox and session.** Enumerate the states; each has an exit by a user action. This makes "no sticky state" structural.
- **Label (c) "held in phase 0, delivered in phase 1"** in plan.md's six statements, so the owner does not read P0-3 as the equality bridge being fixed.
- **R0:** if D9 puts phase 0 and phase 1 in the same release, fold R0 into RS1. Otherwise keep it.
- **Re-verify the issue ledger's states.** The API was rate-limited here.
