"""Time one emit_bundle of the qwen ready template; count SHA-256 bytes; optional cProfile.

usage: python probe.py <vibecomfy_tree> <cold|warm|buildwarm> [profile_out]
"""
import cProfile, hashlib, importlib.util, io, pstats, sys, tempfile, time
from pathlib import Path

tree = Path(sys.argv[1]); mode = sys.argv[2]
prof_out = sys.argv[3] if len(sys.argv) > 3 else None
sys.path.insert(0, str(tree))

from vibecomfy.workflow_bundle import emit_bundle  # noqa
from vibecomfy.porting.object_info import consume as c  # noqa

spec = importlib.util.spec_from_file_location("qwen_tpl", tree / "ready_templates/image/qwen_image_2_1_turbo.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

t0 = time.perf_counter(); wf = mod.build(); t_build = time.perf_counter() - t0
if mode == "cold":
    c.reset_cache()
elif mode == "warm":
    c.reset_cache(); c.get_class("KSamplerSelect")

stats = {"calls": 0, "bytes": 0}
_real = hashlib.sha256
class _Counting:
    def __init__(self, data=b"", **kw):
        stats["calls"] += 1; stats["bytes"] += len(data); self._h = _real(data, **kw)
    def update(self, data):
        stats["bytes"] += len(data); self._h.update(data)
    def __getattr__(self, n):
        return getattr(self._h, n)
hashlib.sha256 = _Counting

orig_wit = c._cache_file_witness if hasattr(c, "_cache_file_witness") else c.cache_file_witness
wit = {"n": 0}
from vibecomfy.porting.object_info import generation as g
_gw = g.cache_file_witness
def counted(p):
    wit["n"] += 1; return _gw(p)
if hasattr(c, "_cache_file_witness"):
    c._cache_file_witness = counted
else:
    c.cache_file_witness = counted

res = {}
_rr = c._resolve_class_type
def rr(ct):
    res[ct] = res.get(ct, 0) + 1; return _rr(ct)
c._resolve_class_type = rr

with tempfile.TemporaryDirectory() as d:
    pr = cProfile.Profile() if prof_out else None
    t0 = time.perf_counter()
    if pr: pr.enable()
    emit_bundle(wf.clone() if hasattr(wf, "clone") else wf, Path(d) / "workflow.py", {"operation": "authored"})
    if pr: pr.disable()
    dt = time.perf_counter() - t0
hashlib.sha256 = _real
print(f"tree={tree.parent.name} mode={mode} build={t_build:.3f}s emit={dt:.3f}s sha256_calls={stats['calls']} sha256_bytes={stats['bytes']/1e9:.3f}GB witness_calls={wit['n']} class_lookups={sum(res.values())} distinct_classes={len(res)}")
if pr:
    s = io.StringIO(); ps = pstats.Stats(pr, stream=s).sort_stats("tottime"); ps.print_stats(25)
    s2 = io.StringIO(); pstats.Stats(pr, stream=s2).sort_stats("cumulative").print_stats(45)
    Path(prof_out).write_text(s.getvalue() + "\n\n=== cumulative ===\n" + s2.getvalue())
