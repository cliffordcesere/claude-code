# ORA — kit de marque et production

Tout le contenu ORA (flyers, posts, stories, vidéos motion, tutos) part d'ici.

**Source de vérité : [`charte/ORA_SYSTEM_PROMPT_v3.1.md`](charte/ORA_SYSTEM_PROMPT_v3.1.md).**
Copie intégrale, non modifiée. En cas de doute, c'est elle qui tranche, pas ce README.
Seul le propriétaire de la marque la modifie (§21) : nouvelle version = nouveau fichier, l'ancien est conservé.

## Contenu

| Dossier | Contenu |
|---|---|
| `charte/` | Charte v3.1 (system prompt ORA). |
| `logo/ORA_logo_construction_v3.1.pdf` | Fiche de construction : seule source valable du logo (§5). |
| `logo/svg/` | Logo vectoriel, extrait tel quel de la fiche. 4 formes × 3 versions officielles, avec ou sans fond (`_fond` = zone de sécurité 12u incluse). |
| `logo/png/` | Exports PNG transparents + favicons (symbole renforcé 16–48 px) + avatar réseaux 1080 px. |
| `fonts/` | Jost variable (100–900), licence OFL. |
| `templates/` | `ora.css` (jetons de charte), `post-4x5.html`, `story-9x16-motion.html`, `index.html` (franchise « Index »), `produit-motion.html` (vidéo produit 9:16 : caméra, lumière, reflet, textes). |
| `produits/` | Photos produit : source + version détourée (PNG transparent). |
| `tools/render.mjs` | Rendu HTML → PNG, HTML → MP4, SVG → PNG. |
| `tools/extract_logo.py` | Régénère les SVG depuis la fiche PDF. |
| `tools/detourer_ia.py` | Détourage IA local (rembg, modèle `birefnet-general`) pour une photo sur fond chargé : `python3 ora/tools/detourer_ia.py birefnet-general photo.jpg sortie.png`. |
| `tools/nettoyer_detourage.py` | Nettoie un détourage : taches isolées, bords, bruit. |
| `tools/resserrer_voix.py` | Voix off : pauses plafonnées, +x % de vitesse, égalisation ; recalcule les repères de synchro. |
| `tools/son.py` | Habillage sonore synthétisé, appelé par `render.mjs` quand la page expose `window.ORA_SONS` (`--muet` pour s'en passer). |
| `tools/detourer.py` | Détoure un produit photographié sur fond blanc : `python3 ora/tools/detourer.py photo.jpg sortie.png 2` (nécessite numpy, scipy, Pillow). |
| `contenus/` | Livrables produits, nommés selon §10. |
| `memoire.md` | Mémoire de marque (§17) : slogans, décisions, informations manquantes. |

## Logo — formes disponibles

| Fichier | Usage |
|---|---|
| `horizontal` | Assemblage principal (41,44u × 12u). Min. 80 px de large. |
| `vertical` | Usages centrés : pilier MARQUE, emballage. Min. 48 px de large. |
| `symbole` | Symbole seul : icône, filigrane. Min. 24 px. |
| `symbole-renforce` | Sous 24 px uniquement : favicon (trait 1,5u, fente 2,25u). |

Versions : `cuivre-sur-noir` (principale) · `blanc-sur-noir` · `noir-sur-blanc`. Aucune autre.

Les SVG sont extraits des tracés vectoriels de la fiche PDF (pages 1, 3, 5), pas redessinés.
Cotes vérifiées contre la fiche : O à 4u de l'anneau, ⌀ 8,24 ; approches O–R 2,6 et R–A 1,4 ; A large de 7,2 ;
assemblage 41,44u × 12u ; vertical 12u × 17,83u.
Le générateur d'origine (`logo/ora-logo.js`, `exporter.ps1`, cités p. 7 de la fiche) n'est pas dans ce dépôt.

## Produire

```bash
# Image fixe (post, flyer, story)
node ora/tools/render.mjs ora/templates/post-4x5.html ora/contenus/ORA_PRODUIT_X_POST_261103_v01.png

# Vidéo motion (la page expose window.ORA_DURATION et window.oraSeek(t))
node ora/tools/render.mjs ora/templates/story-9x16-motion.html ora/contenus/ORA_MARQUE_DETAIL_REEL_261103_v01.mp4 --fps 30

# Logo à une taille donnée
node ora/tools/render.mjs ora/logo/svg/ORA_logo_symbole_cuivre-sur-noir.svg sortie.png --width 512
```

Nécessite Node + Playwright (Chromium) et ffmpeg pour la vidéo. MP4 sortie : H.264, yuv420p, 30 i/s.

### Règles de motion (déduites de la charte, à valider)

- **Accroche (constaté sur TikTok, 2026-11-05) :** la majorité décroche à 0:02. La 1re image est complète : produit ou écran visible, titre déjà affiché, mouvement dès 0 s. Jamais de fondu au noir d'ouverture.

La charte ne fixe pas de règles vidéo détaillées. Celles-ci en sont déduites :

- Logo : apparition par fondu simple, puis fixe. Jamais animé de façon décorative (§5).
- Texte : fondu + montée courte (≤ 14 px), easing doux, une idée à la fois. Pas de rebond, pas de glitch, pas de zoom agressif.
- Pas de boucle décorative infinie (§10 bis, appliqué par cohérence).
- Franchise « Deux minutes » : geste technique filmé net, sans voix, sans musique forte (§9).
- Zone sûre 9:16 : rien d'important dans les 250 px du haut ni les 320 px du bas (§10).

### Contrôle avant livraison

Format §14.A pour toute création. Pré-vol §4 silencieux. Placeholders `[PRIX]`, `[DISPO]`, `[DÉLAI]`, `[GARANTIE]` pour toute information non fournie (règle zéro).
