# תגי שם (Lower third) לעונה 2, משוחזרים מהדוגמאות "סרן יהל כהן.mov" ו-"סאל עמית לוי.mov".
# 1920x1080, 25fps, 113 פריימים (4.52 שנ׳), ProRes 4444 עם ערוץ שקיפות, כמו המקור.
#
# האנימציה (נמדדה פריים-פריים מהמקור):
# - הפילה הסגולה (#4A2671) נפתחת מקו דק כלפי מטה: מראש קבוע ב-y=828 ועד גובה 47, בפריימים 6-23 (ease-out).
# - השם והתפקיד עולים יחד כ-110 פיקסלים בפריימים 7-24. השם נחשף רק מעל ראש הפילה, והתפקיד רק בתוך הפילה.
# - היציאה הפוכה: הטקסט יורד בפריימים 91-108, והפילה נסגרת בפריימים 94-111.
# - מרכז אופקי קבוע ב-x=1537. רוחב הפילה נקבע לפי אורך השם.
#
# שימוש: python3 name_tags.py                  -> כל התגים ברשימה TAGS
#        python3 name_tags.py --still            -> רק פריים סטטי (PNG) לכל תג, לבדיקה

import base64, json, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FPS, FRAMES = 25, 113

TAGS = [
    ("אבנר סטראז׳", "מ״פ פלת״צ מילואים"),
    ("אלעד צליק", "מ״פ פלוגת החוד גדוד שקד"),
    ("אור אדרי", "מ״פ רובאית גדוד שקד"),
    ("שניר שמחון", "מג״ד יחס״מ מילואים"),
]

FONT = "data:font/ttf;base64," + base64.b64encode((HERE / "assets" / "NotoSansHebrew.ttf").read_bytes()).decode()

PAGE = """<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>
@font-face { font-family: "NSH"; src: url("%(font)s") format("truetype"); font-weight: 100 900; font-stretch: 62.5%% 100%%; }
html, body { margin: 0; width: 1920px; height: 1080px; background: transparent; overflow: hidden; }
#tag { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; filter: drop-shadow(8px 12px 8px rgba(0,0,0,.45)) drop-shadow(26px 38px 30px rgba(0,0,0,.42)); }
#pill { position: absolute; top: 828px; height: 47px; border-radius: 24px; background: #4A2671; overflow: hidden; }
#namebox { position: absolute; left: 0; width: 1920px; top: 0; height: 828px; overflow: hidden; }
#name, #role { position: absolute; white-space: nowrap; color: #fff; font-family: "NSH"; transform: translateX(-50%%); }
#name { font-size: 65px; font-weight: 800; font-stretch: 62.5%%; letter-spacing: -2px; text-shadow: 6px 8px 10px rgba(0,0,0,.55); }
#role { font-size: 31.5px; font-weight: 350; font-stretch: 72%%; }
</style></head><body><div id="tag"><div id="pill"><div id="role"></div></div><div id="namebox"><div id="name"></div></div></div>
<script>
const P = %(params)s, CX = 1537;
const name = document.getElementById('name'), role = document.getElementById('role'), pill = document.getElementById('pill');
name.textContent = P.name; role.textContent = P.role;
const out3 = p => 1 - Math.pow(1 - p, 3), in3 = p => p * p * p, cl = (a, b, f) => Math.min(1, Math.max(0, (f - a) / (b - a)));
document.fonts.ready.then(() => {
  const w = Math.max(name.offsetWidth + 84, role.offsetWidth + 70);
  pill.style.left = (CX - w / 2) + 'px'; pill.style.width = w + 'px';
  const f = P.frame;
  // גובה הפילה ותזוזת הטקסט, כניסה ויציאה
  const h = 47 * (f < 60 ? out3(cl(5.5, 23, f)) : 1 - in3(cl(94, 111, f)));
  const d = 110 * (f < 60 ? 1 - out3(cl(7, 24, f)) : in3(cl(91, 108, f)));
  pill.style.height = h + 'px'; pill.style.display = h < 0.6 ? 'none' : 'block';
  name.style.left = CX + 'px'; name.style.top = (P.nameTop + d) + 'px';
  role.style.left = (CX - (CX - w / 2)) + 'px'; role.style.top = (P.roleTop + d) + 'px';
  document.title = 'ready';
});
</script></body></html>"""

NAME_TOP, ROLE_TOP = 735, 0  # מכויל מול המקור: שם בגובה 754-811, תפקיד 839-867


def render(html_dir, name, role, frame, png):
    p = {"name": name, "role": role, "frame": frame, "nameTop": NAME_TOP, "roleTop": ROLE_TOP}
    f = html_dir / f"f{frame:03d}.html"
    f.write_text(PAGE % {"font": FONT, "params": json.dumps(p, ensure_ascii=False)}, encoding="utf-8")
    # לכל Chrome פרופיל משלו, כדי שכמה מופעים במקביל לא יתנגשו. ניסיון חוזר אם נכשל.
    for attempt in range(3):
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=3000",
                            f"--user-data-dir={html_dir / f'prof{frame:03d}'}",
                            "--default-background-color=00000000", "--window-size=1920,1080", f"--screenshot={png}", f.as_uri()],
                           capture_output=True)
        if r.returncode == 0 and Path(png).exists():
            return
    raise RuntimeError(f"render failed: frame {frame}")


def build(name, role, still=False):
    title = f"{name} - {role}".replace("/", "-")
    tmp = Path(tempfile.mkdtemp())
    try:
        if still:
            render(tmp, name, role, 50, HERE / f"{title}.png")
            return
        with ThreadPoolExecutor(8) as ex:
            list(ex.map(lambda i: render(tmp, name, role, i, tmp / f"{i:03d}.png"), range(FRAMES)))
        out = HERE / f"{title}.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%03d.png"),
                        "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-vendor", "apl0",
                        str(out)], check=True)
        shutil.copy(tmp / "050.png", HERE / f"{title}.png")
        print("ok", out.name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    still = "--still" in sys.argv
    for n, r in TAGS:
        build(n, r, still)
