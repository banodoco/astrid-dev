# Nightly 43954031460 comparison

## Provenance

- Repository: `banodoco/astrid-runtime`; run 43954031460, attempt 1; job 133603706731 (`integration`).
- Head: `359e2d7e55369562ca9513557282ea8aff7645bc`; tree: `0291fadcde521650fdc71257a9ec2fd61b7226a4`.
- Run conclusion: failure. The uploaded XML artifact step completed successfully.
- Permanent artifact URL: [JUnit artifact 14269133531](https://github.com/banodoco/astrid-runtime/actions/runs/43954031460/artifacts/14269133531).
- Downloaded ZIP SHA-256: `647bdf2354060ba5e35b8e5d08018289c685370b19f7e10bc425c5a99a9ce177`; matches GitHub artifact metadata and the requested digest.
- Job log: `../nightly-43954031460-job-133603706731.log`; SHA-256: `7fbf8f8cfc549ac018d1298a5e1807fff78618749136b0b0f30b72e1cd851a49`.

## Summary reconciliation

| Source | Tests | Failed | Errors | Passed | Skipped | Deselected |
|---|---:|---:|---:|---:|---:|---:|
| New pytest final summary | 667 | 121 | 28 | 498 | 20 | 9,596 |
| New JUnit XML | 667 | 121 | 28 | 498 | 20 | n/a |
| Previous pytest summary, run 43938386391 | 667 | 39 | 571 | 37 | 20 | 9,596 |
| Previous JUnit XML | 667 | 39 | 571 | 37 | 20 | n/a |

XML total and status counts match the job summary in both runs. All 149 current failure/error IDs in the raw short summary have matching XML status records. The old and new XML contain the exact same 667 testcase IDs.

## Full XML message grouping

The preceding `message-counts.json` and 46-group summary are based on pytest’s final one-line short-summary text, which can abbreviate assertion values. [The full XML message ledger](full-xml-messages.md) adds exact grouping by the JUnit failure/error message attribute for all 149 red testcase records, preserving multiline values, exact IDs, statuses, full per-ID XML detail text, triage provenance, and the Plan 38 source-closure WAITING disposition. It confirms the same 149 IDs and statuses as `new-red-outcomes.json`; it does not replace or inflate the prior G1 comparison counts.

## Per-ID outcome changes

| Transition | Count |
|---|---:|
| `error->error` | 28 |
| `error->failure` | 89 |
| `error->passed` | 454 |
| `failure->failure` | 31 |
| `failure->passed` | 8 |
| `passed->failure` | 1 |
| `passed->passed` | 36 |
| `skipped->skipped` | 20 |

- 454 old errors become passes; 8 old failures become passes.
- 89 old errors become failures. This is newly exposed behavior in the outcome comparison, not automatically a product regression.
- 28 errors and 31 failures remain red; 1 previously passing ID is now failing.
- There are 462 more passes and one new failure, for a net increase of 461 passes. This net change is not a count of individually fixed cases.
- 20 skips stay skipped.

The full 667-row testcase ledger is `status-comparison.json`. All current failed/error IDs and literal messages are in `new-red-outcomes.json`; message groups and exact IDs are in `message-counts.json`.

## Largest current failure/error message groups

| Count | Outcome mix | Prior triage mapping | Literal pytest summary message |
|---:|---|---|---|
| 34 | FAILED 34 | R-n (new; RE1/RE2) 34 | `Failed: DID NOT RAISE RuntimeErrorBase` |
| 21 | FAILED 21 | R-j / RT6 9, R-n (new; RE1/RE2) 12 | `assert 33 == 31` |
| 20 | ERROR 20 | R-c / RE3 20 | `RuntimeError: cannot archive required commit 321cef4b8c89a4a938cb9ede41ba6a5444cf1b62 from /home/runner/work/astrid-runtime/astrid-runtime/astrid-agent; fetch this SHA or full history with \`git -C /home/runner/work/astrid-runtime/astrid-runtime/astrid-agent fetch origin 321cef4b8c89a4a938cb9ede41ba6a5444cf1b62\`` |
| 6 | ERROR 5, FAILED 1 | R-o (new; unclassified) 6 | `RuntimeError: process control is already strict; refusing to change it to sandbox` |
| 5 | FAILED 5 | R-n (new; RE1/RE2) 5 | `AssertionError: assert {'reason': 'r...blication_id'} == {'reason': 'r...3f91bd4312ea'}` |
| 5 | ERROR 1, FAILED 4 | R-d / RT1 4, R-n (new; RE1/RE2) 1 | `runtime_protocol.errors.ConflictError: v33 provider/baseline verification is pending; requests and fresh pins are fenced` |
| 3 | FAILED 3 | R-n (new; RE1/RE2) 3 | `AssertionError: Regex pattern did not match.` |
| 3 | FAILED 3 | R-o (new; unclassified) 3 | `AssertionError: assert False` |
| 3 | FAILED 3 | R-k / RT7 3 | `AssertionError: foreground Runtime exited 1: {` |
| 3 | FAILED 3 | R-n (new; RE1/RE2) 3 | `astrid.core.timeline.clip_fields.ClipFieldError: entrance has unknown key 'durationFrames'; allowed: type, duration` |
| 3 | FAILED 3 | R-n (new; RE1/RE2) 3 | `runtime_protocol.timeline_commit_port.CommitUnavailable: Timeline commit outcome unavailable; retry the exact request` |
| 2 | FAILED 2 | R-n (new; RE1/RE2) 2 | `AssertionError: assert {'clips': [{'...': 'visual'}]} == {'clips': [{'...': 'visual'}]}` |

## Concrete observations

- 34 rows say `Failed: DID NOT RAISE RuntimeErrorBase`, mostly mapped to prior R-n API-compatibility selectors. The summary identifies the failed expectations but does not establish their cause.
- 21 rows report `assert 33 == 31`, mapped by testcase to both R-j/RT6 and R-n; retain per-test attribution.
- 20 errors say historical Agent commit `321cef4b8c89a4a938cb9ede41ba6a5444cf1b62` could not be archived (R-c/RE3).
- Five errors and one failure report process control is already strict and cannot be changed to sandbox; this is new R-o/unclassified evidence.
- Five rows (four failures, one error) remain on the v33 provider/baseline verification fence (R-d/RT1 family). Preserve fail-closed behavior.
- Three portability-lifecycle failures remain R-k/RT7, involving missing `astrid` import.
- One previously passing ID is newly red: `tests/test_verified_host_launch.py::test_nine_component_measurement_parity_without_importing_astrid` now fails with `KeyError: 'source_checkout_closure'`; it had no exact prior triage signature. A subsequent source/contract review identifies a stale source-location assumption after Agent commit4e6e8c9 and places this closure-parity case **WAITING on Plan38**; see [the superseding disposition](source-closure-new-red.md).
- Twelve current rows retain the prior R-o unclassified family. The most frequent signature is strict process-control refusal (6 rows); other observed signatures include assertion mismatches, untracked Agent source, and unavailable capture projection. These remain per-test cause-card candidates.

## Prior API and compiler error groups

- The previous R-n Agent SDK/API compatibility group contained 551 red IDs. In this comparison, 458 are passing (451 prior errors and 7 prior failures), 89 prior errors are now failures, 3 prior failures remain failures, and 1 prior error remains an error. The 89 error-to-failure rows are newly exposed behavior and are not automatically regressions.
- All three prior R-f/RE4 `tsc`-missing errors now pass.
- The 20 prior R-c/RE3 errors for unavailable historical Agent commit `321cef4b8c89a4a938cb9ede41ba6a5444cf1b62` remain errors.

## Ownership and limits

- The prior nightly ledger counted no exact Plan38 or Plan55 WAITING selectors. A subsequent source/contract review assigns the current source-closure pass-to-failure case to Plan38: it remains WAITING and unchanged. This does not close either plan's acceptance or classify unrelated selectors by name.
- RS1 remains `0/1`. This report is a measurement and per-ID comparison, not acceptance or root-cause proof.
- Literal messages preserve exactly the final one-line pytest short-summary text; pytest can abbreviate long assertion representations.
- For IDs red in the prior run, previous triage is carried by exact testcase ID even when the observed message changed. That is family mapping, not a fresh root-cause finding.
- XML confirms identity and outcome, not cause. New red results after old errors are not automatically regressions.

## Preserved files

`nightly-14269133531.zip`, extracted XML, `run-metadata.json`, `job-metadata.json`, `artifact-metadata.json`, `comparison.json`, the complete `status-comparison.json`, the complete `new-red-outcomes.json`, and the full `message-counts.json`.
