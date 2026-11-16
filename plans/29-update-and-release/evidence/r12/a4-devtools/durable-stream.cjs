const {createServer} = require('http');
const {chromium} = require(process.env.TASK_PROBE_CORE);
const assert = require('assert/strict');
(async()=>{
 let resumePartial;const waitPartial=new Promise(resolve=>resumePartial=resolve);let pagehideReached=false;
 const server=createServer(async(req,res)=>{
   if(req.url==='/api/complete'){res.writeHead(200,{'content-type':'application/json'});res.end('{"body":"complete-sentinel"}');return;}
   if(req.url==='/api/partial'){res.writeHead(200,{'content-type':'application/json'});res.write('{"body":"partial-');await waitPartial;res.end('sentinel"}');return;}
   if(req.url==='/api/pagehide'){pagehideReached=true;res.writeHead(200,{'content-type':'application/json'});res.end('{}');return;}
   res.writeHead(200,{'content-type':'text/html'});res.end('<html>ok</html>');
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.TASK_PROBE_BROWSER});
 try{
  const page=await browser.newPage(); const cdp=await page.context().newCDPSession(page);
  await cdp.send('Network.enable',{maxTotalBufferSize:10_000_000,maxResourceBufferSize:1_000_000,enableDurableMessages:true});
  await page.route('**/*',route=>route.fallback());
  const ids=new Map(),chunks=new Map(),buffered=new Map(),terminal=new Map(),streams=new Map(),order=[];
  cdp.on('Network.requestWillBeSent',e=>{const path=new URL(e.request.url).pathname;ids.set(e.requestId,path);if(path==='/api/pagehide')order.push('pagehide-request')});
  cdp.on('Network.responseReceived',e=>{
   const path=ids.get(e.requestId); if(path==='/next' && e.type==='Document')order.push('navigation-response');
   if(path==='/api/complete'||path==='/api/partial'){
    streams.set(path,cdp.send('Network.streamResourceContent',{requestId:e.requestId}).then(result=>{buffered.set(path,Buffer.from(result.bufferedData,'base64'));return true},()=>false));
   }
  });
  cdp.on('Network.dataReceived',e=>{const path=ids.get(e.requestId);if(e.data){const list=chunks.get(path)??[];list.push(Buffer.from(e.data,'base64'));chunks.set(path,list)}});
  for(const name of ['loadingFinished','loadingFailed'])cdp.on(`Network.${name}`,e=>{const path=ids.get(e.requestId);if(path)terminal.set(path,name)});
  await page.goto(origin);
  await page.evaluate(()=>addEventListener('pagehide',()=>{void fetch('/api/pagehide',{keepalive:true}).catch(()=>{})}));
  const complete=page.waitForResponse('**/api/complete');await page.evaluate(()=>{void fetch('/api/complete').catch(()=>{})});const response=await complete;await response.finished();
  await streams.get('/api/complete');
  const partial=page.waitForResponse('**/api/partial');await page.evaluate(()=>{void fetch('/api/partial').catch(()=>{})});await partial;
  await streams.get('/api/partial');
  await page.goto(origin+'/next',{waitUntil:'commit'});resumePartial();
  for(let i=0;i<60&&!pagehideReached;i++) await new Promise(resolve=>setTimeout(resolve,50));
  const body=path=>Buffer.concat([buffered.get(path)??Buffer.alloc(0),...(chunks.get(path)??[])]).toString('utf8');
  const completedId=[...ids].find(([,path])=>path==='/api/complete')?.[0];
  const durable=await cdp.send('Network.getResponseBody',{requestId:completedId}).then(r=>Buffer.from(r.body,r.base64Encoded?'base64':'utf8').toString('utf8'),()=>null);
  const result={completeBodyDurableAfterNavigation:durable==='{\"body\":\"complete-sentinel\"}',completeBodyCaptured:body('/api/complete')==='{"body":"complete-sentinel"}',completeTerminal:terminal.get('/api/complete')??'missing',partialBodyCaptured:body('/api/partial')==='{"body":"partial-sentinel"}',partialTerminal:terminal.get('/api/partial')??'missing',pagehideAfterNavigationResponse:order.indexOf('navigation-response')>=0&&order.indexOf('pagehide-request')>order.indexOf('navigation-response'),pagehideReachedServer:pagehideReached};
  console.log(JSON.stringify(result));
  assert.equal(result.completeBodyDurableAfterNavigation,true);assert.equal(result.completeBodyCaptured,true);assert.equal(result.completeTerminal,'loadingFinished');assert.equal(result.partialBodyCaptured,false);assert.equal(result.pagehideAfterNavigationResponse,true);assert.equal(result.pagehideReachedServer,true);
 }finally{resumePartial();await browser.close();server.close();}
})().catch(()=>{console.log('PROBE_FAILED');process.exitCode=1});
