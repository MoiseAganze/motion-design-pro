from parts import ICON, CARD_CSS, card_front, card_back, scene
from scenes_a import S3_CSS, rows_html

# ---------------------------------------------------------------- S4 QR + SCAN
S4_CSS = r"""
    #root { background: #0B2C5A; }
    .s3-rowtxt { position: absolute; left: 0; white-space: nowrap; font: 900 190px/1 Montserrat, sans-serif; color: transparent;
      -webkit-text-stroke: 2px rgba(255,255,255,.11); letter-spacing: -0.01em; }
    #s4-world { position: absolute; inset: 0; }
    #s4-stage { position: absolute; inset: 0; perspective: 2400px; }
    #s4-card { left: 110px; top: 360px; }
    #s4-lines { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
    #s4-node { position: absolute; left: 110px; top: 196px; width: 170px; height: 170px; border-radius: 50%; background: #fff; color: #0B2C5A; }
    #s4-node svg { position: absolute; inset: 38px; width: 94px; height: 94px; }
    #s4-ring { position: absolute; left: 110px; top: 196px; width: 170px; height: 170px; border-radius: 50%; border: 6px solid #FCD116; opacity: 0; }
    #s4-lbl { position: absolute; left: 312px; top: 222px; }
    #s4-lbl b { display: block; font: 900 50px/1 Montserrat, sans-serif; color: #fff; letter-spacing: -0.01em; }
    #s4-lbl span { display: block; margin-top: 14px; font: 600 29px/1 'Open Sans', sans-serif; color: #A9C8F2; }
    #s4-phone { position: absolute; left: 305px; top: 360px; width: 470px; height: 940px; border-radius: 70px; background: #E8EEF7; padding: 16px;
      box-shadow: 0 40px 80px rgba(0,0,0,.35); }
    #s4-screen { position: absolute; inset: 16px; border-radius: 54px; background: #fff; overflow: hidden; }
    #s4-notch { position: absolute; left: 50%; top: 16px; width: 130px; height: 30px; margin-left: -65px; border-radius: 15px; background: #0B2C5A; }
    #s4-sh { position: absolute; left: 0; right: 0; top: 0; height: 130px; background: linear-gradient(100deg,#1957B8,#2F86E0);
      color: #fff; font: 800 38px/1 Montserrat, sans-serif; text-align: center; padding-top: 66px; }
    #s4-vf { position: absolute; left: 34px; top: 160px; width: 370px; height: 370px; border-radius: 26px; background: #14263F; overflow: hidden;
      border: 6px solid #14263F; }
    #s4-vftile { position: absolute; left: 50px; top: 50px; width: 258px; height: 258px; background: #fff; border-radius: 14px; padding: 16px; }
    #s4-vftile img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
    .s4-cn { position: absolute; width: 54px; height: 54px; border-color: #FCD116; border-style: solid; border-width: 0; }
    #s4-scan { position: absolute; left: 14px; right: 14px; top: 0; height: 90px;
      background: linear-gradient(to bottom, rgba(59,227,138,0), rgba(59,227,138,.35)); border-bottom: 5px solid #3BE38A; }
    #s4-hint { position: absolute; left: 30px; right: 30px; top: 566px; text-align: center; font: 600 27px/1.3 'Open Sans', sans-serif; color: #4A5A70; }
    #s4-ok { position: absolute; left: 159px; top: 562px; width: 120px; height: 120px; border-radius: 50%; background: #1E8E4A; color: #fff; opacity: 0; }
    #s4-ok svg { position: absolute; inset: 20px; width: 80px; height: 80px; }
    #s4-okt { position: absolute; left: 0; right: 0; top: 708px; text-align: center; opacity: 0; }
    #s4-okt b { display: block; font: 800 48px/1 Montserrat, sans-serif; color: #1E8E4A; }
    #s4-okt span { display: block; margin-top: 14px; font: 600 29px/1 'Open Sans', sans-serif; color: #4A5A70; }
    #s4-flood { position: absolute; inset: 0; background: #fff; clip-path: inset(376px 321px 636px 321px round 54px); opacity: 0; }
""" + CARD_CSS


def s4():
    corners = (
        '<div class="s4-cn" style="left:18px;top:18px;border-left-width:7px;border-top-width:7px;border-top-left-radius:16px"></div>'
        '<div class="s4-cn" style="right:18px;top:18px;border-right-width:7px;border-top-width:7px;border-top-right-radius:16px"></div>'
        '<div class="s4-cn" style="left:18px;bottom:18px;border-left-width:7px;border-bottom-width:7px;border-bottom-left-radius:16px"></div>'
        '<div class="s4-cn" style="right:18px;bottom:18px;border-right-width:7px;border-bottom-width:7px;border-bottom-right-radius:16px"></div>'
    )
    paths = [
        "M 470 600 C 470 470, 196 500, 196 370",
        "M 540 600 C 540 450, 240 480, 232 366",
        "M 610 600 C 610 430, 290 460, 266 358",
    ]
    base = "".join(f'<path id="s4-pb{i}" d="{d}" pathLength="1" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="5" stroke-dasharray="1 1" stroke-dashoffset="1"/>' for i, d in enumerate(paths))
    flow = "".join(f'<path id="s4-pf{i}" d="{d}" pathLength="100" fill="none" stroke="#FCD116" stroke-width="7" stroke-linecap="round" stroke-dasharray="2 10" opacity="0"/>' for i, d in enumerate(paths))
    body = f"""    <div id="s4-rows" data-layout-ignore>{rows_html('s4')}</div>
    <div id="s4-world">
      <div id="s4-ring"></div>
      <div id="s4-node">{ICON['db']}</div>
      <div id="s4-lbl"><b>BASE NATIONALE</b><span>Ministère de l'ESURSI · temps réel</span></div>
      <div id="s4-stage">
        <div class="card" id="s4-card">
{card_front('s4c')}
{card_back('s4c')}
        </div>
      </div>
      <svg id="s4-lines" viewBox="0 0 1080 1920">{base}{flow}</svg>
    </div>
    <div id="s4-phone">
      <div id="s4-screen">
        <div id="s4-sh">Vérification</div>
        <div id="s4-notch"></div>
        <div id="s4-vf"><div id="s4-vftile"><img src="assets/img/qr.svg" alt=""></div>{corners}<div id="s4-scan"></div></div>
        <div id="s4-hint">Scanner le QR code<br>de la carte</div>
        <div id="s4-ok">{ICON['check']}</div>
        <div id="s4-okt"><b>Carte valide</b><span>Identité vérifiée</span></div>
      </div>
    </div>
    <div id="s4-flood"></div>"""
    js = r"""
      // background type continues from s3 (same speed, 15 px/s)
      [0, 1, 2, 3].forEach((k) => {
        const from = k % 2 ? -340 : -60, dir = k % 2 ? 1 : -1;
        tl.fromTo("#s4-row" + k, { x: from }, { x: from + dir * 87, duration: 5.8, ease: "none" }, 0);
      });
      tl.set(["#s4-node", "#s4-lbl"], { opacity: 0 }, 0);
      tl.set("#s4-phone", { y: 1700 }, 0);
      // flip to the back on "QR"
      tl.fromTo("#s4-card", { rotationY: 0, scale: 1, x: 0, y: 0 }, { rotationY: 180, duration: 0.72, ease: "power3.inOut" }, 0.19);
      tl.to("#s4-card", { keyframes: [{ scale: 0.9, duration: 0.36, ease: "power2.out" }, { scale: 1, duration: 0.36, ease: "power2.in" }] }, 0.19);
      // push onto the QR code
      tl.to("#s4-card", { scale: 1.4, x: -315, y: 140, duration: 0.7, ease: "power2.inOut" }, 0.88);
      // linked to the national database
      tl.fromTo("#s4-node", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 1.39);
      tl.fromTo("#s4-lbl", { opacity: 0, filter: "blur(8px)", x: -14 }, { opacity: 1, filter: "blur(0px)", x: 0, duration: 0.25, ease: "power3.out" }, 1.52);
      [0, 1, 2].forEach((i) => {
        tl.to("#s4-pb" + i, { attr: { "stroke-dashoffset": 0 }, duration: 0.55, ease: "power2.out" }, 1.4 + i * 0.06);
        tl.to("#s4-pf" + i, { attr: { opacity: 1 }, duration: 0.2 }, 1.8 + i * 0.06);
        tl.fromTo("#s4-pf" + i, { attr: { "stroke-dashoffset": 0 } }, { attr: { "stroke-dashoffset": -140 }, duration: 1.9, ease: "none" }, 1.8);
      });
      tl.fromTo("#s4-ring", { opacity: 1, scale: 1 }, { opacity: 0, scale: 1.8, duration: 0.6, ease: "power2.out", immediateRender: false }, 2.11);
      // the world steps back, the phone rises
      tl.to("#s4-world", { scale: 0.84, y: -150, opacity: 0.28, filter: "blur(6px)", duration: 0.5, ease: "power3.inOut" }, 2.72);
      tl.to("#s4-phone", { y: 0, duration: 0.6, ease: "expo.out" }, 2.72);
      // scanning passes
      tl.fromTo("#s4-scan", { y: -90 }, { y: 290, duration: 0.55, ease: "power1.inOut" }, 3.05);
      tl.to("#s4-scan", { y: -60, duration: 0.5, ease: "power1.inOut" }, 3.6);
      tl.to("#s4-scan", { y: 290, duration: 0.5, ease: "power1.inOut" }, 4.1);
      // verified on "vérifiée"
      tl.to("#s4-scan", { opacity: 0, duration: 0.12 }, 4.68);
      tl.to("#s4-vf", { borderColor: "#1E8E4A", duration: 0.15 }, 4.7);
      tl.to("#s4-hint", { opacity: 0, filter: "blur(6px)", duration: 0.15 }, 4.66);
      tl.fromTo("#s4-ok", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 4.7);
      tl.fromTo("#s4-okt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 4.82);
      // the white screen becomes the next world
      tl.set("#s4-flood", { opacity: 1 }, 5.35);
      tl.fromTo("#s4-flood", { clipPath: "inset(376px 321px 636px 321px round 54px)" }, { clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 0.42, ease: "power3.in" }, 5.35);
"""
    return scene("s4", S4_CSS, body, js)


# ---------------------------------------------------------------- S5 26 PROVINCES
PROVINCES = ["Kinshasa", "Kongo-Central", "Kwango", "Kwilu", "Mai-Ndombe", "Équateur", "Sud-Ubangi", "Nord-Ubangi", "Mongala",
             "Tshuapa", "Tshopo", "Bas-Uele", "Haut-Uele", "Ituri", "Nord-Kivu", "Sud-Kivu", "Maniema", "Lomami", "Sankuru",
             "Kasaï", "Kasaï-Central", "Kasaï-Oriental", "Lualaba", "Haut-Lomami", "Haut-Katanga", "Tanganyika"]

S5_CSS = r"""
    #root { background: #FFFFFF; }
    .s5-h { position: absolute; left: 90px; top: 196px; font: 900 84px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; }
    #s5-grid { position: absolute; inset: 0; perspective: 1400px; }
    .s5-mini { opacity: 0; position: absolute; width: 200px; height: 126px; border-radius: 12px; background: #fff; overflow: hidden;
      box-shadow: 0 10px 22px rgba(11,44,90,.16), 0 1px 3px rgba(11,44,90,.12); }
    .s5-mini .mh { position: absolute; left: 0; right: 0; top: 0; height: 44px; background: linear-gradient(100deg,#1957B8,#2F86E0);
      color: #fff; font: 800 18px/44px Montserrat, sans-serif; text-align: center; letter-spacing: .01em; white-space: nowrap; }
    .s5-mini .mp { position: absolute; left: 12px; top: 54px; width: 40px; height: 52px; border-radius: 5px; background: #DDE6F2; }
    .s5-mini .mb { position: absolute; left: 64px; height: 8px; border-radius: 4px; background: #DCE3EC; }
    .s5-mini .mt { position: absolute; left: 0; right: 0; bottom: 0; height: 6px;
      background: linear-gradient(90deg,#2F86E0 0 33.33%,#FCD116 33.33% 66.66%,#D21034 66.66%); }
    #s5-stage { position: absolute; inset: 0; perspective: 2400px; }
    #s5-hero { left: 110px; top: 420px; }
    #s5-panel { position: absolute; left: 160px; top: 560px; width: 760px; height: 470px; border-radius: 44px; background: #0B2C5A;
      box-shadow: 0 40px 80px rgba(11,44,90,.35); text-align: center; opacity: 0; }
    #s5-num { display: block; margin-top: 40px; font: 900 290px/1 Montserrat, sans-serif; color: #FCD116; letter-spacing: -0.03em; }
    #s5-prov { display: block; margin-top: 4px; font: 900 64px/1 Montserrat, sans-serif; color: #fff; letter-spacing: .08em; }
    #s5-norm { position: absolute; left: 0; right: 0; top: 600px; text-align: center; }
    #s5-n1 { display: block; font: 900 80px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.01em; opacity: 0; }
    #s5-n2wrap { position: relative; display: inline-block; margin-top: 30px; }
    #s5-mk { position: absolute; left: -24px; right: -24px; bottom: 6px; height: 58%; background: #FCD116; transform-origin: 0 50%; border-radius: 6px; }
    #s5-n2 { position: relative; display: block; font: 900 146px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.03em; opacity: 0; }
    #s5-h2 { opacity: 0; }
    #s5-veil { position: absolute; inset: 0; background: rgba(255,255,255,.78); opacity: 0; }
""" + CARD_CSS


def s5():
    # 4 x 7 grid, last row of 2 centred
    slots = []
    for r in range(6):
        for c in range(4):
            slots.append((116 + c * 216, 340 + r * 142))
    slots.append((332, 340 + 6 * 142))
    slots.append((548, 340 + 6 * 142))
    hero_slot = 13  # row 3, col 1
    order = list(range(26))
    order.remove(hero_slot)
    names = PROVINCES[1:]
    assign = {hero_slot: PROVINCES[0]}
    for i, s in enumerate(order):
        assign[s] = names[i]
    minis = []
    for s in range(26):
        x, y = slots[s]
        minis.append(
            f'<div class="s5-mini" id="s5-m{s}" style="left:{x}px;top:{y}px"><div class="mh">{assign[s].upper()}</div>'
            f'<div class="mp"></div><div class="mb" style="top:60px;width:110px"></div><div class="mb" style="top:78px;width:84px"></div>'
            f'<div class="mb" style="top:96px;width:96px"></div><div class="mt"></div></div>')
    hx, hy = slots[hero_slot]
    # appearance order by distance from the hero slot
    dist = sorted(order, key=lambda s: ((slots[s][0] - hx) ** 2 + (slots[s][1] - hy) ** 2, s))
    body = f"""    <div class="s5-h" id="s5-h1">UNE SEULE CARTE.</div>
    <div class="s5-h" id="s5-h2">UN SEUL STANDARD.</div>
    <div id="s5-grid" data-layout-ignore>
      {''.join(minis)}
    </div>
    <div id="s5-stage">
      <div class="card" id="s5-hero">
{card_front('s5c')}
      </div>
    </div>
    <div id="s5-veil"></div>
    <div id="s5-panel"><span id="s5-num">1</span><span id="s5-prov">PROVINCES</span></div>
    <div id="s5-norm"><span id="s5-n1">C'EST MAINTENANT</span><div id="s5-n2wrap"><div id="s5-mk"></div><span id="s5-n2">LA NORME.</span></div></div>"""
    js = """
      const ORDER = %s, HERO = %d, HX = %d, HY = %d;
""" % (dist, hero_slot, hx - 110, hy - 420) + r"""
            tl.set("#s5-mk", { scaleX: 0 }, 0);
            tl.fromTo("#s5-h1", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power3.out" }, 0.02);
      tl.fromTo("#s5-hero", { transformOrigin: "0% 0%", scale: 0.84, x: 69, y: 43, rotationX: 28, opacity: 0 },
        { scale: 1, x: 0, y: 0, rotationX: 0, opacity: 1, duration: 0.6, ease: "expo.out" }, 0.02);
      // "un seul standard": the card drops into its slot, the country fills in around it
      tl.to("#s5-h1", { opacity: 0, filter: "blur(8px)", duration: 0.14, ease: "power2.in" }, 0.8);
      tl.fromTo("#s5-h2", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power3.out" }, 0.86);
      tl.to("#s5-hero", { scale: 200 / 860, x: HX, y: HY, duration: 0.5, ease: "power3.inOut" }, 0.84);
      tl.set("#s5-m" + HERO, { opacity: 1 }, 1.33);
      tl.set("#s5-hero", { opacity: 0 }, 1.34);
      ORDER.forEach((s, i) => {
        tl.fromTo("#s5-m" + s, { opacity: 0, rotationX: -85, y: 24 }, { opacity: 1, rotationX: 0, y: 0, duration: 0.36, ease: "power3.out" }, 1.0 + i * 0.034);
      });
      // 26 provinces
      tl.to("#s5-h2", { opacity: 0, filter: "blur(8px)", duration: 0.15, ease: "power2.in" }, 1.85);
      tl.to("#s5-veil", { opacity: 1, duration: 0.3, ease: "power2.out" }, 1.9);
      tl.fromTo("#s5-panel", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.5)" }, 1.85);
      const cnt = { v: 1 };
      tl.to(cnt, { v: 26, duration: 0.38, ease: "power2.out",
        onUpdate: () => { document.querySelector("#s5-num").textContent = String(Math.round(cnt.v)); } }, 1.9);
      // c'est maintenant la norme
      tl.to("#s5-panel", { opacity: 0, scale: 0.92, filter: "blur(8px)", duration: 0.16, ease: "power2.in" }, 3.0);
      tl.fromTo("#s5-n1", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power3.out" }, 3.13);
      tl.fromTo("#s5-n2", { opacity: 0, scale: 1.15, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, 3.56);
      tl.to("#s5-mk", { scaleX: 1, duration: 0.35, ease: "power3.out" }, 3.76);
"""
    return scene("s5", S5_CSS, body, js)
