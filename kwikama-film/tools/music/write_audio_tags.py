"""Writes the music and sound-effect <audio> clips into index.html from assets/audio/sfx/cues.json."""
import json
import re
import sys

proj = sys.argv[1] if len(sys.argv) > 1 else "."
cues = json.load(open(f"{proj}/assets/audio/sfx/cues.json"))
lines = ['      <!-- musique originale (tools/music/compose.py), déjà atténuée sous la voix (tools/music/mixdown.py) -->',
         '      <audio id="music" class="clip" src="assets/audio/music/kwikama-theme.mp3" data-start="0" data-duration="127" data-track-index="21" data-volume="1"></audio>',
         '      <!-- bruitages : chaque son a une cause à l\'écran -->']
lane_end = []  # first free lane per effect, so overlapping effects sit on separate Studio lanes
for c in cues:
    lane = next((i for i, e in enumerate(lane_end) if e <= c["start"]), len(lane_end))
    if lane == len(lane_end):
        lane_end.append(0)
    lane_end[lane] = c["start"] + c["duration"]
    lines.append(f'      <audio id="{c["id"]}" class="clip" src="{c["src"]}" data-start="{c["start"]}" data-duration="{c["duration"]}" '
                 f'data-track-index="{22 + lane}" data-volume="{c["volume"]}"></audio>')
block = "      <!-- @AUDIO:BEGIN -->\n" + "\n".join(lines) + "\n      <!-- @AUDIO:END -->"
html = open(f"{proj}/index.html").read()
if "@AUDIO:BEGIN" in html:
    html = re.sub(r"      <!-- @AUDIO:BEGIN -->[\s\S]*?<!-- @AUDIO:END -->", block, html)
else:
    html = html.replace("    </div>\n    <script>", block + "\n    </div>\n    <script>", 1)
open(f"{proj}/index.html", "w").write(html)
print("wrote", len(cues), "effects")
