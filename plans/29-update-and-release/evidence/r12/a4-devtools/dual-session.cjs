const {createServer}=require('http');const crypto=require('crypto');const {chromium}=require(process.env.TASK_PROBE_CORE);
(async()=>{
 const server=createServer((req,res)=>{res.writeHead(200,{'content-type':req.url.startsWith('/api/')?'application/json':'text/html'});res.end(req.url.startsWith('/api/')?'{}':'<html><script>setInterval(()=>fetch("/api/background").catch(()=>{}),1)</script></html>')});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin=`http://127.0.0.1:${server.address().port}`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.TASK_PROBE_BROWSER});
 try{const page=await browser.newPage();const cdp=await page.context().newCDPSession(page);await cdp.send('Network.enable',{maxTotalBufferSize:10_000_000,maxResourceBufferSize:1_000_000,enableDurableMessages:true});
 const hashes=new Map();for(const event of ['requestWillBeSent','loadingFailed','loadingFinished'])cdp.on(`Network.${event}`,data=>{const network=parseInt(crypto.createHash('sha256').update(data.requestId).digest('hex').slice(0,12),16);if(hashes.has(network)&&hashes.get(network)!==data.requestId)console.error('DUAL '+JSON.stringify({event:'collision'}));else hashes.set(network,data.requestId);console.error('DUAL '+JSON.stringify({event,network}))});
 await page.route('**/api/**',route=>route.abort());await page.goto(origin);
 for(let i=0;i<200;i++)await page.reload({waitUntil:'commit'});
 await page.close();console.log('RELOADS',200)}finally{await browser.close();server.close()}
})().catch(()=>{console.log('PROBE_FAILED');process.exitCode=1});
