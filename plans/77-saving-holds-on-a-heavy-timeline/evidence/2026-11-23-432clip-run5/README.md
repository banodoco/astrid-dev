# The first cut on the 432-clip project: install, restore and adoption (23 November 2026)

One read-only installed recheck of Plan 77's first cut on the signed 432-clip project, run on the Release 15 Lead's machine at the Plan 77 host's request ([the amended block](../2026-11-22-release-15/plan81-firstcut-rehearsal/432-firstcut-run4-amendment.md)). Raw receipts only; the Plan 77 lane interprets them.

**Sources.** App `846ce8ca`, Agent `b7f0e96a`, Runtime `77c38d03` (the reviewed first-cut heads before the freeze), with pins generated on the machine: App `f0ffe045`, Agent `f19aed4c` ([exact-tuple.txt](receipts/exact-tuple.txt)).

| Step | When (UTC) | Result |
| --- | --- | --- |
| Attempt 1, install | 05:05:42 to 05:05:49 | Exit 1. A set-up fault: the private Runtime mirror did not contain the commit. Nothing else ran. Record in [attempt-1-run4](attempt-1-run4/RESULT.md). |
| Attempt 2, install | 05:09:20 to 05:10:52 | Exit 0, after each mirror was shown to resolve its exact commit. |
| Authenticated restore | 05:11:24 to 05:19:48 | Exit 0. Database SHA-256 `5d1c249a…bbf8`, equal to the signed proof. |
| Adoption | 05:20:21 to 05:33:48 | The command exited 1 with "realm materialized … transport_timeout"; the runbook's catalog checks passed. No restart or resume. |
| Readiness | 05:34:24 | Passed. 843 seconds from the start of adoption to healthy. Health `ok`; the service records show pack-host `failed` after five restarts and chat `starting` (`readiness_timeout`). |
| Compiled build | 05:35:10 to 05:36:10 | Exit 1: "runtime is unavailable at http://127.0.0.1:38175 … The operation was aborted due to timeout". |
| Browser: cold open, reopen, request counts | | **Not measured.** No browser was started. |
| Stop | 05:36:56 to 05:37:26 | Stopped, idle-safe. Proof, working and adopted database hashes all equal the signed digest; the three ports refuse connections. |

Free disk: 30.3 GiB before the install, 24.9 GiB after the restore, 24.0 GiB before the build ([log](receipts/run4-disk-preflight.log)).

**Files.** [MANAGER-RESULT.md](MANAGER-RESULT.md) is the operator's step-by-step result for both attempts. [receipts/](receipts/) holds every receipt of attempt 2, with [SHA256SUMS](receipts/SHA256SUMS) (its own SHA-256 is `bc34460c…0050`); [post-stop-log-extract.md](receipts/post-stop-log-extract.md) quotes the build's three 3-second requests, where port 38175 came from, and the pack-host errors. [manager-prompt.md](manager-prompt.md) and [host-decisions.md](host-decisions.md) are what the operator was told, including the host's decision to allow one second attempt after the set-up fault and to record the stopped build as it was.

**Not done, and why.** The Runtime was not started again: restarting this project is the start-up case of [issue 1521](https://github.com/banodoco/astrid-dev/issues/1521). The service logs carry no timestamps, so their lines cannot be placed in the minute between readiness and the build. The backup's key was never read, copied or hashed, and fields named `key_id` or `manifest_hmac` are absent from every file here. The installation, mirrors, restore and adopted data stay on the machine under `/root/codex/p77box/run5/stack`.
