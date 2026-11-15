# LS-1 partial CPU floor, 15 November 2026

This is **not LS-1 completion** and is not a Runtime redesign decision. The separate transport and Runtime experiments are followed by an integrated stand-in→Runtime experiment below. Real ComfyUI has not been measured. Release 13 Runtime source was `6855dfa8df65cf8ae4c002b57134d6505493c17c`; no Agent integration was exercised. Host: Linux x86-64, kernel 6.18.57; Runtime Python 3.13.5; transport/process Python 3.12.14. Temporary realms used the host's default temporary filesystem. Other host activity was not controlled; there was brief test activity during the Runtime measurements. No flush counts were measured. Times are observations, not predictions or tail guarantees.

| Runtime HTTP, 20 jobs | lifecycle median / slowest, ms | settle median / slowest, ms |
| --- | ---: | ---: |
| 1 MiB PNG, one caller | 21.73 / 33.22 | 16.82 / 28.67 |
| 1 MiB PNG, two callers | 35.81 / 49.80 | 22.42 / 36.22 |
| 10 MiB MP4, one caller | 166.66 / 289.03 | 153.43 / 266.97 |
| 10 MiB MP4, two callers | 319.21 / 517.69 | 221.11 / 450.08 |

Each Runtime sample uses actual HTTP create→claim→settle and scoped worker credentials; settlement stores inline bytes through the unmodified CAS and verifies exact bytes, a succeeded task, and a managed output association afterward. Verification reads are outside the lifecycle timings. Callers use separate HTTP client objects and share one worker actor/executor credential. At two callers a worker can claim the other caller's queued task; all claimed tasks are settled, but this does not measure individual caller-to-owned-task latency. urllib's HTTP connections are not held between calls; this is the current Runtime HTTP path, not the proposed resident transport. Descriptor preparation is timed separately, but payload creation and initial hash are before the lifecycle timer. PNG is a tiny valid image with an ancillary padding chunk; MP4 is a short valid video padded with a free box. They exercise byte volume, not representative codec or video complexity. Large video here is 10 MiB, not a 100 MB workload. Raw 20 records and all component medians/maxima are in the adjacent JSON files.

The scripts assert those post-settlement checks during each run. The saved measurements retain sample indices and digests, but not returned task, attempt or managed-association snapshots; they are timing records, not an independently replayable transaction audit. Durability is requested explicitly and exercised through the unchanged Runtime's settlement path; these probes do not separately inspect the association's durability field or count filesystem flushes.

Stand-in is an artificial aiohttp fixture with a deliberate 1 ms delayed event; it does not implement Comfy validation or execution. `standin-linux.json` contains raw observations. Its timings are transport fixture checks only. HTTP and websocket are established before POST, history is read once after `executing(node=null)`, outputs are fetched and hashed once. Event timestamps are client-observed: `post_response_to_start_observed_ms` may be negative because execution can start before the POST response; it is not an exact queue duration. Server-side enqueue timestamps are needed to isolate true validation and queue wait; no queue is subtracted. Websocket success and history-ready observation are distinct. Failures and interruptions fail the sample; the script does not retry or reconcile a disconnect. A graph must emit at least one output in history. For multiple output descriptors, each is fetched and hashed once.

Process no-op median / slowest: Python 10.12 / 14.90 ms; native 0.67 / 1.22 ms. These include spawn and wait and are not the full CLI. Raw records are in `process-linux.json`.

## Reproduction and outstanding cells

Run from the exact Runtime checkout, with its dependencies installed. The script creates and removes its own isolated realm; it never touches a user realm. Example Linux invocation:

```sh
cd /path/to/astrid-runtime
PYTHONPATH=.:tests /path/to/venv/bin/python /path/to/astrid-dev/releases/14/evidence/ls1/runtime_floor.py --samples 20 --bytes 1048576 --callers 1 --output runtime-1m.json
```

For a 10 MiB video supply a small valid base MP4 (e.g. generated separately with ffmpeg) using `--bytes 10485760 --video-base /path/to/base.mp4`; use `--callers 2` for the second concurrency cell. Windows: in PowerShell set `$env:PYTHONPATH = '.;tests'` and invoke the venv's `Scripts/python.exe` with the same options. Runtime measurements require its actual dependencies and HTTP daemon; `aiohttp` is needed for the transport script.

With an isolated real ComfyUI already running and its dependencies installed, use `python comfy_floor.py --url http://127.0.0.1:8188 --graph trivial-graph.json --samples 20 --output real-trivial.json`. For a warm-model run supply a compatible prepared API-format graph with `__LS1_PREFIX__` on its output prefix and optionally `__LS1_SEED__` on an integer seed: `python comfy_floor.py --url http://127.0.0.1:8188 --graph /path/to/prepared-warm-api-graph.json --samples 20 --output real-warm.json`. Confirm the model is warm first and document model, graph, hardware, OS and output. Do not run this against someone else's active queue without permission. Windows uses the same command in its Python environment.

**NO-RESULT:** real CPU ComfyUI (no isolated installation found); real Linux warm-model/GPU (no GPU on host, no spend authorized); all Windows cells (no tester authorized); integrated real ComfyUI plus Runtime lifecycle; true server queue interval; actual output files or representative large video; 100 MB variant; filesystem flush counts. No inference about LS-7 is made from these partial measurements. The trivial graph assumes standard `EmptyImage` and `SaveImage` nodes; validate on the target's installed version.

Initial focused test lacked aiohttp in the Runtime venv; moving the optional import to the transport entrypoint fixed it. Initial stand-in client raced server startup; a bounded readiness check fixed it. Raw first failures and reruns are in the run workspace, not these published measurements.

## Integrated stand-in → unchanged Runtime, 20 jobs

This follows one caller wall interval from before task creation through durable settlement; the total is measured directly and is not a sum of component medians. Each caller holds its own Comfy HTTP connection and websocket established before measurement. The script creates and claims a Runtime task, submits a filled graph, waits for history-ready, reads history once, fetches and hashes the one output once, and settles those exact bytes through the unmodified Runtime HTTP/CAS. After the interval it verifies the exact object bytes, succeeded task, and managed-output association. The two-caller test serializes create plus claim with a lock to ensure each caller gets its own task; lock wait is included in wall time and reported separately. Runtime HTTP uses urllib and does not hold connections. Concurrent samples do not wait for each other’s post-settlement verification to finish, so other verification reads can overlap a caller’s measured interval.

| Integrated stand-in + Runtime | caller wall median / slowest, ms | settle median / slowest, ms |
| --- | ---: | ---: |
| One caller | 33.09 / 61.95 | 20.38 / 39.71 |
| Two callers | 56.81 / 83.31 | 34.60 / 54.60 |

The stand-in returns a 1,048,576-byte valid RGB PNG with 1024 × 1024 pixels: a solid-color image whose unique ancillary chunk supplies most of its size. This checks a one-megapixel image container and byte volume, not a representative compressed photograph. Fixture-side creation of that padded response is inside POST time; its deliberate 1 ms asynchronous delay is inside the observed post-response-to-start interval. It does no real Comfy validation or model execution. Neither the resulting wall time nor the timing components establish the real Comfy floor. The 20 records and all phase medians and maxima are `integrated-1m-1.json` and `integrated-1m-2.json`; these runs took place after the manager reported competing proof workloads had finished. The host was not otherwise isolated.

The earlier 10 MiB video fixture is a one-second 64 × 64, 10 fps MPEG-4 Part 2 video with a large MP4 free box, not 10 MiB of encoded moving picture. The earlier 1 MiB Runtime-only PNG was 1 × 1 with padding, not a megapixel. The new integrated fixture is the megapixel cell; retain the earlier records only as labeled byte-volume probes. No conclusions about real video processing follow from either payload.

For the **real integrated** Linux CPU or GPU run, start an isolated compatible ComfyUI, warm the model for a warm run, and use a Runtime checkout at the stated revision with its dependencies **and aiohttp** installed. From the Runtime checkout:

```sh
PYTHONPATH=.:tests /path/to/venv/bin/python /path/to/astrid-dev/releases/14/evidence/ls1/integrated_floor.py --url http://127.0.0.1:8188 --graph /path/to/astrid-dev/releases/14/evidence/ls1/trivial-graph.json --samples 20 --callers 1 --output real-integrated-cpu.json
PYTHONPATH=.:tests /path/to/venv/bin/python /path/to/astrid-dev/releases/14/evidence/ls1/integrated_floor.py --url http://127.0.0.1:8188 --graph /path/to/prepared-warm-api-graph.json --samples 20 --callers 2 --output real-integrated-warm.json
```

On Windows PowerShell, in the Runtime checkout, set `$env:PYTHONPATH = '.;tests'`, then invoke the same script with `& .\venv\Scripts\python.exe` and Windows paths for `--graph` and `--output`. Run both `--callers 1` and `--callers 2` per graph; use a single declared output, suitable `--media-type`, and a unique `__LS1_PREFIX__` slot. This only prepares runnable commands: Windows and GPU results still require a tester or authorized machine.

**Real CPU ComfyUI barrier:** no ComfyUI checkout or package was found in the workspace, and `torch` and `comfy` are absent in system Python and both prepared Runtime and VibeComfy Python 3.13 environments. A real trivial run therefore requires an isolated compatible ComfyUI checkout and its CPU PyTorch/runtime dependencies. No weights are needed for the included EmptyImage→SaveImage graph. No large dependencies or models were installed and no existing user ComfyUI was changed.

## Prepared warm-model graph (not executed)

`warm-z-image-graph.json` is a hand-written API prompt transcribed from the
published VibeComfy ready template `ready_templates/image/z_image_turbo.py` at
VibeComfy revision `dba38f8644c46f652376f2cd5112ea161e40f09b`. Its node classes,
links, model filenames, AuraFlow shift, sampler, and eight-step settings follow
that source; the prompt text reuses the template's default prompt. The source
declares three model assets: `z_image_turbo_bf16.safetensors`,
`qwen_3_4b.safetensors`, and `ae.safetensors`, in ComfyUI's diffusion_models,
text_encoders, and vae model directories respectively. This graph is input to
`comfy_floor.py` or `integrated_floor.py`, not a VibeComfy bundle.

The probe substitutes `__LS1_PREFIX__` with a unique output prefix on every
sample. It substitutes `__LS1_SEED__` with the sample index. The graph and node
compatibility have not been validated against a running ComfyUI; it makes no
claim that the named files are installed, that the graph runs on a specific
ComfyUI revision, that its memory fits a particular GPU, or that any runtime or
warm-model timing has been measured. A tester must use an isolated ComfyUI with
these compatible model files already available and record its ComfyUI/model
versions and hardware before execution. No model download or load was performed
to prepare this file.
