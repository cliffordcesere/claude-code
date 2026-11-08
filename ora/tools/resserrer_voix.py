"""ORA — resserre une voix off : pauses plafonnées, accélération sans changer la hauteur, égalisation ; transpose les repères voix→vidéo.
Usage : python3 resserrer.py voix.flac sortie.wav tempo pause_max pause_section t_sections(csv) reperes.json
"""
import sys, json, re, subprocess
src, out, tempo, pmax, psec, tsec, rep = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), [float(x) for x in sys.argv[6].split(',')], json.load(open(sys.argv[7]))
log = subprocess.run(['ffmpeg','-hide_banner','-i',src,'-af','silencedetect=n=-38dB:d=0.12','-f','null','-'], capture_output=True, text=True).stderr
st = [float(v) for v in re.findall(r'silence_start: ([\d.]+)', log)]; en = [float(v) for v in re.findall(r'silence_end: ([\d.]+)', log)]
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src], capture_output=True, text=True).stdout)
# segments gardés
keep = []; cur = 0.0
for a, b in zip(st, en):
    lim = psec if any(a - 0.3 <= t <= b + 0.3 for t in tsec) else pmax
    if b - a > lim:
        keep.append((cur, a + lim / 2)); cur = b - lim / 2
keep.append((cur, dur))
# carte temps ancien -> nouveau
def carte(t):
    acc = 0.0
    for a, b in keep:
        if t < a: return acc / tempo
        if t <= b: return (acc + t - a) / tempo
        acc += b - a
    return acc / tempo
filt = ''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}];' for i, (a, b) in enumerate(keep))
filt += ''.join(f'[s{i}]' for i in range(len(keep))) + f'concat=n={len(keep)}:v=0:a=1,atempo={tempo},'
# Traitement « pièce vide » (2026-11-08) : queues de réverbération raccourcies (expandeur avant l'égalisation),
# son de boîte retiré (190, 380, 650 Hz), clarté rendue (2,2 et 4 kHz, aigus), sifflantes tenues.
filt += ('highpass=f=85,'
         'agate=threshold=0.018:ratio=2.5:attack=4:range=0.25:release=140,'
         'equalizer=f=190:t=o:w=1:g=-4,equalizer=f=380:t=o:w=0.8:g=-6,equalizer=f=650:t=o:w=1:g=-2.5,'
         'equalizer=f=2200:t=o:w=1.2:g=3,equalizer=f=4000:t=o:w=1.2:g=2,highshelf=f=8000:g=2.5,deesser=i=0.35,'
         'acompressor=threshold=-20dB:ratio=2.5:attack=6:release=110:makeup=2,'
         'loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000[o]')
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-filter_complex',filt,'-map','[o]',out], check=True)
new = []; last = -1
for tv, tvid in rep[:-1]:
    t = round(carte(tv), 3)
    if t <= last: t = round(last + 0.05, 3)
    new.append([t, tvid]); last = t
fin_voix = carte(dur)
new.append([round(max(fin_voix + 1.8, last + 0.5), 3), rep[-1][1]])
print(json.dumps(new))
print('durée voix', round(dur, 2), '->', round(fin_voix, 2), file=sys.stderr)
