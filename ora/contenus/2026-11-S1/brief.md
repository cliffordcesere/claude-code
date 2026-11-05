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
