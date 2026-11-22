# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-mobile-catalogs.spec.ts >> legacy section bookmarks open the right dialog and leave no dead hash on dismissal
- Location: tests/e2e/public-astrid-vision-mobile-catalogs.spec.ts:103:1

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByRole('dialog', { name: 'All gaps' })
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByRole('dialog', { name: 'All gaps' })

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
  6   | const FEED = 'https://raw.githubusercontent.com/banodoco/astrid-dev/vision-published/vision.json';
  7   | const folder = 'test-results/vision-captures';
  8   | 
  9   | async function expectContained(page: Page, width: number) {
  10  |   expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width + 1);
  11  |   const dialog = page.getByRole('dialog');
  12  |   const bounds = await dialog.boundingBox();
  13  |   expect(bounds).not.toBeNull();
  14  |   expect(bounds!.x).toBeGreaterThanOrEqual(-1);
  15  |   expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(width + 1);
  16  |   expect(bounds!.y).toBeGreaterThanOrEqual(0);
  17  |   expect(bounds!.y + bounds!.height).toBeLessThanOrEqual(901);
  18  |   if (width <= 760) {
  19  |     expect(Math.abs(bounds!.x)).toBeLessThan(1);
  20  |     expect(Math.abs(bounds!.width - width)).toBeLessThan(1);
  21  |     expect(await dialog.evaluate(el => Number.parseFloat(getComputedStyle(el).maxHeight))).toBeGreaterThan(830);
  22  |   }
  23  | }
  24  | 
  25  | for (const width of [320, 390, 760, 1440]) {
  26  |   test(`real vision grid, counts and on-demand catalogs at ${width}px`, async ({ page, request }, info) => {
  27  |     const response = await request.get(FEED);
  28  |     expect(response.ok()).toBeTruthy();
  29  |     const feed = await response.json() as PublicVisionContent;
  30  |     await page.route(FEED, route => route.fulfill({ json: feed }));
  31  |     await page.emulateMedia({ reducedMotion: 'reduce' });
  32  |     await page.setViewportSize({ width, height: 900 });
  33  |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  34  |     const cards = page.locator('.astrid-vision-principles > li');
  35  |     await expect(cards).toHaveCount(4);
  36  |     await expect(page.locator('.astrid-vision-source-attribution')).toHaveText('Populated by the Astrid Dev repository.');
  37  |     await expect(page.locator('#astrid-vision-parts, #astrid-vision-projects')).toHaveCount(0);
  38  |     await expect(page.getByRole('navigation', { name: 'Vision page sections' }).getByRole('link')).toHaveCount(4);
  39  |     for (const [i, pillar] of feed.pillars.entries()) {
  40  |       const hierarchy = aspirationsForSubject(feed, { kind: 'pillar', id: pillar.id });
  41  |       const groups = [...hierarchy.aspirations.flatMap(item => item.gaps), ...hierarchy.legacyGaps];
  42  |       const gaps = new Set(groups.map(item => item.gap.id)).size;
  43  |       const projects = new Set(groups.flatMap(item => item.projects.map(project => project.id))).size;
  44  |       await expect(cards.nth(i).locator('.astrid-vision-subject-counts'))
  45  |         .toHaveText(`${hierarchy.aspirations.length} ${hierarchy.aspirations.length === 1 ? 'goal' : 'goals'} · ${gaps} ${gaps === 1 ? 'gap' : 'gaps'} · ${projects} ${projects === 1 ? 'project' : 'projects'}`);
  46  |       await expect(cards.nth(i).locator('h3')).toHaveText(pillar.title);
  47  |       await expect(cards.nth(i).locator(':scope > p')).toHaveText(pillar.descriptor);
  48  |       expect(await cards.nth(i).evaluate(node => node.scrollWidth <= node.clientWidth + 1)).toBe(true);
  49  |     }
  50  |     const boxes = await cards.evaluateAll(nodes => nodes.map(node => node.getBoundingClientRect().toJSON()));
  51  |     if (width <= 760) {
  52  |       expect(Math.abs(boxes[0].y - boxes[1].y)).toBeLessThan(2);
  53  |       expect(Math.abs(boxes[2].y - boxes[3].y)).toBeLessThan(2);
  54  |       expect(boxes[1].x).toBeGreaterThan(boxes[0].x + boxes[0].width);
  55  |       expect(boxes[2].y).toBeGreaterThan(boxes[0].y + boxes[0].height);
  56  |       for (const card of await cards.all()) {
  57  |         const art = await card.locator('.astrid-vision-pillar-stage').boundingBox();
  58  |         const title = await card.locator('h3').boundingBox();
  59  |         expect(art!.y + art!.height).toBeLessThanOrEqual(title!.y + 1);
  60  |       }
  61  |       const principles = await page.locator('.astrid-vision-standards-list > li').evaluateAll(nodes =>
  62  |         nodes.map(node => node.getBoundingClientRect().toJSON()));
  63  |       for (let i = 1; i < principles.length; i++) {
  64  |         expect(principles[i].y - principles[i - 1].y - principles[i - 1].height).toBeGreaterThanOrEqual(15);
  65  |       }
  66  |     }
  67  |     mkdirSync(folder, { recursive: true });
  68  |     writeFileSync(`${folder}/mobile-catalogs-${info.project.name}-${width}-source.json`, JSON.stringify(feed.source));
  69  |     await page.locator('.astrid-vision-north-star').screenshot({ path: `${folder}/real-mobile-grid-${info.project.name}-${width}.png` });
  70  |     await cards.first().getByRole('button').click();
  71  |     await expectContained(page, width);
  72  |     await page.screenshot({ path: `${folder}/real-roomy-pillar-${info.project.name}-${width}.png` });
  73  |     await page.keyboard.press('Escape');
  74  |     await expect(page.getByRole('dialog')).toHaveCount(0);
  75  |     const contribution = page.locator('.astrid-vision-contribute');
  76  |     const copy = contribution.getByRole('button', { name: 'Copy instructions for agents', exact: true });
  77  |     const actions = contribution.locator('.astrid-vision-catalog-actions');
  78  |     await actions.scrollIntoViewIfNeeded();
  79  |     const copyBounds = await copy.boundingBox();
  80  |     const actionsBounds = await actions.boundingBox();
  81  |     expect(actionsBounds!.y).toBeGreaterThanOrEqual(copyBounds!.y + copyBounds!.height);
  82  |     await contribution.screenshot({ path: `${folder}/real-catalog-buttons-${info.project.name}-${width}.png` });
  83  |     for (const kind of ['projects', 'gaps'] as const) {
  84  |       const trigger = page.getByRole('button', { name: 'See all ' + kind, exact: true });
  85  |       await trigger.focus();
  86  |       await page.keyboard.press('Enter');
  87  |       const dialog = page.getByRole('dialog', { name: 'All ' + kind });
  88  |       await expect(dialog).toBeVisible();
  89  |       await expectContained(page, width);
  90  |       const selector = dialog.getByRole('combobox', { name: 'Filter ' + kind + ' by status' });
  91  |       await expect(selector).toHaveValue('all');
  92  |       const rows = dialog.locator(kind === 'projects' ? '.astrid-vision-project-row' : '.astrid-vision-part');
  93  |       await expect(rows).toHaveCount(feed[kind].length);
  94  |       await page.screenshot({ path: `${folder}/real-catalog-${kind}-${info.project.name}-${width}.png` });
  95  |       await page.keyboard.press('Escape');
  96  |       await expect(page.getByRole('dialog')).toHaveCount(0);
  97  |       await expect(trigger).toBeFocused();
  98  |       await expect(page.locator('#astrid-vision-parts, #astrid-vision-projects')).toHaveCount(0);
  99  |     }
  100 |   });
  101 | }
  102 | 
  103 | test('legacy section bookmarks open the right dialog and leave no dead hash on dismissal', async ({ page }) => {
  104 |   for (const [hash, label] of [['astrid-vision-parts', 'All gaps'], ['astrid-vision-projects', 'All projects']]) {
  105 |     await page.goto('/vision#' + hash, { waitUntil: 'domcontentloaded' });
> 106 |     await expect(page.getByRole('dialog', { name: label })).toBeVisible();
      |                                                             ^ Error: expect(locator).toBeVisible() failed
  107 |     await page.getByRole('button', { name: 'Close details' }).click();
  108 |     await expect(page.getByRole('dialog')).toHaveCount(0);
  109 |     // Native close removes the dialog from the accessibility tree before its
  110 |     // asynchronous close event finishes the route cleanup. Assert that outcome.
  111 |     await expect(page).toHaveURL(/\/vision$/);
  112 |   }
  113 | });
  114 | 
  115 | test('catalog backdrop consumes the closing tap without activating the button beneath', async ({ browser }) => {
  116 |   const context = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  117 |   const page = await context.newPage();
  118 |   try {
  119 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  120 |     await page.getByRole('button', { name: 'See all gaps', exact: true }).tap();
  121 |     // Closing gestures target the visible modal after its one-frame preparation.
  122 |     await expect(page.getByRole('dialog', { name: 'All gaps' })).toBeVisible();
  123 |     const behind = page.getByRole('button', { name: 'See all projects', exact: true });
  124 |     await behind.evaluate(node => {
  125 |       document.getElementById('root')!.appendChild(node);
  126 |       (node as HTMLElement).style.cssText = 'position:fixed;left:0;top:0;width:18px;height:6px;min-height:0;padding:0;z-index:2147483647;transform:none';
  127 |       node.addEventListener('click', () => node.setAttribute('data-test-clicked', 'true'));
  128 |     });
  129 |     await page.touchscreen.tap(4, 2);
  130 |     await expect(page.getByRole('dialog')).toHaveCount(0);
  131 |     await page.waitForTimeout(350);
  132 |     await expect(behind).not.toHaveAttribute('data-test-clicked', 'true');
  133 |     await page.touchscreen.tap(4, 2);
  134 |     await expect(page.getByRole('dialog', { name: 'All projects' })).toBeVisible();
  135 |   } finally {
  136 |     await context.close();
  137 |   }
  138 | });
  139 | 
  140 | 
  141 | async function expectReachableFrame(page: Page, width: number) {
  142 |   const dialog = page.getByRole('dialog');
  143 |   const header = dialog.locator('.astrid-vision-details-header');
  144 |   const frame = dialog.locator('.astrid-vision-details-scroll-frame');
  145 |   const close = dialog.getByRole('button', { name: 'Close details' });
  146 |   const [panelBox, headerBox, frameBox, closeBox] = await Promise.all([
  147 |     dialog.boundingBox(), header.boundingBox(), frame.boundingBox(), close.boundingBox(),
  148 |   ]);
  149 |   expect(panelBox).not.toBeNull(); expect(headerBox).not.toBeNull();
  150 |   expect(frameBox).not.toBeNull(); expect(closeBox).not.toBeNull();
  151 |   if (width <= 760) {
  152 |     expect(frameBox!.y + frameBox!.height).toBeLessThanOrEqual(headerBox!.y + 1);
  153 |     expect(Math.abs(headerBox!.y + headerBox!.height - panelBox!.y - panelBox!.height)).toBeLessThan(2);
  154 |     expect(closeBox!.y).toBeGreaterThan(page.viewportSize()!.height - 150);
  155 |     expect(closeBox!.width).toBeGreaterThanOrEqual(44);
  156 |     expect(closeBox!.height).toBeGreaterThanOrEqual(44);
  157 |   } else {
  158 |     expect(headerBox!.y + headerBox!.height).toBeLessThanOrEqual(frameBox!.y + 1);
  159 |   }
  160 |   const before = closeBox!.y;
  161 |   await dialog.locator('.astrid-vision-details-scroll').evaluate(node => { node.scrollTop = node.scrollHeight; });
  162 |   expect(Math.abs((await close.boundingBox())!.y - before)).toBeLessThan(1);
  163 |   expect(await dialog.evaluate(dialog => {
  164 |       const surfaces = Array.from(dialog.querySelectorAll<HTMLElement>('.astrid-vision-details-shell, .astrid-vision-details-scroll, .astrid-vision-details-scroll-inner'));
  165 |       return surfaces.length === 3 && surfaces.every(surface => surface.scrollWidth <= surface.clientWidth + 1)
  166 |         && document.documentElement.scrollWidth <= window.innerWidth + 1;
  167 |     })).toBe(true);
  168 | }
  169 | 
  170 | for (const width of [320, 390]) {
  171 |   test(`compact principles, text catalogs and reachable bottom controls at ${width}px`, async ({ page, request }, info) => {
  172 |     const response = await request.get(FEED);
  173 |     expect(response.ok()).toBeTruthy();
  174 |     const feed = await response.json() as PublicVisionContent;
  175 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  176 |     await page.emulateMedia({ reducedMotion: 'reduce' });
  177 |     await page.setViewportSize({ width, height: 844 });
  178 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  179 |     await page.evaluate(() => document.fonts.ready);
  180 |     const nav = page.getByRole('navigation', { name: 'Vision page sections' });
  181 |     await expect(nav.getByRole('link', { name: 'Help', exact: true })).toBeVisible();
  182 |     await expect(nav.getByRole('link', { name: 'Help us', exact: true })).toHaveCount(0);
  183 |     const cards = page.locator('.astrid-vision-standards-list > li');
  184 |     await cards.first().scrollIntoViewIfNeeded();
  185 |     // Measure after the wordmark has finished folding. The final link
  186 |     // shares the header's right inset, rather than leaving spare space.
  187 |     await expect.poll(async () => nav.evaluate(node => {
  188 |       const bar = node.closest('.astrid-vision-bar')!;
  189 |       const last = node.querySelector('a:last-child')!;
  190 |       return Math.abs(last.getBoundingClientRect().right -
  191 |         (bar.getBoundingClientRect().right - Number.parseFloat(getComputedStyle(bar).paddingRight)));
  192 |     })).toBeLessThan(2);
  193 |     for (const [index, principle] of feed.principles.entries()) {
  194 |       const card = cards.nth(index);
  195 |       const hierarchy = aspirationsForSubject(feed, { kind: 'principle', id: principle.id });
  196 |       const groups = [...hierarchy.aspirations.flatMap(item => item.gaps), ...hierarchy.legacyGaps];
  197 |       const gaps = new Set(groups.map(item => item.gap.id)).size;
  198 |       const projects = new Set(groups.flatMap(item => item.projects.map(project => project.id))).size;
  199 |       await expect(card.locator('.astrid-vision-subject-counts'))
  200 |         .toHaveText(`${hierarchy.aspirations.length} ${hierarchy.aspirations.length === 1 ? 'goal' : 'goals'} · ${gaps} ${gaps === 1 ? 'gap' : 'gaps'} · ${projects} ${projects === 1 ? 'project' : 'projects'}`);
  201 |       await expect(card.locator('h3')).toHaveText(principle.title);
  202 |       await expect(card.locator('.astrid-vision-principle-statement')).toHaveText(principle.statement!);
  203 |       const geometry = await card.evaluate(node => {
  204 |         const title = node.querySelector('h3')!;
  205 |         const copy = node.querySelector('.astrid-vision-principle-statement')!;
  206 |         const sigil = node.querySelector('.astrid-vision-principle-sigil')!;
```