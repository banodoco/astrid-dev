#!/usr/bin/env python3
"""Stand-in ComfyUI for the installed baseline. Run with the INSTALLED venv python (it imports the installed
astrid and vibecomfy). Adapted read-only from the managers' tests/integrations/runpod_slot_pod.py and
_pinned_source.attached_comfy (copied as standin_lib.py and *.managers-copy). CPU only: it validates /prompt
against packaged real node schemas and returns a tiny PNG; no image is generated.
Usage: standin_comfy.py --port N [--entry registry-id]   (default entry: qwen-image-2.1-turbo, the image.t2i default)"""
import argparse, http.server, json, os, re, sys
from urllib.parse import parse_qs, urlsplit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import standin_lib as lib

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, required=True)
ap.add_argument("--entry", default="qwen-image-2.1-turbo")
args = ap.parse_args()

from astrid.core.generation import entries
from vibecomfy.model_assets import _referenced_model_values
row = next(r for r in entries.ready_entries() if args.entry in (r["id"], r.get("registry_id")))
wf = entries._load_entry_workflow(row)
classes = {n.class_type for n in wf.runtime_nodes().values()}
files = [f"/x/models/{r['subdir']}/{r['value']}" for r in _referenced_model_values(wf)]
comfy = lib.PodComfy(classes, lambda: files)

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, status, data, mime="application/json"):
        body = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(status); self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        url = urlsplit(self.path)
        if url.path == "/object_info": return self._send(200, comfy.object_info())
        if url.path == "/system_stats": return self._send(200, {"system": {"os": "linux"}})
        if url.path == "/queue": return self._send(200, {"queue_running": [], "queue_pending": []})
        if url.path.startswith("/history"):
            tail = url.path.partition("/history/")[2]; h = getattr(comfy, "history", {})
            return self._send(200, {tail: h[tail]} if tail in h else {} if tail else h)
        if url.path == "/view":
            data, mime = comfy.outputs[parse_qs(url.query)["filename"][0]]; return self._send(200, data, mime)
        self._send(404, {})
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/prompt":
            status, payload = comfy.submit(json.loads(body)); return self._send(status, payload)
        if self.path in ("/queue", "/interrupt", "/free"): return self._send(200, {})
        if self.path == "/upload/image":
            sub = re.search(rb'name="subfolder"\r\n\r\n([^\r]*)\r\n', body); name = re.search(rb'name="image"; filename="([^"]+)"', body)
            saved = name[1].decode(); comfy.uploads[saved] = body
            comfy.input_files.add(f"{sub[1].decode()}/{saved}" if sub and sub[1] else saved)
            return self._send(200, {"name": saved, "subfolder": sub[1].decode() if sub else "", "type": "input"})
        self._send(404, {})

srv = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
print(f"stand-in ComfyUI on 127.0.0.1:{args.port} entry={row['id']} classes={len(classes)}", flush=True)
try: srv.serve_forever()
except KeyboardInterrupt: pass
