# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-entry.spec.ts >> headline remains normal full-column flow on cold entry, reload and viewport changes
- Location: tests/e2e/public-astrid-vision-entry.spec.ts:338:1

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator: locator('#astrid-vision-title')
Expected: "A tool to unlock the artistic potential of the open-source AI community"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveText" with timeout 5000ms
  - waiting for locator('#astrid-vision-title')

```

```yaml
- main:
  - link "Astrid home":
    - /url: /home
    - text: Astrid
  - region:
    - paragraph: 01 Vision
    - status "Loading Astrid's vision"
  - link "Astrid on GitHub":
    - /url: https://github.com/banodoco/astrid-dev
  - link "Astrid community on Discord":
    - /url: https://discord.gg/D5K2c6kfhy
  - link "Astrid on X":
    - /url: https://x.com/astrid_ivi
```

# Test source

```ts
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
  326 |       expect.soft(samples.every(sample => sample.wrap === 'wrap'), 'never invoke paragraph balancing for this heading').toBe(true);
  327 |       expect.soft(samples.every(sample => Math.abs(sample.width - sample.column) <= 1), 'use the whole mobile reading column').toBe(true);
  328 |       expect.soft(new Set(samples.map(sample => JSON.stringify(sample.lines))).size, 'word-to-line assignment is invariant from insertion').toBe(1);
  329 |       expect.soft(samples.every(sample => sample.text === feed.vision.title)).toBe(true);
  330 |       expect.soft(samples.every(sample => sample.lines.join(' ') === feed.vision.title)).toBe(true);
  331 |       if (width === 390) await page.screenshot({ path: `${folder}/ready-headline-${info.project.name}-${trip}.png` });
  332 |       await page.getByRole('link', { name: 'Astrid home', exact: true }).click();
  333 |       await expect(page.locator('.astrid-vision')).toHaveCount(0);
  334 |     }
  335 |   });
  336 | }
  337 | 
  338 | test('headline remains normal full-column flow on cold entry, reload and viewport changes', async ({ page, request }, info) => {
  339 |   const response = await request.get(FEED); expect(response.ok()).toBe(true);
  340 |   const feed = await response.json() as PublicVisionContent;
  341 |   await page.route(FEED, route => route.fulfill({ json: feed }));
  342 |   await page.setViewportSize({ width: 390, height: 844 });
  343 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  344 |   const snapshots = [];
  345 |   for (const viewport of [{ width: 390, height: 844 }, { width: 390, height: 664 },
  346 |     { width: 320, height: 664 }, { width: 414, height: 844 }, { width: 390, height: 844 }]) {
  347 |     await page.setViewportSize(viewport);
> 348 |     await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
      |                                                        ^ Error: expect(locator).toHaveText(expected) failed
  349 |     const before = await hero(page);
  350 |     const style = await page.locator('#astrid-vision-title').evaluate(node => ({
  351 |       wrap: getComputedStyle(node).getPropertyValue('text-wrap'),
  352 |       width: (node as HTMLElement).offsetWidth,
  353 |       column: node.closest<HTMLElement>('.astrid-vision-hero-copy')!.clientWidth,
  354 |       overflow: document.documentElement.scrollWidth > innerWidth + 1,
  355 |     }));
  356 |     expect.soft(style.wrap).toBe('wrap');
  357 |     expect.soft(Math.abs(style.width - style.column)).toBeLessThanOrEqual(1);
  358 |     expect.soft(style.overflow).toBe(false);
  359 |     await page.reload({ waitUntil: 'domcontentloaded' });
  360 |     await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
  361 |     const after = await hero(page);
  362 |     expect.soft(after).toEqual(before);
  363 |     snapshots.push({ viewport, before, after, style });
  364 |   }
  365 |   record(`cold-headline-flow-${info.project.name}`, { source: feed.source, snapshots });
  366 | });
  367 | 
  368 | // Track the shade itself, not only the panel's settled geometry. The
  369 | // previous native-opacity fade reversed in WebKit while every sky pixel
  370 | // and page colour stayed unchanged (owner's light/dark flash).
  371 | for (const scenario of [
  372 |   { width: 390, hour: '10', label: 'phone-day', touch: false },
  373 |   { width: 390, hour: '01', label: 'phone-night', touch: false },
  374 |   { width: 1440, hour: '10', label: 'desktop-day', touch: false },
  375 |   { width: 390, hour: '10', label: 'phone-touch', touch: true },
  376 | ]) {
  377 |   test.describe(`backdrop continuity ${scenario.label}`, () => {
  378 |     test.use({ timezoneId: 'Europe/Berlin', ...(scenario.width === 1440
  379 |       ? { isMobile: false, deviceScaleFactor: 1, hasTouch: false } : scenario.touch ? { isMobile: true, hasTouch: true } : {}) });
  380 |     test('popup shading never reverses or repaints the underlying page', async ({ page, request }, info) => {
  381 |       test.setTimeout(150000);
  382 |       await page.setViewportSize({ width: scenario.width, height: 844 });
  383 |       await page.emulateMedia({ reducedMotion: 'no-preference' });
  384 |       await page.clock.setFixedTime(new Date(`2026-11-15T${scenario.hour}:00:00Z`));
  385 |       const response = await request.get(FEED); expect(response.ok()).toBe(true);
  386 |       const feed = await response.json() as PublicVisionContent;
  387 |       await page.route(FEED, route => route.fulfill({ json: feed }));
  388 |       await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  389 |       await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4, { timeout: 30000 });
  390 |       await page.evaluate(() => document.fonts.ready);
  391 |       await expect.poll(() => page.locator('.astrid-sky canvas').first().evaluate(c => c.style.width)).not.toBe('');
  392 |       // Allow the existing initial sky reveal to complete before opening.
  393 |       await page.waitForTimeout(2000);
  394 |       const results = [];
  395 |       for (const kind of ['pillar', 'principle', 'gaps', 'projects', 'pillar']) {
  396 |         const opener = kind === 'pillar' ? page.locator('.astrid-vision-principles > li').last().getByRole('button')
  397 |           : kind === 'principle' ? page.locator('.astrid-vision-standards-list > li').last().getByRole('button')
  398 |           : page.getByRole('button', { name: 'See all ' + kind, exact: true });
  399 |         await opener.scrollIntoViewIfNeeded();
  400 |         if (!scenario.touch) {
  401 |           const bounds = await opener.boundingBox();
  402 |           expect(bounds).not.toBeNull();
  403 |           await page.mouse.move(bounds!.x + bounds!.width / 2, bounds!.y + bounds!.height / 2);
  404 |         }
  405 |         // Scrolling reveals nearby reading text; let that earlier gesture finish
  406 |         // before measuring a new opening. Ignore ongoing decorative loops.
  407 |         await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
  408 |         await expect.poll(() => page.evaluate(() => document.querySelector('.astrid-vision')!
  409 |           .getAnimations({ subtree: true }).filter(animation =>
  410 |             (animation.playState === 'running' || animation.pending) &&
  411 |             Number.isFinite(animation.effect?.getComputedTiming().iterations ?? 1)).length),
  412 |           { timeout: 10000 }).toBe(0);
  413 |         // Finish the preceding scroll/pointer parallax before measuring a new
  414 |         // action. A fixed delay can leave subpixel easing in the first frame.
  415 |         await page.evaluate(() => new Promise<void>((resolve, reject) => {
  416 |           let previous = '', stable = 0, attempts = 0;
  417 |           const settle = () => {
  418 |             const transforms = JSON.stringify(Array.from(document.querySelectorAll<HTMLCanvasElement>('.astrid-vision .astrid-sky canvas')).map(canvas => {
  419 |               let hash = 2166136261;
  420 |               for (const pixel of canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data)
  421 |                 hash = Math.imul(hash ^ pixel, 16777619);
  422 |               return [canvas.style.transform, canvas.width, canvas.height, hash >>> 0];
  423 |             }));
  424 |             stable = transforms === previous ? stable + 1 : 0;
  425 |             previous = transforms;
  426 |             if (stable >= 4) resolve();
  427 |             else if (++attempts >= 240) reject(new Error('Sky parallax did not settle before the opening gesture'));
  428 |             else requestAnimationFrame(settle);
  429 |           };
  430 |           requestAnimationFrame(settle);
  431 |         }));
  432 |         await page.evaluate(() => {
  433 |           type Frame = { t: number; native: number | null; shade: number; surface: number;
  434 |             colours: string; headerY: number; sky: string };
  435 |           const state = window as unknown as { backdropFrames: Frame[]; backdropInput: string };
  436 |           state.backdropFrames = [];
  437 |           const read = () => {
  438 |             const main = document.querySelector<HTMLElement>('.astrid-vision')!;
  439 |             const dialog = main.querySelector<HTMLDialogElement>('dialog');
  440 |             const backdrop = dialog?.open ? getComputedStyle(dialog, '::backdrop') : null;
  441 |             const rgba = backdrop?.backgroundColor.match(/[\d.]+/g)?.map(Number) ?? [];
  442 |             const alpha = rgba.length === 4 ? rgba[3] : rgba.length === 3 ? 1 : 0;
  443 |             const shell = dialog?.querySelector('.astrid-vision-details-shell');
  444 |             const sky = Array.from(main.querySelectorAll<HTMLCanvasElement>('.astrid-sky canvas')).map(canvas => {
  445 |               const pixels = canvas.getContext('2d')!.getImageData(0, 0, canvas.width, canvas.height).data;
  446 |               let hash = 2166136261;
  447 |               for (const pixel of pixels) hash = Math.imul(hash ^ pixel, 16777619);
  448 |               const rect = canvas.getBoundingClientRect();
```