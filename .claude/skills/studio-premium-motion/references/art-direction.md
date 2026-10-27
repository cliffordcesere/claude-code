# Direction artistique — référence

## Sommaire
1. Marqueurs de rendu générique à éliminer
2. Typographie
3. Grille et composition
4. Couleur
5. Image et matière
6. Typographie française

---

## 1. Marqueurs de rendu générique à éliminer

Ce sont les signes qui font dire « c'est un template » ou « c'est fait par une IA ».
Passe ta composition au crible :

- Dégradé violet → bleu ou rose → orange en fond, halos néon, glassmorphism.
- Inter, Roboto, Montserrat, Poppins, Arial ou Helvetica par défaut **en titre**.
- Tout centré, tout de la même importance, aucun élément dominant.
- Ombres portées, contours, biseaux, reflets, effets 3D gratuits.
- Emojis, icônes de banque d'images, pictogrammes en ligne génériques.
- Noir pur `#000` sur blanc pur `#FFF` sans intention.
- Texte posé sur une photo sans gestion du contraste (ni zone calme, ni dégradé local).
- Cinq informations au même niveau de corps.
- Majuscules partout avec interlettrage par défaut.
- Coins arrondis « carte d'interface » sur un support éditorial.
- Un seul mot en italique ou en couleur au milieu d'un titre romain (« La nuit *des* lumières ») :
  devenu la signature des maquettes générées. Traite le titre d'un seul tenant, ou change de ligne et de corps.
- Petits labels en capitales espacées au-dessus des titres et des infos (« DATE », « LIEU ») :
  préférer la fonte de texte, un cran plus petite, en casse normale, sans interlettrage.
- Badges, pastilles et coups de pinceau pour signaler une offre : l'offre est une ligne de la hiérarchie, pas un autocollant.

Un élément de cette liste peut être justifié par le concept (un dégradé dans une
direction rétro-futuriste assumée, par exemple). Dans ce cas, il est poussé à fond et
expliqué, pas laissé par défaut.

## 2. Typographie

**Deux familles maximum.** Typiquement une display (serif à fort contraste, grotesque
étroite, ou fonte de caractère) et une fonte de texte neutre et précise.

**Choix des fontes** — par ordre de préférence :
1. Les polices de la marque cliente (vérifier la licence web/vidéo).
2. Adobe Fonts via le connecteur Adobe (`font_search`, `font_recommend`) si l'abonnement le couvre.
3. Fonderies premium achetées pour le projet (Pangram Pangram, Grilli Type, Klim, Commercial Type, Dinamo, Displaay).
4. Google Fonts choisies avec soin. Bonnes options moins vues : Instrument Serif, Fraunces,
   Newsreader, Bodoni Moda, Gloock, Young Serif (serifs) ; Inter Tight, Hanken Grotesk,
   Familjen Grotesk, Schibsted Grotesk, Bricolage Grotesque, Unbounded (sans) ; Martian Mono,
   IBM Plex Mono (mono pour les détails). Éviter Playfair Display et Montserrat, devenus des marqueurs de template.

**Échelle.** Contraste de corps franc entre titre et texte : ratio ≥ 4 entre le titre et
les infos secondaires sur un format story. Une hiérarchie timide (titre 1,5× le texte)
est l'un des défauts les plus « amateurs ».

**Réglages display :**
- Interlignage 0,85–1,0 pour les titres sur plusieurs lignes.
- Approche (letter-spacing) légèrement négative en grand corps : -0,01 à -0,04 em.
- Petites capitales et labels : majuscules, corps petit, approche +0,08 à +0,16 em.
- Chiffres : `font-variant-numeric: tabular-nums` pour les dates/heures alignées, ou chiffres elzéviriens dans un texte serif.
- Ligatures et alternates stylistiques (`font-feature-settings: "ss01"`, `"dlig"`) quand la fonte en a — c'est souvent là que se cache le caractère.

**Césure manuelle.** Coupe les lignes des titres à la main (`<span class="line">`)
pour que la forme du bloc soit voulue : pas de mot isolé, rythme long/court assumé.

## 3. Grille et composition

- Marges généreuses : au moins 6–8 % de la largeur sur chaque côté. Le vide est un signe de confiance.
- Grille de 6 ou 12 colonnes, ou modulaire ; aligne tout sur elle. L'alignement à gauche
  (fer à gauche) paraît plus éditorial et plus « studio » que le centrage systématique.
- Un **héros** (titre, image ou objet) occupe 40–70 % de la surface. Le reste est subordonné.
- Les infos pratiques (date, lieu, URL) sont regroupées dans un bloc compact, petit, très lisible, souvent ancré à un bord.
- Tension : asymétrie, éléments qui débordent du cadre (fonds perdus), échelle extrême
  d'un mot ou d'un chiffre. Un seul geste fort vaut mieux que trois moyens.
- Zones de sécurité des formats sociaux : voir `formats.md`.

## 4. Couleur

- Palette de 2 à 3 couleurs plus un neutre. Un accent utilisé avec parcimonie (< 10 % de la surface).
- Noirs et blancs « teintés » : noir chaud `#0E0D0B`, noir froid `#0A0C10`, ivoire `#F3EEE4`, papier `#EDEAE3`.
- Vérifie le contraste des infos pratiques (WCAG AA au minimum : 4,5:1 pour le petit texte).
- Si la marque impose ses couleurs, travaille les proportions et les neutres plutôt que d'ajouter des teintes.

## 5. Image et matière

- Une image forte plutôt qu'un collage. Étalonnage cohérent (même température, même noir) sur toutes les images.
- Texte sur image : choisir une zone calme de l'image, ou poser un dégradé local doux (pas un voile uniforme).
- **Grain** : 2–5 % d'opacité, animé à ~12 images/s. Il donne de la matière et supprime le banding des
  dégradés après compression vidéo. Le template le fournit.
- Pas d'image générée par IA présentée comme une photo réelle du lieu, du produit ou d'une personne
  réelle. Pour une matière abstraite, une texture ou un décor, c'est acceptable si le client le sait.
- Droits : vérifier l'origine de chaque photo, logo et police (licence couvrant la vidéo et l'usage commercial).

## 6. Typographie française

Un client francophone exigeant les remarque immédiatement :
- Espace fine insécable (`&#8239;`) avant `; ! ?` et espace insécable (`&nbsp;`) avant `:` et à l'intérieur des guillemets `« … »`.
- Apostrophe typographique `’`, pas `'`. Points de suspension `…`.
- Heures : `20 h 30` ou `20h30` (cohérent sur tout le support), jamais `20:30` en français éditorial sauf choix graphique assumé.
- Dates : `14.11.2026` ou `14 novembre 2026` ; pas de mélange.
- Majuscules accentuées : `É`, `À`, `Ç` — obligatoires.
- Insécables entre nombre et unité (`25 €`, `3 km`) et dans les noms propres courts.
