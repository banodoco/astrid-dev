# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-sigils-nav.spec.ts >> principle sigils use softer faded page colors while their readable cue stays solid
- Location: tests/e2e/public-astrid-vision-sigils-nav.spec.ts:352:1

# Error details

```
Error: expect(locator).toHaveCSS(expected) failed

Locator: locator('.astrid-vision-standards-list > li').locator('.astrid-vision-principle-sigil').first()
Expected: "0.58"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveCSS" with timeout 5000ms
  - waiting for locator('.astrid-vision-standards-list > li').locator('.astrid-vision-principle-sigil').first()

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
  261 |     await expect(page.getByRole('dialog')).toBeVisible();
  262 |     await page.keyboard.press('Escape');
  263 |   }
  264 | });
  265 | 
  266 | test('sticky header navigation tracks sections and folds the wordmark to its icon', async ({ page, request }) => {
  267 |   await pinnedFeed(page, request);
  268 |   await page.setViewportSize({ width: 1720, height: 900 });
  269 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  270 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  271 |   const nav = page.getByRole('navigation', { name: 'Vision page sections' });
  272 |   await expect(nav).toBeVisible();
  273 |   const header = page.locator('.astrid-vision > header.astrid-vision-bar');
  274 |   const wordmark = header.locator('.astrid-vision-brand-name');
  275 |   await expect(header).toHaveCSS('position', 'sticky');
  276 |   await expect(header.locator('nav')).toHaveCount(1);
  277 |   await expect(nav).toHaveCSS('position', 'relative');
  278 |   await expect(wordmark).toHaveCSS('max-width', '100px');
  279 |   await expect(nav.getByRole('link')).toHaveCount(4);
  280 |   expect(await nav.locator('a').evaluateAll(elements => elements.map(el => el.getAttribute('href'))))
  281 |     .toEqual([
  282 |       '#astrid-vision-manifesto', '#astrid-vision-pillars', '#astrid-vision-standards',
  283 |       '#astrid-vision-contribute',
  284 |     ]);
  285 |   const brand = header.locator('.astrid-vision-brand');
  286 |   const brandRect = await brand.boundingBox();
  287 |   const navRect = await nav.boundingBox();
  288 |   expect(brandRect).not.toBeNull();
  289 |   expect(navRect).not.toBeNull();
  290 |   expect(navRect!.x).toBeGreaterThanOrEqual(brandRect!.x + brandRect!.width);
  291 |   await expect(nav.getByRole('link', { name: /Vision$/ })).toHaveAttribute('aria-current', 'location');
  292 | 
  293 |   for (const [label, id] of [
  294 |     ['Pillars', 'astrid-vision-pillars'],
  295 |     ['Principles', 'astrid-vision-standards'],
  296 |     ['Help', 'astrid-vision-contribute'],
  297 |   ]) {
  298 |     const link = nav.getByRole('link', { name: new RegExp(label + '$') });
  299 |     await link.click();
  300 |     await expect(link).toHaveAttribute('href', '#' + id);
  301 |     await expect(link).toHaveAttribute('aria-current', 'location');
  302 |     await expect(page.locator('#' + id)).toBeVisible();
  303 |   }
  304 | 
  305 |   await expect(header).toHaveAttribute('data-condensed', 'true');
  306 |   await expect(wordmark).toHaveCSS('max-width', '0px');
  307 |   await expect(wordmark).toHaveCSS('opacity', '0');
  308 |   await page.evaluate(() => window.scrollTo(0, 0));
  309 |   await expect(header).not.toHaveAttribute('data-condensed', 'true');
  310 |   await expect(wordmark).toHaveCSS('opacity', '1');
  311 | });
  312 | 
  313 | test('phones get one compact sticky header with navigation beside a folding Astrid wordmark', async ({ page, request }) => {
  314 |   await pinnedFeed(page, request);
  315 |   await page.setViewportSize({ width: 390, height: 780 });
  316 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  317 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  318 |   const nav = page.getByRole('navigation', { name: 'Vision page sections' });
  319 |   const header = page.locator('.astrid-vision > header.astrid-vision-bar');
  320 |   const brand = header.locator('.astrid-vision-brand');
  321 |   await expect(header).toHaveCSS('position', 'sticky');
  322 |   await expect(nav).toHaveCSS('position', 'relative');
  323 |   await expect(header.locator('nav')).toHaveCount(1);
  324 |   const brandBox = await brand.boundingBox();
  325 |   const navBox = await nav.boundingBox();
  326 |   expect(brandBox).not.toBeNull();
  327 |   expect(navBox).not.toBeNull();
  328 |   expect(navBox!.x).toBeGreaterThanOrEqual(brandBox!.x + brandBox!.width);
  329 |   const size = await nav.boundingBox();
  330 |   expect(size).not.toBeNull();
  331 |   expect(size!.x).toBeGreaterThanOrEqual(0);
  332 |   expect(size!.x + size!.width).toBeLessThanOrEqual(391);
  333 |   const link = nav.getByRole('link', { name: /Help$/ });
  334 |   await link.click();
  335 |   await expect(link).toHaveAttribute('aria-current', 'location');
  336 |   await expect(page).toHaveURL(/#astrid-vision-contribute$/);
  337 |   await expect(page.locator('#astrid-vision-contribute')).toBeVisible();
  338 |   await expect(header).toHaveAttribute('data-condensed', 'true');
  339 |   await expect(header.locator('.astrid-vision-brand-name')).toHaveCSS('max-width', '0px');
  340 |   const icon = header.locator('.astrid-vision-brand img');
  341 |   await expect(icon).toBeVisible();
  342 |   const active = await link.boundingBox();
  343 |   const navBounds = await nav.boundingBox();
  344 |   expect(active).not.toBeNull();
  345 |   expect(navBounds).not.toBeNull();
  346 |   expect(active!.x).toBeGreaterThanOrEqual(navBounds!.x - 1);
  347 |   expect(active!.x + active!.width).toBeLessThanOrEqual(navBounds!.x + navBounds!.width + 1);
  348 |   expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(391);
  349 | });
  350 | 
  351 | 
  352 | test('principle sigils use softer faded page colors while their readable cue stays solid', async ({ page, request }) => {
  353 |   await pinnedFeed(page, request);
  354 |   await page.setViewportSize({ width: 1440, height: 900 });
  355 |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  356 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  357 |   const cards = page.locator('.astrid-vision-standards-list > li');
  358 |   const marks = cards.locator('.astrid-vision-principle-sigil');
  359 |   const cornerArrows = cards.locator('.astrid-vision-principle-corner');
  360 |   for (let index = 0; index < 4; index++) {
> 361 |     await expect(marks.nth(index)).toHaveCSS('opacity', '0.58');
      |                                    ^ Error: expect(locator).toHaveCSS(expected) failed
  362 |     await expect(cornerArrows.nth(index)).toHaveCSS('opacity', '1');
  363 |     await expect(marks.nth(index)).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
  364 |     await expect(cornerArrows.nth(index)).toHaveCSS('background-color', 'rgba(0, 0, 0, 0)');
  365 |   }
  366 |   const colors = await marks.evaluateAll(elements => elements.map(element => getComputedStyle(element).color));
  367 |   expect(new Set(colors).size).toBe(4);
  368 |   for (let index = 0; index < 4; index++) {
  369 |     await cards.nth(index).hover();
  370 |     await expect(marks.nth(index)).toHaveCSS('opacity', '0.82');
  371 |     await expect(cornerArrows.nth(index)).toHaveCSS('opacity', '1');
  372 |   }
  373 |   await cards.nth(0).hover();
  374 |   await expect(cards.nth(0).locator('.astrid-vision-sigil-orbit'))
  375 |     .toHaveCSS('animation-name', 'astrid-vision-sigil-orbit');
  376 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  377 |   await expect(cards.nth(0).locator('.astrid-vision-sigil-orbit')).toHaveCSS('animation-name', 'none');
  378 | });
  379 | 
  380 | 
  381 | test('the enlarged header spans the viewport while navigation stays aligned in one bar', async ({ page, request }) => {
  382 |   await pinnedFeed(page, request);
  383 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  384 |   for (const width of [390, 760, 1200, 1720]) {
  385 |     await page.setViewportSize({ width, height: 900 });
  386 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  387 |     const header = page.locator('.astrid-vision > header.astrid-vision-bar');
  388 |     const nav = header.getByRole('navigation', { name: 'Vision page sections' });
  389 |     const bounds = await header.boundingBox();
  390 |     expect(bounds).not.toBeNull();
  391 |     expect(bounds!.x).toBeGreaterThanOrEqual(-1);
  392 |     expect(bounds!.x).toBeLessThanOrEqual(1);
  393 |     expect(bounds!.x + bounds!.width).toBeGreaterThanOrEqual(width - 1);
  394 |     expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(width + 1);
  395 |     expect(bounds!.height).toBeGreaterThanOrEqual(width <= 760 ? 68 : 86);
  396 |     await expect(header).toHaveCSS('position', 'sticky');
  397 |     await expect(nav.getByRole('link')).toHaveCount(4);
  398 |     const pillars = nav.getByRole('link', { name: /Pillars$/ });
  399 |     await expect(pillars).toHaveAttribute('href', '#astrid-vision-pillars');
  400 |     await pillars.click();
  401 |     await expect(pillars).toHaveAttribute('aria-current', 'location');
  402 |     await expect(page.getByRole('heading', { name: 'What we’re building' })).toBeVisible();
  403 |     await expect(page).toHaveURL(/#astrid-vision-pillars$/);
  404 |     expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width + 1);
  405 |   }
  406 | });
  407 | 
  408 | test('principle panels retain their distinct tints and corner arrows stay transparent through dusk hover', async ({ page, request }) => {
  409 |   await pinnedFeed(page, request);
  410 |   await page.setViewportSize({ width: 1440, height: 900 });
  411 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  412 |   const cards = page.locator('.astrid-vision-standards-list > li');
  413 |   await expect(cards).toHaveCount(4);
  414 |   const checkTinted = async () => {
  415 |     const surfaces = await cards.evaluateAll(elements => elements.map(el => ({
  416 |       card: getComputedStyle(el).backgroundColor,
  417 |       arrow: getComputedStyle(el.querySelector('.astrid-vision-principle-corner')!).backgroundColor,
  418 |     })));
  419 |     expect(surfaces).toHaveLength(4);
  420 |     expect(new Set(surfaces.map(surface => surface.card)).size).toBe(4);
  421 |     expect(surfaces.every(surface => surface.card !== 'rgba(0, 0, 0, 0)' && surface.arrow === 'rgba(0, 0, 0, 0)')).toBe(true);
  422 |   };
  423 |   await checkTinted();
  424 |   await page.locator('main.astrid-vision').evaluate(element => {
  425 |     element.style.setProperty('--astrid-dusk', '1');
  426 |     element.style.setProperty('--astrid-dusk-ink', '1');
  427 |     element.style.setProperty('--astrid-dusk-firm', '1');
  428 |   });
  429 |   await checkTinted();
  430 |   await cards.last().hover();
  431 |   await checkTinted();
  432 | });
  433 | 
  434 | 
  435 | test('phone scroll activates each principle sigil through the middle of the viewport', async ({ page, request }) => {
  436 |   await pinnedFeed(page, request);
  437 |   await page.setViewportSize({ width: 390, height: 780 });
  438 |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  439 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  440 |   const cards = page.locator('.astrid-vision-standards-list > li');
  441 |   await expect(cards).toHaveCount(4);
  442 |   const motions = [
  443 |     ['.astrid-vision-sigil-orbit', 'astrid-vision-sigil-orbit'],
  444 |     ['.astrid-vision-sigil-open-ring', 'astrid-vision-sigil-ring'],
  445 |     ['.astrid-vision-sigil-spark', 'astrid-vision-sigil-spark-rise'],
  446 |     ['.astrid-vision-sigil-clear-path', 'none'],
  447 |   ] as const;
  448 |   for (let index = 0; index < motions.length; index++) {
  449 |     const card = cards.nth(index);
  450 |     await card.evaluate(el => {
  451 |       const rect = el.getBoundingClientRect();
  452 |       window.scrollBy(0, rect.top + rect.height / 2 - window.innerHeight / 2);
  453 |     });
  454 |     await expect(card).toHaveAttribute('data-sigil-active', 'true');
  455 |     await expect(card.locator(motions[index][0])).toHaveCSS('animation-name', motions[index][1]);
  456 |     if (index === 3) {
  457 |       await expect(card.locator('.astrid-vision-sigil-knot')).toHaveCSS('transition-duration', '3s');
  458 |       await expect(card.locator('.astrid-vision-sigil-clear-path')).toHaveCSS('transition-duration', '3s');
  459 |     }
  460 |     // Background sigils stay subdued even while their internal shapes animate.
  461 |     await expect(card.locator('.astrid-vision-principle-sigil')).toHaveCSS('opacity', '0.13');
```