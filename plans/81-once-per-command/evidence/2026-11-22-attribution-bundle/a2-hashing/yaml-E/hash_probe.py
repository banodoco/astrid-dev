"""Disposable CLI-only SHA-256 and YAML call observer; never stores input bytes."""
import atexit
from collections import OrderedDict
import hashlib
import json
import os
from pathlib import Path
import threading
import time

_events=[]
_objects=OrderedDict()
_guard=threading.local()
_MAX=96
_MAX_BYTES=8*1024*1024
_retained=0
_peak_retained=0

def _safe(path):
 try:
  p=Path(path).resolve()
  if any(w in str(p).lower() for w in ('.env','credential','secret','token')): return None
  allowed=(Path('/root/codex/plan-81m/profile-a2'),Path('/root/codex/plan-81m/VibeComfy'),Path('/root/codex/plan-81m/a4-runtime'))
  if any(p.is_relative_to(x) for x in allowed): return str(p)
  if str(p).startswith('/tmp/a4-launcher-') and p.suffix.lower() in ('.py','.yaml','.yml','.json','.toml','.md','.txt','.sql','.lock'): return '<fixture>/'+p.name
 except (OSError,TypeError,ValueError): pass
 return None

def _meta(path):
 try:
  s=Path(path).stat(); return [s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 except (OSError,TypeError,ValueError): return None

def _remember(data,path,before,after):
 global _retained,_peak_retained
 safe=_safe(path)
 if safe is None:return
 size=len(data.encode('utf-8')) if isinstance(data,str) else len(data)
 if size>_MAX_BYTES:return
 previous=_objects.pop(id(data),None)
 if previous:_retained-=previous[4]
 _objects[id(data)]=(data,safe,before,after,size); _retained+=size
 _objects.move_to_end(id(data))
 while len(_objects)>_MAX or _retained>_MAX_BYTES:
  _,old=_objects.popitem(last=False); _retained-=old[4]
 _peak_retained=max(_peak_retained,_retained)

def _lookup(value,consume=False):
 global _retained
 row=_objects.get(id(value))
 if row is None or row[0] is not value:return (None,None,None)
 if consume:_objects.pop(id(value)); _retained-=row[4]
 return row[1:4]

def _emit(value):
 try:_events.append(value)
 except Exception:pass

def _caller():
 f=__import__('sys')._getframe(2)
 while f and f.f_code.co_filename==__file__: f=f.f_back
 if not f:return ['unknown',0,'unknown']
 name=_safe(f.f_code.co_filename) or '<other-code>'
 return [name,f.f_lineno,f.f_code.co_name]

def install():
 read_bytes=Path.read_bytes; read_text=Path.read_text
 def bytes_read(p):
  safe=_safe(p); before=_meta(p) if safe else None
  value=read_bytes(p)
  if safe:
   try:_remember(value,p,before,_meta(p))
   except Exception:pass
  return value
 def text_read(p,*a,**kw):
  safe=_safe(p); before=_meta(p) if safe else None
  value=read_text(p,*a,**kw)
  if safe:
   try:_remember(value,p,before,_meta(p))
   except Exception:pass
  return value
 Path.read_bytes=bytes_read; Path.read_text=text_read
 original=hashlib.sha256
 class Hash:
  def __init__(self,data=b'',**kwargs):
   t=time.monotonic_ns(); self.inner=original(data,**kwargs); self.elapsed=time.monotonic_ns()-t
   obs=time.monotonic_ns()
   try:self.caller=_caller(); self.path,self.before,self.after=_lookup(data,True); self.size=memoryview(data).nbytes
   except Exception:self.caller=['<observer-error>',0,'unknown']; self.path=self.before=self.after=None; self.size=None
   self.observer_ns=time.monotonic_ns()-obs; self.done=False
  def update(self,data):
   t=time.monotonic_ns(); result=self.inner.update(data); self.elapsed+=time.monotonic_ns()-t
   obs=time.monotonic_ns()
   try:self.size+=memoryview(data).nbytes
   except Exception:self.size=None
   self.observer_ns+=time.monotonic_ns()-obs; return result
  def _finish(self,name):
   t=time.monotonic_ns(); value=getattr(self.inner,name)(); self.elapsed+=time.monotonic_ns()-t
   if not self.done:
    _emit({'kind':'sha256','caller':self.caller,'path':self.path,'bytes':self.size,'elapsed_ns':self.elapsed,'observer_ns':self.observer_ns,'metadata_before':self.before,'metadata_after':self.after}); self.done=True
   return value
  def digest(self):return self._finish('digest')
  def hexdigest(self):return self._finish('hexdigest')
  def copy(self):
   result=object.__new__(Hash); result.inner=self.inner.copy(); result.caller=self.caller; result.path=self.path; result.before=self.before; result.after=self.after; result.size=self.size; result.elapsed=self.elapsed; result.observer_ns=self.observer_ns; result.done=False; return result
  def __getattr__(self,key):return getattr(self.inner,key)
 hashlib.sha256=Hash
 original_file_digest=hashlib.file_digest
 def file_digest(stream,digest,*a,**kw):
  name=getattr(stream,'name',None); path=_safe(name); before=_meta(name) if path else None; caller=_caller()
  try:start_offset=stream.tell()
  except (OSError,AttributeError):start_offset=None
  t=time.monotonic_ns()
  try:return original_file_digest(stream,digest,*a,**kw)
  finally:
   elapsed=time.monotonic_ns()-t
   try:end_offset=stream.tell()
   except (OSError,AttributeError):end_offset=None
   if digest=='sha256':_emit({'kind':'sha256.file_digest','caller':caller,'path':path,'bytes':end_offset-start_offset if start_offset is not None and end_offset is not None else None,'elapsed_ns':elapsed,'metadata_before':before,'metadata_after':_meta(name) if path else None,'elapsed_includes':'file reads and hashing'})
 hashlib.file_digest=file_digest
 import yaml
 original_load=yaml.safe_load
 original_direct=yaml.load
 def direct_load(stream,*args,**kwargs):
  if getattr(_guard,'safe_load',False):return original_direct(stream,*args,**kwargs)
  path,before,after=_lookup(stream)
  if path is None and hasattr(stream,'name'):
   path=_safe(stream.name); before=_meta(stream.name) if path else None
  caller=_caller(); t=time.monotonic_ns()
  try:return original_direct(stream,*args,**kwargs)
  finally:
   elapsed=time.monotonic_ns()-t
   if path and hasattr(stream,'name'):after=_meta(stream.name)
   _emit({'kind':'yaml.load','caller':caller,'path':path,'elapsed_ns':elapsed,'metadata_before':before,'metadata_after':after})
 yaml.load=direct_load
 def safe_load(stream):
  path,before,after=_lookup(stream)
  if path is None and hasattr(stream,'name'):
   path=_safe(stream.name); before=_meta(stream.name) if path else None
  caller=_caller(); t=time.monotonic_ns()
  previous=getattr(_guard,'safe_load',False); _guard.safe_load=True
  try:return original_load(stream)
  finally:
   _guard.safe_load=previous
   elapsed=time.monotonic_ns()-t
   if path and hasattr(stream,'name'):after=_meta(stream.name)
   _emit({'kind':'yaml.safe_load','caller':caller,'path':path,'elapsed_ns':elapsed,'metadata_before':before,'metadata_after':after})
 yaml.safe_load=safe_load
 @atexit.register
 def flush():
  target=os.environ.get('A4_HASH_LOG')
  if target:
   try:
    import resource
    with open(target,'w',encoding='utf-8') as f:json.dump({'pid':os.getpid(),'events':_events,'peak_retained_bytes':_peak_retained,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},f)
   except Exception:pass
