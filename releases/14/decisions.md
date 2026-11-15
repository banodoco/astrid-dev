# Release 14 decision log

Append-only. The NOW block is replaced; entries below it are never edited. Entries flagged **REVIEW** are user-visible changes, scope-vs-time trades, named exceptions or anything touching Release 13.

## Now

The live board is [run.md](run.md). This file is the append-only log of dated rulings.

## Entries

- **2026-11-15 10:45** **REVIEW** Hannah: "we need the next release to get it very fast, runpod is unimportant. Let's do a proper speed release after this one, focused on getting this as fast as possible. think through it from first principles." Release 14 is a local-first speed release; RunPod speed is out of scope. Relayed by the Release 13 orchestrator and logged at 10:47 in the [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md). The advisor drafted the plan from first principles with an independent review: [Plan 55](https://github.com/banodoco/astrid-dev/pull/662) (`plans/55-local-speed`, astrid-dev #662, not merged; D1–D7 open). The Release 13 publish is unaffected.

  The R13.1 RunPod speed work stopped at pushed branches (astrid-agent):
  - `r13/machines-r131` `ef7c4ac49`
  - `r13/machines-p6obs` `90299aa4f`
  - `r13/machines-wb-dispatch` `97a147705`
  - `r13/machines-p3split` `4aede1d2b`
  - `r13/machines-wa-life` (finishing)
  - `r13/machines-tier1-bprime` `0e8623989`

  Of these, `r13/machines-wa-life` (lifecycle warm attestation; flag off) and `r13/machines-p3split` (named per-phase timing) are donors for Release 14, together with the W-D in-process entry check in `abef725c1` and prepstop (already in Release 13). `r13/machines-wb-dispatch` and `r13/machines-p6obs` are rented-only and are not donors. Plan 54 is proposed (D7) to become RunPod-only and queue behind Plan 55.
