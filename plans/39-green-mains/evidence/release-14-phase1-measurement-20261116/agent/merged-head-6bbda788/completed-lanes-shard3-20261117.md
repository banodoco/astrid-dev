# Agent PR369 merged-head Lanes completion — 17 November 2026 UTC

**Status: hosted attempt-1 measurement complete, failure; provisional G2 only. Formal G1/G2/RS1 acceptance remains incomplete; RS1 0/1.** This is a bounded read of [CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) and [Lanes 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) at **exact Agent head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`**, reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`, attempt **1**. CI was already completed and inventoried in [the earlier report](completed-ci-lanes-followup-20261116.md); no job was cancelled, rerun or dispatched here.

## Newly finished Lanes shard 3

The formerly running [integration shard 3 job 133651923800](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/job/133651923800) **completed failure**. Its **actual raw job log** was retrieved. Literal outer pytest summary, without the timestamp or surrounding delimiter:

```text
81 failed, 372 passed, 1 skipped, 31868 deselected, 13 warnings, 62 errors in 7828.85s (2:10:28)
```

The actual [JUnit artifact 14285717945](https://github.com/banodoco/astrid-agent/actions/runs/43967861160/artifacts/14285717945) was downloaded and its `integration.xml` parsed, not inferred from the job result. All 516 XML testcase elements have exact `(classname, name)` identities; 372 pass, 81 fail, 62 error, one skipped. The ZIP SHA-256 is **`f0da81cc7c13bb8e8c0bac64f6a389b32a96c79406ec67fa6780b71bca76cb70`**, exactly matching the GitHub artifact digest. The decompressed `integration.xml` SHA-256 is **`2851d730e6bafd2452071c7e13f70ee7b1eaf7c24503f9201f51c89b09c14d40`**. There are **64 distinct full literal failure/error `message` strings** in this job (60 distinct first-line signatures), with exact per-message testcase counts held in the XML and updated compressed inventory. These numbers exclude the separate declared skip.

Largest literal error/failure groups (counts are XML rows grouped by full `message`, not independent root causes):

| Count | XML outcome | Literal message or its relevant leading literal line |
|---:|---|---|
| 26 | error | `failed on setup with "astrid.sdk.timeline._command_state.CommandError: replacement changes provider-managed edges"` |
| 16 | error | `failed on setup with "IndexError: list index out of range"` |
| 14 | error | `failed on setup with "runtime_protocol.errors.RuntimeErrorBase: candidate.timing: legacy word anchor is missing"` |
| 7 | failure | `astrid.core.execution.generic_host.HostError: undeclared secret environment variable 'FAL_KEY'` |
| 6 | failure | `astrid.sdk.timeline._command_state.CommandError: created identity is occupied` |
| 6 | failure | `runtime_protocol.errors.RuntimeErrorBase: provider executed a different command` |
| 4 | failure | `AssertionError: Regex pattern did not match.` (full XML distinguishes the expected and actual text) |
| 3 | failure | `AttributeError: 'types.SimpleNamespace' object has no attribute 'session_ref'` |
| 2 | error | `failed on setup with "Failed: the Runtime checkout /home/runner/work/astrid-agent/astrid-agent/astrid-runtime has no commit df3d4ddac7bf73cd858106cc51a802521a4d3552"` |

All other literal groups and complete multiline messages are in the hashed original XML and the verified complete inventory. Do **not** equate these error text clusters with independent root causes or silently bypass credential, provider-edge or pinned-history contracts. The missing `FAL_KEY` can be a security/precondition issue; no secret is supplied. Runtime/SDK command outcome disagreements and historical commit availability need contract/ownership triage before a source change.

## Prior-plan exact-ID comparison

The comparator is **prior plan-branch** Lanes shard 3 [run 43934820639](https://github.com/banodoco/astrid-agent/actions/runs/43934820639), job `133536534907`, artifact [14277921134](https://github.com/banodoco/astrid-agent/actions/runs/43934820639/artifacts/14277921134) at head `b8f2692948d1b5987ee2938920f47aace0732792`. The old ZIP SHA-256 **`88e987ceeff7e87ba3d45b31c2a2ded5029d90f791a78e17355ac465b63544be`** and old XML SHA-256 **`bf717b7e9579957f65aa492687e217ff728e53110558cf62e629a834ef3d0862`** were checked from actual downloaded bytes.

The entire pair of XMLs has **516 shared exact IDs**, no old-only IDs and no current-only IDs. Outcomes are **372 P→P, 81 F→F, 62 E→E and 1 S→S**: zero prior-pass-to-red and zero prior-red-to-pass on this shard. Nine shared red IDs changed their literal `message` text while preserving outcome, involving generated transaction/transcript IDs, process metadata, HTTP result details or temporary archive directory names. This is not an outcome regression. The **frozen G1 shard-3 XML remains unavailable**; the prior-plan comparator is *not* the frozen baseline. Do not label G1's missing IDs fixed or regressed.

## Full merged-head CI and Lanes outcomes

| Workflow | Job outcomes | Verified test evidence |
|---|---|---|
| Agent CI 43967861168 | Completed failure; nine failing test jobs (Darwin + all eight unit shards), failed unit aggregate; five successful named jobs, landing reference skipped | 9 actual JUnit ZIP/XML artifacts; **31,351 tests, 882 failures, 398 errors, 55 skips, 549 per-job full literal-message groups**; 30 failing unit-6 subtests have no individual XML IDs |
| Agent Lanes 43967861160 | Completed failure; **five failing jobs** (opt-in + integration 1/2/3/4); installed wheel **passed** | 4 actual integration XML ZIPs, each 516 testcase records, total **294 failures and 260 errors**; opt-in log-only **12 failures**, 19 passed; **176 per-job full literal-message groups** for integration XML (6+51+64+55) |

Total Lanes failure/error occurrences are **566** (294 integration failures + 260 integration errors + 12 opt-in failures). The two workflows together have **1,188 failed + 658 error occurrences**; these are job-level occurrences and include aggregate pytest subtests with no standalone XML identity. All previous completed-job outer summaries and artifact hashes are in [the earlier report](completed-ci-lanes-followup-20261116.md). No new workflow, product or release-main run was initiated.

The 12 prior-plan-comparable jobs already reported **seven shared exact old-red→pass** and **three shared exact old-pass→red** cases. This final shard adds **no exact status transitions**. Changed shard memberships elsewhere remain unclassified, not inferred regressions. The three previously observed exact new reds (Darwin text-card deadline; unit-2 ComfyUI readiness reasons; integration-1 fcntl flags) remain diagnosis/ownership holds, **not** PR369 regressions proved by this comparison. Plan 55's target/host/SDK scope is WAITING.

## K1 prerequisite and boundary

Draft [Agent PR373](https://github.com/banodoco/astrid-agent/pull/373) is still **unmerged and has no submitted independent reviewer**; it selects two native Windows security tests that the previous passing Windows job's **112 real XML IDs omitted**, and changes their direct platform skip marks to the registered `windows_native` lane. Source inspection confirms the patch retains its lock, ACL, ACE and hardlink assertions, but this reading **is not independent review** and there is **no local focused/policy execution or hosted Windows test artifact for the draft**. Do not merge on this observation or count the guard green. The separate hardlink-unsupported runtime skip remains a distinct blocker; at least the other direct skip-policy gates remain unaccepted.

No change or ruling is made to the **uncommitted Runtime clip port (25 passed / 2 failed)** or its exact accepted-retry vs mandatory CAS-history integrity conflict. Runtime draft PR56 is orphan metadata only. Plan 38/55 WAITING, Release 15 excluded, inputs and task checkboxes unchanged. No auth retry/manual dispatch, no release/14/main or public main push/merge.

**Next bounded work:** independent review and genuine Windows proof for PR373; continue source-and-contract classification of historical Runtime checkout and provider-edge setup errors without relaxing expectations or assuming Plan 55 ownership. Formal G1/G2 and RS1 cannot close without their existing completion gates.
