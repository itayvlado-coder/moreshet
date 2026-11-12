"""בונה תיק אירוע או תיק כוח לאוגדה, בעיצוב של תיקי המועמד האישיים.

שימוש: python build.py <קובץ נתונים .py או .json> [<קובץ נתונים נוסף> ...]
הקובץ נוצר בתיקייה שמוגדרת ב-"out" בקובץ הנתונים, יחד עם תמונות תצוגה מקדימה של העמודים.
"""
import html, json, pathlib, runpy, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TAG = {"קיים": "ok", "לבקש": "ask"}
CHECK_JS = """<div id="overflow"></div><script>
var bad=[];document.querySelectorAll('.page').forEach(function(pg,i){var f=pg.querySelector('.ftr'),b=pg.querySelector('.body');
if(!f||!b)return;var lim=f.getBoundingClientRect().top-2,m=0;b.querySelectorAll('*').forEach(function(el){m=Math.max(m,el.getBoundingClientRect().bottom);});
if(m>lim)bad.push(i+1);});document.getElementById('overflow').textContent=bad.join(',');</script>"""

def e(s):
    return html.escape(str(s or ""))

def tag(s):
    return f'<span class="tag {TAG.get(s, "ask")}">{e(s)}</span>' if s else ""

WAVES = """<svg class="waves" viewBox="0 0 210 297" preserveAspectRatio="none">
<g fill="none" stroke="#ffffff" stroke-opacity="0.09" stroke-width="0.35">
<path d="M0 22 C40 12 80 34 120 20 S180 8 210 16"/><path d="M0 30 C45 20 85 42 125 28 S185 16 210 24"/>
<path d="M0 262 C40 252 80 274 120 260 S180 248 210 256"/><path d="M0 271 C45 261 85 283 125 269 S185 257 210 265"/>
<path d="M0 280 C40 270 80 292 120 278 S180 266 210 274"/></g></svg>"""

def cover(d):
    stats = "".join(f'<div class="stat"><b{"" if any("\u0590" <= c <= "\u05ff" for c in n) else " dir=ltr"}>{e(n)}</b><span>{e(l)}</span></div>' for n, l in d["stats"])
    toc = "".join(f"<div><b>{i}</b>{e(t)}</div>" for i, t in enumerate(d["toc"], 1))
    return f"""<section class="page cover">{WAVES}<div class="inner">
<div class="classif">- שמור -</div>
<div class="badge"><figure><img src="img/givati.png"><figcaption>חטיבת גבעתי</figcaption></figure>
<figure><img src="img/ugda162.png"><figcaption>אוגדה 162</figcaption></figure></div>
<div class="brigade">חטיבת גבעתי</div><div class="war">מלחמת חרבות ברזל</div><div class="rule"></div>
<div class="kind">{e(d["kind"])}</div><div class="title">{e(d["title"])}</div>
<div class="subtitle">{e(d["subtitle"])}</div><div class="pill">{e(d["pill"])}</div>
<div class="dateline">{e(d["dateline"])}</div><div class="stats">{stats}</div>
<div class="toc">{toc}</div><div class="foot">{e(d["footline"])}</div></div></section>"""

def block(b):
    t = b["t"]
    if t == "section":
        return f'<div class="sec"><div class="n">{b["n"]}</div><h2>{e(b["title"])}</h2><div class="ln"></div></div>'
    if t == "sub":
        return f'<div class="sub"><h3>{e(b["h"])}</h3><p>{e(b["p"])}</p></div>'
    if t == "subquote":
        inner = "".join(f'<div class="sub"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in b["items"])
        return (f'<div class="subq"><div class="txt">{inner}</div><div class="quote"><b>"{e(b["quote"])}"</b>'
                f'<span>{e(b["cap"])}</span></div></div>')
    if t == "p":
        return f'<p class="p">{e(b["p"])}</p>'
    if t == "timeline":
        rows = "".join(
            f'<tr class="{"hl" if r.get("hl") else ""}"><td class="when">{e(r["when"])}</td><td class="where">{e(r["where"])}</td>'
            f'<td>{e(r["what"])}</td><td class="doc">{e(r.get("doc"))} {tag(r.get("status"))}</td></tr>' for r in b["rows"])
        return ('<table class="tl"><tr><th style="width:15%">שעה</th><th style="width:15%">מקום</th><th>מה קרה</th>'
                f'<th style="width:19%">תיעוד</th></tr>{rows}</table>')
    if t == "table":
        head = "".join(f'<th style="width:{w}">{e(c)}</th>' if w else f"<th>{e(c)}</th>" for c, w in zip(b["cols"], b.get("widths", [""] * len(b["cols"]))))
        cls = b.get("classes", [""] * len(b["cols"]))
        rows = "".join("<tr>" + "".join(f'<td class="{c}">{e(v)}</td>' for v, c in zip(r, cls)) + "</tr>" for r in b["rows"])
        return f'<table class="tl{" compact" if b.get("compact") else ""}"><tr>{head}</tr>{rows}</table>'
    if t == "cards":
        st = f' style="grid-template-columns: repeat({b["cols"]}, 1fr)"' if b.get("cols") else ""
        return f'<div class="cards"{st}>' + "".join(f'<div class="card"><h4>{e(h)}</h4><p>{e(p)}</p></div>' for h, p in b["items"]) + "</div>"
    if t == "docs":
        return '<div class="docs">' + "".join(
            f'<div class="doc"><div class="ph">מקום לצילום</div><div class="cap"><b>{e(h)}</b><span>{e(p)}</span> {tag(s)}</div></div>'
            for h, p, s in b["items"]) + "</div>"
    if t == "witnesses":
        return f'<div class="wit"><h3>עדים</h3><ul>' + "".join(f"<li>{e(w)}</li>" for w in b["items"]) + "</ul></div>"
    if t == "note":
        return f'<p class="note">{e(b["p"])}</p>'
    if t == "criteria":
        return '<div class="crit">' + "".join(f'<div><h4>{e(h)}</h4><p>{e(p)}</p></div>' for h, p in b["items"]) + "</div>"
    if t == "reco":
        return f'<div class="reco"><div class="lab">{e(b.get("label", "המלצה"))}</div><p>{e(b["p"])}</p></div>'
    if t == "sign":
        return '<div class="sign"><div>שם המפקד הממליץ (אל"מ לפחות)</div><div>תפקיד</div><div>חתימה ותאריך</div></div>'
    if t == "gap":
        return '<div class="gap"></div>'
    raise ValueError(t)

def build(path):
    d = runpy.run_path(str(path))["D"] if str(path).endswith(".py") else json.loads(pathlib.Path(path).read_text())
    total = len(d["pages"]) + 1
    pages = [cover(d)]
    for i, pg in enumerate(d["pages"], 2):
        body = "".join(block(b) for b in pg)
        pages.append(f"""<section class="page"><div class="hdr"><div><div class="t1">{e(d["header"])}</div>
<div class="t2">{e(d["header2"])}</div></div><img src="img/givati-small.png"></div><div class="body">{body}</div>
<div class="ftr"><span>{e(d["kind"])} · {e(d["short"])}</span><span>עמוד {i} מתוך {total} · שמור</span></div></section>""")
    doc = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body>{"".join(pages)}</body></html>'
    tmp = HERE / "_render.html"
    tmp.write_text(doc)
    out = (pathlib.Path(path).resolve().parent / d["out"]).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                    f"--print-to-pdf={out}", tmp.as_uri()], capture_output=True)
    check = tmp.read_text().replace("</body>", CHECK_JS + "</body>")
    tmp.write_text(check)
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=4000", "--dump-dom", tmp.as_uri()],
                         capture_output=True, text=True).stdout
    tmp.unlink()
    bad = dom.split('id="overflow">')[1].split("<")[0] if 'id="overflow">' in dom else "?"
    print(out.name, out.exists(), f"{total} עמודים", "· גלישה בעמודים: " + (bad or "אין"))
    return out

if __name__ == "__main__":
    for p in sys.argv[1:]:
        build(p)
