from u_parts import ICON, CARD_CSS, card_front, card_back, scene, SHAKE_JS

# ======================================================== U4  portal demo in 3 steps  (22.9 – 35.85, local = abs - 22.9)
U4_CSS = r"""
    #root { background: #F4F7FB; }
    #u4-blue { position: absolute; inset: 0; background: #1957B8; }
    #u4-top { position: absolute; left: 70px; right: 70px; top: 196px; height: 96px; border-radius: 24px; background: #0B2C5A; }
    #u4-top img { position: absolute; left: 18px; top: 14px; width: 68px; height: 68px; border-radius: 50%; }
    #u4-top b { position: absolute; left: 104px; top: 30px; font: 800 34px/1 Montserrat, sans-serif; color: #fff; }
    #u4-top span { position: absolute; right: 30px; top: 35px; font: 600 24px/1 'Open Sans', sans-serif; color: #A9C8F2; }
    #u4-steps { position: absolute; left: 130px; right: 130px; top: 318px; height: 110px; }
    .u4-line { position: absolute; top: 31px; height: 6px; border-radius: 3px; background: #CBD5E2; }
    .u4-fill { position: absolute; inset: 0; border-radius: 3px; background: #1E8E4A; transform-origin: 0 50%; }
    .u4-st { position: absolute; top: 0; width: 200px; margin-left: -100px; text-align: center; }
    .u4-dot { position: relative; width: 68px; height: 68px; margin: 0 auto; border-radius: 50%; background: #fff; border: 4px solid #CBD5E2;
      font: 900 30px/60px Montserrat, sans-serif; color: #7B8BA1; }
    .u4-dot .on, .u4-dot .ok { position: absolute; inset: -4px; border-radius: 50%; opacity: 0; color: #fff; }
    .u4-dot .on { background: #1957B8; }
    .u4-dot .ok { background: #1E8E4A; }
    .u4-dot .ok svg { position: absolute; inset: 14px; width: 40px; height: 40px; }
    .u4-st span { display: block; margin-top: 10px; font: 800 26px/1 Montserrat, sans-serif; color: #0B2C5A; }
    #u4-panel { position: absolute; left: 70px; top: 456px; width: 940px; height: 672px; border-radius: 32px; background: #fff; overflow: hidden;
      box-shadow: 0 30px 60px rgba(11,44,90,.16), 0 4px 12px rgba(11,44,90,.08); }
    .u4-p { position: absolute; inset: 0; }
    #u4-p2, #u4-p3, .u4-doc, .u4-mc { opacity: 0; }
    .u4-p h3 { position: absolute; left: 40px; top: 36px; font: 900 42px/1 Montserrat, sans-serif; color: #0B2C5A; }
    .u4-p .sub { position: absolute; left: 42px; top: 90px; font: 600 26px/1 'Open Sans', sans-serif; color: #4A5A70; }
    #u4-sel { position: absolute; left: 40px; right: 40px; top: 140px; height: 88px; border: 3px solid #D5DEEA; border-radius: 18px; background: #F8FAFD; }
    #u4-sel .a, #u4-sel .b { position: absolute; left: 26px; top: 24px; font: 700 34px/1.2 Montserrat, sans-serif; white-space: nowrap; }
    #u4-sel .a { color: #9AA8BA; }
    #u4-sel .b { color: #0B2C5A; opacity: 0; }
    #u4-sel .b em { font-style: normal; display: inline-block; margin-left: 14px; padding: 4px 16px; border-radius: 16px; background: #E3F4EA; color: #1E8E4A;
      font: 800 24px/1.3 'Open Sans', sans-serif; vertical-align: 4px; }
    .u4-sect { position: absolute; left: 40px; top: 270px; font: 900 36px/1 Montserrat, sans-serif; color: #0B2C5A; }
    .u4-sect span { font: 600 24px/1 'Open Sans', sans-serif; color: #4A5A70; margin-left: 12px; }
    .u4-men { position: absolute; left: 40px; right: 40px; height: 86px; border-radius: 18px; background: #F4F7FB; }
    .u4-men b { position: absolute; left: 30px; top: 24px; font: 700 34px/1.1 'Open Sans', sans-serif; color: #0B2C5A; }
    .u4-tg { position: absolute; right: 28px; top: 18px; width: 96px; height: 50px; border-radius: 25px; background: #CBD5E2; }
    .u4-tg i { position: absolute; left: 5px; top: 5px; width: 40px; height: 40px; border-radius: 50%; background: #fff; box-shadow: 0 2px 6px rgba(0,0,0,.2); }
    #u4-drop { position: absolute; left: 40px; right: 40px; top: 140px; height: 180px; border: 4px dashed #9AB0CC; border-radius: 22px; background: #F8FAFD;
      text-align: center; font: 600 28px/172px 'Open Sans', sans-serif; color: #7B8BA1; }
    .u4-doc { position: absolute; width: 120px; height: 150px; color: #fff; }
    .u4-doc svg { position: absolute; inset: 0; width: 120px; height: 150px; }
    .u4-doc b { position: absolute; left: 0; right: 0; top: 78px; text-align: center; font: 900 26px/1 Montserrat, sans-serif; color: #fff; }
    #u4-cols { position: absolute; left: 40px; right: 40px; top: 344px; display: flex; flex-wrap: wrap; gap: 10px; }
    #u4-cols i { font-style: normal; padding: 8px 14px; border-radius: 10px; background: #E3EAF3; font: 700 22px/1 'JetBrains Mono', monospace; color: #0B2C5A; }
    .u4-tr { position: absolute; left: 40px; right: 40px; height: 42px; opacity: 0; border-radius: 10px; background: #F4F7FB; }
    .u4-tr i { position: absolute; top: 14px; height: 14px; border-radius: 7px; background: #CBD5E2; }
    .u4-tr .dupbg { position: absolute; inset: 0; border-radius: 10px; background: #FFF1B8; border-left: 8px solid #FCD116; opacity: 0; }
    #u4-dup { position: absolute; right: 36px; top: 30px; height: 56px; padding: 0 22px 0 16px; border-radius: 28px; background: #FCD116; color: #0B2C5A;
      font: 800 25px/56px 'Open Sans', sans-serif; display: flex; align-items: center; gap: 8px; opacity: 0; }
    #u4-dup svg { width: 30px; height: 30px; }
    .u4-btn { position: absolute; top: 140px; height: 92px; border-radius: 20px; font: 800 32px/92px Montserrat, sans-serif; text-align: center; white-space: nowrap; }
    #u4-gen { left: 40px; width: 470px; background: #1957B8; color: #fff; }
    #u4-imp { left: 530px; right: 40px; background: #0B2C5A; color: #fff; display: flex; align-items: center; justify-content: center; gap: 12px; opacity: 0; }
    #u4-imp svg { width: 36px; height: 36px; }
    #u4-fan { position: absolute; inset: 0; perspective: 2000px; }
    .u4-mc { position: absolute; left: 110px; top: 676px; }
    #u4-status { position: absolute; right: 36px; top: 30px; height: 56px; padding: 0 24px; border-radius: 28px; background: #E3EAF3; color: #0B2C5A;
      font: 800 26px/56px 'Open Sans', sans-serif; opacity: 0; }
    #u4-status2 { position: absolute; right: 36px; top: 30px; height: 56px; padding: 0 22px 0 16px; border-radius: 28px; background: #1E8E4A; color: #fff;
      font: 800 26px/56px 'Open Sans', sans-serif; display: flex; align-items: center; gap: 8px; opacity: 0; }
    #u4-status2 svg { width: 30px; height: 30px; }
""" + CARD_CSS


def u4():
    steps = [("1", "Structure", 0), ("2", "Import", 50), ("3", "Cartes", 100)]
    st = "".join(
        f'<div class="u4-st" style="left:{x}%"><div class="u4-dot">{n}<div class="on" id="u4-on{k}">{n}</div>'
        f'<div class="ok" id="u4-ok{k}">{ICON["check"]}</div></div><span>{lab}</span></div>'
        for k, (n, lab, x) in enumerate(steps))
    lines = ('<div class="u4-line" style="left:6%;width:38%"><div class="u4-fill" id="u4-l0"></div></div>'
             '<div class="u4-line" style="left:56%;width:38%"><div class="u4-fill" id="u4-l1"></div></div>')
    men = "".join(f'<div class="u4-men" style="top:{336 + k * 100}px"><b>{m}</b><div class="u4-tg" id="u4-tg{k}"><i id="u4-kn{k}"></i></div></div>'
                  for k, m in enumerate(["Sciences", "Droit", "Médecine"]))
    cols = "".join(f"<i>{c}</i>" for c in ["nom", "postnom", "prenom", "sexe", "date_naissance", "lieu_naissance", "nationalite"])
    rows = []
    for k in range(4):
        rows.append(f'<div class="u4-tr" id="u4-tr{k}" style="top:{440 + k * 52}px"><div class="dupbg" id="u4-db{k}"></div>'
                    f'<i style="left:20px;width:{150 + (k * 37) % 60}px"></i><i style="left:250px;width:{120 + (k * 53) % 70}px"></i>'
                    f'<i style="left:470px;width:{90 + (k * 29) % 50}px"></i><i style="left:660px;width:60px"></i></div>')
    fan = "".join(f'<div class="card u4-mc" id="u4-mc{k}">{card_front(f"u4m{k}")}</div>' for k in range(4))
    hero = f'<div class="card u4-mc" id="u4-hero">{card_front("u4h")}{card_back("u4h")}</div>'
    body = f"""    <div id="u4-top"><img src="assets/img/seal.png" alt=""><b>ESURSI Connect</b><span>Espace établissement</span></div>
    <div id="u4-steps">{lines}{st}</div>
    <div id="u4-panel">
      <div class="u4-p" id="u4-p1">
        <h3>Années académiques</h3><div class="sub">Définir l'année active</div>
        <div id="u4-sel"><div class="a" id="u4-sa">-- Choisir --</div><div class="b" id="u4-sb">2026-2027<em>active</em></div></div>
        <div class="u4-sect">Mentions<span>Activer / associer cycles</span></div>
        {men}
      </div>
      <div class="u4-p" id="u4-p2">
        <h3>Import étudiants</h3><div class="sub">CSV / Excel + doublons</div>
        <div id="u4-drop"><span id="u4-droptxt">Glissez votre fichier ici</span></div>
        <div id="u4-cols">{cols}</div>
        {''.join(rows)}
        <div id="u4-dup">{ICON['warn']}2 doublons détectés</div>
      </div>
      <div class="u4-p" id="u4-p3">
        <h3>Génération</h3><div class="sub">Génération groupée, impression et suivi</div>
        <div class="u4-btn" id="u4-gen">Générer les cartes</div>
        <div class="u4-btn" id="u4-imp">{ICON['print']}Imprimer</div>
        <div id="u4-status">Générée</div>
        <div id="u4-status2">{ICON['check']}Imprimée</div>
      </div>
    </div>
    <div class="u4-doc" id="u4-xls" style="left:410px;top:590px">{ICON['file'].replace('currentColor', '#1D7044')}<b>XLSX</b></div>
    <div class="u4-doc" id="u4-csv" style="left:550px;top:600px">{ICON['file'].replace('currentColor', '#1957B8')}<b>CSV</b></div>
    <div id="u4-fan">{fan}{hero}</div>
    <div id="u4-blue"></div>"""
    js = SHAKE_JS + r"""
      tl.fromTo("#u4-blue", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "power2.out" }, 0.02);
            tl.set(["#u4-l0", "#u4-l1"], { scaleX: 0 }, 0);
      tl.set("#u4-on0", { opacity: 1 }, 0);
      // ---- step 1 : year + mentions
      tl.to("#u4-sel", { borderColor: "#1957B8", duration: 0.12 }, 0.8);
      tl.to("#u4-sa", { opacity: 0, duration: 0.1 }, 0.9);
      tl.fromTo("#u4-sb", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 0.92);
      [0, 1, 2].forEach((k) => {
        const t = 1.9 + k * 0.2;
        tl.to("#u4-tg" + k, { backgroundColor: "#1E8E4A", duration: 0.15 }, t);
        tl.to("#u4-kn" + k, { x: 46, duration: 0.25, ease: "back.out(2)" }, t);
      });
      // ---- step 2 : import
      const swap = (out, inn, t) => {
        tl.to(out, { opacity: 0, filter: "blur(8px)", duration: 0.15, ease: "power2.in" }, t);
        tl.fromTo(inn, { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out", immediateRender: false }, t + 0.12);
      };
      swap("#u4-p1", "#u4-p2", 2.82);
      tl.to("#u4-on0", { opacity: 0, duration: 0.1 }, 2.86);
      tl.to("#u4-ok0", { opacity: 1, duration: 0.15 }, 2.86);
      tl.to("#u4-l0", { scaleX: 1, duration: 0.35, ease: "power3.out" }, 2.86);
      tl.to("#u4-on1", { opacity: 1, duration: 0.15 }, 3.1);
      tl.fromTo("#u4-xls", { opacity: 0, x: 420, y: -700, rotation: 25 }, { opacity: 1, x: 0, y: 0, rotation: -6, duration: 0.95, ease: "power3.out", immediateRender: false }, 3.6);
      tl.fromTo("#u4-csv", { opacity: 0, x: 380, y: -620, rotation: -20 }, { opacity: 1, x: 0, y: 0, rotation: 7, duration: 0.6, ease: "power3.out", immediateRender: false }, 4.68);
      tl.to("#u4-drop", { borderColor: "#1E8E4A", backgroundColor: "#EAF7EF", duration: 0.2 }, 4.5);
      tl.to("#u4-droptxt", { opacity: 0, duration: 0.15 }, 4.3);
      tl.to(["#u4-xls", "#u4-csv"], { scale: 0.2, opacity: 0, y: 40, duration: 0.3, ease: "power3.in", stagger: 0.05 }, 5.45);
      for (let k = 0; k < 4; k++) tl.fromTo("#u4-tr" + k, { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.25, ease: "power3.out" }, 5.6 + k * 0.1);
      tl.to(["#u4-db1", "#u4-db3"], { opacity: 1, duration: 0.15 }, 6.27);
      tl.fromTo("#u4-dup", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.38, ease: "back.out(2.2)" }, 6.3);
      tl.to(["#u4-db1", "#u4-db3"], { keyframes: [{ opacity: 0.35, duration: 0.12 }, { opacity: 1, duration: 0.12 }, { opacity: 0.35, duration: 0.12 }, { opacity: 1, duration: 0.12 }] }, 7.58);
      // ---- step 3 : generation
      swap("#u4-p2", "#u4-p3", 8.45);
      tl.to("#u4-on1", { opacity: 0, duration: 0.1 }, 8.5);
      tl.to("#u4-ok1", { opacity: 1, duration: 0.15 }, 8.5);
      tl.to("#u4-l1", { scaleX: 1, duration: 0.35, ease: "power3.out" }, 8.5);
      tl.to("#u4-on2", { opacity: 1, duration: 0.15 }, 8.75);
      tl.to("#u4-gen", { keyframes: [{ scale: 0.96, duration: 0.08 }, { scale: 1, duration: 0.14 }] }, 8.94);
      tl.to("#u4-gen", { backgroundColor: "#0B2C5A", duration: 0.1 }, 8.94);
      tl.fromTo("#u4-status", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, 9.1);
      // cards come out in a fan
      const fan = [[-16, -150, 30], [-6, -55, 10], [6, 55, 10], [16, 150, 30]];
      fan.forEach(([rot, x, y], k) => {
        tl.fromTo("#u4-mc" + k, { opacity: 0, scale: 0.2, x: 0, y: -260, rotation: 0 },
          { opacity: 1, scale: 0.42, x: x, y: y, rotation: rot, duration: 0.5, ease: "back.out(1.4)", immediateRender: false }, 9.05 + k * 0.08);
      });
      tl.fromTo("#u4-imp", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, 9.5);
      tl.to("#u4-imp", { keyframes: [{ scale: 0.95, duration: 0.08 }, { scale: 1, duration: 0.14 }] }, 9.8);
      // recto / verso
      tl.to(".u4-mc:not(#u4-hero)", { opacity: 0.25, filter: "blur(3px)", duration: 0.3 }, 10.6);
      tl.fromTo("#u4-hero", { opacity: 0, scale: 0.42, rotationY: 0, y: 40 }, { opacity: 1, scale: 0.78, y: -30, duration: 0.45, ease: "expo.out", immediateRender: false }, 10.62);
      tl.to("#u4-hero", { rotationY: 180, duration: 0.6, ease: "power3.inOut" }, 11.14);
      tl.to("#u4-status", { opacity: 0, duration: 0.1 }, 11.8);
      tl.fromTo("#u4-status2", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)", immediateRender: false }, 11.82);
"""
    return scene("u4", U4_CSS, body, js)
