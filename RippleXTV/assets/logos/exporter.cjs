// Exporte les PNG à partir des SVG du dossier (Playwright + Chromium).
// Usage : node exporter.cjs
const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');
const jobs = [
  // [svg, png, hauteur en px, fond transparent]
  ['RXTV_monogramme_blanc_v01.svg', 'RXTV_monogramme_blanc_v01.png', 2048, true],
  ['RXTV_monogramme_noir_v01.svg', 'RXTV_monogramme_noir_v01.png', 2048, true],
  ['RXTV_avatar_blanc-sur-noir_v01.svg', 'RXTV_avatar_blanc-sur-noir_v01.png', 1080, false],
  ['RXTV_avatar_noir-sur-cobalt_v01.svg', 'RXTV_avatar_noir-sur-cobalt_v01.png', 1080, false],
  ['RXTV_monogramme_plan-construction_v01.svg', 'RXTV_monogramme_plan-construction_v01.png', 1400, false],
];
(async () => {
  const browser = await chromium.launch();
  for (const [svg, png, h, transparent] of jobs) {
    const src = fs.readFileSync(path.join(__dirname, svg), 'utf8');
    const [, , , vw, vh] = src.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/).map(Number);
    const w = Math.round(h * vw / vh);
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    await page.goto('file://' + path.join(__dirname, svg));
    await page.evaluate(([w, h]) => {
      const svg = document.documentElement;
      svg.setAttribute('width', w);
      svg.setAttribute('height', h);
    }, [w, h]);
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(__dirname, png), omitBackground: transparent });
    await page.close();
    console.log(png, `${w}x${h}`);
  }
  await browser.close();
})();
