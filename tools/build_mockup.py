"""Builds a one-file preview of the profile page: python tools/build_mockup.py out.html

The README is dropped into a page laid out like a GitHub profile, with the
images embedded, so the file can be opened anywhere. Badges and the avatar
still come from the web.
"""
import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dest = sys.argv[1]
USER = "ElDiablo66"

with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
    readme = fh.read()


def embed(match):
    with open(os.path.join(ROOT, match.group(1)), "rb") as fh:
        return 'src="data:image/svg+xml;base64,' + base64.b64encode(fh.read()).decode() + '"'


readme = re.sub(r'src="(assets/[^"]+\.svg)"', embed, readme)

page = """<!doctype html>
<html lang="en" data-theme="dark" data-width="desktop">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__USER__ profile mockup</title>
<meta name="description" content="Mockup of the redesigned profile page for __USER__.">
<style>
:root {
  --bg: #0d1117; --bar: #010409; --line: #30363d; --line-soft: #21262d; --text: #e6edf3; --muted: #8d96a0;
  --link: #4493f8; --btn: #21262d; --btn-hover: #30363d; --row: #151b23; --pill: #30363d; --stage: #07030f;
  --accent: #ff4f9a; --gold: #ffc857;
  color-scheme: dark;
}
:root[data-theme="light"] {
  --bg: #ffffff; --bar: #f6f8fa; --line: #d1d9e0; --line-soft: #e4e9ee; --text: #1f2328; --muted: #59636e;
  --link: #0969da; --btn: #f6f8fa; --btn-hover: #eaeef2; --row: #f6f8fa; --pill: #d1d9e0; --stage: #efe7f3;
  color-scheme: light;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--stage); color: var(--text);
  font: 14px/1.5 -apple-system, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.skip { position: absolute; left: -999px; }
.skip:focus { left: 12px; top: 12px; z-index: 5; background: var(--bg); padding: 8px 12px; border-radius: 6px; }

/* bar above the page: this part belongs to the mockup */
.deck { display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center; justify-content: space-between;
  padding: 12px 20px; background: linear-gradient(100deg, #150a33, #43186c 55%, #a52c7c); color: #ffe3f0; }
.deck p { margin: 0; font-size: 13px; }
.deck strong { color: #fff; font-weight: 600; }
.switches { display: flex; flex-wrap: wrap; gap: 14px; }
.seg { display: inline-flex; border: 1px solid rgba(255,255,255,.28); border-radius: 8px; overflow: hidden; }
.seg button { font: inherit; font-size: 12px; font-weight: 500; color: #ffe3f0; background: transparent; border: 0;
  padding: 6px 12px; min-height: 32px; cursor: pointer; transition: background .2s, color .2s, transform .1s; }
.seg button:hover { background: rgba(255,255,255,.12); }
.seg button:active { transform: translateY(1px); }
.seg button[aria-pressed="true"] { background: #ffe3f0; color: #2a0d4f; }

.shell { max-width: 1320px; margin: 24px auto 40px; padding: 0 16px; transition: max-width .3s ease; }
:root[data-width="phone"] .shell { max-width: 422px; }
.frame { background: var(--bg); border: 1px solid var(--line); border-radius: 10px; overflow: hidden;
  box-shadow: 0 24px 60px -24px rgba(110, 30, 120, .55); }

.top { background: var(--bar); padding: 16px 24px 0; border-bottom: 1px solid var(--line); }
.crumb { display: flex; align-items: center; gap: 12px; font-weight: 600; }
.mark { width: 30px; height: 30px; border-radius: 50%; border: 1px solid var(--line); background: var(--btn); }
.tabs { display: flex; gap: 6px; margin: 12px 0 0; padding: 0; list-style: none; overflow-x: auto; }
.tabs li { padding: 8px 10px 10px; white-space: nowrap; border-bottom: 2px solid transparent; color: var(--text); }
.tabs li[aria-current="page"] { border-bottom-color: #fd8c73; font-weight: 600; }
.count { background: var(--pill); border-radius: 20px; padding: 0 6px; font-size: 12px; margin-left: 4px; }

.cols { display: grid; grid-template-columns: 296px minmax(0, 1fr); gap: 24px; padding: 28px 32px 36px; }
:root[data-width="phone"] .cols { grid-template-columns: minmax(0, 1fr); padding: 16px; gap: 16px; }
@media (max-width: 760px) { .cols { grid-template-columns: minmax(0, 1fr); padding: 16px; gap: 16px; } }

.who { display: grid; gap: 12px; align-content: start; }
.face { width: 100%; max-width: 296px; aspect-ratio: 1; border-radius: 50%; border: 1px solid var(--line); object-fit: cover;
  background: radial-gradient(circle at 50% 78%, #ffc857 0 26%, #ff6f61 27% 40%, #a52c7c 56%, #150a33 86%); }
.who h1 { margin: 0; font-size: 24px; line-height: 1.25; font-weight: 600; }
.who h1 span { display: block; font-size: 20px; font-weight: 300; color: var(--muted); }
.follow { font: inherit; font-weight: 500; color: var(--text); background: var(--btn); border: 1px solid var(--line);
  border-radius: 6px; padding: 5px 16px; min-height: 32px; cursor: default; }
.bio { margin: 0; font-size: 16px; }
.meta { margin: 0; color: var(--muted); }
.meta b { color: var(--text); font-weight: 600; }
:root[data-width="phone"] .who { grid-template-columns: 72px 1fr; align-items: center; }
:root[data-width="phone"] .who > :nth-child(n+3) { grid-column: 1 / -1; }
@media (max-width: 760px) {
  .who { grid-template-columns: 72px 1fr; align-items: center; }
  .who > :nth-child(n+3) { grid-column: 1 / -1; }
}

.box { border: 1px solid var(--line); border-radius: 6px; padding: 24px; }
:root[data-width="phone"] .box { padding: 16px; }
.path { margin: 0 0 16px; font: 12px/1.4 ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; color: var(--text); }
.path i { font-style: normal; color: var(--muted); }

.md { font-size: 16px; line-height: 1.5; overflow-wrap: break-word; }
.md > * { margin-top: 0; margin-bottom: 16px; }
.md > :last-child { margin-bottom: 0; }
.md img { max-width: 100%; height: auto; vertical-align: middle; }
.md div[align="center"] > table { margin: 0 auto; }
.md table { display: block; width: max-content; max-width: 100%; overflow: auto; border-spacing: 0; border-collapse: collapse; }
.md th, .md td { padding: 6px 13px; border: 1px solid var(--line); }
.md th { font-weight: 600; }
.md tr { background: var(--bg); border-top: 1px solid var(--line-soft); }
.md tr:nth-child(2n) { background: var(--row); }

h2.sub { font-size: 16px; font-weight: 400; margin: 24px 0 8px; }
.repo { border: 1px solid var(--line); border-radius: 6px; padding: 16px; max-width: 440px; display: grid; gap: 8px; }
.repo a { font-weight: 600; }
.tag { border: 1px solid var(--line); border-radius: 20px; padding: 0 7px; font-size: 12px; color: var(--muted); margin-left: 6px; }
.repo p { margin: 0; font-size: 12px; color: var(--muted); }
.lang { display: flex; align-items: center; gap: 6px; }
.lang::before { content: ""; width: 12px; height: 12px; border-radius: 50%; background: #3572a5; }
.note { max-width: 1320px; margin: 0 auto 40px; padding: 0 20px; color: var(--muted); font-size: 12px; text-wrap: pretty; }
</style>
</head>
<body>
<a class="skip" href="#readme">Skip to the README</a>
<header class="deck">
  <p><strong>Profile mockup</strong> for github.com/__USER__. This is a preview, not the live page.</p>
  <div class="switches">
    <div class="seg" role="group" aria-label="Theme">
      <button type="button" data-set="theme" data-value="dark" aria-pressed="true">Dark</button>
      <button type="button" data-set="theme" data-value="light" aria-pressed="false">Light</button>
    </div>
    <div class="seg" role="group" aria-label="Width">
      <button type="button" data-set="width" data-value="desktop" aria-pressed="true">Desktop</button>
      <button type="button" data-set="width" data-value="phone" aria-pressed="false">Phone</button>
    </div>
  </div>
</header>

<div class="shell">
  <div class="frame">
    <div class="top">
      <div class="crumb"><span class="mark" aria-hidden="true"></span><span>__USER__</span></div>
      <nav aria-label="Profile sections">
        <ul class="tabs">
          <li aria-current="page">Overview</li>
          <li>Repositories <span class="count">1</span></li>
          <li>Projects</li>
          <li>Packages</li>
          <li>Stars</li>
        </ul>
      </nav>
    </div>
    <div class="cols">
      <aside class="who" aria-label="Profile details">
        <img class="face" src="https://github.com/__USER__.png?size=460" alt="Profile picture of __USER__" onerror="this.removeAttribute('src')">
        <h1>Anonymous <span>__USER__</span></h1>
        <button class="follow" type="button" disabled>Follow</button>
        <p class="bio">Developer &amp; Avatar Architect | Systems, Networking, Blender + Unity | Move in silence. Let the work speak.</p>
        <p class="meta"><b>0</b> followers · <b>2</b> following</p>
      </aside>
      <main id="readme">
        <section class="box" aria-label="Profile README">
          <p class="path">__USER__ <i>/</i> README<i>.md</i></p>
          <article class="md">
__README__
          </article>
        </section>
        <h2 class="sub">Popular repositories</h2>
        <div class="repo">
          <div><a href="https://github.com/__USER__/__USER__">__USER__</a><span class="tag">Public</span></div>
          <p>Profile README</p>
          <p class="lang">Python</p>
        </div>
      </main>
    </div>
  </div>
</div>
<p class="note">Only the README box changes with this redesign. The header, sidebar and repository list are drawn to show how it sits on the page.</p>

<script>
document.querySelectorAll(".seg button").forEach(function (b) {
  b.addEventListener("click", function () {
    document.documentElement.setAttribute("data-" + b.dataset.set, b.dataset.value);
    b.parentNode.querySelectorAll("button").forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
  });
});
</script>
</body>
</html>
"""

page = page.replace("__README__", readme).replace("__USER__", USER)
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
with open(dest, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(page)
print("wrote", dest, os.path.getsize(dest))
