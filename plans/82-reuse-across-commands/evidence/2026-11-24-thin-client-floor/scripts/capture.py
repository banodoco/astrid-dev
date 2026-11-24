"""Run one `astrid generate` in-process and record every Runtime HTTP request it makes.

Usage (installed venv, version env applied): python -X utf8 -I capture.py OUTDIR <astrid args...>
The Authorization header is never recorded (only header names are kept).
"""
import io, json, os, sys, time, runpy
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
sys.argv = ["astrid", *sys.argv[2:]]
from astrid_runtime_client import generated as g
orig = g.WorkspaceClient._request
seq = [0]
def logged(self, method, path, *, body=None, headers=None, **kw):
    seq[0] += 1; n = seq[0]
    if body is not None and not isinstance(body, (bytes, bytearray)):
        data = body.read(); body = io.BytesIO(data)
    else:
        data = body
    t0 = time.perf_counter()
    status, rh, rb = orig(self, method, path, body=body, headers=headers, **kw)
    dt = time.perf_counter() - t0
    if data is not None:
        open(f"{out}/{n:03d}.req.bin", "wb").write(data)
    open(f"{out}/{n:03d}.resp.bin", "wb").write(rb if isinstance(rb, (bytes, bytearray)) else b"")
    with open(f"{out}/requests.jsonl", "a") as f:
        f.write(json.dumps({"n": n, "method": method, "path": path, "header_names": sorted((headers or {}).keys()),
                            "headers_no_auth": {k: v for k, v in (headers or {}).items() if k.lower() != "authorization"},
                            "req_bytes": len(data) if data is not None else None, "status": status, "seconds": dt}) + "\n")
    return status, rh, rb
g.WorkspaceClient._request = logged
runpy.run_module("astrid.omp_agent", run_name="__main__", alter_sys=True)
