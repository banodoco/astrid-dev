import json,statistics as st,sys,glob
def q(xs,p):
    xs=sorted(xs); i=min(len(xs)-1,int(round(p*(len(xs)-1)))); return xs[i]
def an(paths):
    allw={'p2':[],'g2s':[],'r2s':[],'g2p':[],'s2s':[]}; per=[]
    for p in paths:
        d=json.load(open(p)); w={'p2':[],'g2s':[],'r2s':[],'g2p':[],'s2s':[]}; cold=None; byscen={}
        for s in d['scenarios']:
            if s['name'] in('B5','B10'):
                b=s['burst']; byscen[s['name']]=(b['last_release_to_saved_ms'],b['refusal_count'],b['n_posts']); continue
            for dr in s['drags']:
                g=dr['save_marks_after_saved']['selected']['phases']
                gm=g['gesture-end'][0];pm=g['post-sent'][0];m2=g['200'][0];sb=g['saved-badge'][0]
                row=(m2-pm,sb-gm,dr['release_to_saved_ms'],pm-gm,sb-m2)
                if s['name']=='cold': cold=row; continue
                for k,v in zip(('p2','g2s','r2s','g2p','s2s'),row): w[k].append(v)
                byscen.setdefault(s['name'],[]).append(dr['release_to_saved_ms'])
        for k in w: allw[k]+=w[k]
        per.append((p,w,cold,byscen,d['s0']['navigation_to_writable_ms'],d['refusals'] if not isinstance(d['refusals'],list) else len(d['refusals']),d['failed_drags'] if not isinstance(d['failed_drags'],list) else len(d['failed_drags'])))
    return allw,per
if __name__=='__main__':
    allw,per=an(sys.argv[1:])
    for p,w,cold,bs,nw,rf,fd in per:
        print(p.split('/')[0][:22],'n',len(w['p2']),'med p2 %.2f g2s %.2f r2s %.2f g2p %.2f s2s %.2f'%tuple(st.median(w[k])/1000 for k in ('p2','g2s','r2s','g2p','s2s')),
          'cold p2 %.2f g2s %.2f'%(cold[0]/1000,cold[1]/1000),'writable %.1f'%(nw/1000),'B5',bs['B5'],'B10',bs['B10'],'refusals',rf,'failed',fd)
        print('   scen medians r2s',{k:round(st.median(v)/1000,2) for k,v in bs.items() if isinstance(v,list)})
    print('ALL n',len(allw['p2']))
    for k in allw:
        x=allw[k]; print(k,'median %.2f p90 %.2f max %.2f'%(st.median(x)/1000,q(x,.9)/1000,max(x)/1000))
