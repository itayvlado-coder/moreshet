"""בונה גרסה חיה (HTML מונפש) של שקפי "מהלך הקרב". זהה לשקף במצגת, אבל האירועים נבנים אחד אחרי השני.

שימוש:  python3 build_live.py            -> כל הזירות שיש להן מפה ב-battle_maps.FLOW
        python3 build_live.py kfaraza    -> זירה אחת

הקובץ נוצר בתיקייה הזו, בשם "חי - מהלך הקרב - <זירה>.html", ונפתח בדפדפן (Chrome).
מקשים בזמן ההצגה: רווח = עצירה והמשך · חצים = אירוע קודם / הבא · R = מההתחלה · F = מסך מלא.
אפשר גם ללחוץ על אירוע ברשימה כדי לקפוץ אליו.
"""
import base64, re, sys
import build_deck as b
from battle_maps import FLOW

LIVE_CSS = """
html, body { background: #14081f; height: 100%; overflow: hidden; }
#stage { position: absolute; top: 50%; left: 50%; width: 1600px; height: 900px; transform-origin: center center; }
#stage .s { page-break-after: auto; box-shadow: 0 20px 80px rgba(0,0,0,.5); }

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

.live .fstep { opacity: .28; transition: opacity .5s, background .5s; border-radius: 8px; padding: 4px 6px; margin: 0 -6px; cursor: pointer; }
.live .fstep.on { opacity: 1; }
.live .fstep.cur { background: var(--lav); box-shadow: inset -4px 0 0 var(--cc); }

/* שעון וכפתורים על המפה */
.fmapbox { position: relative; }
#clock { position: absolute; top: 18px; right: 22px; background: rgba(44,16,64,.85); border: 1px solid var(--gold); border-radius: 10px;
  padding: 6px 16px 8px; color: var(--gold); font: 900 30px/1.1 "Frank Ruhl Libre", serif; min-width: 120px; text-align: center;
  transition: opacity .4s; }
#clock small { display: block; font: 600 13px "Heebo", sans-serif; color: #e4dcef; letter-spacing: 1px; }
#ctl { position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; align-items: center;
  background: rgba(44,16,64,.8); padding: 6px 12px; border-radius: 22px; border: 1px solid rgba(201,162,74,.5); line-height: 1; }
#ctl button { background: none; border: 0; color: #f6f1e6; font-size: 18px; cursor: pointer; width: 30px; height: 30px; border-radius: 50%; }
#ctl button:hover { background: rgba(255,255,255,.12); }
#dots { display: flex; gap: 6px; }
#dots i { width: 9px; height: 9px; border-radius: 50%; background: rgba(255,255,255,.25); display: block; transition: background .3s; }
#dots i.on { background: var(--gold); }
#bar { position: absolute; bottom: 0; right: 0; height: 3px; background: var(--gold); width: 0; }
"""

LIVE_JS = """
(function(){
const stage = document.getElementById('stage');
function fit(){ const k = Math.min(innerWidth/1600, innerHeight/900); stage.style.transform = `translate(-50%,-50%) scale(${k})`; }
addEventListener('resize', fit); fit();

const svg = document.querySelector('.fmap');
const steps = [...document.querySelectorAll('.fstep')];
const N = steps.length, DUR = 6500;
const q = (sel, i) => [...svg.querySelectorAll(sel + '[data-step="' + i + '"]')];
const clock = document.getElementById('clock'), bar = document.getElementById('bar');
const dots = document.getElementById('dots');
steps.forEach((s, i) => { const d = document.createElement('i'); dots.appendChild(d);
  s.style.setProperty('--cc', getComputedStyle(s.querySelector('.fnum')).getPropertyValue('--c'));
  s.addEventListener('click', () => { go(i + 1); }); });

// כל חץ נחשף בהדרגה דרך מסכה, כדי שגם קווים מקווקווים ייבנו מתחילתם לסופם
const NS = 'http://www.w3.org/2000/svg';
const defs = svg.querySelector('defs');
svg.querySelectorAll('.ar').forEach((g, k) => {
  const line = g.querySelector('.arl'), len = line.getTotalLength();
  const m = document.createElementNS(NS, 'mask'); m.id = 'rv' + k; m.setAttribute('maskUnits', 'userSpaceOnUse');
  const r = document.createElementNS(NS, 'rect'); r.setAttribute('width', '100%'); r.setAttribute('height', '100%'); r.setAttribute('fill', 'black');
  const p = document.createElementNS(NS, 'path'); p.setAttribute('d', line.getAttribute('d')); p.setAttribute('fill', 'none');
  p.setAttribute('stroke', 'white'); p.setAttribute('stroke-width', '30'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round');
  p.style.strokeDasharray = len + 40; p.style.strokeDashoffset = len + 40;
  m.append(r, p); defs.appendChild(m); g.setAttribute('mask', 'url(#rv' + k + ')');
  g._rev = p; g._len = len; g._line = line;
  const dot = document.createElementNS(NS, 'circle'); dot.setAttribute('r', '7'); dot.setAttribute('fill', '#fff');
  dot.style.filter = 'drop-shadow(0 0 6px ' + g.dataset.color + ')'; dot.style.opacity = 0; svg.appendChild(dot); g._dot = dot;
});

function drawArrow(g, ms){
  const t0 = performance.now(), len = g._len;
  g.classList.add('on');
  (function f(t){ const k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
    g._rev.style.strokeDashoffset = (len + 40) * (1 - e);
    const pt = g._line.getPointAtLength(len * e); g._dot.setAttribute('cx', pt.x); g._dot.setAttribute('cy', pt.y);
    g._dot.style.opacity = k < 1 ? 1 : 0;
    if (k < 1) requestAnimationFrame(f); else if (g.dataset.dashed === '1') g.classList.add('march'); })(t0);
}
function showArrowNow(g){ g.classList.add('on'); g._rev.style.strokeDashoffset = 0; g._dot.style.opacity = 0; if (g.dataset.dashed === '1') g.classList.add('march'); }
function hideArrow(g){ g.classList.remove('on', 'march'); g._rev.style.strokeDashoffset = g._len + 40; g._dot.style.opacity = 0; }

let cur = 0, playing = true, timer = null, t0 = 0;
function render(n, animate){
  for (let i = 1; i <= N; i++){
    const on = i <= n;
    steps[i-1].classList.toggle('on', on); steps[i-1].classList.toggle('cur', i === n);
    dots.children[i-1].classList.toggle('on', on);
    q('.mk', i).forEach(m => { m.classList.toggle('on', on); m.classList.toggle('cur', i === n); });
    q('.zn', i).forEach(z => z.classList.toggle('on', on));
    q('.ar', i).forEach(g => { if (!on) hideArrow(g); else if (i === n && animate) drawArrow(g, 1800); else showArrowNow(g); });
  }
  if (n > 0){ const s = steps[n-1]; clock.innerHTML = s.querySelector('b').textContent + '<small>אירוע ' + n + ' מתוך ' + N + '</small>'; clock.style.opacity = 1; }
  else { clock.innerHTML = '7.10<small>בוקר</small>'; }
}
function go(n, animate = true){ cur = Math.max(0, Math.min(N, n)); render(cur, animate); restart(); }
function restart(){ clearTimeout(timer); t0 = performance.now(); if (playing && cur < N) timer = setTimeout(() => go(cur + 1), cur === 0 ? 1200 : DUR); }
function tick(){ const k = playing && cur < N ? Math.min(1, (performance.now() - t0) / (cur === 0 ? 1200 : DUR)) : (cur >= N ? 1 : 0);
  bar.style.width = (cur >= N ? 100 : ((cur + k) / N) * 100) + '%'; requestAnimationFrame(tick); }
requestAnimationFrame(tick);
function toggle(){ playing = !playing; document.getElementById('pp').textContent = playing ? '❚❚' : '▶'; restart(); }

document.getElementById('pp').onclick = toggle;
document.getElementById('nx').onclick = () => go(cur + 1);
document.getElementById('pv').onclick = () => go(cur - 1, false);
document.getElementById('rs').onclick = () => go(0, false);
addEventListener('keydown', e => {
  if (e.key === ' ') { e.preventDefault(); toggle(); }
  else if (['ArrowLeft', 'ArrowDown', 'PageDown', 'Enter'].includes(e.key)) go(cur + 1);
  else if (['ArrowRight', 'ArrowUp', 'PageUp', 'Backspace'].includes(e.key)) go(cur - 1, false);
  else if (e.key === 'r' || e.key === 'R' || e.key === 'ק') go(0, false);
  else if (e.key === 'f' || e.key === 'F' || e.key === 'כ') { document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen(); }
});
document.fonts.ready.then(() => go(0, false));
})();
"""


def build(key):
    sl = b.s_flow(key)
    ctl = ('<div id="clock"></div><div id="ctl"><button id="rs" title="מההתחלה (R)">↺</button>'
           '<button id="pv" title="אירוע קודם">▶</button><button id="pp" title="עצירה והמשך (רווח)">❚❚</button>'
           '<button id="nx" title="אירוע הבא">◀</button><div id="dots"></div></div><div id="bar"></div>')
    sl = sl.replace('<div class="fmapbox">', '<div class="fmapbox">' + ctl, 1).replace('<span class="pg"></span>', '<span class="pg">חי</span>')
    css = (b.HERE / "deck.css").read_text(encoding="utf-8")
    title = f'מהלך הקרב - {FLOW[key]["title"]}'
    out = b.HERE / f"חי - {title}.html"
    out.write_text(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{b.e(title)}</title>'
                   f'<meta name="viewport" content="width=device-width,initial-scale=1">'
                   f'<style>{css}{LIVE_CSS}</style></head><body class="live"><div id="stage">{sl}</div>'
                   f'<script>{LIVE_JS}</script></body></html>', encoding="utf-8")
    # הקובץ עצמאי: הגופנים והלוגואים מוטמעים בו, כדי שייפתח בכל מחשב גם בלי תיקיית assets
    html = out.read_text(encoding="utf-8")
    mime = {".ttf": "font/ttf", ".png": "image/png"}
    def inline(m):
        f = b.HERE / m.group(2)
        return m.group(1) + f"data:{mime[f.suffix]};base64," + base64.b64encode(f.read_bytes()).decode() + m.group(3)
    html = re.sub(r'(url\(")(assets/[^"]+\.ttf)("\))', inline, html)
    html = re.sub(r'(src=")(assets/[^"]+\.png)(")', inline, html)
    out.write_text(html, encoding="utf-8")
    print("ok", out.name, f"{out.stat().st_size // 1024} KB")
    return out


if __name__ == "__main__":
    for k in (sys.argv[1:] or list(FLOW)):
        build(k)
