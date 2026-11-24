# PB-7c installed CPU timing result

Date: 2026-11-23 UTC. Candidate A source: `0615e4e99bc06c6b4d201447d8f9f99db3da2dba` (Plan78 merged frozen source), local Vibe pin trial `416abad02933392af73c5ae7a9c4dbb51abe173b`. Candidate B source: `9e243ac485f15b258dd31e3964fa3495cc10146a` (PB-7c fixed head), local Vibe pin trial `0605bae97d95207d8e7eb9cf990f658eb4f32ccd`. Both manifests request runtime `737843e9cb92c565c266452dde540832ee2c745b`, VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`; exact requested and installed manifests are retained here.

Both fresh isolated installs passed `projects list --json`, selected-version and `generate image --help` preflights. The help includes `--timings`. Both used identical `sitecustomize.py` timing instrumentation (SHA-256 `3de488ca2f9b1c18edef7414cc36d0661f32c999aaceee00db62102015b396d7`). A/B listeners were observed on separate ports 18232/18233; stand-in ComfyUI was on 18188. `ASTRID_AB_ATTEST=off`, so this result makes no listener-attestation claim. It is an installed CPU-container stand-in measurement, with `--no-wait`; it does not cover real ComfyUI node-info behavior or GPU work.

Five alternating measured pairs completed successfully with `--timings`. A wall times (seconds): 6.3336, 6.1256, 6.1193, 6.4334, 6.2345; median 6.2345 (reported rounded 6.234). B wall times: 5.0463, 5.1634, 4.9959, 5.0638, 5.1097; median 5.0638 (reported rounded 5.064). Median saving: 1.1707 seconds (18.8%). All 10 measured commands exited 0. Each sample started below the 1.0 one-minute load gate; load after the B commands rose above 1.0, as recorded in the raw timing records.

**Qualification: FAIL.** The authorized threshold is a 1.3-second median saving; the observed saving is about 1.171 seconds. This is the sole authorized run for this candidate, and no further samples were taken.

See `summary-ab.json`, `records.jsonl`, `setup-records.jsonl`, `raw/`, `load-samples.txt`, and `console.log` for full samples, timing stages, load observations, and command outputs. Source fetch proofs, local trial diffs, installer logs and manifest proofs are in `../../receipts/pb7c/`.
