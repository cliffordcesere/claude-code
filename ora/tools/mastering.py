"""ORA — mise au niveau finale du son (voix + habillage) pour les réseaux.

Le propriétaire trouvait le son « très bas » à -14 LUFS (2026-11-16) : cible par défaut -10 LUFS,
crête réelle ≤ -1 dBTP. Compression légère, puis gain mesuré et limiteur (2 à 3 essais pour viser juste).

Usage : python3 mastering.py entree.wav sortie.wav [cible_lufs=-10]
"""
import re, subprocess, sys

src, out = sys.argv[1], sys.argv[2]
cible = float(sys.argv[3]) if len(sys.argv) > 3 else -10.0
COMP = 'acompressor=threshold=-22dB:ratio=2.5:attack=5:release=90:makeup=1'
LIMITE = 'alimiter=limit=0.79:attack=2:release=50:level=disabled'  # -2 dBFS : marge pour l'AAC


def mesure(f):
    log = subprocess.run(['ffmpeg', '-hide_banner', '-i', f, '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    resume = log[log.rfind('Summary:'):]
    i = float(re.search(r'I:\s+(-?[\d.]+) LUFS', resume).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+|-inf) dBFS', resume).group(1))
    return i, tp


def rendre(gain):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-af', f'{COMP},volume={gain:.2f}dB,{LIMITE}',
                    '-ar', '48000', out], check=True)
    return mesure(out)


gain = 0.0
i, tp = rendre(gain)
for _ in range(3):
    if abs(i - cible) < 0.3:
        break
    gain += (cible - i) * 1.15  # le limiteur mange une partie du gain : on vise un peu plus
    i, tp = rendre(gain)
print(f'mastering : {i:.1f} LUFS, crête {tp:.1f} dBFS (gain {gain:+.1f} dB)')
