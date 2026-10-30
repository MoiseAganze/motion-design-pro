"""Derives the vertical scenes (compositions/v/) from the landscape ones by swapping ids
and replacing the layout (positions, sizes, camera keys) for a 1080 x 1920 frame.
Each replacement must match exactly once, so a change to a landscape scene that breaks
a vertical layout fails loudly here instead of drifting."""
import re, sys

def derive(src, dst, n, pairs):
    s = open(src).read()
    s = s.replace(f"s{n}-", f"v{n}-").replace(f'"s{n}"', f'"v{n}"').replace(f"#s{n}", f"#v{n}")
    s = s.replace('data-width="1920" data-height="1080"', 'data-width="1080" data-height="1920"')
    for a, b in pairs:
        c = s.count(a)
        if c != 1:
            sys.exit(f"{dst}: expected 1 match, found {c}: {a[:90]!r}")
        s = s.replace(a, b)
    open(dst, "w").write(s)
    print("wrote", dst)

# ---------------------------------------------------------------- v1: la routine
derive("compositions/s1-routine.html", "../formation-n8n-vertical/compositions/v1-routine.html", 1, [
    ("left: 560px;\n      top: -340px;", "left: -400px;\n      top: 0px;"),
    ("left: -520px;\n      top: 420px;", "left: -500px;\n      top: 1100px;"),
    ('''    #v1-rings {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;''', '''    #v1-rings {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;'''),
    ('''    #v1-title {
      position: absolute;
      left: 140px;
      top: 300px;
      width: 640px;''', '''    #v1-title {
      position: absolute;
      left: 80px;
      top: 220px;
      width: 920px;'''),
    ("      font-size: 112px;\n      line-height: 1.02;", "      font-size: 110px;\n      line-height: 1.02;"),
    ('''    #v1-q {
      position: absolute;
      left: 140px;
      top: 330px;
      width: 760px;''', '''    #v1-q {
      position: absolute;
      left: 80px;
      top: 230px;
      width: 920px;'''),
    ("      font-size: 170px;\n      line-height: 1;", "      font-size: 190px;\n      line-height: 1;"),
    ('''    #v1-q2 {
      margin-top: 24px;
      font-weight: 700;
      font-size: 64px;''', '''    #v1-q2 {
      margin-top: 24px;
      font-weight: 700;
      font-size: 76px;'''),
    ('''    #v1-orbit {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;
      transform-origin: 1260px 560px;''', '''    #v1-orbit {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
      transform-origin: 540px 860px;'''),
    ('''    #v1-hub {
      position: absolute;
      left: 1070px;
      top: 370px;''', '''    #v1-hub {
      position: absolute;
      left: 350px;
      top: 670px;'''),
    ('''    #v1-chip {
      position: absolute;
      left: 1170px;
      top: 778px;''', '''    #v1-chip {
      position: absolute;
      left: 450px;
      top: 1072px;'''),
    ('''    #v1-sheet {
      position: absolute;
      left: 300px;
      top: 740px;
      width: 520px;''', '''    #v1-sheet {
      position: absolute;
      left: 540px;
      top: 410px;
      width: 480px;'''),
    ('<svg id="v1-rings" viewBox="0 0 1920 1080"', '<svg id="v1-rings" viewBox="0 0 1080 1920"'),
    ('''      <circle cx="1260" cy="560" r="280" />
      <circle cx="1260" cy="560" r="420" stroke-dasharray="4 14" />
      <circle cx="1260" cy="560" r="560" />''', '''      <circle cx="540" cy="860" r="270" />
      <circle cx="540" cy="860" r="400" stroke-dasharray="4 14" />
      <circle cx="540" cy="860" r="530" />'''),
    ('id="v1-t-gmail" style="left: 818px; top: 318px"', 'id="v1-t-gmail" style="left: 108px; top: 628px"'),
    ('id="v1-t-cal" style="left: 1118px; top: 88px"', 'id="v1-t-cal" style="left: 848px; top: 650px"'),
    ('id="v1-t-wa" style="left: 1588px; top: 238px"', 'id="v1-t-wa" style="left: 878px; top: 880px"'),
    ('id="v1-t-tg" style="left: 1658px; top: 668px"', 'id="v1-t-tg" style="left: 760px; top: 1040px"'),
    ('id="v1-t-drive" style="left: 1288px; top: 878px"', 'id="v1-t-drive" style="left: 196px; top: 1040px"'),
    ('id="v1-t-sheets" style="left: 868px; top: 728px"', 'id="v1-t-sheets" style="left: 78px; top: 860px"'),
    ('id="v1-mail-1" style="left: 600px; top: 64px"', 'id="v1-mail-1" style="left: 590px; top: 400px"'),
    ('id="v1-mail-2" style="left: 660px; top: 150px"', 'id="v1-mail-2" style="left: 610px; top: 486px"'),
    ('id="v1-rel-1" style="left: 1480px; top: 410px"', 'id="v1-rel-1" style="left: 616px; top: 404px"'),
    ('id="v1-rel-2" style="left: 1500px; top: 492px"', 'id="v1-rel-2" style="left: 584px; top: 470px"'),
    ('id="v1-rel-3" style="left: 1488px; top: 574px"', 'id="v1-rel-3" style="left: 640px; top: 536px"'),
    ('id="v1-rel-4" style="left: 1510px; top: 520px"', 'id="v1-rel-4" style="left: 600px; top: 500px"'),
    ('id="v1-rel-5" style="left: 1484px; top: 448px"', 'id="v1-rel-5" style="left: 624px; top: 438px"'),
    # vertical: the stack area is shared, so each wave clears the previous one
    ('      // ---- "copier les mêmes données…" (2.56): the same row, pasted again and again\n',
     '      // ---- "copier les mêmes données…" (2.56): the same row, pasted again and again\n      tl.to(["#v1-mail-1", "#v1-mail-2"], { opacity: 0, y: -50, duration: 0.25, ease: "power3.in" }, 2.3);\n'),
    ('      count("#v1-b-wa", 2, 9, 4.35, 1.6);', '      tl.to("#v1-sheet", { opacity: 0, y: -50, duration: 0.25, ease: "power3.in" }, 4.05);\n      count("#v1-b-wa", 2, 9, 4.35, 1.6);'),
    ('tl.to("#v1-hub", { x: 960 - 1260, y: 540 - 560, scale: 0.12, duration: 0.7, ease: "power3.in" }, 9.3);',
     'tl.to("#v1-hub", { x: 0, y: 800 - 860, scale: 0.12, duration: 0.7, ease: "power3.in" }, 9.3);'),
])

# ---------------------------------------------------------------- v2: n8n
derive("compositions/s2-n8n.html", "../formation-n8n-vertical/compositions/v2-n8n.html", 2, [
    ("left: -40px;\n      top: -360px;\n      width: 2000px;\n      height: 1800px;", "left: -460px;\n      top: -100px;\n      width: 2000px;\n      height: 2000px;"),
    ('''    #v2-cam {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;
      transform-origin: 380px 600px;''', '''    #v2-cam {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
      transform-origin: 165px 800px;'''),
    ('''    #v2-wires {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;''', '''    #v2-wires {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;'''),
    ('''    #v2-hub {
      position: absolute;
      left: 960px;
      top: 580px;''', '''    #v2-hub {
      position: absolute;
      left: 540px;
      top: 800px;'''),
    ('''    #v2-word {
      position: absolute;
      left: 0;
      top: 70px;
      width: 1920px;
      text-align: center;
      font-weight: 800;
      font-size: 110px;''', '''    #v2-word {
      position: absolute;
      left: 0;
      top: 240px;
      width: 1080px;
      text-align: center;
      font-weight: 800;
      font-size: 150px;'''),
    ('''    #v2-title {
      position: absolute;
      left: 0;
      top: 92px;
      width: 1920px;
      text-align: center;
      font-weight: 800;
      font-size: 76px;''', '''    #v2-title {
      position: absolute;
      left: 0;
      top: 210px;
      width: 1080px;
      text-align: center;
      font-weight: 800;
      font-size: 86px;
      line-height: 1.1;'''),
    ('<svg id="v2-wires" viewBox="0 0 1920 1080"', '<svg id="v2-wires" viewBox="0 0 1080 1920"'),
    ('''          <path id="v2-w1" d="M490 477 Q 700 460 960 580" />
          <path id="v2-w2" d="M873 285 Q 870 450 960 580" />
          <path id="v2-w3" d="M1343 387 Q 1160 420 960 580" />
          <path id="v2-w4" d="M1430 683 Q 1210 720 960 580" />
          <path id="v2-w5" d="M1047 875 Q 1060 700 960 580" />
          <path id="v2-w6" d="M577 773 Q 740 740 960 580" />''', '''          <path id="v2-w1" d="M211 650 Q 350 680 540 800" />
          <path id="v2-w2" d="M540 500 Q 500 650 540 800" />
          <path id="v2-w3" d="M869 650 Q 730 680 540 800" />
          <path id="v2-w4" d="M869 950 Q 730 920 540 800" />
          <path id="v2-w5" d="M540 1100 Q 580 950 540 800" />
          <path id="v2-w6" d="M211 950 Q 350 920 540 800" />'''),
    ('''          <path id="v2-c1" d="M442 600 C 560 600 560 600 690 600" />
          <path id="v2-c2" d="M910 600 C 1000 600 1020 600 1118 600" />
          <path id="v2-c3" d="M1242 600 C 1340 600 1360 600 1478 600" />''', '''          <path id="v2-c1" d="M227 800 C 270 800 280 800 324 800" />
          <path id="v2-c2" d="M506 800 C 540 800 570 800 603 800" />
          <path id="v2-c3" d="M727 800 C 770 800 810 800 853 800" />'''),
    ('id="v2-t-cal" style="left: 873px; top: 285px"', 'id="v2-t-cal" style="left: 540px; top: 500px"'),
    ('id="v2-t-wa" style="left: 1343px; top: 387px"', 'id="v2-t-wa" style="left: 869px; top: 650px"'),
    ('id="v2-t-tg" style="left: 1430px; top: 683px"', 'id="v2-t-tg" style="left: 869px; top: 950px"'),
    ('id="v2-t-drive" style="left: 1047px; top: 875px"', 'id="v2-t-drive" style="left: 540px; top: 1100px"'),
    ('id="v2-t-sheets" style="left: 577px; top: 773px"', 'id="v2-t-sheets" style="left: 211px; top: 950px"'),
    ('id="v2-t-gmail" style="left: 490px; top: 477px"', 'id="v2-t-gmail" style="left: 211px; top: 650px"'),
    ('<span>Vos</span> <span>outils,</span> <span class="v2-acc">enfin</span>', '<span>Vos</span> <span>outils,</span><br /><span class="v2-acc">enfin</span>'),
    ("const C = { x: 960, y: 580 };", "const C = { x: 540, y: 800 };"),
    ('''        [490, 477],
        [873, 285],
        [1343, 387],
        [1430, 683],
        [1047, 875],
        [577, 773],''', '''        [211, 650],
        [540, 500],
        [869, 650],
        [869, 950],
        [540, 1100],
        [211, 950],'''),
    ('tl.to("#v2-t-gmail", { x: 380 - 490, y: 600 - 477, duration: 0.6, ease: "power3.inOut" }, 2.62);', 'tl.to("#v2-t-gmail", { x: 165 - 211, y: 800 - 650, duration: 0.6, ease: "power3.inOut" }, 2.62);'),
    ('tl.to("#v2-hub", { x: 800 - 960, y: 600 - 580, scale: 0.85, duration: 0.6, ease: "power3.inOut" }, 2.62);', 'tl.to("#v2-hub", { x: 415 - 540, y: 0, scale: 0.7, duration: 0.6, ease: "power3.inOut" }, 2.62);'),
    ('tl.to("#v2-t-sheets", { x: 1180 - 577, y: 600 - 773, duration: 0.6, ease: "power3.inOut" }, 2.66);', 'tl.to("#v2-t-sheets", { x: 665 - 211, y: 800 - 950, duration: 0.6, ease: "power3.inOut" }, 2.66);'),
    ('tl.to("#v2-t-wa", { x: 1540 - 1343, y: 600 - 387, duration: 0.6, ease: "power3.inOut" }, 2.7);', 'tl.to("#v2-t-wa", { x: 915 - 869, y: 800 - 650, duration: 0.6, ease: "power3.inOut" }, 2.7);'),
    ('tl.fromTo("#v2-cam", { scale: 1, x: 0, y: 0 }, { scale: 20, x: 580, y: -60, duration: 0.7, ease: "power3.in" }, 3.9);', 'tl.fromTo("#v2-cam", { scale: 1, x: 0, y: 0 }, { scale: 22, x: 375, y: 160, duration: 0.7, ease: "power3.in" }, 3.9);'),
])

# ---------------------------------------------------------------- v3: ESURSI
derive("compositions/s3-courriers.html", "../formation-n8n-vertical/compositions/v3-courriers.html", 3, [
    ('''    #v3-bar {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 104px;''', '''    #v3-bar {
      position: absolute;
      left: 0;
      top: 170px;
      width: 1080px;
      height: 104px;
      border-top: 2px solid #2a2a2a;'''),
    ('''    #v3-crumb {
      position: absolute;
      left: 60px;
      top: 0;
      line-height: 104px;
      font-size: 32px;''', '''    #v3-crumb {
      position: absolute;
      left: 40px;
      top: 0;
      line-height: 104px;
      font-size: 30px;'''),
    ('''    #v3-pub {
      position: absolute;
      right: 60px;''', '''    #v3-pub {
      position: absolute;
      right: 40px;'''),
    ('''    #v3-mail {
      position: absolute;
      left: 470px;
      top: 210px;
      width: 500px;''', '''    #v3-mail {
      position: absolute;
      left: 290px;
      top: 380px;
      width: 500px;'''),
    ('''    #v3-reply {
      position: absolute;
      left: 1250px;
      top: 330px;''', '''    #v3-reply {
      position: absolute;
      left: 250px;
      top: 440px;'''),
    ('''    #v3-shot {
      position: absolute;
      left: 140px;
      top: 190px;
      width: 1640px;
      height: 740px;''', '''    #v3-shot {
      position: absolute;
      left: 40px;
      top: 480px;
      width: 1000px;
      height: 451px;'''),
    ('''    #v3-shot img {
      width: 1640px;
      height: 740px;''', '''    #v3-shot img {
      width: 1000px;
      height: 451px;'''),
    ('Personal&nbsp;&nbsp;/&nbsp;&nbsp;<b>Agent Courriers ESURSI</b>', '<b>Agent Courriers ESURSI</b>'),
    ('tl.fromTo(cam, { x: 560, y: -540, scale: 2.0 }, { x: 460, y: -142, scale: 1.3, duration: 0.7, ease: "expo.out" }, 0);', 'tl.fromTo(cam, { x: 140, y: -320, scale: 2.0 }, { x: 140, y: 18, scale: 1.3, duration: 0.7, ease: "expo.out" }, 0);'),
    ('tl.to(cam, { x: -350, y: -115, scale: 1.25, duration: 0.75, ease: "power2.inOut" }, 0.7);', 'tl.to(cam, { x: -710, y: 45, scale: 1.25, duration: 0.75, ease: "power2.inOut" }, 0.7);'),
    ('tl.to(cam, { x: -2652, y: -150, scale: 1.4, duration: 1.15, ease: "power2.inOut" }, 1.45);', 'tl.to(cam, { x: -2814, y: 120, scale: 1.3, duration: 1.15, ease: "power2.inOut" }, 1.45);'),
    ('tl.to(cam, { x: -2880, y: 32, scale: 1.2, duration: 0.65, ease: "power2.inOut" }, 2.7);', 'tl.to(cam, { x: -3300, y: 192, scale: 1.2, duration: 0.65, ease: "power2.inOut" }, 2.7);'),
    ('tl.to(cam, { x: -3614, y: 270, scale: 1.2, duration: 0.8, ease: "power2.inOut" }, 3.4);', 'tl.to(cam, { x: -4144, y: 450, scale: 1.2, duration: 0.8, ease: "power2.inOut" }, 3.4);'),
    ('tl.to(cam, { x: 200.45, y: 332.24, scale: 0.3556, duration: 0.65, ease: "power3.inOut" }, 4.6);', 'tl.to(cam, { x: 76.86, y: 566.73, scale: 0.2168, duration: 0.65, ease: "power3.inOut" }, 4.6);'),
    ('tl.to("#v3-mail", { x: 720 - 720, y: 300, scale: 0.12, opacity: 0, duration: 0.3, ease: "power3.in" }, 0.42);', 'tl.to("#v3-mail", { x: 400 - 540, y: 290, scale: 0.12, opacity: 0, duration: 0.3, ease: "power3.in" }, 0.42);'),
])

# ---------------------------------------------------------------- v4: MapSante (the camera tracks the real layout)
derive("compositions/s4-requete.html", "../formation-n8n-vertical/compositions/v4-requete.html", 4, [
    ("      transform-origin: 960px 560px;", "      transform-origin: 0 0;"),
    ('''    #v4-bar {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 104px;''', '''    #v4-bar {
      position: absolute;
      left: 0;
      top: 170px;
      width: 1080px;
      height: 104px;
      border-top: 2px solid #2a2a2a;'''),
    ('''    #v4-crumb {
      position: absolute;
      left: 60px;''', '''    #v4-crumb {
      position: absolute;
      left: 40px;'''),
    ('''    #v4-pub {
      position: absolute;
      right: 60px;''', '''    #v4-pub {
      position: absolute;
      right: 40px;'''),
    ("    #v4-req {\n      left: 120px;\n      top: 250px;", "    #v4-req {\n      left: 80px;\n      top: 380px;"),
    ("    #v4-rows {\n      left: 960px;\n      top: 168px;", "    #v4-rows {\n      left: 250px;\n      top: 330px;"),
    ("    #v4-resp {\n      left: 1380px;\n      top: 230px;", "    #v4-resp {\n      left: 360px;\n      top: 450px;"),
    ('Personal&nbsp;&nbsp;/&nbsp;&nbsp;<b>MapSante AI (Assistant Pro)</b>', '<b>MapSante AI (Assistant Pro)</b>'),
    ('      <div id="v4-exec">Execute</div>\n', ''),
    ('tl.fromTo("#v4-cam", { x: 1100, scale: 1.08, filter: "blur(16px)" }, { x: 0, scale: 1.08, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 0);',
     '''tl.fromTo("#v4-cam", { x: 1060, y: 200, filter: "blur(16px)" }, { x: 160, y: 200, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 0);
      // the frame is narrow: the camera follows the request along the real layout
      tl.to("#v4-cam", { x: -274, duration: 0.35, ease: "power2.inOut" }, 0.92);
      tl.to("#v4-cam", { x: -700, y: 230, duration: 0.42, ease: "power2.inOut" }, 1.28);
      tl.to("#v4-cam", { x: -1020, y: 200, duration: 0.42, ease: "power2.inOut" }, 2.58);'''),
    ('tl.to("#v4-req", { x: 223 - 290, y: 560 - 290, scale: 0.15, opacity: 0, duration: 0.25, ease: "power3.in" }, 0.36);',
     'tl.to("#v4-req", { x: 93, y: 335, scale: 0.15, opacity: 0, duration: 0.25, ease: "power3.in" }, 0.36);'),
    ('tl.to("#v4-cam", { scale: 0.55, opacity: 0.25, filter: "blur(6px)", duration: 0.5, ease: "power3.in" }, 4.2);',
     'tl.to("#v4-cam", { scale: 0.5, x: 60, y: 480, opacity: 0.25, filter: "blur(6px)", duration: 0.5, ease: "power3.in" }, 4.2);'),
])

# ---------------------------------------------------------------- v6: la formation
derive("compositions/s6-formation.html", "../formation-n8n-vertical/compositions/v6-formation.html", 6, [
    ("left: -100px;\n      top: -500px;\n      width: 2100px;\n      height: 2000px;", "left: -510px;\n      top: -60px;\n      width: 2100px;\n      height: 2000px;"),
    ('''    #v6-title {
      position: absolute;
      left: 0;
      top: 170px;
      width: 1920px;
      text-align: center;
      transform-origin: 960px 0;''', '''    #v6-title {
      position: absolute;
      left: 0;
      top: 560px;
      width: 1080px;
      text-align: center;
      transform-origin: 540px 0;'''),
    ("      font-size: 54px;\n      letter-spacing: 0.32em;", "      font-size: 50px;\n      letter-spacing: 0.32em;"),
    ("      margin-top: 22px;\n      font-weight: 800;\n      font-size: 168px;", "      margin-top: 22px;\n      font-weight: 800;\n      font-size: 118px;"),
    ('''    #v6-by {
      position: absolute;
      left: 0;
      top: 470px;
      width: 1920px;''', '''    #v6-by {
      position: absolute;
      left: 0;
      top: 560px;
      width: 1080px;'''),
    ('''    #v6-logo {
      position: absolute;
      left: 660px;
      top: 548px;
      width: 600px;
      height: 374px;
      transform-origin: 528px 264px;
    }
    #v6-logo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 600px;
      height: 374px;''', '''    #v6-logo {
      position: absolute;
      left: 190px;
      top: 650px;
      width: 700px;
      height: 436px;
      transform-origin: 616px 308px;
    }
    #v6-logo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 700px;
      height: 436px;'''),
    ('tl.to("#v6-title", { y: -110, scale: 0.6, duration: 0.55, ease: "power3.inOut" }, 2.6);', 'tl.to("#v6-title", { y: -320, scale: 0.68, duration: 0.55, ease: "power3.inOut" }, 2.6);'),
    ('tl.to("#v6-logo", { scale: 13, x: 960 - (660 + 528), y: 540 - (548 + 264), duration: 0.42, ease: "power3.in" }, 3.8);',
     'tl.to("#v6-logo", { scale: 13, x: 540 - (190 + 616), y: 960 - (650 + 308), duration: 0.42, ease: "power3.in" }, 3.8);'),
])

# ---------------------------------------------------------------- v7: Kinshasa / Silikin Village
derive("compositions/s7-kinshasa.html", "../formation-n8n-vertical/compositions/v7-kinshasa.html", 7, [
    ("left: 500px;\n      top: -400px;", "left: -410px;\n      top: -340px;"),
    ('''    #v7-map {
      position: absolute;
      left: 1000px;
      top: 70px;
      width: 837px;
      height: 940px;
      transform-origin: 410px 449px;
    }
    #v7-map img {
      position: absolute;
      left: 0;
      top: 0;
      width: 837px;
      height: 940px;''', '''    #v7-map {
      position: absolute;
      left: 202px;
      top: 250px;
      width: 677px;
      height: 760px;
      transform-origin: 332px 363px;
    }
    #v7-map img {
      position: absolute;
      left: 0;
      top: 0;
      width: 677px;
      height: 760px;'''),
    ("    #v7-pin {\n      position: absolute;\n      left: 380px;\n      top: 359px;", "    #v7-pin {\n      position: absolute;\n      left: 302px;\n      top: 275px;"),
    ('''    #v7-text {
      position: absolute;
      left: 140px;
      top: 380px;
      width: 820px;''', '''    #v7-text {
      position: absolute;
      left: 0;
      top: 940px;
      width: 1080px;
      text-align: center;'''),
    ("      font-size: 150px;\n      line-height: 1;", "      font-size: 132px;\n      line-height: 1;"),
    ("      margin-top: 22px;\n      font-weight: 600;\n      font-size: 40px;", "      margin-top: 14px;\n      font-weight: 600;\n      font-size: 36px;"),
    ('''    #v7-room {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      clip-path: circle(0px at 1410px 519px);''', '''    #v7-room {
      position: absolute;
      left: 0;
      top: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      clip-path: circle(0px at 534px 613px);'''),
    ('''    #v7-photo {
      position: absolute;
      left: 0;
      top: -180px;
      width: 1920px;
      height: 1440px;
      transform-origin: 905px 735px;
    }
    #v7-photo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 1920px;
      height: 1440px;''', '''    #v7-photo {
      position: absolute;
      left: -740px;
      top: 0;
      width: 2560px;
      height: 1920px;
      transform-origin: 1206px 980px;
    }
    #v7-photo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 2560px;
      height: 1920px;'''),
    ('''    #v7-tv {
      position: absolute;
      left: 826px;
      top: 691px;
      width: 158px;
      height: 88px;''', '''    #v7-tv {
      position: absolute;
      left: 1101px;
      top: 920px;
      width: 211px;
      height: 119px;'''),
    ('''    #v7-tv img {
      position: absolute;
      left: 2px;
      top: 9px;
      width: 154px;
      height: 70px;''', '''    #v7-tv img {
      position: absolute;
      left: 2px;
      top: 13px;
      width: 207px;
      height: 93px;'''),
    ("    #v7-label {\n      position: absolute;\n      left: 120px;\n      top: 770px;", "    #v7-label {\n      position: absolute;\n      left: 60px;\n      top: 880px;"),
    ("République démocratique<br />du <b>Congo</b>", "République démocratique du <b>Congo</b>"),
    ('tl.fromTo("#v7-map", { scale: 3.2, x: 960 - 1410, y: 540 - 519, filter: "blur(10px)" }', 'tl.fromTo("#v7-map", { scale: 3.2, x: 540 - 534, y: 960 - 613, filter: "blur(10px)" }'),
    ('tl.fromTo("#v7-room", { clipPath: "circle(0px at 1410px 519px)" }, { clipPath: "circle(2300px at 1410px 519px)"', 'tl.fromTo("#v7-room", { clipPath: "circle(0px at 534px 613px)" }, { clipPath: "circle(2300px at 534px 613px)"'),
])

# ---------------------------------------------------------------- v9: end card
derive("compositions/s9-fin.html", "../formation-n8n-vertical/compositions/v9-fin.html", 9, [
    ("left: -40px;\n      top: -620px;", "left: -460px;\n      top: -380px;"),
    ('''    #v9-logo {
      position: absolute;
      left: 600px;
      top: 92px;
      width: 720px;
      height: 449px;
      transform-origin: 360px 260px;
    }
    #v9-logo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 720px;
      height: 449px;''', '''    #v9-logo {
      position: absolute;
      left: 120px;
      top: 290px;
      width: 840px;
      height: 524px;
      transform-origin: 420px 300px;
    }
    #v9-logo img {
      position: absolute;
      left: 0;
      top: 0;
      width: 840px;
      height: 524px;'''),
    ('''    #v9-what {
      position: absolute;
      left: 0;
      top: 586px;
      width: 1920px;
      text-align: center;
      font-weight: 700;
      font-size: 52px;''', '''    #v9-what {
      position: absolute;
      left: 0;
      top: 862px;
      width: 1080px;
      text-align: center;
      font-weight: 700;
      font-size: 56px;'''),
    ('''    #v9-where {
      position: absolute;
      left: 0;
      top: 656px;
      width: 1920px;''', '''    #v9-where {
      position: absolute;
      left: 0;
      top: 936px;
      width: 1080px;'''),
    ('''    #v9-cta {
      position: absolute;
      left: 560px;
      top: 742px;
      width: 800px;
      height: 104px;''', '''    #v9-cta {
      position: absolute;
      left: 90px;
      top: 1020px;
      width: 900px;
      height: 110px;'''),
    ("      font-size: 44px;\n      line-height: 104px;", "      font-size: 48px;\n      line-height: 110px;"),
    ('''    #v9-contacts {
      position: absolute;
      left: 0;
      top: 884px;
      width: 1920px;''', '''    #v9-contacts {
      position: absolute;
      left: 0;
      top: 1172px;
      width: 1080px;'''),
    ('''    .v9-c {
      display: inline-block;
      margin: 0 30px;
    }''', '''    .v9-c {
      display: block;
      margin: 0 0 12px;
    }'''),
    # contacts wait for the last caption ("Gagnez du temps.") to leave the band
    ('tl.fromTo(["#v9-site", "#v9-wa"], { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, stagger: 0.12, ease: "expo.out" }, 2.2);',
     'tl.fromTo(["#v9-site", "#v9-wa"], { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, stagger: 0.12, ease: "expo.out" }, 3.25);'),
])
