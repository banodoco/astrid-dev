# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-sigils-nav.spec.ts >> the four principles show distinct in-page pixel sigils, with no raster images or placeholder frames
- Location: tests/e2e/public-astrid-vision-sigils-nav.spec.ts:18:1

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
> 24  |     await expect(cards).toHaveCount(4);
      |                         ^ Error: expect(locator).toHaveCount(expected) failed
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
  81  |   await expect(card).toBeVisible();
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
```