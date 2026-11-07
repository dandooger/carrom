"""Draws the app icons (a carrom board seen from above) into icons/. Run once: python make_icons.py"""
import math
import os
from PIL import Image, ImageDraw

os.makedirs("icons", exist_ok=True)
S = 2048  # draw big, then shrink for smooth edges


def board(size_frac, bg):
    im = Image.new("RGBA", (S, S), bg)
    d = ImageDraw.Draw(im)
    half = S * size_frac / 2
    c = S / 2
    u = half / 562  # one board unit (frame edge = 562)

    def P(x, y):
        return (c + x * u, c + y * u)

    def circle(x, y, r, fill=None, outline=None, width=1):
        x0, y0 = P(x - r, y - r)
        x1, y1 = P(x + r, y + r)
        d.ellipse([x0, y0, x1, y1], fill=fill, outline=outline, width=max(1, int(width * u)))

    # frame and surface
    d.rounded_rectangle([*P(-562, -562), *P(562, 562)], radius=int(60 * u), fill=(86, 43, 21))
    d.rounded_rectangle([*P(-548, -548), *P(548, 548)], radius=int(50 * u), outline=(222, 160, 95), width=int(6 * u))
    d.rectangle([*P(-507, -507), *P(507, 507)], fill=(42, 19, 9))
    d.rectangle([*P(-500, -500), *P(500, 500)], fill=(236, 210, 160))
    ink = (43, 27, 16)
    # baselines on four sides
    for k in range(4):
        a = k * math.pi / 2

        def R(x, y):
            return (x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))

        for yy in (320, 363):
            d.line([P(*R(-296, yy)), P(*R(296, yy))], fill=ink, width=int(7 * u))
        for xx in (-296, 296):
            circle(*R(xx, 341.5), 22, fill=(179, 48, 42), outline=ink, width=7)
    circle(0, 0, 118, outline=ink, width=7)
    # pockets
    for px, py in ((470, 470), (-470, 470), (-470, -470), (470, -470)):
        circle(px, py, 36, fill=(10, 5, 2), outline=(120, 80, 50), width=5)
    # coins around the queen
    dd = 46
    spots = []
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        spots.append((dd * math.cos(a), dd * math.sin(a), "w" if k % 2 == 0 else "b"))
        spots.append((2 * dd * math.cos(a), 2 * dd * math.sin(a), "w" if k % 2 == 0 else "b"))
        a2 = a + math.pi / 6
        spots.append((dd * math.sqrt(3) * math.cos(a2), dd * math.sqrt(3) * math.sin(a2), "b" if k % 2 == 0 else "w"))
    col = {"w": ((250, 240, 220), (150, 125, 90)), "b": ((45, 36, 31), (0, 0, 0))}
    for x, y, k in spots:
        circle(x + 4, y + 6, 22, fill=(0, 0, 0, 70))
        circle(x, y, 22, fill=col[k][0], outline=col[k][1], width=3)
        circle(x, y, 13, outline=(0, 0, 0, 60) if k == "w" else (255, 255, 255, 50), width=2)
    circle(4, 6, 22, fill=(0, 0, 0, 70))
    circle(0, 0, 22, fill=(207, 48, 44), outline=(90, 10, 10), width=3)
    # striker on the bottom baseline
    circle(5, 348, 29, fill=(0, 0, 0, 80))
    circle(0, 341.5, 29, fill=(250, 246, 236), outline=(143, 125, 90), width=3)
    circle(0, 341.5, 20, outline=(233, 155, 43), width=6)
    circle(0, 341.5, 11, outline=(196, 61, 42), width=4)
    return im


def save(im, name, px):
    im.resize((px, px), Image.LANCZOS).save(os.path.join("icons", name))


NAVY = (20, 33, 58, 255)
full = board(0.98, (0, 0, 0, 0))
save(full, "icon-512.png", 512)
save(full, "icon-192.png", 192)
safe = board(0.74, NAVY)  # maskable: board inside the safe circle
save(safe, "maskable-512.png", 512)
apple = board(0.86, NAVY)
save(apple, "apple-touch-icon.png", 180)
print("icons done")
