# Commit profile on Release 14 (Agent 458d9d51, Runtime d725811), 18 Nov

Code: installed `program/versions/fdbff077811b`, its own `py/bin/python`. Data: APFS clone of `release-14-plan-59/data` (catalog.json paths rewritten to the clone, `instance.lock`, `discovery.json`, `generic-host.json` removed). Scratch Runtime on a free ephemeral port, door 17777, isolated HOME. Harness: the earlier one (`prof_run.py`, wraps `RuntimeService.commit_timeline`, `list_timeline_commits`, now also `import_media`), re-pointed at fdbff077811b. Commits were sent through `astrid timelines edit ... --add-layer media` (a hold image clip on track `chrome`, a new 64x64 PNG each time, so each commit includes one import), the same Runtime commit route and provider as the editor. Tool: the CLI, not the editor, so the editor's own document handoff is not measured. Live :2400 and the owner's data were not touched. Timeline "Almost Ready (trial v2)", head `...054d181b` at the start.

Caveat: the machine had a load average of 4-8 from other sessions during the run. Sequential numbers below repeat to within 0.5 s; the concurrent-run numbers are noisier.

## Wall times (service side, `commit_timeline`)

| Run | Wall |
|---|---|
| Old profile, Runtime 519b404, unprofiled | 187 s (280 s profiled) |
| R14 commit 1, cProfile, cold process | 28.8 s |
| R14 commit 2, cProfile, warm, same process | 27.4 s |
| R14 first commit after a process restart, no profiler | 11.0 s |
| R14 sequential commits 2-8 in the same process, no profiler | 8.6, 8.6, 8.8, 8.8, 9.0, 8.5, 9.3 s |
| Imports (idle) | 0.04-0.26 s |
| History reads (`list_timeline_commits`) | 0.07-0.2 s warm (was 7.5-9.9 s) |

So the Runtime commit is about 21x faster than the old profile, but it is still about 9 s idle. The CLI's total client time was 12-16 s: about 3-4 s more before the POST (reads, history, import). Cold vs warm differ by about 2.4 s without the profiler, 1.4 s with it.

## Where the time goes (cProfile, the 28.8 s cold commit; the warm one is within 2 points of it)

| Share | Cum s | Location | What |
|---|---|---|---|
| 77% | 22.3 | `astrid/sdk/timeline/validation.py:667 validate_final_candidate` | all of it is timing validation |
| 72% | 20.6 | `_commit_timing_validation.py:691 validate_candidate_timing` | |
| 67% | 19.2 | `_commit_timing_validation.py:328 _legacy_exemptions` via `:315 _signed_failures` (2 calls) | the legacy-declaration pass |
| 54% | 15.5 | `_commit_timing_validation.py:74 _reference_basis` (400 calls) | deep-copies per declaration: `:95` dict-comp and `:98` list-comp (the `word_sources` copies of every shot clip), `:53 _reference_shape` (273,742 calls, 10.8 s) |
| 65% | 18.8 | `copy.py:128 deepcopy`: 25.6M calls, 10.2 s own time (35.5% of the total) | almost all of it under `_reference_basis` |
| 11% | 3.2 | `_timing_evaluators.py:283 evaluate` (moment_rule 204 calls, `lookup.py:332 _cut_id`) | |
| 9% | 2.5 | `json.dumps` (9,585 calls) | |
| 6% | 1.6 | `commit.py:736 _check_reservations` (-> `_load`, ancestry walk) | CAS and history verification |
| 4% | 1.1 | `compiler.py:128 compile_timing` (1 call) | |

By tottime: `copy.deepcopy` 35.5%, `_deepcopy_dict` 11.1%, `json encoder iterencode` 8.6%, `dict.get` 6.9% (57M calls), `id` 3.8%. Everything outside timing validation is small: CAS re-hashing is gone (about 0.4 s).

## Counters, old (519b404, 280 s profiled) vs R14 (cold / warm)

| Counter | Old | R14 |
|---|---|---|
| `_check_history_objects` | 59 | 44 / 41 (0.4 s total) |
| `_confirm_object` | 32,686 | 23,906 / 22,313 (0.4 s) |
| CAS reads and sha256 | 23,268 reads, 90,379 sha256 (79 s) | 2,758 / 2,174 sha256 (0.09 s) |
| `revision_closure` loads | 11 | 13 / 11 (0.5 s total); `_load` 8 / 5 |
| `history_read_scope` | 70 | 42 / 38 |
| legacy probes | 268 `_legacy_declaration_is_resolvable`, 69 `compile_timing`, 536 `_reference_basis` | 0 probes; 1 `compile_timing`; `_reference_basis` 400 (now the whole cost) |
| `_digest` | 39,534 (34.7 s) | 1,797 / 1,752 (1.3 s) |
| deepcopy calls | 54M | 25.6M / 24.8M |
| SQLite `execute` | not captured | 2,193 / 2,190 (0.06-0.08 s) |
| `posix.open` | about 16,000 | 35 / 32 |

The two earlier fixes (CAS verification once per scope, legacy probes) worked. What is left is a different copy cost in the same legacy pass: `_reference_basis` runs 400 times (once per legacy declaration, base and candidate) and each call deep-copies the shot clips and source documents.

## Import vs commit

- Idle import: 0.04-0.26 s.
- **An import does block while a commit runs.** I started a commit, waited for its service entry, 1.5 s later POSTed a 64x64 PNG to `/media-imports` and a `commits?limit=4` GET. Three runs: import took **5.0 s, 5.6 s, 6.7 s** (idle 0.1 s), and the GET took 0.2-0.3 s. A stack dump of the import thread at 1 s showed it waiting at `service.py:522` (`with self.store._mutex`, the `_durable_mutation` wrapper, called from `_settle_media_import_catalog` at `service.py:5736`). The commit thread was at that moment in `commit.py:1489 _check_reservations` -> `_load` -> `timeline_commit_port.py:322 revision_closure` -> `:306 _ancestor` -> `timeline_commit_store.py:196 evaluate` / `:1172 _history_entry_view` -> `:853 _verify_accepted` -> `:270 check`, all inside `store._mutex` (an RLock the commit re-takes thousands of times). That is the Runtime ancestry walk Opus flagged in `opus-396-review.md`; it is where the import waits. Import and commit share the same `store._mutex` and the same SQLite `BEGIN IMMEDIATE` writer (the Haiku route maps agree: commit `server.py:402`, `service.py:3157`, accept `timeline_commit_store.py:1982`; import `server.py:1067`, `service.py:5710`).
- **The commit gets much slower when an import overlaps it**: 24.1, 22.6, 24.0 and 26.4 s in the four overlapping runs, against 8.6-9.3 s sequential. The mechanism is not proven (lock-handoff contention on the RLock is my suspicion), and the machine was loaded. The overlap effect looks real, since the sequential runs at the same load stayed at 9 s.
- The import eventually returned 201 each time; I did not reproduce "Failed to fetch". That error has to come from a client or proxy cut: a commit that overlaps another upload takes 22-26 s here, and with the editor's polling and a 60 s proxy cut this leaves less room.

## History growth

Not growing. After the restart: 11.0 (cold), then 8.6, 8.6, 8.8, 8.8, 9.0, 8.5 s for 6 commits in a row; after 15 more commits (head about 20 commits past the copy point), three sequential commits took 9.3, 8.8, 8.8 s. Cold profiled 28.8 vs warm 27.4 s. The ancestry-walk cost (`_check_reservations`, 1.6 s) did not change visibly with history here, since the timeline's history is short (the copy has about 8 commits). The O(N²) walk may still matter for much longer histories, which I did not construct.

## What to fix next (evidence only, not prototyped)

1. `_reference_basis` / `_legacy_exemptions` (`_commit_timing_validation.py:74-116, 328`): about 67% of the commit. Skip the whole legacy pass when the candidate's timing validates with no legacy declarations unresolved, or build each declaration's basis from a shared one-time snapshot instead of 400 independent deep copies. That alone would take a commit from about 9 s to about 3 s.
2. Hold `store._mutex` less in the ancestry walk (`timeline_commit_store.py:196, 1172, 853`) so that other writers (media import) are not starved for the length of the walk. Do not take it per row inside a loop.

---

# Addendum 18 Nov (afternoon): absorb vs discard, then the bisection

Pins measured: Agent `ca3f830f`, Runtime `4c18af59` (the installed program, frozen by an APFS clone of its version dir `f8413e63b423` because :2400's rebuilds kept deleting the one I started on). Every measurement used an APFS clone of the realm and a scratch Runtime on a free port; :2400, :17500, :17501 and :17340 were not touched. Load gate: every step waited for the 1-min load average below 8; the loads recorded before each step were 3.4-4.0 for all A/B steps and about 3-6 for the bisection (earlier attempts that hit load 20-38 or were killed by a reboot or an install rebuild are discarded).

## A. Absorb (Runtime #62 + #65, `cb05b1e`, overlaid on the installed Runtime) vs Discard (same code, `store._after_commit = None` after start-up, scratch launcher only)

Sequence x3 per mode on Almost Ready (`801a01b3...` / `77f906f3...`): commit, import of a 64x64 PNG, commit. Note that each `astrid timelines edit --add-layer media` first imports its file, so every commit is itself preceded by an import; the table lists all of them. Statements counted with `set_trace_callback` on every SQLite connection, per service call.

History length: 17 accepted entries on Almost Ready at the start of each run, 24 at the end (7 commits).

| | A absorb | B discard |
|---|---|---|
| import wall, idle | 0.17-0.37 s (explicit imports 0.28 / 0.36 / 0.26) | 0.04-0.20 s (explicit 0.12 / 0.05 / 0.05) |
| import statements | 1,583-1,660, rising about 13 per commit | 148-158, almost flat |
| next-commit wall (steps 3: c2, c4, c6) | 4.12 / 4.07 / 4.00 s | 4.02 / 4.06 / 4.10 s |
| next-commit statements | 3,212 / 3,456 / 3,723 | 3,211 / 3,456 / 3,724 |
| first commit after start (cold) | 7.50 s | 7.70 s |
| import started 1.5 s into a commit (idle import in brackets) | 2.26 s (0.29) | 0.96 s (0.04) |
| history GET during the commit | 0.63 s | 0.77 s |
| `timeline_commit_timing` line (provider / accept / reconciliation) | 3.87-4.16 s / 320-450 ms / 114-160 ms | 3.86-4.01 s / 322-406 ms / 111-154 ms (4.69 s provider on the commit that overlapped the import) |

- **What discard really does at step 3:** a full scan, not head-only. Commit statements grow by about 128 per history entry (3,212 at 18 entries, 3,723 at 22; roughly 900 + 128 x entries), and the number is the same in A and B. So the retained proofs did not make the next commit cheaper in absorb: absorb pays about 1,450 extra statements in every unrelated write and the commit statements are identical.
- **Wall:** the next commit is the same 4.0-4.1 s in both; the SQLite part is about 0.3-0.5 s of it, so statements are not what dominates a commit (the Agent's CPU is, see B).
- **The 5-7 s import wait is mostly gone** on this Runtime in both modes (0.96 s discard, 2.3 s absorb, against 5.0-6.7 s before). Absorb still holds the mutex longer because its hook re-checks every retained query inside the write.
- **Winner on this timeline: discard.** It costs nothing extra per import (-1,450 statements, about -0.15 s per import, -1.3 s of overlap wait) and the next commit is identical. Absorb would only win if the next commit's re-verification shrank when the proofs are kept; it does not here. Caveat: 17-24 entries; absorb's per-write cost also grows with history (+13 statements per entry), so the gap widens, never narrows.

## B. Bisection: what the 3.7 s is a function of

Document: Almost Ready, 616 clips, 37 cuts, 596 words, 2.6 MB detached JSON. Nudge = `timelines edit --clip music-song:b --on T` (a one-clip `at` change on the Music track); wall = `commit_timeline` service time; median of 5 warm commits after 1 discarded cold commit, all unprofiled unless stated.

| Step | Cold | Warm median | Note |
|---|---|---|---|
| 1a Almost Ready (baseline) | 4.44 | **3.74** (3.61-4.03) | |
| 1b One-clip timeline, same clone | 0.16 | **0.22** (0.16-0.38) | follows the document, 17x less |
| 2c Fresh duplicate of Almost Ready, no history | 4.41 | **3.54** (3.48-3.81) | history is not the cause (only 0.2 s less) |
| 2a Half the clips | not done | | detached edit refused: "chapter '05 THE YEAR' starts at cut 'c18', which is not in the film"; chapters, cuts and word anchors reference the clips |
| 2b No transcripts | not done | | same dependency; not attempted after 2a |
| 3a `dry_run` of the same nudge | 4.15 | **3.37** | the real commit adds only 0.37 s (store accept + reconciliation, about 10%) |
| 3b skip `validate_final_candidate` (scratch clone only) | 2.22 | **1.63** | saves 2.11 s, 56% |
| 3c skip `_check_readers` (scratch clone only) | 4.07 | **3.72** | no saving; the stage is 0.37 s when it runs, so the same reader work is evidently redone later (accept) |

Stage spans (inclusive, medians of the 5 warm baseline commits, from wrapping the Agent's stage functions): `validate_final_candidate` 2.20 s (59%), `document_from_bundle` 0.54 s (14%, 9 calls), `execute` 0.44 s (12%), `_check_readers` 0.38 s (10%), `_load` 0.08, `_digest` 0.05; Runtime accept about 0.35 s and reconciliation 0.12 s on top.

### cProfile of one warm baseline commit (8.4 s under the profiler, 2.3x inflation; trust ranking, not seconds)

By primitive (own time, exclusive):

| Primitive | Share |
|---|---|
| `copy.deepcopy` (copy.py, 4.1M calls) | 31.0% |
| json serialise/parse (`encoder.iterencode`, `dumps` 9,079 calls) | 24.5% |
| sqlite (2,001 `execute`) | 9.4% |
| jsonschema / referencing | 2.5% |
| hashing (sha256) | 0.8% |
| other Python | 30.6% |

By stage (cumulative, inclusive): `validate_final_candidate` 37.4%; within it `_commit_timing_validation.py:750 validate_candidate_timing` 34.6%, of which `_legacy_exemptions` (:387) 25.5% and `_validate_candidate_timing` (:786) 9.1%; `_check_readers` 16.1%; `document_from_bundle` (`commit.py:302`, 9 calls) 16.7%; `commands.execute` 15.8%; Runtime `accept` 15.4%; `_digest` (1,692 calls) 15.0%; `compile_timing` 5.7% (1 call); schema (`_validate_params` 616 calls) 2.6%. Top deepcopy callers: `timeline_commit_validation.py:49 detached` 5.2%, `commit.py:313` 3.9%, `document_from_bundle` 3.8%, `authoring_bundle.py:165 _copy` 3.5%. Top json callers: `authoring_bundle.py:169 _canonical_json` 14.3% (2,076 calls), `_signed_failures` 3.2%, `_BasisReader.signature` 2.4%.

### Verdict

**A hotspot, with passes inside it.** One stage, `validate_final_candidate`, is 56-59% of the wall time, and removing it takes 3.74 s to 1.63 s. Inside it, the timing validation is about 90%, and the legacy-declaration pass runs twice (`_signed_failures` n=2: candidate and baseline), so the hotspot is built from many passes over the 616 clips (deepcopy 31% and canonical-json 24% by primitive). The work follows the document (0.22 s for one clip), not the history (3.54 s on a duplicate with none).

Top 3 costs (true shares of the 3.74 s from stage spans and skips):
1. `astrid/sdk/timeline/validation.py:667 validate_final_candidate` -> `_commit_timing_validation.py:750 validate_candidate_timing`, mainly `_legacy_exemptions` :387 / `_signed_failures` :374 (run twice) -> `_declaration_failures` :328 -> `_collect_failures` :316 -> `_timing_evaluators.py:620 legacy_declaration_failures`: about 2.1 s, 57%.
2. `astrid/sdk/timeline/commit.py:302 document_from_bundle` (9 calls, deepcopies at :313): about 0.54 s, 14%.
3. `astrid/sdk/timeline/commands.py execute` about 0.45 s (12%); `commit.py:1082 _check_readers` 0.38 s (10%) is close behind and Runtime accept 0.35 s (10%).

Smallest fix: in `_legacy_exemptions` (`_commit_timing_validation.py:387`), skip the baseline `_signed_failures` pass when the candidate's pass reports no legacy declarations touched by the edit, or reuse the baseline's result keyed by revision id across commits; the skip experiment bounds the win at 2.1 s of 3.7 s. Not prototyped.

### Fable's leads

| Lead | Verdict | Share |
|---|---|---|
| Two full timing compiles per commit | Refuted as stated: `compile_timing` runs once (5.7%). What runs twice is the legacy-failure collection (`_collect_failures` n=2, 19% profiled) | 5.7% / 19% |
| A fresh schema validator per clip | Refuted as a cost: 616 per-clip `_validate_params` calls exist but jsonschema is 2.5% own time, `_validate_params` 2.6% cumulative | ~3% |
| Repeated verify and digest passes over the whole document | Confirmed: `_digest` 1,692 calls 15%, `_canonical_json` 2,076 calls 14%, `document_from_bundle` 9 builds 17%, deepcopy 31% across callers | 15-31% |
| `_BasisReader` (#400) rebuilt on every call, nothing cached across commits | Confirmed that it is rebuilt per commit (`:379` x2, `:714` x2) and holds nothing across commits, but it is now small: signatures 2.7% + json 3.2% | ~6% |

Not done: the half-clips and no-transcripts variants (the document is not editable to a smaller valid one through the detached commit, see the table); a `_check_readers` skip that saves nothing means its work is shared with accept, so removing it alone will not help. Clones, scratch Runtimes and the frozen program copy were deleted at the end.
