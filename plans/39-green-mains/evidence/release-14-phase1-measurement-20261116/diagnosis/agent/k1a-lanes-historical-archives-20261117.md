# K1 / AE2 prerequisite: two absent historical archive trees in Agent Lanes

**2026-11-17 UTC · route N · source/hosted-log and actual-XML analysis, plus an isolated draft workflow candidate.** No independent review, local execution, hosted qualification of the candidate, or product acceptance. The prior exact-head run is complete, but the formal G1/G2/RS1 gates remain incomplete.

## Exact source and hosted evidence

- Agent `release/14/plan-39` at `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`, reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`; Lanes [run 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160), attempt 1, completed failure. CI [run 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) likewise completed failure; neither was rerun/cancelled.
- Affected [integration shard 4 job 133651923157](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923157), 516 actual JUnit testcases, **99 failures, 26 errors, zero skips**. Its actual [artifact 14282352655](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14282352655) is preserved in the complete previously verified XML inventory. Artifact ZIP SHA-256 `35038fc7b78af32315598829f361e6e790d74baf20fca25b9b2608ac5bc46b8d`; inner `integration.xml` SHA-256 `af5f41519f22ba1434ef74a6e28f62f5b4c6fdd6ea7fb0ae238aa6ea79db49da`. The complete immutable XML inventory ZIP/message names and testcase IDs are in [the existing shard completion report](../../agent/merged-head-6bbda788/completed-lanes-shard3-20261117.md) and run state. Local complete-inventory gzip SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426` was rechecked.
- The **real 4.8-MB job log** was retrieved again; its failure detail includes literal `fatal: not a tree object: 6d53a19070faf63fc15ae1f81417722edc2c8a5f` and `fatal: not a tree object: 0e1543e0da2215db9cb3320cfd1083174c3c62a9`. Thus `git archive` returned 128 on the actual hosted checkout **before historical assertions ran**. The historical commits resolve through GitHub in their respective upstream repositories; this does not itself prove that a future hosted fetch succeeds.

### Exact red testcases (13, no IDs inferred)

One Runtime history object causes **10** actual XML red records, of which nine are setup **errors** and one is a test **failure**:

- `tests.upgrade.test_busy_fixture_creation::test_creation_and_reconciliation_preserve_existing_data[6d53a19070faf63fc15ae1f81417722edc2c8a5f-none]`
- Same full prefix with `-create`, `-claim`, `-heartbeat`, `-output`, `-nonzero` and `-timeout` (seven exact parameter IDs, all error).
- `tests.upgrade.test_busy_fixture_creation::test_release_rolls_back_partial_settlement[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` (error).
- `tests.upgrade.test_busy_fixture_creation::test_creation_error_remains_primary_and_retry_reconciles[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` (error).
- `tests.upgrade.test_busy_fixture_release::test_release_fails_closed_and_preserves_unrelated_work[6d53a19070faf63fc15ae1f81417722edc2c8a5f]` (failure).

The first nine have **one literal XML error message with count 9**, SHA-256 `6efcc4c3053bfb250cac33b326fbe83d995e590a1ad4079c5c6b95e884b1e7f3`:

```text
failed on setup with "subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'archive', '6d53a19070faf63fc15ae1f81417722edc2c8a5f']' returned non-zero exit status 128."
```

The tenth has **one literal failure message with count 1**, SHA-256 `d9cf0a6bcfc0863f24351de5fa3bfd32023c7a879ad398928864a0f2174d5d23`:

```text
subprocess.CalledProcessError: Command '['git', '-C', '/home/runner/work/astrid-agent/astrid-agent/astrid-runtime', 'archive', '6d53a19070faf63fc15ae1f81417722edc2c8a5f']' returned non-zero exit status 128.
```

A separate Agent history object causes **three** actual XML setup **errors**:

- `tests.test_bootmanifest2_admission::test_busy_rejected_attachment_preserves_r12_resident_reader`
- `tests.test_bootmanifest2_rollback::test_real_rollback_activates_r12_own_composition[False]`
- `tests.test_bootmanifest2_rollback::test_real_rollback_activates_r12_own_composition[True]`

Their **one literal XML error message, count 3**, SHA-256 `069921f216b966aa60a412f58015552383c74d2401b566d4fba7089c95b14fa0`:

```text
failed on setup with "subprocess.CalledProcessError: Command '['git', 'archive', '0e1543e0da2215db9cb3320cfd1083174c3c62a9']' returned non-zero exit status 128."
```

The two causes together account for **13 red testcase occurrences in three distinct full literal XML messages** in a single completed job, *not* 13 independent product defects. They are retained inside the original shard totals; do not add them a second time to global failures. No previous-plan or frozen G1 comparison for these exact 13 IDs was made here, and absence of any old ID is **not** regression evidence.

## Source trace and isolated N-class candidate

1. [Lanes workflow at tested head](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/.github/workflows/lanes.yml#L77-L108) checks out Agent and Runtime at depth 1 and fetches selected historical Agent and Runtime objects, but **neither** `0e1543e0...` nor `6d53a190...`. It verifies the Runtime lock and `efcb326...`, not these source trees.
2. [Historical busy creation fixture](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/upgrade/test_busy_fixture_creation.py#L13-L31) and [release test](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/upgrade/test_busy_fixture_release.py#L14-L23) deliberately archive Runtime `6d53a190...` to exercise historical busy-realm safety.
3. [R12 archive fixture](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/helpers/bootmanifest2_r12.py#L8-L22) deliberately archives Agent `0e1543e0...` for resident provenance tests. Both upstream commit identifiers are accessible as [Runtime source](https://github.com/banodoco/astrid-runtime/commit/6d53a19070faf63fc15ae1f81417722edc2c8a5f) and [Agent source](https://github.com/banodoco/astrid-agent/commit/0e1543e0da2215db9cb3320cfd1083174c3c62a9).
4. Isolated draft [Agent PR374](https://github.com/banodoco/astrid-agent/pull/374), task branch `p39/ae2-historical-archives-20261117`, candidate commit `c815db3f44939df23a65a1c5520a9844e167ad0c`, adds just those two exact fetch SHA values and checks that the object commit and tree identities are available before running tests. One workflow file changed; no source/test/assertion/fixture changes. Base remains the exact reviewed head `6bbda788`. The PR is **draft/unreviewed/unmerged**, has **no local focused execution or hosted candidate result**, and is **not ready for promotion**. File patch and PR state were read back after creation.

**Ownership/scope distinction:** This is only Agent CI history availability under Plan 39's AE2/K1 prerequisite lane. It does not rewrite the pinned historical source, relax its safety assertions, or claim that those tests pass once their source becomes readable. The separate historical Runtime `df3d4dd...` tests belong to GenericPackHost short leases and overlap Plan 55's waiting ownership: intentionally **excluded** from PR374 pending clearance. The Runtime clip replay-versus-CAS integrity decision and its uncommitted 25P/2F patch are untouched. Plan38/55 remain WAITING; Release15 excluded.

**Required gates before PR374 can merge:** independent N-class review (record actual route/model provenance), worker-environment source/check and focused prove-or-fail `git fetch` + `git archive` identity tests, then after *independently approved* integration a real hosted Lanes shard 4 run with all 13 same IDs executed past setup and its actual XML+hashes. There is **no license to dispatch or rerun existing workflows**, no acceptance advance, and no RS1 review credit. Agent PR373 Windows selector remains separately draft/unreviewed with no hosted Windows exact-ID proof.
