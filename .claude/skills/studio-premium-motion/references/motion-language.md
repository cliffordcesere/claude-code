# Langage de mouvement — référence

## Sommaire
1. Principe
2. Courbes d'accélération
3. Durées et rythme
4. Chorégraphie
5. Techniques qui font « studio »
6. À éviter
7. Boucles et fin de séquence

---

## 1. Principe

Le mouvement premium se reconnaît à trois choses : des accélérations franches qui
se posent longuement (on sent le poids), une seule chose qui bouge à la fois, et des
temps de repos. Le mouvement révèle la hiérarchie : ce qui arrive en premier est ce
qui compte le plus.

## 2. Courbes d'accélération

Les noms ci-dessous existent dans le moteur de `assets/template.html`.

| Nom | cubic-bezier | Usage |
|---|---|---|
| `expoOut` | (0.16, 1, 0.3, 1) | Entrée par défaut : départ rapide, longue décélération. La signature « luxe ». |
| `quartOut` | (0.25, 1, 0.5, 1) | Entrée plus sage, éléments secondaires. |
| `quintInOut` | (0.83, 0, 0.17, 1) | Transitions de bloc, rideaux, changements de scène. |
| `expoIn` | (0.7, 0, 0.84, 0) | Sorties : l'élément accélère et quitte le cadre. |
| `sineInOut` | (0.37, 0, 0.63, 1) | Mouvements continus lents (dérive, respiration, parallaxe). |
| `linear` | — | Uniquement pour des défilements continus ou le grain. |

Évite les courbes CSS par défaut `ease` / `ease-in-out` : ce sont celles de toutes les interfaces, et elles se reconnaissent.

## 3. Durées et rythme

À 30 i/s, sur un flyer de 6 à 12 secondes :

| Élément | Durée |
|---|---|
| Révélation d'un titre (par ligne) | 0,9 – 1,4 s, décalage 0,08 – 0,15 s entre lignes |
| Révélation par lettres | 0,6 – 1,0 s par lettre, décalage 0,02 – 0,04 s |
| Infos secondaires | 0,5 – 0,8 s |
| Transition de scène | 0,8 – 1,2 s |
| Dérive lente d'une image (scale 1,00 → 1,06) | toute la durée |
| **Temps de lecture final** | ≥ 2,5 s, ou ~0,3 s par mot affiché + 1 s |

Le temps de lecture final est souvent oublié : si l'œil n'a pas le temps de lire la date et le lieu, le flyer a échoué, quelle que soit sa beauté.

Structure type (8 s) : 0 s fond, matière et signature de marque déjà en place (voir § 7) → 0,35–2,5 s entrée du héros →
2,5–4,5 s entrée des infos secondaires, une par une → 4,5–8 s tenue, avec seulement une dérive lente et le grain.

## 4. Chorégraphie

- **Une chose à la fois.** Le spectateur suit un seul mouvement. Superpose au plus deux mouvements, dont un très lent.
- **Direction cohérente.** Tout entre dans le même sens (de bas en haut, par exemple), sauf intention.
- **Chevauchement.** L'élément suivant démarre quand le précédent est à ~70 % de son mouvement, pas après sa fin : c'est ce qui donne de la fluidité.
- **Ordre = hiérarchie.** Héros → information principale → détails → logo.
- **Amplitude faible.** Les déplacements premium sont courts (20–80 px sur un format 1080) ou masqués. Un élément qui traverse tout l'écran fait « PowerPoint ».

## 5. Techniques qui font « studio »

- **Révélation par masque** : chaque ligne glisse de 100 % vers 0 % à l'intérieur d'un conteneur `overflow: hidden`. C'est la base, le template la fournit (`.mask > .line`).
- **Clip-path** : un rideau ou une fente qui ouvre une image (`clip` en pourcentage dans le template).
- **Flou → net** sur une entrée (blur 12 px → 0) combiné à une légère translation.
- **Échelle extrême** : un chiffre ou un mot à une taille qui déborde le cadre, qui dérive lentement.
- **Kinetic type** : les mots changent de graisse, de largeur ou d'approche dans le temps (fontes variables).
- **Flou de mouvement** : `--motion-blur 4` au rendu. Très efficace sur les révélations rapides ; inutile si tout est lent.
- **Parallaxe douce** entre deux plans (texte et image) à des vitesses différentes.

## 6. À éviter

- Rebonds, élastiques, overshoot — sauf marque explicitement ludique.
- Tout qui apparaît en fondu simultanément.
- Rotations gratuites, zooms brusques, tremblements, effets « glitch » par défaut.
- Machine à écrire avec curseur clignotant.
- Transitions de logiciel de diaporama (cube, page qui tourne, volet).
- Vitesse uniforme : le même timing pour tous les éléments rend le mouvement mécanique.

## 7. Boucles et fin de séquence

- **La première image doit être composée** (fond, matière, au moins un élément graphique). Les plateformes et les messageries utilisent souvent la première image comme aperçu : un écran vide ou noir donne une miniature morte.
- Pour une boucle parfaite, la dernière image doit rejoindre la première : soit sortie symétrique puis retour à l'état initial, soit état final stable et coupe franche sur une tenue.
- Sur les réseaux, privilégier « entrée → tenue longue » plutôt qu'une boucle complexe : la plupart des gens ne verront qu'un passage.
- Le son est rarement entendu (lecture muette par défaut) : le flyer doit fonctionner sans.
