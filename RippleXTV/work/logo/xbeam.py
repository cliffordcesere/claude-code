"""Construction géométrique du monogramme X-Beam (pistes d'exploration).

Chaque forme est calculée analytiquement : droites, intersections et arcs de
cercle vrais. Aucun tracé à main levée, aucune génération d'image. Les cotes
sont exprimées dans un carré de 1000 unités centré en (500, 500).

Vocabulaire :
- faisceau : bande droite (largeur constante ou évasée) qui traverse le centre ;
- bras : la moitié d'un faisceau d'un côté du centre ;
- onde : couronne de vide concentrique qui coupe les faisceaux ;
- impact : la partie des faisceaux restée à l'intérieur de l'onde.

Usage : python3 xbeam.py  ->  écrit les SVG dans ./out/
"""

import math
import os
import re

SIZE = 1000
C = SIZE / 2
COBALT = "#0052FF"
CYAN = "#00D2FF"
WHITE = "#F0F2F5"
ABYSS = "#08090C"


# --- géométrie de base (repère SVG : x vers la droite, y vers le bas) -------

def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def mul(p, k):
    return (p[0] * k, p[1] * k)


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def perp(v):
    """Rotation de +90° dans le repère SVG (sens des angles croissants)."""
    return (-v[1], v[0])


def cross(p, q):
    return p[0] * q[1] - p[1] * q[0]


def polar(deg, r=1.0):
    t = math.radians(deg)
    return (r * math.cos(t), r * math.sin(t))


def intersect(o1, d1, o2, d2):
    """Intersection des droites o1 + t*d1 et o2 + s*d2."""
    den = cross(d1, d2)
    t = cross((o2[0] - o1[0], o2[1] - o1[1]), d2) / den
    return add(o1, mul(d1, t))


def ray_circle(o, d, r):
    """Point o + t*d (t > 0) situé sur le cercle de centre (0, 0) et de rayon r."""
    A = dot(d, d)
    B = 2 * dot(o, d)
    Cc = dot(o, o) - r * r
    t = (-B + math.sqrt(B * B - 4 * A * Cc)) / (2 * A)
    return add(o, mul(d, t))


def fmt(p):
    return f"{p[0] + C:.2f} {p[1] + C:.2f}"


def arc_to(p, q, r):
    """Petit arc de centre (0, 0) allant de p à q."""
    sweep = 1 if cross(p, q) > 0 else 0
    return f"A {r:.2f} {r:.2f} 0 0 {sweep} {fmt(q)}"


def circle_path(r, reverse=False):
    s = 0 if reverse else 1
    return (f"M {C + r:.2f} {C:.2f} A {r:.2f} {r:.2f} 0 1 {s} {C - r:.2f} {C:.2f} "
            f"A {r:.2f} {r:.2f} 0 1 {s} {C + r:.2f} {C:.2f} Z")


# --- faisceaux -------------------------------------------------------------

class Arm:
    """Moitié de faisceau partant du centre dans la direction `angle` (degrés).

    Demi-largeur : h(s) = h0 + k*s, à la distance s du centre le long de l'axe.
    Chaque bord est donc une droite : origine sigma*h0*n, direction u + sigma*k*n.
    """

    def __init__(self, angle, h0, k=0.0):
        self.angle = angle
        self.u = polar(angle)
        self.n = perp(self.u)
        self.h0 = h0
        self.k = k

    def edge(self, sigma):
        o = mul(self.n, sigma * self.h0)
        d = unit(add(self.u, mul(self.n, sigma * self.k)))
        return o, d

    def at_radius(self, sigma, r):
        o, d = self.edge(sigma)
        return ray_circle(o, d, r)

    def at_axis(self, sigma, s):
        """Point du bord dont la projection sur l'axe vaut s (coupe d'équerre)."""
        o, d = self.edge(sigma)
        t = (s - dot(o, self.u)) / dot(d, self.u)
        return add(o, mul(d, t))

    def at_y(self, sigma, y):
        """Point du bord d'ordonnée y (coupe horizontale, comme une lettre)."""
        o, d = self.edge(sigma)
        return add(o, mul(d, (y - o[1]) / d[1]))

    def at_x(self, sigma, x):
        """Point du bord d'abscisse x (coupe verticale)."""
        o, d = self.edge(sigma)
        return add(o, mul(d, (x - o[0]) / d[0]))


def arm_path(arm, r_in, end, R):
    """Bras compris entre le cercle r_in et l'extrémité `end`.

    end = "cercle"   : arc concentrique de rayon R ;
          "equerre"  : coupe perpendiculaire à l'axe, à la distance R ;
          "verticale": coupe verticale à |x| = R*cos(angle).
    """
    a_in, b_in = arm.at_radius(-1, r_in), arm.at_radius(1, r_in)
    if end == "cercle":
        a_out, b_out = arm.at_radius(-1, R), arm.at_radius(1, R)
        outer = f"L {fmt(a_out)} {arc_to(a_out, b_out, R)} "
    elif end == "equerre":
        a_out, b_out = arm.at_axis(-1, R), arm.at_axis(1, R)
        outer = f"L {fmt(a_out)} L {fmt(b_out)} "
    elif end == "verticale":
        x = R * math.cos(math.radians(arm.angle))
        a_out, b_out = arm.at_x(-1, x), arm.at_x(1, x)
        outer = f"L {fmt(a_out)} L {fmt(b_out)} "
    elif end == "horizontale":
        y = R * math.sin(math.radians(arm.angle))
        a_out, b_out = arm.at_y(-1, y), arm.at_y(1, y)
        outer = f"L {fmt(a_out)} L {fmt(b_out)} "
    else:
        raise ValueError(end)
    return f"M {fmt(a_in)} {outer}L {fmt(b_in)} {arc_to(b_in, a_in, r_in)} Z"


def segment_path(arm, r_in, r_out):
    """Tronçon de bras compris entre deux cercles concentriques."""
    a_in, b_in = arm.at_radius(-1, r_in), arm.at_radius(1, r_in)
    a_out, b_out = arm.at_radius(-1, r_out), arm.at_radius(1, r_out)
    return (f"M {fmt(a_in)} L {fmt(a_out)} {arc_to(a_out, b_out, r_out)} "
            f"L {fmt(b_in)} {arc_to(b_in, a_in, r_in)} Z")


def overlap_radius(arms):
    """Distance au centre du sommet rentrant le plus éloigné : en deçà, les
    bras se chevauchent et ne peuvent pas être découpés séparément."""
    arms = sorted(arms, key=lambda a: a.angle % 360)
    d = 0
    for i, arm in enumerate(arms):
        nxt = arms[(i + 1) % len(arms)]
        o1, d1 = arm.edge(1)
        o2, d2 = nxt.edge(-1)
        d = max(d, math.hypot(*intersect(o1, d1, o2, d2)))
    return d


def impact_path(arms, r):
    """Partie des faisceaux située dans le disque de rayon r.

    Le contour alterne : arc de rayon r à l'intérieur d'un bras, puis bord du
    bras jusqu'au sommet rentrant qu'il partage avec le bras suivant.
    """
    arms = sorted(arms, key=lambda a: a.angle % 360)
    parts = []
    for i, arm in enumerate(arms):
        nxt = arms[(i + 1) % len(arms)]
        a = arm.at_radius(-1, r)
        b = arm.at_radius(1, r)
        o1, d1 = arm.edge(1)
        o2, d2 = nxt.edge(-1)
        v = intersect(o1, d1, o2, d2)
        c = nxt.at_radius(-1, r)
        if i == 0:
            parts.append(f"M {fmt(a)}")
        parts.append(arc_to(a, b, r))
        if math.hypot(*v) < r:
            parts.append(f"L {fmt(v)} L {fmt(c)}")
        else:
            # le secteur entre les deux bras est entièrement couvert : on suit le cercle
            parts.append(arc_to(b, c, r))
    parts.append("Z")
    return " ".join(parts)


def mark(arms, cuts, spacing, end, R, offset=0.0):
    """Monogramme complet : impact, ondes (couronnes de vide) et bras.

    cuts    : largeurs des ondes, du centre vers l'extérieur ;
    spacing : longueur de faisceau conservée entre deux ondes ;
    offset  : décalage de la première onde au-delà du rayon de chevauchement.
              À 0, le bord intérieur de l'onde passe exactement par le sommet
              rentrant le plus éloigné : le contour de l'impact n'a pas de pointe.
    """
    r_impact = overlap_radius(arms) + offset
    waves, r = [], r_impact
    for w in cuts:
        waves.append((r, r + w))
        r += w + spacing
    pieces = []
    for (a1, b1), (a2, b2) in zip(waves, waves[1:]):
        for a in arms:
            pieces.append(segment_path(a, b1, a2))
    pieces += [arm_path(a, waves[-1][1], end, R) for a in arms]
    return {
        "impact": impact_path(arms, r_impact + 1e-6),
        "arms": pieces,
        "circles": [r for w in waves for r in w],
        "R": R,
        "arms_obj": arms,
        "end": end,
    }


# --- pistes ----------------------------------------------------------------

def X_arms(phi, h, k=0.0):
    """Quatre bras symétriques, à ±phi de l'horizontale."""
    return [Arm(ang, h, k) for ang in (phi, 180 - phi, 180 + phi, 360 - phi)]


def piste_onde(phi=56.0, h=60, cuts=(18,), spacing=60, Y=400):
    """A. ONDE — un X typographique : deux faisceaux de largeur constante,
    extrémités coupées à l'horizontale (ligne de base et hauteur de
    capitale). Des ondes de vide concentriques entaillent les faisceaux
    autour du point de croisement ; l'œil complète les cercles."""
    return mark(X_arms(phi, h), cuts, spacing, "horizontale", Y / math.sin(math.radians(phi)))


def piste_projection(phi=40.0, h_mid=48, k=0.055, cuts=(18,), spacing=60, X=400):
    """B. PROJECTION — chaque faisceau s'élargit de gauche (la source) vers
    la droite (l'écran) ; toutes les extrémités sont coupées à la
    verticale, comme le plan de l'écran. L'X se lit dans le sens de la
    lecture."""
    arms = [Arm(phi, h_mid, k), Arm(-phi, h_mid, k),
            Arm(180 - phi, h_mid, -k), Arm(180 + phi, h_mid, -k)]
    return mark(arms, cuts, spacing, "verticale", X / math.cos(math.radians(phi)))


def piste_foyer(phi=56.0, h=36, k=0.07, cuts=(18,), spacing=60, Y=400):
    """C. FOYER — chambre noire : les faisceaux s'affinent en convergeant
    vers l'objectif et s'élargissent après s'y être croisés. Extrémités
    horizontales, comme en A."""
    return mark(X_arms(phi, h, k), cuts, spacing, "horizontale", Y / math.sin(math.radians(phi)))


def ecartee_rotor():
    """Écartée : bouts arrondis et symétrie de rotation -> lecture « ventilateur »."""
    return mark(X_arms(45.0, 58), (30,), 60, "cercle", 440, offset=36)


PISTES = {
    "A-onde": piste_onde,
    "A2-onde-double": lambda: piste_onde(cuts=(18, 14)),
    "B-projection": piste_projection,
    "C-foyer": piste_foyer,
    "Z-ecartee-rotor": ecartee_rotor,
}


# --- sortie SVG --------------------------------------------------------------

def svg(m, fill=COBALT, impact_fill=None, bg=None, construction=False, title="RippleXTV — X-Beam"):
    impact_fill = impact_fill or fill
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" role="img">',
           f"<title>{title}</title>"]
    if bg:
        out.append(f'<rect width="{SIZE}" height="{SIZE}" fill="{bg}"/>')
    out.append(f'<path fill="{fill}" d="{" ".join(m["arms"])}"/>')
    out.append(f'<path fill="{impact_fill}" d="{m["impact"]}"/>')
    if construction:
        g = 'fill="none" stroke="#00D2FF" stroke-width="1.5"'
        out.append(f'<g {g} opacity="0.85">')
        for r in sorted(set(m["circles"])):
            out.append(f'<circle cx="{C}" cy="{C}" r="{r:.2f}" stroke-dasharray="6 5"/>')
        for a in m["arms_obj"]:
            p = add((0, 0), mul(a.u, m["R"] + 40))
            out.append(f'<line x1="{C}" y1="{C}" x2="{p[0] + C:.2f}" y2="{p[1] + C:.2f}"/>')
        out.append(f'<line x1="{C}" y1="40" x2="{C}" y2="960" stroke-dasharray="2 6"/>')
        out.append(f'<line x1="40" y1="{C}" x2="960" y2="{C}" stroke-dasharray="2 6"/>')
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def extent(m):
    """Rayon du cercle circonscrit au monogramme (centre du carré)."""
    pts = re.findall(r"(-?\d+\.\d+) (-?\d+\.\d+)", " ".join(m["arms"]))
    return max(math.hypot(float(x) - C, float(y) - C) for x, y in pts)


def avatar(m, fill=COBALT, impact_fill=None, fit=0.86, bg=ABYSS):
    """Avatar 1000 x 1000 : le monogramme occupe `fit` du diamètre du
    cercle de recadrage."""
    s = fit * C / extent(m)
    inner = svg(m, fill=fill, impact_fill=impact_fill).split("\n")
    body = "\n".join(l for l in inner if l.startswith("<path"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" role="img">'
            f"<title>RippleXTV — avatar</title>"
            f'<rect width="{SIZE}" height="{SIZE}" fill="{bg}"/>'
            f'<g transform="translate({C} {C}) scale({s:.4f}) translate({-C} {-C})">{body}</g></svg>')


def write_variants(name, m, outdir):
    variants = {
        "cobalt": svg(m),
        "blanc": svg(m, fill=WHITE),
        "noir": svg(m, fill=ABYSS),
        "bicolore": svg(m, fill=COBALT, impact_fill=CYAN),
        "construction": svg(m, construction=True, bg=ABYSS),
        "avatar": avatar(m),
        "avatar-bicolore": avatar(m, impact_fill=CYAN),
        "avatar-noir-sur-cobalt": avatar(m, fill=ABYSS, bg=COBALT),
        "avatar-noir-sur-abyss": avatar(m, fill=ABYSS),
    }
    for v, s in variants.items():
        with open(os.path.join(outdir, f"{name}_{v}.svg"), "w") as f:
            f.write(s)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, "out")
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        os.remove(os.path.join(outdir, f))
    for name, fn in PISTES.items():
        write_variants(name, fn(), outdir)
    # version optique pour les petites tailles (<= 48 px) : une seule onde, plus large
    write_variants("A-onde-petite-taille", piste_onde(h=66, cuts=(40,)), outdir)
    # B2 : sources épaissies pour mieux tenir aux petites tailles
    write_variants("B2-projection-sources-epaissies", piste_projection(k=0.035), outdir)
    print("ok")
