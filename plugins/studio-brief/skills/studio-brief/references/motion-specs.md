# Specs motion

## Durées

| Format | Durée | Notes |
|---|---|---|
| Flyer animé (story) | 6–10 s | un seul moment orchestré, boucle propre |
| Teaser | 15–20 s | deux temps maximum : accroche, information |
| Bumper / transition | 1,5–3 s | une seule action, fin sur l'image clé |
| Générique | 10–30 s | au-delà : autre brief, autre budget |

## Grammaire

- **Une entrée, une sortie.** Le milieu du plan ne s'anime pas.
- Stagger 60–90 ms entre éléments d'un même groupe ; ne jamais dépasser 120 ms.
- Easing par défaut : `cubic-bezier(0.16, 1, 0.3, 1)` (sortie rapide, atterrissage long).
  Entrée de page : `cubic-bezier(0.22, 1, 0.36, 1)`.
- Interdits : `bounce`, `elastic`, ressort par défaut, rotation gratuite, échelle > 1,15.
- Distance d'entrée : 12–40 px équivalents, ou 4–8 % de la hauteur. Au-delà, ça « vole ».
- Une seule propriété animée par élément, deux maximum (position + opacité).

## Texture

- **Grain 2–4 %** sur toute la surface, animé à 12 ou 24 fps indépendamment de la composition : c'est ce qui distingue une image de synthèse d'une image finie.
- Vignettage 4–8 % si le fond est clair.
- Léger flou de mouvement (2–4 px) sur les translations rapides.
- Aucun flare, aucune aberration chromatique décorative, aucun glitch sans raison narrative.

## Composition et zones sûres

| Format | Zone d'interface à éviter |
|---|---|
| 9:16 (1080 × 1920) | 14 % en haut, 20 % en bas, 6 % à droite |
| 1:1 (1080 × 1080) | 8 % sur les quatre côtés |
| 16:9 (1920 × 1080) | 5 % sur les quatre côtés |

Le recadrage d'un format à l'autre se fait par **déplacement de la caméra**, pas par recomposition : même grille, même point focal.

## Export

```bash
# H.264, profil high, yuv420p, faststart
ffmpeg -i source.mov -c:v libx264 -profile:v high -pix_fmt yuv420p \
  -crf 18 -movflags +faststart -r 30 sortie.mp4

# Audio normalisé pour les plateformes
ffmpeg -i sortie.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v copy sortie_-14lufs.mp4
```

- 30 fps pour du motion typographique, 60 fps si mouvement de caméra.
- `yuv420p` obligatoire pour la compatibilité navigateur et mobile.
- Toujours livrer la **poster frame** (image 0) : c'est la vignette sur toutes les plateformes.
- GIF uniquement en aperçu, jamais en livrable principal.

## Moteurs

### Remotion (React → MP4)

```bash
npx skills add remotion-dev/skills
/remotion-create, /remotion-markup, /remotion-studio, /remotion-render
```

- Rendering déterministe, composition versionnée, données injectables (un CSV de 200 événements = 200 vidéos).
- **Licence** : gratuit pour les particuliers et les structures de 3 personnes ou moins. Au-delà, licence entreprise par siège.

### HyperFrames (HTML/CSS → MP4)

```bash
npx hyperframes skills update
```

- L'agent écrit du HTML/CSS/GSAP/Lottie, le CLI rend un MP4 déterministe.
- **Apache-2.0**, aucune limite de sièges. À privilégier si le budget licences est contraint ou si l'équipe ne code pas en React.

### GSAP (le timing)

```bash
npx skills add greensock/gsap-skills
```

- Depuis le rachat par Webflow, **tous les plugins sont gratuits**, y compris SplitText, MorphSVG et DrawSVG.
- Dans Remotion, on pilote une timeline GSAP en pause et on la « seek » sur la frame courante : c'est le pont qui donne un easing de niveau studio sans casser le déterminisme.

## Boucle de validation

1. Rendre à `--scale 0.5` pour itérer vite.
2. Extraire 6 stills (frame 0, fin d'entrée, milieu, deux moments de texte, dernière frame).
3. Vérifier : marges, crénelage des petites tailles, coupures, lisibilité en vignette, cohérence du grain sur toute la durée.
4. Corriger, rendre à pleine résolution, re-vérifier la première et la dernière frame.

```bash
ffmpeg -i sortie.mp4 -vf "select='eq(n,0)+eq(n,15)+eq(n,45)+eq(n,90)+eq(n,135)+eq(n,199)'" \
  -vsync 0 still_%02d.png
```
