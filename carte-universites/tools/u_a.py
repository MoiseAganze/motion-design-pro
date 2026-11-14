from u_parts import ICON, CARD_CSS, card_front, scene, PHONE_CSS, phone, wipe, SHAKE_JS, BLURIN

# ======================================================== U1  HOOK : the scan that fails  (0 – 7.85)
U1_CSS = r"""
    #root { background: #F4F7FB; }
    #u1-t { position: absolute; left: 90px; right: 90px; top: 196px; }
    #u1-t b { display: block; font: 900 96px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; }
    #u1-t span { display: block; margin-top: 12px; font: 900 64px/1.05 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; }
    #u1-t span em { font-style: normal; color: #1957B8; }
    .ucard { position: absolute; left: 32px; top: 78px; width: 296px; height: 190px; border-radius: 14px; background: #FBF7EF; overflow: hidden;
      box-shadow: 0 10px 20px rgba(0,0,0,.35); }
    .ucard .uh { position: absolute; left: 0; right: 0; top: 0; height: 48px; background: #7B2D3B; color: #F5E6C8;
      font: 800 16px/48px Montserrat, sans-serif; text-align: center; letter-spacing: .04em; }
    .ucard .up { position: absolute; left: 14px; top: 60px; width: 62px; height: 80px; border-radius: 6px; background: #CFC6B4; }
    .ucard .ul { position: absolute; left: 90px; height: 9px; border-radius: 4px; background: #D9CFBC; }
    .ucard .ub { position: absolute; left: 90px; right: 14px; bottom: 14px; height: 34px;
      background: repeating-linear-gradient(90deg,#2B2B2B 0 3px,transparent 3px 6px,#2B2B2B 6px 8px,transparent 8px 12px,#2B2B2B 12px 16px,transparent 16px 18px); }
    #u1-base { position: absolute; left: 70px; top: 230px; width: 940px; height: 600px; border-radius: 34px; background: #fff; overflow: hidden; opacity: 0;
      box-shadow: 0 30px 60px rgba(11,44,90,.16), 0 4px 12px rgba(11,44,90,.08); }
    #u1-bh { position: absolute; left: 0; right: 0; top: 0; height: 120px; background: #0B2C5A; }
    #u1-bh i { position: absolute; left: 30px; top: 24px; width: 72px; height: 72px; border-radius: 50%; background: #fff; color: #0B2C5A; }
    #u1-bh i svg { position: absolute; inset: 15px; width: 42px; height: 42px; }
    #u1-bh b { position: absolute; left: 124px; top: 30px; font: 900 44px/1 Montserrat, sans-serif; color: #fff; }
    #u1-bh span { position: absolute; left: 126px; top: 80px; font: 600 22px/1 'Open Sans', sans-serif; color: #A9C8F2; }
    .u1-row { position: absolute; left: 30px; right: 30px; height: 96px; border-radius: 18px; background: #F4F7FB; }
    .u1-row .ico { position: absolute; left: 20px; top: 18px; width: 60px; height: 60px; border-radius: 50%; background: #E3EAF3; color: #0B2C5A; }
    .u1-row .ico svg { position: absolute; inset: 14px; width: 32px; height: 32px; }
    .u1-row .bar { position: absolute; left: 104px; top: 40px; height: 16px; border-radius: 8px; background: #CBD5E2; }
    .u1-row .ok { position: absolute; right: 20px; top: 25px; height: 46px; padding: 0 20px 0 14px; border-radius: 23px; background: #E3F4EA; color: #1E8E4A;
      font: 800 24px/46px 'Open Sans', sans-serif; display: flex; align-items: center; gap: 6px; }
    .u1-row .ok svg { width: 26px; height: 26px; }
    #u1-me { background: #FDE8EB; border: 4px dashed #D21034; }
    #u1-me b { position: absolute; left: 104px; top: 28px; font: 900 34px/1 Montserrat, sans-serif; color: #D21034; }
    #u1-me .no { position: absolute; right: 20px; top: 23px; height: 48px; padding: 0 22px; border-radius: 24px; background: #D21034; color: #fff;
      font: 900 24px/48px Montserrat, sans-serif; opacity: 0; }
    #u1-stu { position: absolute; left: 0; right: 0; top: 880px; display: flex; justify-content: center; gap: 22px; }
    .u1-s { position: relative; width: 120px; height: 120px; border-radius: 50%; border: 5px dashed #9AA8BA; opacity: 0; }
    .u1-s i { position: absolute; inset: -5px; border-radius: 50%; background: #0B2C5A; color: #fff; }
    .u1-s i svg { position: absolute; inset: 26px; width: 68px; height: 68px; }
""" + PHONE_CSS


def u1():
    vf = ('<div class="ucard" id="u1-card"><div class="uh">VOTRE UNIVERSITÉ</div><div class="up"></div>'
          '<div class="ul" style="top:64px;width:150px"></div><div class="ul" style="top:84px;width:120px"></div>'
          '<div class="ul" style="top:104px;width:170px"></div><div class="ub"></div></div>')
    ph = phone("u1-ph", vf, "Vérification…", False, "x", "ÉTABLISSEMENT<br>INTROUVABLE", "Aucune correspondance<br>dans la base nationale",
               "left:305px;top:500px")
    rows = []
    for k, w in [(0, 430), (1, 360), (3, 470)]:
        rows.append(f'<div class="u1-row" id="u1-r{k}" style="top:{144 + k * 108}px"><div class="ico">{ICON["bank"]}</div>'
                    f'<div class="bar" style="width:{w}px"></div><div class="ok">{ICON["check"]}Inscrit</div></div>')
    rows.append(f'<div class="u1-row" id="u1-me" style="top:{144 + 2 * 108}px"><div class="ico" style="background:#F7C9D1;color:#D21034">{ICON["bank"]}</div>'
                f'<b>VOTRE ÉTABLISSEMENT</b><div class="no" id="u1-no">ABSENT</div></div>')
    studs = "".join(f'<div class="u1-s" id="u1-s{k}"><i id="u1-si{k}">{ICON["user"]}</i></div>' for k in range(6))
    body = f"""    <div id="u1-t"><b>Scannez la carte</b><span>d'un de vos <em>étudiants.</em></span></div>
    {ph}
    <div id="u1-base">
      <div id="u1-bh"><i>{ICON['db']}</i><b>BASE NATIONALE</b><span>Établissements reconnus par le Ministère</span></div>
      {''.join(rows)}
    </div>
    <div id="u1-stu">{studs}</div>"""
    js = SHAKE_JS + r"""
      // scanning passes (the card is already in the viewfinder at frame 0)
      tl.fromTo("#u1-ph-scan", { y: -90 }, { y: 290, duration: 0.6, ease: "power1.inOut" }, 0.3);
      tl.to("#u1-ph-scan", { y: -60, duration: 0.55, ease: "power1.inOut" }, 0.9);
      tl.to("#u1-ph-scan", { y: 290, duration: 0.55, ease: "power1.inOut" }, 1.45);
      tl.to("#u1-ph-scan", { y: -60, duration: 0.55, ease: "power1.inOut" }, 2.0);
      // "Rien."
      tl.to("#u1-ph-scan", { opacity: 0, duration: 0.1 }, 2.68);
      tl.to("#u1-ph-vf", { borderColor: "#D21034", duration: 0.12 }, 2.72);
      tl.to("#u1-ph-hint", { opacity: 0, duration: 0.12 }, 2.7);
      tl.fromTo("#u1-ph-ric", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }, 2.72);
      tl.fromTo("#u1-ph-rt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 2.8);
      shake("#u1-ph", 2.74, 16);
      // the national base, without you
      tl.to("#u1-t", { opacity: 0, y: -30, filter: "blur(8px)", duration: 0.22, ease: "power3.in" }, 3.3);
      tl.to("#u1-ph", { y: 1650, rotation: 8, duration: 0.45, ease: "power3.in" }, 3.3);
      tl.fromTo("#u1-base", { opacity: 0, y: 70 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }, 3.55);
      ["#u1-r0", "#u1-r1", "#u1-me", "#u1-r3"].forEach((s, i) => {
        tl.fromTo(s, { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 3.65 + i * 0.07);
      });
      tl.fromTo("#u1-no", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.2)" }, 4.28);
      tl.to("#u1-me", { keyframes: [{ x: -14, duration: 0.05 }, { x: 11, duration: 0.06 }, { x: -7, duration: 0.06 }, { x: 0, duration: 0.07 }] }, 4.3);
      // "et vos étudiants non plus": they appear, then fade to empty outlines
      for (let k = 0; k < 6; k++) {
        tl.fromTo("#u1-s" + k, { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, 6.28 + k * 0.05);
        tl.to("#u1-si" + k, { opacity: 0, scale: 0.6, duration: 0.3, ease: "power2.in" }, 6.85 + k * 0.08);
      }
"""
    return scene("u1", U1_CSS, body, js)


# ======================================================== U2  craft cards / credibility  (7.85 – 14.85)
U2_CSS = r"""
    #root { background: #EFE7DA; }
    #u2-pile { position: absolute; inset: 0; }
    .u2-pc { position: absolute; left: 230px; width: 620px; height: 390px; border-radius: 10px; overflow: hidden; box-shadow: 0 24px 50px rgba(60,40,10,.22); }
    #u2-a { top: 640px; background: #E7D6AE; border: 2px solid #CDB98A; }
    #u2-a .t1 { position: absolute; left: 34px; top: 30px; font: 400 26px/1 'Space Mono', monospace; color: #6B5530; }
    #u2-a .t2 { position: absolute; left: 34px; top: 68px; font: 700 40px/1 'Space Mono', monospace; color: #4E3B1C; }
    #u2-a .ph { position: absolute; left: 34px; top: 132px; width: 150px; height: 190px; background: #B9B2A4; filter: blur(1.5px); }
    #u2-a .ln { position: absolute; left: 214px; height: 3px; background: repeating-linear-gradient(90deg,#8B7550 0 6px,transparent 6px 12px); }
    #u2-a .st { position: absolute; right: 40px; bottom: 34px; width: 150px; height: 150px; border-radius: 50%; border: 6px solid #3A59A8;
      opacity: .5; filter: blur(1.4px); }
    #u2-b { top: 480px; background: #EFC4BC; }
    #u2-b .t1 { position: absolute; left: 40px; top: 34px; font: italic 700 52px/1 'Playfair Display', serif; color: #7A2E2E; }
    #u2-b .ln { position: absolute; left: 40px; right: 40px; height: 2px; background: #B97D74; }
    #u2-c { top: 330px; background: #D9E3CF; }
    #u2-c .t1 { position: absolute; left: 36px; top: 34px; font: 400 40px/1 Oswald, sans-serif; color: #5D6B57; letter-spacing: .04em; }
    #u2-c .ln { position: absolute; left: 36px; height: 12px; border-radius: 3px; background: #AAB8A1; }
    #u2-stamp { position: absolute; left: 90px; right: 90px; top: 760px; display: flex; justify-content: center; }
    #u2-stampin { display: block; border: 12px solid #D21034; border-radius: 22px; padding: 18px 34px; color: #D21034; opacity: 0;
      font: 900 90px/1 Montserrat, sans-serif; background: rgba(255,255,255,.72); white-space: nowrap; }
    #u2-cred { position: absolute; left: 0; right: 0; top: 600px; height: 150px; }
    .u2-half { position: absolute; left: 0; right: 0; top: 0; text-align: center; font: 900 116px/150px Montserrat, sans-serif; color: #0B2C5A;
      letter-spacing: -0.03em; opacity: 0; }
    #u2-h1 { clip-path: polygon(0 0,100% 0,100% 40%,78% 56%,61% 38%,44% 63%,27% 44%,12% 60%,0 48%); }
    #u2-h2 { clip-path: polygon(0 48%,12% 60%,27% 44%,44% 63%,61% 38%,78% 56%,100% 40%,100% 100%,0 100%); }
    #u2-crack { position: absolute; left: 0; top: 0; width: 1080px; height: 150px; overflow: visible; }
"""


def u2():
    la = "".join(f'<div class="ln" style="top:{150 + k * 46}px;width:{300 - k * 30}px"></div>' for k in range(4))
    lb = "".join(f'<div class="ln" style="top:{140 + k * 54}px"></div>' for k in range(4))
    lc = "".join(f'<div class="ln" style="top:{120 + k * 50}px;width:{520 - (k % 2) * 140}px"></div>' for k in range(5))
    pts = "0,72 130,90 292,66 475,94 659,57 842,84 1080,60"
    body = f"""    <div id="u2-pile">
      <div class="u2-pc" data-layout-ignore id="u2-c"><div class="t1">ATTESTATION D'INSCRIPTION</div>{lc}</div>
      <div class="u2-pc" data-layout-ignore id="u2-b"><div class="t1">Carte d'étudiant</div>{lb}</div>
      <div class="u2-pc" data-layout-ignore id="u2-a"><div class="t1">UNIVERSITÉ ......</div><div class="t2">CARTE D'ÉTUDIANT</div><div class="ph"></div>{la}<div class="st"></div></div>
      <div id="u2-stamp" data-layout-allow-occlusion data-layout-allow-overlap><span id="u2-stampin">NON VÉRIFIABLE</span></div>
    </div>
    <div id="u2-cred" data-layout-allow-overlap>
      <div class="u2-half" id="u2-h1">CRÉDIBILITÉ</div>
      <div class="u2-half" id="u2-h2">CRÉDIBILITÉ</div>
      <svg id="u2-crack" viewBox="0 0 1080 150"><polyline id="u2-line" points="{pts}" pathLength="1" fill="none" stroke="#D21034" stroke-width="7"
        stroke-linejoin="round" stroke-dasharray="1 1" stroke-dashoffset="1"/></svg>
    </div>"""
    js = SHAKE_JS + r"""
      const land = [["#u2-c", 0.13, 9, -40], ["#u2-b", 0.35, -10, 30], ["#u2-a", 0.57, -4, 0]];
      land.forEach(([sel, t, rot, x]) => {
        tl.fromTo(sel, { y: -1500, x: x, rotation: rot - 30, filter: "blur(18px)" },
          { y: 0, x: x, rotation: rot, filter: "blur(0px)", duration: 0.45, ease: "power4.out" }, t);
      });
      // "formats différents": they spread apart
      tl.to("#u2-c", { x: -150, rotation: 14, duration: 0.5, ease: "power3.out" }, 1.27);
      tl.to("#u2-b", { x: 150, rotation: -14, duration: 0.5, ease: "power3.out" }, 1.33);
      // "vérification" : stamp
      tl.fromTo("#u2-stampin", { opacity: 0, scale: 2.6, rotation: -12 }, { opacity: 0.96, scale: 1, rotation: -12, duration: 0.16, ease: "power3.in" }, 2.55);
      shake("#u2-pile", 2.71, 16);
      // "crédibilité"
      tl.to("#u2-pile", { scale: 0.66, y: -40, opacity: 0.22, filter: "blur(3px)", duration: 0.5, ease: "power3.inOut" }, 4.1);
      tl.fromTo(["#u2-h1", "#u2-h2"], { opacity: 0, scale: 1.12, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.25, ease: "expo.out" }, 4.45);
      // "souffre" : it cracks
      tl.to("#u2-line", { attr: { "stroke-dashoffset": 0 }, duration: 0.14, ease: "power2.out" }, 6.36);
      tl.to("#u2-h1", { x: -22, y: -16, rotation: -3, color: "#D21034", duration: 0.35, ease: "power3.out" }, 6.42);
      tl.to("#u2-h2", { x: 22, y: 18, rotation: 2.5, color: "#D21034", duration: 0.35, ease: "power3.out" }, 6.42);
      shake("#u2-cred", 6.42, 12);
"""
    return scene("u2", U2_CSS, body, js)


# ======================================================== U3  Ministry + ESURSI Connect login  (14.6 – 22.95)
WCSS, WHTML, WJS = wipe("u3")
U3_CSS = WCSS + r"""
    #u3-plate { position: absolute; left: 0; right: 0; top: 228px; display: flex; justify-content: center; }
    #u3-platein { display: flex; align-items: center; gap: 18px; background: #fff; border-radius: 999px; padding: 10px 38px 10px 10px; opacity: 0; }
    #u3-platein img { width: 84px; height: 84px; border-radius: 50%; }
    #u3-platein span { font: 800 32px/1 Montserrat, sans-serif; color: #0B2C5A; white-space: nowrap; }
    #u3-login { position: absolute; left: 110px; top: 380px; width: 860px; height: 740px; border-radius: 36px; background: #fff; opacity: 0;
      box-shadow: 0 40px 80px rgba(0,0,0,.3); }
    #u3-lh img { position: absolute; left: 40px; top: 40px; width: 96px; height: 96px; border-radius: 50%; }
    #u3-lh b { position: absolute; left: 156px; top: 44px; font: 900 52px/1 Montserrat, sans-serif; color: #0B2C5A; }
    #u3-lh span { position: absolute; left: 158px; top: 106px; font: 600 25px/1.2 'Open Sans', sans-serif; color: #4A5A70; }
    .u3-lab { position: absolute; left: 40px; font: 700 26px/1 'Open Sans', sans-serif; color: #0B2C5A; }
    .u3-in { position: absolute; left: 40px; right: 40px; height: 88px; border: 3px solid #D5DEEA; border-radius: 18px; background: #F8FAFD; }
    .u3-in div { position: absolute; left: 26px; top: 24px; font: 700 32px/1.2 Montserrat, sans-serif; color: #0B2C5A; white-space: nowrap; }
    .u3-in i { font-style: normal; opacity: 0; }
    #u3-btn { position: absolute; left: 40px; right: 40px; top: 560px; height: 96px; border-radius: 20px; background: #1957B8; color: #fff;
      font: 800 36px/96px Montserrat, sans-serif; text-align: center; }
    #u3-sec { position: absolute; left: 0; right: 0; top: 680px; text-align: center; font: 600 24px/1 'Open Sans', sans-serif; color: #4A5A70;
      display: flex; justify-content: center; align-items: center; gap: 8px; }
    #u3-sec svg { width: 26px; height: 26px; color: #1E8E4A; }
    #u3-zoom { position: absolute; inset: 0; background: #1957B8; opacity: 0; clip-path: inset(940px 150px 884px 150px round 20px); }
"""


def u3():
    email = "votre-etablissement@esu.ac.cd"
    em = "".join(f'<i id="u3-e{k}">{c}</i>' for k, c in enumerate(email))
    pw = "".join(f'<i id="u3-p{k}">•</i>' for k in range(10))
    body = f"""{WHTML}
    <div id="u3-plate"><div id="u3-platein"><img src="assets/img/seal.png" alt=""><span>MINISTÈRE DE L'ESURSI</span></div></div>
    <div id="u3-login">
      <div id="u3-lh"><img src="assets/img/seal.png" alt=""><b>ESURSI Connect</b><span>Plateforme intégrée des<br>établissements de l'ESU</span></div>
      <div class="u3-lab" style="top:210px">Adresse e-mail</div>
      <div class="u3-in" style="top:250px"><div>{em}</div></div>
      <div class="u3-lab" style="top:380px">Mot de passe</div>
      <div class="u3-in" style="top:420px"><div style="letter-spacing:.12em">{pw}</div></div>
      <div id="u3-btn">Se connecter</div>
      <div id="u3-sec">{ICON['lock']}Sécurisé</div>
    </div>
    <div id="u3-zoom"></div>"""
    js = WJS + r"""
      tl.fromTo("#u3-platein", { opacity: 0, scale: 1.05, y: 420 }, { opacity: 1, scale: 1.5, y: 420, duration: 0.45, ease: "back.out(1.6)" }, 0.52);
      tl.to("#u3-platein", { scale: 1, y: 0, duration: 0.55, ease: "power3.inOut" }, 2.6);
      // ESURSI Connect
      tl.fromTo("#u3-login", { opacity: 0, scale: 0.88, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.6, ease: "expo.out" }, 3.0);
      for (let k = 0; k < 29; k++) tl.set("#u3-e" + k, { opacity: 1 }, 4.25 + k * 0.047);
      for (let k = 0; k < 10; k++) tl.set("#u3-p" + k, { opacity: 1 }, 5.75 + k * 0.05);
      tl.to("#u3-btn", { keyframes: [{ scale: 0.95, duration: 0.08 }, { scale: 1, duration: 0.14 }] }, 6.75);
      tl.to("#u3-btn", { backgroundColor: "#0B2C5A", duration: 0.08 }, 6.75);
      tl.to("#u3-btn", { backgroundColor: "#1957B8", duration: 0.2 }, 6.9);
      // zoom through the button
      tl.to("#u3-platein", { opacity: 0, y: -20, filter: "blur(8px)", duration: 0.2, ease: "power3.in" }, 7.5);
      tl.set("#u3-zoom", { opacity: 1 }, 7.75);
      tl.fromTo("#u3-zoom", { clipPath: "inset(940px 150px 884px 150px round 20px)" }, { clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 0.5, ease: "power3.in" }, 7.75);
"""
    return scene("u3", U3_CSS, body, js)
