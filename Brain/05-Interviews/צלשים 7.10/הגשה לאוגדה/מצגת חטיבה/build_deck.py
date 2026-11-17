"""בונה את מצגת חטיבת גבעתי לוועדת הצל"שים של אוגדה 162 (PDF לרוחב, 16:9).

שימוש:  python3 build_deck.py            -> PDF + בדיקת גלישה
        python3 build_deck.py --preview  -> גם גיליונות תצוגה מקדימה (PNG) בתיקייה preview/
"""
import html, json, math, pathlib, subprocess, sys
from deck_data import CAND, FALLEN, RANK_ORDER, PLACES, BORDER, ARENAS
from battle_maps import FLOW, flow_svg, flow_steps_html

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT_PDF = HERE / "מצגת חטיבת גבעתי - ועדת צלשים אוגדה 162.pdf"
CARDS = {json.loads(l)["n"]: json.loads(l) for l in open(HERE / "cards.jsonl", encoding="utf-8")}


def e(s):
    return html.escape(str(s or ""))


def num(s):
    """מספר עם סימנים (25+, 90–100): משמאל לימין, אלא אם יש בו עברית."""
    heb = any("\u0590" <= ch <= "\u05ff" for ch in str(s))
    return f'<b{"" if heb else " dir=ltr"}>{e(s)}</b>'


# ---------------------------------------------------------------- מרשם
def xy(lat, lon):
    return (lon - 34.25) * 1000, (31.62 - lat) * 1000


def map_svg(hi=(), sec=(), counts=None, labels=True, cls="map"):
    """hi: מפתחות זירה מודגשים. sec: זירות משניות. counts: {arena_key: n} למרשם הגדול."""
    bpts = [xy(*p) for p in BORDER]
    coast = [xy(*p) for p in [(31.585, 34.487), (31.52, 34.43), (31.42, 34.34), (31.35, 34.28), (31.315, 34.25)]]
    gaza = bpts[:-1] + [xy(31.30, 34.25)] + coast[::-1]
    sea = [(0, 0), xy(31.62, 34.52)] + coast + [(0, 0)]
    poly = lambda pts: " ".join(f"{x:.0f},{y:.0f}" for x, y in pts)
    s = [f'<svg class="{cls}" viewBox="0 0 500 420" xmlns="http://www.w3.org/2000/svg">',
         f'<rect width="500" height="420" fill="var(--land)"/>',
         f'<polygon points="{poly(sea)}" fill="var(--sea)"/>',
         f'<polygon points="{poly(gaza)}" fill="var(--gaza)"/>',
         f'<polyline points="{poly(bpts)}" fill="none" stroke="var(--border)" stroke-width="2.2" stroke-dasharray="6 4"/>']
    if labels:
        s.append('<text x="108" y="238" class="gz" text-anchor="middle" transform="rotate(-52 108 238)">רצועת עזה</text>'
                 '<text x="70" y="95" class="sealbl" text-anchor="middle">הים התיכון</text>')
    # נקודות לפי זירה
    arena_of = {}
    for a in ARENAS:
        for p in a["points"]:
            arena_of[p] = a["key"]
    arena_of["teiman"] = None
    for key, (name, lat, lon) in PLACES.items():
        x, y = xy(lat, lon)
        ak = arena_of.get(key)
        if key == "teiman":
            s.append(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" fill="none" stroke="var(--hq)" stroke-width="2"/>')
            if labels:
                s.append(f'<text x="{x-12}" y="{y+4}" class="pl hq" text-anchor="end">{e(name)}</text>')
                s.append(f'<text x="{x-12}" y="{y+20}" class="pl hq small" text-anchor="end">מטה החטיבה</text>')
            continue
        if counts is not None:
            n = counts.get(ak, 0)
            first_point = ak and next(a for a in ARENAS if a["key"] == ak)["points"][0] == key
            r = 6 + 3.2 * math.sqrt(n) if first_point else 7
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r+7:.0f}" fill="var(--gold)" opacity=".18"/>')
            s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="var(--gold)" stroke="#fff" stroke-width="2"/>')
            if first_point and n:
                s.append(f'<text x="{x:.0f}" y="{y+6:.0f}" class="cnt" text-anchor="middle">{n}</text>')
        else:
            on = ak in hi
            so = ak in sec
            if on:
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="var(--gold)" opacity=".25"/>')
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="9" fill="var(--gold)" stroke="#fff" stroke-width="2.5"/>')
            elif so:
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="var(--gold-soft)" opacity=".85" stroke="#fff" stroke-width="1.5"/>')
            else:
                s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="var(--dot)"/>')
        if labels:
            right = key in ("sderot", "ofakim", "yakhini", "urim", "nova", "reim", "kfaraza", "netiv", "niryitzhak", "holit")
            anchor = "start" if right else "end"
            if counts is not None:
                n = counts.get(ak, 0)
                fp = ak and next(a for a in ARENAS if a["key"] == ak)["points"][0] == key
                rr = 6 + 3.2 * math.sqrt(n) if fp else 7
                gap = rr + 6
            else:
                gap = 14
            dx = gap if right else -gap
            dy = {"reim": 20, "nova": -6, "holit": 12, "niryitzhak": 0}.get(key, 5)
            weight = " strong" if (counts is not None or ak in hi) else ""
            s.append(f'<text x="{x+dx:.0f}" y="{y+dy:.0f}" class="pl{weight}" text-anchor="{anchor}">{e(name)}</text>')
    s.append("</svg>")
    return "".join(s)


# ---------------------------------------------------------------- רכיבים
WAVES = """<svg class="waves" viewBox="0 0 1600 900" preserveAspectRatio="none"><g fill="none" stroke="#fff" stroke-opacity=".07" stroke-width="1.6">
<path d="M0 70 C300 20 600 130 900 60 S1400 10 1600 50"/><path d="M0 105 C320 55 620 165 920 95 S1420 45 1600 85"/>
<path d="M0 780 C300 730 600 840 900 770 S1400 720 1600 760"/><path d="M0 815 C320 765 620 875 920 805 S1420 755 1600 795"/>
<path d="M0 850 C300 800 600 910 900 840 S1400 790 1600 830"/></g></svg>"""

FOOT_TXT = "חטיבת גבעתי · ועדת צל״שים, אוגדה 162"


def top(kicker, title):
    return (f'<div class="top"><div class="tt"><span class="k">{e(kicker)}</span><span class="h">{e(title)}</span></div>'
            f'<div class="logos"><img src="assets/givati-small.png"><img src="assets/ugda162.png"></div></div>')


def foot(dark=False):
    return f'<div class="foot{" dk" if dark else ""}"><span>{FOOT_TXT}</span><span class="cl">- שמור -</span><span class="pg"></span></div>'


def slide(inner, cls=""):
    return f'<section class="s {cls}">{inner}</section>'


def arena_by_key(k):
    return next(a for a in ARENAS if a["key"] == k)


def level_cls(lv):
    if "עיטור" in lv:
        return "lv-top"
    if "רמטכ" in lv:
        return "lv-ram"
    return ""


def rank_key(n):
    r = CAND[n][0]
    for i, rk in enumerate(RANK_ORDER):
        if r.startswith(rk):
            return i
    return 9


def cands_in(arena_key):
    ns = [n for n, c in CAND.items() if c[5] == arena_key]
    return sorted(ns, key=lambda n: (rank_key(n), n))


def full_name(n):
    return f"{CAND[n][0]} {CAND[n][1]}"


# ---------------------------------------------------------------- שקפים
def s_cover():
    return slide(f"""{WAVES}<div class="cv">
<div class="classif">- שמור -</div>
<div class="badge"><figure><img src="assets/givati.png"><figcaption>חטיבת גבעתי</figcaption></figure>
<figure><img src="assets/ugda162.png"><figcaption>אוגדה 162</figcaption></figure></div>
<div class="kind">ועדת צל״שים · אוגדה 162</div>
<div class="title">חטיבת גבעתי ב-7 באוקטובר</div>
<div class="sub">מצגת החטיבה: תמונת המצב, זירות הלחימה והמועמדים</div>
<div class="rule"></div>
<div class="nums"><div><b>60</b><span>מועמדים אישיים</span></div><div><b>11</b><span>זירות לחימה</span></div>
<div><b>7</b><span>גדודים וכוחות</span></div><div><b>5</b><span>ימי לחימה, 7 עד 11.10</span></div></div>
</div><div class="cvfoot">מלחמת חרבות ברזל · מ-7.10 ועד תחילת התמרון</div>""", "dark cover")


def s_agenda():
    items = [("תמונת מצב חטיבתית", "סד״כ החטיבה ב-6.10, ומהלך הלחימה ב-7.10"),
             ("זירות הלחימה", "מרשם הזירות, ציר הזמנים ופריסת המועמדים"),
             ("פיקוד ושליטה", "המח״ט, הסמח״ט ומטה החטיבה"),
             ("הזירות והמועמדים", "לכל זירה: סדר הכוחות וסיפור הגדוד, ושקף לכל מועמד"),
             ("חיבור לתחקירים", "תחקירי צה״ל לכל זירה, והמלצות יחידתיות")]
    rows = "".join(f'<div class="ag"><b>{i}</b><div><h3>{e(t)}</h3><p>{e(d)}</p></div></div>' for i, (t, d) in enumerate(items, 1))
    return slide(top("סדר המצגת", "מה נציג") + f'<div class="body agenda">{rows}</div>' + foot())


def s_picture():
    rows = [("מטה החטיבה", "שדה תימן", "שבת וחג. המח״ט והסמח״ט בביתם."),
            ("גדוד שקד", "קו באיו״ש", "השבת השנייה בגזרה, עם ציוד שהותאם לתעסוקה."),
            ("גדוד רותם", "צנובר, רמת הגולן", "בכוננות."),
            ("גדוד צבר", "בבית", "ברגילה. הנשקים מאופסנים."),
            ("סיירת גבעתי", "משמר הנגב, איו״ש והגולן", "לא בכוננות. רוב הלוחמים בבית, ופלגות ההכשרה בשבוע האחרון של המסלול."),
            ("גדס״ם גבעתי, מילואים", "בבית", "בלי צווים."),
            ("גדוד 9, חטיבה 401", "אימון בגולן", "צורף לחטיבה ב-7.10."),
            ("קצינים מחוץ לגדודים", "קורסים ותפקידי מטה", "פו״ם, בה״ד 1, מל״י וזרוע היבשה.")]
    tr = "".join(f'<tr><td class="f">{e(a)}</td><td class="w">{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in rows)
    return slide(top("תמונת מצב חטיבתית", "ערב 6 באוקטובר: חטיבה בחג, מפוזרת על פני הארץ") + f"""<div class="body two">
<div class="col"><table class="tb"><tr><th>כוח</th><th>מיקום</th><th>מצב</th></tr>{tr}</table></div>
<div class="col side"><div class="callout"><div class="lab">שבת, שמחת תורה</div>
<p>בבוקר 7.10 אף אחד מכוחות החטיבה לא היה פרוס בעוטף. הגדודים הגיעו מאיו״ש, מהגולן ומהבית, בהרכב חלקי ובציוד חלקי.</p></div>
<div class="callout g"><div class="lab">עד הצהריים</div><p>החטיבה כולה נלחמת בארבע זירות במקביל: כפר עזה, נחל עוז, הנובה ורעים, וכיסופים.</p></div></div>
</div>""" + foot())


GANTT = [  # זירה, [(יום, שעה-התחלה, יום, שעה-סוף)], תווית
    ("sderot", [(7, 6.3, 7, 16.5)], "המח״ט, הסיירת, וכוח של שקד ככוח תגובה"),
    ("nova", [(7, 10.5, 7, 14.5)], "כוח מג״ד שקד, ואחריו כוח הסמח״ט"),
    ("reim", [(7, 9, 7, 13)], "מ״פים של צבר, וכוח מג״ד שקד בדרכו"),
    ("kfaraza", [(7, 11.5, 9, 9)], "חפ״ק המח״ט, רותם, צבר, כוח הסמח״ט"),
    ("nahaloz", [(7, 12.75, 11, 12)], "הסיירת, והגדס״ם בפינוי החללים"),
    ("kissufim", [(7, 14, 10, 12)], "גדוד 9 ופלוגות שקד"),
    ("north", [(7, 8, 7, 23)], "גדס״ם: נתיב העשרה"),
    ("south", [(7, 8, 10, 12)], "קצינים מבה״ד 1 ומל״י"),
    ("ofakim", [(7, 7.5, 7, 11.5)], "קציני גבעתי שהיו בבית"),
]


def gx(day, hour):
    # 7.10: 06:00-24:00 = 50% מהרוחב. 8-11.10: 12.5% כל יום.
    if day == 7:
        return max(0, (hour - 6) / 18) * 50
    return 50 + (day - 8) * 12.5 + hour / 24 * 12.5


def s_gantt():
    axis = "".join(f'<div class="tick" style="right:{gx(7,h)}%"><span>{h:02d}:00</span></div>' for h in (6, 9, 12, 15, 18, 21))
    axis += "".join(f'<div class="tick day" style="right:{gx(d,0)}%"><span>{d}.10</span></div>' for d in (8, 9, 10, 11))
    rows = ""
    for k, spans, lab in GANTT:
        a = arena_by_key(k)
        bars = "".join(f'<div class="bar{" main" if a["main"] else ""}" style="right:{gx(d1,h1)}%;width:{gx(d2,h2)-gx(d1,h1)}%"></div>'
                       for d1, h1, d2, h2 in spans)
        rows += f'<div class="gr"><div class="gl"><b>{e(a["short"])}</b><span>{e(lab)}</span></div><div class="gt">{bars}</div></div>'
    marks = [(7, 10.5, "10:30 · החטיבה מתחלקת לזירות"), (7, 23.9, "לילה · חילוץ תושבים בכל הזירות")]
    mk = "".join(f'<div class="gm" style="right:{gx(d,h)}%"><span>{e(t)}</span></div>' for d, h, t in marks)
    return slide(top("ציר הזמנים", "המאמץ החטיבתי: מתי פעלה החטיבה בכל זירה") + f"""<div class="body gantt">
<div class="gh"><div class="gl"></div><div class="gt axis">{axis}</div></div>
<div class="gwrap">{rows}<div class="gmarks">{mk}</div></div>
<p class="note">7 באוקטובר מוצג בהרחבה (06:00 עד חצות). מ-8.10 כל יום מוצג כיחידה אחת. הזמנים לפי תיקי הכוח והמועמד, ויש לדייק אותם מול תחקירי צה״ל.</p>
</div>""" + foot())


def s_map(counts):
    leg = ""
    for a in ARENAS:
        n = counts.get(a["key"], 0)
        leg += f'<div class="lg{"" if a["main"] else " minor"}"><b>{n}</b><span>{e(a["name"])}</span><i>{e(a["when"])}</i></div>'
    return slide(top("זירות הלחימה", "מרשם חטיבתי: 11 זירות, 60 מועמדים") + f"""<div class="body mapwrap">
<div class="bigmap">{map_svg(counts=counts)}</div>
<div class="legend"><div class="lh">מועמדים לפי זירת המעשה העיקרית</div>{leg}
<p class="note">מרשם סכמטי, לא בקנה מידה. בעיגול: מספר המועמדים שזו זירתם העיקרית. ■ שדה תימן: בסיס מטה החטיבה.</p></div>
</div>""" + foot())


def s_counts(counts, sec_counts):
    mx = max(counts.get(a["key"], 0) + sec_counts.get(a["key"], 0) for a in ARENAS)
    bars = ""
    for a in sorted(ARENAS, key=lambda a: -counts.get(a["key"], 0)):
        n = counts.get(a["key"], 0)
        s2 = sec_counts.get(a["key"], 0)
        w = n / mx * 100
        w2 = s2 / mx * 100
        bars += (f'<div class="hb"><div class="hl">{e(a["short"])}</div><div class="ht"><div class="hf" style="width:{w}%"></div>'
                 f'<div class="hs" style="width:{w2}%;right:{w}%"></div></div><div class="hn">{n}'
                 f'{f"<em>ועוד {s2}</em>" if s2 else ""}</div></div>')
    forces = {}
    levels = {}
    for c in CAND.values():
        forces[c[3]] = forces.get(c[3], 0) + 1
        levels[c[4]] = levels.get(c[4], 0) + 1
    lv_order = ['עיטור העוז', 'עיטור המופת', 'צל"ש רמטכ"ל', 'צל"ש אלוף', 'צל"ש מאו"ג', 'צל"ש מח"ט', 'צל"ש', 'אות הערכה', 'טרם נקבע']
    lvs = "".join(f'<div class="chip {level_cls(l)}"><b>{levels[l]}</b>{e(l)}</div>' for l in lv_order if l in levels)
    fs = "".join(f'<div class="fr"><span>{e(f)}</span><b>{n}</b></div>' for f, n in sorted(forces.items(), key=lambda x: -x[1]))
    return slide(top("המועמדים", "מספר המועמדים לפי מרחבי הלחימה") + f"""<div class="body counts">
<div class="col bars"><div class="lh">לפי זירה <span>· פס מלא: הזירה העיקרית · פס בהיר: לחמו גם בזירה</span></div>{bars}</div>
<div class="col side"><div class="lh">לפי כוח</div><div class="forces">{fs}</div>
<div class="lh" style="margin-top:26px">לפי רמת ההמלצה</div><div class="chips">{lvs}</div></div>
</div>""" + foot())


def s_c2():
    cols = [("המח״ט", "אל״מ לירון בטיטו", ["ממונה בדרך למפקד העיר שדרות, וחובר למשטרה ולראש העיר.",
                                          "מזהה את כביש 232 כציר מסוכן, ומורה לכל הכוחות להגיע ממערב בלבד.",
                                          "מוסר את שדרות לכוח צנחנים, ומחלק את החטיבה לזירות.",
                                          "מורה לנוע בשטחים פתוחים ולהביא את שני הנמ״רים.",
                                          "נכנס בעצמו לכפר עזה בכוח ההבקעה."]),
            ("הסמח״ט", "סא״ל דוד רון", ["מפעיל את מטה החטיבה במלואו בשדה תימן.",
                                       "מוביל את גיוס הגדודים ואנשי המילואים.",
                                       "מרכיב כוח מקצינים מהסדיר ומהמילואים, עם רופא החטיבה.",
                                       "נלחם בנובה, ומשם בכפר עזה, עד 9.10."]),
            ("מטה החטיבה", "אג״ם, חמ״ל, רפואה ולוגיסטיקה", ["קצין האג״ם מתריע בפני המפקדים ומכווין אותם לצירים בטוחים.",
                                                         "תמונת מצב מתצפיות, פניות תושבים וטבלת נעדרים. ארבעה לוחמים נעדרים אותרו.",
                                                         "קרפ״ח החטיבה מקים יכולת פינוי רפואי שלא הייתה בגזרה.",
                                                         "רס״ר הסיירת פותח את מחסני החירום, ונמ״ר המח״ט מזווד תוך כ-45 דקות."])]
    html_cols = ""
    for t, who, items in cols:
        li = "".join(f"<li>{e(x)}</li>" for x in items)
        html_cols += f'<div class="c2c"><div class="c2h"><b>{e(t)}</b><span>{e(who)}</span></div><ul>{li}</ul></div>'
    return slide(top("פיקוד ושליטה", "עבודת המטה, הפיקוד והשליטה ב-7.10") + f'<div class="body c2">{html_cols}</div>' + foot())


ARENA_TXT = {
 "sderot": {
  "forces": [("חפ״ק המח״ט", "06:20", "המח״ט ממונה בדרך למפקד העיר, חובר למשטרה ולראש העיר, ומזהה את תחנת המשטרה כמוקד הלחימה."),
             ("קצין האג״ם", "07:15", "בדרך לבסיס מסתער על מחבלים בצומת שער הנגב, וחובר לחפ״ק המח״ט."),
             ("סיירת גבעתי", "08:30 עד 10:30", "כוחות ראשונים נלחמים בעיר. עד 10:30 נצברת היחידה כולה ומתחילה בסריקות."),
             ("פלוגה רובאית של שקד", "12:30 עד 16:30", "פועלת בעיר ככוח תגובה, בפיקוד מפקד בא״ח צנחנים.")],
  "story": "המח״ט זיהה את כביש 232 כציר מסוכן, והורה לכל הכוחות להגיע ממערב בלבד. בסביבות 10:30, עם קריאה לעזרה ביישובים, מסר את הפיקוד על שדרות למפקד בא״ח צנחנים וחילק את החטיבה לזירות.",
  "stats": []},
 "nova": {
  "forces": [("כוח מג״ד שקד", "כ-10:30", "12 לוחמים מאיו״ש ושלושה לוחמי מצדה מגיעים לטנק פגוע כקילומטר מהמסיבה, ומסתערים רגלית לתוך המתחם."),
             ("כוח מג״ד שקד", "11:50 עד 12:10", "הפיקוד במתחם עובר למ״פ המסייעת. שליטה ברחבה, ונקודת איסוף פצועים בקרוואנים."),
             ("כוח הסמח״ט", "13:00 עד 14:30", "סריקת הבר, הקמפינג והנחל הסבוך, לפי נקודות ציון של מסתתרים."),
             ("נהגי הכוח", "לאורך היום", "פינוי פצועים בלי נשק, מהטנק הפגוע אל אמבולנסים בצמתים.")],
  "story": "חניון רעים ומתחם המסיבה מוצגים כאן כזירה אחת: הנובה.",
  "stats": [("25+", "מחבלים חוסלו במתחם"), ("כ-100", "אנשים חולצו מהמתחם"), ("כ-50", "ניצולים יצאו מהנחל")]},
 "reim": {
  "forces": [("מ״פים של צבר", "בוקר", "נחמני וגוברין יצאו מהבית עם נשק אישי, חברו למח״ט בשדרות ונשלחו לקיבוץ. פרצו תחת אש ממארב בכניסה ולחמו מטווח קרוב."),
             ("כוח מג״ד שקד", "צהריים", "בדרך מהנובה לכיסופים חצה את הצומת, וסייע לכוח בקיבוץ לאתר חייל חסר.")],
  "story": "משם המשיכו מפקדי הפלוגות של צבר לכפר עזה, ונלחמו שם עד 9.10.",
  "stats": []},
 "kfaraza": {
  "forces": [("חפ״ק המח״ט", "11:30", "הבקעה לקיבוץ בכוח מצומצם, תחת אש כבדה מטווח קצר."),
             ("גדוד רותם", "צהריים", "פורק לפני צומת סעד, מתקדם ברגל ומפרק מארב מתוכנן. פלוגת החוד כובשת את הבית הראשון."),
             ("נמ״ר המח״ט", "14:00 עד 14:30", "מעתוק מביא את הנמ״ר משדה תימן. מצטרף לרותם בקרב על קו הבתים הראשון."),
             ("גדוד צבר", "אחר הצהריים", "המג״ד נכנס בראש 11 לוחמים, ויחד עם הסמח״ט מחסל 7 מחבלים בבית הראשון. מ-19:00 מוביל את טיהור הגזרה."),
             ("כוח הסמח״ט", "אחר הצהריים וערב", "מגיע מהנובה. בבית הראשון עם צבר, ובסמטה בדרך לשכונה המערבית: שלושה נפגעים, וארבעה מחבלים שתקפו מאחור חוסלו."),
             ("גדס״ם במילואים", "לילה", "פינוי תחת ירי בשער הקיבוץ, וכניסה עם אוטובוסים לפינוי אזרחים.")],
  "story": "מארבים בהיקף הקיבוץ בלמו מחבלים שניסו לתגבר. מילת קוד שפורסמה בקבוצת הקיבוץ פתחה את דלתות הממ״דים. ב-9.10 בבוקר נמסרה הגזרה לכוח שהחליף.",
  "stats": [("12+", "טנדרים של מחבלים בקיבוץ"), ("94", "תושבים הוצאו בלילה הראשון מגזרת צבר"), ("7", "מחבלים חוסלו בבית הראשון")]},
 "nahaloz": {
  "forces": [("סיירת גבעתי", "11:20 עד 13:00", "פקודה לכבוש קיבוץ שאין בו כוח מגן, וכניסה עם 250 עד 300 לוחמים. בשער: הצנחנים למוצב, הסיירת לקיבוץ."),
             ("סיירת גבעתי", "14:30 עד 17:30", "קרב רדיפה אחרי מחבלים בורחים. כ-11 מחבלים חוסלו, וניסיון להעביר גופות לרצועה סוכל."),
             ("סיירת גבעתי", "לילה", "פינוי כ-359 תושבים בנמ״רים וברכבי היחידה."),
             ("גדס״ם במילואים", "8.10", "פינוי החללים והנרצחים מהקיבוץ, פעמים רבות תחת אש."),
             ("סיירת גבעתי", "8 עד 11.10", "הגנה על הקיבוץ מול מחבלים שניסו לחזור.")],
  "story": "",
  "stats": [("359", "תושבים פונו"), ("כ-11", "מחבלים חוסלו בקרב הרדיפה"), ("4", "ימי הגנה על הקיבוץ")]},
 "kissufim": {
  "forces": [("גדוד 9, חטיבה 401", "7.10", "כוח של כשמונה לוחמים נלחם במוצב עם כוח אגוז, ומפנה את החמ״ל. בערב המג״ד לוקח פיקוד על הקיבוץ."),
             ("כוח מג״ד שקד", "אחר הצהריים", "נקלע למארב בצומת השכונה הצפונית. הכוח חבר למג״ד 9, וקיבל ממנו את משימת החילוצים."),
             ("פלוגות שקד", "לילה", "סבבי חילוץ ברכבים ממוגנים, ופינוי תושבים מבתיהם."),
             ("פלוגות שקד", "8.10 בבוקר", "הכרעת הבית שבו התבצר מחבל."),
             ("גדוד 9", "9 עד 10.10", "סריקה חוזרת, והקיבוץ נמסר נקי לגדוד מילואים.")],
  "story": "",
  "stats": [("8", "לוחמים בכוח שנכנס למוצב"), ("4", "ימים בכיסופים")]},
}

BATT = {
 "shaked": ("גדוד שקד", "כוח מג״ד שקד: סא״ל יאיר אטיאס", "קו באיו״ש", [
   ("יוצא דרומה ביוזמתו", "בסביבות 07:00 קיבל המג״ד את התמונה מהטנדר בשדרות, הקפיץ את הגדוד ויצא מאיו״ש עם הכוח הזמין: 12 לוחמים. את הירידה אישר בדרך מח״ט הגזרה."),
   ("דרך שדה הקטל", "בכביש 234 אסף שלושה לוחמי מצדה. חלף על פני רעים תחת ירי, עד טנק פגוע כקילומטר לפני המסיבה, שלידו היו 40 עד 50 אזרחים ופצועים."),
   ("ההסתערות למתחם", "שתי חוליות בפיקוד המ״פים. פריצת הגדר, קרב של כ-20 דקות, ולפחות 25 מחבלים חוסלו. כ-100 אנשים חולצו."),
   ("רעים וכיסופים", "הכוח המשיך לרעים ולכיסופים, נקלע למארב בצומת השכונה הצפונית ופינה את פצועיו בנמ״ר. בלילה ובבוקר: חילוץ תושבים והכרעת מחבל מתבצר.")],
   [("12", "לוחמים יצאו מאיו״ש"), ("25+", "מחבלים חוסלו במתחם"), ("3", "זירות לחימה ברצף")], "גדוד שקד"),
 "rotem": ("גדוד רותם", "גדוד 435 · סא״ל ענאן פארס", "צנובר, רמת הגולן", [
   ("מהגולן לצומת סעד", "המג״ד העלה את הגדוד על רכבים ואוטובוסים עם השיחה הראשונה עם המח״ט. בצהריים פרק לפני צומת סעד והתקדם ברגל, כדי לא להיכנס למארב בצמתים."),
   ("המארב על החפ״ק", "בדרך לקיבוץ נקלע הגדוד למארב מתוכנן של מחבלים רבים. הסמג״ד איגף, והמארב נשבר עוד לפני שהגיע הנמ״ר. המג״ד, דובר ערבית, האזין לרשת הקשר של המחבלים."),
   ("הבית הראשון ושכונה שלמה", "פלוגת החוד כבשה את הבית הראשון בקיבוץ, שבו חוסלו שבעה מחבלים, וליוותה את משפחות שכונת ״הסבתות״ עד האוטובוסים."),
   ("8.10: הבית השישי", "מ״פ המבצעית נפצע קשה והמשיך לירות. קצין האג״ם ריתק את המחבל והסמ״פ חילץ אותו. המג״ד נפצע וחזר ללחימה אחרי דקות.")],
   [("12", "מועמדים מהגדוד"), ("7", "מחבלים בבית הראשון"), ("4", "מחלקות ליוו את התושבים")], "גדוד רותם"),
 "tzabar": ("גדוד צבר", "גדוד 432 · סא״ל אבירן אלפסי", "בבית, ברגילה", [
   ("הקפצה ביוזמת המג״ד", "הגדוד היה ברגילה והנשקים מאופסנים. המג״ד הקפיץ את כל הגדוד, שלח דרומה חפ״קים מאולתרים ויצא בעצמו."),
   ("ארבעה מ״פים שנלחמו כבר בדרך", "יצאו מהבית, חלקם עם נשק אישי בלבד: נחמני וגוברין נלחמו ברעים. קציר סייר באופקים ופינה פצועים, ועם זגורי עבר את כביש 232 תחת איום עד כפר עזה."),
   ("הבית הראשון", "בשער הקיבוץ נכנס המג״ד בראש 11 לוחמים, ובקרב פנים אל פנים, יחד עם הסמח״ט, חוסלו שבעה מחבלים בבית."),
   ("חילוץ התושבים", "מ-19:00 טיהור הגזרה, ו-94 תושבים הוצאו בלילה, עטופים בלוחמים. ב-8.10 כיבוש שיטתי מבית לבית. בבית האחרון נפל סרן דור שדה ז״ל, והגדוד הכריע את המחבלים בטנק ובדחפור.")],
   [("11", "לוחמים נכנסו עם המג״ד"), ("94", "תושבים הוצאו בלילה הראשון"), ("4", "מ״פים נלחמו כבר בדרך")], "גדוד צבר"),
 "sayeret": ("סיירת גבעתי", "סא״ל זיו בואניש", "משמר הנגב, איו״ש והגולן", [
   ("יחידה מפוזרת שהקפיצה את עצמה", "היחידה לא הייתה בכוננות ורוב הלוחמים היו בבית. המפקד הקפיץ את כולם, כולל המילואים. כ-100 לוחמים התארגנו מהבית, וב-08:30 נלחמו כוחות ראשונים בשדרות."),
   ("כניסה לקיבוץ שאין בו כוח מגן", "בסביבות 11:20 קיבל המפקד פקודה לכבוש את נחל עוז, ובסביבות 13:00 נכנס עם 250 עד 300 לוחמים, חילק גזרות, והכוחות סרקו בית אחרי בית."),
   ("קרב הרדיפה", "כעשרה מחבלים בורחים זוהו. שתי פלגות רדפו אחריהם, וניסיון להעביר לרצועה גופות של אזרחים סוכל."),
   ("פינוי והגנה עד 11.10", "כ-359 תושבים פונו עד הבוקר. עד 11.10 הגנה הסיירת על הקיבוץ.")],
   [("359", "תושבים פונו מנחל עוז"), ("250–300", "לוחמים בכניסה לקיבוץ"), ("16", "מלוחמי הסיירת שלחמו ב-7.10 נפלו במלחמה")], "סיירת גבעתי"),
 "b9": ("גדוד 9 (עשת)", "חטיבה 401, צורף לגבעתי · סא״ל נתנאל ביטון", "אימון בגולן", [
   ("ירידה לעוטף", "הגדוד היה באימון בגולן. המג״ד ירד לעוטף באישור מח״ט גבעתי, ועימו פלוגת טנקיסטים במילואים שנלחמה ברגל."),
   ("מוצב כיסופים", "כוח של כשמונה לוחמים נלחם במוצב עם כוח אגוז, ופינה מהחמ״ל פצועים, תצפיתניות, חיילים ואזרחים."),
   ("פיקוד על הקיבוץ", "בשער הקיבוץ לא היה מי שינהל את הכוחות. המג״ד לקח פיקוד, וניהל כוחות מכמה יחידות. כוח מג״ד שקד חבר אליו וקיבל ממנו את משימת החילוצים."),
   ("עד הבית האחרון", "ב-8.10 פינוי גופות האזרחים, ב-9.10 סריקה חוזרת, וב-10.10 נמסר הקיבוץ ריק ונקי לגדוד מילואים.")],
   [("8", "לוחמים בכוח שנכנס למוצב"), ("4", "ימים בכיסופים")], "גדוד 9, צורף לחטיבה"),
 "gadsam": ("גדס״ם גבעתי במילואים", "סא״ל (מיל׳) אלון פייזר", "בבית, בלי צווים", [
   ("הפעלת הגדוד מהדרך", "פחות משעה מתחילת המתקפה הפעיל המג״ד את שרשרת הפיקוד, וקרא למפקדים וללוחמים להתייצב גם בלי צו."),
   ("לבד, עם אקדח, לנתיב העשרה", "הוזהר שבמרחב פועלים מחבלים רבים, ונכנס לבדו. חיבר את חפ״ק סמח״ט הצנחנים, כוח ממעבר ארז וכיתת הכוננות."),
   ("ארבעה מחבלים בחיים", "הכוח איגף את המחבלים וסגר את נתיבי הבריחה שלהם, עד שנכנעו ונלקחו בחיים."),
   ("כפר עזה ונחל עוז", "פינוי אזרחים מכפר עזה כבר בלילה הראשון, ומ-8.10 פינוי החללים והנרצחים מנחל עוז, פעמים רבות תחת אש.")],
   [("4", "מחבלים נלקחו בחיים"), ("כ-14", "לוחמים בכוח המאולתר"), ("2", "משאיות קירור לפינוי החללים")], None),
}

# איפה מוצג כל סיפור גדוד: לפני שקפי המועמדים של הזירה
BATT_BEFORE = {"nova": ["shaked"], "kfaraza": ["rotem", "tzabar"], "nahaloz": ["sayeret"], "kissufim": ["b9"], "north": ["gadsam"]}


def s_arena(a, idx, total_arenas):
    ns = cands_in(a["key"])
    txt = ARENA_TXT.get(a["key"])
    fr = "".join(f'<div class="fo"><div class="fw">{e(w)}</div><div class="fb"><b>{e(f)}</b><p>{e(d)}</p></div></div>'
                 for f, w, d in txt["forces"])
    st = "".join(f'<div class="st">{num(n)}<span>{e(l)}</span></div>' for n, l in txt["stats"])
    names = "".join(f'<li><span>{e(full_name(n))}</span><i class="{level_cls(CAND[n][4])}">{e(CAND[n][4])}</i></li>' for n in ns)
    story = f'<p class="story">{e(txt["story"])}</p>' if txt["story"] else ""
    dense = " dense" if len(ns) > 12 else ""
    return slide(f"""{WAVES}<div class="ar{dense}">
<div class="arside"><div class="arn">זירה {idx} מתוך {total_arenas}</div><h1>{e(a["name"])}</h1><div class="arw">{e(a["when"])}</div>
<div class="armap">{map_svg(hi=[a["key"]], labels=False, cls="mini")}</div>
<div class="arcnt"><b>{len(ns)}</b><span>מועמדים בזירה</span></div></div>
<div class="armain"><div class="lh">סדר הכוחות</div><div class="forcesq">{fr}</div>{story}
{f'<div class="sts">{st}</div>' if st else ''}
<div class="lh nm2">המועמדים בזירה</div><ul class="names{" many" if len(ns) > 12 else ""}">{names}</ul></div>
</div>""" + foot(True), "dark arena")


def s_flow(key):
    """מהלך הקרב בזירה: מפת היישוב, וחצים ונקודות ממוספרות לפי סדר הזמנים."""
    f = FLOW[key]
    rows, leg = flow_steps_html(key)
    return slide(top("מהלך הקרב", f'{f["title"]}, {f["when"]}') + f"""<div class="body flow">
<div class="fmapbox">{flow_svg(key)}</div>
<div class="fside"><div class="lh">לפי סדר הזמנים</div><div class="fsteps">{rows}</div>
<div class="fleg">{leg}</div><p class="note">{e(f["note"])}</p></div>
</div>""" + foot())


def s_batt(key):
    t, sub, where, beats, stats, force_name = BATT[key]
    bt = "".join(f'<div class="beat"><b>{e(h)}</b><p>{e(p)}</p></div>' for h, p in beats)
    st = "".join(f'<div class="st">{num(n)}<span>{e(l)}</span></div>' for n, l in stats)
    if force_name:
        ns = sorted([n for n, c in CAND.items() if c[3] == force_name], key=lambda n: (rank_key(n), n))
    else:
        ns = [37]
    names = "".join(f"<li>{e(full_name(n))}</li>" for n in ns)
    return slide(top("סיפור הגדוד", t) + f"""<div class="body batt">
<div class="bmain"><div class="bsub">{e(sub)} <span class="pill6">6.10: {e(where)}</span></div><div class="beats">{bt}</div>
<div class="sts light">{st}</div></div>
<div class="bside"><div class="lh">מועמדים מהכוח ({len(ns)})</div><ul class="bnames{" many" if len(ns) > 10 else ""}">{names}</ul></div>
</div>""" + foot())


def s_cand(n, pos, tot, a):
    rank, name, role, force, level, ak, sec = CAND[n]
    c = CARDS[n]
    fallen = n in FALLEN
    dec = FALLEN.get(n, "")
    hi = "".join(f'<div class="hc"><b>{e(h)}</b><p>{e(p)}</p></div>' for h, p in c["hi"][:3])
    st = "".join(f'<div class="cs">{num(x)}<span>{e(l)}</span></div>' for x, l in c.get("stats", [])[:3])
    arena_line = c["arena"].replace(";", " ·")
    rib = f'<div class="ribbon"><span>יהי זכרו ברוך</span>{f"<em>{e(dec)}</em>" if dec else ""}</div>' if fallen else ""
    return slide(f"""<div class="cd{" fallen" if fallen else ""}">
<div class="cside">{WAVES}<div class="cin">
<div class="crumb">{e(a["short"])} · {pos} מתוך {tot}</div>
<div class="rank">{e(rank)}</div><div class="nm">{e(name)}</div>
<div class="role">{e(role)}</div><div class="force">{e(force)}</div>
<div class="lvl {level_cls(level)}">{e(level)}</div>{rib}
<div class="cmap">{map_svg(hi=[ak], sec=sec, labels=False, cls="mini")}<div class="ca">{e(arena_line)}</div></div>
</div></div>
<div class="cmain"><div class="why">למה הוא מועמד</div>
<div class="lead">{e(c["lead"])}</div>
<div class="hcs n{len(c["hi"][:3])}">{hi}</div>
{f'<div class="css">{st}</div>' if st else ''}
</div></div>""" + foot(), "cand")


def s_others():
    boxes = [("north", "גדס״ם גבעתי במילואים", "המג״ד נכנס לבדו עם אקדח ליישוב, חיבר כוחות מכמה יחידות, וארבעה מחבלים נלקחו בחיים."),
             ("south", "קצינים מבה״ד 1 ומל״י", "פריצה לבסיס אורים המותקף, חילוץ הסמח״ט של החטיבה הדרומית מניר יצחק, וטיהור שורת יישובים עד רעים."),
             ("ofakim", "קציני גבעתי שהיו בבית", "יצאו להילחם בעיר עם נשק אישי: לחימה בתחנת המשטרה, וחיסול מחבל מבוצר בשכונה."),
             ("yakhini", "גדוד רותם", "סגן מפקד פלוגה נלחם לבדו לצד כוחות ימ״מ מול מחבלים שהגיעו למושבים, בדרכו לפלוגה."),
             ("mishmar", "סיירת גבעתי", "רס״ר היחידה פתח ביוזמתו את מחסני החירום, והבסיס קלט את תושבי נחל עוז שפונו מבתיהם.")]
    html_b = ""
    for k, f, d in boxes:
        a = arena_by_key(k)
        ns = cands_in(k)
        names = "".join(f"<li>{e(full_name(n))}</li>" for n in ns)
        html_b += (f'<div class="ob"><div class="obt"><h3>{e(a["name"])}</h3>'
                   f'<div class="obw">{e(a["when"])} · {e(f)}</div><p>{e(d)}</p><ul>{names}</ul></div>'
                   f'<div class="obm">{map_svg(hi=[k], labels=False, cls="mini")}</div></div>')
    return slide(top("זירות נוספות", "חמש זירות שבהן נלחמו אנשי החטיבה, מחוץ לזירות המרכזיות") + f'<div class="body others">{html_b}</div>' + foot())


def s_debriefs():
    rows = [("תחקיר החטיבה על 7.10", "תמונת המצב, חלוקת הזירות ומה עשה כל כוח", "מטה החטיבה, דרך האוגדה"),
            ("תחקיר הנובה", "מקום כוח מג״ד שקד בציר הזמנים, ומי עוד פעל במתחם", "צוות התחקיר, דרך האוגדה"),
            ("תחקירי כפר עזה", "ההבקעה, המארבים, וחלקם של רותם, צבר וכוח הסמח״ט", "הגדודים, דרך האוגדה"),
            ("תחקיר נחל עוז", "הכניסה לקיבוץ, קרב הרדיפה ופינוי התושבים", "סיירת גבעתי, דרך האוגדה"),
            ("תחקיר כיסופים", "המוצב, המארב בצומת השכונה הצפונית, והפיקוד על הקיבוץ", "גדוד 9 וחטיבה 401"),
            ("תחקיר האוגדה", "המקום של החטיבה בתמונה של כל הגזרה", "אוגדה 162")]
    tr = "".join(f'<tr><td class="f">{e(a)}</td><td>{e(b)}</td><td class="w">{e(c)}</td></tr>' for a, b, c in rows)
    return slide(top("חיבור לתחקירים", "תיאורי האירועים מול תחקירי צה״ל") + f"""<div class="body">
<table class="tb wide"><tr><th>תחקיר</th><th>מה הוא אמור להראות</th><th>ממי לבקש</th></tr>{tr}</table>
<p class="note big">תחקיר מסווג לא מצרפים. מבקשים הפניה לעמוד ולשורה, בתיאום מול מחלקת היסטוריה.</p></div>""" + foot())


def s_units():
    u = [("חטיבת גבעתי", "צל״ש רמטכ״ל ליחידה",
          "חטיבה שהבינה בשעות הראשונות שהמוקד עבר מהעיר אל היישובים, פיצלה את כוחותיה בין כפר עזה, נחל עוז, הנובה ורעים, וכיסופים, נלחמה בהם עד 10 באוקטובר וחילצה מאות תושבים."),
         ("סיירת גבעתי", "צל״ש רמטכ״ל ליחידה",
          "יחידה שהקפיצה את עצמה מהבית, נלחמה בשדרות, כבשה את נחל עוז, סיכלה ניסיון להעביר גופות לרצועה, פינתה כ-359 תושבים והגנה על הקיבוץ עד 11 באוקטובר.")]
    cards = "".join(f'<div class="uc"><h2>{e(a)}</h2><div class="lvl">{e(b)}</div><p>{e(c)}</p></div>' for a, b, c in u)
    return slide(top("המלצות יחידתיות", "שני תיקים יחידתיים") + f'<div class="body units">{cards}</div>' + foot())


def s_close():
    return slide(f"""{WAVES}<div class="cl1">
<div class="q">חטיבה שלא הייתה בעוטף בבוקר,<br>ונלחמה בו עד 11 באוקטובר.</div>
<div class="rule"></div>
<div class="nums"><div><b>60</b><span>מועמדים אישיים</span></div><div><b>11</b><span>זירות</span></div>
<div><b>359</b><span>תושבים פונו מנחל עוז</span></div><div><b>כ-100</b><span>אנשים חולצו ממתחם המסיבה</span></div></div>
<div class="badge sm"><figure><img src="assets/givati.png"></figure><figure><img src="assets/ugda162.png"></figure></div>
</div>""" + foot(True), "dark close")


# ---------------------------------------------------------------- הרכבה
def build_slides():
    counts, sec_counts = {}, {}
    for c in CAND.values():
        counts[c[5]] = counts.get(c[5], 0) + 1
        for k in c[6]:
            if k != c[5]:
                sec_counts[k] = sec_counts.get(k, 0) + 1
    out = [s_cover(), s_agenda(), s_picture(), s_map(counts), s_gantt(), s_counts(counts, sec_counts), s_c2()]
    main = [a for a in ARENAS if a["main"]]
    for i, a in enumerate(main, 1):
        out.append(s_arena(a, i, len(main) + 1))
        if a["key"] in FLOW:
            out.append(s_flow(a["key"]))
        for b in BATT_BEFORE.get(a["key"], []):
            out.append(s_batt(b))
        ns = cands_in(a["key"])
        for p, n in enumerate(ns, 1):
            out.append(s_cand(n, p, len(ns), a))
    out.append(s_others())
    out.append(s_batt("gadsam"))
    for a in [a for a in ARENAS if not a["main"]]:
        ns = cands_in(a["key"])
        for p, n in enumerate(ns, 1):
            out.append(s_cand(n, p, len(ns), a))
    out += [s_debriefs(), s_units(), s_close()]
    return out


CHECK_JS = """<pre id="ovf"></pre><script>
document.fonts.ready.then(function(){
var bad=[];document.querySelectorAll('.s').forEach(function(s,i){
 var r=s.getBoundingClientRect(), f=s.querySelector('.foot'), lim=f?f.getBoundingClientRect().top-4:r.bottom;
 s.querySelectorAll('.body *, .armain *, .cmain *, .cin *, .cv *, .cl1 *').forEach(function(el){
   if(el.ownerSVGElement) return;  // צורות בתוך מפה נחתכות על ידי ה-SVG, לא גולשות
   var b=el.getBoundingClientRect(); if(b.height===0) return;
   if(b.bottom>lim+1 || b.left<r.left-1 || b.right>r.right+1){bad.push((i+1)+':'+el.className+':'+(el.textContent||'').slice(0,30));}
 });
});
document.getElementById('ovf').textContent=bad.slice(0,80).join('\\n');
});
</script>"""

NUM_JS = """<script>document.querySelectorAll('.pg').forEach(function(p,i){p.textContent=(i+1);});</script>"""


def page(slides, extra=""):
    css = (HERE / "deck.css").read_text(encoding="utf-8")
    return (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>מצגת חטיבת גבעתי</title>'
            f'<style>{css}</style></head><body>{"".join(slides)}{extra}</body></html>')


def main():
    slides = build_slides()
    tmp = HERE / "_deck.html"
    tmp.write_text(page(slides, NUM_JS), encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=6000",
                    f"--print-to-pdf={OUT_PDF}", tmp.as_uri()], capture_output=True)
    chk = HERE / "_check.html"
    chk.write_text(page(slides, CHECK_JS), encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=6000", "--window-size=1600,900",
                          "--dump-dom", chk.as_uri()], capture_output=True, text=True).stdout
    import re
    m = re.search(r'<pre id="ovf">(.*?)</pre>', dom, re.S)
    print(f"slides: {len(slides)}  pdf: {OUT_PDF.name}")
    print("overflow:", html.unescape(m.group(1)) if m and m.group(1).strip() else "none")
    if "--preview" in sys.argv:
        prev = HERE / "preview"
        prev.mkdir(exist_ok=True)
        per = 12
        for k in range(0, len(slides), per):
            group = slides[k:k + per]
            sheet = HERE / "_sheet.html"
            css = (HERE / "deck.css").read_text(encoding="utf-8")
            wrap = "".join(f'<div class="cell"><div class="sc">{g}</div><div class="no">{k+j+1}</div></div>' for j, g in enumerate(group))
            sheet.write_text(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><style>{css}'
                             f'body{{background:#222;display:grid;grid-template-columns:repeat(3,480px);gap:12px;padding:12px;width:1500px}}'
                             f'.cell{{width:480px;height:270px;overflow:hidden;position:relative}}.sc{{transform:scale(.3);transform-origin:top right;width:1600px;position:absolute;right:0;top:0}}'
                             f'.no{{position:absolute;left:4px;top:4px;background:#ff0;color:#000;font:bold 14px sans-serif;padding:1px 5px}}</style></head>'
                             f'<body>{wrap}</body></html>', encoding="utf-8")
            png = prev / f"sheet_{k//per+1:02d}.png"
            subprocess.run([CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=4000", "--hide-scrollbars",
                            "--window-size=1500,1150", f"--screenshot={png}", sheet.as_uri()], capture_output=True)
        print("previews in", prev)


if __name__ == "__main__":
    main()
