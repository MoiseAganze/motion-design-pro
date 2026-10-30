# Vidéo — Formation Automatisation n8n · CHRONOCONCEPT GROUP

Deux projets HyperFrames (HTML → vidéo), même voix, même musique, même minutage (56 s) :

| Dossier | Format | Pour |
| --- | --- | --- |
| `formation-n8n/` | 1920 × 1080 (16:9) | YouTube |
| `formation-n8n-vertical/` | 1080 × 1920 (9:16), sous-titres incrustés | TikTok, Reels, Shorts |

Les vidéos finales sont dans `renders/` de chaque dossier (non versionnées ; régénérables, voir plus bas).

## Ce qu'il y a dedans
- **Voix off** : ElevenLabs, voix `RBhYSNMNu6b2CGZ9Fn1M` (Felix), modèle eleven_v4 — `assets/audio/voix-off.wav`
  (brut : `voix-off.mp3`). Placée à 0,56 s pour que « Avec n8n » tombe sur le drop de la musique.
- **Musique** : composition originale, 120 BPM (`music/compose.py`, puis `music/mixdown.py` qui traite la voix et
  baisse la musique sous la voix) — `assets/audio/musique.wav`.
- **Scènes** (`compositions/`) : s1 la routine · s2 n8n · s3 workflow « Agent Courriers ESURSI » · s4 workflow
  « MapSante AI » · s5 « C'est VOUS » · s6 titre + logo · s7 Kinshasa / Silikin Village · s8 inscription et contacts ·
  s9 carte de fin.
- **Logo** : vectorisé à partir de votre PNG blanc, découpé en pièces dans `assets/img/logo/`.

## Modifier
- Ouvrir le dossier dans l'application HyperFrames (ou `npx hyperframes preview`) : textes, couleurs et timing se
  modifient dans le Studio. Les couleurs et polices sont des variables (`index.html`).
- Changer la musique : modifier `music/compose.py`, puis `python3 music/compose.py && python3 music/mixdown.py`
  (nécessite `fluidsynth` + la banque de sons `fluid-soundfont-gm`, et `numpy scipy soundfile mido`).
- Les scènes verticales v1–v4, v6, v7, v9 sont dérivées des scènes 16:9 par `tools/make_vertical.py` ; v5, v8 et
  les sous-titres (`tools/build_captions.py`) sont propres au vertical.

## Rendre les vidéos
```bash
cd formation-n8n && npx hyperframes render --quality delivery --output renders/formation-n8n-youtube-16x9.mp4
```
```bash
cd formation-n8n-vertical && npx hyperframes render --quality delivery --output renders/formation-n8n-tiktok-9x16.mp4
```

Notes de relecture, brief et storylines (communs aux deux formats) : `../formation-n8n/REVIEW.md`, `../formation-n8n/SPEC.md`, `../formation-n8n/STORYLINES.md`.
