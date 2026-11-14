from parts import ICON, CARD_CSS, card_front, card_back, scene

# ---------------------------------------------------------------- S1 HOOK
S1_CSS = r"""
    #s1-ground { position: absolute; inset: 0; background: #F4F7FB; }
    #s1-all, #s1-cam { position: absolute; inset: 0; }
    #s1-tri { position: absolute; left: 90px; top: 196px; display: flex; gap: 0; }
    #s1-tri i { display: block; width: 74px; height: 12px; }
    #s1-title { position: absolute; left: 86px; top: 222px; font: 900 120px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.02em; }
    #s1-sub { position: absolute; left: 92px; top: 372px; font: 700 34px/1 'Open Sans', sans-serif; color: #4A5A70; }
    #s1-sheet { position: absolute; left: 70px; top: 450px; width: 940px; height: 700px; background: #fff; border-radius: 26px;
      box-shadow: 0 30px 60px rgba(11,44,90,.18), 0 4px 12px rgba(11,44,90,.08); }
    #s1-sheet h3 { position: absolute; left: 60px; top: 50px; font: 800 40px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: .01em; }
    #s1-track { position: absolute; left: 60px; right: 170px; top: 128px; height: 18px; border-radius: 9px; background: #E3EAF3; overflow: hidden; }
    #s1-fill { position: absolute; inset: 0; background: #1E8E4A; border-radius: 9px; transform-origin: 0 50%; }
    #s1-pct { position: absolute; right: 60px; top: 116px; font: 800 38px/1 Montserrat, sans-serif; color: #0B2C5A; }
    .s1-row { position: absolute; left: 30px; right: 30px; height: 112px; border-radius: 20px; }
    .s1-rowbg { position: absolute; inset: 0; border-radius: 20px; background: #FDE8EB; border: 3px solid #D21034; opacity: 0; }
    .s1-box { position: absolute; left: 30px; top: 26px; width: 60px; height: 60px; border-radius: 14px; border: 4px solid #0B2C5A; background: #fff; }
    .s1-boxfill { position: absolute; inset: -4px; border-radius: 14px; background: #1E8E4A; color: #fff; opacity: 0; }
    .s1-boxfill svg { position: absolute; inset: 8px; width: 44px; height: 44px; }
    .s1-label { position: absolute; left: 120px; top: 34px; font: 700 38px/1.1 'Open Sans', sans-serif; color: #0B2C5A; white-space: nowrap; }
    #s1-miss { position: absolute; left: 120px; top: 80px; font: 700 24px/1 'Open Sans', sans-serif; color: #D21034; opacity: 0; }
    #s1-badge { position: absolute; right: 30px; top: 22px; width: 68px; height: 68px; border-radius: 50%; background: #D21034; color: #fff; opacity: 0; }
    #s1-badge svg { position: absolute; inset: 8px; width: 52px; height: 52px; }
    #s1-q { position: absolute; left: 610px; top: 150px; font: 900 820px/1 Montserrat, sans-serif; color: #D21034; opacity: 0;
      text-shadow: 0 30px 60px rgba(210,16,52,.25); }
"""

ROWS = ["Relevés de notes", "Travail de fin de cycle", "Frais académiques", "Preuve d'identité étudiante"]


def s1():
    rows = []
    for i, lab in enumerate(ROWS, 1):
        extra = ""
        if i == 4:
            extra = f'<div id="s1-miss">Document manquant</div><div id="s1-badge">{ICON["alert"]}</div>'
        rows.append(f"""        <div class="s1-row" id="s1-r{i}" style="top:{196 + (i - 1) * 120}px">
          <div class="s1-rowbg" id="s1-r{i}bg"></div>
          <div class="s1-box" id="s1-b{i}"><div class="s1-boxfill" id="s1-f{i}">{ICON['check']}</div></div>
          <div class="s1-label" id="s1-l{i}">{lab}</div>{extra}
        </div>""")
    body = f"""    <div id="s1-ground"></div>
    <div id="s1-all">
      <div id="s1-cam">
        <div id="s1-tri"><i style="background:#2F86E0"></i><i style="background:#FCD116"></i><i style="background:#D21034"></i></div>
        <div id="s1-title">FIN DE CYCLE.</div>
        <div id="s1-sub">Ton dossier de diplôme est presque prêt…</div>
        <div id="s1-sheet">
          <h3>DOSSIER DE FIN DE CYCLE</h3>
          <div id="s1-track"><div id="s1-fill"></div></div>
          <div id="s1-pct">0 %</div>
{chr(10).join(rows)}
        </div>
      </div>
      <div id="s1-q" data-layout-allow-occlusion data-layout-allow-overlap>?</div>
    </div>"""
    js = r"""
      tl.set("#s1-fill", { scaleX: 0 }, 0);
      tl.set("#s1-cam", { transformOrigin: "540px 1092px", scale: 1, y: 0 }, 0);
      // subtitle settles in during the first beat (title is already on screen at frame 0)
      tl.fromTo("#s1-sub", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }, 0.25);
      const pct = { v: 0 };
      const ticks = [1.6, 2.0, 2.4];
      ticks.forEach((t, i) => {
        const n = i + 1;
        tl.fromTo("#s1-f" + n, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }, t);
        tl.to("#s1-fill", { scaleX: (n * 0.25), duration: 0.35, ease: "power3.out" }, t);
        tl.to(pct, { v: n * 25, duration: 0.35, ease: "power3.out",
          onUpdate: () => { document.querySelector("#s1-pct").textContent = Math.round(pct.v) + " %"; } }, t);
      });
      // the missing proof, on "PROUVER"
      tl.to("#s1-r4bg", { opacity: 1, duration: 0.2, ease: "power2.out" }, 4.36);
      tl.to("#s1-b4", { borderColor: "#D21034", duration: 0.2 }, 4.36);
      tl.to("#s1-l4", { color: "#D21034", y: -12, duration: 0.25, ease: "power3.out" }, 4.36);
      tl.fromTo("#s1-miss", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }, 4.46);
      tl.fromTo("#s1-badge", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.2)" }, 4.4);
      tl.to("#s1-r4", { keyframes: [{ x: -16, duration: 0.05 }, { x: 13, duration: 0.06 }, { x: -9, duration: 0.06 }, { x: 5, duration: 0.06 }, { x: 0, duration: 0.07 }] }, 4.4);
      // camera pushes onto the missing row
      tl.to("#s1-cam", { scale: 1.32, y: -170, duration: 1.1, ease: "power2.inOut" }, 4.3);
      tl.to(["#s1-title", "#s1-sub", "#s1-tri"], { opacity: 0, filter: "blur(8px)", duration: 0.3, ease: "power2.in" }, 4.3);
      // the giant question mark on "Tu peux le prouver ?"
      tl.fromTo("#s1-q", { opacity: 0, scale: 2.2, rotation: 18, filter: "blur(16px)" },
        { opacity: 1, scale: 1, rotation: -6, filter: "blur(0px)", duration: 0.38, ease: "expo.out" }, 6.48);
      tl.to("#s1-cam", { filter: "blur(3px)", opacity: 0.55, duration: 0.3, ease: "power2.out" }, 6.5);
      // whip out, upward
      tl.to("#s1-all", { y: -1100, filter: "blur(22px)", duration: 0.27, ease: "power3.in" }, 7.28);
"""
    return scene("s1", S1_CSS, body, js)


# ---------------------------------------------------------------- S2 PAPER
S2_CSS = r"""
    #s2-ground { position: absolute; inset: 0; background: #EFE7DA; }
    #s2-cam { position: absolute; inset: 0; }
    .s2-pc { position: absolute; left: 230px; width: 620px; height: 390px; border-radius: 10px; overflow: hidden;
      box-shadow: 0 24px 50px rgba(60,40,10,.22); }
    #s2-a { top: 640px; background: #E7D6AE; border: 2px solid #CDB98A; }
    #s2-a .t1 { position: absolute; left: 34px; top: 30px; font: 400 24px/1 'Space Mono', monospace; color: #6B5530; }
    #s2-a .t2 { position: absolute; left: 34px; top: 66px; font: 700 40px/1 'Space Mono', monospace; color: #4E3B1C; }
    #s2-a .ph { position: absolute; left: 34px; top: 132px; width: 150px; height: 190px; background: #B9B2A4; filter: blur(1.5px); }
    #s2-a .ln { position: absolute; left: 214px; height: 3px; background: repeating-linear-gradient(90deg,#8B7550 0 6px,transparent 6px 12px); }
    #s2-a .st { position: absolute; right: 40px; bottom: 34px; width: 150px; height: 150px; border-radius: 50%; border: 6px solid #3A59A8;
      opacity: .5; filter: blur(1.4px); font: 700 22px/150px 'Space Mono', monospace; color: #3A59A8; text-align: center; }
    #s2-b { top: 480px; background: #EFC4BC; }
    #s2-b .t1 { position: absolute; left: 40px; top: 34px; font: italic 700 52px/1 'Playfair Display', serif; color: #7A2E2E; }
    #s2-b .ln { position: absolute; left: 40px; right: 40px; height: 2px; background: #B97D74; }
    #s2-c { top: 330px; background: #D9E3CF; }
    #s2-c .t1 { position: absolute; left: 36px; top: 34px; font: 400 40px/1 Oswald, sans-serif; color: #5D6B57; letter-spacing: .04em; }
    #s2-c .ln { position: absolute; left: 36px; height: 12px; border-radius: 3px; background: #AAB8A1; }
    #s2-stamp { position: absolute; left: 90px; right: 90px; top: 760px; display: flex; justify-content: center; }
    #s2-stamp span { display: block; border: 12px solid #D21034; border-radius: 22px; padding: 18px 34px; color: #D21034;
      font: 900 90px/1 Montserrat, sans-serif; letter-spacing: .01em; background: rgba(255,255,255,.72); white-space: nowrap; }
"""


def s2():
    lines_a = "".join(f'<div class="ln" style="top:{150 + k * 46}px;width:{300 - k * 30}px"></div>' for k in range(4))
    lines_b = "".join(f'<div class="ln" style="top:{140 + k * 54}px"></div>' for k in range(4))
    lines_c = "".join(f'<div class="ln" style="top:{120 + k * 50}px;width:{520 - (k % 2) * 140}px"></div>' for k in range(5))
    body = f"""    <div id="s2-ground"></div>
    <div id="s2-cam">
      <div class="s2-pc" data-layout-ignore id="s2-c"><div class="t1">ATTESTATION D'INSCRIPTION</div>{lines_c}</div>
      <div class="s2-pc" data-layout-ignore id="s2-b"><div class="t1">Carte d'étudiant</div>{lines_b}</div>
      <div class="s2-pc" data-layout-ignore id="s2-a"><div class="t1">UNIVERSITÉ ..........</div><div class="t2">CARTE D'ÉTUDIANT</div><div class="ph"></div>{lines_a}<div class="st">CACHET</div></div>
      <div id="s2-stamp"><span id="s2-stampin">NON VÉRIFIABLE</span></div>
    </div>"""
    js = r"""
      const land = [["#s2-c", 0.0, 9, -40], ["#s2-b", 0.1, -10, 30], ["#s2-a", 0.2, -4, 0]];
      land.forEach(([sel, t, rot, x]) => {
        tl.fromTo(sel, { y: -1500, x: x, rotation: rot - 30, filter: "blur(18px)" },
          { y: 0, x: x, rotation: rot, filter: "blur(0px)", duration: 0.45, ease: "power4.out" }, t);
      });
      // NON VÉRIFIABLE stamp on "suffit plus"
      tl.fromTo("#s2-stampin", { opacity: 0, scale: 2.6, rotation: -12 }, { opacity: 0.96, scale: 1, rotation: -12, duration: 0.16, ease: "power3.in" }, 1.09);
      tl.to("#s2-cam", { keyframes: [{ x: 16, y: -8, duration: 0.04 }, { x: -13, y: 7, duration: 0.05 }, { x: 8, y: -4, duration: 0.05 }, { x: -4, y: 2, duration: 0.05 }, { x: 0, y: 0, duration: 0.06 }] }, 1.25);
      tl.to(["#s2-a", "#s2-b", "#s2-c"], { filter: "saturate(.4) brightness(.92)", duration: 0.3, ease: "power2.out" }, 1.25);
"""
    return scene("s2", S2_CSS, body, js)


# ---------------------------------------------------------------- S3 REVEAL
S3_CSS = r"""
    #s3-wipe { position: absolute; left: -760px; top: -340px; width: 2600px; height: 2600px; transform: rotate(-18deg); }
    .s3-band { position: absolute; inset: 0; }
    #s3-rows { position: absolute; inset: 0; opacity: 0; }
    .s3-rowtxt { position: absolute; left: 0; white-space: nowrap; font: 900 190px/1 Montserrat, sans-serif; color: transparent;
      -webkit-text-stroke: 2px rgba(255,255,255,.11); letter-spacing: -0.01em; }
    #s3-rdc { position: absolute; left: 0; right: 0; top: 250px; text-align: center; font: 700 30px/1 'Open Sans', sans-serif;
      color: #A9C8F2; letter-spacing: .2em; }
    #s3-stage { position: absolute; inset: 0; perspective: 2400px; }
    #s3-card { left: 110px; top: 360px; }
    .s3-glosswrap { position: absolute; inset: 0; overflow: hidden; border-radius: 34px; }
    #s3-gloss { position: absolute; left: -500px; top: -300px; width: 260px; height: 1200px;
      background: linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,.55), rgba(255,255,255,0)); }
    .s3-t { position: absolute; left: 0; right: 0; text-align: center; font: 900 96px/1 Montserrat, sans-serif; letter-spacing: -0.02em; }
    #s3-t1 { top: 968px; color: #fff; }
    #s3-t2 { top: 1076px; color: #FCD116; }
    #s3-plate { position: absolute; left: 0; right: 0; top: 1206px; display: flex; justify-content: center; }
    #s3-platein { display: flex; align-items: center; gap: 18px; background: #fff; border-radius: 999px; padding: 10px 38px 10px 10px; }
    #s3-platein img { width: 84px; height: 84px; border-radius: 50%; }
    #s3-platein span { font: 800 32px/1 Montserrat, sans-serif; color: #0B2C5A; white-space: nowrap; }
""" + CARD_CSS


def rows_html(prefix):
    txt = "CARTE NATIONALE · CARTE NATIONALE · CARTE NATIONALE · "
    return "".join(f'<div class="s3-rowtxt" id="{prefix}-row{k}" style="top:{110 + k * 440}px">{txt}</div>' for k in range(4))


def s3():
    gloss = '<div class="s3-glosswrap"><div id="s3-gloss"></div></div>'
    front = card_front("s3c").replace('<div class="c-tri"></div>\n</div>', '<div class="c-tri"></div>\n' + gloss + '\n</div>')
    body = f"""    <div id="s3-wipe">
      <div class="s3-band" id="s3-w1" style="background:#2F86E0"></div>
      <div class="s3-band" id="s3-w2" style="background:#FCD116"></div>
      <div class="s3-band" id="s3-w3" style="background:#D21034"></div>
      <div class="s3-band" id="s3-w4" style="background:#0B2C5A"></div>
    </div>
    <div id="s3-rows" data-layout-ignore>{rows_html('s3')}</div>
    <div id="s3-rdc">RÉPUBLIQUE DÉMOCRATIQUE DU CONGO</div>
    <div id="s3-stage">
      <div class="card" id="s3-card">
{front}
      </div>
    </div>
    <div class="s3-t" id="s3-t1">CARTE NATIONALE</div>
    <div class="s3-t" id="s3-t2">DE L'ÉTUDIANT</div>
    <div id="s3-plate"><div id="s3-platein"><img src="assets/img/seal.png" alt=""><span>MINISTÈRE DE L'ESURSI</span></div></div>"""
    js = r"""
      ["#s3-w1", "#s3-w2", "#s3-w3", "#s3-w4"].forEach((s, i) => {
        tl.fromTo(s, { xPercent: -105 }, { xPercent: 0, duration: 0.48, ease: "power3.inOut" }, i * 0.07);
      });
      // background type drifts (continues in s4 at the same speed)
      tl.fromTo("#s3-rows", { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power2.out" }, 0.5);
      [0, 1, 2, 3].forEach((k) => {
        const from = k % 2 ? -400 : 0, dir = k % 2 ? 1 : -1;
        tl.fromTo("#s3-row" + k, { x: from }, { x: from + dir * 60, duration: 3.95, ease: "none" }, 0);
      });
      tl.fromTo("#s3-rdc", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }, 0.5);
      // the card turns from its edge to face camera
      tl.fromTo("#s3-card", { rotationY: 88, rotationX: 14, scale: 0.55, y: 140, opacity: 0 },
        { rotationY: 0, rotationX: 0, scale: 1, y: 0, opacity: 1, duration: 0.95, ease: "expo.out" }, 0.55);
      tl.fromTo("#s3-gloss", { x: 0, rotation: 20 }, { x: 1700, rotation: 20, duration: 0.75, ease: "power2.inOut" }, 1.25);
      // title on "Carte Nationale" / "de l'Étudiant"
      tl.fromTo("#s3-t1", { opacity: 0, scale: 1.08, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 0.94);
      tl.fromTo("#s3-t2", { opacity: 0, scale: 1.08, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }, 1.77);
      // ministry plate on "Ministère"
      tl.fromTo("#s3-platein", { opacity: 0, scale: 0.7 }, { opacity: 1, scale: 1, duration: 0.42, ease: "back.out(1.6)" }, 2.54);
      // clear the type, keep the card for s4
      tl.to(["#s3-rdc", "#s3-t1", "#s3-t2", "#s3-platein"], { opacity: 0, y: -24, filter: "blur(8px)", duration: 0.2, ease: "power3.in", stagger: 0.04 }, 3.6);
"""
    return scene("s3", S3_CSS, body, js)
