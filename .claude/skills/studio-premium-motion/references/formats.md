# Formats de livraison — référence

Les dimensions des plateformes évoluent ; celles-ci sont les standards courants.
En cas de doute pour un canal précis (écran d'affichage, régie), demander la fiche technique au client.

## Vidéo / animé

| Canal | Dimensions | Ratio | Notes |
|---|---|---|---|
| Story, Reels, TikTok, Shorts | 1080 × 1920 | 9:16 | Zones de sécurité ci-dessous |
| Feed Instagram / Facebook / LinkedIn | 1080 × 1350 | 4:5 | Format le plus visible dans un fil |
| Carré | 1080 × 1080 | 1:1 | |
| Paysage, écran, site | 1920 × 1080 | 16:9 | 3840 × 2160 pour écrans 4K |
| Écran vertical (affichage) | 1080 × 1920 ou 2160 × 3840 | 9:16 | Vérifier codec et durée imposés par la régie |
| GIF e-mail | 600 px de large | libre | 12 i/s, viser < 2 Mo — voir « GIF » ci-dessous |

**Zones de sécurité 9:16** (approximatives, interface des applications par-dessus) :
garder textes et logo hors des ~250 px du haut et des ~340 px du bas, et à ~60 px des bords latéraux.
Le template affiche ces zones avec `?guides=1`.

**Encodage par défaut du script de rendu :**
- MP4 : H.264 High, `yuv420p`, CRF 16, preset slow, `+faststart`. Compatible partout, de très bonne qualité.
- ProRes 4444 (`.mov`) : master pour le client ou pour un monteur ; gros fichier.
- WebM VP9 : pour le web si demandé.
- Cadence : 30 i/s par défaut ; 25 i/s pour une diffusion européenne broadcast ; 24 pour un rendu « cinéma ».
- Durée : 6–12 s pour un flyer animé ; 15 s max en story.

**GIF.** Le format compresse très mal tout ce qui change sur toute l'image. Mesuré sur le template
(600 px, 8 s) : 33 Mo avec grain et halo mobile, 6 Mo sans grain, **0,6 Mo** avec un fond fixe à 12 i/s.
Pour un GIF : fond immobile (pas de dérive, pas de grain — le script coupe le grain automatiquement),
seuls les éléments qui entrent bougent, 12 i/s, `--gif-colors 64` si le poids dépasse encore la cible.
Faire une version dédiée du HTML plutôt que réduire la vidéo.

## Print

| Format | Fini (mm) | Avec fonds perdus 3 mm |
|---|---|---|
| A6 | 105 × 148 | 111 × 154 |
| A5 | 148 × 210 | 154 × 216 |
| A4 | 210 × 297 | 216 × 303 |
| DL | 99 × 210 | 105 × 216 |

- Marge de sécurité intérieure : 5 mm minimum pour tout texte.
- Construire le HTML print en unités `mm` (le stage fait la taille avec fonds perdus) puis rendre avec `--pdf` : le texte et les formes restent vectoriels.
  Depuis le template : `.stage { width: 154mm; height: 216mm; }`, `__config.width/height` en px CSS
  (mm × 96 / 25,4, soit 582 × 816 pour A5 + fonds perdus), et toutes les tailles en `mm` ou `pt`.
  **Recompose** la mise en page (un A5 se lit à 40 cm, pas sur un téléphone) au lieu de réduire la story.
- Masque le grain du template en print (`.grain { display: none }`) : le canvas serait pixellisé à basse
  résolution dans le PDF. Si de la matière est voulue, l'ajouter sur les images (connecteur Adobe, `image_add_grain`).
- Les images matricielles doivent faire 300 ppp à la taille d'impression.
- **Limite connue** : le PDF produit par Chromium est en RVB. La conversion CMJN avec le profil ICC de l'imprimeur (FOGRA39, FOGRA51, etc.) doit se faire dans Acrobat / InDesign ou chez l'imprimeur. Les couleurs vives (bleus électriques, verts fluo) changeront à la conversion : à signaler au client.

## Nommage des fichiers livrés

`CLIENT_PROJET_FORMAT_vNN.ext` — par exemple `MAISONECLAT_SOIREE_9x16_v03.mp4`, `MAISONECLAT_SOIREE_A5-print_v03.pdf`.
