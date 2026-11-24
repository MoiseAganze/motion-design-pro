#!/usr/bin/env python3
"""Generate the CMKS film scenes (one-shot scaffold; the HTML is the source afterwards)."""
import json, os, sys
ROOT = sys.argv[1]
T = json.load(open(os.path.join(ROOT, 'timing.json')))

FONTS = """
@font-face{font-family:'Bricolage Grotesque';src:url('assets/fonts/BricolageGrotesque.woff2') format('woff2');font-weight:200 800;font-display:block}
@font-face{font-family:'Plus Jakarta Sans';src:url('assets/fonts/PlusJakartaSans.woff2') format('woff2');font-weight:200 800;font-display:block}
"""
BASE_CSS = FONTS + """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Plus Jakarta Sans',sans-serif;color:#113F55;
 --teal950:#07293A;--teal900:#113F55;--teal800:#0E5775;--teal700:#0B6B91;--teal600:#0A86B4;--teal500:#15A8D6;--mist:#EFFAFE;
 --or:#E99841;--or6:#D4761B;--green:#10B981;--amber:#F59E0B;--grey:#94A3B8;}
#root *{box-sizing:border-box}
.disp{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:-0.02em;line-height:.92}
.abs{position:absolute}
.full{position:absolute;inset:0}
.shot{position:absolute;inset:0;overflow:hidden;background:#fff}
.cam{position:absolute;left:0;top:0;width:1440px;height:900px;transform-origin:0 0}
.cam img{position:absolute;left:0;top:0;width:1440px;height:900px;display:block}
.cursor{position:absolute;left:0;top:0;width:58px;height:58px;z-index:50}
.ring{position:absolute;border-radius:50%;padding:12px;background:var(--or);box-shadow:0 18px 40px rgba(7,41,58,.25)}
.ring.t{background:var(--teal500)}
.ring>.in{width:100%;height:100%;border-radius:50%;padding:8px;background:#fff}
.ring>.in>img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block}
.band{position:absolute;transform-origin:50% 50%}
.tag{position:absolute;padding:14px 30px;border-radius:999px;font-weight:700;font-size:30px;color:#fff;background:var(--teal700)}
"""
HELPERS = """
const K0 = 1920/1440;
function camS(x,y,s){const k=K0*s;return {x:960-x*k,y:540-y*k,scale:k};}
function pt(px,py,cx,cy,s){const k=K0*s;return {x:960+(px-cx)*k,y:540+(py-cy)*k};}
"""
CURSOR = """<svg viewBox="0 0 24 24"><path d="M4 2.5 L4 19.5 L8.6 15.4 L11.6 22 L14.6 20.7 L11.7 14.2 L18 14.2 Z" fill="#fff" stroke="#07293A" stroke-width="1.6" stroke-linejoin="round"/></svg>"""

def bands(prefix, corner='tl', z=5, teal_w=110, or_w=36, gap=26, length=900, x=0, y=0, rot=-45):
    # two parallel oblique bands (teal + orange), the site's signature
    return f"""<div id="{prefix}-bt" class="band" style="left:{x}px;top:{y}px;width:{length}px;height:{teal_w}px;background:var(--teal500);transform:rotate({rot}deg);z-index:{z}"></div>
<div id="{prefix}-bo" class="band" style="left:{x}px;top:{y+teal_w+gap}px;width:{length}px;height:{or_w}px;background:var(--or);transform:rotate({rot}deg);z-index:{z}"></div>"""

def scene(cid, dur, css, body, js):
    return f"""<template>
<style>{BASE_CSS}{css}</style>
<div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-duration="{dur}">
{body}
</div>
<script>
{HELPERS}
const tl = gsap.timeline({{ paused: true }});
{js}
window.__timelines["{cid}"] = tl;
</script>
</template>
"""

S = {s['id']: s for s in T['scenes']}
def W(name, html):
    open(os.path.join(ROOT, 'compositions', name + '.html'), 'w').write(html)

# ---------------- A: nuit ----------------
d = S['nuit']['dur']
W('nuit', scene('nuit', d, """
#root{background:var(--teal950)}
#a-clock{left:150px;top:150px;font-size:330px;color:#fff}
#a-city{left:160px;top:470px;font-size:120px;color:var(--teal500);letter-spacing:.04em}
#a-city span{display:inline-block}
#a-joel{left:1160px;top:200px;width:560px;height:560px}
#a-cap{left:1040px;top:790px;width:800px;text-align:center;font-size:40px;font-weight:600;color:#fff}
#a-cap b{color:var(--or)}
#a-q{left:150px;top:330px;font-size:170px;color:#fff;width:1500px}
#a-q em{font-style:normal;color:var(--or)}
#a-iris{position:absolute;inset:0;z-index:30}
#a-iris img{width:1920px;height:1200px;position:absolute;left:0;top:0}
""", f"""
<div id="a-bg1" class="band" style="left:900px;top:-300px;width:1800px;height:420px;background:var(--teal900);transform:rotate(-45deg)"></div>
<div id="a-bg2" class="band" style="left:1100px;top:620px;width:1500px;height:120px;background:var(--teal800);transform:rotate(-45deg)"></div>
<div id="a-clock" class="abs disp">21:00</div>
<div id="a-city" class="abs disp">{''.join(f'<span>{c}</span>' if c!=' ' else ' ' for c in 'KINSHASA')}</div>
<div id="a-joel" class="ring"><div class="in"><img src="assets/img/pole4.jpg" alt=""></div></div>
<div id="a-cap" class="abs">Joël — <b>une cheville tordue</b> au foot</div>
<div id="a-q" class="abs disp">Où se faire<br><em>soigner&nbsp;?</em></div>
{bands('a', x=-300, y=560, length=2600, teal_w=120, or_w=40, z=20)}
<div id="a-iris"><img src="assets/shots/home.png" alt=""></div>
""", """
tl.set('#a-iris', {clipPath:'circle(0px at 1460px 560px)'}, 0);
tl.set('#a-bt,#a-bo', {xPercent:-110}, 0);
// frame 0 already shows the clock
tl.fromTo('#a-clock', {opacity:.35, filter:'blur(6px)'}, {opacity:1, filter:'blur(0px)', duration:.5, ease:'expo.out'}, 0);
tl.fromTo('#a-city span', {opacity:0, y:30}, {opacity:1, y:0, duration:.5, ease:'expo.out', stagger:.06}, .9);
tl.fromTo('#a-bg1', {xPercent:30, opacity:.0}, {xPercent:0, opacity:1, duration:1.4, ease:'power2.out'}, 0);
tl.fromTo('#a-bg2', {xPercent:40}, {xPercent:0, duration:1.6, ease:'power2.out'}, .2);
// Joël
tl.fromTo('#a-joel', {scale:.2, opacity:0}, {scale:1, opacity:1, duration:.8, ease:'back.out(1.5)'}, 2.6);
tl.fromTo('#a-cap', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.4}, 3.0);
// question replaces clock
tl.to('#a-clock,#a-city', {opacity:0, filter:'blur(8px)', duration:.3, ease:'power3.in'}, 4.8);
tl.fromTo('#a-q', {opacity:0, filter:'blur(10px)'}, {opacity:1, filter:'blur(0px)', duration:.35, ease:'expo.out'}, 5.0);
// band sweeps, iris opens on the CMKS poster
tl.to('#a-bt', {xPercent:0, duration:.6, ease:'power3.inOut'}, 6.6);
tl.to('#a-bo', {xPercent:0, duration:.6, ease:'power3.inOut'}, 6.68);
tl.to('#a-iris', {clipPath:'circle(1400px at 1460px 560px)', duration:1.0, ease:'power3.inOut'}, 7.1);
tl.to('#a-bt,#a-bo', {xPercent:110, duration:.7, ease:'power3.in'}, 7.6);
"""))

# ---------------- B: affiche + pôles + statuts ----------------
POLES = [("Kinésithérapie",5,1,1),("Médecine",3,0,0),("Nutrition",3,0,0),("Sport-santé",4,0,0),
         ("Périnatalité",4,1,0),("Bien-être",2,2,1),("Médico-technique",3,1,1),("Restauration",0,1,3)]
grid = []
for i,(n,o,dv,e) in enumerate(POLES):
    r, c = divmod(i,4)
    cx = 330 + c*400 + (160 if r else 0); cy = 330 + r*420
    grid.append((cx,cy))
rings = []; labels=[]; rows=[]
for i,(n,o,dv,e) in enumerate(POLES):
    cx,cy = grid[i]; sz=230
    cls = 'ring' if i%2==0 else 'ring t'
    rings.append(f'<div id="b-r{i}" class="{cls}" style="left:{cx-sz//2}px;top:{cy-sz//2}px;width:{sz}px;height:{sz}px;z-index:10"><div class="in"><img src="assets/img/pole{i+1}.jpg" alt=""></div></div>')
    labels.append(f'<div id="b-l{i}" class="abs blab" style="left:{cx-180}px;top:{cy+132}px"><i>{i+1}</i>{n}</div>')
    segs = ''.join(f'<span class="seg {k}"></span>' for k,cnt in (('g',o),('a',dv),('e',e)) for _ in range(cnt))
    rows.append(f'<div id="b-row{i}" class="abs brow" style="top:{214+i*100}px"><div class="bname"><i>{i+1}</i>{n}</div><div class="bbar">{segs}</div></div>')
# board circle targets
board_xy = [(250, 214+i*100+40) for i in range(8)]
d = S['poles']['dur']
W('poles', scene('poles', d, """
#root{background:#fff}
.blab{z-index:11;width:360px;text-align:center;font-size:30px;font-weight:700;color:var(--teal900)}
.blab i,.bname i{font-style:normal;display:inline-flex;width:46px;height:46px;border-radius:50%;background:var(--or);color:#fff;font-size:28px;align-items:center;justify-content:center;margin-right:10px;vertical-align:3px}
.brow{left:320px;height:80px;display:flex;align-items:center;gap:30px}
.bname{width:430px;font-size:34px;font-weight:700;color:var(--teal900)}
.bbar{display:flex;gap:10px}
.seg{width:74px;height:30px;border-radius:15px;background:#E2E8F0}
.seg.g{--c:var(--green)}.seg.a{--c:var(--amber)}.seg.e{--c:var(--grey)}
#b-hero{z-index:1}
#b-title{left:150px;top:70px;font-size:96px;color:var(--teal700);z-index:12}
#b-title em{font-style:normal;color:var(--or)}
.chip{position:absolute;left:1340px;display:flex;align-items:center;gap:18px;font-size:40px;font-weight:700;color:var(--teal900);z-index:12}
.chip b{display:inline-block;width:34px;height:34px;border-radius:50%}
.chip span{font-family:'Bricolage Grotesque';font-weight:800;font-size:76px;width:100px;text-align:right}
""", f"""
<div id="b-hero" class="shot"><div class="cam" id="b-cam"><img src="assets/shots/home.png" alt=""></div></div>
<div id="b-white" class="full" style="background:#fff;z-index:5"></div>
{bands('b1', x=-520, y=-60, length=1100, z=6)}
{bands('b2', x=1480, y=930, length=1100, z=6)}
<div id="b-title" class="abs disp">Huit <em>pôles</em></div>
{''.join(rings)}
{''.join(labels)}
<div id="b-board" style="position:absolute;inset:0;z-index:11">{''.join(rows)}</div>
<div id="b-c1" class="chip" style="top:330px"><span>24</span><b style="background:var(--green)"></b>Opérationnels</div>
<div id="b-c2" class="chip" style="top:470px"><span>6</span><b style="background:var(--amber)"></b>En développement</div>
<div id="b-c3" class="chip" style="top:610px"><span>6</span><b style="background:var(--grey)"></b>Envisagés</div>
""", f"""
const G = {json.dumps(grid)}; const BXY = {json.dumps(board_xy)};
// 0-2.6: the poster (continues the iris from the night scene)
tl.set('#b-cam', camS(720,600,1.0), 0);
tl.to('#b-cam', {{...camS(480,330,1.45), duration:2.2, ease:'power2.inOut'}}, .2);
tl.set('#b-white,#b-title,.blab,[id^=b-r],#b-board .brow,.chip', {{opacity:0}}, 0);
tl.set('#b1-bt,#b1-bo,#b2-bt,#b2-bo', {{xPercent:-100, opacity:1}}, 0);
// wipe to white with the bands
tl.to('#b1-bt,#b2-bt', {{xPercent:0, duration:.6, ease:'power3.out'}}, 2.35);
tl.to('#b1-bo,#b2-bo', {{xPercent:0, duration:.6, ease:'power3.out'}}, 2.42);
tl.fromTo('#b-white', {{clipPath:'polygon(0 0,0 0,0 0,0 0)'}}, {{opacity:1, clipPath:'polygon(0 0,200% 0,0 200%,0 0)', duration:.6, ease:'power3.inOut'}}, 2.35);
tl.fromTo('#b-title', {{opacity:0, filter:'blur(8px)'}}, {{opacity:1, filter:'blur(0px)', duration:.3}}, 2.6);
for (let i=0;i<8;i++) {{
  tl.fromTo('#b-r'+i, {{opacity:0, scale:.3}}, {{opacity:1, scale:1, duration:.7, ease:'back.out(1.6)'}}, 2.7+i*.32);
  tl.fromTo('#b-l'+i, {{opacity:0, filter:'blur(6px)'}}, {{opacity:1, filter:'blur(0px)', duration:.25}}, 2.85+i*.32);
}}
// rebuild into the status board
tl.to('.blab', {{opacity:0, duration:.25, ease:'power3.in'}}, 6.1);
tl.to('#b-title', {{opacity:0, duration:.25}}, 6.1);
for (let i=0;i<8;i++) {{
  tl.to('#b-r'+i, {{x:BXY[i][0]-G[i][0], y:BXY[i][1]-G[i][1], scale:80/230, duration:.8, ease:'power3.inOut'}}, 6.2+i*.03);
  tl.fromTo('#b-row'+i, {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:.4, ease:'expo.out'}}, 6.75+i*.04);
}}
// status segments light up with the three words
const segG = gsap.utils.toArray('#b-board .seg.g'), segA = gsap.utils.toArray('#b-board .seg.a'), segE = gsap.utils.toArray('#b-board .seg.e');
tl.to(segG, {{backgroundColor:'#10B981', duration:.2, stagger:.025}}, 8.4);
tl.fromTo('#b-c1', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.4, ease:'back.out(1.8)'}}, 8.5);
tl.to(segA, {{backgroundColor:'#F59E0B', duration:.2, stagger:.04}}, 9.3);
tl.fromTo('#b-c2', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.4, ease:'back.out(1.8)'}}, 9.35);
tl.to(segE, {{backgroundColor:'#94A3B8', duration:.2, stagger:.04}}, 10.1);
tl.fromTo('#b-c3', {{opacity:0, scale:.6}}, {{opacity:1, scale:1, duration:.4, ease:'back.out(1.8)'}}, 10.15);
// pole 1 circle grows: becomes the service page
tl.to('#b-board,.chip,#b1-bt,#b1-bo,#b2-bt,#b2-bo,[id^=b-r]:not(#b-r0)', {{opacity:0, duration:.3, ease:'power3.in'}}, {d-0.9});
tl.to('#b-r0', {{x:350-G[0][0], y:585-G[0][1], scale:350/230, duration:.8, ease:'power3.inOut'}}, {d-0.9});
"""))

# ---------------- C: page de service ----------------
d = S['service']['dur']
W('service', scene('service', d, """
#root{background:#fff}
#c-shot{clip-path:circle(175px at 350px 585px)}
""", """
<div id="c-shot" class="shot"><div class="cam" id="c-cam"><img src="assets/shots/service-kine.png" alt=""></div></div>
""", """
tl.set('#c-cam', camS(560,300,1.3), 0);
tl.fromTo('#c-shot', {clipPath:'circle(175px at 350px 585px)'}, {clipPath:'circle(2300px at 350px 585px)', duration:.9, ease:'power3.inOut'}, 0);
tl.to('#c-cam', {...camS(470,610,1.55), duration:.8, ease:'power2.inOut'}, 1.7);
tl.to('#c-cam', {...camS(480,840,1.45), duration:.7, ease:'power2.inOut'}, 2.7);
tl.to('#c-cam', {...camS(1100,690,1.45), duration:.8, ease:'power2.inOut'}, 3.6);
"""))

# ---------------- D: rendez-vous ----------------
d = S['rdv']['dur']
W('rdv', scene('rdv', d, """
#root{background:#fff}
#d-s2,#d-s3{opacity:0}
#d-gw{opacity:0}
#d-green{background:#10B981;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:30px;color:#fff}
#d-wa{width:200px;height:200px}
#d-num{font-family:'Bricolage Grotesque';font-weight:800;font-size:110px;letter-spacing:-.01em}
#d-sub{font-size:40px;font-weight:600;opacity:.95}
""", f"""
<div id="d-s1" class="shot"><div class="cam" id="d-cam1"><img src="assets/shots/rdv-filled.png" alt=""></div></div>
<div id="d-s2" class="shot"><div class="cam" id="d-cam2"><img src="assets/shots/rdv-filled-bottom.png" alt=""></div></div>
<div id="d-s3" class="shot"><div class="cam" id="d-cam3"><img src="assets/shots/rdv-sent.png" alt=""></div></div>
<div id="d-cur" class="cursor">{CURSOR}</div>
<div id="d-gw" class="full" style="z-index:40"><div id="d-green" class="full"><svg id="d-wa" viewBox="0 0 24 24"><path fill="#fff" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3c.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg><div id="d-num">+243 998 664 028</div><div id="d-sub">WhatsApp du centre, depuis chaque page</div></div></div>
""", """
tl.set('#d-cam1', camS(470,180,1.75), 0);
tl.fromTo('#d-cam1', camS(470,140,1.6), {...camS(470,180,1.75), duration:1.0, ease:'power2.out'}, 0);
tl.to('#d-cam1', {...camS(470,420,1.75), duration:.8, ease:'power2.inOut'}, 1.4);
// cut to the bottom of the same form, cursor clicks "Envoyer"
tl.set('#d-s2', {opacity:1}, 2.3);
tl.set('#d-cam2', camS(500,480,1.5), 2.3);
tl.fromTo('#d-cur', {x:1500, y:1100}, {x:()=>pt(354,592,500,480,1.5).x-6, y:()=>pt(354,592,500,480,1.5).y-4, duration:.5, ease:'power3.out'}, 2.3);
tl.to('#d-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 2.85);
// sent
tl.set('#d-s3', {opacity:1}, 2.98);
tl.fromTo('#d-cam3', camS(720,330,1.95), {...camS(720,330,1.7), duration:.6, ease:'expo.out'}, 2.98);
tl.set('#d-cur', {opacity:0}, 2.98);
// whatsapp: cursor to the floating button, it grows into the screen
tl.to('#d-cam3', {...camS(1100,600,1.2), duration:.7, ease:'power2.inOut'}, 3.6);
tl.set('#d-cur', {opacity:1, x:1500, y:1150}, 3.6);
tl.to('#d-cur', {x:()=>pt(1392,852,1100,600,1.2).x-4, y:()=>pt(1392,852,1100,600,1.2).y-2, duration:.6, ease:'power3.out'}, 3.8);
tl.to('#d-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 4.45);
tl.set('#d-cur', {opacity:0}, 4.6);
tl.set('#d-gw', {opacity:1}, 4.55);
tl.fromTo('#d-green', {clipPath:()=>{const p=pt(1392,852,1100,600,1.2);return `circle(48px at ${p.x}px ${p.y}px)`;}}, {clipPath:()=>{const p=pt(1392,852,1100,600,1.2);return `circle(2400px at ${p.x}px ${p.y}px)`;}, duration:.7, ease:'power3.in'}, 4.55);
tl.fromTo('#d-wa,#d-num,#d-sub', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.3, stagger:.1}, 5.0);
"""))

# ---------------- E: bascule ----------------
d = S['bascule']['dur']
W('bascule', scene('bascule', d, """
#root{background:#fff}
#e-teal{background:var(--teal950);z-index:5}
#e-l1{left:150px;top:300px;font-size:64px;color:var(--teal700);z-index:3}
#e-l1b{left:150px;top:390px;font-size:210px;color:var(--teal900);z-index:3}
#e-l2{left:150px;top:300px;font-size:64px;color:var(--teal500);z-index:8}
#e-l2b{left:150px;top:390px;font-size:180px;color:#fff;z-index:8;width:1700px}
#e-l2b em{font-style:normal;color:var(--or)}
""", f"""
<div id="e-l1" class="abs disp">Côté patient</div>
<div id="e-l1b" class="abs disp">Simple.</div>
<div id="e-teal" class="full"></div>
{bands('e', x=-400, y=380, length=3000, teal_w=150, or_w=46, z=7)}
<div id="e-l2" class="abs disp">Côté centre</div>
<div id="e-l2b" class="abs disp">L'envers <em>du décor</em></div>
""", """
tl.fromTo('#e-l1', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.3}, .25);
tl.fromTo('#e-l1b', {opacity:0, scale:1.08, filter:'blur(10px)'}, {opacity:1, scale:1, filter:'blur(0px)', duration:.5, ease:'expo.out', transformOrigin:'0 50%'}, .9);
tl.set('#e-bt,#e-bo', {xPercent:-105}, 0);
tl.to('#e-bt', {xPercent:0, duration:.55, ease:'power3.inOut'}, 1.75);
tl.to('#e-bo', {xPercent:0, duration:.55, ease:'power3.inOut'}, 1.82);
tl.fromTo('#e-teal', {clipPath:'polygon(0 0,0 0,0 100%,0 100%)'}, {clipPath:'polygon(0 0,140% 0,100% 100%,0 100%)', duration:.6, ease:'power3.inOut'}, 1.95);
tl.to('#e-bt,#e-bo', {xPercent:105, duration:.6, ease:'power3.in'}, 2.4);
tl.set('#e-l1,#e-l1b', {opacity:0}, 2.56);
tl.fromTo('#e-l2', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.3}, 2.25);
tl.fromTo('#e-l2b', {opacity:0, filter:'blur(10px)'}, {opacity:1, filter:'blur(0px)', duration:.35, ease:'expo.out'}, 2.75);
"""))

# ---------------- F: connexion ----------------
d = S['login']['dur']
W('login', scene('login', d, """
#root{background:var(--teal950)}
#f-wrap{position:absolute;inset:0}
#f-s2{opacity:0}
""", f"""
<div id="f-wrap">
<div id="f-s1" class="shot"><div class="cam" id="f-cam1"><img src="assets/shots/login.png" alt=""></div></div>
<div id="f-s2" class="shot"><div class="cam" id="f-cam2"><img src="assets/shots/login-demo.png" alt=""></div></div>
</div>
<div id="f-cur" class="cursor">{CURSOR}</div>
""", """
tl.fromTo('#f-wrap', {clipPath:'polygon(0 0,0 0,0 100%,0 100%)'}, {clipPath:'polygon(0 0,140% 0,100% 100%,0 100%)', duration:.6, ease:'power3.inOut'}, 0);
tl.set('#f-cam1', camS(1040,560,1.5), 0);
tl.fromTo('#f-cur', {x:1700, y:1150}, {x:()=>pt(1010,653,1040,560,1.5).x, y:()=>pt(1010,653,1040,560,1.5).y, duration:.6, ease:'power3.out'}, .4);
tl.to('#f-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 1.05);
// the demo list opens (page scrolled 150 px on the second capture)
tl.set('#f-s2', {opacity:1}, 1.2);
tl.set('#f-cam2', camS(1040,410,1.5), 1.2);
tl.to('#f-cam2', {...camS(1040,640,1.3), duration:.8, ease:'power2.inOut'}, 1.3);
tl.set('#f-cur', {opacity:0}, 1.2);
// "chacun arrive directement dans son module": the left panel
tl.to('#f-cam2', {...camS(330,580,1.45), duration:.8, ease:'power2.inOut'}, 2.1);
// back to the list, click Nadine (Accueil)
tl.to('#f-cam2', {...camS(1040,640,1.3), duration:.6, ease:'power2.inOut'}, 3.2);
tl.set('#f-cur', {opacity:1, x:1700, y:1150}, 3.3);
tl.to('#f-cur', {x:()=>pt(1110,722,1040,640,1.3).x, y:()=>pt(1110,722,1040,640,1.3).y, duration:.5, ease:'power3.out'}, 3.5);
tl.to('#f-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 4.05);
"""))

# ---------------- G: accueil ----------------
d = S['accueil']['dur']
W('accueil', scene('accueil', d, """
#root{background:#fff}
#g-iris{position:absolute;inset:0}
#g-s2,#g-s3,#g-s4{opacity:0}
""", f"""
<div id="g-iris">
<div id="g-s1" class="shot"><div class="cam" id="g-cam1"><img src="assets/shots/acc-list.png" alt=""></div></div>
<div id="g-s2" class="shot"><div class="cam" id="g-cam2"><img src="assets/shots/acc-detail.png" alt=""></div></div>
<div id="g-s3" class="shot"><div class="cam" id="g-cam3"><img src="assets/shots/acc-plan-form.png" alt=""></div></div>
<div id="g-s4" class="shot"><div class="cam" id="g-cam4"><img src="assets/shots/acc-planned.png" alt=""></div></div>
</div>
<div id="g-cur" class="cursor">{CURSOR}</div>
""", """
tl.fromTo('#g-iris', {clipPath:'circle(40px at 960px 560px)'}, {clipPath:'circle(1300px at 960px 560px)', duration:.5, ease:'power3.in'}, 0);
tl.set('#g-cam1', camS(560,520,1.25), 0);
tl.to('#g-cam1', {...camS(520,640,1.6), duration:1.0, ease:'power2.inOut'}, .3);
// click the request
tl.fromTo('#g-cur', {x:1500, y:1150}, {x:()=>pt(345,645,520,640,1.6).x, y:()=>pt(345,645,520,640,1.6).y, duration:.5, ease:'power3.out'}, .9);
tl.to('#g-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 1.45);
tl.set('#g-s2', {opacity:1}, 1.6);
tl.set('#g-cam2', camS(520,640,1.6), 1.6);
tl.set('#g-cur', {opacity:0}, 1.6);
tl.to('#g-cam2', {...camS(1170,560,1.55), duration:.8, ease:'power2.inOut'}, 1.7);
// call
tl.to('#g-cam2', {...camS(1100,520,1.8), duration:.6, ease:'power2.inOut'}, 2.6);
// plan
tl.set('#g-s3', {opacity:1}, 3.5);
tl.set('#g-cam3', camS(1170,700,1.6), 3.5);
tl.fromTo('#g-s3', {opacity:0}, {opacity:1, duration:.2}, 3.5);
tl.to('#g-cam3', {...camS(1170,660,1.75), duration:.6, ease:'power2.inOut'}, 4.4);
tl.to('#g-cam3', {...camS(1170,760,1.7), duration:.6, ease:'power2.inOut'}, 5.4);
tl.set('#g-cur', {opacity:1, x:1500, y:1150}, 5.8);
tl.to('#g-cur', {x:()=>pt(1170,854,1170,760,1.7).x, y:()=>pt(1170,854,1170,760,1.7).y, duration:.5, ease:'power3.out'}, 5.9);
tl.to('#g-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 6.45);
// planned
tl.set('#g-s4', {opacity:1}, 6.6);
tl.set('#g-cur', {opacity:0}, 6.6);
tl.fromTo('#g-cam4', camS(1180,330,1.45), {...camS(1180,320,1.3), duration:.6, ease:'expo.out'}, 6.6);
tl.to('#g-cam4', {...camS(1180,560,1.35), duration:.7, ease:'power2.inOut'}, 7.35);
"""))

# ---------------- H: modules ----------------
mods = [('kine','Kiné'),('medecin','Médecin'),('coach','Coach'),('caisse','Caisse')]
cuts = S['modules']['cuts']
quad = [(0,0),(960,0),(0,540),(960,540)]
d = S['modules']['dur']
shots_html = ''.join(f'<div id="h-s{i}" class="shot" style="z-index:{i+1}"><div class="cam" id="h-cam{i}"><img src="assets/shots/mod-{m}-toast.png" alt=""></div><div class="tag disp" id="h-t{i}" style="left:110px;bottom:90px;font-size:84px;padding:18px 48px;background:var(--or);box-shadow:0 18px 40px rgba(7,41,58,.3)">{lab}</div></div>' for i,(m,lab) in enumerate(mods))
W('modules', scene('modules', d, """
#root{background:var(--teal950)}
.shot{transform-origin:0 0}
#h-s1,#h-s2,#h-s3{opacity:0}
""", shots_html, f"""
const C = {json.dumps(cuts)}; const Q = {json.dumps(quad)};
for (let i=0;i<4;i++) {{
  tl.set('#h-cam'+i, camS(760,250,1.15), 0);
  tl.set('#h-s'+i, {{opacity:1}}, C[i]);
  if (i>0) tl.set('#h-s'+(i-1), {{opacity:0}}, C[i]+0.02);
  tl.fromTo('#h-cam'+i, camS(760,250,1.22), {{...camS(760,250,1.15), duration:1.6, ease:'power2.out'}}, C[i]);
  tl.fromTo('#h-t'+i, {{opacity:0, x:-40}}, {{opacity:1, x:0, duration:.35, ease:'expo.out'}}, C[i]+.15);
}}
// all four side by side: each in its own module
const g = {d-1.25};
for (let i=0;i<4;i++) {{
  tl.to('#h-s'+i, {{x:Q[i][0]+8, y:Q[i][1]+8, scale:(944/1920), duration:.7, ease:'power3.inOut'}}, g);
  tl.to('#h-t'+i, {{opacity:0, duration:.2}}, g);
  tl.set('#h-s'+i, {{opacity:1}}, g);
}}
"""))

# ---------------- I: direction ----------------
d = S['direction']['dur']
W('direction', scene('direction', d, """
#root{background:var(--teal950)}
#i-shell{position:absolute;inset:0;transform-origin:0 0}
#i-s2,#i-s3{opacity:0}
""", f"""
<div id="i-shell">
<div id="i-s1" class="shot"><div class="cam" id="i-cam1"><img src="assets/shots/dir-dash-toast.png" alt=""></div></div>
<div id="i-s2" class="shot"><div class="cam" id="i-cam2"><img src="assets/shots/dir-part.png" alt=""></div></div>
<div id="i-s3" class="shot"><div class="cam" id="i-cam3"><img src="assets/shots/dir-part-toggled.png" alt=""></div></div>
</div>
<div id="i-cur" class="cursor">{CURSOR}</div>
""", """
// arrives as a fifth tile growing from the grid centre
tl.fromTo('#i-shell', {scale:.2, x:768, y:432}, {scale:1, x:0, y:0, duration:.7, ease:'power3.out'}, 0);
tl.set('#i-cam1', camS(620,250,1.55), 0);
tl.to('#i-cam1', {...camS(720,330,1.12), duration:1.4, ease:'power2.inOut'}, 1.3);
tl.to('#i-cam1', {...camS(140,400,1.35), duration:.9, ease:'power2.inOut'}, 2.8);
// partners
tl.set('#i-s2', {opacity:1}, 3.6);
tl.set('#i-cam2', camS(700,320,1.3), 3.6);
tl.fromTo('#i-s2', {clipPath:'inset(0 0 0 100%)'}, {clipPath:'inset(0 0 0 0%)', duration:.45, ease:'power3.inOut'}, 3.6);
tl.to('#i-cam2', {...camS(640,450,1.5), duration:.9, ease:'power2.inOut'}, 4.6);
tl.fromTo('#i-cur', {x:1500, y:1150}, {x:()=>pt(595,497,640,450,1.5).x, y:()=>pt(595,497,640,450,1.5).y, duration:.6, ease:'power3.out'}, 5.8);
tl.to('#i-cur', {scale:.85, duration:.06, yoyo:true, repeat:1, transformOrigin:'10% 5%'}, 7.05);
tl.set('#i-s3', {opacity:1}, 7.2);
tl.set('#i-cur', {opacity:0}, 7.2);
tl.fromTo('#i-cam3', camS(1000,330,1.25), {...camS(1000,360,1.2), duration:.7, ease:'expo.out'}, 7.2);
"""))

# ---------------- J: promesse ----------------
d = S['promesse']['dur']
W('promesse', scene('promesse', d, """
#root{background:#fff}
.pl{left:150px;font-size:88px;color:var(--teal900);width:1000px}
.pl em{font-style:normal;color:var(--or)}
#j-doc{left:1270px;top:170px;width:520px;height:520px}
#j-p1{left:1530px;top:640px;width:250px;height:250px}
#j-p2{left:1010px;top:40px;width:170px;height:170px}
""", f"""
{bands('j1', x=-560, y=-40, length=1200, z=1)}
{bands('j2', x=1300, y=980, length=1200, z=1)}
<div id="j-doc" class="ring t"><div class="in"><img src="assets/img/hero-doc.jpg" alt="" style="object-position:50% 20%"></div></div>
<div id="j-p1" class="ring"><div class="in"><img src="assets/img/pole4.jpg" alt=""></div></div>
<div id="j-p2" class="ring t"><div class="in"><img src="assets/img/pole5.jpg" alt=""></div></div>
<div id="j-l1" class="abs disp pl" style="top:250px">Un centre <em>moderne</em></div>
<div id="j-l2" class="abs disp pl" style="top:430px">Des patients <em>mieux accueillis</em></div>
<div id="j-l3" class="abs disp pl" style="top:660px">Une Direction qui <em>garde la main</em></div>
""", """
tl.set('#j1-bt,#j1-bo,#j2-bt,#j2-bo', {xPercent:-100}, 0);
tl.to('#j1-bt,#j2-bt', {xPercent:0, duration:.6, ease:'power3.out'}, 0);
tl.to('#j1-bo,#j2-bo', {xPercent:0, duration:.6, ease:'power3.out'}, .07);
tl.fromTo('#j-doc', {scale:.3, opacity:0}, {scale:1, opacity:1, duration:.8, ease:'back.out(1.4)'}, .2);
tl.fromTo('#j-p1', {scale:.3, opacity:0}, {scale:1, opacity:1, duration:.7, ease:'back.out(1.5)'}, 1.7);
tl.fromTo('#j-p2', {scale:.3, opacity:0}, {scale:1, opacity:1, duration:.7, ease:'back.out(1.5)'}, 3.4);
tl.fromTo('#j-l1', {opacity:0, filter:'blur(10px)'}, {opacity:1, filter:'blur(0px)', duration:.3, ease:'expo.out'}, .4);
tl.fromTo('#j-l2', {opacity:0, filter:'blur(10px)'}, {opacity:1, filter:'blur(0px)', duration:.3, ease:'expo.out'}, 1.8);
tl.fromTo('#j-l3', {opacity:0, filter:'blur(10px)'}, {opacity:1, filter:'blur(0px)', duration:.3, ease:'expo.out'}, 3.5);
"""))

# ---------------- K: fin ----------------
d = S['fin']['dur']
W('fin', scene('fin', d, """
#root{background:var(--teal950)}
#k-logo{left:310px;top:300px;width:400px;height:400px}
#k-logo .in{padding:30px}
#k-logo img{object-fit:contain;border-radius:0}
#k-word,#k-sub,#k-motto,#k-cta,#k-credit{z-index:6}
#k-word{left:790px;top:300px;font-size:240px;color:#fff}
#k-sub{left:800px;top:545px;white-space:nowrap;font-size:38px;color:var(--teal500);letter-spacing:.01em}
#k-motto{left:800px;top:620px;white-space:nowrap;font-size:34px;font-weight:800;color:var(--or);letter-spacing:.08em;display:flex;align-items:center;gap:22px}
#k-motto i{display:inline-block;width:90px;height:3px;background:var(--or)}
#k-cta{left:800px;top:740px;font-size:38px;font-weight:700;color:#fff;background:var(--teal600);padding:20px 40px;border-radius:18px}
#k-credit{left:150px;top:960px;font-size:28px;color:#8FB6C8}
""", f"""
{bands('k', x=-500, y=420, length=3200, teal_w=140, or_w=44, z=2)}
<div id="k-logo" class="ring" style="z-index:5"><div class="in"><img src="assets/img/logo.png" alt=""></div></div>
<div id="k-word" class="abs disp">CMKS</div>
<div id="k-sub" class="abs disp">Centre moderne de kinésithérapie &amp; de sports</div>
<div id="k-motto" class="abs"><i></i>EXCELLENCE • BIEN-ÊTRE • PERFORMANCE<i></i></div>
<div id="k-cta" class="abs">cmks.therapeutique.online</div>
<div id="k-credit" class="abs">Musique : « Inspiring Corporate », Soundrider/Dope — CC BY 3.0</div>
""", """
tl.set('#k-bt,#k-bo', {xPercent:-105}, 0);
tl.to('#k-bt', {xPercent:0, duration:.6, ease:'power3.out'}, 0);
tl.to('#k-bo', {xPercent:0, duration:.6, ease:'power3.out'}, .08);
// the band carries the logo in
tl.fromTo('#k-logo', {x:-700, y:350, rotation:-60, opacity:1}, {x:0, y:0, rotation:0, duration:1.0, ease:'expo.out'}, .25);
tl.to('#k-bt,#k-bo', {opacity:.18, duration:.6}, 1.2);
tl.fromTo('#k-word', {clipPath:'inset(0 100% 0 0)'}, {clipPath:'inset(0 0% 0 0)', duration:.5, ease:'power3.out'}, .45);
tl.fromTo('#k-sub', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.3}, .9);
tl.fromTo('#k-motto', {opacity:0, filter:'blur(8px)'}, {opacity:1, filter:'blur(0px)', duration:.35}, 1.4);
tl.fromTo('#k-motto i', {scaleX:0}, {scaleX:1, duration:.5, ease:'expo.out'}, 1.5);
tl.fromTo('#k-cta', {opacity:0, scale:.8}, {opacity:1, scale:1, duration:.5, ease:'back.out(1.6)', transformOrigin:'0 50%'}, 3.0);
tl.fromTo('#k-credit', {opacity:0}, {opacity:1, duration:.4}, 3.4);
"""))

# ---------------- root ----------------
import subprocess
def dur_of(f):
    return round(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',os.path.join(ROOT,f)]).decode()),3)
hosts = []
for i,s in enumerate(T['scenes']):
    hosts.append(f'<div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080" class="clip"></div>')
voices = []
for v in T['voice']:
    voices.append(f'<audio id="vo{v["n"]}" class="clip" src="assets/voice/l{v["n"]}.wav" data-start="{v["at"]}" data-duration="{dur_of("assets/voice/l"+str(v["n"])+".wav")}" data-track-index="2" data-volume="1"></audio>')
sfx = []; lanes = []
for k,e in enumerate(T['sfx']):
    f,at,vol = e[:3]; ms = e[3] if len(e)>3 else 0
    du = round(min(dur_of("assets/sfx/"+f)-ms, 3.0),3)
    li = next((i for i,end in enumerate(lanes) if end <= at), None)
    if li is None: lanes.append(0); li = len(lanes)-1
    lanes[li] = at+du
    extra = f' data-media-start="{ms}"' if ms else ''
    sfx.append(f'<audio id="fx{k+1}" class="clip" src="assets/sfx/{f}" data-start="{at}" data-duration="{du}"{extra} data-track-index="{3+li}" data-volume="{vol}"></audio>')
total = T['total']
bgm = T['bgm']
index = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ margin:0; width:1920px; height:1080px; overflow:hidden; background:#07293A; }}
#root {{ width:100%; height:100%; position:relative; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
<audio id="bgm" class="clip" src="assets/bgm/inspiring-corporate.mp3" data-start="0" data-media-start="{bgm['media_start']}" data-duration="{total}" data-track-index="1" data-volume="{bgm['volume']}" data-fade-in="0.8" data-fade-out="{bgm['fade_out']}"></audio>
{chr(10).join(voices)}
{chr(10).join(sfx)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = gsap.timeline({{ paused: true }});
</script>
</body>
</html>
"""
open(os.path.join(ROOT,'index.html'),'w').write(index)
print('ok')
