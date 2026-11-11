"""KWIKAMA — musique originale du film, version 2 (153 s, ré mineur -> ré majeur, 94–104 BPM).

Partition écrite note à note, rendue avec FluidSynth (banque FluidR3 GM) pour les instruments
acoustiques et synthétisée en numpy pour la section rythmique moderne (kick, clap, hats, basse,
arpège pluck, risers, impacts). Mixage pedalboard. Chaque chapitre du film ouvre une nouvelle phrase :
la grille de mesures repart sur chaque carte de chapitre (le tempo varie de quelques pour cent pour
que le chapitre suivant tombe lui aussi sur un premier temps).

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
DUR = 153.0
N = int(DUR * SR)
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
WORK = sys.argv[1] if len(sys.argv) > 1 else "/tmp/kwk_music"
OUT = sys.argv[2] if len(sys.argv) > 2 else "kwikama-theme.wav"
os.makedirs(WORK, exist_ok=True)
rng = np.random.default_rng(2026)


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

CH.update({"C": "C3 G3 C4 E4 G4", "D/F#": "F#2 D3 A3 D4 F#4", "Am": "A2 E3 A3 C4 E4"})
ROOT.update({"C": "C", "D/F#": "D", "Am": "A"})

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


class Sec:
    """a phrase of bars of equal length starting at film time t0 (one per chapter)."""
    def __init__(self, t0, t1, nbars):
        self.t0, self.n = t0, nbars
        self.bar_len = (t1 - t0) / nbars
        self.beat = self.bar_len / 4

    def at(self, k, beat=0.0):
        return self.t0 + k * self.bar_len + beat * self.beat


# the film's chapters: each one starts on a first beat
SB = Sec(14.36, 23.96, 4)      # reveal
S1 = Sec(23.96, 49.45, 11)     # 1 · contrôle de légalité
S2 = Sec(49.45, 68.65, 8)      # 2 · chaîne de garde
S3 = Sec(68.65, 95.05, 11)     # 3 · croisement des dossiers
S4 = Sec(95.05, 122.55, 11)    # 4 · météo de la coopération + CENAREF
S5 = Sec(122.55, 137.75, 6)    # 5 · reversement au Trésor
S6 = Sec(137.75, 144.46, 3)    # résultat immédiat 8, plein cadre
SF = Sec(144.46, 151.66, 3)    # signature

HOOK = [("A4", 0, 1), ("D5", 1, 1), ("E5", 2, 0.5), ("F#5", 2.5, 1.5), ("E5", 3.5, 0.5),
        ("D5", 4, 1.5), ("B4", 5.5, 0.5), ("A4", 6, 2)]
ANSWER = [("F#5", 0, 1), ("A5", 1, 1), ("G5", 2, 0.5), ("F#5", 2.5, 0.5), ("E5", 3, 1),
          ("D5", 4, 1), ("E5", 5, 1), ("F#5", 6, 2)]


def melody(inst, S, k, notes, vel, octave=0, length=1.0):
    for p, b, d in notes:
        t = S.at(k, b)
        add(inst, [nn(p) + 12 * octave], t, t + d * S.beat * length, vel)


def arpeggio(inst, S, k, c, vel, start=0, pattern=(0, 2, 4, 3, 2, 4, 3, 2)):
    notes = chord(CH[c])
    for j in range(start, 8):
        t = S.at(k, j * 0.5)
        add(inst, [notes[pattern[j] % len(notes)] + (12 if pattern[j] >= 3 else 0)], t, t + S.beat * 0.9, vel)


def chords(S, prog, pad=52, piano=38, slow=0):
    for k, c in enumerate(prog):
        if c is None:
            continue
        add("pad", CH[c], S.at(k), S.at(k + 1), pad)
        if piano:
            add("piano", CH[c].split()[1:4], S.at(k), S.at(k, 1.5), piano)
        if slow:
            add("slow", CH[c].split()[2:5], S.at(k), S.at(k + 1), slow)


def sting(t, vel=60):
    """the chapter motif: three bells and a harp sweep on each chapter card."""
    for i, p in enumerate(["A5", "D6", "F#6"]):
        add("celesta", p, t + i * 0.09, t + 1.4, vel)
    for i, p in enumerate("D5 F#5 A5 D6 E6".split()):
        add("harp", p, t + i * 0.035, t + 1.6, vel)


# ---- A : Kolwezi, six silos (0 – 14.36), free time --------------------------------------------
add("slow", "D2 A2", 0.0, 14.0, 58)
ramp("slow", 11, 0.0, 2.0, 70, 110)
ramp("slow", 11, 12.6, 14.0, 110, 30)
add("pad", CH["Dm9"], 0.0, 8.7, 50)
add("pad", CH["Bb"], 8.7, 11.8, 50)
add("pad", CH["Gm"], 11.8, 13.0, 54)
add("pad", CH["A7b9"], 13.0, 14.0, 50)
ramp("pad", 11, 12.9, 14.1, 115, 20)
for p, s, d, v in [("D5", 0.82, 1.5, 62), ("F5", 2.4, 0.6, 52), ("E5", 3.0, 0.6, 50), ("D5", 3.6, 1.15, 55),
                   ("A4", 4.8, 1.15, 50), ("C5", 6.0, 0.55, 48), ("Bb4", 6.6, 0.9, 52), ("A4", 7.2, 1.6, 50)]:
    add("piano", p, s, s + d, v)
add("piano", "D3 A3", 0.82, 4.8, 38)
add("piano", "Bb2 F3", 4.8, 7.2, 36)
add("timp", "D2", 6.9, 8.0, 70)                      # the flow breaks
for i, p in enumerate("D5 F5 A5 C6 D6 F6".split()):  # six institutions arrive
    add("marimba", p, 9.1 + i * 0.1, 9.7 + i * 0.1, 70 + i * 3)
add("trem", "A2 E3 G3 C#4", 11.8, 13.05, 46)          # the walls rise
ramp("trem", 11, 11.8, 13.0, 40, 118)
add("brass", "A2 E3 A3", 12.95, 13.15, 70)           # routes cut
add("strings", "Bb2 F3 Bb3 D4", 12.95, 13.12, 74)
add("slow", "D6", 13.2, 14.3, 30)

# ---- B : KWIKAMA (14.36 – 23.96) --------------------------------------------------------------
progB = ["Dadd9", "A/C#", "Bm7", "Gmaj7"]
for k, c in enumerate(progB):
    add("pad", CH[c], SB.at(k), SB.at(k + 1), 58)
    add("slow", CH[c], SB.at(k), SB.at(k + 1), 50)
    arpeggio("piano", SB, k, c, 40 if k == 0 else 44, start=2 if k == 0 else 0)
ramp("slow", 11, 14.36, 16.6, 50, 105)
for i, p in enumerate("D4 F#4 A4 D5 E5 F#5 A5 D6".split()):
    add("harp", p, 14.36 + i * 0.045, 16.8, 70)
for i, p in enumerate("D6 F#6 A6 D7 E6 A5 F#5".split()):
    add("celesta", p, 14.42 + i * 0.04, 15.4 + i * 0.04, 58)
melody("piano", SB, 1, HOOK, 64)
add("strings", CH["Asus"], SB.at(3, 2), 23.9, 44)
ramp("strings", 11, SB.at(3, 2), 23.9, 50, 115)

# ---- 1 · contrôle de légalité (23.96 – 49.45) -------------------------------------------------
prog1 = ["Bm", "G", "D", "A", "Bm", "G", "D", "A", "Em", "G", "A"]
chords(S1, prog1, slow=40)
sting(S1.at(0))
melody("slow", S1, 4, HOOK, 52, octave=0)
# validated: a bright major lift; blocked: a stab, then a breath
for p in ["D5", "F#5", "A5"]:
    add("celesta", p, 43.04, 44.4, 56)
add("brass", "B1 F#2 B2", 47.45, 47.8, 96)
add("timp", "B1", 47.45, 48.6, 100)

# ---- 2 · chaîne de garde (49.45 – 68.65) -------------------------------------------------------
prog2 = ["D", "A", "Bm", "G", "D", "A", "Bm", "G"]
chords(S2, prog2, slow=0)
sting(S2.at(0))
# the piece that vanishes on paper (53.97): a falling minor line
for i, p in enumerate(["F5", "E5", "D5", "C#5"]):
    add("slow", p, 53.9 + i * 0.5, 54.5 + i * 0.5, 46)
melody("piano", S2, 4, ANSWER, 58)
for p in ["A5", "D6"]:
    add("celesta", p, 66.19, 67.6, 58)        # "aucun scellé rompu"

# ---- 3 · croisement des dossiers (68.65 – 95.05) -----------------------------------------------
prog3 = ["Em", "C", "G", "D", "Em", "C", "G", "D", "Bm", "G", "A"]
chords(S3, prog3, slow=0)
sting(S3.at(0))
# the map (78.6 – 86.5): sustained discovery
add("slow", "E4 B4 G5", S3.at(4), S3.at(6), 50)
add("slow", "D4 A4 F#5", S3.at(6), S3.at(8), 54)
for i, p in enumerate("E5 G5 B5 D6 E6 G6".split()):
    add("harp", p, 82.6 + i * 0.05, 84.0, 64)
add("timp", "D2", 84.7, 86.2, 104)             # 84 %
for p in ["D6", "A6"]:
    add("celesta", p, 84.7, 86.4, 62)
melody("piano", S3, 8, HOOK, 60)
add("trem", "A3 E4 A4", S3.at(10), 95.0, 56)
ramp("trem", 11, S3.at(10), 95.0, 40, 122)

# ---- 4 · météo de la coopération, puis la vue cloisonnée (95.05 – 122.55) -----------------------
prog4 = ["G", "D", "Em", "C", "G", "D", None, None, None, "G", "D/F#"]
chords(S4, prog4, slow=0)
sting(S4.at(0))
for i, p in enumerate("G5 B5 D6 G6 B6".split()):   # sunshine on the hexagon
    add("celesta", p, 103.6 + i * 0.12, 105.0, 52)
add("timp", "C2", 108.2, 109.4, 96)                # the blockage
# the CENAREF post: muted, filtered, sparse (110.05 – 117.55)
for k, c in [(6, "Em"), (7, "C"), (8, "Em")]:
    add("pad", CH[c], S4.at(k), S4.at(k + 1), 40)
    add("slow", CH[c].split()[1:3], S4.at(k), S4.at(k + 1), 34)
add("strings", "G3 D4 G4 B4", 117.55, S4.at(10), 50)
add("strings", "F#3 D4 A4 D5", S4.at(10), 122.5, 56)
ramp("strings", 11, 117.55, 122.4, 50, 115)
add("brass", "G2 D3 G3 B3", 117.55, 118.6, 64)

# ---- 5 · reversement au Trésor (122.55 – 137.75) ----------------------------------------------
prog5 = ["Bm", "G", "D", "A", "Bm", "G"]
chords(S5, prog5, slow=40)
sting(S5.at(0))
for t, p in [(127.88, "D5"), (128.70, "F#5"), (129.38, "A5"), (130.10, "D6")]:
    add("marimba", p, t, t + 0.7, 96)
    add("celesta", p, t, t + 1.0, 50)
add("celesta", "A6", 131.75, 133.0, 60)          # the Treasury
add("trem", "B3 F#4 B4", 131.3, 137.7, 52)
ramp("trem", 11, 131.3, 137.7, 40, 124)
add("strings", "G3 D4 G4 B4", S5.at(4), S5.at(5), 52)
add("strings", "A3 E4 A4 C#5", S5.at(5), 137.7, 60)
ramp("strings", 11, S5.at(4), 137.7, 60, 124)
add("timp", "A1", 136.3, 137.7, 88)

# ---- résultat immédiat 8 (137.75 – 144.46): the payoff ------------------------------------------
progR = ["D", "A/C#", "G"]
for k, c in enumerate(progR):
    add("pad", CH[c], S6.at(k), S6.at(k + 1) if k < 2 else 143.3, 66)
    add("strings", CH[c], S6.at(k), S6.at(k + 1) if k < 2 else 143.3, 72)
    add("horn", CH[c].split()[1:4], S6.at(k), S6.at(k + 1) if k < 2 else 143.3, 64)
melody("piano", S6, 0, HOOK, 84)
melody("piano", S6, 0, HOOK, 70, octave=-1)
melody("slow", S6, 0, HOOK, 74, octave=1)
add("timp", "D2", 137.75, 139.2, 116)
add("brass", "D3 A3 D4 F#4", 137.75, 138.3, 92)
add("brass", "G2 D3 G3 B3", 142.0, 142.45, 110)    # "devant le GAFI"
add("timp", "G1", 142.0, 143.2, 120)
ramp("strings", 11, 142.6, 143.3, 110, 30)
ramp("pad", 11, 142.6, 143.3, 110, 30)

# ---- signature (144.46 – 153.0) ---------------------------------------------------------------
progF = ["D", "A/C#", "Bm"]
for k, c in enumerate(progF):
    add("pad", CH[c], SF.at(k), SF.at(k + 1), 62)
    add("strings", CH[c], SF.at(k), SF.at(k + 1), 58)
for i, p in enumerate("D5 F#5 A5 D6 E6 F#6 A6 D7".split()):
    add("harp", p, 144.46 + i * 0.04, 146.5, 66)
add("timp", "D2", 144.46, 146.0, 110)
melody("piano", SF, 0, ANSWER, 70)
# final chord, held and fading
add("pad", CH["D"], 151.66, 153.0, 66)
add("strings", "D3 A3 D4 F#4 A4 D5", 151.66, 153.0, 60)
add("piano", "D2 D3 A3 D4 F#4 A4 D5", 151.66, 153.0, 66)
add("celesta", "D6 A6", 151.66, 153.0, 50)
ramp("strings", 11, 151.7, 152.95, 105, 0)
ramp("pad", 11, 151.7, 152.95, 105, 0)

# ---- drums from the GM kit (crashes, rolls) -----------------------------------------------------
CRASH, SNARE, TOM_L, TOM_M, TOM_H, RIDE = 49, 38, 45, 47, 50, 51
for t, v in [(23.96, 70), (49.45, 66), (68.65, 66), (95.05, 66), (117.55, 74), (122.55, 66), (137.75, 108), (142.0, 96), (144.46, 100)]:
    score["drums"].append((CRASH, t, t + 2.5, v))
for j in range(16):   # roll into the payoff
    score["drums"].append((SNARE, S5.at(5, j * 0.25), S5.at(5, j * 0.25) + 0.08, 48 + j * 4))
for j in range(8):    # fill into each chapter
    for S in (S1, S2, S3, S4):
        score["drums"].append((SNARE, S.at(S.n - 1, 2 + j * 0.25), S.at(S.n - 1, 2 + j * 0.25) + 0.07, 34 + j * 5))

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

# heartbeat under Kolwezi, a clock while the institutions wait
for t in (0.82, 3.2, 5.6):
    place(bus["kick"], heartbeat(), t, 0.55)
    place(bus["kick"], heartbeat(), t + 0.3, 0.3)
for j in range(int((13.6 - 8.9) / 0.6) + 1):
    t = 8.9 + j * 0.6
    g = 0.05 + (t - 8.9) / (13.6 - 8.9) * 0.12
    place(bus["tick"], tick(j % 2 == 0), t, g, pan=0.25 if j % 2 else -0.25)
for t in np.arange(8.9, 12.9, 0.3):
    r = "D2" if t < 11.8 else "G1"
    place(bus["bass"], bassnote(hz(r), 0.24), t, 0.28)
# impacts and risers
place(bus["fx"], boom(1.2, 66, 30), 12.95, 0.45)
place(bus["fx"], rev_cymbal(1.2), 13.16, 0.45)
place(bus["fx"], boom(3.5, 58, 26), 14.36, 0.6)
place(bus["fx"], riser(1.6), 22.36, 0.3)
place(bus["fx"], boom(1.4, 70, 30), 47.45, 0.7)
place(bus["fx"], rev_cymbal(1.3), 48.15, 0.4)
place(bus["fx"], rev_cymbal(1.2), 67.45, 0.38)
place(bus["fx"], boom(2.6, 60, 27), 84.7, 0.55)
place(bus["fx"], riser(1.8), 93.25, 0.35)
place(bus["fx"], boom(1.2, 62, 30), 108.2, 0.4)
place(bus["fx"], rev_cymbal(1.4), 116.15, 0.4)
place(bus["fx"], riser(1.5), 121.05, 0.3)
place(bus["fx"], riser(2.6), 135.15, 0.45)
place(bus["fx"], rev_cymbal(2.0), 135.75, 0.55)
place(bus["fx"], boom(3.0, 66, 28), 137.75, 0.85)
place(bus["fx"], boom(1.8, 64, 28), 142.0, 0.75)
place(bus["fx"], rev_cymbal(1.0), 143.46, 0.5)
place(bus["fx"], boom(3.4, 66, 27), 144.46, 0.9)
for t in (23.96, 49.45, 68.65, 95.05, 122.55):      # each chapter card
    place(bus["fx"], boom(1.6, 64, 30), t, 0.4)


def groove(S, k, c, kick_pat, clap_on, hat_div, shaker_on, bass_on, pluck_on, pluck_div=0.5, level=1.0, dark=False):
    root = {"Bm": "B1", "G": "G1", "D": "D2", "A": "A1", "Em": "E2", "Asus": "A1", "A/C#": "A1", "Dadd9": "D2",
            "C": "C2", "D/F#": "D2", "Am": "A1", "Gmaj7": "G1", "Bm7": "B1"}[c]
    at = lambda b: S.at(k, b)
    for b in kick_pat:
        place(bus["kick"], K, at(b), 0.85 * level)
    if clap_on:
        for b in (1, 3):
            place(bus["clap"], CL, at(b), 0.55 * level, pan=0.05)
    if hat_div:
        for j in range(int(4 / hat_div)):
            accent = 1.0 if (j * hat_div) % 1 == 0.5 else 0.6
            place(bus["hats"], HT, at(j * hat_div), 0.32 * accent * level, pan=0.3)
    if shaker_on:
        for j in range(16):
            place(bus["shaker"], SH, at(j * 0.25), (0.25 if j % 2 else 0.15) * level, pan=-0.35)
    if bass_on:
        for j in range(8):
            f = hz(root) * (2 if j in (3, 7) else 1)
            place(bus["bass"], bassnote(f, S.beat * 0.45), at(j * 0.5), 0.5 * level)
    if pluck_on:
        notes = chord(CH[c])
        tones = [notes[1] + 12, notes[3] + 12, notes[4] + 12, notes[3] + 12, notes[2] + 12, notes[4] + 12, notes[3] + 24, notes[4] + 12]
        for j in range(int(4 / pluck_div)):
            p = tones[j % len(tones)]
            v = 0.16 if j % 2 else 0.22
            sig = pluck(pretty_midi.note_number_to_hz(p), 0.5)
            if dark:
                sig = lp(sig, 1600)
            place(bus["pluck"], sig, at(j * pluck_div), v * level, pan=(-0.4 if j % 2 else 0.4))


# reveal: plucks join on "Suivons-le" (bar 2)
for k, c in enumerate(progB):
    if k >= 2:
        groove(SB, k, c, kick_pat=(0,) if k == 3 else (), clap_on=False, hat_div=0.5 if k == 3 else 0, shaker_on=k == 3,
               bass_on=k == 3, pluck_on=True, level=0.75)
# 1 · légalité
for k, c in enumerate(prog1):
    groove(S1, k, c, kick_pat=(0, 2) if k < 4 else (0, 1.5, 2), clap_on=k >= 4, hat_div=0.5, shaker_on=True,
           bass_on=True, pluck_on=True, pluck_div=0.5 if k < 8 else 0.25, level=0.88)
# the lock: the groove stops for a breath (47.45 – 48.2)
for name in ["kick", "clap", "hats", "shaker", "bass", "pluck"]:
    a, b = int(47.4 * SR), int(48.25 * SR)
    bus[name][a:b] *= 0.0
# 2 · chaîne de garde: the paper problem is bare (bars 1 – 2), the answer comes back full
for k, c in enumerate(prog2):
    bare = k in (1, 2)
    groove(S2, k, c, kick_pat=() if bare else ((0, 2) if k < 5 else (0, 1.5, 2)), clap_on=k >= 4, hat_div=0 if bare else 0.5,
           shaker_on=not bare, bass_on=not bare, pluck_on=True, dark=bare, level=0.86)
# 3 · croisement: half-time on the map (bars 4 – 7), full on the infrastructure
for k, c in enumerate(prog3):
    mapb = 4 <= k <= 7
    groove(S3, k, c, kick_pat=(0,) if mapb else ((0, 2) if k < 4 else (0, 1, 2, 3)), clap_on=not mapb and k >= 2,
           hat_div=0 if mapb else (0.5 if k < 8 else 0.25), shaker_on=not mapb, bass_on=not mapb or k == 7, pluck_on=True,
           pluck_div=0.5 if k < 8 else 0.25, dark=mapb, level=0.88)
# 4 · coopération; the CENAREF post is muted (bars 6 – 8)
for k, c in enumerate(prog4):
    if c is None:
        continue
    groove(S4, k, c, kick_pat=(0, 2) if k < 2 else (0, 1.5, 2), clap_on=k >= 2, hat_div=0.5 if k < 9 else 0.25,
           shaker_on=True, bass_on=True, pluck_on=True, pluck_div=0.5, level=0.86)
for k, c in [(6, "Em"), (7, "C"), (8, "Em")]:
    groove(S4, k, c, kick_pat=(), clap_on=False, hat_div=0, shaker_on=False, bass_on=False, pluck_on=True,
           pluck_div=0.5, dark=True, level=0.7)
# 5 · reversement
for k, c in enumerate(prog5):
    groove(S5, k, c, kick_pat=(0, 2) if k < 3 else (0, 1, 2, 3), clap_on=k >= 1, hat_div=0.5 if k < 4 else 0.25,
           shaker_on=True, bass_on=True, pluck_on=True, pluck_div=0.5 if k < 4 else 0.25, level=0.9)
# payoff
for k, c in enumerate(progR):
    groove(S6, k, c, kick_pat=(0, 1, 2, 3), clap_on=True, hat_div=0.25, shaker_on=True, bass_on=True, pluck_on=True,
           pluck_div=0.25, level=1.08)
    for b in (0.5, 1.5, 2.5, 3.5):
        place(bus["hats"], HO, S6.at(k, b), 0.2, pan=0.35)
for name in ["kick", "clap", "hats", "shaker", "bass", "pluck"]:   # the panel empties: silence before the logo
    a, b = int(143.25 * SR), int(144.46 * SR)
    bus[name][a:b] *= np.linspace(1, 0, b - a)[:, None] ** 2
    bus[name][b:] *= 0.0
# signature: one soft pulse
for k, c in enumerate(progF):
    groove(SF, k, c, kick_pat=(0,), clap_on=False, hat_div=0, shaker_on=False, bass_on=True, pluck_on=True, pluck_div=0.5, level=0.7)
place(bus["kick"], K, 144.46, 1.0)
place(bus["bass"], bassnote(hz("D2"), 1.3), 151.66, 0.55)

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

# arrangement automation: a breath before the reveal, a warmer reveal, a lifted payoff
t_ax = np.arange(N) / SR
auto = np.ones(N)
def seg_gain(t0, t1, g, ramp_in=0.3, ramp_out=0.3):
    up = np.clip((t_ax - (t0 - ramp_in)) / ramp_in, 0, 1)
    down = np.clip(((t1 + ramp_out) - t_ax) / ramp_out, 0, 1)
    return 1 + (g - 1) * np.minimum(up, down)
auto *= seg_gain(13.45, 14.25, 10 ** (-12 / 20), ramp_in=0.3, ramp_out=0.1)   # breath before KWIKAMA
auto *= seg_gain(14.4, 23.0, 10 ** (3 / 20), ramp_in=0.1, ramp_out=0.6)       # a warmer reveal
auto *= seg_gain(138.0, 142.4, 10 ** (2 / 20), ramp_in=0.2, ramp_out=0.3)     # the payoff
auto *= seg_gain(51.9, 56.0, 10 ** (8 / 20), ramp_in=0.4, ramp_out=0.4)       # the bare paper route
auto *= seg_gain(78.9, 83.2, 10 ** (6 / 20), ramp_in=0.4, ramp_out=0.5)       # the map
auto *= seg_gain(110.2, 116.6, 10 ** (9 / 20), ramp_in=0.3, ramp_out=0.4)     # the CENAREF post
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
