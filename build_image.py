#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: a newspaper front page for
Sunday, 22 November 2026. Output: entry.png, 1024x1024, PNG.
All art is drawn with PIL primitives; no photos, no external assets.
Run: python3 build_image.py  (writes entry.png beside this file)
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (20, 20, 20)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GREY = (90, 86, 76)
LIGHT = (233, 227, 210)
ORANGE = (214, 110, 30)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # no oblique shipped; regular


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading, color=INK):
    return para(draw, x, y, text, fnt, max_w, leading, color)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 19)
    draw.text((x, y), text, font=f, fill=color)
    return y + 26


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def box(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---- icons (simple drawn shapes) ----
def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=3)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=BLUE, width=3)
    d.ellipse([cx - 12, cy - r - 14, cx + 12, cy - r + 10], fill=(232, 180, 60),
              outline=ORANGE, width=2)


def ship(d, x, y, s):
    # hull + mast + flag, s = scale
    d.polygon([(x, y), (x + 110 * s, y), (x + 95 * s, y + 28 * s),
               (x + 15 * s, y + 28 * s)], fill=BLUE)
    d.line([(x + 55 * s, y), (x + 55 * s, y - 52 * s)], fill=INK, width=4)
    d.polygon([(x + 55 * s, y - 52 * s), (x + 88 * s, y - 42 * s),
               (x + 55 * s, y - 32 * s)], fill=RED)
    for wx in (28, 52, 76):
        d.line([(x + wx * s, y - 30 * s), (x + wx * s, y - 52 * s)],
               fill=INK, width=3)


def flame(d, x, y, s):
    d.polygon([(x, y + 60 * s), (x + 18 * s, y + 18 * s), (x + 34 * s, y + 38 * s),
               (x + 44 * s, y), (x + 58 * s, y + 34 * s), (x + 76 * s, y + 14 * s),
               (x + 84 * s, y + 60 * s)], fill=ORANGE, outline=RED, width=3)
    d.polygon([(x + 30 * s, y + 60 * s), (x + 42 * s, y + 34 * s),
               (x + 56 * s, y + 60 * s)], fill=(242, 201, 76))


def ballot(d, x, y, s):
    d.rectangle([x, y, x + 84 * s, y + 62 * s], outline=INK, width=4, fill=(255, 255, 255))
    d.rectangle([x + 28 * s, y - 14 * s, x + 56 * s, y + 6 * s], outline=INK, width=3,
                fill=LIGHT)
    d.line([(x + 14 * s, y + 34 * s), (x + 34 * s, y + 50 * s), (x + 72 * s, y + 14 * s)],
           fill=RED, width=6)


def star(d, cx, cy, r):
    import math
    pts = []
    for k in range(10):
        ang = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, outline=RED, width=3, fill=(242, 201, 76))


def chart(d, x, y, s):
    d.line([(x, y + 56 * s), (x + 96 * s, y + 56 * s)], fill=INK, width=3)
    d.line([(x, y + 56 * s), (x, y)], fill=INK, width=3)
    d.line([(x + 6 * s, y + 14 * s), (x + 30 * s, y + 26 * s), (x + 52 * s, y + 8 * s),
            (x + 74 * s, y + 34 * s), (x + 92 * s, y + 48 * s)], fill=RED, width=5)


def ball(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4, fill=(255, 255, 255))
    d.polygon([(cx, cy - 12), (cx + 12, cy - 4), (cx + 7, cy + 11),
               (cx - 7, cy + 11), (cx - 12, cy - 4)], fill=INK)
    for ang in (90, 210, 330):
        import math
        a = math.radians(ang)
        d.line([(cx, cy), (cx + int(r * 0.95 * math.cos(a)), cy - int(r * 0.95 * math.sin(a)))],
               fill=INK, width=3)


def flag(d, x, y, s):
    d.line([(x, y), (x, y + 62 * s)], fill=INK, width=4)
    d.polygon([(x, y), (x + 62 * s, y + 10 * s), (x, y + 24 * s)], fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=INK, width=1)

    # ---- masthead ----
    f_title = font(SERIF_B, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 34), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 36)
    date = "SUNDAY, 22 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 106), date, font=f_date, fill=RED)
    f_sub = font(SANS_I, 20)
    sub = "One day's world news — from Antalya to Anfield"
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw) / 2, 150), sub, font=f_sub, fill=GREY)
    rule(d, 36, 182, W - 36, 4)
    rule(d, 36, 189, W - 36, 1)

    # ---- lead: COP31 ----
    y = 206
    y = kicker(d, 40, y, "CLIMATE  •  LEAD STORY")
    f_h = font(SERIF_B, 34)
    y = headline(d, 40, y, "Climate talks collapse: no deal at COP31", f_h, 660, 40)
    f_b = font(SANS, 20)
    y = para(d, 40, y + 6,
             "The UN summit in Antalya, Turkey, ended on Sunday with no "
             "agreement, after two days of overtime. The EU rejected a draft "
             "that made no mention of fossil fuels.",
             f_b, 660, 26)
    globe(d, 850, 280, 62)
    d.text((782, 350), "Antalya, Turkey", font=font(SANS_I, 17), fill=GREY)

    rule(d, 36, 402, W - 36, 2)

    # ---- row 2: Mexico | Libya ----
    def two_col(y0, y1, left, right):
        mid = W // 2
        d.line([(mid, y0 + 4), (mid, y1 - 4)], fill=INK, width=2)
        for x0, x1, story in ((40, mid - 18, left), (mid + 18, W - 40, right)):
            yy = kicker(d, x0, y0, story["kick"])
            yy = headline(d, x0, yy, story["head"], font(SERIF_B, 25), x1 - x0 - 96, 30)
            yy = para(d, x0, yy + 4, story["body"], font(SANS, 18), x1 - x0 - 96, 24)
            story["icon"](d, x1 - 88, y0 + 8, 0.8)

    two_col(416, 588,
            {"kick": "MEXICO",
             "head": "Cartel boss 'El Chapo Isidro' captured",
             "body": "Mexican forces seized Fausto Isidro Meza Flores in "
                     "Sinaloa. Eleven were killed, four of them soldiers.",
             "icon": lambda dd, x, y, s: star(dd, x + 40, y + 34, 34)},
            {"kick": "WAR AT SEA",
             "head": "Drones 'hit Russian warship off Libya'",
             "body": "Suspected Ukrainian sea drones struck a Russian "
                     "warship at Benghazi, officials said; unconfirmed.",
             "icon": lambda dd, x, y, s: ship(dd, x, y + 52, s)})

    rule(d, 36, 600, W - 36, 2)

    # ---- row 3: Indonesia | Israel ----
    two_col(614, 786,
            {"kick": "INDONESIA",
             "head": "Factory fire kills 3; dozens missing",
             "body": "A blaze at a candy factory in Cikande killed three "
                     "workers. Rescuers searched for dozens still missing.",
             "icon": lambda dd, x, y, s: flame(dd, x, y, s)},
            {"kick": "ISRAEL",
             "head": "Coalition talks end with no deal",
             "body": "Netanyahu and Eisenkot ended talks with no deal. "
                     "Eisenkot condemned settler arson in the West Bank.",
             "icon": lambda dd, x, y, s: ballot(dd, x, y, s)})

    rule(d, 36, 792, W - 36, 2)

    # ---- row 4: Markets | Sport | Nepal ----
    cols = [
        ("MARKETS", "Asian states step in as AI sell-off eases",
         "After a sharp sell-off left the S&P 500 in correction, Asian "
         "governments moved to steady markets.",
         lambda dd, x, y, s: chart(dd, x + 14, y + 6, 0.3)),
        ("SPORT", "Liverpool 4–0 Manchester United",
         "Liverpool thrashed Manchester United 4–0 at Anfield in the "
         "Premier League on Sunday.",
         lambda dd, x, y, s: ball(dd, x + 16, y + 10, 12)),
        ("NEPAL", "Nepal PM begins first visit to India",
         "Balendra Shah arrived in Delhi on Sunday for his first official "
         "visit, with energy and links on the agenda.",
         lambda dd, x, y, s: flag(dd, x + 16, y + 4, 0.3)),
    ]
    cw = (W - 72 - 40) / 3
    for i, (kick, head, body, icon) in enumerate(cols):
        x0 = 40 + i * (cw + 20)
        x1 = x0 + cw
        if i:
            d.line([(x0 - 10, 812), (x0 - 10, 958)], fill=INK, width=2)
        yy = kicker(d, int(x0), 806, kick)
        yy = headline(d, int(x0), yy, head, font(SERIF_B, 21), int(x1 - x0), 24)
        yy = para(d, int(x0), yy + 3, body, font(SANS, 16), int(x1 - x0), 20)
        icon(d, int(x1 - 52), 806, 0.7)

    # ---- footer ----
    rule(d, 36, 972, W - 36, 1)
    f_f = font(SANS, 15)
    foot = "Reported 22 Nov 2026  •  AP  •  AFP  •  Reuters  •  The Hindu"
    tw = d.textlength(foot, font=f_f)
    d.text(((W - tw) / 2, 980), foot, font=f_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
