// Exporte les deux canevas 1080 x 1920 puis la planche annotée.
const { chromium } = require('playwright');
const path = require('node:path');
const out = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1900, height: 2200 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve('exemple.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const lines = await p.$$eval('.st p', ps => ps.map(e => Math.round(e.getBoundingClientRect().height / (44 * 1.2))));
  console.log('lignes de sous-titres (A, B) :', lines.join(', '));
  const a = path.join(out, 'RXTV_FR_Exemple_VIDEO-EXTRAIT_fr_v01.png');
  const bb = path.join(out, 'RXTV_FR_Exemple_VIDEO-PLEIN-CADRE_fr_v01.png');
  await (await p.$('#A')).screenshot({ path: a });
  await (await p.$('#B')).screenshot({ path: bb });
  await p.evaluate(([a, bb]) => { imgA.src = 'file://' + a; imgB.src = 'file://' + bb; }, [a, bb]);
  await p.waitForTimeout(400);
  await (await p.$('#planche')).screenshot({ path: path.join(out, 'RXTV_FR_Exemple_planche-habillage_fr_v01.png') });
  await b.close();
})();
