from pathlib import Path
import subprocess,json,shutil
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parents[1]
shutil.copyfile('/home/user/cells/evidence/h3real/in/T1-i2v-bike.mp4',p/'assets/bike.mp4')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p/'assets/bike.mp4'),'-t','3','-vf',"select='eq(n,0)+eq(n,35)+eq(n,71)',scale=iw:ih:flags=lanczos+accurate_rnd+full_chroma_int,format=rgb24",'-fps_mode','passthrough','-threads','1','-f','rawvideo','-pix_fmt','rgb24','pipe:1'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(3,576,1024,3)
boxes=[]
for n,a in zip((0,35,71),frames):
 Image.fromarray(a).resize((512,288)).save(p/f'evidence/frame-{n:02}.png')
 if n==0: Image.fromarray(a).save(p/'assets/subject-bike.png')
 m=(a[:,:,0]>140)&(a[:,:,1]<90)&(a[:,:,2]<90)
 # 8-connected components; discard tiny blobs (<20 strongly-red pixels).
 seen=np.zeros(m.shape,bool); kept=[]; sizes=[]
 for y,x in zip(*np.where(m)):
  if seen[y,x]: continue
  seen[y,x]=True; todo=[(y,x)]; comp=[]
  while todo:
   yy,xx=todo.pop(); comp.append((yy,xx))
   for dy in (-1,0,1):
    for dx in (-1,0,1):
     y2,x2=yy+dy,xx+dx
     if 0<=y2<576 and 0<=x2<1024 and m[y2,x2] and not seen[y2,x2]:
      seen[y2,x2]=True; todo.append((y2,x2))
  if len(comp)>=20: kept.extend(comp); sizes.append(len(comp))
 coords=np.array(kept); y0,x0=coords.min(0); y1,x1=coords.max(0)+1
 box=list(map(int,(x0,y0,x1,y1))); boxes.append(box)
 print(n,box,'components',sizes)
u=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
box=[max(0,u[0]-20),max(0,u[1]-20),min(1024,u[2]+20),min(576,u[3]+20)]
print('union',u,'margin box',box)
(p/'evidence/red-bounds.json').write_text(json.dumps(dict(convention='half-open x0,y0,x1,y1',threshold='R>140,G<90,B<90; 8-connected components >=20 pixels',frames=dict(zip(('0','35','71'),boxes)),union=u,margin_box=box),indent=2)+'\n')

d=json.loads((p/'evidence/red-bounds.json').read_text())
d['strict_red_margin_box']=d.pop('margin_box')
d.update(approximate_visual_bicycle_bounds={'0':[335,225,718,482],'35':[322,218,730,495],'71':[310,210,748,506]},approximate_visual_union=[310,210,748,506],chosen_mask_box=[290,190,768,526],reason='Strict red threshold misses dark red parts, wheels, saddle and handlebars; approximate visual whole-bicycle union plus 20 pixels. Drainpipe excluded; wall within rectangle is unavoidably editable.')
(p/'evidence/red-bounds.json').write_text(json.dumps(d,indent=2)+'\n')
