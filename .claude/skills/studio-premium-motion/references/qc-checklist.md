# Contrôle qualité avant livraison

Passe chaque point. Signale à l'utilisateur ceux que tu n'as pas pu vérifier.

## Contenu
- [ ] Date, heure, lieu, prix, URL identiques au brief, au caractère près. Aucun élément inventé.
- [ ] Orthographe et typographie française (insécables, apostrophes, accents sur capitales).
- [ ] Placeholders `[…]` restants listés explicitement dans la note de livraison.

## Image fixe (composition finale, `--still`)
- [ ] Un héros clair ; l'information principale se lit en 1 seconde.
- [ ] Lisible en miniature : regarder l'image réduite à ~25 % (`--still … --scale 0.25`).
- [ ] Infos pratiques ≥ 36 px et nom de marque ≥ 56 px sur un format 1080 de large (≈ 13 pt et 20 pt sur téléphone).
- [ ] Contraste suffisant des infos pratiques.
- [ ] Aucune ligne de titre avec un mot isolé ; césures voulues.
- [ ] Accents des capitales intacts (É, È, À, Ç) dans l'image finale : un masque de révélation trop serré les rogne.
- [ ] Zones de sécurité respectées (rendre avec `?guides=1` pour vérifier, puis sans).
- [ ] Aucun marqueur de rendu générique (liste dans `art-direction.md`), ou alors justifié par le concept.

## Mouvement
- [ ] Première image composée (pas de cadre vide).
- [ ] Une seule chose qui bouge à la fois ; ordre d'apparition = hiérarchie.
- [ ] Temps de lecture final suffisant.
- [ ] Pas de saccade, pas de saut d'un élément entre deux images (vérifier 3–4 images clés autour des transitions).
- [ ] Boucle propre si le format boucle.

## Son (si présent)
- [ ] Chaque impact tombe sur l'arrivée visuelle de l'élément (± 1 image).
- [ ] Sonie ≈ -14 LUFS, crête < 0 dBFS (`ffmpeg -af ebur128=peak=true`).
- [ ] Équilibre vérifié aussi à travers un passe-haut 180 Hz (haut-parleur de téléphone).
- [ ] Droits : musique fournie par le client ou générée ; jamais une piste du commerce sans licence.

## Technique
- [ ] Le rendu n'a pas signalé de police manquante.
- [ ] Dimensions, cadence et durée conformes au canal (`ffprobe` sur le fichier).
- [ ] Poids raisonnable (MP4 story 8 s : quelques Mo ; GIF e-mail < 2 Mo).
- [ ] Fichiers nommés `CLIENT_PROJET_FORMAT_vNN.ext`.
- [ ] Licences : polices (usage vidéo/commercial), photos, musique éventuelle.

## Note de livraison (à joindre)
Formats produits · hypothèses prises · points à valider par le client · limites connues (ex. PDF en RVB).
