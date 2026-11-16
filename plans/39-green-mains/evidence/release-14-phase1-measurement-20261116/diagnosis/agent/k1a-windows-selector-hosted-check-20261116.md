# K1a Windows-native prerequisite — hosted negative coverage proof

**Classification:** independent, source-supported K1a prerequisite cause; **diagnosis only**, not an implemented/reviewed fix and not a completed skip-policy acceptance card. No Runtime clip contract, Plan 38/55 test, Release 15 row, or release/public-main branch is changed.

## Source and actual hosted record

Read on exact Agent `release/14/plan-39` commit `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`:

- [Windows CI workflow](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/.github/workflows/ci.yml#L23-L65) creates four explicit `--junitxml` collections. Native process/permission selection includes platform helpers and host child tests, **not** either target below.
- [R0 checkpoint native lock test](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/test_journey_diagnostic_checkpoint.py#L304-L345) `test_native_windows_locked_owner_file_is_not_read`: currently direct `@pytest.mark.skipif(sys.platform != "win32", ...)`, exercises real `LockFileEx` / `UnlockFileEx` and an owner-lock unreadability assertion.
- [ACL capture native test](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/test_journey_windows_acl_capture.py#L69-L141) `test_windows_explicit_users_ace_and_hardlink`: direct Windows-platform skip guard; creates dedicated ACL fixture descriptors, checks protected DACL/Users ACE and hardlink identity. Its *separate* `except OSError: pytest.skip('hard links unavailable')` is **not** the same platform gate and must not silently disappear.
- Existing `windows_native` lane in [tests/lanes.py](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/lanes.py#L121-L145) names the Windows CI job, but a lane registration does not add a file to a focused pytest command.

Real finished Windows job [133651924610](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924610) **passed** at the exact reviewed merge head, CI run [43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168), attempt 1. Its [artifact 14276253359](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14276253359) was **downloaded and parsed**, not merely assumed from the green check. ZIP SHA-256 `54563060ed7cc4772b6336ae252af9d8598ce2103a7eee83a442f79b98a7fb57`, matching the GitHub digest.

| Real XML member | SHA-256 of decompressed XML | Testcases | Fail/error/skip |
|---|---|---:|---|
| `installer-windows-tasks.xml` | `ec8a207e78df3a68b95e5cb30f08f7132883e2fef670e56f647287c8d8841e5e` | 15 | 0/0/0 |
| `host-recovery-services.xml` | `d36d03deb7c1b82fbef714ee3f1a353d077fc8df38b932ad44c547d4dff1c7d8` | 40 | 0/0/0 |
| `native-windows.xml` | `3107da84f5f7d1845c60f2d062e889f96e0a948baaf5d7ab2ecf4d3901c6c011` | 21 | 0/0/0 |
| `remotion-host-regressions.xml` | `5eda5b34421cd0c9640f02c09d9c79eabcb5622c99ca6798adf90711ae4845fc` | 36 | 0/0/0 |

**Result:** all **112 actual testcase XML IDs** passed, but the two named Windows-native test IDs are **absent from all four files**. So a passing Windows job provides *no execution proof* of their native security/lock behavior. This is a proven **selector gap**, not evidence that either product assertion passes or fails.

## Bounded candidate and proof gate (not yet executed)

N-class implementation candidate: add the two *exact* node selectors to the existing Windows native pytest command (not a new default-off lane). Then replace only each native-platform `skipif` with the supported `windows_native` marker once it is established that the lane mechanism excludes it outside Windows and the Windows selector executes it. Preserve the full real lock/ACL/hardlink assertions, including the separate hardlink-capability refusal/skip pending its own decision. Require source/task-owner review of the unmodified assertion contract and independent reviewer of the focused proof before any merge into `release/14/plan-39`. No claim of an X/S or judgment review is made here.

The workflow itself has `if: github.event_name != 'pull_request'`; a green draft PR alone **cannot** supply the required Windows-job hosted proof. The exact selected test IDs must appear and pass in a real Windows artifact on the integrated (reviewed) plan-head, without skipped IDs. A failing native assertion should be triaged rather than removed or skipped. The policy checker must still report other 17+ direct gates until separately proven.

**Stop/ownership boundaries:** The source proof justifies a future narrow selector fix but does not justify bypassing a test. Plan 38/55 ownership stays WAITING; Runtime replay integrity remains an owner decision; formal G1/G2/RS1 stay incomplete, RS1 0/1. No product branch/PR is created by this assessment.
