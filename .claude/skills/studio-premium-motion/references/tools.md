# Outils — quand utiliser quoi

Les connecteurs disponibles varient selon le compte. Vérifie leur présence
(ToolSearch) avant de les annoncer à l'utilisateur.

## Pipeline local (toujours prioritaire pour l'animation)

HTML/CSS/JS + `assets/template.html` → `scripts/render.cjs` (Playwright + ffmpeg).
- Contrôle total de la typographie, des courbes et du timing, rendu image par image reproductible.
- Prérequis : Node, Playwright avec Chromium, ffmpeg. `node scripts/render.cjs --check` vérifie l'environnement.
- Les polices web doivent être accessibles (Google Fonts, fichiers locaux via `@font-face`, ou kit Adobe Fonts).

## Connecteur Adobe

- **Polices** : `font_search`, `font_recommend`, `font_preview`, `font_create_kit` / `get_fontkit_embed_url` pour obtenir un kit web Adobe Fonts à charger dans le HTML. La meilleure source de fontes premium si l'abonnement le couvre.
- **Retouche d'image** : détourage (`image_remove_background`), recadrage, grain, flou de profondeur (`image_apply_lens_blur`), étalonnage, extension générative (`image_generative_expand`) pour adapter une photo à un autre ratio.
- **Express** : `export_html_to_express` si le client veut éditer le visuel lui-même dans Adobe Express. Le serveur Adobe impose d'appeler `adobe_mandatory_init` en premier.
- `animate_design` anime un document Express existant : utile pour un client autonome, moins fin que le pipeline local.

## Flora / Figma (génération d'images)

- Textures, matières, décors abstraits, fonds. Annoncer le coût avant de générer (Flora le demande).
- Ne pas générer de fausse photo d'un lieu, d'un produit ou d'une personne réelle.

## Canva

- Handoff quand le client travaille dans Canva : import d'un motion depuis une URL, export, déclinaisons.
- Ne pas partir d'un template Canva pour un client premium : c'est précisément le rendu générique à éviter.

## v0 / Vercel

- Héberger un flyer animé en HTML (lien partageable, landing d'événement).

## Ce qui n'est pas couvert

- Conversion CMJN avec profil ICC (Acrobat, InDesign ou imprimeur).
- 3D réaliste et simulation (Blender, Cinema 4D) : hors périmètre ; on peut intégrer un rendu 3D fourni en vidéo ou en image.
