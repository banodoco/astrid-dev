const { createServer } = require('http');
const { chromium } = require(process.env.TASK_PROBE_CORE);
(async () => {
 let release; const hold = new Promise(resolve => release=resolve); let arrived=false;
 const server=createServer(async (req,res) => {
   if(req.url==='/api/stream') {arrived=true;res.writeHead(200,{'content-type':'application/json'});res.write('{"body":"');await hold;res.end('complete"}');return;}
   res.writeHead(200,{'content-type':'text/html'});res.end('<html></html>');
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.TASK_PROBE_BROWSER});
 try {
  const page=await browser.newPage();await page.route('**/*',r=>r.fallback());await page.goto(origin);
  const started=page.waitForResponse('**/api/stream');await page.evaluate(()=>{void fetch('/api/stream').catch(()=>{});});const response=await started;
  const body=response.text().then(()=> 'read',()=> 'unavailable');
  await page.goto(origin+'/next',{waitUntil:'commit'});release();
  console.log('INTERRUPTED_BODY',await body,'ARRIVED',arrived);
  await page.close();
  const page2=await browser.newPage();await page2.goto(origin);
  let held, ready; const routeReady=new Promise(resolve=>ready=resolve);
  await page2.route('**/api/**',route=>{held=route;ready()});
  await page2.evaluate(()=>{void fetch('/api/held').catch(()=>{});});await routeReady;
  await page2.goto(origin+'/next',{waitUntil:'commit'});
  const result=await held.abort().then(()=>'resolved',()=> 'rejected');
  console.log('STALE_ABORT',result);
  await page2.close();
 } finally {release();await browser.close();server.close();}
})().catch(()=>{process.exitCode=1});
