# Plan 77 installed recheck — partial results

## Attempt 1 — Run 4

The first install failed in set-up before any product step. The Runtime commit existed on the source clone's remote-tracking ref, which was not made available as a named branch in the bare mirror used by the installer. The host authorized one second install in a new root. Run 4 remains as recorded in `/root/codex/p77box/run4/receipts/RESULT.md` and its existing checksum file.

The amendment setup block ran once, 05:04:29–05:04:36 UTC, exit 0. The installer ran 05:05:42–05:05:49 UTC, exit 1, reporting that Runtime commit `77c38d037f98f744bd8f41c15d95429c124a8003` could not be resolved. No restore or adoption was started. On the second attempt's preflight, 05:08:12 UTC, PIDs 5294, 5296, 5298 and 5300 were absent; no signal was sent. Run 4 before-install free space was 32,260,376 KiB. Its OMP transport substitution was `/root/codex/p77box/omp-cache`, commit `78f0e0960f471c2c62b943272a48c33366f239fe`.

## Attempt 2 — Run 5

Exact tuple from `firstcut-432-reviewed-pins/exact-tuple.txt`, SHA-256 `ae558705708ba32c54b9111c41092d85d9bff4af0f6e7f690913e552c5e10e2d`:

```text
846ce8cafdf8ca2e58a101a18242c9e50358f89c
b7f0e96a4934ddb4c123eab791a6e18efb8f79ac
f0ffe045411295fcbd9f73262d2506b7cd83e706
f19aed4c515df9bbaf85c4482bc4fed6aa243f9c
77c38d037f98f744bd8f41c15d95429c124a8003
```

- Section 1: `setsid nohup bash run5/receipts/section1.sh`, 05:09:19–05:10:58 UTC, exit 0. Both worktrees were clean; both exact commits resolved from named private mirror refs (`mirror-commits.txt`). The offline manifest checker passed (`manifest-check.txt`). The OMP source used `/root/codex/p77box/omp-cache` at `78f0e0960f471c2c62b943272a48c33366f239fe`, transport only. Installer 05:09:20–05:10:52 UTC, exit 0 (`install.log`, `install-exit.txt`); installed empty-realm down reported stopped and idle-safe (`installed-empty-down.json`). Original App manifest SHA-256 `eff2d1deb0da5b2910b21f6b21802b92bc53498c951f3dd20a22c6c2e595ac7e`; private manifest `618dd4538272ded0ed2f530f5394a6190e3dcc156663d64c2ab152bc3b7dfe95`; installed source profile `b5be1de76053fd5bbe6e86b075f1fbf6d312095c2dca72128df6bf2343e59e7e`.
- Section 2: `setsid nohup bash run5/receipts/section2.sh`, 05:11:23–05:19:51 UTC, exit 0. Authenticated restore 05:11:24–05:19:48 UTC, exit 0, realm `0d6fd08f-8754-489c-8af9-276dcde43762`, schema 33, database SHA-256 `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8`. `restore.json` has the two prohibited authentication fields removed. Proof and working hashes agreed (`pre-adopt-databases.sha256`).
- Section 3: `setsid nohup bash run5/receipts/section3.sh`, 05:20:21–05:33:48 UTC, classification exit 0; actual adoption exit 1. `adopt.json` reports `realm materialized at /root/codex/p77box/run5/stack/direct-data/runtime/realms/0d6fd08f-8754-489c-8af9-276dcde43762; finish with astrid-runtime up after resolving: transport_timeout: runtime request timed out`. The target and selected catalog passed the runbook's exact checks (`selected-catalog-check.json`). No restart or resume was run.
- Section 4: `setsid nohup bash run5/receipts/section4.sh`, readiness 05:34:24–05:34:24 UTC, exit 0. Time from adoption start to observed healthy: 843 seconds (14m03s), not a browser-open time. `discovery-safe.json`, `health.json`, and `door-health.json` record PID 7685, process birth `proc-start-ticks:4849884;boot:faef980d-65dd-4ae0-bc58-fdaee8072985;pidns:4026531836`, instance `f82aab3da4f04e87888e34e0b6a7f8ec`, the exact selected realm, protocol and schema digest. Health responses report status `ok`; their service records include pack-host `failed`, restart count 5, and chat `starting`, reason `readiness_timeout`.
- Section 5 build: `setsid nohup bash run5/receipts/build.sh`, 05:35:10–05:36:10 UTC, exit 1. `npm ci` completed; the subsequent compiled build command reported `Astrid's engine isn't running` and `runtime is unavailable at http://127.0.0.1:38175 ... The operation was aborted due to timeout` (`build.log`). No compiled output proof, preview or browser was started. Cold browser open: not measured. Same-process reopen: not measured. Browser request counts and timeline commit POST counts: not measured; no browser was started. No SDK history read or edit was run.
- Section 6: `setsid nohup bash run5/receipts/section6.sh`, 05:36:56–05:37:26 UTC, exit 0. `adopted-down.json` reports `status: stopped` and `idle.safe: true`. Proof, working and adopted database hashes all equal `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8` (`post-stop-databases.sha256`); adopted SQLite `user_version` was 0 (`adopted-schema.json`). Ports 2400, 17500 and 17501 each returned connection refusal (`ports-after-stop.txt`); PID 7685 was absent after stop.

Run 5 disk checks (`run4-disk-preflight.log`): before install 31,742,876 KiB; after restore 26,090,192 KiB; before browser build 25,150,040 KiB. All three gates passed. The proof restore's DB digest is unchanged. The backup and stopped source were not re-hashed during this run, so unchanged status is not independently verified. No pod was created.

The authenticated restore and exact readiness checks passed. The authenticated editor read-back, full document and identity proof, compiled browser open, reopen and request counts remain unproved. A fixture inventory was extracted from the previously recorded outbox into `fixture-inventory.json` with provenance and assertions in `fixture-extraction.json`; it was not used for browser observation. Its source SHA-256 was `9346d2d69188f1793f1abff3be6e2d5abfc3eae38dbf5861ed037f69797f8943`.

Created roots: `/root/codex/p77box/firstcut-432-reviewed-pins/` with the App and Agent worktrees and tuple; `/root/codex/p77box/run4/` and `/root/codex/p77box/run5/`, each with stack and receipts; operator scripts and result in `/root/codex/p77box/run4-manager/`. Full command scripts and all run receipts are under each run's `receipts/`; the Run 5 installation, mirrors, working restore and adopted data remain under `run5/stack/`. No cleanup was performed. Run 5 receipt hashes are in `run5/receipts/SHA256SUMS`.

## Disposition

The host recorded attempt 2 as stopped at the compiled build in section 5. No browser observation was made; no further attempt, restart or resume is authorized, and the Runtime was not started again. The post-stop raw log extract is `run5/receipts/post-stop-log-extract.md`; the available service logs have no per-entry timestamps, and the adoption journal does not name final-verification start or end. Runbook section 6 names hashes for the proof, working and adopted databases; it names no hashing command for the signed backup database or stopped source database. Those two were therefore not re-hashed, and their unchanged status remains unverified in this run.
