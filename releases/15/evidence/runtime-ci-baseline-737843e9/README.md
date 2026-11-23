# Runtime macOS watchdog baseline for Release 15

The unchanged Release 15 Runtime can miss every watchdog sample during the test's held request. The Release Lead classified that assertion as an inherited test defect and cleared the Plan 77 Runtime landing. [Open fragility issue #1621](https://github.com/banodoco/astrid-dev/issues/1621)

| Runtime revision | Commit |
| --- | --- |
| Release 15 before Plan 77 | `53a035ba7c04156dc45aa096f099b4c0224dfb14` |
| Reviewed Plan 77 source | `60fcf27d78d5d5f26abaec53dd81441e351ed34b` |
| Release 15 after the squash | `737843e9cb92c565c266452dde540832ee2c745b` |

The reviewed source and squash have the same Git tree, `6a1e9f2644b0a9e387ad576b9953ea1903cbe277`. The comparison leaves the watchdog test, fixtures and skips unchanged. [Runtime landing #102](https://github.com/banodoco/astrid-runtime/pull/102)

## Ordinary macOS unit runs

The same watchdog case failed in **0 of 6** ordinary runs of the exact base and **3 of 5** candidate runs across the earlier and repaired heads. The earlier failure stopped at the missing private stack sink. The two later failures reached the sample-count assertion. These counts do not establish a change in failure rate. [Case assertions](https://github.com/banodoco/astrid-runtime/blob/53a035ba7c04156dc45aa096f099b4c0224dfb14/tests/test_p2_commit_phase_capture.py#L1349)

| Source | Watchdog passes | Watchdog failures |
| --- | --- | --- |
| Base `53a035ba` | [45121527000](https://github.com/banodoco/astrid-runtime/actions/runs/45121527000), [45128266281](https://github.com/banodoco/astrid-runtime/actions/runs/45128266281), [45137156732](https://github.com/banodoco/astrid-runtime/actions/runs/45137156732), [45140009552](https://github.com/banodoco/astrid-runtime/actions/runs/45140009552), [45142882915](https://github.com/banodoco/astrid-runtime/actions/runs/45142882915), [45146039810](https://github.com/banodoco/astrid-runtime/actions/runs/45146039810) | 0 |
| Earlier head `b89cd48` | [45122402145](https://github.com/banodoco/astrid-runtime/actions/runs/45122402145) | [45122377997](https://github.com/banodoco/astrid-runtime/actions/runs/45122377997) |
| Reviewed head `60fcf27d` | [45125723115](https://github.com/banodoco/astrid-runtime/actions/runs/45125723115) | [45125706921](https://github.com/banodoco/astrid-runtime/actions/runs/45125706921), [45129347658](https://github.com/banodoco/astrid-runtime/actions/runs/45129347658) |

## Diagnostic receipts

The macOS diagnostic commits `697ca30e42ea34dc5d2b463047a5f82c84b59d86` (base) and `c122ad7a44dbc8c5e49781fda43c8aabf1512bd7` (head) add the same workflow-only instrumentation on their respective source parents. The base job completed. The Lead cancelled the head job after stages A and B had finished. [Base macOS job](https://github.com/banodoco/astrid-runtime/actions/runs/45138193652/job/137569436552) [Head macOS job](https://github.com/banodoco/astrid-runtime/actions/runs/45138193680/job/137569437243)

| Receipt | Base | Head |
| --- | --- | --- |
| A, 20 fresh isolated watchdog processes | 19 pass, iteration 19 fails at `assert 0 > 0` | 17 pass, iterations 01, 14 and 15 fail at the same assertion |
| B, full macOS unit selection, two workers | Watchdog passes, lifecycle case passes in 1.078 s | Watchdog passes on `gw1` in 511.564 ms in the hooks trace. Eight other-worker overlaps were existing project object filter cases. Lifecycle case passes in 1.084 s |
| C, full macOS unit selection, one worker | Watchdog passes, lifecycle case passes in 1.089 s | Cancelled. The last stdout line announces the lifecycle case at 47%. Its predecessor passed. Stderr is empty and there is no exit row or JUnit |

The test uses a 10 ms timer and a 20 ms sampler with a held request of 50 ms. Isolated base iteration 19 returned HTTP 200 and produced the private stack sink before finding zero samples. The failure therefore occurs on the base without another test worker or Plan 77 code. The evidence does not distinguish timer scheduling from a missed eligible frame. [Sampler implementation](https://github.com/banodoco/astrid-runtime/blob/53a035ba7c04156dc45aa096f099b4c0224dfb14/tests/helpers/p2_commit_phase_capture.py#L331)

Base B, head B and base C each retained 477 inherited failed or errored IDs and each added the same seven workflow-census failures from the diagnostic workflow. Head B had 35 new test IDs and no additional failed or errored IDs compared with base B. The unit selection, project code and test bodies were unchanged within each diagnostic arm.

The last case printed in head C was `tests/test_runtime_lifecycle.py::test_interruption_fence_keeps_http_owner_identity_reachable_during_claim`. It is unchanged. Its HTTP owner-identity reads use `RealmStore._read_snapshot`, which the first cut changed to select the new SQLite connection subclass. The case passed in all six ordinary exact-base runs (1.064–1.125 s) and all five ordinary candidate runs (1.063–1.147 s). The partial log establishes where reporting stopped. The cause of the stall remains open. [Owner-identity snapshot code at the landed head](https://github.com/banodoco/astrid-runtime/blob/737843e9cb92c565c266452dde540832ee2c745b/runtime_protocol/store.py#L1178-L1193)

| Archived macOS artifact | SHA-256 |
| --- | --- |
| [14803294320](https://github.com/banodoco/astrid-runtime/actions/runs/45138193652/artifacts/14803294320), base A/B/C diagnostics | `7c693abd230f56b6ad9e45192aba765458c3d7d4c0739ab14cc171ffac29243b` |
| [14804565127](https://github.com/banodoco/astrid-runtime/actions/runs/45138193652/artifacts/14804565127), base B JUnit | `de7af958cb034a1d8d6af2a30d23b6a6f63930e2d33381ee6f4371d591bb45b1` |
| [14808898635](https://github.com/banodoco/astrid-runtime/actions/runs/45138193680/artifacts/14808898635), head A/B and partial C diagnostics | `e4bdd33e86275d719e6a0183310d420663a78db5613a8872278885524a7141f2` |
| [14808787819](https://github.com/banodoco/astrid-runtime/actions/runs/45138193680/artifacts/14808787819), head B JUnit | `1f29650013d4267609a675c7ec00b1becc0c19b3b37ae48fb9088771ce36cb47` |

## Gate disposition

The Lead cleared Runtime #102 on the isolated base failure and opened #1621. The inherited watchdog assertion does not hold a Release 15 landing. The head's cancelled one-worker run and the exact-head Linux hang check are separate evidence about serial completion. [Lead disposition in #1621](https://github.com/banodoco/astrid-dev/issues/1621)
