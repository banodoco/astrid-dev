# K1a / N-route — prepared-video frozen-history objects absent from the tested CI checkout (2026-11-17)

## Identity, scope and original proof

- Agent exact reviewed head: `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`; reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`.
- Original [CI run 43967861168, attempt 1](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), completed failure; unit shard 3 job **133651924518**: **1,865 tests, 31 failures, 0 errors, 1,834 passes**. The two groups below are **seven of those existing 31**. They are already within the overall CI **882 failures / 398 errors**, not additional failures.
- Previously retrieved and verified *actual JUnit XML* artifact [14279162456](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14279162456): ZIP SHA-256 `6bb5af87d04b19801da97ecb6b109238d3e321979f0ec3fd40838ce1771e7f3f`; extracted XML SHA-256 `643987abce5a08925a9ecba818036c6bd5a12ad95ce2ba2ec8f786051ac36006`. Exact testcase records reused from complete XML inventory gzip SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`.
- Retrieved the original hosted job log, 2026-11-16 22:49:46–22:49:47 UTC. The full failure commands appear in the XML and log. Log prints `fatal: path 'runtime_protocol/schemas/timeline-commit-bundle.json' exists on disk, but not in '34eac0041b0891e9011966b39bcbd26053fde5bc'` and the corresponding message for `astrid/sdk/timeline/native_parent_media_commands.py` at `c36ca8c...`. **This Git diagnostic alone does not establish that the historical file is absent upstream**: it also occurs when the named historical object is missing locally.

## Two complete literal XML-message groups

**Six failures**, message SHA-256 `de56bca83fd20b6e25f59a9bf373e2200232ed9992598e47a92760a19a64470a`:

```text
subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'show', '34eac0041b0891e9011966b39bcbd26053fde5bc:runtime_protocol/schemas/timeline-commit-bundle.json']' returned non-zero exit status 128.
```

Exact red testcase IDs (class prefix `tests.editing_conformance.test_prepared_video_birth::`):

- `test_normalized_production_video_birth_and_guarded_inverse[4]`
- `test_normalized_production_video_birth_and_guarded_inverse[None]`
- `test_normalized_production_video_birth_and_guarded_inverse[absent]`
- `test_normalized_production_video_birth_and_guarded_inverse[0.02]`
- `test_frozen_request_envelope_rejects_unknown_fields[unexpected]`
- `test_frozen_request_envelope_rejects_unknown_fields[idempotency_key]`

**One failure**, message SHA-256 `0caf5260f5e7c8fd2406c2e8281dc0aca01027db53608aa7c6667e6ba512dee2`:

```text
subprocess.CalledProcessError: Command '['git', 'show', 'c36ca8c94b695b0e25b7d42c89f194661f187423:astrid/sdk/timeline/native_parent_media_commands.py']' returned non-zero exit status 128.
```

Exact red ID: `tests.editing_conformance.test_prepared_video_birth::test_literal_after_insert_request_is_identical_on_c36_and_new`.

## Source and cause

At the exact Agent head, `tests/editing_conformance/test_prepared_video_birth.py` uses `frozen_validator()` to read *both* frozen Runtime schema revisions `34eac0041b0891e9011966b39bcbd26053fde5bc` (PRODUCER) and `8ea0766f5e9fb23cea26c7398770a8aaac06b258` (RUNTIME), and uses `git show` at Agent historical `c36ca8c94b695b0e25b7d42c89f194661f187423` for frozen parent-media source. The unit-shard job's standard `actions/checkout@v4` steps fetch only the pinned Agent/Runtime HEADs; no explicit old-history fetch exists in the tested workflow.

GitHub source reads at all **three exact historical commit refs** returned the named files: the two Runtime schema sources each resolve to blob `252f71f0acdc94db3a2b0dabec70b249877fb131`; Agent source resolves to blob `433f94a1b3a4f1a5f9bd2aa5c4fa5d344231a557`. That supports **missing local history/provisioning** over a changed contract as the first prerequisite diagnosis. The exact local `cat-file` state in the original runner was not recorded, and no post-fetch product outcome is presumed.

## Isolated candidate and acceptance hold

[Agent draft PR382](https://github.com/banodoco/astrid-agent/pull/382), head `53054252477e57b6666e7c96ae0b08e97f0c20c6`, exact base `6bbda788`, makes a **single workflow-file, unit-shard-only** change: fetch all three exact historical objects and verify commit and named source through `git cat-file` and real `git show`, without changing current checkout HEAD, Runtime lock, any test oracle/assertion, skips, xfails, or product implementation. The authentic origin is used; no synthetic files are substituted.

**Proof limits:** source-identity checks and diff inspection only. No worker environment execution, authentic candidate `git fetch`, focused test, or hosted candidate JUnit XML has been obtained. Route: **N direct source/log/XML diagnosis and bounded candidate**, separately delegated model identity unavailable/not invented. Independent submitted N review: **zero at opening**; PR remains draft, unmerged; no claimed seven passes and no authority to merge without a reviewer and hosted proof. No prior baseline exact-testcase comparison was repeated in this checkpoint; no regression is inferred from a missing old ID.

This draft changes the same workflow as draft PR376's *different* release-0 archive prerequisite, so their two **non-overlapping patches must be composed and reviewed as one candidate before any integration**; do not overwrite one with the other or claim either hosted-qualified. Existing Agent PR373–378 likewise remain draft/unaccepted.

## Run boundaries preserved

Both exact-head attempt-1 workflows remain complete with failures: CI **882F/398E**; Lanes [43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) **306F (including 12 opt-in log-only)/260E**. Their prior complete-job summary, message counts, original artifact IDs and hashes, and exact-ID comparisons are retained, not overwritten.

Plan 38 / Plan 55 ownership **WAITING**; Release 15 excluded. Runtime clip patch stays **uncommitted 25P/2F** awaiting an owner decision on exact retry after corrupt required CAS history versus later integrity validation; no assertions, history guard or contract changed. Runtime draft PR56 is orphan declaration metadata only. Formal G1/G2 acceptance incomplete and RS1 **0/1**. No existing workflow cancelled, rerun, manually dispatched or authenticated anew; no `release/14/main`, public `main`, `inputs.md`, or plan task-checkbox write.
