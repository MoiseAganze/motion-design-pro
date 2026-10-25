# KWIKAMA — film de présentation

Projet [HyperFrames](https://hyperframes.heygen.com) (HTML → vidéo). 1920 x 1080, 30 fps, 127 s.

- `SPEC.md` décrit la direction artistique.
- `SCRIPT.md` contient la voix off, avec ses sources dans le manuel EFP.
- `STORYLINES.md` présente les trois pistes narratives.
- `REVIEW.md` fait le bilan.

## Structure

- `index.html` : composition racine. Elle contient 8 actes, la voix off (14 clips), la musique et les effets entre `<!-- @AUDIO:BEGIN -->` et `<!-- @AUDIO:END -->`.
- `src/acts/*.html` : **les sources à éditer**. `src/base.css` regroupe le style commun (MacBook, cartes, puces), `src/helpers.js` les fonctions caméra, curseur et compteurs, et `src/mac.html` le MacBook.
- `compositions/*.html` : fichiers **générés**, à ne pas éditer à la main. Pour les régénérer :
  ```bash
  node tools/build.mjs            # tous les actes
  node tools/build.mjs act4 act8  # seulement ceux-là
  ```
- `assets/ui/` : captures 2x de kwikama.vercel.app. `assets/brand/` : logo vectorisé et tracé de la RDC. `assets/audio/` : voix, musique et effets.

## Commandes

```bash
npx hyperframes preview --background   # Studio dans le navigateur
npm run check                          # lint + runtime + layout + motion + contraste
npx hyperframes render --quality delivery --output renders/kwikama-presentation.mp4
```

## Musique et mix (`tools/music/`)

- `compose.py` écrit la partition (FluidSynth + FluidR3_GM et synthèse numpy) et produit `music_free.wav`.
- `mixdown.py <projet> <music_free.wav> <work>` traite la voix, fait le ducking et pose les 84 effets. Il écrit `assets/audio/music/kwikama-theme.*` et `assets/audio/sfx/cues.json`.
- `write_audio_tags.py` réécrit le bloc audio de `index.html` à partir de `cues.json`.

Dépendances Python : numpy, scipy, pedalboard, pretty_midi, soundfile, pyloudnorm, plus fluidsynth et la soundfont FluidR3_GM.
