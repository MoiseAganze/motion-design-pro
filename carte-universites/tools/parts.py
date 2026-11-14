# Shared pieces for the scene files (written out into self-contained HTML).

NAVY = "#0B2C5A"
BLUE = "#1957B8"
SKY = "#2F86E0"
YELLOW = "#FCD116"
RED = "#D21034"
GREEN = "#1E8E4A"
GROUND = "#F4F7FB"

ICON = {
    "cap": '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3Zm-7 10.2v4L12 21l7-3.8v-4L12 17l-7-3.8Z"/></svg>',
    "avatar": '<svg viewBox="0 0 200 250" preserveAspectRatio="xMidYMax meet"><circle cx="100" cy="98" r="50" fill="#AFC0D6"/><path d="M14 252c0-58 38-94 86-94s86 36 86 94Z" fill="#AFC0D6"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M5 12.5 9.5 17 19 7.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "x": '<svg viewBox="0 0 24 24"><path d="M6.5 6.5l11 11M17.5 6.5l-11 11" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.6"/><path d="M15.5 15.5 21 21" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M4.5 7.5h15M4.5 16.5h15"/></svg>',
    "db": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5.5" rx="7.5" ry="3"/><path d="M4.5 5.5v13c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-13"/><path d="M4.5 12c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3"/></svg>',
    "user": '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4.2" fill="currentColor"/><path d="M3.5 21c0-4.6 3.8-7.6 8.5-7.6s8.5 3 8.5 7.6Z" fill="currentColor"/></svg>',
    "bank": '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2.5 2.5 8v2h19V8L12 2.5ZM4.5 11.5v6h2.6v-6H4.5Zm4.5 0v6h2.6v-6H9Zm4.4 0v6H16v-6h-2.6Zm4.5 0v6h2.6v-6h-2.6ZM2.5 19v2.5h19V19h-19Z"/></svg>',
    "alert": '<svg viewBox="0 0 24 24"><path d="M12 6.5v7" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/><circle cx="12" cy="18" r="1.9" fill="currentColor"/></svg>',
}

CARD_CSS = f"""
.card {{ position: absolute; width: 860px; height: 540px; transform-style: preserve-3d; }}
.card .face {{ position: absolute; inset: 0; border-radius: 34px; background: #fff; overflow: hidden;
  backface-visibility: hidden; -webkit-backface-visibility: hidden;
  box-shadow: 0 30px 60px rgba(11,44,90,.28), 0 6px 14px rgba(11,44,90,.12); }}
.card .face.back {{ transform: rotateY(180deg); }}
.card .c-head {{ position: absolute; left: 0; right: 0; top: 0; height: 168px; background: linear-gradient(100deg,{BLUE},{SKY}); }}
.card .c-cap {{ position: absolute; left: 34px; top: 32px; width: 104px; height: 104px; border-radius: 50%; background: #fff;
  color: {BLUE}; display: flex; align-items: center; justify-content: center; }}
.card .c-cap svg {{ width: 60px; height: 60px; }}
.card .c-inst {{ position: absolute; left: 150px; right: 150px; top: 30px; text-align: center; color: #fff;
  font: 800 31px/1.1 Montserrat, sans-serif; letter-spacing: .02em; }}
.card .c-pill {{ position: absolute; left: 150px; right: 150px; top: 84px; display: flex; justify-content: center; }}
.card .c-pill span {{ background: #fff; color: {BLUE}; font: 800 19px/1 Montserrat, sans-serif; padding: 11px 20px;
  border-radius: 999px; letter-spacing: .04em; white-space: nowrap; }}
.card .c-seal {{ position: absolute; right: 30px; top: 30px; width: 108px; height: 108px; border-radius: 50%; background: #fff; padding: 4px; }}
.card .c-seal img {{ width: 100%; height: 100%; display: block; }}
.card .c-photo {{ position: absolute; left: 44px; top: 200px; width: 200px; height: 252px; border-radius: 14px; background: #DDE6F2; overflow: hidden; }}
.card .c-photo svg {{ position: absolute; left: 0; bottom: 0; width: 100%; height: 100%; }}
.card .c-name {{ position: absolute; left: 284px; top: 192px; font: 800 40px/1.2 Montserrat, sans-serif; color: {NAVY}; }}
.card .c-rows {{ position: absolute; left: 284px; right: 44px; top: 256px; }}
.card .c-row {{ display: flex; align-items: center; height: 38px; }}
.card .c-row b {{ width: 168px; font: 600 19px/1 'Open Sans', sans-serif; color: #4A5A70; }}
.card .c-row i {{ display: block; height: 14px; border-radius: 7px; background: #DCE3EC; }}
.card .c-status {{ position: absolute; right: 44px; bottom: 42px; font: 800 20px/1 'Open Sans', sans-serif; color: {GREEN}; }}
.card .c-tri {{ position: absolute; left: 0; right: 0; bottom: 0; height: 16px;
  background: linear-gradient(90deg,{SKY} 0 33.33%,{YELLOW} 33.33% 66.66%,{RED} 66.66%); }}
.card .b-head {{ position: absolute; left: 0; right: 0; top: 0; height: 124px; background: linear-gradient(100deg,{BLUE},{SKY});
  padding: 24px 40px 0; color: #fff; }}
.card .b-head h4 {{ font: 800 33px/1.1 Montserrat, sans-serif; letter-spacing: .02em; }}
.card .b-head p {{ font: 600 20px/1.4 'Open Sans', sans-serif; opacity: .92; margin-top: 6px; }}
.card .b-left {{ position: absolute; left: 40px; top: 160px; width: 400px; }}
.card .b-left b {{ display: block; font: 600 20px/1 'Open Sans', sans-serif; color: #4A5A70; margin-bottom: 12px; }}
.card .b-left i {{ display: block; height: 16px; border-radius: 8px; background: #DCE3EC; margin-bottom: 30px; }}
.card .b-left h5 {{ font: 800 24px/1.2 Montserrat, sans-serif; color: {NAVY}; margin-top: 4px; }}
.card .b-left p {{ font: 600 18px/1.35 'Open Sans', sans-serif; color: #4A5A70; margin-top: 6px; }}
.card .b-qr {{ position: absolute; right: 40px; top: 152px; width: 330px; height: 330px; padding: 14px; background: #fff;
  border-radius: 18px; border: 3px solid #E3EAF3; }}
.card .b-qr img {{ width: 100%; height: 100%; display: block; image-rendering: pixelated; }}
"""


def card_front(cid, status="Statut : valide"):
    return f"""<div class="face front" data-layout-ignore id="{cid}-front">
  <div class="c-head">
    <div class="c-cap">{ICON['cap']}</div>
    <div class="c-inst">NOM DE L'ÉTABLISSEMENT</div>
    <div class="c-pill"><span>CARTE NATIONALE D'ÉTUDIANT</span></div>
    <div class="c-seal"><img src="assets/img/seal.png" alt=""></div>
  </div>
  <div class="c-photo">{ICON['avatar']}</div>
  <div class="c-name">NOM Prénom</div>
  <div class="c-rows">
    <div class="c-row"><b>Numéro carte</b><i style="width:300px"></i></div>
    <div class="c-row"><b>Numéro national</b><i style="width:340px"></i></div>
    <div class="c-row"><b>Sexe</b><i style="width:60px"></i></div>
    <div class="c-row"><b>Année</b><i style="width:170px"></i></div>
    <div class="c-row"><b>Promotion</b><i style="width:110px"></i></div>
  </div>
  <div class="c-status">{status}</div>
  <div class="c-tri"></div>
</div>"""


def card_back(cid):
    return f"""<div class="face back" data-layout-ignore id="{cid}-back">
  <div class="b-head"><h4>CONDITIONS / VALIDATION</h4><p>Cette carte est personnelle et ne peut être cédée.</p></div>
  <div class="b-left">
    <b>Cycle / Mention</b><i style="width:360px"></i>
    <b>Niveau</b><i style="width:250px"></i>
    <h5>DÉLIVRÉE PAR LE MINISTÈRE</h5>
    <p>Vérifier le QR pour confirmer la validité.</p>
  </div>
  <div class="b-qr" id="{cid}-qr"><img src="assets/img/qr.svg" alt=""></div>
  <div class="c-tri"></div>
</div>"""


def scene(cid, css, body, js, extra_attrs=""):
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920"{extra_attrs}>
{body}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["{cid}"] = tl;
    }})();
  </script>
</template>
"""
