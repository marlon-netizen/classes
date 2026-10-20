#!/usr/bin/env python3
"""Connect lesson pages to Supabase (student code sign-in + saved progress).

Usage
  python3 supabase/apply_to_pages.py                       # patch the default lesson pages
  python3 supabase/apply_to_pages.py --url https://xxxx.supabase.co --key YOUR_ANON_KEY
  python3 supabase/apply_to_pages.py some-new-page.html    # patch other pages built from the same template

What it does to each page (safe to run again – it never patches twice):
  * inserts the sign-in / sync module (supabase/lia-sync.snippet.html) into <head>
  * adds <meta name="lia-page" content="..."> – the key that progress is stored under
  * routes the page's progress load/save through the module
  * with --url/--key it also writes your project settings into every page
Pages that were not patched keep saving in the browser only.
"""
import argparse, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIPPET = (ROOT / "supabase" / "lia-sync.snippet.html").read_text(encoding="utf8")
DEFAULT_PAGES = {
    "physics-lesson-10-3.html": "lesson-10-3",
    "physics-lesson-2-2.html": "lesson-2-2",
    "physics-lesson-2-3.html": "lesson-2-3",
    "ap-stats-unit-2.html": "ap-stats-unit-2",
}
MARK = re.compile(r"<!--LIA-SUPABASE-START.*?<!--LIA-SUPABASE-END-->\n?", re.S)
CONFIG = re.compile(r"/\*LIA-CONFIG\*/.*?/\*END-LIA-CONFIG\*/", re.S)


def config_line(url, key):
    return "/*LIA-CONFIG*/window.LIA_CONFIG={url:%r,anonKey:%r};/*END-LIA-CONFIG*/" % (url, key)


def patch(path, page_key, url, key):
    s = path.read_text(encoding="utf8")
    snippet = SNIPPET
    if url and key:
        snippet = CONFIG.sub(lambda m: config_line(url, key), snippet)
    elif MARK.search(s):  # keep the settings already in the page
        old = CONFIG.search(MARK.search(s).group(0))
        if old:
            snippet = CONFIG.sub(lambda m: old.group(0), snippet)

    # 1) route the page's own progress code through the module (before the snippet is inserted,
    #    so the snippet's own code is never touched)
    s = MARK.sub("", s)
    if "LiaSync.start(function(){" not in s:
        reps = [
            ("try{ state=JSON.parse(localStorage.getItem(KEY))||{}; }catch(e){ state={}; }", "state=LiaSync.load(KEY);"),
            ("const save=()=>{ try{ localStorage.setItem(KEY,JSON.stringify(state)); }catch(e){} };", "const save=()=>LiaSync.save(KEY,state);"),
            ("(function(){\n'use strict';", "LiaSync.start(function(){\n'use strict';"),
            ("$('#overallText').textContent=", "LiaSync.summary(done,P.length);\n  $('#overallText').textContent="),
        ]
        for a, b in reps:
            if a not in s:
                sys.exit("%s: expected code not found: %s" % (path.name, a[:60]))
            s = s.replace(a, b, 1)
        s, n = re.subn(r"\}\)\(\);\s*</script>\s*</body>", "});\n</script>\n</body>", s)
        if n != 1:
            sys.exit("%s: could not find the end of the main script" % path.name)

    # 2) insert the module and the page key
    s = s.replace("</head>", snippet + "</head>", 1)
    s = re.sub(r'<meta name="lia-page"[^>]*>\n?', "", s)
    s = s.replace("<title>", '<meta name="lia-page" content="%s">\n<title>' % page_key, 1)
    path.write_text(s, encoding="utf8")
    print("patched", path.name, "->", page_key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="*")
    ap.add_argument("--url")
    ap.add_argument("--key")
    a = ap.parse_args()
    if bool(a.url) != bool(a.key):
        sys.exit("Give both --url and --key (or neither).")
    targets = {}
    for p in a.pages:
        name = pathlib.Path(p).name
        targets[name] = DEFAULT_PAGES.get(name) or re.sub(r"[^a-z0-9-]", "-", name.replace(".html", "").lower())
    if not targets:
        targets = DEFAULT_PAGES
    for name, key in targets.items():
        patch(ROOT / name, key, a.url, a.key)
    if a.url:  # the teacher admin page needs the same project settings
        admin = ROOT / "admin.html"
        t = admin.read_text(encoding="utf8")
        t = CONFIG.sub(lambda m: config_line(a.url, a.key), t, count=1)
        admin.write_text(t, encoding="utf8")
        print("configured admin.html")


if __name__ == "__main__":
    main()
