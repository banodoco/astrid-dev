**Verdict: clean by name** on App PR #268 head `adad82f07cf35007f96fa44adea9211a09117391`. Every final-head job has completed. The failed E2E and Lanes jobs match the specified App main runs by failure ID; no new check name appeared.

The full evidence, superseded runs and available failure messages are in [summary.md](/home/user/wt/r13-tests/runs/w206/summary.md).

| Check | App main | Final head | Attribution |
|---|---|---|---|
| release-guard | Pass | PR pass; push skipped | Pass |
| Dockerfile checks | Pass | PR pass | Pass |
| boundary | Pass | Push pass; PR skipped | Pass |
| vitest | Pass | Push pass; PR skipped | Pass |
| release-tooling-macos | Pass | Push pass; PR skipped | Pass |
| extension-accessibility | Fail | Fail | Same nine cases |
| extension-visual | Fail | Fail | Same `:154` |
| extension-cross-browser | Fail | Fail | Same six cases: `:76`, `:97` across three browsers |
| playwright-timeline-chrome-export | Fail | Fail | Same three IDs: `:304`, `:412`, `:231` |
| playwright-timeline | Fail | Fail | Same 36 failure-context IDs |
| playwright-default | Fail | Fail | Same 27 failure-context IDs |
| checkout-lanes | Fail | Fail | Same test and missing Chromium executable |
| installer-posix (ubuntu-latest) | Pass | Pass | Pass |
| installer-posix (macos-latest) | Pass | Pass | Pass |
| installer-powershell | Pass | Pass | Pass |
| quick-journey | Fail | Fail | Same `:3419` and source-tuple assertion |
| direct-journey | Pass | Pass | Pass |
| three-products | Fail `:3674` | Pass | Pass |

**Release guard ran and passed on the PR merge ref**, commit `8649ae88a772a9051e2b3aa8dd3c10e4b2fe850b`. Its log reports release 12 → 13 and matching manifest and Runtime lock pins. [PR job](https://github.com/banodoco/astrid-app/actions/runs/43729125823/job/132857457247)

The [three-products dispatch](https://github.com/banodoco/astrid-app/actions/runs/43729124337/job/132857530301) had **one workflow attempt and no test retries**:

| Test in `three-products.spec.ts` | Attempt 1 |
|---|---|
| `:417` concurrent edit and retained draft | Pass |
| `:611` Runtime restart | Pass |
| `:1558` lost ACK and dependent gesture | Pass |
| `:1691` Agent edit and newer gesture | Pass |
| `:1917` ordinary extension batch | Expected failure |
| `:2098` manual video drop | Expected failure |
| `:2355` dependency conflict | Pass |
| `:2437` native occurrence duplicate | Expected failure |
| `:2629` mixed editing and recovery | Pass |
| `:3200` render R after R+1 | Expected failure |
| `:3504` bootstrap actual consumer | Pass |
| `:3674` empty bootstrap and image drop | Pass |
| `:2904` native None single | Pass |
| `:2996` native None bulk | Pass |

The outcome check reported four allowlisted expected failures and zero unexpected, flaky or skipped results. The job log and uploaded JSON contain no `quiet-update-notice` mention. The four referenced error-context files were not included in the artifact, so interception in those missing contexts cannot be ruled out; the available first-error messages are recorded in the summary.

The superseded dispatches for `4e9faabc8`, `b5b1e188f`, `e7d27462e` and `54b435d86` were cancelled without three-products test outcomes. No PR-event job ran the 14-test suite. GitHub access was read-only.