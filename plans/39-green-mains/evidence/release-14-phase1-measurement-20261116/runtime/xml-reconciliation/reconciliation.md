# Runtime CI XML reconciliation

CI run 43938386357, attempt 1, head `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`. For each runtime CI ZIP, the downloaded hash matches both the captured artifact digest and job report digest; XML totals match the measured JUnit totals.

| Job | Artifact ID | Tests | Failures | Errors | Skipped | XML testcase records | Passed testcase records |
|---|---:|---:|---:|---:|---:|---:|---:|
| 133548963837 (ci-portability-macos-14264336834.zip) | 14264336834 | 662 | 8 | 0 | 59 | 662 | 595 |
| 133548963714 (ci-portability-ubuntu-14263697451.zip) | 14263697451 | 662 | 7 | 0 | 45 | 662 | 610 |
| 133548963680 (ci-process-control-14263048850.zip) | 14263048850 | 9559 | 85 | 843 | 39 | 9499 | 8532 |
| 133548963937 (ci-unit-macos-14265574916.zip) | 14265574916 | 9635 | 76 | 839 | 143 | 9575 | 8517 |
| 133548963731 (ci-unit-ubuntu-14263361597.zip) | 14263361597 | 9635 | 76 | 839 | 39 | 9575 | 8621 |

Permanent GitHub artifact URLs:

- [ci-portability-macos-14264336834.zip](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/artifacts/14264336834) — SHA-256 `4bf75da79780ac07215740d701a44e0b6eb7de900dc11b875720714dd202c197`.
- [ci-portability-ubuntu-14263697451.zip](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/artifacts/14263697451) — SHA-256 `d64fb4bf208a6d41fc7ee510da49366dfdf1b58702bc77018b6ed01e9582325f`.
- [ci-process-control-14263048850.zip](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/artifacts/14263048850) — SHA-256 `844be74119a3918e0d68ecc27339f9f3c895df6d56985b9cdd5e5c52d27b5001`.
- [ci-unit-macos-14265574916.zip](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/artifacts/14265574916) — SHA-256 `30a697a2d9d5977e8512c5b6f0cd7628f9fcbb5684f3d921fd316aad671a769e`.
- [ci-unit-ubuntu-14263361597.zip](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/artifacts/14263361597) — SHA-256 `f8a105069721cbca8953445bad1428c524dc686b369bfc49a05e2c949573c891`.

## 60 subtests and xfails

- Unit and sandbox-process-control JUnit `tests` totals include 60 passing subtests that are absent as separate `<testcase>` elements; this explains the 60-record difference between root totals and testcase elements. The 60 subtests are corroborated by each job summary.
- Xfails appear inside JUnit skipped totals: unit Ubuntu 26 skipped + 13 xfailed = 39; unit macOS 130 skipped + 13 xfailed = 143; sandbox-process-control 26 skipped + 13 xfailed = 39.
- Portability jobs have no testcase count delta: Ubuntu 610 pass / 7 fail / 45 skip; macOS 595 pass / 8 fail / 59 skip. Full testcase IDs from the XML are preserved in `testcase-index.json`.

## Nightly integration

- Run 43938386391, attempt 1, job 133548961758.
- Permanent GitHub artifact: [Nightly integration results](https://github.com/banodoco/astrid-runtime/actions/runs/43938386391/artifacts/14262378752).
- ZIP SHA-256: `f7e368f0492cfbaec9b9ee4a40de08fb6bc3510ddae43b6c7f3ab7d51d93bbf1`, matching the recorded digest.
- XML: 667 testcases = 37 passed + 39 failed + 571 errors + 20 skipped, matching the measured job summary.

Extracted XML and downloaded ZIPs are preserved in this directory. `reconciliation.json` contains per-artifact summaries and hashes.
