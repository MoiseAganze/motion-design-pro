#!/usr/bin/env python3
"""Génère index.html et compositions/*.html du film COOPECPLUS.

Les scènes produit sont décrites par des listes d'événements en temps GLOBAL (secondes de la voix) ;
le script les convertit en temps local de scène et écrit des fichiers HTML statiques.
Relancer : python3 build.py
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
COMP = os.path.join(ROOT, "compositions")
os.makedirs(COMP, exist_ok=True)

TOTAL = 112.0
INK, BLUE, CYAN, PAPER, GREEN, RED = "#132032", "#1E4976", "#5CB8DA", "#F9FAFC", "#15803D", "#DC2626"

# Fenêtre de l'appli dans le cadre (coordonnées des captures en px CSS 1536 x 864)
WX, WY, WW = 160, 140, 1600
K = WW / 1536
WH = 864 * K
FX, FY = 960, 560  # point du cadre où l'on centre la cible
LOGO = (28, 32)  # carré « C+ » dans la capture
LOGO_SIZE = 260  # taille du C+ HTML au raccord

SFX = []  # (t, fichier, volume)


def sfx(t, f, v=0.45):
    SFX.append((round(t, 3), f, v))


def cam_state(px, py, z, clamp=True, fy=FY):
    X, Y = WX + px * K, WY + py * K
    tx, ty = FX - z * X, fy - z * Y
    if clamp:
        if z * WW >= 1920:
            tx = min(-z * WX, max(1920 - z * (WX + WW), tx))
        else:
            tx = 960 - z * (WX + WW / 2)
        if z * WH >= 1080:
            ty = min(-z * WY, max(1080 - z * (WY + WH), ty))
        else:
            ty = 590 - z * (WY + WH / 2)
    return round(tx, 1), round(ty, 1), z


def logo_state():
    z = LOGO_SIZE / (32 * K)
    return cam_state(LOGO[0], LOGO[1], z, clamp=False, fy=540)[:2] + (z,)


CURSOR_SVG = (
    '<svg width="28" height="28" viewBox="0 0 28 28"><path d="M3 2 L3 22 L8.5 17 L12 25.5 L15.6 24 L12.2 15.8 L19.5 15.8 Z" '
    'fill="#0b0f19" stroke="#ffffff" stroke-width="1.8" stroke-linejoin="round"/></svg>'
)

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;font-family:Inter,sans-serif;}
#root .ground{position:absolute;inset:0;}
#root .rule{position:absolute;inset:0;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 53px,var(--rule) 53px,var(--rule) 54px);}
#root .shift{position:absolute;inset:0;}
#root .cam{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;}
#root .win{position:absolute;left:%(wx)spx;top:%(wy)spx;width:%(ww)spx;height:%(wh)spx;border-radius:14px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.35);background:#F9FAFC;}
#root .inner{position:absolute;left:0;top:0;width:1536px;height:864px;transform:scale(%(k)s);transform-origin:0 0;}
#root .plate{position:absolute;left:0;top:0;width:1536px;height:auto;}
#root .cur{position:absolute;left:0;top:0;width:28px;height:28px;}
#root .hl{position:absolute;border:3.5px solid #5CB8DA;border-radius:9px;background:rgba(92,184,218,.10);}
#root .role{position:absolute;left:44px;top:34px;height:66px;display:flex;align-items:center;gap:16px;padding:0 24px 0 12px;background:#132032;border-radius:12px;color:#fff;font-weight:600;font-size:28px;letter-spacing:-.01em;}
#root .role .av{width:44px;height:44px;border-radius:50%%;background:#1E4976;color:#fff;font-size:20px;font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid #5CB8DA;}
#root .role .clock{font-variant-numeric:tabular-nums;color:#5CB8DA;font-weight:700;}
#root .role .who{color:rgba(255,255,255,.72);font-weight:500;}
#root .co{position:absolute;padding:16px 26px;background:#132032;color:#fff;font-weight:700;font-size:40px;letter-spacing:-.015em;border-radius:12px;box-shadow:0 14px 40px rgba(0,0,0,.28);white-space:nowrap;}
#root .co .w{display:inline-block;margin-right:.26em;}
#root .co .w:last-child{margin-right:0;}
#root .co .acc{color:#5CB8DA;}
#root .obj{position:absolute;left:0;top:0;box-shadow:0 40px 90px rgba(0,0,0,.45);border-radius:4px;}
""" % {"wx": WX, "wy": WY, "ww": WW, "wh": round(WH, 2), "k": round(K, 6)}


def words_html(text, cls="w"):
    out = []
    for w in text.split(" "):
        acc = w.startswith("*")
        w = w.lstrip("*")
        out.append(f'<span class="{cls}{" acc" if acc else ""}">{w}</span>')
    return "".join(out)


class UIScene:
    def __init__(self, sid, start, end, ground=BLUE, rule="rgba(255,255,255,.06)", enter="whip", exit_whip=True):
        self.sid, self.start, self.end = sid, start, end
        self.dur = round(end - start, 3)
        self.ground, self.rule = ground, rule
        self.enter, self.exit_whip = enter, exit_whip
        self.plates = []  # [img]
        self.html_extra = []
        self.js = []
        self.n = 0

    def L(self, t):
        return round(t - self.start, 3)

    def uid(self, p):
        self.n += 1
        return f"{self.sid}-{p}{self.n}"

    # --- plaques
    def plate(self, img):
        if img not in self.plates:
            self.plates.append(img)
        return f"#{self.sid}-pl{self.plates.index(img)}"

    def show(self, t, img, fade=0.15):
        sel = self.plate(img)
        others = [f"#{self.sid}-pl{i}" for i, p in enumerate(self.plates) if p != img]
        self.js.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:{fade},ease:"none",immediateRender:false}},{self.L(t)});')
        self._pending_hide = getattr(self, "_pending_hide", [])
        self._pending_hide.append((t + fade, img))

    def first(self, img):
        sel = self.plate(img)
        self.js.append(f'tl.set("{sel}",{{opacity:1}},0);')
        self._pending_hide = getattr(self, "_pending_hide", [])
        self._pending_hide.append((self.start, img))

    def wipe(self, t, img, dur=1.4):
        sel = self.plate(img)
        self.js.append(f'tl.set("{sel}",{{opacity:1}},{self.L(t)});')
        self.js.append(f'tl.fromTo("{sel}",{{clipPath:"inset(0 0 100% 0)"}},{{clipPath:"inset(0 0 0% 0)",duration:{dur},ease:"power1.inOut"}},{self.L(t)});')
        self._pending_hide = getattr(self, "_pending_hide", [])
        self._pending_hide.append((t + dur, img))

    def iris(self, t, img, px, py, dur=0.4):
        sel = self.plate(img)
        self.js.append(f'tl.set("{sel}",{{opacity:1}},{self.L(t)});')
        self.js.append(f'tl.fromTo("{sel}",{{clipPath:"circle(0px at {px}px {py}px)"}},{{clipPath:"circle(1800px at {px}px {py}px)",duration:{dur},ease:"power2.in"}},{self.L(t)});')
        self._pending_hide = getattr(self, "_pending_hide", [])
        self._pending_hide.append((t + dur, img))

    # --- caméra
    def cam_set(self, t, state):
        tx, ty, z = state
        self.js.append(f'tl.set("#{self.sid}-cam",{{x:{tx},y:{ty},scale:{z}}},{self.L(t)});')

    def cam(self, t, px, py, z, dur=0.7, ease="power2.inOut"):
        tx, ty, z = cam_state(px, py, z)
        self.js.append(f'tl.to("#{self.sid}-cam",{{x:{tx},y:{ty},scale:{z},duration:{dur},ease:"{ease}"}},{self.L(t)});')

    def cam_to(self, t, state, dur, ease):
        tx, ty, z = state
        self.js.append(f'tl.to("#{self.sid}-cam",{{x:{tx},y:{ty},scale:{z},duration:{dur},ease:"{ease}"}},{self.L(t)});')

    # --- curseur
    def cursor(self, t_in, x0, y0, moves):
        """moves: [(t_arrive, x, y, click_bool)]"""
        c = f"#{self.sid}-cur"
        self.js.append(f'tl.set("{c}",{{x:{x0},y:{y0},opacity:0}},0);')
        self.js.append(f'tl.to("{c}",{{opacity:1,duration:0.15}},{self.L(t_in)});')
        prev = t_in
        for (ta, x, y, click) in moves:
            d = max(0.25, min(0.6, ta - prev))
            self.js.append(f'tl.to("{c}",{{x:{x},y:{y},duration:{round(d,3)},ease:"power2.inOut"}},{self.L(ta - d)});')
            if click:
                self.js.append(f'tl.to("{c}",{{scale:0.82,duration:0.07,ease:"power2.in",transformOrigin:"3px 2px"}},{self.L(ta + 0.02)});')
                self.js.append(f'tl.to("{c}",{{scale:1,duration:0.12,ease:"power2.out",transformOrigin:"3px 2px"}},{self.L(ta + 0.09)});')
                sfx(ta + 0.03, "click.mp3", 0.55)
            prev = ta

    def cursor_hide(self, t):
        self.js.append(f'tl.to("#{self.sid}-cur",{{opacity:0,duration:0.12}},{self.L(t)});')

    # --- surlignage (coordonnées capture)
    def hl(self, t, cx, cy, w, h, until):
        i = self.uid("hl")
        self.html_extra.append(("inner", f'<div id="{i}" class="hl" style="left:{cx - w/2 - 6}px;top:{cy - h/2 - 6}px;width:{w + 12}px;height:{h + 12}px;opacity:0"></div>'))
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:0.35,ease:"expo.out"}},{self.L(t)});')
        self.js.append(f'tl.to("#{i}",{{opacity:0,duration:0.2}},{self.L(until)});')

    # --- repère texte (coordonnées cadre)
    def callout(self, t, text, x, y, until, anchor="left"):
        i = self.uid("co")
        pos = f"left:{x}px;" if anchor == "left" else f"right:{1920 - x}px;"
        self.html_extra.append(("top", f'<div id="{i}" class="co" style="{pos}top:{y}px;opacity:0">{words_html(text)}</div>'))
        self.js.append(f'tl.set("#{i}",{{opacity:1}},{self.L(t)});')
        self.js.append(f'tl.fromTo("#{i}",{{clipPath:"inset(0 100% 0 0 round 12px)"}},{{clipPath:"inset(0 0% 0 0 round 12px)",duration:0.35,ease:"expo.out"}},{self.L(t)});')
        self.js.append(f'tl.fromTo("#{i} .w",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.13,stagger:0.07}},{self.L(t + 0.08)});')
        self.js.append(f'tl.to("#{i}",{{opacity:0,filter:"blur(8px)",duration:0.2,ease:"power3.in"}},{self.L(until)});')
        sfx(t, "pop.mp3", 0.28)

    # --- ligne de rôle
    def role(self, t, initials, clock, role, who, until=None):
        i = self.uid("role")
        self.html_extra.append(("top", f'<div id="{i}" class="role" style="opacity:0"><div class="av" data-layout-ignore>{initials}</div><span class="clock">{clock}</span><span>{role}</span><span class="who">{who}</span></div>'))
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,x:-30,filter:"blur(6px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:0.45,ease:"expo.out"}},{self.L(t)});')
        if until is not None:
            self.js.append(f'tl.to("#{i}",{{opacity:0,filter:"blur(6px)",duration:0.18,ease:"power3.in"}},{self.L(until)});')

    # --- objet porté (reçu, contrat) : img native 2x
    def paper(self, t_in, t_out, img, nat_w, nat_h, width, cx, fracs):
        """fracs: [(t, frac)] — la fraction de hauteur du papier placée au centre vertical du cadre."""
        i = self.uid("obj")
        h = width * nat_h / nat_w
        self.html_extra.append(("top", f'<img id="{i}" class="obj" src="{img}" style="width:{width}px;height:{round(h,1)}px;opacity:0" alt="">'))
        x = cx - width / 2
        ty0 = 540 - fracs[0][1] * h
        self.js.append(f'tl.set("#{i}",{{x:{round(x,1)},y:1120,opacity:1,rotation:-1.2}},{self.L(t_in)});')
        self.js.append(f'tl.to("#{i}",{{y:{round(ty0,1)},rotation:0,duration:0.65,ease:"expo.out"}},{self.L(t_in)});')
        for (t, f) in fracs[1:]:
            self.js.append(f'tl.to("#{i}",{{y:{round(540 - f*h,1)},duration:0.8,ease:"power2.inOut"}},{self.L(t)});')
        self.js.append(f'tl.to("#{i}",{{y:1150,duration:0.32,ease:"power3.in"}},{self.L(t_out)});')
        sfx(t_in, "whoosh-short.mp3", 0.35)

    def bignum(self, t, until, num, label, x, y):
        i = self.uid("big")
        self.html_extra.append(("top", f'<div id="{i}" style="position:absolute;left:{x}px;top:{y}px;opacity:0;padding:26px 44px 30px;background:#132032;border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,.45)"><div style="font-weight:900;font-size:220px;line-height:1;letter-spacing:-.04em;color:#5CB8DA">{num}</div><div style="font-weight:700;font-size:44px;color:#fff;margin-top:6px">{label}</div></div>'))
        self.js.append(f'tl.fromTo("#{i}",{{opacity:0,scale:0.86,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.5,ease:"back.out(1.6)"}},{self.L(t)});')
        self.js.append(f'tl.to("#{i}",{{opacity:0,filter:"blur(8px)",duration:0.22,ease:"power3.in"}},{self.L(until)});')
        sfx(t, "pop.mp3", 0.4)

    # --- whip entre deux rôles dans la scène
    def whip(self, t, after):
        """after(): appelée pour poser l'état (caméra, plaque) au milieu du whip."""
        s = f"#{self.sid}-shift"
        self.js.append(f'tl.to("{s}",{{x:-1300,filter:"blur(18px)",duration:0.2,ease:"power3.in"}},{self.L(t)});')
        after(t + 0.2)
        self.js.append(f'tl.fromTo("{s}",{{x:1300,filter:"blur(18px)"}},{{x:0,filter:"blur(0px)",duration:0.38,ease:"power3.out",immediateRender:false}},{self.L(t + 0.2)});')
        sfx(t + 0.05, ["whoosh.mp3", "whoosh-short.mp3"][len(SFX) % 2], 0.4)

    def render(self):
        # Masquage des plaques précédentes : chaque nouvelle plaque, une fois opaque, cache les autres.
        hides = []
        for (t, img) in sorted(getattr(self, "_pending_hide", [])):
            sel = self.plate(img)
            others = ",".join(f"#{self.sid}-pl{i}" for i, p in enumerate(self.plates) if p != img)
            if others:
                hides.append(f'tl.set("{others}",{{opacity:0}},{self.L(t)});')
        # Entrée / sortie
        pre = []
        if self.enter == "whip":
            pre.append(f'tl.fromTo("#{self.sid}-shift",{{x:1300,filter:"blur(18px)"}},{{x:0,filter:"blur(0px)",duration:0.4,ease:"power3.out"}},0);')
            sfx(self.start, "whoosh.mp3", 0.38)
        post = []
        if self.exit_whip:
            post.append(f'tl.to("#{self.sid}-shift",{{x:-1300,filter:"blur(18px)",duration:0.2,ease:"power3.in"}},{round(self.dur - 0.2,3)});')
        plates = "\n".join(f'<img id="{self.sid}-pl{i}" class="plate" src="assets/ui/{p}.png" style="opacity:0" alt="">' for i, p in enumerate(self.plates))
        inner_extra = "\n".join(h for (where, h) in self.html_extra if where == "inner")
        top_extra = "\n".join(h for (where, h) in self.html_extra if where == "top")
        js = "\n    ".join(pre + self.js + hides + post)
        html = f"""<template>
  <style>
{BASE_CSS}
#root .ground{{background:{self.ground};}}
#root{{--rule:{self.rule};}}
  </style>
  <div id="root" data-composition-id="{self.sid}" data-width="1920" data-height="1080">
    <div class="ground" id="{self.sid}-ground"></div>
    <div class="rule"></div>
    <div class="shift" id="{self.sid}-shift">
      <div class="cam" id="{self.sid}-cam">
        <div class="win"><div class="inner">
{plates}
{inner_extra}
          <div class="cur" id="{self.sid}-cur">{CURSOR_SVG}</div>
        </div></div>
      </div>
    </div>
{top_extra}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {js}
    tl.set({{}}, {{}}, {self.dur});
    window.__timelines["{self.sid}"] = tl;
  </script>
</template>
"""
        with open(os.path.join(COMP, f"{self.sid}.html"), "w") as f:
            f.write(html)


SCENES = []  # (sid, start, end)


def add(sid, start, end):
    SCENES.append((sid, start, end))


# ============================================================ scènes typographiques
LEDGER_CSS = """
#root{position:absolute;inset:0;overflow:hidden;font-family:Inter,sans-serif;background:#EEF2F7;}
#root .rule{position:absolute;inset:0;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 53px,rgba(19,32,50,.07) 53px,rgba(19,32,50,.07) 54px);}
#root .margin{position:absolute;top:0;bottom:0;left:220px;width:2px;background:rgba(220,38,38,.14);}
"""


def scene_hook():
    sid, start, end = "s01", 0.0, 6.5
    add(sid, start, end)
    digits = "07:30"
    # Rouleau par chiffre : chaque chiffre défile quelques valeurs puis se pose.
    rolls = {"0": "5830", "7": "2947", "3": "8163", ":": ":"}
    d_html = []
    js = []
    for i, ch in enumerate(digits):
        if ch == ":":
            d_html.append(f'<span class="dg colon" id="s01-d{i}">:</span>')
            js.append(f'tl.fromTo("#s01-d{i}",{{opacity:0}},{{opacity:1,duration:0.1}},{0.15 + i*0.09});')
            continue
        seq = list(rolls[ch]) + [ch]
        stack = "".join(f"<span>{c}</span>" for c in seq)
        d_html.append(f'<span class="dg" id="s01-d{i}" data-layout-ignore><span class="stk" id="s01-k{i}" data-layout-ignore>{stack}</span></span>')
        n = len(seq) - 1
        t0 = 0.12 + i * 0.09
        js.append(f'tl.fromTo("#s01-k{i}",{{y:0}},{{y:{-n*250},duration:{0.1*n + 0.25},ease:"power3.out"}},{round(t0,2)});')
        sfx(t0 + 0.1 * n + 0.1, "key-press.mp3", 0.35)
    html = f"""<template>
  <style>
{LEDGER_CSS}
#root .clock{{position:absolute;left:300px;top:250px;display:flex;font-weight:900;font-size:250px;line-height:250px;letter-spacing:-.04em;color:{INK};font-variant-numeric:tabular-nums;}}
#root .dg{{display:inline-block;height:250px;overflow:hidden;}}
#root .dg .stk{{display:flex;flex-direction:column;}}
#root .dg .stk span{{height:250px;}}
#root .colon{{padding:0 6px;}}
#root .place{{position:absolute;left:306px;top:540px;font-weight:600;font-size:52px;color:{INK};letter-spacing:-.01em;}}
#root .place .w{{display:inline-block;margin-right:.25em;color:rgba(19,32,50,.18);}}
#root .line{{position:absolute;left:300px;top:700px;height:4px;width:1320px;background:{INK};transform-origin:0 50%;}}
#root .juste{{position:absolute;left:300px;top:812px;display:flex;align-items:center;gap:26px;font-weight:900;font-size:120px;letter-spacing:-.03em;color:{INK};}}
#root .chk{{width:118px;height:118px;border-radius:50%;background:{GREEN};display:flex;align-items:center;justify-content:center;}}
#root .lbl{{position:absolute;left:300px;top:742px;font-weight:600;font-size:46px;color:rgba(19,32,50,.55);}}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div class="rule"></div><div class="margin"></div>
    <div class="clock">{''.join(d_html)}</div>
    <div class="place" id="s01-place">{words_html("Bukavu · vendredi 20 novembre 2026")}</div>
    <div class="line" id="s01-line"></div>
    <div class="lbl" id="s01-lbl">Écart de caisse en fin de journée :</div>
    <div class="juste" id="s01-juste"><div class="chk" id="s01-chk"><svg width="70" height="70" viewBox="0 0 24 24"><path id="s01-tick" d="M4 12.5 L9.5 18 L20 6.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="30" stroke-dashoffset="30"/></svg></div><span>0 franc.</span></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {chr(10).join(js)}
    tl.to("#s01-place .w",{{color:"{INK}",duration:0.1,stagger:0.08}},1.0);
    tl.fromTo("#s01-line",{{scaleX:0}},{{scaleX:1,duration:1.1,ease:"power2.inOut"}},3.0);
    tl.fromTo("#s01-lbl",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},4.2);
    tl.fromTo("#s01-juste",{{opacity:0,filter:"blur(10px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2,ease:"power4.out"}},6.0);
    tl.fromTo("#s01-chk",{{scale:0.4}},{{scale:1,duration:0.45,ease:"back.out(2)"}},6.0);
    tl.to("#s01-tick",{{strokeDashoffset:0,duration:0.3,ease:"power2.out"}},6.1);
    tl.to("#root .clock, #s01-place, #s01-line",{{opacity:0.0,duration:0.2,ease:"power3.in"}},6.3);
    tl.set({{}}, {{}}, {end-start});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    sfx(6.05, "pop.mp3", 0.45)
    open(os.path.join(COMP, f"{sid}.html"), "w").write(html)


def scene_tension():
    sid, start, end = "s02", 6.5, 15.3
    add(sid, start, end)
    L = lambda t: round(t - start, 3)
    html = f"""<template>
  <style>
#root{{position:absolute;inset:0;overflow:hidden;font-family:Inter,sans-serif;background:#EFE8DA;}}
#root .rule{{position:absolute;inset:0;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 53px,rgba(43,95,160,.18) 53px,rgba(43,95,160,.18) 54px);}}
#root .margin{{position:absolute;top:0;bottom:0;left:220px;width:3px;background:rgba(220,38,38,.35);}}
#root .t{{position:absolute;font-weight:900;color:#2B2B2B;letter-spacing:-.035em;line-height:1;}}
#root .xl{{position:absolute;left:1010px;top:360px;}}
#root .cell{{position:absolute;border:2px solid rgba(43,43,43,.35);}}
#root .num{{position:absolute;font-weight:700;font-size:64px;color:#2B2B2B;font-variant-numeric:tabular-nums;letter-spacing:-.02em;}}
#root .strike{{position:absolute;height:9px;background:{RED};border-radius:5px;transform-origin:0 50%;}}
#root .neq{{position:absolute;font-weight:900;font-size:96px;color:{RED};}}
#root .conf{{position:absolute;left:0;right:0;top:390px;height:280px;text-align:center;font-weight:900;font-size:250px;letter-spacing:-.05em;color:#2B2B2B;line-height:1;}}
#root .half{{position:absolute;left:0;right:0;top:0;bottom:0;}}
#root .crack{{position:absolute;left:330px;top:340px;width:1260px;height:6px;background:{RED};transform-origin:0 50%;}}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div class="rule"></div><div class="margin"></div>
    <div id="s02-a" class="t" style="left:300px;top:150px;font-size:150px">Registres papier</div>
    <div id="s02-b" class="xl">
      <div class="cell" style="left:0;top:0;width:300px;height:150px"></div><div class="cell" style="left:298px;top:0;width:300px;height:150px"></div>
      <div class="cell" style="left:0;top:148px;width:300px;height:150px"></div><div class="cell" style="left:298px;top:148px;width:300px;height:150px"></div>
      <div class="t" style="left:44px;top:62px;font-size:170px;color:#1D6F42">Excel</div>
    </div>
    <div id="s02-c">
      <div class="num" style="left:300px;top:780px">Registre : 9 836 500</div>
      <div class="neq" style="left:1010px;top:752px">≠</div>
      <div class="num" style="left:1110px;top:780px">Caisse : 9 786 500</div>
      <div class="strike" id="s02-s" style="left:290px;top:812px;width:1420px"></div>
    </div>
    <div class="conf" id="s02-conf">
      <div class="half" id="s02-h1" style="clip-path:polygon(0 0,100% 0,100% 46%,0 58%)">confiance</div>
      <div class="half" id="s02-h2" style="clip-path:polygon(0 58%,100% 46%,100% 100%,0 100%)">confiance</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#s02-a",{{opacity:0,filter:"blur(10px)",x:-60}},{{opacity:1,filter:"blur(0px)",x:0,duration:0.5,ease:"expo.out"}},{L(6.8)});
    tl.fromTo("#s02-b",{{opacity:0,scale:0.9,filter:"blur(10px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:0.5,ease:"expo.out"}},{L(8.3)});
    tl.fromTo("#s02-c",{{opacity:0,filter:"blur(10px)"}},{{opacity:1,filter:"blur(0px)",duration:0.3,ease:"power4.out"}},{L(9.5)});
    tl.fromTo("#s02-s",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{L(10.4)});
    tl.to("#s02-a, #s02-b, #s02-c",{{opacity:0,filter:"blur(12px)",duration:0.25,ease:"power3.in",stagger:0.05}},{L(12.3)});
    tl.fromTo("#s02-conf",{{opacity:0,filter:"blur(14px)"}},{{opacity:1,filter:"blur(0px)",duration:0.4,ease:"power4.out"}},{L(12.6)});
    tl.to("#s02-h1",{{y:-26,x:-14,rotation:-1.5,duration:0.35,ease:"power3.out"}},{L(14.75)});
    tl.to("#s02-h2",{{y:30,x:16,rotation:1.5,duration:0.35,ease:"power3.out"}},{L(14.75)});
    tl.set({{}}, {{}}, {end-start});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    sfx(6.8, "pop.mp3", 0.3); sfx(8.3, "pop.mp3", 0.3); sfx(9.55, "pop.mp3", 0.3); sfx(14.72, "impact-bass-1.mp3", 0.35)
    open(os.path.join(COMP, f"{sid}.html"), "w").write(html)


def logo_html(prefix, size):
    r = round(size * 0.22)
    fs = round(size * 0.44)
    return (f'<div id="{prefix}-logo" style="position:absolute;left:{960 - size/2}px;top:{540 - size/2}px;width:{size}px;height:{size}px;border-radius:{r}px;'
            f'background:{CYAN};display:flex;align-items:center;justify-content:center;font-weight:700;font-size:{fs}px;color:#172033;letter-spacing:-.02em">C+</div>')


def scene_reveal():
    sid, start, end = "s03", 15.3, 21.9
    add(sid, start, end)
    L = lambda t: round(t - start, 3)
    letters = "".join(f'<span class="l">{c}</span>' for c in "COOPECPLUS")
    html = f"""<template>
  <style>
#root{{position:absolute;inset:0;overflow:hidden;font-family:Inter,sans-serif;background:#EFE8DA;}}
#root .flood{{position:absolute;inset:0;background:{INK};transform-origin:50% 0;}}
#root .rule{{position:absolute;inset:0;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 53px,rgba(255,255,255,.05) 53px,rgba(255,255,255,.05) 54px);}}
#root .word{{position:absolute;left:0;top:0;font-weight:900;font-size:140px;letter-spacing:-.045em;color:#fff;line-height:1;white-space:nowrap;}}
#root .word .l{{display:inline-block;}}
#root .sub{{position:absolute;left:0;top:0;font-weight:600;font-size:46px;color:rgba(255,255,255,.82);white-space:nowrap;}}
#root .sub .w{{display:inline-block;margin-right:.25em;}}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div class="flood" id="s03-flood"></div>
    <div class="rule"></div>
    {logo_html("s03", LOGO_SIZE)}
    <div class="word" id="s03-word" style="left:655px;top:418px">{letters}</div>
    <div class="sub" id="s03-sub" style="left:662px;top:590px">{words_html("Gestion intégrée des coopératives")}<br>{words_html("d'épargne et de crédit")}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#s03-flood",{{scaleY:0}},{{scaleY:1,duration:0.4,ease:"power2.inOut"}},0);
    tl.fromTo("#s03-logo",{{scale:0,rotation:-25,x:-505}},{{scale:1,rotation:0,x:-505,duration:0.7,ease:"back.out(1.5)"}},{L(15.85)});
    tl.fromTo("#s03-word .l",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.14,stagger:0.06}},{L(16.2)});
    tl.fromTo("#s03-sub .w",{{opacity:0,filter:"blur(6px)"}},{{opacity:1,filter:"blur(0px)",duration:0.13,stagger:0.07}},{L(17.4)});
    tl.to("#s03-sub",{{opacity:0,filter:"blur(8px)",duration:0.2,ease:"power3.in"}},{L(21.05)});
    tl.to("#s03-word",{{opacity:0,filter:"blur(10px)",x:60,duration:0.22,ease:"power3.in"}},{L(21.1)});
    tl.to("#s03-logo",{{x:0,duration:0.5,ease:"power3.inOut"}},{L(21.3)});
    tl.set({{}}, {{}}, {end-start});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    sfx(15.0, "whoosh-cinematic.mp3", 0.3); sfx(15.9, "impact-bass-1.mp3", 0.5)
    open(os.path.join(COMP, f"{sid}.html"), "w").write(html)


def scene_end():
    sid, start, end = "s13", 104.6, TOTAL
    add(sid, start, end)
    L = lambda t: round(t - start, 3)
    letters = "".join(f'<span class="l">{c}</span>' for c in "COOPECPLUS")
    html = f"""<template>
  <style>
#root{{position:absolute;inset:0;overflow:hidden;font-family:Inter,sans-serif;background:{INK};}}
#root .rule{{position:absolute;inset:0;background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 53px,rgba(255,255,255,.05) 53px,rgba(255,255,255,.05) 54px);}}
#root .word{{position:absolute;left:655px;top:398px;font-weight:900;font-size:140px;letter-spacing:-.045em;color:#fff;line-height:1;white-space:nowrap;}}
#root .word .l{{display:inline-block;}}
#root .claim{{position:absolute;left:0;right:0;top:720px;text-align:center;font-weight:800;font-size:72px;letter-spacing:-.03em;color:#fff;white-space:nowrap;}}
#root .claim .w{{display:inline-block;margin-right:.24em;color:rgba(255,255,255,.18);}}
#root .claim .w.acc{{}}
#root .sub{{position:absolute;left:662px;top:560px;font-weight:600;font-size:40px;color:rgba(255,255,255,.7);white-space:nowrap;}}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
    <div class="rule"></div>
    {logo_html("s13", LOGO_SIZE)}
    <div class="word" id="s13-word">{letters}</div>
    <div class="sub" id="s13-sub">Gestion intégrée des COOPEC</div>
    <div class="claim" id="s13-claim">{words_html("Votre coopérative, en toute *confiance")}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#s13-logo",{{x:0,y:0,scale:1}},{{x:-505,y:-60,scale:1,duration:0.7,ease:"power3.inOut"}},0.15);
    tl.fromTo("#s13-word",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:0.6,ease:"power3.out"}},0.55);
    tl.fromTo("#s13-sub",{{opacity:0,filter:"blur(8px)"}},{{opacity:1,filter:"blur(0px)",duration:0.2}},1.0);
    tl.fromTo("#s13-claim",{{opacity:0}},{{opacity:1,duration:0.2}},{L(105.45)});
    tl.to("#s13-claim .w",{{color:"#ffffff",duration:0.1,stagger:0.09}},{L(105.7)});
    tl.to("#s13-claim .acc",{{color:"{CYAN}",duration:0.15}},{L(107.65)});
    tl.set({{}}, {{}}, {round(end-start,3)});
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""
    open(os.path.join(COMP, f"{sid}.html"), "w").write(html)


# ============================================================ scènes produit
def s04():
    s = UIScene("s04", 21.9, 30.3, enter="none")
    add(s.sid, s.start, s.end)
    s.first("a11-caisse-journee-fermee")
    s.cam_set(21.9, logo_state())
    s.cam_to(21.95, cam_state(0, 0, 1), 1.0, "power3.inOut")
    s.role(22.6, "JK", "07:30", "Directeur", "Josué Kabila Mulumba", until=24.25)
    s.cam(23.0, 392, 250, 1.8, 0.6)
    s.cursor(22.9, 900, 560, [(23.45, 392, 263, True)])
    s.show(23.55, "a12-journee-ouverte")
    s.callout(23.65, "Journée *ouverte ✓", 1240, 900, 24.25)
    s.cursor_hide(24.0)

    def after(t):
        s.cam_set(t, cam_state(590, 470, 1.35))
        s.js.append(f'tl.set("#{s.sid}-cur",{{opacity:0}},{s.L(t)});')
    s.whip(24.3, after)
    s.show(24.5, "a20-caisse-ouvrir-session", fade=0.01)
    s.role(24.6, "EM", "07:42", "Caissière", "Esther Mwamini")
    s.callout(25.2, "Billetage coupure par coupure", 1120, 900, 27.4, anchor="right")
    s.wipe(25.35, "a20c-billetage-conforme", 1.5)
    s.cam(27.3, 560, 720, 1.8, 0.7)
    s.hl(27.85, 592, 735, 592, 100, 29.0)
    s.callout(27.9, "*Caisse *juste ✓", 1240, 900, 29.0)
    s.cam(28.8, 1150, 700, 1.5, 0.5)
    s.cursor(28.7, 1150, 600, [(29.15, 1418, 826, True)])
    s.show(29.3, "a21-session-ouverte")
    s.cam(29.35, 768, 300, 1.0, 0.6)
    s.cursor_hide(29.5)
    s.render()


def s05():
    s = UIScene("s05", 30.3, 38.9)
    add(s.sid, s.start, s.end)
    s.first("c02-wizard-vide")
    s.cam_set(30.3, cam_state(0, 0, 1))
    s.role(30.5, "GN", "08:15", "Gestionnaire des membres", "Grâce Namegabe")
    s.cam(30.9, 850, 215, 1.9, 0.8)
    for i, x in enumerate([534, 714, 894, 1076, 1258]):
        s.hl(32.2 + i * 0.42, x, 207, 160, 26, 32.2 + i * 0.42 + 0.4 if i < 4 else 34.3)
        sfx(32.2 + i * 0.42, "key-press.mp3", 0.3)
    s.show(34.4, "c03-wizard-identite")
    s.cam(34.4, 760, 480, 1.55, 0.6)
    s.show(35.55, "c05-wizard-piece-photo")
    s.cam(35.5, 1117, 349, 2.0, 0.45)
    s.cam(36.15, 496, 627, 2.3, 0.45)
    s.hl(36.4, 496, 628, 64, 64, 36.85)
    s.cam(36.75, 938, 627, 2.3, 0.45)
    s.hl(36.95, 938, 627, 64, 64, 37.6)
    s.show(37.7, "c06-wizard-beneficiaire")
    s.cam(37.6, 800, 430, 1.3, 0.5)
    s.show(38.3, "c07-wizard-recap")
    s.render()


def s06():
    s = UIScene("s06", 38.9, 47.9)
    add(s.sid, s.start, s.end)
    s.first("c10-encaisser-adhesion")
    s.cam_set(38.9, cam_state(768, 430, 1.35))
    s.role(39.1, "EM", "08:40", "Caissière", "Esther Mwamini")
    s.cam(40.3, 768, 545, 1.95, 0.8)
    s.hl(41.2, 768, 540, 452, 92, 42.5)
    s.cursor(41.5, 700, 610, [(42.65, 972, 641, True)])
    s.show(42.8, "c11-adhesion-ok")
    s.cam(42.85, 768, 432, 1.0, 0.6)
    s.cursor_hide(42.9)
    s.paper(43.35, 45.95, "assets/obj/recu-adhesion.png", 550, 1406, 640, 1180, [(43.35, 0.22), (44.35, 0.585)])
    s.callout(44.7, "Montant en lettres", 200, 860, 45.9)
    s.show(46.1, "c13-fiche-active")
    s.cam_set(46.1, cam_state(768, 432, 1.0))
    s.cam(46.15, 690, 168, 2.0, 0.55)
    s.hl(46.75, 796, 168, 56, 24, 47.8)
    sfx(46.8, "pop.mp3", 0.4)
    s.render()


def s07():
    s = UIScene("s07", 47.9, 55.4, enter="none")
    add(s.sid, s.start, s.end)
    s.first("c20-depot-recherche")
    s.js.append('tl.fromTo("#s07-shift",{opacity:0,filter:"blur(8px)"},{opacity:1,filter:"blur(0px)",duration:0.2},0);')
    s.cam_set(47.9, cam_state(768, 380, 1.45))
    s.role(48.0, "EM", "09:05", "Caissière", "Esther Mwamini")
    s.show(49.3, "c21-depot-saisi")
    s.cam(49.3, 952, 477, 2.05, 0.6)
    s.cam(51.1, 768, 620, 1.95, 0.6)
    s.hl(51.45, 768, 1490 - 864, 720, 66, 52.8)
    s.callout(51.6, "Frais et solde *calculés en direct", 200, 860, 52.9)
    s.cursor(52.2, 980, 700, [(52.85, 1100, 713, True)])
    s.cursor_hide(53.2)
    s.paper(53.2, 55.0, "assets/obj/recu-depot.png", 550, 1508, 640, 1180, [(53.2, 0.52)])
    s.render()


def s08():
    s = UIScene("s08", 55.4, 62.9)
    add(s.sid, s.start, s.end)
    s.first("f01-retrait-photo-signature")
    s.cam_set(55.4, cam_state(768, 280, 1.6))
    s.role(55.6, "EM", "10:20", "Caissière", "Esther Mwamini", until=58.95)
    s.hl(55.9, 469, 267, 96, 96, 56.9)
    s.hl(56.1, 1035, 260, 160, 80, 56.9)
    s.callout(56.0, "Photo et signature affichées", 1760, 860, 56.95, anchor="right")
    s.cam(56.9, 950, 560, 1.7, 0.55)
    s.cursor(56.95, 900, 600, [(57.55, 1099, 711, True)])
    s.show(57.7, "f02-retrait-en-attente")
    s.cursor_hide(57.75)
    s.cam(57.75, 1250, 160, 1.6, 0.55)
    s.hl(58.3, 1340, 70, 330, 70, 58.95)

    def after(t):
        s.cam_set(t, cam_state(1150, 440, 1.6))
        s.js.append(f'tl.set("#{s.sid}-cur",{{opacity:0,x:1150,y:600}},{s.L(t)});')
    s.whip(59.0, after)
    s.show(59.2, "f10-supervision", fade=0.01)
    s.role(59.3, "JK", "10:21", "Directeur", "Josué Kabila Mulumba")
    s.js.append(f'tl.to("#s08-cur",{{opacity:1,duration:0.1}},{s.L(59.35)});')
    s.js.append(f'tl.to("#s08-cur",{{x:1353,y:444,duration:0.45,ease:"power2.inOut"}},{s.L(59.4)});')
    s.js.append(f'tl.to("#s08-cur",{{scale:0.82,duration:0.07,transformOrigin:"3px 2px"}},{s.L(59.87)});')
    s.js.append(f'tl.to("#s08-cur",{{scale:1,duration:0.12,transformOrigin:"3px 2px"}},{s.L(59.95)});')
    sfx(59.88, "click.mp3", 0.55)
    s.show(60.0, "f12-approuve")
    s.cursor_hide(60.2)
    s.paper(60.45, 62.55, "assets/obj/recu-retrait.png", 550, 1573, 640, 1180, [(60.45, 0.66)])
    s.callout(60.9, "Validé par un *second *agent", 200, 860, 62.55)
    s.render()


def s09():
    s = UIScene("s09", 62.9, 75.0)
    add(s.sid, s.start, s.end)
    s.first("g02-demande-simulation")
    s.cam_set(62.9, cam_state(0, 0, 1))
    s.role(63.1, "EL", "11:30", "Gestionnaire de crédit", "Espoir Lukusa", until=70.55)
    s.cam(63.6, 488, 520, 1.6, 0.7)
    s.cam(65.3, 1115, 345, 1.75, 0.7)
    s.cam(66.9, 1115, 610, 1.35, 0.7)
    s.cam(67.9, 1110, 310, 2.4, 0.55)
    s.hl(68.3, 1110, 307, 236, 54, 69.2)
    s.callout(68.4, "TEG affiché *avant *signature", 200, 860, 69.25)
    s.show(69.3, "g05-analyse-ok")
    s.cam(69.3, 590, 600, 1.55, 0.55)
    s.hl(69.95, 617, 650, 130, 44, 70.5)

    def after(t):
        s.cam_set(t, cam_state(620, 300, 1.6))
    s.whip(70.6, after)
    s.show(70.8, "g10-comite", fade=0.01)
    s.role(70.9, "JK", "14:00", "Directeur", "Josué Kabila Mulumba")
    s.cursor(70.95, 600, 420, [(71.15, 358, 309, True)])
    s.show(71.3, "g12-approuve")
    s.cursor_hide(71.5)
    s.show(71.85, "g14-debloquer-dialog")
    s.cam(71.85, 768, 436, 1.55, 0.5)
    s.cursor(71.9, 800, 520, [(72.4, 969, 562, True)])
    s.show(72.55, "g16-echeancier")
    s.cursor_hide(72.6)
    s.cam(72.55, 768, 432, 1.0, 0.5)
    s.paper(73.15, 74.75, "assets/obj/contrat.png", 1594, 2213, 900, 960, [(73.15, 0.36), (73.9, 0.62)])
    s.render()


def s10():
    s = UIScene("s10", 75.0, 82.7)
    add(s.sid, s.start, s.end)
    s.first("h01-ecritures")
    s.cam_set(75.0, cam_state(900, 450, 1.15))
    s.role(75.2, "AM", "16:30", "Comptable", "Alain Mushagalusha")
    s.cam(76.0, 1150, 560, 1.6, 0.7)
    s.hl(76.5, 1258, 580, 104, 560, 78.6)
    s.callout(76.7, "Écritures *automatiques, partie double", 200, 860, 78.7)
    s.show(79.05, "h03-balance")
    s.cam(79.0, 900, 420, 1.2, 0.5)
    s.show(79.7, "h04-etats")
    s.cam(79.7, 900, 330, 1.3, 0.5)
    s.hl(79.95, 1464, 228, 110, 26, 80.4)
    s.cam(80.35, 960, 690, 1.45, 0.6)
    s.hl(80.95, 1424, 730, 190, 26, 82.3)
    s.render()


def s11():
    s = UIScene("s11", 82.7, 95.9, ground=INK, rule="rgba(255,255,255,.05)", enter="none")
    add(s.sid, s.start, s.end)
    # inondation : le sol part du bleu vers le marine, titre « Sécurité »
    s.js.append(f'tl.fromTo("#s11-ground",{{backgroundColor:"{BLUE}"}},{{backgroundColor:"{INK}",duration:0.4,ease:"power2.inOut"}},0);')
    s.html_extra.append(("top", '<div id="s11-title" style="position:absolute;left:0;right:0;top:380px;text-align:center;font-weight:900;font-size:190px;letter-spacing:-.05em;color:#fff;line-height:1">Sécurit<span style="color:#5CB8DA">é</span></div>'))
    s.html_extra.append(("top", f'<div id="s11-tsub" style="position:absolute;left:0;right:0;top:600px;text-align:center;font-weight:600;font-size:46px;color:rgba(255,255,255,.75)">{words_html("au cœur du système").replace('class="w"','class="w" style="display:inline-block;margin-right:.25em"')}</div>'))
    s.js.append('tl.fromTo("#s11-title",{opacity:0,filter:"blur(14px)",scale:1.06},{opacity:1,filter:"blur(0px)",scale:1,duration:0.5,ease:"expo.out"},0.15);')
    s.js.append('tl.fromTo("#s11-tsub .w",{opacity:0,filter:"blur(6px)"},{opacity:1,filter:"blur(0px)",duration:0.13,stagger:0.07},0.95);')
    s.js.append(f'tl.to("#s11-title, #s11-tsub",{{opacity:0,filter:"blur(10px)",duration:0.22,ease:"power3.in"}},{s.L(84.55)});')
    sfx(82.75, "whoosh-cinematic.mp3", 0.28)
    s.js.append('tl.set("#s11-shift",{y:1100},0);')
    s.js.append(f'tl.fromTo("#s11-shift",{{y:1100}},{{y:0,duration:0.55,ease:"expo.out",immediateRender:false}},{s.L(84.7)});')
    s.first("d03-mdp-refuse")
    s.cam_set(82.7, cam_state(768, 440, 1.75))
    s.role(84.9, "A", "07:00", "Administrateur", "premier accès", until=86.9)
    s.hl(85.4, 745, 492, 450, 30, 86.85)
    s.callout(85.5, "Mot de passe prévisible : *refusé", 200, 860, 86.85)
    s.show(87.0, "d11-roles")
    s.cam(86.95, 1000, 330, 1.3, 0.5)
    s.bignum(87.15, 88.75, "91", "permissions, 7 rôles", 170, 330)
    s.hl(87.4, 1172, 380, 110, 360, 88.75)
    s.show(88.9, "h11-journal-audit")
    s.cam(88.85, 700, 290, 1.6, 0.55)
    s.role(89.0, "CI", "17:00", "Contrôleur interne", "lecture seule", until=91.95)
    s.cursor(89.6, 640, 420, [(90.85, 395, 204, True)])
    s.iris(90.95, "h12-audit-integrite-ok", 395, 204, 0.4)
    s.cursor_hide(91.4)
    s.hl(91.35, 565, 262, 560, 56, 92.0)
    s.callout(91.3, "Journal chaîné *intègre", 1760, 860, 92.0, anchor="right")
    s.show(92.1, "f22-caisse-apres-retrait")
    s.cam(92.05, 1150, 540, 1.5, 0.55)
    s.role(92.2, "EM", "17:10", "Caissière", "Esther Mwamini")
    s.hl(92.7, 1443, 540, 44, 230, 95.5)
    s.callout(93.2, "Une erreur ? Opération *inverse, validée", 200, 860, 95.5)
    s.render()


def s12():
    s = UIScene("s12", 95.9, 104.6, ground=BLUE, exit_whip=False)
    add(s.sid, s.start, s.end)
    s.first("i01-cloture-billetage")
    s.cam_set(95.9, cam_state(583, 640, 1.8))
    s.role(96.0, "EM", "18:30", "Caissière", "Esther Mwamini", until=98.05)
    s.hl(96.85, 583, 645, 345, 80, 97.9)
    s.cam(97.4, 900, 680, 1.6, 0.4)
    s.cursor(97.3, 900, 650, [(97.85, 1065, 741, True)])

    def after(t):
        s.cam_set(t, cam_state(1150, 160, 1.6))
        s.js.append(f'tl.set("#{s.sid}-cur",{{opacity:0}},{s.L(t)});')
    s.whip(98.05, after)
    s.show(98.25, "i11-valider-cloture", fade=0.01)
    s.role(98.35, "JK", "18:40", "Directeur", "Josué Kabila Mulumba")
    s.hl(98.6, 1360, 48, 300, 44, 99.0)
    s.callout(98.6, "Clôture validée : *caisse *juste", 200, 860, 99.0)
    s.show(99.1, "h20-dashboard-directeur")
    s.cam(99.05, 768, 432, 1.0, 0.6)
    s.cam(100.2, 585, 240, 1.9, 0.7)
    s.hl(101.8, 585, 240, 600, 64, 102.7)
    s.cam(102.65, 1350, 596, 1.9, 0.7)
    s.hl(103.45, 1350, 596, 290, 100, 104.0)
    s.cam_to(103.92, logo_state(), 0.6, "power3.in")
    sfx(103.6, "riser.mp3", 0.0)
    sfx(104.62, "impact-bass-1.mp3", 0.5)
    s.render()


# ============================================================ index
def build():
    scene_hook(); scene_tension(); scene_reveal()
    s04(); s05(); s06(); s07(); s08(); s09(); s10(); s11(); s12()
    scene_end()
    hosts = []
    for (sid, st, en) in SCENES:
        hosts.append(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{round(en-st,3)}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>')
    auds = ['      <audio id="voix" class="clip" src="assets/voice/voix-off.mp3" data-start="0" data-track-index="2" data-volume="1"></audio>']
    lanes = []  # éviter les chevauchements sur une même piste
    for n, (t, f, v) in enumerate(sorted(SFX)):
        if v <= 0:
            continue
        dur = {"riser.mp3": 10.0, "whoosh-cinematic.mp3": 5.5, "impact-bass-1.mp3": 2.1, "pop.mp3": 0.72, "key-press.mp3": 0.43, "click.mp3": 0.36, "click-soft.mp3": 0.36}.get(f, 0.57)
        lane = 0
        while lane < len(lanes) and lanes[lane] > t:
            lane += 1
        if lane == len(lanes):
            lanes.append(0)
        lanes[lane] = t + dur
        auds.append(f'      <audio id="sfx{n:03d}" class="clip" src="assets/sfx/{f}" data-start="{t}" data-duration="{dur}" data-track-index="{3 + lane}" data-volume="{v}"></audio>')
    html = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {INK}; }}
      #main {{ position: relative; width: 1920px; height: 1080px; font-family: Inter, sans-serif; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
{chr(10).join(auds)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      tl.set({{}}, {{}}, {TOTAL});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    open(os.path.join(ROOT, "index.html"), "w").write(html)
    print(f"{len(SCENES)} scènes, {len(auds)} pistes audio")


if __name__ == "__main__":
    build()
