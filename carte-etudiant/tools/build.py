import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from scenes_a import s1, s2, s3
from scenes_b import s4, s5
from scenes_c import s6, s7, s8

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.makedirs(OUT + "/compositions", exist_ok=True)

SCENES = [  # id, start, duration
    ("s1", 0.0, 7.55, s1),
    ("s2", 7.55, 2.07, s2),
    ("s3", 9.3, 3.95, s3),
    ("s4", 13.25, 5.8, s4),
    ("s5", 19.0, 4.35, s5),
    ("s6", 23.35, 4.15, s6),
    ("s7", 27.35, 5.5, s7),
    ("s8", 32.75, 5.25, s8),
]
TOTAL = 38.0

for cid, _, _, fn in SCENES:
    open(f"{OUT}/compositions/{cid}.html", "w").write(fn())

# ------------------------------------------------------------ captions (voice-timed, take 1)
# [text, start, end, keyword(s) to colour]
GROUPS = [
    ["et on te demande", 3.48, 4.16, ""],
    ["de PROUVER", 4.16, 4.8, "PROUVER"],
    ["que tu étais", 4.8, 5.32, ""],
    ["bien étudiant.", 5.32, 6.3, "étudiant."],
    ["Tu peux le prouver ?", 6.48, 7.42, "prouver ?"],
    ["Une carte en papier ?", 7.58, 8.61, "papier ?"],
    ["Ça ne suffit plus.", 8.61, 9.45, "plus."],
    ["Un QR code unique,", 13.28, 14.64, "QR code"],
    ["relié à la", 14.64, 15.2, ""],
    ["base nationale.", 15.2, 16.2, "base nationale."],
    ["Un scan…", 16.2, 17.08, "scan…"],
    ["et ton identité", 17.08, 17.84, "identité"],
    ["est vérifiée.", 17.84, 18.85, "vérifiée."],
    ["Mais si ton université", 23.48, 24.52, "université"],
    ["n'est pas encore", 24.52, 25.24, ""],
    ["sur la plateforme…", 25.24, 26.4, "plateforme…"],
    ["pas de carte pour toi.", 26.4, 27.45, "pas de carte"],
]


def cap_html(i, text, start, end, key):
    inner = text
    if key:
        inner = text.replace(key, f'<em>{key}</em>')
    return (f'      <div class="cap clip" id="cap{i}" data-start="{start}" data-duration="{round(end - start, 3)}" data-track-index="1">'
            f'<span class="capbox" id="capb{i}">{inner}</span></div>')


caps = "\n".join(cap_html(i, *g) for i, g in enumerate(GROUPS))
cap_js = "\n".join(
    f'      tl.fromTo("#capb{i}", {{ opacity: 0, scale: 0.9, y: 14 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {g[1]});'
    for i, g in enumerate(GROUPS))
CAPTIONS = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; width: 1080px; top: 1166px; height: 140px; display: flex; align-items: center; justify-content: center; }}
    .capbox {{ display: inline-block; max-width: 940px; text-align: center; background: #0B2C5A; color: #fff; border: 4px solid rgba(255,255,255,.92);
      border-radius: 22px; padding: 16px 32px 20px; font: 800 62px/1.1 Montserrat, sans-serif; letter-spacing: -0.01em;
      box-shadow: 0 16px 34px rgba(11,44,90,.32); }}
    .capbox em {{ font-style: normal; color: #FCD116; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{caps}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{cap_js}
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
open(f"{OUT}/compositions/captions.html", "w").write(CAPTIONS)

# ------------------------------------------------------------ sound
PEAK = {"pop": .12, "ping": .324, "chime": .418, "error": .745, "whoosh": .162, "whoosh-short": .162, "sparkle": .027,
        "impact-bass-1": .073, "impact-bass-2": 1.986, "glitch-1": .1, "click": .02, "typing": 0.0, "key-press": 0.0}
DUR = {"pop": .72, "ping": 1.32, "chime": 2.544, "error": 1.62, "whoosh": .575, "whoosh-short": .575, "sparkle": 1.802,
       "impact-bass-1": 2.116, "impact-bass-2": 2.592, "glitch-1": 2.638, "click": .37, "typing": 1.5, "key-press": .4}
# (name, picture time the hit belongs to, volume, label)
CUES = [
    ("pop", 1.6, .32, "coche 1"), ("pop", 2.0, .32, "coche 2"), ("pop", 2.4, .32, "coche 3"),
    ("error", 4.36, .28, "preuve manquante"),
    ("impact-bass-2", 6.48, .5, "point d'interrogation"),
    ("whoosh-short", 7.4, .42, "whip vers le papier"),
    ("impact-bass-1", 8.8, .55, "tampon"),
    ("whoosh", 9.55, .42, "balayage tricolore"),
    ("sparkle", 10.6, .28, "reflet sur la carte"),
    ("pop", 11.9, .32, "plaque Ministère"),
    ("whoosh-short", 13.8, .34, "carte retournée"),
    ("ping", 15.36, .32, "base nationale"),
    ("whoosh", 16.15, .34, "téléphone"),
    ("click", 16.3, .3, "scan"),
    ("chime", 17.95, .4, "carte valide"),
    ("whoosh-short", 18.85, .38, "écran plein cadre"),
    ("sparkle", 20.0, .26, "26 cartes"),
    ("ping", 21.08, .36, "26"),
    ("pop", 22.8, .38, "la norme"),
    ("glitch-1", 23.36, .28, "coupe glitch"),
    ("typing", 23.68, .26, "frappe recherche"),
    ("error", 25.56, .32, "non inscrite"),
    ("impact-bass-2", 26.4, .45, "aucune carte"),
    ("whoosh", 27.55, .4, "aplat jaune"),
    ("impact-bass-1", 27.84, .55, "bouge"),
    ("whoosh-short", 29.05, .36, "ton délégué"),
    ("whoosh", 29.9, .34, "ton secrétariat"),
    ("impact-bass-2", 31.96, .55, "maintenant"),
    ("whoosh", 32.9, .32, "iris blanc"),
    ("typing", 32.95, .24, "url 1"), ("typing", 34.45, .24, "url 2"),
    ("sparkle", 35.4, .28, "bandeau final"),
]
audio = []
for k, (name, t, vol, label) in enumerate(CUES):
    start = round(max(0.0, t + 1 / 30 - PEAK[name]), 3)
    audio.append(f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{name}.mp3" data-start="{start}" data-duration="{DUR[name]}" '
                 f'data-track-index="{11 + k % 3}" data-volume="{vol}"></audio><!-- {label} -->')

hosts = []
for z, (cid, st, du, _) in enumerate(SCENES, 1):
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" '
                 f'data-duration="{du}" data-track-index="{1 + (z - 1) % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{z}"></div>')

INDEX = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Carte Nationale de l'Étudiant — TikTok</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #F4F7FB; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #F4F7FB; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}"
        data-track-index="4" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:50"></div>
      <audio id="voix" class="clip" src="assets/audio/voix.mp3" data-start="0" data-duration="35.36" data-track-index="10" data-volume="1"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
open(f"{OUT}/index.html", "w").write(INDEX)
print("built", len(SCENES), "scenes,", len(GROUPS), "caption groups,", len(CUES), "sfx")
