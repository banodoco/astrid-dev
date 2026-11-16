# Runtime CI 43954031461 — provisional post-batch measurement

Exact head `359e2d7e55369562ca9513557282ea8aff7645bc`, tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`, attempt1. Prior comparable CI43938386357 at4fe2c0b. Five failed jobs, **1489 failure/error records** and **166 per-job distinct full literal-message groups**. All five actual XML archives verified against GitHub SHA-256 metadata; every failure/error ID matches the raw log.

| Job | Job ID | Complete pytest summary | Message groups |
|---|---|---|---:|
| portability-lifecycle (ubuntu-latest) | [133603709482](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/133603709482) | 7 failed, 610 passed, 45 skipped in 44.07s | 7 |
| unit (ubuntu-latest) | [133603709490](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/133603709490) | 119 failed, 9050 passed, 26 skipped, 13 xfailed, 367 errors, 60 subtests passed in 806.59s (0:13:26) | 49 |
| sandbox-process-control | [133603709503](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/133603709503) | 132 failed, 8957 passed, 26 skipped, 13 xfailed, 371 errors, 60 subtests passed in 1033.01s (0:17:13) | 55 |
| portability-lifecycle (macos-latest) | [133603709524](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/133603709524) | 8 failed, 595 passed, 59 skipped in 56.28s | 8 |
| unit (macos-latest) | [133603709671](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/job/133603709671) | 118 failed, 8947 passed, 130 skipped, 13 xfailed, 367 errors, 60 subtests passed in 1140.82s (0:19:00) | 47 |

The other jobs: boundary, typescript-client, windows-realm-publication and darwin-native passed; landing reference was skipped. Exact statuses are retained in jobs-attempt-1.json.

## Same-ID comparison

All five jobs have identical testcase ID sets to their corresponding previous jobs: **True**. Counts below count job occurrences, so the same test on several platforms is counted several times.

| Prior -> current | Count |
|---|---:|
| error->error | 1105 |
| error->failure | 186 |
| error->passed | 1230 |
| failure->failure | 198 |
| failure->passed | 54 |
| passed->passed | 26875 |
| skipped->skipped | 286 |
| xfailed->xfailed | 39 |

A prior error that now reaches a failing assertion is newly exposed behavior, not automatically a product regression. Changed-testcases.json contains every exact changed ID and both messages. The paired per-job Markdown/JSON reports contain all literal messages with counts and triage or new, including ownership holds.

## Artifact reconciliation

| Job ID | Artifact ID | Archive SHA-256 | XML tests | Testcase records | Passing subtests without separate elements |
|---|---|---|---:|---:|---:|
| 133603709482 | [14269247265](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/14269247265) | `589b291e350968f12af548beeb5f61edccd006fbdbb64331cc05ce07ead64daa` | 662 | 662 | 0 |
| 133603709490 | [14272675371](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/14272675371) | `0a259726f0f455488591f9a62e31e7a3e27628961afe24fc0ba160dffd0b3afd` | 9635 | 9575 | 60 |
| 133603709503 | [14272008264](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/14272008264) | `d2e89b90a46ba65471489607dfd9f0eeb0b1aad1382cd85456c7d43856b0397d` | 9559 | 9499 | 60 |
| 133603709524 | [14272245594](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/14272245594) | `a849a82b005909491455f5d27421d5c29fcc7460eb92cca3c1fbac809e4abdfd` | 662 | 662 | 0 |
| 133603709671 | [14272906578](https://github.com/banodoco/astrid-runtime/actions/runs/43954031461/artifacts/14272906578) | `2845fb4a0ae40aac18e220cefcde4e459e6dadec53dd90df0d5d17d2f81493f3` | 9635 | 9575 | 60 |

Expected xfails are included in XML skipped totals. The three broad jobs include60 passing subtests in suite totals without individual testcase elements; this is reconciled, not a missing-case claim. Raw logs, actual XML and the complete testcase index are retained outside the repository evidence package for the separate evidence archive. Formal RS1 remains0/1; this report is not acceptance or proof that every cause is understood.
