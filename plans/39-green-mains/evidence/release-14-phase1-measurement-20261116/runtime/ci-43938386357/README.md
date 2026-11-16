# Runtime CI post-batch measurement — provisional G2

Exact head `4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce`, tree `3fff009d7cb8c46a1a1df21f3f541596b98480bd`; [CI43938386357](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357), attempt1, failed. All five failed jobs have complete captured logs. No product or repository task/run-state files were edited, and no workflow was started or rerun. Formal RS1 remains **0/1**.

## Complete failed-job table

| Job | Job ID | Exact pytest summary | Full literal groups | Established Plan38 / Plan55 holds |
|---|---|---|---:|---:|
| sandbox-process-control | [133548963680](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/job/133548963680) | 85 failed, 8532 passed, 26 skipped, 13 xfailed, 843 errors, 60 subtests passed in 690.75s (0:11:30) | 57 | 19 / 1 |
| portability-lifecycle (ubuntu-latest) | [133548963714](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/job/133548963714) | 7 failed, 610 passed, 45 skipped in 71.84s (0:01:11) | 7 | 0 / 0 |
| unit (ubuntu-latest) | [133548963731](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/job/133548963731) | 76 failed, 8621 passed, 26 skipped, 13 xfailed, 839 errors, 60 subtests passed in 634.44s (0:10:34) | 49 | 15 / 1 |
| portability-lifecycle (macos-latest) | [133548963837](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/job/133548963837) | 8 failed, 595 passed, 59 skipped in 36.45s | 8 | 0 / 0 |
| unit (macos-latest) | [133548963937](https://github.com/banodoco/astrid-runtime/actions/runs/43938386357/job/133548963937) | 76 failed, 8517 passed, 130 skipped, 13 xfailed, 839 errors, 60 subtests passed in 987.08s (0:16:27) | 49 | 10 / 1 |

The five jobs contain **2773 outer failures/errors** (252 FAILED + 2521 ERROR) and **170 distinct full literal per-job message groups**. These are outcome/message counts, not root-cause counts. Each paired job JSON/Markdown file reports every literal message with its exact count and triage; JSON additionally retains every exact test ID, source/detail line anchors and raw E-lines.

Every job reconciles with its emitted JUnit summary. Pytest subtests contribute60 additional passed cases to the JUnit totals in each broad suite; expected xfails are included in JUnit skipped. No XML archive was downloaded. Artifact identities and digests are retained in `artifacts.json` and each job record.

## Useful diagnosis

- **RE4 environment defect remains in sandbox:** four existing tests fail with `FileNotFoundError: [Errno 2] No such file or directory: 'tsc'`. The container entrypoint installs Node/npm and runs locked `npm ci`, but does not add `packages/typescript/node_modules/.bin` to the environment PATH passed to pytest. The Ubuntu and macOS unit jobs have zero `tsc` failures. Preserve compiler assertions; fix the actual sandbox environment.
- **Agent SDK API mismatch remains:** the selected Agent checkout is present and all failed-job environments record its exact pin `b05ac03a5bcab278bccf99d85b49f4037b5dec10`; the broad suites now fail imports of `commit`, `capture`, `timeline.commit`, or `_commit_patch`. One macOS case additionally reports a circular import of `Checkout`. These are distinct from the former missing-checkout signature. Product versus stale test contract is unresolved.
- **K1b is correctly red:** the new registry guard reports20 quarantined test node IDs against a cap of10, with required metadata missing. Other declared-lane/skip-policy guard failures remain. No cap or guard was weakened.
- **Portability remains7F on Ubuntu and8F on macOS.** Most child/installed-run failures still report no `astrid` in that child environment; these are not disproved by a parent process having a checkout.
- **macOS watchdog remains unclassified:** `test_live_watchdog_uses_real_handler_and_private_faulthandler_output` reports `assert 0 > 0`; one observation does not establish flakiness.

## Ownership

**44 Plan38 and3 Plan55 outcomes** retain the established exact G1 ownership holds. In addition, **9 outcomes across the3 `test_timeline_render_publication.py` cases in the broad suites** are marked in a separate ownership-review ledger as **WAITING — Plan55 ownership confirmation before test changes**. Their contracts cover task publication, cancellation, stale producer fences and retry, which overlap Plan55’s broader Runtime lifecycle/publication inventory. These9 are not silently added to the established exact count. Other unreviewed rows are not automatically cleared for Plan39 fixes.

## Method and evidence limits

Only the final outer pytest short summary supplies outcome counts. Each outcome is uniquely matched to one detailed ERROR/FAILURE block; no unmatched or ambiguous blocks remain. Sandbox emits empty outer messages for926 of928 outcomes, so those messages are recovered from the last contiguous E-line group in the corresponding detail block. Unit/portability continuation lines are retained. Transport timestamps, ANSI sequences and embedded BOM framing are removed; literal paths, values and multiline messages are not normalized. Nested captured pytest output is excluded from counts.

All full logs and API metadata were retrieved without an access failure. Pytest itself may abbreviate displayed values; the raw captured log is the evidence boundary. This is measurement and triage, not a proof that any unclassified failure is a test or product bug.

## Source references

- [Exact CI workflow](https://github.com/banodoco/astrid-runtime/blob/4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce/.github/workflows/ci.yml)
- [Exact sandbox entrypoint](https://github.com/banodoco/astrid-runtime/blob/4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce/tests/seccomp/container-entrypoint.py)
- [TypeScript generator contract tests](https://github.com/banodoco/astrid-runtime/blob/4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce/tests/test_timeline_commit_type_generator.py)
- [Document object contract tests](https://github.com/banodoco/astrid-runtime/blob/4fe2c0b847cf83771b2f3ce4e4fba0934f64f6ce/tests/test_timeline_document_object_contract.py)

`measurement.json` records SHA256 and byte size for every evidence file. Per-job reports include the full raw-log hash.
