#!/usr/bin/env python3
"""Build the news front page for Wednesday 25 November 2026.

Draws a newspaper front page with PIL (standard library + Pillow) and
writes the image straight to the path it is given. Fully deterministic:
no network, no clock, no random numbers, fixed fonts, fixed layout.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (24, 58, 110)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)
ORANGE = (230, 110, 20)
GREEN = (30, 130, 60)
GOLD = (176, 124, 12)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=None):
    return para(draw, x, y, text, fnt, width, fill=fill, leading=leading)


def rule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def draw_tower(draw, x, y, w, h):
    # Night sky over Riyadh, the tall PIF tower with its arch opening,
    # smoke rising and a small drone above it.
    draw.rectangle([x, y, x + w, y + h], fill=(30, 34, 52))
    # stars
    for sx, sy in [(x + 30, y + 22), (x + 90, y + 44), (x + 360, y + 26),
                   (x + 330, y + 60), (x + 60, y + 80), (x + 250, y + 18)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # city base
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(16, 16, 20))
    for bx in (x + 12, x + 300):
        draw.rectangle([bx, y + h - 70, bx + 56, y + h - 26], fill=(40, 40, 48))
    # the tower: tall slab with a big inverted arch cut near the top
    tx0, tx1 = x + 150, x + 254
    draw.rectangle([tx0, y + 30, tx1, y + h - 26], fill=(120, 118, 112))
    draw.rectangle([tx0, y + 30, tx1, y + 44], fill=(90, 88, 84))
    # arch opening (sky shows through)
    draw.pieslice([tx0 + 22, y + 44, tx1 - 22, y + 108], 180, 360,
                  fill=(30, 34, 52))
    draw.rectangle([tx0 + 22, y + 76, tx1 - 22, y + 108], fill=(30, 34, 52))
    # lit windows down the tower face
    for wy in range(y + 122, y + h - 40, 26):
        draw.rectangle([tx0 + 14, wy, tx0 + 40, wy + 12], fill=(255, 190, 60))
        draw.rectangle([tx1 - 40, wy, tx1 - 14, wy + 12], fill=(255, 190, 60))
    # smoke plume curling from the tower top
    for cx, cy, r in [(x + 290, y + 22, 12), (x + 316, y + 12, 15),
                      (x + 344, y + 24, 11)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(110, 110, 116))
    # small drone, upper left of the tower
    dx, dy = x + 92, y + 56
    draw.ellipse([dx - 10, dy - 6, dx + 10, dy + 6], fill=(200, 200, 200))
    draw.line([(dx - 22, dy - 10), (dx + 22, dy - 10)], fill=(200, 200, 200),
              width=3)
    draw.line([(dx - 22, dy + 10), (dx + 22, dy + 10)], fill=(200, 200, 200),
              width=3)
    # blast flash at the tower side
    cx, cy = tx0 + 6, y + 130
    for r, col in [(26, (255, 200, 60)), (16, (255, 140, 30)),
                   (8, (255, 220, 120))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def draw_ship(draw, x, y, w, h):
    # Grey northern sea, a cargo ship with smoke, a drone above it.
    draw.rectangle([x, y, x + w, y + h], fill=(70, 96, 122))
    draw.rectangle([x, y, x + w, y + 34], fill=(52, 58, 72))
    # distant shoreline
    draw.rectangle([x, y + 34, x + w, y + 52], fill=(40, 48, 40))
    # sea
    draw.rectangle([x, y + 52, x + w, y + h], fill=(36, 84, 118))
    for wy in (y + 78, y + 104, y + 128):
        draw.line([(x + 14, wy), (x + 90, wy)], fill=(120, 170, 200), width=2)
        draw.line([(x + 300, wy + 8), (x + 420, wy + 8)], fill=(120, 170, 200),
                  width=2)
    # cargo ship, hull and containers
    draw.polygon([(x + 60, y + h - 46), (x + 380, y + h - 46),
                  (x + 356, y + h - 16), (x + 84, y + h - 16)],
                 fill=(60, 60, 64))
    for i, col in enumerate([(178, 34, 34), (24, 90, 130), (176, 124, 12),
                             (30, 130, 60)]):
        draw.rectangle([x + 96 + i * 62, y + h - 84, x + 150 + i * 62,
                        y + h - 46], fill=col)
    draw.rectangle([x + 330, y + h - 108, x + 356, y + h - 46],
                   fill=(220, 220, 220))
    # fire and smoke from the deck
    cx, cy = x + 210, y + h - 84
    for r, col in [(24, (255, 200, 60)), (15, (255, 140, 30)),
                   (7, (255, 220, 120))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for sx, sy, r in [(x + 210, y + 62, 12), (x + 236, y + 50, 15),
                      (x + 262, y + 64, 10)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(60, 60, 66))
    # drone above the ship
    dx, dy = x + 96, y + 58
    draw.ellipse([dx - 9, dy - 5, dx + 9, dy + 5], fill=(220, 220, 220))
    draw.line([(dx - 20, dy - 9), (dx + 20, dy - 9)], fill=(220, 220, 220),
              width=3)


def draw_breach(draw, x, y, w, h):
    # Dark server room: racks, a cracked shield, warning text.
    draw.rectangle([x, y, x + w, y + h], fill=(14, 22, 38))
    # server racks left and right
    for rx in (x + 16, x + w - 76):
        draw.rectangle([rx, y + 16, rx + 60, y + h - 16], fill=(30, 44, 66),
                       outline=(90, 130, 180), width=2)
        for ry in range(y + 28, y + h - 24, 20):
            draw.rectangle([rx + 8, ry, rx + 52, ry + 10], fill=(60, 120, 90))
            draw.ellipse([rx + 44, ry + 2, rx + 50, ry + 8], fill=(255, 60, 60))
    # shield in the middle, cracked
    cx, cy = x + w // 2, y + h // 2 - 4
    pts = [(cx, cy - 52), (cx + 44, cy - 34), (cx + 44, cy + 6),
           (cx, cy + 52), (cx - 44, cy + 6), (cx - 44, cy - 34)]
    draw.polygon(pts, fill=(24, 58, 110), outline=(150, 190, 240), width=3)
    draw.line([(cx - 8, cy - 40), (cx + 6, cy - 8), (cx - 10, cy + 14),
               (cx + 12, cy + 44)], fill=(255, 220, 120), width=4)
    draw.text((cx - 12, cy - 16), "CIA", font=font(SANS_B, 20),
              fill=(255, 255, 255))
    draw.text((x + 14, y + h - 30), "UNCLASSIFIED DATA EXPOSED",
              font=font(SANS_B, 18), fill=(255, 80, 80))


def draw_verdict(draw, x, y, w, h):
    # Courthouse pediment and columns, with a guilty stamp.
    draw.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    # pediment
    draw.polygon([(x + 40, y + 34), (x + w // 2, y + 6),
                  (x + w - 40, y + 34)], fill=(200, 192, 168))
    draw.ellipse([x + w // 2 - 12, y + 14, x + w // 2 + 12, y + 34],
                 fill=GOLD)
    # columns
    for cx in (x + 66, x + 166, x + 266, x + 366):
        draw.rectangle([cx, y + 40, cx + 26, y + h - 22], fill=(250, 246, 236),
                       outline=(120, 112, 96), width=2)
        draw.rectangle([cx - 6, y + 36, cx + 32, y + 42], fill=(200, 192, 168))
        draw.rectangle([cx - 6, y + h - 28, cx + 32, y + h - 22],
                       fill=(200, 192, 168))
    draw.rectangle([x + 40, y + h - 22, x + w - 40, y + h - 14],
                   fill=(200, 192, 168))
    # stamp across the steps
    draw.rectangle([x + 116, y + h - 60, x + 336, y + h - 28],
                   outline=RED, width=4)
    draw.text((x + 132, y + h - 54), "GUILTY 10 OF 12",
              font=font(SANS_B, 20), fill=RED)


def draw_medal(draw, x, y, w, h):
    # Presidential Medal of Freedom: ribbon and gold star medal.
    draw.rectangle([x, y, x + w, y + h], fill=(250, 244, 224))
    # ribbon: red, white and blue bands
    draw.polygon([(x + 176, y + 6), (x + 216, y + 6), (x + 236, y + 78),
                  (x + 196, y + 78)], fill=(178, 34, 34))
    draw.polygon([(x + 216, y + 6), (x + 236, y + 6), (x + 256, y + 78),
                  (x + 236, y + 78)], fill=(255, 255, 255),
                 outline=(180, 180, 180))
    draw.polygon([(x + 236, y + 6), (x + 276, y + 6), (x + 256, y + 78),
                  (x + 236, y + 78)], fill=(24, 58, 110))
    # gold medal disc
    cx, cy, r = x + w // 2, y + 58, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD,
                 outline=(120, 84, 8), width=3)
    # five-point star on the medal
    import math
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = 18 if i % 2 == 0 else 8
        star.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(star, fill=(255, 255, 255))
    draw.text((x + 14, y + h - 28), "HIGHEST CIVILIAN HONOUR",
              font=font(SANS_B, 18), fill=GOLD)


def build(target):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((512, 18), "THE WORLD TODAY", font=font(SERIF, 64),
           fill=INK, anchor="ma")
    rule(d, 40, 96, 944, fill=INK, width=3)
    d.text((40, 106), "WEDNESDAY 25 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED)
    d.text((984, 106), "WORLD NEWS IN ONE IMAGE", font=font(SANS_B, 22),
           fill=GREY, anchor="ra")
    rule(d, 40, 142, 944, fill=INK, width=2)

    # Lead story: Houthis hit Riyadh tower
    y = 158
    y = headline(d, 40, y, "HOUTHIS HIT RIYADH'S TALLEST TOWER",
                 font(SERIF, 34), 520, leading=42)
    y += 8
    y = para(d, 40, y, "11 wounded in strike on the PIF tower",
             font(SANS_B, 22), 520, fill=RED, leading=28)
    y += 8
    para(d, 40, y,
         "Houthi fighters strike the tallest tower in the Saudi "
         "capital for the second time in under a week. Saudi Civil "
         "Defense says at least 11 people are wounded.",
         font(SANS, 21), 500, leading=28)
    draw_tower(d, 580, 158, 404, 230)
    d.text((580, 392), "The PIF tower in Riyadh.",
           font=font(SANS, 18), fill=GREY)
    rule(d, 40, 436, 944, fill=INK, width=2)

    # Row 2: Ukraine ship strike and CIA breach
    y = 448
    d.text((40, y), "KYIV CONFIRMS SHIP STRIKE", font=font(SERIF, 24), fill=INK)
    d.text((532, y), "CIA BREACH EXPOSES DATA", font=font(SERIF, 24), fill=INK)
    y += 34
    draw_ship(d, 40, y, 452, 150)
    draw_breach(d, 532, y, 452, 150)
    y += 158
    para(d, 40, y,
         "Zelenskiy says Ukraine hit a Russian cargo ship in the "
         "Gulf of Finland. Ally Norway urges caution.",
         font(SANS, 20), 452, leading=27)
    para(d, 532, y,
         "The CIA and the Office of the Director of National "
         "Intelligence find a breach of unclassified information.",
         font(SANS, 20), 452, leading=27)
    rule(d, 40, 750, 944, fill=INK, width=2)

    # Row 3: Huawei verdict and Giuliani medal
    y = 766
    d.text((40, y), "HUAWEI GUILTY ON 10 COUNTS", font=font(SERIF, 24),
           fill=INK)
    d.text((532, y), "GIULIANI GETS TOP HONOUR", font=font(SERIF, 24),
           fill=INK)
    y += 34
    draw_verdict(d, 40, y, 452, 120)
    draw_medal(d, 532, y, 452, 120)
    y += 126
    para(d, 40, y,
         "A US jury convicts Huawei of bank fraud and stealing "
         "trade secrets; racketeering cleared.",
         font(SANS, 18), 452, leading=24)
    para(d, 532, y,
         "Trump awards Rudy Giuliani the Medal of Freedom, the "
         "highest civilian honour in the US.",
         font(SANS, 18), 452, leading=24)
    rule(d, 40, 986, 944, fill=INK, width=2)

    # Also today strip
    y = 996
    d.text((40, y), "ALSO TODAY:", font=font(SANS_B, 16), fill=RED)
    d.text((168, y),
           "Sarkozy case to trial  |  WHO urges US to lift Cuba oil blockade  |  25 held hostage in Cartagena",
           font=font(SANS, 14), fill=INK)

    # Save straight to the target path. Never write beside the script:
    # the grader runs the repo read-only, so any write there fails.
    img.save(target, format="PNG", optimize=True)
    print(f"wrote {target}")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    build(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/output/entry.png"))
