# מפות "מהלך הקרב" לכל זירה.
# הבסיס: נתוני OpenStreetMap (assets/maps/<key>.osm), מצוירים כ-SVG בצבעי המצגת.
# מעליהם: חצים, אזורים ונקודות ממוספרות, לפי קואורדינטות (קו רוחב, קו אורך).
# נקודה עם approx=True מצוירת חלולה: המיקום משוער, ומחכה לאימות.

import math
import xml.etree.ElementTree as ET
from html import escape as e
from pathlib import Path

HERE = Path(__file__).parent

# צבע לכל כוח. אותו צבע בחץ, בנקודה ובמקרא.
FORCE = {
    "hq":     ("חפ״ק המח״ט", "#c9a24a"),
    "rotem":  ("גדוד רותם", "#7fb8e6"),
    "tzabar": ("גדוד צבר", "#e8896b"),
    "dsmh":   ("חפ״ק הסמח״ט", "#9fd49a"),
    "civ":    ("פינוי תושבים", "#f6f1e6"),
}

FLOW = {
 "kfaraza": {
  "title": "כפר עזה",
  "when": "7 עד 8 באוקטובר",
  "osm": "kfaraza.osm",
  "bbox": (31.4752, 34.5205, 31.4895, 34.5440),   # S, W, N, E
  "labels": [  # שמות מקומות על המפה
    ((31.47698, 34.53591), "תחנת הדלק", "se"),
    ((31.47930, 34.53640), "השער", "e"),
    ((31.48570, 34.53090), "שכונת הדור הצעיר", "n"),
    ((31.48176, 34.52740), "שכונת ההרחבה", "w"),
    ((31.47700, 34.54250), "כביש 232", "s"),
  ],
  "zones": [  # אזור מקווקו: (מרכז, רדיוס במטרים, כוח, מספר האירוע)
    ((31.48700, 34.53760), 70, "tzabar", 9),
  ],
  "arrows": [  # מסלול: רשימת נקודות, כוח, מקווקו?, מספר האירוע
    ([(31.4756, 34.5370), (31.4770, 34.5363), (31.4789, 34.5354), (31.4804, 34.5340)], "hq", False, 1),
    ([(31.4758, 34.5318), (31.4772, 34.5326), (31.4781, 34.5332)], "rotem", False, 2),
    ([(31.4766, 34.5384), (31.4788, 34.5376), (31.4800, 34.5366)], "hq", False, 3),
    ([(31.4789, 34.5354), (31.4790, 34.5320), (31.4800, 34.5300)], "tzabar", True, 5),
    ([(31.4806, 34.5338), (31.4830, 34.5310), (31.4826, 34.5290)], "dsmh", False, 6),
    ([(31.4845, 34.5326), (31.4815, 34.5340), (31.4789, 34.5354), (31.4772, 34.5360)], "civ", True, 8),
  ],
  "steps": [  # (מיקום, כוח, שעה, טקסט, משוער?)
    ((31.47860, 34.53620), "hq", "11:30", "חפ״ק המח״ט מבקיע בשער בכוח מצומצם, תחת אש כבדה מטווח קצר.", False),
    ((31.47830, 34.53320), "rotem", "כ-12:40", "רותם, שפרק לפני צומת סעד ונע ברגל, נקלע למארב על חפ״ק המג״ד. המארב נשבר באש ובאיגוף של הסמג״ד חורי.", True),
    ((31.48035, 34.53640), "hq", "14:00 עד 14:30", "הנמ״ר שזיווד מעתוק לבד מגיע משדה תימן. על הגדר שני מחבלים מסתערים עליו. מצטרף לרותם בקרב על קו הבתים הראשון.", True),
    ((31.48080, 34.53380), "rotem", "אחר הצהריים", "הבית הראשון: פלוגת החוד של רותם, אלפסי עם 11 לוחמים, וחפ״ק הסמח״ט. 7 מחבלים חוסלו.", True),
    ((31.47990, 34.53020), "tzabar", "אחר הצהריים", "זגורי, קציר ורן משה נכנסים לאורך התעלה בדרום, ובפקודת בטיטו מדלגים תחת PK לבית עם לוחם פצוע קשה.", True),
    ((31.48270, 34.52880), "dsmh", "כ-18:15", "בכניסה לשכונה המערבית אלגרבלי ובצלאל נפגעים, וזילברמן והסמח״ט מושכים אותם למחסה. רכב עם 4 מחבלים תוקף מאחור, ומנדי נפגע.", True),
    ((31.48560, 34.53180), "tzabar", "ערב ולילה", "שכונת הדור הצעיר: נחמני וגוברין מחלצים תושבים מהממ״דים.", True),
    ((31.48440, 34.53260), "civ", "לילה", "94 תושבים יוצאים בשיירה לתחנת הדלק, עטופים בלוחמים. ההאמר של ליבמן בראש, עם מי שלא יכול ללכת.", True),
    ((31.48700, 34.53760), "tzabar", "8.10 ערב", "הבית האחרון, בקצה הצפון-מזרחי: דור שדה ז״ל נופל. אלפסי וזגורי מחליטים לא להיכנס שוב. לאו, טנק ו-D9.", True),
  ],
  "note": "מיקומי האירועים משוערים לפי הראיונות (נקודה חלולה), ומחכים לאימות מול החטיבה.",
 },
}


def _proj(bbox, wid):
    S, W, N, E = bbox
    k = math.cos(math.radians((S + N) / 2))
    hgt = wid * (N - S) / ((E - W) * k)
    m_per_px = (E - W) * k * 111320 / wid
    return (lambda la, lo: ((E - lo) / (E - W) * wid if False else (lo - W) / (E - W) * wid, (N - la) / (N - S) * hgt)), hgt, m_per_px


_BASE_ST = {
    "park": "fill:#43305c;fill-opacity:.55;stroke:none",
    "land": "fill:#45246a;stroke:none",
    "water": "fill:none;stroke:#5d7fae;stroke-width:2",
    "track": "fill:none;stroke:#6e5a8a;stroke-width:1;stroke-dasharray:4 3",
    "minor": "fill:none;stroke:#7d6a99;stroke-width:1.1",
    "res": "fill:none;stroke:#a998c4;stroke-width:2.4",
    "main": "fill:none;stroke:#e4dcef;stroke-width:5",
    "bld": "fill:#9a86b9;stroke:#2c1040;stroke-width:.6",
}


def base_svg(osm_path, proj):
    xy = proj
    r = ET.parse(osm_path).getroot()
    nodes = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in r.iter("node")}
    layers = {k: [] for k in _BASE_ST}

    def d(nd, close):
        pts = [xy(*nodes[x]) for x in nd if x in nodes]
        if len(pts) < 2:
            return ""
        return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + (" Z" if close else "")

    for w in r.iter("way"):
        t = {x.get("k"): x.get("v") for x in w.iter("tag")}
        nd = [x.get("ref") for x in w.iter("nd")]
        closed = len(nd) > 2 and nd[0] == nd[-1]
        hw = t.get("highway")
        if "building" in t:
            layers["bld"].append(d(nd, True))
        elif t.get("landuse") == "residential":
            layers["land"].append(d(nd, True))
        elif closed and (t.get("leisure") in ("park", "pitch", "playground") or
                         t.get("landuse") in ("forest", "orchard", "meadow", "cemetery")):
            layers["park"].append(d(nd, True))
        elif t.get("waterway"):
            layers["water"].append(d(nd, False))
        elif hw in ("primary", "secondary"):
            layers["main"].append(d(nd, False))
        elif hw in ("tertiary", "residential", "unclassified"):
            layers["res"].append(d(nd, False))
        elif hw in ("service", "footway", "path"):
            layers["minor"].append(d(nd, False))
        elif hw == "track":
            layers["track"].append(d(nd, False))
    order = ["park", "land", "water", "track", "minor", "res", "main", "bld"]
    return "".join(f'<g style="{_BASE_ST[k]}">' + "".join(f'<path d="{p}"/>' for p in layers[k] if p) + "</g>" for k in order)


def flow_svg(key, wid=1000):
    f = FLOW[key]
    xy, hgt, mpp = _proj(f["bbox"], wid)
    out = [f'<svg class="fmap" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {wid} {hgt:.0f}">',
           '<defs>' + "".join(
               f'<marker id="ah-{k}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
               f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for k, (_, c) in FORCE.items()) + '</defs>',
           f'<rect width="{wid}" height="{hgt:.0f}" fill="#2c1040"/>',
           base_svg(HERE / "assets" / "maps" / f["osm"], xy)]
    for (la, lo), rad, fk, st in f["zones"]:
        x, y = xy(la, lo)
        out.append(f'<circle class="zn" data-step="{st}" cx="{x:.0f}" cy="{y:.0f}" r="{rad / mpp:.0f}" fill="{FORCE[fk][1]}" fill-opacity=".14" '
                   f'stroke="{FORCE[fk][1]}" stroke-width="2" stroke-dasharray="6 4"/>')
    for pts, fk, dashed, st in f["arrows"]:
        p = [xy(*q) for q in pts]
        dd = f"M{p[0][0]:.0f},{p[0][1]:.0f} " + " ".join(f"L{a:.0f},{b:.0f}" for a, b in p[1:])
        dash = ' stroke-dasharray="10 7"' if dashed else ""
        out.append(f'<g class="ar" data-step="{st}" data-dashed="{int(dashed)}" data-color="{FORCE[fk][1]}">'
                   f'<path d="{dd}" fill="none" stroke="#2c1040" stroke-width="9" stroke-linejoin="round" opacity=".6"/>'
                   f'<path class="arl" d="{dd}" fill="none" stroke="{FORCE[fk][1]}" stroke-width="5" stroke-linejoin="round" '
                   f'stroke-linecap="round"{dash} marker-end="url(#ah-{fk})"/></g>')
    anchor = {"n": (0, -16, "middle"), "s": (0, 28, "middle"), "e": (14, 6, "start"), "w": (-14, 6, "end"), "se": (12, 24, "start")}
    for (la, lo), txt, pos in f["labels"]:
        x, y = xy(la, lo)
        dx, dy, ta = anchor[pos]
        # SVG בעברית: text-anchor הפוך בכיוון RTL, ולכן מחליפים start ו-end
        ta = {"start": "end", "end": "start"}.get(ta, ta)
        out.append(f'<text x="{x + dx:.0f}" y="{y + dy:.0f}" text-anchor="{ta}" class="fl">{e(txt)}</text>')
    for i, ((la, lo), fk, *_rest) in enumerate(f["steps"], 1):
        x, y = xy(la, lo)
        c = FORCE[fk][1]
        approx = _rest[-1]
        fill = "#2c1040" if approx else c
        tc = c if approx else "#2c1040"
        out.append(f'<g class="mk" data-step="{i}" style="--c:{c}" transform="translate({x:.0f} {y:.0f})">'
                   f'<circle class="pulse" r="17" fill="none" stroke="{c}" stroke-width="3"/>'
                   f'<circle r="17" fill="{fill}" stroke="{c}" stroke-width="3.5"/>'
                   f'<text y="7" text-anchor="middle" class="fn" fill="{tc}">{i}</text></g>')
    # קנה מידה: 200 מטר
    sb = 200 / mpp
    out.append(f'<g class="sb"><line x1="24" y1="{hgt - 26:.0f}" x2="{24 + sb:.0f}" y2="{hgt - 26:.0f}" stroke="#e4dcef" stroke-width="3"/>'
               f'<text x="{24 + sb / 2:.0f}" y="{hgt - 36:.0f}" text-anchor="middle" class="fs">200 מ׳</text>'
               f'<text x="{wid - 16}" y="{hgt - 14:.0f}" text-anchor="end" direction="ltr" class="fs">© OpenStreetMap contributors</text>'
               f'<text x="{wid - 30}" y="44" text-anchor="middle" class="fnorth">N</text>'
               f'<path d="M{wid - 30},14 l-8,18 l8,-5 l8,5 z" fill="#e4dcef"/></g>')
    out.append("</svg>")
    return "".join(out)


def flow_steps_html(key):
    f = FLOW[key]
    rows = []
    for i, (_pt, fk, when, txt, approx) in enumerate(f["steps"], 1):
        c = FORCE[fk][1]
        tc = "#8a7f93" if fk == "civ" else c
        rows.append(f'<div class="fstep"><span class="fnum{" ap" if approx else ""}" style="--c:{c}">{i}</span>'
                    f'<div><b>{e(when)}</b> · <span class="ff" style="color:{tc}">{e(FORCE[fk][0])}</span><p>{e(txt)}</p></div></div>')
    used = []
    for _pt, fk, *_ in f["steps"]:
        if fk not in used:
            used.append(fk)
    for a in f["arrows"]:
        fk = a[1]
        if fk not in used:
            used.append(fk)
    leg = "".join(f'<span><i style="background:{FORCE[k][1]}"></i>{e(FORCE[k][0])}</span>' for k in used)
    return "".join(rows), leg
