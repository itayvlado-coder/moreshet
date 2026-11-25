# מפת "דפיקה בדלת", אל-חיאם, 21.03.26: גדוד 52 יוצא מהמגנן שלו כעתודה אל מארב הצלפים.
# אותה שפת עיצוב כמו מפת עיינתא (build_sectors.py): תצלום אוויר כהה, סגול זוהר, יעד אדום, כיתוב לבן.
#
# מקורות המיקומים:
# - מגנן 52: קואורדינטות מ-Google Earth, מאיתי (25.11): 33°19.6809'N 35°36.8575'E.
# - מארב הצלפים: לפי הסרטון של הגרפיקאי "TOP MAP SAYERET MOVES TO MARAV ZALAFIM", מותאם לתצלום האוויר
#   דרך כביש הסרפנטינות שממערב לעיירה. דיוק של כ-30 עד 50 מ׳.
# - נקודת החיסול של 52: צמודה למארב, ממערב לו, לפי שקף "דפיקה בדלת" והסרטון HITAKLOT+HISOL. משוערת.
# - המסלול: מסלול ב׳ שאיתי בחר, לאורך הכבישים ב-OSM. נכנס למארב מדרום, כמו בשקף.
#
# שימוש: python3 build_khiam.py   ->  PNG ו-MP4 (1920x1080, 30fps), ושכבת PNG של הפריים האחרון.

import base64, heapq, json, math, shutil, subprocess, tempfile, urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from html import escape as e
from pathlib import Path

HERE = Path(__file__).parent
DECK = HERE.parents[1] / "צלשים 7.10" / "הגשה לאוגדה" / "מצגת חטיבה"
OSM = HERE / "assets" / "maps" / "khiam.osm"
TILES = HERE / "assets" / "tiles_khiam"
IMG = HERE / "assets" / "imagery_khiam.jpg"
OUT = HERE / "מפת דפיקה בדלת - 52 לעתודה במארב הצלפים, אל-חיאם"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H, FPS, DUR = 1920, 1080, 30, 16
Z = 17
BBOX = (33.32422, 35.60352, 33.33079, 35.61749)  # S, W, N, E

MIGNAN = (33 + 19.6809 / 60, 35 + 36.8575 / 60)
AMBUSH = (33.32786, 35.60877)
KILL = (33.32776, 35.60842)          # כ-35 מ׳ ממערב-דרום-מערב למארב (משוער)
VIA = (33.326876, 35.607923)          # נקודת ביניים שמכריחה את המסלול להיכנס מדרום (מסלול ב׳)


def merc(la, lo, z=Z):
    n = 2 ** z * 256
    r = math.radians(la)
    return (lo + 180) / 360 * n, (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * n


S, Wl, N, E = BBOX
X0, Y0 = merc(N, Wl)
X1, Y1 = merc(S, E)


def xy(la, lo):
    x, y = merc(la, lo)
    return (x - X0) / (X1 - X0) * W, (y - Y0) / (Y1 - Y0) * H


def imagery():
    if IMG.exists():
        return
    TILES.mkdir(parents=True, exist_ok=True)
    tx0, ty0, tx1, ty1 = int(X0 // 256), int(Y0 // 256), int(X1 // 256), int(Y1 // 256)

    def get(t):
        tx, ty = t
        f = TILES / f"{Z}_{tx}_{ty}.jpg"
        if not f.exists():
            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{ty}/{tx}"
            f.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "map-builder/1.0"}), timeout=30).read())
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(get, [(x, y) for x in range(tx0, tx1 + 1) for y in range(ty0, ty1 + 1)]))
    tmp = Path(tempfile.mkdtemp())
    rows = []
    for j, ty in enumerate(range(ty0, ty1 + 1)):
        ins = sum([["-i", str(TILES / f"{Z}_{tx}_{ty}.jpg")] for tx in range(tx0, tx1 + 1)], [])
        rows.append(tmp / f"r{j}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f"hstack=inputs={tx1 - tx0 + 1}", str(rows[-1])], check=True)
    ins = sum([["-i", str(r)] for r in rows], [])
    flt = (f"vstack=inputs={len(rows)},crop={X1 - X0:.0f}:{Y1 - Y0:.0f}:{X0 - tx0 * 256:.0f}:{Y0 - ty0 * 256:.0f},"
           f"scale={W}:{H}:flags=lanczos,hue=s=0,eq=contrast=1.35:brightness=-0.16:gamma=0.85,unsharp=5:5:0.6")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", flt, "-q:v", "3", str(IMG)], check=True)
    shutil.rmtree(tmp)


def route():
    """המסלול הקצר בכבישי OSM: מגנן -> נקודת ביניים -> מארב. בלי ענפים מיותרים (לולאות נחתכות)."""
    r = ET.parse(OSM).getroot()
    nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in r.iter("node")}
    d = lambda a, b: math.hypot((a[0] - b[0]) * 111320, (a[1] - b[1]) * 111320 * math.cos(math.radians(33.33)))
    g = {}
    for w in r.iter("way"):
        t = {x.get("k"): x.get("v") for x in w.iter("tag")}
        if "highway" not in t or t["highway"] in ("footway", "path", "steps"):
            continue
        nd = [x.get("ref") for x in w.iter("nd") if x.get("ref") in nodes]
        for a, b in zip(nd, nd[1:]):
            l = d(nodes[a], nodes[b])
            g.setdefault(a, []).append((b, l))
            g.setdefault(b, []).append((a, l))
    near = lambda p: min(g, key=lambda n: d(nodes[n], p))

    def sp(s, t):
        dist, prev, pq = {s: 0}, {}, [(0, s)]
        while pq:
            c, u = heapq.heappop(pq)
            if u == t:
                break
            if c > dist[u]:
                continue
            for v, l in g[u]:
                if c + l < dist.get(v, 1e18):
                    dist[v], prev[v] = c + l, u
                    heapq.heappush(pq, (c + l, v))
        p = [t]
        while p[-1] != s:
            p.append(prev[p[-1]])
        return p[::-1]
    path = sp(near(MIGNAN), near(VIA)) + sp(near(VIA), near(AMBUSH))[1:]
    # חיתוך לולאות: אם המסלול חוזר לצומת שכבר עבר, מדלגים על מה שביניהם
    out = []
    for n in path:
        if n in out:
            out = out[:out.index(n) + 1]
        else:
            out.append(n)
    pts = [nodes[n] for n in out] + [KILL]
    # הסרת "שיניים": צומת שבו הקו חוזר כמעט לאחור (פחות מ-50 מעלות) נשמט
    def ang(a, b, c):
        v1 = ((a[0] - b[0]), (a[1] - b[1]) * 0.836)
        v2 = ((c[0] - b[0]), (c[1] - b[1]) * 0.836)
        n = math.hypot(*v1) * math.hypot(*v2)
        return 180 if n == 0 else math.degrees(math.acos(max(-1, min(1, (v1[0] * v2[0] + v1[1] * v2[1]) / n))))
    changed = True
    while changed:
        changed = False
        for i in range(1, len(pts) - 1):
            if ang(pts[i - 1], pts[i], pts[i + 1]) < 100:
                del pts[i]
                changed = True
                break

    # פישוט (Douglas-Peucker, 12 מ׳): מחליק פיתולים קטנים שנראים כמו רעש בגרפיקה
    def rdp(p, eps=12):
        if len(p) < 3:
            return p
        m = lambda q: (q[0] * 111320, q[1] * 111320 * 0.836)
        a, b = m(p[0]), m(p[-1])
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        dd = [abs((b[0] - a[0]) * (a[1] - m(q)[1]) - (a[0] - m(q)[0]) * (b[1] - a[1])) / L for q in p[1:-1]]
        i = max(range(len(dd)), key=dd.__getitem__) + 1
        return rdp(p[:i + 1], eps)[:-1] + rdp(p[i:], eps) if dd[i - 1] > eps else [p[0], p[-1]]
    return rdp(pts)


def svg(route_pts):
    img = "data:image/jpeg;base64," + base64.b64encode(IMG.read_bytes()).decode()
    rp = [xy(*p) for p in route_pts]
    rd = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in rp)
    mx, my = xy(*MIGNAN)
    ax, ay = xy(*AMBUSH)
    kx, ky = xy(*KILL)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="rglow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="tsh" x="-10%" y="-30%" width="120%" height="160%"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity=".9"/></filter>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".75"/></radialGradient>
<mask id="reveal" maskUnits="userSpaceOnUse"><path id="revpath" d="{rd}" fill="none" stroke="#fff" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/></mask>
</defs>
<g id="cam">
<image href="{img}" width="{W}" height="{H}" preserveAspectRatio="none"/>
<rect width="{W}" height="{H}" fill="url(#vig)"/>
<g id="route" mask="url(#reveal)">
 <path d="{rd}" fill="none" stroke="#b46bff" stroke-width="9" stroke-opacity=".5" filter="url(#glow)" stroke-linejoin="round"/>
 <path id="rline" d="{rd}" fill="none" stroke="#d9b3ff" stroke-width="4" stroke-dasharray="16 10" stroke-linejoin="round" stroke-linecap="round"/>
</g>
<circle id="head" r="7" fill="#fff" style="filter:drop-shadow(0 0 8px #c77dff)"/>
<g id="mignan">
 <circle cx="{mx:.0f}" cy="{my:.0f}" r="46" fill="#9b4dff" fill-opacity=".28" stroke="#d2a8ff" stroke-width="3" stroke-dasharray="9 6" filter="url(#glow)"/>
 <text class="md" x="{mx:.0f}" y="{my - 62:.0f}" text-anchor="middle" filter="url(#tsh)">מגנן גדוד 52</text>
</g>
<g id="ambush">
 <circle id="apulse" cx="{ax:.0f}" cy="{ay:.0f}" r="30" fill="#ff1f1f" filter="url(#rglow)"/>
 <circle cx="{ax:.0f}" cy="{ay:.0f}" r="15" fill="#ff3030"/><circle cx="{ax:.0f}" cy="{ay:.0f}" r="6" fill="#ffd0d0"/>
 <text class="md" x="{ax:.0f}" y="{ay - 42:.0f}" text-anchor="middle" filter="url(#tsh)">היתקלות במארב צלפים</text>
</g>
<g id="kill">
 <circle cx="{kx:.0f}" cy="{ky:.0f}" r="26" fill="#9b4dff" fill-opacity=".35" stroke="#e3c6ff" stroke-width="3" filter="url(#glow)"/>
 <text class="sm" x="{kx - 50:.0f}" y="{ky + 80:.0f}" text-anchor="end" direction="ltr" filter="url(#tsh)">חיסול מחבלים, גדוד 52</text>
</g>
</g>
<text class="cr" x="{W - 24}" y="{H - 20}" text-anchor="end" direction="ltr">Imagery © Esri, Maxar · © OpenStreetMap contributors</text>
</svg>"""


# לוח זמנים (שניות)
T = {"bg": (0, 1.2), "mignan": (1.2, 0.8), "ambush": (2.6, 0.8), "route": (4.6, 5.0), "kill": (9.8, 0.8)}

JS = """
const T = %(T)s, DUR = %(DUR)s;
const ease = p => 1 - Math.pow(1 - p, 3), cl = (a, d, t) => Math.min(1, Math.max(0, (t - a) / d));
function frame(t) {
  document.getElementById('cam').style.opacity = cl(...T.bg, t);
  const z = 1 + 0.08 * (t / DUR);
  document.getElementById('cam').setAttribute('transform', `translate(%(cx)s %(cy)s) scale(${z}) translate(-%(cx)s -%(cy)s)`);
  for (const k of ['mignan', 'ambush', 'kill']) document.getElementById(k).style.opacity = ease(cl(...T[k], t));
  const rp = document.getElementById('revpath'), L = rp.getTotalLength(), p = ease(cl(...T.route, t));
  rp.style.strokeDasharray = L; rp.style.strokeDashoffset = L * (1 - p);
  document.getElementById('rline').style.strokeDashoffset = -t * 40;
  const h = document.getElementById('head'), pt = rp.getPointAtLength(L * p);
  h.setAttribute('cx', pt.x); h.setAttribute('cy', pt.y); h.style.opacity = (p > 0 && p < 1) ? 1 : 0;
  const ph = (t - T.ambush[0]) / 1.6;
  document.getElementById('apulse').style.opacity = t < T.ambush[0] ? 0 : 0.45 + 0.55 * (0.5 - 0.5 * Math.cos(2 * Math.PI * ph));
}
const t = parseFloat((location.hash.match(/t=([\\d.]+)/) || [0, %(DUR)s])[1]);
document.fonts.ready.then(() => { frame(t); document.title = 'ready'; });
"""


def page(route_pts):
    font = "data:font/ttf;base64," + base64.b64encode((DECK / "assets" / "Heebo.ttf").read_bytes()).decode()
    css = (f'@font-face{{font-family:"Heebo";src:url("{font}") format("truetype");font-weight:100 900}}'
           'html,body{margin:0;background:#000;width:1920px;height:1080px;overflow:hidden}'
           'svg{display:block;font-family:"Heebo",sans-serif}text{fill:#fff}'
           '.md{font-size:40px;font-weight:700}.sm{font-size:28px;font-weight:600}.cr{font-size:13px;fill:#aaa}')
    ax, ay = xy(*AMBUSH)
    mx, my = xy(*MIGNAN)
    js = JS % {"T": json.dumps(T), "DUR": DUR, "cx": f"{(ax + mx) / 2:.0f}", "cy": f"{(ay + my) / 2:.0f}"}
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>דפיקה בדלת</title>'
            f'<style>{css}</style></head><body>{svg(route_pts)}<script>{js}</script></body></html>')


def shot(html, t, png, prof):
    for _ in range(3):
        r = subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=3000",
                            f"--user-data-dir={prof}", "--window-size=1920,1080", f"--screenshot={png}",
                            html.as_uri() + f"#t={t:.4f}"], capture_output=True)
        if r.returncode == 0 and Path(png).exists():
            return
    raise RuntimeError(f"frame {t}")


if __name__ == "__main__":
    imagery()
    pts = route()
    html = OUT.with_suffix(".html")
    html.write_text(page(pts), encoding="utf-8")
    shot(html, DUR, OUT.with_suffix(".png"), Path(tempfile.mkdtemp()))
    tmp = Path(tempfile.mkdtemp())
    n = DUR * FPS
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda i: shot(html, i / FPS, tmp / f"{i:04d}.png", tmp / f"p{i}"), range(n)))
    mp4 = OUT.with_suffix(".mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(tmp / "%04d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print("ok", mp4.name, f"{mp4.stat().st_size // 1024} KB")
