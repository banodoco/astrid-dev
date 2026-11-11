const {createServer}=require('http'); const {chromium}=require(process.env.TASK_PROBE_CORE);
(async()=>{
 let reached=false;
 const server=createServer((req,res)=>{if(req.url==='/api/leaving')reached=true;res.writeHead(200,{'content-type':'text/html'});res.end('<html><script>addEventListener("pagehide",()=>{fetch("/api/leaving",{keepalive:true}).catch(()=>{})})</script></html>')});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.TASK_PROBE_BROWSER});
 try{const page=await browser.newPage();await page.goto(origin);let ready,held;let terminal=false;
 const waiting=new Promise(resolve=>ready=resolve);page.on('requestfailed',r=>{if(r.url().endsWith('/api/leaving'))terminal=true});page.on('requestfinished',r=>{if(r.url().endsWith('/api/leaving'))terminal=true});
 await page.route('**/api/leaving',route=>{held=route;ready()});
 await page.goto(origin+'/next',{waitUntil:'commit'});await waiting;await held.abort();await new Promise(resolve=>setTimeout(resolve,100));
 console.log('PAGEHIDE_GATE_ABORT_RETURNED','TERMINAL',terminal,'SERVER',reached);await page.close();
 }finally{await browser.close();server.close()}
})().catch(()=>process.exitCode=1);
