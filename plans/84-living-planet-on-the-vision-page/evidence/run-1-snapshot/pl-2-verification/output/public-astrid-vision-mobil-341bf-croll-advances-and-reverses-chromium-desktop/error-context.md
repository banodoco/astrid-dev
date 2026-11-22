# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-mobile-catalogs.spec.ts >> two-column mobile pillars animate in reading order as scroll advances and reverses
- Location: tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts:422:1

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  locator('.astrid-vision-principles > li')
Expected: 4
Received: 0
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" with timeout 5000ms
  - waiting for locator('.astrid-vision-principles > li')
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
  331 | });
  332 | 
  333 | for (const width of [390, 1440]) {
  334 |   test(`next subject cycles inside one modal with reset content at ${width}px`, async ({ page, request }, info) => {
  335 |     // Same regression case, now with the owner's bounded back/forward contract.
  336 |     const response = await request.get(FEED);
  337 |     expect(response.ok()).toBeTruthy();
  338 |     const feed = await response.json() as PublicVisionContent;
  339 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  340 |     await page.setViewportSize({ width, height: 900 });
  341 |     await page.emulateMedia({ reducedMotion: 'reduce' });
  342 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  343 |     for (const kind of ['pillar', 'principle'] as const) {
  344 |       const subjects = kind === 'pillar' ? feed.pillars : feed.principles;
  345 |       const opener = page.getByRole('button', { name: 'Explore ' + subjects[0].title + ': gaps and projects' });
  346 |       await opener.focus(); await page.keyboard.press('Enter');
  347 |       const dialog = page.getByRole('dialog');
  348 |       await dialog.evaluate(node => node.setAttribute('data-same-modal', 'yes'));
  349 |       const scroll = dialog.locator('.astrid-vision-details-scroll');
  350 |       const next = dialog.locator('.astrid-vision-details-next');
  351 |       const previous = dialog.locator('.astrid-vision-details-previous');
  352 |       const initialWidth = await scroll.evaluate(node => node.clientWidth);
  353 |       const navigationY = (await next.boundingBox())!.y;
  354 |       for (let index = 0; index < subjects.length; index++) {
  355 |         await expect(dialog).toHaveAccessibleName(subjects[index].title);
  356 |         await expect(dialog).toHaveAttribute('data-same-modal', 'yes');
  357 |         await expect(dialog.locator('.astrid-vision-details-statement')).toHaveText(subjects[index].statement!);
  358 |         await expect.poll(() => scroll.evaluate(node => node.scrollTop)).toBe(0);
  359 |         expect(await scroll.evaluate(node => node.clientWidth)).toBe(initialWidth);
  360 |         expect(await scroll.evaluate(node => {
  361 |           const css = getComputedStyle(node);
  362 |           return Math.abs(parseFloat(css.paddingLeft) - parseFloat(css.paddingRight));
  363 |         })).toBeLessThan(1);
  364 |         if (index === 0) await expect(previous).toBeDisabled();
  365 |         else await expect(previous).toHaveAccessibleName('Previous ' + kind + ': ' + subjects[index - 1].title);
  366 |         if (index === subjects.length - 1) await expect(next).toBeDisabled();
  367 |         else await expect(next).toHaveAccessibleName('Next ' + kind + ': ' + subjects[index + 1].title);
  368 |         const frame = (await dialog.locator('.astrid-vision-details-shell').boundingBox())!;
  369 |         for (const arrow of [previous, next]) {
  370 |           const box = (await arrow.boundingBox())!;
  371 |           expect(Math.abs(box.y + box.height / 2 - frame.y - frame.height / 2)).toBeLessThan(2);
  372 |           expect(box.width).toBeGreaterThanOrEqual(44);
  373 |           expect(Math.abs(box.y - navigationY)).toBeLessThan(1);
  374 |           await expect(arrow).toHaveCSS('position', 'absolute');
  375 |         }
  376 |         // The overlay must not reserve a rail or change the underlying text width.
  377 |         const text = (await dialog.locator('.astrid-vision-details-scroll-inner').boundingBox())!;
  378 |         if (await dialog.evaluate(node => node.hasAttribute('data-exterior-nav'))) {
  379 |           const bounds = (await dialog.boundingBox())!;
  380 |           const left = (await previous.boundingBox())!;
  381 |           const right = (await next.boundingBox())!;
  382 |           expect(left.x + left.width).toBeLessThan(bounds.x);
  383 |           expect(right.x).toBeGreaterThan(bounds.x + bounds.width);
  384 |           expect(left.x).toBeGreaterThanOrEqual(0);
  385 |           expect(right.x + right.width).toBeLessThanOrEqual(width);
  386 |           expect(text.x).toBeGreaterThan(bounds.x);
  387 |           expect(text.x + text.width).toBeLessThan(bounds.x + bounds.width);
  388 |         } else {
  389 |           expect(text.x).toBeLessThan((await previous.boundingBox())!.x + 44);
  390 |           expect(text.x + text.width).toBeGreaterThan((await next.boundingBox())!.x);
  391 |         }
  392 |         if (index === 1) {
  393 |           mkdirSync(folder, { recursive: true });
  394 |           await page.screenshot({ path: `${folder}/real-floating-${kind}-${info.project.name}-${width}.png` });
  395 |         }
  396 |         if (index < subjects.length - 1) {
  397 |           await scroll.evaluate(node => { node.scrollTop = node.scrollHeight; });
  398 |           await next.click();
  399 |         }
  400 |       }
  401 |       // Native disabled click cannot wrap the fourth item around to the first.
  402 |       await next.evaluate(node => (node as HTMLButtonElement).click());
  403 |       await expect(dialog).toHaveAccessibleName(subjects.at(-1)!.title);
  404 |       for (let index = subjects.length - 2; index >= 0; index--) {
  405 |         await previous.click();
  406 |         await expect(dialog).toHaveAccessibleName(subjects[index].title);
  407 |         expect(Math.abs((await previous.boundingBox())!.y - navigationY)).toBeLessThan(1);
  408 |         expect(Math.abs((await next.boundingBox())!.y - navigationY)).toBeLessThan(1);
  409 |         await expect.poll(() => scroll.evaluate(node => node.scrollTop)).toBe(0);
  410 |         await expect(dialog).toHaveAttribute('data-same-modal', 'yes');
  411 |       }
  412 |       await expect(previous).toBeDisabled();
  413 |       await previous.evaluate(node => (node as HTMLButtonElement).click());
  414 |       await expect(dialog).toHaveAccessibleName(subjects[0].title);
  415 |       await page.keyboard.press('Escape');
  416 |       await expect(dialog).toHaveCount(0);
  417 |       await expect(opener).toBeFocused();
  418 |     }
  419 |   });
  420 | }
  421 | 
  422 | test('two-column mobile pillars animate in reading order as scroll advances and reverses', async ({ page, request }, info) => {
  423 |   const response = await request.get(FEED);
  424 |   expect(response.ok()).toBeTruthy();
  425 |   const feed = await response.json() as PublicVisionContent;
  426 |   await page.route(FEED, route => route.fulfill({ json: feed }));
  427 |   await page.setViewportSize({ width: 390, height: 844 });
  428 |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  429 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  430 |   const cards = page.locator('.astrid-vision-principles > li');
> 431 |   await expect(cards).toHaveCount(4);
      |                       ^ Error: expect(locator).toHaveCount(expected) failed
  432 |   await page.evaluate(() => document.fonts.ready);
  433 |   // Exercise actual forward/backward scrolling, not coordinates copied from
  434 |   // the selection algorithm. At page top the first row is already visible.
  435 |   await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
  436 |   await expect(cards.first()).toHaveAttribute('data-play', 'true');
  437 |   const end = await cards.last().evaluate(node => {
  438 |     const box = node.getBoundingClientRect();
  439 |     return Math.max(0, box.bottom + window.scrollY - window.innerHeight / 2);
  440 |   });
  441 |   const samples: { direction: string; scrollY: number; active: number }[] = [];
  442 |   const sweep = async (direction: 'down' | 'up') => {
  443 |     const observed: number[] = [];
  444 |     const steps = Math.ceil(end / 32);
  445 |     for (let step = 0; step <= steps; step++) {
  446 |       const top = end * (direction === 'down' ? step / steps : 1 - step / steps);
  447 |       await page.evaluate(top => new Promise<void>(resolve => {
  448 |         window.scrollTo({ top, behavior: 'instant' });
  449 |         requestAnimationFrame(() => requestAnimationFrame(() => resolve()));
  450 |       }), top);
  451 |       const selected = await cards.evaluateAll(nodes => nodes.flatMap((node, i) => node.hasAttribute('data-play') ? [i] : []));
  452 |       expect(selected).toHaveLength(1);
  453 |       const active = selected[0];
  454 |       if (observed.at(-1) !== active) {
  455 |         observed.push(active);
  456 |         samples.push({ direction, scrollY: await page.evaluate(() => window.scrollY), active });
  457 |         await expect(cards.nth(active).locator('.astrid-vision-art-layer').first()).toHaveCSS('animation-play-state', 'running');
  458 |       }
  459 |     }
  460 |     return observed;
  461 |   };
  462 |   expect(await sweep('down')).toEqual([0, 1, 2, 3]);
  463 |   // Each of the first three cards gets a substantial visible scroll interval.
  464 |   const down = samples.filter(sample => sample.direction === 'down');
  465 |   for (let i = 1; i < down.length; i++) expect(down[i].scrollY - down[i - 1].scrollY).toBeGreaterThan(180);
  466 |   expect(end - down[3].scrollY).toBeGreaterThan(100);
  467 |   expect(await sweep('up')).toEqual([3, 2, 1, 0]);
  468 |   mkdirSync(folder, { recursive: true });
  469 |   writeFileSync(`${folder}/pillar-sequence-${info.project.name}.json`, JSON.stringify({ source: feed.source, samples }, null, 2));
  470 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  471 |   await expect.poll(() => cards.evaluateAll(nodes => nodes.some(node => node.hasAttribute('data-play')))).toBe(false);
  472 | });
  473 | 
  474 | 
  475 | // WebKit mobile emulation rejects wheel input before dispatch. Exercise real
  476 | // wheels at both responsive widths in a wheel-capable context, with a separate
  477 | // mobile-emulated touch cancellation check below. No assertions are skipped.
  478 | test.describe('native wheel scroll isolation', () => {
  479 |   test.use({ isMobile: false });
  480 | for (const width of [390, 1440]) {
  481 |   test(`all popup types lock the page and ignore control-bar scrolling at ${width}px`, async ({ page }, info) => {
  482 |     await page.setViewportSize({ width, height: 900 });
  483 |     await page.emulateMedia({ reducedMotion: 'reduce' });
  484 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  485 |     // Existing longhand styles must survive the shared page lock.
  486 |     await page.evaluate(() => { document.body.style.overflowY = 'auto'; });
  487 |     const openers = [
  488 |       page.locator('.astrid-vision-principles > li').first().getByRole('button'),
  489 |       page.locator('.astrid-vision-standards-list > li').first().getByRole('button'),
  490 |       page.getByRole('button', { name: 'See all gaps', exact: true }),
  491 |       page.getByRole('button', { name: 'See all projects', exact: true }),
  492 |     ];
  493 |     const records = [];
  494 |     for (const [index, opener] of openers.entries()) {
  495 |       await opener.scrollIntoViewIfNeeded();
  496 |       await opener.focus();
  497 |       const before = await page.evaluate(() => ({ x: scrollX, y: scrollY, body: document.body.style.cssText,
  498 |         overflow: document.documentElement.style.overflow, behavior: document.documentElement.style.scrollBehavior }));
  499 |       await page.keyboard.press('Enter');
  500 |       const dialog = page.getByRole('dialog');
  501 |       const scroll = dialog.locator('.astrid-vision-details-scroll');
  502 |       const header = dialog.locator('.astrid-vision-details-header');
  503 |       await expect(dialog).toBeVisible();
  504 |       await expect(page.locator('body')).toHaveCSS('position', 'fixed');
  505 |       const anchor = await opener.boundingBox();
  506 |       const lockedY = await page.evaluate(() => scrollY);
  507 |       const h = (await header.boundingBox())!;
  508 |       const originalInner = await scroll.evaluate(node => node.scrollTop);
  509 |       await page.mouse.move(h.x + h.width / 2, h.y + h.height / 2);
  510 |       for (const delta of [360, -360]) {
  511 |         await page.mouse.wheel(0, delta);
  512 |         await page.waitForTimeout(100);
  513 |         expect(await page.evaluate(() => scrollY)).toBe(lockedY);
  514 |         expect(await scroll.evaluate(node => node.scrollTop)).toBe(originalInner);
  515 |       }
  516 |       // Touch cancellation is checked directly in WebKit as well as Chromium.
  517 |       // Synthetic touches do not claim to reproduce physical iPhone momentum.
  518 |       const touch = await header.evaluate(node => {
  519 |         const drag = new Event('touchmove', { bubbles: true, cancelable: true });
  520 |         Object.defineProperty(drag, 'touches', { value: [{ identifier: 1 }] });
  521 |         node.dispatchEvent(drag);
  522 |         const pinch = new Event('touchmove', { bubbles: true, cancelable: true });
  523 |         Object.defineProperty(pinch, 'touches', { value: [{ identifier: 1 }, { identifier: 2 }] });
  524 |         node.dispatchEvent(pinch);
  525 |         return { drag: drag.defaultPrevented, pinch: pinch.defaultPrevented };
  526 |       });
  527 |       expect(touch).toEqual({ drag: true, pinch: false });
  528 |       // Some closed desktop subjects legitimately fit without a scrollbar.
  529 |       // Open their real disclosures before asserting scroll movement;
  530 |       // the control-bar checks above also exercise the short state.
  531 |       if (index < 2) {
```