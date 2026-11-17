"""בונה את הגרסה החיה (HTML מונפש) של שקפי "מהלך הקרב".

שימוש:  python3 build_live.py            -> קובץ לכל זירה, וקובץ מפה אחד לכל הזירות
        python3 build_live.py kfaraza    -> זירה אחת

נוצרים בתיקייה הזו:
- "חי - מהלך הקרב - <זירה>.html": שקף אחד, זהה לשקף במצגת, והאירועים נבנים אחד אחרי השני.
- "חי - מהלך הקרב - כל הזירות.html": מפת העוטף. לוחצים על זירה, ונפתח מהלך הקרב שלה.
מקשים: רווח = עצירה והמשך · חצים = אירוע קודם / הבא · R = מההתחלה · F = מסך מלא · Esc = חזרה למפה.
הקבצים עצמאיים: הגופנים והלוגואים מוטמעים בהם.
"""
import base64, math, re, sys
import build_deck as b
from battle_maps import FLOW, FORCE
from deck_data import BORDER, PLACES

LIVE_CSS = """
html, body { background: #14081f; height: 100%; overflow: hidden; margin: 0; }
#stage { position: absolute; top: 50%; left: 50%; width: 1600px; height: 900px; transform-origin: center center; }
#stage .s { page-break-after: auto; box-shadow: 0 20px 80px rgba(0,0,0,.5); }
.view { display: none; } .view.show { display: block; }

/* מצב התחלה: רק המפה. האירועים מופיעים לפי הסדר */
.live .mk, .live .zn, .live .ar { opacity: 0; }
.live .mk { transition: opacity .3s; }
.live .mk.on { opacity: 1; }
.live .mk.on > circle:not(.pulse), .live .mk.on text { animation: pop .55s cubic-bezier(.3,1.6,.5,1) both; transform-box: fill-box; transform-origin: center; }
.live .mk .pulse { opacity: 0; transform-box: fill-box; transform-origin: center; }
.live .mk.cur .pulse { animation: pulse 1.8s ease-out infinite; }
.live .zn { transition: opacity 1s; transform-box: fill-box; transform-origin: center; }
.live .zn.on { opacity: 1; animation: zone 3s ease-in-out infinite; }
.live .ar.on { opacity: 1; }
.live .ar.on.march .arl { animation: march 1.2s linear infinite; }
@keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }
@keyframes pulse { 0% { transform: scale(1); opacity: .9; } 100% { transform: scale(2.8); opacity: 0; } }
@keyframes zone { 0%,100% { fill-opacity: .10; } 50% { fill-opacity: .28; } }
@keyframes march { to { stroke-dashoffset: -34; } }
@media (prefers-reduced-motion: reduce) { .live .mk.cur .pulse, .live .zn.on, .live .ar.on.march .arl { animation: none; } }

.live .fstep { opacity: .28; transition: opacity .5s, background .5s; border-radius: 8px; padding: 1px 6px; margin: 0 -6px; cursor: pointer; }
.live .fsteps { gap: 4px; }
.live .fmapbox { align-self: start; }
.live .fstep.on { opacity: 1; }
.live .fstep.cur { background: var(--lav); box-shadow: inset -4px 0 0 var(--cc); }

/* שעון וכפתורים על המפה */
.fmapbox { position: relative; }
.clock { position: absolute; top: 18px; left: 22px; background: rgba(44,16,64,.85); border: 1px solid var(--gold); border-radius: 10px;
  padding: 6px 16px 8px; color: var(--gold); font: 900 30px/1.1 "Frank Ruhl Libre", serif; min-width: 120px; text-align: center; }
.clock small { display: block; font: 600 13px "Heebo", sans-serif; color: #e4dcef; letter-spacing: 1px; }
.ctl { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; align-items: center;
  background: rgba(44,16,64,.8); padding: 6px 12px; border-radius: 22px; border: 1px solid rgba(201,162,74,.5); line-height: 1; }
.ctl button { background: none; border: 0; color: #f6f1e6; font-size: 18px; cursor: pointer; width: 30px; height: 30px; border-radius: 50%; }
.ctl button:hover, .ctl button:focus-visible { background: rgba(255,255,255,.12); outline: none; }
.dots { display: flex; gap: 6px; }
.dots i { width: 9px; height: 9px; border-radius: 50%; background: rgba(255,255,255,.25); display: block; transition: background .3s; }
.dots i.on { background: var(--gold); }
.bar { position: absolute; bottom: 0; right: 0; height: 3px; background: var(--gold); width: 0; }
.back { position: absolute; top: 24px; left: 210px; background: var(--cream); color: var(--purple); border: 1px solid var(--gold-soft);
  border-radius: 22px; padding: 8px 18px; font: 700 16px "Heebo", sans-serif; cursor: pointer; }
.back:hover, .back:focus-visible { background: #fff; outline: 2px solid var(--gold); }

/* מפת הזירות */
.atlas .body { display: grid; grid-template-columns: 1fr 640px; gap: 36px; padding-top: 22px; }
.amap { grid-column: 2; grid-row: 1; border-radius: 12px; overflow: hidden; border: 2px solid var(--gold-soft); line-height: 0; background: #2c1040; }
.amap svg { width: 640px; height: 724px; display: block; font-family: "Heebo", sans-serif; }
.amap .ar-box { cursor: pointer; }
.amap .ar-box rect { fill: rgba(201,162,74,.10); stroke: #c9a24a; stroke-width: 1.5; stroke-dasharray: 5 4; transition: fill .2s; }
.amap .ar-box:hover rect, .amap .ar-box:focus rect, .amap .ar-box.hl rect { fill: rgba(201,162,74,.35); }
.amap .ar-box circle { fill: #c9a24a; stroke: #2c1040; stroke-width: 3; }
.amap .ar-box text.n { fill: #2c1040; font-size: 15px; font-weight: 900; }
.amap .ar-box text.t { fill: #f6f1e6; font-size: 15px; font-weight: 800; paint-order: stroke; stroke: #2c1040; stroke-width: 4px; }
.amap .pl { fill: #b9aac7; font-size: 12px; }
.amap .gz { fill: #1d0a2b; stroke: #8f7bb0; stroke-width: 1.5; }
.amap .gzl { fill: #8f7bb0; font-size: 22px; font-weight: 800; letter-spacing: 3px; }
.alist { grid-column: 1; grid-row: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; align-content: start; }
.acard { display: block; text-align: right; background: #fff; border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; cursor: pointer;
  font-family: "Heebo", sans-serif; color: var(--ink); transition: border-color .2s, box-shadow .2s; }
.acard:hover, .acard:focus-visible, .acard.hl { border-color: var(--gold); box-shadow: 0 4px 14px rgba(58,23,82,.15); outline: none; }
.acard .an { display: inline-flex; width: 26px; height: 26px; border-radius: 50%; background: var(--gold); color: var(--purple3);
  font-weight: 900; align-items: center; justify-content: center; margin-left: 8px; font-size: 14px; }
.acard b { font-size: 19px; color: var(--purple); }
.acard .aw { display: block; color: var(--muted); font-size: 14px; margin-top: 4px; }
.acard .af { display: flex; flex-wrap: wrap; gap: 4px 10px; margin-top: 8px; font-size: 13px; color: var(--muted); }
.acard .af i { display: inline-block; width: 14px; height: 5px; border-radius: 3px; margin-left: 4px; vertical-align: middle; }
.ahint { grid-column: 1 / -1; font-size: 15px; color: var(--muted); margin-top: 6px; }
"""

ENGINE_JS = """
(function(){
const stage = document.getElementById('stage');
function fit(){ const k = Math.min(innerWidth/1600, innerHeight/900); stage.style.transform = `translate(-50%,-50%) scale(${k})`; }
addEventListener('resize', fit); fit();
const NS = 'http://www.w3.org/2000/svg';

function initFlow(root){
  const svg = root.querySelector('.fmap'), key = root.dataset.key;
  const steps = [...root.querySelectorAll('.fstep')];
  const N = steps.length, DUR = 6500;
  const q = (sel, i) => [...svg.querySelectorAll(sel + '[data-step="' + i + '"]')];
  const clock = root.querySelector('.clock'), bar = root.querySelector('.bar'), dots = root.querySelector('.dots');
  steps.forEach((s, i) => { const d = document.createElement('i'); dots.appendChild(d);
    s.style.setProperty('--cc', getComputedStyle(s.querySelector('.fnum')).getPropertyValue('--c'));
    s.addEventListener('click', () => go(i + 1)); });
  // כל חץ נחשף בהדרגה דרך מסכה, כדי שגם קווים מקווקווים ייבנו מתחילתם לסופם
  const defs = svg.querySelector('defs');
  svg.querySelectorAll('.ar').forEach((g, k) => {
    const line = g.querySelector('.arl'), len = line.getTotalLength();
    const m = document.createElementNS(NS, 'mask'); m.id = 'rv-' + key + '-' + k; m.setAttribute('maskUnits', 'userSpaceOnUse');
    const r = document.createElementNS(NS, 'rect'); r.setAttribute('width', '100%'); r.setAttribute('height', '100%'); r.setAttribute('fill', 'black');
    const p = document.createElementNS(NS, 'path'); p.setAttribute('d', line.getAttribute('d')); p.setAttribute('fill', 'none');
    p.setAttribute('stroke', 'white'); p.setAttribute('stroke-width', '30'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round');
    p.style.strokeDasharray = len + 40; p.style.strokeDashoffset = len + 40;
    m.append(r, p); defs.appendChild(m); g.setAttribute('mask', 'url(#' + m.id + ')');
    g._rev = p; g._len = len; g._line = line;
    const dot = document.createElementNS(NS, 'circle'); dot.setAttribute('r', '7'); dot.setAttribute('fill', '#fff');
    dot.style.filter = 'drop-shadow(0 0 6px ' + g.dataset.color + ')'; dot.style.opacity = 0; svg.appendChild(dot); g._dot = dot;
  });
  function drawArrow(g, ms){
    const t0 = performance.now(), len = g._len; g.classList.add('on');
    (function f(t){ const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
      g._rev.style.strokeDashoffset = (len + 40) * (1 - e);
      const pt = g._line.getPointAtLength(len * e); g._dot.setAttribute('cx', pt.x); g._dot.setAttribute('cy', pt.y);
      g._dot.style.opacity = k < 1 ? 1 : 0;
      if (k < 1) requestAnimationFrame(f); else if (g.dataset.dashed === '1') g.classList.add('march'); })(t0);
  }
  const showArrowNow = g => { g.classList.add('on'); g._rev.style.strokeDashoffset = 0; g._dot.style.opacity = 0; if (g.dataset.dashed === '1') g.classList.add('march'); };
  const hideArrow = g => { g.classList.remove('on', 'march'); g._rev.style.strokeDashoffset = g._len + 40; g._dot.style.opacity = 0; };
  let cur = 0, playing = true, timer = null, t0 = 0, active = false;
  function render(n, animate){
    for (let i = 1; i <= N; i++){
      const on = i <= n;
      steps[i-1].classList.toggle('on', on); steps[i-1].classList.toggle('cur', i === n);
      dots.children[i-1].classList.toggle('on', on);
      q('.mk', i).forEach(m => { m.classList.toggle('on', on); m.classList.toggle('cur', i === n); });
      q('.zn', i).forEach(z => z.classList.toggle('on', on));
      q('.ar', i).forEach(g => { if (!on) hideArrow(g); else if (i === n && animate) drawArrow(g, 1800); else showArrowNow(g); });
    }
    clock.innerHTML = n > 0 ? steps[n-1].querySelector('b').textContent + '<small>אירוע ' + n + ' מתוך ' + N + '</small>' : 'התחלה<small>' + N + ' אירועים</small>';
  }
  function go(n, animate = true){ cur = Math.max(0, Math.min(N, n)); render(cur, animate); restart(); }
  function restart(){ clearTimeout(timer); t0 = performance.now(); if (active && playing && cur < N) timer = setTimeout(() => go(cur + 1), cur === 0 ? 1200 : DUR); }
  (function tick(){ const k = active && playing && cur < N ? Math.min(1, (performance.now() - t0) / (cur === 0 ? 1200 : DUR)) : (cur >= N ? 1 : 0);
    bar.style.width = (cur >= N ? 100 : ((cur + k) / N) * 100) + '%'; requestAnimationFrame(tick); })();
  function toggle(){ playing = !playing; root.querySelector('.pp').textContent = playing ? '❚❚' : '▶'; restart(); }
  root.querySelector('.pp').onclick = toggle;
  root.querySelector('.nx').onclick = () => go(cur + 1);
  root.querySelector('.pv').onclick = () => go(cur - 1, false);
  root.querySelector('.rs').onclick = () => go(0, false);
  return { start(){ active = true; playing = true; root.querySelector('.pp').textContent = '❚❚'; go(0, false); },
           stop(){ active = false; clearTimeout(timer); },
           key(e){ if (e.key === ' ') { e.preventDefault(); toggle(); }
             else if (['ArrowLeft', 'ArrowDown', 'PageDown', 'Enter'].includes(e.key)) go(cur + 1);
             else if (['ArrowRight', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) go(cur - 1, false);
             else if ('rRק'.includes(e.key)) go(0, false); } };
}

const views = [...document.querySelectorAll('.view')], flows = {};
let current = null;
function show(key){
  const flowViews = views.filter(v => v.dataset.key);
  const target = views.find(v => v.dataset.key === key) || views.find(v => v.classList.contains('atlas')) || flowViews[0];
  if (current && flows[current.dataset.key]) flows[current.dataset.key].stop();
  views.forEach(v => v.classList.toggle('show', v === target));
  current = target;
  if (target.dataset.key){ flows[target.dataset.key] = flows[target.dataset.key] || initFlow(target); flows[target.dataset.key].start(); }
}
const route = () => show(location.hash.slice(1));
addEventListener('hashchange', route);
document.querySelectorAll('[data-go]').forEach(el => {
  el.addEventListener('click', () => { location.hash = el.dataset.go; });
  el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); location.hash = el.dataset.go; } });
  el.addEventListener('mouseenter', () => document.querySelectorAll('[data-go="' + el.dataset.go + '"]').forEach(x => x.classList.add('hl')));
  el.addEventListener('mouseleave', () => document.querySelectorAll('[data-go="' + el.dataset.go + '"]').forEach(x => x.classList.remove('hl')));
});
document.querySelectorAll('.back').forEach(el => el.addEventListener('click', () => { history.pushState('', '', location.pathname); route(); }));
addEventListener('keydown', e => {
  if (e.key === 'f' || e.key === 'F' || e.key === 'כ') { (document.fullscreenElement ? document.exitFullscreen() : (document.documentElement.requestFullscreen() || Promise.resolve())).catch(() => {}); return; }
  if (e.key === 'Escape' && document.querySelector('.atlas')) { history.pushState('', '', location.pathname); route(); return; }
  if (current && current.dataset.key) flows[current.dataset.key].key(e);
});
document.fonts.ready.then(route);
})();
"""

CTL = ('<div class="clock"></div><div class="ctl"><button class="rs" title="מההתחלה (R)">↺</button>'
       '<button class="pv" title="אירוע קודם">▶</button><button class="pp" title="עצירה והמשך (רווח)">❚❚</button>'
       '<button class="nx" title="אירוע הבא">◀</button><div class="dots"></div></div><div class="bar"></div>')

ORDER = ["sderot", "kfaraza", "nahaloz", "nova", "kissufim", "north", "south", "ofakim"]


def flow_view(key, back):
    sl = b.s_flow(key)
    sl = sl.replace('<div class="fmapbox">', '<div class="fmapbox">' + CTL, 1).replace('<span class="pg"></span>', '<span class="pg">חי</span>')
    if back:
        sl = sl.replace('<section class="s ">', '<section class="s "><button class="back" title="חזרה למפה (Esc)">→ חזרה למפת הזירות</button>', 1)
    return f'<div class="view" data-key="{key}">{sl}</div>'


def atlas_view(keys):
    # אזור המפה: כל הזירות, עם שוליים
    S = min(FLOW[k]["bbox"][0] for k in keys) - 0.02
    N = max(FLOW[k]["bbox"][2] for k in keys) + 0.02
    W = min(FLOW[k]["bbox"][1] for k in keys) - 0.06
    E = max(FLOW[k]["bbox"][3] for k in keys) + 0.03
    WID, HGT = 640, 724
    kx = math.cos(math.radians((S + N) / 2))
    sc = min(WID / ((E - W) * kx), HGT / (N - S))
    cx, cy = (W + E) / 2, (S + N) / 2
    xy = lambda la, lo: (WID / 2 + (lo - cx) * kx * sc, HGT / 2 - (la - cy) * sc)
    # רצועת עזה: מהקו עד שולי המפה במערב
    bpts = [xy(la, lo) for la, lo in BORDER]
    gaza = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in bpts) + f" L-20,{bpts[-1][1]:.0f} L-20,{bpts[0][1]:.0f} Z"
    out = [f'<svg viewBox="0 0 {WID} {HGT}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="מפת הזירות">',
           f'<rect width="{WID}" height="{HGT}" fill="#2c1040"/><path class="gz" d="{gaza}"/>']
    gx, gy = xy(31.43, 34.40)
    out.append(f'<text class="gzl" x="{gx - 40:.0f}" y="{gy:.0f}" text-anchor="middle" transform="rotate(-55 {gx - 40:.0f} {gy:.0f})">רצועת עזה</text>')
    taken = {k: FLOW[k]["bbox"] for k in keys}
    for key, (nm, la, lo) in PLACES.items():
        x, y = xy(la, lo)
        inside = any(bb[0] - .006 <= la <= bb[2] + .006 and bb[1] - .006 <= lo <= bb[3] + .006 for kk, bb in taken.items() if kk != "south")
        if not (0 < x < WID and 0 < y < HGT) or inside:
            continue
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.5" fill="#8f7bb0"/><text class="pl" x="{x - 6:.0f}" y="{y + 4:.0f}" direction="ltr" text-anchor="end">{b.e(nm)}</text>')
    for i, k in enumerate(keys, 1):
        s, w, n, e = taken[k]
        x1, y1 = xy(n, w); x2, y2 = xy(s, e)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        rw, rh = max(x2 - x1, 16), max(y2 - y1, 16)
        out.append(f'<g class="ar-box" data-go="{k}" tabindex="0" role="button" aria-label="{b.e(FLOW[k]["title"])}">'
                   f'<rect x="{mx - rw / 2:.0f}" y="{my - rh / 2:.0f}" width="{rw:.0f}" height="{rh:.0f}" rx="4"/>'
                   f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="14"/><text class="n" x="{mx:.0f}" y="{my + 5:.0f}" text-anchor="middle">{i}</text>'
                   + (f'<text class="t" x="{mx - 20:.0f}" y="{my + 5:.0f}" direction="ltr" text-anchor="end">{b.e(FLOW[k]["title"])}</text></g>'
                      if mx > 260 and k != "kfaraza" else f'<text class="t" x="{mx + 20:.0f}" y="{my + 5:.0f}" direction="ltr" text-anchor="start">{b.e(FLOW[k]["title"])}</text></g>'))
    out.append('</svg>')
    cards = []
    for i, k in enumerate(keys, 1):
        f = FLOW[k]
        used = []
        for st in f["steps"]:
            if st[1] not in used:
                used.append(st[1])
        forces = "".join(f'<span><i style="background:{FORCE[u][1]}"></i>{b.e(FORCE[u][0])}</span>' for u in used if u != "civ")
        cards.append(f'<button class="acard" data-go="{k}"><span class="an">{i}</span><b>{b.e(f["title"])}</b>'
                     f'<span class="aw">{b.e(f["when"])} · {len(f["steps"])} אירועים</span><span class="af">{forces}</span></button>')
    total = sum(len(FLOW[k]["steps"]) for k in keys)
    body = (f'<div class="body"><div class="amap">{"".join(out)}</div><div class="alist">{"".join(cards)}'
            f'<p class="ahint">בוחרים זירה על המפה או ברשימה, ומהלך הקרב נבנה אירוע אחרי אירוע. Esc חוזר למפה. '
            f'מיקומי האירועים בתוך כל זירה משוערים לפי העדויות.</p></div></div>')
    sl = b.slide(b.top("מהלך הקרב", f"זירות החטיבה, 7 עד 11 באוקטובר · {len(keys)} זירות, {total} אירועים") + body + b.foot())
    return f'<div class="view atlas">{sl}</div>'


def inline_assets(html):
    mime = {".ttf": "font/ttf", ".png": "image/png"}
    def inline(m):
        f = b.HERE / m.group(2)
        return m.group(1) + f"data:{mime[f.suffix]};base64," + base64.b64encode(f.read_bytes()).decode() + m.group(3)
    html = re.sub(r'(url\(")(assets/[^"]+\.ttf)("\))', inline, html)
    return re.sub(r'(src=")(assets/[^"]+\.png)(")', inline, html)


def write(name, title, views):
    css = (b.HERE / "deck.css").read_text(encoding="utf-8")
    out = b.HERE / name
    html = (f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{b.e(title)}</title>'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<style>{css}{LIVE_CSS}</style></head><body class="live"><div id="stage">{"".join(views)}</div>'
            f'<script>{ENGINE_JS}</script></body></html>')
    out.write_text(inline_assets(html), encoding="utf-8")
    print("ok", out.name, f"{out.stat().st_size // 1024} KB")
    return out


def build(key):
    return write(f'חי - מהלך הקרב - {FLOW[key]["title"]}.html', f'מהלך הקרב - {FLOW[key]["title"]}', [flow_view(key, back=False)])


def build_atlas():
    keys = [k for k in ORDER if k in FLOW] + [k for k in FLOW if k not in ORDER]
    return write("חי - מהלך הקרב - כל הזירות.html", "מהלך הקרב בזירות החטיבה",
                 [atlas_view(keys)] + [flow_view(k, back=True) for k in keys])


if __name__ == "__main__":
    args = sys.argv[1:]
    for k in (args or list(FLOW)):
        build(k)
    if not args:
        build_atlas()
