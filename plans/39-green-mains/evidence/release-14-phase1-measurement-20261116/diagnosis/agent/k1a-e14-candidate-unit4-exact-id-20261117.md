# Agent K1a — PR377 unit-shard-4 exact-ID qualification (17 November 2026)

## Source and immutable identities

- Frozen Plan 39 Agent head: `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`, reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`.
- Baseline [CI 43967861168 attempt 1, unit shard 4 job 133651924745](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924745); [actual JUnit artifact 14282820153](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14282820153). Downloaded and parsed ZIP SHA-256 `2acb279263d68ae27adb9a008e0e0d610dc9bf4662c40fb2c6645cf7bdbe1cf7`; embedded `unit-shard.xml` SHA-256 `63ea09f25b19ec3267f75f37d07a4fc0af9b122117fd956fa90a49e44b508008`.
- Isolated [draft PR377](https://github.com/banodoco/astrid-agent/pull/377) candidate `5b9db95c84f863c0eee63c238bdeb4583b49d7c7`, not integrated. [CI 44110964432 attempt 1, shard 4 job 134136117723](https://github.com/banodoco/astrid-agent/actions/runs/44110964432/job/134136117723) completed failure; [actual JUnit artifact 14351776351](https://github.com/banodoco/astrid-agent/actions/runs/44110964432/artifacts/14351776351). Downloaded and parsed ZIP SHA-256 `f0ada6f638fbdc7d76b4ba37c2895afa82341177f5ac5a85b4aae5b689526528`, **equal to GitHub artifact digest**. Embedded `unit-shard.xml` SHA-256 `1c26f6ee645effea6de115146de162dfeef86b00d052705af0d1b02710f4f560`.

## Actual XML comparison — all 16 previously outstanding E14 IDs accounted for

Both XML inventories have exactly **2,054 unique testcase IDs**, identical membership and outcomes: **2,007 passed / 28 failed / 19 errors / 0 skipped**, with **zero status transitions** (all 2,054 exact IDs matched). The 16 baseline stale-Runtime-pin setup errors no longer contain `9ef8087` in the candidate; **all 16 remain setup errors**, now at the untouched `runtime_protocol.timeline_commit_store` source-authenticity assertion, imported from Python 3.11 `site-packages` instead of the checked-out `astrid-runtime`. Full candidate `<error message>` literal, 16 occurrences (UTF-8 message SHA-256 `51e067ab72f35763ef953f4574d73e093905959ba3d5a3de3d71ae9920d1b828`):

```text
failed on setup with "AssertionError: assert PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py') == (PosixPath('/home/runner/work/astrid-agent/astrid-agent/astrid-runtime') / 'runtime_protocol/timeline_commit_store.py')
 +  where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py') = resolve()
 +    where resolve = PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py').resolve
 +      where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py') = Path('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py')
 +        where '/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py' = <module 'runtime_protocol.timeline_commit_store' from '/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/timeline_commit_store.py'>.__file__"
```

The other **three** unit-4 errors retain a distinct literal setup message (UTF-8 SHA-256 `069e959438f5f0f123097cc7b049fb9e98d44cae6883d58c4c1ed2a62e569f7e`), count 3: `failed on setup with "FileNotFoundError: [Errno 2] No such file or directory: '/home/user/work/runtimes/agent-remotion-composition14-255b6856'"`. They are not part of the E14 revision correction.

The complete 16 old-ID → same new-ID cohort (each **error → error**, with the source-guard replacement) is:

- `tests.editing_conformance.test_reviewed_list_runtime_v3::test_disjoint_reviewed_doc_patch_list_merges`
- `tests.editing_conformance.test_reviewed_list_runtime_v3::test_reviewed_list_before_state_conflicts`
- `tests.editing_conformance.test_reviewed_list_runtime_v3::test_reviewed_list_aba_order_membership_and_idless_still_conflict`
- `tests.editing_conformance.test_reviewed_list_runtime_v3::test_function_commit_still_atomic`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_j1_overlapping_list_survives_restart_and_rederive_closes_record`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_function_swap_of_new_file_reruns_with_runtime_verified_media`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_function_swap_runtime_refusal_is_saved_and_retry_reruns`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_reviewed_list_runtime_refusal_is_saved_and_recovered`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_j3_exhausted_function_retry_lands_and_closes_record[True]`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_j3_exhausted_function_retry_lands_and_closes_record[False]`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_explicit_atomic_function_fallback_rederives_after_disjoint_edit`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_j4_lost_ack_on_retry_is_confirmed_once_and_record_closes`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_cli_retry_reports_accepted_part_from_durable_pending_state`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_j5_two_actors_retry_one_record_and_group_id_closes_other_actor`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_f3_idempotency_mismatch_is_refused_and_saved`
- `tests.editing_conformance.test_timeline_clash_back_acceptance_runtime::test_f4_rederived_list_replay_is_idempotent_across_actors`

## Review limits / decision

This finishes the previously missing **16/85** PR377 exact-ID comparisons: prior candidate observations had all 68 shard-7 IDs and the one Darwin ID; the full 85 now lack the stale hard-coded SHA error. **No E14 functional pass is proved by the 16 or the 68**; all 84 Linux targets now stop at the source-path assertion, while the Darwin target reaches a substantive Remotion validation refusal (see PR377 evidence comment). The 95 independent source-import provenance errors at baseline remain distinct; do not double-count them or assume repair of the retained guard. No old-ID absences were used to infer regressions.

**Route:** N exact artifact/XML and source-provenance verification only, not an independent PR review. Product/packaging resolution remains X-class; authority-sensitive source authentication may require S review. No assertion weakening, editable-install substitution, module-cache purge, test skip, branch merge or unrelated CI action is authorized by this record. PR377 is still draft/unmerged, with **zero independent submitted reviews** at last check. The original CI **882 failures/398 errors** and Lanes **306 failures (including 12 opt-in)/260 errors** are unchanged, and formal G1/G2 remain incomplete; RS1 **0/1**. Plan38/55 WAITING, Release15 excluded, uncommitted Runtime clip 25P/2F conflict held.

**Candidate conclusion:** the revision expectation was corrected (85/85 reached downstream outcomes), but **the full relevant acceptance tests are not green**; no merge. Candidate CI run itself has additional incomplete shards and cannot be declared a final green or fully qualified G2.
