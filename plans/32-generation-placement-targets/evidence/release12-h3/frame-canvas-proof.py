"""Bounded CPU fakes; execute extracted exact pinned source methods, no node registration."""
import ast, hashlib, json, math
from pathlib import Path
from types import SimpleNamespace
from enum import Enum
from astrid.packs.h3_av.shared.timing import plan_continuation

comfy=Path('/tmp/r12-b5-comfy'); h3=Path('/tmp/r12-b5-h3-source')
assert __import__('subprocess').check_output(['git','-C',str(comfy),'rev-parse','HEAD'],text=True).strip()=='ee71d5c4993f29086b27fde1629a945ae48425bf'
assert __import__('subprocess').check_output(['git','-C',str(h3),'rev-parse','HEAD'],text=True).strip()=='361624fb406b63eb6694442eac6c895fc1533a70'

def method(path, cls, method, namespace):
 tree=ast.parse(path.read_text()); clsnode=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==cls)
 fn=next(n for n in clsnode.body if isinstance(n,ast.FunctionDef) and n.name==method)
 fn.decorator_list=[]; fn.returns=None
 for a in (*fn.args.posonlyargs,*fn.args.args,*fn.args.kwonlyargs):a.annotation=None
 module=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])); exec(compile(module,str(path),'exec'),namespace); return namespace[method]

# Fixed expression from compiled API graph. The fake evaluator admits only its
# constants, variable, arithmetic and max/round calls; it is not simpleeval.
graph=json.loads(Path('/tmp/r12-b5-h3-graphs2/continuation-False.json').read_text()); expression=graph['102']['inputs']['expression']
expected='max(5, round(a * 24)) + (5 - (max(5, round(a * 24)) % 17)) % 17'; assert expression==expected
allowed=(ast.Expression,ast.BinOp,ast.Add,ast.Sub,ast.Mult,ast.Mod,ast.Call,ast.Name,ast.Load,ast.Constant)
def fake_simple_eval(text,*,names,functions):
 tree=ast.parse(text,mode='eval'); assert all(isinstance(n,allowed) for n in ast.walk(tree)); assert all(not isinstance(n,ast.Name) or n.id in ('a','max','round') for n in ast.walk(tree)); return eval(compile(tree,'<bounded-expression>','eval'),{'__builtins__':{}},{'a':names['a'],'max':functions['max'],'round':functions['round']})
io=SimpleNamespace(NodeOutput=lambda *a:a)
math_method=method(comfy/'comfy_extras/nodes_math.py','MathExpressionNode','execute',{'simple_eval':fake_simple_eval,'MATH_FUNCTIONS':{'max':max,'round':round},'math':math,'io':io})
crop=method(h3/'h3_auto_crop32.py','MiniMaxH3CropTo32','crop_to_32',{})
select=method(h3/'h3_auto_crop32.py','MiniMaxH3StartCanvasSelector','select',{})
# Source ratio and exact execute method with inert io.NodeOutput.
ratio_source=ast.parse((comfy/'comfy_extras/nodes_resolution.py').read_text()); statements=[n for n in ratio_source.body if isinstance(n,ast.ClassDef) and n.name=='AspectRatio' or isinstance(n,ast.AnnAssign) and isinstance(n.target,ast.Name) and n.target.id=='ASPECT_RATIOS']; ns={'Enum':Enum}; exec(compile(ast.fix_missing_locations(ast.Module(body=statements,type_ignores=[])),str(comfy/'comfy_extras/nodes_resolution.py'),'exec'),ns)
resolve=method(comfy/'comfy_extras/nodes_resolution.py','ResolutionSelector','execute',{'ASPECT_RATIOS':ns['ASPECT_RATIOS'],'math':math,'io':io})
class Image:
 ndim=4
 def __init__(self,w,h):self.shape=(1,h,w,3)
 def __getitem__(self,key):return ('fake-slice',key)

print('expression',expression)
for output_frames in (25,26,41,42,48,120,240,362):
 plan=plan_continuation(source_end=1,output_duration=output_frames/24); result=math_method(None,expression,{'a':plan.workflow_duration}); n=result[1]
 assert n==plan.raw_extension_frames and 5<=n<=3600 and (n-5)%17==0
 print('timing',f'source=24 output={output_frames} new={plan.requested_new_frames} workflow={plan.workflow_duration:.12g} node102={n} trim={plan.trim_tail_frames}')
width,height=resolve(None,'16:9 (Widescreen)',0.5,32); print('resolution node1024',width,height); assert (width,height)==(960,544)
for w,h in ((1024,576),(1920,1080),(641,479),(32,32),(16385,8193)):
 _,cw,ch=crop(None,Image(w,h)); selected=select(None,'existing_video',width,height,cw,ch); assert selected==(cw,ch) and all(32<=x<=16384 and x%32==0 for x in selected); print('canvas',f'source={w}x{h} crop={cw}x{ch} selected={selected[0]}x{selected[1]}')
_,oversized_w,oversized_h=crop(None,Image(16416,8192)); oversized=select(None,'existing_video',width,height,oversized_w,oversized_h); assert oversized[0]>16384; print('canvas source=16416x8192 returns 16416x8192, above ee71 H3 width max=16384 (unbounded fake; actual loader limits not proven)')
try:crop(None,Image(31,100))
except ValueError: print('canvas source=31x100 refused as too small')
else:raise AssertionError('small source not refused')
print('ok: extracted source methods, faked evaluator/io/image; no registration, actual media, GPU or installed-node claim')
