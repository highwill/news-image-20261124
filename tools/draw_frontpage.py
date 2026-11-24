#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a newspaper front page, 1024x1024 PNG.

Facts come from the verified news brief of 24 Nov 2026 (see README.md).
Flat colours + shapes only, so the PNG stays well under 1 MiB.
Run: python3 tools/draw_frontpage.py  ->  writes entry.png next to this repo root.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (247, 243, 234)   # off-white newsprint
INK = (16, 16, 16)
RED = (160, 30, 30)
BLUE = (30, 60, 110)
GREY = (110, 110, 108)
LIGHT = (226, 220, 208)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MASTHEAD = font("DejaVuSerif-Bold.ttf", 104)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_LEAD = font("DejaVuSerif-Bold.ttf", 46)
F_DECK = font("DejaVuSerif.ttf", 23)
F_HEAD = font("DejaVuSerif-Bold.ttf", 25)
F_BODY = font("DejaVuSerif.ttf", 18)
F_SMALL = font("DejaVuSans.ttf", 17)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 17)
F_CAPTION = font("DejaVuSans.ttf", 16)
F_LABEL = font("DejaVuSans-Bold.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, leading, fill=INK):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def rule(draw, x0, y, x1, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- top thin rule + kicker ---------------------------------------------
rule(d, MARGIN, 26, W - MARGIN, 3)
d.text((MARGIN, 34), "WORLD NEWS", font=F_LABEL, fill=RED)
r = d.textlength("24 NOVEMBER 2026", font=F_LABEL)
d.text((W - MARGIN - r, 34), "24 NOVEMBER 2026", font=F_LABEL, fill=RED)

# ---- masthead ------------------------------------------------------------
d.text((W // 2, 56), "THE WORLD", font=F_MASTHEAD, fill=INK, anchor="ma")
rule(d, MARGIN, 178, W - MARGIN, 4)

# ---- date banner (very prominent) ----------------------------------------
d.rectangle([MARGIN, 190, W - MARGIN, 238], fill=INK)
d.text((W // 2, 214), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE,
       fill=(255, 255, 255), anchor="mm")

# ---- lead headline --------------------------------------------------------
y = 258
y = draw_wrapped(d, "TRUMP, XI AND PUTIN TO HOLD HISTORIC SUMMIT IN SHENZHEN",
                 F_LEAD, MARGIN, y, W - 2 * MARGIN, 54)
y += 4
y = draw_wrapped(d, "The three leaders will meet in Shenzhen in a first-of-its-kind "
                    "trilateral summit — the biggest story of the day.",
                 F_DECK, MARGIN, y, W - 2 * MARGIN, 30)
y += 10

# ---- lead picture: Shenzhen skyline + three flags --------------------------
pic_y0, pic_y1 = y, y + 84
d.rectangle([MARGIN, pic_y0, W - MARGIN, pic_y1], fill=(214, 226, 235))
# sun
d.ellipse([W - MARGIN - 100, pic_y0 + 8, W - MARGIN - 52, pic_y0 + 56],
          fill=(214, 120, 60))
# skyline silhouette
sky = [(MARGIN + 10, 65), (MARGIN + 60, 43), (MARGIN + 110, 73),
       (MARGIN + 170, 33), (MARGIN + 215, 55), (MARGIN + 280, 77),
       (MARGIN + 330, 40), (MARGIN + 400, 70), (MARGIN + 470, 48),
       (MARGIN + 540, 80), (MARGIN + 610, 37), (MARGIN + 680, 67),
       (MARGIN + 740, 50), (MARGIN + 820, 77), (MARGIN + 880, 58)]
for i, (bx, bh) in enumerate(sky):
    x0 = MARGIN + i * 62
    d.rectangle([x0, pic_y1 - bh, x0 + 46, pic_y1], fill=(52, 68, 92))
# flags row (US / China / Russia) on the skyline band
fw, fh, fy = 150, 34, pic_y1 - 40
fx = MARGIN + 24
# US flag
d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
for i in range(4):
    d.rectangle([fx, fy + i * 9, fx + fw, fy + i * 9 + 4], fill=(178, 34, 52))
d.rectangle([fx, fy, fx + 62, fy + 18], fill=(60, 59, 110))
for sx in (10, 26, 42):
    for sy in (5, 12):
        d.ellipse([fx + sx - 1, fy + sy - 1, fx + sx + 1, fy + sy + 1],
                  fill=(255, 255, 255))
# China flag
fx += fw + 24
d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
star(d, fx + 22, fy + 15, 10, (255, 222, 0))
for sx, sy in ((44, 8), (52, 14), (50, 24), (40, 26)):
    star(d, fx + sx, fy + sy, 4, (255, 222, 0))
# Russia flag
fx += fw + 24
d.rectangle([fx, fy, fx + fw, fy + 11], fill=(255, 255, 255))
d.rectangle([fx, fy + 11, fx + fw, fy + 23], fill=(0, 57, 166))
d.rectangle([fx, fy + 23, fx + fw, fy + fh], fill=(213, 0, 50))
d.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=1)

y = pic_y1 + 8
d.text((MARGIN, y), "Shenzhen will host the three leaders for the historic meeting.",
       font=F_CAPTION, fill=GREY)
y += 20
rule(d, MARGIN, y, W - MARGIN, 3)
y += 14

# ---- story grid: two columns, three rows (5 stories + Also today) --------
col_w = (W - 2 * MARGIN - 28) // 2
col_x = [MARGIN, MARGIN + col_w + 28]

stories = [
    ("WORLD", "FIRE AT BANTEN FACTORY KILLS AT LEAST 24",
     "Around 30 people are still missing after the Banten factory blaze. "
     "Rescue operations continue."),
    ("WORLD", "DRONE STRIKE HITS KYIV REGION",
     "Several people were killed or are missing in a Russian drone strike, "
     "President Zelenskyy said."),
    ("CLIMATE", "COP31 ENDS DIVIDED ON FOSSIL FUELS",
     "Antalya talks ended without agreement on stronger language to phase "
     "out fossil fuels."),
    ("SPORT", "VERSTAPPEN WINS IN LAS VEGAS",
     "Max Verstappen took victory at the 2026 Las Vegas Grand Prix."),
    ("INDIA – NEPAL", "MODI AND SHAH FLAG OFF SARYU-KAMALA EXPRESS",
     "Modi and Nepal PM Balendra Shah flagged off the train from "
     "Ayodhya to Janakpur Dham."),
]

grid_top = y
row_h = 126
for i, (label, head, deck) in enumerate(stories):
    cx = col_x[i % 2]
    cy = grid_top + (i // 2) * row_h
    d.text((cx, cy), label, font=F_LABEL, fill=RED)
    cy += 20
    cy = draw_wrapped(d, head, F_HEAD, cx, cy, col_w, 29)
    cy += 2
    draw_wrapped(d, deck, F_BODY, cx, cy, col_w, 22)
    if i % 2 == 0:
        d.line([(MARGIN + col_w + 14, grid_top + (i // 2) * row_h),
                (MARGIN + col_w + 14, grid_top + (i // 2) * row_h + row_h - 14)],
               fill=LIGHT, width=2)
for r in (1, 2):
    rule(d, MARGIN, grid_top + r * row_h - 8, W - MARGIN, 2, fill=LIGHT)

# ALSO TODAY cell (bottom right)
bx = col_x[1]
by = grid_top + 2 * row_h
d.text((bx, by), "ALSO TODAY", font=F_LABEL, fill=RED)
by += 20
also = [
    "Rishabh Pant scored 128 against New Zealand in the drawn Wellington Test.",
    "Ferrari unveiled the 296 Challenge Stradale and Evo at Finali Mondiali in Spain.",
    "Fourteen countries acknowledged the ICJ ruling of genocide against the Rohingya.",
]
for item in also:
    d.text((bx, by), "•", font=F_BODY, fill=RED)
    by = draw_wrapped(d, item, F_BODY, bx + 18, by, col_w - 18, 22)
    by += 2

# ---- footer ----------------------------------------------------------------
fy = H - 30
rule(d, MARGIN, fy, W - MARGIN, 2)
d.text((W // 2, fy + 8), "THE WORLD  —  TUESDAY, 24 NOVEMBER 2026",
       font=F_SMALL, fill=GREY, anchor="ma")

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "entry.png")
img.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes")
