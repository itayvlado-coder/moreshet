"""מצגת "מהלך הקרב" שמיועדת להעלאה ל-Google Slides.

שקף פתיחה עם מפת הזירות, ולחיצה על זירה (במפה או ברשימה) קופצת לשקף שלה.
בכל שקף זירה: קליק לכל אירוע, וכפתור "חזרה למפה".
האנימציות כאן הן רק הופעה והיעלמות בדעיכה (Fade), כי אלה האנימציות ש-Google Slides יודע לייבא מ-PowerPoint.

שימוש:  python3 build_gslides.py
נוצר:   "מהלך הקרב - Google Slides.pptx"
"""
import json, re, subprocess
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR

import build_pptx as bp
import build_live as bl
from battle_maps import FLOW

HERE = bp.HERE
OUT = HERE / "מהלך הקרב - Google Slides.pptx"
IMG = bp.IMG


class FadeTimeline(bp.Timeline):
    """אותו רצף קליקים, אבל כל כניסה היא Fade: Google Slides לא מייבא Wipe ו-Zoom."""
    def add(self, kind, spid, delay=0, dur=500, sub=None):
        if kind in ("wipe", "zoom"):
            kind, dur = "fade", min(dur, 800)
        super().add(kind, spid, delay, dur, None)


def atlas_assets():
    """צילום של שקף מפת הזירות מהגרסה החיה, ומיקום כל אזור לחיץ בו."""
    keys = [k for k in bl.ORDER if k in FLOW] + [k for k in FLOW if k not in bl.ORDER]
    html_path = bl.build_atlas()
    IMG.mkdir(exist_ok=True)
    png = IMG / "atlas.png"
    subprocess.run([bp.b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=5000", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1600,900", f"--screenshot={png}", html_path.as_uri()],
                   capture_output=True, timeout=120)
    js = ("<pre id='m'></pre><script>document.fonts.ready.then(function(){var o=[];"
          "document.querySelectorAll('.atlas [data-go]').forEach(function(e){var r=e.getBoundingClientRect();"
          "o.push([e.dataset.go,r.left,r.top,r.width,r.height]);});document.getElementById('m').textContent=JSON.stringify(o);});</script>")
    tmp = HERE / "_atlas_measure.html"
    tmp.write_text(html_path.read_text(encoding="utf-8").replace("</body>", js + "</body>"), encoding="utf-8")
    dom = subprocess.run([bp.b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=5000", "--window-size=1600,900",
                          "--dump-dom", tmp.as_uri()], capture_output=True, text=True, timeout=120).stdout
    tmp.unlink()
    boxes = json.loads(re.search(r"<pre id=\"m\">(.*?)</pre>", dom, re.S).group(1).replace("&quot;", '"'))
    return keys, bp.to_jpg(png), boxes


def link_box(slide, x, y, w, h, target, name):
    """מלבן שקוף שמקשר לשקף אחר. שקיפות מלאה, בלי קו, כדי שהצילום שמתחת ייראה כמו שהוא."""
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, bp.emu(x), bp.emu(y), bp.emu(w), bp.emu(h))
    bp.style(sh, "FFFFFF", 0.0, name=name)
    sh.click_action.target_slide = target
    return sh


def back_button(slide, target):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bp.emu(210), bp.emu(24), bp.emu(190), bp.emu(42))
    bp.style(sh, "F6F1E6", line="D8BC7E", line_px=1.5, name="חזרה למפה")
    sh.adjustments[0] = 0.5
    bp.set_text(sh, [[("→ חזרה למפת הזירות", 16, "3A1752", True)]], MSO_ANCHOR.MIDDLE, 4)
    sh.text_frame.paragraphs[0]._p.get_or_add_pPr().set("algn", "ctr")
    sh.click_action.target_slide = target
    return sh


def main():
    bp.Timeline = FadeTimeline
    keys, atlas_jpg, boxes = atlas_assets()
    prs = Presentation()
    prs.slide_width, prs.slide_height = bp.emu(1600), bp.emu(900)
    atlas = prs.slides.add_slide(prs.slide_layouts[6])
    atlas.shapes.add_picture(str(atlas_jpg), 0, 0, prs.slide_width, prs.slide_height).name = "מפת הזירות"
    atlas.notes_slide.notes_text_frame.text = "לחיצה על זירה, במפה או ברשימה, עוברת לשקף שלה. בכל שקף זירה: קליק לכל אירוע."
    flows = {}
    for k in keys:
        png = IMG / f"gflow_{k}.png"
        page = bp.flow_page(k, bp.BG_CSS)
        bp.chrome_shot(page, png)
        s = bp.add_flow_slide(prs, k, bp.to_jpg(png))
        back_button(s, atlas)
        flows[k] = s
    for k, x, y, w, h in boxes:
        link_box(atlas, x, y, w, h, flows[k], f"קישור: {FLOW[k]['title']}")
    prs.save(OUT)
    print("ok", OUT.name, len(prs.slides._sldIdLst), "slides", f"{OUT.stat().st_size // 1024} KB", "links:", len(boxes))


if __name__ == "__main__":
    main()
