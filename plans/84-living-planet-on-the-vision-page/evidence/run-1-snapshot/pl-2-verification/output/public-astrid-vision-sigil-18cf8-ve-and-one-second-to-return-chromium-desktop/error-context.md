# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-sigils-nav.spec.ts >> technical wrangling takes three seconds to resolve and one second to return
- Location: tests/e2e/public-astrid-vision-sigils-nav.spec.ts:72:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.astrid-vision-standards-list > li').last()
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for locator('.astrid-vision-standards-list > li').last()

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
  1   | import { expect, test } from '@playwright/test';
  2   | 
  3   | const FEED = 'https://raw.githubusercontent.com/banodoco/astrid-dev/vision-published/vision.json';
  4   | 
  5   | async function pinnedFeed(page: import('@playwright/test').Page,
  6   |   request: import('@playwright/test').APIRequestContext) {
  7   |   const response = await request.get(FEED);
  8   |   expect(response.ok()).toBeTruthy();
  9   |   const content = await response.json();
  10  |   await page.route(FEED, route => route.fulfill({
  11  |     status: 200,
  12  |     contentType: 'application/json',
  13  |     headers: { 'access-control-allow-origin': '*' },
  14  |     body: JSON.stringify(content),
  15  |   }));
  16  | }
  17  | 
  18  | test('the four principles show distinct in-page pixel sigils, with no raster images or placeholder frames', async ({ page, request }) => {
  19  |   await pinnedFeed(page, request);
  20  |   for (const width of [390, 1440, 1720]) {
  21  |     await page.setViewportSize({ width, height: 900 });
  22  |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  23  |     const cards = page.locator('.astrid-vision-standards-list > li');
  24  |     await expect(cards).toHaveCount(4);
  25  |     const sigils = cards.locator('.astrid-vision-principle-sigil');
  26  |     await expect(sigils).toHaveCount(4);
  27  |     await expect(sigils.locator('svg[viewBox="0 0 40 40"]')).toHaveCount(4);
  28  |     await expect(sigils.locator('img')).toHaveCount(0);
  29  |     const colors = await sigils.evaluateAll(elements =>
  30  |       elements.map(element => getComputedStyle(element).color));
  31  |     expect(new Set(colors).size).toBe(4);
  32  |     const structure = [
  33  |       '.astrid-vision-sigil-orbit',
  34  |       '.astrid-vision-sigil-open-ring',
  35  |       '.astrid-vision-sigil-hand',
  36  |       '.astrid-vision-sigil-knot',
  37  |     ];
  38  |     for (let index = 0; index < 4; index++) {
  39  |       await expect(cards.nth(index).locator(structure[index])).toHaveCount(1);
  40  |       const mark = await sigils.nth(index).boundingBox();
  41  |       const card = await cards.nth(index).boundingBox();
  42  |       expect(mark).not.toBeNull();
  43  |       expect(card).not.toBeNull();
  44  |       expect(mark!.x).toBeGreaterThanOrEqual(card!.x);
  45  |       expect(mark!.x + mark!.width).toBeLessThanOrEqual(card!.x + card!.width);
  46  |     }
  47  |     expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width + 1);
  48  |   }
  49  | });
  50  | 
  51  | test('each principle animates a different part of its sigil on hover and respects reduced motion', async ({ page, request }) => {
  52  |   await pinnedFeed(page, request);
  53  |   await page.setViewportSize({ width: 1720, height: 900 });
  54  |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  55  |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  56  |   const cards = page.locator('.astrid-vision-standards-list > li');
  57  |   const motions = [
  58  |     ['.astrid-vision-sigil-orbit', 'astrid-vision-sigil-orbit'],
  59  |     ['.astrid-vision-sigil-open-ring', 'astrid-vision-sigil-ring'],
  60  |     ['.astrid-vision-sigil-spark', 'astrid-vision-sigil-spark-rise'],
  61  |   ] as const;
  62  |   for (let i = 0; i < motions.length; i++) {
  63  |     await cards.nth(i).hover();
  64  |     await expect(cards.nth(i).locator(motions[i][0])).toHaveCSS('animation-name', motions[i][1]);
  65  |   }
  66  |   await page.emulateMedia({ reducedMotion: 'reduce' });
  67  |   for (let i = 0; i < motions.length; i++) {
  68  |     await expect(cards.nth(i).locator(motions[i][0])).toHaveCSS('animation-name', 'none');
  69  |   }
  70  | });
  71  | 
  72  | test('technical wrangling takes three seconds to resolve and one second to return', async ({ page, request }) => {
  73  |   await pinnedFeed(page, request);
  74  |   await page.setViewportSize({ width: 1720, height: 900 });
  75  |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  76  |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  77  |   const card = page.locator('.astrid-vision-standards-list > li').last();
  78  |   const knot = card.locator('.astrid-vision-sigil-knot');
  79  |   const fragments = card.locator('.astrid-vision-sigil-knot-fragments');
  80  |   const arrow = card.locator('.astrid-vision-sigil-clear-path');
> 81  |   await expect(card).toBeVisible();
      |                      ^ Error: expect(locator).toBeVisible() failed
  82  |   await expect(knot).toHaveCSS('opacity', '1');
  83  |   await expect(fragments).toHaveCSS('opacity', '1');
  84  |   await expect(arrow).toHaveCSS('opacity', '0.26');
  85  |   for (const part of [knot, fragments, arrow]) {
  86  |     await expect(part).toHaveCSS('transition-duration', '1s');
  87  |     await expect(part).toHaveCSS('animation-name', 'none');
  88  |   }
  89  |   await card.hover();
  90  |   for (const part of [knot, fragments, arrow]) {
  91  |     await expect(part).toHaveCSS('transition-duration', '3s');
  92  |   }
  93  |   await page.waitForTimeout(450);
  94  |   const halfway = await card.evaluate(el => {
  95  |     const opacity = (selector: string) => Number(getComputedStyle(el.querySelector(selector)!).opacity);
  96  |     return {
  97  |       knot: opacity('.astrid-vision-sigil-knot'),
  98  |       fragments: opacity('.astrid-vision-sigil-knot-fragments'),
  99  |       arrow: opacity('.astrid-vision-sigil-clear-path'),
  100 |     };
  101 |   });
  102 |   for (const value of Object.values(halfway)) {
  103 |     expect(value).toBeGreaterThan(0);
  104 |     expect(value).toBeLessThan(1);
  105 |   }
  106 |   await expect(knot).toHaveCSS('opacity', '0.16', { timeout: 4500 });
  107 |   await expect(fragments).toHaveCSS('opacity', '0.16', { timeout: 4500 });
  108 |   await expect(arrow).toHaveCSS('opacity', '1', { timeout: 4500 });
  109 | 
  110 |   await page.mouse.move(0, 3);
  111 |   for (const part of [knot, fragments, arrow]) {
  112 |     await expect(part).toHaveCSS('transition-duration', '1s');
  113 |   }
  114 |   await page.waitForTimeout(330);
  115 |   const reversing = Number(await arrow.evaluate(el => getComputedStyle(el).opacity));
  116 |   expect(reversing).toBeGreaterThan(0);
  117 |   expect(reversing).toBeLessThan(1);
  118 |   await expect(arrow).toHaveCSS('opacity', '0.26', { timeout: 1800 });
  119 |   await expect(knot).toHaveCSS('opacity', '1', { timeout: 1800 });
  120 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  121 |   await expect(arrow).toHaveCSS('transition-duration', '0s');
  122 |   await expect(knot).toHaveCSS('transition-duration', '0s');
  123 | });
  124 | 
  125 | 
  126 | test('mobile hero gets breathing room and the editorial cues and pillar numbers use pixel type', async ({ page, request }) => {
  127 |   await pinnedFeed(page, request);
  128 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  129 |   for (const width of [390, 1440]) {
  130 |     await page.setViewportSize({ width, height: 800 });
  131 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  132 |     const hero = page.locator('#astrid-vision-manifesto');
  133 |     const heroPadding = await hero.evaluate(el => Number.parseFloat(getComputedStyle(el).paddingTop));
  134 |     if (width === 390) expect(heroPadding).toBeGreaterThanOrEqual(34);
  135 |     else expect(heroPadding).toBeLessThan(20);
  136 |     const pixelNumbers = page.locator('.astrid-vision-pillar-number');
  137 |     await expect(pixelNumbers).toHaveCount(4);
  138 |     await expect(pixelNumbers.first()).toHaveCSS('font-family', /Departure Mono/);
  139 |     const arrows = page.locator('.astrid-vision-standards-list > li .astrid-vision-principle-corner');
  140 |     await expect(arrows).toHaveCount(4);
  141 |     const cues = page.locator('.astrid-vision-principles .astrid-vision-pillar-details, .astrid-vision-standards-list .astrid-vision-principle-corner');
  142 |     await expect(cues).toHaveCount(8);
  143 |     for (let index = 0; index < 8; index++) {
  144 |       const cue = cues.nth(index);
  145 |       await expect(cue.locator('.astrid-vision-card-arrow svg[viewBox="0 0 18 18"]')).toHaveCount(1);
  146 |       await expect(cue).toHaveText(/\d+ gaps?.*\d+ projects?/i);
  147 |       await expect(cue).toHaveCSS('font-family', /Departure Mono/);
  148 |       await expect(cue).toHaveCSS('font-size', '11px');
  149 |       await expect(cue).toHaveCSS('border-top-width', '0px');
  150 |     }
  151 |     expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width + 1);
  152 |   }
  153 | });
  154 | 
  155 | test('pillars put the art on a stage above the copy, beside it in one column, with a left-aligned cue', async ({ page, request }) => {
  156 |   await pinnedFeed(page, request);
  157 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  158 |   for (const width of [390, 760, 800, 1179, 1280, 1440]) {
  159 |     await page.setViewportSize({ width, height: 900 });
  160 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  161 |     const cards = page.locator('.astrid-vision-principles > li');
  162 |     await expect(cards).toHaveCount(4);
  163 |     const items = await cards.evaluateAll(elements => elements.map(card => {
  164 |       const box = (selector: string) => card.querySelector(selector)!.getBoundingClientRect().toJSON();
  165 |       return {
  166 |         card: card.getBoundingClientRect().toJSON(),
  167 |         number: box('.astrid-vision-pillar-number'),
  168 |         heading: box('h3'),
  169 |         copy: box('p'),
  170 |         art: box('.astrid-vision-principle-art'),
  171 |         detail: box('.astrid-vision-pillar-details'),
  172 |       };
  173 |     }));
  174 |     const columns = width >= 1180 ? 4 : 2;
  175 |     const rowCount = 4 / columns;
  176 |     for (let i = 0; i < items.length; i++) {
  177 |       const item = items[i];
  178 |       expect(Math.abs(item.number.x - item.heading.x)).toBeLessThan(2);
  179 |       expect(Math.abs(item.heading.x - item.copy.x)).toBeLessThan(2);
  180 |       // The details cue sits under the copy on the same left edge, not off to the right.
  181 |       expect(Math.abs(item.detail.x - item.copy.x)).toBeLessThan(2);
```