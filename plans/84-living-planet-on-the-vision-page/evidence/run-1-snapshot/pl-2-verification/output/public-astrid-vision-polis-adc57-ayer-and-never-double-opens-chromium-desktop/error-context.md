# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-polish.spec.ts >> opening prepares viewport before the native top layer and never double-opens
- Location: tests/e2e/public-astrid-vision-polish.spec.ts:19:1

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
  1   | import { expect, test, type Page } from '@playwright/test';
  2   | import { mkdirSync, writeFileSync } from 'node:fs';
  3   | import type { PublicVisionContent } from '../../src/pages/Home/publicVisionContent';
  4   | import { visionFixture } from '../fixtures/public-vision';
  5   | 
  6   | const FEED = 'https://raw.githubusercontent.com/banodoco/astrid-dev/vision-published/vision.json';
  7   | const folder = 'test-results/vision-captures';
  8   | 
  9   | async function pinLive(page: Page) {
  10  |   const response = await page.request.get(FEED);
  11  |   expect(response.ok()).toBeTruthy();
  12  |   const feed = await response.json() as PublicVisionContent;
  13  |   await page.route(FEED, route => route.fulfill({ json: feed }));
  14  |   return feed;
  15  | }
  16  | 
  17  | // This also runs against the previous source in the focused baseline reproduction.
  18  | // It measures real native-dialog opening; it is not an iPhone toolbar simulation.
  19  | test('opening prepares viewport before the native top layer and never double-opens', async ({ page }, info) => {
  20  |   const feed = await pinLive(page);
  21  |   await page.setViewportSize({ width: 390, height: 844 });
  22  |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  23  |   await page.addInitScript(() => {
  24  |     type Opening = { prepared: boolean; autofocus: boolean; frames: { y: number; height: number; scroll: number }[] };
  25  |     const state = window as typeof window & { __visionOpenings: Opening[] };
  26  |     state.__visionOpenings = [];
  27  |     const original = HTMLDialogElement.prototype.showModal;
  28  |     HTMLDialogElement.prototype.showModal = function () {
  29  |       const record: Opening = {
  30  |         prepared: !!this.style.getPropertyValue('--vision-viewport-height') && !!this.style.getPropertyValue('--vision-viewport-top'),
  31  |         autofocus: !!this.querySelector('h2[autofocus]'), frames: [],
  32  |       };
  33  |       state.__visionOpenings.push(record);
  34  |       original.call(this);
  35  |       const sample = () => {
  36  |         if (!this.open) return;
  37  |         const b = this.getBoundingClientRect();
  38  |         record.frames.push({ y: b.y, height: b.height, scroll: this.querySelector('.astrid-vision-details-scroll')!.scrollTop });
  39  |         if (record.frames.length < 12) requestAnimationFrame(sample);
  40  |       };
  41  |       sample();
  42  |     };
  43  |   });
  44  |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
> 45  |   await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
      |                                                                ^ Error: expect(locator).toHaveCount(expected) failed
  46  |   await page.evaluate(() => document.fonts.ready);
  47  |   const names = [
  48  |     'Explore ' + feed.pillars[0].title + ': gaps and projects',
  49  |     'Explore ' + feed.principles[3].title + ': gaps and projects',
  50  |     'See all projects', 'See all gaps',
  51  |   ];
  52  |   for (const [index, name] of [...names, names[0]].entries()) {
  53  |     const opener = page.getByRole('button', { name, exact: true });
  54  |     await opener.scrollIntoViewIfNeeded();
  55  |     const before = await page.evaluate(() => window.scrollY);
  56  |     await opener.evaluate(node => {
  57  |       node.addEventListener('pointerdown', () => {
  58  |         (window as typeof window & { __openerScroll?: number }).__openerScroll = window.scrollY;
  59  |       }, { once: true, capture: true });
  60  |     });
  61  |     await opener.click();
  62  |     const dialog = page.getByRole('dialog');
  63  |     await expect(dialog).toBeVisible();
  64  |     await expect(dialog.locator('h2')).toBeFocused();
  65  |     await expect.poll(() => page.evaluate(i => {
  66  |       const log = (window as typeof window & { __visionOpenings: { frames: unknown[] }[] }).__visionOpenings;
  67  |       return log[i]?.frames.length ?? 0;
  68  |     }, index)).toBe(12);
  69  |     const log = await page.evaluate(() => (window as typeof window & {
  70  |       __visionOpenings: { prepared: boolean; autofocus: boolean; frames: { y: number; height: number; scroll: number }[] }[];
  71  |     }).__visionOpenings);
  72  |     // Keep the frame trace even when a first-paint regression fails below.
  73  |     mkdirSync(folder, { recursive: true });
  74  |     writeFileSync(`${folder}/opening-frames-${info.project.name}.json`,
  75  |       JSON.stringify({ source: feed.source, openings: log }, null, 2));
  76  |     expect(log).toHaveLength(index + 1);
  77  |     expect(log[index].prepared).toBe(true);
  78  |     expect(log[index].autofocus).toBe(true);
  79  |     const frames = log[index].frames;
  80  |     expect(Math.max(...frames.map(f => f.y)) - Math.min(...frames.map(f => f.y))).toBeLessThan(2);
  81  |     expect(Math.max(...frames.map(f => f.height)) - Math.min(...frames.map(f => f.height))).toBeLessThan(2);
  82  |     expect(frames.every(f => f.scroll === 0)).toBe(true);
  83  |     expect(await dialog.evaluate(node => getComputedStyle(node, '::backdrop').backdropFilter)).toBe('none');
  84  |     await dialog.getByRole('button', { name: 'Close details' }).click();
  85  |     await expect(dialog).toHaveCount(0);
  86  |     writeFileSync(`${folder}/closing-restoration-${info.project.name}-${index}.json`, JSON.stringify({ before, state: await page.evaluate(() => ({ scrollY: window.scrollY, openerScroll: (window as typeof window & { __openerScroll?: number }).__openerScroll, maxScroll: document.documentElement.scrollHeight - window.innerHeight, active: document.activeElement?.outerHTML.slice(0, 300), body: document.body.getAttribute('style') })) }, null, 2));
  87  |     // Playwright may scroll again while making the opener actionable. The
  88  |     // modal must restore the page position at the actual opening gesture,
  89  |     // not the earlier scrollIntoView helper's intermediate position.
  90  |     const openedAt = await page.evaluate(() => (window as typeof window & { __openerScroll?: number }).__openerScroll);
  91  |     expect(typeof openedAt).toBe('number');
  92  |     await expect.poll(() => page.evaluate(() => window.scrollY)).toBeCloseTo(openedAt!, 0);
  93  |   }
  94  |   mkdirSync(folder, { recursive: true });
  95  |   writeFileSync(`${folder}/opening-frames-${info.project.name}.json`, JSON.stringify({ source: feed.source,
  96  |     openings: await page.evaluate(() => (window as typeof window & { __visionOpenings: unknown }).__visionOpenings) }, null, 2));
  97  | });
  98  | 
  99  | for (const width of [390, 1440]) {
  100 |   test(`quiet arrows, intro rule and direct project links at ${width}px`, async ({ page }, info) => {
  101 |     const feed = await pinLive(page);
  102 |     await page.setViewportSize({ width, height: 900 });
  103 |     await page.emulateMedia({ reducedMotion: 'reduce' });
  104 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  105 |     await page.getByRole('button', { name: 'Explore ' + feed.pillars[0].title + ': gaps and projects', exact: true }).click();
  106 |     const dialog = page.getByRole('dialog');
  107 |     await page.mouse.move(0, 0);
  108 |     const enabled = dialog.locator('.astrid-vision-details-next');
  109 |     const disabled = dialog.locator('.astrid-vision-details-previous');
  110 |     await expect(enabled).toBeEnabled();
  111 |     await expect(disabled).toBeDisabled();
  112 |     await expect(enabled).toHaveCSS('opacity', '0.36');
  113 |     await expect(disabled).toHaveCSS('opacity', '0.25');
  114 |     await expect(enabled).toHaveCSS('border-top-width', '2px');
  115 |     await expect(disabled).toHaveCSS('border-top-width', '1px');
  116 |     await expect(enabled.locator('svg')).toHaveCSS('stroke-width', '3px');
  117 |     await expect(disabled.locator('svg')).toHaveCSS('stroke-width', '1.5px');
  118 |     const intro = dialog.locator('.astrid-vision-details-description');
  119 |     await expect(intro).toHaveCSS('border-bottom-width', '1px');
  120 |     const introBox = (await intro.boundingBox())!;
  121 |     const restBox = (await dialog.locator('.astrid-vision-details-characteristics').boundingBox())!;
  122 |     expect(restBox.y - introBox.y - introBox.height).toBeGreaterThanOrEqual(20);
  123 |     mkdirSync(folder, { recursive: true });
  124 |     await page.screenshot({ path: `${folder}/real-polished-popup-${info.project.name}-${width}.png` });
  125 |     await page.keyboard.press('Escape');
  126 |     const gap = feed.gaps.find(g => g.assessment !== 'closed' && g.aspiration && g.primaryAppliesTo?.startsWith('pillar:') &&
  127 |       feed.projects.some(p => (p.primaryGapId ?? p.gapIds[0]) === g.id))!;
  128 |     const pillar = feed.pillars.find(p => 'pillar:' + p.id === gap.primaryAppliesTo)!;
  129 |     await page.getByRole('button', { name: 'Explore ' + pillar.title + ': gaps and projects', exact: true }).click();
  130 |     const row = dialog.locator(`[data-gap-id="${gap.id}"]`);
  131 |     await row.locator(':scope > summary').click();
  132 |     const cards = row.locator('.astrid-vision-project');
  133 |     expect(await cards.count()).toBeGreaterThan(0);
  134 |     await expect(cards.locator('summary, details, .astrid-vision-project-body, .astrid-vision-project-metadata')).toHaveCount(0);
  135 |     for (const card of await cards.all()) {
  136 |       await expect(card.locator('.astrid-vision-project-title')).not.toBeEmpty();
  137 |       await expect(card.locator('.astrid-vision-project-intro')).not.toBeEmpty();
  138 |       await expect(card.getByRole('link', { name: /^Read the full project plan:/ })).toBeVisible();
  139 |     }
  140 |     await expect(dialog.getByText('No current projects linked yet.', { exact: true })).toHaveCount(0);
  141 |     await row.scrollIntoViewIfNeeded();
  142 |     await page.screenshot({ path: `${folder}/real-direct-project-links-${info.project.name}-${width}.png` });
  143 |     writeFileSync(`${folder}/polish-${info.project.name}-${width}-source.json`, JSON.stringify(feed.source));
  144 |   });
  145 | }
```