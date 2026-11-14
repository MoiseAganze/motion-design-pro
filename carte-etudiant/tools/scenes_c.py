from parts import ICON, CARD_CSS, card_front, scene

# ---------------------------------------------------------------- S6 NOT REGISTERED
S6_CSS = r"""
    #root { background: #F4F7FB; }
    #s6-all { position: absolute; inset: 0; }
    .s6-gl { position: absolute; left: 0; width: 1080px; }
    #s6-panel { position: absolute; left: 70px; top: 250px; width: 940px; height: 540px; border-radius: 34px; background: #fff; overflow: hidden;
      box-shadow: 0 30px 60px rgba(11,44,90,.16), 0 4px 12px rgba(11,44,90,.08); }
    #s6-head { position: absolute; left: 0; right: 0; top: 0; height: 110px; background: #0B2C5A; }
    #s6-head img { position: absolute; left: 26px; top: 19px; width: 72px; height: 72px; border-radius: 50%; background: #fff; }
    #s6-head b { position: absolute; left: 116px; top: 26px; font: 800 36px/1 Montserrat, sans-serif; color: #fff; }
    #s6-head span { position: absolute; left: 116px; top: 70px; font: 600 21px/1 'Open Sans', sans-serif; color: #A9C8F2; }
    #s6-search { position: absolute; left: 36px; right: 36px; top: 138px; height: 96px; border: 3px solid #D5DEEA; border-radius: 22px; background: #F8FAFD; }
    #s6-search svg { position: absolute; left: 26px; top: 26px; width: 40px; height: 40px; color: #7B8BA1; }
    #s6-typed { position: absolute; left: 88px; top: 26px; font: 700 40px/1.1 Montserrat, sans-serif; color: #0B2C5A; white-space: nowrap; }
    #s6-typed i { font-style: normal; opacity: 0; }
    #s6-ph { position: absolute; left: 88px; top: 30px; font: 600 34px/1 'Open Sans', sans-serif; color: #9AA8BA; }
    #s6-caret { display: inline-block; width: 4px; height: 42px; margin-left: 4px; background: #1957B8; vertical-align: -6px; opacity: 0; }
    .s6-row { position: absolute; left: 36px; right: 36px; height: 86px; border-radius: 18px; background: #F4F7FB; }
    .s6-ico { position: absolute; left: 18px; top: 15px; width: 56px; height: 56px; border-radius: 50%; background: #E3EAF3; color: #0B2C5A; }
    .s6-ico svg { position: absolute; inset: 12px; width: 32px; height: 32px; }
    .s6-bar { position: absolute; left: 96px; top: 36px; height: 16px; border-radius: 8px; background: #CBD5E2; }
    .s6-ok { position: absolute; right: 18px; top: 20px; height: 46px; padding: 0 20px 0 14px; border-radius: 23px; background: #E3F4EA; color: #1E8E4A;
      font: 800 24px/46px 'Open Sans', sans-serif; display: flex; align-items: center; gap: 6px; }
    .s6-ok svg { width: 26px; height: 26px; }
    #s6-me { top: 256px; opacity: 0; }
    #s6-mebg { position: absolute; inset: 0; border-radius: 18px; background: #FDE8EB; border: 3px solid #D21034; opacity: 0; }
    #s6-me b { position: absolute; left: 96px; top: 24px; font: 800 36px/1 Montserrat, sans-serif; color: #0B2C5A; }
    #s6-load { position: absolute; right: 18px; top: 20px; height: 46px; width: 130px; border-radius: 23px; background: #E3EAF3;
      display: flex; align-items: center; justify-content: center; gap: 10px; }
    #s6-load i { width: 12px; height: 12px; border-radius: 50%; background: #7B8BA1; }
    #s6-no { position: absolute; right: 18px; top: 18px; height: 50px; padding: 0 22px 0 14px; border-radius: 25px; background: #D21034; color: #fff;
      font: 800 25px/50px Montserrat, sans-serif; display: flex; align-items: center; gap: 6px; opacity: 0; white-space: nowrap; }
    #s6-no svg { width: 28px; height: 28px; }
    #s6-empty { position: absolute; left: 270px; top: 826px; width: 540px; height: 326px; border-radius: 30px; border: 6px dashed #D21034;
      background: rgba(210,16,52,.05); opacity: 0; }
    #s6-eph { position: absolute; left: 34px; top: 58px; width: 140px; height: 190px; border-radius: 14px; border: 4px dashed rgba(210,16,52,.55);
      font: 900 110px/182px Montserrat, sans-serif; color: #D21034; text-align: center; }
    #s6-et { position: absolute; left: 200px; top: 82px; font: 900 66px/1.02 Montserrat, sans-serif; color: #D21034; letter-spacing: -0.02em; }
"""


def s6():
    typed = "".join(f'<i id="s6-ch{k}">{"&nbsp;" if ch == " " else ch}</i>' for k, ch in enumerate("Ton université"))
    others = []
    for k, w in enumerate([420, 340, 470]):
        others.append(f'<div class="s6-row" id="s6-o{k}" style="top:{256 + k * 96}px"><div class="s6-ico">{ICON["bank"]}</div>'
                      f'<div class="s6-bar" style="width:{w}px"></div><div class="s6-ok">{ICON["check"]}Inscrit</div></div>')
    body = f"""    <div id="s6-all">
      <div id="s6-panel">
        <div id="s6-head"><img src="assets/img/seal.png" alt=""><b>ESURSI Connect</b><span>Établissements de l'ESU</span></div>
        <div id="s6-search">{ICON['search']}<div id="s6-ph">Rechercher un établissement…</div><div id="s6-typed">{typed}<span id="s6-caret"></span></div></div>
        {''.join(others)}
        <div class="s6-row" id="s6-me"><div id="s6-mebg"></div><div class="s6-ico">{ICON['bank']}</div><b>Ton université</b>
          <div id="s6-load"><i id="s6-d0"></i><i id="s6-d1"></i><i id="s6-d2"></i></div>
          <div id="s6-no">{ICON['x']}NON INSCRITE</div></div>
      </div>
      <div id="s6-empty"><div id="s6-eph">?</div><div id="s6-et">AUCUNE<br>CARTE</div></div>
    </div>
    <div class="s6-gl" id="s6-gl1" style="top:560px;height:90px;background:#D21034"></div>
    <div class="s6-gl" id="s6-gl2" style="top:980px;height:46px;background:#2F86E0"></div>"""
    js = r"""
      // glitch cut in
      tl.fromTo("#s6-all", { x: 46, skewX: 9 }, { keyframes: [{ x: -34, skewX: -6, duration: 0.034 }, { x: 18, skewX: 3, duration: 0.033 }, { x: 0, skewX: 0, duration: 0.05 }] }, 0);
      tl.fromTo("#s6-gl1", { x: -1080 }, { x: 1080, duration: 0.12, ease: "none" }, 0);
      tl.fromTo("#s6-gl2", { x: 1080 }, { x: -1080, duration: 0.1, ease: "none" }, 0.03);
      // typing "Ton université"
      tl.to("#s6-ph", { opacity: 0, duration: 0.05 }, 0.33);
      tl.set("#s6-caret", { opacity: 1 }, 0.33);
      for (let k = 0; k < 14; k++) tl.set("#s6-ch" + k, { opacity: 1 }, 0.33 + k * 0.055);
      tl.set("#s6-caret", { opacity: 0 }, 1.25);
      // the registered ones filter away, yours stays
      tl.to(["#s6-o0", "#s6-o1", "#s6-o2"], { opacity: 0, y: -22, duration: 0.24, ease: "power3.in", stagger: 0.05 }, 1.12);
      tl.fromTo("#s6-me", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "expo.out" }, 1.4);
      [0, 1, 2, 3, 4].forEach((step) => {
        [0, 1, 2].forEach((d) => tl.set("#s6-d" + d, { opacity: d === step % 3 ? 1 : 0.3 }, 1.5 + step * 0.14));
      });
      // NON INSCRITE on "plateforme"
      tl.to("#s6-load", { opacity: 0, scale: 0.7, duration: 0.1 }, 2.18);
      tl.fromTo("#s6-no", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.38, ease: "back.out(2.2)" }, 2.21);
      tl.to("#s6-mebg", { opacity: 1, duration: 0.15 }, 2.21);
      tl.to("#s6-me", { keyframes: [{ x: -15, duration: 0.05 }, { x: 12, duration: 0.06 }, { x: -8, duration: 0.06 }, { x: 4, duration: 0.06 }, { x: 0, duration: 0.07 }] }, 2.24);
      // no card for you
      tl.fromTo("#s6-empty", { opacity: 0, scale: 1.25, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "power4.out" }, 3.05);
      tl.to("#s6-empty", { keyframes: [{ x: -14, rotation: -1.2, duration: 0.05 }, { x: 11, rotation: 1, duration: 0.06 }, { x: -6, rotation: -0.5, duration: 0.06 }, { x: 0, rotation: 0, duration: 0.07 }] }, 3.69);
"""
    return scene("s6", S6_CSS, body, js)


# ---------------------------------------------------------------- S7 CALL TO ACTION
S7_CSS = r"""
    #s7-flood { position: absolute; inset: 0; background: #FCD116; clip-path: circle(0px at 540px 980px); }
    #s7-cam { position: absolute; inset: 0; }
    #s7-head { position: absolute; left: 0; right: 0; top: 540px; height: 400px; }
    #s7-alors { position: absolute; left: 0; right: 0; top: 0; text-align: center; font: 900 78px/1 Montserrat, sans-serif; color: #0B2C5A; opacity: 0; }
    #s7-bouge { position: absolute; left: 0; right: 0; top: 100px; text-align: center; font: 900 224px/1 Montserrat, sans-serif; color: #0B2C5A;
      letter-spacing: -0.03em; opacity: 0; }
    #s7-parle { position: absolute; left: 90px; top: 600px; font: 900 82px/1 Montserrat, sans-serif; color: #0B2C5A; opacity: 0; }
    .s7-c { position: absolute; left: 90px; width: 900px; height: 170px; border-radius: 34px; background: #0B2C5A;
      box-shadow: 0 24px 48px rgba(11,44,90,.28); }
    .s7-c .ic { position: absolute; left: 28px; top: 28px; width: 114px; height: 114px; border-radius: 50%; background: #FCD116; color: #0B2C5A; }
    .s7-c .ic svg { position: absolute; inset: 24px; width: 66px; height: 66px; }
    .s7-c b { position: absolute; left: 172px; top: 52px; font: 900 64px/1 Montserrat, sans-serif; color: #fff; letter-spacing: -0.01em; white-space: nowrap; }
    #s7-c1 { top: 740px; }
    #s7-c2 { top: 944px; }
    .s7-r { position: absolute; left: 0; right: 0; text-align: center; font: 900 150px/1 Montserrat, sans-serif; color: #0B2C5A; letter-spacing: -0.03em; opacity: 0; }
    #s7-r1 { top: 470px; }
    #s7-r2 { top: 640px; }
    #s7-r3 { position: absolute; left: 0; right: 0; top: 856px; display: flex; justify-content: center; }
    #s7-r3in { display: block; background: #D21034; color: #fff; font: 900 104px/1 Montserrat, sans-serif; letter-spacing: -0.02em;
      padding: 26px 44px 30px; border-radius: 24px; white-space: nowrap; opacity: 0; box-shadow: 0 24px 50px rgba(210,16,52,.35); }
"""


def s7():
    body = f"""    <div id="s7-flood"></div>
    <div id="s7-cam">
      <div id="s7-head"><div id="s7-alors">ALORS</div><div id="s7-bouge">BOUGE !</div></div>
      <div id="s7-parle">PARLE À…</div>
      <div class="s7-c" id="s7-c1"><div class="ic">{ICON['user']}</div><b>TON DÉLÉGUÉ</b></div>
      <div class="s7-c" id="s7-c2"><div class="ic">{ICON['bank']}</div><b>TON SECRÉTARIAT</b></div>
      <div class="s7-r" id="s7-r1">RÉCLAME</div>
      <div class="s7-r" id="s7-r2">TA CARTE</div>
      <div id="s7-r3"><span id="s7-r3in">MAINTENANT !</span></div>
    </div>"""
    js = r"""
      tl.fromTo("#s7-flood", { clipPath: "circle(0px at 540px 980px)" }, { clipPath: "circle(1250px at 540px 980px)", duration: 0.42, ease: "power3.inOut" }, 0);
      tl.fromTo("#s7-alors", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16, ease: "power3.out" }, 0.23);
      tl.fromTo("#s7-bouge", { opacity: 0, scale: 1.7, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.28, ease: "expo.out" }, 0.47);
      const shake = (t, a) => tl.to("#s7-cam", { keyframes: [{ x: a, y: -a / 2, duration: 0.04 }, { x: -a * 0.8, y: a / 2, duration: 0.05 }, { x: a * 0.5, y: -a / 4, duration: 0.05 }, { x: 0, y: 0, duration: 0.06 }] }, t);
      shake(0.52, 18);
      // parle à ton délégué / ton secrétariat
      tl.to("#s7-head", { y: -330, scale: 0.55, transformOrigin: "50% 0%", duration: 0.42, ease: "power3.inOut" }, 1.2);
      tl.fromTo("#s7-parle", { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power3.out" }, 1.3);
      tl.fromTo("#s7-c1", { opacity: 1, x: -1150, filter: "blur(16px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 1.62);
      tl.fromTo("#s7-c2", { opacity: 1, x: 1150, filter: "blur(16px)" }, { opacity: 1, x: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }, 2.46);
      // réclame ta carte, maintenant
      tl.to(["#s7-head", "#s7-parle", "#s7-c1", "#s7-c2"], { opacity: 0, y: "-=160", filter: "blur(8px)", duration: 0.24, ease: "power3.in", stagger: 0.035 }, 3.22);
      tl.fromTo("#s7-r1", { opacity: 0, scale: 1.3, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }, 3.45);
      tl.fromTo("#s7-r2", { opacity: 0, scale: 1.3, filter: "blur(12px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.24, ease: "expo.out" }, 3.93);
      tl.fromTo("#s7-r3in", { opacity: 0, scale: 2.1, rotation: -10 }, { opacity: 1, scale: 1, rotation: -4, duration: 0.22, ease: "power4.out" }, 4.6);
      shake(4.7, 22);
"""
    return scene("s7", S7_CSS, body, js)


# ---------------------------------------------------------------- S8 END CARD
S8_CSS = r"""
    #s8-flood { position: absolute; inset: 0; background: #FFFFFF; clip-path: circle(0px at 540px 960px); }
    #s8-head { position: absolute; left: 200px; top: 196px; width: 680px; opacity: 0; }
    #s8-tri { position: absolute; left: 90px; top: 450px; width: 900px; height: 12px; display: flex; }
    #s8-tri i { flex: 1; height: 12px; transform-origin: 0 50%; }
    #s8-stage { position: absolute; inset: 0; perspective: 2400px; }
    #s8-card { left: 110px; top: 470px; }
    #s8-url { position: absolute; left: 0; right: 0; top: 1004px; display: flex; justify-content: center; }
    #s8-urlin { display: flex; align-items: center; gap: 18px; height: 116px; padding: 0 46px 0 34px; border-radius: 58px; background: #0B2C5A;
      box-shadow: 0 24px 50px rgba(11,44,90,.3); opacity: 0; }
    #s8-urlin svg { width: 56px; height: 56px; color: #FCD116; flex: none; }
    #s8-urltxt { font: 800 50px/1 Montserrat, sans-serif; color: #fff; white-space: nowrap; letter-spacing: -0.01em; }
    #s8-urltxt i { font-style: normal; opacity: 0; }
    #s8-band { position: absolute; left: 0; right: 0; top: 1158px; height: 160px; background: #FCD116; clip-path: inset(0px 100% 0px 0px); }
    #s8-bandtxt { position: absolute; left: 90px; right: 90px; top: 30px; font: 800 46px/1.1 Montserrat, sans-serif; color: #0B2C5A; opacity: 0; }
""" + CARD_CSS


def s8():
    url = "carte.minesursi.gouv.cd"
    chars = "".join(f'<i id="s8-u{k}">{ch}</i>' for k, ch in enumerate(url))
    body = f"""    <div id="s8-flood"></div>
    <img id="s8-head" src="assets/img/ministere_header.png" alt="Ministère de l'ESURSI">
    <div id="s8-tri"><i id="s8-t0" style="background:#2F86E0"></i><i id="s8-t1" style="background:#FCD116"></i><i id="s8-t2" style="background:#D21034"></i></div>
    <div id="s8-stage">
      <div class="card" id="s8-card">
{card_front('s8c')}
      </div>
    </div>
    <div id="s8-url"><div id="s8-urlin">{ICON['globe']}<span id="s8-urltxt">{chars}</span></div></div>
    <div id="s8-band"><div id="s8-bandtxt">Réclame ta carte auprès de<br>ton établissement !</div></div>"""
    js = r"""
      tl.fromTo("#s8-flood", { clipPath: "circle(0px at 540px 960px)" }, { clipPath: "circle(1250px at 540px 960px)", duration: 0.36, ease: "power3.inOut" }, 0);
      tl.set(["#s8-t0", "#s8-t1", "#s8-t2"], { scaleX: 0 }, 0);
      tl.fromTo("#s8-head", { opacity: 0, filter: "blur(10px)", y: 14 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.3, ease: "power3.out" }, 0.3);
      ["#s8-t0", "#s8-t1", "#s8-t2"].forEach((s, i) => tl.to(s, { scaleX: 1, duration: 0.3, ease: "power3.out" }, 0.42 + i * 0.08));
      tl.fromTo("#s8-card", { opacity: 0, y: 420, rotationX: 38, rotationY: 0, scale: 0.8 },
        { opacity: 1, y: 0, rotationX: 0, rotationY: -7, scale: 0.8, duration: 0.75, ease: "expo.out" }, 0.3);
      tl.to("#s8-card", { rotationY: 7, duration: 3.6, ease: "sine.inOut" }, 1.05);
      tl.fromTo("#s8-urlin", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }, 0.12);
      for (let k = 0; k < 23; k++) tl.set("#s8-u" + k, { opacity: 1 }, 0.2 + k * 0.1);
      tl.fromTo("#s8-band", { clipPath: "inset(0px 100% 0px 0px)" }, { clipPath: "inset(0px 0% 0px 0px)", duration: 0.45, ease: "power3.out" }, 2.6);
      tl.fromTo("#s8-bandtxt", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }, 2.75);
"""
    return scene("s8", S8_CSS, body, js)
