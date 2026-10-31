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
5. Appuie sur **« Create API Key »**, donne-lui un nom simple : `telephone`.
6. Une clé apparaît, elle ressemble à ça : `gsk_xxxxxxxxxxxxxxxxxxxx`

> ⚠️ **Copie-la immédiatement.** Groq ne la réaffichera plus jamais. Si tu la perds,
> tu en crées une autre — ce n'est pas grave, mais c'est une perte de temps.

**Cette clé est un mot de passe.** Ne la partage avec personne, ne la colle pas dans un
message, ne la montre pas sur une capture d'écran. Si elle fuite : retourne sur cette page
et appuie sur la corbeille pour la supprimer, puis crées-en une neuve.

---

## Étape 2 — Installer l'application

1. Ouvre le **Play Store**.
2. Cherche **« Chatbox »** — l'application de discussion IA (éditeur : Chatbox AI).
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
