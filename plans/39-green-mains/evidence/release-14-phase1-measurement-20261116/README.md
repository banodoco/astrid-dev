# Release 14 Plan 39 — phase 1 measurement and evidence package

<!-- CURRENT-MEASUREMENT-START -->
## Latest measurements and repair state

These are **provisional post-batch observations**, separate from the frozen G1 table below. G1 evidence and phase-1 acceptance remain incomplete; formal G2 is not closed and RS1 remains **0/1**. This session has made no push or merge to `release/14/main` or public `main`.

### Merged-head Agent CI/Lanes continuation checkpoint

A later read of Agent commit `6bbda788` (reviewed tree `c0a0cc55`) found completed failure jobs in attempt-1 CI/Lanes alongside unfinished shards. The [new partial qualification record](agent/merged-head-6bbda788/partial-qualification-20261116.md) preserves exact completed-job summaries, GitHub artifact IDs, verified ZIP and XML SHA-256 hashes, message counts, and old-versus-new *exact testcase-ID* comparisons. At this checkpoint, Darwin has 14 failures/1 error and one prior-pass-to-failure ID; CI unit shard 8 has 94 failures/2 errors and two shared prior-failures now passing; Lanes opt-in is 12 failures; integration 1 is 37 failures (one previous pass now red), and integration 2 is 77 failures/172 errors (one previous failure now passing). Previous and current shard membership differ, so absent prior IDs are **not** called regressions.

**These are provisional findings, not an accepted full-run G2.** CI shards 1–7 and Lanes shards 3–4 were still active at that poll. The two new exact-red tests require source/runner triage; no assertions were relaxed. Plan 38/55 remain WAITING, the Runtime replay/history owner rule is unaltered, Release 15 is excluded, and formal RS1 remains **0/1**. All updates in this continuation were confined to `astrid-dev` `p39/g1`.

### Current release heads

At the 22:11 UTC ref check on 16 November, Agent's release head had moved externally. Runtime and App still matched the frozen baseline. A workflow result at an older head does not qualify the new head.

| Repository | Current `release/14/main` SHA | Exact-head workflows |
|---|---|---|
| Agent | `fc391dea696ec5799db222799a34f9de6a69659b` | CI [43956915061](https://github.com/banodoco/astrid-agent/actions/runs/43956915061) and Lanes [43956915056](https://github.com/banodoco/astrid-agent/actions/runs/43956915056) pending; Chat [43956914843](https://github.com/banodoco/astrid-agent/actions/runs/43956914843) passed; Windows journey [43956914988](https://github.com/banodoco/astrid-agent/actions/runs/43956914988) failed. See the [separately dated current-head table](agent/current-main-fc391dea/README.md). |
| Runtime | `2537fed24385ec1c24f48a812e09af4bb63fb794` | CI [43888599361](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361); no exact-head Nightly as rechecked at 22:14:41 UTC. |
| App | `0b6ef16152dc3fa11246ccc2007da630c66d1a1a` | Tests [43883626058](https://github.com/banodoco/astrid-app/actions/runs/43883626058), Lanes [43883625781](https://github.com/banodoco/astrid-app/actions/runs/43883625781), E2E [43883625971](https://github.com/banodoco/astrid-app/actions/runs/43883625971); no exact-head Direct Journey as rechecked at 22:14:41 UTC. |

### Completed and partial plan-branch measurements

| Repository | Measured `release/14/plan-39` head | Run and outcome | Detailed evidence |
|---|---|---|---|
| Runtime | `359e2d7e55369562ca9513557282ea8aff7645bc` | CI **43954031461**, attempt 1: five failed jobs, **1,489** failure/error occurrences, **166** per-job literal-message groups | [All five summaries, complete messages, XML reconciliation and review](runtime/ci-43954031461/README.md) |
| Runtime | `359e2d7e55369562ca9513557282ea8aff7645bc` | Nightly **43954031460**, attempt 1: **121 failed, 498 passed, 20 skipped, 28 errors** | [667 exact-ID transitions](runtime/nightly-43954031460/comparison.md); [53 full XML-message groups](runtime/nightly-43954031460/full-xml-messages.md) |
| Agent | `b8f2692948d1b5987ee2938920f47aace0732792` | CI **43934820640**, attempt 1: nine failed jobs; XML totals **31,316 tests, 886 failures, 398 errors, 55 skips**. PR369 was not integrated in this measured head. | [Per-job summaries, messages and evidence limits](agent/ci-43934820640/README.md) |
| Agent | `b8f2692948d1b5987ee2938920f47aace0732792` | Lanes **43934820639**, attempt 1: five failed jobs, one passed wheel job; **566 failure/error records in 179 per-job literal-message groups**. Shard 3 has actual XML but no raw job log. | [Reconciliation and snapshot history](agent/lanes-43934820639/reconciliation/README.md) |
| App | `e94d7ab53f22c03cec6856ae469d952912b4ad52` | Tests **43938449477**, attempt 2: success. **21,205** Vitest passes are retained from successful attempt 1; only cancelled macOS tooling reran. | [Actual XML reconciliation](app/xml-reconciliation/reconciliation.md) |

Runtime CI has the same testcase ID sets in corresponding jobs before and after PR55: **1,230 error-to-pass and 54 failure-to-pass occurrences**, 186 error-to-failure occurrences, and **zero prior passes becoming red**. These counts are job occurrences, not globally unique tests. Newly reached failing assertions require diagnosis; a setup error turning into an assertion failure does not itself prove a regression.

Nightly has **462 old-red-to-pass transitions and one pass-to-failure**, for a net increase of 461 passes. Its 89 error-to-failure transitions expose previously unexecuted assertions. All three previous compiler setup errors now pass. The sole pass-to-failure case extracts a function from a former source file: Agent commit `4e6e8c9` deliberately moved it. The closure-parity contract is Plan 38 owned and remains waiting. See the [source and history diagnosis](runtime/nightly-43954031460/source-closure-new-red.md).

Four Agent Lanes jobs reproduce **423 exact G1 red IDs**: opt-in 12, integration 1 36, integration 2 250, integration 4 125. Shard 4 is compared with the separately dated late G1 supplement, not inserted into the frozen cutoff. The 27 explicitly Plan 55 owned failures in integration 1 remain waiting. Parameter-family similarities are not counted as exact recurrence. The last shard contributes **143 red XML records (81 failures, 62 errors)**, plus 372 passes and one skip; its 64 complete XML-message groups are retained. Its raw-log request returned `Transport closed`, so no outer pytest summary is invented. The old G1 shard-3 evidence is missing, and these 143 IDs are not labelled new regressions.

### Published repairs and remaining acceptance causes

Runtime [PR54](https://github.com/banodoco/astrid-runtime/pull/54) and [PR55](https://github.com/banodoco/astrid-runtime/pull/55) are merged into the plan branch at `359e2d7` (tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`). App [PR280](https://github.com/banodoco/astrid-app/pull/280) is merged at `e94d7ab`.

Agent [PR369](https://github.com/banodoco/astrid-agent/pull/369) is **merged** at `6bbda788c1a62abcdda242f85c7a1cae86c57d3d`. The remote candidate `72e7ed279c4623964c4584a098b48a9dab5bea12`, local candidate `fbe59a319d9419a875353c4176ff0bde749a9d75`, and merge all have the exact reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`. The prior-plan Lanes run was allowed to finish before this merge. New qualification runs are CI [43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) and Lanes [43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160), attempt 1; at 22:13 UTC they were queued and in progress respectively. No passing result is claimed for this merged head.

The batch contains **35 equivalent lane substitutions and one redundant gate removal**, preserving supported-platform eligibility. Passing cards preserve **41 selected cases before and after**. The six-module card separately preserves all **330 exact IDs and their outcomes: 262 passed, eight failed, 60 errors**, with full signature parity; its existing failures remain visible. Independent reviews cover the [six Linux modules](diagnosis/agent/k1a-linux-parity/review.md), [five parameter gates](diagnosis/agent/k1a-posix-parameters/review.md), and [three recovery gates](diagnosis/agent/k1a-posix-recovery/review.md). The final full policy proof remains red: **22 passed, one failed in 8.63s; 19 remaining direct gates**. The [current 19-gate assessment](diagnosis/agent/k1a-policy-fbe59a3/remaining-assessment.md) records every remaining owning test/fixture, dependency and hold.

Runtime [draft PR56](https://github.com/banodoco/astrid-runtime/pull/56) contains only the reviewed orphan-declaration removal, at `3833e205d745b668fa6cdc4e6670fd4558503cf4` (tree `2749ee50447b2082b198cf561c895796a6d09444`). The live test was already deleted by an earlier product change; this patch removes stale declaration metadata and preserves current project-reference controls. Six selected cases pass before and after. The count falls from 20 to 19 only when this draft is integrated; the cap of ten and authentic issue/owner/expiry requirements remain unresolved.

### Paused clip port: an unresolved product contract

The [strengthened partial clip port](runtime/k1b-clip-contract-strengthened/candidate.patch) is **uncommitted, unmerged and not accepted**. Its full focused run reports **25 passed and two failed**. The two atomic IDs expose the same preserved assertion: retrying an accepted edit after corruption of old media in its required history is expected to return the original receipt, but Runtime's accepted-history integrity guard returns **503 `CommitOutcomeUnknown`, reason `runtime_unavailable`**. No second acceptance is observed.

The [S-class source assessment](runtime/k1b-replay-contract/assessment.md) traces the conflict to the earlier exact-retry assertion in `3021a5b`, the normative `contract/commit-v2.md`, and the later deliberate CAS-history guard in `43407a18`. It does not establish permission to bypass history authentication or weaken the replay assertion. An explicit owner rule is needed: preserve fail-closed integrity refusal and clarify the replay guarantee, or design an independently authenticated receipt proof that can survive corrupt history. The latter is not an early return from the ledger. The first independent review found three coverage losses. The strengthened patch restores populated sibling/effect/registry-metadata preservation, precise refusal categories, and replay after a real intervening change. The [independent rereview](runtime/k1b-clip-contract-strengthened/independent-review.md) closes all three findings. Final proof remains **25 passed, two failed**, while legacy-authority controls pass **nine tests**. The atomic checks after the unchanged replay failure remain unexecuted and unproved; this is still not an accepted clip patch. Intermediate 19-pass/eight-failure evidence from test setup/assertion mistakes is retained alongside the corrected proof.

### Windows journey cause now traced

The [pinned-source diagnosis](agent/windows-journey-contract-diagnosis.md) establishes an entrypoint mismatch in the journey harness: it calls pack management through `python -I -m astrid`, which enters the gateway, while the installed `astrid` console entrypoint supports `packs list/add`. The run's driver checkout is Agent `fc391dea`, but the App's shipped release-13 manifest installs Agent `9814193a73f606719e81883a8be197d27dd361d4`. Workflow SHA and installed product SHA are recorded separately. Using the installed console executable for pack setup is a supported narrow correction candidate; it has not been implemented or qualified here, and the subsequent SDK/host/settlement assertions remain unexecuted. This diagnosis does not clear Plan38/55 ownership or phase acceptance.

### Retained raw evidence and limits

[Download the hosted evidence archive](https://chatgpt.com/library?file_id=libfile_fde3_f-3bf50906ce5c819199b0850de740fff6_6b5886b89d0881919e73a1e3270986c8&account_id=personal): **112 raw files**, 220,113,841 uncompressed bytes; 24,491,929-byte ZIP. SHA-256: `5f37945a6f1b1b9f44b4509f48f4bec92b79423b8577be16d1a6544f19cf466e`. It holds frozen-baseline logs, completed Runtime/App/Agent-CI logs and actual XML/ZIP artifacts, full testcase indexes and a hash inventory. Later Agent Lanes and current-release-head observations are retained separately in this package, with artifact identities and full per-job messages. Focused repair proofs and the partial patch are retained in this repository package.

[Download the later Agent raw-evidence supplement](https://chatgpt.com/library?file_id=libfile_fde3_f-8c2f44b6a13c819180f448e4b5202a82_6b5886b89d0881919e73a1e3270986c8&account_id=personal): **18 raw files**, 36,306,023 uncompressed bytes; 5,399,989-byte ZIP, SHA-256 `c8d2bc07bbf84e98350b9275cbd777bde436728e75ca854ebbae3fad2943fe18`. It preserves all four integration XML archives, the complete cross-shard testcase index, available Lanes logs, the recorded shard-3 transport error, completion metadata, and both current-main Windows logs. Its file hash inventory was verified. The missing raw shard-3 log remains missing.


Agent CI shard 6's XML reports **30 failing subtests without standalone IDs**, and its raw log could not be retrieved. These are aggregate-only failures; no individual IDs are invented. Missing, cancelled and unfinished G1 runs remain incomplete evidence. App Lanes/E2E/Direct Journey have no new exact plan-head run from this session. The [final exact-release-head workflow inventory](final-release-head-runs.json) was refreshed at 22:14:41 UTC. Secure sign-in was aborted, no manual workflow dispatch occurred, and no authentication retry was attempted.

A one-off continuation check is scheduled for **22:44:16 UTC** to inspect the new exact-head Agent runs and continue within the existing destination, ownership and replay-contract holds. This is a scheduled check, not a completed qualification result.

The [run-state snapshot](run-state/run.yaml), [rulings](run-state/rulings.md), and bounded task cards record authority, identities, evidence and holds. `inputs.md` and the plan task checkboxes are unchanged. Plan 38/55 owned tests remain waiting, and Release 15 remains excluded.
<!-- CURRENT-MEASUREMENT-END -->





**Package dated:** 2026-11-16 UTC  
**Scope:** frozen G1 baseline and retained provisional post-batch G2 Runtime/App/Agent measurement and diagnosis evidence.  
**Status:** evidence package only; all G2 results linked here are provisional post-batch measurements and required prerequisites remain incomplete. Formal RS1 remains 0/1 in retained records. Newer workflow candidates are not measured results.

## Frozen G1 baseline (17:26 UTC)

The historical cutoff is **2026-11-16 17:26:09–17:26:12 UTC**. It remains **52 jobs: 27 failed, 17 passed, 2 running, 1 cancelled, 5 skipped; 4,935 failure/error records and 810 per-job literal-message groups**. Four skipped jobs were expected; the Agent `unit` aggregate was skipped after failed dependencies. These are occurrences and per-job message groups, not independent cause counts.

The [full baseline Library HTML report](https://chatgpt.com/library?file_id=libfile_fde3_f-1aa7139eb6ec81919e9ca5d88c1f2b5f_6b5886b89d0881919e73a1e3270986c8&account_id=personal) holds message/count tables, exact heads, workflow/job links, triage and ownership mapping. The compressed [frozen report data](baseline-g1/final-report-data.json.gz) preserves the source rows losslessly.



Frozen baseline heads:

| Repository | Exact frozen head |
|---|---|
| Agent | `ab95803ce28fa51eec937b4074f5ec0f0439b98a` |
| Runtime | `2537fed24385ec1c24f48a812e09af4bb63fb794` |
| App | `0b6ef16152dc3fa11246ccc2007da630c66d1a1a` |

### Historical workflow and job table

| Repository | Workflow | Job (cutoff name) | Job ID | Result at cutoff | Available summary |
|---|---|---|---:|---|---|
| astrid-agent | Lanes | opt-in | [133451219675](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451219675) | completed / failure | 12 failed, 19 passed, 31254 deselected, 2 warnings in 183.22s (0:03:03) |
| astrid-agent | Lanes | integration shard 3 / 4 | [133451219876](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451219876) | in_progress | — |
| astrid-agent | Lanes | installed wheel | [133451219942](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451219942) | completed / success | — |
| astrid-agent | Lanes | integration shard 1 / 4 | [133451220016](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451220016) | completed / failure | == 36 failed, 480 passed, 32163 deselected, 13 warnings in 690.94s (0:11:30) === |
| astrid-agent | Lanes | integration shard 2 / 4 | [133451220033](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451220033) | completed / failure | = 78 failed, 266 passed, 32163 deselected, 22 warnings, 172 errors in 1911.72s (0:31:51) = |
| astrid-agent | Lanes | integration shard 4 / 4 | [133451220087](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451220087) | in_progress | — |
| astrid-agent | Windows task host journey | Windows task host journey (pwsh.exe) | [133373325591](https://github.com/banodoco/astrid-agent/actions/runs/43888589737/job/133373325591) | completed / failure | RuntimeError: journey-packs-list.json: exit 2 |
| astrid-agent | Windows task host journey | Windows task host journey (powershell.exe) | [133373326128](https://github.com/banodoco/astrid-agent/actions/runs/43888589737/job/133373326128) | completed / failure | RuntimeError: journey-packs-list.json: exit 2 |
| astrid-agent | Chat service | windows-launchers | [133373325597](https://github.com/banodoco/astrid-agent/actions/runs/43888589704/job/133373325597) | completed / success | — |
| astrid-agent | Chat service | chat | [133373326350](https://github.com/banodoco/astrid-agent/actions/runs/43888589704/job/133373326350) | completed / success | — |
| astrid-agent | CI | darwin native | [133426796454](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796454) | completed / cancelled | — |
| astrid-agent | CI | unit shard 7 / 8 (ubuntu-latest) | [133426796544](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796544) | completed / failure | = 250 failed, 5427 passed, 2 skipped, 25628 deselected, 2 warnings, 160 errors, 113 subtests passed in 3539.09s (0:58:59) = |
| astrid-agent | CI | unit shard 5 / 8 (ubuntu-latest) | [133426796667](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796667) | completed / failure | = 95 failed, 2214 passed, 29051 deselected, 10 warnings, 107 errors in 1948.67s (0:32:28) = |
| astrid-agent | CI | windows-native-and-installer | [133426796788](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796788) | completed / success | 15 passed in 9.04s; 40 passed, 48 deselected in 92.66s (0:01:32); 36 passed in 40.77s; 21 passed in 26.13s |
| astrid-agent | CI | release wheel / Python 3.11 | [133426796900](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796900) | completed / success | === installed Astrid wheel smoke PASSED ===; No broken requirements found. |
| astrid-agent | CI | unit shard 1 / 8 (ubuntu-latest) | [133426796979](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426796979) | completed / failure | = 44 failed, 5221 passed, 3 skipped, 26145 deselected, 60 warnings, 54 errors, 153 subtests passed in 4287.52s (1:11:27) = |
| astrid-agent | CI | release wheel / Python 3.12 | [133426797013](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797013) | completed / success | === installed Astrid wheel smoke PASSED ===; No broken requirements found. |
| astrid-agent | CI | unit shard 2 / 8 (ubuntu-latest) | [133426797081](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797081) | completed / failure | = 79 failed, 3865 passed, 19 skipped, 27453 deselected, 2 warnings, 51 errors, 26 subtests passed in 3095.41s (0:51:35) = |
| astrid-agent | CI | boundary | [133426797139](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797139) | completed / success | — |
| astrid-agent | CI | unit shard 3 / 8 (ubuntu-latest) | [133426797146](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797146) | completed / failure | == 31 failed, 1832 passed, 29604 deselected, 2 warnings in 2453.02s (0:40:53) == |
| astrid-agent | CI | unit shard 6 / 8 (ubuntu-latest) | [133426797162](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797162) | completed / failure | = 247 failed, 4913 passed, 6 skipped, 26330 deselected, 59 warnings, 4 errors, 92 subtests passed in 4248.86s (1:10:48) = |
| astrid-agent | CI | unit shard 4 / 8 (ubuntu-latest) | [133426797267](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797267) | completed / failure | = 28 failed, 2011 passed, 29409 deselected, 2 warnings, 19 errors in 2385.31s (0:39:45) = |
| astrid-agent | CI | unit shard 8 / 8 (ubuntu-latest) | [133426797296](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797296) | completed / failure | = 98 failed, 3861 passed, 25 skipped, 27481 deselected, 2 warnings, 2 errors, 202 subtests passed in 1476.36s (0:24:36) = |
| astrid-agent | CI | fast checks | [133426797448](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426797448) | completed / failure | Ruff findings: current=2006 baseline=2008; ERROR: Ruff improved by 2; lock it in with `python -m scripts.reshape.compare_ruff_baseline --write-baseline`.; make: *** [Makefile:52: ruff] Error 1; process exit code 2.; Collection gate passed |
| astrid-agent | CI | landing reference | [133426798969](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133426798969) | completed / skipped | — |
| astrid-agent | CI | unit | [133477748086](https://github.com/banodoco/astrid-agent/actions/runs/43888589837/job/133477748086) | completed / skipped | — |
| astrid-runtime | CI | unit (macos-latest) | [133373360363](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360363) | completed / failure | 73 failed, 8340 passed, 130 skipped, 13 xfailed, 1010 errors, 60 subtests passed in 794.18s (0:13:14) |
| astrid-runtime | CI | sandbox-process-control | [133373360674](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360674) | completed / failure | 82 failed, 8355 passed, 26 skipped, 13 xfailed, 1014 errors, 60 subtests passed in 791.83s (0:13:11) |
| astrid-runtime | CI | darwin-native | [133373360752](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360752) | completed / success | — |
| astrid-runtime | CI | boundary | [133373360792](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360792) | completed / success | — |
| astrid-runtime | CI | windows-realm-publication | [133373360888](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360888) | completed / success | — |
| astrid-runtime | CI | typescript-client | [133373360942](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360942) | completed / success | — |
| astrid-runtime | CI | unit (ubuntu-latest) | [133373360947](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360947) | completed / failure | 77 failed, 8440 passed, 26 skipped, 13 xfailed, 1010 errors, 60 subtests passed in 713.82s (0:11:53) |
| astrid-runtime | CI | portability-lifecycle (ubuntu-latest) | [133373360980](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373360980) | completed / failure | 7 failed, 610 passed, 45 skipped in 50.13s |
| astrid-runtime | CI | portability-lifecycle (macos-latest) | [133373361197](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373361197) | completed / failure | 8 failed, 595 passed, 59 skipped in 54.01s |
| astrid-runtime | CI | landing reference | [133373364232](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361/job/133373364232) | completed / skipped | — |
| astrid-app | Lanes | checkout-lanes | [133355779879](https://github.com/banodoco/astrid-app/actions/runs/43883625781/job/133355779879) | completed / failure | Test Files  1 failed \| 4 passed (5); Tests  1 failed \| 89 passed (90) |
| astrid-app | Lanes | installer-powershell | [133355780201](https://github.com/banodoco/astrid-app/actions/runs/43883625781/job/133355780201) | completed / success | — |
| astrid-app | Lanes | installer-posix (ubuntu-latest) | [133355780219](https://github.com/banodoco/astrid-app/actions/runs/43883625781/job/133355780219) | completed / success | — |
| astrid-app | Lanes | quick-journey | [133355780419](https://github.com/banodoco/astrid-app/actions/runs/43883625781/job/133355780419) | completed / failure | 1 failed; astrid dev journey (quick): FAIL (failure); Total: 77.97s |
| astrid-app | Lanes | installer-posix (macos-latest) | [133355780727](https://github.com/banodoco/astrid-app/actions/runs/43883625781/job/133355780727) | completed / success | — |
| astrid-app | Tests | boundary | [133356532932](https://github.com/banodoco/astrid-app/actions/runs/43883626058/job/133356532932) | completed / success | — |
| astrid-app | Tests | vitest | [133356533395](https://github.com/banodoco/astrid-app/actions/runs/43883626058/job/133356533395) | completed / success | Test Files 1434 passed (1434); Tests 20870 passed (20870); Separate boundary command: Test Files 1 passed (1); Tests 335 passed (335) |
| astrid-app | Tests | release-tooling-macos | [133356533889](https://github.com/banodoco/astrid-app/actions/runs/43883626058/job/133356533889) | completed / success | — |
| astrid-app | Tests | release-guard | [133356535452](https://github.com/banodoco/astrid-app/actions/runs/43883626058/job/133356535452) | completed / skipped | — |
| astrid-app | Tests | landing reference | [133356609939](https://github.com/banodoco/astrid-app/actions/runs/43883626058/job/133356609939) | completed / skipped | — |
| astrid-app | E2E | playwright-timeline-chrome-export | [133369371361](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369371361) | completed / failure | 3 failed |
| astrid-app | E2E | playwright-default | [133369371821](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369371821) | completed / failure | 27 failed; 555 passed (29.0m) |
| astrid-app | E2E | extension-visual | [133369372026](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369372026) | completed / failure | 1 failed; 4 did not run |
| astrid-app | E2E | extension-cross-browser | [133369372244](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369372244) | completed / failure | 6 failed; 3 passed (2.0m) |
| astrid-app | E2E | extension-accessibility | [133369372249](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369372249) | completed / failure | 9 failed; 6 passed (3.9m) |
| astrid-app | E2E | playwright-timeline | [133369372355](https://github.com/banodoco/astrid-app/actions/runs/43883625971/job/133369372355) | completed / failure | 36 failed; 3 passed (9.5m) |

Workflow roll-up links: [Agent CI](https://github.com/banodoco/astrid-agent/actions/runs/43888589837), [Agent Lanes](https://github.com/banodoco/astrid-agent/actions/runs/43888589840), [Agent Chat service](https://github.com/banodoco/astrid-agent/actions/runs/43888589704), [Agent Windows task host journey](https://github.com/banodoco/astrid-agent/actions/runs/43888589737), [Runtime CI](https://github.com/banodoco/astrid-runtime/actions/runs/43888599361), [App Tests](https://github.com/banodoco/astrid-app/actions/runs/43883626058), [App Lanes](https://github.com/banodoco/astrid-app/actions/runs/43883625781), and [App E2E](https://github.com/banodoco/astrid-app/actions/runs/43883625971). No exact-head Runtime Nightly or App Direct Journey run was found at that cutoff.

Every G2 reference below denotes a **provisional post-batch measurement**; required prerequisites remain incomplete. The historical G1 baseline remains frozen as shown above.

### Literal-message/count table index

Each linked Markdown report contains the complete literal message and count table for its job. The paired losslessly compressed JSON retains exact test IDs, messages, detailed lines and anchors.

- G1: [full baseline Library HTML report](https://chatgpt.com/library?file_id=libfile_fde3_f-1aa7139eb6ec81919e9ca5d88c1f2b5f_6b5886b89d0881919e73a1e3270986c8&account_id=personal) — all available baseline distinct-message/count tables and triage.
- Late Agent Lanes shard 4 supplement: [message table](../release-14-first-repair-batch/baseline-supplement/lanes-integration-4-133451220087.md) and [complete outcome/message JSON](../release-14-first-repair-batch/baseline-supplement/lanes-integration-4-133451220087.json). This is a supplement observed later than the G1 cutoff; it does not change 52/4,935/810.
- Provisional post-batch Runtime CI G2 measurement, run 43938386357 (five failed jobs, 2,773 outer failures/errors, 170 per-job literal-message groups; prerequisites incomplete): [sandbox-process-control](runtime/ci-43938386357/job-133548963680.md), [portability Ubuntu](runtime/ci-43938386357/job-133548963714.md), [unit Ubuntu](runtime/ci-43938386357/job-133548963731.md), [portability macOS](runtime/ci-43938386357/job-133548963837.md), [unit macOS](runtime/ci-43938386357/job-133548963937.md). Full exact-ID data is paired in each same-named `.json.gz` file. The [measurement summary](runtime/ci-43938386357/measurement.json) and [XML reconciliation](runtime/xml-reconciliation/reconciliation.md) record totals and hashes.
- Provisional post-batch Runtime Nightly G2 measurement, run 43938386391, job 133548961758 (610 outcomes; 23 distinct per-job groups; prerequisites incomplete): [message table](runtime/nightly-43938386391-job-133548961758.md), [exact-ID JSON](runtime/nightly-43938386391-job-133548961758.json.gz), and [XML reconciliation](runtime/xml-reconciliation/reconciliation.md).
- App Tests run 43938449477, attempt 2: XML reconciliation shows 21,205 passing testcase records; [reconciliation summary](app/xml-reconciliation/reconciliation.md) and [run events](app/all-events-43938449477-response.json) are retained. This is a success summary, not a literal failure-message table.

## Follow-up observations and limitations

- Agent Lanes shard 4 was later observed complete; its supplement records 99 failed, 391 passed, 32,163 deselected, 8 warnings and 26 errors, with 125 exact outcome IDs and 55 full message groups. Agent Lanes shard 3 also later completed, but its log was closed by transport; no complete literal-message table is asserted for that shard.
- The original Agent Darwin job was cancelled and had no available job log. The original Agent unit shard 6 log exceeded transport limits; its outer summary was recovered, but the full raw log was not retained, so inner traceback evidence is incomplete.
- At the G1 cutoff, the exact-head Runtime Nightly and App Direct Journey were absent. The provisional post-batch Runtime Nightly G2 result is a different run/head observation; it does not fill the historical G1 gap.
- No giant testcase indexes, raw hosted logs, downloaded XML archives or ZIPs are duplicated here. XML reconciliation summaries retain artifact IDs, hashes and permanent GitHub artifact links. Full raw logs/XML for the completed snapshot are saved in the linked hosted evidence archive; this package retains report JSON/Markdown, parser, reconciliation summaries and focused proof logs.
- G1 remained incomplete evidence. No cancelled, unfinished or absent run is treated as a pass.

## Diagnosis and retained focused evidence

### Runtime setup and source-contract diagnosis

- A stale R1 Agent pin at `b05ac03a5bcab278bccf99d85b49f4037b5dec10` was corrected to the published R12 Agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`. The evidence establishes qualification for 3 operation tests and 29 compiler contract tests; this does not substitute for hosted integrated acceptance. See [pin/contract trace](runtime/agent-pin-contract-trace.md), [qualification review and logs](runtime/re1a-re4ab-tooling/README.txt), [compiler output](runtime/re1a-re4ab-tooling/compiler.log), and [operation output](runtime/re1a-re4ab-tooling/operation.log).
- The clip selector remained exit 1: 10 declared strict xfails and 17 deselected, with no passing test in that file. See [clip log](runtime/re1a-re4ab-tooling/clip.log).
- Keep the Nightly and sandbox findings distinct: Nightly lacked compiler provisioning; the sandbox had the compiler installed but omitted it from `PATH`. The retained [RE4a summary](runtime/re4a-nightly-compiler/summary.md) documents the initial Nightly setup blocker, while the focused [RE4 evidence](runtime/re4-proof.md) and full-file proof files record the sandbox `PATH` issue. Both require hosted integrated acceptance.
- Earlier Agent gate snapshot (before the later reviewed batches above): 14 gate replacements plus one redundant-gate removal accounted for 15 direct gates. The three reviewed cards had 19 selected cases passing before and after; separately, one stale cleanup-contract failure became a pass. This does not mean the full Agent gate suite passes. See the [filesystem six gate proof](diagnosis/agent/k1a-posix-filesystem-six/), [installer gate proof](diagnosis/agent/k1a-posix-installer/), and [POSIX publish gate proof](diagnosis/agent/k1a-posix-publish/), plus retained [skip-policy-after logs](diagnosis/agent/k1a-posix-installer/skip-policy-after.log), [publish skip-policy log](diagnosis/agent/k1a-posix-publish/skip-policy-after.log), and [cleanup-contract skip-policy log](diagnosis/agent/k1a-installer-cleanup-contract/skip-policy-after.log). The stale cleanup-contract before/after outcome is in [review](diagnosis/agent/k1a-installer-cleanup-contract/combined-review.md) and [after output](diagnosis/agent/k1a-installer-cleanup-contract/after.stdout).
- Ownership remains explicit: the Agent native-token test is excluded / waiting on Plan 38; Runtime installed-pair source-closure behavior is also Plan 38-owned, with issue, accountable owner and expiry metadata unassigned. See [ownership resolution](diagnosis/k1-ownership-resolution.md).
- The five Runtime job reports retain exact per-job literal messages. The CI diagnosis identifies stale pinned Agent API imports, the sandbox-local `tsc` PATH issue, K1b's 20 quarantined exact IDs against a cap of 10 with missing metadata, portability child environments missing `astrid`, and unresolved macOS watchdog behavior. These are triage findings, not a blanket classification of all failures as product/test defects.

### Package contents

- [Existing first repair batch review package](../release-14-first-repair-batch/README.md), including exact candidate patches, focused proof/review logs, and late shard-4 supplement. The original evidence is referenced in place; its README gains a navigation link to this later package.
- [Provisional post-batch Runtime per-job measurement directory](runtime/ci-43938386357/) — five Markdown count tables, matching gzipped per-job JSON, parser, metadata, artifact inventory and measurement summary; required prerequisites remain incomplete.
- [Provisional post-batch Runtime Nightly report](runtime/nightly-43938386391-job-133548961758.md) with exact-message JSON and XML reconciliation summary; required prerequisites remain incomplete.
- [App run metadata](app/) and XML reconciliation summary; no giant testcase index, XML file, ZIP or hosted raw log.
- [Diagnosis and focused contract evidence](diagnosis/) plus Runtime source-trace and repair evidence.

### Integrity and scope

The [SHA-256 inventory](SHA256SUMS) covers every copied file except the inventory itself. Per-job JSON is gzip-compressed without changing its decoded content. This publication changes evidence and navigation only. It does not change product tests, workflow execution, inputs.md or task/release records. No environment pip-freeze or temporary signed transfer URLs are included. Full raw logs/XML for the completed snapshot are saved in the linked hosted evidence archive.
