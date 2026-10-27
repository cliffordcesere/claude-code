#!/usr/bin/env python3
"""
Sound design synthétisé, synchronisé sur la timeline d'un flyer animé.
Aucun échantillon externe : tout est généré (pas de question de droits).

    python3 sfx.py cues.json --out son.wav
    python3 sfx.py cues.json --out son.wav --video flyer.mp4 --mux flyer_son.mp4

cues.json :
{
  "duration": 10,
  "cues": [
    {"type": "bed", "sound": "sizzle", "start": 0, "end": 10, "gain_db": -24, "fade_in": 0.3, "fade_out": 1.2},
    {"type": "whoosh", "at": 0.66, "dur": 0.55, "gain_db": -12},
    {"type": "impact", "at": 0.68, "gain_db": -6},
    {"type": "tick",   "at": 2.2,  "gain_db": -18, "pitch": 1.0},
    {"type": "swish",  "at": 3.6,  "dur": 0.9, "gain_db": -22}
  ]
}
"at" = instant où le son culmine (l'arrivée visuelle de l'élément), pas son début.
Types : bed (sizzle | room), whoosh, impact, tick, swish. Seule dépendance : numpy (+ ffmpeg pour --mux).
Le mixage est amené à -14 LUFS (standard des réseaux sociaux) avec un limiteur à -1,5 dBFS.
"""
import argparse, json, subprocess, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(11)


def db(g):
    return 10 ** (g / 20)


def band(x, lo, hi, tilt=0.0):
    """Filtre passe-bande par FFT (doux, sans phase non linéaire audible pour du bruit)."""
    n = len(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X = np.fft.rfft(x)
    m = 1 / (1 + (lo / np.maximum(f, 1)) ** 4) / (1 + (f / hi) ** 4)
    if tilt:
        m *= (np.maximum(f, 20) / 1000) ** tilt
    return np.fft.irfft(X * m, n)


def norm(x):
    p = np.max(np.abs(x)) or 1
    return x / p


def pan(x, p):
    """p dans [-1, 1], scalaire ou tableau ; loi à puissance constante."""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], axis=1)


def env_ar(n_attack, n_release, curve=4.0):
    a = np.linspace(0, 1, max(n_attack, 1)) ** 2
    r = np.exp(-curve * np.linspace(0, 1, max(n_release, 1)))
    return np.concatenate([a, r])


def bed_sizzle(dur):
    n = int(dur * SR)
    # Friture : souffle aigu modulé lentement + crépitements épars (impulsions courtes, panoramique aléatoire).
    base = band(rng.standard_normal(n), 1800, 9000, tilt=-0.3)
    lfo = band(rng.standard_normal(n), 0.2, 3)            # modulation lente
    base = norm(base) * (0.55 + 0.45 * norm(lfo))
    out = pan(base * 0.35, 0.0)
    k = int(dur * 38)                                      # ~38 crépitements par seconde
    for t0 in rng.uniform(0, dur, k):
        L = int(rng.uniform(0.002, 0.009) * SR)
        burst = band(rng.standard_normal(L * 4), 2500, 12000)[:L] * np.exp(-np.linspace(0, 6, L))
        i = int(t0 * SR)
        if i + L >= n:
            continue
        out[i:i + L] += pan(norm(burst) * rng.uniform(0.15, 1.0), rng.uniform(-0.8, 0.8))
    return out


def bed_room(dur):
    n = int(dur * SR)
    x = norm(band(rng.standard_normal(n), 60, 900, tilt=-1.0))
    return pan(x * 0.5, 0.0)


def whoosh(dur):
    """Bruit filtré dont la bande monte, culmine à 75 % puis retombe vite ; balayage gauche → droite."""
    n = int(dur * SR)
    seg = 512
    noise = rng.standard_normal(n + seg)
    out = np.zeros(n)
    win = np.hanning(seg * 2)
    for s in range(0, n, seg):
        k = s / n
        c = 250 * (18 ** min(k / 0.75, 1))                 # 250 Hz → 4,5 kHz
        chunk = band(noise[s:s + seg * 2], c * 0.5, c * 2.2)
        e = min(len(chunk), n - s)
        out[s:s + e] += (chunk * win[:len(chunk)])[:e]
    peak = int(0.75 * n)
    env = np.concatenate([np.linspace(0, 1, peak) ** 3, np.exp(-5 * np.linspace(0, 1, n - peak))])
    return pan(norm(out) * env, np.linspace(-0.6, 0.6, n)), peak


def impact():
    """Coup grave pensé pour les téléphones : un haut-parleur de smartphone ne reproduit presque rien
    sous ~150 Hz, donc le sub (110 → 55 Hz) est doublé d'un corps 150-300 Hz et d'harmoniques
    (saturation) qui portent l'impact sur mobile ; le sub reste là pour les écouteurs."""
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 55 + 55 * np.exp(-t * 9)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    fb = 150 + 120 * np.exp(-t * 14)
    body = np.sin(2 * np.pi * np.cumsum(fb) / SR) * np.exp(-t * 11) * 0.9
    click = band(rng.standard_normal(n), 900, 7000) * np.exp(-t * 90)
    x = 0.6 * sub + body + norm(click) * 0.35
    x = np.tanh(2.4 * x) / np.tanh(2.4)                   # harmoniques : l'impact « s'entend » sur petit haut-parleur
    return pan(x, 0.0), int(0.004 * SR)


def tick(pitch=1.0):
    """« Toc » boisé court : deux partiels inharmoniques à décroissance rapide."""
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * 1180 * pitch * t) + 0.5 * np.sin(2 * np.pi * 2730 * pitch * t)) * np.exp(-t * 55)
    x += norm(band(rng.standard_normal(n), 2000, 9000)) * np.exp(-t * 400) * 0.3
    return pan(norm(x), 0.15), int(0.002 * SR)


def swish(dur):
    n = int(dur * SR)
    x = norm(band(rng.standard_normal(n), 3000, 11000))
    env = np.sin(np.linspace(0, np.pi, n)) ** 2
    return pan(x * env, np.linspace(-0.3, 0.3, n)), n // 2


def place(mix, sig, at, peak_offset, gain):
    i = int(at * SR) - peak_offset
    a, b = max(i, 0), min(i + len(sig), len(mix))
    if b > a:
        mix[a:b] += sig[a - i:b - i] * gain


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cues"); ap.add_argument("--out", required=True)
    ap.add_argument("--video"); ap.add_argument("--mux")
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()
    spec = json.load(open(a.cues))
    dur = float(spec["duration"])
    mix = np.zeros((int(dur * SR), 2))
    for c in spec["cues"]:
        g = db(c.get("gain_db", -12))
        if c["type"] == "bed":
            s0, s1 = c.get("start", 0), c.get("end", dur)
            sig = {"sizzle": bed_sizzle, "room": bed_room}[c.get("sound", "sizzle")](s1 - s0)
            fi, fo = int(c.get("fade_in", 0.3) * SR), int(c.get("fade_out", 1.0) * SR)
            e = np.ones(len(sig)); e[:fi] = np.linspace(0, 1, fi); e[len(e) - fo:] = np.linspace(1, 0, fo)
            place(mix, norm(sig) * e[:, None], s0, 0, g)
        elif c["type"] == "whoosh":
            sig, pk = whoosh(c.get("dur", 0.6)); place(mix, sig, c["at"], pk, g)
        elif c["type"] == "impact":
            sig, pk = impact(); place(mix, sig, c["at"], pk, g)
        elif c["type"] == "tick":
            sig, pk = tick(c.get("pitch", 1.0)); place(mix, sig, c["at"], pk, g)
        elif c["type"] == "swish":
            sig, pk = swish(c.get("dur", 0.8)); place(mix, sig, c["at"], pk, g)
        else:
            sys.exit(f"Type de cue inconnu : {c['type']}")
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)               # garde-fou contre l'écrêtage avant normalisation
    raw = a.out.replace(".wav", "_raw.wav")
    write_wav(raw, mix * 0.7)
    # Mise au niveau : gain puis limiteur (plafond -1,5 dBFS, marge pour l'encodage AAC), mesuré et
    # corrigé en deux itérations. loudnorm seul reste sous la cible : le pic de l'impact bloque le gain.
    def integrated(path, af="anull"):
        e = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", f"{af},ebur128", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        return float(e[e.rindex("I:"):].split()[1])
    gain = a.lufs - integrated(raw)
    for _ in range(3):
        chain = f"volume={gain:.2f}dB,alimiter=limit=0.84:attack=2:release=80:level=false"
        got = integrated(raw, chain)
        if abs(got - a.lufs) < 0.3:
            break
        gain += a.lufs - got
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", chain, "-ar", str(SR), a.out], check=True)
    print(f"Sonie : {got:.1f} LUFS (cible {a.lufs})")
    print("Son :", a.out)
    if a.video and a.mux:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-i", a.out, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.mux], check=True)
        print("Vidéo avec son :", a.mux)


if __name__ == "__main__":
    main()
