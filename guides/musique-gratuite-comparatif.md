# Musique gratuite : le catalogue international, sans payer

> **Correction de la version précédente de ce guide.** Elle recommandait Audiomack en
> supposant un répertoire caribéen. C'était une déduction abusive. Ce guide-ci part du bon
> problème : **le catalogue mainstream (pop, rap, R&B, afro, latin, électro…), celui que
> les plateformes font payer.**

---

## 1. Pourquoi ton problème est structurel

Sur Audiomack, 90 % de tes titres sont payants pour une raison simple : ce ne sont pas des
artistes indépendants qui publient eux-mêmes, ce sont des **ayants droit sous licence**. Les
gros catalogues sont cédés à Spotify, Apple, Amazon, YouTube — et facturés.

Il n'existe donc que deux portes d'accès au catalogue mainstream complet :

1. **Payer** un abonnement (Spotify, Amazon Unlimited, Apple, Tidal, Deezer…).
2. **Passer par YouTube**, qui a déjà payé les licences pour toi.

Tout le reste — « Spotify gratuit », « Deezer gratuit » — est un teaser : aléatoire, pub,
pas de hors-connexion. C'est vrai de **toutes** les plateformes officielles, y compris
Amazon Music.

---

## 2. Ce que te donne vraiment Amazon Music

Tu l'utilises déjà, donc autant savoir où tu te situes :

| Formule | Prix | Choix des titres | Hors connexion | Pub |
|---|---|---|---|---|
| **Amazon Music Free** | 0 | Limité, sélections imposées | ❌ Non | ✅ Oui |
| **Prime Music** (avec Prime) | inclus | **Aléatoire** sur le catalogue | ❌ Sauf « All-Access Playlists » | Non |
| **Unlimited** | ~11 $/mois | ✅ Oui | ✅ Oui | Non |

Autrement dit : si tu es sur Free, tu as le même problème que Spotify gratuit. Si tu as
Prime, tu as 100 millions de titres… mais en lecture aléatoire. Le libre choix est réservé
à Unlimited.

---

## 3. La vraie solution gratuite : les clients YouTube Music libres

Ce sont des applications **open source** qui utilisent le catalogue public de YouTube Music
(le plus grand du monde) comme source. Résultat : catalogue mainstream complet, sans pub,
en arrière-plan, avec **téléchargement hors connexion** — pour 0 €.

**Vérifié à l'instant sur GitHub (1er novembre 2026)** — ces trois projets sont vivants,
licenciés, et publient leurs propres APK :

| Application | Étoiles | Licence | Dernière version | Taille APK | Atout |
|---|---|---|---|---|---|
| **Metrolist** | 13 900 | GPL-3.0 | v13.7.0 | 25 Mo | Le plus sobre, Android Auto, Cast |
| **SimpMusic** | 12 600 | GPL-3.0 | **v2.5.0 — aujourd'hui** | 27 Mo | Le plus complet : paroles traduites, Canvas Spotify, + versions Windows/Mac/Linux |
| **Spotube** | 50 500 | AGPL-3.0 | v6.0.0 — 30 oct. | ~30 Mo | Importe tes **playlists Spotify** et lit l'audio via YouTube |

**Lequel prendre ?** Metrolist si tu veux simple et stable. SimpMusic si tu veux la totale
(et l'équivalent sur PC). Spotube si tu as déjà des playlists Spotify à récupérer.

---

## 4. Installation (Android)

1. Ouvre **github.com** et cherche le dépôt : `MetrolistGroup/Metrolist` ou
   `maxrave-dev/SimpMusic` ou `KRTirtho/spotube`.
2. Onglet **Releases** (à droite), puis la dernière version.
3. Télécharge le fichier **`.apk`** :
   - Metrolist → `Metrolist.apk`
   - SimpMusic → `SimpMusic-foss-arm64-v8a-release.apk` (99 % des téléphones récents) ;
     en cas de doute, `SimpMusic-foss-universal-release.apk` (53 Mo, marche partout)
   - Spotube → `Spotube-android-all-arch.apk`
4. Android affiche « Installation d'applications inconnues » → autorise **ton navigateur**
   à installer, puis valide.
5. Ouvre l'appli, cherche un titre mainstream, lance-le. Puis **télécharge-le** (icône ⬇)
   et teste en mode avion.

---

## 5. ⚠️ Les faux sites — le vrai danger

En cherchant ces applis, on tombe sur des sites qui usurpent leur nom. Constaté pendant
cette recherche :

- **`simpmusic.us`** se présente comme le site officiel et affirme que l'appli « n'est pas
  open source » et s'installe « uniquement depuis le Play Store », avec un identifiant
  `com.simpmusic.offlinemusicplayerr`. **Le vrai SimpMusic est `com.maxrave.simpmusic`**,
  sur GitHub. Ce site n'est pas celui du développeur.
- Des miroirs d'APK (`appteka`, `moddoom`, `malavida`…) republient des versions modifiées.

**La règle, sans exception :** l'APK se télécharge **uniquement** depuis
`github.com/<auteur-officiel>/<projet>/releases`. Jamais un site d'APK, jamais un lien
envoyé par message.

---

## 6. Ce que je te dois en toute franchise

Ces clients ne sont **pas** des outils de piratage au sens strict : ils lisent un catalogue
public via une interface libre, comme NewPipe pour YouTube. Mais :

- ils utilisent YouTube d'une manière que **ses conditions d'utilisation n'autorisent pas** ;
- **ils peuvent cesser de fonctionner** après une mise à jour de YouTube — c'est déjà arrivé ;
- il n'y a **pas de mises à jour automatiques** : il faut revenir sur GitHub de temps en temps ;
- le risque pour ton compte Google est faible mais non nul.

Si un jour tu veux zéro friction et zéro risque : c'est l'abonnement. Les applis libres sont
le compromis gratuit.

---

## 7. Et les applis « interdites en Haïti » ?

Tu m'as dit que ça ne te dérangeait pas. Je te réponds franchement : **ça ne résout pas ton
problème.**

Les services géo-bloqués (Pandora, iHeartRadio, Deezer dans certains marchés, offres Amazon
localisées) sont soit **payants**, soit **verrouillés par carte bancaire locale**. Contourner
le blocage demande un VPN — ce qui viole leurs conditions — et ne débloque pas le paiement.

En revanche, les trois applis libres ci-dessus **fonctionnent en Haïti sans VPN**, sans
compte, sans carte. C'est précisément ce que tu cherchais, et c'est pour ça qu'elles sont
la bonne réponse — pas un détour par un service étranger.

---

## En résumé

1. **Metrolist** ou **SimpMusic** depuis GitHub → catalogue mainstream complet, gratuit,
   hors connexion.
2. **Spotube** si tu veux récupérer tes playlists Spotify.
3. **Audiomack** reste utile pour découvrir, pas pour retrouver tes titres.
4. **Amazon Music** : garde-le pour ce qu'il fait bien, mais sache que le libre choix est
   derrière Unlimited.
