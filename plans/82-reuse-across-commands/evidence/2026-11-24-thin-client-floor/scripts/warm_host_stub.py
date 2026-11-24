"""Plan 82 floor experiment: a STUB warm host (not product code).

Run once with the installed venv python and the selected version's env applied:
    python -X utf8 -I warm_host_stub.py SOCKET COMFY_URL PROJECT

At start it runs one `astrid generate` through the full product path in-process
(astrid.console.main, an embedded invocation) and keeps:
  * the exact Runtime requests it sent (object imports and POST /v1/tasks body),
  * the emitted workflow.py / workflow.vibe.json bytes,
  * a deep copy of the workflow object handed to emit_bundle (the built graph).
Then it opens its own Runtime connection with the product's
AstridClient.open_from_launcher() (product code reads the launcher-issued
credential; this script never reads it) and serves one-line JSON requests on a
Unix socket. Modes per request:
  naive    literal substitution of prompt and seed into the kept bytes, stale
           companion and stale approval digests, 2 object POSTs + POST /v1/tasks
  real     node-list fetch, deep copy + set_input (slot checks), emit_bundle
           (render), 3 object POSTs as the CLI does, the product's invocation
           preflight (approval digests), POST /v1/tasks
  realfull real, plus the product's target node list and model resolution
           (_capture_model_resolution, TargetSchemaProvider, require_workflow_assets)
           and the approval compile (load_bundle, require_canonical_authority, compile)
  product  astrid.console.main(["generate", ...]) in this warm process (today's
           code, held warm)
  wait     poll a task until it is terminal (untimed housekeeping)
Every request returns the server-side step timings.
"""
from __future__ import annotations

import contextlib, copy, hashlib, io, json, os, socket, sys, tempfile, time, uuid
from pathlib import Path

SOCK, COMFY, PROJECT = sys.argv[1], sys.argv[2], sys.argv[3]
WARM_PROMPT, WARM_SEED = "a blue circle, variation 7", 12345
T0 = time.perf_counter()
FULL = [False]

# ---- 1. warm-up through the full product path, recording what it sends
from astrid_runtime_client import generated as g
_orig_request = g.WorkspaceClient._request
recorded: list[dict] = []
recording = [True]

def _recording_request(self, method, path, *, body=None, headers=None, **kw):
    data = body
    if body is not None and not isinstance(body, (bytes, bytearray)):
        data = body.read(); body = io.BytesIO(data)
    status, rh, rb = _orig_request(self, method, path, body=body, headers=headers, **kw)
    if recording[0]:
        recorded.append({"method": method, "path": path, "body": data, "status": status, "response": rb,
                         "headers": {k: v for k, v in (headers or {}).items() if k.lower() != "authorization"}})
    return status, rh, rb

g.WorkspaceClient._request = _recording_request

import vibecomfy.workflow_bundle as wb
_orig_emit = wb.emit_bundle
kept_workflow: list = []

def _keeping_emit(workflow, path, *a, **kw):
    if not kept_workflow:
        kept_workflow.append(copy.deepcopy(workflow))
    return _orig_emit(workflow, path, *a, **kw)

wb.emit_bundle = _keeping_emit

import astrid.core.generation.backends.vibecomfy as _vcb
_orig_capture = _vcb._capture_model_resolution
kept_capture: list = []

def _keeping_capture(*a, **kw):
    if not kept_capture:
        kept_capture.append((a, kw))
    return _orig_capture(*a, **kw)

_vcb._capture_model_resolution = _keeping_capture

from astrid import console
args = ["generate", "image", WARM_PROMPT, "--seed", str(WARM_SEED), "--mode", "t2i", "--placement", COMFY,
        "--project", PROJECT, "--no-wait", "--json"]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = console.main(args)
warm_out = json.loads(buf.getvalue())
assert rc == 0 and warm_out["ok"], buf.getvalue()[:2000]
recording[0] = False
wb.emit_bundle = _orig_emit
_vcb._capture_model_resolution = _orig_capture
T_WARM = time.perf_counter() - T0

objs = [r for r in recorded if r["method"] == "POST" and r["path"].endswith("/objects")]
task_req = [r for r in recorded if r["method"] == "POST" and r["path"] == "/v1/tasks"][-1]
by_name = {r["headers"]["X-Original-Name"]: r for r in objs}
SRC_NAME = next(n for n in by_name if n not in ("workflow.py", "workflow.vibe.json"))
PY0, COMP0, SRC0 = by_name["workflow.py"]["body"], by_name["workflow.vibe.json"]["body"], by_name[SRC_NAME]["body"]
TASK0 = json.loads(task_req["body"])
OBJ_PATH = objs[0]["path"]

# ---- 2. our own Runtime connection through the product's launcher boundary
from astrid.sdk.client import AstridClient
t = time.perf_counter()
client = AstridClient.open_from_launcher()
T_CONNECT = time.perf_counter() - t
ws = client._remote._transport          # astrid.sdk.workspace_client.WorkspaceClient
gen = ws._generated                      # generated Runtime client (holds the session)
from astrid.sdk.remote import _vibecomfy_invocation_preflight
from astrid.core.generation.entries import _EntryDiscovery
ENTRY = "qwen-image-2.1-turbo"
DISCOVERY = _EntryDiscovery()
REGISTRY = DISCOVERY.registry

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def post_object(data: bytes, name: str, ctype: str) -> None:
    gen._request("POST", OBJ_PATH, body=data, expected=(200, 201),
                 headers={"Content-Type": ctype, "Idempotency-Key": uuid.uuid4().hex,
                          "Content-Length": str(len(data)), "X-Original-Name": name})

def task_body(py: bytes, comp: bytes, prompt: str, seed: int, receipt: dict | None) -> bytes:
    text = json.dumps(TASK0)
    for old, new in ((sha(PY0), sha(py)), (sha(COMP0), sha(comp))):
        text = text.replace(old, new)
    body = json.loads(text)
    inputs = body["spec"]["inputs"]
    inputs["python"]["bytes"] = len(py); inputs["companion"]["bytes"] = len(comp)
    inputs["workflow_inputs"] = json.dumps({"prompt": prompt, "seed": seed}, sort_keys=True)
    # input_object_ids is sorted by digest in the CLI's request
    body["input_object_ids"] = sorted(body["input_object_ids"])
    if receipt is not None:
        body["spec"]["invocation_preflight"] = receipt
    return json.dumps(body).encode()

def admit(body: bytes) -> dict:
    status, _, rb = gen._request("POST", "/v1/tasks", body=body, expected=(200, 201),
                                 headers={"Content-Type": "application/json", "Idempotency-Key": uuid.uuid4().hex})
    return json.loads(rb)

def naive(prompt: str, seed: int) -> dict:
    s = {}; t = time.perf_counter()
    py = PY0.replace(repr(WARM_PROMPT).encode(), repr(prompt).encode()) \
            .replace(f"DEFAULT_SEED = {WARM_SEED}\n".encode(), f"DEFAULT_SEED = {seed}\n".encode())
    comp = COMP0  # stale generation_id; see README
    s["substitute"] = time.perf_counter() - t; t = time.perf_counter()
    post_object(py, "workflow.py", "text/x-python"); post_object(comp, "workflow.vibe.json", "application/json")
    s["object POSTs x2"] = time.perf_counter() - t; t = time.perf_counter()
    body = task_body(py, comp, prompt, seed, None)  # approval digests stay those of the warm-up graph
    s["task body"] = time.perf_counter() - t; t = time.perf_counter()
    res = admit(body)
    s["POST /v1/tasks"] = time.perf_counter() - t
    return {"task": res, "steps": s, "py_sha": sha(py), "comp_sha": sha(comp)}

def real(prompt: str, seed: int, keep: bool = False) -> dict:
    import urllib.request
    s = {}; t = time.perf_counter()
    with urllib.request.urlopen(COMFY.rstrip("/") + "/object_info", timeout=15) as r:
        info = json.loads(r.read())
    assert isinstance(info, dict) and info
    s["node-list fetch"] = time.perf_counter() - t; t = time.perf_counter()
    ws.health()
    s["Runtime liveness (GET health)"] = time.perf_counter() - t; t = time.perf_counter()
    DISCOVERY.resolve_entry_inputs(ENTRY, {"prompt": prompt, "seed": seed}, mode="t2i", kind="image", registry=REGISTRY)
    s["slot checks (resolve_entry_inputs)"] = time.perf_counter() - t; t = time.perf_counter()
    wf = copy.deepcopy(kept_workflow[0])
    wf.set_input("prompt", prompt); wf.set_input("seed", seed)
    s["copy + slot fill/check"] = time.perf_counter() - t; t = time.perf_counter()
    if FULL[0]:
        from astrid.core.generation.backends.comfy_schema import TargetSchemaProvider
        from astrid.core.generation.asset_gaps import require_workflow_assets
        a, kw = kept_capture[0]; target = a[0]
        _plan, observed = _orig_capture(*a, **kw)
        schema = TargetSchemaProvider.from_object_info(observed, server_url=target.http_origin,
                                                       model_availability="target", refresh_object_info=target.object_info)
        require_workflow_assets(wf, observed, ENTRY)
        s["target node list + model resolution (product)"] = time.perf_counter() - t; t = time.perf_counter()
        bundle = wb.load_bundle(wf); bundle.require_canonical_authority("generate on target")
        bundle.compile(schema_provider=schema)
        s["approval compile (load_bundle + compile)"] = time.perf_counter() - t; t = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="floor-render-") as d:
        _orig_emit(wf, Path(d) / "workflow.py", {"operation": "authored"})
        py = (Path(d) / "workflow.py").read_bytes(); comp = (Path(d) / "workflow.vibe.json").read_bytes()
    s["render (emit_bundle)"] = time.perf_counter() - t; t = time.perf_counter()
    post_object(SRC0, SRC_NAME, by_name[SRC_NAME]["headers"]["Content-Type"])
    post_object(py, "workflow.py", "text/x-python"); post_object(comp, "workflow.vibe.json", "application/json")
    s["object POSTs x3"] = time.perf_counter() - t; t = time.perf_counter()
    spec = json.loads(task_body(py, comp, prompt, seed, None))["spec"]
    receipt = _vibecomfy_invocation_preflight(ws, spec)
    s["approval digests (invocation preflight)"] = time.perf_counter() - t; t = time.perf_counter()
    ws.list_capabilities()
    s["capability lookup (GET capabilities)"] = time.perf_counter() - t; t = time.perf_counter()
    body = task_body(py, comp, prompt, seed, receipt)
    s["task body"] = time.perf_counter() - t; t = time.perf_counter()
    res = admit(body)
    s["POST /v1/tasks"] = time.perf_counter() - t
    out = {"task": res, "steps": s, "py_sha": sha(py), "comp_sha": sha(comp),
           "receipt_api_digest": receipt.get("api_digest") if receipt else None}
    if keep:
        out["py"] = py.decode(); out["comp"] = comp.decode(); out["receipt"] = receipt
    return out

def product(prompt: str, seed: int) -> dict:
    t = time.perf_counter(); b = io.StringIO()
    with contextlib.redirect_stdout(b):
        rc = console.main(["generate", "image", prompt, "--seed", str(seed), "--mode", "t2i", "--placement", COMFY,
                           "--project", PROJECT, "--no-wait", "--json", "--timings"])
    d = json.loads(b.getvalue())
    return {"task": {"task_id": d.get("kernel_task_id"), "state": (d.get("raw_result") or {}).get("state")},
            "rc": rc, "steps": {"console.main": time.perf_counter() - t}, "timings": d.get("timings")}

def profile_render(prompt: str, seed: int) -> dict:
    import cProfile, pstats
    wf = copy.deepcopy(kept_workflow[0]); wf.set_input("prompt", prompt); wf.set_input("seed", seed)
    pr = cProfile.Profile()
    with tempfile.TemporaryDirectory(prefix="floor-prof-") as d:
        t = time.perf_counter(); pr.enable()
        _orig_emit(wf, Path(d) / "workflow.py", {"operation": "authored"})
        pr.disable(); wall = time.perf_counter() - t
    st = pstats.Stats(pr); rows = []
    for (fn, ln, name), (cc, nc, tt, ct, callers) in st.stats.items():
        rows.append({"func": f"{fn.split('site-packages/')[-1]}:{ln}:{name}", "calls": nc, "tottime": tt, "cumtime": ct})
    by_cum = sorted(rows, key=lambda r: -r["cumtime"])[:40]
    by_tot = sorted(rows, key=lambda r: -r["tottime"])[:25]
    return {"wall_profiled": wall, "by_cumtime": by_cum, "by_tottime": by_tot, "steps": {}}

def wait(task_id: str, limit: float = 60.0) -> dict:
    end = time.monotonic() + limit
    while True:
        task = ws.get_task(task_id)
        task = task if isinstance(task, dict) else getattr(task, "__dict__", {"repr": repr(task)})
        state = task.get("state") or task.get("status")
        if state in ("succeeded", "failed", "cancelled", "rejected", "settled", "completed") or time.monotonic() > end:
            return {"state": state, "task": json.loads(json.dumps(task, default=str))}
        time.sleep(0.5)

# ---- 3. validation of the real path against the warm-up's own bytes
check = real(WARM_PROMPT, WARM_SEED, keep=True)
VALID = {"py_identical": check["py"].encode() == PY0, "companion_identical": check["comp"].encode() == COMP0,
         "receipt_identical": check["receipt"] == TASK0["spec"]["invocation_preflight"],
         "warmup_seconds": T_WARM, "connect_seconds": T_CONNECT, "warmup_task": warm_out.get("kernel_task_id"),
         "validation_task": check["task"].get("task_id") or check["task"].get("id")}

try: os.unlink(SOCK)
except FileNotFoundError: pass
srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); srv.bind(SOCK); srv.listen(4)
print(json.dumps({"ready": True, "validation": VALID}), flush=True)
def real_full(prompt: str, seed: int) -> dict:
    FULL[0] = True
    try: return real(prompt, seed)
    finally: FULL[0] = False
HANDLERS = {"realfull": real_full, "naive": naive, "real": real, "product": product, "profile_render": profile_render}
while True:
    conn, _ = srv.accept()
    with conn:
        f = conn.makefile("rwb")
        line = f.readline()
        t = time.perf_counter()
        try:
            req = json.loads(line)
            if req["mode"] == "wait":
                out = wait(req["task_id"])
            elif req["mode"] == "validation":
                out = VALID
            else:
                out = HANDLERS[req["mode"]](req["prompt"], int(req["seed"]))
            out["ok"] = True
        except Exception as exc:  # report, keep serving
            out = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
        out["server_seconds"] = time.perf_counter() - t
        f.write(json.dumps(out, default=str).encode() + b"\n"); f.flush()
