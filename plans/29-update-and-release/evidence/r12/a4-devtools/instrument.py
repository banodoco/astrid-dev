from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
helper='''\nconst __probe = (() => { let n=0; const ids=new Map(), guids=new Map(); return { guid: x => { const h=parseInt(require('crypto').createHash('sha256').update(x).digest('hex').slice(0,12),16); if(guids.has(h) && guids.get(h)!==x) require('fs').writeSync(2, 'PROBE {\"event\":\"collision\"}\\n'); else guids.set(h,x); return h; }, id: x => { if(!x)return 0; if(!ids.has(x))ids.set(x,++n); return ids.get(x); }, emit:(event, fields={})=>{ try { require('fs').writeSync(2, 'PROBE ' + JSON.stringify({event,time:Date.now(),...fields}) + '\\n'); } catch {} } }; })();\n'''
s=s.replace('"use strict";\nvar __create', '"use strict";\n'+helper+'var __create',1)
def replace(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError(f'anchor count {s.count(a)}')
 s=s.replace(a,b,1)
replace('        this._requestIdToRequest.set(requestWillBeSentEvent.requestId, request2);', '''        __probe.emit("created", {request:__probe.id(requestWillBeSentEvent.requestId), route:__probe.id(requestPausedEvent?.requestId), guid:__probe.guid(request2.request.guid)});
        this._requestIdToRequest.set(requestWillBeSentEvent.requestId, request2);''')
for kind in ('Failed','Finished'):
 a=f'      _onLoading{kind}(sessionInfo, event) {{\n'
 b=a+f'        __probe.emit("loading-{kind.lower()}", {{request:__probe.id(event.requestId)}});\n'
 replace(a,b)
a='''          await this._session.send("Fetch.failRequest", {
            requestId: this._interceptionId,
            errorReason
          });'''
b='''          __probe.emit("fail-begin", {route:__probe.id(this._interceptionId)});
          try { await this._session.send("Fetch.failRequest", {requestId:this._interceptionId, errorReason});
            __probe.emit("fail-success", {route:__probe.id(this._interceptionId)});
          } catch (error) {
            const text = String(error?.message ?? "");
            __probe.emit(text.includes("Invalid InterceptionId") ? "fail-invalid-id" : text.includes("Invalid state for continueInterceptedRequest") ? "fail-invalid-state" : "fail-other", {route:__probe.id(this._interceptionId)});
            throw error;
          }'''
replace(a,b); p.write_text(s)
