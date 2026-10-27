# Youmi Wings — reconstruction du flyer

Source : `IMG-20261026-WA0007.jpg`, 720 × 1080 px, flyer généré par ChatGPT.

## Ce qui a été produit

Deux directions, trois formats chacune, chacune en PDF print et PNG de contrôle.

| Fichier | Direction | Format | Taille du document |
|---|---|---|---|
| `out/youmi_v2_A5.pdf` | Reprise | A5 148 × 210 | 154 × 216 mm |
| `out/youmi_v2_A6.pdf` | Reprise | A6 105 × 148 | 111 × 154 mm |
| `out/youmi_v2_4x5.pdf` | Reprise | 4:5 social | 114 × 141 mm |
| `out/youmi_v3_A5.pdf` | Studio | A5 | 154 × 216 mm |
| `out/youmi_v3_A6.pdf` | Studio | A6 | 111 × 154 mm |
| `out/youmi_v3_4x5.pdf` | Studio | 4:5 social | 114 × 141 mm |

Chaque document inclut **3 mm de fond perdu sur les quatre côtés** : le format fini est le format nominal, le document papier est 6 mm plus grand.

## Direction retenue

**v4, fond noir** — le plat en grand, les bières en encart, le prix sur encre. Trois formats : A5, A6, 4:5.

## Les deux directions

**v2 « Reprise »** — même architecture que l'original : wordmark en haut sur fond encre, photo produit en bande pleine largeur, prix en gros chiffres, barre d'informations en bas, bandeau accent en pied. Ce qui change :

- une grille réelle (marges à 4,6 % du format, trois colonnes de coordonnées) ;
- deux familles typographiques (Lobster + Bevan pour la marque, Inter pour l'information) au lieu de cinq ;
- plus de badges à main levée, plus de contours blancs, plus de tache jaune en filigrane ;
- le prix passe de « 5 POU 1000 gds » collé à un bloc lisible ;
- la mention légale n'est plus un rond jaune illisible mais un bandeau.

**v3 « Studio »** — même contenu, recomposé. Le chiffre fait le travail : « 5 POU / 1 000 GDS » en trois lignes de grotesque condensé, un filet accent de 1,6 mm, la photo en bande pleine largeur qui occupe le bas. Aucun badge. C'est la version qui tient à 3 mètres.

## Ce qui n'a pas été copié, volontairement

L'original contient du **mobilier de marque tiers** : trois bouteilles **Prestige 50 ans** et un pictogramme de chope.

- Le **pictogramme de chope** (un emoji) n'a été repris dans aucune version.
- Les **bouteilles** ont été retirées de v2 et v3, puis **réintroduites dans v4** à la demande du client. Elles restent la propriété de Prestige : pour une impression commerciale, il faut leur accord écrit, sinon il faudra retirer l'encart ou le remplacer par un visuel de bière neutre.

Si Prestige est partenaire de l'opération, demande-leur leur **logo vectoriel** : l'encart sera refait avec leur fichier officiel au lieu d'une photo de produit prise dans le flyer d'origine.

## Limite à connaître : la photo

La source fait 720 px de large. À 300 DPI, elle ne couvre que **61 mm**. Un A5 en demande 148, un A3 en demande 297.

Ce qui a été fait : recadrage, agrandissement LANCZOS ×2,6, masque de netteté léger, puis réintroduction d'un grain fin (5,5 %) pour que la douceur se lise comme une texture photographique et non comme un flou. À l'écran et en A6, c'est bon. **En A4 ou A3, c'est visible.**

Deux sorties propres : demander la photo originale au client (téléphone récent = 4000 px, largement suffisant), ou faire un shooting. Tant que ce n'est pas fait, ce fichier est un bon A5 et un mauvais A3.

## État technique du PDF

Vérifié sur le fichier produit :

- page 154 × 216 mm exactement, soit 148 × 210 + 3 mm de fond perdu par côté ;
- couleurs écrites en **opérateurs CMJN** (`k` / `K`), aucun opérateur RVB ;
- **toutes les fontes embarquées** (7 fontes en v2, 4 en v3), licences SIL OFL ;
- images aplaties, pas de transparence ;
- fichiers texte cherchables, pas des images.

**Reste à faire avant l'imprimeur** : ajouter un *Output Intent* ICC (PDF/X-4). ReportLab n'en écrit pas. Une commande suffit :

```bash
gs -dSAFER -dBATCH -dNOPAUSE -dPDFX \
   -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress \
   -sOutputICCProfile=/usr/share/color/icc/ISOcoated_v2_300_eci.icc \
   -sOutputFile=youmi_v2_A5_X4.pdf youmi_v2_A5.pdf
```

Sans Ghostscript, Pitstop ou Acrobat Pro le font. Le fichier actuel s'imprime très bien en pratique ; le profil est la ceinture de sécurité.

## Ce qu'il me faut pour aller plus loin

1. **La photo originale** (ou 3–4 autres prises du plat) — c'est le seul vrai plafond de qualité.
2. **Le logo Youmi en vectoriel** (SVG, AI ou EPS). Dans ce fichier, le wordmark est recomposé en Lobster + Bevan : beau, mais ce n'est pas *ton* logo. Si tu as le vrai, tout s'aligne.
3. **Le prix exact** : « 5 pou 1 000 gds » — est-ce 5 wings pour 1 000 gourdes, ou 5 pièces + une bière ?
4. **La bière** : Prestige est partenaire ou c'est juste un clin d'œil ?
5. **Le format cible** : A5 pour la main, A3 pour la vitrine, A6 pour le sac ? Je décline tout en une commande.

## Régénérer

```bash
python3 prepare_assets.py        # recadre et nettoie les photos depuis la source
python3 build.py                 # tous les formats, les deux directions
python3 build.py v3 A5           # une seule sortie
```

Toute la mise en page est dans `build.py`, en millimètres, écrite une seule fois et rendue par deux backends : Pillow pour le PNG de contrôle, ReportLab pour le PDF vectoriel. Le contrôle ne peut donc pas diverger du fichier d'impression.

Polices : Lobster, Bevan, Anton, Inter, Archivo Black, Space Mono, Playfair Display Italic — toutes SIL OFL, téléchargées dans `.tmp-fonts/`.
