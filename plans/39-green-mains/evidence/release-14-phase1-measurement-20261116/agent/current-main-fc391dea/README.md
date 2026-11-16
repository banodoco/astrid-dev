# Agent current-main exact-head snapshot

Snapshot taken once at 2026-11-16T21:56:43Z UTC from GitHub read APIs; no workflow reruns, dispatches, cancellations, or tests were performed.

Repository `banodoco/astrid-agent`, branch `release/14/main`, exact head `fc391dea696ec5799db222799a34f9de6a69659b`. All four run records report this head and attempt 1.

## Run and job inventory

| Workflow | Run | Run state | Job | Job state | Conclusion | URL |
|---|---:|---|---|---|---|---|
| Chat service | 43956914843 | completed / success | windows-launchers (133617848828) | completed | success | [job](https://github.com/banodoco/astrid-agent/actions/runs/43956914843/job/133617848828) |
| Chat service | 43956914843 | completed / success | chat (133617849509) | completed | success | [job](https://github.com/banodoco/astrid-agent/actions/runs/43956914843/job/133617849509) |
| Windows task host journey | 43956914988 | completed / failure | Windows task host journey (pwsh.exe) (133618183570) | completed | failure | [job](https://github.com/banodoco/astrid-agent/actions/runs/43956914988/job/133618183570) |
| Windows task host journey | 43956914988 | completed / failure | Windows task host journey (powershell.exe) (133618184010) | completed | failure | [job](https://github.com/banodoco/astrid-agent/actions/runs/43956914988/job/133618184010) |
| CI | 43956915061 | pending / pending | No jobs returned at snapshot | — | — | [run](https://github.com/banodoco/astrid-agent/actions/runs/43956915061) |
| Lanes | 43956915056 | pending / pending | No jobs returned at snapshot | — | — | [run](https://github.com/banodoco/astrid-agent/actions/runs/43956915056) |

Chat service succeeded in both jobs. The Windows journey failed in both shell variants at the same installed-profile SDK invocation step; each raw log is saved here. CI and Lanes were `pending` with zero jobs returned in the snapshot, so they provide no test results yet.

## Windows task-host journey: full error observations

Both jobs reached install, scheduled-task startup, health, pack-host ready, and the installed-profile SDK invocation. The invocation failed when it requested `astrid packs list --json`; the installed CLI reported an unknown `packs` command. Scheduled-task shutdown, process cleanup, diagnostic collection, and artifact upload then succeeded.

| Shell | Job | Conclusion | Failed step | Summary line |
|---|---:|---|---|---|
| pwsh.exe | 133618183570 | failure | Run an installed-profile SDK invocation through settlement | `unknown command 'packs'`; `RuntimeError: journey-packs-list.json: exit 2` |
| powershell.exe | 133618184010 | failure | Run an installed-profile SDK invocation through settlement | `unknown command 'packs'`; `RuntimeError: journey-packs-list.json: exit 2` |

### Distinct literal messages and counts

Counts are per job log (two job occurrences each unless otherwise stated). The `valid options` logical message is identical across both shells after preserving an un-timestamped continuation fragment in the powershell raw log; the physical line layout differs.

- **cli_unknown_command × 2** — `unknown command 'packs'` (jobs 133618183570, 133618184010).
- **fix_hint × 2** — `fix: astrid --help` (jobs 133618183570, 133618184010).
- **journey_wrapper × 2** — `RuntimeError: journey-packs-list.json: exit 2` (jobs 133618183570, 133618184010).
- **recovery_hint × 2** — `recovery: astrid --help` (jobs 133618183570, 133618184010).
- **state_snapshot × 2** — `state snapshot: {"command": "packs"}` (jobs 133618183570, 133618184010).
- **valid_options_logical_message × 2** — `valid options: backup, dev, developer, doctor, documents, generate, generation, h3_av, hivemind, local, media, preferences, projects, rendering, runpod, runs, setup, skills, tasks, timeline, timelines, training, vibecomfy, wan2gp` (jobs 133618183570 and 133618184010). The powershell log wraps this logical message after `local`; the continuation is preserved in the raw log and per-job record.

These logs contain a journey-step failure, not a pytest short-summary row. **No testcase ID is asserted or invented.**

### Frozen G1 comparison

The frozen G1 Windows journey run is [43888589737](https://github.com/banodoco/astrid-agent/actions/runs/43888589737) at `ab95803ce28fa51eec937b4074f5ec0f0439b98a`; its [pwsh job](https://github.com/banodoco/astrid-agent/actions/runs/43888589737/job/133373325591) and [powershell job](https://github.com/banodoco/astrid-agent/actions/runs/43888589737/job/133373326128) logs show the same unknown `packs` command and journey wrapper error. The current pair repeats the existing A-h / AT4 issue family, with the same failed journey step and same observed `packs` refusal. This is a symptom match only; these run records do not establish whether the App CLI or the journey expectation is at fault. Exact per-job messages and counts are in `snapshot.json`. Both jobs checked out Agent `fc391dea696ec5799db222799a34f9de6a69659b`, Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`, and App `de7dd1e668aa6dcf3cbce013c701fa7c76615f99`. Both diagnostic artifacts uploaded successfully: pwsh artifact 14273601073 (150,237 bytes, SHA-256 `1c690f53d74b3007f9668d9303cd4e66add984c6a1da80103622d2b979efd74e`) and powershell artifact 14273820614 (149,742 bytes, SHA-256 `9864837a8bb1d91a8d80d17fd60d26a854dc3ca8703f74cc408babb0db830f75`).

## Commit ancestry and change context

Commit `fc391dea696ec5799db222799a34f9de6a69659b` is a verified merge commit for PR #372, “Baseline gates pass on an improvement.” Its parents are `ce5fb85bd2afeb9266a2ba159b6be315c27e2b1f` and `52aa9a4f170c24760d1e2f5fb0450c67084c14a6`; compare metadata reports the frozen G1 SHA as merge base, 13 commits ahead and 0 behind. The 13-commit span includes short-result manifests, shorter installer paths, Windows path-budget tests, and baseline gates that permit improvements; the final merge changes 20 files per GitHub compare data. See `commit-comparison.json` for commit and file inventory.

## Evidence files

- `run-<id>.json` and `jobs-<id>.json`: exact one-time API snapshots, attempt 1.
- `job-<id>.log`: full decoded raw logs for both completed failing Windows jobs.
- `windows-pwsh.exe.json` and `windows-powershell.exe.json`: per-job status, failed step, and exact observed output lines.
- `snapshot.json`: aggregate run/job table, literal-message counts, frozen G1 comparison, and commit summary.
- `commit-comparison.json`: exact merge parents and compare summary against frozen G1 head.

## Subsequent source diagnosis

The [pinned-source contract trace](../windows-journey-contract-diagnosis.md) establishes a journey-harness entrypoint mismatch for the observed `packs` failure. It distinguishes driver checkout fc391dea from the release-manifest installed Agent9814193. This supersedes the snapshot-only uncertainty about that command symptom; downstream SDK/host/settlement behavior remains unproved. The two raw logs also appear in the [later Agent evidence archive](https://chatgpt.com/library?file_id=libfile_fde3_f-8c2f44b6a13c819180f448e4b5202a82_6b5886b89d0881919e73a1e3270986c8&account_id=personal).
