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

> Si tu ne vois pas « Skills » dans les paramètres : c'est que ton compte n'a pas encore
> cette fonction. Dans ce cas, utilise le Cas B, ou demande-moi — on trouvera un plan B.

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
