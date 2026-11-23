#!/usr/bin/env python3
"""Build the 1024x1024 editorial poster for make.fun bounty news-image-20261122 (v2).
Clean dark editorial infographic, drawn with PIL only. Deterministic output.
Rebuilt from scratch in a fresh session; stories verified live on 2026-11-22.
Illustrated (no real photos)."""
import os, textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), (11, 18, 32))
d = ImageDraw.Draw(img, "RGBA")

NAVY = (11, 18, 32); PANEL = (20, 32, 56); PANEL2 = (16, 26, 46)
GOLD = (255, 196, 0); RED = (214, 48, 49); WHITE = (255, 255, 255)
LIGHT = (200, 214, 235); MUTED = (150, 165, 190); ORANGE = (255, 122, 0)
TEAL = (0, 180, 180)

def wrap(text, width):
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width=width))
    return out

# ---- Header ----
d.rectangle([0, 0, 1024, 96], fill=(8, 15, 30))
d.rectangle([0, 96, 1024, 100], fill=GOLD)
d.text((28, 14), "WORLD NEWS", font=font(BOLD, 52), fill=WHITE)
d.text((28, 66), "SUNDAY  •  22 NOVEMBER 2026", font=font(BOLD, 22), fill=GOLD)
d.text((996, 20), "7 STORIES", font=font(BOLD, 28), fill=WHITE, anchor="ra")
d.text((996, 56), "ONE DAY, ONE MAP", font=font(REG, 20), fill=MUTED, anchor="ra")

# ---- Lead panel: Hormuz ----
lx, ly, lw, lh = 28, 112, 968, 272
d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=18, fill=PANEL, outline=GOLD, width=2)
# pin 1 badge
d.ellipse([lx + 18, ly + 18, lx + 58, ly + 58], fill=RED, outline=WHITE, width=2)
d.text((lx + 38, ly + 24), "1", font=font(BOLD, 26), fill=WHITE, anchor="ma")
d.text((lx + 72, ly + 20), "LEAD  •  STRAIT OF HORMUZ", font=font(BOLD, 20), fill=ORANGE)
d.text((lx + 72, ly + 48), "TANKERS HIT IN THE STRAIT", font=font(SERIF, 34), fill=WHITE)
d.text((lx + 72, ly + 88), "OF HORMUZ", font=font(SERIF, 34), fill=WHITE)
lead = ("Two tankers struck by unknown projectiles near Khasab, Oman, "
        "Sat 21 Nov. No casualties — UKMTO. Iran says its 2-day plan to "
        "reopen the strait stays on the table if the US meets its "
        "conditions; Qatari mediators held talks in Tehran.")
y = ly + 136
for line in wrap(lead, 62):
    d.text((lx + 18, y), line, font=font(REG, 19), fill=LIGHT); y += 25
d.text((lx + 18, ly + lh - 30), "NEAR KHASAB, OMAN  •  UKMTO  •  21 NOV 2026", font=font(BOLD, 15), fill=MUTED)

# circular inset: tanker on fire at sea
cx, cy, r = 862, 248, 104
inset = Image.new("RGB", (2 * r, 2 * r), (8, 42, 58))
di = ImageDraw.Draw(inset, "RGBA")
di.rectangle([0, 130, 208, 208], fill=(10, 55, 70))
# tanker hull
di.rectangle([28, 128, 180, 152], fill=(30, 30, 38))
di.rectangle([28, 118, 180, 128], fill=(120, 40, 40))
di.rectangle([120, 96, 150, 118], fill=(200, 200, 200))
# flames
for (fx, fy, fw, fh) in [(48, 78, 26, 44), (82, 62, 30, 60), (122, 80, 24, 40), (152, 92, 18, 30)]:
    di.polygon([(fx, fy + fh), (fx + fw // 2, fy), (fx + fw, fy + fh)], fill=ORANGE)
    di.polygon([(fx + 6, fy + fh), (fx + fw // 2, fy + 14), (fx + fw - 6, fy + fh)], fill=GOLD)
# smoke
for (sx, sy, sr) in [(70, 48, 12), (95, 34, 15), (122, 46, 11)]:
    di.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 130, 145))
mask = Image.new("L", (2 * r, 2 * r), 0)
dm = ImageDraw.Draw(mask); dm.ellipse([0, 0, 2 * r, 2 * r], fill=255)
img.paste(inset, (cx - r, cy - r), mask)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3)
d.text((cx, cy + r - 26), "KHASAB", font=font(BOLD, 15), fill=WHITE, anchor="ma")

# ---- Dot-matrix world map ----
mx, my, mw, mh = 28, 396, 968, 188
d.rounded_rectangle([mx, my, mx + mw, my + mh], radius=14, fill=PANEL2, outline=(42, 63, 102), width=1)
d.text((mx + 16, my + 10), "WHERE IT HAPPENED", font=font(BOLD, 17), fill=GOLD)
d.text((mx + mw - 16, my + 10), "PINS 1–7  •  NUMBERED ON THE MAP", font=font(BOLD, 14), fill=MUTED, anchor="ra")

def map_xy(lon, lat):
    x = mx + 14 + (lon + 180.0) / 360.0 * (mw - 28)
    y = my + 38 + (75.0 - lat) / 130.0 * (mh - 48)
    return x, y

LAND = [(-170, 15, -55, 72), (-80, -55, -35, 10), (-10, 36, 40, 70),
        (-18, -35, 50, 35), (40, 5, 180, 75), (110, -45, 155, -10)]
lon = -174
while lon <= 180:
    lat = -52
    while lat <= 74:
        if any(x0 <= lon <= x1 and y0 <= lat <= y1 for (x0, y0, x1, y1) in LAND):
            x, y = map_xy(lon, lat)
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(74, 111, 165))
        lat += 6
    lon += 6

PINS = [
    (1, 56.0, 26.5, RED, (0, 0)),
    (2, 30.3, 50.8, (255, 122, 0), (16, -8)),
    (3, 27.0, 60.0, (0, 180, 180), (-20, -12)),
    (4, 30.7, 36.9, (255, 196, 0), (12, 14)),
    (5, 106.0, -6.1, (180, 80, 200), (0, 0)),
    (6, -108.5, 25.6, (80, 180, 90), (0, 0)),
    (7, 6.3, 4.9, (255, 90, 120), (0, 0)),
]
for num, lon_, lat_, col, (dx, dy) in PINS:
    tx, ty = map_xy(lon_, lat_)
    px, py = tx + dx, ty + dy
    if dx or dy:
        d.line([tx, ty, px, py], fill=WHITE, width=1)
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=col, outline=WHITE, width=2)
    d.text((px, py - 1), str(num), font=font(BOLD, 14), fill=WHITE, anchor="mm")

# ---- Six secondary cards, 3 x 2 ----
CARDS = [
    (2, "UKRAINE  •  DYMER", "Drone collapses\nblock near Kyiv",
     "5-storey block hit overnight. 9 evacuated, 2 hurt. 14 unaccounted for, may be trapped — Zelenskyy.", ORANGE),
    (3, "BALTIC SEA", "Sparta II ablaze\nat sea",
     "Russian cargo ship hit by drones Sat. Crew of 16 evacuated; ship drifts into Finnish waters, still burning.", TEAL),
    (4, "COP31  •  ANTALYA", "Final deal put\nto a vote",
     "After 2 days overtime, a 10-page deal goes to a vote Sun — still no mention of “fossil fuels”.", GOLD),
    (5, "INDONESIA  •  SERANG", "Candy factory\nfire",
     "Fonusa Agung Mulia blaze Sat evening. 3 dead, 36 missing; 15 rescued alive.", (180, 80, 200)),
    (6, "MEXICO  •  SINALOA", "“Chapo Isidro”\ncaptured",
     "Army seizes Fausto Isidro Meza Flores in Guasave. 11 killed in gunfights; roadblocks, burning trucks.", (80, 180, 90)),
    (7, "NIGERIA  •  BAYELSA", "Funeral boat\ncapsizes",
     "Boat from Ayama to Ukubie capsizes Fri. At least 24 dead, 24 rescued; search goes on.", (255, 90, 120)),
]
cw, ch, gx, gy = 312, 186, 16, 14
for i, (num, tag, title, body, col) in enumerate(CARDS):
    x = 28 + (i % 3) * (cw + gx)
    y = 598 + (i // 3) * (ch + gy)
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=PANEL, outline=(42, 63, 102), width=1)
    d.ellipse([x + 14, y + 12, x + 44, y + 42], fill=col, outline=WHITE, width=1)
    d.text((x + 29, y + 19), str(num), font=font(BOLD, 18), fill=WHITE, anchor="ma")
    d.text((x + 54, y + 16), tag, font=font(BOLD, 15), fill=col)
    ty = y + 48
    for line in title.split("\n"):
        d.text((x + 14, ty), line, font=font(BOLD, 22), fill=WHITE); ty += 27
    by = ty + 6
    for line in wrap(body, 30):
        d.text((x + 14, by), line, font=font(REG, 16), fill=LIGHT); by += 21

d.text((28, 1002), "SOURCES: REUTERS  •  AP  •  BBC  •  AL JAZEERA  •  KYIV INDEPENDENT  •  XINHUA  •  ANADOLU  •  UKMTO",
       font=font(BOLD, 13), fill=MUTED)
d.rectangle([0, 1020, 1024, 1024], fill=GOLD)
img.save(OUT, "PNG", optimize=True)
print(OUT, os.path.getsize(OUT), img.size)
