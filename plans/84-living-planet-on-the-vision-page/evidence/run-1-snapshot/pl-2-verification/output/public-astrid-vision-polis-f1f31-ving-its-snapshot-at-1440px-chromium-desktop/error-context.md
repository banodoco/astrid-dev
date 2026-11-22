# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-polish.spec.ts >> room transition context at 1440px >> scrolled Vision returns to the retained main page without moving its snapshot at 1440px
- Location: tests/e2e/public-astrid-vision-polish.spec.ts:288:3

# Error details

```
Error: expect(locator).not.toHaveAttribute() failed

Locator:  locator('html')
Expected: not have attribute
Received: have attribute
Timeout:  5000ms

Call log:
  - Expect "not toHaveAttribute" with timeout 5000ms
  - waiting for locator('html')

```

```yaml
- document:
  - main
```

# Test source

```ts
  230 |     mkdirSync(folder, { recursive: true });
  231 |     await page.locator('.astrid-vision-standards').screenshot({ path: `${folder}/real-coloured-principles-${info.project.name}-${width}.png` });
  232 |     const measurements: unknown[] = [];
  233 |     for (const mode of ['light', 'dark'] as const) {
  234 |       const paper = mode === 'light' ? '#f7f5ef' : '#0d0e17';
  235 |       const ink = mode === 'light' ? '#25241f' : '#f3eee4';
  236 |       const dusk = mode === 'light' ? 0 : 1;
  237 |       const control = await page.addStyleTag({ content: `main.astrid-vision { --astrid-paper: ${paper} !important; --astrid-ink: ${ink} !important; --astrid-dusk-ink: ${dusk} !important; --astrid-dusk-firm: 0 !important; }` });
  238 |       const colours = await cards.evaluateAll((nodes, paper) => {
  239 |         const canvas = document.createElement('canvas'); canvas.width = canvas.height = 1;
  240 |         const ctx = canvas.getContext('2d', { willReadFrequently: true })!;
  241 |         const rgba = (value: string) => {
  242 |           ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = value; ctx.fillRect(0, 0, 1, 1);
  243 |           const data = ctx.getImageData(0, 0, 1, 1).data;
  244 |           return [data[0], data[1], data[2], data[3] / 255];
  245 |         };
  246 |         const over = (fg: number[], bg: number[]) => fg.slice(0, 3).map((v, i) => v * fg[3] + bg[i] * (1 - fg[3]));
  247 |         const luminance = (rgb: number[]) => rgb.slice(0, 3).map(v => v / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4).reduce((s, v, i) => s + v * [.2126, .7152, .0722][i], 0);
  248 |         const contrast = (fg: number[], bg: number[]) => (Math.max(luminance(fg), luminance(bg)) + .05) / (Math.min(luminance(fg), luminance(bg)) + .05);
  249 |         return nodes.map(node => {
  250 |           const style = getComputedStyle(node);
  251 |           const fill = rgba(style.backgroundColor);
  252 |           const heading = rgba(getComputedStyle(node.querySelector('h3')!).color);
  253 |           const body = rgba(getComputedStyle(node.querySelector('.astrid-vision-principle-statement, .astrid-vision-markdown')!).color);
  254 |           const mark = getComputedStyle(node.querySelector('.astrid-vision-principle-sigil')!);
  255 |           const sigil = rgba(mark.color); sigil[3] *= Number(mark.opacity);
  256 |           const background = over(fill, rgba(paper));
  257 |           const markedBackground = over(sigil, background);
  258 |           return { fill, heading, body, headingLuminance: luminance(heading), bodyLuminance: luminance(body), headingContrast: contrast(heading, background), bodyContrast: contrast(body, background), bodyOverSigilContrast: contrast(body, markedBackground) };
  259 |         });
  260 |       }, paper);
  261 |       expect(new Set(colours.map(c => JSON.stringify(c.fill))).size).toBe(4);
  262 |       expect(new Set(colours.map(c => JSON.stringify(c.heading))).size).toBe(4);
  263 |       expect(new Set(colours.map(c => JSON.stringify(c.body))).size).toBe(4);
  264 |       for (const c of colours) {
  265 |         expect(c.fill[3]).toBeGreaterThan(.04); expect(c.fill[3]).toBeLessThan(.16);
  266 |         expect(c.heading[3]).toBe(1); expect(c.body[3]).toBe(1);
  267 |         if (mode === 'light') expect(c.headingLuminance).toBeLessThan(c.bodyLuminance);
  268 |         else expect(c.headingLuminance).toBeGreaterThan(c.bodyLuminance);
  269 |         expect(c.headingContrast).toBeGreaterThanOrEqual(4.5);
  270 |         expect(c.bodyContrast).toBeGreaterThanOrEqual(4.5);
  271 |         if (width === 390) expect(c.bodyOverSigilContrast).toBeGreaterThanOrEqual(4.5);
  272 |       }
  273 |       measurements.push({ mode, colours });
  274 |       await control.evaluate(node => node.remove());
  275 |     }
  276 |     await expect(cards.locator('h3')).toHaveText(feed.principles.map(p => p.title));
  277 |     await expect(cards.locator('.astrid-vision-principle-statement')).toHaveText(feed.principles.map(p => p.statement!));
  278 |     writeFileSync(`${folder}/principle-colours-${info.project.name}-${width}.json`, JSON.stringify({ source: feed.source, measurements }, null, 2));
  279 |   });
  280 | }
  281 | 
  282 | 
  283 | for (const width of [390, 1440]) {
  284 |   test.describe(`room transition context at ${width}px`, () => {
  285 |     // Match the desktop case to a desktop raster/input context. The 390px
  286 |     // case retains the project's iPhone profile and all frame assertions.
  287 |     if (width === 1440) test.use({ isMobile: false, deviceScaleFactor: 1, hasTouch: false });
  288 |   test(`scrolled Vision returns to the retained main page without moving its snapshot at ${width}px`, async ({ page }, info) => {
  289 |     await pinLive(page);
  290 |     await page.setViewportSize({ width, height: 844 });
  291 |     await page.emulateMedia({ reducedMotion: 'no-preference' });
  292 |     await page.addInitScript(() => {
  293 |       type Frame = { scroll: number; top: number };
  294 |       type Record = { destination?: string; presentation?: string; outgoing: number; snapshot?: Frame; frames: Frame[]; named: string[] };
  295 |       const state = window as typeof window & { __roomTransitions: Record[]; __homeTapY?: number };
  296 |       state.__roomTransitions = [];
  297 |       document.addEventListener('pointerdown', event => {
  298 |         if ((event.target as Element)?.closest('.astrid-public-site a[href="/vision"]')) state.__homeTapY = window.scrollY;
  299 |       }, true);
  300 |       const native = document.startViewTransition?.bind(document);
  301 |       if (!native) return;
  302 |       document.startViewTransition = ((callback: () => void) => {
  303 |         const record: Record = { destination: document.documentElement.dataset.astridPageTransition,
  304 |           presentation: document.documentElement.dataset.astridPageTransitionStyle,
  305 |           outgoing: window.scrollY, frames: [], named: [] };
  306 |         state.__roomTransitions.push(record);
  307 |         return native(() => {
  308 |           callback();
  309 |           const home = document.querySelector<HTMLElement>('.astrid-public-site');
  310 |           if (record.destination !== 'home' || !home) return;
  311 |           const read = () => ({ scroll: window.scrollY, top: home.getBoundingClientRect().top });
  312 |           record.snapshot = read();
  313 |           record.named = [home, ...home.querySelectorAll('*')].map(node => getComputedStyle(node).viewTransitionName)
  314 |             .filter(name => name && name !== 'none');
  315 |           const sample = () => {
  316 |             record.frames.push(read());
  317 |             if (record.frames.length < 12) requestAnimationFrame(sample);
  318 |           };
  319 |           requestAnimationFrame(sample);
  320 |         });
  321 |       }) as typeof document.startViewTransition;
  322 |     });
  323 |     await page.goto('/home', { waitUntil: 'domcontentloaded' });
  324 |     const home = page.locator('.astrid-public-site');
  325 |     await expect(home).toBeVisible();
  326 |     await home.evaluate(node => node.setAttribute('data-retained-proof', 'same'));
  327 |     await page.addStyleTag({ content: 'html { scroll-behavior: smooth !important; }' });
  328 |     await page.getByRole('link', { name: 'Vision', exact: true }).first().click();
  329 |     await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
> 330 |     await expect(page.locator('html')).not.toHaveAttribute('data-astrid-page-transition');
      |                                            ^ Error: expect(locator).not.toHaveAttribute() failed
  331 |     const expectedHomeY = await page.evaluate(() => (window as typeof window & { __homeTapY: number }).__homeTapY);
  332 |     expect(Number.isFinite(expectedHomeY)).toBe(true);
  333 |     const outgoing = await page.evaluate(() => new Promise<number>(resolve => {
  334 |       window.scrollTo({ top: 900, behavior: 'instant' });
  335 |       requestAnimationFrame(() => requestAnimationFrame(() => resolve(window.scrollY)));
  336 |     }));
  337 |     expect(outgoing).toBeGreaterThan(500);
  338 |     // The sticky link shrinks while its wordmark folds. Locator.click() can
  339 |     // retry with end/center scroll alignment and move the already-visible
  340 |     // header before the click. Hit-test and click the visible icon instead;
  341 |     // keep smooth scrolling and all application navigation behavior intact.
  342 |     const homeLink = page.getByRole('link', { name: 'Astrid home', exact: true });
  343 |     await expect(homeLink.locator('img')).toBeInViewport({ ratio: 1 });
  344 |     const point = await homeLink.locator('img').evaluate(node => {
  345 |       const box = node.getBoundingClientRect();
  346 |       const x = box.x + box.width / 2, y = box.y + box.height / 2;
  347 |       return { x, y, hit: document.elementFromPoint(x, y)?.closest('a') === node.closest('a') };
  348 |     });
  349 |     expect(point.hit).toBe(true);
  350 |     await page.mouse.click(point.x, point.y);
  351 |     await expect(home).toBeVisible();
  352 |     await expect(home).toHaveAttribute('data-retained-proof', 'same');
  353 |     await expect.poll(() => page.evaluate(() => window.scrollY)).toBeCloseTo(expectedHomeY, 0);
  354 |     const supported = await page.evaluate(() => typeof document.startViewTransition === 'function');
  355 |     if (supported) {
  356 |       await expect.poll(() => page.evaluate(() => (window as typeof window & {
  357 |         __roomTransitions: { destination?: string; frames: unknown[] }[];
  358 |       }).__roomTransitions.filter(r => r.destination === 'home').at(-1)?.frames.length ?? 0)).toBe(12);
  359 |       const record = await page.evaluate(() => (window as typeof window & {
  360 |         __roomTransitions: { destination?: string; presentation?: string; outgoing: number;
  361 |           snapshot: { scroll: number; top: number }; frames: { scroll: number; top: number }[]; named: string[] }[];
  362 |       }).__roomTransitions.filter(r => r.destination === 'home').at(-1)!);
  363 |       mkdirSync(folder, { recursive: true });
  364 |       writeFileSync(`${folder}/room-transition-${info.project.name}-${width}.json`, JSON.stringify(record, null, 2));
  365 |       const sharedBrand = width > 640 && expectedHomeY <= 72;
  366 |       expect(record.presentation).toBe(sharedBrand ? 'brand' : 'crossfade');
  367 |       expect(record.outgoing).toBeGreaterThan(500);
  368 |       expect(record.outgoing).toBeCloseTo(outgoing, 0);
  369 |       expect(record.snapshot.scroll).toBeCloseTo(expectedHomeY, 0);
  370 |       expect(record.named).toEqual(sharedBrand ? ['astrid-brand-mink', 'astrid-brand-name', 'astrid-brand-beta'] : []);
  371 |       for (const frame of record.frames) {
  372 |         expect(frame.scroll).toBeCloseTo(expectedHomeY, 0);
  373 |         expect(Math.abs(frame.top - record.snapshot.top)).toBeLessThan(1);
  374 |       }
  375 |     }
  376 |     await expect(page.locator('html')).not.toHaveAttribute('data-astrid-page-transition');
  377 |     await expect(page.locator('html')).not.toHaveAttribute('data-astrid-page-transition-style');
  378 |     expect(await page.evaluate(() => history.scrollRestoration)).toBe('manual');
  379 |     mkdirSync(folder, { recursive: true });
  380 |     await page.screenshot({ path: `${folder}/real-main-after-vision-${info.project.name}-${width}.png` });
  381 |   });
  382 |   });
  383 | }
  384 | 
```