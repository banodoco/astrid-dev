"""Run `python -m astrid.omp_agent ARGS` and record, for selected modules, the first Python stack that triggers their import."""
import sys, runpy, traceback, json
T={"astrid.core.execution.generic_host","vibecomfy.porting.emit.ui","astrid.core.generation.backends.comfy_schema","numpy"}
seen={}
class F:
    def find_spec(self,name,path=None,target=None):
        if name in T and name not in seen and name not in sys.modules:
            fr=[f"{'/'.join(f.filename.split('/')[-3:])}:{f.lineno} {f.name}" for f in traceback.extract_stack()[:-1] if "importlib" not in f.filename and "trace_importer" not in f.filename and not f.filename.startswith("<")]
            seen[name]=fr[-9:]
        return None
sys.meta_path.insert(0,F())
sys.argv=["astrid.omp_agent"]+sys.argv[1:]
try: runpy.run_module("astrid.omp_agent",run_name="__main__",alter_sys=True)
except SystemExit: pass
finally: json.dump(seen,open("/home/user/baseline/importprofile/importers.json","w"),indent=1)
