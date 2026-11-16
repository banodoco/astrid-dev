#!/usr/bin/env python3
"""Resident ComfyUI floor; graph JSON is an already-prepared API prompt.
Requires aiohttp. Graph can contain literal __LS1_PREFIX__ and __LS1_SEED__ slots.
"""
import argparse, asyncio, copy, hashlib, json, statistics, time, uuid
from pathlib import Path

def stamp(): return time.perf_counter_ns()
def ms(a,b): return (b-a)/1e6

def fill(value, prefix, seed):
    if isinstance(value,dict): return {k:fill(v,prefix,seed) for k,v in value.items()}
    if isinstance(value,list): return [fill(v,prefix,seed) for v in value]
    if value=='__LS1_PREFIX__': return prefix
    if value=='__LS1_SEED__': return seed
    return value

async def main(a):
    import aiohttp
    graph=json.loads(Path(a.graph).read_text()); client_id=str(uuid.uuid4()); rows=[]
    timeout=aiohttp.ClientTimeout(total=a.timeout)
    async with aiohttp.ClientSession(timeout=timeout,connector=aiohttp.TCPConnector(limit=1)) as http, aiohttp.ClientSession(timeout=timeout) as events:
        # Establish HTTP before first POST as well as the WS; HTTP pool holds one connection.
        async with http.get(a.url+'/system_stats') as r: r.raise_for_status(); await r.read()
        async with events.ws_connect(a.url.replace('http://','ws://').replace('https://','wss://')+'/ws',params={'clientId':client_id}) as ws:
            queue=asyncio.Queue()
            async def receive():
                async for message in ws:
                    await queue.put((stamp(),message))
                await queue.put((stamp(),None))
            reader=asyncio.create_task(receive())
            for i in range(a.samples):
                start=stamp(); prompt=fill(graph,'ls1_'+uuid.uuid4().hex,i); filled=stamp()
                async with http.post(a.url+'/prompt',json={'prompt':prompt,'client_id':client_id}) as r:
                    data=await r.json(); r.raise_for_status()
                accepted=stamp(); pid=data['prompt_id']; execution_start=None; success=None
                while True:
                    t,msg=await asyncio.wait_for(queue.get(), timeout=a.timeout)
                    if msg is None or msg.type!=aiohttp.WSMsgType.TEXT: raise RuntimeError('websocket closed or unexpected message')
                    event=json.loads(msg.data); typ=event.get('type'); d=event.get('data',{})
                    if d.get('prompt_id')!=pid: continue
                    if typ=='execution_start': execution_start=t
                    if typ=='execution_success': success=t
                    if typ in ('execution_error','execution_interrupted'): raise RuntimeError(str(event))
                    if typ=='executing' and d.get('node') is None: ready=t; break
                if execution_start is None or success is None: raise RuntimeError('missing execution_start or execution_success; cannot calculate timing')
                async with http.get(a.url+'/history/'+pid) as r: r.raise_for_status(); hist=await r.json()
                fetched_history=stamp(); entry=hist[pid]; outputs=[]
                for node in entry.get('outputs',{}).values():
                    for category in ('images','gifs','videos','audio'):
                        for item in node.get(category,[]): outputs.append(item)
                if not outputs: raise RuntimeError('no output files in history')
                files=[]
                for item in outputs:
                    h=hashlib.sha256(); size=0
                    async with http.get(a.url+'/view',params={k:item.get(k,'') for k in ('filename','subfolder','type')}) as r:
                        r.raise_for_status()
                        async for chunk in r.content.iter_chunked(65536): h.update(chunk); size+=len(chunk)
                    files.append({'sha256':h.hexdigest(),'bytes':size,'filename':item['filename']})
                end=stamp()
                rows.append({'sample':i,'prompt_id':pid,'fill_ms':ms(start,filled),'post_validation_ms':ms(filled,accepted),'post_response_to_start_observed_ms':ms(accepted,execution_start),'execution_ms':ms(execution_start,success),'history_ready_after_success_ms':ms(success,ready),'history_fetch_ms':ms(ready,fetched_history),'output_fetch_hash_ms':ms(fetched_history,end),'wall_ms':ms(start,end),'outputs':files})
            reader.cancel()
    fields=[k for k in rows[0] if k.endswith('_ms')]; summary={k:{'median':statistics.median(r[k] for r in rows),'max':max(r[k] for r in rows)} for k in fields}
    Path(a.output).write_text(json.dumps({'url':a.url,'samples':a.samples,'summary_ms':summary,'records':rows},indent=2)+'\n'); print(json.dumps(summary,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--url',default='http://127.0.0.1:8188'); p.add_argument('--graph',required=True); p.add_argument('--output',required=True); p.add_argument('--samples',type=int,default=20); p.add_argument('--timeout',type=float,default=60); asyncio.run(main(p.parse_args()))
