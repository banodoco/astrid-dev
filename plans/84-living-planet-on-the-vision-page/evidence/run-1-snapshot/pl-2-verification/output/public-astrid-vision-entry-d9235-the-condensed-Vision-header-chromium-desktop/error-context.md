# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-entry.spec.ts >> paired scrolled desktop brand >> wordmark accompanies the mink from the condensed Vision header
- Location: tests/e2e/public-astrid-vision-entry.spec.ts:833:3

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
    3 × locator resolved to <html lang="en" data-astrid-navigation="ready" data-astrid-page-transition="vision" data-astrid-page-transition-style="shared">…</html>
      - unexpected value "attribute present"

```

```yaml
- document:
  - main
```

# Test source

```ts
  748 |           : page.getByRole('button', { name: 'See all ' + kind, exact: true });
  749 |         await opener.scrollIntoViewIfNeeded();
  750 |         await page.evaluate(() => {
  751 |           const original = HTMLDialogElement.prototype.showModal;
  752 |           const state = window as unknown as { steadyShade: { first?: Record<string, unknown>; frames: Record<string, unknown>[]; done: boolean } };
  753 |           state.steadyShade = { frames: [], done: false };
  754 |           HTMLDialogElement.prototype.showModal = function () {
  755 |             HTMLDialogElement.prototype.showModal = original;
  756 |             original.call(this);
  757 |             const read = () => {
  758 |               const shade = getComputedStyle(this, '::backdrop');
  759 |               return { ready: this.dataset.ready ?? null, progress: this.style.getPropertyValue('--vision-open-progress'),
  760 |                 shade: shade.backgroundColor, opacity: shade.opacity, transition: shade.transitionDuration,
  761 |                 animation: shade.animationName, native: getComputedStyle(this).opacity,
  762 |                 surface: getComputedStyle(this.querySelector('.astrid-vision-details-shell')!).opacity };
  763 |             };
  764 |             state.steadyShade.first = read();
  765 |             let count = 0;
  766 |             const tick = () => {
  767 |               if (!this.open) { state.steadyShade.done = true; return; }
  768 |               state.steadyShade.frames.push(read());
  769 |               if (++count < 40) requestAnimationFrame(tick);
  770 |               else state.steadyShade.done = true;
  771 |             };
  772 |             requestAnimationFrame(tick);
  773 |           };
  774 |         });
  775 |         if (width === 390) await opener.tap(); else await opener.click();
  776 |         const dialog = page.getByRole('dialog');
  777 |         await expect(dialog).toHaveAttribute('data-ready', 'true');
  778 |         await expect.poll(() => page.evaluate(() => (window as unknown as { steadyShade: { done: boolean } }).steadyShade.done), { timeout: 30000 }).toBe(true);
  779 |         const trace = await page.evaluate(() => (window as unknown as { steadyShade: { first: { ready: string | null; progress: string; shade: string; surface: string }; frames: { shade: string; opacity: string; native: string; transition: string; animation: string; surface: string }[] } }).steadyShade);
  780 |         records.push({ kind, trace });
  781 |         record(`steady-shade-${info.project.name}-${width}`, { source: feed.source, records });
  782 |         expect.soft(trace.first.ready, 'measure before panel readiness').toBeNull();
  783 |         expect.soft(trace.first.progress).toBe('0');
  784 |         expect.soft(trace.first.shade, 'native dimmer is already complete at showModal').toBe('rgba(22, 20, 18, 0.58)');
  785 |         expect.soft(trace.frames).toHaveLength(40);
  786 |         for (const frame of trace.frames) {
  787 |           expect.soft(frame.shade).toBe('rgba(22, 20, 18, 0.58)');
  788 |           expect.soft(frame.opacity).toBe('1');
  789 |           expect.soft(frame.native).toBe('1');
  790 |           expect.soft(frame.animation).toBe('none');
  791 |           expect.soft(frame.transition).toBe('0s');
  792 |         }
  793 |         expect.soft(trace.first.surface, 'the panel still has its own reveal').toBe('0');
  794 |         await expect(dialog.locator('.astrid-vision-details-shell')).toHaveCSS('opacity', '1');
  795 |         if (index === 0) {
  796 |           // Compare actual painted backdrop pixels, not just computed styles.
  797 |           // The top-left gutter is outside the surface at both widths.
  798 |           // Isolate the native dimmer from the intentional foreground/shadow fade.
  799 | await dialog.locator('.astrid-vision-details-shell').evaluate(node => (node as HTMLElement).style.opacity = '1');
  800 | const reference = await page.screenshot({ clip: { x: 0, y: 0, width: 8, height: 8 }, scale: 'css' });
  801 |           const painted = [];
  802 |           for (const state of [{ ready: false, progress: '0' }, { ready: true, progress: '0.5' }, { ready: true, progress: '1' }]) {
  803 |             await dialog.evaluate((node, state) => {
  804 |               if (state.ready) node.setAttribute('data-ready', 'true'); else node.removeAttribute('data-ready');
  805 |               (node as HTMLElement).style.setProperty('--vision-open-progress', state.progress);
  806 |             }, state);
  807 |             const pixels = await page.screenshot({ clip: { x: 0, y: 0, width: 8, height: 8 }, scale: 'css' });
  808 |             const unchanged = pixels.equals(reference);
  809 |             painted.push({ ...state, unchanged });
  810 |             expect.soft(unchanged, 'surface readiness/progress cannot change painted dimmer pixels').toBe(true);
  811 |           }
  812 |           record(`steady-shade-pixels-${info.project.name}-${width}`, painted);
  813 | await dialog.locator('.astrid-vision-details-shell').evaluate(node => (node as HTMLElement).style.removeProperty('opacity'));
  814 |           await page.screenshot({ path: `${folder}/steady-shade-${info.project.name}-${width}.png` });
  815 |         }
  816 |         await page.keyboard.press('Escape');
  817 |         await expect(page.locator('dialog.astrid-vision-details')).toHaveCount(0);
  818 |       }
  819 |     });
  820 |   });
  821 | }
  822 | 
  823 | 
  824 | type BrandFollowFrame = { minkY: number; wordY: number; minkTransform: string; wordTransform: string;
  825 |   minkDuration: string; wordDuration: string; minkCurve: string; wordCurve: string; wordOpacity: number; scroll: number; wordWidth: number; wordHeight: number;
  826 |   betaTransform: string; betaDuration: string; betaCurve: string; betaOpacity: number; minkWidth: number; minkHeight: number };
  827 | type BrandFollowBox = { x: number; y: number; width: number; height: number; right: number };
  828 | type BrandFollowTrace = { ready: boolean; done: boolean; error?: string; frames: BrandFollowFrame[];
  829 |   old?: { name: string; opacity: string; box: BrandFollowBox; mink: BrandFollowBox; headerWidth: number };
  830 |   incoming?: { names: string[]; word: BrandFollowBox; mink: BrandFollowBox; beta: BrandFollowBox } };
  831 | test.describe('paired scrolled desktop brand', () => {
  832 |   test.use({ isMobile: false, hasTouch: false, deviceScaleFactor: 1 });
  833 |   test('wordmark accompanies the mink from the condensed Vision header', async ({ page, request }, info) => {
  834 |     test.setTimeout(120000);
  835 |     const response = await request.get(FEED); expect(response.ok()).toBe(true);
  836 |     const feed = await response.json();
  837 |     await page.route(FEED, route => route.fulfill({ json: feed }));
  838 |     await page.setViewportSize({ width: 1440, height: 900 });
  839 |     await page.emulateMedia({ reducedMotion: 'no-preference' });
  840 |     await page.goto('/home', { waitUntil: 'domcontentloaded' });
  841 |     await expect(page.getByRole('link', { name: 'Vision', exact: true })).toBeVisible({ timeout: 30000 });
  842 |     const records = [];
  843 |     for (const [audience, fraction] of [['App', 1], ['App', .5], ['Agent', 1], ['Agent', .5]] as const) {
  844 |       await page.locator('.astrid-public-site').getByRole('button', { name: audience, exact: true }).click();
  845 |       await expect(page.locator('.astrid-public-site')).toHaveAttribute('data-audience', audience.toLowerCase());
  846 |       await page.getByRole('link', { name: 'Vision', exact: true }).click();
  847 |       await expect(page.locator('.astrid-vision-principles > li')).toHaveCount(4);
> 848 |       await expect(page.locator('html')).not.toHaveAttribute('data-astrid-page-transition');
      |                                              ^ Error: expect(locator).not.toHaveAttribute() failed
  849 |       await page.evaluate(fraction => window.scrollTo({ top: (document.documentElement.scrollHeight - innerHeight) * fraction,
  850 |         behavior: 'instant' }), fraction);
  851 |       const header = page.locator('.astrid-vision-bar');
  852 |       await expect(header).toHaveAttribute('data-condensed');
  853 |       await expect(header.locator('.astrid-vision-brand-name')).toHaveCSS('opacity', '0');
  854 |       await expect(header.locator('.astrid-vision-brand-name')).toHaveCSS('max-width', '0px');
  855 |       const before = await header.locator('.astrid-vision-brand').evaluate(node => ({
  856 |         width: node.getBoundingClientRect().width,
  857 |         mink: node.querySelector('img')!.getBoundingClientRect().toJSON(),
  858 |       }));
  859 |       await page.evaluate(() => {
  860 |         const state = window as unknown as { brandFollow: BrandFollowTrace };
  861 |         const trace: BrandFollowTrace = { ready: false, done: false, frames: [] };
  862 |         state.brandFollow = trace;
  863 |         type Native = { ready: Promise<void>; finished: Promise<void> };
  864 |         const doc = document as unknown as { startViewTransition: (update: () => void | Promise<void>) => Native };
  865 |         const original = doc.startViewTransition.bind(doc);
  866 |         doc.startViewTransition = update => {
  867 |           doc.startViewTransition = original;
  868 |           const name = document.querySelector<HTMLElement>('.astrid-vision-brand-name')!;
  869 |           const mink = document.querySelector<HTMLElement>('.astrid-vision-brand img')!;
  870 |           trace.old = { name: getComputedStyle(name).viewTransitionName, opacity: getComputedStyle(name).opacity,
  871 |             box: name.getBoundingClientRect().toJSON(), mink: mink.getBoundingClientRect().toJSON(),
  872 |             headerWidth: name.parentElement!.getBoundingClientRect().width };
  873 |           const transition = original(async () => {
  874 |             await update();
  875 |             const home = document.querySelector('.astrid-public-site[data-astrid-lifecycle="active"]')!;
  876 |             trace.incoming = {
  877 |               names: [home, ...home.querySelectorAll('*')].map(n => getComputedStyle(n).viewTransitionName)
  878 |                 .filter(n => n && n !== 'none'),
  879 |               word: home.querySelector('.astrid-brand-name')!.getBoundingClientRect().toJSON(),
  880 |               beta: home.querySelector('.astrid-beta')!.getBoundingClientRect().toJSON(),
  881 |               mink: home.querySelector('.astrid-brand-mink:not(.astrid-brand-mink-glint)')!.getBoundingClientRect().toJSON(),
  882 |             };
  883 |           });
  884 |           void transition.ready.then(() => {
  885 |             trace.ready = true;
  886 |             const sample = () => {
  887 |               if (trace.done) return;
  888 |               const root = document.documentElement;
  889 |               const mink = getComputedStyle(root, '::view-transition-group(astrid-brand-mink)');
  890 |               const word = getComputedStyle(root, '::view-transition-group(astrid-brand-name)');
  891 |               const image = getComputedStyle(root, '::view-transition-new(astrid-brand-name)');
  892 |               const beta = getComputedStyle(root, '::view-transition-group(astrid-brand-beta)');
  893 |               const betaImage = getComputedStyle(root, '::view-transition-new(astrid-brand-beta)');
  894 |               // Copy the moving transforms together before reading other live styles.
  895 |               const wordTransform = word.transform;
  896 |               const betaTransform = beta.transform;
  897 |               const minkTransform = mink.transform;
  898 |               trace.frames.push({ minkY: new DOMMatrix(minkTransform).f, wordY: new DOMMatrix(wordTransform).f,
  899 |                 minkTransform, wordTransform, minkWidth: Number.parseFloat(mink.width), minkHeight: Number.parseFloat(mink.height),
  900 |                 minkDuration: mink.animationDuration, wordDuration: word.animationDuration,
  901 |                 minkCurve: mink.animationTimingFunction, wordCurve: word.animationTimingFunction,
  902 |                 wordOpacity: Number(image.opacity), scroll: scrollY,
  903 |                 wordWidth: Number.parseFloat(word.width), wordHeight: Number.parseFloat(word.height),
  904 |                 betaTransform, betaDuration: beta.animationDuration,
  905 |                 betaCurve: beta.animationTimingFunction, betaOpacity: Number(betaImage.opacity) });
  906 |               requestAnimationFrame(sample);
  907 |             };
  908 |             sample();
  909 |           }, error => { trace.error = String(error); });
  910 |           void transition.finished.then(() => { trace.done = true; }, error => {
  911 |             trace.error = String(error); trace.done = true;
  912 |           });
  913 |           return transition;
  914 |         };
  915 |       });
  916 |       await page.getByRole('link', { name: 'Astrid home', exact: true }).click();
  917 |       await expect.poll(() => page.evaluate(() => (window as unknown as { brandFollow: BrandFollowTrace }).brandFollow.ready)).toBe(true);
  918 |       await page.waitForTimeout(350);
  919 |       await page.screenshot({ path: `${folder}/wordmark-moving-${info.project.name}-${audience}-${fraction}.png` });
  920 |       await expect.poll(() => page.evaluate(() => (window as unknown as { brandFollow: BrandFollowTrace }).brandFollow.done), { timeout: 15000 }).toBe(true);
  921 |       const trace = await page.evaluate(() => (window as unknown as { brandFollow: BrandFollowTrace }).brandFollow);
  922 |       records.push({ audience, fraction, before, trace });
  923 |       record(`wordmark-follow-${info.project.name}`, records);
  924 |       expect(trace.error).toBeUndefined();
  925 |       expect(trace.old!.name, 'the hidden wordmark needs an outgoing capture origin').toBe('astrid-brand-name');
  926 |       expect(trace.incoming!.names, 'Beta must travel separately from the settled page fade').toEqual(['astrid-brand-mink', 'astrid-brand-name', 'astrid-brand-beta']);
  927 |       expect(trace.old!.opacity, 'do not flash the collapsed header text before the transition').toBe('0');
  928 |       expect(trace.old!.box.width, 'avoid a zero-width wordmark morph').toBeGreaterThan(30);
  929 |       expect(Math.abs(trace.old!.headerWidth - before.width), 'no header expansion at capture').toBeLessThan(.5);
  930 |       for (const axis of ['x', 'y', 'width', 'height'] as const) expect(Math.abs(trace.old!.mink[axis] - before.mink[axis])).toBeLessThan(.5);
  931 |       expect(Math.abs(trace.old!.box.x - trace.old!.mink.right), 'wordmark starts beside the current mink').toBeLessThan(24);
  932 |       const frames = trace.frames.filter(f => f.minkTransform !== 'none' && f.wordTransform !== 'none'
  933 |         && f.minkDuration === '0.9s' && f.wordDuration === '0.9s');
  934 |       expect(frames.length).toBeGreaterThan(5);
  935 |       expect(new Set(frames.map(f => f.wordTransform)).size).toBeGreaterThan(4);
  936 |       const first = frames[0], last = frames.at(-1)!;
  937 |       expect(Math.abs(last.wordY - first.wordY)).toBeGreaterThan(30);
  938 |       expect(Math.abs(first.wordY - trace.old!.box.y)).toBeLessThan(5);
  939 |       expect(Math.abs(last.wordY - trace.incoming!.word.y)).toBeLessThan(2);
  940 |       for (const frame of frames) {
  941 |         expect(frame.scroll).toBe(0);
  942 |         expect(frame.wordCurve).toBe(frame.minkCurve);
  943 |         const minkProgress = (frame.minkY - first.minkY) / (last.minkY - first.minkY);
  944 |         const wordProgress = (frame.wordY - first.wordY) / (last.wordY - first.wordY);
  945 |         expect(Math.abs(wordProgress - minkProgress), 'wordmark and mink travel together').toBeLessThan(.04);
  946 |       }
  947 |       expect(frames.some(f => f.wordOpacity > .99)).toBe(true);
  948 |       const badgeFrames = frames.filter(f => f.betaTransform !== 'none' && f.betaDuration === '0.9s');
```