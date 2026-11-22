# 432-clip backup — authenticated read-back not proved after authorized start

This is a partial 432-clip project, not the 616-clip fixture. The only seed ran once and stopped on a 300-second `list_timeline_commits` transport timeout. It was not resumed. The one-clip control remained at bootstrap and final fixture checks and manifest were not reached.

- App `be9cc2407306eff06252c0d54be1c7f5afcacf3f`; Agent `18adee8034973837a97fcd7392cd67f4566fa992`; Runtime `d7be2f0458a55c1f26e1138a125ffefe382f56f4`.
- Realm `0d6fd08f-8754-489c-8af9-276dcde43762`; project `23e489705d764d1497e6c9b830f55ffe`; timeline `save-loop-heavy-c2930794`.
- Public head `authoring-parent-revision-811ee570a87ee8eb1a3fd7d94309320dd12485a2db35aef4e1f774fb6d4ad69b`; publication `txn-f3cbd404b1a0417ebc39901a3cd2b97a`; 38 history entries, 432 clips, 9 tracks, 0 shot revisions, 342924 canonical document bytes. Canonical SHA-256 `5d8e8ce015e55bc0692ee906bc4d01d612e1dded960a65de75c8bfc6bc8c5036`. These are verified on the original live realm, not read back from the restore.

## Backup and proof

- Backup: `/root/codex/p77box/backup/realm-432`; authentication material remains at its original product-owned path `/root/codex/p77box/support/backup-auth.key`. Do not move either. The key was never opened, copied, printed, or hashed by the operator.
- The offline doctor passed schema, integrity and revisions. Its result is `09-doctor.json`.
- Stopped source database SHA-256 before and after backup: `1d0f661bb97ddf39c353f7d8538714da4d32c5dc44b4078688c096e7f8086060`.
- Signed manifest database SHA-256, actual backup database SHA-256, and authenticated restored database SHA-256: `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8`. Restore returned the recorded realm UUID; final re-hash of the preserved inactive restore agreed. These bytes do **not** equal the stopped source bytes.
- Source, backup and restore passed immutable `integrity_check`; table counts and deterministic logical digest `b07d26a00dd9f3e9dc794ae5c8ef1c652b42770f89a7eb6482ec69efc1594230` agree. Each reports page size 4096, page count 211542, freelist 0, journal mode delete, and no WAL or SHM. Details and all 57 table counts: `12-sqlite-compare.json`.
- The required authenticated read-back from an adopted copy is **not proved**. The single adoption attempt materialized the realm then exited 1 with `transport_timeout`; the 900-second history read was never started. The temporary Runtime was stopped idle-safe afterward. All three ports 2400, 17500 and 17501 are closed.

The successfully authenticated restore command was:

```sh
/root/codex/p77box/stack/program/versions/1d2700baa660/py/bin/astrid-runtime-protocol restore --backup /root/codex/p77box/backup/realm-432 --destination /root/codex/p77box/restore-432-proof
```

Use a **new, absent destination** for any future restore. The required adoption command was attempted as follows and failed; it is not a proven working route on this fixture:

```sh
HOME=/root/codex/p77box/stack/home XDG_DATA_HOME=/root/codex/p77box/stack/home/.local/share XDG_STATE_HOME=/root/codex/p77box/stack/home/.local/state ASTRID_NODE_EXECUTABLE=/root/codex/p77box/node-v20.19.4-linux-x64/bin/node ASTRID_RUNTIME_ADMISSION_TIMEOUT_SECONDS=600 /root/codex/p77box/stack/program/versions/1d2700baa660/py/bin/astrid-runtime workspace adopt --profile astrid --data-root /root/codex/p77box/readback-data --source-manifest /root/codex/p77box/stack/data/runtime/source-profiles/astrid.json --from /root/codex/p77box/restore-432-copy --realm-id 0d6fd08f-8754-489c-8af9-276dcde43762 --door-port 17501 --json
```

Preserved paths: stopped source `/root/codex/p77box/stack/data/runtime/realms/0d6fd08f-8754-489c-8af9-276dcde43762`; inactive authenticated restore `/root/codex/p77box/restore-432-proof`; copy `/root/codex/p77box/restore-432-copy`; materialized temporary data `/root/codex/p77box/readback-data`; App worktree `/root/codex/p77box/wt`. No cleanup of these proof paths was attempted after the failed adoption.

## Evidence and timing

Raw diagnostics, both full history pages, top-25 rankings, all five dumps and per-file SHA-256s are indexed in `phaseA/SUMMARY.md`; key artifact hashes are in `16-evidence-sha256.txt`. First history read: 342.104 s, 263792569 response bytes, 38 entries, Runtime CPU 337.01 s. Second: 34.709 s, same bytes and entries, CPU 25.16 s. The seed log and 36 accepted clip batch timings are `seed.log` and `07-accepted-batches.csv`. The resource probe is `probe.log` and has the restart gap recorded in `02b-probe-restart.txt`.

Seed: 16:28:28–18:02:02 UTC (1 h 33 m 34 s). Doctor: 18:15:04–18:19:48 (4 m 44 s). Backup: 18:20:12–18:29:51 (9 m 39 s). Restore: 18:30:14–18:39:30 (9 m 16 s). Copy: 18:39:56–18:39:57. Adoption: 18:40:13–18:55:15 (15 m 2 s), exit 1. Earlier npm and installer exact start times were not recorded; their logs and phase receipts are retained. Free disk was 52439024 KiB at preflight, 44927256 KiB before backup, 43054328 KiB before copying the restore, and 41170864 KiB after shutdown.

Specification differences encountered: the stock installer OMP archive returned HTTP 403; host approved an exact-commit local git transport substitution (`03b-install-retry.txt`). `astrid-runtime status` rejects `--profile`; the successful status omitted it. The pre-backup source and backup database byte digests differ despite the logical checks. The specified workspace adoption timed out, so no successful adopt command or restored authenticated read-back can be claimed.

## Authorized single start, 2026-11-22

At 18:58:54 UTC, with 42165071872 bytes free and all three ports closed, the installed Runtime `up` was attempted once on `/root/codex/p77box/readback-data` with the requested isolated environment and scoped 600-second admission. It exited 1 reporting “Managed Astrid selection is missing or inconsistent; no Runtime was stopped.” No Runtime discovery or PID appeared; status observations at 0, 30 and 60 seconds are in `readback/status.jsonl`. The monitor stopped after 72.6 seconds because the start had definitively failed; it did **not** wait 45 minutes. CPU time and stack dumps are unavailable without a Runtime PID (`readback/dump-60.txt` records the attempt); no later dumps were possible. Readiness was not observed and the single authenticated history read was not run. No second start was attempted.

Installed `down` returned idle-safe/stopped; ports 2400, 17500 and 17501 are closed. The preserved inactive restore still hashes to the signed backup database digest `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8`. Raw start, command response, status, shutdown and final hash are under `readback/`. The proof paths remain in place.
