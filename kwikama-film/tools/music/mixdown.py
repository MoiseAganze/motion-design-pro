"""Mixdown helper for the KWIKAMA film.

- processes the voice-over segments (compression, presence, level),
- ducks the composed music under the voice and sets its level,
- prepares the sound effects (trimmed foley + bundled Pixabay effects, pitch variants),
- writes the cue list used by index.html and a reference mix to measure loudness.

Usage: python mixdown.py <project_dir> <music_free.wav> <work_dir>
"""
import json
import os
import shutil
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from pedalboard import Compressor, HighpassFilter, Limiter, Pedalboard, PeakFilter, PitchShift, Gain
from scipy.signal import resample_poly

SR = 48000
DUR = 127.0
N = int(DUR * SR)
PROJ, MUSIC_FREE, WORK = sys.argv[1], sys.argv[2], sys.argv[3]
SFX_LIB = os.path.join(PROJ, "..", ".claude", "skills", "media-use", "audio", "assets", "sfx")
os.makedirs(os.path.join(PROJ, "assets/audio/sfx"), exist_ok=True)
os.makedirs(os.path.join(PROJ, "assets/audio/music"), exist_ok=True)
meter = pyln.Meter(SR)


def load(path, mono=False):
    x, sr = sf.read(path, always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    if mono:
        x = x.mean(axis=1, keepdims=True)
    return x


# ---------------- voice ----------------
segs = json.load(open(os.path.join(PROJ, "assets/audio/vo/segments.json")))
raw_dir = os.path.join(WORK, "vo_raw")
os.makedirs(raw_dir, exist_ok=True)
vo_track = np.zeros((N, 1))
chain = Pedalboard([HighpassFilter(85), Compressor(threshold_db=-24, ratio=2.6, attack_ms=8, release_ms=140), PeakFilter(3000, 1.8, 0.9), PeakFilter(220, -1.5, 1.0)])
proc = {}
for s in segs:
    src = os.path.join(raw_dir, s["id"] + ".wav")
    if not os.path.exists(src):
        shutil.copy(os.path.join(PROJ, s["file"]), src)   # keep the untouched cut once
    x = load(src, mono=True)
    y = chain(x.T.astype(np.float32), SR).T
    proc[s["id"]] = y
    i = int(round(s["start"] * SR))
    vo_track[i:i + len(y)] += y[: N - i]
speech = np.concatenate([proc[s["id"]] for s in segs])
# mono file, played on both channels: -19 LUFS measured mono ~ -16 LUFS in stereo playback
g_vo = 10 ** ((-19.0 - meter.integrated_loudness(speech)) / 20)


def soft_limit(y, ceiling_db=-3.0, release=0.06):
    """peak limiter: instant attack, smooth release."""
    c = 10 ** (ceiling_db / 20)
    need = np.minimum(1.0, c / np.maximum(np.abs(y[:, 0]), 1e-9))
    g = np.ones_like(need)
    k = np.exp(-1 / (release * SR))
    cur = 1.0
    for i in range(len(need)):
        cur = need[i] if need[i] < cur else cur * k + (1 - k) * need[i]
        g[i] = cur
    return y * g[:, None]


vo_track[:] = 0
for s in segs:
    y = soft_limit(proc[s["id"]] * g_vo)
    sf.write(os.path.join(PROJ, s["file"]), y.astype(np.float32), SR, subtype="PCM_16")
    i = int(round(s["start"] * SR))
    vo_track[i:i + len(y)] += y[: N - i]

# ---------------- music, ducked under the voice ----------------
music = load(MUSIC_FREE)
music = np.pad(music, ((0, max(0, N - len(music))), (0, 0)))[:N]
hop = int(0.02 * SR)
env = np.array([np.sqrt((vo_track[i:i + hop] ** 2).mean()) for i in range(0, N, hop)])
active = (20 * np.log10(env + 1e-9) > -42).astype(float)
# hold short gaps between words, then smooth (attack 80 ms, release 450 ms)
hold = int(0.35 / 0.02)
act = active.copy()
for i in range(len(active)):
    if active[max(0, i - hold):i + 1].any():
        act[i] = 1.0
sm = np.zeros_like(act)
a_up, a_dn = 1 - np.exp(-0.02 / 0.08), 1 - np.exp(-0.02 / 0.45)
v = 0.0
for i, a in enumerate(act):
    v += (a - v) * (a_up if a > v else a_dn)
    sm[i] = v
DUCK_DB = 11.0
duck = 1 - (1 - 10 ** (-DUCK_DB / 20)) * sm
duck_s = np.repeat(duck, hop)[:N]
# overall music level: free sections around -17 LUFS short-term
free = (np.repeat(sm, hop)[:N] < 0.05)
g_mus = 10 ** ((-18.0 - meter.integrated_loudness(music[free])) / 20)
music_d = music * g_mus * duck_s[:, None]

# ---------------- sound effects ----------------
def sfx_src(name):
    return os.path.join(SFX_LIB, name + ".mp3")


def prep(name, src, trim=(0, None), pitch=0.0, gain_db=0.0, fade_out=0.02):
    x = load(src, mono=True)
    a = int(trim[0] * SR)
    b = len(x) if trim[1] is None else int(trim[1] * SR)
    x = x[a:b]
    if pitch:
        x = PitchShift(semitones=pitch)(x.T.astype(np.float32), SR).T
    x = x * 10 ** (gain_db / 20)
    fo = int(fade_out * SR)
    x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    path = f"assets/audio/sfx/{name}.wav"
    sf.write(os.path.join(PROJ, path), x.astype(np.float32), SR, subtype="PCM_16")
    return path, len(x) / SR


FOLEY = os.path.join(WORK, "..", "sfx")
lib = {
    "click": prep("click", sfx_src("click-soft")),
    "pop": prep("pop", sfx_src("pop")),
    "pop-hi": prep("pop-hi", sfx_src("pop"), pitch=3),
    "pop-lo": prep("pop-lo", sfx_src("pop"), pitch=-3),
    "key": prep("key", sfx_src("key-press")),
    "typing": prep("typing", sfx_src("typing")),
    "whoosh": prep("whoosh", sfx_src("whoosh")),
    "whoosh-short": prep("whoosh-short", sfx_src("whoosh-short")),
    "whoosh-cine": prep("whoosh-cine", sfx_src("whoosh-cinematic"), trim=(0, 2.4), fade_out=0.4),
    "stamp": prep("stamp", os.path.join(FOLEY, "stamp1.wav"), trim=(1.255, 1.95), fade_out=0.15),
    "envelope": prep("envelope", os.path.join(FOLEY, "env1.wav"), trim=(0.25, 2.6), fade_out=0.2),
}
# (time, effect, volume) — every cue has a cause on screen
CUES = [
    (1.48, "envelope", 1.6), (7.58, "pop-lo", 0.35), (9.18, "whoosh", 0.45),
    (17.2, "whoosh-cine", 0.35), (19.92, "pop-lo", 0.25), (21.35, "pop", 0.3), (21.75, "pop-hi", 0.22), (22.2, "pop-hi", 0.22),
    (22.95, "key", 0.4), (23.15, "key", 0.4), (23.35, "key", 0.45), (23.45, "pop", 0.3), (23.78, "whoosh-short", 0.25),
    (25.9, "stamp", 1.0),
    (32.95, "whoosh-cine", 0.28), (36.05, "whoosh-short", 0.3), (37.2, "whoosh", 0.35),
    (40.05, "whoosh-short", 0.3), (43.6, "click", 0.7), (44.55, "click", 0.7), (45.6, "click", 0.7), (45.66, "whoosh-short", 0.2),
    (47.55, "click", 0.7), (48.95, "click", 0.7), (50.35, "click", 0.7), (50.98, "click", 0.65), (51.65, "click", 0.75),
    (52.55, "whoosh-short", 0.3), (53.45, "whoosh-short", 0.3), (54.0, "key", 0.3), (54.2, "key", 0.3), (54.38, "key", 0.3), (54.56, "key", 0.32),
    (56.45, "click", 0.7), (58.6, "pop-hi", 0.22), (59.45, "pop-hi", 0.22), (60.78, "click", 0.7),
    (61.7, "whoosh-short", 0.25), (62.5, "whoosh-short", 0.25), (64.4, "pop", 0.25), (64.6, "pop", 0.25), (65.15, "pop-hi", 0.28), (65.35, "pop-hi", 0.28),
    (66.15, "whoosh-short", 0.25), (67.25, "click", 0.7),
    (67.8, "whoosh-cine", 0.4), (73.05, "pop-lo", 0.22), (73.5, "pop-lo", 0.22), (73.95, "pop-lo", 0.22), (75.5, "pop-lo", 0.22), (77.65, "pop-lo", 0.22),
    (79.8, "whoosh-short", 0.3),
    (81.94, "stamp", 0.9), (82.6, "typing", 0.45), (84.5, "whoosh-short", 0.22), (85.05, "pop-hi", 0.2), (85.6, "pop-hi", 0.2), (86.15, "pop-hi", 0.2),
    (86.45, "whoosh", 0.35), (88.35, "pop", 0.22), (89.2, "whoosh-short", 0.25),
    (89.9, "pop-lo", 0.22), (90.9, "pop-lo", 0.22), (92.0, "pop-lo", 0.22), (92.8, "pop-lo", 0.22), (93.35, "pop-lo", 0.22), (93.6, "whoosh", 0.35), (96.55, "pop", 0.28),
    (98.3, "whoosh-cine", 0.38),
    (99.4, "pop-hi", 0.2), (100.0, "pop-hi", 0.2), (100.9, "pop-hi", 0.22), (101.9, "pop-hi", 0.22), (103.2, "pop-hi", 0.24), (103.9, "pop", 0.26),
    (105.35, "whoosh", 0.32), (107.75, "whoosh-short", 0.25), (108.25, "key", 0.28), (108.8, "key", 0.28), (109.3, "key", 0.28), (111.0, "whoosh-short", 0.22),
    (113.95, "whoosh-short", 0.25), (114.72, "whoosh-cine", 0.4),
    (121.4, "pop", 0.25),
]
sfx_track = np.zeros((N, 1))
cues_out = []
for i, (t, name, vol) in enumerate(CUES):
    path, d = lib[name]
    x = load(os.path.join(PROJ, path), mono=True)
    a = int(round(t * SR))
    sfx_track[a:a + len(x)] += x[: N - a] * vol
    cues_out.append({"id": f"sfx{i + 1:02d}", "src": path, "start": round(t, 3), "duration": round(d, 3), "volume": vol})

# ---------------- reference mix + loudness ----------------
mix = music_d + vo_track + sfx_track
peak = np.abs(mix).max()
print("music gain", round(20 * np.log10(g_mus), 2), "dB; voice gain", round(20 * np.log10(g_vo), 2), "dB")
print("reference mix: integrated", round(meter.integrated_loudness(mix), 2), "LUFS; sample peak", round(20 * np.log10(peak), 2), "dBFS")
over = resample_poly(mix, 4, 1, axis=0)
print("true peak (4x)", round(20 * np.log10(np.abs(over).max()), 2), "dBTP")
music_out = music_d.astype(np.float32)
sf.write(os.path.join(WORK, "kwikama-theme.wav"), music_out, SR, subtype="PCM_24")
sf.write(os.path.join(WORK, "reference_mix.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
json.dump(cues_out, open(os.path.join(PROJ, "assets/audio/sfx/cues.json"), "w"), indent=1)
print("cues", len(cues_out))
