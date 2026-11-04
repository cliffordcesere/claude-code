"""ORA — habillage sonore synthétisé (aucune musique sous licence).

Usage :
    python3 ora/tools/son.py <evenements.json> <duree_s> <sortie.wav>
    ffmpeg -i video_muette.mp4 -i son.wav -c:v copy -c:a aac -b:a 192k -shortest sortie.mp4

evenements.json (écrit par tools/render.mjs depuis window.ORA_SONS) :
    { "souffles": [t, ...], "crans": [t, ...], "impact": t }

Esthétique : calme, jamais fort (§9 « sans musique forte »). Nappe en ré mineur,
souffles filtrés sur les transitions, crans secs sur les compteurs, une note grave au logo.
Nécessite numpy.
"""
import json, sys, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def db(x):
    return 10 ** (x / 20)


def nappe(duree, accords):
    """accords : liste de (debut, [fréquences]). Fondu enchaîné de 0,8 s entre accords."""
    t = np.arange(int(duree * SR)) / SR
    out = np.zeros((len(t), 2))
    for i, (t0, freqs) in enumerate(accords):
        t1 = accords[i + 1][0] if i + 1 < len(accords) else duree
        env = np.clip((t - t0 + 0.4) / 0.8, 0, 1) * np.clip((t1 + 0.4 - t) / 0.8, 0, 1)
        for k, f in enumerate(freqs):
            for c, det in ((0, -0.18), (1, 0.18)):  # léger désaccord gauche/droite
                ph = 2 * np.pi * (f + det) * t + k
                v = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
                out[:, c] += v * env / (1 + 0.6 * k)
    trem = 1 + 0.12 * np.sin(2 * np.pi * 0.11 * t)
    gen = np.clip(t / 2.0, 0, 1) * np.clip((duree - t) / 1.6, 0, 1)
    out *= (trem * gen)[:, None]
    # passe-bas doux (un pôle)
    a = np.exp(-2 * np.pi * 1800 / SR)
    for c in range(2):
        y = np.empty_like(out[:, c]); s = 0.0
        x = out[:, c]
        for n in range(len(x)):
            s = (1 - a) * x[n] + a * s; y[n] = s
        out[:, c] = y
    return out / np.max(np.abs(out)) * db(-22)


def souffle(dur=0.75):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    # filtre d'état variable, fréquence balayée 350 → 3200 Hz
    fc = 350 * (3200 / 350) ** (t / dur)
    lp = bp = 0.0; y = np.empty(n); q = 0.9
    for i in range(n):
        f = 2 * np.sin(np.pi * fc[i] / SR)
        hp = x[i] - lp - q * bp; bp += f * hp; lp += f * bp; y[i] = bp
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    y = y * env; y /= np.max(np.abs(y))
    pan = t / dur  # gauche → droite
    return np.stack([y * np.cos(pan * np.pi / 2), y * np.sin(pan * np.pi / 2)], 1) * db(-28)


def cran():
    n = int(0.03 * SR); t = np.arange(n) / SR
    f = 2300 * (1 + 0.04 * rng.standard_normal())
    y = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) + 0.25 * rng.standard_normal(n) * np.exp(-t / 0.002)
    return np.stack([y, y], 1) * db(-30)


def impact():
    n = int(2.4 * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 55 * t) + 0.6 * np.sin(2 * np.pi * 110 * t)) * np.exp(-t / 0.7) * np.clip(t / 0.01, 0, 1)
    ch = np.sin(2 * np.pi * 1174.66 * t) * np.exp(-t / 0.9) * 0.18  # ré6, très discret
    y = y / np.max(np.abs(y)) * db(-14) + ch * db(-6) * db(-14)
    return np.stack([y, y], 1)


def poser(piste, clip, t):
    i = int(t * SR)
    if i >= len(piste): return
    j = min(len(piste), i + len(clip))
    piste[i:j] += clip[: j - i]


def main():
    ev = json.load(open(sys.argv[1])); duree = float(sys.argv[2]); sortie = sys.argv[3]
    D2, A2, D3, F3, C4, E4 = 73.42, 110.0, 146.83, 174.61, 261.63, 329.63
    Bb1, F2 = 58.27, 87.31
    tiers = duree / 2.5
    piste = nappe(duree, [(0, [D2, A2, D3, F3, C4, E4]), (tiers, [Bb1, F2, D3, F3, A2 * 2]), (2 * tiers, [D2, A2, D3, F3, E4])])
    for t in ev.get('souffles', []): poser(piste, souffle(), max(0, t - 0.45))
    for t in ev.get('crans', []): poser(piste, cran(), t)
    if ev.get('impact') is not None: poser(piste, impact(), ev['impact'])
    piste = np.tanh(piste * 1.2) / np.tanh(1.2)  # limiteur doux
    piste = piste / np.max(np.abs(piste)) * db(-1.5)
    with wave.open(sortie, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((piste * 32767).astype('<i2').tobytes())
    print('OK', sortie)


if __name__ == '__main__':
    main()
