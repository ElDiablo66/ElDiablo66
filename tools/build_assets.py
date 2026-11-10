import math, random, sys, os
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
random.seed(59)
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
RED = "#e5383b"


def save(name, text):
    with open(os.path.join(out, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------- banner ----------
bars = []
n = 34
for i in range(n):
    x = 742 + i * 12
    h = 26 + 86 * abs(math.sin(i * 0.47)) * (0.55 + 0.45 * random.random())
    d = round(0.9 + random.random() * 1.1, 2)
    delay = round(-random.random() * 2, 2)
    op = round(0.35 + 0.65 * (i / (n - 1)), 2)
    bars.append(
        f'<rect class="bar" x="{x}" y="{270 - h:.1f}" width="6" height="{h:.1f}" rx="3" '
        f'fill="url(#barfill)" opacity="{op}" style="animation-duration:{d}s;animation-delay:{delay}s"/>'
    )

banner = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="1200" height="360" role="img" aria-labelledby="t d">
<title id="t">El Diablo</title>
<desc id="d">Developer and Avatar Architect. Systems, Networking, Blender and Unity. Move in silence. Let the work speak.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#07090d"/>
    <stop offset="0.6" stop-color="#0d1117"/>
    <stop offset="1" stop-color="#1c080b"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{RED}" stop-opacity="0.42"/>
    <stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="barfill" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ff6b6b"/>
    <stop offset="1" stop-color="#7a0f14"/>
  </linearGradient>
  <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{RED}"/>
    <stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.045" stroke-width="1"/>
  </pattern>
  <clipPath id="card"><rect width="1200" height="360" rx="18"/></clipPath>
  <clipPath id="type"><rect class="reveal" x="70" y="206" width="420" height="40"/></clipPath>
</defs>
<style>
  .bar {{ transform-box: fill-box; transform-origin: 50% 100%; animation: eq 1.4s ease-in-out infinite alternate; }}
  @keyframes eq {{ from {{ transform: scaleY(0.25); }} to {{ transform: scaleY(1); }} }}
  .glow {{ animation: pulse 6s ease-in-out infinite alternate; }}
  @keyframes pulse {{ from {{ opacity: 0.55; }} to {{ opacity: 1; }} }}
  .scan {{ animation: scan 7s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(-40px); }} to {{ transform: translateY(400px); }} }}
  .reveal {{ animation: reveal 2.8s steps(28) 0.6s both; }}
  @keyframes reveal {{ from {{ width: 0; }} to {{ width: 420px; }} }}
  .caret {{ animation: caret 2.8s steps(28) 0.6s both, blink 1s step-end infinite; }}
  @keyframes caret {{ from {{ transform: translateX(0); }} to {{ transform: translateX(404px); }} }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .rise {{ animation: rise 0.9s ease-out both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .bar, .glow, .scan, .reveal, .caret, .rise {{ animation: none; }}
    .caret {{ transform: translateX(404px); }}
  }}
</style>
<g clip-path="url(#card)">
  <rect width="1200" height="360" fill="url(#bg)"/>
  <rect width="1200" height="360" fill="url(#grid)"/>
  <circle class="glow" cx="960" cy="190" r="340" fill="url(#glow)"/>
  <rect class="scan" x="0" y="0" width="1200" height="36" fill="#ffffff" opacity="0.025"/>
  <g>{''.join(bars)}</g>
  <rect x="742" y="276" width="402" height="1.5" fill="{RED}" opacity="0.5"/>
  <g class="rise">
    <text x="70" y="84" font-family="{MONO}" font-size="17" letter-spacing="3" fill="{RED}">// ElDiablo66</text>
    <text x="66" y="172" font-family="{SANS}" font-size="96" font-weight="900" letter-spacing="4" fill="#f0f6fc">EL DIABLO</text>
    <rect x="70" y="190" width="300" height="4" rx="2" fill="url(#rule)"/>
  </g>
  <g clip-path="url(#type)">
    <text x="70" y="235" font-family="{MONO}" font-size="24" textLength="403" lengthAdjust="spacing" fill="#c9d1d9">Developer &amp; Avatar Architect</text>
  </g>
  <rect class="caret" x="76" y="213" width="12" height="27" fill="{RED}"/>
  <text x="70" y="282" font-family="{SANS}" font-size="20" fill="#8b949e">Move in silence. Let the work speak.</text>
  <text x="70" y="322" font-family="{MONO}" font-size="14" letter-spacing="3" fill="#6e7681">SYSTEMS  /  NETWORKING  /  BLENDER  /  UNITY</text>
</g>
<rect x="0.5" y="0.5" width="1199" height="359" rx="18" fill="none" stroke="#30363d"/>
</svg>
"""
save("banner.svg", banner)

# ---------- cards ----------
S = f'fill="none" stroke="{RED}" stroke-width="3"'
icons = {
    "avatars": f'<circle cx="62" cy="62" r="13" {S}/>'
               f'<path d="M38 100c3-17 13-24 24-24s21 7 24 24" {S} stroke-linecap="round"/>',
    "systems": "".join(
        f'<rect x="38" y="{y}" width="48" height="15" rx="4" {S}/><circle cx="48" cy="{y + 7.5}" r="2.4" fill="{RED}"/>'
        for y in (42, 63, 84)
    ),
    "tools": f'<path d="M52 48 36 70l16 22M72 48l16 22-16 22" {S} stroke-linecap="round" stroke-linejoin="round"/>',
}
cards = [
    ("avatars", "Avatars", ["Blender to Unity.", "Sculpting, rigging, weights", "and shaders."]),
    ("systems", "Systems", ["Windows and Linux.", "Networking and the layers", "underneath."]),
    ("tools", "Tools", ["Desktop apps and Blender", "add-ons I build for my", "own workflow."]),
]
for i, (key, title, lines) in enumerate(cards):
    body = "".join(
        f'<text x="38" y="{176 + j * 27}" font-family="{SANS}" font-size="19" fill="#9aa4af">{l}</text>'
        for j, l in enumerate(lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260" width="400" height="260" role="img" aria-label="{title}: {' '.join(lines)}">
<defs>
  <linearGradient id="cbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#150a0c"/></linearGradient>
  <linearGradient id="top" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
  <clipPath id="c"><rect width="400" height="260" rx="16"/></clipPath>
</defs>
<style>
  .sweep {{ animation: sweep 5s ease-in-out {i * 0.8}s infinite; }}
  @keyframes sweep {{ 0%, 55% {{ transform: translateX(-140px); }} 100% {{ transform: translateX(420px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .sweep {{ animation: none; opacity: 0; }} }}
</style>
<g clip-path="url(#c)">
  <rect width="400" height="260" fill="url(#cbg)"/>
  <rect width="400" height="4" fill="url(#top)"/>
  <rect class="sweep" x="0" y="0" width="120" height="4" fill="#ffb3b3" opacity="0.9"/>
  {icons[key]}
  <text x="38" y="140" font-family="{SANS}" font-size="30" font-weight="800" fill="#f0f6fc">{title}</text>
  {body}
  <text x="362" y="52" text-anchor="end" font-family="{MONO}" font-size="15" fill="#484f58">0{i + 1}</text>
</g>
<rect x="0.5" y="0.5" width="399" height="259" rx="16" fill="none" stroke="#30363d"/>
</svg>
"""
    save(f"card-{key}.svg", svg)

# ---------- divider ----------
div = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24" role="presentation">
<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset="0.5" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient></defs>
<style>
  .dot {{ animation: run 6s linear infinite; }}
  @keyframes run {{ from {{ transform: translateX(0); }} to {{ transform: translateX(1280px); }} }}
  @media (prefers-reduced-motion: reduce) {{ .dot {{ animation: none; opacity: 0; }} }}
</style>
<rect x="0" y="11" width="1200" height="2" fill="url(#l)" opacity="0.7"/>
<rect class="dot" x="-80" y="10" width="80" height="4" rx="2" fill="#ff8a8a"/>
</svg>
"""
save("divider.svg", div)

import xml.dom.minidom as m
for f in sorted(os.listdir(out)):
    m.parse(os.path.join(out, f))
    print("ok", f)
