# Plan 81 Part 2b: installed timing and parity receipts (23 November 2026)

Receipts for cards PB-2, PB-3 and PB-4 of [Part 2b](../../tasks.md). Accepted by the Release 15 Lead on 23 November 2026.

**Result (PB-4):** real installed `astrid generate --timings` against the stand-in ComfyUI, one warm-up then five alternating samples per arm, same instrumentation in both arms. The accept line was a median saving of at least 3 s.

| Arm | VibeComfy | Samples (s) | Median (s) | Object-info SHA calls | Bytes hashed |
| --- | --- | --- | ---: | ---: | ---: |
| A, base | `48b5fa9e` | 12.089, 12.134, 11.838, 11.828, 11.803 | 11.838 | 6,912 | 6,563,328,600 |
| B, Part 2b | `589e542a` | 6.373, 6.084, 6.128, 6.074, 6.151 | 6.128 | 246 | 287,596,236 |

Median saving **5.71 s**. Agent base `b324d7c1`; trial Agent `fd9e83b0` differs only in the generator-written pins and derived digest files (`trial-pin-with-witness.diff`); Runtime `737843e9`.

**Caveats.** Runtime and listener attestation are off, as the run block rules. The SHA instrumentation overhead is in both arms. The container's proxy refuses GitHub archive tarballs, so both arms installed from local Git clones named in the manifests (`install-*.log`, `manifest-*.json`); component SHAs are identical in both arms.

**Files.** `measurement.md` is the summary; `SHA256SUMS` lists every file in this folder as of the run (check from the folder above `receipts/`; paths are relative to the original run root). `pb2-pb3/` holds the PB-2 focused, hash-count and overlap logs and the PB-3 comparison: all 53 templates, warm and cold, match `48b5fa9e` at `589e542a` on both bundle member digests, revisions, warnings and refusals (`pb3-comparison.csv`, `pb3-summary.md`).
