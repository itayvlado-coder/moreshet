"""שקפים סטטיים להדפסה: מהלך הקרב בכל זירה, בארבעה שלבים.

לכל זירה שקף אחד עם ארבע מפות קטנות. כל מפה מראה את הקרב עד סוף השלב שלה:
האירועים של השלב בצבע מלא, אירועים משלבים קודמים חיוורים, ואירועים מאוחרים לא מופיעים.
ליד כל מפה: השעות של השלב, והאירועים שלו בקצרה.

שימוש:  python3 build_print.py
נוצר:   "מהלך הקרב בשלבים - שקפים להדפסה.pdf" (שקף לכל זירה, 1600x900, כמו המצגת)
"""
import subprocess
import build_deck as b
from battle_maps import FLOW, FORCE, flow_svg, _proj

OUT_PDF = b.HERE / "מהלך הקרב בשלבים - שקפים להדפסה.pdf"
ORDER = ["sderot", "kfaraza", "nahaloz", "nova", "kissufim", "north", "south", "ofakim"]
PANELS = 4
MAP_W = 560          # רוחב ה-viewBox של המפה הקטנה. הסימנים והכיתוב יוצאים גדולים יחסית
BOX_W, BOX_H = 440, 296   # המקום של המפה בתוך כל שלב

PRINT_CSS = """
.ph-grid { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 16px 22px; padding: 18px 56px 0; height: 690px; }
.ph { display: grid; grid-template-columns: 1fr auto; gap: 14px; background: #fff; border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; }
.ph-map { grid-column: 2; grid-row: 1; width: 440px; height: 296px; display: flex; align-items: center; justify-content: center;
  background: #2c1040; border-radius: 8px; overflow: hidden; line-height: 0; }
.ph-map svg { display: block; font-family: "Heebo", sans-serif; }
.ph-map .fl { fill: #f6f1e6; font-size: 15px; font-weight: 700; paint-order: stroke; stroke: #2c1040; stroke-width: 4px; }
.ph-map .fn { font-size: 18px; font-weight: 900; }
.ph-map .fs { fill: #e4dcef; font-size: 12px; paint-order: stroke; stroke: #2c1040; stroke-width: 3px; }
.ph-map .fnorth { fill: #e4dcef; font-size: 13px; font-weight: 800; }
.ph-map .pulse { display: none; }
.ph-txt { grid-column: 1; grid-row: 1; min-width: 0; display: flex; flex-direction: column; gap: 6px; overflow: hidden; }
.ph-h { display: flex; align-items: baseline; gap: 8px; border-bottom: 1px solid var(--line); padding-bottom: 5px; margin-bottom: 2px; }
.ph-h b { font-size: 16px; color: var(--purple); }
.ph-h span { font-size: 14px; color: var(--muted); font-weight: 700; }
.ph-ev { display: grid; grid-template-columns: 24px 1fr; gap: 7px; font-size: 12.6px; line-height: 1.38; }
.ph-ev .n { width: 22px; height: 22px; border-radius: 50%; border: 2.5px solid var(--c); background: var(--c); color: var(--purple3);
  font-weight: 900; font-size: 12px; display: flex; align-items: center; justify-content: center; }
.ph-ev .n.ap { background: var(--purple3); color: var(--c); }
.ph-ev b { color: var(--purple); } .ph-ev i { font-style: normal; font-weight: 700; }
.ph-foot { position: absolute; bottom: 60px; align-items: flex-end; left: 56px; right: 56px; display: flex; justify-content: space-between; gap: 20px; font-size: 13px; color: var(--muted); }
.ph-foot .ph-lg { font-size: 13px; font-weight: 400; display: flex; flex-wrap: wrap; gap: 4px 14px; }
.ph-foot .ph-lg i { display: inline-block; width: 16px; height: 5px; border-radius: 3px; margin-left: 5px; vertical-align: middle; outline: 1px solid #b9aac7; }
.ph-foot .nt { text-align: left; max-width: 760px; }
"""


def groups(n):
    """חלוקה מאוזנת של n אירועים ל-4 שלבים, לפי הסדר. השלבים הראשונים מקבלים את העודף."""
    base, extra = divmod(n, PANELS)
    out, s = [], 1
    for i in range(PANELS):
        size = base + (1 if i < extra else 0)
        if size:
            out.append(list(range(s, s + size)))
            s += size
    return out


def span(f, idxs):
    a = f["steps"][idxs[0] - 1][2].split(" עד ")[0]
    z = f["steps"][idxs[-1] - 1][2].split(" עד ")[-1]
    return a if a == z else f"{a} עד {z}"


def panel(key, j, idxs):
    f = FLOW[key]
    first, last = idxs[0], idxs[-1]
    cls = f"ph-{key}-{j}"
    # אחרי השלב: לא מוצג. לפני השלב: חיוור
    rules = [f".{cls} [data-step=\"{n}\"] {{ display: none; }}" for n in range(last + 1, len(f["steps"]) + 1)]
    rules += [f".{cls} [data-step=\"{n}\"] {{ opacity: .32; }}" for n in range(1, first)]
    _, hgt, _ = _proj(f["bbox"], MAP_W)
    k = min(BOX_W / MAP_W, BOX_H / hgt)
    svg = flow_svg(key, MAP_W).replace('<svg class="fmap"', f'<svg class="fmap" width="{MAP_W * k:.0f}" height="{hgt * k:.0f}"', 1)
    evs = []
    for n in idxs:
        _pt, fk, when, txt, approx = f["steps"][n - 1]
        c = FORCE[fk][1]
        tc = "#8a7f93" if fk == "civ" else b_darker(c)
        evs.append(f'<div class="ph-ev"><span class="n{" ap" if approx else ""}" style="--c:{c}">{n}</span>'
                   f'<div><b>{b.e(when)}</b> · <i style="color:{tc}">{b.e(FORCE[fk][0])}</i><br>{b.e(txt)}</div></div>')
    return (f'<style>{"".join(rules)}</style><div class="ph {cls}"><div class="ph-map">{svg}</div>'
            f'<div class="ph-txt"><div class="ph-h"><b>שלב {j}</b><span>{b.e(span(f, idxs))}</span></div>{"".join(evs)}</div></div>')


def b_darker(h, k=0.72):
    h = h.lstrip("#")
    return "#" + "".join(f"{min(255, int(int(h[i:i + 2], 16) * k)):02x}" for i in (0, 2, 4))


def print_slide(key):
    f = FLOW[key]
    gs = groups(len(f["steps"]))
    panels = "".join(panel(key, j, g) for j, g in enumerate(gs, 1))
    used = []
    for st in f["steps"]:
        if st[1] not in used:
            used.append(st[1])
    for a in f["arrows"]:
        if a[1] not in used:
            used.append(a[1])
    leg = "".join(f'<span><i style="background:{FORCE[u][1]}"></i>{b.e(FORCE[u][0])}</span>' for u in used)
    note = (f'{f["note"]} בכל מפה: אירועי השלב בצבע מלא, ואירועים משלבים קודמים חיוורים. '
            f'מפות: © OpenStreetMap contributors.')
    return b.slide(b.top("מהלך הקרב בשלבים", f'{f["title"]}, {f["when"]}') +
                   f'<div class="ph-grid">{panels}</div><div class="ph-foot"><div class="ph-lg">{leg}</div><div class="nt">{b.e(note)}</div></div>' +
                   b.foot())


def build_slides():
    keys = [k for k in ORDER if k in FLOW] + [k for k in FLOW if k not in ORDER]
    return [print_slide(k) for k in keys]


def main():
    slides = build_slides()
    css = (b.HERE / "deck.css").read_text(encoding="utf-8") + PRINT_CSS
    html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>מהלך הקרב בשלבים</title>'
            f'<style>{css}</style></head><body>{"".join(slides)}{b.NUM_JS}</body></html>')
    tmp = b.HERE / "_print.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run([b.CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={OUT_PDF}", tmp.as_uri()], capture_output=True)
    chk = html.replace("</body>", b.CHECK_JS.replace(".body *, ", ".ph-txt *, .ph-foot *, ") + "</body>")
    tmp.write_text(chk, encoding="utf-8")
    dom = subprocess.run([b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=8000", "--window-size=1600,900",
                          "--dump-dom", tmp.as_uri()], capture_output=True, text=True).stdout
    import re, html as h
    m = re.search(r'<pre id="ovf">(.*?)</pre>', dom, re.S)
    # טקסט ב-.ph-txt שנחתך בגבול הכרטיס: בדיקה נפרדת
    tmp.write_text(html.replace("</body>", """<pre id="clip"></pre><script>document.fonts.ready.then(function(){var bad=[];
document.querySelectorAll('.s').forEach(function(s,i){s.querySelectorAll('.ph-txt').forEach(function(t,j){if(t.scrollHeight>t.clientHeight+1)bad.push((i+1)+'.'+(j+1));});});
document.getElementById('clip').textContent=bad.join(' ');});</script></body>"""), encoding="utf-8")
    dom2 = subprocess.run([b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=8000", "--window-size=1600,900",
                           "--dump-dom", tmp.as_uri()], capture_output=True, text=True).stdout
    m2 = re.search(r'<pre id="clip">(.*?)</pre>', dom2, re.S)
    tmp.unlink()
    print(f"slides: {len(slides)}  pdf: {OUT_PDF.name}")
    print("overflow:", h.unescape(m.group(1)) if m and m.group(1).strip() else "none")
    print("clipped panels:", m2.group(1).strip() if m2 and m2.group(1).strip() else "none")


if __name__ == "__main__":
    main()
