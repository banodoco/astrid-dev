# W206 App PR #268 check attribution

Final snapshot 2026-11-15 16:15 UTC. Verdict: **clean by name**. PR REST API reports head `adad82f07cf35007f96fa44adea9211a09117391`; base `main`. This is the only head used for the verdict. GitHub access is read-only.

Final-head runs: PR Tests [43729125823](https://github.com/banodoco/astrid-app/actions/runs/43729125823), PR Dockerfile [43729125918](https://github.com/banodoco/astrid-app/actions/runs/43729125918), push Tests [43729117890](https://github.com/banodoco/astrid-app/actions/runs/43729117890), E2E [43729117914](https://github.com/banodoco/astrid-app/actions/runs/43729117914), Lanes [43729117891](https://github.com/banodoco/astrid-app/actions/runs/43729117891), dispatch Direct Journey [43729124337](https://github.com/banodoco/astrid-app/actions/runs/43729124337). PR and push/dispatch workflows completed; PR boundary, vitest and release-tooling-macos skipped, as did push release-guard.

Main references: Tests 43703109315, E2E 43703109324, Lanes 43709054148, Direct Journey 43707235824, Dockerfile 43703109391.

| Job | Main | Final head | Attribution |
|---|---|---|---|
| release-guard | pass | PR pass; push skipped | pass on merge ref |
| Dockerfile checks | pass | PR pass | pass |
| boundary | pass | push pass; PR skipped | pass |
| vitest | pass | push pass; PR skipped | pass |
| release-tooling-macos | pass | push pass; PR skipped | pass |
| extension-accessibility | fail | fail | same nine IDs: `:114`, `:156` across browsers and device cases |
| extension-visual | fail `:154` | fail `:154` | same ID |
| extension-cross-browser | fail | fail | same six IDs: `:76`, `:97` in Chrome, Firefox, WebKit |
| playwright-timeline-chrome-export | fail | fail | same three IDs: audio-reactive `:304`, `:412`; preview-scrub `:231` |
| playwright-timeline | fail | fail | same 36 failure-context IDs |
| playwright-default | fail | fail | same 27 failure-context IDs |
| checkout-lanes | fail | fail | same `runtimePackRefresh.integration.test.ts` test, missing Chromium executable |
| installer-posix (ubuntu-latest) | pass | pass | pass |
| installer-posix (macos-latest) | pass | pass | pass |
| installer-powershell | pass | pass | pass |
| quick-journey | fail `:3419` | fail `:3419` | same ID and source-tuple assertion |
| direct-journey | pass | dispatch pass | pass |
| three-products | fail `:3674` | dispatch pass, attempt 1 | pass |

No new check name in the final-head check-runs API. All final-head checks have completed; no new check name observed.

Superseded runs, in workflow order PR Tests, PR Dockerfile, push Tests/E2E/Lanes, dispatch Direct Journey (statuses at snapshot):

- `4e9faabc8`: 43726254576 cancelled, 43726254573 cancelled, 43726249234 success / 43726249307 queued / 43726249195 failure, 43726256150 cancelled.
- `b5b1e188f`: 43726713927 success, 43726713940 success, 43726709954 running / 43726709882 queued / 43726709861 queued, 43726716728 cancelled.
- `e7d27462e`: 43727145353 cancelled, 43727145345 success, 43727140355 running / 43727140361 queued / 43727140404 queued, 43727146575 cancelled.
- `54b435d86`: 43728682193 cancelled, 43728682200 cancelled, 43728676624 / 43728676616 / 43728676633 queued, 43728683352 cancelled.
- `3b3c85fd`: 43724989550 success, 43724989545 success, 43724984500 success / 43724984521 failure / 43724984470 failure, 43724990246 cancelled.

Superseded dispatch three-products jobs: 4e9 job 132848799559, b5b job 132850136975, and 54b job 132856181388 cancelled with no logs available; e7 job 132851533215 cancelled during hosted build before test outcomes. None provides an observed three-products result. No notice interception observed in available e7 log; absent logs do not establish absence.

15:24 UTC poll: all six final-head workflows remain queued; job states unchanged.

15:29 UTC poll: PR Tests completed successfully; release-guard [job 132857457247](https://github.com/banodoco/astrid-app/actions/runs/43729125823/job/132857457247) checked out merge `8649ae88a772a9051e2b3aa8dd3c10e4b2fe850b` merging `adad82f0`; guard reports release 12 -> 13 and matching manifest and Runtime lock pins. Other five workflows queued.

15:34 UTC poll: PR Dockerfile checks passed; four push/dispatch workflows remain queued; Direct Journey attempt count 1.

15:38 UTC poll: remaining four workflows queued; no additional Direct Journey attempt.

15:42 UTC poll: push Tests in progress; E2E, Lanes and Direct Journey queued.

15:47 UTC poll: push release-tooling-macos and macOS installer passed; extension-visual and extension-cross-browser failed with same IDs as main, per completed job logs. Other jobs running or queued.

15:52 UTC poll: PowerShell installer passed; quick-journey failed the same `three-products.spec.ts:3419` quick test and source-tuple assertion as main. This push job selects the quick test, not the 14-test dispatch suite. Checkout-lanes running.

15:56 UTC poll: direct-journey and playwright-timeline started; checkout-lanes failed the same `runtimePackRefresh.integration.test.ts` test with missing Chromium executable as main. Three-products remains queued.

16:01 UTC poll: push Tests completed successfully, including vitest. Three-products started; direct-journey running.

16:06 UTC poll: direct-journey and Ubuntu installer passed. Timeline failure-context sets match main exactly (36 each); accessibility failure-context sets match exactly (18 including retries, nine cases). Three-products remains running.

16:10 UTC poll: E2E completed; all six failed job ID sets match main. Default has 27 matching failure-context IDs; Chrome-export has three matching contexts (`audio-reactive-colour-export.spec.ts:304,412`, `preview-scrub-evidence.spec.ts:231`). Three-products is the only running job.

## Final three-products attempt

[Run 43729124337, attempt 1, job 132857530301](https://github.com/banodoco/astrid-app/actions/runs/43729124337/job/132857530301): one workflow attempt, no test retries. The JSON outcome check reports 14 total, four expected failures all allowlisted, zero unexpected, flaky or skipped. The raw report marks the four listed cases failed as expected. No PR-event job runs this 14-test suite. The separate push quick-journey selects `:3419`.

| Order | three-products.spec.ts | Attempt 1 |
|---:|---|---|
| 1 | :417 concurrent edit and retained draft | pass |
| 2 | :611 Runtime restart | pass |
| 3 | :1558 lost ACK and dependent gesture | pass |
| 4 | :1691 Agent edit and newer gesture | pass |
| 5 | :1917 ordinary extension batch | expected failure |
| 6 | :2098 manual video drop | expected failure |
| 7 | :2355 dependency conflict | pass |
| 8 | :2437 native occurrence duplicate | expected failure |
| 9 | :2629 mixed editing and recovery | pass |
| 10 | :3200 render R after R+1 | expected failure |
| 11 | :3504 bootstrap actual consumer | pass |
| 12 | :3674 empty bootstrap and image drop | pass |
| 13 | :2904 native None single | pass |
| 14 | :2996 native None bulk | pass |

Neither the job log nor the uploaded JSON report contains `quiet-update-notice`. The JSON references four error-context files, but the uploaded artifact contains only JSON summaries, not those files; therefore notice interception cannot be ruled out from the missing contexts. The log does not print first-error details for expected failures. The report supplies the full first error messages below; each has fewer than 30 lines, and the referenced context files were not uploaded, so 30 lines of surrounding context are unavailable.

**:1917 first error (complete available message):**

```text
Error: expect(locator).toContainText(expected) failed

Locator: getByTestId('scene-markers-summary')
Expected substring: "2 markers"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for getByTestId('scene-markers-summary')
```

**:2098 first error (complete available message):**

```text
TimeoutError: page.waitForResponse: Timeout 90000ms exceeded while waiting for event "response"
```

**:2437 first error (complete available message):**

```text
Error: expect(received).toBe(expected) // Object.is equality

Expected: 1
Received: 0

Call Log:
- Timeout 90000ms exceeded while waiting on the predicate
```

**:3200 first error (complete available message):**

```text
Error: astrid call exited 1: -m astrid timelines commit 04b3c47f-3bcf-496d-96c2-c072b448f82d --project direct-journey-d35518 --file /tmp/astrid-direct-zTzwsN/astrid-data/drafts/2a177e70cbcd48acb418ac18e73d2e06/04b3c47f-3bcf-496d-96c2-c072b448f82d/main.json -m agent: marker clip in the slot --idempotency-key f2-render-r --json
{"data":null,"error":{"code":"timeline_commit_error","details":{"hint":"re-check out the detached document and retry with its exact base pair","path":"/file","suggested_command":"astrid timelines checkout 04b3c47f-3bcf-496d-96c2-c072b448f82d --project direct-journey-d35518"},"message":"patch references media outside Runtime-verified inputs"},"idempotency_key":"f2-render-r","ok":false,"receipt":null}
```

Final REST verification: PR head remains `adad82f07cf35007f96fa44adea9211a09117391`, merge `8649ae88a772a9051e2b3aa8dd3c10e4b2fe850b`. All 17 distinct check names match main. No workflow was dispatched or rerun by this investigation.
