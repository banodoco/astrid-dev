# Plan 81 attribution completeness and combined range — 22 November 2026

## Scope and provenance

This is an evidence summary, not a performance claim. The combined A-4 source run is the clean pre-instrumentation baseline at Agent `315b8b7a9336ec3147b399f6bf6f168011d09b27`, Runtime `182311f9d363712c0339254bd27e091d0e18318d`, and VibeComfy `799d90f619a6723d0b376b7e77aef09c244a0821`. It contains five processes per route/mode, with separate plain-wall, timings, importtime, and cProfile distributions. The route tables and provenance are in [`2026-11-22-attribution-bundle`](2026-11-22-attribution-bundle/README.md), particularly `combined/tables/attribution-{W,I,E}.md`.

The A-3 instrumentation was developed on pre-fix Agent `315b8b7a9336ec3147b399f6bf6f168011d09b27` and retained in the instrumented tree `72bc29d88e0c1a605842a9f9407e5ca4dbfcb17a`, which descends from `315b8b7a9336ec3147b399f6bf6f168011d09b27`. Its independent collector `C` and occurrence scopes were tested and merged in Agent PR #524 at `9c95c680e645335a4a2ea8091f02b88934a2492b`. The instrumentation tree and merged A-3 result are separate facts; the clean A-4 source timings do not include A-3. The later Agent/Runtime `release/15/plan-81` heads are distinct from the attribution-only pre-fix tree and are not the parent of these pre-fix measurements.

No successful A-6 production sample is available. There is no measured A-6 `C` or `S/R` result in this record. Source-checkout measurements and the separately hosted installed A/B are distinct evidence sets; no installed outcome is inferred here. The A-4 `pack host source identity` stage applies to both source and installed code paths by code inspection, as recorded in prior source-label evidence (#1389). The installed path also has a separate verifier. A source run therefore does not establish installed savings or installed timing.

## Combined ranges

Each cell below is the five-process median; ranges are min–max. These are different process distributions. The `timings` and cProfile numbers must not be combined with plain-wall numbers as if they partitioned the same run.

| Route | Plain wall, seconds | Timings-mode wall, seconds | Importtime wall, seconds | cProfile wall, seconds |
| --- | ---: | ---: | ---: | ---: |
| W — workflow | 12.082247 (11.660194–12.559038) | 12.085370 (11.698617–12.334390) | 11.875733 (11.858366–12.455423) | 18.884807 (18.675092–22.031384) |
| I — image | 11.566748 (11.028328–12.080149) | 12.123561 (11.636938–12.346628) | 11.381852 (11.147795–11.622176) | 18.418344 (17.874915–20.033003) |
| E — image with entry | 15.425347 (15.135064–16.519653) | 15.930426 (15.602783–16.923032) | 15.753123 (15.425246–16.326477) | 34.392873 (33.816035–40.267050) |

The cProfile wall is perturbed. Its self and cumulative rows overlap, and cumulative rows are not additive. The largest cProfile self-time row is `openssl_sha256` in W and I (about 4.64 s and 4.44 s respectively in the profiled distribution); E shows a large `discover_pack_metadata`/YAML parsing subtree (about 18.9 s and 13.3 s cumulative, respectively, in the profiled report). These values explain sampled/profiled work, not a slice of plain wall.

The retained [`combined/manifest.json`](2026-11-22-attribution-bundle/combined/manifest.json) also records separate per-route medians, in seconds since process spawn, for Runtime admission emission, target acknowledgment emission, and CLI exit:

| Route | Runtime admission emission | Target acknowledgment emission | CLI exit |
| --- | ---: | ---: | ---: |
| W | 11.852 | 17.246 | 12.082 |
| I | 11.356 | 21.195 | 11.567 |
| E | 15.207 | 24.966 | 15.425 |

These are separate measured process medians, not differences of medians. The target acknowledgment emission can occur after CLI exit because the command uses `--no-wait`; the acknowledgment timestamp is a server emission observation, not a client receipt time.

## Attribution completeness table

“Measured” means a retained timing, count, or profile observation exists. “Attributed” means the evidence connects it to a code location or operation. Neither implies the value is portable to an installed build.

| Area | Evidence and route coverage | What is attributed | What remains open |
| --- | --- | --- | --- |
| End-to-end wall | Plain five-process distributions for W, I, E above | Whole command wall for the exact source fixture | No successful A-6 installed production samples; no savings or installed-before/after result established here |
| Timed `other command work` | Separate timings-mode process medians: W 6.686327 s, I 6.452376 s, E 6.183114 s | Remainder computed by the collector for work outside named timing stages | This is not itself a named operation. Do not add it to unrelated timing-stage medians or treat it as a percentage-of-plain-wall decomposition |
| `pack discovery` | Separate timings-mode medians: W 1.817729 s, I 2.781301 s, E 6.608134 s | `discover_pack_metadata` / `astrid/core/pack/discovery.py`; E is the largest listed named stage | Timing stage spans repeated calls and nested behavior; it does not account for every operation within the plain-wall run |
| Runtime launcher connection | Separate timings-mode medians: W 2.052320 s, I 1.046507 s, E 1.006597 s | `astrid/sdk/client.py` launcher connection path | Source measurements only. The source identity mechanism exists in both code modes, but this does not quantify installed behavior |
| Pack host stages | `pack host attachment`: W 0.502105 s, I 0.394091 s, E 0.238609 s. `pack host source identity`: W 0.271157 s, I 0.150641 s, E 0.137152 s | Attachment and source identity stages have code locations in `astrid/sdk/autobootstrap.py` and `astrid/sdk/host_bootstrap.py`; identity is applicable to source and installed paths by code inspection | These are source-fixture timing observations, not an installed profile or installed comparison |
| Bundle witness / hashing | W source CLI observer capture and cProfile reports; prior witness capture counted 2,348 `cache_file_witness` calls for one object-info file in the CLI process. Separate cProfile rows show repeated SHA-256 activity | Witness loop in VibeComfy and file hashing are identified in the profile/caller evidence; see the witness section below | CLI-only scope; host/Runtime processes are not covered; observer totals may be incomplete if it suppresses errors. These counts are not a global hashing budget or elapsed savings estimate |
| E discovery/YAML work | E cProfile shows `discover_pack_metadata` about 18.9 s cumulative and YAML loading about 13.3 s cumulative, in the perturbed profile | Pack discovery and YAML load/parse stack are connected to the large E profile subtree | Not a plain-wall decomposition and not an unprofiled per-file parse-time attribution for the complete process |
| A-3 coverage | Tested independent collector `C`; generation stage/occurrence scopes included in merged A-3 PR #524 | Instrumentation can report per-occurrence spans and named scopes on the instrumented source tree | Instrumentation does not make the clean A-4 measurements retroactively complete; A-6 production evidence is absent |
| A-5 count observer | Local unqualified draft and focused-run results | Scope is redundant witness/file-read seam plus observable discovery/launcher counts | No complete cross-process hashing gate or global hash-byte count. Each of two focused runs had 6 failures and 22 passes due to eager alias binding; host ruled local/unqualified, with no gate PR |

A-4’s separate timings-stage distributions are not an accounting identity for the plain-wall distribution. In particular, the three `other command work` values above are not “the unexplained share” of their corresponding plain-wall medians, and the separately measured stage values must not be summed to invent such a share. A-3 improves instrumented coverage, but did not produce a successful A-6 `C`/`S/R` production attribution. The 90% attribution target and a one-second command-time target are therefore not established.

## Witness attempts and limits

Attempts 01 and 02 each waited 600 seconds for an available timing lock/load condition and produced no samples. Attempt 03 stopped at the first untimed before-arm attestation: the host/descendant observation did not attest a qualifying execution of `vibecomfy/porting/object_info/consume.py`; the attempt failed closed and collected no valid timed A/B pair. Host notes suggest bundle emission may run in the CLI process, but this attempt did not establish that execution path. There is no measured witness before/after result from these attempts.

The archived attempts are `/root/codex/plan-81m/run/witness-attempts-2026-11-22.tar.gz`, SHA-256 `36200a120eb9178077c88266007082395075b782500f385c47819425ec8b5171`. Existing counts-based evidence remains limited to its observed process and fixture: the W capture reports 2,348 witness calls for one object-info file in the CLI process. It does not establish host/Runtime counts, complete process coverage, or elapsed savings. No claim is made that metadata equality proves unchanged file bytes.

## Source evidence pointers

- Clean A-4 combined wall, timing, import and profile tables: [`2026-11-22-attribution-bundle/README.md`](2026-11-22-attribution-bundle/README.md) and `2026-11-22-attribution-bundle/combined/tables/`.
- W witness caller capture and process/observer limits: [`2026-11-22-attribution-bundle/a2-hashing/witness/README.md`](2026-11-22-attribution-bundle/a2-hashing/witness/README.md).
- Failed A-6a environment warmup and import-path correction: `/root/codex/plan-81m/run/a6a-env-fix.md` (the correction enabled import discovery; it did not establish successful generation).
- Host’s attempt disposition and stop ruling: `/root/codex/plan-81m/run/to-codex.md`, 15:52 UTC, 22 November 2026.

