# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-sigils-nav.spec.ts >> desktop section clicks keep the chosen highlight throughout smooth page scrolling
- Location: tests/e2e/public-astrid-vision-sigils-nav.spec.ts:543:1

# Error details

```
Error: expect(locator).toHaveAttribute(expected) failed

Locator: getByRole('navigation', { name: 'Vision page sections' }).getByRole('link', { name: /Vision$/ })
Expected: "location"
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toHaveAttribute" with timeout 5000ms
  - waiting for getByRole('navigation', { name: 'Vision page sections' }).getByRole('link', { name: /Vision$/ })

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
  542 | 
  543 | test('desktop section clicks keep the chosen highlight throughout smooth page scrolling', async ({ page, request }) => {
  544 |   await pinnedFeed(page, request);
  545 |   await page.setViewportSize({ width: 1720, height: 900 });
  546 |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  547 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  548 |   const nav = page.getByRole('navigation', { name: 'Vision page sections' });
> 549 |   await expect(nav.getByRole('link', { name: /Vision$/ })).toHaveAttribute('aria-current', 'location');
      |                                                            ^ Error: expect(locator).toHaveAttribute(expected) failed
  550 | 
  551 |   await page.evaluate(() => {
  552 |     const monitor = window as typeof window & { __astridNavSelections?: string[] };
  553 |     monitor.__astridNavSelections = [];
  554 |     const nav = document.querySelector('.astrid-vision-section-nav')!;
  555 |     new MutationObserver(() => {
  556 |       const selected = nav.querySelector('a[aria-current="location"]');
  557 |       if (selected) monitor.__astridNavSelections?.push(selected.getAttribute('href') ?? '');
  558 |     }).observe(nav, { subtree: true, attributes: true, attributeFilter: ['aria-current'] });
  559 |   });
  560 | 
  561 |   const destination = nav.getByRole('link', { name: /Help$/ });
  562 |   await destination.click();
  563 |   await expect(destination).toHaveAttribute('aria-current', 'location');
  564 |   await expect.poll(() => page.evaluate(() => {
  565 |     const target = document.getElementById('astrid-vision-contribute')!;
  566 |     const margin = Number.parseFloat(getComputedStyle(target).scrollMarginTop) || 0;
  567 |     const requested = window.scrollY + target.getBoundingClientRect().top - margin;
  568 |     const maximum = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
  569 |     return Math.abs(window.scrollY - Math.min(maximum, Math.max(0, requested)));
  570 |   })).toBeLessThan(3);
  571 |   await page.waitForTimeout(200);
  572 |   const selections = await page.evaluate(() =>
  573 |     (window as typeof window & { __astridNavSelections?: string[] }).__astridNavSelections ?? []);
  574 |   expect(selections.length).toBeGreaterThan(0);
  575 |   expect(selections.every(id => id === '#astrid-vision-contribute'), selections.join(' → ')).toBe(true);
  576 | 
  577 |   // After the smooth jump completes, ordinary user scrolling can update the
  578 |   // active section again; the clicked item must not remain locked.
  579 |   await page.evaluate(() => window.scrollTo(0, 0));
  580 |   await expect(nav.getByRole('link', { name: /Vision$/ })).toHaveAttribute('aria-current', 'location');
  581 | });
  582 | 
```