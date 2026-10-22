"""Monogramme X-Beam — construction de référence.

Ce fichier est la définition du monogramme. Les SVG et PNG du dossier en sont
dérivés ; en cas de doute, c'est ce fichier qui fait foi.

Règles de construction (U = 1/100 de la hauteur du monogramme) :

  1. Deux faisceaux droits de largeur constante FAISCEAU, symétriques par
     rapport à la verticale. Leurs axes ont une pente de 3:2 (3 en hauteur pour
     2 en largeur), soit atan(3/2) ≈ 56,31° sur l'horizontale.
  2. Les extrémités sont coupées à l'horizontale : ligne de base et ligne de
     tête, distantes de HAUTEUR.
  3. Le croisement des axes est placé LEVEE au-dessus du centre de la hauteur
     (centre optique) : les bras du bas, plus longs, s'écartent davantage.
  4. L'onde est une couronne de vide concentrique au croisement, de largeur
     ONDE. Son bord intérieur passe exactement par les deux sommets rentrants
     haut et bas du croisement (rayon = demi-faisceau / cos de l'angle).
  5. L'impact est la partie des faisceaux située à l'intérieur de l'onde.

Zone de protection : deux largeurs de faisceau (26U) sur chaque côté, soit
plus que les 25 % de la largeur demandés par la charte (§5.4).

Usage : python3 monogramme.py   (régénère les SVG du dossier)
"""

import math
import os

U = 8.0                      # unité de dessin (en unités SVG) ; U = HAUTEUR / 100
HAUTEUR = 100 * U
PENTE = (3, 2)               # hauteur:largeur des axes
LEVEE = 2 * U
VERSIONS = {
    # nom : (largeur du faisceau, largeur de l'onde)
    "standard": (13 * U, 2 * U),
    "petite-taille": (15 * U, 4 * U),   # sous 64 px de hauteur affichée
}
PROTECTION = 2 * 13 * U

ABYSS = "#08090C"
TITANIUM = "#F0F2F5"
COBALT = "#0052FF"

PHI = math.atan2(PENTE[0], PENTE[1])
COS, SIN = math.cos(PHI), math.sin(PHI)


# --- géométrie (origine au croisement des axes, y vers le bas) ---------------

def _add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def _mul(p, k):
    return (p[0] * k, p[1] * k)


def _cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def _meet(o1, d1, o2, d2):
    t = _cross((o2[0] - o1[0], o2[1] - o1[1]), d2) / _cross(d1, d2)
    return _add(o1, _mul(d1, t))


class _Bras:
    """Demi-faisceau de demi-largeur h, d'axe u ; n est u tourné de +90°."""

    def __init__(self, sx, sy, h):
        self.u = (sx * COS, sy * SIN)
        self.n = (-self.u[1], self.u[0])
        self.h = h
        self.vers_le_bas = sy > 0

    def bord(self, s):
        """Droite du bord s (+1 ou -1) : point d'origine et direction."""
        return _mul(self.n, s * self.h), self.u

    def sur_cercle(self, s, r):
        return _add(_mul(self.n, s * self.h), _mul(self.u, math.sqrt(r * r - self.h * self.h)))

    def sur_coupe(self, s, y):
        o, d = self.bord(s)
        return _add(o, _mul(d, (y - o[1]) / d[1]))


def _bras(h):
    # triés par angle croissant dans le repère SVG
    return [_Bras(1, 1, h), _Bras(-1, 1, h), _Bras(-1, -1, h), _Bras(1, -1, h)]


def _f(x):
    s = f"{x:.2f}"
    return "0.00" if s == "-0.00" else s


class _Trace:
    def __init__(self, dy):
        self.parts = []
        self.last = None
        self.dy = dy  # translation verticale vers le repère final

    def pt(self, p):
        return f"{_f(p[0])} {_f(p[1] + self.dy)}"

    def move(self, p):
        self.parts.append(f"M {self.pt(p)}")
        self.last = p

    def line(self, p):
        if math.dist(p, self.last) > 1e-6:
            self.parts.append(f"L {self.pt(p)}")
            self.last = p

    def arc(self, p, r):
        if math.dist(p, self.last) > 1e-6:
            sweep = 1 if _cross(self.last, p) > 0 else 0
            self.parts.append(f"A {r:.2f} {r:.2f} 0 0 {sweep} {self.pt(p)}")
            self.last = p

    def close(self):
        self.parts.append("Z")


def chemin(version="standard"):
    """Contour du monogramme (un seul chemin, remplissage nonzero).

    Repère final : x = 0 sur l'axe vertical de symétrie, y = 0 sur la ligne de tête.
    """
    faisceau, onde = VERSIONS[version]
    h = faisceau / 2
    haut = -(HAUTEUR / 2 - LEVEE)          # ligne de tête, mesurée depuis le croisement
    bas = HAUTEUR / 2 + LEVEE              # ligne de base
    r1 = h / COS                           # règle 4
    r2 = r1 + onde
    bras = _bras(h)
    t = _Trace(dy=-haut)

    # impact : disque r1 ∩ faisceaux
    for i, b in enumerate(bras):
        suivant = bras[(i + 1) % 4]
        a, c = b.sur_cercle(-1, r1), b.sur_cercle(1, r1)
        if i == 0:
            t.move(a)
        t.arc(c, r1)
        v = _meet(*b.bord(1), *suivant.bord(-1))
        if math.hypot(*v) <= r1 + 1e-6:
            t.line(v)
            t.line(suivant.sur_cercle(-1, r1))
        else:
            t.arc(suivant.sur_cercle(-1, r1), r1)
    t.close()

    # bras : au-delà de l'onde, jusqu'aux coupes horizontales
    for b in bras:
        y = bas if b.vers_le_bas else haut
        a_in, c_in = b.sur_cercle(-1, r2), b.sur_cercle(1, r2)
        t.move(a_in)
        t.line(b.sur_coupe(-1, y))
        t.line(b.sur_coupe(1, y))
        t.line(c_in)
        t.arc(a_in, r2)
        t.close()
    return " ".join(t.parts)


def dimensions(version="standard"):
    """Largeur hors tout (en bas, là où les jambes s'écartent le plus) et hauteur."""
    faisceau, _ = VERSIONS[version]
    demi = (HAUTEUR / 2 + LEVEE) * PENTE[1] / PENTE[0] + (faisceau / 2) / SIN
    return 2 * demi, HAUTEUR


# --- fichiers ----------------------------------------------------------------

def svg_monogramme(version, couleur, marge=0.0):
    w, hgt = dimensions(version)
    x0, y0 = -w / 2 - marge, -marge
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_f(x0)} {_f(y0)} '
            f'{_f(w + 2 * marge)} {_f(hgt + 2 * marge)}" role="img">'
            f"<title>RippleXTV</title>"
            f'<path fill="{couleur}" d="{chemin(version)}"/></svg>\n')


def svg_avatar(couleur, fond, version="standard", occupation=0.54):
    """Avatar carré (1080 unités) : le monogramme occupe `occupation` de la
    hauteur ; il reste dans le recadrage rond des plateformes."""
    w, hgt = dimensions(version)
    s = occupation * 1080 / hgt
    tx, ty = 540, 540 - hgt * s / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" role="img">'
            f"<title>RippleXTV</title>"
            f'<rect width="1080" height="1080" fill="{fond}"/>'
            f'<path transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})" fill="{couleur}" '
            f'd="{chemin(version)}"/></svg>\n')


def svg_plan():
    """Plan de construction coté (1800 x 1400)."""
    w, hgt = dimensions()
    h = VERSIONS["standard"][0] / 2
    r1 = h / COS
    r2 = r1 + VERSIONS["standard"][1]
    yc = HAUTEUR / 2 - LEVEE                     # croisement, depuis la ligne de tête
    P = PROTECTION
    cy, sl, tx = "#00D2FF", "#8B949E", TITANIUM
    L = []
    a = L.append

    def line(x1, y1, x2, y2, c=sl, dash=None, wdt=1.5):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{c}" stroke-width="{wdt}"{d}/>')

    def text(x, y, s, c=tx, size=14, anchor="start", rot=None):
        r = f' transform="rotate({rot} {_f(x)} {_f(y)})"' if rot else ""
        a(f'<text x="{_f(x)}" y="{_f(y)}" fill="{c}" font-size="{size}" text-anchor="{anchor}"{r}>{s}</text>')

    def cote_v(x, y1, y2, label, c=cy):
        line(x, y1, x, y2, c)
        line(x - 8, y1, x + 8, y1, c)
        line(x - 8, y2, x + 8, y2, c)
        text(x - 12, (y1 + y2) / 2, label, c, anchor="middle", rot=-90)

    a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 1400">')
    a('<style>@font-face{font-family:"Space Mono";src:url("../fonts/space-mono-latin-400-normal.woff")}'
      'text{font-family:"Space Mono",monospace;letter-spacing:.04em}</style>')
    a(f'<rect width="1800" height="1400" fill="{ABYSS}"/>')
    a('<g transform="translate(620 300)">')
    # zone de protection
    a(f'<rect x="{_f(-w / 2 - P)}" y="{_f(-P)}" width="{_f(w + 2 * P)}" height="{_f(hgt + 2 * P)}" '
      f'fill="none" stroke="{sl}" stroke-width="1.5" stroke-dasharray="3 6"/>')
    text(-w / 2 - P + 12, hgt + P - 16, "ZONE DE PROTECTION", sl)
    cote_v(-w / 2 - 60, -P, 0, "26U", sl)
    # monogramme
    a(f'<path fill="#262C36" d="{chemin()}"/>')
    # lignes horizontales
    for y, lab in ((0, "LIGNE DE TÊTE"), (hgt, "LIGNE DE BASE")):
        line(-w / 2 - 130, y, w / 2 + 40, y, sl, "2 5")
        text(w / 2 + 50, y + 5, lab, sl)
    line(-w / 2 - 130, hgt / 2, w / 2 + 40, hgt / 2, sl, "2 5")
    text(w / 2 + 50, hgt / 2 + 20, "CENTRE 50U", sl)
    line(-w / 2 - 130, yc, w / 2 + 40, yc, cy, "8 5")
    text(w / 2 + 50, yc - 8, "CROISEMENT 48U", cy)
    # axes des faisceaux
    k = PENTE[1] / PENTE[0]
    for s in (1, -1):
        line(-s * (yc + 60) * k, -60, s * (hgt - yc + 60) * k, hgt + 60, cy, "10 5", 1)
    # pente 3:2
    x0 = (600 - yc) * k
    line(x0, 600, x0 + 80, 600, cy)
    line(x0 + 80, 600, x0 + 80, 720, cy)
    text(x0 + 40, 590, "2", cy, anchor="middle")
    text(x0 + 92, 666, "3", cy)
    # onde
    for r in (r1, r2):
        a(f'<circle cx="0" cy="{_f(yc)}" r="{_f(r)}" fill="none" stroke="{cy}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for y in (yc - r1, yc + r1):
        a(f'<circle cx="0" cy="{_f(y)}" r="5" fill="{cy}"/>')
    ang = math.radians(195)
    px, py = r2 * math.cos(ang), yc + r2 * math.sin(ang)
    line(px, py, -215, py - 20, cy, wdt=1)
    text(-222, py - 30, "ONDE 2U", cy, anchor="end")
    text(-222, py - 10, f"r1 = {r1 / U:.2f}U".replace(".", ","), cy, anchor="end")
    # largeur du faisceau (perpendiculaire au bras haut droit)
    y0 = 150
    ax = (yc - y0) * k
    nx, ny = SIN, COS
    line(ax - h * nx, y0 - h * ny, ax + h * nx, y0 + h * ny, cy, wdt=2)
    text(ax + h * nx + 14, y0 + h * ny + 18, "FAISCEAU 13U", cy)
    # hauteur et largeur hors tout
    cote_v(-w / 2 - 140, 0, hgt, "100U")
    line(-w / 2, hgt + 20, -w / 2, hgt + 100, sl, wdt=1)
    line(w / 2, hgt + 20, w / 2, hgt + 100, sl, wdt=1)
    line(-w / 2, hgt + 80, w / 2, hgt + 80, cy)
    text(0, hgt + 70, f"{w / U:.2f}U".replace(".", ","), cy, anchor="middle")
    a("</g>")
    # cartouche
    X = 1270
    text(X, 120, "RIPPLEXTV", tx, 15)
    text(X, 158, "MONOGRAMME X-BEAM", tx, 26)
    text(X, 186, "PLAN DE CONSTRUCTION · v01", sl)
    text(X, 230, "U = 1/100 DE LA HAUTEUR", cy)
    regles = [
        ("1", "FAISCEAUX DROITS, LARGEUR 13U"),
        ("2", "AXES EN PENTE 3:2 (56,31°)"),
        ("3", "COUPES HORIZONTALES, HAUTEUR 100U"),
        ("4", "CROISEMENT 2U AU-DESSUS DU CENTRE"),
        ("5", "ONDE 2U ; SON BORD INTÉRIEUR PASSE"),
        ("", "PAR LES SOMMETS HAUT ET BAS"),
        ("", "DU CROISEMENT"),
        ("6", "LARGEUR HORS TOUT DÉDUITE : 84,96U"),
    ]
    for i, (n, s) in enumerate(regles):
        text(X, 290 + 26 * i, n, cy)
        text(X + 28, 290 + 26 * i, s)
    y = 540
    text(X, y, "VERSIONS", sl)
    text(X, y + 30, "STANDARD · 64 PX ET PLUS")
    text(X, y + 54, "FAISCEAU 13U · ONDE 2U", sl)
    text(X, y + 90, "PETITE TAILLE · MOINS DE 64 PX")
    text(X, y + 114, "FAISCEAU 15U · ONDE 4U", sl)
    y = 720
    text(X, y, "COULEURS", sl)
    a(f'<rect x="{X}" y="{y + 16}" width="26" height="26" fill="{ABYSS}" stroke="{sl}"/>')
    text(X + 40, y + 35, "NOIR ABYSS #08090C")
    a(f'<rect x="{X}" y="{y + 54}" width="26" height="26" fill="{TITANIUM}"/>')
    text(X + 40, y + 73, "BLANC TITANIUM #F0F2F5")
    text(X, y + 120, "UNE SEULE COULEUR À LA FOIS.", sl)
    text(X, y + 144, "NI DÉGRADÉ, NI CONTOUR, NI EFFET.", sl)
    text(X, 1270, "STATUT : PROPOSÉ À VALIDATION", cy)
    text(X, 1296, "RECHERCHE D’ANTÉRIORITÉ À FAIRE", sl)
    a("</svg>")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = {
        "RXTV_monogramme_blanc_v01.svg": svg_monogramme("standard", TITANIUM),
        "RXTV_monogramme_noir_v01.svg": svg_monogramme("standard", ABYSS),
        "RXTV_monogramme-petite-taille_blanc_v01.svg": svg_monogramme("petite-taille", TITANIUM),
        "RXTV_monogramme-petite-taille_noir_v01.svg": svg_monogramme("petite-taille", ABYSS),
        "RXTV_avatar_blanc-sur-noir_v01.svg": svg_avatar(TITANIUM, ABYSS),
        "RXTV_avatar_noir-sur-cobalt_v01.svg": svg_avatar(ABYSS, COBALT),
        "RXTV_monogramme_plan-construction_v01.svg": svg_plan(),
    }
    for name, content in out.items():
        with open(os.path.join(here, name), "w") as f:
            f.write(content)
    w, hgt = dimensions()
    print(f"angle {math.degrees(PHI):.2f}°  largeur {w / U:.2f}U  hauteur {hgt / U:.0f}U  "
          f"onde r1 {VERSIONS['standard'][0] / 2 / COS / U:.3f}U")
