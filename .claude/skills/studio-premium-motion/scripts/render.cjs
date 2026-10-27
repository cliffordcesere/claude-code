#!/usr/bin/env node
/*
 * Rendu image par image d'un flyer HTML animé (contrat window.__config / window.__seek).
 * Playwright (Chromium) capture chaque image à un temps exact, ffmpeg encode.
 *
 *   node render.cjs flyer.html --out flyer.mp4
 *   node render.cjs --help
 */
const { spawn, spawnSync } = require("child_process");
const path = require("path");
const fs = require("fs");

const HELP = `
Usage : node render.cjs <fichier.html> [options]

Sortie
  --out <fichier>         Fichier de sortie (défaut : <nom>.mp4, .png avec --still, .pdf avec --pdf)
  --format <f>            mp4 | prores | webm | gif   (déduit de l'extension si absent)
  --still <t>             Exporte une seule image PNG au temps t (secondes ; "end" = config.still)
  --pdf                   Exporte un PDF vectoriel de la composition au temps config.still (ou --at)
  --at <t>                Temps utilisé pour --pdf

Réglages
  --fps <n>               Cadence (défaut : config.fps)
  --duration <s>          Durée (défaut : config.duration)
  --scale <n>             Facteur de pixels (2 = rendu deux fois plus défini ; 0.25 = test miniature)
  --workers <n>           Pages de rendu en parallèle (défaut : min(4, cœurs - 1))
  --motion-blur <n>       Flou de mouvement : n sous-images moyennées par image (4 conseillé ; obturateur 180°)
  --crf <n>               Qualité H.264 / VP9 (défaut 16 / 24 ; plus bas = meilleur)
  --gif-width <px>        Largeur du GIF (défaut 600). Le grain est coupé pour les GIF (poids) ; --keep-grain pour le garder
  --alpha                 Fond transparent (ProRes 4444 / WebM) : la scène doit avoir un fond transparent
  --query <k=v&...>       Paramètres d'URL ajoutés (ex. "guides=1")
  --allow-missing-fonts   Ne pas échouer si une police déclarée manque (déconseillé)

Diagnostic
  --check                 Vérifie Playwright, Chromium et ffmpeg puis quitte
`;

function parseArgs(argv) {
  const a = { _: [] };
  const flags = new Set(["pdf", "alpha", "check", "help", "allow-missing-fonts", "keep-grain"]);
  for (let i = 0; i < argv.length; i++) {
    const s = argv[i];
    if (s.startsWith("--")) {
      const k = s.slice(2);
      if (flags.has(k)) a[k] = true; else a[k] = argv[++i];
    } else a._.push(s);
  }
  return a;
}

function loadPlaywright() {
  try { return require("playwright"); } catch (_) {}
  try { return require("@playwright/test"); } catch (_) {}
  console.error("Playwright introuvable. Installe-le (npm i playwright) ou lance depuis un environnement où require('playwright') fonctionne.");
  process.exit(1);
}

async function launch(pw) {
  try { return await pw.chromium.launch(); }
  catch (e) {
    if (fs.existsSync("/opt/pw-browsers/chromium")) return pw.chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
    throw e;
  }
}

function hasFfmpeg() { return spawnSync("ffmpeg", ["-version"]).status === 0; }

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(HELP); return; }
  const pw = loadPlaywright();

  if (args.check) {
    const b = await launch(pw); console.log("Chromium :", b.version()); await b.close();
    console.log("ffmpeg   :", hasFfmpeg() ? "ok" : "ABSENT");
    return;
  }

  const input = args._[0];
  if (!input) { console.log(HELP); process.exit(1); }
  const file = path.resolve(input);
  if (!fs.existsSync(file)) { console.error("Fichier introuvable :", file); process.exit(1); }
  // Le grain animé multiplie le poids d'un GIF par 10 ou plus : on le coupe sauf demande contraire.
  const isGif = args.format === "gif" || /\.gif$/i.test(args.out || "");
  const query = [args.query, isGif && !args["keep-grain"] ? "nograin=1" : null].filter(Boolean).join("&");
  const url = "file://" + file + "?render=1" + (query ? "&" + query : "");

  const browser = await launch(pw);
  try {
    // 1. Lire la configuration de la scène
    const probe = await browser.newPage();
    await probe.goto(url, { waitUntil: "load" });
    const cfg = await probe.evaluate(() => window.__config);
    await probe.close();
    if (!cfg || !cfg.width || !cfg.height) throw new Error("window.__config absent ou incomplet (width/height requis).");

    const fps = Number(args.fps || cfg.fps || 30);
    const duration = Number(args.duration || cfg.duration || 8);
    const scale = Number(args.scale || 1);
    const blur = Math.max(1, Number(args["motion-blur"] || 1));
    const stillDefault = cfg.still != null ? cfg.still : duration;

    // 2. Page de rendu à la taille exacte, polices vérifiées : on refuse un rendu avec police de secours
    const openPage = async (warn) => {
      const ctx = await browser.newContext({ viewport: { width: cfg.width, height: cfg.height }, deviceScaleFactor: scale });
      const page = await ctx.newPage();
      page.on("pageerror", e => console.error("Erreur JS dans la page :", e.message));
      await page.goto(url, { waitUntil: "networkidle" });
      await page.evaluate(() => { if (typeof window.__seek !== "function") throw new Error("window.__seek absent"); window.__seek(0); });
      const fontReport = await page.evaluate(async (families) => {
        await document.fonts.ready;
        await Promise.all((families || []).flatMap(f => [
          document.fonts.load(`16px "${f}"`, "AÉaé0").catch(() => null),
          document.fonts.load(`italic 16px "${f}"`, "AÉaé0").catch(() => null),
        ]));
        await document.fonts.ready;
        const faces = [...document.fonts];
        return (families || []).map(f => ({ family: f, loaded: faces.some(x => x.family.replace(/["']/g, "") === f && x.status === "loaded") }));
      }, cfg.fonts);
      const missing = fontReport.filter(f => !f.loaded).map(f => f.family);
      if (missing.length) {
        const msg = "Police(s) non chargée(s) : " + missing.join(", ") + ". Vérifie l'accès réseau (Google Fonts / kit Adobe) ou les @font-face locaux.";
        if (!args["allow-missing-fonts"]) throw new Error(msg);
        if (warn) console.warn("ATTENTION — " + msg);
      }
      return { ctx, page };
    };
    const { ctx, page } = await openPage(true);

    const stage = await page.$("#stage, .stage");
    const shot = async (opts = {}) => stage
      ? stage.screenshot(Object.assign({ type: "png", omitBackground: !!args.alpha }, opts))
      : page.screenshot(Object.assign({ type: "png", omitBackground: !!args.alpha }, opts));

    // 4a. Image fixe
    if (args.still !== undefined) {
      const t = args.still === "end" ? stillDefault : Number(args.still);
      const out = path.resolve(args.out || input.replace(/\.html?$/, "") + `_t${t}.png`);
      await page.evaluate(t => window.__seek(t), t);
      fs.writeFileSync(out, await shot());
      console.log("Image :", out);
      return;
    }

    // 4b. PDF vectoriel
    if (args.pdf) {
      const t = args.at !== undefined ? Number(args.at) : stillDefault;
      const out = path.resolve(args.out || input.replace(/\.html?$/, "") + ".pdf");
      await page.evaluate(t => window.__seek(t), t);
      const box = await page.evaluate(() => { const s = document.querySelector("#stage, .stage") || document.body; const r = s.getBoundingClientRect(); return { w: r.width, h: r.height }; });
      await page.emulateMedia({ media: "screen" });
      await page.addStyleTag({ content: "@page { margin: 0 } html, body { background: none !important; display: block !important; min-height: 0 !important; }" });
      await page.pdf({ path: out, width: box.w + "px", height: box.h + "px", printBackground: true, pageRanges: "1" });
      console.log("PDF (RVB) :", out, `— ${(box.w * 25.4 / 96).toFixed(1)} × ${(box.h * 25.4 / 96).toFixed(1)} mm`);
      return;
    }

    // 4c. Vidéo
    if (!hasFfmpeg()) throw new Error("ffmpeg est requis pour la vidéo.");
    const out = path.resolve(args.out || input.replace(/\.html?$/, "") + ".mp4");
    const ext = path.extname(out).slice(1).toLowerCase();
    const format = args.format || ({ mov: "prores", webm: "webm", gif: "gif" }[ext] || "mp4");

    const frames = Math.round(duration * fps);
    const inRate = fps * blur;
    const pre = ["-y", "-hide_banner", "-loglevel", "error", "-f", "image2pipe", "-c:v", "png", "-framerate", String(inRate), "-i", "-"];
    const filters = [];
    if (blur > 1) filters.push(`tmix=frames=${blur}`, `select='eq(mod(n\\,${blur})\\,${blur - 1})'`, `setpts=N/(${fps}*TB)`);
    // Dimensions paires pour yuv420p
    const even = "scale=trunc(iw/2)*2:trunc(ih/2)*2";
    let enc;
    if (format === "mp4") enc = ["-vf", [...filters, even].join(","), "-r", String(fps), "-c:v", "libx264", "-preset", "slow", "-crf", String(args.crf || 16), "-pix_fmt", "yuv420p", "-movflags", "+faststart", out];
    else if (format === "prores") enc = [...(filters.length ? ["-vf", filters.join(",")] : []), "-r", String(fps), "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", args.alpha ? "yuva444p10le" : "yuv444p10le", out];
    else if (format === "webm") enc = ["-vf", [...filters, even].join(","), "-r", String(fps), "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", String(args.crf || 24), "-row-mt", "1", "-pix_fmt", args.alpha ? "yuva420p" : "yuv420p", out];
    else if (format === "gif") {
      const w = Number(args["gif-width"] || 600);
      enc = ["-filter_complex", [...filters, `scale=${w}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4`].join(","), "-r", String(fps), "-loop", "0", out];
    } else throw new Error("Format inconnu : " + format);

    const ff = spawn("ffmpeg", [...pre, ...enc], { stdio: ["pipe", "inherit", "inherit"] });
    const ffDone = new Promise((res, rej) => ff.on("close", c => c === 0 ? res() : rej(new Error("ffmpeg a échoué (code " + c + ")"))));
    const write = buf => new Promise(res => ff.stdin.write(buf) ? res() : ff.stdin.once("drain", res));

    // Capture directe via CDP (bien plus rapide que locator.screenshot), répartie sur plusieurs
    // pages : chaque page est un processus de rendu Chromium distinct, donc les cœurs travaillent en parallèle.
    const box = await page.evaluate(() => { const s = document.querySelector("#stage, .stage"); const r = s ? s.getBoundingClientRect() : { x: 0, y: 0, width: innerWidth, height: innerHeight }; return { x: r.x, y: r.y, width: r.width, height: r.height }; });
    const makeWorker = async ({ ctx, page }) => {
      const cdp = await ctx.newCDPSession(page);
      if (args.alpha) await cdp.send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
      return async t => {
        await page.evaluate(t => window.__seek(t), t);
        const r = await cdp.send("Page.captureScreenshot", { format: "png", optimizeForSpeed: true, captureBeyondViewport: false, clip: Object.assign({ scale: 1 }, box) });
        return Buffer.from(r.data, "base64");
      };
    };
    const nWorkers = Math.max(1, Number(args.workers || Math.min(4, Math.max(1, require("os").cpus().length - 1))));
    const workers = [await makeWorker({ ctx, page })];
    for (let w = 1; w < nWorkers; w++) workers.push(await makeWorker(await openPage(false)));

    const shutter = 0.5; // obturateur 180°
    const units = [];     // une unité = une capture (sous-image si flou de mouvement)
    for (let i = 0; i < frames; i++) for (let k = 0; k < blur; k++) units.push((i + (blur > 1 ? (k / blur) * shutter : 0)) / fps);
    const started = Date.now();
    for (let u = 0; u < units.length; u += workers.length) {
      const batch = units.slice(u, u + workers.length);
      const bufs = await Promise.all(batch.map((t, j) => workers[j](t)));
      for (const buf of bufs) await write(buf);
      const done = Math.min(frames, Math.floor((u + batch.length) / blur));
      if (done % fps < workers.length || done === frames) process.stdout.write(`\rImage ${done}/${frames}`);
    }
    ff.stdin.end();
    await ffDone;
    const size = (fs.statSync(out).size / 1e6).toFixed(2);
    console.log(`\n${format.toUpperCase()} : ${out} — ${frames} images, ${fps} i/s, ${size} Mo, ${((Date.now() - started) / 1000).toFixed(1)} s`);
  } finally {
    await browser.close();
  }
}

main().catch(e => { console.error("\nÉchec :", e.message); process.exit(1); });
