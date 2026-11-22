"""Generate every Clean Air logo variant from one master airflow geometry.

Run: python3 site/src/logo/build_logos.py  (writes site/static/logo/*.svg)
The wordmark is live text (Georgia, a system font), not outlined lettering, and does not
claim to match the reference wordmark exactly.
"""
import os
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "static", "logo")
os.makedirs(OUT, exist_ok=True)
NAVY, RED, INK, WHITE = "#141F52", "#E3120B", "#1A1A1A", "#FFFFFF"

# Master geometry: one tapered airflow ribbon, repeated three times.
RIBBON = "M0 24 C16 8 38 4 58 9 C74 13 88 12 100 0 C94 17 79 26 60 24 C41 22 20 16 0 24 Z"
ROWS = [(0, 0, 1.00), (6, 24, 0.86), (0, 48, 0.90)]   # (x offset, y offset, x scale)

def symbol(colours, x=0, y=0, s=1.0):
    g = []
    for (dx, dy, sx), c in zip(ROWS, colours):
        g.append(f'<path d="{RIBBON}" fill="{c}" transform="translate({x+dx*s:.2f} {y+dy*s:.2f}) scale({sx*s:.3f} {s:.3f})"/>')
    return "".join(g)

def svg(w, h, body, title, decorative=False):
    a = 'aria-hidden="true" focusable="false"' if decorative else f'role="img" aria-labelledby="t"'
    t = "" if decorative else f"<title id=\"t\">{title}</title>"
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {a}>{t}{body}</svg>\n'

def wordmark(fill, x, y, size):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="Georgia, \'Times New Roman\', serif" '
            f'font-weight="700" font-size="{size}" letter-spacing="-0.5">Clean Air</text>')

V = {
 "logo-horizontal.svg": (330, 78, symbol([NAVY, RED, NAVY], 4, 3) + wordmark(INK, 118, 56, 46), "Clean Air"),
 "logo-reversed.svg":   (330, 78, symbol([WHITE, RED, WHITE], 4, 3) + wordmark(WHITE, 118, 56, 46), "Clean Air"),
 "logo-navy.svg":       (330, 78, symbol([NAVY, NAVY, NAVY], 4, 3) + wordmark(NAVY, 118, 56, 46), "Clean Air"),
 "logo-white.svg":      (330, 78, symbol([WHITE, WHITE, WHITE], 4, 3) + wordmark(WHITE, 118, 56, 46), "Clean Air"),
 "symbol.svg":          (108, 76, symbol([NAVY, RED, NAVY], 2, 2), "Clean Air"),
}
for name, (w, h, body, title) in V.items():
    open(os.path.join(OUT, name), "w").write(svg(w, h, body, title))

# Favicon: simplified, thicker bars that survive 16 px. Derived from the same three-row rhythm.
BAR = "M2 9 C8 4 15 4 20 6 C25 8 28 7 30 4 L30 9 C28 12 25 13 20 11 C15 9 8 9 2 14 Z"
fav = "".join(f'<path d="{BAR}" fill="{c}" transform="translate(0 {dy})"/>' for dy, c in [(-1, NAVY), (8, RED), (17, NAVY)])
open(os.path.join(OUT, "favicon.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32"><title>Clean Air</title>{fav}</svg>\n')
print(sorted(os.listdir(OUT)))
