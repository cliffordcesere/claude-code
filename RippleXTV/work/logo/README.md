# X-Beam — exploration du monogramme

Statut : **exploration close**. Direction retenue : A-signature ; fichiers maîtres dans `../../assets/logos/`. Ce dossier garde l'historique des pistes ; aucun de ses fichiers n'est un actif officiel.

- `xbeam.py` : construction géométrique exacte. Chaque piste est une fonction paramétrée ; `python3 xbeam.py` régénère `out/`.
- `out/` : SVG par piste et par variante (`cobalt`, `blanc`, `noir`, `bicolore`, `construction`, `avatar`, `avatar-bicolore`).
- `planche.html` → `planche.png` : planche de comparaison, rendue à l'échelle 1 (`node render.cjs planche.html planche.png 1660 1`, Playwright requis).

Polices de la planche : `../../assets/fonts/` (SIL OFL 1.1, licences dans `licenses/`).
