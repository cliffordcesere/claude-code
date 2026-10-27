# Matières, palettes et voix typographiques

Une **matière** n'est pas une couleur : c'est un ensemble cohérent (support, encres, typographie, texture). On en choisit une seule par projet, et on n'en change plus.

Les fontes citées sont toutes sous SIL Open Font License (Google Fonts, embedding PDF autorisé). Vérifie la licence si tu télécharges une version modifiée.

---

## 1. Encre litho sur chiffon — *par défaut*

Papier non couché légèrement froid, deux encres, un accent imprimé en aplat franc.

- Fond papier `#DFE0DB`
- Encre `#111315`
- Accent **jaune de chrome** `#F2C14E` — surface maximale 4 %
- Graphite (filets, mentions) `#3A4048`

Typographie : titre **Newsreader** (400/600, interlettrage -2 %), courant **Archivo** (400, interlignage 1,42), chiffres **Archivo** tabulaire.
Textures autorisées : grain 3 %, léger défaut de repérage simulé (0,3 mm) sur l'accent uniquement.

*Pourquoi ce défaut :* il imprime proprement en deux passages, coûte peu cher, et ne ressemble à aucune des palettes générées d'usage.

## 2. Sérigraphie sur kraft

Deux tons, pas plus. Le support est visible et fait partie du design.

- Fond kraft `#B98A5E` (ou couleur réelle du support)
- Encre `#1B1A17`
- Accent blanc opaque `#F5F2EA` — 100 % de couverture, pas de demi-teinte

Typographie : titre **Archivo Expanded** (700, capitales, interlettrage +1 %), courant **Newsreader** italique.
Contrainte : la sérigraphie ne gère pas les dégradés fins. Aplats, traits épais (≥ 1,5 mm), pas de photo tramée au-delà de 45 lpi.

## 3. Gaufrage à sec sur blanc optique

Luxe de retenue : aucune couleur, seulement du relief et de la lumière rasante.

- Fond blanc optique `#FAFAF7`
- Relieflisible `#EDEDE8` / ombre `#D6D4CC`
- Accent : néant, ou un seul filet `#9A9A93`

Typographie : titre **Bodoni Moda** (500), courant **Inter** (300, corps 9/13).
Danger : sans encre, la composition doit être irréprochable. Aucun élément ne peut se rattraper par la couleur.

## 4. Bichromie froide — écran et social

Pour du digital uniquement : deux teintes froides, contraste élevé, lisible en vignette.

- Fond `#0C1B21` (pétrole)
- Texte `#E6EDED`
- Accent `#9FD8D0` — surface maximale 6 %
- Filets `#2A4048`

Typographie : titre **Instrument Serif** ou **Archivo Expanded**, courant **Inter Tight**.

## 5. Argentique — photo et grain

Quand il y a une image réelle, elle porte tout. La typo se retire.

- Noir photographique `#151311`
- Blanc cassé `#EFEAE0`
- Accent unique choisi dans l'image elle-même (échantillonné, pas inventé)

Typographie : titre **Newsreader** 300, très grand corps ; courant **Inter** 400 à 8/12 pt.
Traitement : grain 4 %, désaturation -15 %, halo léger, aucun filtre « vintage » préréglé.

## 6. Signalétique industrielle

Pour affiches de salle, concerts, événements sportifs.

- Fond encre `#101418`
- Blanc `#F2F2F0`
- Accent **orange sécurité** `#FF5A1F` — usage fonctionnel (flèche, numéro, urgence)

Typographie : titre **Archivo Black** capitales condensées, courant **JetBrains Mono** (données : horaires, numéros, prix).
Règle : chaque élément graphique doit encoder une information (ordre, hiérarchie, parcours). Rien d'ornemental.

---

## Palettes à éviter

| Combinaison | Pourquoi |
|---|---|
| `#F4F1EA` + `#D97757` + serif contraste | signature d'un rendu généré, y compris dans ce dépôt voisin |
| Quasi-noir + un seul accent vert acide | idem, très daté 2023-2025 |
| Dégradé violet → bleu saturé | tell de gabarit |
| Or métallisé simulé sur noir | lit « parfum discount » si l'or est un simple dégradé |

## Choisir un accent

Un seul accent, et il doit être **imprimable** :

- Évite les verts et bleus saturés en RVB : ils s'assombrissent en CMJN.
- Vérifie le contraste de l'accent sur le fond : texte sur accent ≥ 4,5:1, accent sur fond ≥ 3:1.
- Si l'accent ne sert qu'à décorer, supprime-le.
