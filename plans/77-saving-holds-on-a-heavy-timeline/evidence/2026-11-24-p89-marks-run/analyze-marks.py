import json,statistics as st,sys
d=json.load(open(sys.argv[1]))
warm=[];cold=None
for s in d['scenarios']:
    if s['name'] in('B5','B10'):continue
    for dr in s['drags']:
        g=dr['save_marks_after_saved']; sel=g['selected']['correlation']
        ph={m['name'].split('.',3)[3]:m['t'] for m in g['raw'] if m['name'].split('.',3)[2]==sel}
        if s['name']=='cold': cold=ph
        else: warm.append((ph,dr))
print('warm saves',len(warm))
print('median offset from gesture-end (ms): phase  median min max')
for k in sorted(warm[0][0],key=lambda k:st.median([p[k]-p['gesture-end'] for p,_ in warm])):
    v=[p[k]-p['gesture-end'] for p,_ in warm]; print('%-22s %8.1f %8.1f %8.1f'%(k,st.median(v),min(v),max(v)))
print('stage medians (ms): from -> to  median min max')
for a,b in [('debounce-armed','debounce-fired'),('draft-write-queued','draft-write-start'),('draft-write-start','draft-write-ready'),('capture-start','capture-returned'),('capture-returned','capture-settled'),('debounce-fired','attempt-build-start'),('attempt-build-start','attempt-build-end'),('capture-wait-start','capture-wait-end'),('capture-wait-end','post-sent'),('debounce-fired','post-sent'),('gesture-end','post-sent'),('post-sent','200'),('accepted-decode-start','accepted-decode-end'),('200','hook-ack-start'),('hook-ack-start','hook-status-update'),('hook-status-update','saved-badge'),('200','saved-badge'),('gesture-end','saved-badge')]:
    v=[p[b]-p[a] for p,_ in warm]; print('%-22s -> %-22s %8.1f %8.1f %8.1f'%(a,b,st.median(v),min(v),max(v)))
print('driver release-to-saved median %.2f s'%(st.median([dr['release_to_saved_ms'] for _,dr in warm])/1000))
for s in d['scenarios']:
    if s['name'] in('B5','B10'): print(s['name'],'last edit to Saved %.1f s, refusals %d'%(s['burst']['last_release_to_saved_ms']/1000,s['burst']['refusal_count']))
print('cold offsets',{k:round(v-cold['gesture-end'],1) for k,v in sorted(cold.items(),key=lambda x:x[1])})
