# vibecomfy: generated
# For hand-editing, run: python -m vibecomfy.cli copy-to-recipe <id>
# vibecomfy: surface=canonical
"""Auto-generated ready_template — use python -m vibecomfy.cli copy-to-recipe <id> for hand-editing."""
from __future__ import annotations

from vibecomfy.templates import InputSpec, ModelAsset, OutputSpec, ReadyMetadata, new_workflow, node as raw_call, ref
from vibecomfy.workflow import VibeWorkflow
from vibecomfy.nodes.core import AudioConcat, BasicGuider, BasicScheduler, CLIPLoader, EmptyAudio, ImageBatch, ImageFromBatch, KSamplerSelect, LoadImageMask, LoraLoaderModelOnly, RandomNoise, RepeatImageBatch, SamplerCustomAdvanced, UNETLoader, VAEDecode, VAEDecodeAudio, VAELoader
from vibecomfy.nodes.videohelpersuite import VHS_LoadVideoFFmpeg, VHS_VideoCombine


AUDIO_VAE_NAME = 'minimax_h3_audio_vae_fp32.safetensors'
CLIP_NAME = 'qwen3vl_32b_minimax_h3_int8_convrot.safetensors'
DEFAULT_FRAMES = 1
DEFAULT_FRAMES_2 = 39
DEFAULT_SEED = 123456789
GUIDE_STRENGTH = 0.95
LORA_NAME = 'minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors'
UNET_NAME = 'minimax_h3_ref2va_pruned_int8_convrot.safetensors'
VIDEO_VAE_NAME = 'minimax_h3_video_vae_int8_convrot.safetensors'
DEFAULT_STEPS = 8
DEFAULT_SOURCE_VIDEO = ''
DEFAULT_MASK_0 = ''
DEFAULT_PROMPT = 'Edit the white region.'
DEFAULT_SAMPLER = 'res_multistep'
DEFAULT_SCHEDULER = 'simple'


MODELS = {
    'diffusion_model': ModelAsset(url='https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/e5eb578a89295337b8ff433a035929ce0279e0b6/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors', sha256='9255f52b6677845ad238f20dfaafa94727053694127ab7f255c048f0f9365779', size_bytes=20970379616, subdir='diffusion_models'),
    'text_encoder': ModelAsset(url='https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/e5eb578a89295337b8ff433a035929ce0279e0b6/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors', sha256='bc2ced0fbea64757fa9acddccfc0b3f4819d1dcf1da6c124d690d368be283923', size_bytes=27141342152, subdir='text_encoders'),
    'vae': ModelAsset(url='https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/e5eb578a89295337b8ff433a035929ce0279e0b6/vae/minimax_h3_video_vae_int8_convrot.safetensors', sha256='52a2c8c73583c86e4f41cdcce3a6ad0ea562987bc0bf3d60a0cef5f5c8e60c0e', size_bytes=2811065184, subdir='vae'),
    'vae_2': ModelAsset(url='https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/e5eb578a89295337b8ff433a035929ce0279e0b6/vae/minimax_h3_audio_vae_fp32.safetensors', sha256='8e505d95dd1561d47abd43d4238fd40d9bb1ae9e147ed0a4cba778d76ae4db48', size_bytes=605254808, subdir='vae'),
    'lora': ModelAsset(url='https://huggingface.co/Comfy-Org/MiniMax-H3/resolve/e5eb578a89295337b8ff433a035929ce0279e0b6/loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors', sha256='2339acdf19bfe123f46b971ea35d367a84adb85de43627e1eceafa5a5b2b111e', size_bytes=1956193000, subdir='loras'),
}


PUBLIC_INPUT_METADATA = {
    'model': InputSpec(node=ref('unetloader'), field='unet_name', default=UNET_NAME, type='CHOICE', infer_type=False),
    'steps': InputSpec(node=ref('basicscheduler'), field='steps', default=DEFAULT_STEPS, type='INT', infer_type=False),
    'seed': InputSpec(node=ref('randomnoise'), field='noise_seed', default=DEFAULT_SEED, type='INT', infer_type=False),
    'source_video': InputSpec(node=ref('vhs_loadvideoffmpeg'), field='video', default=DEFAULT_SOURCE_VIDEO, type='CHOICE', required=True, media_semantics='video', infer_type=False),
    'mask_0': InputSpec(node=ref('loadimagemask'), field='image', default=DEFAULT_MASK_0, type='CHOICE', required=True, media_semantics='image', infer_type=False),
    'prompt': InputSpec(node=ref('minimaxh3referencetovideo'), field='prompt', default=DEFAULT_PROMPT, type='STRING', infer_type=False),
    'sampler': InputSpec(node=ref('ksamplerselect'), field='sampler_name', default=DEFAULT_SAMPLER, type='COMBO', infer_type=False),
    'scheduler': InputSpec(node=ref('basicscheduler'), field='scheduler', default=DEFAULT_SCHEDULER, type='COMBO', infer_type=False),
    'guidance': InputSpec(node=ref('loraloadermodelonly'), field='strength_model', default=GUIDE_STRENGTH, type='FLOAT', infer_type=False),
}


READY_METADATA = ReadyMetadata.build(
    capability='video',
    template_id='h3_av_reference_generation',
    inputs=PUBLIC_INPUT_METADATA,
    models=MODELS,
    requirements={'runtime': {'comfy_commit': '6bfaacc67c2103481e5f0c84d75257cd0581d86a', 'comfy_version': '==0.36.0', 'packages': {'comfy-aimdo': '==0.5.5', 'comfy-kitchen': '==0.2.35', 'torch': '==2.10.0+cu130'}, 'launch_flags': ['--use-ck-attention', '--disable-comfy-compiler']}, 'custom_node_refs': [{'slug': 'ComfyUI-H3-Motion-Context-MultiRef', 'source': 'git', 'commit': '361624fb406b63eb6694442eac6c895fc1533a70', 'url': 'https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef.git', 'classes': ['H3V2VGranularFractionalDenoise', 'MiniMaxH3AudioVAECompatibility']}, {'slug': 'ComfyUI-VideoHelperSuite', 'source': 'git', 'commit': '4ee72c065db22c9d96c2427954dc69e7b908444b', 'url': 'https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git', 'classes': ['VHS_LoadVideoFFmpeg', 'VHS_VideoCombine']}]},
    custom_node_packs={'ComfyUI-H3-Motion-Context-MultiRef': {'commit': '361624fb406b63eb6694442eac6c895fc1533a70', 'url': 'https://github.com/seitanism/ComfyUI-H3-Motion-Context-MultiRef.git', 'classes_used': ['H3V2VGranularFractionalDenoise', 'MiniMaxH3AudioVAECompatibility', 'MiniMaxH3ReferenceToVideo', 'MiniMaxH3SigmaShift'], 'pip_packages': ['safetensors'], 'status': 'discovered'}, 'ComfyUI-VideoHelperSuite': {'commit': '4ee72c065db22c9d96c2427954dc69e7b908444b', 'url': 'https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git', 'class_schema_sha256': '8391e679554eecd5d324a3e34a713ff240e619e3a07476587845ba18c9fae310', 'classes_used': ['VHS_LoadVideoFFmpeg', 'VHS_VideoCombine'], 'pip_packages': [], 'status': 'discovered'}},
    provenance={'operation': 'authored'},
    source_bundle={'format_version': 2, 'generation_id': '3139c6986e55e8afff35962c7a334423cf7f6116572f45678f40a5ee6ddcb473', 'custody_digest': 'b84b193ff85227408fdedca85a2f8a1912a38843e1d5aa65f2b3b7d2ada179ea'},
)

def build() -> VibeWorkflow:
    """Build the workflow (auto-generated)."""
    with new_workflow(READY_METADATA, source_path=__file__) as wf:

        # Loaders
        cliploader = CLIPLoader(clip_name=CLIP_NAME, type='minimax', device='default')
        vaeloader = VAELoader(vae_name=VIDEO_VAE_NAME)
        vaeloader_2 = VAELoader(vae_name=AUDIO_VAE_NAME)
        emptyaudio = EmptyAudio(duration=0.625, sample_rate=44100, channels=2)

        vhs_loadvideoffmpeg = VHS_LoadVideoFFmpeg(
            custom_height=0,
            custom_width=0,
            force_rate=24,
            format='AnimateDiff',
            frame_load_cap=24,
            start_time=0.0,
            video=DEFAULT_SOURCE_VIDEO,
            videopreview={'hidden': False, 'paused': False, 'params': {}, 'muted': False},
        )

        loadimagemask = LoadImageMask(channel='red', image=DEFAULT_MASK_0)
        unetloader = UNETLoader(unet_name=UNET_NAME, weight_dtype='default')
        randomnoise = RandomNoise(noise_seed=DEFAULT_SEED)

        # Sampling
        ksamplerselect = KSamplerSelect(sampler_name=DEFAULT_SAMPLER)

        minimaxh3audiovaecompatibility = raw_call('MiniMaxH3AudioVAECompatibility',
            _outputs=('audio_vae',),
            audio_vae=vaeloader_2.out('VAE'),
        )

        modelattentionbackend = raw_call('ModelAttentionBackend',
            _outputs=('MODEL',),
            attention='comfy kitchen attention',
            model=unetloader.out('MODEL'),
        )

        imagefrombatch = ImageFromBatch(
            batch_index=23,
            length=DEFAULT_FRAMES,
            image=vhs_loadvideoffmpeg.out('IMAGE'),
        )

        audioconcat = AudioConcat(
            direction='after',
            audio1=vhs_loadvideoffmpeg.out('AUDIO'),
            audio2=emptyaudio.out('AUDIO'),
        )

        repeatimagebatch = RepeatImageBatch(
            amount=15,
            image=imagefrombatch.out('IMAGE'),
        )

        minimaxh3referencetovideo = raw_call('MiniMaxH3ReferenceToVideo',
            _outputs=('positive', 'LATENT'),
            height=576,
            length=DEFAULT_FRAMES_2,
            prompt=DEFAULT_PROMPT,
            ref_image_size='match',
            width=1024,
            audio_vae=minimaxh3audiovaecompatibility.out('audio_vae'),
            clip=cliploader.out('CLIP'),
            vae=vaeloader.out('VAE'),
        )

        loraloadermodelonly = LoraLoaderModelOnly(
            lora_name=LORA_NAME,
            strength_model=GUIDE_STRENGTH,
            model=modelattentionbackend.out('MODEL'),
        )

        minimaxh3sigmashift = raw_call('MiniMaxH3SigmaShift',
            _outputs=('MODEL',),
            shift_audio=3.0,
            shift_video=12.0,
            model=loraloadermodelonly.out('MODEL'),
        )

        imagebatch = ImageBatch(
            image1=vhs_loadvideoffmpeg.out('IMAGE'),
            image2=repeatimagebatch.out('IMAGE'),
        )

        h3v2vgranularfractionaldenoise = raw_call('H3V2VGranularFractionalDenoise',
            _outputs=('latent', 'model', 'diagnostics'),
            audio_strength=0,
            crop='disabled',
            global_strength=0.9995,
            inside_strength=1.0,
            invert_mask=False,
            mask_temporal_reduce='max',
            mode='spatial',
            outside_strength=0,
            source_fit='start',
            source_fps=24.0,
            audio_vae=minimaxh3audiovaecompatibility.out('audio_vae'),
            latent=minimaxh3referencetovideo.out('LATENT'),
            model=minimaxh3sigmashift.out('MODEL'),
            source_audio=audioconcat.out('AUDIO'),
            source_frames=imagebatch.out('IMAGE'),
            source_mask=loadimagemask.out('MASK'),
            vae=vaeloader.out('VAE'),
        )

        basicguider = BasicGuider(
            conditioning=minimaxh3referencetovideo.out('positive'),
            model=h3v2vgranularfractionaldenoise.out('model'),
        )

        basicscheduler = BasicScheduler(
            scheduler=DEFAULT_SCHEDULER,
            steps=DEFAULT_STEPS,
            denoise=1.0,
            model=h3v2vgranularfractionaldenoise.out('model'),
        )

        samplercustomadvanced = SamplerCustomAdvanced(
            guider=basicguider.out('GUIDER'),
            latent_image=h3v2vgranularfractionaldenoise.out('latent'),
            noise=randomnoise.out('NOISE'),
            sampler=ksamplerselect.out('SAMPLER'),
            sigmas=basicscheduler.out('SIGMAS'),
        )

        # Decode
        vaedecode = VAEDecode(
            samples=samplercustomadvanced.out('OUTPUT'),
            vae=vaeloader.out('VAE'),
        )

        vaedecodeaudio = VAEDecodeAudio(
            samples=samplercustomadvanced.out('OUTPUT'),
            vae=minimaxh3audiovaecompatibility.out('audio_vae'),
        )

        # Outputs
        vhs_videocombine = VHS_VideoCombine(
            frame_rate=24,
            loop_count=0,
            filename_prefix='h3_av/generated',
            format='video/h264-mp4',
            pingpong=False,
            save_output=True,
            crf=19,
            pix_fmt='yuv420p',
            save_metadata=False,
            trim_to_audio=False,
            audio=vaedecodeaudio.out('AUDIO'),
            images=vaedecode.out('IMAGE'),
        )

        return wf.finalize(PUBLIC_INPUT_METADATA, outputs=[OutputSpec(node=vhs_videocombine, output_type='VHS_VideoCombine', name='video', artifact_kind='video', mime_type='video/mp4', filename_prefix='h3_av/generated', expected_cardinality='one')])
