# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-polish.spec.ts >> mobile sigils share full-height alignment and the footer illustration needs no entrance
- Location: tests/e2e/public-astrid-vision-polish.spec.ts:181:1

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
  146 | 
  147 | test('optional aspiration commitments are separately collapsed and empty projects stay silent', async ({ page }, info) => {
  148 |   const feed = visionFixture();
  149 |   await page.route(FEED, route => route.fulfill({ json: feed }));
  150 |   await page.setViewportSize({ width: 390, height: 844 });
  151 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  152 |   await page.getByRole('button', { name: 'Explore Artistic ambition: gaps and projects' }).click();
  153 |   const dialog = page.getByRole('dialog');
  154 |   const aspirations = dialog.locator('.astrid-vision-details-characteristic');
  155 |   const first = aspirations.first();
  156 |   await expect(first.locator('.astrid-vision-guidance > summary')).toBeHidden();
  157 |   await first.locator(':scope > summary').click();
  158 |   const guidance = first.locator('.astrid-vision-guidance');
  159 |   await expect(guidance).not.toHaveAttribute('open', '');
  160 |   await expect(guidance.locator('.astrid-vision-guidance-body')).toBeHidden();
  161 |   await guidance.locator('summary').focus();
  162 |   await page.keyboard.press('Enter');
  163 |   await expect(guidance.locator('.astrid-vision-guidance-body')).toBeVisible();
  164 |   await expect(guidance.locator('strong')).toHaveText(['We should:', 'We should never:']);
  165 |   await expect(guidance.locator('ul')).toHaveCount(2);
  166 |   await page.keyboard.press('Space');
  167 |   await expect(guidance.locator('.astrid-vision-guidance-body')).toBeHidden();
  168 |   await expect(first).toHaveAttribute('open', '');
  169 |   await expect(aspirations.nth(1).locator('.astrid-vision-guidance')).toHaveCount(0);
  170 |   const emptyGap = dialog.locator('[data-gap-id="AA-002"]');
  171 |   await emptyGap.locator(':scope > summary').click();
  172 |   await expect(emptyGap.locator('.astrid-vision-details-gap-description')).toBeVisible();
  173 |   await expect(emptyGap.locator('.astrid-vision-details-projects, .astrid-vision-details-empty')).toHaveCount(0);
  174 |   await expect(dialog.getByText('No current projects linked yet.', { exact: true })).toHaveCount(0);
  175 |   mkdirSync(folder, { recursive: true });
  176 |   await guidance.locator('summary').click();
  177 |   await guidance.scrollIntoViewIfNeeded();
  178 |   await page.screenshot({ path: `${folder}/fixture-optional-guidance-${info.project.name}.png` });
  179 | });
  180 | 
  181 | test('mobile sigils share full-height alignment and the footer illustration needs no entrance', async ({ page }, info) => {
  182 |   const feed = await pinLive(page);
  183 |   await page.setViewportSize({ width: 390, height: 844 });
  184 |   await page.emulateMedia({ reducedMotion: 'no-preference' });
  185 |   await page.goto('/vision', { waitUntil: 'domcontentloaded' });
> 186 |   await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
      |                                                                ^ Error: expect(locator).toHaveCount(expected) failed
  187 |   await page.evaluate(() => document.fonts.ready);
  188 |   const visual = page.locator('.astrid-vision-tinkerer');
  189 |   expect(await visual.evaluate(node => {
  190 |     for (let current: Element | null = node; current; current = current.parentElement) {
  191 |       if (current.hasAttribute('data-reveal') || getComputedStyle(current).opacity !== '1') return false;
  192 |     }
  193 |     return true;
  194 |   })).toBe(true);
  195 |   const underline = page.locator('#astrid-vision-title .pixel-underline');
  196 |   await expect(underline).toHaveText('artistic potential');
  197 |   await expect(underline.locator('svg')).toHaveAttribute('shape-rendering', 'crispEdges');
  198 |   await expect(underline.locator('path')).toHaveAttribute('stroke-linecap', 'square');
  199 |   await expect(page.locator('#astrid-vision-title')).toHaveText(feed.vision.title);
  200 |   await expect(page.locator('#astrid-vision-standards-title')).toHaveText('What guides us');
  201 |   await expect(page.locator('#astrid-vision-north-star-title')).toHaveText('What we’re building');
  202 |   await page.emulateMedia({ reducedMotion: 'reduce' });
  203 |   const cards = page.locator('.astrid-vision-standards-list > li');
  204 |   const layouts = await cards.evaluateAll(nodes => nodes.map(card => {
  205 |     const sigil = card.querySelector('.astrid-vision-principle-sigil')!;
  206 |     return { card: card.getBoundingClientRect().toJSON(), sigil: sigil.getBoundingClientRect().toJSON() };
  207 |   }));
  208 |   for (const { card, sigil } of layouts) {
  209 |     expect(Math.abs(sigil.y - card.y)).toBeLessThan(2);
  210 |     expect(Math.abs(sigil.height - card.height)).toBeLessThan(3);
  211 |     expect(Math.abs(card.x + card.width - sigil.x - sigil.width - 9)).toBeLessThan(2);
  212 |   }
  213 |   expect(Math.max(...layouts.map(x => x.sigil.height)) - Math.min(...layouts.map(x => x.sigil.height))).toBeLessThan(2);
  214 |   mkdirSync(folder, { recursive: true });
  215 |   await page.locator('.astrid-vision-manifesto').screenshot({ path: `${folder}/real-pixel-hero-${info.project.name}.png` });
  216 |   await page.locator('.astrid-vision-standards').screenshot({ path: `${folder}/real-aligned-sigils-${info.project.name}.png` });
  217 |   await page.locator('.astrid-vision-contribute').screenshot({ path: `${folder}/real-static-footer-${info.project.name}.png` });
  218 | });
  219 | 
  220 | 
  221 | for (const width of [390, 1440]) {
  222 |   test(`principles retain four translucent colour identities and readable text at ${width}px`, async ({ page }, info) => {
  223 |     const feed = await pinLive(page);
  224 |     await page.setViewportSize({ width, height: 900 });
  225 |     await page.emulateMedia({ reducedMotion: 'reduce' });
  226 |     await page.goto('/vision', { waitUntil: 'domcontentloaded' });
  227 |     const cards = page.locator('.astrid-vision-standards-list > li');
  228 |     await expect(cards).toHaveCount(4);
  229 |     await page.evaluate(() => document.fonts.ready);
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
```