# Agent CI 43934820640 — exact-head prior-plan baseline

## Provenance

- Repository: `banodoco/astrid-agent`; run 43934820640, attempt 1, branch `release/14/plan-39`.
- Head: `b8f2692948d1b5987ee2938920f47aace0732792`.
- Run conclusion: failure. This is a measurement, not acceptance or RS1 proof.
- The nine failed jobs are eight Ubuntu unit shards and the macOS `darwin native` job. XML artifacts for all nine were downloaded and SHA-256 verified against the saved GitHub artifact metadata.
- Eight raw logs were available. Shard 6 job 133536534814 log access returned the saved `Transport closed` error; no retry was made. Artifact 14266922439 XML is the sole outcome source for that shard.

## Failed-job summary

| Job | Job ID | Tests | Failed | Errors | Skipped | Direct testcase records | Subtest/test delta | Log |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| unit shard 1 / 8 (ubuntu-latest) | 133536534737 | 5475 | 44 | 54 | 3 | 5322 | +153 tests, +0 failures | available |
| unit shard 2 / 8 (ubuntu-latest) | 133536534935 | 4039 | 81 | 51 | 19 | 4013 | +26 tests, +0 failures | available |
| unit shard 3 / 8 (ubuntu-latest) | 133536534765 | 1861 | 31 | 0 | 0 | 1861 | +0 tests, +0 failures | available |
| unit shard 4 / 8 (ubuntu-latest) | 133536535002 | 2061 | 28 | 19 | 0 | 2061 | +0 tests, +0 failures | available |
| unit shard 5 / 8 (ubuntu-latest) | 133536535000 | 2416 | 95 | 107 | 0 | 2416 | +0 tests, +0 failures | available |
| unit shard 6 / 8 (ubuntu-latest) | 133536534814 | 5287 | 247 | 4 | 6 | 5162 | +125 tests, +30 failures | XML only |
| unit shard 7 / 8 (ubuntu-latest) | 133536534843 | 6008 | 250 | 160 | 2 | 5895 | +113 tests, +0 failures | available |
| unit shard 8 / 8 (ubuntu-latest) | 133536535034 | 4114 | 97 | 2 | 25 | 3912 | +202 tests, +0 failures | available |
| darwin native | 133536535052 | 55 | 13 | 1 | 0 | 55 | +0 tests, +0 failures | available |

The `Tests` and failure/error/skipped totals come from the JUnit suite counters. Direct testcase records may omit subtests. Across shards, root JUnit `tests` exceeds testcase elements by the aggregate test-count delta; shard 6 also has 30 more root failures than direct failure testcase records, so at least 30 failing subtests have no individual XML testcase IDs.

Combined across the nine XML artifacts: 31,316 JUnit tests, 886 failures, 398 errors, 55 skipped, and 29,977 pass by residual. There are 30,697 direct `<testcase>` elements; the 619 root-test delta consists of subtests reflected only in the aggregate suite counters.

## Other job status

The saved run metadata lists 16 jobs: 9 failures, 5 successes, and 2 skipped jobs. These seven nonfailed jobs are summarized from metadata only; no additional artifacts were downloaded for them.

| Job | Job ID | Status | Conclusion |
|---|---:|---|---|
| windows-native-and-installer | 133536534486 | completed | success |
| fast checks | 133536534666 | completed | success |
| release wheel / Python 3.11 | 133536534779 | completed | success |
| boundary | 133536534800 | completed | success |
| release wheel / Python 3.12 | 133536534896 | completed | success |
| landing reference | 133536537291 | completed | skipped |
| unit | 133612796426 | completed | skipped |

## Ownership and triage method

- Complete per-job Markdown files list every distinct exact JUnit failure/error `message` value, count, outcome mix, testcase IDs, plus summary messages where raw logs exist. Per-job JSON retains the full JUnit detail text and testcase IDs.
- `failed-outcomes.json` contains the full 1,254 direct failed/error testcase records with exact IDs, literal JUnit messages, full XML detail text, G1 recurrence mapping, and exact-owner status. `testcase-index.json` contains all 30,697 direct testcase IDs and statuses.
- Prior G1 evidence contained 1,239 unique red test IDs across summary and audited tables; 1,169 current red IDs recur there and 85 are absent from the prior red ledger. G1 summary rows do not provide triage ownership; G1 audited Agent rows mark explicit Plan 55 ownership holds for a subset.
- Plan 38 has no exact selector match in current red records. Eight exact current-red IDs are marked WAITING in the G1 audited Plan 55 table; these remain unresolved pending ownership confirmation. Broad directory or task-family overlap is not assigned. This report does not authorize edits.
- Shard 6 XML has 5,162 direct testcase records, 247 root failures, 4 root errors, and 6 root skips. It therefore shows +125 root test records beyond testcase nodes and +30 failures beyond direct failure testcase nodes. Because the log is unavailable, the XML does not identify the individual subtest IDs or any raw pytest-only summary fields such as deselected count.
- Formal RS1 remains unverified; do not claim phase-1 acceptance.

## Files

- `xml-artifacts/`: all nine downloaded ZIPs and extracted XML.
- `jobs/`: per-job Markdown and JSON for every failed job.
- `failed-outcomes.json`: complete red testcase ledger.
- `testcase-index.json`: every direct XML testcase ID and outcome.
- `measurement.json`: run/job status, hash verification, aggregate reconciliation, and ownership limits.
- `artifacts.json`, `run-metadata.json`, `jobs-attempt-1.json`, and saved raw logs are original metadata/evidence.
