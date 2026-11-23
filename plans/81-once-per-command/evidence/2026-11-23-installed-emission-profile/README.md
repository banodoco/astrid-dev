# Where installed workflow emission spends its time (23 November 2026)

An investigation for the owner's question "what are the 6 seconds of workflow emission in `generate`, and is it work ComfyUI already does?", made after the [Part 2 installed run](../installed-container-baseline/runs/2026-11-23-part2-lead-machine/README.md) showed Part 2 saving nothing. [probe.py](probe.py) calls the real `emit_bundle` for the `qwen_image_2_1_turbo` ready template using the installed trees from that run, three repeats per arm, on the Lead machine (load 0.7 to 1.1). "Warm" loads the offline node list once before emitting, as `generate`'s earlier stages do; "cold" resets it.

| VibeComfy tree | mode | emit | SHA-256 bytes | file witnesses |
| --- | --- | ---: | ---: | ---: |
| 48b5fa9e (landed, vc48) | cold or warm | 5.5 to 5.8 s | 5.43 GB | about 7,550 |
| 675f5dc2 (PR 182, Part 2) | cold | 2.1 to 2.3 s | 1.52 GB | 2,034 |
| 675f5dc2 (PR 182, Part 2) | warm (the `generate` case) | 5.5 to 5.9 s | 5.44 GB | 7,560 |
| 36ea976f (bare per-class memo, laid over the vc48 tree) | | 0.79 to 0.83 s | 0.20 GB | |

Raw lines: [runs.txt](runs.txt); profiles: [prof-48-warm.txt](prof-48-warm.txt), [prof-675-cold.txt](prof-675-cold.txt); notes: [NOTES.txt](NOTES.txt).

**Findings.**
- About 5 of the roughly 6 s is re-witnessing the shipped offline object_info index (63 files, 13.7 MB): 476 class lookups for 13 classes make 1,904 reader syncs and about 7,600 file witnesses (sha256 3.98 s and reads 0.45 s of 6.84 s profiled, `prof-48-warm.txt`).
- ComfyUI-side checks (target check, target node list) cost about 0.004 s. The rest of emission (rewriting the workflow, the UI sidecar, compiling, writing) is about 0.4 to 0.8 s and is Astrid's own work, which the approval and provenance fingerprints depend on.
- Part 2's memo turns itself off when the reader was loaded earlier in the command (675f5dc2 `consume.py:273-276`), which is always so in `generate`; the dev measurement saw only the cold case. That is why the installed run measured no saving.

**What follows.** The Lead reopened Part 2 as a narrow Part 2b: a memo local to one `emit_bundle` invocation and passed down (never shared state, which removes the blind review's class (i) mechanism), applying whether or not the reader is warm, each file witnessed once per invocation and the whole read set re-witnessed once before any publication. Its gate is the same blind-review classes on the reviewer's existing reproductions, 53 identical templates, and one installed three-arm run with the hash count printed inside a real `generate --timings`; it is accepted only if it saves at least 3 s per installed command against vc48.

The investigation's own reasoning (not a measurement): emission across all 53 templates was not timed here; the base hashed about 630 GB across them in the earlier sweep, so other templates may cost more.
