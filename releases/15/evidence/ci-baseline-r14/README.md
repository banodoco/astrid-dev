# Release 14 reference sets for the Runtime and the App (24 November 2026)

What fails in each repository's hosted CI on the published Release 14 head, so the Release 15 candidate can be compared with it whole run to whole run, by test id, from full job logs ([qualification bar](../../qualification.md), Tier 1 item 1). The Agent's set is in [agent-ci-baseline-8807f820](../agent-ci-baseline-8807f820/README.md).

| | Release 14 head | CI run | Result |
| --- | --- | --- | --- |
| astrid-runtime | `5120462d67479dc4719406d0d34440edb616ace1` (`release/14/main`) | [44996701468](https://github.com/banodoco/astrid-runtime/actions/runs/44996701468) | failure: 5 of 10 jobs red |
| astrid-app | `e0da794ac9d26a808ab4082b29f60408b66b3a4c` (`main`) | [45028860223](https://github.com/banodoco/astrid-app/actions/runs/45028860223) (the same commit on `release/14/main`: [45023090092](https://github.com/banodoco/astrid-app/actions/runs/45023090092)) | success: every job green |

## Runtime

[runtime-release-14-5120462d-failing-ids.tsv](runtime-release-14-5120462d-failing-ids.tsv): 1,466 rows (`outcome`, `job`, `id`), 508 distinct ids. Read from the full logs of the five red jobs with `env/baseline-diff.py`'s own parser; no log was truncated or cancelled; the only failing step in each job is its pytest step.

| Job | pytest's final line | Rows |
| --- | --- | --- |
| unit (ubuntu-latest) | 112 failed, 9209 passed, 26 skipped, 13 xfailed, 367 errors | 478 |
| unit (macos-latest) | 110 failed, 9107 passed, 130 skipped, 13 xfailed, 367 errors | 477 |
| sandbox-process-control | 125 failed, 9116 passed, 26 skipped, 13 xfailed, 371 errors | 496 |
| portability-lifecycle (ubuntu-latest) | 7 failed, 610 passed, 45 skipped | 7 |
| portability-lifecycle (macos-latest) | 8 failed, 595 passed, 59 skipped | 8 |

- **One row short.** unit (ubuntu-latest) lists 478 ids where pytest counts 112 + 367 = 479; one id appears twice in pytest's own count or is a subtest. Not yet traced; a whole-run comparison by id cannot be hurt by it, a count comparison can.
- **Against Plan 39's Release 15 measurement** ([runtime-failing-ids.tsv](../../../../plans/39-green-mains/evidence/release-15-measure/runtime-failing-ids.tsv), `24e2c929`, union over jobs, outcome and job ignored): 507 ids fail on both; one is only on Release 14 (`tests/test_timeline_headless_overwrite_refused.py::test_original_trackless_authored_payload_with_verified_media_is_invalid_untouched`); one is only in Plan 39's file (`check_it.py::test_gap`, which looks like a helper's stray row, not a test of the Runtime). That comparison is by a different measurer on a different head, so it is context, not the Release 15 comparison; the qualification run compares the frozen head's own full logs with this file.
- The Runtime's CI has more jobs than the five that fail (Windows realm publication, boundary, darwin-native, typescript-client): they pass on Release 14 and must pass on the candidate.

## App

The App's `vitest` job runs `npm test` in one step and its log does not name single tests: vitest's default reporter prints each **file** with its test count, and names a test only when it fails (or is slow). So the App cannot be compared test by test from the log. [`scripts/qualification/app_test_ids.py`](../../../../scripts/qualification/app_test_ids.py) closes the gap as far as the log allows:

- `extract JOB.log` writes every test file with its test, failed and skipped counts, every failing test by its full name, and the totals of each vitest run in the job (`npm test`, then the `sdk-boundary` run).
- `diff BASE.tsv CAND.tsv --strict` exits 1 on a new failing test, a file newly failing, a file that has disappeared, or a file with fewer tests than on Release 14 (a lost id counts as red until explained).

[app-release-14-e0da794a-vitest-counts.tsv](app-release-14-e0da794a-vitest-counts.tsv): 1,453 files, 21,384 tests, 0 failing, 0 skipped; the per-file counts sum to the 21,384 in vitest's own totals line. The second run in the log (`sdk-boundary`) is 1 file, 335 tests. The job also runs `node --test` steps (`release-tooling-macos`, 18 tests in the vitest job's `release.test.mjs` step), which print their own `# tests / # pass / # fail` totals.

**Limits of the App reference:** a test renamed inside a file, or one removed and another added, keeps the file's count the same and is not seen. A Playwright (`e2e`, `direct-journey`) failing id is named in its own log and is compared by name. If a later step needs true per-test ids, vitest's `--reporter=json --outputFile` in `test.yml` is the repair; that changes a workflow in a release branch, so it goes to the Lead first, and it is not required for Release 15.
