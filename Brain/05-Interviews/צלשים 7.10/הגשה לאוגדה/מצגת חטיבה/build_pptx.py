"""בונה את המצגת כקובץ PowerPoint.

כל שקף נשמר כתמונה חדה (פי 2), חוץ משקפי "מהלך הקרב": בהם המפה היא רקע,
והאירועים, החצים, הנקודות והשעון הם צורות של PowerPoint עם אנימציה. כל קליק מוסיף אירוע.

שימוש:  python3 build_pptx.py            -> כל המצגת
        python3 build_pptx.py --only-flow -> רק שקפי מהלך הקרב (לבדיקה מהירה)
דורש: Google Chrome, python-pptx.
"""
import json, re, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

import build_deck as b
from battle_maps import FLOW, FORCE

HERE = b.HERE
OUT = HERE / "מצגת חטיבת גבעתי - ועדת צלשים אוגדה 162.pptx"
IMG = HERE / "_pptx_img"
PX = 7620                       # EMU לפיקסל: שקף של 1600 פיקסלים = 13.333 אינץ׳
PT_PER_PX = 0.6                 # 1600 פיקסלים = 960 נקודות
FONT = "Arial"

INK, PURPLE, PURPLE3, GOLD, LAV, CREAM = "2A2230", "3A1752", "2C1040", "C9A24A", "F3EFF6", "F6F1E6"


def chrome_shot(html, out_png, budget=4000):
    f = Path(tempfile.mkstemp(suffix=".html", dir=HERE)[1])
    f.write_text(html, encoding="utf-8")
    try:
        subprocess.run([b.CHROME, "--headless", "--disable-gpu", f"--virtual-time-budget={budget}", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--window-size=1600,900", f"--screenshot={out_png}", f.as_uri()],
                       capture_output=True, timeout=120)
    finally:
        f.unlink()


def dump_dom(html):
    f = Path(tempfile.mkstemp(suffix=".html", dir=HERE)[1])
    f.write_text(html, encoding="utf-8")
    try:
        return subprocess.run([b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=4000", "--window-size=1600,900",
                               "--dump-dom", f.as_uri()], capture_output=True, text=True, timeout=120).stdout
    finally:
        f.unlink()


# ---------------------------------------------------------------- שקף המפה: רקע ומדידות
BG_CSS = """.mk, .zn, .ar { visibility: hidden; } .fstep { visibility: hidden; }
#m { position: absolute; left: -9999px; }"""

MEASURE_JS = """<pre id="m"></pre><script>
document.fonts.ready.then(function(){
 const svg = document.querySelector('.fmap'), M = svg.getScreenCTM();
 const P = (x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; const q = p.matrixTransform(M); return [q.x, q.y]; };
 const R = el => { const r = el.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; };
 const out = { box: R(document.querySelector('.fmapbox')), scale: M.a, steps: [], marks: [], arrows: [], zones: [] };
 document.querySelectorAll('.fstep').forEach(s => out.steps.push({ row: R(s), num: R(s.querySelector('.fnum')), txt: R(s.querySelector('div')) }));
 document.querySelectorAll('.mk').forEach(m => { const t = m.transform.baseVal.consolidate().matrix; out.marks.push({ step: +m.dataset.step, c: P(t.e, t.f) }); });
 document.querySelectorAll('.ar').forEach(g => { const d = g.querySelector('.arl').getAttribute('d');
   const pts = [...d.matchAll(/(-?[\\d.]+),(-?[\\d.]+)/g)].map(m => P(+m[1], +m[2]));
   out.arrows.push({ step: +g.dataset.step, dashed: g.dataset.dashed === '1', color: g.dataset.color, pts }); });
 document.querySelectorAll('.zn').forEach(z => { out.zones.push({ step: +z.dataset.step, c: P(+z.getAttribute('cx'), +z.getAttribute('cy')),
   r: +z.getAttribute('r') * M.a, color: z.getAttribute('stroke') }); });
 document.getElementById('m').textContent = JSON.stringify(out);
});</script>"""


def flow_page(key, extra_css, extra_html=""):
    css = (HERE / "deck.css").read_text(encoding="utf-8")
    sl = b.s_flow(key)
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{css}{extra_css}</style></head>'
            f'<body>{sl}{extra_html}</body></html>')


def measure_flow(key):
    dom = dump_dom(flow_page(key, BG_CSS, MEASURE_JS))
    m = re.search(r'<pre id="m">(.*?)</pre>', dom, re.S)
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))


# ---------------------------------------------------------------- עזרים ל-PowerPoint
def rgb(h):
    return RGBColor.from_string(h.lstrip("#").upper())


def darker(h, k=0.72):
    h = h.lstrip("#")
    return "".join(f"{min(255, int(int(h[i:i + 2], 16) * k)):02X}" for i in (0, 2, 4))


def emu(px):
    return Emu(int(round(px * PX)))


def set_text(shape, paras, anchor=MSO_ANCHOR.TOP, margin=0):
    """paras: רשימה של פסקאות, כל אחת רשימה של (טקסט, גודל בפיקסלים, צבע, מודגש?). עברית, מימין לשמאל."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = emu(margin)
    for i, runs in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        pPr.set("rtl", "1")
        pPr.set("algn", "ctr" if anchor == MSO_ANCHOR.MIDDLE and len(paras) and shape.width < emu(220) else "r")
        for text, size, color, bold in runs:
            r = p.add_run()
            r.text = text
            rPr = r._r.get_or_add_rPr()
            rPr.set("lang", "he-IL")
            rPr.set("altLang", "en-US")
            rPr.set("sz", str(int(round(size * PT_PER_PX * 100))))
            if bold:
                rPr.set("b", "1")
            sf = etree.SubElement(rPr, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr")).set("val", color)
            for tag in ("a:latin", "a:cs"):
                etree.SubElement(rPr, qn(tag)).set("typeface", FONT)


def no_shadow(shape):
    # בלי <p:style> של ערכת הנושא: אחרת חלק מהתוכנות מוסיפות צל ומסגרת ברירת מחדל
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)
    sp = shape._element.spPr
    if sp.find(qn("a:effectLst")) is None:
        etree.SubElement(sp, qn("a:effectLst"))


def style(shape, fill=None, fill_alpha=None, line=None, line_px=0, dash=None, name=None):
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
        if fill_alpha is not None:
            clr = shape._element.spPr.find(qn("a:solidFill"))[0]
            etree.SubElement(clr, qn("a:alpha")).set("val", str(int(fill_alpha * 100000)))
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = rgb(line)
        shape.line.width = emu(line_px)
        if dash:
            ln = shape._element.spPr.find(qn("a:ln"))
            etree.SubElement(ln, qn("a:prstDash")).set("val", dash)
    else:
        shape.line.fill.background()
    no_shadow(shape)
    if name:
        shape.name = name
    return shape


def polyline(slide, pts, color, width_px, dash=None, arrow=True, name=None):
    fb = slide.shapes.build_freeform(emu(pts[0][0]), emu(pts[0][1]), scale=1.0)
    fb.add_line_segments([(emu(x), emu(y)) for x, y in pts[1:]], close=False)
    shp = fb.convert_to_shape()
    style(shp, None, line=color, line_px=width_px, dash=dash, name=name)
    ln = shp._element.spPr.find(qn("a:ln"))
    ln.set("cap", "rnd")
    etree.SubElement(ln, qn("a:round"))
    if arrow:
        etree.SubElement(ln, qn("a:tailEnd")).set("type", "triangle")
        ln[-1].set("w", "med"); ln[-1].set("len", "med")
    return shp


# ---------------------------------------------------------------- אנימציות (OOXML)
class Timeline:
    """רצף קליקים. בכל קליק כמה אפקטים במקביל, כל אחד עם השהיה משלו."""

    def __init__(self):
        self.clicks, self.ids, self.shapes = [], 3, set()

    def nid(self):
        self.ids += 1
        return self.ids

    def click(self):
        self.clicks.append([])

    def add(self, kind, spid, delay=0, dur=500, sub=None):
        self.clicks[-1].append((kind, spid, delay, dur, sub))
        self.shapes.add(spid)

    def _effect(self, kind, spid, delay, dur, sub, first):
        node = "clickEffect" if first else "withEffect"
        tgt = f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>'
        vis = (f'<p:set><p:cBhvr><p:cTn id="{self.nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
               f'{tgt}<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>')
        if kind == "fade":
            pid, cls, st, body = 10, "entr", 0, vis + (f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>'
                                                      f'{tgt}</p:cBhvr></p:animEffect>')
        elif kind == "wipe":
            filt, st = sub
            pid, cls, body = 22, "entr", vis + (f'<p:animEffect transition="in" filter="{filt}"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>'
                                                f'{tgt}</p:cBhvr></p:animEffect>')
        elif kind == "zoom":
            def an(attr):
                return (f'<p:anim calcmode="lin" valueType="num"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}" fill="hold"/>{tgt}'
                        f'<p:attrNameLst><p:attrName>{attr}</p:attrName></p:attrNameLst></p:cBhvr><p:tavLst>'
                        f'<p:tav tm="0"><p:val><p:strVal val="0"/></p:val></p:tav>'
                        f'<p:tav tm="100000"><p:val><p:strVal val="#{attr}"/></p:val></p:tav></p:tavLst></p:anim>')
            pid, cls, st = 53, "entr", 16
            body = vis + an("ppt_w") + an("ppt_h") + (f'<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>'
                                                      f'{tgt}</p:cBhvr></p:animEffect>')
        elif kind == "out":
            pid, cls, st = 10, "exit", 0
            body = (f'<p:animEffect transition="out" filter="fade"><p:cBhvr><p:cTn id="{self.nid()}" dur="{dur}"/>{tgt}</p:cBhvr></p:animEffect>'
                    f'<p:set><p:cBhvr><p:cTn id="{self.nid()}" dur="1" fill="hold"><p:stCondLst><p:cond delay="{dur - 1}"/></p:stCondLst></p:cTn>'
                    f'{tgt}<p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="hidden"/></p:to></p:set>')
        return (f'<p:par><p:cTn id="{self.nid()}" presetID="{pid}" presetClass="{cls}" presetSubtype="{st}" fill="hold" grpId="0" nodeType="{node}">'
                f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>{body}</p:childTnLst></p:cTn></p:par>')

    def xml(self):
        clicks = []
        for effs in self.clicks:
            outer, inner = self.nid(), self.nid()
            body = "".join(self._effect(*e, first=(i == 0)) for i, e in enumerate(effs))
            clicks.append(f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
                          f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{body}'
                          f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
        bld = "".join(f'<p:bldP spid="{s}" grpId="0" animBg="1"/>' for s in sorted(self.shapes))
        return ('<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
                '<p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
                '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
                + "".join(clicks) +
                '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
                '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
                f'</p:childTnLst></p:cTn></p:par></p:tnLst><p:bldLst>{bld}</p:bldLst></p:timing>')


def wipe_dir(pts):
    dx, dy = pts[-1][0] - pts[0][0], pts[-1][1] - pts[0][1]
    if abs(dx) >= abs(dy):
        return ("wipe(right)", 8) if dx > 0 else ("wipe(left)", 2)
    return ("wipe(down)", 1) if dy > 0 else ("wipe(up)", 4)


# ---------------------------------------------------------------- בניית שקף המפה
def add_flow_slide(prs, key, bg_png):
    f, m = FLOW[key], measure_flow(key)
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(str(bg_png), 0, 0, prs.slide_width, prs.slide_height).name = "רקע: מפה"
    tl = Timeline()
    steps = f["steps"]
    box = m["box"]

    # שעונים: אחד לכל מצב. הראשון ("7.10 בוקר") גלוי מההתחלה
    cw, ch = 170, 70
    cx, cy = box[0] + box[2] - 22 - cw, box[1] + 18
    clocks = []
    for i in range(len(steps) + 1):
        sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, emu(cx), emu(cy), emu(cw), emu(ch))
        style(sh, PURPLE3, .88, GOLD, 1.5, name=f"שעון {i}")
        sh.adjustments[0] = 0.14
        top_txt, sub = ("7.10", "בוקר") if i == 0 else (steps[i - 1][2], f"אירוע {i} מתוך {len(steps)}")
        set_text(sh, [[(top_txt, 30 if len(top_txt) < 9 else 24, GOLD, True)], [(sub, 13, "E4DCEF", False)]], MSO_ANCHOR.MIDDLE, 4)
        for p in sh.text_frame.paragraphs:
            p._p.get_or_add_pPr().set("algn", "ctr")
        clocks.append(sh)

    by_step = lambda lst, i: [a for a in lst if a["step"] == i]
    on_top = list(clocks)   # נקודות ושעונים מעל כל החצים
    for i, (_pt, fk, when, txt, approx) in enumerate(steps, 1):
        c = FORCE[fk][1].lstrip("#").upper()
        row, num, tx = m["steps"][i - 1]["row"], m["steps"][i - 1]["num"], m["steps"][i - 1]["txt"]
        # הדגשת האירוע הנוכחי ברשימה
        hl = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, emu(row[0] - 8), emu(row[1] - 4), emu(row[2] + 16), emu(row[3] + 8))
        style(hl, LAV, name=f"הדגשה {i}")
        hl.adjustments[0] = 0.12
        # מספר ברשימה
        nb = s.shapes.add_shape(MSO_SHAPE.OVAL, emu(num[0]), emu(num[1]), emu(num[2]), emu(num[3]))
        style(nb, PURPLE3 if approx else c, line=c, line_px=3, name=f"מספר ברשימה {i}")
        set_text(nb, [[(str(i), 15, c if approx else PURPLE3, True)]], MSO_ANCHOR.MIDDLE, 0)
        # הטקסט ברשימה
        tb = s.shapes.add_textbox(emu(tx[0]), emu(tx[1]), emu(tx[2]), emu(tx[3] + 6))
        tb.name = f"אירוע {i}"
        tcol = "8A7F93" if fk == "civ" else darker(c)
        set_text(tb, [[(when, 15, PURPLE, True), (" · ", 15, INK, False), (FORCE[fk][0], 15, tcol, True)],
                      [(txt, 15, INK, False)]])
        # על המפה: אזור, חצים, נקודה
        zs = []
        for z in by_step(m["zones"], i):
            zz = s.shapes.add_shape(MSO_SHAPE.OVAL, emu(z["c"][0] - z["r"]), emu(z["c"][1] - z["r"]), emu(2 * z["r"]), emu(2 * z["r"]))
            zs.append(style(zz, c, .2, c, 2, "dash", name=f"אזור {i}"))
        ars = []
        for a in by_step(m["arrows"], i):
            under = polyline(s, a["pts"], PURPLE3, 9 * m["scale"], arrow=False, name=f"צל חץ {i}")
            line = polyline(s, a["pts"], c, 5 * m["scale"], dash="dash" if a["dashed"] else None, name=f"חץ {i}")
            ars.append((under, line, wipe_dir(a["pts"])))
        for mk in by_step(m["marks"], i):
            r = 17 * m["scale"]
            mo = s.shapes.add_shape(MSO_SHAPE.OVAL, emu(mk["c"][0] - r), emu(mk["c"][1] - r), emu(2 * r), emu(2 * r))
            style(mo, PURPLE3 if approx else c, line=c, line_px=3.5 * m["scale"], name=f"נקודה {i}")
            set_text(mo, [[(str(i), 19 * m["scale"], c if approx else PURPLE3, True)]], MSO_ANCHOR.MIDDLE, 0)
            mark = mo

        tl.click()
        tl.add("out", clocks[i - 1].shape_id, 0, 250)
        tl.add("fade", clocks[i].shape_id, 0, 400)
        if i > 1:
            tl.add("out", hl_prev.shape_id, 0, 300)
        tl.add("fade", hl.shape_id, 0, 400)
        tl.add("fade", nb.shape_id, 0, 400)
        tl.add("fade", tb.shape_id, 100, 500)
        t = 250
        for zz in zs:
            tl.add("zoom", zz.shape_id, t, 700)
        for under, line, wd in ars:
            tl.add("wipe", under.shape_id, t, 1500, wd)
            tl.add("wipe", line.shape_id, t, 1500, wd)
        if ars:
            t += 1400
        tl.add("zoom", mark.shape_id, t, 500)
        hl_prev = hl
        on_top.append(mark)

    tree = s.shapes._spTree
    for sh in on_top:
        tree.remove(sh._element)
        tree.append(sh._element)
    # התזמון בא אחרי cSld ו-clrMapOvr, ולפני extLst אם יש. השעון הראשון גלוי מההתחלה, ולכן יש לו רק יציאה
    sld, tm = s._element, etree.fromstring(tl.xml())
    ext = sld.find(qn("p:extLst"))
    (ext.addprevious(tm) if ext is not None else sld.append(tm))
    s.notes_slide.notes_text_frame.text = (f'{f["title"]}: מהלך הקרב. כל קליק מוסיף אירוע ({len(steps)} אירועים). '
                                           f'{f["note"]} מפה: OpenStreetMap contributors.')
    return s


# ---------------------------------------------------------------- כל המצגת
def render_all():
    IMG.mkdir(exist_ok=True)
    slides = b.build_slides()
    css = (HERE / "deck.css").read_text(encoding="utf-8")
    jobs = []
    for i, sl in enumerate(slides, 1):
        html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head>'
                f'<body>{sl}<script>document.querySelectorAll(".pg").forEach(p=>p.textContent="{i}")</script></body></html>')
        jobs.append((html, IMG / f"s{i:03d}.png"))
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(lambda j: chrome_shot(*j), jobs))
    return slides


def to_jpg(png):
    jpg = png.with_suffix(".jpg")
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", str(png), "--out", str(jpg)], capture_output=True)
    return jpg


def main():
    only_flow = "--only-flow" in sys.argv
    prs = Presentation()
    prs.slide_width, prs.slide_height = emu(1600), emu(900)
    flow_keys = {}
    if only_flow:
        slides = b.build_slides()
    else:
        slides = render_all()
    for i, sl in enumerate(slides, 1):
        k = next((k for k in FLOW if 'class="body flow"' in sl and f'{FLOW[k]["title"]}, {FLOW[k]["when"]}' in sl), None)
        if k:
            flow_keys[i] = k
    IMG.mkdir(exist_ok=True)
    for i, k in flow_keys.items():
        png = IMG / f"flow_{k}.png"
        page = flow_page(k, BG_CSS).replace('<span class="pg"></span>', f'<span class="pg">{i}</span>')
        chrome_shot(page, png)
    for i, sl in enumerate(slides, 1):
        if i in flow_keys:
            add_flow_slide(prs, flow_keys[i], to_jpg(IMG / f"flow_{flow_keys[i]}.png"))
        elif not only_flow:
            s = prs.slides.add_slide(prs.slide_layouts[6])
            s.shapes.add_picture(str(to_jpg(IMG / f"s{i:03d}.png")), 0, 0, prs.slide_width, prs.slide_height)
    out = OUT if not only_flow else HERE / "_flow_test.pptx"
    prs.save(out)
    print("ok", out.name, len(prs.slides._sldIdLst), "slides", f"{out.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
