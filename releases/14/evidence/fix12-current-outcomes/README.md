# FIX-12 exact-source outcome recovery

These receipts compare Agent release/14/main at `ae929cda` and the frozen FIX-12 candidate at `253456ce`. The input is the original GitHub Actions job log for each job, attempt 1. Each gzip JSON file records its source SHA, job URL, raw-log SHA-256, raw process exit, and per-ID outcomes. No jobs were rerun.

| Receipt | Compressed SHA-256 |
| --- | --- |
| `unit6-reference.json.gz` | `4114cd0df24d590888b49e8282f655d9df770ec4e31025b49500582b6d57262a` |
| `unit6-candidate.json.gz` | `8ad15be2552afaf85a47c3c7c5bd141df23d1852a5bbd59880f350ae391a620c` |
| `integration3-pair.json.gz` | `a18c08d7141daa0a7a16249558a6e05ffadd7970ae4e2cdff8c369861a0ef895` |

**Reference unit shard 6.** All 5,271 selected primary IDs had exactly one reported result. The log shows 5,023 passed, 220 failed, 22 errors and 6 skipped. Separately, 92 subtests passed and 33 failed, bringing pytest's aggregate failure count to 253. Raw exit 1. The recovered candidate log for `253456ce` reports the same literal 5,271 IDs and primary outcomes, the same subtest totals and raw exit 1. [Candidate job 135637529103](https://github.com/banodoco/astrid-agent/actions/runs/44546258657/job/135637529103). [Reference job 135599743368](https://github.com/banodoco/astrid-agent/actions/runs/44535516200/job/135599743368)

**Integration shard 3.** Each job printed a selected count of 517. The reference reported all 517 IDs: 371 passed, 83 failed, 62 setup errors and 1 skipped. It finished pytest with raw exit 1. The candidate reported 218 distinct IDs: 146 passed, 31 failed, 41 errors. All 218 match their reference statuses. The candidate then segfaulted with raw exit 139 before printing a final summary. The reference passed the test active at the crash, `test_dry_run_equals_live_run[video/h3-local-managed]`; the candidate recorded no outcome for that ID. There is no candidate traceback establishing the cause of the native crash or the phase of its 41 errors. [Reference job 135599744499](https://github.com/banodoco/astrid-agent/actions/runs/44535516469/job/135599744499) · [Candidate job 135637556260](https://github.com/banodoco/astrid-agent/actions/runs/44546268151/job/135637556260)

The candidate did not publish a complete selected-ID list. The 299 entries in `base_ids_without_candidate_outcomes` are the reference ID set minus the candidate's observed outcomes. The candidate itself has 299 unreported outcomes, derived from its printed selection count and observed results. Their exact identities are not established by the candidate log. This comparison supersedes the missing-log status for the current reference jobs; the historical comparisons on other SHAs keep their original outcomes.

## Completed shard 3 on the revised head

On Agent `dbb7152e`, all 517 destination IDs reported the same primary outcome as `ae929cda`: 371 passes, 83 call failures, 62 setup errors and one skip, raw exit 1. The 299 destination IDs with no observed result on historical `253456ce` now have 225 passes, 52 call failures, 21 setup errors and one skip. The H3 managed-service case passed. The current run identifies the phase of its errors; the 41 historical errors retain an unknown phase. The earlier process terminated with exit 139 and its cause remains open. [Revised native job](https://github.com/banodoco/astrid-agent/actions/runs/44610761362/job/135866420980) · [Per-ID comparison](integration3-current.json.gz), SHA-256 `3e832fb48ccbe1f558430feab9e5af89fea9b03d34859b286fad3e19a7896b31`

## Final unit comparison on the revised head

Unit shard 6 on `dbb7152e` retained all 5,271 original IDs and primary outcomes against both `ae929cda` and `253456ce`. Its 22 errors occurred in setup. All 33 failed subtests match. Of the 125 subtests, one passing diagnostic contains a different temporary path. The final eight-shard union has the same 30,887 primary IDs on all three commits. Both destination and current candidate report 29,592 passes, 843 failures, 397 errors and 55 skips. The per-ID comparison retains the two improvements and the adverse #733 readiness and #785 H3 cases. [Final unit 6 job](https://github.com/banodoco/astrid-agent/actions/runs/44610755868/job/135866403237) · [Final unit 6 comparison](unit6-dbb-final.json.gz), SHA-256 `2065f45d54e2efcabbd73584e935e9b049435f9a24a1f9256419a864209817b9`.

The H3 composition case that reported 167/108 in hosted unit 1 reproduced the frame-count failure on both exact product pairs. Six alternating isolated trials on macOS 15.4 arm64 returned PASS, FAIL, PASS on each side. Trial two measured 181/108 on the destination and 166/108 on the candidate. All setups and teardowns passed. [Per-trial outcomes and digests](h3-isolation.json) · [Original hosted observation](https://github.com/banodoco/astrid-dev/issues/785#issuecomment-7024956216)
