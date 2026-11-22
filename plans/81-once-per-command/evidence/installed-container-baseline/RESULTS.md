# Installed-Astrid baseline on a container (22 November 2026)

Working evidence only, not a release claim (the release claim is the owner's own installed machine). Published Release 14 (build c0ad6b54) installed by the official installer into an isolated home; the only deviation is that the chat engine `omp` came from npm because its GitHub source was blocked for this session (the timed commands never call it). Stand-in ComfyUI on CPU; the commands queue with `--no-wait`.

| Group (5 runs) | Median | Range | 1-minute load before |
| --- | ---: | ---: | --- |
| `generate image`, same prompt | 15.55 s | 15.10 to 15.85 | 1.3 to 2.5 |
| `generate image`, changed prompt | 15.31 s | 15.06 to 15.80 | 2.3 to 3.1 |
| `timelines edit` | 1.13 s | 1.00 to 2.38 | about 3.0 |

The load gate (below 1.0) was never met, so treat these as indicative; a gated re-run follows in a quiet window. The installed build has no `--timings` on `generate`. One cProfile of the installed `generate image` (about 21.8 s of profiled CPU, inflated by the profiler): hashing in the VibeComfy workflow/object-info cache about 6.8 s, pack discovery about 5.5 s, entry-registry loading about 4 s, workflow build and emit about 7 to 8 s (see `run-1/profile-generate-top.txt`). Re-run: `run-installed-baseline.sh`.
