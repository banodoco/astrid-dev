# Warm generation probe: `950023c8` vs release base `48b5fa9e`

Ran the reviewer's unchanged standalone probe from `review-81/scratch/second/probe_warm_generation.py` against two isolated source trees, at low scheduler priority (`nice -n 19`). The `950023c8` tree was made from `git archive` at the exact commit, so the dirty `/tmp/option-a` checkout was not used. Both arms received the same probe bytes (SHA-256 `6e90852811369299d3f6844084d625657df3579886e1ce0530afe6638ca81af5`). The probe builds an identical temporary committed cache, warms the Spare pack, mutates it to `[]` during the second Integer lookup, then records the emitter outcome and final-path existence.

| Revision | Outcome | Final Python | Final sidecar |
|---|---|---:|---:|
| VibeComfy `950023c8846233f0006aac100d26b76711c42515` | Emitted digest `f34fab9f749d2b1fed9458ca0daf39183a62e81815676013d24c1cc00a5d40fe`; 32 Integer lookups | Present | Present |
| VibeComfy `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` | `ObjectInfoCacheCorruptError: object_info generation artifact 'custom_nodes.Spare@v1.json' failed its hash check next action: vibecomfy schemas refresh`; 11 Integer lookups | Absent | Absent |

This establishes the required failing-first behavior on `950023c8` and the refusal/no-publication behavior on the release base. The exact command was `nice -n 19 uv run --frozen --extra dev python probe_warm_generation.py` from each source tree. Raw outputs are [950023c8](./warm-generation-probe-950023c8.log) and [48b5fa9e](./warm-generation-probe-48b5fa9e.log). The 950 tree was an archive; the base worktree was clean at `48b5fa9e` before the temporary probe copy and is clean after it was removed. No product files were changed for this proof.
