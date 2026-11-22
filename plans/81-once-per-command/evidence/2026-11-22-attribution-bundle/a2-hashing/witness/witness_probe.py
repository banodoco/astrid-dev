"""Disposable CLI-only witness call observer. No file contents are retained."""
import atexit
import json
import os
from pathlib import Path
import sys
import time

_events=[]
_frame_names={}

def safe(path):
 try:
  p=Path(path).resolve()
  if any(s in str(p).lower() for s in ('.env','credential','secret','token')):return None
  for base in ('/root/codex/plan-81m/profile-a2','/root/codex/plan-81m/VibeComfy','/root/codex/plan-81m/a4-runtime'):
   if p.is_relative_to(base):return str(p)
  parts=p.parts
  if len(parts)>3 and parts[1]=='tmp' and parts[2].startswith('a4-launcher-'):
   return '<fixture>/'+str(Path(*parts[3:]))
 except (OSError,TypeError,ValueError):pass
 return None

def stat(path):
 try:
  s=Path(path).stat();return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 except (OSError,ValueError,TypeError):return None

def install():
 import vibecomfy.porting.object_info.generation as g
 original=g.cache_file_witness
 def observed(path):
  safe_path=safe(path); before=stat(path) if safe_path else None
  frames=[]; f=sys._getframe(1)
  while f:
   raw=f.f_code.co_filename
   if raw not in _frame_names:_frame_names[raw]=safe(raw) or '<external-code>'
   filename=_frame_names[raw]
   frames.append([filename,f.f_lineno,f.f_code.co_name]); f=f.f_back
  t=time.monotonic_ns()
  try:return original(path)
  finally:
   elapsed=time.monotonic_ns()-t
   try:_events.append({'path':safe_path,'stack':frames,'elapsed_ns':elapsed,'metadata_before':before,'metadata_after':stat(path) if safe_path else None})
   except Exception:pass
 g.cache_file_witness=observed
 for name in ('vibecomfy.porting.object_info.consume','vibecomfy.schema.provider'):
  module=sys.modules.get(name)
  if module is not None and getattr(module,'cache_file_witness',None) is original:module.cache_file_witness=observed
 @atexit.register
 def flush():
  target=os.environ.get('A4_WITNESS_LOG')
  if target:
   try:
    with open(target,'w',encoding='utf-8') as f:json.dump({'pid':os.getpid(),'events':_events},f)
   except Exception:pass
