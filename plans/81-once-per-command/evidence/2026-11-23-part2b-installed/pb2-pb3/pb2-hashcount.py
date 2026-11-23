import hashlib,sys,tempfile
from pathlib import Path
from vibecomfy.cli_loader import load_workflow_any
from vibecomfy.workflow_bundle import emit_bundle
workflow=load_workflow_any('image/qwen_image_2_1_turbo')
with tempfile.TemporaryDirectory() as folder:
 emit_bundle(workflow,Path(folder)/'warm'/'workflow.py',{})
 old=hashlib.sha256
 count=[0]
 def counted(*args,**kwargs):
  frame=sys._getframe(1)
  while frame:
   if '/vibecomfy/porting/object_info/' in frame.f_code.co_filename:
    count[0]+=1
    break
   frame=frame.f_back
  return old(*args,**kwargs)
 hashlib.sha256=counted
 emit_bundle(workflow,Path(folder)/'out'/'workflow.py',{})
 print('object-info sha256 calls:',count[0])
