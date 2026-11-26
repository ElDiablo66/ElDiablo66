"""Writes the profile images: python tools/build_assets.py assets

Wording that appears as lettering lives in make_lettering.py (run that first
when a word changes). Colours and layout are here.
"""
import json, math, os, random, sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "lettering.json"), encoding="utf-8") as fh:
    LETTERS = json.load(fh)

NIGHT = "#150a33"
INK = "#12062a"
PINK = "#ff4f9a"
ORANGE = "#ff8a4c"
GOLD = "#ffc857"
CYAN = "#5fd8ff"
BLUSH = "#ffe3f0"


def save(name, text):
    with open(os.path.join(out, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def word(key, size, x, y, anchor="start", skew=0, attrs=""):
    """One lettering path. x, y is the baseline point; size is the font size in px."""
    g = LETTERS[key]
    k = size / 1000
    w = g["w"] * k
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    sk = f" skewX({skew})" if skew else ""
    return f'<path transform="translate({x:.1f} {y:.1f}){sk} scale({k:.4f})" d="{g["d"]}" {attrs}/>'


def width(key, size):
    return LETTERS[key]["w"] * size / 1000


def quad(p0, p1, p2, t):
    a = (1 - t) ** 2
    b = 2 * (1 - t) * t
    c = t * t
    return a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1]


def palm(x, base, h, lean, s, rnd, fill=INK):
    """Palm silhouette: a curved trunk and fronds with hanging leaflets."""
    cx, cy = x + lean, base - h
    parts = [
        f'<path d="M{x - 6 * s:.1f} {base}Q{x + lean * 0.15 - 4 * s:.1f} {base - h * 0.55:.1f} {cx - 3 * s:.1f} {cy:.1f}'
        f'L{cx + 3 * s:.1f} {cy:.1f}Q{x + lean * 0.15 + 5 * s:.1f} {base - h * 0.55:.1f} {x + 7 * s:.1f} {base}Z"/>'
    ]
    for a in (-28, 4, 34, 62, 90, 118, 146, 176, 208):
        ang = math.radians(a + rnd.uniform(-7, 7))
        L = (88 + rnd.uniform(-12, 14)) * s
        dx, dy = math.cos(ang), math.sin(ang)
        tip = (cx + L * dx, cy - L * dy * 0.7 + L * 0.34)
        c1 = (cx + L * 0.5 * dx, cy - L * dy * 0.7 - L * 0.26)
        c2 = (c1[0], c1[1] + L * 0.2)
        d = f"M{cx:.1f} {cy:.1f}Q{c1[0]:.1f} {c1[1]:.1f} {tip[0]:.1f} {tip[1]:.1f}Q{c2[0]:.1f} {c2[1]:.1f} {cx:.1f} {cy:.1f}Z"
        t = 0.22
        while t < 0.97:
            px, py = quad((cx, cy), c1, tip, t)
            ln = L * 0.2 * (1 - abs(t - 0.55))
            sway = (1 if dx >= 0 else -1) * ln * 0.3
            d += f"M{px - 2.2 * s:.1f} {py:.1f}L{px + sway:.1f} {py + ln:.1f}L{px + 2.6 * s:.1f} {py:.1f}Z"
            t += 0.075
        parts.append(f'<path d="{d}"/>')
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy + 3 * s:.1f}" r="{6 * s:.1f}"/>')
    return f'<g fill="{fill}">{"".join(parts)}</g>'


# ---------- banner ----------
W, H, HZ = 1200, 420, 318  # HZ is the horizon line
rnd = random.Random(66)

stars = "".join(
    f'<circle class="tw" cx="{rnd.uniform(20, 1180):.0f}" cy="{rnd.uniform(14, 150):.0f}" r="{rnd.choice((0.8, 1, 1.3))}" '
    f'fill="#fff" opacity="{rnd.uniform(0.35, 0.9):.2f}" style="animation-delay:{-rnd.uniform(0, 5):.1f}s"/>'
    for _ in range(46)
)

clouds = ""
for cx, cy, rx, ry, col, op in (
    (300, 142, 250, 9, "#ff8fb8", 0.30), (860, 118, 300, 8, "#b05ad6", 0.32), (560, 186, 330, 7, "#ffb089", 0.34),
    (140, 222, 240, 7, "#ff7aa8", 0.36), (1010, 236, 260, 8, "#ff9a6b", 0.36), (640, 262, 420, 6, "#ffd08a", 0.38),
    (360, 288, 300, 5, "#ffe2a6", 0.34), (930, 296, 260, 4, "#ffd9a0", 0.32),
):
    clouds += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{op}"/>'


def skyline(seed, top, low, colour, lights):
    """Row of towers. Low in the middle so the sun shows, taller at the sides."""
    r = random.Random(seed)
    shapes, wins = "", ""
    x = -10
    while x < W + 10:
        w = r.randint(20, 54)
        d = abs(x + w / 2 - 600)
        f = min(1, max(0, (d - 150) / 300))
        h = low + (top - low) * f * r.uniform(0.45, 1) + r.uniform(0, 10)
        y = HZ - h
        shapes += f'<rect x="{x}" y="{y:.0f}" width="{w}" height="{h + 2:.0f}"/>'
        if h > 46 and r.random() < 0.5:  # setback floor and a mast
            shapes += f'<rect x="{x + w * 0.25:.0f}" y="{y - 12:.0f}" width="{w * 0.5:.0f}" height="13"/>'
            if r.random() < 0.6:
                shapes += f'<rect x="{x + w * 0.5 - 1:.0f}" y="{y - 34:.0f}" width="2" height="24"/>'
        if lights and h > 30:
            wy = y + 7
            while wy < HZ - 8:
                wx = x + 5
                while wx < x + w - 6:
                    if r.random() < 0.3:
                        col = r.choice((GOLD, GOLD, "#ff9ccb", CYAN))
                        wins += f'<rect x="{wx}" y="{wy:.0f}" width="3" height="4" fill="{col}" opacity="{r.uniform(0.5, 0.95):.2f}"/>'
                    wx += 7
                wy += 9
        x += w + r.choice((0, 0, 2, 6))
    return f'<g fill="{colour}">{shapes}</g>{wins}'


reflect = ""
for i in range(11):
    y = HZ + 7 + i * 9
    wdt = max(16, 250 - i * 19 + rnd.uniform(-26, 26))
    reflect += (
        f'<rect class="sh" x="{600 - wdt / 2 + rnd.uniform(-10, 10):.0f}" y="{y}" width="{wdt:.0f}" height="3" rx="1.5" '
        f'fill="{GOLD if i < 4 else ORANGE}" opacity="{0.85 - i * 0.055:.2f}" style="animation-delay:{-rnd.uniform(0, 4):.1f}s"/>'
    )
for _ in range(38):
    x = rnd.choice((rnd.uniform(20, 400), rnd.uniform(800, 1180)))
    reflect += (
        f'<rect class="sh" x="{x:.0f}" y="{rnd.uniform(HZ + 6, H - 40):.0f}" width="{rnd.uniform(10, 46):.0f}" height="2" rx="1" '
        f'fill="{rnd.choice((PINK, PINK, CYAN, GOLD))}" opacity="{rnd.uniform(0.2, 0.5):.2f}" style="animation-delay:{-rnd.uniform(0, 4):.1f}s"/>'
    )

palms = (
    palm(96, H + 6, 262, 34, 1.25, rnd) + palm(196, H + 6, 168, -22, 0.9, rnd) + palm(22, H + 6, 150, 16, 0.8, rnd)
    + palm(1098, H + 6, 276, -40, 1.3, rnd) + palm(1004, H + 6, 176, 24, 0.92, rnd) + palm(1180, H + 6, 140, -12, 0.78, rnd)
)

TS, TY = 176, 216  # title size and baseline
tk = TS / 1000
title_x = 600 - width("title", TS) / 2 - 8
title = (
    word("title", TS, title_x + 7, TY + 8, skew=-9, attrs=f'fill="{INK}" opacity="0.75"')
    + word("title", TS, title_x, TY, skew=-9, attrs=f'fill="none" stroke="{PINK}" stroke-opacity="0.4" stroke-width="{24 / tk:.0f}" stroke-linejoin="round"')
    + word("title", TS, title_x, TY, skew=-9, attrs=f'fill="url(#tfill)" stroke="{INK}" stroke-width="{12 / tk:.0f}" stroke-linejoin="round" paint-order="stroke"')
)
RS = 21
rw = width("role", RS) + 64
ribbon = (
    f'<path d="M{600 - rw / 2 + 8:.0f} 242H{600 + rw / 2 + 8:.0f}L{600 + rw / 2 - 8:.0f} 282H{600 - rw / 2 - 8:.0f}Z" '
    f'fill="{INK}" fill-opacity="0.93" stroke="{PINK}" stroke-width="1.6"/>'
    + word("role", RS, 600, 269.5, "middle", attrs='fill="#ffffff"')
)

banner = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">El Diablo</title>
<desc id="d">Developer and avatar architect. Systems, networking, Blender and Unity. Move in silence. Let the work speak. The lettering sits over a sunset skyline with palm trees and water.</desc>
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NIGHT}"/>
    <stop offset="0.3" stop-color="#43186c"/>
    <stop offset="0.55" stop-color="#a52c7c"/>
    <stop offset="0.78" stop-color="#f25a66"/>
    <stop offset="1" stop-color="#ffb061"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff4bd"/>
    <stop offset="0.55" stop-color="{GOLD}"/>
    <stop offset="1" stop-color="#ff6f61"/>
  </linearGradient>
  <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#ffd08a" stop-opacity="0.75"/>
    <stop offset="1" stop-color="#ffd08a" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5a1d6e"/>
    <stop offset="0.35" stop-color="#2c1055"/>
    <stop offset="1" stop-color="#10062a"/>
  </linearGradient>
  <linearGradient id="tfill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fffbe6"/>
    <stop offset="0.42" stop-color="#ffe08a"/>
    <stop offset="0.72" stop-color="#ff9a5c"/>
    <stop offset="1" stop-color="#ff4f9a"/>
  </linearGradient>
  <linearGradient id="foot" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{INK}" stop-opacity="0"/>
    <stop offset="1" stop-color="{INK}" stop-opacity="0.85"/>
  </linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="6"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.55 -0.2"/>
  </filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="above"><rect width="{W}" height="{HZ}"/></clipPath>
</defs>
<style>
  .tw {{ animation: tw 4.5s ease-in-out infinite alternate; }}
  @keyframes tw {{ from {{ opacity: 0.15; }} }}
  .sh {{ animation: sh 3.4s ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }}
  @keyframes sh {{ from {{ transform: scaleX(0.55); opacity: 0.25; }} }}
  .halo {{ animation: halo 7s ease-in-out infinite alternate; }}
  @keyframes halo {{ from {{ opacity: 0.7; }} }}
  @media (prefers-reduced-motion: reduce) {{ .tw, .sh, .halo {{ animation: none; }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  {stars}
  <g clip-path="url(#above)">
    <circle class="halo" cx="600" cy="{HZ}" r="430" fill="url(#halo)"/>
    <circle cx="600" cy="{HZ - 6}" r="148" fill="url(#sun)"/>
    {clouds}
    {skyline(7, 96, 10, "#7a2a78", False)}
    {skyline(21, 124, 6, "#241047", True)}
  </g>
  <rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#sea)"/>
  <rect y="{HZ - 1}" width="{W}" height="2" fill="#ffd9a0" opacity="0.7"/>
  {reflect}
  {palms}
  <rect y="{H - 110}" width="{W}" height="110" fill="url(#foot)"/>
  {word("tags", 14, 600, 62, "middle", attrs=f'fill="{BLUSH}" opacity="0.9"')}
  {title}
  {ribbon}
  {word("motto", 21, 600, 392, "middle", attrs=f'fill="{BLUSH}"')}
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity="0.14"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#ffffff" stroke-opacity="0.14"/>
</svg>
"""
save("banner.svg", banner)

# ---------- work panels ----------
PW, PH = 1200, 330


def neon(shape, colour):
    """Line drawing with a soft coloured glow behind a pale core line."""
    return (
        f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
        f'<g stroke="{colour}" stroke-width="11" opacity="0.28">{shape}</g>'
        f'<g stroke="{colour}" stroke-width="5.5" opacity="0.6">{shape}</g>'
        f'<g stroke="#fff7fb" stroke-width="2.6">{shape}</g></g>'
    )


art = {
    "avatars": '<circle cx="60" cy="34" r="22"/><path d="M12 116c4-30 22-44 48-44s44 14 48 44"/>'
               '<path d="M60 72v30M60 86 36 104M60 86l24 18"/><circle cx="60" cy="86" r="3.2"/>',
    "systems": '<rect x="10" y="8" width="92" height="26" rx="6"/><rect x="10" y="46" width="92" height="26" rx="6"/>'
               '<rect x="10" y="84" width="92" height="26" rx="6"/><path d="M24 21h.1M24 59h.1M24 97h.1M44 21h42M44 59h30M44 97h42"/>',
    "tools": '<path d="M36 22 8 60l28 38M84 22l28 38-28 38M70 14 50 106"/>',
}
panels = [
    # key, number, clip shape, left edge of text, backdrop stops, glow colour, art position
    ("avatars", "n1", f"M0 0H414L374 {PH}H0Z", 40, ("#ff5f93", "#b0307f", "#2a0d4f"), GOLD, 232),
    ("systems", "n2", f"M426 0H814L774 {PH}H386Z", 432, ("#2a1a78", "#3b1d86", "#150a33"), CYAN, 628),
    ("tools", "n3", f"M826 0H{PW}V{PH}H786Z", 832, ("#ffa552", "#f2507a", "#2a0d4f"), "#fff1b0", 1034),
]
pr = random.Random(3)
defs, body = "", ""
for i, (key, num, shape, tx, stops, glow, ax) in enumerate(panels):
    defs += (
        f'<linearGradient id="p{i}" x1="0" y1="0" x2="0.25" y2="1"><stop offset="0" stop-color="{stops[0]}"/>'
        f'<stop offset="0.5" stop-color="{stops[1]}"/><stop offset="1" stop-color="{stops[2]}"/></linearGradient>'
        f'<clipPath id="c{i}"><path d="{shape}"/></clipPath>'
    )
    extra = ""
    if key == "avatars":
        extra = f'<circle cx="300" cy="100" r="96" fill="#6d1a72" opacity="0.5"/>' + palm(30, PH + 8, 150, 20, 0.7, pr, "#7d1f70")
    elif key == "systems":
        extra = "".join(f'<path d="M600 150 {x} {PH}" stroke="{CYAN}" stroke-opacity="0.2" stroke-width="1.5"/>' for x in range(300, 901, 60))
        extra += "".join(f'<rect x="380" y="{y}" width="440" height="1.5" fill="{CYAN}" opacity="0.18"/>' for y in (176, 198, 228, 270, 322))
        extra += f'<rect x="380" y="150" width="440" height="2" fill="{PINK}" opacity="0.7"/>'
    else:
        extra = "".join(
            f'<rect x="{x}" y="{PH - h}" width="{w}" height="{h}" fill="#4a1466" opacity="0.55"/>'
            for x, w, h in ((800, 44, 150), (850, 30, 210), (886, 52, 120), (944, 36, 180), (1100, 46, 230), (1150, 60, 160))
        )
    body += (
        f'<g clip-path="url(#c{i})"><rect width="{PW}" height="{PH}" fill="url(#p{i})"/>{extra}'
        f'<rect y="{PH - 170}" width="{PW}" height="170" fill="url(#fade)"/>'
        f'<g transform="translate({ax} 34) scale(1.12)">{neon(art[key], glow)}</g>'
        + word(num, 26, tx, 58, attrs='fill="#ffffff" opacity="0.92"')
        + f'<rect x="{tx}" y="70" width="34" height="3" fill="#ffffff" opacity="0.85"/>'
        + word(key, 80, tx + 4, 274, skew=-9, attrs=f'fill="{INK}" opacity="0.6"')
        + word(key, 80, tx, 270, skew=-9, attrs=f'fill="url(#pt)" stroke="{INK}" stroke-width="{8 / 0.08:.0f}" stroke-linejoin="round" paint-order="stroke"')
        + word(key + "_sub", 15, tx + 2, 304, attrs=f'fill="{BLUSH}"')
        + "</g>"
    )

work = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}" height="{PH}" role="img" aria-labelledby="t d">
<title id="t">What I work on</title>
<desc id="d">Three slanted panels. Avatars: Blender to Unity. Systems: Windows and Linux. Tools: apps and add-ons.</desc>
<defs>
  {defs}
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}" stop-opacity="0.9"/></linearGradient>
  <linearGradient id="pt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="0.6" stop-color="#ffe9a8"/><stop offset="1" stop-color="#ffb37a"/></linearGradient>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="9"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.55 -0.2"/>
  </filter>
  <clipPath id="frame"><rect width="{PW}" height="{PH}" rx="16"/></clipPath>
  <clipPath id="all"><path d="{panels[0][2]}{panels[1][2]}{panels[2][2]}"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  {body}
  <g clip-path="url(#all)"><rect width="{PW}" height="{PH}" filter="url(#grain)" opacity="0.13"/></g>
</g>
</svg>
"""
save("work.svg", work)

# ---------- divider ----------
div = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24" role="presentation">
<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PINK}" stop-opacity="0"/><stop offset="0.3" stop-color="{PINK}"/><stop offset="0.5" stop-color="{GOLD}"/><stop offset="0.7" stop-color="{PINK}"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></linearGradient></defs>
<style>
  .dot {{ animation: run 7s linear infinite; }}
  @keyframes run {{ from {{ transform: translateX(0); }} to {{ transform: translateX(1280px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .dot {{ animation: none; opacity: 0; }} }}
</style>
<rect x="0" y="11" width="1200" height="2" fill="url(#l)" opacity="0.85"/>
<rect class="dot" x="-80" y="10" width="80" height="4" rx="2" fill="#fff1b0"/>
</svg>
"""
save("divider.svg", div)

for old in ("card-avatars.svg", "card-systems.svg", "card-tools.svg"):
    p = os.path.join(out, old)
    if os.path.exists(p):
        os.remove(p)

import xml.dom.minidom as m
for f in sorted(os.listdir(out)):
    m.parse(os.path.join(out, f))
    print("ok", f, os.path.getsize(os.path.join(out, f)))
