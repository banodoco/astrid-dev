# Ready-template digest gaps

VibeComfy revision: `ae7dd067f21f9df270b7c7d636d5415f5c87b7e3`.
Agent loader revision: `fc4b36d432b30f9cb8e6db44e5450ab338095039`.

Offline CPU survey: 52 ready templates loaded; 0 load failures; 0 manifest errors.
132 incomplete declared records across 31 templates.
31 templates still have gaps at the Agent managed-preparation manifest boundary.

Method: `repo_ready_template_discovery` -> `workflow_from_ready` -> `build_plan(...).models` for source-backed declarations, plus the Agent generation.engine contribution's exact `ComfyUIEngine.workflow_requirements([workflow])` builder, including `_pinned_locks()` / `load_recipe_model_lock` backfill. The Agent manifest calls `size_bytes` `size`; this report uses `size_bytes` throughout.

Recipe-lock audit: 36 model-lock rows loaded successfully; 36 effective pinned-lock keys. See `vc7-lock-loader-audit.txt`.

Only `audio/hunyuan_video_foley` public input metadata and the two aliases of the requested `video/ltx2_3_i2v` checkpoint were repaired. Other gaps are reported for the manager; no further network lookup or fix was made.

The LTX i2v checkpoint aliases now have the observed digest, size, and pinned revision. Its separate LoRA and text-encoder records remain incomplete, so this refresh does not establish full managed readiness for that template.

| Template id | Model name | Subdir | Missing declared fields | Missing at Agent guard |
|---|---|---|---|---|
| `edit/flux2_klein_4b_image_edit_base` | `flux-2-klein-base-4b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_4b_image_edit_base` | `qwen_3_4b.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_4b_image_edit_base` | `full_encoder_small_decoder.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_4b_image_edit_distilled` | `flux-2-klein-4b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_4b_image_edit_distilled` | `qwen_3_4b.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_4b_image_edit_distilled` | `flux2-vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_base` | `flux-2-klein-base-9b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_base` | `qwen_3_8b_fp8mixed.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_base` | `full_encoder_small_decoder.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_distilled` | `flux-2-klein-9b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_distilled` | `qwen_3_8b_fp8mixed.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `edit/flux2_klein_9b_image_edit_distilled` | `full_encoder_small_decoder.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_4b_t2i` | `flux-2-klein-base-4b.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_4b_t2i` | `qwen_3_4b.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_4b_t2i` | `flux2-vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_4b_t2i` | `flux-2-klein-4b.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_gguf_t2i` | `flux-2-klein-base-9b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_gguf_t2i` | `qwen_3_8b_fp8mixed.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_gguf_t2i` | `full_encoder_small_decoder.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_t2i` | `flux-2-klein-base-9b-fp8.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_t2i` | `qwen_3_8b_fp8mixed.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `image/flux2_klein_9b_t2i` | `full_encoder_small_decoder.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `image/qwen_image_2512` | `Qwen-Image-2512-Lightning-4steps-V1.0-fp32.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `image/qwen_image_2512` | `qwen_2.5_vl_7b_fp8_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `image/qwen_image_2512` | `qwen_image_2512_fp8_e4m3fn.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `image/qwen_image_2512` | `qwen_image_vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_i2v` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_i2v` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_hdr` | `ltx-2.3-22b-dev.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_hdr` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_hdr` | `ltxv/ltx2/ltx-2.3-22b-ic-lora-hdr-0.9.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_hdr` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_motion_track` | `ltx-2.3-22b-dev.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_motion_track` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_motion_track` | `ltxv/ltx2/ltx-2.3-22b-ic-lora-motion-track-control-ref0.5.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_motion_track` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_union_control` | `ltx-2.3-22b-dev.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_union_control` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_union_control` | `ltxv/ltx2/ltx-2.3-22b-ic-lora-union-control-ref0.5.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_iclora_union_control` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_two_stage` | `ltx-2.3-22b-dev.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_two_stage` | `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` | `latent_upscale_models` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_two_stage` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_lightricks_two_stage` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `gemma_3_12B_it_fp8_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `ltx-2.3_text_projection_bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `LTX23_video_vae_bf16_KJ.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `LTX23_audio_vae_bf16_KJ.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `vae_approx/taeltx2_3.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `LTXVideo/v2/ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `LTX/v2/ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_frame` | `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` | `latent_upscale_models` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `ltx-2.3_text_projection_bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `LTX23_video_vae_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `LTX23_audio_vae_bf16.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `taeltx2_3.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `ltx-2.3-22b-distilled-1.1_transformer_only_fp8_scaled.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `LTX/v2/ltx-2.3-22b-distilled-1.1_lora-dynamic_fro09_avg_rank_111_bf16.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `gemma_3_12B_it_fp4_mixed.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_runexx_first_last_raw_video_guide` | `ltx-2.3-spatial-upscaler-x2-1.1.safetensors` | `latent_upscale_models` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_t2v` | `ltx-2.3-22b-dev.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_t2v` | `ltxv/ltx2/ltx-2.3-22b-distilled-lora-384-1.1.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_t2v` | `ltx-2.3-22b-dev-fp8.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/ltx2_3_t2v` | `comfy_gemma_3_12B_it.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `clip_vision_h.safetensors` | `clip_vision` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `sam2_hiera_base_plus.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `wan_2.1_vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `yolox_l.onnx` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_animate_native_first_stage` | `dw-ll_ucoco_384_bs5.torchscript.pt` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wan22_i2v_comfy_lightx2v` | `wan_2.1_vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_i2v` | `clip_vision_h.safetensors` | `clip_vision` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_i2v` | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_i2v` | `wan2.1_i2v_480p_14B_fp16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_i2v` | `wan_2.1_vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_t2v` | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_t2v` | `wan2.1_t2v_1.3B_fp16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wan_t2v` | `wan_2.1_vae.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_control_lora` | `WanVideo/wan2.1_t2v_1.3B_fp16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_control_lora` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_control_lora` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_control_lora` | `WanVid/wan2.1-1.3b-control-lora-tile-v0.1_comfy.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_vace` | `WanVideo/wan2.1_t2v_1.3B_fp16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_vace` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_13b_vace` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_v2v_infinitetalk` | `WanVideo/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_v2v_infinitetalk` | `clip_vision_h.safetensors` | `clip_vision` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_v2v_infinitetalk` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_v2v_infinitetalk` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_wanmove_i2v` | `WanVideo/WanMove/Wan21-WanMove_fp8_scaled_e4m3fn_KJ.safetensors` | `diffusion_models` | size_bytes | size_bytes |
| `video/wanvideo_wrapper_21_14b_wanmove_i2v` | `WanVideo/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` | `loras` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_wanmove_i2v` | `clip_vision_h.safetensors` | `clip_vision` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_wanmove_i2v` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_21_14b_wanmove_i2v` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models/WanVideo/2_2` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models/WanVideo/2_2` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `Wan2_1_VAE_bf16.safetensors` | `vae/wanvideo` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `umt5_xxl_fp16.safetensors` | `checkpoints` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_14b_i2v_kijai` | `lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` | `loras/WanVideo/Lightx2v` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_i2v_controlnet` | `Wan2_2-TI2V-5B-FastWanFullAttn_bf16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_i2v_controlnet` | `Wan2_2_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_i2v_controlnet` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_ovi_audio_i2v` | `WanVideo/Ovi/Wan_2_1_Ovi_video_model_bf16.safetensors` | `diffusion_models` | size_bytes | size_bytes |
| `video/wanvideo_wrapper_22_5b_ovi_audio_i2v` | `Wan2_2_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_ovi_audio_i2v` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_t2v_controlnet` | `Wan2_2-TI2V-5B-FastWanFullAttn_bf16.safetensors` | `diffusion_models` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_t2v_controlnet` | `Wan2_2_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_5b_t2v_controlnet` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_s2v_context_window` | `WanVideo/S2V/Wan2_2-S2V-14B_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models` | size_bytes | size_bytes |
| `video/wanvideo_wrapper_22_s2v_context_window` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_s2v_context_window` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_s2v_framepack_pose` | `WanVideo/S2V/Wan2_2-S2V-14B_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models` | size_bytes | size_bytes |
| `video/wanvideo_wrapper_22_s2v_framepack_pose` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_s2v_framepack_pose` | `wanvideo/Wan2_1_VAE_bf16.safetensors` | `vae` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `Wan2_2-Animate-14B_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models/WanVideo/2_2` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `WanAnimate_relight_lora_fp16.safetensors` | `loras/WanVideo` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `clip_vision_h.safetensors` | `clip_vision` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `sam2_hiera_base_plus.safetensors` | `sams` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `yolov10m.onnx` | `detection` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `vitpose-l-wholebody.onnx` | `detection` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `yolox_l.torchscript.pt` | `onnx/yolo` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `dw-ll_ucoco_384_bs5.torchscript.pt` | `onnx/dwpose` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `Wan2_1_VAE_bf16.safetensors` | `vae/wanvideo` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `umt5-xxl-enc-bf16.safetensors` | `text_encoders` | sha256, size_bytes | sha256, size_bytes |
| `video/wanvideo_wrapper_22_wan_animate_preprocess_kijai` | `lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors` | `loras/WanVideo/Lightx2v` | sha256, size_bytes | sha256, size_bytes |

## Templates with complete declared integrity fields

`audio/ace_step_1_5_t2a_song`, `audio/hunyuan_foley_v2a`, `audio/hunyuan_video_foley`, `audio/minimax_music_3`, `audio/qwen3_tts_custom_voice`, `audio/qwen3_tts_voice_clone`, `audio/qwen3_tts_voice_design`, `edit/qwen_image_2_1_turbo_edit`, `edit/qwen_image_edit`, `image/basic_image_upscale`, `image/qwen_image_2_1_turbo`, `image/z_image`, `image/z_image_img2img`, `image/z_image_turbo`, `smoke/empty_image_red`, `video/basic_video_enhance`, `video/ltx2_3_first_last_frame_travel_iclora_control`, `video/ltx2_3_lightricks_first_last_parity`, `video/ltx2_3_lightricks_first_last_two_stage_lowvram`, `video/wanvideo_wrapper_22_14b_t2i`, `video/wanvideo_wrapper_22_14b_vace_cocktail`

Raw data and reproducible offline script: `vc7-survey-after.json`, `vc7-survey.py`. The baseline survey is `vc7-survey-before.json`; the change removes exactly two incomplete checkpoint alias records (134 -> 132).
