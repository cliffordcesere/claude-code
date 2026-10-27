#!/usr/bin/env node
/**
 * preflight.mjs — contrôle d'un fichier print avant envoi à l'imprimeur.
 *
 * Usage :
 *   node scripts/preflight.mjs affiche.pdf  --trim 297 420
 *   node scripts/preflight.mjs flyer.png    --trim 148 210 --dpi 300 --bleed 3
 *
 * Vérifie : présence du fond perdu, dimensions au format fini, DPI effectif,
 * espace colorimétrique. S'appuie sur ImageMagick (identify) et/ou poppler
 * (pdfinfo) ; sans ces outils, affiche les commandes à lancer à la main.
 *
 * Sortie : 0 = conforme, 1 = au moins un avertissement bloquant, 2 = outils absents.
 */

import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { extname } from 'node:path';

const MM_PER_INCH = 25.4;

function parseArgs(argv) {
  const out = { file: null, trim: null, dpi: 300, bleed: 3 };
  const rest = argv.slice(2);
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (a === '--trim') {
      out.trim = [Number(rest[++i]), Number(rest[++i])];
    } else if (a === '--dpi') {
      out.dpi = Number(rest[++i]);
    } else if (a === '--bleed') {
      out.bleed = Number(rest[++i]);
    } else if (!a.startsWith('--')) {
      out.file = a;
    }
  }
  return out;
}

function has(bin) {
  try {
    execFileSync('which', [bin], { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

function run(bin, args) {
  return execFileSync(bin, args, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
}

const results = [];
const push = (level, label, detail) => results.push({ level, label, detail });

function main() {
  const { file, trim, dpi, bleed } = parseArgs(process.argv);

  if (!file) {
    console.error('Usage : node scripts/preflight.mjs <fichier> --trim 297 420 [--dpi 300] [--bleed 3]');
    process.exit(2);
  }
  if (!existsSync(file)) {
    console.error(`Fichier introuvable : ${file}`);
    process.exit(1);
  }
  if (!trim || trim.some((n) => !Number.isFinite(n) || n <= 0)) {
    console.error('Indique le format fini : --trim <largeur_mm> <hauteur_mm>');
    process.exit(2);
  }

  const ext = extname(file).toLowerCase();
  const isPdf = ext === '.pdf';
  const expectedW = trim[0] + bleed * 2;
  const expectedH = trim[1] + bleed * 2;

  push("info", "Format fini visé", `${trim[0]} × ${trim[1]} mm`);
  push('info', 'Document attendu (avec fond perdu)', `${expectedW} × ${expectedH} mm`);

  if (isPdf) {
    if (!has('pdfinfo')) {
      push('warn', 'pdfinfo absent', 'Installe poppler-utils pour vérifier le PDF. Sinon : ouvrir le PDF, vérifier les traits de coupe et le fond perdu à l’œil.');
      push('info', 'Commande manuelle', 'pdfinfo -box ' + file);
    } else {
      const out = run('pdfinfo', ['-box', file]);
      const size = out.match(/Page size:\s+([\d.]+) x ([\d.]+) pts/);
      if (size) {
        const wMm = (Number(size[1]) / 72) * MM_PER_INCH;
        const hMm = (Number(size[2]) / 72) * MM_PER_INCH;
        const fmt = (n) => n.toFixed(1);
        push('info', 'Page mesurée', `${fmt(wMm)} × ${fmt(hMm)} mm`);

        const dW = Math.abs(wMm - expectedW);
        const dH = Math.abs(hMm - expectedH);
        const dWTrim = Math.abs(wMm - trim[0]);
        const dHTrim = Math.abs(hMm - trim[1]);

        if (dW < 1 && dH < 1) {
          push('ok', 'Fond perdu', `présent (${bleed} mm sur les quatre côtés)`);
        } else if (dWTrim < 1 && dHTrim < 1) {
          push('warn', 'Fond perdu absent', `le document fait le format fini : aucun débord. Ajoute ${bleed} mm sur chaque côté ou demande un fond perdu à l’imprimeur.`);
        } else {
          push('warn', 'Dimensions inattendues', `écart de ${fmt(dW)} / ${fmt(dH)} mm avec le format attendu.`);
        }
      }
      if (/Pages:\s+1\b/.test(out)) push('ok', 'Pages', '1 page');
      else push('info', 'Pages', out.match(/Pages:\s+(\d+)/)?.[1] ?? '?');
    }

    if (has('pdffonts')) {
      // Colonnes pdffonts : name type encoding emb sub uni object generation
      // On lit l'avant-dernier trio depuis la fin (ID objet = 2 jetons), donc emb = tokens[-5].
      const fonts = run('pdffonts', [file])
        .split('\n')
        .filter((l) => l.trim() && !/^-+\s|^name\s+type\s/.test(l))
        .map((l) => l.trim().split(/\s+/));
      const notEmbedded = fonts.filter((t) => t.length >= 6 && t[t.length - 5] === 'no');
      if (fonts.length === 0) {
        push('info', 'Fontes', 'aucune fonte détectée (texte vectorisé)');
      } else if (notEmbedded.length) {
        push('warn', 'Fontes non embarquées', `${notEmbedded.length} fonte(s) sur ${fonts.length} à vectoriser ou embeder.`);
      } else {
        push('ok', 'Fontes', `${fonts.length} embarquée(s)`);
      }
    } else {
      push('info', 'Fontes', 'pdffonts absent — vérifier avec : pdffonts ' + file);
    }

    if (has('gs')) {
      push('info', 'Encrage', 'vérifier le total ≤ 300 % avec : gs -o /dev/null -sDevice=inkcov ' + file);
    } else {
      push('info', 'Encrage', 'Ghostscript absent — demander le rapport de couverture d’encre à l’imprimeur.');
    }
  } else {
    if (!has('identify')) {
      push('warn', 'ImageMagick absent', 'Installe ImageMagick pour un contrôle automatique. Sinon : ouvrir les propriétés de l’image et vérifier dimensions + profil.');
      push('info', 'Commande manuelle', `identify -format "%w x %h | %[colorspace]\\n" ${file}`);
    } else {
      const out = run('identify', ['-format', '%w|%h|%[colorspace]|%x|%y', file + '[0]']);
      const [w, h, colorspace] = out.split('|');
      const wPx = Number(w);
      const hPx = Number(h);

      // Pixels attendus, au format fini seul puis avec fond perdu.
      const pxAtTrim = [Math.round((trim[0] / MM_PER_INCH) * dpi), Math.round((trim[1] / MM_PER_INCH) * dpi)];
      const pxWithBleed = [
        Math.round((expectedW / MM_PER_INCH) * dpi),
        Math.round((expectedH / MM_PER_INCH) * dpi),
      ];
      const near = (a, b) => Math.abs(a - b) / b < 0.01;
      const hasBleed =
        near(wPx, pxWithBleed[0]) && near(hPx, pxWithBleed[1]);

      // DPI effectif : rapporté à la taille physique que le fichier représente réellement
      // (le fond perdu fait partie du document, il ne « densifie » pas l'image).
      const refW = hasBleed ? expectedW : trim[0];
      const refH = hasBleed ? expectedH : trim[1];
      const dpiW = Math.round(wPx / (refW / MM_PER_INCH));
      const dpiH = Math.round(hPx / (refH / MM_PER_INCH));

      push('info', 'Pixels', `${wPx} × ${hPx} px`);

      if (hasBleed) {
        push('ok', 'Fond perdu', `présent (${bleed} mm sur les quatre côtés)`);
      } else if (near(wPx, pxAtTrim[0]) && near(hPx, pxAtTrim[1])) {
        push('warn', 'Fond perdu absent', `le fichier fait le format fini pile : aucun débord. Ajoute ${bleed} mm par côté (soit ${pxWithBleed[0]} × ${pxWithBleed[1]} px à ${dpi} dpi).`);
      } else {
        push('warn', 'Dimensions inattendues', `ni le format fini ni le format avec fond perdu. Attendu : ${pxWithBleed[0]} × ${pxWithBleed[1]} px à ${dpi} dpi.`);
      }

      push(dpiW >= dpi - 5 && dpiH >= dpi - 5 ? 'ok' : 'warn', 'DPI effectif',
        `${dpiW} × ${dpiH} dpi au format fini (cible ${dpi})`);

      const cm = (colorspace || '').toLowerCase();
      if (cm.includes('cmyk')) push('ok', 'Espace colorimétrique', 'CMJN');
      else if (cm.includes('gray')) push('warn', 'Espace colorimétrique', 'niveaux de gris — convient pour un texte noir, pas pour un aplat couleur');
      else push('warn', 'Espace colorimétrique', `${colorspace} — convertir en CMJN avant l’envoi`);
    }
  }

  const w = 78;
  console.log('\n' + '─'.repeat(w));
  console.log(` Preflight — ${file}`);
  console.log('─'.repeat(w));
  for (const r of results) {
    const icon = { ok: '✔', warn: '▲', info: '·' }[r.level];
    console.log(` ${icon} ${r.label.padEnd(34)} ${r.detail}`);
  }
  console.log('─'.repeat(w));

  const warnings = results.filter((r) => r.level === 'warn').length;
  if (warnings === 0) {
    console.log(' Conforme. Reste à valider à l’œil la plus petite mention.\n');
  } else {
    console.log(` ${warnings} point(s) à corriger avant envoi.\n`);
  }
  process.exit(warnings === 0 ? 0 : 1);
}

main();
