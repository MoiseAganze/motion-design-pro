from u_parts import ICON, CARD_CSS, card_front, scene, PHONE_CSS, phone, SHAKE_JS

# ======================================================== U7  accredited / institutional responsibility  (45.2 – 53.25, local = abs - 45.2)
U7_CSS = r"""
    #root { background: #F4F7FB; }
    #u7-a { position: absolute; inset: 0; }
    .u7-l { position: absolute; left: 90px; font: 900 86px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; opacity: 0; }
    #u7-l1 { top: 196px; }
    #u7-l2 { top: 290px; }
    #u7-l3w { position: absolute; left: 90px; top: 384px; }
    #u7-mk { position: absolute; left: -14px; right: -14px; bottom: 4px; height: 56%; background: #FCD116; border-radius: 6px; transform-origin: 0 50%; }
    #u7-l3 { position: relative; display: block; font: 900 86px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; opacity: 0; }
    #u7-stage { position: absolute; inset: 0; perspective: 2400px; }
    .u7-cd { left: 110px; top: 520px; opacity: 0; }
    #u7-stamp { position: absolute; left: 330px; top: 846px; display: flex; align-items: center; gap: 16px; padding: 14px 28px 14px 14px;
      border: 8px solid #0B2C5A; border-radius: 22px; background: rgba(255,255,255,.94); opacity: 0; box-shadow: 0 16px 34px rgba(11,44,90,.25); }
    #u7-stamp img { width: 96px; height: 96px; border-radius: 50%; }
    #u7-stamp b { font: 900 36px/1.05 Montserrat, sans-serif; color: #0B2C5A; white-space: nowrap; }
    #u7-flood { position: absolute; inset: 0; background: #FCD116; clip-path: circle(0px at 640px 920px); }
    #u7-b { position: absolute; inset: 0; }
    #u7-shield { position: absolute; left: 465px; top: 300px; width: 150px; height: 150px; border-radius: 50%; background: #0B2C5A; color: #FCD116; opacity: 0; }
    #u7-shield svg { position: absolute; inset: 32px; width: 86px; height: 86px; }
    .u7-r { position: absolute; left: 0; right: 0; text-align: center; font: 900 74px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; opacity: 0; }
    #u7-r1 { top: 500px; }
    #u7-r2 { top: 590px; }
    #u7-r3 { top: 700px; font-size: 48px; }
    #u7-r4w { position: absolute; left: 0; right: 0; top: 784px; display: flex; justify-content: center; }
    #u7-r4 { display: block; background: #D21034; color: #fff; font: 900 76px/1 Montserrat, sans-serif; padding: 20px 40px 24px; border-radius: 20px;
      letter-spacing: -0.02em; opacity: 0; box-shadow: 0 20px 44px rgba(210,16,52,.3); }
    #u7-r5 { top: 940px; font-size: 72px; }
""" + CARD_CSS


def u7():
    cards = "".join(f'<div class="card u7-cd" id="u7-c{k}">{card_front(f"u7c{k}")}</div>' for k in (1, 2, 0))
    body = f"""    <div id="u7-a">
      <div class="u7-l" id="u7-l1">SEULS LES</div>
      <div class="u7-l" id="u7-l2">ÉTABLISSEMENTS</div>
      <div id="u7-l3w"><div id="u7-mk"></div><span id="u7-l3">AGRÉÉS.</span></div>
      <div id="u7-stage">{cards}</div>
      <div id="u7-stamp"><img src="assets/img/seal.png" alt=""><b>AGRÉÉ PAR LE<br>MINISTÈRE</b></div>
    </div>
    <div id="u7-flood"></div>
    <div id="u7-b">
      <div id="u7-shield">{ICON['shield']}</div>
      <div class="u7-r" id="u7-r1">L'identification</div>
      <div class="u7-r" id="u7-r2">de chaque étudiant</div>
      <div class="u7-r" id="u7-r3">est une</div>
      <div id="u7-r4w"><span id="u7-r4">RESPONSABILITÉ</span></div>
      <div class="u7-r" id="u7-r5">INSTITUTIONNELLE.</div>
    </div>"""
    blur = '{ opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }'
    js = SHAKE_JS + r"""
      tl.set("#u7-mk", { scaleX: 0 }, 0);
      tl.fromTo("#u7-l1", BLUR, 0.06);
      tl.fromTo("#u7-l2", BLUR, 0.3);
      tl.fromTo("#u7-l3", { opacity: 0, scale: 1.15, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, 1.1);
      tl.to("#u7-mk", { scaleX: 1, duration: 0.35, ease: "power3.out" }, 1.25);
      tl.fromTo("#u7-c0", { opacity: 0, y: 260, rotationX: 30 }, { opacity: 1, y: 0, rotationX: 0, duration: 0.7, ease: "expo.out" }, 0.1);
      // stamp on "Ministère"
      tl.fromTo("#u7-stamp", { opacity: 0, scale: 2.4, rotation: -8 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.16, ease: "power3.in" }, 1.6);
      shake("#u7-a", 1.76, 14);
      // "peuvent émettre ces cartes"
      tl.fromTo("#u7-c1", { opacity: 0, x: 0, rotation: 0 }, { opacity: 1, x: -120, y: 40, rotation: -9, duration: 0.5, ease: "power3.out" }, 2.68);
      tl.fromTo("#u7-c2", { opacity: 0, x: 0, rotation: 0 }, { opacity: 1, x: 120, y: 40, rotation: 9, duration: 0.5, ease: "power3.out" }, 2.76);
      // yellow flood from the stamp
      tl.fromTo("#u7-flood", { clipPath: "circle(0px at 640px 920px)" }, { clipPath: "circle(1500px at 640px 920px)", duration: 0.45, ease: "power3.inOut" }, 3.75);
      tl.set("#u7-a", { opacity: 0 }, 4.2);
      tl.fromTo("#u7-shield", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(1.8)" }, 3.95);
      tl.fromTo("#u7-r1", BLUR, 3.87);
      tl.fromTo("#u7-r2", BLUR, 4.88);
      tl.fromTo("#u7-r3", BLUR, 5.68);
      tl.fromTo("#u7-r4", { opacity: 0, scale: 1.9, rotation: -6 }, { opacity: 1, scale: 1, rotation: -2, duration: 0.22, ease: "power4.out" }, 6.12);
      shake("#u7-b", 6.3, 12);
      tl.fromTo("#u7-r5", { opacity: 0, scale: 1.12, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, 6.88);
""".replace("BLUR", blur)
    return scene("u7", U7_CSS, body, js)


# ======================================================== U8  don't wait / take the lead  (53.2 – 56.95, local = abs - 53.2)
U8_CSS = r"""
    #root { background: #0B2C5A; }
    #u8-a { position: absolute; inset: 0; }
    #u8-t1 { position: absolute; left: 0; right: 0; top: 230px; text-align: center; font: 900 92px/1 Montserrat, sans-serif; color: #fff; letter-spacing: -0.02em; opacity: 0; }
    #u8-t2 { position: absolute; left: 0; right: 0; top: 345px; text-align: center; font: 800 56px/1.15 Montserrat, sans-serif; color: #A9C8F2; opacity: 0; }
    #u8-t3 { position: absolute; left: 0; right: 0; top: 415px; text-align: center; font: 800 56px/1.15 Montserrat, sans-serif; color: #fff; opacity: 0; }
    #u8-t3 em { font-style: normal; color: #FCD116; }
    .u8-b { position: absolute; display: flex; align-items: flex-end; gap: 16px; opacity: 0; }
    .u8-b i { flex: none; width: 76px; height: 76px; border-radius: 50%; background: #2F86E0; color: #fff; position: relative; }
    .u8-b i svg { position: absolute; inset: 16px; width: 44px; height: 44px; }
    .u8-b span { display: block; background: #fff; color: #0B2C5A; font: 700 38px/1.2 'Open Sans', sans-serif; padding: 22px 30px; border-radius: 32px;
      white-space: nowrap; box-shadow: 0 16px 34px rgba(0,0,0,.28); }
    #u8-b0 { left: 90px; top: 580px; }
    #u8-b0 span { border-bottom-left-radius: 8px; }
    #u8-b1 { right: 90px; top: 740px; flex-direction: row-reverse; }
    #u8-b1 span { border-bottom-right-radius: 8px; }
    #u8-b2 { left: 90px; top: 900px; }
    #u8-b2 span { border-bottom-left-radius: 8px; }
    #u8-p1 { position: absolute; left: 0; right: 0; top: 560px; text-align: center; font: 900 150px/1 Montserrat, sans-serif; color: #fff; letter-spacing: -0.03em; opacity: 0; }
    #u8-p2w { position: absolute; left: 0; right: 0; top: 740px; display: flex; justify-content: center; }
    #u8-p2 { display: block; background: #FCD116; color: #0B2C5A; font: 900 96px/1 Montserrat, sans-serif; padding: 24px 40px 28px; border-radius: 22px;
      letter-spacing: -0.02em; white-space: nowrap; opacity: 0; box-shadow: 0 24px 50px rgba(0,0,0,.3); }
"""


def u8():
    bubbles = [("Où est ma carte ?", 0), ("Ma carte d'étudiant ?", 1), ("Quand aura-t-on nos cartes ?", 2)]
    bh = "".join(f'<div class="u8-b" id="u8-b{k}"><i>{ICON["user"]}</i><span>{t}</span></div>' for t, k in bubbles)
    body = f"""    <div id="u8-a">
      <div id="u8-t1">N'ATTENDEZ PAS</div>
      <div id="u8-t2">que vos étudiants</div>
      <div id="u8-t3"><em>réclament</em> leurs cartes.</div>
      {bh}
    </div>
    <div id="u8-p1">PRENEZ</div>
    <div id="u8-p2w"><span id="u8-p2">LES DEVANTS !</span></div>"""
    js = SHAKE_JS + r"""
      tl.fromTo("#u8-t1", { opacity: 0, scale: 1.2, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, 0.12);
      tl.fromTo("#u8-t2", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0.86);
      tl.fromTo("#u8-t3", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 1.42);
      [0, 1, 2].forEach((k) => {
        tl.fromTo("#u8-b" + k, { opacity: 0, scale: 0.4, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.35, ease: "back.out(1.8)" }, 1.04 + k * 0.2);
      });
      // prenez les devants
      tl.to("#u8-a", { opacity: 0, scale: 1.12, filter: "blur(12px)", duration: 0.2, ease: "power3.in" }, 2.45);
      tl.fromTo("#u8-p1", { opacity: 0, scale: 1.3, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }, 2.56);
      tl.fromTo("#u8-p2", { opacity: 0, scale: 2, rotation: -10 }, { opacity: 1, scale: 1, rotation: -3, duration: 0.22, ease: "power4.out" }, 3.0);
      shake("#u8-p2w", 3.12, 18);
"""
    return scene("u8", U8_CSS, body, js)


# ======================================================== U9  rescan → recognised, end card  (56.8 – 64.5, local = abs - 56.8)
U9_CSS = r"""
    #u9-flood { position: absolute; inset: 0; background: #FFFFFF; clip-path: circle(0px at 540px 960px); }
    #u9-head { position: absolute; left: 200px; top: 196px; width: 680px; opacity: 0; }
    #u9-tri { position: absolute; left: 90px; top: 450px; width: 900px; height: 12px; display: flex; }
    #u9-tri i { flex: 1; height: 12px; transform-origin: 0 50%; }
    #u9-stage { position: absolute; inset: 0; perspective: 2400px; }
    #u9-card { left: 110px; top: 470px; opacity: 0; }
    #u9-url { position: absolute; left: 0; right: 0; top: 1004px; display: flex; justify-content: center; }
    #u9-urlin { display: flex; align-items: center; gap: 18px; height: 116px; padding: 0 46px 0 34px; border-radius: 58px; background: #0B2C5A;
      box-shadow: 0 24px 50px rgba(11,44,90,.3); opacity: 0; }
    #u9-urlin svg { width: 56px; height: 56px; color: #FCD116; flex: none; }
    #u9-urltxt { font: 800 50px/1 Montserrat, sans-serif; color: #fff; white-space: nowrap; letter-spacing: -0.01em; }
    #u9-urltxt i { font-style: normal; opacity: 0; }
    #u9-band { position: absolute; left: 0; right: 0; top: 1158px; height: 160px; background: #FCD116; clip-path: inset(0px 100% 0px 0px); }
    #u9-bandtxt { position: absolute; left: 90px; right: 90px; top: 30px; font: 800 46px/1.1 Montserrat, sans-serif; color: #0B2C5A; opacity: 0; }
""" + PHONE_CSS + CARD_CSS


def u9():
    url = "carte.minesursi.gouv.cd"
    chars = "".join(f'<i id="u9-u{k}">{c}</i>' for k, c in enumerate(url))
    vf = '<div class="vtile"><img src="assets/img/qr.svg" alt=""></div>'
    ph = phone("u9-ph", vf, "Scanner le QR code<br>de la carte", True, "check", "ÉTABLISSEMENT<br>RECONNU", "Carte valide · base nationale", "left:305px;top:330px")
    body = f"""    <div id="u9-flood"></div>
    {ph}
    <img id="u9-head" src="assets/img/ministere_header.png" alt="Ministère de l'ESURSI">
    <div id="u9-tri"><i id="u9-t0" style="background:#2F86E0"></i><i id="u9-t1" style="background:#FCD116"></i><i id="u9-t2" style="background:#D21034"></i></div>
    <div id="u9-stage"><div class="card" id="u9-card">{card_front('u9c')}</div></div>
    <div id="u9-url"><div id="u9-urlin">{ICON['globe']}<span id="u9-urltxt">{chars}</span></div></div>
    <div id="u9-band"><div id="u9-bandtxt">Un établissement organisé,<br>des étudiants identifiés !</div></div>"""
    js = SHAKE_JS + r"""
      tl.fromTo("#u9-flood", { clipPath: "circle(0px at 540px 960px)" }, { clipPath: "circle(1250px at 540px 960px)", duration: 0.36, ease: "power3.inOut" }, 0);
      tl.set(["#u9-t0", "#u9-t1", "#u9-t2"], { scaleX: 0 }, 0);
      // the same scan as the opening, now it works
      tl.fromTo("#u9-ph", { y: 1700, opacity: 1 }, { y: 0, duration: 0.55, ease: "expo.out" }, 0.08);
      tl.fromTo("#u9-ph-scan", { y: -90 }, { y: 290, duration: 0.5, ease: "power1.inOut" }, 0.5);
      tl.to("#u9-ph-scan", { opacity: 0, duration: 0.1 }, 1.0);
      tl.to("#u9-ph-vf", { borderColor: "#1E8E4A", duration: 0.12 }, 1.05);
      tl.to("#u9-ph-hint", { opacity: 0, duration: 0.12 }, 1.03);
      tl.fromTo("#u9-ph-ric", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.42, ease: "back.out(2)" }, 1.05);
      tl.fromTo("#u9-ph-rt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 1.15);
      tl.to("#u9-ph", { y: 1750, rotation: -6, duration: 0.45, ease: "power3.in" }, 2.2);
      // end card
      tl.fromTo("#u9-head", { opacity: 0, filter: "blur(10px)", y: 14 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.3, ease: "power3.out" }, 2.45);
      ["#u9-t0", "#u9-t1", "#u9-t2"].forEach((s, i) => tl.to(s, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 2.55 + i * 0.08));
      tl.fromTo("#u9-card", { opacity: 0, y: 420, rotationX: 38, rotationY: 0, scale: 0.8 },
        { opacity: 1, y: 0, rotationX: 0, rotationY: -7, scale: 0.8, duration: 0.75, ease: "expo.out" }, 2.45);
      tl.to("#u9-card", { rotationY: 7, duration: 4.4, ease: "sine.inOut" }, 3.2);
      tl.fromTo("#u9-urlin", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, 2.35);
      for (let k = 0; k < 23; k++) tl.set("#u9-u" + k, { opacity: 1 }, 2.48 + k * 0.11);
      tl.fromTo("#u9-band", { clipPath: "inset(0px 100% 0px 0px)" }, { clipPath: "inset(0px 0% 0px 0px)", duration: 0.45, ease: "power3.out" }, 5.2);
      tl.fromTo("#u9-bandtxt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }, 5.35);
"""
    return scene("u9", U9_CSS, body, js)
