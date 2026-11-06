# Discuter avec une IA gratuite, sans la limite des 5 heures

**Ce que tu vas obtenir :** une deuxième application de discussion sur ton téléphone, avec
son **propre quota** — environ **1 000 messages par jour**, séparé de la limite de Claude.

**Ce qu'il te faut :** 15 minutes, un e-mail, aucune carte bancaire, aucun abonnement.

**Sois lucide avant de commencer :** les modèles gratuits de Groq sont **moins bons** que
Claude. C'est un outil de dépannage, pas un remplaçant. Tu y gagnes en quantité, tu perds
en finesse. Les deux ensemble, c'est ça la solution.

---

## Étape 1 — Récupérer la clé Groq

1. Dans ton navigateur, va sur **console.groq.com**
2. **Sign up** (inscription) avec Google ou ton e-mail. Aucune carte n'est demandée.
3. Vérifie ton e-mail si on te le demande, puis reconnecte-toi.
4. Dans le menu de gauche, cherche **« API Keys »**.
5. Appuie sur **« Create API Key »**. Deux champs :
   - **Display Name** : un nom parlant, par exemple `chatbox-android` (50 caractères max).
     Évite ton nom ou ton e-mail : ce nom est visible dans la console.
   - **Expiration** : si le menu propose des durées (30 / 60 / 90 jours), prends-en une.
     « No expiration » est pratique mais, si la clé fuite, elle reste valable indéfiniment.
     Une clé qui expire se recrée en 20 secondes.
6. Une clé apparaît, elle ressemble à ça : `gsk_xxxxxxxxxxxxxxxxxxxx`

> ⚠️ **Groq ≠ Grok.** Une lettre d'écart, deux entreprises sans rapport :
>
> | | **Groq** (avec un q) | **Grok** (avec un k) |
> |---|---|---|
> | Qui | Plateforme d'inférence (matériel LPU) | Modèle d'IA de xAI |
> | Site | `groq.com` / `console.groq.com` | `grok.com` / `console.x.ai` |
> | Clé | commence par **`gsk_`** | commence par **`xai-`** |
> | Adresse | `https://api.groq.com/openai/v1` | `https://api.x.ai/v1` |
>
> Les deux sont « compatibles OpenAI », donc une erreur de clé ne donne pas un message clair :
> juste un `401`. Vérifie le préfixe avant de coller.

> ⚠️ **Copie-la immédiatement.** Groq ne la réaffichera plus jamais. Si tu la perds,
> tu en crées une autre — ce n'est pas grave, mais c'est une perte de temps.

**Cette clé est un mot de passe.** Ne la partage avec personne, ne la colle pas dans un
message, ne la montre pas sur une capture d'écran. Si elle fuite : retourne sur cette page
et appuie sur la corbeille pour la supprimer, puis crées-en une neuve.

---

## Étape 2 — Installer l'application

1. Ouvre le **Play Store**, ou va directement sur le lien officiel :
   `https://play.google.com/store/apps/details?id=xyz.chatboxapp.chatbox`
2. **Vérifie que tu es sur la bonne application** — il existe plusieurs clones :
   - identifiant dans l'URL : **`xyz.chatboxapp.chatbox`** (le seul critère fiable) ;
   - nom affiché : « Chatbox AI: Powerful AI Client » ;
   - éditeur : **Mediocre Company** (oui, c'est vraiment son nom) ;
   - 100 K+ téléchargements.
3. Installe-la et ouvre-la.
4. **Ignore les écrans qui proposent un abonnement.** Tu n'en as pas besoin : tu vas
   utiliser ta propre clé, gratuitement.

> Pas envie d'installer ? La même application existe dans le navigateur :
> **web.chatboxai.app**. Ça marche aussi, mais tes conversations restent dans ce
> navigateur-là.

---

## Étape 3 — Brancher la clé

Les libellés changent un peu selon la version, en français ou en anglais. Cherche les
équivalents :

| Français | Anglais |
|---|---|
| Paramètres | Settings |
| Fournisseur d'IA | AI Provider |
| Ajouter un fournisseur personnalisé | Add Custom Provider |
| Mode API : compatible OpenAI | API Mode: OpenAI API Compatible |

1. Ouvre les **Paramètres** (la roue dentée).
2. Va dans la section **Fournisseur d'IA** (*AI Provider*).
3. Appuie sur **Ajouter un fournisseur personnalisé** (*Add Custom Provider*).
4. Remplis ainsi :

| Champ | Valeur à écrire |
|---|---|
| Nom | `Groq` |
| Mode API | **OpenAI API Compatible** |
| Hôte / Host | `https://api.groq.com` |
| Chemin / Path | `/v1/chat/completions` |
| Clé API / API Key | ta clé `gsk_...` |

> **Si tu n'as qu'un seul champ « Base URL »** au lieu de Hôte + Chemin, mets :
> `https://api.groq.com/openai/v1`

5. Dans la section **Modèles**, ajoute ce nom, **exactement** comme ceci :

```
openai/gpt-oss-120b
```

C'est le meilleur modèle gratuit de Groq. Tu peux en ajouter un second, plus rapide :
`openai/gpt-oss-20b`

6. Enregistre.

---

## Étape 4 — Tester

1. Retourne à l'écran des conversations, crée une **nouvelle discussion**.
2. En haut, vérifie que le modèle sélectionné est bien **Groq** / `gpt-oss-120b`.
3. Écris : *« Bonjour, présente-toi en deux phrases. »*

Si tu as une réponse, **c'est gagné**.

---

## Si ça ne marche pas

| Message d'erreur | Ce que ça veut dire | Quoi faire |
|---|---|---|
| `401` / *Unauthorized* | La clé est refusée | Recopie la clé en entier, sans espace avant ou après |
| `404` / *model not found* | Le nom du modèle est faux | Vérifie : `openai/gpt-oss-120b`, avec la barre oblique |
| `429` / *rate limit* | Tu as dépassé le quota | Attends une minute (limite : 30 messages/minute) |
| Aucune connexion | L'adresse est mal écrite | Hôte : `https://api.groq.com` — pas de `/v1` à la fin si le chemin est séparé |

---

## Ce que tu as maintenant, en clair

- **Claude** : le plus fin, mais coupé tous les ~15-40 messages, 5 heures d'attente.
- **Chatbox + Groq** : moins fin, mais ~1 000 messages par jour.

**La méthode :** tu travailles sur Claude tant que ça passe. À la coupure, tu bascules sur
Chatbox et tu continues. Tu ne perds plus 5 heures.

Et un bénéfice inattendu : en cas de panne de Claude, tu as un plan B qui ne dépend pas
d'Anthropic.

---

## Étape 5 (bonus) — Ajouter Gemini, plus puissant que Groq

Groq est rapide, mais ses modèles sont des modèles ouverts (gpt-oss-120b). Pour de la
**qualité de raisonnement**, le meilleur gratuit aujourd'hui est **Gemini**, via une clé
Google AI Studio. Gratuit, sans carte bancaire.

**Pourquoi ça vaut le coup :** les modèles `gemini-3.8-flash` ont une fenêtre de **1 million
de tokens** et lisent texte, image, audio et vidéo. C'est plusieurs crans au-dessus de Groq
pour analyser un document ou une capture d'écran.

### Le plus simple : sans rien installer

**Google AI Studio** est un site. Tu y discutes avec `gemini-3.8-flash` directement, sans
application, sans clé, sans carte bancaire.

1. Ouvre **aistudio.google.com** dans ton navigateur.
2. Connecte-toi avec ton compte Google.
3. En haut, dans le sélecteur de modèle, choisis **Gemini 3.8 Flash**.
4. Écris dans le champ du bas. C'est tout.

Tu y gagnes en plus deux réglages invisibles dans l'application grand public :

- le **niveau de réflexion** (*thinking level*) : `low`, `medium` (défaut) ou `high` —
  mets `high` pour un problème difficile, `low` pour une réponse rapide ;
- le **compteur de tokens**, pour voir ce que tu consommes.

> ⚠️ **Piège à connaître :** l'application mobile **Gemini** (celle du Play Store) **n'inclut
> pas** 3.8 Flash sur son palier gratuit — depuis le 9 octobre 2026, elle route la plupart
> des questions vers Flash-Lite, sans choix du modèle. Si tu veux 3.8 gratuitement, c'est
> AI Studio ou l'API. Pas l'appli.

**Quand préférer Chatbox alors ?** Si tu veux **une seule application** sur ton téléphone,
qui garde l'historique et où tu peux brancher plusieurs fournisseurs (Gemini, Groq, autre
clé) et basculer de l'un à l'autre. Sinon, AI Studio suffit.

### Obtenir la clé

1. Va sur **aistudio.google.com/app/apikey**
2. Connecte-toi avec un compte Google.
3. **Create API key** → copie-la (elle ressemble à `AIza...`).

### L'ajouter dans Chatbox

Même écran que pour Groq : *Paramètres → Fournisseur d'IA → Ajouter un fournisseur*.

| Champ | Valeur |
|---|---|
| Nom | `Gemini` |
| Mode API | **OpenAI API Compatible** |
| Hôte / Host | `https://generativelanguage.googleapis.com` |
| Chemin / Path | `/v1beta/openai/chat/completions` |
| Clé API | ta clé `AIza...` |

> Un seul champ « Base URL » ? Mets :
> `https://generativelanguage.googleapis.com/v1beta/openai/`

Modèles à saisir, du plus récent au plus léger :

```
gemini-3.8-flash
gemini-3.6-flash
gemini-2.5-flash
```

### ⚠️ Vie privée — important

Sur le **palier gratuit** de l'API Gemini, Google peut utiliser tes échanges pour améliorer
ses produits (sauf si tu es dans l'EEE, en Suisse ou au Royaume-Uni). Donc : **pas de
données personnelles, pas de mots de passe, pas de documents confidentiels** dans cette
appli. Pour ça, garde Claude ou un modèle local.

### Ce que tu as maintenant

| Fournisseur | Force | Quota |
|---|---|---|
| Claude (app) | Le plus fin | ~15-40 messages / 5 h |
| **Gemini (Chatbox)** | **Raisonnement, 1 M de contexte, images** | Généreux, gratuit |
| Groq (Chatbox) | Vitesse | ~1 000 messages/jour |

Trois quotas séparés. Tu ne peux plus être bloqué.
