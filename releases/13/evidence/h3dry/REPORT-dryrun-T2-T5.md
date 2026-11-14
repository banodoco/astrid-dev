# h3dry — T2–T5 CPU dry-run evidence

Base: `cf49d41507f832e855630790b2e6907a11cc3947`, detached, clean before and after; compose `941fca2a4` is an ancestor. Route N; brief/launcher: Sol, medium. No product changes, commits, pushes, GPU work, downloads or provider calls. All generation commands included `--dry-run` and ran inside a new network namespace with the product worktree mounted read-only. Evidence date: 2026-11-14 UTC.

**Result:** unchanged T4 is admitted. Unchanged T2/T3/T5(a), and T5(b) with its audio intent retained, are refused. Video-only corrections are admitted. “ADMITTED” here means CPU declaration/preparation/compilation ready; every successful target is `pending_host_readiness`, with no live-target approval or pixel-preservation proof.

## Requests and actual results

All modes below are `video-edit`, as documented by the edit live-input README. All sources are 3 seconds, 72 frames at 24 fps and 1024×576. All admitted compilations request 72 frames, sample 73 internally, and declare one tail frame to trim. The public workflow identity is `h3_av_reference_generation` even for edits; the actual branch is `source_backed_v2v`.

Paths below are relative to this evidence directory. Error messages are verbatim. Public CLI errors use `input_rejected`; the underlying pack codes were separately confirmed in `pack-errors.json`.

| Request | Admission | Typed error / success | Graph facts / refusal line | Exact command and outputs |
|---|---|---|---|---|
| [T2](requests/T2.yaml) | REFUSED | `input_rejected: Only video regeneration is supported` | spec.py:287–293; underlying h3.spec.unsupported_op at ops[1]. No compiled graph. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T2.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T2`; [stdout](T2.output.json), [stderr](T2.stderr), [exit](T2.exit) |
| [T3](requests/T3.yaml) | REFUSED | `input_rejected: ops[0].during[0] is not representable on the native clock` | request_v2.py:110–114, called by spec.py:223; wrapped at spec.py:410–415 as h3.spec.invalid. No compiled graph. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T3.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T3`; [stdout](T3.output.json), [stderr](T3.stderr), [exit](T3.exit) |
| [T4](requests/T4.yaml) | ADMITTED | `exit 0; status ready; issues/fixes []` | Static mask_0, red channel; 72 source frames; steps 8; seed 42; Turbo 0.95. Native spatial mask route (source inspection below). | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T4.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T4`; [stdout](T4.output.json), [stderr](T4.stderr), [exit](T4.exit) |
| [T5a](requests/T5a.yaml) | REFUSED | `input_rejected: Only video regeneration is supported` | spec.py:287–293; underlying h3.spec.unsupported_op at ops[1]. steps=8 is valid; audio generation refuses it. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T5a.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T5a`; [stdout](T5a.output.json), [stderr](T5a.stderr), [exit](T5a.exit) |
| [T5b-v1-attempt](requests/T5b-v1-attempt.yaml) | REFUSED | `input_rejected: overrides contains unsupported field(s): turbo` | request.py:280 → _unknown at :98–101; underlying h3.request.invalid. v1 has no Turbo toggle. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T5b-v1-attempt.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T5b-v1-attempt`; [stdout](T5b-v1-attempt.output.json), [stderr](T5b-v1-attempt.stderr), [exit](T5b-v1-attempt.exit) |
| [T5b](requests/T5b.yaml) | REFUSED | `input_rejected: Only video regeneration is supported` | Real v2 settings.turbo.enabled=false, steps=20, retaining T2 audio intent. spec.py:287–293; h3.spec.unsupported_op. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T5b.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T5b`; [stdout](T5b.output.json), [stderr](T5b.stderr), [exit](T5b.exit) |
| [T2-video-only](requests/T2-video-only.yaml) | ADMITTED | `exit 0; status ready; issues/fixes []` | Native source_backed_v2v; edit [36,72); black mask 0–35, white 36–71; audio preserved; steps 8, seed 42, Turbo on. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T2-video-only.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T2-video-only`; [stdout](T2-video-only.output.json), [stderr](T2-video-only.stderr), [exit](T2-video-only.exit) |
| [T3-corrected](requests/T3-corrected.yaml) | ADMITTED | `exit 0; status ready; issues/fixes []` | v2 exact "1/6"; native source_backed_v2v; edit [4,72); black mask 0–3, white 4–71; audio preserved; steps 8, seed 42. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T3-corrected.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T3-corrected`; [stdout](T3-corrected.output.json), [stderr](T3-corrected.stderr), [exit](T3-corrected.exit) |
| [T5a-video-only](requests/T5a-video-only.yaml) | ADMITTED | `exit 0; status ready; issues/fixes []` | Edit [36,72); audio preserved; steps 8, effective seed 0; Turbo on at 0.95. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T5a-video-only.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T5a-video-only`; [stdout](T5a-video-only.output.json), [stderr](T5a-video-only.stderr), [exit](T5a-video-only.exit) |
| [T5b-video-only](requests/T5b-video-only.yaml) | ADMITTED | `exit 0; status ready; issues/fixes []` | v2; edit [36,72); audio preserved; steps 20; Turbo off; no LoraLoaderModelOnly and only four model requirements; default seed 123456789. | `/home/user/wt/h3dry.env/venv/bin/astrid generate video --entry h3 --mode video-edit --input request=/home/user/cells/evidence/h3dry/requests/T5b-video-only.yaml --input asset_map=/home/user/cells/evidence/h3dry/asset_map.json --placement runpod --dry-run --out /home/user/cells/evidence/h3dry/out/T5b-video-only`; [stdout](T5b-video-only.output.json), [stderr](T5b-video-only.stderr), [exit](T5b-video-only.exit) |

Execution wrapper: `unshare -mn bash /home/user/cells/evidence/h3dry/run.sh <request-name>`. `run.sh` preserves the full scrubbed environment, read-only bind mount, exact argv, and stdout/stderr redirections. Its PATH starts with the temporary environment. `--out` is accepted but this revision does not persist a dry-run directory there: plans are the stdout JSON files. Intermediate job directories named in stdout are ephemeral; retained compilation bundles are under `intermediates/`, indexed in `graph-facts.json`. T4 finished before its transient compilation directory was copied; its actual bindings/model requirements are in `T4.output.json`, and its node route below is established from the exact source.

## Preservation and graph facts

- Original T2 has no compiled graph: its audio generate permission fails canonical normalization. The admitted `T2-video-only` variant binds `video_mask_0`; its actual generated `bounded-mask.mkv` decodes to 36 black frames followed by 36 white frames (`graph-facts.json`). Thus frames 0–35 are protected and 36–71 are permitted to change. Permission to regenerate does not prove that every permitted pixel/frame will visibly change. Audio remains source audio for the entire timeline.
- Corrected T3 binds a per-frame video mask with four black frames followed by 68 white frames. This locates the intended seam at frame 4, with frames 0–3 protected. The original decimal 0.1667 seconds is 4.0008 frames and fails exact-grid validation; exact v2 `"1/6"` succeeds.
- The still clip is lossy H.264/yuv420p as requested. Its decoded frame 0 differs from `subject-bike.png` at 498,839 of 589,824 pixels (`still-frame-comparison.json`, decoded `still-clip-frame0.png`). A live preservation test must compare kept frames against decoded `bike-still.mp4`, not assert pixel identity to the original PNG. No generated candidate was made here.
- T4 binds `mask_0=5e4f279cfefea35e-resolved-mask.png`, channel `red`, source cap 72, start time 0. Its supplied mask is black except the half-open rectangle x=[384,640), y=[144,432), where it is white. This grants regional edits on all 72 requested frames and protects the other 516,096 pixels/frame. Source audio is protected. Spatial preservation is an intended composition/verification contract, not demonstrated output equality.
- Native mask path: `compile.py:1048–1053` selects `_compile_native_masked_edit` for v1 edits; v2 source-backed edits do likewise at `:918–919`. The compiler resolves static masks at `:529–536`, temporally bounds them at `:537–542`, then builds the graph at `:557–567`. The graph uses `H3V2VGranularFractionalDenoise` in spatial mode, inside strength 1, outside strength 0, audio strength 0, crop disabled, and `invert_mask=False` (`generation.py:400–418`).
- Static T4 masks use `LoadImageMask`. Temporal corrections use `VHS_LoadVideoFFmpeg` → `ImageToMask` (red channel) → `H3V2VGranularFractionalDenoise`. Source video also loads through `VHS_LoadVideoFFmpeg`; reference target is `MiniMaxH3ReferenceToVideo`; sampling uses `BasicScheduler` and `SamplerCustomAdvanced`. These classes are captured in the corrected variants’ workflow bundles and `graph-facts.json`; static loader selection is source-backed at `generation.py:396–399`. No LanPaint nodes are selected.
- Requested temporal masks end at frame 72. The internal 73rd frame is padded with a black preserve mask; source video repeats its last selected frame and source audio gets silence for the internal tail (`generation.py:368–395`). Composition owns exact trimming and source paste-back (`compose.py:1302–1318`); regional verification rejects changed outside-mask pixels (`compose.py:678–680`).
- T5(a) admits steps 8 once unsupported audio regeneration is removed. T5(b) admits steps 20 with Turbo disabled once audio regeneration is removed. Turbo-off is confirmed by absence of `LoraLoaderModelOnly`, absence of Turbo in connected/model requirements, and absence of public guidance binding. v1 and v2 omitted-seed defaults differ (0 versus 123456789 here); set an explicit common seed for a controlled live comparison.

## LanPaint / README discrepancy

`shared/compile.py:183–203` contains a real LanPaint helper, including:

```python
mask_id = change.get("mask_asset") or area.get("mask_asset")
if area.get("full_frame"):
    binding = internal_full_frame if mask_id is None else asset_binding.get(str(mask_id))
else:
    if mask_id is None:
        raise CompilationError(f"changes.video[{index}] regional edits require an explicit mask asset")
    binding = asset_binding.get(str(mask_id))
```

It assembles frame-keyframe and independent audio schedules through `:226`. It can represent explicit regional masks as a helper, but it is not reached by the active edit dispatch. `_compile_lanpaint` remains defined at `:382`; `compile_prepared` instead selects the native masked edit at `:1053`. Thus the claim “LanPaint admits this current request” misidentifies the active route.

`README.md:49–52` says:

> The composer applies temporal full-frame video permissions and whole-stream audio intervals. Regional spatial masks, channel-specific audio edits, continuation, audio-only timelines, and separate timeline audio or image anchors fail before execution.

Its regional-mask refusal statement is stale for ordinary source-backed edits: unchanged T4 returns ready with the supplied static mask. The paragraph is located under the Character Swap section, so it should not be generalized to every h3 edit; this run does not establish regional support for Character Swap itself. `README.md:80–82` also describes the ordinary edit compiler as LanPaint, which is stale against `compile.py:1053`. No documentation was edited.

## Request format surprises and admitted YAML

1. `changes.audio: ... action: generate` is syntactically accepted by the v1 normalizer but refused by the active canonical subset (`spec.py:287–293`). Correct to `audio: []` to preserve source audio. This changes the requested audio behavior; no admitted equivalent of the original audio-regenerating edit was found.
2. v1 numeric `during: [0.1667, 3.0]` is off the native frame grid. v1 does not accept a rational string in that numeric interval. Migrate T3 to v2 and use exact `"1/6"`, or choose a different exact frame-aligned decimal boundary (which changes the seam).
3. v1 `overrides.turbo` is unsupported. The real toggle is **v2 `settings.turbo.enabled: false`**, with `settings.steps: 20`. `guidance: 0` only sets strength; it is not the explicit Turbo-off contract. Ref2VA is required by the v2 schema/normalizer when Turbo is disabled.
4. v2 has no `operation`, `source`, `output`, `content`, `changes`, or `overrides` top-level fields. Rename/map them as below; merely switching `version` is invalid. v1 remains supported, so the advisor’s v1 field names need no migration for T2/T4/T5(a).

| v1 | v2 |
|---|---|
| `operation: edit` | implied by bounded timeline media with edit permissions |
| `source.asset`, `source.range` | `media[]` asset/range, role timeline, modality video, at frame 0 |
| `output.duration` | `duration` |
| `content.prompt` | `prompt` |
| `changes.video[]` | timeline `edit[]`, `stream: video` |
| `area.full_frame` | `mask.full_frame` |
| `area.mask_asset` | `mask: {asset: frame-mask.png}` |
| `changes.audio[]` | timeline `edit[]`, `stream: audio` (generation still unsupported on this route) |
| `overrides` | `settings` |

All following complete YAML documents were actually admitted; each exact file and stdout is linked in the table.

### T2-video-only

```yaml
version: 1
operation: edit
source: {asset: bike.mp4, range: [0.0, 3.0]}
output: {duration: 3.0}
content: {prompt: "End state: the same bicycle and wall at dusk, long warm shadows, a street lamp flickers on. Quiet evening ambience."}
changes:
  video: [{during: [1.5, 3.0], area: {full_frame: true}, action: generate}]
  audio: []
overrides: {steps: 8, seed: 42}
```

### T3-corrected

```yaml
version: 2
prompt: "The bicycle begins to roll forward along the wall."
duration: 3.0
media:
  - asset: bike-still.mp4
    role: timeline
    modality: video
    at: {frame: 0}
    range: [0.0, 3.0]
    edit:
      - {stream: video, during: ["1/6", 3.0], mask: {full_frame: true}, action: generate}
settings: {steps: 8, seed: 42, turbo: {enabled: true}}
```

### T5a-video-only

```yaml
version: 1
operation: edit
source: {asset: bike.mp4, range: [0.0, 3.0]}
output: {duration: 3.0}
content: {prompt: "Gently brighten the scene."}
changes:
  video: [{during: [1.5, 3.0], area: {full_frame: true}, action: generate}]
  audio: []
overrides: {steps: 8}
```

### T5b-video-only

```yaml
version: 2
prompt: "Gently brighten the scene."
duration: 3.0
media:
  - asset: bike.mp4
    role: timeline
    modality: video
    at: {frame: 0}
    range: [0.0, 3.0]
    edit:
      - {stream: video, during: [1.5, 3.0], mask: {full_frame: true}, action: generate}
settings: {steps: 20, turbo: {enabled: false}}
```

T4 already admits its unchanged v1 YAML in `requests/T4.yaml`; no rename or added references are needed. An asset-map key exactly matches each referenced asset; map paths resolve relative to `asset_map.json`.

## Exact assets for a live reproduction

The following are the exact local CPU-admission inputs I would use for a controlled live reproduction. They are synthetic patterns, not photographic bicycle footage. T2/T5 use `bike.mp4`; T3 uses `bike-still.mp4` derived from `subject-bike.png`; T4 uses `bike.mp4` plus `frame-mask.png`. The still PNG is the T3 construction/reference baseline, not an additional graph reference.

| Asset | Bytes | Duration / frames | Format |
|---|---:|---|---|
| [assets/bike-still.mp4](assets/bike-still.mp4) | 29,054 | 3.000000 s; 72 frames; 24/1 fps; 1024×576 | h264/yuv420p + aac |
| [assets/bike.mp4](assets/bike.mp4) | 604,364 | 3.000000 s; 72 frames; 24/1 fps; 1024×576 | h264/yuv420p + aac |
| [assets/frame-mask.png](assets/frame-mask.png) | 3,449 | still; 1024×576 | png/rgb24 |
| [assets/subject-bike.png](assets/subject-bike.png) | 72,650 | still; 1024×576 | png/rgb24 |

SHA-256 values and full ffprobe stream metadata: `asset-inventory.json`. Exact bounded ffmpeg creation commands: `make-assets.sh`. Both videos have a 3-second AAC track; bike.mp4 has 440 Hz audio and the still clip has silence. Replacing these with real media changes digests and requires a fresh dry-run. Real inputs must retain the requested 24 fps, 1024×576 canvas, bounded duration and usable source audio for these preservation plans.

## Environment and scope of evidence

- First command was `df -h /home`: available 1.6G (>1.5 GB), 96% used. ffmpeg is 6.1.1-3ubuntu5. Temporary environment: `/home/user/wt/h3dry.env`.
- `agent-setup.sh` was invoked offline under `unshare -mn`; its editable install attempted an in-worktree egg-info directory and was denied by the read-only mount (`setup.log`, exit 1). No file was created there. Fallback copied package build inputs into the env, installed from the offline cache, and forced actual product imports from the original worktree via `PYTHONPATH`. Exact setup scripts/logs are retained.
- Cached Runtime wheel fallback reused warmrel4’s wheel: SHA-256 `1e8b9789e8ca487a1cc04dea22c1d2d0e341efe55689a62cec4b65ed4aab5968`. The product lock names Runtime `6855dfa8df65cf8ae4c002b57134d6505493c17c`; this fallback is a wheel, not a checked-out source attestation. VibeComfy used local object `dba38f8644c46f652376f2cd5112ea161e40f09b`. See `provenance.txt` for exact import origins and tree identity.
- Commands ran with isolated HOME/cache/tmp, `UV_OFFLINE=1`, `PIP_NO_INDEX=1`, `GIT_NO_LAZY_FETCH=1`, and Git protocols disabled. Network namespaces had no external interfaces. No `.env`, credential file or `~/.codex` was read. No `astrid machines`, git fetch, GPU inference or paid operation ran.
- Local object-store READMEs are archived as `h3-i2v-README.md`, `h3-video-edit-README.md`, and `h3-v2v-README.md`; no remote access was used.
- These are preparation/compilation observations only. No live sampling, composition, candidate verification, seam-quality, pixel equality or execution-memory claim is established.
- Temporary environment was removed; final repository identity/status and disk space are recorded in `cleanup.log`.
