"""Builds compositions/v/captions.html (vertical cut) from the ElevenLabs alignment of
the voice take (times are take-relative; the voice starts at VO_OFFSET in the film).
Phone-number word times come from the energy map of the take (the aligner squashed them)."""
import html
VO_OFFSET = 0.56
GROUPS = [
    [("Répondre", .16, .56), ("aux", .64, .72), ("mêmes", .76, .96), ("e-mails…", 1.04, 1.8)],
    [("copier", 2.0, 2.32), ("les", 2.4, 2.48), ("mêmes", 2.52, 2.72), ("données…", 2.8, 3.44)],
    [("relancer,", 3.68, 4.48), ("encore", 4.64, 5.28), ("et", 5.44, 5.52), ("encore.", 5.64, 6.36)],
    [("Et", 6.768, 6.8), ("si", 6.88, 7.04), ("tout", 7.12, 7.28), ("ça…", 7.36, 7.88)],
    [("se", 8.08, 8.16), ("faisait", 8.2, 8.48), ("tout", 8.56, 8.64), ("seul ?", 8.72, 9.37)],
    [("Avec", 9.44, 9.68), ("n8n,", 9.76, 10.56)],
    [("vos", 10.64, 10.72), ("applications", 10.8, 11.28), ("se", 11.36, 11.52), ("parlent,", 11.6, 12.0)],
    [("et", 12.04, 12.08), ("vos", 12.16, 12.24), ("tâches", 12.32, 12.56), ("s'enchaînent", 12.64, 13.2)],
    [("automatiquement.", 13.36, 14.24)],
    [("Un", 14.28, 14.32), ("e-mail", 14.4, 14.64), ("arrive :", 14.76, 15.41)],
    [("il", 15.467, 15.52), ("est", 15.6, 15.68), ("lu,", 15.8, 16.16), ("analysé,", 16.32, 17.04), ("classé…", 17.24, 17.84)],
    [("et", 17.88, 17.92), ("la", 17.96, 18.0), ("réponse", 18.08, 18.4), ("part,", 18.48, 18.96)],
    [("toute", 19.013, 19.12), ("seule.", 19.2, 19.76)],
    [("Une", 19.84, 19.92), ("requête", 20.04, 20.24), ("arrive :", 20.32, 20.99)],
    [("la", 21.013, 21.04), ("base", 21.12, 21.28), ("de", 21.36, 21.44), ("données", 21.52, 21.68)],
    [("est", 21.76, 21.84), ("interrogée,", 21.92, 22.64)],
    [("et", 22.68, 22.72), ("le", 22.76, 22.8), ("résultat", 22.88, 23.28), ("est", 23.44, 23.52), ("renvoyé.", 23.64, 24.24)],
    [("Ces", 24.48, 24.56), ("workflows,", 24.64, 25.36)],
    [("c'est", 25.44, 25.6), ("VOUS", 25.68, 25.84)],
    [("qui", 25.92, 25.96), ("allez", 26.0, 26.187), ("les", 26.213, 26.24), ("construire.", 26.32, 27.12)],
    [("Étape", 27.2, 27.44), ("par", 27.52, 27.6), ("étape,", 27.68, 28.24)],
    [("jusqu'aux", 28.32, 28.72), ("agents", 28.88, 29.04), ("IA.", 29.12, 29.48)],
    [("La", 29.68, 29.76), ("formation", 29.84, 30.32)],
    [("Automatisation", 30.48, 31.28), ("n8n,", 31.44, 32.16)],
    [("organisée", 32.32, 32.72), ("par", 32.8, 32.88)],
    [("Chronoconcept", 32.96, 33.68), ("Group.", 33.76, 34.24)],
    [("Rendez-vous", 34.32, 34.72), ("à", 34.76, 34.8), ("Kinshasa,", 34.88, 35.6)],
    [("à", 35.64, 35.68), ("Silikin", 35.76, 36.16), ("Village.", 36.24, 36.84)],
    [("Le", 37.027, 37.04), ("formulaire", 37.12, 37.52), ("d'inscription", 37.547, 38.08)],
    [("et", 38.16, 38.24), ("tous", 38.32, 38.4), ("les", 38.44, 38.48), ("détails :", 38.56, 39.24)],
    [("lien", 39.28, 39.44), ("en", 39.52, 39.6), ("description.", 39.88, 40.32)],
    [("Des", 40.48, 40.56), ("questions ?", 40.64, 41.33)],
    [("Contactez-nous", 41.467, 41.84), ("sur", 41.92, 42.0)],
    [("chronoconcept.net,", 42.08, 43.52)],
    [("ou", 43.56, 43.6), ("sur", 43.68, 43.76), ("WhatsApp", 43.84, 44.32), ("au", 44.4, 44.56)],
    [("+243", 44.68, 45.42), ("853", 45.62, 46.38), ("420", 46.42, 46.88), ("317", 47.1, 48.08)],
    [("Automatisez", 48.56, 49.16), ("votre", 49.2, 49.36), ("travail.", 49.4, 50.08)],
    [("Gagnez", 50.16, 50.48), ("du", 50.52, 50.56), ("temps.", 50.64, 51.2)],
]
ACCENT = {"n8n,", "VOUS", "IA.", "Chronoconcept", "Group.", "Kinshasa,", "Silikin", "Village.", "description.", "chronoconcept.net,", "WhatsApp", "+243", "853", "420", "317", "temps."}

groups_html, js = [], []
for gi, g in enumerate(GROUPS):
    start = g[0][1] + VO_OFFSET - 0.08
    nxt = GROUPS[gi + 1][0][1] + VO_OFFSET - 0.08 if gi + 1 < len(GROUPS) else None
    end = g[-1][2] + VO_OFFSET + 0.3
    if nxt is not None:
        end = min(end, nxt - 0.02)
    spans = []
    for wi, (w, a, b) in enumerate(g):
        cls = ' class="vc-acc"' if w in ACCENT else ""
        spans.append(f'<span id="vc-{gi}-{wi}"{cls}>{html.escape(w)}</span>')
        js.append(f'      word("#vc-{gi}-{wi}", {a + VO_OFFSET:.2f});')
    groups_html.append(f'    <div class="vc-g" id="vc-{gi}"><div class="vc-box">{" ".join(spans)}</div></div>')
    js.append(f'      group("#vc-{gi}", {start:.2f}, {end:.2f});')

out = f'''<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      pointer-events: none;
      font-family: var(--font-display, "Poppins"), sans-serif;
    }}
    .vc-g {{
      position: absolute;
      left: 0;
      top: 1176px;
      width: 1080px;
      text-align: center;
      opacity: 0;
      overflow: visible;
    }}
    .vc-box {{
      display: inline-block;
      max-width: 940px;
      padding: 12px 30px 16px;
      border-radius: 22px;
      background: rgba(11, 42, 69, 0.92);
      box-shadow: 0 14px 34px rgba(11, 42, 69, 0.28);
      font-weight: 800;
      font-size: 58px;
      line-height: 1.16;
      letter-spacing: -0.01em;
      color: rgba(255, 255, 255, 0.5);
    }}
    .vc-box span {{
      display: inline-block;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(groups_html)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      // a group pops in just before its first word and is hard-killed after its last
      const group = (id, a, b) => {{
        tl.fromTo(id, {{ opacity: 0, y: 14, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.14, ease: "power2.out" }}, a);
        tl.to(id, {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, b - 0.08);
        tl.set(id, {{ opacity: 0, visibility: "hidden" }}, b);
      }};
      // each word lights up when it is spoken; names, places and contacts in cyan
      const word = (id, at) => {{
        const el = document.querySelector(id);
        const lit = el.classList.contains("vc-acc") ? "#3FD0E6" : "#FFFFFF";
        tl.set(id, {{ color: "rgba(255,255,255,0.5)" }}, 0);
        tl.set(id, {{ color: lit }}, at);
      }};
{chr(10).join(js)}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
'''
open("../formation-n8n-vertical/compositions/captions.html", "w").write(out)
print(len(GROUPS), "groups")
