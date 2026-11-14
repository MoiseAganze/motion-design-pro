from u_parts import ICON, CARD_CSS, card_front, card_back, scene, PHONE_CSS, phone, SHAKE_JS

ROWTXT = "CARTE NATIONALE · CARTE NATIONALE · CARTE NATIONALE · "

# ======================================================== U5  QR → national base → verified 24h/24  (35.8 – 43.2, local = abs - 35.8)
U5_CSS = r"""
    #root { background: #0B2C5A; }
    .u5-row { position: absolute; left: 0; white-space: nowrap; font: 900 190px/1 Montserrat, sans-serif; color: transparent;
      -webkit-text-stroke: 2px rgba(255,255,255,.11); }
    #u5-world { position: absolute; inset: 0; }
    #u5-stage { position: absolute; inset: 0; perspective: 2400px; }
    #u5-card { left: 110px; top: 360px; opacity: 0; }
    #u5-lines { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
    #u5-node { position: absolute; left: 110px; top: 196px; width: 170px; height: 170px; border-radius: 50%; background: #fff; color: #0B2C5A; opacity: 0; }
    #u5-node svg { position: absolute; inset: 38px; width: 94px; height: 94px; }
    #u5-ring { position: absolute; left: 110px; top: 196px; width: 170px; height: 170px; border-radius: 50%; border: 6px solid #FCD116; opacity: 0; }
    #u5-lbl { position: absolute; left: 312px; top: 222px; opacity: 0; }
    #u5-lbl b { display: block; font: 900 50px/1 Montserrat, sans-serif; color: #fff; }
    #u5-lbl span { display: block; margin-top: 14px; font: 600 29px/1 'Open Sans', sans-serif; color: #A9C8F2; }
    #u5-24 { position: absolute; left: 690px; top: 286px; width: 190px; height: 190px; border-radius: 50%; background: #FCD116; color: #0B2C5A;
      text-align: center; opacity: 0; box-shadow: 0 20px 40px rgba(0,0,0,.3); }
    #u5-24 b { display: block; margin-top: 50px; font: 900 56px/1 Montserrat, sans-serif; }
    #u5-24 span { display: block; margin-top: 8px; font: 800 26px/1 Montserrat, sans-serif; }
    #u5-flood { position: absolute; inset: 0; background: #fff; opacity: 0; clip-path: inset(376px 321px 636px 321px round 54px); }
""" + PHONE_CSS + CARD_CSS


def u5():
    rows = "".join(f'<div class="u5-row" id="u5-row{k}" style="top:{110 + k * 440}px">{ROWTXT}</div>' for k in range(4))
    paths = ["M 470 600 C 470 470, 196 500, 196 370", "M 540 600 C 540 450, 240 480, 232 366", "M 610 600 C 610 430, 290 460, 266 358"]
    base = "".join(f'<path id="u5-pb{i}" d="{d}" pathLength="1" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/>' for i, d in enumerate(paths))
    flow = "".join(f'<path id="u5-pf{i}" d="{d}" pathLength="100" fill="none" stroke="#FCD116" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 10" opacity="0"/>' for i, d in enumerate(paths))
    back = card_back("u5c").replace('class="face back"', 'class="face back" style="transform:none"')
    vf = '<div class="vtile"><img src="assets/img/qr.svg" alt=""></div>'
    ph = phone("u5-ph", vf, "Scanner le QR code<br>de la carte", True, "check", "Carte valide", "Identité vérifiée", "left:305px;top:360px")
    body = f"""    <div id="u5-rows" data-layout-ignore>{rows}</div>
    <div id="u5-world">
      <div id="u5-ring"></div>
      <div id="u5-node">{ICON['db']}</div>
      <div id="u5-lbl"><b>BASE NATIONALE</b><span>Ministère de l'ESURSI · temps réel</span></div>
      <div id="u5-stage"><div class="card" id="u5-card">{back}</div></div>
      <svg id="u5-lines" viewBox="0 0 1080 1920">{base}{flow}</svg>
    </div>
    {ph}
    <div id="u5-24"><b>24h</b><span>sur 24</span></div>
    <div id="u5-flood"></div>"""
    js = SHAKE_JS + r"""
      [0, 1, 2, 3].forEach((k) => {
        const from = k % 2 ? -300 : 0, dir = k % 2 ? 1 : -1;
        tl.fromTo("#u5-row" + k, { x: from }, { x: from + dir * 110, duration: 7.4, ease: "none" }, 0);
      });
      tl.set("#u5-ph", { y: 1700 }, 0);
      tl.fromTo("#u5-card", { opacity: 0, scale: 0.8, y: 80 }, { opacity: 1, scale: 1, y: 0, duration: 0.55, ease: "expo.out" }, 0.02);
      tl.to("#u5-card", { scale: 1.4, x: -315, y: 140, duration: 0.7, ease: "power2.inOut" }, 1.08);
      tl.fromTo("#u5-node", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)", immediateRender: false }, 2.28);
      tl.fromTo("#u5-lbl", { opacity: 0, filter: "blur(8px)", x: -14 }, { opacity: 1, filter: "blur(0px)", x: 0, duration: 0.25, ease: "power3.out", immediateRender: false }, 2.4);
      [0, 1, 2].forEach((i) => {
        tl.to("#u5-pb" + i, { attr: { "stroke-dashoffset": 0 }, duration: 0.5, ease: "power2.out" }, 2.3 + i * 0.06);
        tl.to("#u5-pf" + i, { attr: { opacity: 1 }, duration: 0.2 }, 2.7 + i * 0.06);
        tl.fromTo("#u5-pf" + i, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -110 }, duration: 1.5, ease: "none", immediateRender: false }, 2.7);
      });
      tl.fromTo("#u5-ring", { opacity: 1, scale: 1 }, { opacity: 0, scale: 1.8, duration: 0.6, ease: "power2.out", immediateRender: false }, 3.04);
      // verified anywhere
      tl.to("#u5-world", { scale: 0.84, y: -150, opacity: 0.28, filter: "blur(6px)", duration: 0.5, ease: "power3.inOut" }, 3.8);
      tl.to("#u5-ph", { y: 0, duration: 0.6, ease: "expo.out" }, 3.8);
      tl.fromTo("#u5-ph-scan", { y: -90 }, { y: 290, duration: 0.45, ease: "power1.inOut" }, 4.1);
      tl.to("#u5-ph-scan", { opacity: 0, duration: 0.1 }, 4.55);
      tl.to("#u5-ph-vf", { borderColor: "#1E8E4A", duration: 0.12 }, 4.6);
      tl.to("#u5-ph-hint", { opacity: 0, duration: 0.12 }, 4.58);
      tl.fromTo("#u5-ph-ric", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.42, ease: "back.out(2)", immediateRender: false }, 4.6);
      tl.fromTo("#u5-ph-rt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out", immediateRender: false }, 4.7);
      tl.fromTo("#u5-24", { opacity: 0, scale: 0.3, rotation: -40 }, { opacity: 1, scale: 1, rotation: -10, duration: 0.5, ease: "back.out(1.8)", immediateRender: false }, 5.32);
      // the screen becomes the dashboard
      tl.to("#u5-24", { opacity: 0, scale: 0.8, duration: 0.15 }, 6.8);
      tl.set("#u5-flood", { opacity: 1 }, 6.88);
      tl.fromTo("#u5-flood", { clipPath: "inset(376px 321px 636px 321px round 54px)" }, { clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 0.42, ease: "power3.in", immediateRender: false }, 6.88);
"""
    return scene("u5", U5_CSS, body, js)


# ======================================================== U6  dashboard  (43.0 – 45.3, local = abs - 43.0)
U6_CSS = r"""
    #root { background: #FFFFFF; }
    #u6-h { position: absolute; left: 80px; top: 200px; }
    #u6-h b { display: block; font: 900 58px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.01em; }
    #u6-h span { display: block; margin-top: 14px; font: 600 30px/1 'Open Sans', sans-serif; color: #4A5A70; }
    .u6-t { position: absolute; width: 450px; height: 210px; border-radius: 26px; background: #F4F7FB; border: 2px solid #E3EAF3; overflow: hidden; opacity: 0; }
    .u6-t i { position: absolute; left: 0; top: 0; bottom: 0; width: 10px; }
    .u6-t span { position: absolute; left: 34px; top: 30px; font: 700 28px/1 'Open Sans', sans-serif; color: #4A5A70; }
    .u6-t b { position: absolute; left: 32px; top: 86px; font: 900 76px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; }
    .u6-bar { position: absolute; left: 34px; right: 34px; bottom: 28px; height: 12px; border-radius: 6px; background: #DCE3EC; overflow: hidden; }
    .u6-bar u { position: absolute; inset: 0; border-radius: 6px; transform-origin: 0 50%; }
"""

TILES = [("Étudiants (total)", 1250, "", "#1957B8"), ("Cartes générées", 1250, "", "#2F86E0"),
         ("Étudiants avec photo", 1238, "", "#1E8E4A"), ("Cartes distribuées", 980, "", "#FCD116"),
         ("Couverture photos", 99, " %", "#1E8E4A"), ("Progression cartes", 100, " %", "#D21034")]


def u6():
    tiles = []
    for k, (lab, v, unit, col) in enumerate(TILES):
        x = 80 + (k % 2) * 470
        y = 340 + (k // 2) * 230
        bar = f'<div class="u6-bar"><u id="u6-u{k}" style="background:{col}"></u></div>' if unit else ""
        tiles.append(f'<div class="u6-t" id="u6-t{k}" style="left:{x}px;top:{y}px"><i style="background:{col}"></i><span>{lab}</span>'
                     f'<b id="u6-v{k}">0{unit}</b>{bar}</div>')
    body = f"""    <div id="u6-h"><b>Tableau de bord</b><span>Cockpit de pilotage académique</span></div>
    {''.join(tiles)}"""
    vals = [(v, unit) for (_, v, unit, _) in TILES]
    js = "      const VALS = %s;\n" % [[v, u] for v, u in vals] + r"""
      tl.fromTo("#u6-h", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0.02);
      VALS.forEach(([v, unit], k) => {
        const t = 0.12 + k * 0.06;
        tl.fromTo("#u6-t" + k, { opacity: 0, y: 40, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "expo.out" }, t);
        const o = { n: 0 };
        tl.to(o, { n: v, duration: 0.9, ease: "power2.out", onUpdate: () => {
          const n = Math.round(o.n);
          document.querySelector("#u6-v" + k).textContent = (n >= 1000 ? Math.floor(n / 1000) + " " + String(n % 1000).padStart(3, "0") : String(n)) + unit;
        } }, t + 0.1);
        if (unit) tl.fromTo("#u6-u" + k, { scaleX: 0 }, { scaleX: v / 100, duration: 0.9, ease: "power2.out" }, t + 0.1);
      });
"""
    return scene("u6", U6_CSS, body, js)
