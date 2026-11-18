# Opus review: astrid-agent PR #396 (`release/14/commit-loads` into `release/14/main`)

18 Nov 2026. Read-only review: nothing merged, pushed or commented. Branch head `a2b5681ba`, cut from `b126d7482`. The target is now `fa1efe291` (#394).

Claim labels: **verified** (I read or ran it), **peer** (a Haiku helper reported it and I spot-checked), **unverified**.

## Verdict

**Merge after one small fix (three parts, roughly 25 lines).** The memo is sound for integrity. I found no path where a stale row lets a retired identity through. The fix tightens the fallback and adds the one test the safety argument most depends on. Moving the memo onto the provider instance is recommended, but it doesn't block the merge.

### Required fix (one commit)

1. **Test the fallback directly.** Add a test to `tests/sdk/test_timeline_commit_reservation_memo.py`. It retires an identity (create, then inverse). It then seeds `_RESERVED_HISTORY` with a row for the same scope whose publication isn't in this realm, and whose reserved set is `frozenset()`. Then it re-creates the retired identity. The test asserts three things:
   - the refusal is `identity_collision`;
   - the head is unchanged;
   - the row now names the head's publication.

   Add a second case where the row's publication is newer than the head (for example `publication-99`).

   Today no test drives a warm-path miss into a full scan that succeeds. The damage cases only reach the fallback when the full scan also fails. So a regression that kept the foreign reserved set after a miss would pass the suite. (Probe results are below.)

   Also, in `test_damage_newer_than_the_memo_still_fails_closed`, assert the memo is unchanged after the refusal: `before = dict(commit._RESERVED_HISTORY)` … `assert commit._RESERVED_HISTORY == before`. That pins "stored only after a clean scan".
2. **Narrow the fallback to the refusal it means.** In `read_history` (`commit.py:1037-1043`), change `except Exception: pass` to `except rejected:`.
   - Every non-ancestor or unreadable case already raises that class. Three places raise it: the agent's own `_history` (`rejected(...)`), the Runtime store (`reject("history_unavailable", …)`, `timeline_commit_store.py:38-46`, for a missing entry, an after-entry later than the head, a chain break or a through mismatch), and the Runtime port (`refused(...)`, `timeline_commit_port.py:89-96`).
   - `DetachedPort` raises the same `CommitRejected`.
   - With `except Exception`, any bug in the warm path, such as a `KeyError` or `TypeError` in building `after`, turns into a silent full scan. Nothing reports it, and saves quietly go back to O(history), which is the 3-minute symptom this PR exists to remove.
3. **Drop the redundant branch.** In the same block, `[] if after == current else _history(...)` duplicates `_history`. When `after == through`, `_history` already returns `[]` with no port call (`while previous != through` never runs, `commit.py:670-672`). Use `entries = _history(port, current, after, rejected, base)`.

### Recommended, not blocking

4. **Key the memo by scope.** "One newest row per timeline" is a dict keyed by `(project, timeline)`: `_RESERVED_HISTORY[scope] = (head_pair, frozenset(reserved), recorded)`. That removes the linear scan in `_warm_reserved`, the scan-and-delete loop in `_remember_reserved`, and the `key[2]`/`key[3]` indexing in the code and tests. It's about ten fewer lines with the same behaviour.
5. **Scope the memo to the provider instance, not the module.** The Runtime builds one provider per start, right before the `RuntimeService` for one realm (`daemon.py:301-303`). Keeping the memo on `RuntimeCommitService` would mean:
   - each Runtime start begins cold, including an in-process restart after `replace_from_backup`;
   - one memo can't span two realms;
   - the global autouse fixture in `tests/conftest.py` can go. It now runs for every test in the suite, and it exists only because fake realms reuse ids.

   The cost is one argument to `_check_reservations` (required, with no default, so there's still one path). `DetachedRealm` would hold one service instead of building one per `call`, and the direct callers in `test_timeline_commit_graph_roots.py` and the fork tests would pass a memo. This copies the Runtime's own pattern: its `_history_state` entry and closure caches belong to the store instance, so they're realm-bound by construction.
6. Optional nits:
   - `_load` deep-copies the document before storing it (`commit.py:445`). That copy isn't needed: `bundle_from_document` deep-copies its input and never mutates it, and both ports return detached values. Dropping it saves one closure deepcopy per unique revision.
   - A single real-Runtime-port assertion would catch a Runtime-side regression that the fake port can't. For example, in `test_timeline_commit_graph_roots.py`, check that the second creating commit pages with a non-None `after_publication_id`.

## 1. Safety of the process-level memo

**Can a stale row let a retired identity through? No, in every case I checked (verified).** A row is trusted only when its key `(project, timeline, publication, revision)` sits on the head's chain. Two checks prove that:
- the Runtime returns a contiguous chain from that publication to the head (store `_history_page`, `timeline_commit_store.py:1180-1219`, with its own chain-break and through checks);
- the agent re-verifies the linkage (`_history`, `commit.py:668-694`).

Three facts make a match mean "same ancestry":
- **Publication ids are random.** Each accepted publication's id is `txn-<uuid4>` (`store.py` `_record_command_receipt` → `util.new_id`).
- **History is insert-only.** There is no `UPDATE` or `DELETE` of `timeline_commit_history` anywhere in `runtime_protocol`.
- **History is linear per timeline**, ordered by `project_seq`.

So a publication id that appears in two places carries the same ancestry in both, and its reserved set is the same.

- **Reserved sets combine by union.** History scans run with `check=False` and only ever add to `reserved` (`commit.py:968-1029`, `:1047-1067`). So reserved(head) = memo(P) ∪ the contributions of the entries in (P, head]. This holds for every entry kind (fork, place-shared, restore-in-history, inverse). `recorded` is carried over correctly.
- **Restore / `timeline.restore`.** Restore goes through `commit()` and publishes a new forward entry (`commit.py:1269-1276`, peer + verified). It's scanned as a new entry. The head never moves backwards, and the union never shrinks.
- **Forks and inverse commits.** Fork contributions depend only on the entry's own `accepted_base` and `requested_base`. An inverse retires an identity, and the identity stays reserved by union. The PR's `test_retired_identity_is_still_refused_from_a_warm_memo` covers this.
- **Publication changes and CAS retries.** A newer head scans (memo, head]. Attempt 1 of the CAS loop reuses attempt 0's row, which is correct and faster.
- **Realm swapped under a running process; two realms or projects in one process.** The key carries `project_id`, but not the realm. That's safe only because ids are uuid4 and realm copies (the :2400 rebuild, `replace_from_backup`, the RunPod `replace_realm`) copy history byte for byte. A copied publication has the same ancestry. One that isn't in the new realm fails `read_entry` and falls back to a full scan.
  - The trust is exactly key identity: a row whose key matches an ancestor is used without rescanning (probe below). That's why fix 5 is recommended.
  - **Import** (`.astrid` and copy-to-new-timeline) requires a new timeline id and `expected_head` None (`service.py:2015-2050`), so it makes new publications. It can't reuse an old key.
- **Runtime restarts.** A process restart clears the memo. An in-process restart (the daemon's `_start` again) keeps the global memo, which is safe by the uuid argument. Fix 5 makes it cold by construction.
- **Failed or partial commits.** The row is written after the history loop succeeds and before the plan scan (`commit.py:1071`). It describes accepted history at `current = port.head()`, not the candidate. If the plan is refused or the CAS fails later, the row is still true. If a scan fails, nothing is stored. A rolled-back or unknown publication can only cause a miss and a full scan.

**Is the ancestor check sound, and what does it cost? Yes; it costs the read of the new entries and nothing more (verified).**
- On the Runtime it's one `history(head, after)` page per 100 new entries: `_ancestor(head)` is one step because the head was observed, `read_entry(after)` is one entry view, and then a range select.
- A miss costs one refused entry lookup before the full scan.
- Out of scope, but it will show in the re-profile: the Runtime port's `revision_closure` authorises a non-head, non-base revision by walking the whole ancestry from the head. The loop at `timeline_commit_port.py:299-306` has no early exit, and each `_ancestor` call re-walks from the roots. That's O(N²) entry views, each running `_verify_accepted`, on the first such closure per request. The warm path still asks for the memo boundary's closure, so this term stays until the Runtime fixes it.

**Is skipping older entries a new trust? No; the Agent and Runtime already grant the same trust (verified).**
- The rebase path reads only (base, head] (`commit.py:1402`).
- The Runtime keeps process-level `_history_state` caches of entries and closures, keyed by publication and revision.
- What changes is detection, not reservations. Before this PR, a damaged old entry made every creating commit refuse with `history_unavailable`. Now a warm process keeps using a reserved set computed while that entry was intact, and a cold process still refuses. Neither can reuse a retired identity, so this is acceptable.
- There's one consequence: an outcome can depend on how warm the process is, but only on corrupted history.

## 2. Is process-level state warranted?

**Cross-commit state, yes.** A per-commit memo is still O(history) on every creating commit. Fable's point, adopted as plan R2: "the real fix is to keep the reserved-identity set per publication". The provider has no session concept, so "per session" really means "per provider instance".

The right owner is the **provider instance** (fix 5), not the module. The PR's global works, but it outlives Runtime restarts inside a process, spans realms, and needs a suite-wide autouse fixture.

**Two paths?** Barely. The warm and cold paths share `_history`, the entry loop and `scan`. They differ only in their starting tuple: `(None, ∅, False)` or the stored row. The oracle test pins them to equal output. What can drift is the fallback's silence, so fix 2 makes it catch only the refusal it means.

## 3. Tests

- **The oracle is independent enough (verified).** The cold run patches `_warm_reserved` to always miss, so every commit runs the pre-PR full scan. Both runs record the stored `(current, reserved, recorded)` at every creating commit and compare them.
  - Its history (track creates, an inverse, more creates) is thin. But since history scans only add to `reserved`, entry kind doesn't change the decomposition.
  - A richer history would only protect against a future change that makes the per-entry scan stateful.
- **Load count.** `test_loads_per_creating_commit_do_not_grow_with_history` is a good count-not-clock proof. It also checks that the warm path engages: every history read has a non-None `after`.
- **Damage tests (11 kinds).** These are useful, but `missing_entry`, `ancestry` and `previous` fail through the fallback, because the full scan also fails. They prove the code fails closed, not that the warm path validates.
- **Missing:** the fallback-success test (fix 1), memo-unchanged-on-failure (fix 1), and a real-port warm-path check (nit 6).
- **Added markers:** no `TODO`, `skip` or `xfail`. The only marker is one `# noqa: F401` on the autouse `runtime_abi` import, which is fine (peer + verified).

## 4. Elegance

At +60/−9 in `commit.py`, the change is close to minimal, and its comment block states the invariant well. Fixes 3 and 4 remove about 12 lines and every tuple-index lookup. Fix 5 swaps a module global plus a suite-wide fixture for one instance attribute and one argument. Nothing else to cut.

## Merge with #394

- **Textually clean (verified).** `git merge-tree --write-tree origin/release/14/main HEAD` exits 0. A local merge in a scratch worktree succeeded.
- **No interaction.** #394 touches only `_commit_timing_validation.py`, `_timing_evaluators.py` and tests. It adds no module-level state and doesn't call `_load`, `revision_closure` or `_check_reservations`. Its timing validation runs inside `validate_final_candidate`, after the reservation check.
- Note: the worktree's `git fetch` only refreshes `release/14/commit-loads`. Fetch `release/14/main` explicitly. Haiku helper (b) compared against the stale `b126d7482` and wrongly reported #394 as absent.

## Evidence

All runs were local, on Python 3.11 with a sandboxed HOME. The Runtime was `runtime-src` (branch `task/plan59-shot-trim`, not the pinned Runtime), which explains the 24 pre-existing failures below.

**Suites (verified).** I ran the reservation, commit-provider, semantic-reservation, fork and preexisting-violation suites, plus `test_timeline_commit_graph_roots.py`, whose 31 integration tests were deselected.

| Tree | Result |
|---|---|
| Base `b126d7482` | 24 failed, 195 passed |
| PR `a2b5681ba` | the same 24, plus `test_move_reload_and_inverse_import_no_renderer` |
| PR + `fa1efe291`, merged locally | 24 failed, 254 passed (includes #394's differential tests) |

- On the PR tree, all 14 new memo tests pass.
- The extra PR failure is environmental: the subprocess's Runtime locator found no sibling checkout. It passes with `ASTRID_RUNTIME_CHECKOUT` set.
- So the PR adds no new failures in these suites.
- The real-port reservation tests (graph_roots integration) didn't run here.

**Probes (verified).** These were scratch tests in the merged tree, never committed. A copy is at `/private/tmp/claude-501/-Users-hannahomalley/89e96a59-5dfa-43fb-8013-1fe9d0216757/scratchpad/test_zz_review_probe_396.py`. All five pass.

| Probe | Result |
|---|---|
| Foreign row (publication not in the realm, empty reserved set), then re-create a retired identity | Refused with `identity_collision`; the head is unchanged and the row is replaced by the head's key. The fallback works; fix 1 makes this a permanent test. |
| Row for a publication newer than the head | Falls back, refuses. |
| Damage to the newest entry, then a creating commit | Refused; memo unchanged. |
| Row with the head's exact key but an empty reserved set | The retired identity is **accepted**. This shows the trust is exactly key identity. |
| Two fake realms with colliding deterministic ids; realm a's row left in the memo; realm b re-creates its retired `y` | **Accepted**. Both realms had head `(publication-2, parent-1)`. The fake's inverse returns to revision `parent-1`, so the key's revision adds nothing, and safety rests only on the publication id. |

The last two can't happen in production, because publication ids are `txn-<uuid4>`. They are why the suite-wide autouse fixture is needed, and why fix 5 is worth doing.

**Helpers (peer):**
- (a) The only production caller is `commit.py:1449`, in the CAS loop. Restore, undo and inverse go through `commit()`. Import and duplicate-to-new-timeline create a new timeline through the Runtime import endpoint. Realm replacement (`pod_reset.replace_realm`, `daemon.replace_from_backup`) needs a stopped Runtime.
- (b) Diff stats: +202/−9 over 3 files; 4 test functions, 14 cases; one `noqa`, no `TODO`, `skip` or `xfail`.
