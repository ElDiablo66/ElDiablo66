"""Turn the words used in the images into outline paths.

GitHub shows the SVG files as images, and an image cannot load a web font,
so the lettering is stored as shapes. Run this only when the wording changes:

    python tools/make_lettering.py path/to/Saira-Variable.ttf

Needs fonttools. Saira is under the SIL Open Font License.
The result goes to tools/lettering.json, which build_assets.py reads.
"""
import json, os, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))

# key: (text, weight, width, extra spacing in font units)
WORDS = {
    "title": ("EL DIABLO", 900, 84, 14),
    "role": ("DEVELOPER & AVATAR ARCHITECT", 700, 100, 120),
    "tags": ("SYSTEMS  /  NETWORKING  /  BLENDER  /  UNITY", 600, 100, 150),
    "motto": ("Move in silence. Let the work speak.", 500, 100, 30),
    "avatars": ("AVATARS", 900, 84, 10),
    "systems": ("SYSTEMS", 900, 84, 10),
    "tools": ("TOOLS", 900, 84, 10),
    "avatars_sub": ("BLENDER TO UNITY", 600, 100, 110),
    "systems_sub": ("WINDOWS AND LINUX", 600, 100, 110),
    "tools_sub": ("APPS AND ADD-ONS", 600, 100, 110),
    "n1": ("01", 700, 100, 40),
    "n2": ("02", 700, 100, 40),
    "n3": ("03", 700, 100, 40),
}

cache = {}


def face(wght, wdth):
    if (wght, wdth) not in cache:
        cache[(wght, wdth)] = instantiateVariableFont(TTFont(FONT), {"wght": wght, "wdth": wdth})
    return cache[(wght, wdth)]


out = {}
for key, (text, wght, wdth, gap) in WORDS.items():
    f = face(wght, wdth)
    glyphs, cmap, hmtx = f.getGlyphSet(), f.getBestCmap(), f["hmtx"]
    pen = SVGPathPen(glyphs, ntos=lambda v: str(int(round(v))))
    x = 0
    for ch in text:
        name = cmap[ord(ch)]
        # flip y so the baseline sits at y = 0 and letters go up into negative y
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        x += hmtx[name][0] + gap
    out[key] = {"d": pen.getCommands(), "w": x - gap, "cap": f["OS/2"].sCapHeight}

with open(os.path.join(HERE, "lettering.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, separators=(",", ":"))
for k, v in out.items():
    print(k, v["w"], v["cap"], len(v["d"]))
