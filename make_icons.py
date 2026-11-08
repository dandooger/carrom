"""Builds the logo files and app icons from the Carrom Israel logo artwork (logo-source.webp).
Run: python make_icons.py"""
import os
from PIL import Image, ImageDraw

os.makedirs("icons", exist_ok=True)
SRC = "logo-source.webp"
im = Image.open(SRC).convert("RGB")
BG = im.getpixel((5, 5))  # the artwork's cream background
W, H = im.size

# full logo (board + CARROM ISRAEL), trimmed with a small margin
full = im.crop((142 - 30, 122 - 30, 1024 + 30, 1078 + 30))
full.thumbnail((640, 640), Image.LANCZOS)
full.save("icons/logo.webp", quality=86, method=6)

# the mark alone (board and flying striker) for small places like the lobby corner
mark = im.crop((142 - 14, 122 - 14, 1018 + 14, 666 + 14))
mark.thumbnail((240, 240), Image.LANCZOS)
mark.save("icons/logo-mark.webp", quality=88, method=6)


def square(img, frac, size, round_corners):
    """Logo centred on a square cream tile; frac = how much of the tile the logo may fill."""
    tile = Image.new("RGBA", (1024, 1024), BG + (255,))
    art = img.copy()
    art.thumbnail((int(1024 * frac), int(1024 * frac)), Image.LANCZOS)
    tile.paste(art, ((1024 - art.width) // 2, (1024 - art.height) // 2))
    if round_corners:
        m = Image.new("L", (1024, 1024), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, 1023, 1023], radius=200, fill=255)
        tile.putalpha(m)
    return tile.resize((size, size), Image.LANCZOS)


logo_sq = im.crop((142 - 20, 122 - 20, 1024 + 20, 1078 + 20))
square(logo_sq, .92, 512, True).save("icons/icon-512.png", optimize=True)
square(logo_sq, .92, 192, True).save("icons/icon-192.png", optimize=True)
square(logo_sq, .72, 512, False).save("icons/maskable-512.png", optimize=True)  # Android may crop to a circle
square(logo_sq, .9, 180, False).convert("RGB").save("icons/apple-touch-icon.png", optimize=True)
print("logo and icons done")
