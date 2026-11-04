#!/usr/bin/env python3
"""Generates the Growing in Values weekly lesson pages (growing-in-values/gv8-q2-week-N-*.html).
   Content lives in weekN.py (one per week), the shared page engine in engine.js / engine.css, pictures in lib.py.
   Edit those, then:  python3 tools/gv/make.py [week numbers]   and   python3 tools/build_site.py
   (the generated .html files are committed; they are self-contained like every other lesson page).
   To add a new quarter: copy weekN.py, change slug/week/label text, add the file to the list in lib.build if needed."""
import sys, importlib, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.dont_write_bytecode = True
from lib import build
OUT = HERE.parent.parent / "growing-in-values"
weeks = [int(a) for a in sys.argv[1:]] or range(1, 8)
for n in weeks:
    try:
        m = importlib.import_module("week%d" % n)
    except ModuleNotFoundError as e:
        if e.name == "week%d" % n: continue
        raise
    (OUT / (m.W["slug"] + ".html")).write_text(build(m.W, n), encoding="utf8")
    print("wrote", m.W["slug"])
