import json, html, pathlib
HERE = pathlib.Path(__file__).parent
TEACHER = "Nathaly López"
CSS = (HERE / "engine.css").read_text()
JS = (HERE / "engine.js").read_text()

def svg(inner, vb="0 0 100 100", label="", w=120):
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" width="%d" role="img" aria-label="%s">%s</svg>' % (vb, w, html.escape(label, quote=True), inner)

# ---- pictures (simplified drawings) ----
def _emblem_inner():
    """Coat of arms of Nicaragua, simplified but faithful: ring with the country name, triangle with five volcanoes,
    sea, rainbow, sunrays and the Phrygian cap on a pole. Drawn in a 200x200 box."""
    rays = ''.join('<line x1="100" y1="72" x2="%.1f" y2="%.1f" stroke="#f2c230" stroke-width="2.4"/>' % (100 + 52 * __import__('math').cos(__import__('math').radians(a)), 72 - 52 * __import__('math').sin(__import__('math').radians(a))) for a in range(20, 161, 14))
    bows = ''.join('<path d="M%d 100a%d %d 0 0 1 %d 0" fill="none" stroke="%s" stroke-width="3.2"/>' % (100 - r, r, r, 2 * r, c) for r, c in ((34, "#d8322b"), (31, "#f28c28"), (28, "#f2d12b"), (25, "#3f9b4a"), (22, "#2f7fd0"), (19, "#7d4ca8")))
    return (
        '<defs><clipPath id="gvTri"><polygon points="100,40 44,136 156,136"/></clipPath>'
        '<path id="gvTop" d="M22 100a78 78 0 0 1 156 0"/><path id="gvBot" d="M30 100a70 70 0 0 0 140 0"/></defs>'
        '<circle cx="100" cy="100" r="97" fill="#fbf3d0" stroke="#b8901e" stroke-width="3"/><circle cx="100" cy="100" r="62" fill="#fffaf0" stroke="#b8901e" stroke-width="2"/>'
        '<text font-family="Arial,sans-serif" font-size="13.5" font-weight="700" fill="#5b4208" letter-spacing="1.6"><textPath href="#gvTop" startOffset="50%" text-anchor="middle">REPÚBLICA DE NICARAGUA</textPath></text>'
        '<text font-family="Arial,sans-serif" font-size="13.5" font-weight="700" fill="#5b4208" letter-spacing="1.6"><textPath href="#gvBot" startOffset="50%" text-anchor="middle" dominant-baseline="hanging">AMÉRICA CENTRAL</textPath></text>'
        '<g clip-path="url(#gvTri)"><rect x="40" y="36" width="120" height="104" fill="#bfe4f5"/>' + rays +
        '<rect x="40" y="119" width="120" height="20" fill="#1e72b8"/><path d="M44 126q8-4 16 0t16 0 16 0 16 0 16 0 16 0" fill="none" stroke="#7cc0ea" stroke-width="1.6"/>'
        '<g fill="#3d6a3b" stroke="#27492a" stroke-width="1"><polygon points="52,121 68,99 84,121"/><polygon points="78,121 93,92 108,121"/><polygon points="102,121 117,94 132,121"/><polygon points="124,121 138,101 152,121"/><polygon points="90,121 104,104 118,121"/></g>'
        '<g fill="none" stroke="#e8e8e8" stroke-width="1.4" opacity=".85"><path d="M93 92q3-6 0-10M117 94q3-6 0-10"/></g>' + bows +
        '<line x1="100" y1="100" x2="100" y2="64" stroke="#7a5a2a" stroke-width="2.2"/>'
        '<path d="M87 76c1-14 13-20 24-15-5 1-6 5-4 9 3 6-1 9-9 9-5 0-10-1-11-3z" fill="#d8322b" stroke="#8c1a16" stroke-width="1"/><path d="M87 76c2 3 11 4 20 1" fill="none" stroke="#fff" stroke-width="2"/></g>'
        '<polygon points="100,40 44,136 156,136" fill="none" stroke="#1d6b3a" stroke-width="3.2" stroke-linejoin="round"/>')

def coat():
    return svg(_emblem_inner(), "0 0 200 200", "Coat of arms of Nicaragua, simplified: a ring with the name of the country, and a triangle with five volcanoes, a rainbow, the sun's rays and a Phrygian cap", 170)

def flag():
    return svg('<rect x="1" y="1" width="148" height="88" fill="#fff" stroke="#9a9a9a"/><rect x="1" y="1" width="148" height="29" fill="#0f5fb8"/><rect x="1" y="60" width="148" height="29" fill="#0f5fb8"/>'
               '<svg x="58.5" y="30.5" width="33" height="33" viewBox="0 0 200 200">' + _emblem_inner() + '</svg>',
               "0 0 150 90", "Flag of Nicaragua, simplified: blue, white, blue horizontal stripes with the coat of arms in the center", 200)

def stop():
    return svg('<polygon points="30,6 70,6 94,30 94,70 70,94 30,94 6,70 6,30" fill="#c0262d" stroke="#fff" stroke-width="3"/><text x="50" y="58" font-size="26" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif">STOP</text>', label="Stop sign")
def yield_():
    return svg('<polygon points="8,12 92,12 50,90" fill="#fff" stroke="#c0262d" stroke-width="9" stroke-linejoin="round"/>', label="Yield sign: a downward-pointing triangle with a red border")
def diamond(sym, label):
    return svg('<polygon points="50,4 96,50 50,96 4,50" fill="#f7c81e" stroke="#111" stroke-width="3"/>' + sym, label=label)
def kids():
    return diamond('<g fill="#111"><circle cx="40" cy="32" r="5"/><path d="M40 38v18M33 44l7 4 7-4M40 56l-6 14M40 56l6 14"/><circle cx="60" cy="38" r="4"/><path d="M60 43v14M54 49l6 3 6-3M60 57l-5 12M60 57l5 12"/></g>'.replace('<path','<path stroke="#111" stroke-width="3" fill="none"'), "Yellow diamond warning sign: children crossing (school zone)")
def curve():
    return diamond('<path d="M40 76c0-14 20-14 20-28s-20-14-20-28" fill="none" stroke="#111" stroke-width="7" stroke-linecap="round"/>', "Yellow diamond warning sign: winding road ahead")
def round_sign(inner, label, border="#c0262d"):
    return svg('<circle cx="50" cy="50" r="44" fill="#fff" stroke="%s" stroke-width="9"/>' % border + inner, label=label)
def speed(n):
    return round_sign('<text x="50" y="62" font-size="38" font-weight="800" text-anchor="middle" fill="#111" font-family="Arial,sans-serif">%s</text>' % n, "Regulatory sign: speed limit %s" % n)
def no_parking():
    return round_sign('<text x="50" y="66" font-size="46" font-weight="800" text-anchor="middle" fill="#111" font-family="Arial,sans-serif">P</text><line x1="22" y1="78" x2="78" y2="22" stroke="#c0262d" stroke-width="8"/>', "Regulatory sign: no parking")
def no_bikes():
    return round_sign(_bike("#111") + '<line x1="22" y1="78" x2="78" y2="22" stroke="#c0262d" stroke-width="8"/>', "Regulatory sign: bicycles prohibited")
def _bike(c):
    return ('<g fill="none" stroke="%s" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><circle cx="32" cy="60" r="10"/><circle cx="68" cy="60" r="10"/><path d="M32 60l12-20h16l8 20M44 40l10 20M40 34h8M58 34l2-6h6"/></g>' % c)
def blue_rect(inner, label):
    return svg('<rect x="6" y="14" width="88" height="72" rx="8" fill="#1760b8" stroke="#fff" stroke-width="3"/>' + inner, label=label)
def hospital():
    return blue_rect('<text x="50" y="68" font-size="52" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif">H</text>', "Informative sign: hospital")
def wheelchair():
    return blue_rect('<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle cx="46" cy="34" r="3" fill="#fff"/><path d="M46 42v14h14l6 14"/><circle cx="44" cy="64" r="11"/></g>', "Informative sign: wheelchair accessible place")
def airport():
    return svg('<rect x="4" y="22" width="92" height="56" rx="6" fill="#1760b8" stroke="#fff" stroke-width="3"/><text x="50" y="58" font-size="15" font-weight="800" text-anchor="middle" fill="#fff" font-family="Arial,sans-serif">AIRPORT</text>', label="Informative sign: airport")
def bike_lane():
    return blue_rect(_bike("#fff"), "Informative sign: bicycle path")
def ped_cross_blue():
    return blue_rect('<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle cx="50" cy="30" r="5" fill="#fff"/><path d="M50 38v20M40 48l10-4 10 4M50 58l-8 16M50 58l8 16"/></g>', "Informative sign: pedestrian crossing")
def traffic_light(on):
    cols = {"r": "#d63a2f", "y": "#e9b824", "g": "#2e9e5b"}
    c = ''.join('<circle cx="40" cy="%d" r="11" fill="%s" opacity="%s"/>' % (26 + 24*i, cols[k], 1 if k == on else .22) for i, k in enumerate("ryg"))
    return svg('<rect x="22" y="6" width="36" height="88" rx="10" fill="#222"/>' + c, "0 0 80 100", "Traffic light showing %s" % {"r": "red", "y": "yellow", "g": "green"}[on], 80)
def helmet():
    return svg('<path d="M14 62a36 36 0 0 1 72 0z" fill="#1f7a8c" stroke="#0b3d4a" stroke-width="3"/><path d="M14 62h72v8H14z" fill="#0b3d4a"/><path d="M30 28v34M50 24v38M70 28v34" stroke="#fff" stroke-width="3" opacity=".7"/>', label="Bicycle helmet")
def flower():
    petal = '<path d="M50 52C34 44 30 18 46 6C58 -1 70 16 62 36C58 46 54 50 50 52Z" fill="url(#gvPet)" stroke="#e3d3a6" stroke-width="1"/>'
    petals = ''.join('<g transform="rotate(%d 50 52)">%s</g>' % (a, petal) for a in range(0, 360, 72))
    return svg('<defs><radialGradient id="gvPet" cx="50%" cy="100%" r="100%"><stop offset="0" stop-color="#f6c93a"/><stop offset=".35" stop-color="#fbeec0"/><stop offset="1" stop-color="#fffdf6"/></radialGradient></defs>'
               '<g fill="#3f7f3a" stroke="#2c5c2a" stroke-width="1"><path d="M50 60C18 66 4 86 6 98 28 96 46 82 50 60Z"/><path d="M50 60C82 66 96 86 94 98 72 96 54 82 50 60Z"/></g>'
               + petals + '<circle cx="50" cy="52" r="6" fill="#f2b81f"/><circle cx="50" cy="52" r="2.6" fill="#e48a14"/>',
               label="Sacuanjoche flower (Plumeria rubra): five twisted cream-white petals with a yellow center, with green leaves, simplified drawing", w=120)

def tree():
    import math
    blobs = [(50, 30, 20), (30, 38, 16), (70, 38, 16), (40, 22, 14), (62, 22, 14), (22, 50, 11), (78, 50, 11), (50, 44, 15)]
    green = ''.join('<circle cx="%d" cy="%d" r="%d" fill="#5d8f45"/>' % b for b in blobs)
    flo = ''.join('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fbf5e1" stroke="#e6dcb8" stroke-width=".6"/>' % (b[0] + b[2] * .75 * math.cos(k * 1.7 + b[0]), b[1] + b[2] * .75 * math.sin(k * 1.9 + b[1]), 3 + (k % 3)) for b in blobs for k in range(6))
    return svg('<path d="M10 96H90" stroke="#8a6d3b" stroke-width="3"/><path d="M47 96C47 78 44 68 38 58M53 96C53 80 54 66 60 56M50 78C50 66 50 58 50 50M44 70C34 64 28 58 26 52M56 68C68 62 72 56 74 52" fill="none" stroke="#9c8f7a" stroke-width="4.5" stroke-linecap="round"/>'
               + green + flo, label="Madroño tree in flower: a pale smooth trunk and a crown covered with cream-white flowers among green leaves, simplified drawing", w=120)

def bird():
    return svg('<path d="M4 62C30 56 60 58 96 52" stroke="#7a5a35" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M92 52l8-6" stroke="#7a5a35" stroke-width="3" stroke-linecap="round"/>'
               # tail: long dark-green feathers with bare shaft ending in blue rackets
               '<path d="M44 66C30 80 22 92 14 104" stroke="#2c6e5a" stroke-width="3.2" fill="none" stroke-linecap="round"/><path d="M50 68C42 84 38 96 36 106" stroke="#2c6e5a" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
               '<ellipse cx="13" cy="106" rx="6" ry="3.4" transform="rotate(-55 13 106)" fill="#1e5fbf" stroke="#0b2f7a" stroke-width=".8"/><ellipse cx="36" cy="109" rx="6" ry="3.4" transform="rotate(-82 36 109)" fill="#1e5fbf" stroke="#0b2f7a" stroke-width=".8"/>'
               '<path d="M13 106l-3-2M36 109l1-3" stroke="#0b2f7a" stroke-width="1.4"/>'
               # body
               '<path d="M42 62C46 40 66 30 82 36C92 40 94 54 84 64C74 74 52 76 42 62Z" fill="#c9772f" stroke="#8a4d18" stroke-width="1"/>'
               '<path d="M60 60C58 46 70 38 84 42C80 56 72 66 60 60Z" fill="#5a9a6b" stroke="#2f6b46" stroke-width="1"/>'
               '<path d="M58 66C70 74 82 70 86 60C80 66 68 70 58 66Z" fill="#e2b265"/>'
               # head
               '<circle cx="88" cy="38" r="12.5" fill="#d98a38" stroke="#8a4d18" stroke-width="1"/><path d="M78 30C84 22 96 24 99 32C92 29 84 29 78 30Z" fill="#c9772f"/>'
               '<path d="M79 33C86 28 94 29 99 34" fill="none" stroke="#35c3d4" stroke-width="3.2" stroke-linecap="round"/>'
               '<path d="M80 38C86 35 94 36 99 40L96 45C90 42 84 43 80 42Z" fill="#171717"/><circle cx="92" cy="39" r="2" fill="#fff"/><circle cx="92.4" cy="39.2" r="1" fill="#171717"/>'
               '<path d="M98 38l14 5-14 5z" fill="#1c1c1c"/>'
               # black throat spot with turquoise edge
               '<ellipse cx="86" cy="58" rx="4.2" ry="3" fill="#171717" stroke="#35c3d4" stroke-width="1.2"/>'
               '<path d="M66 72l-3 8M74 72l-1 8" stroke="#5a4a36" stroke-width="2.2" stroke-linecap="round"/>',
               "0 0 120 120", "Guardabarranco (turquoise-browed motmot): cinnamon and green body, turquoise eyebrow, black eye mask and throat spot, and a long tail ending in two blue rackets, perched on a branch; simplified drawing", 150)

def hand_chest():
    return svg('<circle cx="50" cy="20" r="10" fill="#c98f5a"/><rect x="34" y="32" width="32" height="46" rx="8" fill="#2f6b8f"/><path d="M60 46l-10 10" stroke="#c98f5a" stroke-width="8" stroke-linecap="round"/><rect x="38" y="78" width="9" height="16" fill="#333"/><rect x="53" y="78" width="9" height="16" fill="#333"/>', label="A person standing straight with the right hand over the heart")

def js_dump(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")

def build(W, idx):
    """W: dict with slug, week, topic, eyebrow, title, guiding, target, learn_html, ideas, vocab, examples, acts, pages, indicator, source"""
    label = "Q02 Week %d: %s" % (W["week"], W["short"])
    G = {"slug": W["slug"], "label": label, "ideas": W["ideas"], "vocab": W["vocab"], "examples": W["examples"], "acts": W["acts"]}
    acts_main = [a for a in W["acts"] if not a.get("reflect")]
    acts_ref = [a for a in W["acts"] if a.get("reflect")]
    n = 0
    def card(a):
        nonlocal n; n += 1
        return '<div class="card act" id="%s"><h3>%d. %s <span class="done-mark">✓ Completed</span></h3><div class="mount"></div></div>' % (a["id"], n, html.escape(a["title"]))
    practice = "\n  ".join(card(a) for a in acts_main)
    reflect = "\n  ".join(card(a) for a in acts_ref)
    total = len(W["acts"])
    head = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(short)s | Lincoln International Academy</title>
<meta name="description" content="%(desc)s">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
%(css)s
</style>
</head>
<body>

<header class="top">
  <div class="wrap">
    <div>
      <p class="school">Lincoln International Academy</p>
      <p class="crumbs">Class: <strong>Growing in Values</strong> &nbsp;·&nbsp; Teacher: <strong>%(teacher)s</strong> &nbsp;·&nbsp; Lesson: <strong>%(short)s</strong></p>
    </div>
    <div class="meta">
      <span class="pill">8th Grade · Q02 Week %(week)d of 7</span>
      <span class="pill">Unit 2: We live in community with respect and responsibility</span>
      <button class="theme" id="themeBtn" type="button" aria-label="Toggle light or dark theme">Light / Dark</button>
    </div>
  </div>
</header>

<nav class="sticky" aria-label="Page sections">
  <div class="wrap">
    <a href="#learn">Learn</a>
    <a href="#vocab">Vocabulary</a>
    <a href="#examples">Worked examples</a>
    <a href="#practice">Practice</a>
    <a href="#reflect">Write &amp; reflect</a>
    <div class="progress-box" aria-live="polite"><span id="progText">0 of %(total)d activities</span><div class="bar"><i id="progBar"></i></div></div>
  </div>
</nav>

<main class="wrap">

<section class="sec" id="learn">
  <div class="eyebrow">%(eyebrow)s</div>
  <h2>%(title)s</h2>
  <div class="card soft">
    <h3>Guiding question</h3>
    <p><strong>%(guiding)s</strong></p>
    <div class="callout"><strong>Learning target:</strong> %(target)s</div>
    <p class="ref" style="margin:0">Unit indicator: %(indicator)s &nbsp;·&nbsp; Textbook: <em>Creciendo en Valores</em> 8, %(book)s</p>
  </div>
  %(learn)s
  <h3>Key ideas</h3>
  <p>Select each tab to read it. Say it in your own words before you move on.</p>
  <div class="card">
    <div class="tabs" role="tablist" aria-label="Key ideas" id="stageTabs"></div>
    <div id="stagePanel" class="tabpanel" role="tabpanel" aria-live="polite"></div>
  </div>
</section>

<section class="sec" id="vocab">
  <div class="eyebrow">Key vocabulary</div>
  <h2>Words to Know</h2>
  <p>Tap a card to flip it. Say the meaning in your own words before you flip!</p>
  <div class="grid g3" id="flips"></div>
</section>

<section class="sec" id="examples">
  <div class="eyebrow">Step by step</div>
  <h2>Worked Examples</h2>
  <p>Each example shows how to think it through. Press <strong>Show next step</strong> and try to predict the next step before you reveal it. The steps you opened are remembered.</p>
  %(method)s
  <div id="exampleList"></div>
</section>

<section class="sec" id="practice">
  <div class="eyebrow">Your turn</div>
  <h2>Practice with Instant Feedback</h2>
  <p>You get feedback right after every answer. Mistakes are part of learning, so use the explanations and try again. Everything you answer is saved to your account, so you can sign in from any device and continue.</p>
  %(practice)s
  <div class="card soft" id="summaryCta" style="display:none">
    <h3>All activities complete!</h3>
    <p>Great work. See how you did on each activity.</p>
    <button class="btn" type="button" id="openSummary">View my score summary</button>
  </div>
</section>

<section class="sec" id="reflect">
  <div class="eyebrow">In your own words</div>
  <h2>Write and Reflect</h2>
  <div class="callout warm"><strong>Your written answers are saved automatically</strong> and your teacher can read them. Write full sentences and use what you learned this week.</div>
  %(reflect)s
  <div class="card">
    <h3>Self-check</h3>
    <ul>%(selfcheck)s</ul>
  </div>
  <p style="text-align:center;font-size:1.3rem;font-weight:800;margin:22px 0"><em>%(motto)s</em></p>
</section>

</main>

<footer>
  <div class="wrap">
    Lincoln International Academy · Growing in Values · Ms. %(teacher)s · 8th Grade, Q02 Week %(week)d (Semester 1, Unit 2).
    <br>Based on the lesson plan "%(planTopic)s" and the textbook <em>Creciendo en Valores</em> 8 (%(book)s).
  </div>
</footer>

<div id="overlay" class="overlay" role="dialog" aria-modal="true" aria-labelledby="sumTitle" hidden>
  <div class="modal">
    <div class="eyebrow">Growing in Values · Week %(week)d</div>
    <h2 id="sumTitle">Your Score Summary</h2>
    <div class="bigscore" id="sumBig"></div>
    <p id="sumMsg"></p>
    <table class="cmp" id="sumTable"></table>
    <p class="ref">Scores count your latest try of each scored activity. Written activities show "Completed" when every answer is filled in.</p>
    <div class="row"><button class="btn" type="button" id="closeSummary">Close</button><button class="btn ghost" type="button" id="reviewBtn">Practice again</button></div>
  </div>
</div>

<script>
window.GV = %(G)s;
%(gens)s
</script>
<script>
%(js)s
</script>
</body>
</html>
'''
    return head % dict(
        short=html.escape(W["short"]), desc=html.escape(W["desc"], quote=True), css=CSS, teacher=TEACHER, week=W["week"], total=total,
        eyebrow=html.escape(W["eyebrow"]), title=html.escape(W["title"]), guiding=W["guiding"], target=W["target"], indicator=html.escape(W["indicator"]),
        book=html.escape(W["book"]), learn=W["learn"], method=W.get("method", ""), practice=practice, reflect=reflect,
        selfcheck="".join("<li>%s</li>" % s for s in W["selfcheck"]), motto=html.escape(W["motto"]), planTopic=html.escape(W["plan"]),
        G=js_dump(G), gens=W.get("gens", ""), js=JS)

def Q(q, o, e, svg=None, a=0):
    d = {"q": q, "o": o, "a": a, "e": e}
    if svg: d["svg"] = svg
    return d

def exit_acts(exit_prompts, reflect_q, model=None):
    """the two standard written activities at the end of every week"""
    return [
      {"id": "act-reflect", "type": "open", "reflect": True, "title": "Five-Line Reflection", "rtitle": "Reflection", "min": 25, "who": True,
       "intro": "Apply what you learned at home, at school or in your community.", "prompts": [{"q": reflect_q, "rows": 6}]},
      {"id": "act-exit", "type": "open", "reflect": True, "title": "Exit Ticket", "rtitle": "Exit ticket", "min": 20, "who": True,
       "intro": "Answer in your own words before you leave this page.", "prompts": [{"q": q, "rows": 4} for q in exit_prompts]},
    ]
