from parts import ICON, CARD_CSS, card_front, card_back, scene  # noqa: F401  (re-exported)

ICON = dict(ICON)
ICON["shield"] = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5l-8-3Zm-1.2 14.2-3.6-3.6 1.4-1.4 2.2 2.2 5-5 1.4 1.4-6.4 6.4Z"/></svg>'
ICON["lock"] = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M7 10V7a5 5 0 0 1 10 0v3h1.5v11h-13V10H7Zm2 0h6V7a3 3 0 0 0-6 0v3Z"/></svg>'
ICON["warn"] = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2 1 21h22L12 2Zm-1 7h2v6h-2V9Zm0 8h2v2h-2v-2Z"/></svg>'
ICON["print"] = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M6 2h12v5H6V2Zm-2 6h16a2 2 0 0 1 2 2v7h-4v5H6v-5H2v-7a2 2 0 0 1 2-2Zm4 8v4h8v-4H8Z"/></svg>'
ICON["file"] = '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M6 2h8l6 6v14H6V2Zm8 1.5V9h5.5L14 3.5Z"/></svg>'

GRAD = "linear-gradient(100deg,#1957B8,#2F86E0)"

PHONE_CSS = r"""
    .phone { position: absolute; width: 470px; height: 940px; border-radius: 70px; background: #E8EEF7; box-shadow: 0 40px 80px rgba(11,44,90,.32); }
    .phone .scr { position: absolute; inset: 16px; border-radius: 54px; background: #fff; overflow: hidden; }
    .phone .notch { position: absolute; left: 50%; top: 16px; width: 130px; height: 30px; margin-left: -65px; border-radius: 15px; background: #0B2C5A; }
    .phone .sh { position: absolute; left: 0; right: 0; top: 0; height: 130px; background: linear-gradient(100deg,#1957B8,#2F86E0);
      color: #fff; font: 800 38px/1 Montserrat, sans-serif; text-align: center; padding-top: 66px; }
    .phone .vf { position: absolute; left: 34px; top: 160px; width: 370px; height: 370px; border-radius: 26px; background: #14263F; overflow: hidden;
      border: 6px solid #14263F; }
    .phone .cn { position: absolute; width: 54px; height: 54px; border-color: #FCD116; border-style: solid; border-width: 0; }
    .phone .scan { position: absolute; left: 14px; right: 14px; top: 0; height: 90px;
      background: linear-gradient(to bottom, rgba(59,227,138,0), rgba(59,227,138,.35)); border-bottom: 5px solid #3BE38A; }
    .phone .hint { position: absolute; left: 30px; right: 30px; top: 566px; text-align: center; font: 600 28px/1.3 'Open Sans', sans-serif; color: #4A5A70; }
    .phone .ric { position: absolute; left: 159px; top: 562px; width: 120px; height: 120px; border-radius: 50%; color: #fff; opacity: 0; }
    .phone .ric svg { position: absolute; inset: 20px; width: 80px; height: 80px; }
    .phone .rt { position: absolute; left: 20px; right: 20px; top: 704px; text-align: center; opacity: 0; }
    .phone .rt b { display: block; font: 900 36px/1.1 Montserrat, sans-serif; }
    .phone .rt span { display: block; margin-top: 12px; font: 600 26px/1.25 'Open Sans', sans-serif; color: #4A5A70; }
    .vtile { position: absolute; left: 50px; top: 50px; width: 258px; height: 258px; background: #fff; border-radius: 14px; padding: 16px; }
    .vtile img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
"""

CORNERS = (
    '<div class="cn" style="left:18px;top:18px;border-left-width:7px;border-top-width:7px;border-top-left-radius:16px"></div>'
    '<div class="cn" style="right:18px;top:18px;border-right-width:7px;border-top-width:7px;border-top-right-radius:16px"></div>'
    '<div class="cn" style="left:18px;bottom:18px;border-left-width:7px;border-bottom-width:7px;border-bottom-left-radius:16px"></div>'
    '<div class="cn" style="right:18px;bottom:18px;border-right-width:7px;border-bottom-width:7px;border-bottom-right-radius:16px"></div>'
)


def phone(pid, vf_inner, hint, ok, icon, title, sub, style):
    color = "#1E8E4A" if ok else "#D21034"
    return f"""<div class="phone" id="{pid}" style="{style}">
  <div class="scr">
    <div class="sh">Vérification</div>
    <div class="notch"></div>
    <div class="vf" id="{pid}-vf">{vf_inner}{CORNERS}<div class="scan" id="{pid}-scan"></div></div>
    <div class="hint" id="{pid}-hint">{hint}</div>
    <div class="ric" id="{pid}-ric" style="background:{color}">{ICON[icon]}</div>
    <div class="rt" id="{pid}-rt"><b style="color:{color}">{title}</b><span>{sub}</span></div>
  </div>
</div>"""


def wipe(prefix):
    css = f"""
    #{prefix}-wipe {{ position: absolute; left: -760px; top: -340px; width: 2600px; height: 2600px; transform: rotate(-18deg); }}
    .{prefix}-band {{ position: absolute; inset: 0; }}
"""
    html = f"""    <div id="{prefix}-wipe">
      <div class="{prefix}-band" id="{prefix}-w1" style="background:#2F86E0"></div>
      <div class="{prefix}-band" id="{prefix}-w2" style="background:#FCD116"></div>
      <div class="{prefix}-band" id="{prefix}-w3" style="background:#D21034"></div>
      <div class="{prefix}-band" id="{prefix}-w4" style="background:#0B2C5A"></div>
    </div>"""
    js = f"""
      ["#{prefix}-w1", "#{prefix}-w2", "#{prefix}-w3", "#{prefix}-w4"].forEach((s, i) => {{
        tl.fromTo(s, {{ xPercent: -105 }}, {{ xPercent: 0, duration: 0.48, ease: "power3.inOut" }}, i * 0.07);
      }});
"""
    return css, html, js


SHAKE_JS = r"""
      const shake = (sel, t, a) => tl.to(sel, { keyframes: [{ x: a, y: -a / 2, duration: 0.04 }, { x: -a * 0.8, y: a / 2, duration: 0.05 }, { x: a * 0.5, y: -a / 4, duration: 0.05 }, { x: 0, y: 0, duration: 0.06 }] }, t);
"""

BLURIN = '{ opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power3.out" }'
