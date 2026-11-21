"""CPU diagnostic: pinned VHS loader and Comfy mask nodes with import-only shims."""
import importlib.util
import sys
import types
import torch


def module(name):
    obj = types.ModuleType(name)
    sys.modules[name] = obj
    return obj


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj


folder = module('folder_paths')
folder.get_annotated_filepath = lambda path: path
folder.get_temp_directory = lambda: '/tmp'
server = module('server')
server.PromptServer = types.SimpleNamespace(instance=types.SimpleNamespace(prompt_queue=None))
nodes = module('nodes')
nodes.MAX_RESOLUTION = 16384
comfy = module('comfy')
comfy.__path__ = []
comfy.utils = module('comfy.utils')
class ProgressBar:
    def __init__(self, *args): pass
    def update(self, *args): pass
comfy.utils.ProgressBar = ProgressBar
comfy.utils.common_upscale = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError('unexpected upscale'))
comfy.model_management = module('comfy.model_management')
kdiff = module('comfy.k_diffusion')
kdiff.__path__ = []
module('comfy.k_diffusion.utils').FolderOfImages = object
module('node_helpers')
scipy = module('scipy')
scipy.__path__ = []
scipy.ndimage = module('scipy.ndimage')
api = module('comfy_api')
api.__path__ = []
latest = module('comfy_api.latest')
class IO:
    ComfyNode = object
    NodeOutput = staticmethod(lambda *args: args)
latest.IO = IO
latest.UI = object
latest.ComfyExtension = object
pkg = module('vhs_diagnostic')
pkg.__path__ = ['/tmp/plan64-vhs-src/videohelpersuite']
load('vhs_diagnostic.logger', '/tmp/plan64-vhs-src/videohelpersuite/logger.py')
load('vhs_diagnostic.utils', '/tmp/plan64-vhs-src/videohelpersuite/utils.py')
vhs = load('vhs_diagnostic.load_video_nodes', '/tmp/plan64-vhs-src/videohelpersuite/load_video_nodes.py')
mask_nodes = load('pinned_nodes_mask', '/tmp/plan64-comfy-src/comfy_extras/nodes_mask.py')

import json
import zipfile
from pathlib import Path
manifest = json.loads(Path(sys.argv[1]).read_text())
binding = next(row for row in manifest['managed_assets']['manifest']['assets'] if row['binding'] == 'audio_time_mask')
member = binding['member']
assert Path(member).name == manifest['workflow_inputs']['audio_time_mask']
values = manifest['capabilities']['audio_time_mask']
artifact = '/tmp/plan64-sr5-managed-mask.mkv'
with zipfile.ZipFile(manifest['managed_assets']['path']) as archive:
    Path(artifact).write_bytes(archive.read(member))
import hashlib
assert hashlib.sha256(Path(artifact).read_bytes()).hexdigest() == binding['sha256']
expected = torch.tensor(values['decoded_frame_values'], dtype=torch.float32)
images, _, _, info = vhs.LoadVideoFFmpegUpload().load_video(
    video=artifact, force_rate=24, custom_width=0, custom_height=0,
    frame_load_cap=len(expected), start_time=0, format='AnimateDiff')
mask, = mask_nodes.ImageToMask.execute(images, 'red')
crop, = mask_nodes.CropMask.execute(mask, x=0, y=0, width=1, height=1)
assert crop.shape == (len(expected), 1, 1), crop.shape
assert torch.equal(crop.flatten(), expected)
assert max(abs(a-b) for a, b in zip(values['requested_frame_values'], crop.flatten().tolist())) <= 0.5 / 65535 + 1e-7
import hashlib
print('managed member', member, 'sha256', hashlib.sha256(Path(artifact).read_bytes()).hexdigest(), 'loaded frames', info['loaded_frame_count'], 'mask shape', tuple(crop.shape))
print('nonzero frames', [(i, x) for i, x in enumerate(crop.flatten().tolist()) if x])
# Execute the pinned motion node with real torch and real Comfy NestedTensor;
# only its environment compatibility check is stubbed (no inference here).
comfy.nested_tensor = load('comfy.nested_tensor', '/tmp/plan64-comfy-src/comfy/nested_tensor.py')
motion_pkg = module('h3_diagnostic')
motion_pkg.__path__ = []
audio_grid = module('h3_diagnostic.h3_audio_grid')
audio_grid.audio_grid_geometry = lambda *args, **kwargs: None
audio_grid.encode_exact_audio_grid = lambda *args, **kwargs: None
compat = module('h3_diagnostic.h3_compat')
compat.ensure_existing_video_compat = lambda: None
timing = module('h3_diagnostic.h3_timing')
for name in ('largest_h3_video_run', 'smallest_h3_video_run', 'is_exact_av_boundary', 'sample_boundary_from_frames'):
    setattr(timing, name, lambda *args, **kwargs: None)
motion = load('h3_diagnostic.existing_video_extension', '/tmp/plan64-h3-existing-video-extension.py')
video = torch.zeros((1, 24, 2, 1, 1))
ticks = round(len(expected) * 40 / 24)
audio = torch.zeros((1, 32, 2, ticks))
video_mask = torch.tensor([[[[[0.25]], [[0.75]]]]])
latent = {'samples': comfy.nested_tensor.NestedTensor((video, audio)),
          'noise_mask': comfy.nested_tensor.NestedTensor((video_mask, torch.zeros((1, 1, 2, ticks))))}
updated, = motion.MiniMaxH3SetAVNoiseMask().set_mask(latent, audio_mask=crop)
actual_video, actual_audio = updated['noise_mask'].unbind()
expected_audio = torch.nn.functional.interpolate(expected.reshape(1, 1, -1), size=ticks, mode='linear', align_corners=False)
assert torch.equal(actual_video, video_mask)
assert actual_audio.shape == (1, 1, 2, ticks)
assert torch.equal(actual_audio[0, 0, 0], expected_audio.flatten())
assert torch.equal(actual_audio[0, 0, 1], expected_audio.flatten())
print('H3 preserved video mask', actual_video.flatten().tolist())
print('H3 audio mask shape', tuple(actual_audio.shape), 'nonzero ticks', [(i, x) for i, x in enumerate(actual_audio[0, 0, 0].tolist()) if x][:12])
assert max(abs(a-b) for a, b in zip(values['resampled_40hz'], actual_audio[0, 0, 0].tolist())) < 1e-6
