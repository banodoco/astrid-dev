# An ordinary managed start of the 432-clip project (22 November 2026)

Raw records of one ordinary start of the installed Runtime on the existing 432-clip project, on the build machine hosted by the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG), ordered by [Plan 77](../../../plan.md)'s host. Nothing here is interpreted. [RESULT.md](RESULT.md) is the run's own account.

**Tuple:** App `be9cc2407306eff06252c0d54be1c7f5afcacf3f`, Agent `18adee8034973837a97fcd7392cd67f4566fa992`, Runtime `d7be2f0458a55c1f26e1138a125ffefe382f56f4` (the Round 5 Runtime; not stock Release 15 and not the first cut).

- **Command:** the installed `astrid-runtime up --profile astrid --data-root <the stack's data> --door-port 17501 --json`, in the stack's own environment, with no admission budget set (`02-start.txt`).
- **Outcome:** `up` exited 1 after 123.485 s with `realm root is not one healthy unambiguous canonical workspace` (`02-up.stdout`). No discovery or health response was observed and no Runtime process remained.
- **What ran:** a child process, `python -m runtime_protocol doctor --root <the realm>`, used one processor for the whole time: 30.48, 42.51, 58.93, 88.62 and 118.46 CPU seconds at the samples, then gone (`03-monitor.jsonl`). Stack dumps at about 44 s and at 120 s show it in JSON schema validation entered from `runtime_protocol/timeline_commit_validation.py` (`03-pyspy-30.txt`, `03-pyspy-120.txt`).
- **For comparison, from [the earlier records](../README.md):** the offline doctor on this same realm took 4 minutes 44 seconds with a 600-second budget.
- **Nothing was written:** the source database has the same SHA-256 before and after, with no WAL or SHM file; the verified restore is unchanged (`01-preflight.txt`, `06-postflight.txt`).
- **Not done:** the two authenticated reads, because the Runtime never became healthy. One attempt; nothing was retried.
