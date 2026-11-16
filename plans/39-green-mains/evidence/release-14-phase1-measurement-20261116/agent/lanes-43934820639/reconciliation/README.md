# Agent Lanes run 43934820639 reconciliation

Read-only evidence for attempt 1 at `b8f2692948d1b5987ee2938920f47aace0732792`. The prior partial snapshot, rechecked by the manager at 21:55 UTC, recorded: four failed jobs, installed-wheel pass, and shard 3 still running. A fresh completion snapshot around 22:11 UTC shows the run completed failure at 22:07:55Z: five failed jobs (opt-in and integration shards 1–4) plus the passed installed-wheel job. This is diagnostic evidence only, not G2 acceptance. The earlier partial snapshot is retained in `measurement.json` history.

## Job inventory

| Job | Conclusion | Summary/evidence |
|---|---|---|
| Opt-in 133536534262 | failure | 12 failed, 19 passed; no XML, log-based IDs/messages. |
| Integration shard 1 133536534579 | failure | XML: 36 failed, 480 passed; raw summary reconciled exactly. |
| Installed wheel 133536534771 | success | Passing receipt artifact 14261125354; not downloaded. |
| Integration shard 2 133536534820 | failure | XML: 78 failed, 172 errors, 266 passed; raw summary reconciled exactly. |
| Integration shard 3 133536534907 | failure | XML: 81 failed, 62 errors, 372 passed, 1 skipped. Raw-log request returned `Transport closed`; no retry. |
| Integration shard 4 133536534794 | failure | XML: 99 failed, 26 errors, 391 passed; raw summary reconciled exactly. |

## Files

- `measurement.json`: all six observed job results, artifact digests, preserved partial and completed snapshots, exact G1 comparisons, and Plan 38/55 holds.
- `testcase-index.json`: full testcase outcome index, including exact XML details for all four integration shards.
- `opt-in.json` / `.md` and `integration-1.json` / `.md`, `integration-2.json` / `.md`, `integration-3.json` / `.md`, `integration-4.json` / `.md`: per-job ledgers and exact literal message groups.
- `../artifacts/<artifact-id>.zip` and extracted `integration.xml`: original JUnit archives. Shard 3 is artifact 14277921134.
- `../job-*.log`: saved raw logs for the original four completed failure jobs. The one shard-3 log-fetch error is saved as `../job-133536534907-log-fetch-error.json`.

All four integration XML files contain 516 testcase records. Shard 3 artifact SHA-256 `88e987ceeff7e87ba3d45b31c2a2ded5029d90f791a78e17355ac465b63544be` matches the run artifact metadata. XML counts are 81 failures, 62 errors, 372 passes, and 1 skip (143 failure/error records). The one-shot raw-log request returned `Transport closed`; this shard's XML supplies testcase IDs, outcome status, full XML `message` attributes, and full XML detail text. It cannot supply the outer pytest summary line, deselected count, warnings, or elapsed time. Those values are not inferred.

## G1 comparison and limits

The old frozen G1 Lanes shard-3 job was 133451219876 at `ab95803ce28fa51eec937b4074f5ec0f0439b98a`; it remained in progress in the saved G1 snapshot and its full log is unavailable. Current shard-3 IDs were checked against the other saved G1 red-ID ledgers by exact node ID. No exact match was found there, but unmatched IDs are not called new regressions or prior passes because the corresponding old shard-3 evidence is missing. Per-ID triage uses that same limitation.

Current shard-3 failures/errors have no exact Plan 38/55 ownership matches in the inspected task documents or saved audited rows. Both scopes remain WAITING/unassigned; ownership is not inferred from path or test family. This does not clear either plan hold. Existing Plan 55 holds from shard 1 and all other G1 mappings are preserved in `measurement.json`.

The other four failure jobs remain at 423 failure/error IDs in total; shard 3 adds 143 XML failure/error IDs. The resulting cross-job selected outcome ledger is an aggregation of separate jobs, not a single pytest run.

## Retained raw archive

The source logs, XML/ZIP artifacts, full testcase index and completion snapshots listed above are preserved in the [late Agent raw-evidence archive](https://chatgpt.com/library?file_id=libfile_fde3_f-8c2f44b6a13c819180f448e4b5202a82_6b5886b89d0881919e73a1e3270986c8&account_id=personal). The repository package carries the per-job JSON/Markdown ledgers; large raw files and the unified index are not duplicated there.
