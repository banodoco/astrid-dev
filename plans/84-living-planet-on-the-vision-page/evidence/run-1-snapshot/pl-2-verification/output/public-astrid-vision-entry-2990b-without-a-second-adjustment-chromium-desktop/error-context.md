# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-entry.spec.ts >> iPad returns from scrolled Vision at the top without a second adjustment
- Location: tests/e2e/public-astrid-vision-entry.spec.ts:208:1

# Error details

```
Error: Timeout 5000ms exceeded while waiting on the predicate
```

# Test source

```ts
  125 |     const observer = new MutationObserver(read);
  126 |     observer.observe(document.querySelector('.astrid-vision-hero-copy')!, { childList: true, attributes: true, subtree: true });
  127 |     let count = 0;
  128 |     const sample = () => { read(); if (++count < 120) requestAnimationFrame(sample); else observer.disconnect(); };
  129 |     requestAnimationFrame(sample);
  130 |   });
  131 |   release();
  132 |   await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
  133 |   const frames = await page.locator('#astrid-vision-title').evaluate(node => new Promise<{ height: number; width: number; font: string; transform: string; parentWidth: number }[]>(resolve => {
  134 |     const samples: { height: number; width: number; font: string; transform: string; parentWidth: number }[] = [];
  135 |     const sample = () => {
  136 |       const style = getComputedStyle(node);
  137 |       samples.push({ height: (node as HTMLElement).offsetHeight, width: (node as HTMLElement).offsetWidth,
  138 |         font: style.font, transform: style.transform, parentWidth: node.parentElement!.getBoundingClientRect().width });
  139 |       if (samples.length < 72) requestAnimationFrame(sample); else resolve(samples);
  140 |     };
  141 |     sample();
  142 |   }));
  143 |   const arrival = await page.evaluate(() => (window as unknown as { arrival: { height: number; width: number; text: string | null }[] }).arrival);
  144 |   record(`home-vision-entry-${info.project.name}`, { source: feed.source, requestsBeforeRelease, frames, arrival });
  145 |   expect.soft(arrival.length).toBeGreaterThan(0);
  146 |   expect.soft(new Set(arrival.map(frame => `${frame.height}/${frame.width}`)).size).toBe(1);
  147 |   expect.soft(requestsBeforeRelease).toBe(1);
  148 |   expect.soft(new Set(frames.map(frame => `${frame.height}/${frame.width}/${frame.font}`)).size).toBe(1);
  149 |   await page.getByRole('link', { name: 'Astrid home', exact: true }).click();
  150 |   await expect(link).toBeVisible();
  151 |   await link.click();
  152 |   await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
  153 |   await expect(page.getByRole('status', { name: "Loading Astrid's vision" })).toHaveCount(0);
  154 | });
  155 | 
  156 | // Use tablet emulation explicitly rather than resizing a 3x phone context.
  157 | test('iPad single-screen Home rejects document overflow and remains fitted', async ({ browser, baseURL, request }, info) => {
  158 |   const response = await request.get(FEED); expect(response.ok()).toBe(true);
  159 |   const feed = await response.json() as PublicVisionContent;
  160 |   const context = await browser.newContext({ baseURL, viewport: { width: 820, height: 1180 },
  161 |     screen: { width: 820, height: 1180 }, isMobile: true, hasTouch: true,
  162 |     deviceScaleFactor: 1, reducedMotion: 'reduce' });
  163 |   try {
  164 |     const page = await context.newPage();
  165 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  166 |     await page.goto('/home', { waitUntil: 'domcontentloaded' });
  167 |     const home = page.locator('.astrid-public-site');
  168 |     // Cold Vite compilation is not layout readiness. Keep geometry assertions
  169 |     // strict, but wait explicitly for the application to mount first.
  170 |     await expect(home).toBeVisible({ timeout: 30000 });
  171 |     await page.evaluate(() => document.fonts.ready);
  172 |     const samples = [];
  173 |     for (const viewport of [{ width: 820, height: 1180 }, { width: 820, height: 1024 },
  174 |       { width: 834, height: 1194 }, { width: 768, height: 1024 }, { width: 1024, height: 1366 }]) {
  175 |       await page.setViewportSize(viewport);
  176 |       for (const audience of ['App', 'Agent']) {
  177 |         await home.getByRole('button', { name: audience, exact: true }).click();
  178 |         await expect(home).toHaveAttribute('data-audience', audience.toLowerCase());
  179 |         await expect.poll(() => page.evaluate(() => getComputedStyle(document.documentElement).overflowY)).toBe('clip');
  180 |         await page.evaluate(() => window.scrollTo({ left: 0, top: 3000, behavior: 'instant' }));
  181 |         await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
  182 |         const geometry = await home.evaluate(node => ({
  183 |           height: innerHeight, y: scrollY, scrollHeight: document.documentElement.scrollHeight,
  184 |           bodyHeight: document.body.scrollHeight, home: node.getBoundingClientRect().toJSON(),
  185 |           controls: ['.astrid-brand', 'h1', '.astrid-audience-switch', '.astrid-hero-actions'].map(selector => {
  186 |             const box = node.querySelector(selector)!.getBoundingClientRect();
  187 |             return { selector, top: box.top, bottom: box.bottom, left: box.left, right: box.right };
  188 |           }),
  189 |         }));
  190 |         expect(geometry.scrollHeight).toBeLessThanOrEqual(viewport.height + 1);
  191 |         expect(geometry.bodyHeight).toBeLessThanOrEqual(viewport.height + 1);
  192 |         expect(geometry.home.y).toBe(0);
  193 |         for (const box of geometry.controls) {
  194 |           expect(box.top).toBeGreaterThanOrEqual(-1);
  195 |           expect(box.bottom).toBeLessThanOrEqual(viewport.height + 1);
  196 |           expect(box.left).toBeGreaterThanOrEqual(-1);
  197 |           expect(box.right).toBeLessThanOrEqual(viewport.width + 1);
  198 |         }
  199 |         samples.push({ viewport, audience, ...geometry });
  200 |       }
  201 |     }
  202 |     record(`ipad-home-fit-${info.project.name}`, { source: feed.source, samples });
  203 |     await page.setViewportSize({ width: 820, height: 1180 });
  204 |     await page.screenshot({ path: `${folder}/ipad-home-fit-${info.project.name}.png` });
  205 |   } finally { await context.close(); }
  206 | });
  207 | 
  208 | test('iPad returns from scrolled Vision at the top without a second adjustment', async ({ browser, baseURL, request }, info) => {
  209 |   const response = await request.get(FEED); expect(response.ok()).toBe(true);
  210 |   const feed = await response.json() as PublicVisionContent;
  211 |   const context = await browser.newContext({ baseURL, viewport: { width: 820, height: 1180 },
  212 |     screen: { width: 820, height: 1180 }, isMobile: true, hasTouch: true,
  213 |     deviceScaleFactor: 1, reducedMotion: 'no-preference' });
  214 |   try {
  215 |     const page = await context.newPage();
  216 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  217 |     await page.goto('/home', { waitUntil: 'domcontentloaded' });
  218 |     const home = page.locator('.astrid-public-site');
  219 |     await expect(home).toBeVisible({ timeout: 30000 });
  220 |     const traces = [];
  221 |     for (const height of [1180, 1024, 1180]) {
  222 |       await page.setViewportSize({ width: 820, height });
  223 |       await home.getByRole('link', { name: 'Vision', exact: true }).click();
  224 |       await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
> 225 |       await expect.poll(() => page.evaluate(() => getComputedStyle(document.documentElement).overflowY)).not.toBe('clip');
      |                                                                                                              ^ Error: Timeout 5000ms exceeded while waiting on the predicate
  226 |       await page.evaluate(() => window.scrollTo({ top: 900, behavior: 'instant' }));
  227 |       await expect.poll(() => page.evaluate(() => window.scrollY)).toBeGreaterThanOrEqual(899);
  228 |       await page.getByRole('link', { name: 'Astrid home', exact: true }).click();
  229 |       await expect(page.locator('.astrid-vision')).toHaveCount(0);
  230 |       await expect(home).toHaveAttribute('data-astrid-lifecycle', 'active');
  231 |       const frames = await page.evaluate(() => new Promise<{ y: number; top: number; overflow: number }[]>(resolve => {
  232 |         const samples: { y: number; top: number; overflow: number }[] = [];
  233 |         const sample = () => {
  234 |           samples.push({ y: scrollY, top: document.querySelector('.astrid-public-site')!.getBoundingClientRect().top,
  235 |             overflow: document.documentElement.scrollHeight - innerHeight });
  236 |           if (samples.length < 16) requestAnimationFrame(sample); else resolve(samples);
  237 |         };
  238 |         sample();
  239 |       }));
  240 |       expect(frames.every(frame => frame.y === 0 && Math.abs(frame.top) < 1 && frame.overflow <= 1)).toBe(true);
  241 |       traces.push({ height, frames });
  242 |     }
  243 |     // A direct Vision entry has no previous Home scroll or retained DOM.
  244 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  245 |     await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
  246 |     await page.evaluate(() => window.scrollTo({ top: 900, behavior: 'instant' }));
  247 |     await page.getByRole('link', { name: 'Astrid home', exact: true }).click();
  248 |     await expect(home).toBeVisible();
  249 |     await expect.poll(() => page.evaluate(() => window.scrollY)).toBe(0);
  250 |     record(`ipad-home-return-${info.project.name}`, { source: feed.source, traces });
  251 |     await page.screenshot({ path: `${folder}/ipad-home-return-${info.project.name}.png` });
  252 |   } finally { await context.close(); }
  253 | });
  254 | 
  255 | // The previous entry test deliberately held the feed pending. Cover a
  256 | // ready preload too, starting before the incoming title is inserted.
  257 | async function beginHeadlineTrace(page: Page) {
  258 |   await page.evaluate(() => {
  259 |     type Sample = { source: string; text: string; width: number; column: number; height: number; wrap: string; lines: string[]; transition: string | null };
  260 |     const samples: Sample[] = [];
  261 |     let stopped = false;
  262 |     let frame = 0;
  263 |     const read = (source: string) => {
  264 |       const title = document.querySelector<HTMLElement>('.astrid-vision-hero-copy h1');
  265 |       if (!title || !title.getBoundingClientRect().width) return;
  266 |       const rows: { y: number; words: string[] }[] = [];
  267 |       const walker = document.createTreeWalker(title, NodeFilter.SHOW_TEXT);
  268 |       let node: Node | null;
  269 |       while ((node = walker.nextNode())) {
  270 |         for (const match of (node.textContent ?? '').matchAll(/\S+/g)) {
  271 |           const range = document.createRange();
  272 |           range.setStart(node, match.index!);
  273 |           range.setEnd(node, match.index! + match[0].length);
  274 |           const box = range.getBoundingClientRect();
  275 |           if (!box.width) continue;
  276 |           let row = rows.find(item => Math.abs(item.y - box.y) < 2);
  277 |           if (!row) { row = { y: box.y, words: [] }; rows.push(row); }
  278 |           row.words.push(match[0]);
  279 |         }
  280 |       }
  281 |       samples.push({ source, text: title.textContent ?? '', width: title.offsetWidth,
  282 |         column: title.closest<HTMLElement>('.astrid-vision-hero-copy')!.clientWidth,
  283 |         height: title.offsetHeight, wrap: getComputedStyle(title).getPropertyValue('text-wrap'),
  284 |         lines: rows.map(row => row.words.join(' ')),
  285 |         transition: document.documentElement.getAttribute('data-astrid-page-transition') });
  286 |     };
  287 |     const observer = new MutationObserver(() => read('mutation'));
  288 |     observer.observe(document.body, { childList: true, subtree: true });
  289 |     const tick = () => { if (stopped) return; read('frame'); frame = requestAnimationFrame(tick); };
  290 |     frame = requestAnimationFrame(tick);
  291 |     (window as unknown as { finishHeadlineTrace: () => Sample[]; headlineSamples: Sample[] }).headlineSamples = samples;
  292 |     (window as unknown as { finishHeadlineTrace: () => Sample[] }).finishHeadlineTrace = () => {
  293 |       stopped = true; cancelAnimationFrame(frame); observer.disconnect(); return samples;
  294 |     };
  295 |   });
  296 | }
  297 | 
  298 | for (const width of [375, 390, 414]) {
  299 |   test(`ready Home entry keeps full-width headline word lines at ${width}px`, async ({ page, request }, info) => {
  300 |     await page.emulateMedia({ reducedMotion: 'no-preference' });
  301 |     await page.setViewportSize({ width, height: 844 });
  302 |     const response = await request.get(FEED); expect(response.ok()).toBe(true);
  303 |     const feed = await response.json() as PublicVisionContent;
  304 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  305 |     const preloaded = page.waitForResponse(FEED);
  306 |     await page.goto('/home', { waitUntil: 'domcontentloaded' });
  307 |     await expect(page.getByRole('link', { name: 'Vision', exact: true })).toBeVisible({ timeout: 30000 });
  308 |     await (await preloaded).finished();
  309 |     // Let the completed response reach the shared cache, not a pending-feed fixture.
  310 |     await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
  311 |     const traces = [];
  312 |     for (let trip = 0; trip < 2; trip++) {
  313 |       await beginHeadlineTrace(page);
  314 |       await page.getByRole('link', { name: 'Vision', exact: true }).click();
  315 |       await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
  316 |       await expect(page.getByRole('status', { name: "Loading Astrid's vision" })).toHaveCount(0);
  317 |       await expect.poll(() => page.evaluate(() =>
  318 |         (window as unknown as { headlineSamples: { source: string }[] }).headlineSamples.filter(s => s.source === 'frame').length),
  319 |         { timeout: 20000 }).toBeGreaterThanOrEqual(72);
  320 |       const samples = await page.evaluate(() => (window as unknown as { finishHeadlineTrace: () => {
  321 |         source: string; text: string; width: number; column: number; height: number; wrap: string; lines: string[]; transition: string | null;
  322 |       }[] }).finishHeadlineTrace());
  323 |       traces.push({ trip, samples });
  324 |       record(`ready-headline-${info.project.name}-${width}`, { source: feed.source, traces });
  325 |       expect.soft(samples.some(sample => sample.source === 'mutation'), 'observe first insertion, not only settled frames').toBe(true);
```