#!/usr/bin/env python3
"""One end-to-end HTTP Runtime + resident Comfy session experiment.
Run from Runtime checkout, PYTHONPATH=.:tests with Runtime and aiohttp installed.
"""
import argparse, asyncio, base64, hashlib, json, statistics, tempfile, time, uuid
from pathlib import Path
import aiohttp
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.store import RealmStore
from tests.runtime_credentials import provision_executor_token
from http_helpers import Api
from comfy_floor import fill

def now(): return time.perf_counter_ns()
def elapsed(a,b): return (b-a)/1e6
def digest(b): return 'sha256:'+hashlib.sha256(b).hexdigest()

async def main(a):
    graph=json.loads(Path(a.graph).read_text()); cap='ls1.smoke'; executor='ls1-worker'; cd=digest(cap.encode()); results=[]; admission=asyncio.Lock()
    with tempfile.TemporaryDirectory(prefix='ls1-integrated-') as tmp:
        root=Path(tmp)/'realm'; RealmStore.initialize(root).close(); daemon=RuntimeDaemon(root,support_root=Path(tmp)/'support').start()
        try:
            owner=Api(daemon.endpoint,daemon.token); owner.request('POST','/v1/capabilities',{'capability_id':cap,'definition_digest':cd,'required_resource_keys':[]}); owner.register_executor(executor,[cap],max_concurrency=a.callers); owner.create_project('ls1','LS1'); token=provision_executor_token(daemon,executor); epoch=owner.health()['runtime_epoch']
            async def caller(slot):
                owner=Api(daemon.endpoint,daemon.token); worker=Api(daemon.endpoint,token); client=str(uuid.uuid4()); timeout=aiohttp.ClientTimeout(total=a.timeout)
                async with aiohttp.ClientSession(timeout=timeout,connector=aiohttp.TCPConnector(limit=1)) as http, aiohttp.ClientSession(timeout=timeout) as events:
                    async with http.get(a.url+'/system_stats') as r: r.raise_for_status(); await r.read()
                    async with events.ws_connect(a.url.replace('http://','ws://').replace('https://','wss://')+'/ws',params={'clientId':client}) as ws:
                        q=asyncio.Queue()
                        async def read_events():
                            async for msg in ws: await q.put((now(),msg))
                            await q.put((now(),None))
                        reader=asyncio.create_task(read_events())
                        try:
                            for i in range(slot,a.samples,a.callers):
                                key=str(uuid.uuid4()); start=now()
                                # Lock preserves task ownership under competing claims; lock wait remains in caller wall time.
                                async with admission:
                                    admission_enter=now()
                                    task=await asyncio.to_thread(owner.create_task,cap,{},project='ls1',idempotency_key='task-'+key); created=now()
                                    attempt=await asyncio.to_thread(worker.request,'POST','/v1/tasks/claim',{'executor_id':executor,'capability_ids':[cap],'runtime_epoch':epoch},headers={'Idempotency-Key':'claim-'+key}); claimed=now()
                                    assert task['task_id']==attempt['task_id']
                                prompt=fill(graph,'ls1_'+uuid.uuid4().hex,i); filled=now()
                                async with http.post(a.url+'/prompt',json={'prompt':prompt,'client_id':client}) as r: data=await r.json(); r.raise_for_status()
                                accepted=now(); pid=data['prompt_id']; execution_start=success=None
                                while True:
                                    t,msg=await asyncio.wait_for(q.get(),a.timeout)
                                    if msg is None or msg.type!=aiohttp.WSMsgType.TEXT: raise RuntimeError('websocket ended')
                                    event=json.loads(msg.data); kind=event.get('type'); d=event.get('data',{})
                                    if d.get('prompt_id')!=pid: continue
                                    if kind=='execution_start': execution_start=t
                                    if kind=='execution_success': success=t
                                    if kind in ('execution_error','execution_interrupted'): raise RuntimeError(str(event))
                                    if kind=='executing' and d.get('node') is None: ready=t; break
                                if execution_start is None or success is None: raise RuntimeError('missing execution events')
                                async with http.get(a.url+'/history/'+pid) as r: r.raise_for_status(); history=await r.json()
                                history_done=now(); outputs=[]
                                for node in history[pid].get('outputs',{}).values():
                                    for category in ('images','gifs','videos','audio'): outputs.extend(node.get(category,[]))
                                if len(outputs)!=1: raise RuntimeError(f'expected one output, got {len(outputs)}')
                                item=outputs[0]; h=hashlib.sha256(); chunks=[]
                                async with http.get(a.url+'/view',params={k:item.get(k,'') for k in ('filename','subfolder','type')}) as r:
                                    r.raise_for_status()
                                    async for chunk in r.content.iter_chunked(65536): h.update(chunk); chunks.append(chunk)
                                payload=b''.join(chunks); dg='sha256:'+h.hexdigest(); fetched=now()
                                output={'kind':'object','name':'result','filename':item['filename'],'output_port':'result','digest':dg,'media_type':a.media_type,'size':len(payload),'data_base64':base64.b64encode(payload).decode(),'role':'result','is_primary':True,'durability':'durable','producer':{'capability_id':cap,'view':'ls1'}}; prepared=now()
                                await asyncio.to_thread(worker.request,'POST',f"/v1/attempts/{attempt['attempt_id']}/settle",{'lease_id':attempt['lease_id'],'fence':attempt['fence'],'runtime_epoch':epoch,'outputs':[output]},headers={'Idempotency-Key':'settle-'+key}); settled=now()
                                managed=await asyncio.to_thread(owner.request,'GET',f"/v1/tasks/{attempt['task_id']}/managed-outputs"); stored=(await asyncio.to_thread(owner.read_object,dg))[0]; finished=await asyncio.to_thread(owner.task,attempt['task_id'])
                                assert stored==payload and dg in json.dumps(managed) and 'succeed' in json.dumps(finished).lower()
                                results.append({'sample':i,'caller':slot,'bytes':len(payload),'digest':dg,'admission_wait_ms':elapsed(start,admission_enter),'create_ms':elapsed(admission_enter,created),'claim_ms':elapsed(created,claimed),'fill_ms':elapsed(claimed,filled),'post_validation_ms':elapsed(filled,accepted),'post_response_to_start_observed_ms':elapsed(accepted,execution_start),'execution_observed_ms':elapsed(execution_start,success),'history_ready_after_success_ms':elapsed(success,ready),'history_fetch_ms':elapsed(ready,history_done),'fetch_hash_ms':elapsed(history_done,fetched),'descriptor_ms':elapsed(fetched,prepared),'settle_ms':elapsed(prepared,settled),'caller_wall_ms':elapsed(start,settled)})
                        finally: reader.cancel()
            await asyncio.gather(*(caller(i) for i in range(a.callers)))
            results.sort(key=lambda x:x['sample']); fields=[k for k in results[0] if k.endswith('_ms')]; summary={k:{'median':statistics.median(x[k] for x in results),'max':max(x[k] for x in results)} for k in fields}; Path(a.output).write_text(json.dumps({'samples':a.samples,'callers':a.callers,'url':a.url,'summary_ms':summary,'records':results},indent=2)+'\n'); print(json.dumps(summary,indent=2))
        finally: daemon.stop()
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--url',default='http://127.0.0.1:8188'); p.add_argument('--graph',required=True); p.add_argument('--output',required=True); p.add_argument('--samples',type=int,default=20); p.add_argument('--callers',type=int,choices=(1,2),default=1); p.add_argument('--timeout',type=float,default=60); p.add_argument('--media-type',default='image/png'); asyncio.run(main(p.parse_args()))
