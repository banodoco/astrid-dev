# Installed-Astrid baseline on a container (22 November 2026)

Working evidence only, not a release claim (the release claim is the owner's own installed machine). Published Release 14 (build c0ad6b54) installed by the official installer into an isolated home; the only deviation is that the chat engine `omp` came from npm because its GitHub source was blocked for this session (the timed commands never call it). Stand-in ComfyUI on CPU; the commands queue with `--no-wait`.

| Group (5 runs) | Median | Range | 1-minute load before |
| --- | ---: | ---: | --- |
| `generate image`, same prompt | 15.55 s | 15.10 to 15.85 | 1.3 to 2.5 |
| `generate image`, changed prompt | 15.31 s | 15.06 to 15.80 | 2.3 to 3.1 |
| `timelines edit` | 1.13 s | 1.00 to 2.38 | about 3.0 |

The load gate (below 1.0) was never met, so treat these as indicative; a gated re-run follows in a quiet window. The installed build has no `--timings` on `generate`. One cProfile of the installed `generate image` (about 21.8 s of profiled CPU, inflated by the profiler): hashing in the VibeComfy workflow/object-info cache about 6.8 s, pack discovery about 5.5 s, entry-registry loading about 4 s, workflow build and emit about 7 to 8 s (see `run-1/profile-generate-top.txt`). Re-run: `run-installed-baseline.sh`.

## Run 2 (three-arm update)

Run 2, recorded 22 November 2026 at 16:32 UTC, used the same installed CPU-container/stand-in/`--no-wait` setup. It ran published before, candidate after and candidate vc48 in fixed order, with one warm-up and five measured runs per arm for each of same-prompt generation, changed-prompt generation and timeline edit (9 warmups, 45 measured, 54 total).

| Group | Before | After | vc48 |
|---|---:|---:|---:|
| Same-prompt generate | 15.183 s | 5.906 s | 11.294 s |
| Changed-prompt generate | 15.127 s | 5.453 s | 10.951 s |
| Timeline edit | 1.113 s | 1.147 s | 1.122 s |

Candidate commands used `--timings`; before did not. Workflow emission after/vc48 medians were 0.4261/5.8054 s (same) and 0.4146/5.6831 s (changed). These spans are nested measurements and do not sum to whole command time. The after and vc48 tuples also differ in Agent pin, so the comparison does not isolate VibeComfy's causal share.

Raw records support exclusive-row and collector-span accounting. The original records lack C although raw output contains it; `collector-spans.json` is a derived reconstruction. After medians for W−S / R / W−C were 0.8969 / 0.4412 / 0.4313 s (same) and 0.7688 / 0.4121 / 0.3407 s (changed); vc48 values were 0.8129 / 0.4419 / 0.3873 s (same) and 0.7168 / 0.3956 / 0.3103 s (changed). This does not provide an occurrence-count oracle or a whole-process 90% attribution claim. See `AB-RESULT.md` and `ab-run-2/` for limits and provenance.
