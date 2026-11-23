# Inputs — One acceptor (fast saving)

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked whether to split the save work into stability, speed, multi-edit robustness and extensibility; the main thread accepted the four-plan structure, and **on 18 November 2026 the owner accepted the final recommendations** (Release 15; a speed target of **300 ms with no conditional stage**, [D19](../63-dependable-saving/inputs.md#owner-decisions); the others are Plan 63's). This plan is queued and starts on her go. Next: the owner says go and answers D14; the scope PR records the answers here; only then does the plan become `Accepted`.

**Prior art:** This is the cost half of Plan 18's former Phase 0, moved to Plan 63 on 18 November 2026 and then carved out into its own plan (CC-1, CC-2, CC-9, CC-11). Sources: the reviews and profiles of 17 and 18 November held by the Release 14 Lead (`fable-near-instant-review.md`, `plan-near-instant-commits.md` Rev 2, `near-instant-facts.md`, `sonnet-commit-profile.md`, `sonnet-commit-profile-r14.md`, `fable-four-questions.md` section 3); they are private and not committed, so what matters is restated here as shapes and counts. Nothing here copies content from the owner's timeline.

- *The measured shape.* One timeline with shots, about 8 records and a closure of 7 shots, about 1 MB per revision and about 1,100 distinct stored objects. An uncontended add-media commit took 187 seconds (176 live); profiled, 280 seconds, of which about 190 were CAS re-verification (59 history read passes, 32,686 confirmations, 23,268 physical reads, the Agent loading the base 11 times) and about 80 were legacy timing probes. The reservation scan (2 + 3N closure loads per attempt) grows by three loads per edit. The editor polls about 110 requests a minute per tab; a history GET took 8 to 9 seconds while holding the store mutex.
- The Release 14 profile (Agent `458d9d51`, Runtime `d725811`, 18 November, on the owner's timeline cloned): the Runtime commit is about 9 s idle (was 187 s, about 21 times faster), 67% of it in `_legacy_exemptions` through `_reference_basis` (400 calls, each deep-copying the shot clips and source documents; 25.6M `deepcopy` calls). CAS re-hashing is gone (about 0.4 s). History reads are 0.07 to 0.2 s warm. **An import does wait on a commit:** 5.0 to 6.7 s behind `store._mutex` (idle 0.1 s), and a commit that overlaps an import takes 22 to 26 s against 9 s sequential (mechanism unproven). So a save in progress does delay an upload, but the failure itself was the cut connection, not the wait. The fix of the 67% is in Release 14; CC-2 starts from the profile. The import wait is what Release 14 Runtime #62 and #65 addressed; CC-2's proof re-measures it.
- *Landed on Release 14 since that profile, not measured:* Agent #400 (`6b8780669`: the legacy pass builds its bases once; about 3 s inferred, which is 33% of 9 s), Runtime #62 (keep verified history across unrelated writes so an import never forces a re-walk) and Runtime #63 (one reply writer, health off the mutex, commit timing at INFO), plus the two earlier cost fixes (187 s to 9 s, measured), N5, N6, N10 and N11. **Their effect is not measured; FS-1 measures it.**
- *Never measured by anyone:* the time from a gesture ending in the editor to the accept; the browser's write per edit; the size of the document and of the reply.
- *The bisection, run 1* (coordinator-reported, measured on an APFS realm clone at the Release 14 pins, median of warm one-clip nudges; run 2, with no history, dry run, skipping the validator and the reader check, and a cProfile run, is not in): **3.74 s on Almost Ready against 0.22 s on a one-clip timeline on the same stack; `validate_final_candidate` about 2.2 s (about 60%); everything else that follows the document about 1.3 s (my subtraction; not yet split).** Twelve commits of the same nudge cost 4,086 to 4,399 ms, a 7% spread (`fable-diagnosis-check.md`). Until run 2 is in, "60%" is one measurement.

**Where the time goes today, and what makes each step cost the change** (from the independent check; sizes in [tasks.md](tasks.md)):

| Step | Scales with today | What makes it cost the change | State | Size |
| --- | --- | --- | --- | --- |
| Wait before sending | A fixed 500 ms, plus every earlier edit's commit (`useTimelinePersistence.ts:47`) | Send at once when idle; one batch waiting | [Plan 63](../63-dependable-saving/plan.md) | there |
| The browser's record | About three whole documents per edit, plus a recovery snapshot in a second database | The record is the patch; one display copy per timeline | Plan 63 CC-5b | there |
| The request | The change: one `doc.patch` and the base ids | already so | done | 0 |
| The legacy timing pass | The document times the number of declarations: 400 deep-copying calls, 67% (measured) | Built once per bundle (the pass still runs on every commit) | **landed** (#400), unmeasured | re-measure (FS-1) |
| Timing compile and evaluate; the validator | `validate_final_candidate` is about 2.2 s, about 60% of 3.74 s (bisection run 1, measured); the older profile put compile and evaluate at 15% | Validate only what the effects touch, against the head's stored findings | new | FS-3a, 1.5 days; FS-3b, 4.5 days |
| The Runtime's check of the answer | It re-projects every effect from the recorder's records and compares the result with the provider's: about 91 of 340 refusal sites and 940 lines (one Haiku reader's classification; about 158 sites are identity and binding work and stay, 63 check shape, 28 ordering and coverage) | The Runtime applies the effect list and compares nothing the provider already computed | new | FS-6, 5 days (3 to 8) |
| Serialising and hashing | The document, many times: 9,585 `json.dumps` calls (9%) and 1,797 digests (measured) | Once per commit; an unchanged child keeps its digest | CC-2 | here |
| The history check | The history: the ancestry walk under `_check_reservations` (6% at 8 entries, measured; suspected to grow as the square on long histories, not constructed) | Accepted history is immutable, so the head is trusted and nothing is walked | partly landed (#62); CC-2, CC-11 | here |
| Replay over a moved head | The number of commits since the writer's base, two whole-document loads each (`_commit_patch.py:885-887`; not measured) | Replay against the net difference | new, conditional | FS-4, 2 days |
| Losing the race at accept | The whole validation again, up to three times (`commit.py:1427`, `:1552`) | One commit at a time per timeline, in arrival order; the three attempts and `head_busy` are deleted | new | FS-5, 2 days |
| The store's writes | The document (a new revision row holds the whole payload) | Leave it; all of SQLite is under 0.1 s (measured) | — | 0 |
| Steps that follow the history or the number of commits (all reported, none measured) | see CC-1 | Each becomes a counter at 300 entries; fix only the ones that go red | new counters | in CC-1, CC-2 |
| The reply | The document: every reply carries the canonical document (`localSaveSession.ts:297`) | The reply is ids and a digest | new | FS-2, 1.5 days |
| Waiting on a lock | An import waited the length of the commit's history walk (5 to 7 s, measured) | Reads and imports do not take the commit's lock | landed (#62, #63), unmeasured | CC-9, 1 day |

**Approach:** Measure from the editor first (FS-0, FS-1); then make the proof proportional to the edit, in order: store the head's findings with the head (FS-3a), validate only what the effects touch (FS-3b), one commit at a time (FS-5), keep the verified base by immutable revision id and make history immutable (CC-2, CC-11), and let the Runtime apply the effect list and re-compare nothing the provider already computed (FS-6, sized by a one-day shadow-applier experiment). The two-stage split is dropped: the bisection shows the cost follows the document and 60% is one stage, so validating only what a change touches is the plan, not an option. Alternatives rejected: tuning; trimming repeats alone (it cannot reach a second when one stage is 2.2 s and runs once); a faster language, a second process, an "accept now, validate later" reply (a refusal must stay an answer to the request); a cache keyed by base revision (every ordinary edit creates a new base, so it only helps retries); a clock gate (the owner forbids it; the proof is counts, with the measured numbers as evidence); preferring a cache to deleting a re-check once history is immutable.

**Challenge:** Reviewed: the independent four-questions check (`fable-four-questions.md`, 18 November 2026, held by the Release 14 Lead; read-only, nothing built or run) gave the stages, the arithmetic and the honest limit, and accepted by the main thread. Its own caveats: the stage estimates scale profiled seconds by 9 ÷ 28.8, which is rough because a profiler slows call-heavy code more than the rest; `lookup.py:332` and the evaluate cost, the remaining server time after the landed fixes and the browser's write per edit are unmeasured. Next: a further reviewer may read it against the code before the owner's answers. **The final recommendations** (`fable-final-recommendations.md`, 18 November 2026, with `fable-commit-proof-fit.md` and `fable-end-state-review.md`; accepted by the owner) made this plan "one acceptor": FS-3a, FS-3b and FS-5 unconditional, FS-6 new (about 91 re-check sites and 940 lines of the authenticator, one Haiku reader's classification), FS-0 new, and the first experiment (the shadow applier) as FS-6's first task. Not checked: the authenticator classification and the lock facts are Haiku readers'; the bisection's run 1 (3.74 s, 0.22 s, about 2.2 s in the validator) was reported by the coordinator and its run 2 is not in; the 1.3 s remainder and the 1.5 s after FS-3b are subtraction; whether the shadow applier can use the stored records as they are (derived writes and materialised shots may need more than a generic apply).

**Proof and limits:** Completion is the list in [plan.md](plan.md#completion). Limits: nothing here was built or run; the sizes are the independent check's judgment on the plan's own figures, not a bottom-up estimate; stage 1's arithmetic reaches only 1.5 to 2 s.

**Review rounds:** Pending — one round at the end (it changes the commit path and removes a class of checks), alongside Plan 63's R0 for the shared corpus. Next: the owner confirms.

**Run start:** Pending — no run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, what needs her go, and the advisor session.

### Issue ledger

| Issue | State now | This plan | How |
| --- | --- | --- | --- |
| [#826](https://github.com/banodoco/astrid-dev/issues/826) history reads pay for the whole history; every write clears the verification cache | open | closes | CC-1, CC-2, check FS-C1 (the verification-cost part is already on the Runtime's `p59/revision-listing-perf`) |
| [#846](https://github.com/banodoco/astrid-dev/issues/846) every refusal clears the replay memo | open | closes | CC-2, check FS-C1 (zero re-hashes after a refusal) |

### Deferred

| Item | Decision | Reason |
| --- | --- | --- |
| The editor's poll rate (about 110 requests a minute per tab) | Deferred; the cost is bounded by CC-2 | After CC-2 a GET does no hashing and clears no trust, proven by count. Lowering the rate needs the editor to adopt the head it saves (Plan 18's TL-5) or a push (Plan 76's nice-to-have) |
| The roughly 1 MB snapshot stored per revision | Deferred; file an issue | The contract bounds work, not disk. Delta storage is a storage-format change with a migration |
| The residue under one second | Decided on FS-1's numbers | "Low seconds" is the honest expectation until measured. The editor's 500 ms save debounce is a separate floor (Plan 63 deletes it) |
| Waveform peaks stored beside the object | Deferred | N6 fetches each object once; storing derived peaks is a separate storage question |
| The two proxy hops of the local install | Deferred | Each is a second mechanism around a cause N5 and N6 remove; proxy limits, connection pooling and a longer proxy timeout are not built |
| One object reader and one URL builder | Deferred; file an issue | No incident needs the refactor; the GET-count test catches a returned bulk download |
| Metadata reads other than object and health sharing the commit's mutex | Deferred | #62, #63 and N10 address the import and health waits; CC-2 re-measures |

### Absorbed by Plan 77's save run (23 November 2026)

The owner had the cheap parts of this plan done now, in [Plan 77's save run](../77-saving-holds-on-a-heavy-timeline/tasks.md), after an independent Astra critique of a "Plan 75 lite" proposal (held by the save run's orchestrator, session_011EzfW2o5WfJcvHwr8fSDzC). Taken there: FS-0 (stage spans and size fields, on the save run's timing sink), FS-1 (timing from the editor), a narrow CC-1 (copy and compare counts equal at 3, 30 and 300 entries), CC-11 (accepted history immutable, with detection of an already corrupted store), and the verified-base part of CC-2. The critique's advice, kept here: wait for the installed measurement after the save run's copy and compare removal before funding anything else; defer FS-5 until real contention appears and FS-2 until the reply measurably costs; FS-3a, FS-5 and FS-2 are not standalone as written (they need Plan 63's CC-3, CC-4 and CC-5b); FS-3b and FS-6 stay here. What remains of this plan is re-estimated from the save run's final numbers.

## Owner decisions

Decision ids keep the numbers they had in [Plan 18](../18-timeline-editing/inputs.md#owner-decisions) so references stay valid. **D9 (which release) is [Plan 63's](../63-dependable-saving/inputs.md#owner-decisions): one decision for the four plans, decided 18 November 2026: Release 15, with this plan running in parallel from the same day.** D19 (the 300 ms target, no conditional stage) is decided there too. The one decision that is this plan's:

**D14 — Open (owner): persist verified trust across restarts (cold start).** Recommended: persist each verified object's `file_identity` (dev, inode, size, `mtime_ns`, `ctime_ns`) in the store database, so a restart does not re-hash every media object (about 8 s on one timeline, 2.2 GB on this realm, growing with media bytes; [#847](https://github.com/banodoco/astrid-dev/issues/847) first start lives here). It is the largest uncovered cost: every restart re-hashes. What is given up is corruption that changes no file metadata, across restarts; a running process already gives that up. Until decided, CC-2 hashes each object of the requested closure once and only those.

| ID | Decision | Status |
| --- | --- | --- |
| D9 | Release for this plan | **Decided: Release 15**, with Plan 63's |
| D19 | Speed target | **Decided: 300 ms, no conditional stage** (Plan 63's decisions) |
| D14 | Persist verified trust across restarts | **Open (owner).** Recommended: persist `file_identity` |

## Source identities

Before code work, record the actual repository, ref and SHA for each. This plan changes three product repositories and astrid-dev. Branches: `release/15/plan-75` in each repository the plan changes, cut from that repository's `release/15/main`, for Release 15 (decided).

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-agent | TBD: `release/15/main` | Agent #400 (`6b8780669`), `release/14/legacy-probes`, `commit-loads`, the `_reference_basis` fix | the uniform baseline rule (#842) | `release/15/plan-75` | `release/15/main` |
| astrid-runtime | TBD: `release/15/main` | `release/14/commit-cost` (cut from `519b404`), Runtime #62 and #63, N5, N10, N11 | #62, #63 | `release/15/plan-75` | `release/15/main` |
| astrid-app | TBD: `release/15/main` | the timing marks (FS-1) are new | N6 | `release/15/plan-75` | `release/15/main` |
| astrid-dev | `origin/main` | this pack | None | `plan/63-dependable-saving` (with Plans 63, 76, 18) | `main` by the scope PR |

## References

- [Plan 63 Dependable saving](../63-dependable-saving/plan.md), [Plan 76 Editing together](../76-editing-together/plan.md), [Plan 18 Extensible editing](../18-timeline-editing/plan.md); Principle: [Plan 54](../54-warm-latency/plan.md) "Verify at a trust boundary once".
- Issues: [#826](https://github.com/banodoco/astrid-dev/issues/826), [#846](https://github.com/banodoco/astrid-dev/issues/846), [#847](https://github.com/banodoco/astrid-dev/issues/847).
- Release 14: [`releases/14.md`](../../releases/14.md); gap: [F-001](../../vision/gaps/F-001-platform-reliability.md).
- Reviews and profiles of 17 and 18 November (held by the Release 14 Lead; their findings are summarised above).

## Plan 77 evidence for FS-0 and FS-1

Round 5 on the 300-clip synthetic v30 reached first usable and full opening at 42.669 and 43.727 s cold and 27.586 and 28.564 s warm. The first complete metadata response under one second came 205.452 s after the first UI marker, compared with 152.779 s in the Round 4 continuation. Several slow responses completed earlier in Round 5. The first edit remained unconfirmed. Its 447.99 Runtime CPU s over a 451.819 s whole-row observation include competing reads and repeated verification. Keep opening, verification, transport availability and commit execution as separate intervals in FS-0 and FS-1. Seed batches on the partial fixture grew from seconds to minutes, and the direct history read serialized more than 120 MB in Round 1. [Plan 77 Round 5 and loop closure](../77-saving-holds-on-a-heavy-timeline/rounds.md#round-5--22-november-2026-blocked-save-at-the-round-cap)

The next design can evaluate removing the automatic complete history walk at opening, verifying inverse targets on demand, persisting a verification checkpoint and serving authenticated reads during shared verification. Preserve the exact pin, freshness and receipt conditions for any proposal. The checkpoint remains an owner decision, and these findings do not change Plan 75's release placement. [Plan 77 Round 5 and loop closure](../77-saving-holds-on-a-heavy-timeline/rounds.md#round-5--22-november-2026-blocked-save-at-the-round-cap)
