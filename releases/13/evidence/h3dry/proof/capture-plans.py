from pathlib import Path
import time,shutil
root=Path('/home/user/wt/h3real.env/tmp')
p=Path('/home/user/cells/evidence/h3real/plan-snapshots');p.mkdir(exist_ok=True)
while not Path('/home/user/cells/evidence/h3real/capture.stop').exists():
 for f in root.glob('astrid-job-*/h3/plan/compile/compilation.json'):
  dest=p/f.parts[-5];dest.mkdir(exist_ok=True)
  try:
   shutil.copy2(f,dest/'compilation.json')
   graph=f.parent/'workflow-bundle/workflow.vibe.json'
   if graph.exists(): shutil.copy2(graph,dest/'workflow.vibe.json')
  except FileNotFoundError: pass
 time.sleep(.3)
