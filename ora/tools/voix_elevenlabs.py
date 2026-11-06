"""ORA — voix off ElevenLabs, avec minutage mot par mot (pour caler les écrans).

La clé n'est jamais dans le code : le proxy de la session l'injecte dans l'en-tête xi-api-key
(secret réseau « Clé API ElevenLabs » de l'environnement ORA).

Usage :
    python3 ora/tools/voix_elevenlabs.py voix                       # voix disponibles (fr en tête)
    python3 ora/tools/voix_elevenlabs.py dire <voice_id> texte.txt sortie.mp3 [modèle]
        → sortie.mp3 + sortie.mots.json : [[mot, début_s, fin_s], ...]
"""
import base64, json, sys, urllib.request

API = 'https://api.elevenlabs.io'


def appel(chemin, corps=None):
    req = urllib.request.Request(API + chemin, method='POST' if corps else 'GET',
                                 data=json.dumps(corps).encode() if corps else None,
                                 headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def voix():
    d = appel('/v1/voices')
    for v in sorted(d.get('voices', []), key=lambda v: (v.get('labels', {}).get('language', '') != 'fr', v['name'])):
        lab = v.get('labels', {})
        print(f"{v['voice_id']}  {v['name']:<24} {lab.get('gender','')}/{lab.get('accent','')}/{lab.get('language','')}  {lab.get('description','') or lab.get('descriptive','')}")


def dire(voice_id, fichier_texte, sortie, modele='eleven_multilingual_v2'):
    texte = open(fichier_texte, encoding='utf-8').read().strip()
    d = appel(f'/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128', {
        'text': texte, 'model_id': modele, 'language_code': 'fr',
        'voice_settings': {'stability': 0.45, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True, 'speed': 1.05},
    })
    open(sortie, 'wb').write(base64.b64decode(d['audio_base64']))
    al = d.get('normalized_alignment') or d['alignment']
    mots, cur, deb, fin = [], '', None, None
    for c, a, b in zip(al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']):
        if c.isspace():
            if cur: mots.append([cur, round(deb, 3), round(fin, 3)]); cur = ''
            continue
        if not cur: deb = a
        cur += c; fin = b
    if cur: mots.append([cur, round(deb, 3), round(fin, 3)])
    json.dump(mots, open(sortie.rsplit('.', 1)[0] + '.mots.json', 'w'), ensure_ascii=False)
    print('OK', sortie, f'{mots[-1][2]:.2f} s', len(mots), 'mots')


if __name__ == '__main__':
    if sys.argv[1] == 'voix': voix()
    elif sys.argv[1] == 'dire': dire(*sys.argv[2:])
