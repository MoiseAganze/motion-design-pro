# KWIKAMA — film de démonstration (v2)

Projet [HyperFrames](https://hyperframes.heygen.com) (HTML → vidéo) : 1920 x 1080, 30 fps, 153 s.

Il filme https://kwikamademo.vercel.app/ en suivant la note de démonstration : cinq écrans, un seul dossier, un changement de rôle.

| Document | Contenu |
|---|---|
| `SPEC.md` | Direction artistique |
| `SCRIPT.md` | Voix off et sources |
| `STORYLINES.md` | Pistes narratives |
| `REVIEW.md` | Bilan, points à écouter, avertissements |

## Structure

- **`index.html`** — composition racine : le fond, 7 scènes, la voix (17 clips), la musique et 122 bruitages. Les deux derniers sont écrits entre `<!-- @AUDIO:BEGIN -->` et `<!-- @AUDIO:END -->`.

  | Scène | Contenu | Début |
  |---|---|---|
  | `s0` | ouverture | 0 s |
  | `s1` | contrôle de légalité | 21,6 s |
  | `s2` | chaîne de garde | 49,0 s |
  | `s3` | croisement des dossiers | 68,2 s |
  | `s4` | coordination et vue CENAREF | 94,6 s |
  | `s5` | avoirs et RI 8 | 121,8 s |
  | `s6` | signature | 143,8 s |

- **`src/acts/*.html`** — **les sources à éditer.**
  - `src/base.css` : MacBook, composite de défilement `.pg`, surlignage `.hl`, carte de chapitre `.chap`.
  - `src/helpers.js` : caméra `camAt`, `clickAt`, `over`, `chapter`, odomètres. Il contient aussi `BOX`, les positions mesurées des éléments d'UI, injectées depuis `assets/ui/boxes.json`.
  - `src/mac.html`.
- **`compositions/*.html`** — fichiers **générés**, à ne pas éditer à la main.
  ```bash
  node tools/build.mjs            # tout régénérer
  node tools/build.mjs s3 s4      # seulement ces scènes
  ```
- **`assets/ui/`** — captures 2x de kwikamademo.vercel.app, message « À dire » masqué. Pour les refaire : `node tools/capture/capture.js <dossier>/`, puis `python tools/capture/drawers.py <dossier> .` ; convertir les PNG en WebP dans `assets/ui/` et copier `boxes.json`.
  - `drawer_0163/0186.webp` : tiroirs reconstitués pour le défilement.
  - `boxes.json` : positions des éléments en px de page.

## Commandes

```bash
npx hyperframes preview --background   # Studio
npm run check
npx hyperframes render --quality delivery --output renders/kwikama-demonstration.mp4
```

## Son (`tools/`)

1. **`vo/cut_vo.py <prise.wav> <words.json> .`** découpe la prise ElevenLabs en 17 phrases et les place sur l'horloge du film. Il écrit `assets/audio/vo/segments.json` et `words_film.json`, qui donnent l'heure de chaque mot dans le film.
2. **`music/compose.py <work> x`** produit la partition : une phrase par chapitre, la grille de mesures repart sur chaque carte de chapitre. Rendu FluidSynth (FluidR3_GM) plus synthèse numpy, vers `<work>/music_free.wav`.
3. **`music/mixdown.py . <work>/music_free.wav <work>`** traite la voix, atténue la musique sous la voix, prépare les bruitages et écrit `cues.json`. Il mesure aussi le mix de référence.
4. **`music/write_audio_tags.py .`** réécrit le bloc audio de `index.html`.

Dépendances Python : numpy, scipy, pedalboard, pretty_midi, soundfile, pyloudnorm, plus fluidsynth et FluidR3_GM.
