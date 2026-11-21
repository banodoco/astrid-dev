> Historical research, not instructions. Where this differs from the current plan, inputs or tasks files, those win.

# H3 miscellaneous unknowns

Research is read-only except for this findings file. Code evidence is from `origin/release/14/plan-59` unless otherwise stated. “Resolved” below means the source evidence answers the stated implementation question; it does not imply inference quality unless explicitly said.

## 1. Do `<Video k>` / `<Audio j>` / `<Picture i>` bind a voice to a specific face in multi-speaker H3?

**Evidence.** In the official MiniMax H3 full-reference prompt guide, `<Audio N>` may be explicitly associated with a target speaker by naming `<Subject N> (Sx)`; its worked example ties `<Audio 1>` to `<Subject 1> (S1)`, and speakers are separately identified by stable `(Sx)` IDs. The guide says the labels preserve their meaning throughout the prompt. This documents the intended prompt-level mapping, rather than a hard binding in the node: the ComfyUI `MiniMaxH3ReferenceToVideo` implementation submits the prompt and typed reference items to the tokenizer (`nodes_minimax_h3.py`, lines 269–335 at [ComfyUI commit 6bfaacc](https://github.com/comfyanonymous/ComfyUI/blob/6bfaacc67c2103481e5f0c84d75257cd0581d86a/comfy_extras/nodes_minimax_h3.py)); it does not pair an audio slot with a face slot in code. The official prompt guide’s explicit subject/speaker convention is at [lines 217–220 and 336–350](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/refs/pr/69/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md).

Hivemind message **1572421386692206747** reports a related visual-reference ambiguity: “I do feel like it sometimes makes their face weird because H3 takes the distant face as a reference instead.” That is anecdotal and about competing face references; it does not establish voice-to-face binding. The searches did not find direct multi-speaker evidence.

**Verdict: still unknown.** The model docs prescribe a mapping, but neither the prompt tags nor code prove that the generated voice reliably follows the intended face. Cheapest resolution: one GPU spike with two visibly distinct people and two distinct short voice references, explicitly map `<Audio 1>` to `<Subject 1> (S1)` and `<Audio 2>` to `<Subject 2> (S2)`, have each say one distinct line, then inspect the faces and listen/transcribe each line. Swap the two audio assignments in a second seed/run if the initial result is ambiguous.

## 2. Does the rented-worker node revision match the schema Astrid reads?

**Evidence.** The rented-worker recipe `workflows/astrid_intro_h3_anchor_chain/workflow.py:24–34` pins ComfyUI to `6bfaacc67c2103481e5f0c84d75257cd0581d86a` and the Seitanism H3 motion pack to `361624fb406b63eb6694442eac6c895fc1533a70`. VibeComfy’s cached `MiniMaxH3AddGuide` schema records that same ComfyUI commit at `vibecomfy/porting/cache/object_info/comfy_core@cpu-runtime.json:58944–58952`; its `MiniMaxH3ReferenceToVideo` entry is likewise from `6bfaacc` (same file at lines 59287–59294). The cached schema therefore matches the worker recipe’s ComfyUI revision. The H3 node source at the worker pin is available at the official [ComfyUI commit](https://github.com/comfyanonymous/ComfyUI/tree/6bfaacc67c2103481e5f0c84d75257cd0581d86a).

There are two different pins that should not be conflated with that recipe/cache match: VibeComfy’s global `comfy_version_matrix.json:3–4` names default ComfyUI commit `ff7644a70dba1707f4caee52576496ce848792f8`, while the H3 `generation.py:1–4` source header identifies its node contract as `423cbd20511becb1f16122ab518e92e58bfa03d9`. The worker-specific recipe overrides the global default with `6bfaacc`; the source header remains a provenance discrepancy worth reconciling.

**Verdict: resolved yes for the rented-worker recipe versus the cached schema.** Both identify `6bfaacc`. The global default and the source header differ, so avoid using either as evidence of the worker’s effective pin. No live worker was inspected (the brief prohibits machine claims).

## 3. What does `MiniMaxH3AddGuide` do; does it work with Ref2VA, and can it pin an exact start image at frame 0?

**Evidence.** At ComfyUI `6bfaacc`, the node takes existing positive conditioning and a MiniMax H3 AV latent, plus optional image/audio guides and a `frame_idx`. It rejects a non-H3 nested AV latent and rejects having neither guide. For an image it requires the video VAE, resizes/encodes the guide, and appends a `minimax_keyframes` entry with `resolved_frame_index` equal to the supplied frame index. `frame_idx=0` is valid and is not adjusted (`nodes_minimax_h3.py:151–219`; schema cache inputs at `comfy_core@cpu-runtime.json:58944–59018`). Thus the graph can place the image’s encoded latent as a frame-zero anchor. “Exact” here means exact anchor index and input image passed through the VAE; the code does not promise pixel-identical decoded output.

The node accepts conditioning and latent from another H3 conditioning node, so it is structurally composable after Ref2VA. However, source code/schema do not establish that the Ref2VA path honors the added `minimax_keyframes` at inference. The plan spec also records this as “unverified with ref2va.” Hivemind searches produced no direct AddGuide/Ref2VA result.

**Verdict: still unknown for Ref2VA compatibility; resolved yes for structural frame-zero anchoring.** Cheapest resolution: one GPU spike using the pinned Ref2VA workflow, a deliberately unmistakable start image, and `MiniMaxH3AddGuide(frame_idx=0)` connected to the Ref2VA positive and latent outputs; inspect output frame 0 against the input and compare with an otherwise identical run without AddGuide. This tests actual rendered adherence, not just successful graph execution.

## 4. Can Character Swap reuse the existing video-reference binding as-is?

**Evidence.** `_compile_character_swap_v2` already selects one typed image plus one typed video reference and builds `video_reference_rows` with the video binding, range, and audio flag (`compile.py:838–863`). It calls the shared `build_generation_workflow`, passing image references as `reference_0` and the video row separately (`compile.py:873–887`; compiler manifest identifies `<Video 1>` and `<Picture 1>` at `compile.py:987–995`). The builder has the existing video loader loop: it registers a managed video input, loads it at 24 fps, binds it to `ref_videos.ref_video_N`, and, when enabled, binds that same video’s soundtrack to the paired `ref_video_audios.ref_video_audio_N` input (`generation.py:346–364`). The target call at `generation.py:375–376` connects the audio VAE on line 375. The node numbers enabled video soundtracks ahead of standalone audio, so declaration order alone cannot identify the speaker slot.

Hivemind message **1572496981547421728** describes an H3 workflow using reference images and prompt together, but offers no specific evidence about Astrid’s Character Swap binding. No Hivemind item was found that changes the code conclusion.

**Verdict: resolved yes, for reusing the existing typed binding in the compiled graph.** Character Swap already routes its typed video reference through the shared builder, with optional soundtrack, alongside the replacement image. This establishes workflow wiring only; the compiler explicitly does not claim Character Swap inference quality or live GPU acceptance (`compile.py:995–997`).
