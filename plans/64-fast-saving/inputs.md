# Inputs — Fast saving

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner asked whether to split the save work into stability, speed, multi-edit robustness and extensibility and the main thread accepted the four-plan structure of an independent check; the owner then said to add it to astrid-dev and not do it yet. This plan is queued, in no release, with its release open. Next: the owner chooses the release (recommended with [Plan 63](../63-dependable-saving/plan.md)) and says go, and answers D14; the scope PR records the answers here; only then does the plan become `Accepted`.

**Prior art:** This is the cost half of Plan 18's former Phase 0, moved to Plan 63 on 18 November 2026 and then carved out into its own plan (CC-1, CC-2, CC-9, CC-11). Sources: the reviews and profiles of 17 and 18 November held by the Release 14 Lead (`fable-near-instant-review.md`, `plan-near-instant-commits.md` Rev 2, `near-instant-facts.md`, `sonnet-commit-profile.md`, `sonnet-commit-profile-r14.md`, `fable-four-questions.md` section 3); they are private and not committed, so what matters is restated here as shapes and counts. Nothing here copies content from the owner's timeline.

- *The measured shape.* One timeline with shots, about 8 records and a closure of 7 shots, about 1 MB per revision and about 1,100 distinct stored objects. An uncontended add-media commit took 187 seconds (176 live); profiled, 280 seconds, of which about 190 were CAS re-verification (59 history read passes, 32,686 confirmations, 23,268 physical reads, the Agent loading the base 11 times) and about 80 were legacy timing probes. The reservation scan (2 + 3N closure loads per attempt) grows by three loads per edit. The editor polls about 110 requests a minute per tab; a history GET took 8 to 9 seconds while holding the store mutex.
- The Release 14 profile (Agent `458d9d51`, Runtime `d725811`, 18 November, on the owner's timeline cloned): the Runtime commit is about 9 s idle (was 187 s, about 21 times faster), 67% of it in `_legacy_exemptions` through `_reference_basis` (400 calls, each deep-copying the shot clips and source documents; 25.6M `deepcopy` calls). CAS re-hashing is gone (about 0.4 s). History reads are 0.07 to 0.2 s warm. **An import does wait on a commit:** 5.0 to 6.7 s behind `store._mutex` (idle 0.1 s), and a commit that overlaps an import takes 22 to 26 s against 9 s sequential (mechanism unproven). So a save in progress does delay an upload, but the failure itself was the cut connection, not the wait. The fix of the 67% is in Release 14; CC-2 starts from the profile. The import wait is what Release 14 Runtime #62 and #65 addressed; CC-2's proof re-measures it.
- *Landed on Release 14 since that profile, not measured:* Agent #400 (`6b8780669`: the legacy pass builds its bases once; about 3 s inferred, which is 33% of 9 s), Runtime #62 (keep verified history across unrelated writes so an import never forces a re-walk) and Runtime #63 (one reply writer, health off the mutex, commit timing at INFO), plus the two earlier cost fixes (187 s to 9 s, measured), N5, N6, N10 and N11. **Their effect is not measured; FS-1 measures it.**
- *Never measured by anyone:* the time from a gesture ending in the editor to the accept; the browser's write per edit; the size of the document and of the reply.

**Where the time goes today, and what makes each step cost the change** (from the independent check; sizes in [tasks.md](tasks.md)):

| Step | Scales with today | What makes it cost the change | State | Size |
| --- | --- | --- | --- | --- |
| Wait before sending | A fixed 500 ms, plus every earlier edit's commit (`useTimelinePersistence.ts:47`) | Send at once when idle; one batch waiting | [Plan 63](../63-dependable-saving/plan.md) | there |
| The browser's record | About three whole documents per edit, plus a recovery snapshot in a second database | The record is the patch; one display copy per timeline | Plan 63 CC-5b | there |
| The request | The change: one `doc.patch` and the base ids | already so | done | 0 |
| The legacy timing pass | The document times the number of declarations: 400 deep-copying calls, 67% (measured) | Built once per bundle (the pass still runs on every commit) | **landed** (#400), unmeasured | re-measure (FS-1) |
| Timing compile and evaluate | The whole document, once per commit: 15% of the old profile, perhaps 1.3 s (inferred) | Stage 1: find why 204 rule evaluations cost this much. Stage 2: validate what the change touches | new | FS-3, 6 days |
| Serialising and hashing | The document, many times: 9,585 `json.dumps` calls (9%) and 1,797 digests (measured) | Once per commit; an unchanged child keeps its digest | CC-2 | here |
| The history check | The history: the ancestry walk under `_check_reservations` (6% at 8 entries, measured; suspected to grow as the square on long histories, not constructed) | Accepted history is immutable, so the head is trusted and nothing is walked | partly landed (#62); CC-2, CC-11 | here |
| Replay over a moved head | The number of commits since the writer's base, two whole-document loads each (`_commit_patch.py:885-887`; not measured) | Replay against the net difference | new | FS-4, 2 days |
| Losing the race at accept | The whole validation again, up to three times (`commit.py:1427`, `:1552`) | Stage 1 makes it rare; then one commit at a time per timeline | new, after stage 1 | FS-5, 1.5 days |
| The store's writes | The document (a new revision row holds the whole payload) | Leave it; all of SQLite is under 0.1 s (measured) | — | 0 |
| Steps that follow the history or the number of commits (all reported, none measured) | see CC-1 | Each becomes a counter at 300 entries; fix only the ones that go red | new counters | in CC-1, CC-2 |
| The reply | The document: every reply carries the canonical document (`localSaveSession.ts:297`) | The reply is ids and a digest | new | FS-2, 1.5 days |
| Waiting on a lock | An import waited the length of the commit's history walk (5 to 7 s, measured) | Reads and imports do not take the commit's lock | landed (#62, #63), unmeasured | CC-9, 1 day |

**Approach:** Measure from the editor first; then remove the repeated whole-document work (stage 1); only on stage 1's numbers make validation follow the change (stage 2). Alternatives rejected: tuning (stage 2 must come from the principled change); a faster language, a second process, an "accept now, validate later" reply (a refusal must stay an answer to the request); a cache keyed by base revision (every ordinary edit creates a new base, so it only helps retries); a clock gate (the owner forbids it; the proof is counts, with the measured numbers as evidence).

**Challenge:** Reviewed: the independent four-questions check (`fable-four-questions.md`, 18 November 2026, held by the Release 14 Lead; read-only, nothing built or run) gave the stages, the arithmetic and the honest limit, and accepted by the main thread. Its own caveats: the stage estimates scale profiled seconds by 9 ÷ 28.8, which is rough because a profiler slows call-heavy code more than the rest; `lookup.py:332` and the evaluate cost, the remaining server time after the landed fixes and the browser's write per edit are unmeasured. Next: a further reviewer may read it against the code before the owner's answers.

**Proof and limits:** Completion is the list in [plan.md](plan.md#completion). Limits: nothing here was built or run; the sizes are the independent check's judgment on the plan's own figures, not a bottom-up estimate; stage 1's arithmetic reaches only 1.5 to 2 s.

**Review rounds:** Pending — none recommended for stage 1 beyond the review of the integrated candidate that Plan 63's R0 already gives the shared corpus; for stage 2 (a change to validation) one round at the end, because it changes the commit path. Next: the owner confirms.

**Run start:** Pending — no run is authorized. Next: when the owner starts a run, record the date, the tasks it covers, the accountable session, what it may do without asking, what needs her go, and the advisor session.

### Issue ledger

| Issue | State now | This plan | How |
| --- | --- | --- | --- |
| [#826](https://github.com/banodoco/astrid-dev/issues/826) history reads pay for the whole history; every write clears the verification cache | open | closes | CC-1, CC-2, check FS-C1 (the verification-cost part is already on the Runtime's `p59/revision-listing-perf`) |
| [#846](https://github.com/banodoco/astrid-dev/issues/846) every refusal clears the replay memo | open | closes | CC-2, check FS-C1 (zero re-hashes after a refusal) |

### Deferred

| Item | Decision | Reason |
| --- | --- | --- |
| The editor's poll rate (about 110 requests a minute per tab) | Deferred; the cost is bounded by CC-2 | After CC-2 a GET does no hashing and clears no trust, proven by count. Lowering the rate needs the editor to adopt the head it saves (Plan 18's TL-5) or a push (Plan 65's nice-to-have) |
| The roughly 1 MB snapshot stored per revision | Deferred; file an issue | The contract bounds work, not disk. Delta storage is a storage-format change with a migration |
| The residue under one second | Decided on FS-1's numbers | "Low seconds" is the honest expectation until measured. The editor's 500 ms save debounce is a separate floor (Plan 63 deletes it) |
| Waveform peaks stored beside the object | Deferred | N6 fetches each object once; storing derived peaks is a separate storage question |
| The two proxy hops of the local install | Deferred | Each is a second mechanism around a cause N5 and N6 remove; proxy limits, connection pooling and a longer proxy timeout are not built |
| One object reader and one URL builder | Deferred; file an issue | No incident needs the refactor; the GET-count test catches a returned bulk download |
| Metadata reads other than object and health sharing the commit's mutex | Deferred | #62, #63 and N10 address the import and health waits; CC-2 re-measures |

## Owner decisions

Decision ids keep the numbers they had in [Plan 18](../18-timeline-editing/inputs.md#owner-decisions) so references stay valid. **D9 (which release) is [Plan 63's](../63-dependable-saving/inputs.md#owner-decisions): one decision for the four plans, open, recommended Release 15 for Plan 63 with this plan running in parallel from the same day.** The one decision that is this plan's:

**D14 — Open (owner): persist verified trust across restarts (cold start).** Recommended: persist each verified object's `file_identity` (dev, inode, size, `mtime_ns`, `ctime_ns`) in the store database, so a restart does not re-hash every media object (about 8 s on one timeline, 2.2 GB on this realm, growing with media bytes; [#847](https://github.com/banodoco/astrid-dev/issues/847) first start lives here). It is the largest uncovered cost: every restart re-hashes. What is given up is corruption that changes no file metadata, across restarts; a running process already gives that up. Until decided, CC-2 hashes each object of the requested closure once and only those.

| ID | Decision | Status |
| --- | --- | --- |
| D9 | Release for this plan | **Open (owner)**, with Plan 63's |
| D14 | Persist verified trust across restarts | **Open (owner).** Recommended: persist `file_identity` |

## Source identities

Before code work, record the actual repository, ref and SHA for each. This plan changes three product repositories and astrid-dev. Branches: `release/<NN>/plan-64` in each repository the plan changes, cut from that repository's `release/<NN>/main`, where NN is the release chosen (open).

| Repository | Starting branch + SHA | Retained work / donor SHAs / unpublished changes | Verified predecessor output | Candidate branch | Intended destination |
|---|---|---|---|---|---|
| astrid-agent | TBD: `release/<NN>/main` | Agent #400 (`6b8780669`), `release/14/legacy-probes`, `commit-loads`, the `_reference_basis` fix | the uniform baseline rule (#842) | `release/<NN>/plan-64` | `release/<NN>/main` |
| astrid-runtime | TBD: `release/<NN>/main` | `release/14/commit-cost` (cut from `519b404`), Runtime #62 and #63, N5, N10, N11 | #62, #63 | `release/<NN>/plan-64` | `release/<NN>/main` |
| astrid-app | TBD: `release/<NN>/main` | the timing marks (FS-1) are new | N6 | `release/<NN>/plan-64` | `release/<NN>/main` |
| astrid-dev | `origin/main` | this pack | None | `plan/63-dependable-saving` (with Plans 63, 65, 18) | `main` by the scope PR |

## References

- [Plan 63 Dependable saving](../63-dependable-saving/plan.md), [Plan 65 Editing together](../65-editing-together/plan.md), [Plan 18 Extensible editing](../18-timeline-editing/plan.md); Principle: [Plan 54](../54-warm-latency/plan.md) "Verify at a trust boundary once".
- Issues: [#826](https://github.com/banodoco/astrid-dev/issues/826), [#846](https://github.com/banodoco/astrid-dev/issues/846), [#847](https://github.com/banodoco/astrid-dev/issues/847).
- Release 14: [`releases/14.md`](../../releases/14.md); gap: [F-001](../../vision/gaps/F-001-platform-reliability.md).
- Reviews and profiles of 17 and 18 November (held by the Release 14 Lead; their findings are summarised above).
