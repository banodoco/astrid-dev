# Independent rereview — strengthened clip invariant port

**Verdict: prior coverage findings R1, R2 and R3 are CLOSED for this exact strengthened patch. Overall clip-port disposition remains HOLD for the unresolved replay/history contract and incomplete atomic proof.** No new blocking coverage finding was identified in this bounded rereview. This is not acceptance of the two failing tests, quarantine removal, publication approval, or formal RS1. **Formal RS1 remains 0/1.**

Reviewed Runtime HEAD `2777051c06c3d15e14d3e8d13de26b19f875c4bc` and the current uncommitted `tests/test_timeline_clip_replacement.py` change. That is the only dirty product file. Saved `candidate.patch` exactly matches current `git diff`, independently verified SHA-256 `5ff1ff46ad12d17e4059c6ca38cf186980896db34fc481da374d51a9d49489f5`. References below use the strengthened working file's line numbers. I compared it with the original Git HEAD legacy assertions, my prior `../k1b-clip-contract/partial-review.md`, and the saved partial/strengthening/final evidence.

No tests, collection, product edits, commits, contract decisions or remote actions were performed. This review is my sole written artifact.

## Disposition of prior findings

### R1 — populated sibling/effects/registry metadata: CLOSED

The atomic helper now commits an explicit guarded `doc.patch` before the media swap (lines 291–314). It creates:

- Target effects exactly `[{"id": "grade"}]`.
- A separate same-owner text sibling, `untouched`, with its own authored fields and text.
- Populated registry metadata exactly `{"keep": True}`.

These are inserted through `_native_commit`, not by forging an accepted Runtime document or bypassing product validation. The fixture asserts all three values in the returned canonical document before capturing the swap. The sibling's corrected `at=0, hold=1` lies within the five-second occurrence; moving the old legacy fixture's out-of-occurrence position is a valid canonical-fixture adaptation because the invariant is that the unrelated sibling remains unchanged.

The swap then calls the existing full-payload assertion at line 325 and explicitly reasserts all three populated values at 327–329. `_assert_native_swap_result` still changes only the expected target asset and new registry binding, including exact verified duration, then compares the entire internal payload. Thus the original old-asset binding, target timing and unrelated populated data remain covered. Existing parent/shot/receipt/event checks remain intact. Receipt/event baseline counts are taken after the separate fixture-seeding commit, so the subsequent `+1` checks correctly measure the swap alone.

The final raw failures occur later, at line **339**, after corruption of the retained old CAS object. Both atomic case traces establish execution reached that unchanged assertion. The populated preconditions, full-payload preservation, explicit sibling/effects/metadata assertions and immediate swap receipt/event-count checks therefore executed successfully before the failure. I do not infer this coverage from the intermediate proof, where fixture seeding failed earlier.

### R2 — precise negative refusal causes: CLOSED

Cross-project refusal (427–437) now requires exact `NotFoundError`, exact managed-project-selection message, `not_found` and 404. It retains the full DB snapshot comparison and adds full timeline-head equality. This identifies the ownership boundary instead of accepting arbitrary Runtime failure.

Wrong-stream refusal (509–521) now requires the exact `media swap preserves media kind` message plus all of:

- Public `code == "validation_error"`, HTTP status 422.
- Semantic `details["status"] == "invalid"`.
- Exact semantic reason and detail code `unsupported_media`.

Both too-short and authored-end cases (525–540) similarly require the exact `source window differs from hold or exceeds media` message, validation_error/422, invalid status, and `unsupported_timing` as both reason and detail code. Durations remain separately 1 and 3.5 against the authored window ending at 4, retaining the distinction between insufficient span and failure to reach the authored endpoint. Full DB/head no-write comparisons remain.

Using `pytest.raises(RuntimeErrorBase)` for the latter cases is now appropriate: `runtime_protocol/timeline_commit_port.py:99–103` deliberately constructs that class and assigns the public code/status dynamically. The following exact code/status/reason/message assertions eliminate the prior overly broad acceptance. Requiring a Python `ValidationError` subclass would contradict this adapter even when its public refusal contract is correct. The intermediate class-expectation failures and their correction are transparently retained. All these negative tests and their legacy wrappers pass in the final proof.

### R3 — genuine intervening edit and exact retained head: CLOSED

The clean replay helper (582–614) now makes a substantive `hold` change from 3 to 2. It explicitly checks both old and intervening values, captures the intervening accepted document and full head, and binds the captured head's publication ID to the intervening receipt.

After close/reopen, it requires the original exact retry envelope, full equality to the saved intervening head, equality of the stored revision closure to the entire intervening canonical document, and retained hold 2. Existing exact receipt/event counts remain. This is stronger and more precise than the former head-inequality check and faithfully replaces the legacy requirement that the later edit remain selected after restart/replay. Both the native case and legacy wrapper pass in the final proof. This clean-history result does not resolve the different corrupt-history retry rule.

## Independent evidence verification

I parsed the intermediate and final XMLs independently and matched each exact case inventory against its own raw pytest `PASSED`/`FAILED` node lines. The initial partial-port XML, intermediate strengthening XML, and final XML all have the same **27 unique node IDs**. I checked the recorded exit files separately.

| Evidence | Result | Exit | Interpretation |
| --- | --- | --- | --- |
| Initial strengthening `after.xml` / `after-a.log` | 19 passed, 8 failed | 1 | Retained intermediate fixture/class mistakes; not passing evidence for R1 or exact semantic refusal assertions. |
| Corrected `final.xml` / `final-a.log` | 25 passed, 2 failed | 1 | R1 preservation prefix executes; R2/R3 tests pass; old-history replay collision remains red. |
| Legacy-authority `after-b.log` | 9 passed, 71 deselected | 0 | Focused unchanged retired-route refusal controls pass; not the full legacy-authority module. |

Both final failures are precisely `test_native_clip_swap_is_atomic_cas_and_exactly_replayable` and its retained legacy wrapper. Their XML messages identify `CommitOutcomeUnknown`, and their failure trace includes line 339, the exact request/key retry after old-CAS corruption. Neither is a new preservation-fixture or refusal-signature failure. The recorded 25 passed/2 failed total is therefore accurate; it is not a green result.

The low-severity invalid-escape warning from my prior review is also corrected: the malformed-byte message regex is now a raw string. Its exact message/code/status and Runtime DB/head checks remain.

## Preserved limits and remaining hold

All ten legacy names remain, with no integration/default-off decorators. The existing modern integration marks remain; registry, mirror, workflow, product implementation and pin files are unchanged. No hidden selection reduction was introduced by the strengthening. The generic visual-audio case remains the explicitly authorized Agent capture/precommit check; its surrounding Runtime snapshot is not evidence of Runtime-side refusal, and the worker assessment accurately states that limitation. The previously accepted malformed-byte admission, selected-source corruption, authenticated HTTP route, exact merged status, duration and distinct-object fixture ports remain intact.

Nine legacy IDs now pass with their intended current-contract checks. For the atomic ID, only the prefix through successful replacement/preservation and immediate single-acceptance counts is established. The failed line 339 does **not** establish exact replay under corrupt retained history. The subsequent no-duplicate counts, CAS restoration, same-key mismatch and stale-request tail at lines 340–363 remain present but **unexecuted** in these two final results. No acceptance is inferred for that tail.

The unresolved owner guarantee remains exactly as described in `../k1b-replay-contract/assessment.md`. This review neither prefers a 503 refusal nor permits bypassing retained-history verification to force successful replay. Quarantine removal, guard completion and whole-port publication remain held. Closing the three test-coverage findings improves the owner's reviewable candidate; it does not decide the product contract or make K1b complete.
