# Specs print

## Formats

| Usage | Dimensions (mm) | Fond perdu | DPI |
|---|---|---|---|
| A6 flyer | 105 × 148 | 3 mm | 300 |
| A5 flyer | 148 × 210 | 3 mm | 300 |
| A4 | 210 × 297 | 3 mm | 300 |
| **A3 affiche** (défaut) | 297 × 420 | 3 mm | 300 |
| A2 | 420 × 594 | 3 mm | 300 |
| A1 | 594 × 841 | 5 mm | 300 |
| Bâche / grand format | > 1 m | 10 mm | 150 (ou 72 au-delà de 3 m) |
| Carré social | 1080 × 1350 px | — | 72 (écran) |
| Story | 1080 × 1920 px | — | 72 (écran) |

Calcul DPI grand format : `DPI ≈ 9000 / distance de lecture en cm`. Un 4 × 3 m vu à 3 m se conçoit à ~30 DPI réels ; on reste néanmoins à 100–150 DPI pour la marge de sécurité.

## Fond perdu, traits de coupe, sécurité

```
┌──────────────────────────────┐  ← bord du document = trait de coupe + fond perdu
│  ┌────────────────────────┐  │
│  │   zone de sécurité     │  │      fond perdu : +3 mm au-delà du format fini
│  │   (aucun texte ici)    │  │      sécurité   : -5 mm à l'intérieur du format fini
│  └────────────────────────┘  │
└──────────────────────────────┘
```

- Le fond perdu s'applique au **document**, pas au contenu : le PDF fait 303 × 426 mm pour un A3.
- Aucun texte ni logo à moins de 5 mm du trait de coupe.
- Traits de coupe (crop marks) inclus, à 3 mm du format fini, longueur 5 mm, épaisseur 0,25 pt, en repérage.

## Couleur

- **CMJN**, profil **ISO Coated v2 (FOGRA39)** pour du couché, **ISO Uncoated** pour du non couché.
- Conversion **avant** le rendu final ; ne jamais laisser le prestataire convertir à l'aveugle.
- Texte noir : **K100 uniquement**. Un texte en quadri noir se décale à l'impression.
- Aplats noirs > 30 % de la surface : **noir riche** `C60 M40 Y40 K100`.
- Totaux d'encre : **≤ 300 %** (feuilles à séchage lent : ≤ 280 %).
- Surimpression : activer uniquement sur le noir de texte, sur aplat clair, jamais sur un visuel.

## Images

- Résolution réelle ≥ 300 DPI au format final (pas de « suréchantillonnage » d'une image 72 DPI).
- Profil source converti en CMJN ; conserve une version RVB pour le web.
- Pas de transparence (aplatie), pas de calque masqué, pas de lien manquant.

## Typographie

- Fontes **embarquées** ou vectorisées. Une fonte commerciale sans licence d'embedding est un risque juridique, pas un détail.
- Corps minimum : 6 pt pour les mentions légales, 8–9 pt pour le texte courant, jamais moins de 5 pt.
- Interlettrage négatif sur les gros corps uniquement ; ne pas descendre sous -4 %.

## Export

1. PDF/X-4 (transparence aplatie, profils intégrés) pour l'imprimeur.
2. PNG 2× RVB pour la validation client.
3. Les deux versions portent le même nom de base, dossier par commande.
4. Contrôle : ouvrir le PDF, zoomer à 400 % sur la mention la plus petite, vérifier qu'aucune ligne ne touche la sécurité.

## Contrôle automatique

```bash
node scripts/preflight.mjs fichier.pdf --trim 297 420
node scripts/preflight.mjs affiche.png --trim 297 420 --dpi 300
```

Le script lit les dimensions réelles et l'espace colorimétrique (via ImageMagick `identify` si présent), calcule le DPI effectif au format fini, et signale un fond perdu absent. Sans ImageMagick, il affiche les commandes à lancer manuellement.

```bash
# À la main, si ImageMagick est installé
identify -format "%w x %h | %[colorspace] | %x x %y ppi\n" fichier.png
# Vérifier les polices embarquées d'un PDF
pdffonts fichier.pdf
# Vérifier l'espace colorimétrique d'un PDF
gs -o /dev/null -sDEVICE=inkcov fichier.pdf
```
