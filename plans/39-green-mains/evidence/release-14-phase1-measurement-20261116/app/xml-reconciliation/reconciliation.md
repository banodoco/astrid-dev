# App CI XML reconciliation

Run 43938449477, attempt 2. The Vitest artifact is associated with job 133579734809; its job log was reused from attempt 1, job 133549190737.

- Permanent GitHub artifact: [App Vitest results](https://github.com/banodoco/astrid-app/actions/runs/43938449477/artifacts/14262849293).
- ZIP SHA-256: `5010e805e6245658226bf335b775885071c9d441b317e2805be968d85bbe86eb` (matches the job log digest).

| XML file | Tests | Failures | Errors | Skipped | Testcase records |
|---|---:|---:|---:|---:|---:|
| `vitest-app.xml` | 20,870 | 0 | 0 | 0 | 20,870 |
| `vitest-sdk-boundary.xml` | 335 | 0 | 0 | 0 | 335 |

The XML confirms 21,205 passing testcase records in total; totals match the job log. Full testcase IDs are in `testcase-index.json`. Extracted XML and source ZIP are preserved in this directory.
