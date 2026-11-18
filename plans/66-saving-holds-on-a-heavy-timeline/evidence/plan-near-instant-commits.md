# Plan: near-instant saves on long-lived timelines

## Rev 2, after Fable's review (`fable-near-instant-review.md`), main-thread decisions

I re-read three claims in the code before deciding. Each holds:
- `service.py:6031-6036` keeps `_verified_cas_objects`, which the commit store doesn't use.
- `timeline_commit_execution.py:462-485` holds a lock per idempotency key.
- `commit.py:1005-1021` loads each history entry's boundary on every creating commit.

| Draft item | Decision | Branch |
|---|---|---|
| R1 CAS re-hash | **Keep, tightened.** One verify-once map by file identity, which survives memo clears and DB writes. A confirm is one stat. Inner scopes don't re-verify. Proof by count (hashes, opens, stats), at 3 and at 30 history entries. | runtime `release/14/commit-cost` |
| A1 same-key wait | **Drop.** It already exists. The 400 instead returns a retryable reason the App already retries, and the Runtime logs which component moved. | runtime `release/14/commit-cost` |
| R2 loads | **Change.** Memoise the verified document per commit, with a fresh bundle per use. Memoise the reserved identities per accepted revision, so each commit scans only new history. | agent `release/14/commit-loads` |
| R3 legacy probes | **Change.** First test whether the probes are a constant on bases with `gap_after_s`. Then one collect pass in the evaluator (base and candidate), judged by `split_findings`, with the old probe kept as a test oracle. If the sets differ, that's an owner decision, not a silent change. | agent `release/14/legacy-probes` |
| R5 + R6 | **Merge into one delta gate.** R6 is done in #393. R5 signs an unsupported declaration by its own value. | agent `release/14/legacy-probes` |
| R4 digests | **Drop until a re-profile.** | — |
| A2 | **Split.** Classification moves to the Runtime (above). The App makes a rejected change dischargeable from both buttons (#732). | app `release/14/rejected-discharge` |
| A3 | **Keep, simplified.** Position fields use the existing `onValueCommitted`. No new debounce. | app `release/14/rejected-discharge` |
| Deeper issue | "Nothing treats an accepted head as settled." Fable proposes extending Plan 18 with a "Phase 0, the commit contract", rather than a new plan. **Offered to the owner, not started.** | — |

After the fixes, re-profile on a clone, then rebuild :2400 and record wall times as evidence. Under 1 s isn't shown yet. "Low seconds" is the honest expectation until the re-profile.

---

# Draft (rev 1, kept for the record)

18 Nov 2026. Owner bar: "this should be near instant". A single editor gesture commit (move, trim, drop and so on) on "Almost Ready" should land in well under a second. Today it takes 176–187 s.

## Evidence

- **Live check:** `plan-review/live-check-almost-ready.md`. Each save takes 2–3 min. The discovery proxy cuts at 60 s (503), the outbox retries with the same key, and an overlapping verification returns 400 `protocol_error: accepted commit inputs changed during verification`. The App classes that as permanent `rejected`, and the tab sticks on "This timeline changed somewhere else"; neither button clears it. Inspector fields commit on every keystroke. Two tabs on one origin share the draft slot and block each other.
- **Profile:** `plan-review/sonnet-commit-profile.md`. An uncontended `clip.add-media` takes 187 s, so polling is not the cause. History has 3 items, so history length is not the cause. The cost is repeated work over one ~1 MB base (8 records, a 7-shot closure):
  - **CAS re-verification, ~190 of 280 profiled seconds.** The Agent loads the base 11 times (`commit.py:432 _load` via `_check_reservations :730`, `boundary :767`). Each `revision_closure` read opens its own `history_read_scope`, and `_check_history_objects` re-reads and re-hashes every consumed CAS object (~1,100). That's 59 passes, 32,686 `_confirm_object` calls and 23,268 physical reads (`runtime_protocol/timeline_commit_store.py:435/441/568/617`, `timeline_commit_port.py:217/282`). A GET history read pays it once (8–9 s) while holding `store._mutex` (`server.py:1553`), so each tab's ~110 req/min polling saturates the Runtime.
  - **Legacy timing probes, ~80 s.** `_commit_timing_validation._legacy_exemptions` (`:247`), added by `2ad707b7a` ("gate legacy timing exemptions by baseline validity", 23 Oct), proves each unchanged `on`/`until` declaration is unresolvable in the base before exempting it. Each of the 268 proofs deep-copies the whole bundle, clears every other `on`/`until`, and runs a nested full `validate_candidate_timing`: 69 compiles, 45 s of `deepcopy`.
  - **Canonical-JSON digests, ~29 s** (overlapping the above). There are 39,686 `authoring_bundle._digest` calls and 61,636 `json.dumps` calls.
- **A separate refusal:** moving a VO clip that carries a legacy `gap_after_s` is refused (`unsupported timing declaration ('parent','','vo-N19-0').gap_after_s`). #387's unsupported-declaration signature is the whole clip row minus `params` (`_commit_timing_validation.py:~489-503`). So any move "touches" an inert declaration the kernel never evaluates.

## Principle

A commit costs O(change) plus at most one pass over the document, never O(declarations × document) or O(loads × objects). Integrity and validation semantics stay exactly as they are; only repeated work goes.

## Changes

| # | Repo | Change | Removes |
|---|---|---|---|
| R1 | Runtime | Verify each CAS object once per process while its file is unchanged. Keep a verified set keyed by object id and file identity (inode, size, `mtime_ns`), consulted by `_confirm_object` and `_read_object`. A changed file is re-hashed as today. This matches the existing stat-based version tuple (`timeline_commit_store.py:350-366`). | ~190 s per commit; 8 s → ms per history GET, and with it the mutex hold time under polling |
| R2 | Agent | Load each revision closure once per commit: memoise `_load` / `revision_closure` by ref within one `commit()` call. | 10 of 11 loads, plus their deepcopies and digests |
| R3 | Agent | Prove legacy exemptions in one pass. Compile the baseline once with every `on`/`until` cleared, then resolve each unchanged declaration against that compiled context. Return the same set as today's per-declaration probes. No per-declaration deepcopy or full validation. | ~80 s |
| R4 | Agent | Memoise `_digest` / `_canonical_json` of immutable payloads (revision payloads, shot and internal timelines) by identity within a commit. | most of the 39k digests |
| R5 | Agent | Sign an unsupported declaration by its own value only, not the whole row, so moving or editing a clip with an unchanged inert declaration is allowed. A new or changed declaration still refuses. | the VO-move refusal |
| A1 | Runtime | A same-idempotency-key request that arrives while that key is still executing waits for it and returns its result, rather than verifying again. | the overlapping-retry 400 |
| A2 | App | Classify `protocol_error: accepted commit inputs changed during verification` as retryable (re-read and re-verify). Make "Keep my changes" and "Use latest version" always leave the conflict state. | the unrecoverable stuck tab |
| A3 | App | Inspector fields commit at the end of an edit (blur, Enter or a short debounce), not on every keystroke. | commit storms |

**Filed, not in this fix:**
- the editor's ~110 req/min polling (cheap after R1);
- the two-tab draft-slot clash;
- the proxy's 60 s cut, which is moot once commits are fast;
- the per-revision ~1 MB snapshot, which is a storage format question.

## Proof

There are no wall-clock gates in tests, per the owner's rule. Use deterministic counts instead:
- **Runtime test:** a commit and a history read on a corpus-sized timeline confirm each CAS object at most once per process while files are unchanged, and a changed file is still re-hashed and refused.
- **Agent test:** one commit performs one closure load per ref, at most two timing compiles, and an exemption set identical to the old probe's on the real-shape corpus (doc-a with its closure). A move of a clip with an unchanged `gap_after_s` is accepted, and a changed one refused.
- **App test:** the `protocol_error` path recovers, and both conflict buttons leave the state.
- **Live:** re-run the browser check on :2400 and record each gesture's wall time as evidence. The target is under 1 s per gesture, with no banner and no 503.

## Order and routing

Ship R1, R2, R3, R5 and A1 first: they're independent and remove the time. A2, A3 and R4 follow in the same Release 14 fix branches (`release/14/<topic>` per repo). The editor goes into astrid-app's plan-59 branch, and the Agent and Runtime into their plan-59 branches. Then rebuild :2400.

## Open questions for the reviewer

1. Is R1's stat-keyed verified set sound, or should it be one verification scope per commit? What did the per-read re-hash protect against?
2. Is R3 truly equivalent to the per-declaration probe? Do declarations interact, and is the evaluator's fallback (`_physical_shot_context`) preserved?
3. Is there a deeper root, so that the Agent shouldn't need the closure loaded 11 times, or legacy proofs per commit, at all? For example, should the proof be cached per base revision, since the base is immutable?
4. Is anything here over-engineered, or missing for "near instant"?
