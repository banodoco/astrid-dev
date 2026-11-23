# Plan 81 Part 2b: receipts on the fixed head (23 November 2026)

Receipts for the VibeComfy plan head `f9790674` (PB-2 plus the review repair, [VibeComfy #185](https://github.com/banodoco/VibeComfy/pull/185)); the Release 15 Lead confirmed the gate on these numbers. The earlier receipts for `589e542a`, which had the two bugs the review found, are in [`../2026-11-23-part2b-installed/`](../2026-11-23-part2b-installed/).

**PB-4, installed `astrid generate --timings` against the stand-in ComfyUI** (A: base `48b5fa9e`, samples kept from the earlier run; B: `f9790674`, five fresh samples after a warm-up; same instrumentation both arms; attestation off as the run block rules):

| Arm | Samples (s) | Median (s) | Object-info SHA calls | Bytes hashed |
| --- | --- | ---: | ---: | ---: |
| A, base | 12.089, 12.134, 11.838, 11.828, 11.803 | 11.838 | 6,912 | 6,563,328,600 |
| B, fixed head | 5.942, 5.764, 5.513, 6.027, 5.829 | 5.829 | 246 | 287,596,236 |

Median saving **6.01 s** (accept line 3 s). Agent base `b324d7c1`, fixed local trial `f2dd1434` (generator pins and digest files only), Runtime `737843e9`. `SHA256SUMS` covers the files at the top of this folder.

**`pb3/`** all 53 ready templates, warm and cold, match `48b5fa9e` at `f9790674` on both bundle member digests, revisions, warnings and failures (`comparison.jsonl`, `summary.json`; the emitted bundles themselves are not filed).

**`inventory/`** the named test inventory by id: base 45 failed / 654 passed (10 files), fixed head 45 failed / 676 passed (13 files), identical failing ids (`base.ids`, `head.ids`). `six-*.log` are the single-id runs of the six candidate-only hosted failures (hosted 60 s timeouts) at base, `589e542a` and `f9790674`: all pass alone.
