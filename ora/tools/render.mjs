#!/usr/bin/env node
// ORA — rendu des gabarits HTML en PNG (image) ou MP4 (motion).
//
//   node ora/tools/render.mjs <page.html> <sortie.png>
//   node ora/tools/render.mjs <page.html> <sortie.mp4> [--fps 30]
//   node ora/tools/render.mjs <logo.svg>  <sortie.png> --width 1024
//
// La page doit contenir un élément #canvas (taille du visuel).
// Pour la vidéo, la page expose window.ORA_DURATION (s) et window.oraSeek(t) ;
// elle est chargée avec ?render pour couper la lecture automatique.
// Une page animée rendue en PNG est figée sur sa dernière image.
// Sortie : sRGB, PNG ; MP4 H.264 yuv420p (compatible Instagram/TikTok/WhatsApp).

import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const [, , input, output, ...rest] = process.argv;
if (!input || !output) {
  console.error('Usage : node render.mjs <page.html|logo.svg> <sortie.png|sortie.mp4> [--fps 30] [--width N]');
  process.exit(1);
}
const opt = (name, def) => {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 ? Number(rest[i + 1]) : def;
};

// L'entrée peut porter des paramètres : page.html?n=90°&l=...
const [inFile, inQuery = ''] = input.split('?');
const url = 'file://' + path.resolve(inFile);
const query = new URLSearchParams(inQuery);
query.set('render', '1');
const browser = await chromium.launch();

try {
  if (inFile.endsWith('.svg')) {
    // Export PNG transparent d'un logo à une largeur donnée.
    const width = opt('width', 1024);
    const svg = fs.readFileSync(inFile, 'utf8');
    const [, , , vw, vh] = svg.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
    const height = Math.round(width * Number(vh) / Number(vw));
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.goto(url); // SVG sans width/height : il remplit la fenêtre, au bon ratio
    await page.screenshot({ path: output, omitBackground: true, clip: { x: 0, y: 0, width, height } });
  } else {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    const video = output.endsWith('.mp4');
    await page.goto(url + '?' + query.toString());
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(() => window.ORA_READY !== false); // pages à chargement asynchrone
    const canvas = page.locator('#canvas');
    const box = await canvas.boundingBox();
    await page.setViewportSize({ width: Math.ceil(box.width), height: Math.ceil(box.height) });

    if (!video) {
      // Page animée : on fige la dernière image.
      await page.evaluate(() => window.oraSeek && window.oraSeek(window.ORA_DURATION || 0));
      await canvas.screenshot({ path: output });
    } else {
      const fps = opt('fps', 30);
      const duration = await page.evaluate(() => window.ORA_DURATION);
      if (!duration) throw new Error('window.ORA_DURATION absent : la page n’est pas animable.');
      const frames = Math.round(duration * fps);
      const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
        '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'slow',
        '-movflags', '+faststart', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
        output], { stdio: ['pipe', 'inherit', 'inherit'] });
      for (let i = 0; i < frames; i++) {
        await page.evaluate(t => window.oraSeek(t), i / fps);
        const buf = await canvas.screenshot({ type: 'png' });
        if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      }
      ff.stdin.end();
      const code = await new Promise(r => ff.on('close', r));
      if (code !== 0) throw new Error(`ffmpeg a échoué (code ${code})`);
    }
  }
  console.log('OK', output);
} finally {
  await browser.close();
}
