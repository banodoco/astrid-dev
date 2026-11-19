# FIX-12 exact-source outcome recovery

These receipts compare Agent release/14/main at `ae929cda` and the frozen FIX-12 candidate at `253456ce`. The input is the original GitHub Actions job log for each job, attempt 1. Each gzip JSON file records its source SHA, job URL, raw-log SHA-256, raw process exit, and per-ID outcomes. No jobs were rerun.

| Receipt | Compressed SHA-256 |
| --- | --- |
| `unit6-reference.json.gz` | `4114cd0df24d590888b49e8282f655d9df770ec4e31025b49500582b6d57262a` |
| `integration3-pair.json.gz` | `a18c08d7141daa0a7a16249558a6e05ffadd7970ae4e2cdff8c369861a0ef895` |

**Reference unit shard 6.** All 5,271 selected primary IDs had exactly one reported result. The log shows 5,023 passed, 220 failed, 22 errors and 6 skipped. Separately, 92 subtests passed and 33 failed, bringing pytest's aggregate failure count to 253. Raw exit 1. This receipt covers the reference only. [Reference job 135599743368](https://github.com/banodoco/astrid-agent/actions/runs/44535516200/job/135599743368)

**Integration shard 3.** Each job printed a selected count of 517. The reference reported all 517 IDs: 371 passed, 83 failed, 62 setup errors and 1 skipped. It finished pytest with raw exit 1. The candidate reported 218 distinct IDs: 146 passed, 31 failed, 41 errors. All 218 match their reference statuses. The candidate then segfaulted with raw exit 139 before printing a final summary. The reference passed the test active at the crash, `test_dry_run_equals_live_run[video/h3-local-managed]`; the candidate recorded no outcome for that ID. There is no candidate traceback establishing the cause of the native crash or the phase of its 41 errors. [Reference job 135599744499](https://github.com/banodoco/astrid-agent/actions/runs/44535516469/job/135599744499) · [Candidate job 135637556260](https://github.com/banodoco/astrid-agent/actions/runs/44546268151/job/135637556260)

The candidate did not publish a complete selected-ID list. The 299 entries in `base_ids_without_candidate_outcomes` are the reference ID set minus the candidate's observed outcomes. The candidate itself has 299 unreported outcomes, derived from its printed selection count and observed results. Their exact identities are not established by the candidate log. This comparison supersedes the missing-log status for the current reference jobs; the historical comparisons on other SHAs keep their original outcomes.
