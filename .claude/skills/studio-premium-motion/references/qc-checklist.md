# Contrôle qualité avant livraison

Passe chaque point. Signale à l'utilisateur ceux que tu n'as pas pu vérifier.

## Contenu
- [ ] Date, heure, lieu, prix, URL identiques au brief, au caractère près. Aucun élément inventé.
- [ ] Orthographe et typographie française (insécables, apostrophes, accents sur capitales).
- [ ] Placeholders `[…]` restants listés explicitement dans la note de livraison.

## Image fixe (composition finale, `--still`)
- [ ] Un héros clair ; l'information principale se lit en 1 seconde.
- [ ] Lisible en miniature : regarder l'image réduite à ~25 % (`--still … --scale 0.25`).
- [ ] Contraste suffisant des infos pratiques.
- [ ] Aucune ligne de titre avec un mot isolé ; césures voulues.
- [ ] Zones de sécurité respectées (rendre avec `?guides=1` pour vérifier, puis sans).
- [ ] Aucun marqueur de rendu générique (liste dans `art-direction.md`), ou alors justifié par le concept.

## Mouvement
- [ ] Première image composée (pas de cadre vide).
- [ ] Une seule chose qui bouge à la fois ; ordre d'apparition = hiérarchie.
- [ ] Temps de lecture final suffisant.
- [ ] Pas de saccade, pas de saut d'un élément entre deux images (vérifier 3–4 images clés autour des transitions).
- [ ] Boucle propre si le format boucle.

## Technique
- [ ] Le rendu n'a pas signalé de police manquante.
- [ ] Dimensions, cadence et durée conformes au canal (`ffprobe` sur le fichier).
- [ ] Poids raisonnable (MP4 story 8 s : quelques Mo ; GIF e-mail < 2 Mo).
- [ ] Fichiers nommés `CLIENT_PROJET_FORMAT_vNN.ext`.
- [ ] Licences : polices (usage vidéo/commercial), photos, musique éventuelle.

## Note de livraison (à joindre)
Formats produits · hypothèses prises · points à valider par le client · limites connues (ex. PDF en RVB).
