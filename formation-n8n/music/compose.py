"""Original score for the CHRONOCONCEPT GROUP n8n training film.

120 BPM, 4/4, 28 bars = 56 s. One bar = 2 s, so every section boundary sits
on an even second that the picture also cuts on.

  bars  1-5   0-10 s  tension: tic-tac clock, pizzicato ostinato (repetitive tasks), filtered pad
  bars  6-12 10-24 s  drop on "Avec n8n": F C G Am, kalimba hook, house groove
  bars 13-15 24-30 s  lift: Dm F Gsus G, snare build
  bars 16-17 30-34 s  peak: title "Formation Automatisation n8n", strings
  bars 18-19 34-38 s  Kinshasa: congas + sebene guitar (Congolese rumba nod)
  bars 20-24 38-48 s  call to action: lighter groove under the contact details
  bar  25    48-50 s  breakdown + riser
  bars 26-28 50-56 s  impact on the logo, final cadence, ring-out

Melodic stems are written as MIDI and rendered with FluidSynth (FluidR3 GM);
drums, bass, risers and impacts are synthesised here with numpy.
Run:  python3 compose.py  -> stems/*.wav and music-master.wav
"""
import os
import subprocess
import numpy as np
import mido

SR = 44100
BPM = 120
BEAT = 60 / BPM            # 0.5 s
BAR = 4 * BEAT             # 2.0 s
BARS = 28
DUR = BARS * BAR           # 56 s
N = int(DUR * SR) + SR * 3  # tail room for reverbs
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
HERE = os.path.dirname(os.path.abspath(__file__))
STEMS = os.path.join(HERE, "stems")
os.makedirs(STEMS, exist_ok=True)
rng = np.random.default_rng(243)  # seeded: the score renders identically every time


def t_of(bar, beat=0.0):
    """Seconds at a 1-indexed bar and 0-indexed beat."""
    return (bar - 1) * BAR + beat * BEAT


# ---------------------------------------------------------------- harmony
NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def n(name, octave):
    return 12 * (octave + 1) + NOTE[name]


CHORDS = {  # voicings around middle C (piano / pads)
    "Am": [n("A", 3), n("C", 4), n("E", 4), n("B", 4)],
    "F": [n("F", 3), n("A", 3), n("C", 4), n("E", 4)],
    "C": [n("C", 4), n("E", 4), n("G", 4), n("D", 5)],
    "G": [n("G", 3), n("B", 3), n("D", 4), n("A", 4)],
    "Dm": [n("D", 4), n("F", 4), n("A", 4), n("C", 5)],
    "Gsus": [n("G", 3), n("C", 4), n("D", 4), n("G", 4)],
}
ROOT = {"Am": n("A", 1), "F": n("F", 1), "C": n("C", 2), "G": n("G", 1), "Dm": n("D", 2), "Gsus": n("G", 1)}

# one chord per bar (two per bar written as a tuple)
PROG = {
    1: "Am", 2: "Am", 3: "Am", 4: "Am", 5: "Am",
    6: "F", 7: "C", 8: "G", 9: "Am", 10: "F", 11: "C", 12: "G",
    13: "Dm", 14: "F", 15: ("Gsus", "G"),
    16: ("F", "C"), 17: ("G", "Am"),
    18: "C", 19: "G",
    20: "F", 21: "C", 22: "G", 23: "Am", 24: "F",
    25: "Gsus", 26: "F", 27: "C", 28: "C",
}


def chord_at(bar, half=0):
    c = PROG[bar]
    if isinstance(c, tuple):
        return c[half]
    return c


# ---------------------------------------------------------------- MIDI stems
class Stem:
    def __init__(self, name, program, channel=0, volume=100):
        self.name, self.program, self.channel, self.volume = name, program, channel, volume
        self.events = []  # (time_s, note, vel, dur_s)

    def add(self, t, note, vel, dur):
        self.events.append((t, note, int(np.clip(vel, 1, 127)), dur))

    def render(self, gain=0.5, reverb=True):
        mid = mido.MidiFile(ticks_per_beat=480)
        tr = mido.MidiTrack()
        mid.tracks.append(tr)
        tr.append(mido.MetaMessage("set_tempo", tempo=int(BEAT * 1e6)))
        if self.channel != 9:
            tr.append(mido.Message("program_change", program=self.program, channel=self.channel))
        tr.append(mido.Message("control_change", control=7, value=self.volume, channel=self.channel))
        tr.append(mido.Message("control_change", control=91, value=40 if reverb else 0, channel=self.channel))
        tr.append(mido.Message("control_change", control=93, value=10, channel=self.channel))
        msgs = []
        for t, note, vel, dur in self.events:
            msgs.append((t, 1, note, vel))
            msgs.append((t + dur, 0, note, 0))
        msgs.sort(key=lambda m: (m[0], m[1]))
        tick_now = 0
        for t, on, note, vel in msgs:
            tick = int(round(t / BEAT * 480))
            delta = max(0, tick - tick_now)
            tick_now += delta
            kind = "note_on" if on else "note_off"
            tr.append(mido.Message(kind, note=note, velocity=vel, channel=self.channel, time=delta))
        path_mid = os.path.join(STEMS, self.name + ".mid")
        path_wav = os.path.join(STEMS, self.name + ".wav")
        mid.save(path_mid)
        subprocess.run(
            ["fluidsynth", "-ni", "-q", "-g", str(gain), "-r", str(SR), "-R", "1" if reverb else "0",
             "-C", "0", "-F", path_wav, SF2, path_mid],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return load_wav(path_wav)


def load_wav(path):
    import wave
    with wave.open(path) as w:
        ch, sw, sr, frames = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(frames)
    assert sr == SR, (path, sr)
    data = np.frombuffer(raw, dtype=np.int16 if sw == 2 else np.int32).astype(np.float32)
    data /= 32768.0 if sw == 2 else 2147483648.0
    data = data.reshape(-1, ch)
    if ch == 1:
        data = np.repeat(data, 2, axis=1)
    out = np.zeros((N, 2), np.float32)
    m = min(N, len(data))
    out[:m] = data[:m]
    return out


# ---------------------------------------------------------------- DSP helpers
def buf():
    return np.zeros((N, 2), np.float32)


def place(dst, sig, t, gain=1.0, pan=0.0):
    """Mix mono or stereo `sig` into dst at time t (s), constant-power pan."""
    i = int(round(t * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        l = np.cos((pan + 1) * np.pi / 4)
        r = np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l * 1.4142, sig * r * 1.4142], axis=1)
    m = min(len(sig), N - i)
    dst[i:i + m] += sig[:m] * gain


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    s = 0.0
    for k in range(len(x)):
        s = (1 - a) * x[k] + a * s
        y[k] = s
    return y


def biquad(x, kind, fc, q=0.707):
    """RBJ biquad on a mono array; vectorised enough for short one-shots."""
    from scipy.signal import lfilter
    w0 = 2 * np.pi * fc / SR
    alpha = np.sin(w0) / (2 * q)
    c = np.cos(w0)
    if kind == "lp":
        b = [(1 - c) / 2, 1 - c, (1 - c) / 2]
    elif kind == "hp":
        b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]
    else:  # band-pass, 0 dB peak
        b = [alpha, 0, -alpha]
    a = [1 + alpha, -2 * c, 1 - alpha]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def filt(x, kind, fc, q=0.707):
    if x.ndim == 2:
        return np.stack([biquad(x[:, 0], kind, fc, q), biquad(x[:, 1], kind, fc, q)], axis=1).astype(np.float32)
    return biquad(x, kind, fc, q).astype(np.float32)


def env_exp(length, decay):
    tt = np.arange(int(length * SR)) / SR
    return np.exp(-tt / decay)


def noise(length):
    return rng.standard_normal(int(length * SR)).astype(np.float32)


def reverb_ir(seconds=2.2, damp=4500):
    """Synthetic stereo room: decaying filtered noise with a few early reflections."""
    L = int(seconds * SR)
    tt = np.arange(L) / SR
    ir = np.zeros((L, 2), np.float32)
    for ch in range(2):
        nz = rng.standard_normal(L) * np.exp(-tt / (seconds / 6.9))
        nz = biquad(nz, "lp", damp)
        ir[:, ch] = nz
        for d, g in [(0.011, 0.5), (0.019, 0.35), (0.027 + ch * 0.004, 0.3), (0.041, 0.22)]:
            ir[int(d * SR), ch] += g
    ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True))
    return ir


def convolve_reverb(x, ir, wet=0.2):
    from scipy.signal import fftconvolve
    y = np.stack([fftconvolve(x[:, c], ir[:, c])[:N] for c in range(2)], axis=1)
    return (x * (1 - wet * 0.3) + y * wet).astype(np.float32)


# ---------------------------------------------------------------- synth voices
def kick(vel=1.0):
    L = 0.45
    tt = np.arange(int(L * SR)) / SR
    f = 46 + 110 * np.exp(-tt / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-tt / 0.22)
    click = biquad(noise(L), "hp", 3000) * np.exp(-tt / 0.004) * 0.35
    return (np.tanh((body + click) * 1.6) * 0.9 * vel).astype(np.float32)


def clap(vel=1.0):
    L = 0.35
    tt = np.arange(int(L * SR)) / SR
    e = np.zeros_like(tt)
    for d in (0.0, 0.011, 0.022):
        e += (tt >= d) * np.exp(-(tt - d).clip(0) / 0.006)
    e += (tt >= 0.03) * np.exp(-(tt - 0.03).clip(0) / 0.09) * 0.6
    s = biquad(noise(L), "bp", 1600, 0.9) * e
    return (s * 1.6 * vel).astype(np.float32)


def hat(open_=False, vel=1.0):
    L = 0.25 if open_ else 0.06
    tt = np.arange(int(L * SR)) / SR
    s = biquad(biquad(noise(L), "hp", 7500), "hp", 7500) * np.exp(-tt / (0.07 if open_ else 0.013))
    return (s * 0.55 * vel).astype(np.float32)


def shaker(vel=1.0):
    L = 0.09
    tt = np.arange(int(L * SR)) / SR
    e = (1 - np.exp(-tt / 0.012)) * np.exp(-tt / 0.025)
    s = biquad(noise(L), "bp", 6500, 1.2) * e
    return (s * 0.9 * vel).astype(np.float32)


def snare(vel=1.0):
    L = 0.25
    tt = np.arange(int(L * SR)) / SR
    tone = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.05) * 0.5
    nz = biquad(noise(L), "hp", 1800) * np.exp(-tt / 0.07)
    return ((tone + nz) * 0.7 * vel).astype(np.float32)


def tick(high=True, vel=1.0):
    """Clock escapement: a short woody tick (Chrono)."""
    L = 0.05
    tt = np.arange(int(L * SR)) / SR
    f = 2600 if high else 1900
    s = np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.006)
    s += biquad(noise(L), "bp", f * 1.5, 3) * np.exp(-tt / 0.003) * 0.5
    return (s * 0.5 * vel).astype(np.float32)


def crash(L=3.0, vel=1.0):
    tt = np.arange(int(L * SR)) / SR
    metal = np.zeros_like(tt)
    for f in (420, 563, 811, 1033, 1377, 1702, 2311):
        metal += np.sign(np.sin(2 * np.pi * f * tt + f))
    s = biquad(noise(L) + metal * 0.08, "hp", 5000) * np.exp(-tt / 0.9)
    s *= 1 - np.exp(-tt / 0.002)
    return (s * 0.5 * vel).astype(np.float32)


def riser(L=2.0, vel=1.0):
    tt = np.arange(int(L * SR)) / SR
    x = noise(L)
    out = np.zeros_like(x)
    seg = int(0.05 * SR)
    for k in range(0, len(x), seg):  # sweep a band-pass upwards in 50 ms blocks
        fc = 400 * (12000 / 400) ** (k / len(x))
        out[k:k + seg] = biquad(x[k:k + seg + 2048], "bp", fc, 1.4)[:len(out[k:k + seg])]
    sweep = np.sin(2 * np.pi * np.cumsum(220 * (8 ** (tt / L))) / SR) * 0.12
    e = (tt / L) ** 2.2
    return ((out * 0.9 + sweep) * e * vel).astype(np.float32)


def reverse_cymbal(L=1.5, vel=1.0):
    return crash(L, vel)[::-1].copy()


def impact(vel=1.0):
    L = 2.6
    tt = np.arange(int(L * SR)) / SR
    f = 38 + 60 * np.exp(-tt / 0.08)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.7)
    hit = biquad(noise(L), "lp", 2500) * np.exp(-tt / 0.12) * 0.6
    return (np.tanh((boom + hit) * 1.4) * 0.9 * vel).astype(np.float32)


def bass_note(midi, length, vel=1.0):
    """Warm synth bass: sine sub + low-passed saw, plucky envelope."""
    f = 440 * 2 ** ((midi - 69) / 12)
    tt = np.arange(int(length * SR)) / SR
    sub = np.sin(2 * np.pi * f * tt)
    saw = 2 * ((f * tt) % 1) - 1
    saw = biquad(saw, "lp", 380 + 900 * 0.3, 0.9)
    e = (1 - np.exp(-tt / 0.004)) * np.exp(-tt / 0.6)
    rel = np.clip((length - tt) / 0.03, 0, 1)
    return ((sub * 0.8 + saw * 0.45) * e * rel * vel).astype(np.float32)


def pad_chord(notes, length, bright=1.0):
    """Supersaw-ish pad, low-passed; used for the intro tension and the glue."""
    tt = np.arange(int(length * SR)) / SR
    s = np.zeros((len(tt), 2), np.float32)
    for k, m in enumerate(notes):
        f = 440 * 2 ** ((m - 69) / 12)
        for det, pan in ((-0.12, -0.7), (0.0, 0.0), (0.11, 0.7)):
            ff = f * 2 ** (det / 12)
            w = 2 * ((ff * tt + 0.37 * k) % 1) - 1
            s[:, 0] += w * np.cos((pan + 1) * np.pi / 4)
            s[:, 1] += w * np.sin((pan + 1) * np.pi / 4)
    s = filt(s, "lp", 900 * bright, 0.6)
    a = np.clip(tt / 0.6, 0, 1) * np.clip((length - tt) / 0.5, 0, 1)
    return (s * a[:, None] * 0.05).astype(np.float32)


# ---------------------------------------------------------------- write the score
def write_score():
    stems = {}

    # ---- intro ostinato: pizzicato strings, the "same task again" figure
    pizz = Stem("pizz", 45, volume=96)
    figure = [n("A", 4), n("C", 5), n("E", 5), n("C", 5)]
    for bar in range(1, 5):
        for s16 in range(16):
            if bar == 4 and s16 >= 6:      # stops on "Et si tout ça…"
                break
            if bar == 1 and s16 < 8:       # enters half a bar in
                continue
            t = t_of(bar, s16 / 4)
            vel = 70 + (18 if s16 % 4 == 0 else 0) + bar * 6
            pizz.add(t, figure[s16 % 4], vel, 0.11)
    stems["pizz"] = pizz

    # ---- piano: syncopated stabs from the drop
    piano = Stem("piano", 0, volume=100)
    stab = [0, 1.5, 2.5, 3.5]  # beats
    for bar in list(range(6, 18)) + list(range(20, 25)) + [26, 27]:
        for b in stab:
            half = 0 if b < 2 else 1
            ch = CHORDS[chord_at(bar, half)]
            vel = 82 if b == 0 else 66
            if 20 <= bar <= 24:
                vel -= 12  # lighter under the contact details
            for m in ch:
                piano.add(t_of(bar, b), m + 12 if m < n("C", 4) else m, vel, 0.42)
    # final chord rings
    for m in CHORDS["C"]:
        piano.add(t_of(28), m, 90, 3.5)
        piano.add(t_of(28), m - 12, 80, 3.5)
    stems["piano"] = piano

    # ---- kalimba hook (thumb piano: a nod to the Congolese likembe)
    kal = Stem("kalimba", 108, volume=110)
    hook = {  # 8th-note lines per chord, two octaves above the pad
        "F": [n("A", 5), n("C", 6), n("F", 6), n("C", 6), n("A", 5), n("G", 5), n("A", 5), n("C", 6)],
        "C": [n("G", 5), n("C", 6), n("E", 6), n("C", 6), n("G", 5), n("E", 5), n("G", 5), n("D", 6)],
        "G": [n("B", 5), n("D", 6), n("G", 6), n("D", 6), n("B", 5), n("A", 5), n("B", 5), n("D", 6)],
        "Am": [n("C", 6), n("E", 6), n("A", 6), n("E", 6), n("C", 6), n("B", 5), n("A", 5), n("E", 5)],
        "Dm": [n("A", 5), n("D", 6), n("F", 6), n("D", 6), n("A", 5), n("F", 5), n("A", 5), n("C", 6)],
        "Gsus": [n("G", 5), n("C", 6), n("D", 6), n("G", 6), n("D", 6), n("C", 6), n("G", 5), n("D", 6)],
    }
    for bar in list(range(6, 18)) + list(range(20, 25)) + [26, 27]:
        for e in range(8):
            if 20 <= bar <= 24 and e % 2 == 1:
                continue  # sparser under speech
            half = 0 if e < 4 else 1
            line = hook[chord_at(bar, half)]
            vel = 92 if e % 2 == 0 else 74
            if bar in (16, 17, 26, 27):
                vel += 12
            kal.add(t_of(bar, e / 2), line[e], vel, 0.45)
    stems["kalimba"] = kal

    # ---- strings: lift, peak and outro
    strings = Stem("strings", 48, volume=92)
    for bar in list(range(13, 18)) + [25, 26, 27]:
        for half in (0, 1):
            if not isinstance(PROG[bar], tuple) and half == 1:
                continue
            ch = CHORDS[chord_at(bar, half)]
            length = BAR / (2 if isinstance(PROG[bar], tuple) else 1)
            for m in ch[:3]:
                strings.add(t_of(bar, half * 2), m, 78 if bar < 16 else 92, length * 0.98)
            strings.add(t_of(bar, half * 2), ch[0] - 12, 70, length * 0.98)
    for m in (n("C", 4), n("E", 4), n("G", 4), n("C", 3)):
        strings.add(t_of(28), m, 88, 3.8)
    stems["strings"] = strings

    # ---- sebene guitar for Kinshasa (bars 18-19) and a reprise in the outro
    gtr = Stem("sebene", 27, volume=100)
    seb = {
        "C": [n("E", 5), n("G", 5), n("C", 6), n("G", 5), n("E", 5), n("G", 5), n("C", 6), n("E", 6)],
        "G": [n("D", 5), n("G", 5), n("B", 5), n("G", 5), n("D", 5), n("G", 5), n("B", 5), n("D", 6)],
        "F": [n("C", 5), n("F", 5), n("A", 5), n("F", 5), n("C", 5), n("F", 5), n("A", 5), n("C", 6)],
    }
    for bar in (18, 19, 26, 27):
        line = seb[chord_at(bar)]
        for s16 in range(16):
            note = line[s16 % 8]
            vel = 88 if s16 % 4 == 0 else (74 if s16 % 2 == 0 else 62)
            if bar >= 26:
                vel -= 14
            gtr.add(t_of(bar, s16 / 4), note, vel, 0.12)
            if s16 % 2 == 0:  # parallel thirds, rumba style
                gtr.add(t_of(bar, s16 / 4), note - 4 if note % 12 in (4, 11) else note - 3, vel - 16, 0.12)
    stems["sebene"] = gtr

    # ---- congas and maracas (GM drum channel), Kinshasa section and outro
    perc = Stem("congas", 0, channel=9, volume=105)
    pat = {0: 62, 3: 63, 6: 63, 8: 62, 10: 64, 11: 63, 14: 64}
    for bar in (18, 19, 20, 21, 22, 23, 24, 26, 27):
        for s16, note in pat.items():
            perc.add(t_of(bar, s16 / 4), note, 96 if s16 in (0, 8) else 80, 0.2)
        for s16 in range(0, 16, 2):
            perc.add(t_of(bar, s16 / 4), 70, 60 + (20 if s16 % 4 == 2 else 0), 0.1)
    stems["congas"] = perc
    return stems


def synth_layers():
    drums, bass, fx, pad, clock = buf(), buf(), buf(), buf(), buf()

    # clock tic-tac through the intro, accelerating attention in bar 4-5
    for bar in range(1, 6):
        for e in range(8):
            t = t_of(bar, e / 2)
            vel = 0.55 if e % 2 == 0 else 0.4
            if bar >= 4:
                vel *= 0.8
            place(clock, tick(e % 2 == 0, vel), t, pan=-0.25 if e % 2 else 0.25)
    # heartbeat kick under the question (bar 5)
    for b in (0, 1.75, 2, 3.75):
        place(drums, kick(0.45), t_of(5, b))

    # groove sections
    groove_bars = list(range(6, 25)) + [26, 27]
    for bar in groove_bars:
        light = 20 <= bar <= 24
        build = bar in (13, 14, 15)
        for b in range(4):
            if not (bar == 15 and b >= 2):
                place(drums, kick(0.95 if not light else 0.8), t_of(bar, b))
            place(drums, hat(True, 0.5 if not light else 0.35), t_of(bar, b + 0.5), pan=0.3)
        if not light:
            for b in (1, 3):
                place(drums, clap(0.75), t_of(bar, b), pan=-0.05)
        for s16 in range(16):
            acc = 1.0 if s16 % 4 == 2 else 0.55
            place(drums, shaker(0.4 * acc), t_of(bar, s16 / 4), pan=0.45)
        if build:
            for s16 in range(16):
                if bar == 15 or s16 % 2 == 0:
                    v = 0.25 + 0.6 * ((bar - 13) * 16 + s16) / 48
                    place(drums, snare(v), t_of(bar, s16 / 4), pan=-0.15)

    # bass: syncopated root / fifth figure
    bass_bars = list(range(6, 25)) + [26, 27]
    for bar in bass_bars:
        for half in (0, 1):
            c = chord_at(bar, half)
            r = ROOT[c]
            if half == 0:
                place(bass, bass_note(r, 0.7, 0.9), t_of(bar, 0))
                place(bass, bass_note(r, 0.22, 0.6), t_of(bar, 1.5))
            else:
                place(bass, bass_note(r if not isinstance(PROG[bar], tuple) else r, 0.45, 0.8), t_of(bar, 2))
                place(bass, bass_note(r + 7, 0.22, 0.6), t_of(bar, 3.5))
    # final root under the last chord
    place(bass, bass_note(ROOT["C"], 3.2, 0.9), t_of(28))
    place(bass, bass_note(ROOT["C"] - 12 + 12, 0.0001), 0)  # no-op keeps signature honest

    # pads: tension pad in the intro opening up, glue pad later
    for bar in range(1, 6):
        place(pad, pad_chord(CHORDS["Am"], BAR + 0.4, bright=0.45 + 0.18 * bar), t_of(bar))
    for bar in range(6, 28):
        for half in (0, 1):
            if not isinstance(PROG[bar], tuple) and half == 1:
                continue
            length = BAR / (2 if isinstance(PROG[bar], tuple) else 1)
            place(pad, pad_chord(CHORDS[chord_at(bar, half)], length + 0.3, bright=1.0), t_of(bar, half * 2), gain=0.8)
    place(pad, pad_chord(CHORDS["C"], 4.0, bright=1.2), t_of(28), gain=0.9)

    # transitions: each one has a cause on screen
    place(fx, riser(2.0, 0.55), t_of(5) - 0.05)                # into the drop "Avec n8n"
    place(fx, reverse_cymbal(1.5, 0.6), t_of(6) - 1.5)
    place(fx, crash(3.0, 0.55), t_of(6))
    place(fx, riser(2.0, 0.45), t_of(15) - 0.05)               # into the title
    place(fx, crash(3.0, 0.6), t_of(16))
    place(fx, reverse_cymbal(1.2, 0.4), t_of(18) - 1.2)        # into Kinshasa
    place(fx, crash(2.4, 0.4), t_of(18))
    place(fx, riser(2.0, 0.6), t_of(25) - 0.02)                # into the logo
    place(fx, reverse_cymbal(1.6, 0.6), t_of(26) - 1.6)
    place(fx, impact(0.9), t_of(26))
    place(fx, crash(3.5, 0.6), t_of(26))
    place(fx, crash(3.0, 0.35), t_of(28))
    return drums, bass, fx, pad, clock


def sidechain_env(times, depth=0.45, release=0.22):
    """Pump the pads and bass against the kick, like a house record."""
    e = np.ones(N, np.float32)
    rel = np.exp(-np.arange(int(0.45 * SR)) / SR / release)
    shape = 1 - depth * rel
    for t in times:
        i = int(t * SR)
        m = min(len(shape), N - i)
        e[i:i + m] = np.minimum(e[i:i + m], shape[:m])
    return e[:, None]


def main():
    stems = write_score()
    gains = {"pizz": 0.75, "piano": 0.55, "kalimba": 0.65, "strings": 0.55, "sebene": 0.55, "congas": 0.7}
    audio = {k: s.render(gain=gains[k]) for k, s in stems.items()}
    drums, bass, fx, pad, clock = synth_layers()

    # intro ostinato sits behind a low-pass that opens toward the drop
    pz = audio["pizz"]
    audio["pizz"] = pz

    kicks = [t_of(bar, b) for bar in list(range(6, 25)) + [26, 27] for b in range(4) if not (bar == 15 and b >= 2)]
    sc = sidechain_env(kicks)
    bass = bass * sc
    pad = pad * sc

    levels = {  # mix gains, set from the measured contributions printed below
        "drums": (drums, 0.27), "bass": (bass, 0.40), "pad": (pad, 0.80), "clock": (clock, 0.55),
        "fx": (fx, 0.45), "pizz": (audio["pizz"], 1.5), "piano": (audio["piano"], 2.9),
        "kalimba": (audio["kalimba"], 3.4), "strings": (audio["strings"], 2.0),
        "sebene": (audio["sebene"], 2.4), "congas": (audio["congas"], 1.3),
    }
    mix = buf()
    a, b = int(10 * SR), int(30 * SR)
    for name, (sig, g) in levels.items():
        mix += sig * g
        seg = (sig[a:b] * g).mean(axis=1)
        act = np.abs(seg) > 1e-4
        r = np.sqrt((seg[act] ** 2).mean()) if act.any() else 0
        print(f"  {name:8s} contribution {20 * np.log10(r + 1e-9):6.1f} dBFS (10-30 s, while active)")
    ir = reverb_ir(2.4)
    mix = convolve_reverb(mix, ir, wet=0.16)

    # keep the low end tidy, then glue
    mix = filt(mix, "hp", 32)
    # gentle bus compression (RMS follower) then a soft-clip limiter
    rms = np.sqrt(np.convolve((mix ** 2).mean(axis=1), np.ones(2205) / 2205, mode="same")) + 1e-6
    thr = 0.18
    gr = np.where(rms > thr, (thr / rms) ** 0.35, 1.0)
    gr = onepole_lp(gr.astype(np.float64), 8).astype(np.float32)
    mix = mix * gr[:, None]

    # fades: start at full energy on frame 0, ring out under the end card
    total = int(DUR * SR)
    mix = mix[:total]
    fade_in = int(0.02 * SR)
    mix[:fade_in] *= np.linspace(0, 1, fade_in)[:, None]
    fo = int(1.8 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5

    peak = np.abs(mix).max()
    mix = mix / peak * 0.89  # -1 dBFS peak before loudness normalisation
    mix = np.tanh(mix * 1.15) / np.tanh(1.15)

    import soundfile as sf
    sf.write(os.path.join(HERE, "music-master.wav"), mix, SR, subtype="PCM_24")
    for name, a in [("drums", drums), ("bass", bass), ("fx", fx), ("pad", pad), ("clock", clock)]:
        sf.write(os.path.join(STEMS, name + ".wav"), a[:total] / max(1e-6, np.abs(a).max()) * 0.9, SR)
    print("wrote music-master.wav", mix.shape, "peak", np.abs(mix).max())


if __name__ == "__main__":
    main()
