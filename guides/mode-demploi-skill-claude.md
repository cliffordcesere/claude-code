# Installer un « skill » sur Claude — mode d'emploi simple

## D'abord : c'est quoi un skill ?

Un skill (on dit aussi « compétence ») est un **petit dossier de texte** qu'on donne à Claude
pour lui apprendre un sujet précis. Ça ne s'installe pas comme un logiciel : c'est juste un
fichier de consignes que Claude lit quand le sujet arrive dans la conversation.

Analogie : c'est une **fiche de recettes** que tu glisses dans la cuisine de Claude.
Tant que personne ne demande la recette, elle reste dans le tiroir.

Un skill = un dossier, avec un fichier `SKILL.md` dedans (et parfois des fichiers annexes).

---

## Le fichier que j'ai préparé pour toi

`free-llm-apis.zip`

Dedans : le skill **free-llm-apis**, tiré d'un dépôt GitHub très populaire
(11 800 étoiles) qui recense les services d'IA **gratuits et sans carte bancaire**
(Google Gemini, Groq, Mistral, OpenRouter…), avec pour chacun : où récupérer la clé,
comment la brancher, et un exemple qui marche.

Traduction : après installation, tu pourras demander à Claude *« aide-moi à obtenir une clé
gratuite chez Groq »* et il saura exactement quoi te faire faire.

---

## Installation — choisis TON cas

### Cas A — Tu utilises Claude sur le site claude.ai (le plus simple)

1. Va sur **claude.ai** et connecte-toi.
2. Clique sur ton **avatar** (en bas à gauche) → **Settings** (Paramètres).
3. Onglet **Capabilities** (ou **Skills** selon la version).
4. Active l'**exécution de code** si on te le demande.
5. Clique sur **Upload skill** / **Add skill** et choisis le fichier `free-llm-apis.zip`.
6. C'est fini. Ouvre une nouvelle conversation et écris :
   *« Je veux une clé API gratuite pour utiliser une IA dans mes scripts. »*

> **Bonne nouvelle : c'est possible avec le compte gratuit.** Depuis février 2026, les skills
> (y compris l'envoi de ton propre ZIP) font partie du plan Free. Il faut juste activer
> l'exécution de code, sinon la rubrique Skills est grisée.

### Cas A bis — Tu n'as que l'application sur téléphone

**D'abord, les mots français / anglais** (tous les guides en ligne sont en anglais) :

| Sur ton écran (FR) | Dans les guides (EN) |
|---|---|
| Capacités | Capabilities |
| Artéfacts | Artifacts |
| Compétences | Skills |
| Importer une compétence | Upload a skill |
| Personnaliser | Customize |

L'application mobile sert surtout à *utiliser* les skills déjà présents. Pour **envoyer**
un ZIP, le plus fiable est la version navigateur :

1. Ouvre **claude.ai** dans le navigateur de ton téléphone (Safari / Chrome), connecte-toi.
2. Menu (les trois barres) → **Paramètres** → onglet **Capacités**.
3. Active l'interrupteur **« Artéfacts »**. C'est l'étape que tout le monde rate : sans lui,
   la rubrique « Compétences » n'apparaît pas (le texte le dit : *requis pour l'exécution de
   code et la création de fichiers*).
4. Ferme et rouvre les paramètres, reviens dans **Capacités**, fais défiler vers le bas
   jusqu'à **« Compétences »** → bouton **+** → **Importer une compétence**.
5. Choisis `free-llm-apis.zip`. Puis vérifie que son interrupteur est bien activé.

Si l'envoi du fichier ne passe pas depuis le téléphone, fais-le depuis un ordinateur
(même un ordinateur d'ami ou de cybercafé) : le skill reste attaché **à ton compte**, donc
tu le retrouveras ensuite dans l'application mobile.

> À savoir : un skill n'est **pas obligatoire**. C'est un confort — il évite de réexpliquer
> le contexte à chaque fois. Sans lui, tu peux simplement coller le texte de la fiche dans
> la conversation.

### Cas B — Tu utilises Claude dans une fenêtre noire (Claude Code)

Là, un dossier remplace le ZIP. Deux endroits possibles :

- **Pour tous tes projets** → dossier `skills` caché dans ton dossier personnel
- **Pour un seul projet** → un dossier `.claude/skills/` dans ce projet

Le plus simple, colle ces deux lignes l'une après l'autre dans la fenêtre noire :

```bash
mkdir -p ~/.claude/skills && unzip ~/Téléchargements/free-llm-apis.zip -d ~/.claude/skills/
```

(remplace `~/Téléchargements` par l'endroit où le fichier a été téléchargé — souvent
`~/Downloads` sur Mac)

Puis **ferme et rouvre** Claude Code. Tape `/skills` pour vérifier qu'il apparaît.

---

## Comment savoir que ça a marché

Pose la question à Claude, en langage normal :

> « Quels skills as-tu ? »

Il doit citer `free-llm-apis`. Ensuite, au lieu de taper une commande bizarre, tu écris
simplement : *« je veux une IA gratuite pour mon projet »* — et il se sert du skill tout seul.

---

## Le seul vrai danger

Un skill, ce sont des **instructions** : il peut demander à Claude de faire des choses.
Donc **n'installe jamais un skill trouvé au hasard** sans l'avoir fait lire par quelqu'un
de confiance (ou par moi). Celui-ci, je l'ai ouvert et lu : ce sont des notes et des exemples,
il ne fait rien tourner tout seul.

Règle simple : avant d'installer, demande-toi *« qui a écrit ça, et est-ce que quelqu'un l'a vérifié ? »*

---

## Et sur les autres plateformes (Arena, ChatGPT, Gemini…) ?

Le format `SKILL.md` est une convention **propre à Claude**. Ailleurs, il n'y a pas
d'« installation » : un skill n'est qu'un fichier texte, donc on peut toujours s'en servir,
mais autrement.

| Plateforme | Ce que tu peux faire |
|---|---|
| **Arena** | Rien à installer : joins le fichier `SKILL.md` à ta conversation et je l'utilise. Il n'est pas mémorisé d'une conversation à l'autre. |
| **Claude** (app / site) | Envoi du ZIP dans Customize > Skills, comme décrit plus haut. |
| **ChatGPT / Gemini** | Pas de skills au même sens : on met les consignes dans un « projet » ou des « instructions personnalisées ». |
| **Autres outils pour développeurs** | Beaucoup acceptent le même dossier de consignes (Cursor, Codex…), avec des noms différents. |

Conclusion : le ZIP est fait pour Claude. Ailleurs, le texte reste réutilisable — c'est
juste une question de copier-coller.

---

## À quoi sert VRAIMENT une clé API gratuite

Point important, souvent mal compris : une clé API n'est pas une application. C'est une
**clé d'accès** que l'on donne à un logiciel pour qu'il puisse parler à une IA.

- Si tu veux **discuter avec une IA** → tu n'as besoin d'aucune clé : l'application Claude
  gratuite (ou Gemini, ou ChatGPT) suffit.
- Si tu veux **qu'un logiciel utilise une IA** (un site, une application, un automatisme) →
  là, il faut une clé.
- Cas intermédiaire, sans coder : certains logiciels de discussion acceptent une clé et une
  adresse (« base URL »), et affichent ensuite une interface de chat classique. On y colle
  une clé gratuite, et on utilise des modèles gratuits.

Donc avant de créer un compte quelque part, la bonne question est : **quel est le projet
exact ?** La réponse détermine s'il faut une clé, et laquelle.

