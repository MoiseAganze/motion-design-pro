import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from u_a import u1, u2, u3
from u_b import u4
from u_c import u5, u6
from u_d import u7, u8, u9

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.makedirs(OUT + "/compositions", exist_ok=True)

SCENES = [  # id, start, duration
    ("u1", 0.0, 7.85, u1),
    ("u2", 7.85, 7.0, u2),
    ("u3", 14.6, 8.35, u3),
    ("u4", 22.9, 12.95, u4),
    ("u5", 35.8, 7.4, u5),
    ("u6", 43.0, 2.3, u6),
    ("u7", 45.2, 8.05, u7),
    ("u8", 53.2, 3.75, u8),
    ("u9", 56.8, 7.7, u9),
]
TOTAL = 64.5
VOICE_DUR = 61.76

for cid, _, _, fn in SCENES:
    open(f"{OUT}/compositions/{cid}.html", "w").write(fn())

# [text, start, end, keyword]  — timed on the ElevenLabs alignment of take 2
GROUPS = [
    ["Votre établissement", 3.52, 4.28, ""],
    ["n'apparaît pas", 4.28, 4.88, "n'apparaît pas"],
    ["dans la base nationale…", 4.88, 6.28, "base nationale…"],
    ["et vos étudiants non plus.", 6.28, 7.8, "non plus."],
    ["Cartes artisanales,", 7.98, 9.12, "artisanales,"],
    ["formats différents,", 9.12, 10.2, "différents,"],
    ["aucune vérification", 10.2, 11.2, "vérification"],
    ["possible :", 11.2, 12.08, ""],
    ["c'est la crédibilité", 12.08, 13.0, "crédibilité"],
    ["de votre établissement", 13.0, 14.08, ""],
    ["qui en souffre.", 14.08, 14.85, "souffre."],
    ["Le Ministère de l'ESURSI", 15.0, 16.32, "l'ESURSI"],
    ["met à votre disposition", 16.32, 17.6, ""],
    ["ESURSI Connect :", 17.6, 18.85, "ESURSI Connect"],
    ["la plateforme nationale", 18.85, 20.0, "nationale"],
    ["de production", 20.0, 20.64, ""],
    ["des cartes d'étudiant.", 20.64, 21.88, "cartes d'étudiant."],
    ["Et c'est simple.", 21.88, 22.9, "simple."],
    ["Définissez", 22.96, 23.49, ""],
    ["votre année académique", 23.49, 24.64, "année académique"],
    ["et vos mentions.", 24.64, 25.76, "mentions."],
    ["Importez vos étudiants", 25.76, 26.72, "Importez"],
    ["depuis un fichier", 26.72, 27.44, ""],
    ["Excel ou CSV :", 27.44, 29.07, "Excel ou CSV"],
    ["les doublons sont détectés", 29.07, 30.48, "doublons"],
    ["automatiquement.", 30.48, 31.4, "automatiquement."],
    ["Puis générez et imprimez", 31.4, 33.12, "générez"],
    ["les cartes, recto verso,", 33.12, 34.56, "recto verso,"],
    ["en quelques clics.", 34.56, 35.84, "quelques clics."],
    ["Chaque carte porte", 35.84, 36.88, ""],
    ["un QR code unique,", 36.88, 38.08, "QR code"],
    ["relié à la base nationale :", 38.08, 39.76, "base nationale"],
    ["vérifiable partout,", 39.76, 41.12, "partout,"],
    ["24 heures sur 24.", 41.12, 42.68, "24 heures sur 24."],
    ["Et vous pilotez tout", 42.68, 43.92, "pilotez"],
    ["depuis votre tableau de bord.", 43.92, 45.2, "tableau de bord."],
    ["peuvent émettre ces cartes.", 47.56, 49.05, "émettre"],
    ["Connectez votre établissement", 56.96, 58.16, "Connectez"],
    ["dès aujourd'hui.", 58.16, 59.15, "aujourd'hui."],
]


def cap_html(i, text, start, end, key):
    inner = text.replace(key, f"<em>{key}</em>") if key else text
    return (f'      <div class="cap clip" id="cap{i}" data-start="{start}" data-duration="{round(end - start, 3)}" data-track-index="1">'
            f'<span class="capbox" id="capb{i}">{inner}</span></div>')


caps = "\n".join(cap_html(i, *g) for i, g in enumerate(GROUPS))
cap_js = "\n".join(
    f'      tl.fromTo("#capb{i}", {{ opacity: 0, scale: 0.9, y: 14 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "power3.out" }}, {g[1]});'
    for i, g in enumerate(GROUPS))
open(f"{OUT}/compositions/captions.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; width: 1080px; top: 1166px; height: 140px; display: flex; align-items: center; justify-content: center; }}
    .capbox {{ display: inline-block; max-width: 960px; text-align: center; background: #0B2C5A; color: #fff; border: 4px solid rgba(255,255,255,.92);
      border-radius: 22px; padding: 16px 32px 20px; font: 800 56px/1.1 Montserrat, sans-serif; letter-spacing: -0.01em; white-space: nowrap;
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
""")

PEAK = {"pop": .12, "ping": .324, "chime": .418, "error": .745, "whoosh": .162, "whoosh-short": .162, "sparkle": .027,
        "impact-bass-1": .073, "impact-bass-2": 1.986, "glitch-1": .1, "click": .02, "typing": 0.0, "key-press": 0.0}
DUR = {"pop": .72, "ping": 1.32, "chime": 2.544, "error": 1.62, "whoosh": .575, "whoosh-short": .575, "sparkle": 1.802,
       "impact-bass-1": 2.116, "impact-bass-2": 2.592, "glitch-1": 2.638, "click": .37, "typing": 1.5, "key-press": .4}
CUES = [
    ("click", 0.3, .3, "scan"), ("error", 2.72, .32, "rien"), ("whoosh-short", 3.5, .36, "téléphone sort"),
    ("impact-bass-1", 4.3, .4, "absent"), ("pop", 6.3, .3, "étudiants"),
    ("whoosh-short", 8.1, .36, "cartes papier"), ("impact-bass-1", 10.56, .5, "tampon"),
    ("whoosh", 12.4, .3, "crédibilité"), ("glitch-1", 14.27, .3, "fissure"),
    ("whoosh", 14.85, .4, "balayage"), ("pop", 15.2, .3, "plaque"), ("sparkle", 17.65, .26, "ESURSI Connect"),
    ("typing", 18.85, .24, "email"), ("click", 21.35, .32, "se connecter"), ("whoosh", 22.6, .4, "plongée bouton"),
    ("click", 23.72, .3, "année"), ("pop", 24.82, .26, "mention 1"), ("pop", 25.02, .26, "mention 2"), ("pop", 25.22, .26, "mention 3"),
    ("whoosh-short", 25.75, .3, "étape 2"), ("whoosh", 27.1, .34, "fichier excel"), ("pop", 27.62, .3, "csv"),
    ("ping", 29.2, .34, "doublons"), ("whoosh-short", 31.38, .3, "étape 3"), ("click", 31.84, .32, "générer"),
    ("sparkle", 32.0, .26, "cartes"), ("click", 32.7, .3, "imprimer"), ("whoosh", 34.15, .34, "recto verso"), ("chime", 34.75, .36, "imprimée"),
    ("whoosh-short", 36.95, .34, "zoom qr"), ("ping", 38.84, .32, "base nationale"), ("whoosh", 39.75, .34, "téléphone"),
    ("chime", 40.4, .36, "carte valide"), ("pop", 41.15, .34, "24h"), ("whoosh-short", 43.05, .36, "dashboard"),
    ("sparkle", 43.2, .24, "compteurs"),
    ("whoosh-short", 45.3, .32, "carte"), ("impact-bass-1", 46.96, .5, "agréé"), ("whoosh", 47.95, .3, "cartes émises"),
    ("whoosh", 49.05, .38, "aplat jaune"), ("impact-bass-2", 51.32, .45, "responsabilité"),
    ("glitch-1", 53.22, .26, "coupe"), ("pop", 54.24, .32, "bulle 1"), ("pop", 54.44, .32, "bulle 2"), ("pop", 54.64, .32, "bulle 3"),
    ("whoosh", 55.7, .38, "souffle"), ("impact-bass-1", 56.2, .55, "les devants"),
    ("whoosh", 56.9, .32, "iris blanc"), ("click", 57.3, .3, "rescan"), ("chime", 57.85, .38, "reconnu"),
    ("typing", 59.3, .22, "url 1"), ("typing", 60.8, .22, "url 2"), ("sparkle", 62.0, .26, "bandeau"),
]
audio = []
for k, (name, t, vol, label) in enumerate(CUES):
    start = round(max(0.0, t + 1 / 30 - PEAK[name]), 3)
    audio.append(f'      <audio id="sfx{k}" class="clip" src="assets/sfx/{name}.mp3" data-start="{start}" data-duration="{DUR[name]}" '
                 f'data-track-index="{11 + k % 4}" data-volume="{vol}"></audio><!-- {label} -->')

hosts = []
for z, (cid, st, du, _) in enumerate(SCENES, 1):
    hosts.append(f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" '
                 f'data-duration="{du}" data-track-index="{1 + (z - 1) % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index:{z}"></div>')

open(f"{OUT}/index.html", "w").write(f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Carte Nationale de l'Étudiant — Universités</title>
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
      <audio id="voix" class="clip" src="assets/audio/voix.mp3" data-start="0" data-duration="{VOICE_DUR}" data-track-index="10" data-volume="1"></audio>
{chr(10).join(audio)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", len(SCENES), "scenes,", len(GROUPS), "captions,", len(CUES), "sfx")
