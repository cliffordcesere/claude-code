#!/usr/bin/env python3
"""
build.py — Youmi Wings flyer, rebuilt as a real, print-ready file.

Two directions from the same brief:
  v2  "reproduce"  keeps the ChatGPT architecture (wordmark on top, product
                   photo in the middle, information bar at the bottom) but
                   executes it on a grid with one accent and no decoration.
  v3  "studio"     same content, recomposed: type does the work, the photo is
                   a band, no badges, one accent.

Layout is written once in millimetres against a display list, then rendered by
two backends: Pillow (PNG proof at 300 dpi) and ReportLab (vector PDF with
embedded fonts). Both read the same primitives, so the proof cannot drift from
the print file.

Usage:
    python3 build.py                 # every format, both directions
    python3 build.py v2 A5           # one direction, one format
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image
from reportlab.lib.colors import CMYKColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
OUT = ROOT / "out"
FONTS = ROOT.parent.parent / ".tmp-fonts"

MM = 72 / 25.4  # points per millimetre

# ─────────────────────────────────────────────────────────────── palette
V2 = {
    "ink": "#F3EADA",
    "paper": "#17130F",
    "accent": "#FFC21F",
    "muted": "#A79C8B",
    "rule": "#3C342A",
}
V3 = {
    "ink": "#14120F",
    "paper": "#E7E1D4",
    "accent": "#FFC21F",
    "muted": "#6E685C",
    "rule": "#C6BEAE",
}

FONT_FILES = {
    "script": "Lobster-Regular.ttf",
    "slab": "Bevan-Regular.ttf",
    "condensed": "Anton-Regular.ttf",
    "sans": "Inter%5Bopsz,wght%5D.ttf",
    "sansbold": "ArchivoBlack-Regular.ttf",
    "mono": "SpaceMono-Regular.ttf",
    "monobold": "SpaceMono-Bold.ttf",
    "italic": "PlayfairDisplay-Italic%5Bwght%5D.ttf",
}


# ─────────────────────────────────────────────────────────────── display list
@dataclass
class Scene:
    w: float
    h: float
    ops: list = field(default_factory=list)

    def rect(self, x, y, w, h, color):
        self.ops.append(("rect", x, y, w, h, color))

    def line(self, x1, y1, x2, y2, color, weight=0.2):
        self.ops.append(("line", x1, y1, x2, y2, color, weight))

    def image(self, path, x, y, w, h):
        self.ops.append(("image", str(path), x, y, w, h))

    def text(self, x, y, s, font, size, color, tracking=0.0, align="left"):
        """size in mm (em size); y is the baseline, measured from the top edge."""
        self.ops.append(("text", x, y, s, font, size, color, tracking, align))

    def measure(self, s, font, size):
        """Width in mm of a string, from the actual font file (same file in both backends)."""
        from PIL import ImageFont

        f = ImageFont.truetype(str(FONTS / FONT_FILES[font]), 200)
        return f.getlength(s) / 200 * size

    def gradient(self, x, y, w, h, color, direction="up", bands=90):
        """Solid colour fading to transparent, banded so both backends agree."""
        for i in range(bands):
            t = i / (bands - 1)
            alpha = t if direction == "up" else 1 - t
            y0 = y + h * (i / bands)
            self.rect(x, y0, w, h / bands + 0.06, (color, alpha))


def hex_rgb(c):
    c = c.lstrip("#")
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def cover(path, w_mm, h_mm, dpi, tmpdir):
    """Crop to the target aspect ratio so both backends scale identically."""
    im = Image.open(path).convert("RGB")
    target = w_mm / h_mm
    src = im.width / im.height
    if src > target:
        nw = int(im.height * target)
        left = (im.width - nw) // 2
        im = im.crop((left, 0, left + nw, im.height))
    else:
        nh = int(im.width / target)
        top = int((im.height - nh) * 0.42)
        im = im.crop((0, top, im.width, top + nh))
    out = Path(tmpdir) / f"cover_{abs(hash((str(path), w_mm, h_mm)))}.png"
    im.save(out)
    return out


# ─────────────────────────────────────────────────────────────── PIL backend
def render_png(scene: Scene, path: Path, dpi=300):
    px = dpi / 25.4
    size = (round(scene.w * px), round(scene.h * px))
    canvas = Image.new("RGB", size, (255, 255, 255))
    fonts_cache = {}

    def font(key, size_mm):
        if key not in FONT_FILES:
            raise KeyError(f"unknown font {key}")
        px_size = max(1, round(size_mm * px))
        ck = (key, px_size)
        if ck not in fonts_cache:
            from PIL import ImageFont

            fonts_cache[ck] = ImageFont.truetype(str(FONTS / FONT_FILES[key]), px_size)
        return fonts_cache[ck]

    tmpdir = tempfile.mkdtemp()

    for op in scene.ops:
        kind = op[0]
        if kind == "rect":
            _, x, y, w, h, color = op
            layer = Image.new("RGBA", size, (0, 0, 0, 0))
            from PIL import ImageDraw

            d = ImageDraw.Draw(layer)
            if isinstance(color, tuple):
                rgb, alpha = color
                fill = hex_rgb(rgb) + (round(alpha * 255),)
            else:
                fill = hex_rgb(color) + (255,)
            d.rectangle(
                [round(x * px), round(y * px), round((x + w) * px), round((y + h) * px)],
                fill=fill,
            )
            canvas = Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB")
        elif kind == "line":
            _, x1, y1, x2, y2, color, weight = op
            from PIL import ImageDraw

            d = ImageDraw.Draw(canvas)
            d.line(
                [x1 * px, y1 * px, x2 * px, y2 * px],
                fill=hex_rgb(color),
                width=max(1, round(weight * px)),
            )
        elif kind == "image":
            _, p, x, y, w, h = op
            cropped = cover(p, w, h, dpi, tmpdir)
            tile = Image.open(cropped).resize((round(w * px), round(h * px)), Image.LANCZOS)
            canvas.paste(tile, (round(x * px), round(y * px)))
        elif kind == "text":
            _, x, y, s, fontkey, size_mm, color, tracking, align = op
            from PIL import ImageDraw

            d = ImageDraw.Draw(canvas)
            f = font(fontkey, size_mm)
            tr = tracking * px
            total = sum(f.getlength(ch) for ch in s) + tr * max(0, len(s) - 1)
            if align == "center":
                cx = x * px - total / 2
            elif align == "right":
                cx = x * px - total
            else:
                cx = x * px
            for ch in s:
                d.text((cx, y * px), ch, font=f, fill=hex_rgb(color), anchor="ls")
                cx += f.getlength(ch) + tr

    canvas.save(path, dpi=(dpi, dpi))
    return path


# ─────────────────────────────────────────────────────────────── PDF backend
def register_fonts():
    for key, file in FONT_FILES.items():
        pdfmetrics.registerFont(TTFont(f"Y-{key}", str(FONTS / file)))


def rgb_to_cmyk(color):
    r, g, b = [v / 255 for v in hex_rgb(color)]
    k = 1 - max(r, g, b)
    if k >= 1:
        return CMYKColor(0, 0, 0, 1)
    return CMYKColor(
        (1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k
    )


def render_pdf(scene: Scene, path: Path, dpi=300):
    register_fonts()
    W, H = scene.w * MM, scene.h * MM
    c = rl_canvas.Canvas(str(path), pagesize=(W, H))
    c.setTitle("Youmi Wings")
    tmpdir = tempfile.mkdtemp()

    def Y(y_mm):
        return H - y_mm * MM

    for op in scene.ops:
        kind = op[0]
        if kind == "rect":
            _, x, y, w, h, color = op
            if isinstance(color, tuple):
                col = rgb_to_cmyk(color[0])
                col.alpha = color[1]
            else:
                col = rgb_to_cmyk(color)
            c.setFillColor(col)
            c.rect(x * MM, Y(y + h), w * MM, h * MM, stroke=0, fill=1)
        elif kind == "line":
            _, x1, y1, x2, y2, color, weight = op
            c.setStrokeColor(rgb_to_cmyk(color))
            c.setLineWidth(max(0.2, weight * MM))
            c.line(x1 * MM, Y(y1), x2 * MM, Y(y2))
        elif kind == "image":
            _, p, x, y, w, h = op
            cropped = cover(p, w, h, dpi, tmpdir)
            c.drawImage(
                ImageReader(str(cropped)),
                x * MM,
                Y(y + h),
                w * MM,
                h * MM,
                preserveAspectRatio=False,
                mask=None,
            )
        elif kind == "text":
            _, x, y, s, fontkey, size_mm, color, tracking, align = op
            c.setFillColor(rgb_to_cmyk(color))
            c.setFont(f"Y-{fontkey}", size_mm * MM)
            c._charSpace = tracking * MM
            width = pdfmetrics.stringWidth(s, f"Y-{fontkey}", size_mm * MM) + tracking * MM * max(
                0, len(s) - 1
            )
            if align == "center":
                px = x * MM - width / 2
            elif align == "right":
                px = x * MM - width
            else:
                px = x * MM
            c.drawString(px, Y(y), s)
            c._charSpace = 0

    c.showPage()
    c.save()
    return path


# ─────────────────────────────────────────────────────────────── content
COPY = {
    "brand": "Youmi",
    "brand2": "WINGS",
    "tagline": "Le goût qui fait la différence",
    "claim1": "Des wings savoureux,",
    "claim2": "à chaque bouchée.",
    "offer": "SPÉCIAL BIÈRE",
    "n1": "5",
    "n2": "1 000",
    "unit": "GDS",
    "special": "SPÉCIALITÉ WINGS",
    "day": "Chaque vendredi",
    "delivery": "Livraison disponible",
    "addr1": "Delmas 75",
    "addr2": "Siloe M",
    "tel1": "3179 3416",
    "tel2": "4943 2244",
    "minimum": "Minimum prix : 750 gds",
}


def layout_v2(scene: Scene, P):
    """Reproduce the original architecture, executed on a grid.

    Order of bands, top to bottom, each one computed from the previous so the
    layout cannot overlap: header, photo, price, claim, information, footer.
    """
    W = scene.w
    tw, th = W - 6, scene.h - 6
    m = 3 + tw * 0.046
    right = 3 + tw - tw * 0.046
    k = th / 210.0

    y = 3.0
    h_header, h_photo, h_price, h_claim, h_bar, h_foot = (
        42 * k, 86 * k, 24 * k, 13 * k, 30 * k, 11 * k,
    )

    scene.rect(0, 0, W, scene.h, P["paper"])

    # ── 1. header
    scene.text(W / 2, y + 17 * k, COPY["brand"], "script", 21 * k, P["accent"], align="center")
    scene.text(W / 2, y + 27.5 * k, COPY["brand2"], "slab", 10.5 * k, P["ink"], tracking=1.5, align="center")
    scene.text(W / 2, y + 33.5 * k, COPY["tagline"], "italic", 3.9 * k, P["muted"], align="center")
    scene.line(m, y + 37.5 * k, right, y + 37.5 * k, P["accent"], 0.45)
    y += h_header

    # ── 2. photo band, full bleed
    scene.image(ASSETS / "tray_full.png", 0, y, W, h_photo)
    scene.gradient(0, y + h_photo - 8 * k, W, 8 * k, P["paper"], "up")
    y += h_photo

    # ── 3. price, set on paper
    scene.text(m, y + 5 * k, COPY["offer"], "mono", 2.6 * k, P["accent"], tracking=0.5)
    x = m
    scene.text(x, y + 19 * k, COPY["n1"], "condensed", 15.5 * k, P["ink"], tracking=-0.35)
    x += scene.measure(COPY["n1"], "condensed", 15.5 * k) + 2.2 * k
    scene.text(x, y + 19 * k, "POU", "condensed", 6.2 * k, P["muted"], tracking=0.3)
    x += scene.measure("POU", "condensed", 6.2 * k) + 2.6 * k
    scene.text(x, y + 19 * k, COPY["n2"], "condensed", 15.5 * k, P["accent"], tracking=-0.35)
    x += scene.measure(COPY["n2"], "condensed", 15.5 * k) + 2.4 * k
    scene.text(x, y + 19 * k, COPY["unit"], "mono", 3.2 * k, P["muted"])
    y += h_price

    # ── 4. claim, one line, no block
    scene.text(m, y + 5 * k, COPY["claim1"] + " " + COPY["claim2"], "italic", 4.3 * k, P["muted"])
    y += h_claim

    # ── 5. information bar
    bar_bottom = scene.h - 3 - h_foot
    scene.rect(0, y, W, bar_bottom - y, P["paper"])
    top = bar_bottom - 13 * k
    scene.text(m, top, COPY["special"], "condensed", 4.4 * k, P["ink"], tracking=0.3)
    scene.text(m, top + 6.2 * k, COPY["day"], "italic", 3.6 * k, P["accent"])

    c1, c2 = m + tw * 0.34, m + tw * 0.66
    for cx in (c1 - 5, c2 - 5):
        scene.line(cx, top - 3.6 * k, cx, top + 10 * k, P["rule"], 0.18)
    scene.text(c1, top + 0.4 * k, COPY["addr1"], "sans", 4.0 * k, P["ink"])
    scene.text(c1, top + 5.9 * k, COPY["addr2"], "sans", 4.0 * k, P["ink"])
    scene.text(c2, top + 0.4 * k, COPY["tel1"], "mono", 3.4 * k, P["ink"])
    scene.text(c2, top + 5.9 * k, COPY["tel2"], "mono", 3.4 * k, P["ink"])

    # ── 6. footer strip
    fy = scene.h - 3 - h_foot
    scene.rect(0, fy, W, h_foot, P["accent"])
    scene.text(m, fy + h_foot / 2 + 1.1 * k, COPY["minimum"], "monobold", 2.9 * k, P["paper"])
    scene.text(right, fy + h_foot / 2 + 1.1 * k, "LIVRAISON DISPONIBLE", "mono", 2.5 * k, P["paper"],
               tracking=0.25, align="right")


def layout_v3(scene: Scene, P):
    """Studio direction: type carries the piece, the photo is a band."""
    W = scene.w
    tw, th = W - 6, scene.h - 6
    m = 3 + tw * 0.052
    right = 3 + tw - tw * 0.052
    k = th / 210.0

    scene.rect(0, 0, W, scene.h, P["paper"])

    # ── masthead
    scene.text(m, 3 + 9 * k, "YOUMI", "condensed", 5.6 * k, P["ink"], tracking=0.45)
    w_youmi = scene.measure("YOUMI", "condensed", 5.6 * k) + 0.45 * 5.6 * k * 4
    scene.text(m + w_youmi + 3.2 * k, 3 + 9 * k,
               "WINGS", "condensed", 5.6 * k, P["muted"], tracking=0.45)
    scene.text(right, 3 + 9 * k, "DELMAS 75 · SILOE M", "mono", 2.2 * k, P["muted"], tracking=0.3, align="right")
    scene.line(m, 3 + 12.6 * k, right, 3 + 12.6 * k, P["ink"], 0.3)

    # ── the number, one idea
    scene.text(m, 3 + 17.5 * k, "OFFRE SPÉCIALE BIÈRE", "mono", 2.4 * k, "#9A7413", tracking=0.5)
    scene.text(m, 3 + 44 * k, "5 POU", "condensed", 21 * k, P["ink"], tracking=-0.45)
    scene.text(m, 3 + 66 * k, "1 000", "condensed", 21 * k, P["ink"], tracking=-0.45)
    scene.text(m + scene.measure("1 000", "condensed", 21 * k) + 2.4 * k, 3 + 66 * k,
               "GDS", "mono", 4.2 * k, P["muted"], tracking=0.5)
    scene.line(m, 3 + 70.5 * k, right, 3 + 70.5 * k, P["accent"], 1.6 * k)

    scene.text(m, 3 + 79 * k, COPY["tagline"], "italic", 4.7 * k, P["ink"])
    scene.text(m, 3 + 85.5 * k, "SPÉCIALITÉ WINGS · CHAQUE VENDREDI · LIVRAISON", "mono", 2.1 * k, P["muted"], tracking=0.28)
    scene.text(m, 3 + 93 * k, COPY["claim1"] + " " + COPY["claim2"], "italic", 3.8 * k, P["muted"])

    # ── photo band, full bleed
    band_y = 3 + 99 * k
    scene.image(ASSETS / "tray_full.png", 0, band_y, W, scene.h - 3 - 12 * k - band_y)
    scene.line(0, band_y, W, band_y, P["ink"], 0.35)

    # ── footer
    scene.rect(0, scene.h - 3 - 12 * k, W, 12 * k, P["ink"])
    scene.text(m, scene.h - 3 - 4.4 * k, "3179 3416   ·   4943 2244", "monobold", 2.9 * k, P["accent"])
    scene.text(right, scene.h - 3 - 4.4 * k, "MINIMUM 750 GDS", "mono", 2.5 * k, P["ink"], tracking=0.28, align="right")


def layout_v4(scene: Scene, P):
    """Dark direction: the address the client picked, with the plate and the bucket."""
    W = scene.w
    tw, th = W - 6, scene.h - 6
    m = 3 + tw * 0.046
    right = 3 + tw - tw * 0.046
    k = th / 210.0

    y = 3.0
    h_header, h_hero, h_price, h_bar, h_foot = 40 * k, 100 * k, 31 * k, 27 * k, 11 * k

    scene.rect(0, 0, W, scene.h, P["paper"])

    # ── 1. header
    scene.text(m, y + 17 * k, COPY["brand"], "script", 20 * k, P["accent"])
    scene.text(m, y + 27 * k, COPY["brand2"], "slab", 9.6 * k, P["ink"], tracking=1.4)
    scene.text(m, y + 33.6 * k, COPY["tagline"], "italic", 3.8 * k, P["muted"])
    scene.line(m, y + 37 * k, right, y + 37 * k, P["accent"], 0.45)

    # ── 2. the plate, full bleed
    scene.image(ASSETS / "tray_hero.png", 0, y + h_header, W, h_hero)
    scene.gradient(0, y + h_header + h_hero - 10 * k, W, 10 * k, P["paper"], "up")

    # ── 3. the bucket, sitting on the photo like an inset
    bw = tw * 0.28
    bh = bw * 1.00
    bx = right - bw
    by = y + h_header + 7 * k
    scene.rect(bx - 1.2 * k, by - 1.2 * k, bw + 2.4 * k, bh + 2.4 * k, P["paper"])
    scene.image(ASSETS / "beer_ice.png", bx, by, bw, bh)
    for a, b, c, d in (
        (bx - 0.4 * k, by - 0.4 * k, bx + bw + 0.4 * k, by - 0.4 * k),
        (bx - 0.4 * k, by + bh + 0.4 * k, bx + bw + 0.4 * k, by + bh + 0.4 * k),
        (bx - 0.4 * k, by - 0.4 * k, bx - 0.4 * k, by + bh + 0.4 * k),
        (bx + bw + 0.4 * k, by - 0.4 * k, bx + bw + 0.4 * k, by + bh + 0.4 * k),
    ):
        scene.line(a, b, c, d, P["accent"], 0.35)
    y += h_header + h_hero

    # ── 4. price
    scene.text(m, y + 4.6 * k, COPY["offer"], "mono", 2.6 * k, P["accent"], tracking=0.5)
    x = m
    scene.text(x, y + 18.5 * k, COPY["n1"], "condensed", 15.5 * k, P["ink"], tracking=-0.35)
    x += scene.measure(COPY["n1"], "condensed", 15.5 * k) + 2.2 * k
    scene.text(x, y + 18.5 * k, "POU", "condensed", 6.2 * k, P["muted"], tracking=0.3)
    x += scene.measure("POU", "condensed", 6.2 * k) + 2.6 * k
    scene.text(x, y + 18.5 * k, COPY["n2"], "condensed", 15.5 * k, P["accent"], tracking=-0.35)
    x += scene.measure(COPY["n2"], "condensed", 15.5 * k) + 2.4 * k
    scene.text(x, y + 18.5 * k, COPY["unit"], "mono", 3.2 * k, P["muted"])
    scene.text(m, y + 25.5 * k, COPY["claim1"] + " " + COPY["claim2"], "italic", 3.8 * k, P["muted"])
    y += h_price

    # ── 5. information bar
    bar_bottom = scene.h - 3 - h_foot
    scene.rect(0, y, W, bar_bottom - y, P["paper"])
    top = bar_bottom - 12.5 * k
    scene.line(m, y + 3 * k, right, y + 3 * k, P["rule"], 0.2)
    scene.text(m, top, COPY["special"], "condensed", 4.4 * k, P["ink"], tracking=0.3)
    scene.text(m, top + 6.2 * k, COPY["day"], "italic", 3.6 * k, P["accent"])

    c1, c2 = m + tw * 0.34, m + tw * 0.66
    for cx in (c1 - 5, c2 - 5):
        scene.line(cx, top - 3.6 * k, cx, top + 10 * k, P["rule"], 0.18)
    scene.text(c1, top + 0.4 * k, COPY["addr1"], "sans", 4.0 * k, P["ink"])
    scene.text(c1, top + 5.9 * k, COPY["addr2"], "sans", 4.0 * k, P["ink"])
    scene.text(c2, top + 0.4 * k, COPY["tel1"], "mono", 3.4 * k, P["ink"])
    scene.text(c2, top + 5.9 * k, COPY["tel2"], "mono", 3.4 * k, P["ink"])

    # ── 6. footer strip
    fy = scene.h - 3 - h_foot
    scene.rect(0, fy, W, h_foot, P["accent"])
    scene.text(m, fy + h_foot / 2 + 1.1 * k, COPY["minimum"], "monobold", 2.9 * k, P["paper"])
    scene.text(right, fy + h_foot / 2 + 1.1 * k, "LIVRAISON DISPONIBLE", "mono", 2.5 * k,
               P["paper"], tracking=0.25, align="right")


LAYOUTS = {"v2": (layout_v2, V2), "v3": (layout_v3, V3), "v4": (layout_v4, V2)}
FORMATS = {"A5": (148, 210), "A6": (105, 148), "4x5": (108, 135)}


def build(direction: str, fmt: str, bleed=3):
    layout, palette = LAYOUTS[direction]
    tw, th = FORMATS[fmt]
    scene = Scene(tw + bleed * 2, th + bleed * 2)
    layout(scene, palette)
    stem = OUT / f"youmi_{direction}_{fmt}"
    render_png(scene, stem.with_suffix(".png"))
    render_pdf(scene, stem.with_suffix(".pdf"))
    print(f"  {stem.name}.png / .pdf   {scene.w}×{scene.h} mm")
    return stem


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    args = sys.argv[1:]
    dirs = [args[0]] if args and args[0] in LAYOUTS else list(LAYOUTS)
    fmts = [args[1]] if len(args) > 1 and args[1] in FORMATS else list(FORMATS)
    for d in dirs:
        for f in fmts:
            build(d, f)
