# 432-clip project: measurements, backup and what was not proved (22 November 2026)

Raw records from the build machine hosted by the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG) for [Plan 77](../../plan.md). Nothing here is interpreted; the reading belongs to Plan 77's record.

**Tuple:** App `be9cc2407306eff06252c0d54be1c7f5afcacf3f`, Agent `18adee8034973837a97fcd7392cd67f4566fa992`, Runtime `d7be2f0458a55c1f26e1138a125ffefe382f56f4` (the Round 5 Runtime, which includes Plan 77's nine Runtime commits).

## What is here

- [READY.md](READY.md): the final statement of what was and was not proved. Start there.
- `seed.log`, `07-seed-failure.txt` and [07-accepted-batches.csv](07-accepted-batches.csv): the single seed, which stopped at 432 of 616 clips when `list_timeline_commits` did not answer within 300 s, and the time of each of its 36 accepted clip batches.
- [phaseA/](phaseA/SUMMARY.md): two read-only history reads on the live 432-clip project (342.1 s, then 34.7 s; 263,792,569 bytes each), stack dumps at 10, 30, 60, 120 and 240 s, the strict and recovery profile rankings, processor time before and after, and the counts.
- `08-*` to `16-*` and `readback/`: safe stop, doctor, backup, restore, the read-only comparison of the three databases, and the two failed attempts to start a Runtime on a copy of the restore.
- [host-instructions-phase-a-b.md](host-instructions-phase-a-b.md): the instructions the build's manager was given for these two phases.
- `00-*` to `06-*`, `install*.log`, `npm-ci.log`, `probe.log`: set-up, launch and the 30-second resource probe.

## What is not in Git

These stay on the build machine and are indexed by size and SHA-256. The two backup and restore results carry the backup's key identifier and signature, so only [a summary with those withheld](10-11-backup-restore-summary.json) is committed. The backup itself, the support directory and the key are not in Git and were never opened.

| File | Bytes | SHA-256 |
| --- | --- | --- |
| `phaseA/read1-page.json` | 494,225,974 | `c715506ef0839f445f5d3fa30131693f60732b461c2adfebaee3731ec65a41cc` |
| `phaseA/read2-page.json` | 494,225,974 | `c715506ef0839f445f5d3fa30131693f60732b461c2adfebaee3731ec65a41cc` |
| `phaseA/profile.json.py-spy.raw` | 13,159,173 | `7687f6f7917154a51dab4056d89897834aff1eb3c3245781364a5dbf890c955b` |
| `10-backup-432-result.json` | 216,092 | `4f08021ede51ab4d444095aab3d8244c1e14fc2ddc38f598c7516c85e8806ffe` |
| `11-restore-432.json` | 1,240 | `6b00e194fa15a34cec7109ef27ef405822837d673595798b5eef769f83ad7f5d` |

`phaseA/SUMMARY.md` lists a SHA-256 for every Phase A file, including the three above.
