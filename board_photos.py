"""Straightens the real board photos (boards/src/*.webp) so the playing surface fills exactly the
game's walls (-500..500) with FRAME units of the real frame around it. Writes boards/<id>.webp
and boards/check-<id>.png (with the game's pockets and baselines drawn on top, to eyeball the fit).
Run: python board_photos.py"""
import numpy as np
from PIL import Image, ImageDraw

HALF, FRAME, OUT = 500, 100, 1800  # must match HALF / FRAME in game.html
SPAN = 2 * (HALF + FRAME)


def lum(a):
    return .299 * a[..., 0] + .587 * a[..., 1] + .114 * a[..., 2]


def edge_points(A, side):
    """Where the black rubber cushion meets the light, warm wood of the playing surface, along one side."""
    L = lum(A); warm = (A[..., 0] - A[..., 2]) > 15
    H, W = L.shape
    pts = []
    span = H if side in 'lr' else W
    for k in range(int(.3 * span), int(.7 * span), 5):
        line = L[k, :] if side in 'lr' else L[:, k]
        wl = warm[k, :] if side in 'lr' else warm[:, k]
        if side in 'rb':
            line = line[::-1]; wl = wl[::-1]
        n = len(line); i = 0
        while i < n * .15:
            if line[i] < 85:
                j = i
                while j < n and line[j] < 85:
                    j += 1
                seg = slice(j, j + 60)
                if j - i >= 4 and ((line[seg] > 145) & wl[seg]).mean() > .7:
                    pts.append((k, j if side in 'lt' else n - 1 - j))
                    break
                i = j
            i += 1
    return pts


def fit(pts):
    """Robust straight line pos = a*k + b."""
    k = np.array([p[0] for p in pts], float); v = np.array([p[1] for p in pts], float)
    a, b = np.polyfit(k, v, 1)
    for _ in range(3):
        r = np.abs(v - (a * k + b)); keep = r < max(3, np.median(r) * 3)
        a, b = np.polyfit(k[keep], v[keep], 1)
    return a, b


def corners(img):
    A = np.asarray(img).astype(float)
    left, right = fit(edge_points(A, 'l')), fit(edge_points(A, 'r'))   # x = a*y + b
    top, bot = fit(edge_points(A, 't')), fit(edge_points(A, 'b'))      # y = a*x + b

    def cross(v, h):  # x = v.a*y + v.b ; y = h.a*x + h.b
        y = (h[0] * v[1] + h[1]) / (1 - h[0] * v[0]); x = v[0] * y + v[1]
        return x, y
    return [cross(left, top), cross(right, top), cross(right, bot), cross(left, bot)]


def perspective_coeffs(dst, src):
    """Coefficients PIL needs to map output (dst) points back to input (src) points."""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def to_px(w):
    return (w + HALF + FRAME) / SPAN * OUT


for name in ['classic', 'pro', 'champion']:
    img = Image.open(f'boards/src/{name}.webp').convert('RGB')
    src = corners(img)
    a, b = to_px(-HALF), to_px(HALF)
    dst = [(a, a), (b, a), (b, b), (a, b)]
    out = img.transform((OUT, OUT), Image.PERSPECTIVE, perspective_coeffs(dst, src), Image.BICUBIC)
    out.save(f'boards/{name}.webp', quality=82, method=6)
    chk = out.copy(); d = ImageDraw.Draw(chk)
    for px, py in [(470, 470), (-470, 470), (-470, -470), (470, -470)]:
        r = 36 / SPAN * OUT; d.ellipse([to_px(px) - r, to_px(py) - r, to_px(px) + r, to_px(py) + r], outline=(255, 0, 0), width=4)
    for s in (1, -1):
        y = to_px(s * 341.5); d.line([to_px(-296), y, to_px(296), y], fill=(255, 0, 0), width=3)
        x = to_px(s * 341.5); d.line([x, to_px(-296), x, to_px(296)], fill=(255, 0, 0), width=3)
    d.rectangle([a, a, b, b], outline=(0, 255, 0), width=3)
    chk.resize((600, 600)).save(f'boards/check-{name}.png')
    print(name, 'corners', [(round(x), round(y)) for x, y in src])
