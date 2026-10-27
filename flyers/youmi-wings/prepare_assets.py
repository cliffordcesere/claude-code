#!/usr/bin/env python3
"""
prepare_assets.py — extract and clean the photographic assets from the source flyer.

The source JPEG is 720x1080. Any print use is therefore soft: we upscale with
LANCZOS, apply a light unsharp mask, then re-introduce a fine grain so the
softness reads as photographic texture instead of blur. The limitation is
recorded in NOTES.md; the client should supply the original photo for A3.

Outputs (assets/):
  tray_hero.png    the tray, wide crop, for the dark direction
  tray_full.png    the same tray in a thin band, for the light direction
  beer_ice.png     the bucket of bottles, credited to the client as supplied art
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

SRC = Path("/tmp/arena-coding-uploads/IMG-20261026-WA0007.jpg")
OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)


def upscale(im: Image.Image, factor: float) -> Image.Image:
    w, h = im.size
    big = im.resize((int(w * factor), int(h * factor)), Image.LANCZOS)
    big = big.filter(ImageFilter.UnsharpMask(radius=2.2, percent=95, threshold=2))
    return ImageEnhance.Color(big).enhance(1.06)


def add_grain(im: Image.Image, amount: int = 7) -> Image.Image:
    """Deterministic fine grain, so re-runs are identical."""
    import random

    random.seed(20261026)
    noise = Image.new("L", im.size)
    noise.putdata(
        [128 + random.randint(-amount, amount) for _ in range(im.size[0] * im.size[1])]
    )
    return Image.blend(im, Image.merge("RGB", (noise, noise, noise)), 0.055)


def main() -> None:
    src = Image.open(SRC).convert("RGB")

    # 1. wings close-up — top left of the tray, the glazed side
    # 1b. tray, wide crop — keeps the whole plate visible in a tall band
    hero = src.crop((52, 395, 708, 812))
    hero = upscale(hero, 2.6)
    hero = add_grain(hero)
    hero.save(OUT / "tray_hero.png")
    print("tray_hero.png", hero.size)

    # 1c. the beer bucket, cropped above the original badge so no borrowed
    #     artwork leaks in. The bottles keep their own labels: see NOTES.md.
    beer = src.crop((468, 8, 716, 258))
    beer = upscale(beer, 2.0)
    beer = add_grain(beer, 5)
    beer.save(OUT / "beer_ice.png")
    print("beer_ice.png", beer.size)

    # 2. full tray — the whole composed plate, for the "reproduce" version.
    #    Bottom edge stops at y=628: below that sits the original "spécial bière"
    #    badge and the dark panel, which must not be borrowed into the new file.
    tray = src.crop((52, 432, 708, 628))
    tray = upscale(tray, 2.6)
    tray = add_grain(tray)
    tray.save(OUT / "tray_full.png")
    print("tray_full.png", tray.size)


if __name__ == "__main__":
    main()
