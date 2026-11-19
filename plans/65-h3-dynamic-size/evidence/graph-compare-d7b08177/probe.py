from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

source_root = Path(sys.argv[1]).resolve()
out_root = Path(sys.argv[2]).resolve()
out_root.mkdir(parents=True, exist_ok=True)

from astrid.packs.h3_av.shared.compile import compile_preparation, _compile_native_v2
from astrid.packs.h3_av.shared.generation import build_generation_workflow, generation_inputs_from_bindings
from astrid.packs.h3_av.shared.prepare import prepare_request
from astrid.packs.h3_av.shared.request import normalize_request
from astrid.packs.h3_av.shared import engine_facts as h3_engine_facts
from astrid.core.generation.engine_facts import comfyui_facts
from vibecomfy.cli_loader import load_workflow_any

h3_engine_facts.install(comfyui_facts())


def ffmpeg(*args: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True, capture_output=True)


def request_assets(raw: dict, paths: dict[str, Path]) -> dict:
    req = normalize_request(raw)
    prepared = prepare_request(req, asset_map={key: str(value) for key, value in paths.items()})
    return req, prepared


def graph_from_compile(compiled: dict) -> dict:
    wf = load_workflow_any(compiled["workflow"]["workflow.py"]["path"])
    return wf.compile("api", run_inputs=compiled["workflow_inputs"])


def save(name: str, graph: dict) -> dict:
    data = json.dumps(graph, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    path = out_root / f"{name}.json"
    path.write_bytes(json.dumps(graph, sort_keys=True, indent=2, ensure_ascii=False).encode() + b"\n")
    return {"case": name, "path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "nodes": len(graph)}


fixtures = out_root / "fixtures"
fixtures.mkdir(exist_ok=True)
image = fixtures / "reference.png"
Image.new("RGB", (32, 32), (21, 42, 63)).save(image)
mask = fixtures / "mask.png"
Image.new("L", (1024, 576), 255).save(mask)
video = fixtures / "source.mp4"
ffmpeg("-f", "lavfi", "-i", "color=c=blue:s=1024x576:r=24:d=1", "-f", "lavfi", "-i",
       "sine=frequency=440:sample_rate=48000:duration=1", "-map", "0:v:0", "-map", "1:a:0",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(video))
performance = fixtures / "performance.mp4"
ffmpeg("-f", "lavfi", "-i", "color=c=green:s=64x64:r=24:d=4", "-an", "-c:v", "libx264",
       "-pix_fmt", "yuv420p", str(performance))
replacement = fixtures / "replacement.png"
Image.new("RGB", (64, 64), (210, 22, 19)).save(replacement)

results = []

# Source-free, image-guided native-v2.
raw = {"version": 2, "prompt": "A quiet scene with <Picture 1>.", "duration": 1,
       "media": [{"id": "ref", "asset": "reference.png", "role": "reference", "modality": "image"}]}
req, prep = request_assets(raw, {"reference.png": image})
compiled = compile_preparation(prep, out_dir=out_root / "compile-source-free")
results.append(save("source-free-image-guided", graph_from_compile(compiled)))

# Static-mask native edit; use a stable source and authored still mask.
raw = {"version": 2, "duration": 1, "prompt": "Edit the white region.", "media": [
    {"id": "source", "asset": "source.mp4", "role": "timeline", "modality": "video",
     "at": {"frame": 0}, "range": [0, 1],
     "edit": [{"stream": "video", "during": [0, 1], "mask": {"asset": "mask.png"}}]}]}
req, prep = request_assets(raw, {"source.mp4": video, "mask.png": mask})
compiled = compile_preparation(prep, out_dir=out_root / "compile-masked-static")
results.append(save("masked-static", graph_from_compile(compiled)))

# Character Swap native-v2. Paths and content are identical across source exports.
raw = {"version": 2, "prompt": "Replace <Video 1> with <Picture 1>.", "duration": 1,
       "media": [{"id": "performance", "asset": "performance.mp4", "role": "reference", "modality": "video", "range": [0, 1], "audio": False},
                 {"id": "replacement", "asset": "replacement.png", "role": "reference", "modality": "image"}],
       "settings": {"turbo": {"enabled": True}, "adapter": {"id": "character_swap_v1"}}}
req = normalize_request(raw)
compiled = _compile_native_v2(req, {"performance.mp4": performance, "replacement.png": replacement}, out_root / "compile-character-swap")
results.append(save("character-swap", graph_from_compile(compiled)))

# Direct generation builder exercises the generated video-mask tail EmptyImage.
inputs = generation_inputs_from_bindings(
    references=[], prompt="A quiet scene.", frames=25,
    model="minimax_h3_ref2va_pruned_int8_convrot.safetensors", steps=8, seed=7,
    masked_edit={"source_binding": "source_video", "mask_binding": "video_mask_0", "mask_channel": "red",
                 "mask_kind": "video", "frame_load_cap": 24, "start_time": 0, "strength": 1},
)
workflow = build_generation_workflow(inputs)
workflow_path = out_root / "masked-video-tail.py"
from vibecomfy.workflow_bundle import emit_bundle
from vibecomfy.security.provenance import Provenance
emit_bundle(workflow, workflow_path, provenance=Provenance.AGENT_AUTHORED)
graph = load_workflow_any(workflow_path).compile(
    "api", run_inputs={"source_video": "stable-source.mp4", "video_mask_0": "stable-mask.mp4"})
results.append(save("masked-video-tail", graph))

summary = {"source_root": str(source_root), "cases": results}
(out_root / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(summary, sort_keys=True))
