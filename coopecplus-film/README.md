# Film de présentation COOPECPLUS

Vidéo motion design (1920 x 1080, 30 fps, 112 s) qui présente COOPECPLUS à travers une journée dans une COOPEC : ouverture de journée, billetage, adhésion d'un membre, dépôt, retrait soumis à double validation, crédit complet, comptabilité automatique, sécurité, clôture et pilotage.

## Contenu

| Fichier | Rôle |
|---|---|
| `SCRIPT.md` | Texte de la voix off (ElevenLabs, voix `PSVUmed8NvS8aUA3d5oO`, modèle eleven_v4) |
| `STORYLINES.md` | Les trois pistes narratives (A retenue) |
| `SPEC.md` | Cahier des charges : couleurs, typographie, mouvements, plans minutés |
| `build.py` | Génère `index.html` et `compositions/*.html` à partir de la liste des plans (temps calés sur la voix) |
| `assets/ui/` | Captures réelles de COOPECPLUS (base de démonstration, 2x) |
| `assets/obj/` | Reçus et contrat découpés depuis les captures |
| `assets/voice/` | Voix off (`voix-off.mp3` = prise retenue) |
| `assets/sfx/` | Effets sonores fournis avec HyperFrames |
| `../captures-tools/` | Scripts Playwright qui ont joué les parcours et pris les captures |

## Refaire le film

```bash
python3 build.py
```

```bash
npx hyperframes@0.9.72 check
```

```bash
npx hyperframes@0.9.72 render --quality high -o renders/coopecplus.mp4
```
