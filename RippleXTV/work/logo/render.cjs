// Usage : node render.cjs page.html sortie.png [largeur] [échelle]
const { chromium } = require('playwright');
const path = require('node:path');
const [, , page, out, width = '1600', dsf = '1'] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: +width, height: 400 }, deviceScaleFactor: +dsf });
  const p = await ctx.newPage();
  await p.goto('file://' + path.resolve(page));
  await p.waitForTimeout(500);
  await p.screenshot({ path: out, fullPage: true });
  await browser.close();
})();
