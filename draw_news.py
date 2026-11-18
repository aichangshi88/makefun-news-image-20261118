#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page, 1024x1024 PNG.

Deterministic, stdlib + Pillow only, no network. Every story was checked
against reporting dated 18 Nov 2026 (Reuters / AP / Horizon / One Turn):
  - Trump lands in Shenzhen, Xi greets him; first Trump-Xi-Putin trilateral Thu
  - US strikes Qeshm Island; Iran drones hit Bahrain & Kuwait, ship in Hormuz
  - Ukraine strike collapses part of the Kerch bridge to Crimea
  - US loses measles-free status: 5,400+ cases, 10 deaths, after 26 years
  - Ebola in DR Congo more than doubles: 11,000+ cases, 5,400 deaths (UN)
  - Peltola wins Alaska Senate; Democrats reach 56 seats
Footer: Cyclone Xavier Cat 5 (Cook Islands), Russian An-12 crash, 19 dead,
S&P 500 -1.03%, Brent $92.47.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (18, 48, 86)
TEAL = (14, 90, 100)
GOLD = (201, 162, 39)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def panel(draw, x, y, w, h, tag, tagcolor):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=(255, 255, 255), outline=(200, 192, 172), width=2)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=tagcolor)
    draw.rectangle([x, y + 24, x + w, y + 34], fill=tagcolor)
    draw.text((x + 14, y + 6), tag, font=font(BOLD, 19), fill=(255, 255, 255))


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                           fill=(178, 34, 34))
    draw.rectangle([x, y, x + w * 0.4, y + h * 4 // 7], fill=(30, 60, 120))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    cx, cy = x + w * 0.22, y + h * 0.28
    for dx, dy, r in [(0, 0, 7), (18, -6, 3), (20, 4, 3), (14, 12, 3), (4, 12, 3)]:
        draw.regular_polygon((cx + dx, cy + dy, r), 5, fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def draw_lead_art(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(158, 196, 222))
    # sun
    draw.ellipse([x + w - 78, y + 14, x + w - 22, y + 70], fill=(255, 214, 90))
    # skyline
    base = y + h
    heights = [150, 210, 120, 240, 170, 260, 140, 190]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 4
        draw.rectangle([bx, base - hh, bx + bw - 8, base], fill=NAVY)
        for wy in range(base - hh + 12, base - 10, 22):
            for wx in range(bx + 8, bx + bw - 14, 18):
                draw.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 220, 120))
    # ground
    draw.rectangle([x, base - 14, x + w, base], fill=(30, 60, 40))
    # three flags on poles
    fx = x + 22
    for flag in (flag_us, flag_cn, flag_ru):
        draw.line([fx + 14, y + 18, fx + 14, y + 96], fill=INK, width=3)
        flag(draw, fx + 14, y + 22, 62, 40)
        fx += 108


def draw_gulf(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(10, 60, 80))
    # sky + missile
    draw.line([x + 18, y + 26, x + w - 30, y + 62], fill=(255, 200, 60), width=5)
    draw.ellipse([x + w - 44, y + 54, x + w - 16, y + 78], fill=(255, 120, 40))
    for dx, dy in [(0, 0), (16, 10), (-6, 14)]:
        draw.ellipse([x + w - 60 + dx, y + 30 + dy, x + w - 46 + dx, y + 44 + dy],
                     fill=(255, 255, 255))
    # sea
    draw.rectangle([x, y + h - 46, x + w, y + h], fill=(20, 110, 130))
    for wx in range(x + 8, x + w - 10, 26):
        draw.arc([wx, y + h - 40, wx + 22, y + h - 22], 180, 360,
                 fill=(255, 255, 255), width=3)
    # ship
    draw.polygon([(x + 22, y + h - 48), (x + w - 22, y + h - 48),
                  (x + w - 34, y + h - 22), (x + 34, y + h - 22)], fill=(40, 40, 40))
    draw.rectangle([x + w // 2 - 14, y + h - 74, x + w // 2 + 14, y + h - 48],
                   fill=(200, 200, 200))


def draw_bridge(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(210, 225, 235))
    # water
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(40, 110, 160))
    # towers + deck with a gap in the middle
    for tx in (x + 22, x + w - 42):
        draw.rectangle([tx, y + 18, tx + 20, y + h - 34], fill=NAVY)
    draw.rectangle([x + 6, y + 62, x + w // 2 - 14, y + 74], fill=(90, 90, 90))
    draw.rectangle([x + w // 2 + 14, y + 62, x + w - 6, y + 74], fill=(90, 90, 90))
    # fallen span sinking in the gap
    draw.polygon([(x + w // 2 - 16, y + 78), (x + w // 2 + 16, y + 70),
                  (x + w // 2 + 10, y + h - 30), (x + w // 2 - 22, y + h - 30)],
                 fill=(70, 70, 70))
    # blast star
    cx, cy = x + w // 2, y + 52
    for ang in range(0, 360, 45):
        import math
        ex, ey = cx + 26 * math.cos(math.radians(ang)), cy + 26 * math.sin(math.radians(ang))
        draw.line([cx, cy, ex, ey], fill=(255, 140, 0), width=5)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 200, 0))


def draw_virus(draw, x, y, w, h, color, spikes=12):
    import math
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 8
    for i in range(spikes):
        ang = 2 * math.pi * i / spikes
        x1, y1 = cx + (r - 12) * math.cos(ang), cy + (r - 12) * math.sin(ang)
        x2, y2 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        draw.line([x1, y1, x2, y2], fill=color, width=4)
        draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=color)
    draw.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], fill=color)
    for dx, dy in [(-10, -7), (8, -10), (10, 9), (-8, 10), (0, 0)]:
        draw.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4],
                     fill=(255, 255, 255))


def draw_ballot(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=(230, 238, 250))
    # star
    draw.regular_polygon((x + w // 2, y + 22, 20), 5, fill=GOLD)
    # ballot box
    draw.rectangle([x + 18, y + 48, x + w - 18, y + h - 6], fill=NAVY)
    draw.rectangle([x + 12, y + 42, x + w - 12, y + 52], fill=(30, 60, 120))
    draw.rectangle([x + w // 2 - 16, y + 45, x + w // 2 + 16, y + 49], fill=(255, 255, 255))
    # paper going in
    draw.polygon([(x + w // 2 - 12, y + 28), (x + w // 2 + 12, y + 28),
                  (x + w // 2 + 9, y + 46), (x + w // 2 - 9, y + 46)],
                 fill=(255, 255, 255), outline=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    # ---- masthead ----
    d.text((M, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 26), fill=RED)
    d.line([M, 58, W - M, 58], fill=INK, width=3)
    d.text((M, 66), "WEDNESDAY, 18 NOVEMBER 2026",
           font=font(SERIFB, 50), fill=INK)
    d.rectangle([M, 138, W - M, 146], fill=RED)

    # ---- lead story ----
    lx, ly, lw, lh = M, 158, W - 2 * M, 296
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                        fill=(255, 255, 255), outline=(200, 192, 172), width=2)
    d.text((lx + 20, ly + 14), "SHENZHEN  •  APEC SUMMIT", font=font(BOLD, 20), fill=RED)
    draw_lines(d, ["TRUMP LANDS IN", "SHENZHEN"], lx + 20, ly + 48,
               font(BOLD, 52), leading=58)
    sub = ("Xi greets him at the airport. The first-ever "
           "Trump–Xi–Putin trilateral is set for Thursday.")
    draw_lines(d, wrap(d, sub, font(REG, 23), 540), lx + 20, ly + 178,
               font(REG, 23), leading=30)
    d.text((lx + 20, ly + 252), "Xi and Putin met for the 50th time earlier in the day.",
           font=font(REG, 19), fill=(90, 90, 90))
    draw_lead_art(d, lx + 580, ly + 14, 360, 268)

    # ---- row 2: Gulf + Crimea ----
    y2, h2 = 470, 222
    w2 = (W - 2 * M - 16) // 2
    # Gulf
    panel(d, M, y2, w2, h2, "GULF WAR WIDENS", (140, 30, 30))
    draw_lines(d, ["US STRIKES QESHM;", "IRAN HITS BAHRAIN", "& KUWAIT"],
               M + 16, y2 + 48, font(BOLD, 26), leading=32)
    draw_lines(d, wrap(d, "Drones hit US bases; ship struck in Hormuz.",
                       font(REG, 20), 310), M + 16, y2 + 152, font(REG, 20), leading=26)
    draw_gulf(d, M + w2 - 132, y2 + 46, 116, 160)
    # Crimea
    x2 = M + w2 + 16
    panel(d, x2, y2, w2, h2, "UKRAINE  •  CRIMEA", NAVY)
    draw_lines(d, ["KERCH BRIDGE", "SPAN COLLAPSES"],
               x2 + 16, y2 + 48, font(BOLD, 29), leading=35)
    draw_lines(d, wrap(d, "Ukrainian strike hits the bridge to Crimea for a second day; traffic halted.",
                       font(REG, 20), 310), x2 + 16, y2 + 132, font(REG, 20), leading=26)
    draw_bridge(d, x2 + w2 - 132, y2 + 46, 116, 160)

    # ---- row 3: Measles, Ebola, Alaska ----
    y3, h3 = 708, 222
    w3 = (W - 2 * M - 32) // 3
    panels = [
        ("USA  •  HEALTH", RED, "MEASLES-FREE\nSTATUS LOST",
         "5,400+ cases, 10 deaths — first loss in 26 years.",
         lambda dd, xx, yy, ww, hh: draw_virus(dd, xx, yy, ww, hh, (200, 40, 40))),
        ("CONGO  •  HEALTH", (90, 30, 90), "EBOLA CASES\nDOUBLE",
         "11,000+ cases, 5,400 deaths, the UN says.",
         lambda dd, xx, yy, ww, hh: draw_virus(dd, xx, yy, ww, hh, (120, 30, 120))),
        ("USA  •  POLITICS", NAVY, "DEMOCRATS\nWIN ALASKA",
         "Peltola beats Sullivan; Democrats take 56 seats, 56–44.",
         draw_ballot),
    ]
    for i, (tag, color, head, sub, art) in enumerate(panels):
        x = M + i * (w3 + 16)
        panel(d, x, y3, w3, h3, tag, color)
        draw_lines(d, wrap(d, head.replace("\n", " "), font(BOLD, 24), w3 - 112),
                   x + 14, y3 + 46, font(BOLD, 24), leading=29)
        draw_lines(d, wrap(d, sub, font(REG, 19), w3 - 28), x + 14, y3 + 138,
                   font(REG, 19), leading=24)
        art(d, x + w3 - 100, y3 + 42, 88, 84)

    # ---- footer ----
    fy = 946
    d.rectangle([M, fy, W - M, fy + 56], fill=INK)
    foot = ("ALSO TODAY:  Cyclone Xavier, Category 5, hits the Cook Islands   •   "
            "Russian military plane crashes in Siberia, 19 dead   •   "
            "Markets: S&P 500 −1.03%, Brent $92.47")
    draw_lines(d, wrap(d, foot, font(BOLD, 18), W - 2 * M - 24), M + 12, fy + 8,
               font(BOLD, 18), fill=(255, 255, 255), leading=24)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
