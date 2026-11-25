# מפת גזרות: עיינתא, רכס המחיצה ובינת ג׳בל עם הקסבה (עונה 2, פרקים 2-3).
# שפת העיצוב של מפות לבנון בסרטונים: תצלום אוויר בשחור-לבן כהה, פוליגונים סגולים זוהרים, יעד אדום, כיתוב לבן.
#
# מקורות הגבולות:
# - עיינתא ובינת ג׳בל: פוליגוני השטח הבנוי (landuse=residential) ב-OpenStreetMap, ways 1047470387 ו-1044368247.
# - רכס המחיצה: הרצועה שבין שני הפוליגונים, לאורך הכביש. בנתוני הגובה (Terrarium/SRTM) זה קו הרכס,
#   790 עד 800 מ׳, בין העמק של עיינתא (כ-740) לקערה של בינת ג׳בל (כ-720). עליו שני בתי החולים.
# - הקסבה: לפי מפת "רובוטיקה ומטרות קרב בקסבה" במצגת "מכת חולים", מעוגנת לבריכה העגולה (OSM).
#
# שימוש: python3 build_sectors.py          ->  HTML ו-PNG ברזולוציה 1920x1080
#        python3 build_sectors.py --video  ->  גם MP4 מונפש, ושכבות PNG שקופות בתיקייה "שכבות"

import base64, math, subprocess, urllib.request
from html import escape as e
from pathlib import Path

HERE = Path(__file__).parent
DECK = HERE.parents[1] / "צלשים 7.10" / "הגשה לאוגדה" / "מצגת חטיבה"
TILES = HERE / "assets" / "tiles"
IMG = HERE / "assets" / "imagery_bintjbeil.jpg"
OUT = HERE / "מפת גזרות - עיינתא, רכס המחיצה ובינת גבל"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1920, 1080
BBOX = (33.1139, 35.4175, 33.1351, 35.4626)  # S, W, N, E
Z = 16


def merc(la, lo, z=Z):
    n = 2 ** z * 256
    r = math.radians(la)
    return (lo + 180) / 360 * n, (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * n


S, Wl, N, E = BBOX
X0, Y0 = merc(N, Wl)
X1, Y1 = merc(S, E)
KX, KY = W / (X1 - X0), H / (Y1 - Y0)


def xy(la, lo):
    x, y = merc(la, lo)
    return (x - X0) * KX, (y - Y0) * KY


def imagery():
    """תצלום אוויר (Esri World Imagery), מחובר, חתוך לגבולות ומעובד לשחור-לבן כהה."""
    if IMG.exists():
        return
    TILES.mkdir(parents=True, exist_ok=True)
    tx0, ty0, tx1, ty1 = int(X0 // 256), int(Y0 // 256), int(X1 // 256), int(Y1 // 256)
    cols, rows = tx1 - tx0 + 1, ty1 - ty0 + 1
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            f = TILES / f"{Z}_{tx}_{ty}.jpg"
            if not f.exists():
                url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{ty}/{tx}"
                req = urllib.request.Request(url, headers={"User-Agent": "map-builder/1.0"})
                f.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    inputs, layout = [], []
    for j, ty in enumerate(range(ty0, ty1 + 1)):
        for i, tx in enumerate(range(tx0, tx1 + 1)):
            inputs += ["-i", str(TILES / f"{Z}_{tx}_{ty}.jpg")]
            layout.append(f"{i * 256}_{j * 256}")
    cx, cy = X0 - tx0 * 256, Y0 - ty0 * 256
    cw, ch = X1 - X0, Y1 - Y0
    flt = (f"xstack=inputs={cols * rows}:layout={'|'.join(layout)},"
           f"crop={cw:.0f}:{ch:.0f}:{cx:.0f}:{cy:.0f},scale={W}:{H}:flags=lanczos,"
           "hue=s=0,eq=contrast=1.35:brightness=-0.16:gamma=0.85,unsharp=5:5:0.6")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", flt, "-q:v", "3", str(IMG)], check=True)


# ---------- הגזרות ----------
AYNATA = [(33.13379, 35.43635), (33.13131, 35.43581), (33.13077, 35.43592), (33.13007, 35.43543), (33.12945, 35.43526),
          (33.12896, 35.43458), (33.12497, 35.43847), (33.12366, 35.43971), (33.12332, 35.44123), (33.12268, 35.44239),
          (33.12234, 35.44284), (33.12189, 35.4455), (33.12221, 35.4472), (33.12274, 35.44777), (33.12328, 35.4485),
          (33.12348, 35.44899), (33.12352, 35.44962), (33.12385, 35.45046), (33.12431, 35.45142), (33.12584, 35.45193),
          (33.12767, 35.45174), (33.12823, 35.45211), (33.12824, 35.45407), (33.12898, 35.45383), (33.13004, 35.45398),
          (33.13009, 35.45308), (33.13154, 35.45168), (33.13229, 35.45331), (33.13305, 35.45289), (33.13235, 35.45178),
          (33.13197, 35.44938), (33.1331, 35.44927), (33.13147, 35.44537), (33.13192, 35.44335), (33.1321, 35.4427),
          (33.13224, 35.4419)]
BINTJBEIL = [(33.11419, 35.44212), (33.11499, 35.44228), (33.11636, 35.43781), (33.1169, 35.43905), (33.11726, 35.44017),
             (33.11745, 35.44183), (33.11769, 35.4422), (33.11819, 35.44197), (33.1184, 35.44149), (33.11874, 35.44154),
             (33.11922, 35.44141), (33.11976, 35.44141), (33.11997, 35.44115), (33.12099, 35.44089), (33.12134, 35.44022),
             (33.12125, 35.4394), (33.12179, 35.43876), (33.12404, 35.4386), (33.12863, 35.4301), (33.13105, 35.42564),
             (33.13059, 35.42161), (33.12925, 35.42165), (33.12906, 35.42354), (33.12787, 35.42373), (33.12703, 35.42304),
             (33.12701, 35.42074), (33.12512, 35.41933), (33.12391, 35.41861), (33.12259, 35.41772), (33.11967, 35.4201),
             (33.1168, 35.42385), (33.115, 35.42331), (33.11419, 35.42125), (33.11034, 35.42035), (33.10945, 35.41989),
             (33.10815, 35.4198), (33.10648, 35.41821), (33.10585, 35.4211), (33.10423, 35.42059), (33.10136, 35.41872),
             (33.10114, 35.42087), (33.10061, 35.42344), (33.10391, 35.42522), (33.10626, 35.42599), (33.10628, 35.42754),
             (33.10761, 35.42986), (33.109, 35.43155), (33.11006, 35.43323), (33.11035, 35.43388), (33.11061, 35.43455),
             (33.11124, 35.43559), (33.11313, 35.43464), (33.11181, 35.43662), (33.112, 35.43951), (33.11219, 35.44199)]
# הרכס: מהשפה הדרום-מערבית של עיינתא ועד השפה הצפון-מזרחית של בינת ג׳בל. בצפון-מערב נמשך עד קו הרכס
# שמעל בית החולים סלאח ע׳נדור (כ-800 מ׳). הוואדי שממזרח לו (כ-720 עד 740 מ׳) נשאר מחוץ לגזרות.
RIDGE = [(33.13105, 35.42564), (33.1336, 35.4280), (33.1338, 35.4318), (33.1310, 35.4345), (33.12945, 35.43526), (33.12896, 35.43458), (33.12497, 35.43847), (33.12366, 35.43971),
         (33.12332, 35.44123), (33.12268, 35.44239), (33.12234, 35.44284), (33.12150, 35.44260), (33.12099, 35.44089),
         (33.12134, 35.44022), (33.12125, 35.4394), (33.12179, 35.43876), (33.12404, 35.4386), (33.12863, 35.4301)]
KASBA = [(33.12025, 35.43216), (33.12034, 35.43369), (33.11988, 35.43632), (33.11793, 35.43625), (33.11705, 35.43588),
         (33.11685, 35.43493), (33.11692, 35.43281), (33.11793, 35.43267), (33.11872, 35.43296)]

SITES = [  # יעדים על הרכס (נקודה אדומה)
    ((33.1305, 35.4296), "בית החולים סלאח ע׳נדור", "n"),
    ((33.1278, 35.4355), "בית החולים הממשלתי", "e"),
]


def path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (xy(*p) for p in pts)) + " Z"


def svg():
    img = "data:image/jpeg;base64," + base64.b64encode(IMG.read_bytes()).decode()
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         '<defs>',
         '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
         '<filter id="rglow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="9"/></filter>',
         '<filter id="tsh" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity=".9"/></filter>',
         # הרכס חותך את שתי העיירות, כדי שלא יהיו שטחים חופפים
         f'<mask id="noridge"><rect width="{W}" height="{H}" fill="#fff"/><path d="{path(RIDGE)}" fill="#000"/></mask>',
         '<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/>'
         '<stop offset="100%" stop-color="#000" stop-opacity=".75"/></radialGradient>',
         '</defs>',
         f'<g id="bg"><image href="{img}" width="{W}" height="{H}" preserveAspectRatio="none"/>',
         f'<rect width="{W}" height="{H}" fill="url(#vig)"/></g>']

    def zone(pts, fill, line, op, mask=""):
        d = path(pts)
        m = f' mask="url(#{mask})"' if mask else ""
        o.append(f'<g{m}><path d="{d}" fill="{fill}" fill-opacity="{op}"/>'
                 f'<path d="{d}" fill="none" stroke="{line}" stroke-width="7" stroke-opacity=".45" filter="url(#glow)"/>'
                 f'<path d="{d}" fill="none" stroke="{line}" stroke-width="2.4" stroke-dasharray="9 6" stroke-linejoin="round"/></g>')

    def label(la, lo, t, cls):
        x, y = xy(la, lo)
        o.append(f'<text class="{cls}" x="{x:.0f}" y="{y:.0f}" text-anchor="middle" filter="url(#tsh)">{e(t)}</text>')

    o.append('<g id="bj">')
    zone(BINTJBEIL, "#5b3cf0", "#a99bff", .20, "noridge")
    label(33.1238, 35.4268, "בינת ג׳בל", "big")
    o.append('</g><g id="aynata">')
    zone(AYNATA, "#9b4dff", "#d2a8ff", .26, "noridge")
    label(33.1312, 35.4462, "עיינתא", "big")
    o.append('</g><g id="ridge">')
    zone(RIDGE, "#e05cff", "#f4c2ff", .42)
    # שם הרכס לאורך הרכס
    x1, y1 = xy(33.12640, 35.43500)
    x2, y2 = xy(33.12240, 35.44110)
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    o.append(f'<text class="md ridge" x="{cx:.0f}" y="{cy + 8:.0f}" text-anchor="middle" transform="rotate({ang:.1f} {cx:.0f} {cy:.0f})" filter="url(#tsh)">רכס המחיצה</text>')
    for (la, lo), t, side in SITES:
        x, y = xy(la, lo)
        tx, ty, ta = (x, y - 22, "middle") if side == "n" else (x + 22, y + 8, "start")
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" fill="#ff3030"/><circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="#ffd0d0"/>'
                 f'<text class="sm" x="{tx:.0f}" y="{ty:.0f}" direction="ltr" text-anchor="{ta}" filter="url(#tsh)">{e(t)}</text>')
    o.append('</g><g id="kasba">')
    d = path(KASBA)
    o.append(f'<path d="{d}" fill="#ff2a2a" fill-opacity=".34"/>'
             f'<path d="{d}" fill="none" stroke="#ff7a7a" stroke-width="2.4" stroke-dasharray="9 6"/>')
    label(33.1210, 35.4342, "קסבת בינת ג׳בל", "md")
    # זוהר אדום: הקסבה ובתי החולים. בסרטון הוא פועם
    o.append('</g><g id="pulse">')
    o.append(f'<path d="{d}" fill="none" stroke="#ff5a5a" stroke-width="8" stroke-opacity=".6" filter="url(#glow)"/>')
    for (la, lo), _t, _s in SITES:
        x, y = xy(la, lo)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="#ff1f1f" opacity=".85" filter="url(#rglow)"/>')
    o.append('</g><g id="credit">')
    o.append(f'<text class="cr" x="{W - 24}" y="{H - 20}" text-anchor="end" direction="ltr">Imagery © Esri, Maxar · © OpenStreetMap contributors</text>')
    o.append("</g></svg>")
    return "".join(o)


LAYERS = ["bj", "aynata", "ridge", "kasba", "pulse", "credit"]


def page(only=None):
    """only=None: המפה המלאה. only="bg": רק הרקע. only=<שכבה>: השכבה לבד, על רקע שקוף."""
    font = "data:font/ttf;base64," + base64.b64encode((DECK / "assets" / "Heebo.ttf").read_bytes()).decode()
    css = (f'@font-face{{font-family:"Heebo";src:url("{font}") format("truetype");font-weight:100 900}}'
           'html,body{margin:0;background:#000;height:100%;overflow:hidden}'
           'svg{display:block;width:100vw;height:100vh;font-family:"Heebo",sans-serif}'
           'text{fill:#fff}'
           '.big{font-size:64px;font-weight:800;letter-spacing:1px}'
           '.md{font-size:38px;font-weight:700}'
           '.ridge{fill:#fbe4ff}'
           '.sm{font-size:24px;font-weight:600}'
           '.cr{font-size:13px;fill:#aaa}')
    if only == "bg":
        css += "".join(f"#{k}{{display:none}}" for k in LAYERS)
    elif only:
        css += "html,body{background:transparent}#bg{display:none}" + "".join(f"#{k}{{display:none}}" for k in LAYERS if k != only)
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>עיינתא ובינת ג׳בל</title>'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><style>{css}</style></head>'
            f'<body>{svg()}</body></html>')


def shot(html, png, transparent=False):
    extra = ["--default-background-color=00000000"] if transparent else []
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=4000", "--hide-scrollbars", *extra,
                    f"--window-size={W},{H}", f"--screenshot={png}", html.as_uri()], capture_output=True, check=True)


# ---------- סרטון ----------
# לוח זמנים (שניות): הרקע עולה מהשחור, ואז הגזרות אחת-אחת, והזוהר האדום פועם.
FADE = {"aynata": 1.6, "ridge": 4.0, "bj": 6.4, "kasba": 8.8, "credit": 0.6}
PULSE_FROM, DUR, FPS = 9.6, 16, 30


def video():
    lay = HERE / "שכבות"
    lay.mkdir(exist_ok=True)
    tmp = lay / "_layer.html"
    tmp.write_text(page("bg"), encoding="utf-8")
    shot(tmp, lay / "00 - רקע.png")
    names = {"bj": "03 - בינת גבל", "aynata": "01 - עיינתא", "ridge": "02 - רכס המחיצה", "kasba": "04 - הקסבה",
             "pulse": "05 - זוהר אדום", "credit": "06 - קרדיט"}
    for k in LAYERS:
        tmp.write_text(page(k), encoding="utf-8")
        shot(tmp, lay / f"{names[k]}.png", transparent=True)
    tmp.unlink()
    inputs = ["-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(lay / "00 - רקע.png")]
    for k in LAYERS:
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", str(DUR), "-i", str(lay / f"{names[k]}.png")]
    f = [f"[0]format=rgba,fade=in:st=0:d=1.2[b0]"]
    cur = "b0"
    for i, k in enumerate(LAYERS, 1):
        if k == "pulse":
            f.append(f"[{i}]format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':"
                     f"a='alpha(X,Y)*gte(T,{PULSE_FROM})*(0.35+0.65*(0.5-0.5*cos(2*PI*(T-{PULSE_FROM})/1.6)))'[l{i}]")
        else:
            f.append(f"[{i}]format=rgba,fade=in:st={FADE[k]}:d=0.9:alpha=1[l{i}]")
        f.append(f"[{cur}][l{i}]overlay=format=auto[b{i}]")
        cur = f"b{i}"
    # תנועת מצלמה איטית פנימה, כמו בסרטונים
    f.append(f"[{cur}]scale=3840:2160:flags=lanczos,"
             f"zoompan=z='1+0.07*on/({DUR}*{FPS})':x='iw/2-(iw/zoom/2)':y='ih*0.47-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
             "format=yuv420p[v]")
    mp4 = OUT.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[v]",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-r", str(FPS), "-movflags", "+faststart", str(mp4)],
                   check=True)
    print("ok", mp4.name, f"{mp4.stat().st_size // 1024} KB")


if __name__ == "__main__":
    import sys
    imagery()
    html = OUT.with_suffix(".html")
    html.write_text(page(), encoding="utf-8")
    shot(html, OUT.with_suffix(".png"))
    print("ok", html.name)
    if "--video" in sys.argv:
        video()
