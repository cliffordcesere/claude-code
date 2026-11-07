// ORA — moteur des tutos « écran de téléphone » (interface reconstruite, rendu image par image).
// La page décrit sa scène avec SCENE({...}) ; tools/render.mjs appelle window.oraSeek(t).
//
// SCENE({
//   textes:       [{ a, b, label?, titre, sous?, visible?, centre?, retard? }]   « | » = retour à la ligne
//   nav:          [[t, idPage, sens]]           sens 0 = ouverture (fondu), 1 = avancer, -1 = revenir
//   defil:        [[t, idPage, y | 'idElement:hauteur']]   défilement vertical d'une page (.contenu)
//   taps:         [[t, sélecteur]]              doigt + clic sonore
//   glisser:      [[t0, t1, sélecteurDépart, sélecteurArrivée]]   doigt qui glisse
//   surbrillance: [[t0, t1, sélecteur, classe='hl']]
//   camera:       [[t, zoom, sélecteur|null, hauteurCible, poussée?]]
//   fin:          t                             le téléphone descend, signature centrée
//   sons:         { souffles: [t...], crans: [t...] (en plus des taps), impact: t }
//   voix:         { src, reperes: [[tVoix, tVideo]...] }   activé par ?voix
//   apres:        t => {}                       états propres à la scène
// })
(function () {
  const clamp = x => Math.min(Math.max(x, 0), 1);
  const out = x => 1 - Math.pow(1 - clamp(x), 4);
  const io = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  const lerp = (a, b, k) => a + (b - a) * k;
  const $ = s => document.querySelector(s);

  window.SCENE = function (C) {
    window.ORA_READY = false;
    const q = new URLSearchParams(location.search);
    const pages = [...document.querySelectorAll('.page')];
    const contenu = id => document.querySelector(`#${id} > .contenu`);
    const canvas = $('#canvas'), camera = $('#camera'), phone = $('#phone'), doigt = $('#doigt');
    const textes = $('#textes'), logoV = $('#logoV'), contact = $('#contact'), noir = $('#noir');

    // Textes
    const blocs = C.textes.map(p => {
      const b = document.createElement('div'); b.className = 'bloc' + (p.centre ? ' centre' : '');
      const l = (cls, txt) => txt.split('|').map(x => `<span class="ligne ${cls}"><span>${x}</span></span>`).join('');
      b.innerHTML = (p.label ? l('label', p.label) : '') + l('titre', p.titre) + (p.sous ? `<div style="margin-top:16px">${l('sous', p.sous)}</div>` : '');
      textes.append(b); return b;
    });

    // Mesures (téléphone au repos, sans caméra, sans défilement)
    const POS = {}, DEFIL = {};
    function mesurer() {
      phone.style.transform = 'none'; camera.style.transform = 'none';
      pages.forEach(p => { p.style.display = 'block'; p.style.transform = 'none'; p.style.opacity = 1; const c = p.querySelector(':scope > .contenu'); if (c) c.style.transform = 'none'; });
      const cr = canvas.getBoundingClientRect();
      const sels = new Set([...C.taps.map(x => x[1]), ...(C.glisser || []).flatMap(g => [g[2], g[3]]), ...C.camera.filter(c => c[2]).map(c => c[2]), ...(C.surbrillance || []).map(h => h[2])]);
      sels.forEach(s => { const r = $(s).getBoundingClientRect(); POS[s] = { x: r.left - cr.left + r.width / 2, y: r.top - cr.top + r.height / 2, page: $(s).closest('.page')?.id }; });
      (C.defil || []).forEach(([t, id, y]) => {
        if (typeof y === 'string') {
          const [eid, h] = y.split(':'); const pr = document.getElementById(id).getBoundingClientRect(), er = document.getElementById(eid).getBoundingClientRect();
          y = (er.top - pr.top) - Number(h);
        }
        (DEFIL[id] = DEFIL[id] || []).push([t, y]);
      });
      pages.forEach(p => { p.style.display = 'none'; });
    }
    const defil = (id, t) => {
      const L = DEFIL[id]; if (!L) return 0;
      let i = 0; while (i + 1 < L.length && t >= L[i + 1][0]) i++;
      if (i === 0 && t < L[0][0]) return L[0][1];
      const prev = i > 0 ? L[i - 1][1] : L[i][1];
      return lerp(prev, L[i][1], io((t - L[i][0]) / 0.8));
    };
    const pos = (s, t) => { const p = POS[s]; return { x: p.x, y: p.y - (p.page ? defil(p.page, t) : 0) }; };

    // Sons
    window.ORA_SONS = { souffles: (C.sons && C.sons.souffles) || [], crans: C.taps.map(x => x[0] + 0.12).concat((C.sons && C.sons.crans) || []), impact: C.sons && C.sons.impact };

    function seek(t) {
      noir.style.opacity = 0; // la 1re image est complète (décrochage à 0:02 constaté)

      // Téléphone : descend à la fin
      const descend = io((t - C.fin) / 0.9);
      phone.style.transform = `translateY(${descend * 1100}px)`;
      phone.style.opacity = 1 - descend;

      // Pages
      let cur = 0; while (cur + 1 < C.nav.length && t >= C.nav[cur + 1][0]) cur++;
      pages.forEach(p => { p.style.display = 'none'; p.style.transform = 'none'; p.style.opacity = 1; p.style.zIndex = ''; p.style.boxShadow = ''; });
      const [t0, id, sens] = C.nav[cur], k = io((t - t0) / 0.45);
      const ent = document.getElementById(id); ent.style.display = 'block';
      if (cur > 0 && k < 1) {
        const sor = document.getElementById(C.nav[cur - 1][1]);
        if (sor !== ent) {
          sor.style.display = 'block';
          if (sens === 0) { ent.style.opacity = k; ent.style.transform = `scale(${lerp(.9, 1, k)})`; sor.style.opacity = 1 - k; ent.style.zIndex = 2; }
          else {
            ent.style.transform = `translateX(${sens * (1 - k) * 100}%)`; sor.style.transform = `translateX(${-sens * k * 30}%)`;
            (sens > 0 ? ent : sor).style.zIndex = 2; (sens > 0 ? sor : ent).style.zIndex = 1;
            (sens > 0 ? ent : sor).style.boxShadow = '-20px 0 40px rgba(0,0,0,.6)';
          }
        }
      }
      Object.keys(DEFIL).forEach(pid => { const c = contenu(pid); if (c) c.style.transform = `translateY(${-defil(pid, t)}px)`; });

      // Surbrillances
      (C.surbrillance || []).forEach(([a, b, s, cls = 'hl']) => $(s).classList.remove(cls));
      (C.surbrillance || []).forEach(([a, b, s, cls = 'hl']) => { if (t >= a && t < b) $(s).classList.add(cls); });

      // Doigt
      const tap = C.taps.filter(x => t >= x[0] - 0.35 && t < x[0] + 0.35).pop();
      const gl = (C.glisser || []).find(g => t >= g[0] - 0.3 && t < g[1] + 0.3);
      if (gl) {
        const a = pos(gl[2], gl[0]), b = pos(gl[3], gl[1]), k = io((t - gl[0]) / (gl[1] - gl[0]));
        doigt.style.left = lerp(a.x, b.x, k) + 'px'; doigt.style.top = lerp(a.y, b.y, k) + 'px';
        doigt.style.opacity = 0.9 * Math.min(out((t - gl[0] + 0.3) / 0.25), 1 - clamp((t - gl[1]) / 0.3));
        doigt.style.transform = 'scale(0.9)';
      } else if (tap) {
        const p = pos(tap[1], tap[0]), d = t - tap[0];
        doigt.style.left = p.x + 'px'; doigt.style.top = p.y + 'px';
        doigt.style.opacity = d < 0 ? out((d + 0.35) / 0.25) * 0.9 : 0.9 * (1 - clamp(d / 0.35));
        doigt.style.transform = `scale(${d < 0 ? 1 : lerp(0.8, 1.3, clamp(d / 0.35))})`;
      } else doigt.style.opacity = 0;

      // Caméra
      const K = C.camera;
      const etat = (c, j) => {
        if (!c[2]) return { z: c[1], x: 0, y: 0 };
        let z = c[1];
        if (c[4] && j === 0) z *= 1 + c[4] * clamp(t / (K[1] ? K[1][0] : 3));
        const p = pos(c[2], c[0] + 0.9);
        return { z, x: 540 - p.x * z, y: c[3] - p.y * z };
      };
      let i = 0; while (i + 1 < K.length && t >= K[i + 1][0]) i++;
      const A = etat(K[Math.max(0, i - 1)], Math.max(0, i - 1)), B = etat(K[i], i), ke = i ? io((t - K[i][0]) / 0.9) : 1;
      camera.style.transform = `translate(${lerp(A.x, B.x, ke)}px, ${lerp(A.y, B.y, ke)}px) scale(${lerp(A.z, B.z, ke)})`;

      // Textes : entrée par masque, sortie par fondu montant
      C.textes.forEach((p, j) => {
        const el = blocs[j], tin = p.visible ? t + 2 : t - p.a - 0.5, tout = t - (p.b - 0.35);
        el.style.opacity = t < p.a - 0.01 ? 0 : tout > 0 ? 1 - clamp(tout / 0.35) : 1;
        el.style.transform = `translateY(${tout > 0 ? -16 * out(tout / 0.35) : 0}px)`;
        let n = 0;
        el.querySelectorAll('.ligne > span').forEach(sp => {
          const sous = sp.parentElement.classList.contains('sous');
          const e = out((tin - (sous ? (p.retard ?? 0.6) : 0) - n * 0.1) / 0.7); n++;
          sp.style.transform = `translateY(${(1 - e) * 110}%)`;
        });
      });

      // Signature
      logoV.style.opacity = out((t - C.fin - 0.9) / 0.6);
      contact.style.opacity = out((t - C.fin - 1.6) / 0.6);
      contact.style.transform = `translateY(${(1 - out((t - C.fin - 1.6) / 0.6)) * 12}px)`;

      if (C.apres) C.apres(t);
    }

    // Version voix off (?voix) : la vidéo suit la voix (repères voix → vidéo, images figées entre deux)
    function versVideo(t) { const R = C.voix.reperes; for (let i = 1; i < R.length; i++) if (t <= R[i][0]) { const [a, va] = R[i - 1], [b, vb] = R[i]; return va + (vb - va) * (t - a) / (b - a); } return R[R.length - 1][1]; }
    function versVoix(v) { const R = C.voix.reperes; for (let i = 1; i < R.length; i++) { const [a, va] = R[i - 1], [b, vb] = R[i]; if (vb > va && v >= va && v <= vb) return a + (b - a) * (v - va) / (vb - va); } return v; }

    Promise.all([...document.images].map(i => i.decode().catch(() => {}))).then(() => document.fonts.ready).then(() => {
      mesurer();
      window.oraSeek = seek;
      if (C.voix && q.has('voix')) {
        window.oraSeek = t => seek(versVideo(t));
        window.ORA_DURATION = C.voix.reperes[C.voix.reperes.length - 1][0];
        const S0 = window.ORA_SONS;
        window.ORA_SONS = { souffles: S0.souffles.map(versVoix), crans: S0.crans.map(versVoix), impact: S0.impact != null ? versVoix(S0.impact) : null,
          voix: decodeURIComponent(new URL(C.voix.src, location.href).pathname), voix_debut: 0 };
      }
      if (!q.has('render')) {
        const d0 = performance.now();
        const loop = () => { window.oraSeek(((performance.now() - d0) / 1000) % (window.ORA_DURATION + 1)); requestAnimationFrame(loop); };
        loop();
      } else window.oraSeek(0);
      window.ORA_READY = true;
    });
  };
})();
