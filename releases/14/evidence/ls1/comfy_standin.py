#!/usr/bin/env python3
"""Minimal artificial transport fixture; it does not measure ComfyUI."""
import asyncio, json, uuid
from aiohttp import web
clients={}; histories={}
async def stats(r): return web.json_response({})
async def ws(r):
    sock=web.WebSocketResponse(); await sock.prepare(r); clients[r.query['clientId']]=sock
    async for _ in sock: pass
    return sock
async def prompt(r):
    body=await r.json(); pid=str(uuid.uuid4()); sock=clients[body['client_id']]
    async def execute():
        await asyncio.sleep(0.001)
        for kind,data in [('execution_start',{}),('execution_success',{})]: await sock.send_json({'type':kind,'data':{'prompt_id':pid,**data}})
        histories[pid]={'outputs':{'1':{'images':[{'filename':'test.bin','subfolder':'','type':'output'}]}}}
        await sock.send_json({'type':'executing','data':{'prompt_id':pid,'node':None}})
    asyncio.create_task(execute()); return web.json_response({'prompt_id':pid})
async def history(r): return web.json_response({r.match_info['pid']:histories[r.match_info['pid']]})
async def view(r): return web.Response(body=b'ls1 stand-in output')
app=web.Application(); app.add_routes([web.get('/system_stats',stats),web.get('/ws',ws),web.post('/prompt',prompt),web.get('/history/{pid}',history),web.get('/view',view)])
if __name__=='__main__': web.run_app(app,host='127.0.0.1',port=18188,print=None)
