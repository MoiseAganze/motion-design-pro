"""Voice treatment + music ducking for the film.

  voice  : assets/audio/voix-off.mp3 (ElevenLabs, raw)  -> assets/audio/voix-off.wav
           high-pass, light compression, dual-mono stereo at -16 LUFS, true peak -1.5 dBTP
  music  : music/music-master.wav -> assets/audio/musique.wav
           ducked under the voice (the voice clip starts at VO_OFFSET in the film)
  check  : music/mix-preview.wav = voice + music, to measure the full mix

Run after compose.py:  python3 mixdown.py
"""
import os
import subprocess
import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR = 44100
VO_OFFSET = 0.56          # "Avec n8n" lands on bar 6 (10.0 s)
MUSIC_BASE_DB = -4.0      # music level with no voice over it
DUCK_DB = -9.0           # extra reduction while the voice speaks
ATTACK, RELEASE = 0.08, 0.45

vo_in = os.path.join(ROOT, "assets/audio/voix-off.mp3")
vo_out = os.path.join(ROOT, "assets/audio/voix-off.wav")
subprocess.run([
    "ffmpeg", "-v", "error", "-y", "-i", vo_in, "-ac", "2", "-ar", str(SR),
    "-af", "highpass=f=75,acompressor=threshold=-22dB:ratio=2.2:attack=6:release=90:makeup=1.5,"
           "loudnorm=I=-16:TP=-1.5:LRA=8",
    "-ar", str(SR), vo_out], check=True)

vo, _ = sf.read(vo_out)
vo_mono = vo.mean(axis=1)
music, _ = sf.read(os.path.join(HERE, "music-master.wav"))
n = len(music)

# voice activity envelope on the film's clock
lane = np.zeros(n)
i0 = int(VO_OFFSET * SR)
m = min(len(vo), n - i0)
lane[i0:i0 + m] = vo_mono[:m]
win = int(0.03 * SR)
rms = np.sqrt(np.convolve(lane ** 2, np.ones(win) / win, mode="same"))
active = (20 * np.log10(rms + 1e-9) > -42).astype(float)

# smooth: fast attack, slow release, computed at 1 ms resolution
step = SR // 1000
coarse = active[::step]
g = np.zeros_like(coarse)
a_att = np.exp(-1 / (ATTACK * 1000))
a_rel = np.exp(-1 / (RELEASE * 1000))
s = 0.0
for k, v in enumerate(coarse):
    a = a_att if v > s else a_rel
    s = a * s + (1 - a) * v
    g[k] = s
# look ahead by the attack time so the dip is in place when the first syllable lands
shift = int(ATTACK * 1000)
g = np.concatenate([g[shift:], np.zeros(shift)])
gain_db = MUSIC_BASE_DB + DUCK_DB * np.interp(np.arange(n) / step, np.arange(len(g)), g)
gain = 10 ** (gain_db / 20)
ducked = music * gain[:, None]
sf.write(os.path.join(ROOT, "assets/audio/musique.wav"), ducked.astype(np.float32), SR, subtype="PCM_16")

mix = ducked.copy()
mix[i0:i0 + m] += vo[:m]
sf.write(os.path.join(HERE, "mix-preview.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
print("voice", len(vo) / SR, "s; music", n / SR, "s; peak of preview mix", np.abs(mix).max())
