// Exporte chaque .slide en PNG 1080 x 1350 et signale tout débordement de texte.
// Usage : node export.cjs carrousels.html ../../../exports/2026-10-23_carrousels
const { chromium } = require('playwright');
const path = require('node:path');
const [, , page, outDir] = process.argv;
(async () => {
  const browser = await chromium.launch();
  const p = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(page));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const report = await p.evaluate(() => [...document.querySelectorAll('.slide')].map(s => {
    const z = s.querySelector('.zone');
    const fonts = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight);
    return { name: s.dataset.name, overflow: z.scrollHeight - z.clientHeight, fonts: [...new Set(fonts)].join(', ') };
  }));
  const slides = await p.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: path.join(outDir, report[i].name + '.png') });
    console.log(report[i].name, report[i].overflow > 0 ? `DÉBORDEMENT ${report[i].overflow}px` : 'ok');
  }
  console.log('polices chargées :', report[0].fonts);
  await browser.close();
})();
