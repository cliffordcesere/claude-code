# ORA — mémoire de marque (§17)

Mise à jour : 2026-11-04 · Charte de référence : v3.1 (2026-10-24)

## Slogans figés vivants (5 max)

| Slogan | Statut | Depuis |
|---|---|---|
| « La tech, en clair. » | Signature de marque | v3.1 |
| « Nou pa pale anpil. Nou livre. » | Franchise | v3.0 |

Retiré : « La tech que tu mérites » (v3.1). Ne pas réutiliser.
Tout nouveau slogan proposé est étiqueté **candidat**, jamais présenté comme historique.

## Objectif en cours

Premiers **1 000 abonnés qui font confiance à ORA** (communauté fidèle, pas du volume brut).
La charte évolue avec la pratique : chaque ajustement est proposé, puis versionné par le propriétaire (§21).

## Décision : la voix d'ORA (propriétaire, 2026-11-06)

**Toutes les voix off sont la voix du propriétaire. Jamais de voix IA.** Raison : compte sans visage (faceless) ; la voix est le seul élément humain qui construit la confiance. Si la voix n'est pas disponible, on attend plutôt que de publier avec une voix IA.
ElevenLabs abandonné (`tools/voix_elevenlabs.py` conservé mais non utilisé).

## Idées en attente de décision (2026-11-07)

- Ouverture « poubelle » — **VALIDÉE (2026-11-07)** : des photos tombent dans la corbeille d'iOS, puis « 29 jours · avant la suppression définitive » (sans personnage). Faite dans « iPhone plein » 1/3 v03.
- **Projet mascotte ORA** — validé sur le principe par le propriétaire (2026-11-07), à concevoir dans une séance dédiée (pas improvisé dans un tuto). Contraintes : charte premium et calme, palette ORA, déclinable en série.
- Logos des apps tierces (WhatsApp, TikTok, Facebook, YouTube) — **FAIT (2026-11-07)**, demandé par le propriétaire : redessinés en monochrome dans `tools/icones_ios.py` (usage descriptif ; jamais à côté du logo ORA, §5).

## Façon de travailler (demandée par le propriétaire, 2026-11-06)

- **Précision (2026-11-07) :** un « pourquoi ne pas… ? » qui corrige un défaut visible (ex. « pourquoi ne pas utiliser leurs logos ? ») est une **demande** : l'exécuter. Ne s'arrêter pour discuter que sur les vraies questions de stratégie ou de marque.
- **Une question n'est pas un feu vert.** Quand le propriétaire pose une question de stratégie (« et si… ? », « on essaie… ? »), répondre avec un avis argumenté (pour, contre, recommandation), puis attendre sa validation avant d'agir.
- **Pas de jargon technique.** Le propriétaire ne code pas : expliquer simplement (pas de « clé API », « environnement », « proxy » sans les traduire en mots courants), et privilégier la solution qui ne lui demande aucune manipulation technique.
- Incident du 2026-11-06 : création d'un environnement « ORA (claude-code) » et demande d'une clé ElevenLabs sans accord explicite. Le propriétaire a saisi « xi-api-key » (le nom du champ, rien de sensible) ; aucun risque, rien à faire.

## Retours du propriétaire

- 2026-11-08 : **règle du propriétaire : toutes les voix off sont accélérées (~8 %, pauses resserrées), sans changer le ton** (`tools/resserrer_voix.py`, tempo 1.08). S'applique à chaque nouvelle vidéo, sans redemander.
- 2026-11-07 : consigne de voix off : ne plus écrire « Ne pas lire » (compris comme « ne pas dire »). Écrire : **tout se dit, avec vos mots** ; seuls les mots-clés de l'écran, la 1re et la dernière phrase restent exacts.
- 2026-11-07 : **toute légende, tout texte de voix off proposé va aussitôt dans le brief de la semaine** (`brief.md` + page « ORA • Semaine 1 »), même à l'état de proposition : c'est là que le propriétaire copie.
- 2026-11-04 : **toujours montrer le produit vendu.** Les visuels texte seul (« Index » sans produit) sont du bruit à ce stade.
- 2026-11-04 : le motion doit aller plus loin que des fondus de texte.
- 2026-11-04 : vidéo produit animée (v1) = « un bon début » ; risque perçu : « un bout de câble » → toujours rendre la taille ou la longueur lisible.
- 2026-11-05 : tuto iPhone publié avec « va dans Réglages » (tutoiement) par choix du propriétaire ; à l'avenir : « Allez dans Réglages ».
- 2026-11-05 : **le public des tutos est débutant** : montrer chaque geste (écran d'accueil, appui sur l'icône de l'app), ne rien supposer connu.
- 2026-11-05 : volume de sortie : -14 LUFS, crête -1 dBFS (le propriétaire trouvait sa voix trop basse ; Adobe Podcast utilisé pour le débruitage).
- 2026-11-04 : le son est souhaité. Habillage synthétisé par défaut (`tools/son.py`), version muette livrée à côté.
- 2026-11-04 : version courante : iOS 27 (sortie avec l'iPhone 18, selon le propriétaire). Captures de référence : Réglages FR (bloc compte Apple en haut, recherche flottante), Informations iOS 27 (référence affichée directement, ex. MG1D4LL/A).
- 2026-11-04 : le propriétaire n'a pas d'iPhone ; les tutos d'interface se font en écrans reconstruits (HTML), exactitude à faire vérifier sur un vrai appareil.
- 2026-11-04 : la photo maison est préférée à l'image fournisseur ; la plaque perforée et le désordre sont retirés au détourage.

## Lexique local (donné par le propriétaire, 2026-11-05)

| Mot | Sens | Usage ORA |
|---|---|---|
| **blende** | protection d'écran « blindée » (comme une voiture blindée). Chez ORA : **nano liquide d'abord, puis film hydrogel** | mot-clé des contenus protection d'écran ; titre créole « Nou Blende Ekran Tout Telefòn » déjà utilisé. Specs du nano liquide à confirmer avant toute affirmation |
| **zaza** | iPhone en mauvais état mais fonctionnel : batterie ~72–78 %, Face ID HS, pas full unlock, pièces non d'origine | mot-clé de la série tutos « repérer un zaza » ; ORA dit l'état, toujours |

Légende créole écrite par le propriétaire (en réserve, le français est préféré pour l'instant) :
« Avan w achte yon iPhone okazyon ayiti, men 3 fason ou ka rekonèt si se yon zaza. »

## Interface iOS 27.1 (captures FR, iPhone 17 Pro Max, 2026-11-06)

- Écran d'accueil : icônes sombres, « Caméra » (pas « Appareil photo »), widgets Météo + Photos, 4 rangées, Recherche, dock Téléphone/Safari/Messages/Musique.
- **Règle du propriétaire (2026-11-07) : le dessin des icônes doit être identique à iOS** ; la couleur peut rester dans la palette ORA. Icônes redessinées dans `tools/icones_ios.py` (FaceTime, Photos, Caméra, Mail, Notes, Rappels, Horloge, Podcasts, App Store, Plans, Santé, Cartes, Réglages, Téléphone, Safari, Messages, Musique). Logo Apple : **affiché** dans les tutos qui montrent un iPhone (usage descriptif, icône TV comprise). Interdit : pomme à côté du logo ORA, pomme comme décor de marque, « agréé / certifié Apple » si ce n'est pas vrai (§5).
- Photos : onglets **Photothèque / Collections** + loupe en bas. Collections : sections Voyages, Types de média, **Autres** (grille 2 colonnes : Favorites, Mes captures, **Suppr. récemment** 🔒, Documents, Doublons, Reçus), Suggestions de fond d'écran.
- Suppr. récemment : « Utilisez Face ID ou saisissez votre code pour afficher cet album. » / « Afficher l'album ». Dedans : « Sélect. », tri, « N élément(s) », vignettes « 9 jours ».
- Sélection : pastille « ··· ✕ », « 1 photo sélectionnée » en bas ; menu « ··· » → **Supprimer** / Récupérer ; confirmation en haut : « Cette photo sera définitivement supprimée d'iCloud et de tous vos appareils. » → « Supprimer de tous les appareils ».
- **Tout supprimer** (vidéo iOS 27.1, 2026-11-06) : Sélect. → rien coché, en bas « Sélectionner des éléments » → « ··· » → **Tout supprimer** / Tout récupérer → « Ces éléments seront définitivement supprimés d'iCloud et de tous vos appareils. » → « Supprimer de tous les appareils » → « 0 élément », « Aucune photo ou vidéo ». Face ID s'anime en haut, dans l'îlot.

## Voix off — prise du 2026-11-07 (« iPhone plein » 1/3)

27,5 s, rythme naturel, texte suivi (méthode « ne pas lire » efficace). Débruitée par le propriétaire (Adobe Podcast) ; ici : égalisation légère, niveau -14 LUFS au mixage, **vitesse non modifiée**. Écrans calés sur les mots-clés (Photos, Collections, Supprimées récemment, Face ID, Sélectionner, points, Tout supprimer). Vidéo v01 28,4 s ; retour : 10 premières secondes statiques, vidéo un peu longue. v02 : voix +8 % et pauses resserrées (24,6 s), début animé (jauge qui se remplit, ligne Photos, scène « Gardées 30 jours » sur l'album), 25,6 s. **Règle : jamais plus de ~3 s sur un écran fixe, surtout dans les 10 premières secondes ; par défaut, voix accélérée de ~8 % sans changer la hauteur.**

## Voix off (2026-11-06)

- Le texte de voix off s'écrit **pour être dit**, pas avec la cadence d'affiche : une situation vécue (« vous venez d'effacer 200 photos… »), le **pourquoi**, puis le geste. Le narrateur peut dire « je » (le propriétaire) ; vouvoiement maintenu.
- Méthode : ne pas lire. Fixes : 1re phrase (accroche en < 2 s), mots-clés des écrans, dernière phrase. Entre les deux, parler comme au comptoir. Les écrans sont calés sur les mots-clés après transcription.
- Durée : 25–30 s maximum.
- À arbitrer (§6) : questions rhétoriques interdites à l'écrit ; les autoriser à l'oral ? Non tranché.

## Règle éditoriale (propriétaire, 2026-11-06)

**« Le succès est dans le geste banal expliqué enfin clairement. »**
À éviter : comparatifs de flagships, astuces de développeur, raccourcis Android avancés (« ça fait plaisir à celui qui filme, ça n'intéresse personne »).
Un sujet = un geste, un gain immédiat, 15–20 s.

Constat du propriétaire : le stockage plein est un vrai problème, surtout sur iPhone (pas de nettoyage de cache comme sur Android).
Idées du propriétaire : batterie qui se vide (« 3 réglages à changer ») ; écran cassé mais téléphone vivant (angle sûr : sauvegarder avant).

## Série « iPhone plein » (proposée 2026-11-06)

1. Supprimées récemment (féminin, album verrouillé par code) — Photos › Autres › Supprimées récemment › Sélectionner › Tout supprimer. Vidéo faite le 2026-11-06 (17,6 s), voix off à enregistrer.
2. Doublons — Photos › Autres › Doublons › Fusionner (vu sur capture : « Doublons 633 »).
   **Vérifié sur vidéo d'écran iOS 27.1 (2026-11-07)** : Doublons (« N éléments ⓘ », groupes datés avec « Fusionner », vignettes bord à bord avec taille « 161 ko ») ; en haut ‹ · ≡ ··· · « Sélect. » ; Sélect. → « Tout sélectionner » / ✕, groupes « Sélectionner » ; tout coché → « Tout désélectionner » / « ··· ✕ », groupes « Désélectionner » ; en bas partage · « Fusionner (N) » · corbeille ; 1re bulle « Les doublons comprennent… » → « Fusionner N copies exactes uniquement… » / « Fusionner N éléments… » ; 2e bulle « La fusion permettra de conserver une version de chaque ensemble de doublons, qui associe la meilleure qualité d'image et les données pertinentes tout en déplaçant le reste vers l'album « Supprimés récemment ». » → « Fusionner N éléments » ; « Fusion des doublons… N éléments », compteur jusqu'à « 0 élément », « Aucune photo ou vidéo », « Fusionner les doublons · Terminé ».
   Nom officiel de l'album à l'écrit : **« Supprimés récemment »** (masculin, vu dans la bulle iOS 27.1) ; abrégé « Suppr. récemment » dans Collections.
   v02 sans voix (21,8 s) faite sur ces écrans. **Voix du propriétaire reçue le 2026-11-08** (25,5 s, déjà débruitée, -25,6 LUFS) : +8 %, pauses plafonnées → 22,7 s ; vidéo avec voix 25,3 s, -14,5 LUFS (rendu à -15,8 : +3 dB et limiteur ajoutés après coup). Phrase de fin non enregistrée (affichée à l'écran).
   Le 1er fichier reçu n'était pas le bon (version non traitée, plus réverbérée) ; refait le 2026-11-08 avec « Enregistrement_standard_79-optimis_-v2.wav » (Adobe Podcast) : voix 22,0 s, vidéo 24,7 s, -14,7 LUFS.
- **Voix « pièce vide » (2026-11-08)** : mesuré sur la prise Adobe : bosse de bas-médium vers 380–400 Hz (+11,5 dB / 1 kHz) et peu de présence → son de boîte. `tools/resserrer_voix.py` applique désormais : expandeur avant l'égalisation (queues raccourcies), -4 dB à 190 Hz, -6 dB à 380 Hz, -2,5 dB à 650 Hz, +3 dB à 2,2 kHz, +2 dB à 4 kHz, aigus +2,5 dB, dé-esseur. Rapport bas-médium/présence 21,9 → 12,8 dB ; chute après les mots 30 → 45 dB. Jugé à la mesure (pas d'écoute possible) : le retour du propriétaire fait foi.
- Conseil de prise (si la pièce sonne encore) : parler près du téléphone (15 cm), dans un placard ou face à des rideaux, des vêtements ou un lit ; éviter les pièces vides et carrelées.
3. WhatsApp › Gérer le stockage.

## Série « En clair » — vie pratique du téléphone en Haïti (proposée 2026-11-06)

Critère du propriétaire : utile, apprend vraiment quelque chose, suscite partage, enregistrement, abonnement.
Hypothèse (non vérifiée) : public majoritairement Android → privilégier WhatsApp et les usages communs plutôt que les réglages iPhone.
1. WhatsApp mange votre forfait — téléchargement automatique des médias → « Aucun média » sur données mobiles. 20 s, « Partie 1/3 ».
2. WhatsApp remplit votre téléphone — Gérer le stockage.
3. Tenir pendant le délestage — 4 réglages de batterie (lien avec l'offre énergie).
Fabrication : captures d'écran réelles du téléphone du propriétaire, animées (contacts floutés).

## Série « Avant d'acheter » (proposée 2026-11-06)

1. Zaza : batterie, référence, IMEI — publié le 2026-11-05.
2. ~~Compte Apple / iCloud~~ — écarté par le propriétaire (2026-11-06) : en Haïti, les iPhone se vendent rarement avec un compte Apple dessus.
3. Full unlock : verrouillage opérateur dans Informations.

## Série « Zaza » (proposée 2026-11-05)

1. Batterie, référence, IMEI — fait (`tuto-iphone-occasion.html`).
2. Full unlock — Réglages › Général › Informations, verrouillage opérateur. Captures iOS 27 FR à recevoir.
3. Pièces d'origine et Face ID — historique des pièces et réparations. Captures iOS 27 FR à recevoir.

Vidéo existante « Nou Blende Ekran Tout Telefòn » (06-06) : 260 vues, 12 j'aime, 1 enregistrement. Légende « Invisible. Impénétrable. Sur mesure. » : « blende » absent de la légende ; « Impénétrable » = promesse excessive (§1), proposer « Invisible. Résistant. Sur mesure. » Le propriétaire dit l'avoir corrigé par un post sur le canal et TikTok ; la légende de la vidéo reste à modifier si TikTok le permet.
Post canal « La vérité sur l'hydrogel » (25 mai 2026) : bon fond (l'hydrogel ne remplace pas le verre trempé) ; forme pré-v3.1 (tutoiement, capitales, 3 emojis). Sujet à refaire en vidéo « En clair » avec le nano liquide.

## Mesures

Reel câble USB-C 90° v2 (TikTok, publié le 2026-11-04 12:29, relevé le 2026-11-05) : 379 vues, 16 j'aime, 0 commentaire, 0 partage, **0 enregistrement**, 2 nouveaux abonnés.
Visionnage moyen 6,2 s sur 15,5 s (40 %) ; vidéo complète 8,86 % ; **décrochage principal à 0:02**. Trafic : Pour toi 97,4 %. Spectateurs : 98 % non-abonnés ; hommes 54 %, femmes 45 % ; 18–24 ans 48 %, 25–34 ans 36 % ; Haïti 75,2 %, **Jamaïque 17,9 %**, États-Unis 3,9 %.
Leçon appliquée : ouverture sans fondu au noir, 1re image complète.
À suivre : part anglophone (Jamaïque) qui ne lit pas le français.

Compte TikTok, 28 jours (7 oct. – 3 nov., relevé le 2026-11-05) : 1,5 K vues de publication (+80,5 %), 25 vues du profil, 15 j'aime, 8 commentaires, 2 partages ; 1,1 K spectateurs (dont 1,1 K nouveaux) ; 124 abonnés au total, +2 nets. Spectateurs : 49 % hommes, 49 % femmes.
**Sources de trafic : Recherche 48,4 %, Pour toi 48,2 %**, profil 3,4 %. Recherches qui mènent à ORA : « blende pou Haïti », « bleindè dos iphone », « Téléphone blender », « iphone xr zaza prix en haïti », « Wondel iphone ».
Déduction : en Haïti, le film de protection se cherche sous le mot **« blende »** ; les légendes doivent reprendre les mots tapés (blende, zaza, iPhone, Haïti).
Activité : spectateurs actifs de ~7 h à ~19 h (pic samedi 8–9 h) ; abonnés : pic le 3 nov. à 17 h (une seule journée, faible). Heures supposées locales (creux la nuit).
Règle de publication provisoire : en journée (11 h–17 h, 16 h conseillé), jamais le soir ; programmer dans TikTok Studio.

Tuto « iPhone d'occasion / zaza » (TikTok, publié le 2026-11-05 15:30, relevé le 2026-11-06) : 388 vues, 8 j'aime, 0 commentaire, 1 partage, **4 enregistrements**, **3 nouveaux abonnés**. Visionnage moyen 6,5 s sur 36,9 s (18 %), vidéo complète 2,83 %, décrochage principal à 0:02 malgré l'accroche. Trafic : Pour toi 98,4 %, Recherche 0 % (vidéo récente). 97 % non-abonnés ; 18–34 ans 87 % ; Haïti 75,7 %, Jamaïque 20 %.
Leçons : le format éducatif produit des enregistrements (0 pour le reel produit) ; 37 s est trop long (viser 20–25 s) ; l'accroche visuelle seule ne suffit pas, la première phrase doit frapper.
Objectif 1000 : 124 abonnés au 2026-11-05 ; à 2–3 abonnés par vidéo, ~290 vidéos ; à 10, ~88. Leviers : accroche (0:02), durée, régularité.

## Produits en stock (2026-11-04)

| Produit | Données confirmées | À confirmer |
|---|---|---|
| Câble USB-C ↔ USB-C, un embout coudé 90° | 100 W, 1 m, photos maison (2026-11-04) | — |
| Chargeur sans fil à support | — | 15 W, Verizon d'origine, prix (ancien visuel : 2 000 HTG) |
| Films hydrogel (pose sur machine Rich) | — | Modèles couverts, prix de pose, durée |

## Comptes et coordonnées (constatés le 2026-11-04)

| Canal | Compte | Base au 2026-11-04 |
|---|---|---|
| TikTok | @ora_haiti (nom affiché « ORA 📲📡 ») | 63 abonnés (+60 récents), 404 j'aime, 7 abonnements |
| Instagram | @ora.haiti (ex-@oratechofficial, renommé le 2026-11-04) | 211 abonnés, 11 publications, 13 vues sur 30 jours ; compte quasi inactif pendant ~1 an |
| Chaîne WhatsApp | ORA | 93 abonnés |
| Facebook | « Oratech » — retiré du profil Instagram, renommage à faire | — |
| Site | ora-haiti.vercel.app (officiel selon le propriétaire) | La bio Instagram pointe encore vers oratechhaiti.vercel.app |

Identifiants : « ora » et « oraofficial » sont pris sur les autres plateformes, d'où « oratech » et « haiti ».
Bio Instagram (2026-11-04) : « Téléphones, accessoires, énergie solaire, réparation. / Neuf ou occasion : toujours dit clairement. / La tech, en clair. »
WhatsApp : +509 4630 2424 · Adresse : Carr Gerald Bataille, Delmas, Ouest.
Hashtags déjà utilisés (non validés comme set officiel) : #ORA #Hydrogel #PortauPrince.

## Historique de contenu (constaté le 2026-11-04)

Vues TikTok : WITV « Toutes vos chaînes. Un seul écran. » 5 937 · ventilateur Joker « Chaleur + délestage » 1 108 ·
« 100 % n'est pas toujours 100 % » 410 · onduleur solaire EEKOO 377 · concept site restaurant 368 · tablette DIALN S10 340.
Échantillon trop petit pour conclure ; tendance à vérifier : les problèmes locaux concrets (chaleur, délestage, TV) dépassent le contenu d'image de marque.

Contenus antérieurs hors charte v3.1 : ancien logo et « La tech que tu mérites » sur plusieurs visuels et sur l'avatar de la chaîne WhatsApp ;
bio Instagram au tutoiement avec « astuces IA » (hors offre) ; bio TikTok chargée d'emojis ; posts « services web » (offre retirée en v3.1) ;
question rhétorique sur le visuel Joker ; police serif sur le visuel « 100 % ».

## Franchises récurrentes (§9)

1. « Détail » — macro d'un élément, une phrase.
2. « Nou pa pale anpil » — preuve brute : livraison, pose, test. Créole.
3. « Deux minutes » — geste technique filmé, sans voix, sans musique forte.
4. « Index » — un chiffre, fond noir, une ligne.

## Décisions de charte tranchées

Voir §21 de la charte. Ne pas dupliquer ici.

## Informations manquantes — à fournir par le propriétaire

Tant qu'elles manquent, placeholder obligatoire, jamais d'invention.

| Information | Placeholder | Utilisée pour |
|---|---|---|
| Set de hashtags officiel | `[HASHTAGS]` | Captions Instagram (3 max) |
| Politique de garantie écrite | `[GARANTIE]` | Posts, DM, escalade (§12) |
| Prix, stock, délais | `[PRIX]` `[DISPO]` `[DÉLAI]` | Tout contenu produit |
| Comptes réseaux, numéro WhatsApp, adresse | `[CONTACT]` | CTA, stories, flyers |
| Moyens de paiement acceptés | `[PAIEMENT]` | Flyers, site |
| Campagnes passées | — | Cohérence, séries |
| Photos produit détourées (fond transparent ou noir mat) | `[PHOTO PRODUIT]` | Tous visuels produit |

## Points de la charte à arbitrer (relevés le 2026-11-03)

0. **Écran de fin des vidéos (2026-11-04).** Le propriétaire veut combler le vide de fin. *Provisoire :* signature centrée (titre, logo vertical ~25 % de largeur, WhatsApp en cuivre). Écart au §5 (logo centré réservé au pilier MARQUE, taille 5–8 %).
4. **Voix off — TRANCHÉ le 2026-11-06 : voix du propriétaire, toujours (voir « Décision : la voix d'ORA »).** Historique : Enregistrement humain reçu le 2026-11-05 (gardé hors dépôt) ; le propriétaire préfère ElevenLabs à Flora (jugé « un peu robotique »). Le propriétaire veut une voix off sur les tutos. La charte ne l'interdit que pour la franchise « Deux minutes ». *Provisoire :* voix du propriétaire, calme ; test à mesurer (enregistrements, partages) contre les vidéos sans voix.

Ce sont des tensions entre règles, pas des décisions. Application provisoire indiquée ; seul le propriétaire tranche (§21).

1. **Taille du logo vs taille minimale.** Logo à 5–8 % de la largeur (§5) = 54–86 px sur un visuel de 1080 px. Or l'assemblage horizontal exige 80 px minimum (fiche p. 6). Seule la plage 7,5–8 % est conforme.
   *Provisoire :* horizontal à 8 % (86 px) sur les formats 1080 ; en dessous, symbole seul.
2. **Logo en bas à droite vs zone sûre 9:16.** §10 demande d'éviter les 320 px du bas (interface Reels/TikTok) ; §5 place le logo en bas à droite.
   *Provisoire :* logo en bas à droite, posé juste au-dessus des 320 px.
3. **Titre 6–9 % de la hauteur en 9:16.** Soit 115–173 px de corps sur ~950 px de largeur utile : environ 15 caractères par ligne au minimum de la plage. Avec la règle « 2 lignes max », un titre de 7 mots ne tient souvent pas.
   *Provisoire :* titre à 6 %, phrase courte ; la suite passe en sous-texte (3,5 %).
