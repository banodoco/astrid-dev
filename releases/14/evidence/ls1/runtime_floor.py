#!/usr/bin/env python3
"""Measure unchanged Runtime HTTP lifecycle and durable inline output on an isolated realm.
Run from a Runtime checkout: PYTHONPATH=.:tests <venv>/bin/python <this file>.
"""
import argparse, base64, concurrent.futures, hashlib, json, os, statistics, struct, tempfile, time, uuid, zlib
from pathlib import Path
from runtime_protocol.daemon import RuntimeDaemon
from runtime_protocol.store import RealmStore
from tests.runtime_credentials import provision_executor_token
from http_helpers import Api

def digest(b): return 'sha256:' + hashlib.sha256(b).hexdigest()
def chunk(kind, data): return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
def make_payload(size, i, video):
    if video:
        source=Path(video).read_bytes(); remaining=size-len(source)
        if remaining < 16: raise ValueError('video base must leave 16 bytes for free box')
        return source+struct.pack('>I4s',remaining,b'free')+i.to_bytes(8,'big')+bytes(remaining-16)
    # A valid 1x1 PNG with an ancillary padding chunk; vary its contents per job.
    base=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b'\x00\x00\x00\x00'))
    pad=size-len(base)-12-12
    if pad<8: raise ValueError('size too small')
    return base+chunk(b'npAD',i.to_bytes(8,'big')+bytes(pad-8))+chunk(b'IEND',b'')
def now(): return time.perf_counter_ns()
def ms(a,b): return (b-a)/1e6

def main():
    p=argparse.ArgumentParser(); p.add_argument('--samples',type=int,default=20); p.add_argument('--bytes',type=int,default=1048576); p.add_argument('--callers',type=int,choices=(1,2),default=1); p.add_argument('--video-base'); p.add_argument('--output',required=True); a=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='ls1-runtime-') as tmp:
        root=Path(tmp)/'realm'; RealmStore.initialize(root).close(); daemon=RuntimeDaemon(root,support_root=Path(tmp)/'support').start()
        try:
            owner=Api(daemon.endpoint,daemon.token); cap='ls1.smoke'; cd=digest(cap.encode()); executor='ls1-worker'
            owner.request('POST','/v1/capabilities',{'capability_id':cap,'definition_digest':cd,'required_resource_keys':[]})
            owner.register_executor(executor,[cap],max_concurrency=a.callers)
            owner.create_project('ls1','LS1'); project='ls1'; worker_token=provision_executor_token(daemon,executor); epoch=owner.health()['runtime_epoch']
            # Distinct payloads prevent deduplication from disguising publication work.
            def run(i):
                client=Api(daemon.endpoint,daemon.token); worker=Api(daemon.endpoint,worker_token); key=str(uuid.uuid4()); payload=make_payload(a.bytes,i,a.video_base); dg=digest(payload)
                t0=now(); task=client.create_task(cap,{},project=project,idempotency_key='task-'+key); t1=now()
                attempt=worker.request('POST','/v1/tasks/claim',{'executor_id':executor,'capability_ids':[cap],'runtime_epoch':epoch},headers={'Idempotency-Key':'claim-'+key}); t2=now()
                # Concurrent callers may claim each other's queued task; each claimed task is settled once.
                output={'kind':'object','name':'result','filename':'result.mp4' if a.video_base else 'result.png','output_port':'result','digest':dg,'media_type':'video/mp4' if a.video_base else 'image/png','size':len(payload),'data_base64':base64.b64encode(payload).decode(),'role':'result','is_primary':True,'durability':'durable','producer':{'capability_id':cap,'view':'ls1'}}
                t3=now(); worker.request('POST',f"/v1/attempts/{attempt['attempt_id']}/settle",{'lease_id':attempt['lease_id'],'fence':attempt['fence'],'runtime_epoch':epoch,'outputs':[output]},headers={'Idempotency-Key':'settle-'+key}); t4=now()
                managed=client.request('GET',f"/v1/tasks/{attempt['task_id']}/managed-outputs"); stored=client.read_object(dg)[0]; task_after=client.task(attempt['task_id']); assert stored==payload and dg in json.dumps(managed) and 'succeed' in json.dumps(task_after).lower(), (managed,task_after)
                return {'sample':i,'create_ms':ms(t0,t1),'claim_ms':ms(t1,t2),'prepare_descriptor_ms':ms(t2,t3),'settle_ms':ms(t3,t4),'lifecycle_ms':ms(t0,t4),'verified_bytes':len(stored),'digest':dg}
            with concurrent.futures.ThreadPoolExecutor(max_workers=a.callers) as pool: rows=list(pool.map(run,range(a.samples)))
            fields=['create_ms','claim_ms','prepare_descriptor_ms','settle_ms','lifecycle_ms']; summary={k:{'median':statistics.median(r[k] for r in rows),'max':max(r[k] for r in rows)} for k in fields}
            result={'kind':'unchanged-runtime-http','samples':a.samples,'callers':a.callers,'bytes':a.bytes,'payload':'mp4 with free-box padding' if a.video_base else 'PNG with ancillary padding','summary_ms':summary,'records':rows}; Path(a.output).write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(summary,indent=2))
        finally: daemon.stop()
if __name__=='__main__': main()
