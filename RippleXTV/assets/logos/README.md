# Monogramme X-Beam — fichiers maîtres v01

**Statut : proposé à validation.** La direction est choisie (piste A-signature). Les fichiers ci-dessous ne deviennent des actifs officiels qu'après validation du propriétaire et une recherche d'antériorité (charte §5.2).

## Fichiers

| Fichier | Usage |
| :--- | :--- |
| `RXTV_monogramme_blanc_v01.svg` / `.png` | Sur fond sombre et sur images (filigrane). PNG transparent, 2048 px de haut. |
| `RXTV_monogramme_noir_v01.svg` / `.png` | Sur fond clair (presse, documents). PNG transparent, 2048 px de haut. |
| `RXTV_monogramme-petite-taille_{blanc,noir}_v01.svg` | Sous 64 px de hauteur affichée : faisceau 15U, onde 4U. |
| `RXTV_avatar_blanc-sur-noir_v01.svg` / `.png` | Avatar principal, 1080 × 1080. |
| `RXTV_avatar_noir-sur-cobalt_v01.svg` / `.png` | Variante d'avatar, 1080 × 1080. |
| `RXTV_monogramme_plan-construction_v01.svg` / `.png` | Plan coté : la référence pour redessiner le monogramme. |

`monogramme.py` est la définition du monogramme ; tous les fichiers en sont dérivés. Pour les régénérer : `python3 monogramme.py`, puis `node exporter.cjs` (Playwright).

## Règles d'usage

- Une seule couleur à la fois : noir Abyss `#08090C` sur fond clair, blanc Titanium `#F0F2F5` sur fond sombre ou sur image. Le X n'est jamais en cobalt ni en cyan.
- Ni dégradé, ni contour, ni ombre, ni lueur, ni rotation, ni déformation.
- Zone de protection : 26U (deux largeurs de faisceau) de chaque côté, U étant le centième de la hauteur.
- Sous 64 px de hauteur : version petite taille. Sous environ 24 px, l'onde n'est plus perceptible et le monogramme devient un X à cœur plein ; c'est accepté.
- Ne pas retracer : utiliser les fichiers de ce dossier ou les régénérer depuis `monogramme.py`.
