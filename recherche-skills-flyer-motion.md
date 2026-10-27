# Skills Claude Code pour flyers + motion design « grand studio »

**Recherche vérifiée le 26 octobre 2026.** Étoiles, licences et dates de dernier commit relevées via l'API GitHub à cette date. Toutes les commandes d'installation sont celles documentées par les dépôts eux-mêmes.

---

## 1. La stack minimale qui donne un résultat de studio (5 commandes)

```bash
# 1. Le moteur vidéo : composition React → MP4 (skills officielles Remotion)
npx skills add remotion-dev/skills

# 2. Le timing : GSAP officiel (easing, timelines, stagger) — MIT
npx skills add greensock/gsap-skills

# 3. Le vocabulaire motion : durée, courbes, chorégraphie, archétype « Premium »
npx skills add LottieFiles/motion-design-skill --skill motion-design

# 4. Le flyer statique print : PNG/PDF via philosophie de design (Anthropic)
npx skills add anthropics/skills --skill canvas-design --agent claude-code

# 5. Le garde-fou anti-« AI slop » : refuse le rendu générique, audite en navigateur
npx skills add nutlope/hallmark -g
```

Avec ces cinq-là, tu couvres : **direction artistique → flyer print → déclinaison animée → contrôle qualité**. Le reste de ce document sert à affiner (After Effects, beat-sync, Lottie, logo animé) ou à remplacer une brique.

> Convention : `npx skills add <repo>` installe dans `.claude/skills/` du projet courant ; `-g` installe pour tous les projets. Un skill coûte ~100 tokens tant qu'il n'est pas déclenché : en empiler douze ne pénalise pas le contexte.

---

## 2. Couche A — Direction artistique et flyer statique (le visuel qui tient tout seul)

| Skill | Dépôt | ⭐ | Licence | Rôle |
|---|---|---|---|---|
| **canvas-design** | `anthropics/skills` | 184 k (repo) | Apache-2.0 | Le socle « poster » officiel d'Anthropic. Deux passes : d'abord une philosophie de design (mouvement esthétique nommé, 4–6 paragraphes), puis exécution en PDF/PNG. Texte rare, typo traitée comme partie de l'image. C'est ce qui sort un **flyer imprimable**, pas une capture d'écran. |
| **hallmark** | `Nutlope/hallmark` | 36,3 k | MIT | Le meilleur garde-fou disponible. 48 thèmes « matière » (papier, encre, surfaces), et surtout `sloplint` qui rend la page à 8 largeurs et fait relire le résultat par un agent en contexte neuf. Il refuse explicitement l'eyebrow au-dessus de chaque titre, le mot coloré dans le titre, les cadres vides. |
| **poster-generator** | `howardz27/poster-generator-skill` | 26 | non déclarée | 20 styles visuels, 6 ratios (1:1 → 16:9), analyse de contenu automatique, et une **traçabilité complète** `source.md → analysis.md → structured-content.md → prompts/poster.md → poster.png`. Excellent pour itérer proprement. ⚠️ Exige une capacité de génération d'image dans l'agent. |
| **brand-guidelines** | `anthropics/skills` | 184 k | Apache-2.0 | À ne pas utiliser tel quel (c'est la charte d'Anthropic). À **dupliquer et réécrire** avec tes couleurs/fontes : c'est le modèle de référence pour ton propre skill de marque. |
| **design (ui-ux-pro-max)** | `nextlevelbuilder/ui-ux-pro-max-skill` | 140,9 k | MIT | Le plus gros pack design du registre. Contient un module bannière avec les règles print dures : **300 DPI, CMYK, 3–5 mm de fond perdu**, zone de sécurité 70–80 %, max 2 fontes, texte < 20 %. |
| **huashu-design** | `alchaincyf/huashu-design` | 26,7 k | MIT | 84 styles avec planches d'exemple, six candidats puis trois directions. Interface en chinois, sorties exploitables. Utile comme **banque de références stylistiques**. |
| **html-anything** | `nexu-io/html-anything` | 9,3 k | Apache-2.0 | 75 templates dont `magazine-poster` (broadsheet, titre serif surdimensionné, 6 sections numérotées) et `frame-glitch-title`. Export PNG/HTML. Local, sans clé API. |
| **ai-poster-maker** | `beatra-ai/ai-poster-maker-skill` | 6 | — | Générateurs d'images (Qwen Image 3.0 Pro, GPT Image 2.5, Wan 2.7) jusqu'à 16,8 MP. ⚠️ **Nécessite un compte Beatra payant en crédits** : le skill est gratuit, le rendu non. |

**Alternative payante mais légitime :** `op7418/guizang-yingzao-skill` (519 ⭐) pour transformer une photo en affiche art-dirigée — très bon sur l'architecture et le voyage.

---

## 3. Couche B — Motion design (le flyer qui bouge, ou la vidéo 6–10 s)

| Skill | Dépôt | ⭐ | Licence | Rôle |
|---|---|---|---|---|
| **Remotion Agent Skills** | `remotion-dev/skills` | 5,7 k | voir licence Remotion | La référence. 8 skills : `/remotion-create`, `/remotion-markup` (layout, typo, easing, audio, fonts), `/remotion-studio`, `/remotion-render` (vidéo **et** still), `/remotion-captions`, `/remotion-maps`, `/remotion-saas`, `/remotion-best-practices`. Sortie MP4 déterministe, code versionnable. |
| **HyperFrames** | `heygen-com/hyperframes` | 73 k | **Apache-2.0** | L'alternative sans React : l'agent écrit du HTML/CSS/GSAP/Lottie, le CLI rend un MP4 déterministe. 7 skills, dont `/hyperframes`, `/figma`, `/remotion-to-hyperframes`. `npx hyperframes skills update` installe le set « core ». **Gratuit pour tous**, pas de licence par siège. |
| **GSAP Skills** | `greensock/gsap-skills` | 17,2 k | MIT | Officiel GreenSock. Timelines, labels, nesting, ScrollTrigger (pin, scrub, snap), SplitText, Flip, MorphSVG, DrawSVG. Depuis le rachat par Webflow, **tous les plugins sont gratuits** — c'est un changement majeur pour le motion premium. |
| **motion-design-skills (iart)** | `iart-ai/motion-design-skills` | 164 | MIT | **La couche « direction artistique motion »** la plus complète : `animation-principles` (12 principes, timing), `color-motion` (OKLCH/Lab, gestion couleur de rendu), `shot-composition` (grilles, safe areas, cadrage multi-ratios), `motion-art-direction` (langage de mouvement, rythme, retenue), `after-effects`, `beat-sync-editing`, `remotion-video`, `logo-animation`, `motion-background` (mesh gradients, shaders, particules). |
| **motion-design (LottieFiles)** | `LottieFiles/motion-design-skill` | 2,5 k | MIT | Le vocabulaire : tables de durées, familles de courbes, chorégraphie primaire/secondaire/ambiante, et des **archétypes de personnalité** dont « **Premium** ». C'est là que se joue la différence entre « ça bouge » et « ça coûte cher ». |
| **motion-design-studio** (plugin) | `frankxai/awesome-motion-design-agent-skills` | 82 | CC0-1.0 | Bundle prêt : GSAP, Motion, Remotion, Lottie, Rive + `web-motion-auditor`. Installation plugin : `/plugin marketplace add frankxai/awesome-motion-design-agent-skills` puis `/plugin install motion-design-studio@frankx-motion`. |
| **motion-graphics (Bart)** | `Barty-Bart/motion-graphics` | 875 | à vérifier | Skills « un job chacune » : `explainer-high-energy` (12–20 s beat-locked, kinetic type), `motion-broll`, `sound-effects` (SFX mesurés au beat), `object-separation`. Le meilleur pour un **teaser vertical** de flyer. |
| **Pixel2Motion** | `nolangz/pixel2motion` | 2,5 k | à vérifier | Logo bitmap → animation SVG (H/Lottie). Indispensable si le flyer doit inclure un logo animé. |
| **OpenMontage** | `calesthio/OpenMontage` | 72,2 k | à vérifier | Pipeline de production complet (footage, voix off, graphismes). Surengineering pour un flyer — utile si tu passes à un vrai film de marque. |

---

## 4. Couche C — Trouver, comparer, vérifier

| Ressource | Lien | Pourquoi |
|---|---|---|
| **awesome-claude-skills** | `ComposioHQ/awesome-claude-skills` (78 k ⭐) | La liste généraliste de référence, avec les SKILL.md lisibles en ligne. |
| **awesome-claude-video-skills** | `zhuyansen/awesome-claude-video-skills` (1 k ⭐) | 353 dépôts vidéo/motion, **chacun lu et noté** (agentskillshub.top, rafraîchi toutes les 8 h). Le filtre le plus utile pour ce sujet. |
| **skills CLI** | `vercel-labs/skills` (36,7 k ⭐, MIT) | L'outil `npx skills` utilisé partout ci-dessus. |
| **awesome-motion-design-agent-skills** | `frankxai/...` (82 ⭐, CC0) | Comparatif ciblé GSAP / Motion / Remotion / Lottie / Rive + QA motion. |

**Règles de prudence avant d'installer** (valables pour tous les skills communautaires) :
1. **Lis le `SKILL.md`** avant de l'activer. Un skill est du prompt exécuté : instructions cachées, appels réseau, scripts `scripts/*.mjs` — tout est à auditer.
2. **Méfie-toi des dépôts à moins de ~50 ⭐ sans licence claire.** Il y a beaucoup de « 6 331 lignes de secrets » auto-proclamés.
3. **Vérifie la licence du moteur, pas seulement du skill** (voir § 6).
4. Installe en local projet (`.claude/skills/`) plutôt qu'en global tant que tu testes.

---

## 5. Le pipeline « grand studio » appliqué à un flyer

> **Déjà en place dans ce dépôt :** le skill décrit ci-dessous existe maintenant sous forme de plugin complet dans `plugins/studio-brief/` — `SKILL.md`, 5 fichiers de référence (palettes, print, motion, tells, brief) et un script de contrôle `preflight.mjs`. Installation : `/plugin marketplace add ./` puis `/plugin install studio-brief@claude-code-plugins`.

### Étape 0 — Ton kit de marque (30 minutes, une fois)
Le plugin en contient une version de référence ; si tu veux l'écrire à la main, le minimum est ceci :

```markdown
---
name: studio-brief
description: Direction artistique maison. À utiliser avant tout flyer, affiche, post ou vidéo pour appliquer la charte et le niveau d'exigence du studio.
---
# Studio Brief
## Matière (choisir une seule)
papier non couché / encre offset + vernis / métal brossé / verre dépoli / encre fluorescente sur noir
## Palette (max 3 + neutre)
#0B0B0C (encre), #F4F1EA (papier), #C8452F (accent)
## Typographie (max 2, licences vérifiées)
Titre : … (graisse, interlettrage -2%)
Courant : …
## Interdits
dégradé saturé plein cadre, 3e fonte, emoji, ombre portée douce, stock photo souriante, badge "NEW"
## Preuves à produire
3 déclinaisons maximum, une seule idée forte, grille et marges visibles
```
Nommer ta matière et tes interdits est ce qui produit un rendu « studio » plutôt que « template ».

### Étape 1 — Direction artistique (avant tout code)
Demande **trois pistes nommées** en une ligne chacune, pas trois rendus. `canvas-design` impose déjà cette étape philosophie → exécution : laisse-la faire, mais refuse tout ce qui ressemble à « dégradé violet + Inter ».

### Étape 2 — Flyer statique, prêt imprimeur
- Format : A3 297 × 420 mm (ou 1080 × 1350 px pour le social).
- **300 DPI au format final, CMJN, 3 mm de fond perdu, 5 mm de zone de sécurité.** Ces quatre chiffres sont non négociables, et c'est exactement ce que vérifie le module bannière de `ui-ux-pro-max`.
- Export PDF pour l'imprimeur + PNG pour la validation client.
- ⚠️ La plupart des chaînes HTML→PDF sortent en **RVB**. Prévois une conversion CMJN (Ghostscript / ImageMagick) et un soft-proof des couleurs critiques : un bleu RVB vif ne s'imprime pas.

### Étape 3 — Déclinaison motion
- Durée : **6 à 10 s** pour un flyer animé ; 15–20 s pour un teaser.
- Formats : 9:16 (Reels/TikTok), 1:1 (feed), 16:9 (écran/lobby). Le même layout, pas trois créations.
- Réutilise **exactement** la grille et la typo du flyer : c'est ce qui crée la cohérence « campagne ».
- Grammaire : une entrée, une sortie. `stagger` 60–90 ms, easing custom type `cubic-bezier(0.16, 1, 0.3, 1)`, grain 2–4 % pour tuer l'aspect « numérique propre », aucun bounce générique.
- Si tu es à l'aise en React → Remotion. Sinon → HyperFrames (HTML), qui est aussi gratuit sans limite de sièges.

### Étape 4 — Boucle qualité (ce qui distingue vraiment les skills récents)
`render → extraire des stills → inspecter → corriger → re-render`. Les skills Remotion comme `claude-remotion-skill` (652 ⭐, MIT) imposent cette boucle au lieu de livrer à l'aveugle. Pour le web, `hallmark` fait la même chose avec `sloplint --render` sur 8 largeurs.

### Étape 5 — Livraison
PDF print CMJN + PNG 2× + MP4 9:16 + MP4 1:1 + GIF de prévisualisation + la **poster frame** (image 0) qui sert de vignette.

---

## 6. Pièges à connaître avant de promettre du « premium »

| Piège | Réalité |
|---|---|
| **Licence Remotion** | Gratuit pour les particuliers et les structures **≤ 3 personnes**. Au-delà : licence entreprise (~25 $/siège/mois, ou 0,01 $/rendu avec minimum mensuel). HyperFrames (Apache-2.0) n'a pas cette contrainte. |
| **Skills de génération d'image** | Ils consomment des crédits et exigent un compte tiers (Beatra, Gemini, etc.). Aucun skill ne rend une image « gratuitement » sans moteur derrière. |
| **Fontes** | Le PDF embarque la fonte : une fonte commerciale sans licence d'embedding est un risque juridique. Reste sur des fontes libres (Inter, Instrument Serif, Fraunces, Space Grotesk…) ou achète l'embedding. |
| **CMJN** | Un rendu écran validé en RVB peut virer au terne à l'impression. Toujours demander un BAT. |
| **« Premium » = retenue** | Les rendus qui font cheap sont surchargés : 4 fontes, 6 accents, 3 effets. Un flyer de studio, c'est une idée, deux fontes, une texture. |
| **Skills auto-proclamés** | Beaucoup de dépôts promettent « 6 000 lignes de motion Awwwards ». Vérifie les ⭐, la licence, la date du dernier commit. |

---

## 7. Prompt de départ à coller dans Claude Code

```text
Utilise canvas-design et mon skill studio-brief.

Brief : flyer A3 pour [événement], [date], [lieu], [une phrase de promesse].
Direction : matière [papier non couché / encre + vernis], palette imposée, 2 fontes max.
Contraintes : 300 DPI, CMJN, 3 mm de fond perdu, 5 mm de sécurité, aucune fonte commerciale.
Livre : (1) trois directions nommées en une ligne, (2) le PDF print + PNG 2x,
(3) une déclinaison 9:16 de 8 s rendue en MP4 sous Remotion (ou HyperFrames), 
grain 2–4 %, easing custom, stagger 80 ms.
Avant de livrer : re-render, extrais 6 stills, inspecte-les, corrige, re-render.
```

---

*Sources : API GitHub (étoiles/licences/commits au 26/10/2026), README officiels des dépôts cités, documentation Remotion, HyperFrames, GreenSock, Anthropic Skills.*
