# ORA — semaine 1 (à partir du 2026-11-04)

Règle du propriétaire (2026-11-04) : **toujours montrer le produit vendu**, de préférence en photo maison.

## Livré — câble USB-C coudé 90° (100 W, 1 m)

| Fichier | Canal | Contenu |
|---|---|---|
| `ORA_PRODUIT_CABLE-USBC-90_REEL_261104_v02.mp4` | TikTok, Reels, statut WhatsApp | 15,5 s avec son : coude → embout droit → « 1 mètre » (règle 0→100 cm) → « 100 W » → fin |
| `ORA_PRODUIT_CABLE-USBC-90_REEL-MUET_261104_v02.mp4` | Idem | Même vidéo sans son, pour poser un son TikTok/Instagram à la place |
| `ORA_PRODUIT_CABLE-USBC-90_POST_261104_v02.png` | Instagram, chaîne WhatsApp | Embout coudé, « Coudé à 90°. », 100 W · 1 mètre · USB-C des deux côtés |

Sources : `cable-reel-v2.html`, `cable-post-v2.html`. Photos : `ora/produits/cable-usbc-90/` (photos maison 1 et 2, détourées par IA en local, plaque retirée).
La v1 (photo fournisseur) est retirée : elle faisait croire à un câble court.

## Captions

**TikTok**
```
Coudé à 90°. 100 W. Un mètre. Disponible à Delmas.
```

**Instagram / Reels**
```
Le connecteur coudé garde le câble le long du téléphone. USB-C des deux côtés, 100 W, un mètre. Disponible à Delmas, réponse sur WhatsApp.
#ORA #PortauPrince #USBC
```

**Statut WhatsApp** : la vidéo avec son, sans texte.

## Son

Synthétisé (`tools/son.py`) : nappe discrète, souffles aux transitions, crans pendant les compteurs, note grave au logo. Aucun droit à gérer.
Non écouté avant livraison : vérifier au casque et sur le haut-parleur du téléphone.

## Prochaines photos (pour aller plus loin)

1. Le câble **entier**, posé en S sur une feuille ou un sol uni : montre le mètre pour de vrai.
2. Le coude **branché** dans un téléphone tenu à l'horizontale : montre l'usage.
3. Lumière du jour, sans soleil direct, appareil stable : moins de bruit sur le métal de l'embout.

## Tuto — « Avant d'acheter un iPhone d'occasion » (37 s)

Fichiers : `ORA_EDUCATION_IPHONE-OCCASION_TUTO_261104_v01.mp4` (avec son), `…TUTO-MUET…` (sans son). Source : `tuto-iphone-occasion.html`.
Interface iOS 27 reconstruite d'après les captures du propriétaire (Réglages FR avec bloc compte Apple, bouton retour rond, recherche flottante ; Informations iOS 27 avec référence affichée directement). Compte « Jean M. » et valeurs fictifs ; IMEI et numéro de série floutés.

TikTok : `Trois vérifications avant d'acheter un iPhone d'occasion.`
Instagram : `Batterie, référence, IMEI. Trois écrans à regarder avant de payer un iPhone d'occasion. Chez ORA, l'état de chaque appareil est dit avant la vente. #ORA #PortauPrince #iPhone`

À faire vérifier sur un vrai iPhone : page Batterie d'iOS 27 (faite d'après iOS 26, aucune capture) ; règle M / F / N ; seuil de 80 % ; cycles affichés à partir de l'iPhone 15.

### Écran de fin
Logo vertical centré + WhatsApp en cuivre + « Delmas, Haïti ». Écart à la charte à valider (§5 : logo centré réservé au pilier MARQUE ; taille 5–8 %).

### Voix off — texte à lire (~40 s)
- [Intro] Avant d'acheter un iPhone d'occasion, faites ces trois vérifications.
- [1] Un : la batterie. Réglages, Batterie, État de la batterie. Sous 80 % de capacité maximale, elle est usée. Sur iPhone 15 et plus récents, regardez aussi le nombre de cycles.
- [2] Deux : neuf ou reconditionné. Réglages, Général, Informations. Regardez le numéro de modèle. M, c'est neuf. F, reconditionné. N, un appareil de remplacement.
- [3] Trois : l'IMEI. Tapez étoile, dièse, zéro, six, dièse. Le numéro doit être le même que sur la boîte et sur la facture.
- [Fin] Chez ORA, neuf ou occasion, c'est toujours dit clairement.

Enregistrement : pièce calme, téléphone à 20 cm, une partie à la fois avec 2 s de silence, voix calme, fichier d'origine (pas de vocal WhatsApp). La vidéo sera recalée sur la voix.

### Version voix off (2026-11-05)
`ORA_EDUCATION_IPHONE-OCCASION_TUTO-VOIX_261104_v01.mp4` — 43 s. Rendu : `tuto-iphone-occasion.html?voix`.
La voix et cette vidéo restent en local (exclues du dépôt via .gitignore) tant que le propriétaire n'a pas dit qu'il veut les y mettre.
Écrans recalés sur la voix (repères `VOIX.reperes` dans la page), nappe baissée de 11 dB pendant la voix.
À noter : « va dans Réglages » (0:06) tutoie ; vers 0:20, peut-être aussi (transcription incertaine).
ElevenLabs en direct : bloqué par le réseau de la session (api.elevenlabs.io). Le Voice Changer d'ElevenLabs garde le minutage : la synchro resterait valable.

### Voix off v02 (2026-11-05)
`ORA_EDUCATION_IPHONE-OCCASION_TUTO-VOIX_261104_v02.mp4` — 37 s (43 s en v01). Voix v2 : pauses plafonnées à 0,26 s (0,5 s entre parties), +7 % sans changer la hauteur, égalisation (-4,5 dB à 250 Hz, +3,5 dB à 3,5 kHz), atténuation de la résonance entre les mots, -14 LUFS. Repères recalculés par `tools/resserrer_voix.py`.
Retour propriétaire : voix trop lente, effet « chambre vide ». La résonance est atténuée, pas supprimée. Prochaine étape envisagée : ElevenLabs (clone de la voix du propriétaire ou Voice Changer).

### v03 (2026-11-05) — après les stats TikTok du reel câble (décrochage à 0:02)
- Accroche : plus de fondu au noir ; 1re image = titre affiché + « Capacité maximale 87 % » en surbrillance, poussée lente ; passage à Réglages à 3,6 s.
- Référence : la 1re lettre change avec la voix — **M**YE73ZD/A → **F**YE73ZD/A → **N**YE73ZD/A (lettre en cuivre).
- Fichiers : `…TUTO-VOIX_261104_v03.mp4` (local, hors dépôt), `…TUTO_261104_v02.mp4` et `…TUTO-MUET_261104_v02.mp4` (sans voix, mêmes corrections).

### v04 (2026-11-05) — pour un public débutant
- Étape 1 : écran d'accueil de l'iPhone, appui sur l'icône Réglages (entourée de cuivre) quand la voix dit « Réglages », puis ouverture de l'app.
- Étape 3 : même chose avec l'app Téléphone dans le dock.
- Étape 2 inchangée : on est déjà dans Réglages, retour à sa page principale.
- Accueil et clavier en zoom 0,72 : tout reste au-dessus des 320 px du bas (interface TikTok).
- Fichiers : `…TUTO-VOIX_261104_v04.mp4` (local, hors dépôt) ; `…TUTO_261104_v03.mp4` et `…TUTO-MUET_261104_v03.mp4` (sans voix).

### Publication du tuto
TikTok : `Avant d'acheter un iPhone en Haïti : comment repérer un zaza. #iphone #zaza #haiti` — en journée (16 h conseillé), programmable dans TikTok Studio.

## Tuto « iPhone plein » 1/3 — Supprimées récemment (2026-11-06)
- `ORA_EDUCATION_IPHONE-PLEIN-1_TUTO_261106_v01.mp4` (habillage sonore) et `…TUTO-MUET…` (base voix off). 17,6 s. Source : `stockage-supprimees.html` + moteur `templates/moteur-tuto-ios.js`.
- Déroulé : jauge 61,2/64 Go → accueil, appui sur Photos → défilement jusqu'à « Autres » → Supprimées récemment (verrouillé, « Afficher l'album ») → Sélectionner → Tout supprimer → confirmation → album vide → jauge 55,8/64 Go → signature « La tech, en clair. » + Partie 1 sur 3.
- Libellés vérifiés (captures + recherche web) : « Supprimées récemment », verrouillage par code, Sélectionner, Tout supprimer / Tout récupérer, jusqu'à 30 jours. Non vérifiés : fenêtre de confirmation, album vide.
- TikTok : `iPhone plein : vos photos supprimées sont encore là. #iphone #stockage #haiti`
- Voix off : Vous supprimez vos photos. Votre iPhone, lui, les garde. / Jusqu'à trente jours, dans Supprimées récemment. / Ouvrez Photos. Descendez jusqu'à Supprimées récemment. Entrez votre code. / Touchez Sélectionner, puis Tout supprimer. / L'espace revient tout de suite. / Partie 1 sur 3. La suite : les doublons.

### Voix off, version parlée (2026-11-06)
Vous venez d'effacer deux cents photos, et votre iPhone affiche encore : stockage plein. / C'est normal : elles ne sont pas parties. L'iPhone les garde trente jours, au cas où vous changeriez d'avis. / Pour vraiment faire de la place : ouvrez Photos, descendez tout en bas, Supprimées récemment. / Il vous demande votre code, c'est normal. / Touchez Sélectionner, puis Tout supprimer. Et là, la place revient vraiment. / Dans la prochaine vidéo, je vous montre les doublons.
Tout se dit, avec vos mots. Seuls les mots-clés (Photos, Supprimées récemment, Tout supprimer), la 1re et la dernière phrase restent exacts.

### v02 (2026-11-06) — interface iOS 27.1 d'après captures réelles
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO_261106_v02.mp4` (+ MUET), 18,8 s. Parcours : Photos › Collections › Suppr. récemment (Face ID ou code) › Sélect. › glisser › « ··· » › Supprimer › Supprimer de tous les appareils.
Voix off : … ouvrez Photos, touchez Collections, descendez jusqu'à Supprimées récemment. Il vous demande Face ID ou votre code, c'est normal. Touchez Sélectionner, glissez le doigt sur vos photos, puis les trois petits points, et Supprimer. …
À confirmer : sélection de tout l'album ; confirmation au pluriel.

### v03 (2026-11-06) — flux exact d'après une vidéo d'écran iOS 27.1
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO_261106_v03.mp4` (+ MUET), 17,8 s. Sélect. → « ··· » → Tout supprimer → Supprimer de tous les appareils (sans cocher ni glisser).
Voix off : … Touchez Sélectionner, puis les trois petits points, et Tout supprimer. …

### v04 (2026-11-07) — icônes iOS redessinées à l'identique (monochrome)
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO_261107_v04.mp4` (+ MUET). Écran d'accueil d'après la capture iOS 27.1 : widgets Météo/Photos, 4 rangées, dessins fidèles ; TV remplacée par Calculette (pas de logo Apple).

### Version avec voix (2026-11-07) — À PUBLIER
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO-VOIX_261107_v01.mp4` — 28,4 s, voix du propriétaire, écrans calés sur les mots-clés ; icône TV avec la pomme remise. Hors dépôt (voix).
Rendu : `stockage-supprimees.html?voix` (repères dans `voix.reperes`). Sans voix : `…TUTO_261107_v05.mp4` (+ MUET).
TikTok : `iPhone plein : vos photos supprimées sont encore là. #iphone #stockage #haiti`

### Version avec voix v02 (2026-11-07) — À PUBLIER
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO-VOIX_261107_v02.mp4` — 25,6 s. Voix +8 % (24,6 s), début animé : jauge qui se remplit (0–4 s), ligne Photos (4–6 s), « Pourquoi · Gardées 30 jours » sur l'album avec « 29 jours » (6–9 s), puis le parcours. Sans voix : `…TUTO_261107_v06.mp4` (+ MUET).

### Version avec voix v03 (2026-11-07) — À PUBLIER
`ORA_EDUCATION_IPHONE-PLEIN-1_TUTO-VOIX_261107_v03.mp4` — 25,6 s. Ouverture « poubelle » (0–2,4 s) : 8 photos tombent dans la corbeille, « 29 jours · avant la suppression définitive », puis le téléphone monte sur « iPhone ». Sans voix : `…TUTO_261107_v07.mp4` (+ MUET).

### v04 voix / v08 sans voix (2026-11-07) — logos des apps
Liste « Stockage iPhone » : logos Photos (fleur), WhatsApp, TikTok, Facebook, YouTube en monochrome. `…TUTO-VOIX_261107_v04.mp4` (hors dépôt), `…TUTO_261107_v08.mp4` (+ MUET).

## Tuto « iPhone plein » 2/3 — Doublons (2026-11-07)

v02 sans voix, 21,8 s : `ORA_EDUCATION_IPHONE-PLEIN-2_TUTO_261107_v02.mp4` (sera recalée sur la voix).
Écrans d'après la vidéo d'écran iOS 27.1 (2026-11-07) : Photos › Collections › Doublons › Sélect. › Tout sélectionner › Fusionner (186) › « Fusionner 186 éléments… » › « Fusionner 186 éléments », puis « 0 élément », « Aucune photo ou vidéo ». Valeurs fictives.

- TikTok : `iPhone plein : la même photo, en double. Partie 2/3. #iphone #stockage #haiti`
- Commentaire à épingler :
  > Photos › Collections › Doublons › Sélect. › Tout sélectionner › Fusionner.
  > Deux choix s'affichent : « Fusionner … éléments » fusionne tout ; « … copies exactes uniquement » ne touche qu'aux photos identiques (plus prudent).
  > L'iPhone garde la meilleure version de chaque photo. Le reste va dans Supprimés récemment : videz-le pour libérer l'espace (partie 1).
  > Album Doublons absent : votre iPhone n'en a pas trouvé, ou il les cherche encore.

### Voix off — à dire avec vos mots

> Votre iPhone garde souvent la même photo en double. Parfois en triple.
> Ouvrez Photos, touchez Collections, puis Doublons.
> Touchez Sélectionner, puis Tout sélectionner.
> En bas, touchez Fusionner. Il vous propose deux choix : prenez celui du bas, puis confirmez.
> L'iPhone garde la meilleure version de chaque photo.
> Le reste part dans Supprimés récemment : videz-le, comme dans la partie 1, sinon l'espace ne revient pas.
> Partie 2 sur 3. La suite : WhatsApp.

Tout se dit, avec vos mots. Restent exacts (l'écran change dessus) : Photos, Collections, Doublons, Sélectionner, Tout sélectionner, Fusionner, Supprimés récemment ; et la 1re et la dernière phrase.

### Version avec voix (2026-11-08) — À PUBLIER

`ORA_EDUCATION_IPHONE-PLEIN-2_TUTO-VOIX_261108_v02.mp4` (24,7 s, hors dépôt) — fichier Adobe Podcast « optimisé v2 » (la v01 avait été faite sur le mauvais fichier, supprimée). Voix +8 %, pauses resserrées, traitement « pièce vide », -14,7 LUFS. Écrans calés sur : en double, triple, Photos, Collections, Doublons, Sélectionner, tout, Fusionner, celui du bas, confirmez, meilleure version, Supprimés récemment.
La dernière phrase (« Partie 2 sur 3. La suite : WhatsApp. ») n'est pas dans la prise ; l'écran de fin l'affiche en texte.

## Tuto « iPhone plein » 3/3 — WhatsApp (lancé le 2026-11-08)

En préparation : écrans WhatsApp d'après une vidéo d'écran à recevoir. Ouverture : page Stockage iPhone (partie 1), ligne WhatsApp en cuivre.

- TikTok : `iPhone plein : WhatsApp prend plus de place que vous ne pensez. Partie 3/3. #iphone #stockage #whatsapp #haiti`
- Commentaire à épingler :
  > WhatsApp › Vous (ou Réglages) › Stockage et données › Gérer le stockage › Plus de 5 Mo › Sélectionner › Supprimer.
  > Supprimer dans WhatsApp n'efface pas la copie déjà enregistrée dans Photos : vérifiez aussi vos photos.
  > Parties 1 et 2 : Supprimés récemment, Doublons.

### Voix off — provisoire, ne pas enregistrer encore

> WhatsApp peut prendre plusieurs gigas sur votre iPhone, sans que vous le voyiez.
> Ouvrez WhatsApp, touchez Vous en bas à droite, puis Stockage et données, puis Gérer le stockage.
> Commencez par Plus de 5 Mo : ce sont les grosses vidéos qu'on vous a envoyées.
> Touchez Sélectionner, choisissez ce que vous ne voulez plus, puis supprimez.
> Et regardez la liste en dessous : les groupes sont souvent les plus lourds.
> Fin de la série. Enregistrez-la : un jour, votre iPhone sera encore plein.

Libellés à confirmer par la vidéo d'écran (Vous ou Réglages, Plus de 5 Mo, Supprimer) avant l'enregistrement.
Vidéo d'écran demandée : accueil › WhatsApp › onglet bas droite › Stockage et données › Gérer le stockage › Plus de 5 Mo › Sélectionner › 1–2 fichiers › corbeille › Annuler ; puis une discussion de la liste.
