#!/usr/bin/env python3
"""Build / refresh the class website.

Folder layout (each student folder = one "area" with its own student list and codes):
    faith-formation/     lesson pages + lia-config.js + index.html     (student facing)
    ciencias-sociales/   ...
    math/  physics/      ...
    teacher/             ALL teacher tools in one place - NOT linked from any student page:
                           index.html (teacher home), admin.html (students & codes), scores.html (scores & progress),
                           responses.html (students' saved text answers), access.html (assign lessons)
    shared/lia-sync.js   the sign-in + progress-saving module every student page loads
    shared/*.template.html   sources of the teacher pages (admin, scores, access, responses)
    index.html           the site's front page (students)

Run it any time you add or move a page (it is safe to run again and again):

    python3 tools/build_site.py                      # connect all pages, rebuild hubs and admin pages
    python3 tools/build_site.py --url https://xxxx.supabase.co --key ANON_KEY
    python3 tools/build_site.py --area physics --url https://yyyy.supabase.co --key OTHER_KEY

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
    "math": dict(font="Source+Serif+4:wght@400;600;700", family="'Source Serif 4',Georgia,serif",
        light=dict(bg="#f1eff7", surface="#fdfcff", ink="#211d33", muted="#605a78", line="#d9d4ea", primary="#4b3f8f", warm="#b0782a", soft="#e7e3f5", head="#2a2250", headink="#f1eefb", eyebrow="#d9bf85"),
        dark=dict(bg="#13111d", surface="#1c1928", ink="#ebe8f5", muted="#a39eb9", line="#312d46", primary="#b9aef0", warm="#dcae66", soft="#221f33")),
    "physics": dict(font="Oswald:wght@300;400;500;600;700", family="'Oswald','Arial Narrow',system-ui,sans-serif",
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
    dict(folder="math", name="Math",
         blurb="Mathematics classes: Advanced Algebra, AP Statistics and Pre-Calculus."),
    dict(folder="physics", name="Physics",
         blurb="Physics I (chapters 1–2) and Physics II (chapters 9–11)."),
]
SKIP = {"index.html", "admin.html", "scores.html"}   # (older copies of the teacher pages are removed from the student folders)

# ---- browser-tab icons (favicons): one per folder, same colour as the folder's look; teacher pages have their own
ICON_GLYPHS = {
    "faith-formation": '<rect x="28" y="12" width="8" height="40" rx="2" fill="#fff"/><rect x="18" y="22" width="28" height="8" rx="2" fill="#fff"/>',
    "ciencias-sociales": '<g fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"><circle cx="32" cy="32" r="17"/><ellipse cx="32" cy="32" rx="7.5" ry="17"/><path d="M15.5 32h33M18 22.5h28M18 41.5h28"/></g>',
    "math": '<g fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 22h32"/><path d="M25 23v23"/><path d="M39 23v16q0 7 7 7"/></g>',
    "physics": '<g fill="none" stroke="#fff" stroke-width="3"><ellipse cx="32" cy="32" rx="21" ry="8"/><ellipse cx="32" cy="32" rx="21" ry="8" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="21" ry="8" transform="rotate(120 32 32)"/></g><circle cx="32" cy="32" r="5" fill="#fff"/>',
    "teacher": '<path d="M23 14v32h21" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
}
ICON_BG = {"faith-formation": "#7a2e3b", "ciencias-sociales": "#2f6b4a", "math": "#4b3f8f", "physics": "#1f4e8c", "teacher": "#1b2f4b"}


def icon_svg(key):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="%s"/>%s'
            '</svg>\n' % (ICON_BG[key], ICON_GLYPHS[key]))


def icon_links(prefix=""):
    return ('<link rel="icon" type="image/svg+xml" href="%sfavicon.svg"><link rel="alternate icon" type="image/png" href="%sfavicon.png">' % (prefix, prefix))

START, END = "<!--LIA-SYNC-START-->", "<!--LIA-SYNC-END-->"
BLOCK = START + icon_links() + '<script src="lia-config.js"></script><script src="../shared/lia-sync.js"></script>' + END
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
    for area in AREAS:
        folder = ROOT / area["folder"]
        folder.mkdir(exist_ok=True)
        files = sorted(p for p in folder.glob("*.html") if p.name not in SKIP)
        pages = {}
        for p in files:
            connect(p)
            title, short, desc = page_info(p)
            pages[p.stem.lower()] = short
        use = a.url and (not a.area or a.area == area["folder"])
        write_config(folder, area, pages, a.url if use else None, a.key if use else None)
        (folder / "favicon.svg").write_text(icon_svg(area["folder"]), encoding="utf8")
        for old in ("admin.html", "scores.html", "index.html"):   # no student menu: lessons are shared by direct link only
            if (folder / old).exists():
                (folder / old).unlink()
        print("%-18s %2d pages connected" % (area["folder"], len(files)))
    # ---- teacher tools: the site root is the (signed-in) teacher home; there is no public student index
    tdir = ROOT / "teacher"
    tdir.mkdir(exist_ok=True)
    (tdir / "favicon.svg").write_text(icon_svg("teacher"), encoding="utf8")
    (tdir / "admin.html").write_text(template, encoding="utf8")
    (tdir / "scores.html").write_text(scores_template, encoding="utf8")
    (tdir / "access.html").write_text((ROOT / "shared" / "access.template.html").read_text(encoding="utf8"), encoding="utf8")
    (tdir / "responses.html").write_text((ROOT / "shared" / "responses.template.html").read_text(encoding="utf8"), encoding="utf8")
    (tdir / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=../index.html"><title>Teacher tools</title>' + icon_links() + '<a href="../index.html">Teacher tools</a>\n', encoding="utf8")
    (ROOT / "index.html").write_text(teacher_home(), encoding="utf8")
    print("root index.html (teacher sign-in) written")


THEME_JS = "<script>\n(function(){var r=document.documentElement,mq=matchMedia('(prefers-color-scheme: dark)');\ntry{var t=localStorage.getItem('lia-theme');if(t==='light'||t==='dark')r.setAttribute('data-theme',t);}catch(e){}\nvar wrap=document.querySelector('header .wrap'),who=document.getElementById('who');if(!wrap)return;\nvar hr=document.createElement('div');hr.className='hr';if(who)hr.appendChild(who);wrap.appendChild(hr);\nvar b=document.createElement('button');b.type='button';b.id='btnTheme';b.className='ghost small tg';hr.appendChild(b);\nfunction eff(){return r.getAttribute('data-theme')||(mq.matches?'dark':'light');}\nfunction lab(){b.textContent=eff()==='dark'?'☀ Light':'☾ Dark';b.setAttribute('aria-label','Switch to '+(eff()==='dark'?'light':'dark')+' mode');}\nb.addEventListener('click',function(){var n=eff()==='dark'?'light':'dark';r.setAttribute('data-theme',n);try{localStorage.setItem('lia-theme',n);}catch(e){}lab();});\nif(mq.addEventListener)mq.addEventListener('change',lab);lab();})();\n</script>\n"


def darkify(css):
    """Make the prefers-color-scheme dark palette also available as an explicit light/dark switch (data-theme on <html>)."""
    def f(m):
        return '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){%s}}\n:root[data-theme="dark"]{%s}' % (m.group(1), m.group(1))
    css = re.sub(r"@media \(prefers-color-scheme: dark\)\{:root\{([^{}]*)\}\}", f, css, 1)
    return re.sub(r"@media \(prefers-color-scheme: dark\)\{\.(a\d)\{([^{}]*)\}\}",
                  lambda m: '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .%s{%s}}\n:root[data-theme="dark"] .%s{%s}' % (m.group(1), m.group(2), m.group(1), m.group(2)), css)


def teacher_home():
    css_areas, cards = "", []
    for n, ar in enumerate(AREAS):
        th = THEMES[ar["folder"]]
        L, D = th["light"], th["dark"]
        css_areas += (".a%d{--p:%s;--pi:#fff;--w:%s}@media (prefers-color-scheme: dark){.a%d{--p:%s;--pi:#14181f;--w:%s}}\n"
                      % (n, L["primary"], L["warm"], n, D["primary"], D["warm"]))
        lessons = sorted(p for p in (ROOT / ar["folder"]).glob("*.html") if p.name not in SKIP)
        rows = "".join('<li><div><b>%s</b><a class="lk" data-rel="%s/%s" href="%s/%s" target="_blank" rel="noopener"></a></div><button class="btn ghost sm" type="button" data-copy>Copy link</button></li>'
                       % (html.escape(page_info(p)[1]), ar["folder"], p.name, ar["folder"], p.name) for p in lessons)
        cards.append(
            '<section class="card a%d" data-area="%s"><span class="tag">%d lessons</span><h3>%s</h3><p>%s</p>'
            '<p class="pv"><span>Teacher preview code:</span> <code data-pv>…</code> <button class="btn ghost sm" type="button" data-copycode>Copy</button></p>'
            '<p class="acts"><a class="btn" href="teacher/scores.html?area=%s">Scores &amp; progress</a><a class="btn" href="teacher/admin.html?area=%s">Students &amp; codes</a>'
            '<a class="btn" href="teacher/access.html?area=%s">Assign lessons</a><a class="btn" href="teacher/responses.html?area=%s">Student responses</a></p>'
            '<details open><summary>Links to share with students</summary><ul class="lessons">%s</ul></details></section>'
            % (n, ar["folder"], len(lessons), html.escape(ar["name"]), html.escape(ar["blurb"]), ar["folder"], ar["folder"], ar["folder"], ar["folder"], rows))
    js = r"""
(function(){
'use strict';
var CFG=window.LIA_CONFIG||{}, $=function(s){return document.querySelector(s);}, BASE=String(CFG.url||'').replace(/\/+$/,''), SK='lia-admin-session:'+(CFG.url||''), sess=null;
var LIVE=CFG.url&&CFG.anonKey&&!/YOUR_SUPABASE/.test(CFG.url+CFG.anonKey);
function msg(t){var e=$('#lErr');e.textContent=t||'';e.hidden=!t;}
function save(j){ sess={access_token:j.access_token,refresh_token:j.refresh_token,expires_at:Date.now()+(j.expires_in||3600)*1000,email:(j.user&&j.user.email)||(sess&&sess.email)||''}; try{localStorage.setItem(SK,JSON.stringify(sess));}catch(e){} }
function auth(body,grant){ return fetch(BASE+'/auth/v1/token?grant_type='+grant,{method:'POST',headers:{apikey:CFG.anonKey,'Content-Type':'application/json'},body:JSON.stringify(body)}).then(function(r){return r.json().then(function(j){ if(!r.ok) throw new Error(j.error_description||j.msg||j.message||'Sign-in failed'); return j; });}); }
function check(){ var go=function(){ return fetch(BASE+'/rest/v1/admins?select=user_id',{headers:{apikey:CFG.anonKey,Authorization:'Bearer '+sess.access_token}}); };
  return go().then(function(r){ if(r.status===401&&sess.refresh_token) return auth({refresh_token:sess.refresh_token},'refresh_token').then(function(j){save(j);return go();}); return r; }).then(function(r){ if(!r.ok) throw new Error('expired'); return r.json(); }).then(function(a){ if(!a||!a.length) throw new Error('This account is not an administrator yet (see supabase/README.md).'); }); }
function fmt(c){ c=String(c||'').toUpperCase(); return c.replace(/(.{4})(?=.)/g,'$1-'); }
function previews(){ fetch(BASE+'/rest/v1/students?select=area,code&is_preview=eq.true',{headers:{apikey:CFG.anonKey,Authorization:'Bearer '+sess.access_token}}).then(function(r){return r.ok?r.json():[];}).then(function(rows){
  [].forEach.call(document.querySelectorAll('section[data-area]'),function(sec){ var m=rows.filter(function(x){return x.area===sec.dataset.area;})[0], c=sec.querySelector('[data-pv]'); c.textContent=m?fmt(m.code):'not created yet'; c.dataset.code=m?fmt(m.code):''; sec.querySelector('[data-copycode]').hidden=!m; }); },function(){}); }
function show(){ previews(); $('#gate').hidden=true; $('#home').hidden=false; $('#who').hidden=false; $('#whoMail').textContent=(sess&&sess.email)||'';
  [].forEach.call(document.querySelectorAll('a.lk'),function(a){ var u=new URL(a.dataset.rel,location.href).href; a.textContent=u; a.href=u; }); }
function out(t){ sess=null; try{localStorage.removeItem(SK);}catch(e){} $('#home').hidden=true; $('#who').hidden=true; $('#gate').hidden=false; msg(t); }
document.addEventListener('click',function(e){ var cb=e.target.closest('[data-copycode]'); if(cb){ var c=cb.closest('.pv').querySelector('[data-pv]').dataset.code; try{navigator.clipboard.writeText(c);}catch(x){} var o=cb.textContent; cb.textContent='Copied ✓'; setTimeout(function(){cb.textContent=o;},1400); return; } var b=e.target.closest('[data-copy]'); if(!b) return; var u=b.closest('li').querySelector('a.lk').href;
  (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).catch(function(){ var t=document.createElement('textarea'); t.value=u; document.body.appendChild(t); t.select(); try{document.execCommand('copy');}catch(x){} t.remove(); }).then(function(){ var o=b.textContent; b.textContent='Copied ✓'; setTimeout(function(){b.textContent=o;},1400); }); });
$('#btnOut').addEventListener('click',function(){ out(''); });
$('#lf').addEventListener('submit',function(ev){ ev.preventDefault(); $('#lBtn').disabled=true; msg('');
  auth({email:$('#lEmail').value.trim(),password:$('#lPass').value},'password').then(function(j){ save(j); sess.email=$('#lEmail').value.trim(); return check(); }).then(show).catch(function(e){ out(''); msg(e.message); }).then(function(){ $('#lBtn').disabled=false; }); });
if(!LIVE){ $('#gate').hidden=false; msg('Supabase is not connected yet (see supabase/README.md).'); }
else { try{ sess=JSON.parse(localStorage.getItem(SK)||'null'); }catch(e){ sess=null; } if(sess) check().then(show,function(){ out(''); }); else $('#gate').hidden=false; }
})();
"""
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta name="robots" content="noindex,nofollow">\n'
        '<title>Teacher tools | Lincoln International Academy</title>\n' + icon_links('teacher/') + FONTS + '\n<script src="physics/lia-config.js"></script>\n<style>' + darkify(HUB_CSS + css_areas) +
        '.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px}.card h3{margin:0 0 .3em;font-size:1.25rem;color:var(--p)}.card p{margin:.2em 0 .8em;color:var(--muted)}'
        '.card .tag{display:inline-block;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--w);font-weight:600}'
        '.acts{display:flex;flex-wrap:wrap;gap:8px}.btn{display:inline-block;text-decoration:none;font:inherit;font-weight:600;font-size:.9rem;border-radius:8px;padding:7px 14px;border:1px solid var(--p);background:var(--p);color:var(--pi);cursor:pointer}'
        '.btn.ghost{background:transparent;color:var(--p)}.btn.sm{padding:3px 10px;font-size:.8rem;white-space:nowrap}details{margin-top:6px}summary{cursor:pointer;color:var(--p);font-weight:600}'
        'ul.lessons{list-style:none;margin:8px 0 0;padding:0}ul.lessons li{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--line)}'
        'ul.lessons b{display:block;font-weight:600;color:var(--ink);font-size:.95rem}ul.lessons a.lk{display:block;font-size:.74rem;color:var(--muted);word-break:break-all;text-decoration:none}'
        '.note{background:var(--soft);border-radius:10px;padding:12px 16px;margin:18px 0 0;color:var(--muted);font-size:.95rem}'
        '.login{max-width:420px;margin:30px auto;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:26px}.login label{display:block;font-weight:600;font-size:.9rem;margin:12px 0 4px}'
        '.login input{width:100%;font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}.login .btn{margin-top:16px;width:100%;background:var(--primary);border-color:var(--primary);color:var(--bg)}'
        '.err{margin-top:10px;color:#c0504a;font-weight:600}.who{margin-left:auto;font-size:.85rem;display:flex;gap:10px;align-items:center;color:#cfd8e6}.who button{font:inherit;background:none;color:inherit;border:1px solid rgba(255,255,255,.5);border-radius:8px;padding:2px 10px;cursor:pointer}'
        'header .wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px 20px}header .wrap>.hr{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center}'
        'header .tg{font:inherit;font-weight:600;font-size:.8rem;border-radius:8px;padding:4px 11px;cursor:pointer;background:transparent;color:#f3f0e9;border:1px solid rgba(255,255,255,.5)}'
        '.pv{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;background:var(--soft);border-radius:8px;padding:8px 12px;margin:0 0 .8em!important;color:var(--ink)!important;font-size:.9rem}.pv code{font:700 1.05rem ui-monospace,Menlo,Consolas,monospace;letter-spacing:.12em;color:var(--p)}</style>\n</head>\n<body>\n'
        '<header><div class="wrap"><div><div class="eyebrow">Teacher tools</div><div class="school">Lincoln International Academy</div></div>'
        '<div class="who" id="who" hidden><span id="whoMail"></span><button type="button" id="btnOut">Sign out</button></div></div></header>\n'
        '<main><div class="wrap">'
        '<div id="gate" hidden><form class="login" id="lf"><h2 style="margin:0">Teacher sign-in</h2><p style="color:var(--muted);margin:.2em 0 0">This area is for teachers only.</p>'
        '<label for="lEmail">E-mail</label><input id="lEmail" type="email" autocomplete="username" required><label for="lPass">Password</label><input id="lPass" type="password" autocomplete="current-password" required>'
        '<button class="btn" type="submit" id="lBtn">Sign in</button><div class="err" id="lErr" hidden></div></form></div>'
        '<div id="home" hidden><div class="grid">\n' + "\n".join(cards) + '\n</div>'
        '<p class="note"><b>Sharing with students:</b> there is no public student menu. Send each class the link to its lesson; the student signs in with their own code (one code per folder works for every lesson in it). '
        'A lesson that is not assigned to a student\'s grade and class stays closed to them.</p></div>'
        '</div></main>\n<script>' + js + '</script>\n' + THEME_JS + '</body>\n</html>\n')


if __name__ == "__main__":
    main()
