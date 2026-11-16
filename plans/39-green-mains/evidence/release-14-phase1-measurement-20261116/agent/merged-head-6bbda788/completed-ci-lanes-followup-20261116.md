# Agent PR369 merged-head qualification: completed CI, incomplete Lanes (2026-11-16 23:49 UTC)

**Provisional G2 evidence only. Formal G1/G2 and phase-1 acceptance remain INCOMPLETE; RS1 0/1.** Agent exact plan-branch commit `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`, reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`. Both workflow runs are **attempt 1**, with GitHub artifact metadata matching that head SHA. No runs were cancelled or rerun. This adds to [the earlier checkpoint](partial-qualification-20261116.md), not to frozen G1.

**Run states:** [CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) completed **failure**; 8/8 unit shards plus Darwin failed, the aggregate `unit` job failed, fast checks/boundary/Windows native/release wheels 3.11 and 3.12 **passed**, and landing reference was skipped. [Lanes 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) was **in progress**: opt-in and integration shards 1, 2 and 4 failed, installed wheel passed, integration shard 3 still running. Do not invent its summary or XML.

## Exact outer pytest summary lines for every finished failing test job

These are the terminal summary lines extracted from each *completed* attempt-1 job log, separate from XML test-count totals. The still-running Lanes shard 3 has no outer summary yet.

| Job | Literal outer summary (minus GitHub log timestamp and delimiter) |
|---|---|
| CI Darwin | `14 failed, 40 passed, 30933 deselected, 2 warnings, 1 error in 437.15s (0:07:17)` |
| CI unit 1 | `43 failed, 5227 passed, 3 skipped, 26182 deselected, 346 warnings, 54 errors, 153 subtests passed in 5474.98s (1:31:14)` |
| CI unit 2 | `80 failed, 3862 passed, 19 skipped, 27497 deselected, 2 warnings, 51 errors, 26 subtests passed in 3587.11s (0:59:47)` |
| CI unit 3 | `31 failed, 1834 passed, 29644 deselected, 2 warnings in 2099.38s (0:34:59)` |
| CI unit 4 | `28 failed, 2007 passed, 29455 deselected, 2 warnings, 19 errors in 3514.64s (0:58:34)` |
| CI unit 5 | `95 failed, 2213 passed, 29094 deselected, 10 warnings, 107 errors in 2369.72s (0:39:29)` |
| CI unit 6 | `247 failed, 4943 passed, 6 skipped, 26342 deselected, 59 warnings, 4 errors, 92 subtests passed in 4983.60s (1:23:03)` |
| CI unit 7 | `250 failed, 5636 passed, 4 skipped, 25459 deselected, 2 warnings, 160 errors, 113 subtests passed in 3470.90s (0:57:50)` |
| CI unit 8 | `94 failed, 3668 passed, 23 skipped, 27722 deselected, 5 warnings, 2 errors, 202 subtests passed in 1638.02s (0:27:18)` |
| Lanes opt-in | `12 failed, 19 passed, 30959 deselected, 2 warnings in 189.62s (0:03:09)` |
| Lanes integration 1 | `37 failed, 479 passed, 31868 deselected, 13 warnings in 1095.70s (0:18:15)` |
| Lanes integration 2 | `77 failed, 267 passed, 31868 deselected, 22 warnings, 172 errors in 1870.91s (0:31:10)` |
| Lanes integration 4 | `99 failed, 391 passed, 31868 deselected, 9 warnings, 26 errors in 4719.75s (1:18:39)` |

Actual downloaded ZIPs and decompressed JUnit XML were independently SHA-256 checked. ZIP hashes agree with GitHub's recorded `sha256:` digests. The JUnit totals are **tests/failures/errors/skipped**, not unique failure causes; full literal messages are grouped per job by exact XML `message` string, including differences in multiline text. Subtests in pytest `tests` totals do not always have separate XML testcase IDs.

| Finished job | JUnit T/F/E/S | Distinct full XML literal messages | Actual artifact ID | ZIP SHA-256 | Inner XML SHA-256 |
|---|---|---:|---|---|---|
| CI darwin native [133651924059](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924059) | 55 / 14 / 1 / 0 | 12 | [14277714424](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14277714424) | `06a2bac5da6c594ded3ca0f5dec3f0237fc6d02bff165cebd39d39450c386df0` | `07bd706c3faced716a9a421820e8da6a2bddf099af6fdc7d1347fa574483b984` |
| CI unit 1/8 [133651924807](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924807) | 5480 / 43 / 54 / 3 | 34 | [14283258791](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14283258791) | `48d274a24fd1e823308b1783b0c345e70eb816bb8e93f278fc013a70310a487e` | `76fe167a3fecc8f534aeb9e2fe1542df83c28fb944de1662e7cc30706fb0cab8` |
| CI unit 2/8 [133651924632](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924632) | 4038 / 80 / 51 / 19 | 104 | [14282895123](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14282895123) | `09aef837e988828d0d8d808d669e4329f7e31773b5d501c69a48f9f070534a5a` | `7e701bf709f938713eddbcbd0755e3339c86c95da69e821976ccdf9bb916891e` |
| CI unit 3/8 [133651924518](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924518) | 1865 / 31 / 0 / 0 | 10 | [14279162456](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14279162456) | `6bb5af87d04b19801da97ecb6b109238d3e321979f0ec3fd40838ce1771e7f3f` | `643987abce5a08925a9ecba818036c6bd5a12ad95ce2ba2ec8f786051ac36006` |
| CI unit 4/8 [133651924745](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924745) | 2054 / 28 / 19 / 0 | 22 | [14282820153](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14282820153) | `2acb279263d68ae27adb9a008e0e0d610dc9bf4662c40fb2c6645cf7bdbe1cf7` | `63ea09f25b19ec3267f75f37d07a4fc0af9b122117fd956fa90a49e44b508008` |
| CI unit 5/8 [133651924751](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924751) | 2415 / 95 / 107 / 0 | 32 | [14280895809](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14280895809) | `0794ad36aecedac140e209565055f10a1be0897d868d904d75c17b719e150ecf` | `c23191801822c359feb5117e8d123e2c44e5e7152168721431ab12c8ab6cf8dd` |
| CI unit 6/8 [133651924641](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924641) | 5292 / 247 / 4 / 6 | 162 | [14283023095](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14283023095) | `74811e80afd29518a356b8f2dd4b4794b4a34f5ea375412dc5ad11cab0ea7d47` | `b397f917a9ef5f01734ff06fcaeb7b7e39d8a35d3064f4d610977fc97168f89a` |
| CI unit 7/8 [133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616) | 6163 / 250 / 160 / 4 | 110 | [14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130) | `3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a` | `3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b` |
| CI unit 8/8 [133651924880](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924880) | 3989 / 94 / 2 / 23 | 63 | [14278249808](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14278249808) | `035eb0316e0ca3b3294b4eeb5ac205d78bdd0ce754b86628d090fd253ca7d891` | `adb00f44093c9f0656c1b050b4e712e83a5e31203fd72f89224af0d598885c42` |
| Lanes integration 1/4 [133651923670](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923670) | 516 / 37 / 0 / 0 | 6 | [14277479708](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14277479708) | `33674c246e51d362e7b526f7a8f38ff643b2585a6272e39d9efd949c8d2b571f` | `94fb374cce6ea7e5694fe4cb48ec7ce51bdc519a7de437f425e89568f00c4055` |
| Lanes integration 2/4 [133651924063](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651924063) | 516 / 77 / 172 / 0 | 51 | [14278972799](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14278972799) | `4f26e9f301570707244087dfa9e65b13b2966daa1d1539fbf3c2f3a07829714e` | `17f03f1f12be6a7809a310d29f822aa12997cb0cd049252cd7ab77a9cb246991` |
| Lanes integration 4/4 [133651923157](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923157) | 516 / 99 / 26 / 0 | 55 | [14282352655](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14282352655) | `35038fc7b78af32315598829f361e6e790d74baf20fca25b9b2608ac5bc46b8d` | `af5f41519f22ba1434ef74a6e28f62f5b4c6fdd6ea7fb0ae238aa6ea79db49da` |

The completed **CI failing XML jobs** total **31,351 tests, 882 failures, 398 errors, 55 skips**, across 9 failing jobs and **549 per-job full-literal message groups** (not unique root causes). The finished Lanes integration XML shards 1, 2 and 4 total **213 failures and 198 errors**, while opt-in adds **12 failed log cases** without an available first-page JUnit artifact. The incomplete Lanes shard 3 is excluded from totals.

## Exact testcase-ID transitions (against prior-plan job artifact, not baseline cutoff)

Exact identity is `(classname,name)` in the corresponding prior-plan job's actual JUnit. Missing old/current IDs mean shard-membership drift, never automatically regression.

| Job | Shared exact IDs | Transitions and membership changes |
|---|---:|---|
| CI Darwin | 55 | 40 P→P, 13 F→F, 1 E→E, **1 P→F**: text-card reconciliation timeout |
| CI unit 1 | 5,322 | 5,221 P→P, 43 F→F, 54 E→E, 3 S→S, **1 F→P**; current-only 5 passes |
| CI unit 2 | 4,008 | 3,856 P→P, 79 F→F, 51 E→E, 19 S→S, **2 F→P, 1 P→F**; old-only 5 passes, new-only 4 passes |
| CI unit 3 | 1,857 | 1,826 P→P, 31 F→F; old-only 4 passes, new-only 8 passes |
| CI unit 4 | 2,053 | 2,006 P→P, 28 F→F, 19 E→E; old-only 8 passes, new-only 1 pass |
| CI unit 5 | 2,415 | 2,213 P→P, 95 F→F, 107 E→E; old-only 1 pass |
| CI unit 6 | 5,162 | 4,935 P→P, 217 F→F, 4 E→E, 6 S→S; current-only 5 passes. **30 aggregate failing subtests lack distinct testcase IDs**, so 247 XML failures do not imply 247 distinct failing testcase identities |
| CI unit 7 | 5,890 | 5,478 P→P, 249 F→F, 160 E→E, 2 S→S, **1 F→P**; old-only 5 passes; current-only 160 IDs (157 passes, 2 skips, **1 failure**): not a proven regression |
| CI unit 8 | 3,752 | 3,631 P→P, 94 F→F, 2 E→E, 23 S→S, **2 F→P**; old-only 160, new-only 35 (different shard membership) |
| Lanes integration 1 | 516 | 479 P→P, 36 F→F, **1 P→F**: bridge fd flags |
| Lanes integration 2 | 516 | 266 P→P, 77 F→F, 172 E→E, **1 F→P** |
| Lanes integration 4 | 516 | 391 P→P, 99 F→F, 26 E→E; no transitions |

This totals **seven shared previously red exact IDs now passing** and **three shared previously passing exact IDs now red**, across compared completed jobs. Neither direction is attributed to PR369 solely from the run comparison. Full error-string groups are **549 CI + 112 completed Lanes integration groups**; opt-in errors are log-only and explicitly separate. The raw JUnit ZIPs above preserve all literal messages. Prior supplementary evidence covers the earlier jobs' first-line/error counts.

## New exact-red cases and ownership triage

1. **CI unit 2:** `tests.core.generation.test_readiness_missing_models::test_list_and_defaults_agree_when_files_are_missing` changed exact P→F. Actual literal mismatch: `'no attached ComfyUI target or model probe unavailable'` versus `'required models missing or ambiguous'`. Two other tests in the same module changed F→P, suggesting setup/readiness variation rather than proving a product regression. This exercises the attached-ComfyUI generation family adjacent to Plan 55's owned target/lane inventory; **keep WAITING pending explicit ownership/provisioning assessment**; do not relax the readiness assertion.
2. **Darwin:** exact `test_text_card_render_smoke` P→F, `RendererInternalError` reconciliation deadline, previously recorded; needs repeat/source investigation before assigning regression cause.
3. **Lanes integration 1:** exact `test_host_bridge_outer_send_diagnostic_preserves_revoke_close[False]` P→F, `AssertionError: assert 2049 == 1` (fcntl flags), previously recorded; generic host is a Plan 55 inventory overlap. Preserve revoke/close controls.
4. **Unit 7 current-only one failing test** cannot be called a new regression without a shared old ID or cross-job lookup.

Further clusters visible in the literal messages: unit 1 has **45** setup messages `ModuleNotFoundError: No module named 'tests.test_verified_host_launch'` and **8** RunPod lifecycle checkout failures; unit 2 has **50** missing pinned Node/esbuild setup messages; unit 4 has **16** source SHA mismatch setup messages; unit 5 has **33** missing `ASTRID_REMOTION_PROJECT_DIR` setup messages and **32** lambda-argument setup errors; unit 6 has **13** missing `scripts/pod_bootstrap.sh` records and **9** `SystemExit: 2`; unit 7 has **92** Runtime site-packages-vs-checkout setup mismatches and **68** source SHA mismatch setup messages; integration 4 includes **14** `pytest-timeout` 120s errors and **12** selected-PARAM-authority errors. These are counts of literal XML first-line prefixes and may involve distinct underlying full strings. They are **not** 16/33/etc independent product causes. See real XML artifact links for all full messages; no truncated traceback is passed off as exhaustive literal evidence.

## Independent K1a prerequisite candidate

Hosted [Windows job 133651924610](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924610) passed **112 actual testcases**, but omitted both native owner-lock and ACL/hardlink exact security test IDs. This selector omission is proven by downloaded JUnit and source. Prepared **N-class isolated draft [Agent PR373](https://github.com/banodoco/astrid-agent/pull/373)** on `p39/k1a-windows-native-coverage-20261116` at `80e748fff9d41a1e33728c49d81832df12eb0773`: only adds both exact pytest selectors to existing Windows job and replaces their platform skipif with registered `windows_native` marker; retains all behavior assertions. **Unmerged, unreviewed, not hosted-qualified.** Hardlink-unsupported direct `pytest.skip` remains a separate blocked capability judgement. PR needs independent review, focused/policy proof, and real integrated Windows job proving both IDs run and pass. Do not treat a green PR status as qualifying that push-only job.

## Other holds and next checkpoint

Runtime strengthened clip port remains **uncommitted 25P/2F** because old-media corruption replay conflicts with the later CAS-history integrity guard: **no contract change, assertion relaxation, or replay bypass** without explicit owner decision. Runtime draft PR56 is orphan-declaration metadata only. **Plan 38 and Plan 55 remain WAITING; Release 15 excluded. G1/G2 not accepted; RS1 0/1.** No input changes, task-checkbox edits, release/14/main push, public-main push, product merge, auth retry or manual workflow dispatch.

**Next bounded step:** capture completed Lanes integration shard 3 job log and real XML on the *same* run attempt/head; compare with prior-plan shard 3 actual XML but mark missing frozen G1 shard-3 evidence as unavailable; then reconcile Lanes total and verify PR373 independent-review/proof gates. Do not rerun or cancel other sessions' jobs.