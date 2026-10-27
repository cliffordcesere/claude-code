/* Moteur partagé, extrait de studio-premium-motion/assets/template.html. Charger après window.__config. */
/* ============================== MOTEUR ==============================
   Timeline déterministe : chaque propriété d'un élément est une fonction pure de t.
   Propriétés : x, y (px) · xp, yp (% de l'élément) · scale, sx, sy · rotate (deg) · opacity
               blur (px) · clip [haut, droite, bas, gauche] en % (inset) · ls (letter-spacing, em)
               toute variable CSS commençant par "--" (ex. "--wght" pour une fonte variable). */
(function () {
  function bezier(x1, y1, x2, y2) {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
    const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const sx = t => ((ax * t + bx) * t + cx) * t;
    const sy = t => ((ay * t + by) * t + cy) * t;
    const dx = t => (3 * ax * t + 2 * bx) * t + cx;
    return x => {
      if (x <= 0) return 0; if (x >= 1) return 1;
      let t = x;
      for (let i = 0; i < 8; i++) {
        const e = sx(t) - x; if (Math.abs(e) < 1e-6) return sy(t);
        const d = dx(t); if (Math.abs(d) < 1e-6) break; t -= e / d;
      }
      let lo = 0, hi = 1; t = x;
      for (let i = 0; i < 40; i++) { const v = sx(t); if (Math.abs(v - x) < 1e-6) break; v < x ? lo = t : hi = t; t = (lo + hi) / 2; }
      return sy(t);
    };
  }
  const EASE = {
    linear: t => t,
    expoOut: bezier(0.16, 1, 0.3, 1),
    quartOut: bezier(0.25, 1, 0.5, 1),
    quintInOut: bezier(0.83, 0, 0.17, 1),
    expoIn: bezier(0.7, 0, 0.84, 0),
    sineInOut: bezier(0.37, 0, 0.63, 1),
  };
  const DEFAULTS = { x: 0, y: 0, xp: 0, yp: 0, scale: 1, sx: 1, sy: 1, rotate: 0, opacity: 1, blur: 0, ls: null, clip: null };
  const tweens = [];
  const elements = new Set();

  /* tween(cible, { prop: [de, à], ... }, { at, dur, ease, stagger }) */
  window.tween = function (target, props, opts) {
    const els = typeof target === "string" ? [...document.querySelectorAll(target)] : [].concat(target);
    if (!els.length) console.warn("tween : aucune cible pour", target);
    const o = Object.assign({ at: 0, dur: 1, ease: "expoOut", stagger: 0 }, opts);
    const ease = typeof o.ease === "function" ? o.ease : EASE[o.ease];
    if (!ease) throw new Error("Courbe inconnue : " + o.ease);
    els.forEach((el, i) => {
      elements.add(el);
      for (const p in props) tweens.push({ el, p, from: props[p][0], to: props[p][1], start: o.at + i * o.stagger, dur: o.dur, ease });
    });
  };

  /* Découpe un élément en mots puis en lettres (span.word > span.char) pour les animations par lettre. */
  window.splitChars = function (selector) {
    document.querySelectorAll(selector).forEach(el => {
      const words = el.textContent.split(/(\s+)/);
      el.textContent = "";
      words.forEach(w => {
        if (/^\s+$/.test(w)) { el.appendChild(document.createTextNode(" ")); return; }
        const ws = document.createElement("span"); ws.className = "word"; ws.style.display = "inline-block";
        [...w].forEach(c => { const cs = document.createElement("span"); cs.className = "char"; cs.style.display = "inline-block"; cs.textContent = c; ws.appendChild(cs); });
        el.appendChild(ws);
      });
    });
  };

  const lerp = (a, b, k) => Array.isArray(a) ? a.map((v, i) => v + (b[i] - v) * k) : a + (b - a) * k;

  function apply(el, s) {
    el.style.transform = `translate(${s.x}px, ${s.y}px) translate(${s.xp}%, ${s.yp}%) scale(${s.scale}) scale(${s.sx}, ${s.sy}) rotate(${s.rotate}deg)`;
    el.style.opacity = s.opacity;
    el.style.filter = s.blur > 0.01 ? `blur(${s.blur}px)` : "";
    if (s.clip) el.style.clipPath = `inset(${s.clip.map(v => v + "%").join(" ")})`;
    if (s.ls !== null) el.style.letterSpacing = s.ls + "em";
    for (const k in s) if (k.startsWith("--")) el.style.setProperty(k, s[k]);
  }

  let sorted = null;
  const hooks = [];
  window.onSeek = fn => hooks.push(fn);   // pour des effets calculés (canvas, compteurs…)

  window.__seek = function (t) {
    if (!sorted) sorted = tweens.slice().sort((a, b) => a.start - b.start);
    const state = new Map();
    for (const el of elements) state.set(el, Object.assign({}, DEFAULTS));
    const seen = new Set();
    for (const tw of sorted) {                       // valeur initiale = « de » du premier tween de la propriété
      const key = tw.p + "|" + [...elements].indexOf(tw.el);
      if (!seen.has(key)) { seen.add(key); state.get(tw.el)[tw.p] = tw.from; }
    }
    for (const tw of sorted) {
      if (t < tw.start) continue;
      const k = tw.dur > 0 ? Math.min(1, (t - tw.start) / tw.dur) : 1;
      state.get(tw.el)[tw.p] = lerp(tw.from, tw.to, tw.ease(k));
    }
    for (const [el, s] of state) apply(el, s);
    hooks.forEach(fn => fn(t));
  };
  window.EASE = EASE;
})();

/* ============================== GRAIN ==============================
   Bruit déterministe (même t = même image), renouvelé à 12 i/s comme un grain de pellicule. */
(function () {
  const cfg = window.__config, c = document.getElementById("grain");
  if (!c) return;
  if (new URLSearchParams(location.search).has("nograin")) { c.style.display = "none"; return; }  // GIF : le bruit ruine la compression
  c.width = cfg.width; c.height = cfg.height;
  const ctx = c.getContext("2d");
  const tiles = [];
  let seed = 7;
  const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let n = 0; n < 6; n++) {
    const tc = document.createElement("canvas"); tc.width = tc.height = 256;
    const tx = tc.getContext("2d"), img = tx.createImageData(256, 256);
    for (let i = 0; i < img.data.length; i += 4) { const v = rnd() * 255; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
    tx.putImageData(img, 0, 0); tiles.push(ctx.createPattern(tc, "repeat"));
  }
  window.onSeek(t => {
    const f = Math.floor(t * 12);
    ctx.save(); ctx.fillStyle = tiles[f % tiles.length];
    ctx.translate((f * 97) % 256, (f * 61) % 256);
    ctx.fillRect(-256, -256, cfg.width + 512, cfg.height + 512); ctx.restore();
  });
})();

/* ============================== LECTURE (lancée au chargement, après la timeline) ============================== */
window.addEventListener("load", function () {
  const q = new URLSearchParams(location.search), cfg = window.__config;
  const stage = document.getElementById("stage");
  if (q.has("guides")) document.documentElement.classList.add("show-guides");
  if (q.has("render")) { document.documentElement.classList.add("render"); document.body.classList.add("render"); window.__seek(0); return; }
  const fit = () => { const s = Math.min(innerWidth / cfg.width, innerHeight / cfg.height) * 0.96; stage.style.transform = `scale(${s})`; };
  addEventListener("resize", fit); fit();
  let t0 = performance.now(), paused = false, t = 0;
  addEventListener("keydown", e => {
    if (e.code === "Space") { paused = !paused; t0 = performance.now() - t * 1000; }
    if (e.code === "ArrowRight") { paused = true; t = Math.min(cfg.duration, t + 1 / cfg.fps); window.__seek(t); }
    if (e.code === "ArrowLeft") { paused = true; t = Math.max(0, t - 1 / cfg.fps); window.__seek(t); }
  });
  (function loop(now) {
    if (!paused) { t = ((now - t0) / 1000) % cfg.duration; window.__seek(t); }
    requestAnimationFrame(loop);
  })(performance.now());
});
