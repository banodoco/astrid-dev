import copy
from pathlib import Path
from tests.packs.h3_av.test_native_masked_edit import WATERMARK, _prepare
from astrid.packs.h3_av.shared.compile import compile_preparation
from astrid.packs.h3_av.shared.request import normalize_request

from astrid.core.generation.engine_facts import comfyui_facts
from astrid.packs.h3_av.shared import engine_facts
engine_facts.install(comfyui_facts())

root = Path('/tmp/plan64-sr5-managed-repro')
root.mkdir(exist_ok=True)
raw = copy.deepcopy(WATERMARK)
prepared = _prepare(raw, root)
raw['media'][0]['edit'].append({'stream': 'audio', 'during': ['2001/48000', '3999/48000'], 'strength': 0.5})
request = normalize_request(raw)
prepared['request'], prepared['request_digest'] = request.value, request.digest
manifest = compile_preparation(prepared, out_dir=root / 'compiled')
print(manifest['manifest_path'])
print(manifest['workflow_inputs']['audio_time_mask'])
