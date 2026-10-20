#!/usr/bin/env python3
"""Build / refresh the class website.

Folder layout (each student folder = one "area" with its own student list and codes):
    faith-formation/     lesson pages + lia-config.js + index.html     (student facing)
    ciencias-sociales/   ...
    math-physics/        ...
    teacher/             ALL teacher tools in one place - NOT linked from any student page:
                           index.html (teacher home), admin.html (students & codes), scores.html (scores & progress)
    shared/lia-sync.js   the sign-in + progress-saving module every student page loads
    shared/admin.template.html, shared/scores.template.html   sources of the teacher pages
    index.html           the site's front page (students)

Run it any time you add or move a page (it is safe to run again and again):

    python3 tools/build_site.py                      # connect all pages, rebuild hubs and admin pages
    python3 tools/build_site.py --url https://xxxx.supabase.co --key ANON_KEY
    python3 tools/build_site.py --area math-physics --url https://yyyy.supabase.co --key OTHER_KEY

What it does
  1. adds the sign-in / saving scripts to the <head> of EVERY lesson page in each folder
  2. writes <folder>/lia-config.js (keeps the URL/key already there unless you pass new ones)
  3. regenerates <folder>/admin.html, <folder>/index.html and the root index.html

To add a page: drop the .html file into the right folder and run this script.
"""
import argparse, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
# every folder has its OWN look (colours + font): nothing visual is shared between folders - only the database and the sign-in code
THEMES = {
    "faith-formation": dict(font="Lora:wght@400;500;600;700", family="'Lora',Georgia,serif",
        light=dict(bg="#f6f1ea", surface="#fffcf8", ink="#2b1d22", muted="#6a5a5f", line="#e3d5cb", primary="#7a2e3b", warm="#b8893b", soft="#f3e6e8", head="#4a1a25", headink="#f6ecdc", eyebrow="#e0c28a"),
        dark=dict(bg="#1a1214", surface="#241a1d", ink="#efe6e8", muted="#b4a2a8", line="#3b2c31", primary="#e2a3ae", warm="#d9b36a", soft="#2e2024")),
    "ciencias-sociales": dict(font="Merriweather:wght@400;700", family="'Merriweather',Georgia,serif",
        light=dict(bg="#eef2ea", surface="#fbfdf9", ink="#1f2a22", muted="#55655a", line="#d3ddcc", primary="#2f6b4a", warm="#c0762b", soft="#e1eee5", head="#1d3d2c", headink="#eef4ea", eyebrow="#d8c08a"),
        dark=dict(bg="#101712", surface="#18221b", ink="#e3ece5", muted="#97aa9d", line="#2a3a2f", primary="#8fd0a9", warm="#e0a25e", soft="#1c2a21")),
    "math-physics": dict(font="Oswald:wght@300;400;500;600;700", family="'Oswald','Arial Narrow',system-ui,sans-serif",
        light=dict(bg="#eef1f5", surface="#fbfcfe", ink="#17212e", muted="#566475", line="#d2d9e3", primary="#1f4e8c", warm="#2b7a76", soft="#e1eaf6", head="#14263f", headink="#eef2f8", eyebrow="#8fd0cb"),
        dark=dict(bg="#0e141c", surface="#161e29", ink="#e5ebf3", muted="#9aa8ba", line="#2a3646", primary="#9dc1f0", warm="#58b5ae", soft="#1a2636")),
}
DEFAULT_THEME = dict(font="Oswald:wght@300;400;500;600;700", family="'Oswald','Arial Narrow',system-ui,sans-serif",
    light=dict(bg="#f3f0e9", surface="#fffdf9", ink="#1e2937", muted="#5a6575", line="#ddd6c7", primary="#1f3a5f", warm="#b4763a", soft="#e6edf5", head="#1b2f4b", headink="#f3f0e9", eyebrow="#d3b48a"),
    dark=dict(bg="#11161d", surface="#18202a", ink="#e5e9ef", muted="#9aa5b5", line="#2d3947", primary="#9dbce6", warm="#d9a165", soft="#1b2838"))
AREAS = [
    dict(folder="faith-formation", name="Faith Formation",
         blurb="Religion and values lessons: scripture, doctrine and Growing in Values."),
    dict(folder="ciencias-sociales", name="Ciencias Sociales",
         blurb="Social science lessons and practice."),
    dict(folder="math-physics", name="Math & Physics",
         blurb="All mathematics and physics classes: Algebra, AP Statistics, Physics I and Physics II."),
]
SKIP = {"index.html", "admin.html", "scores.html"}   # (older copies of the teacher pages are removed from the student folders)
START, END = "<!--LIA-SYNC-START-->", "<!--LIA-SYNC-END-->"
BLOCK = START + '<script src="lia-config.js"></script><script src="../shared/lia-sync.js"></script>' + END
BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)
CFG_RE = re.compile(r"url:\s*'([^']*)'\s*,\s*anonKey:\s*'([^']*)'")


def page_info(path):
    s = path.read_text(encoding="utf8")
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = html.unescape(m.group(1)).strip() if m else path.stem
    short = title.split(" | ")[0].strip()
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    return title, short, html.unescape(d.group(1)).strip() if d else ""


def connect(path):
    s = path.read_text(encoding="utf8")
    s = BLOCK_RE.sub("", s)
    # remove the older per-page snippets if present
    s = re.sub(r"<!--LIA-SUPABASE-START.*?<!--LIA-SUPABASE-END-->\n?", "", s, flags=re.S)
    if "</head>" not in s:
        sys.exit("%s has no </head>" % path)
    s = s.replace("</head>", BLOCK + "\n</head>", 1)
    path.write_text(s, encoding="utf8")


def write_config(folder, area, pages, url, key):
    cfg = folder / "lia-config.js"
    old_url, old_key = "YOUR_SUPABASE_URL", "YOUR_SUPABASE_ANON_KEY"
    if cfg.exists():
        m = CFG_RE.search(cfg.read_text(encoding="utf8"))
        if m:
            old_url, old_key = m.group(1), m.group(2)
    url, key = url or old_url, key or old_key
    pm = ",\n".join("    %s: %s" % (js(k), js(v)) for k, v in sorted(pages.items()))
    cfg.write_text(
        "/* Settings for the \"%s\" area. Edit url and anonKey, then reload the pages.\n"
        "   url / anonKey: Supabase dashboard -> Project Settings -> API (the anon/publishable key is meant to be public).\n"
        "   area: keep as is - it separates this folder's students and codes from the other folders. */\n"
        "window.LIA_CONFIG={\n  url: %s,\n  anonKey: %s,\n  area: %s,\n  areaName: %s,\n  pages: {\n%s\n  }\n};\n"
        % (area["name"], js(url), js(key), js(area["folder"]), js(area["name"]), pm), encoding="utf8")


def js(v):
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"


HUB_CSS = """
:root{--bg:#f3f0e9;--surface:#fffdf9;--ink:#1e2937;--muted:#5a6575;--line:#ddd6c7;--primary:#1f3a5f;--warm:#b4763a;--soft:#e6edf5}
@media (prefers-color-scheme: dark){:root{--bg:#11161d;--surface:#18202a;--ink:#e5e9ef;--muted:#9aa5b5;--line:#2d3947;--primary:#9dbce6;--warm:#d9a165;--soft:#1b2838}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 'Oswald','Arial Narrow',system-ui,sans-serif}
header{background:#1b2f4b;color:#f3f0e9;border-bottom:4px solid var(--warm)}
.wrap{max-width:1000px;margin:0 auto;padding:0 16px}header .wrap{padding-top:22px;padding-bottom:20px}
.eyebrow{font-size:.78rem;text-transform:uppercase;letter-spacing:.14em;color:#d3b48a}.school{font-size:clamp(1.5rem,4vw,2.1rem);font-weight:700}
header p{margin:.2em 0 0;color:#cfd8e6}main{padding:26px 0 50px}h2{font-size:1.5rem;margin:0 0 .6em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px}
a.card{display:block;text-decoration:none;color:inherit;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px;box-shadow:0 1px 2px rgba(0,0,0,.06),0 4px 14px rgba(0,0,0,.05);transition:transform .12s,border-color .12s}
a.card:hover{transform:translateY(-2px);border-color:var(--primary)}a.card h3{margin:0 0 .3em;font-size:1.2rem;color:var(--primary)}a.card p{margin:0;color:var(--muted);font-size:.95rem}
a.card .tag{display:inline-block;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--warm);font-weight:600;margin-bottom:4px}
footer{border-top:1px solid var(--line);padding:18px 0 40px;color:var(--muted);font-size:.9rem}footer a{color:var(--primary)}
"""


def themed_css(th):
    """HUB_CSS with this folder's own palette and font."""
    L, D = th["light"], th["dark"]
    css = HUB_CSS
    root_l = "--bg:%(bg)s;--surface:%(surface)s;--ink:%(ink)s;--muted:%(muted)s;--line:%(line)s;--primary:%(primary)s;--warm:%(warm)s;--soft:%(soft)s" % L
    root_d = "--bg:%(bg)s;--surface:%(surface)s;--ink:%(ink)s;--muted:%(muted)s;--line:%(line)s;--primary:%(primary)s;--warm:%(warm)s;--soft:%(soft)s" % D
    lines = css.strip("\n").split("\n")
    lines[0] = ":root{%s}" % root_l
    lines[1] = "@media (prefers-color-scheme: dark){:root{%s}}" % root_d
    css = "\n".join(lines)
    css = css.replace("font:17px/1.6 'Oswald','Arial Narrow',system-ui,sans-serif", "font:17px/1.6 %s" % th["family"])
    css = css.replace("header{background:#1b2f4b;color:#f3f0e9;", "header{background:%s;color:%s;" % (L["head"], L["headink"]))
    css = css.replace("color:#d3b48a}", "color:%s}" % L["eyebrow"]).replace("header p{margin:.2em 0 0;color:#cfd8e6}", "header p{margin:.2em 0 0;color:%s;opacity:.85}" % L["headink"])
    return css + "\n"


def fonts(th):
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=%s&display=swap" rel="stylesheet">' % th["font"])


FONTS = fonts(DEFAULT_THEME)
LIA_HUB = '<meta name="lia-hub" content="1">\n<script src="lia-config.js"></script><script src="../shared/lia-sync.js"></script>\n'


def hub(title, sub, cards, footer, theme=None, signin=False):
    th = theme or DEFAULT_THEME
    body = "\n".join('<a class="card" href="%s"><span class="tag">%s</span><h3>%s</h3><p>%s</p></a>' % (
        html.escape(h), html.escape(t), html.escape(n), html.escape(d)) for h, t, n, d in cards)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>%s | Lincoln International Academy</title>\n%s\n%s<style>%s</style>\n</head>\n<body>\n'
            '<header><div class="wrap"><div class="eyebrow">Student learning site</div><div class="school">Lincoln International Academy</div><p>%s</p></div></header>\n'
            '<main><div class="wrap"><div class="grid">\n%s\n</div></div></main>\n<footer><div class="wrap">%s</div></footer>\n</body>\n</html>\n'
            % (html.escape(title), fonts(th), LIA_HUB if signin else "", themed_css(th), html.escape(sub), body, footer))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url"), ap.add_argument("--key")
    ap.add_argument("--area", help="only set --url/--key for this folder (default: all folders)")
    a = ap.parse_args()
    if bool(a.url) != bool(a.key):
        sys.exit("Give both --url and --key (or neither).")
    template = (ROOT / "shared" / "admin.template.html").read_text(encoding="utf8")
    scores_template = (ROOT / "shared" / "scores.template.html").read_text(encoding="utf8")
    root_cards = []
    for area in AREAS:
        folder = ROOT / area["folder"]
        folder.mkdir(exist_ok=True)
        files = sorted(p for p in folder.glob("*.html") if p.name not in SKIP)
        pages, cards = {}, []
        for p in files:
            connect(p)
            title, short, desc = page_info(p)
            pages[p.stem.lower()] = short
            cards.append((p.name, "", title, desc))
        use = a.url and (not a.area or a.area == area["folder"])
        write_config(folder, area, pages, a.url if use else None, a.key if use else None)
        for old in ("admin.html", "scores.html"):   # teacher tools live in teacher/ now
            if (folder / old).exists():
                (folder / old).unlink()
        (folder / "index.html").write_text(hub(
            area["name"], area["blurb"], cards,
            '<a href="../index.html">← All subjects</a>', theme=THEMES[area["folder"]], signin=True), encoding="utf8")
        root_cards.append((area["folder"] + "/", "%d lessons" % len(files), area["name"], area["blurb"]))
        print("%-18s %2d pages connected" % (area["folder"], len(files)))
    (ROOT / "index.html").write_text(hub(
        "Student learning site", "Choose your subject, then sign in with the access code your teacher gave you.", root_cards,
        "Sign in on each lesson page with the access code your teacher gave you."), encoding="utf8")
    # ---- teacher tools (separate from the student pages)
    tdir = ROOT / "teacher"
    tdir.mkdir(exist_ok=True)
    (tdir / "admin.html").write_text(template, encoding="utf8")
    (tdir / "scores.html").write_text(scores_template, encoding="utf8")
    (tdir / "access.html").write_text((ROOT / "shared" / "access.template.html").read_text(encoding="utf8"), encoding="utf8")
    tcards = []
    for ar in AREAS:
        th = THEMES[ar["folder"]]["light"]
        lessons = sorted(p for p in (ROOT / ar["folder"]).glob("*.html") if p.name not in SKIP)
        lis = "".join('<li><a href="../%s/%s" target="_blank" rel="noopener">%s</a><code>%s</code></li>' % (
            ar["folder"], p.name, html.escape(page_info(p)[1]), p.name) for p in lessons)
        tcards.append(
            '<section class="card" style="--primary:%s;--warm:%s;--soft:%s"><span class="tag">%d lessons</span><h3>%s</h3><p>%s</p>'
            '<p class="acts"><a class="btn" href="scores.html?area=%s">Scores &amp; progress</a><a class="btn" href="admin.html?area=%s">Students &amp; codes</a>'
            '<a class="btn" href="access.html?area=%s">Assign lessons</a><a class="btn ghost" href="../%s/" target="_blank" rel="noopener">Student menu ↗</a></p>'
            '<details><summary>All lesson links</summary><ul class="lessons">%s</ul></details></section>'
            % (th["primary"], th["warm"], th["soft"], len(lessons), html.escape(ar["name"]), html.escape(ar["blurb"]), ar["folder"], ar["folder"], ar["folder"], ar["folder"], lis))
    tcards = "\n".join(tcards)
    (tdir / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex,nofollow">\n'
        '<title>Teacher tools | Lincoln International Academy</title>\n' + FONTS + '\n<style>' + HUB_CSS +
        '.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px}.card h3{margin:0 0 .3em;font-size:1.25rem;color:var(--primary)}.card p{margin:.2em 0 .8em;color:var(--muted)}'
        '.acts{display:flex;flex-wrap:wrap;gap:8px}.btn{display:inline-block;text-decoration:none;font-weight:600;font-size:.9rem;border-radius:8px;padding:7px 14px;border:1px solid var(--primary);background:var(--primary);color:#fff}'
        '.btn.ghost{background:transparent;color:var(--primary)}details{margin-top:6px}summary{cursor:pointer;color:var(--primary);font-weight:600}ul.lessons{list-style:none;margin:8px 0 0;padding:0}ul.lessons li{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px;padding:5px 0;border-bottom:1px solid var(--line)}ul.lessons a{color:var(--primary);text-decoration:none}ul.lessons code{font-size:.78rem;color:var(--muted)}.note{background:var(--soft);border-radius:10px;padding:12px 16px;margin:18px 0 0;color:var(--muted);font-size:.95rem}</style>\n</head>\n<body>\n'
        '<header><div class="wrap"><div class="eyebrow">Teacher tools</div><div class="school">Lincoln International Academy</div><p>Scores, progress, students and access codes for every subject.</p></div></header>\n'
        '<main><div class="wrap"><div class="grid">\n' + tcards + '\n</div>'
        '<p class="note"><b>Student site:</b> <a href="../index.html">front page</a> · <a href="../math-physics/">Math &amp; Physics</a> · <a href="../ciencias-sociales/">Ciencias Sociales</a> · <a href="../faith-formation/">Faith Formation</a></p>'
        '<p class="note"><b>Sign in</b> with your teacher account on the page you open (one login works for all of them). '
        'This area is not linked from the student pages; students only ever see the lessons. First time? Follow <code>supabase/README.md</code>.</p></div></main>\n'
        '<footer><div class="wrap"><a href="../index.html">← Student site</a></div></footer>\n</body>\n</html>\n', encoding="utf8")
    print("root index.html written")


if __name__ == "__main__":
    main()
