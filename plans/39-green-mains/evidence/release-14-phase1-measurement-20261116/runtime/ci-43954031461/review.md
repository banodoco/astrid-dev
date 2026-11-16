# Independent review — Runtime CI 43954031461

Read-only review of the saved measurement, five artifact ZIPs, extracted XML, per-job metadata, and prior-run XML. No tests or parser reruns were performed.

## Identity and coverage

- Run 43954031461, attempt 1, repository `banodoco/astrid-runtime`, head `359e2d7e55369562ca9513557282ea8aff7645bc`, tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`.
- The five per-job reports and artifact metadata agree on the run and job identities. The prior comparison run is 43938386357 at `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`.
- Independently compared each artifact ZIP's SHA-256 with `artifacts.json`; each matches. For each job, XML suite totals match the saved per-job JUnit summary, and the XML testcase IDs match the saved current testcase index and the previous job's XML testcase ID set.
- The five job failure/error totals sum to 1,489 records. The per-job distinct message-group counts sum to 166.

| Job | Job ID | Artifact ID | SHA-256 verified | XML tests | Failed | Errors | Skipped | Direct testcase IDs | Prior-pass-to-red |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| Ubuntu portability | 133603709482 | 14269247265 | Yes | 662 | 7 | 0 | 45 | 662 | 0 |
| Ubuntu unit | 133603709490 | 14272675371 | Yes | 9,635 | 119 | 367 | 39 | 9,575 | 0 |
| Sandbox process control | 133603709503 | 14272008264 | Yes | 9,559 | 132 | 371 | 39 | 9,499 | 0 |
| macOS portability | 133603709524 | 14272245594 | Yes | 662 | 8 | 0 | 59 | 662 | 0 |
| macOS unit | 133603709671 | 14272906578 | Yes | 9,635 | 118 | 367 | 143 | 9,575 | 0 |

The three broad jobs include 60 passing subtests in the JUnit suite totals without separate testcase elements. Xfails remain within skipped counts. This explains the 60-case gap in each broad job; it does not change the direct failure/error counts.

## Status transitions

Directly comparing old and new XML testcase records gives 0 prior-pass-to-failure/error transitions in all five jobs. The changed records consist of prior failures/errors becoming passing, prior errors becoming failures, or the same status remaining. In particular, the 186 error-to-failure transitions are newly exposed behavior and are not automatically product regressions.

Per-job status transition counts from the XML comparison:

- Ubuntu unit: 410 error-to-pass, 19 failure-to-pass, 62 error-to-failure; 367 errors and 57 failures remain.
- Sandbox process control: 410 error-to-pass, 15 failure-to-pass, 62 error-to-failure; 371 errors and 70 failures remain.
- macOS unit: 410 error-to-pass, 20 failure-to-pass, 62 error-to-failure; 367 errors and 56 failures remain.
- The two portability jobs preserve their full status totals: Ubuntu 7 failures/45 skips; macOS 8 failures/59 skips.

## Finding

No reconciliation blocker found. The saved identity, archive hashes, JUnit totals, testcase indexes, and no-prior-pass-to-red conclusion are consistent with the XML evidence. This review does not establish root cause or acceptance.
