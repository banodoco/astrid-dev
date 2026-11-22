# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-sigils-nav.spec.ts >> phone scroll activates each principle sigil through the middle of the viewport
- Location: tests/e2e/public-astrid-vision-sigils-nav.spec.ts:435:1

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  locator('.astrid-vision-standards-list > li')
Expected: 4
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" with timeout 5000ms
  - waiting for locator('.astrid-vision-standards-list > li')
    5 × locator resolved to 0 elements
      - unexpected value "0"

```

# Page snapshot

```yaml
- main [ref=e3]:
  - generic [ref=e4]:
    - link "Astrid home" [ref=e5] [cursor=pointer]:
      - /url: /home
      - generic [ref=e6]: Astrid
    - navigation "Vision page sections" [ref=e7]:
      - link "Vision" [ref=e8] [cursor=pointer]:
        - /url: "#astrid-vision-manifesto"
        - generic [ref=e9]: Vision
      - link "Pillars" [ref=e10] [cursor=pointer]:
        - /url: "#astrid-vision-pillars"
        - generic [ref=e11]: Pillars
      - link "Principles" [ref=e12] [cursor=pointer]:
        - /url: "#astrid-vision-standards"
        - generic [ref=e13]: Principles
      - link "Help" [ref=e14] [cursor=pointer]:
        - /url: "#astrid-vision-contribute"
        - generic [ref=e15]: Help
  - generic [ref=e16]:
    - region "A tool to unlock the artistic potential of the open-source AI community":
      - generic [ref=e18]:
        - paragraph [ref=e19]: 01 Vision
        - generic [ref=e20]:
          - heading "A tool to unlock the artistic potential of the open-source AI community" [level=1] [ref=e21]:
            - generic [ref=e22]:
              - text: A tool to unlock the
              - generic [ref=e23]:
                - text: artistic potential
                - img
              - text: of the open-source AI community
          - paragraph [ref=e26]: Astrid aims to help individuals and the community as a whole pursue artistic work beyond what they thought possible.
          - paragraph [ref=e27]:
            - generic [ref=e28]:
              - text: Populated by the
              - link "Astrid Dev repository" [ref=e29] [cursor=pointer]:
                - /url: https://github.com/banodoco/astrid-dev
              - text: .
    - region "Foundations":
      - region "What we’re building":
        - generic:
          - paragraph: 02 Pillars
          - heading "What we’re building" [level=2]
        - list:
          - listitem [ref=e30]:
            - generic [ref=e31]: "01"
            - heading "A Tool for Artistic Ambition" [level=3] [ref=e34]
            - paragraph [ref=e35]: Astrid is designed to support serious, sustained artistic practice.
            - generic:
              - generic:
                - generic: 3 goals
                - generic: ·
                - generic: 1 gap
                - generic: ·
                - generic: 0 projects
              - generic:
                - img
            - 'button "Explore A Tool for Artistic Ambition: gaps and projects" [ref=e36] [cursor=pointer]'
          - listitem [ref=e37]:
            - generic [ref=e38]: "02"
            - heading "Agent-Powered Liquid Software" [level=3] [ref=e41]
            - paragraph [ref=e42]: Tools should adapt to creative work as people and agents create together.
            - generic:
              - generic:
                - generic: 6 goals
                - generic: ·
                - generic: 6 gaps
                - generic: ·
                - generic: 13 projects
              - generic:
                - img
            - 'button "Explore Agent-Powered Liquid Software: gaps and projects" [ref=e43] [cursor=pointer]'
          - listitem [ref=e44]:
            - generic [ref=e45]: "03"
            - heading "Intelligence That Compounds" [level=3] [ref=e48]
            - paragraph [ref=e49]: What anyone learns should become something everyone can build on.
            - generic:
              - generic:
                - generic: 3 goals
                - generic: ·
                - generic: 3 gaps
                - generic: ·
                - generic: 3 projects
              - generic:
                - img
            - 'button "Explore Intelligence That Compounds: gaps and projects" [ref=e50] [cursor=pointer]'
          - listitem [ref=e51]:
            - generic [ref=e52]: "04"
            - heading "A Shared Creative Endeavor" [level=3] [ref=e55]
            - paragraph [ref=e56]: We want to create the conditions for the community to do more together.
            - generic:
              - generic:
                - generic: 4 goals
                - generic: ·
                - generic: 3 gaps
                - generic: ·
                - generic: 6 projects
              - generic:
                - img
            - 'button "Explore A Shared Creative Endeavor: gaps and projects" [ref=e57] [cursor=pointer]'
      - region "What guides us":
        - generic:
          - paragraph: 03 Principles
          - heading "What guides us" [level=2]
        - list:
          - listitem [ref=e58] [cursor=pointer]:
            - generic:
              - img
            - generic [ref=e59]:
              - heading "Local-first, cloud-capable" [level=3] [ref=e60]
              - paragraph [ref=e61]: Run fully locally, or cheaply and conveniently in the cloud.
            - generic:
              - generic:
                - generic: 4 goals
                - generic: ·
                - generic: 2 gaps
                - generic: ·
                - generic: 3 projects
              - generic:
                - img
            - 'button "Explore Local-first, cloud-capable: gaps and projects" [ref=e62]'
          - listitem [ref=e63] [cursor=pointer]:
            - generic:
              - img
            - generic [ref=e64]:
              - heading "Completely open by design" [level=3] [ref=e65]
              - paragraph [ref=e66]: We aim to share our code, knowledge, ideas and ownership.
            - generic:
              - generic:
                - generic: 4 goals
                - generic: ·
                - generic: 2 gaps
                - generic: ·
                - generic: 4 projects
              - generic:
                - img
            - 'button "Explore Completely open by design: gaps and projects" [ref=e67]'
          - listitem [ref=e68] [cursor=pointer]:
            - generic:
              - img
            - generic [ref=e69]:
              - heading "In the creator's control" [level=3] [ref=e70]
              - paragraph [ref=e71]: Creators have the final say over their creative environments.
            - generic:
              - generic:
                - generic: 3 goals
                - generic: ·
                - generic: 2 gaps
                - generic: ·
                - generic: 5 projects
              - generic:
                - img
            - 'button "Explore In the creator''s control: gaps and projects" [ref=e72]'
          - listitem [ref=e73] [cursor=pointer]:
            - generic:
              - img
            - generic [ref=e74]:
              - heading "Eliminate technical wrangling" [level=3] [ref=e75]
              - paragraph [ref=e76]: Your agents handle technical work so you can focus on art.
            - generic:
              - generic:
                - generic: 4 goals
                - generic: ·
                - generic: 3 gaps
                - generic: ·
                - generic: 40 projects
              - generic:
                - img
            - 'button "Explore Eliminate technical wrangling: gaps and projects" [ref=e77]'
  - region "Want to help build Astrid?" [ref=e78]:
    - generic [ref=e79]:
      - paragraph [ref=e80]: 04 Help
      - heading "Want to help build Astrid?" [level=2] [ref=e81]
      - paragraph [ref=e83]: You and your agents can contribute to Astrid's tools, knowledge and creative community.
      - button "Copy instructions for agents" [ref=e84] [cursor=pointer]:
        - generic [ref=e85]: Copy instructions for agents
      - generic [ref=e86]:
        - button "See all projects" [ref=e87] [cursor=pointer]
        - generic [ref=e88]: "|"
        - button "See all gaps" [ref=e89] [cursor=pointer]
  - generic [ref=e93]:
    - link "Astrid on GitHub" [ref=e94] [cursor=pointer]:
      - /url: https://github.com/banodoco/astrid-dev
      - img [ref=e95]
    - link "Astrid community on Discord" [ref=e98] [cursor=pointer]:
      - /url: https://discord.gg/D5K2c6kfhy
      - img [ref=e99]
    - link "Astrid on X" [ref=e101] [cursor=pointer]:
      - /url: https://x.com/astrid_ivi
      - img [ref=e102]
```

# Test source

```ts
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
  361 |     await expect(marks.nth(index)).toHaveCSS('opacity', '0.58');
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
> 441 |   await expect(cards).toHaveCount(4);
      |                       ^ Error: expect(locator).toHaveCount(expected) failed
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
  462 |     await expect(card.locator('.astrid-vision-principle-corner')).toHaveCSS('opacity', '1');
  463 |     if (index > 0) await expect(cards.nth(index - 1)).not.toHaveAttribute('data-sigil-active', 'true');
  464 |   }
  465 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  466 |   await expect(cards.last()).not.toHaveAttribute('data-sigil-active', 'true');
  467 |   await expect(cards.last().locator('.astrid-vision-sigil-clear-path')).toHaveCSS('animation-name', 'none');
  468 | });
  469 | 
  470 | test('touch modal never starts with an X outline and dismissal clears card focus; keyboard still restores focus', async ({ browser, request }) => {
  471 |   const response = await request.get(FEED);
  472 |   expect(response.ok()).toBeTruthy();
  473 |   const content = await response.json();
  474 |   const context = await browser.newContext({
  475 |     viewport: { width: 390, height: 780 },
  476 |     isMobile: true, hasTouch: true, deviceScaleFactor: 2,
  477 |   });
  478 |   const page = await context.newPage();
  479 |   try {
  480 |     await page.route(FEED, route => route.fulfill({
  481 |       status: 200, contentType: 'application/json',
  482 |       headers: { 'access-control-allow-origin': '*' }, body: JSON.stringify(content),
  483 |     }));
  484 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  485 |     const card = page.locator('.astrid-vision-standards-list > li').nth(1);
  486 |     const trigger = card.getByRole('button', { name: /Explore .*: gaps and projects/ });
  487 |     await trigger.tap();
  488 |     const dialog = page.getByRole('dialog');
  489 |     await expect(dialog).toBeVisible();
  490 |     await expect(dialog.getByRole('heading', { level: 2 })).toBeFocused();
  491 |     await expect(dialog.getByRole('button', { name: 'Close details' })).not.toBeFocused();
  492 | 
  493 |     await dialog.getByRole('button', { name: 'Close details' }).tap();
  494 |     await expect(dialog).toHaveCount(0);
  495 |     await expect(trigger).not.toBeFocused();
  496 |     await expect.poll(() => trigger.evaluate(el => el.matches(':focus-visible'))).toBe(false);
  497 |     await expect.poll(() => card.evaluate(el => getComputedStyle(el, '::after').opacity)).toBe('0');
  498 | 
  499 |     // Restoring focus is correct when the opening action used a keyboard.
  500 |     await trigger.focus();
  501 |     await page.keyboard.press('Enter');
  502 |     await expect(dialog).toBeVisible();
  503 |     await expect(dialog.getByRole('heading', { level: 2 })).toBeFocused();
  504 |     await page.keyboard.press('Escape');
  505 |     await expect(dialog).toHaveCount(0);
  506 |     await expect(trigger).toBeFocused();
  507 |   } finally {
  508 |     await context.close();
  509 |   }
  510 | });
  511 | 
  512 | test('phone header centers the active section when horizontal scroll bounds permit', async ({ page, request }) => {
  513 |   await pinnedFeed(page, request);
  514 |   await page.setViewportSize({ width: 320, height: 740 });
  515 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  516 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  517 |   const nav = page.getByRole('navigation', { name: 'Vision page sections' });
  518 |   await expect(nav).toBeVisible();
  519 | 
  520 |   for (const label of ['Pillars', 'Principles', 'Help']) {
  521 |     const active = nav.getByRole('link', { name: new RegExp(label + '$') });
  522 |     await active.click();
  523 |     await expect(active).toHaveAttribute('aria-current', 'location');
  524 |     // Four links can all fit, or leave only edge-clamped positions. Assert the
  525 |     // actual bounded center rather than requiring a fictitious interior slot.
  526 |     await expect.poll(() => nav.evaluate(el => {
  527 |       const selected = el.querySelector('a[aria-current="location"]')!;
  528 |       const a = selected.getBoundingClientRect();
  529 |       const n = el.getBoundingClientRect();
  530 |       const desired = el.scrollLeft + a.left - n.left + a.width / 2 - el.clientWidth / 2;
  531 |       const bounded = Math.max(0, Math.min(el.scrollWidth - el.clientWidth, desired));
  532 |       return Math.abs(el.scrollLeft - bounded);
  533 |     })).toBeLessThan(10);
  534 |     const activeBox = await active.boundingBox();
  535 |     const navBox = await nav.boundingBox();
  536 |     expect(activeBox!.x).toBeGreaterThanOrEqual(navBox!.x - 1);
  537 |     expect(activeBox!.x + activeBox!.width).toBeLessThanOrEqual(navBox!.x + navBox!.width + 1);
  538 |   }
  539 |   expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(321);
  540 | });
  541 | 
```