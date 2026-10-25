"""KWIKAMA — musique originale du film (127 s, ré mineur -> ré majeur, 100 BPM).

Partition écrite note à note, rendue avec FluidSynth (banque FluidR3 GM) pour les instruments
acoustiques et synthétisée en numpy pour la section rythmique moderne (kick, clap, hats, basse,
arpège pluck, risers, impacts). Mixage pedalboard. La grille des mesures est calée sur le film :
la révélation (28,6 s), le flux d'argent (76,6 s) et le logo (115,0 s) tombent sur des premiers temps.

Usage : python compose.py <dossier_de_travail> <sortie.wav>
"""
import json
import os
import subprocess
import sys

import numpy as np
import pretty_midi
import soundfile as sf
from pedalboard import (Chorus, Compressor, Delay, Distortion, Gain, HighpassFilter, HighShelfFilter,
                        Limiter, LowpassFilter, LowShelfFilter, Pedalboard, PeakFilter, Reverb)
from scipy.signal import butter, sosfilt

SR = 48000
DUR = 127.0
N = int(DUR * SR)
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
BEAT, BAR, T0 = 0.6, 2.4, -0.2
WORK = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kwk_music"
OUT = sys.argv[2] if len(sys.argv) > 2 else "kwikama-theme.wav"
os.makedirs(WORK, exist_ok=True)
rng = np.random.default_rng(2026)


def bar(k, beat=0.0):
    """film time of bar k (+ beats); bar 12 = 28.6 s (reveal), 32 = 76.6 s (payoff), 48 = 115.0 s (logo)."""
    return T0 + k * BAR + beat * BEAT


def nn(name):
    return pretty_midi.note_name_to_number(name)


def chord(names):
    return [nn(x) for x in names.split()]


CH = {
    "Dm": "D3 A3 D4 F4 A4", "Dm9": "D3 A3 E4 F4 A4", "Bb": "Bb2 F3 Bb3 D4 F4", "Gm": "G2 D3 G3 Bb3 D4", "A": "A2 E3 A3 C#4 E4",
    "A7b9": "A2 G3 C#4 Bb4 E5", "F": "F2 C3 F3 A3 C4", "C/E": "E2 C3 G3 C4 E4",
    "D": "D3 A3 D4 F#4 A4", "Dadd9": "D3 A3 E4 F#4 A4", "A/C#": "C#3 A3 C#4 E4 A4", "Bm": "B2 F#3 B3 D4 F#4", "Bm7": "B2 F#3 A3 D4 F#4",
    "G": "G2 D3 G3 B3 D4", "Gmaj7": "G2 D3 F#3 B3 D4", "Em": "E3 B3 E4 G4 B4", "Asus": "A2 E3 A3 D4 E4",
}
ROOT = {"Dm": "D", "Dm9": "D", "Bb": "Bb", "Gm": "G", "A": "A", "A7b9": "A", "F": "F", "C/E": "C", "D": "D", "Dadd9": "D", "A/C#": "A",
        "Bm": "B", "Bm7": "B", "G": "G", "Gmaj7": "G", "Em": "E", "Asus": "A"}

# ----------------------------------------------------------------------------------------------
# score: instrument -> list of (pitch, start, end, velocity); cc -> list of (cc, value, time)
# ----------------------------------------------------------------------------------------------
score = {k: [] for k in ["piano", "strings", "slow", "trem", "pad", "harp", "celesta", "marimba", "timp", "brass", "horn", "drums"]}
ccs = {k: [] for k in score}


def add(inst, names, start, end, vel):
    for p in (names if isinstance(names, list) else chord(names) if " " in names else [nn(names)]):
        score[inst].append((nn(p) if isinstance(p, str) else int(p), start, end, vel))


def ramp(inst, cc, t0, t1, v0, v1, steps=24):
    for i in range(steps + 1):
        t = t0 + (t1 - t0) * i / steps
        ccs[inst].append((cc, int(v0 + (v1 - v0) * i / steps), t))


# ---- A1 : Kolwezi (0 – 9.4) ------------------------------------------------------------------
add("slow", "D2 A2", 0.0, 9.5, 60)
ramp("slow", 11, 0.0, 2.0, 70, 110)
add("pad", CH["Dm9"], 0.0, 9.4, 52)
for p, s, d, v in [("D5", 0.62, 1.5, 62), ("F5", 2.2, 0.6, 52), ("E5", 2.8, 0.6, 50), ("D5", 3.4, 1.15, 55),
                   ("A4", 4.6, 1.15, 50), ("C5", 5.8, 0.55, 48), ("Bb4", 6.4, 0.9, 52), ("A4", 7.0, 2.3, 50)]:
    add("piano", p, s, s + d, v)
add("piano", "D3 A3", 0.62, 4.6, 38)
add("piano", "Bb2 F3", 4.6, 7.0, 36)
add("trem", "C#3 G3", 7.55, 9.35, 50)
ramp("trem", 11, 7.55, 9.3, 40, 115)

# ---- A2 : dix-huit institutions (9.4 – 16.6) ---------------------------------------------------
for k, c in [(4, "Dm"), (5, "F"), (6, "C/E")]:
    add("pad", CH[c], bar(k), bar(k + 1), 50)
add("slow", "D2 A2", 9.4, 16.7, 55)
for t, p in [(11.43, "D5"), (12.47, "F5"), (13.23, "A5"), (14.03, "C6")]:
    add("marimba", p, t, t + 0.6, 92)
    add("marimba", pretty_midi.note_number_to_name(nn(p) - 12), t, t + 0.6, 60)
for i, p in enumerate("D5 E5 F5 G5 A5 C6 D6 E6 F6 A6".split()):
    add("harp", p, 14.98 + i * 0.055, 16.6, 62 + i * 2)
add("celesta", "D6", 15.6, 16.6, 60)

# ---- A3 : silos (16.6 – 26.2) ---------------------------------------------------------------
progA3 = [(7, "Dm"), (8, "Bb"), (9, "Gm"), (10, "A7b9")]
for k, c in progA3:
    add("pad", CH[c], bar(k), bar(k + 1) if k < 10 else 25.9, 54 if k < 10 else 62)
    if k >= 8:
        add("timp", ROOT[c] + ("2" if ROOT[c] in "AB" or ROOT[c] == "Bb" else "2"), bar(k), bar(k) + 1.2, 58 + (k - 8) * 12)
# low string ostinato: 8ths then 16ths, crescendo
for k, c in progA3:
    r = ROOT[c]
    lo = nn(r + "2") if r not in ("A", "Bb") else nn(r + "1") + 12
    hi = lo + 7
    step = BEAT / 2 if k < 9 else BEAT / 4
    t = bar(k)
    i = 0
    while t < (bar(k + 1) if k < 10 else 25.85) - 1e-6:
        v = int(42 + (t - 16.6) / (25.9 - 16.6) * 48)
        score["strings"].append((lo if i % 2 == 0 else hi, t, t + step * 0.55, v))
        t += step
        i += 1
add("strings", CH["A7b9"], 23.8, 25.85, 44)
ramp("strings", 11, 23.8, 25.85, 60, 127)
ramp("pad", 11, 16.6, 25.85, 80, 120)
# the stamp: orchestral stab, then silence
add("timp", "D2", 25.92, 26.6, 120)
add("brass", "Bb2 F3 Bb3 D4", 25.92, 26.25, 118)
add("strings", "Bb2 F3 Bb3 D4 F4", 25.92, 26.15, 120)
add("slow", "D6", 26.25, 28.55, 34)
ramp("slow", 11, 26.25, 28.5, 50, 100)

# ---- B : révélation (28.6 – 38.2) ------------------------------------------------------------
progB = [(12, "Dadd9"), (13, "A/C#"), (14, "Bm7"), (15, "Gmaj7")]
for k, c in progB:
    add("pad", CH[c], bar(k), bar(k + 1), 58)
    add("slow", CH[c], bar(k), bar(k + 1), 50)
ramp("slow", 11, 28.6, 31.0, 50, 105)
for i, p in enumerate("D4 F#4 A4 D5 E5 F#5 A5 D6".split()):
    add("harp", p, 28.6 + i * 0.045, 31.0, 70)
for i, p in enumerate("D6 F#6 A6 D7 E6 A5 F#5".split()):
    add("celesta", p, 28.66 + i * 0.04, 29.6 + i * 0.04, 58)


def arpeggio(inst, k, c, vel, start_beat=0, pattern=(0, 2, 4, 3, 2, 4, 3, 2)):
    notes = chord(CH[c])
    for j in range(start_beat, 8):
        t = bar(k, j * 0.5)
        add(inst, [notes[pattern[j] % len(notes)] + (12 if pattern[j] >= 3 else 0)], t, t + 0.55, vel)


for k, c in progB:
    arpeggio("piano", k, c, 40 if k == 12 else 44, start_beat=2 if k == 12 else 0)
HOOK = [("A4", 0, 1), ("D5", 1, 1), ("E5", 2, 0.5), ("F#5", 2.5, 1.5), ("E5", 3.5, 0.5),   # bar 1
        ("D5", 4, 1.5), ("B4", 5.5, 0.5), ("A4", 6, 2)]                                 # bar 2
ANSWER = [("F#5", 0, 1), ("A5", 1, 1), ("G5", 2, 0.5), ("F#5", 2.5, 0.5), ("E5", 3, 1),
          ("D5", 4, 1), ("E5", 5, 1), ("F#5", 6, 2)]


def melody(inst, k, notes, vel, octave=0, length=1.0):
    for p, b, d in notes:
        t = bar(k, b)
        add(inst, [nn(p) + 12 * octave], t, t + d * BEAT * length, vel)


melody("piano", 14, HOOK, 64)

# ---- C : parcours (38.2 – 67.0), 12 bars Bm G D A ------------------------------------------
progC = [(16 + i, ["Bm", "G", "D", "A"][i % 4]) for i in range(12)]
for k, c in progC:
    add("pad", CH[c], bar(k), bar(k + 1), 50)
    add("piano", CH[c].split()[1:4], bar(k), bar(k, 1.5), 38)
cm = ["F#5", "G5", "A5", "A5", "B5", "B5", "A5", "E5"]
for i, (k, c) in enumerate(progC[4:]):
    add("slow", cm[i % len(cm)], bar(k), bar(k + 1), 46)

# ---- D : l'argent (67.0 – 81.4) ---------------------------------------------------------------
progD = [(28, "Bm"), (29, "G"), (30, "Em"), (31, "Asus")]
for k, c in progD:
    add("pad", CH[c], bar(k), bar(k + 1) - (0.25 if k == 31 else 0), 56)
for k, p in [(28, "F#4"), (29, "G4"), (30, "B4"), (31, "C#5")]:
    add("trem", [nn(p), nn(p) - 12], bar(k), bar(k + 1) - (0.25 if k == 31 else 0), 64)
ramp("trem", 11, 67.0, 76.3, 50, 127)
add("pad", CH["A"], bar(31, 2), 76.35, 60)
# payoff: D | A/C#
for k, c in [(32, "D"), (33, "A/C#")]:
    add("pad", CH[c], bar(k), bar(k + 1), 66)
    add("strings", CH[c], bar(k), bar(k + 1), 70)
    add("horn", CH[c].split()[1:4], bar(k), bar(k + 1), 62)
melody("piano", 32, HOOK, 84)
melody("piano", 32, HOOK, 70, octave=-1)
melody("slow", 32, HOOK, 74, octave=1)
add("timp", "D2", 76.6, 78.0, 112)

# ---- E : preuves, avoirs, qualité (81.4 – 112.6) ----------------------------------------------
progE = [(34 + i, ["D", "Bm", "G", "A"][i % 4]) for i in range(12)]
for k, c in progE:
    add("pad", CH[c], bar(k), bar(k + 1), 50)
    add("piano", CH[c].split()[1:4], bar(k), bar(k, 1.5), 36)
    if k >= 38:
        add("slow", CH[c].split()[2:5], bar(k), bar(k + 1), 40)
add("pad", CH["Asus"], bar(46), bar(47), 46)
add("slow", "A4 D5 E5", bar(46), bar(47), 36)
ramp("pad", 11, bar(46), bar(47), 110, 60)
# build into the logo (112.6 – 115.0)
add("trem", "A3 E4 A4", bar(47), 114.95, 60)
ramp("trem", 11, bar(47), 114.9, 40, 127)
add("timp", "A1", 113.8, 114.95, 90)

# ---- F : signature (115.0 – 127.0) -----------------------------------------------------------
progF = [(48, "D"), (49, "A/C#"), (50, "Bm"), (51, "G")]
for k, c in progF:
    add("pad", CH[c], bar(k), bar(k + 1), 64)
    add("strings", CH[c], bar(k), bar(k + 1), 64)
    add("horn", CH[c].split()[1:4], bar(k), bar(k + 1), 58)
add("pad", CH["A"], bar(51, 2), bar(52), 64)
add("strings", CH["A"], bar(51, 2), bar(52), 62)
add("timp", "D2", 115.0, 116.6, 120)
add("brass", "D3 A3 D4 F#4", 115.0, 115.6, 96)
melody("piano", 48, HOOK, 80)
melody("piano", 50, ANSWER, 76)
melody("slow", 48, HOOK, 70, octave=1)
melody("slow", 50, ANSWER, 66, octave=1)
for i, p in enumerate("D5 F#5 A5 D6 E6 F#6 A6 D7".split()):
    add("harp", p, 115.0 + i * 0.04, 117.0, 66)
# final chord, held and fading
add("pad", CH["D"], 124.6, 127.0, 70)
add("strings", "D3 A3 D4 F#4 A4 D5", 124.6, 127.0, 66)
add("piano", "D2 D3 A3 D4 F#4 A4 D5", 124.6, 127.0, 70)
add("celesta", "D6 A6", 124.6, 126.5, 54)
add("timp", "D2", 124.6, 126.0, 96)
ramp("strings", 11, 125.4, 126.95, 110, 0)
ramp("pad", 11, 125.4, 126.95, 110, 0)

# ---- drums from the GM kit (crashes, rolls, toms) ---------------------------------------------
CRASH, SNARE, TOM_L, TOM_M, TOM_H, RIDE = 49, 38, 45, 47, 50, 51
for t in [76.6, 98.2, 115.0, 124.6]:
    score["drums"].append((CRASH, t, t + 2.5, 104 if t != 98.2 else 70))
for i, (p, b) in enumerate([(TOM_H, 2.0), (TOM_H, 2.5), (TOM_M, 3.0), (TOM_L, 3.5)]):
    score["drums"].append((p, bar(27, b), bar(27, b) + 0.3, 70 + i * 8))
# snare build before the payoff: 8ths then 16ths
for j in range(8):
    score["drums"].append((SNARE, bar(30, j * 0.5), bar(30, j * 0.5) + 0.1, 40 + j * 3))
for j in range(16):
    score["drums"].append((SNARE, bar(31, j * 0.25), bar(31, j * 0.25) + 0.08, 60 + j * 3))
# fill into act 7 (97.6 – 98.2) and roll into the logo
for j in range(4):
    score["drums"].append((SNARE, bar(40, 3 + j * 0.25), bar(40, 3 + j * 0.25) + 0.08, 58 + j * 8))
for j in range(8):
    score["drums"].append((SNARE, bar(47, 2 + j * 0.25), bar(47, 2 + j * 0.25) + 0.08, 50 + j * 9))

PROGRAMS = {"piano": 0, "strings": 48, "slow": 49, "trem": 44, "pad": 89, "harp": 46, "celesta": 8, "marimba": 12,
            "timp": 47, "brass": 61, "horn": 60, "drums": 0}
PAN = {"piano": 64, "strings": 52, "slow": 76, "trem": 60, "pad": 64, "harp": 84, "celesta": 44, "marimba": 72,
       "timp": 64, "brass": 58, "horn": 70, "drums": 64}


def render_inst(name):
    pm = pretty_midi.PrettyMIDI(initial_tempo=100)
    inst = pretty_midi.Instrument(program=PROGRAMS[name], is_drum=(name == "drums"))
    inst.control_changes.append(pretty_midi.ControlChange(10, PAN[name], 0.0))
    inst.control_changes.append(pretty_midi.ControlChange(7, 110, 0.0))
    inst.control_changes.append(pretty_midi.ControlChange(11, 100, 0.0))
    for cc, v, t in sorted(ccs[name], key=lambda x: x[2]):
        inst.control_changes.append(pretty_midi.ControlChange(cc, max(0, min(127, v)), max(0.0, t)))
    for p, s, e, v in score[name]:
        s = max(0.0, s)
        inst.notes.append(pretty_midi.Note(velocity=int(max(1, min(127, v))), pitch=int(p), start=s, end=max(s + 0.02, e)))
    pm.instruments.append(inst)
    mid = os.path.join(WORK, name + ".mid")
    wav = os.path.join(WORK, name + ".wav")
    pm.write(mid)
    subprocess.run(["fluidsynth", "-ni", "-q", "-R", "0", "-C", "0", "-g", "0.5", "-r", str(SR), "-F", wav, SF2, mid], check=True)
    x, sr = sf.read(wav, always_2d=True)
    assert sr == SR
    y = np.zeros((N, 2))
    m = min(N, len(x))
    y[:m] = x[:m]
    return y


# ----------------------------------------------------------------------------------------------
# numpy synthesis: rhythm section, bass, plucks, risers, impacts
# ----------------------------------------------------------------------------------------------
def bp(sig, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), sig)


def hp(sig, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), sig)


def lp(sig, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), sig)


def tvec(d):
    return np.arange(int(d * SR)) / SR


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= len(buf):
        return
    if i < 0:
        sig = sig[-i:]
        i = 0
    seg = sig[: len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    if seg.ndim == 1:
        buf[i:i + len(seg), 0] += seg * gain * l * 1.4142
        buf[i:i + len(seg), 1] += seg * gain * r * 1.4142
    else:
        buf[i:i + len(seg)] += seg * gain


def kick():
    t = tvec(0.5)
    f = 46 + 90 * np.exp(-t * 32)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = hp(rng.standard_normal(len(t)), 1500) * np.exp(-t * 400) * 0.25
    return np.tanh(1.6 * (s + click)) * 0.9


def clap():
    t = tvec(0.35)
    n = rng.standard_normal(len(t))
    env = np.zeros_like(t)
    for d in (0.0, 0.011, 0.022):
        env += (t >= d) * np.exp(-np.maximum(t - d, 0) * 180)
    env += (t >= 0.03) * np.exp(-np.maximum(t - 0.03, 0) * 14) * 0.35
    return bp(n, 900, 3500) * env * 0.9


def hat(open_=False):
    t = tvec(0.35 if open_ else 0.08)
    return hp(rng.standard_normal(len(t)), 7000, 4) * np.exp(-t * (9 if open_ else 70)) * 0.5


def shaker():
    t = tvec(0.09)
    env = np.minimum(t / 0.012, 1) * np.exp(-t * 45)
    return bp(rng.standard_normal(len(t)), 4500, 11000) * env * 0.35


def tick(high=True):
    t = tvec(0.05)
    return (hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 300) * 0.5 +
            np.sin(2 * np.pi * (1900 if high else 1450) * t) * np.exp(-t * 160) * 0.5)


def boom(d=3.0, f0=62, f1=27):
    t = tvec(d)
    f = f1 + (f0 - f1) * np.exp(-t * 2.2)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.5)
    n = lp(rng.standard_normal(len(t)), 900) * np.exp(-t * 9) * 0.35
    return np.tanh(1.3 * (s + n))


def heartbeat():
    t = tvec(0.45)
    f = 40 + 25 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11)


def riser(d):
    t = tvec(d)
    n = rng.standard_normal(len(t))
    out = np.zeros_like(t)
    bands = np.geomspace(250, 9000, 14)
    for i, fc in enumerate(bands):
        w = np.exp(-((t / d) * (len(bands) - 1) - i) ** 2 / 1.2)
        out += bp(n, fc / 1.4, min(fc * 1.4, SR / 2 - 100)) * w
    saw_f = 180 * (2 ** (3 * t / d))
    ph = np.cumsum(saw_f) / SR
    saw = 2 * (ph % 1) - 1
    env = (t / d) ** 2.2
    return (out * 0.8 + lp(saw, 2500) * 0.12) * env


def rev_cymbal(d):
    t = tvec(d)
    s = hp(rng.standard_normal(len(t)), 5000, 3) * np.exp(-t * 2.4)
    return s[::-1] * 0.6


def pluck(freq, d=0.45, bright=1.0):
    t = tvec(d)
    nh = int(min(28, (SR / 2 - 200) // freq))
    s_b = np.zeros_like(t)
    s_d = np.zeros_like(t)
    for k in range(1, nh + 1):
        h = np.sin(2 * np.pi * k * freq * t) / k
        s_b += h
        if k <= 4:
            s_d += h
    env_b = np.exp(-t * 26) * bright
    env_d = np.exp(-t * 7)
    a = np.minimum(t / 0.004, 1)
    return (s_b * env_b * 0.35 + s_d * env_d * 0.55) * a


def bassnote(freq, d):
    t = tvec(d)
    s = np.sin(2 * np.pi * freq * t) + 0.22 * np.sin(4 * np.pi * freq * t) + 0.08 * np.sin(6 * np.pi * freq * t)
    env = np.minimum(t / 0.006, 1) * (0.72 + 0.28 * np.exp(-t * 9)) * np.minimum((d - t) / 0.04, 1)
    return np.tanh(1.4 * s * env) * 0.8


def hz(name):
    return pretty_midi.note_number_to_hz(nn(name))


bus = {k: np.zeros((N, 2)) for k in ["kick", "clap", "hats", "shaker", "bass", "pluck", "fx", "tick"]}
K, CL, HT, HO, SH = kick(), clap(), hat(), hat(True), shaker()

# heartbeat during the hook, clock during the delays
for b in (1, 2, 3):
    place(bus["kick"], heartbeat(), bar(b), 0.55)
    place(bus["kick"], heartbeat(), bar(b) + 0.3, 0.3)
for j in range(int((25.85 - 9.4) / BEAT) + 1):
    t = 9.4 + j * BEAT
    if t > 25.85:
        break
    g = 0.05 if t < 22.6 else 0.05 + (t - 22.6) / (25.85 - 22.6) * 0.16
    place(bus["tick"], tick(j % 2 == 0), t, g, pan=0.25 if j % 2 else -0.25)
# pulse bass in A2 / A3
for k, c in [(4, "Dm"), (5, "F"), (6, "C/E"), (7, "Dm"), (8, "Bb"), (9, "Gm"), (10, "A")]:
    r = {"Dm": "D2", "F": "F2", "C/E": "C2", "Bb": "Bb1", "Gm": "G1", "A": "A1"}[c]
    for j in range(8):
        t = bar(k, j * 0.5)
        if t >= 25.85:
            break
        place(bus["bass"], bassnote(hz(r), 0.26), t, 0.32 + 0.1 * (k >= 7))
# stamp + reveal impacts, risers
place(bus["fx"], boom(1.4, 70, 30), 25.92, 0.9)
place(bus["fx"], riser(1.4), 27.2, 0.35)
place(bus["fx"], rev_cymbal(1.4), 27.2, 0.5)
place(bus["fx"], boom(3.5, 58, 26), 28.6, 0.55)
place(bus["fx"], riser(2.4), 74.2, 0.45)
place(bus["fx"], rev_cymbal(2.0), 74.6, 0.55)
place(bus["fx"], boom(3.0, 66, 28), 76.6, 0.8)
place(bus["fx"], riser(2.4), 112.6, 0.4)
place(bus["fx"], rev_cymbal(1.6), 113.4, 0.6)
place(bus["fx"], boom(3.4, 66, 27), 115.0, 0.95)
place(bus["fx"], boom(2.6, 60, 26), 124.6, 0.6)


def groove(k, c, kick_pat, clap_on, hat_div, shaker_on, bass_on, pluck_on, pluck_div=0.5, level=1.0):
    root = {"Bm": "B1", "G": "G1", "D": "D2", "A": "A1", "Em": "E2", "Asus": "A1", "A/C#": "A1", "Dadd9": "D2"}[c]
    for b in kick_pat:
        place(bus["kick"], K, bar(k, b), 0.85 * level)
    if clap_on:
        for b in (1, 3):
            place(bus["clap"], CL, bar(k, b), 0.55 * level, pan=0.05)
    if hat_div:
        n = int(4 / hat_div)
        for j in range(n):
            accent = 1.0 if (j * hat_div) % 1 == 0.5 else 0.6
            place(bus["hats"], HT, bar(k, j * hat_div), 0.32 * accent * level, pan=0.3)
    if shaker_on:
        for j in range(16):
            place(bus["shaker"], SH, bar(k, j * 0.25), (0.25 if j % 2 else 0.15) * level, pan=-0.35)
    if bass_on:
        for j in range(8):
            f = hz(root) * (2 if j in (3, 7) else 1)
            place(bus["bass"], bassnote(f, 0.27), bar(k, j * 0.5), 0.5 * level)
    if pluck_on:
        notes = chord(CH[c])
        tones = [notes[1] + 12, notes[3] + 12, notes[4] + 12, notes[3] + 12, notes[2] + 12, notes[4] + 12, notes[3] + 24, notes[4] + 12]
        n = int(4 / pluck_div)
        for j in range(n):
            p = tones[j % len(tones)]
            v = 0.16 if j % 2 else 0.22
            place(bus["pluck"], pluck(pretty_midi.note_number_to_hz(p), 0.5), bar(k, j * pluck_div), v * level, pan=(-0.4 if j % 2 else 0.4))


# C : parcours
for i, (k, c) in enumerate(progC):
    groove(k, c, kick_pat=(0, 2) if i < 4 else (0, 1.5, 2), clap_on=i >= 4, hat_div=0.5 if i < 8 else 0.25,
           shaker_on=True, bass_on=True, pluck_on=True, pluck_div=0.5 if i < 8 else 0.25, level=0.9)
# D : build and payoff
for i, (k, c) in enumerate(progD):
    groove(k, c, kick_pat=(0, 2) if i < 2 else (0, 1, 2, 3), clap_on=i < 2, hat_div=0.25, shaker_on=True,
           bass_on=True, pluck_on=True, pluck_div=0.25, level=0.95 + 0.05 * i)
# pre-drop silence: cut the groove buses just before 76.6
for name in ["kick", "clap", "hats", "shaker", "bass", "pluck"]:
    a, b = int(76.32 * SR), int(76.6 * SR)
    bus[name][a:b] *= np.linspace(1, 0, b - a)[:, None] ** 3
for k, c in [(32, "D"), (33, "A/C#")]:
    groove(k, c, kick_pat=(0, 1, 2, 3), clap_on=True, hat_div=0.25, shaker_on=True, bass_on=True, pluck_on=True, pluck_div=0.25, level=1.1)
    for b in (0.5, 1.5, 2.5, 3.5):
        place(bus["hats"], HO, bar(k, b), 0.2, pan=0.35)
# E : evidence, assets, quality
for i, (k, c) in enumerate(progE):
    full = i >= 8
    groove(k, c, kick_pat=(0, 2) if not full else (0, 1.5, 2), clap_on=i >= 2, hat_div=0.5 if not full else 0.25,
           shaker_on=i < 4 or full, bass_on=True, pluck_on=i >= 1, pluck_div=0.5 if not full else 0.25, level=0.82)
# breakdown bar 46: filtered plucks only
for j in range(8):
    place(bus["pluck"], lp(pluck(hz("A4") if j % 2 else hz("E5"), 0.5), 1800), bar(46, j * 0.5), 0.14 * (1 - j / 10))
# F : signature
for i, (k, c) in enumerate(progF):
    groove(k, c, kick_pat=(0, 1, 2, 3), clap_on=True, hat_div=0.5, shaker_on=True, bass_on=True, pluck_on=True, pluck_div=0.5, level=1.0)
place(bus["kick"], K, 124.6, 1.0)
place(bus["bass"], bassnote(hz("D2"), 2.2), 124.6, 0.6)

# ----------------------------------------------------------------------------------------------
# mix
# ----------------------------------------------------------------------------------------------
print("rendering FluidSynth stems...")
stems = {name: render_inst(name) for name in score}
fx_chain = {
    "piano": Pedalboard([HighpassFilter(70), LowShelfFilter(250, -2), Reverb(room_size=0.62, damping=0.45, wet_level=0.24, dry_level=0.86, width=0.9)]),
    "strings": Pedalboard([HighpassFilter(60), Reverb(room_size=0.82, damping=0.4, wet_level=0.34, dry_level=0.8, width=1.0)]),
    "slow": Pedalboard([HighpassFilter(80), Reverb(room_size=0.9, damping=0.35, wet_level=0.42, dry_level=0.7, width=1.0)]),
    "trem": Pedalboard([HighpassFilter(80), Reverb(room_size=0.8, damping=0.4, wet_level=0.35, dry_level=0.75, width=1.0)]),
    "pad": Pedalboard([HighpassFilter(90), LowpassFilter(9000), Chorus(rate_hz=0.3, depth=0.2, mix=0.25), Reverb(room_size=0.85, wet_level=0.35, dry_level=0.7)]),
    "harp": Pedalboard([Reverb(room_size=0.8, wet_level=0.4, dry_level=0.75)]),
    "celesta": Pedalboard([Delay(delay_seconds=0.45, feedback=0.28, mix=0.22), Reverb(room_size=0.85, wet_level=0.45, dry_level=0.7)]),
    "marimba": Pedalboard([Reverb(room_size=0.7, wet_level=0.35, dry_level=0.8)]),
    "timp": Pedalboard([Reverb(room_size=0.85, wet_level=0.35, dry_level=0.85)]),
    "brass": Pedalboard([Reverb(room_size=0.8, wet_level=0.35, dry_level=0.8)]),
    "horn": Pedalboard([HighpassFilter(90), Reverb(room_size=0.85, wet_level=0.38, dry_level=0.75)]),
    "drums": Pedalboard([Reverb(room_size=0.6, wet_level=0.2, dry_level=0.9)]),
}
gains_db = {"piano": 0.0, "strings": -2.0, "slow": -3.0, "trem": -4.0, "pad": -6.0, "harp": -4.0, "celesta": -6.0, "marimba": -5.0,
            "timp": -1.0, "brass": -4.0, "horn": -6.0, "drums": -6.0}
mix = np.zeros((N, 2))
for name, y in stems.items():
    z = fx_chain[name](y.T.astype(np.float32), SR).T
    mix[: len(z)] += z[:N] * 10 ** (gains_db[name] / 20)
bus_chain = {
    "kick": (Pedalboard([LowShelfFilter(80, 2), Compressor(threshold_db=-12, ratio=3, attack_ms=5, release_ms=120)]), -4.0),
    "clap": (Pedalboard([Reverb(room_size=0.5, wet_level=0.25, dry_level=0.85)]), -9.0),
    "hats": (Pedalboard([HighShelfFilter(9000, 2)]), -13.0),
    "shaker": (Pedalboard([]), -14.0),
    "bass": (Pedalboard([LowpassFilter(900), Distortion(drive_db=4), LowpassFilter(1200)]), -7.0),
    "pluck": (Pedalboard([HighpassFilter(250), Delay(delay_seconds=0.45, feedback=0.32, mix=0.25), Reverb(room_size=0.7, wet_level=0.3, dry_level=0.8)]), -9.0),
    "fx": (Pedalboard([Reverb(room_size=0.9, wet_level=0.3, dry_level=0.85)]), -5.0),
    "tick": (Pedalboard([HighpassFilter(400), Reverb(room_size=0.4, wet_level=0.2, dry_level=0.9)]), -10.0),
}
for name, (ch, g) in bus_chain.items():
    z = ch(bus[name].T.astype(np.float32), SR).T
    mix[: len(z)] += z[:N] * 10 ** (g / 20)

# arrangement automation: a real breath before the reveal, a warmer reveal, an audible breakdown
t_ax = np.arange(N) / SR
auto = np.ones(N)
def seg_gain(t0, t1, g, ramp_in=0.3, ramp_out=0.3):
    up = np.clip((t_ax - (t0 - ramp_in)) / ramp_in, 0, 1)
    down = np.clip(((t1 + ramp_out) - t_ax) / ramp_out, 0, 1)
    return 1 + (g - 1) * np.minimum(up, down)
auto *= seg_gain(26.5, 27.15, 10 ** (-16 / 20), ramp_in=0.35, ramp_out=0.45)
auto *= seg_gain(28.75, 38.0, 10 ** (4 / 20), ramp_in=0.15, ramp_out=0.25)
auto *= seg_gain(110.4, 112.5, 10 ** (5 / 20), ramp_in=0.2, ramp_out=0.1)
mix *= auto[:, None]

# gentle master: glue + tone, fade out
master = Pedalboard([HighpassFilter(28), Compressor(threshold_db=-16, ratio=2.0, attack_ms=25, release_ms=250), PeakFilter(3200, 1.0, 0.7), Limiter(threshold_db=-2.0, release_ms=120)])
mix = master(mix.T.astype(np.float32), SR).T
fo = int(1.4 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
fi = int(0.05 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
sf.write(os.path.join(WORK, "music_free.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
print("free mix written", os.path.join(WORK, "music_free.wav"))
