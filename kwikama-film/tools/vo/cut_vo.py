"""Cut the ElevenLabs take into one clip per sentence group and place them on the film's clock.

Usage: python cut_vo.py <take.wav> <words.json> <project_dir>

Writes assets/audio/vo/voNN.wav (untreated cuts), assets/audio/vo/segments.json and
assets/audio/vo/words_film.json (every word with its time on the film's clock).
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

TAKE, WORDS, PROJ = sys.argv[1], sys.argv[2], sys.argv[3]
# first word of each paragraph, and where it starts on the film's clock (seconds)
PLAN = [
    ("Kolwezi.", 0.8), ("Six", 8.9), ("KWIKAMA", 14.3), ("Premier", 23.8), ("Rien", 30.2),
    ("Le", 41.3), ("Deuxième", 49.4), ("184", 57.3), ("Troisième", 68.6), ("Elle", 75.3),
    ("C'est", 87.6), ("Quatrième", 95.0), ("L'arrêté", 99.8), ("Vu", 110.4), ("Cinquième", 122.4),
    ("Au", 131.2), ("KWIKAMA.", 144.4),
]
x, sr = sf.read(TAKE, always_2d=True)
x = x.mean(axis=1)
words = [w for w in json.load(open(WORDS))["words"] if w["type"] == "word"]

# paragraph index of each word
starts, k = [], 0
for i, w in enumerate(words):
    if k < len(PLAN) and w["text"] == PLAN[k][0] and (k == 0 or i > starts[-1]):
        starts.append(i)
        k += 1
assert len(starts) == len(PLAN), (len(starts), [words[i]["text"] for i in starts])

hop = int(0.01 * sr)
rms = np.array([np.sqrt((x[i:i + hop] ** 2).mean() + 1e-12) for i in range(0, len(x), hop)])
db = 20 * np.log10(rms)


def quietest(a, b):
    """middle of the longest run of the quietest 10 ms frames between a and b (seconds)."""
    ia, ib = int(a * 100), max(int(a * 100) + 1, int(b * 100))
    seg = db[ia:ib]
    thr = seg.min() + 4
    best, cur, bs = (0, ia), 0, ia
    for j, v in enumerate(seg):
        if v <= thr:
            if cur == 0:
                bs = ia + j
            cur += 1
            if cur > best[0]:
                best = (cur, bs)
        else:
            cur = 0
    return (best[1] + best[0] / 2) / 100


cuts = [0.0]
for p in range(1, len(starts)):
    prev_last = words[starts[p] - 1]
    nxt = words[starts[p]]
    # the aligner's word ends run late; search from the middle of the last word to the next word's start
    a = (prev_last["start"] + prev_last["end"]) / 2
    cuts.append(quietest(a, nxt["start"] + 0.06))
cuts.append(len(x) / sr)

os.makedirs(os.path.join(PROJ, "assets/audio/vo"), exist_ok=True)
segs, film_words = [], []
fade = int(0.012 * sr)
for p, (first, at) in enumerate(PLAN):
    a, b = cuts[p], cuts[p + 1]
    y = x[int(a * sr):int(b * sr)].copy()
    # trim leading/trailing silence below -50 dB, keep 40 ms of air
    env = np.abs(y)
    on = np.where(env > 10 ** (-50 / 20))[0]
    lo = max(0, on[0] - int(0.04 * sr)) if len(on) else 0
    hi = min(len(y), on[-1] + int(0.08 * sr)) if len(on) else len(y)
    y = y[lo:hi]
    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)
    src0 = a + lo / sr
    vid = f"vo{p + 1:02d}"
    path = f"assets/audio/vo/{vid}.wav"
    sf.write(os.path.join(PROJ, path), y.astype(np.float32), sr, subtype="PCM_16")
    dur = len(y) / sr
    segs.append({"id": vid, "file": path, "src": [round(src0, 3), round(src0 + dur, 3)], "start": at, "dur": round(dur, 3), "end": round(at + dur, 3)})
    last = starts[p + 1] if p + 1 < len(starts) else len(words)
    for w in words[starts[p]:last]:
        film_words.append({"seg": vid, "text": w["text"], "start": round(at + w["start"] - src0, 3), "end": round(at + w["end"] - src0, 3)})

for s, t in zip(segs, segs[1:]):
    gap = t["start"] - s["end"]
    flag = "  <-- OVERLAP" if gap < 0.25 else ""
    print(f'{s["id"]} {s["start"]:7.2f} -> {s["end"]:7.2f}  ({s["dur"]:.2f}s)  gap {gap:5.2f}{flag}')
s = segs[-1]
print(f'{s["id"]} {s["start"]:7.2f} -> {s["end"]:7.2f}  ({s["dur"]:.2f}s)')
json.dump(segs, open(os.path.join(PROJ, "assets/audio/vo/segments.json"), "w"), indent=1)
json.dump(film_words, open(os.path.join(PROJ, "assets/audio/vo/words_film.json"), "w"), ensure_ascii=False, indent=0)
