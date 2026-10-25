# REVIEW — KWIKAMA, « Un dossier, dix-huit institutions »

Film 1920 x 1080, 30 fps, 127 s (3 810 images). Rendu : `renders/kwikama-presentation.mp4`.

## Choix créatifs

- **Un seul dossier traverse le film.** DPJ-2026-014 (Kolwezi, 12,6 M$US de redevances minières non reversées) va du signalement du sonneur d'alerte au Parquet. Chaque étape suit le manuel EFP : vérification §9.3, numéro unique, 23 étapes et réquisitions, traçage des flux, scellés et chaîne de possession, avoirs, assurance qualité en 7 stations, Parquet, journal d'audit.
- **Chaîne d'objets plutôt que des coupes.** Chaque plan finit sur l'objet qui ouvre le suivant : lettre → 18 tuiles → bouclier → Mac → carte « Validée » → numéro → graphe → scellé → montant → rapport → Parquet → logo. Les seules coupes franches sont le flash du bouclier (28,6 s) et le fouet entre les avoirs et l'AQ (98,4 s).
- **Deux mondes.** Une « nuit » marine reprend le vrai fond du site (#031829), avec les arcs or et bleu inspirés des vidéos de référence. Le « papier » est l'UI réelle, filmée dans un MacBook en 3D. L'or est réservé à l'argent, au montant, au bouclier et au bouton final.
- **Les écrans sont les vrais.** Ce sont des captures 2x de kwikama.vercel.app, prises avec les comptes de démo (Coordonnateur, Chef d'équipe, Magistrat, Administrateur). Les cartes « extraites » (rôles, SIG-2026-0163, RQ-2026-0102/0103, PRV-2026-0355, avoirs) sont reconstruites à partir des mêmes données.
- **Voix off.** ElevenLabs, voix `PSVUmed8NvS8aUA3d5oO`, modèle eleven_v4, en 14 phrases. La voix sert d'horloge et l'image est calée au mot près grâce à la transcription Scribe.
- **Musique composée pour le film** (`tools/music/compose.py`).
  - Elle part d'un drone et d'une horloge pendant le problème, puis tient une respiration quasi silencieuse après le tampon « Classé sans suite ».
  - Elle s'ouvre en ré majeur sur le bouclier, avec un groove à 100 BPM pendant le parcours, un sommet sur le flux d'argent (76,6 s) et une résolution sur le logo (115,0 s).
  - Les 84 effets sonores ont tous une cause à l'écran.

## Pistes non construites (voir STORYLINES.md)

- **B — « Suivre l'argent »** : le résultat d'abord. On montre les 12,6 M$ en traits d'or jusqu'à l'immeuble de Lubumbashi, puis on remonte comment KWIKAMA a rendu ce trajet visible.
- **C — « La procédure, en typographie »** : les 23 étapes du manuel en typographie cinétique géante, coupées sur le temps, avec des éclats d'écrans réels.

## Ce qui a été mesuré, regardé, ou pas vérifié

- **Mesuré**
  - `hyperframes check` : 0 erreur (lint, runtime, layout, motion, contraste).
  - Mix de référence : −16,2 LUFS intégré, crête vraie −1,6 dBTP.
  - Voix à −19 LUFS en mono, avec un ducking de la musique de 11 dB.
  - Durée et pistes audio du MP4 contrôlées avec ffprobe et `hyperframes audio`.
- **Regardé** : planches de revue (17 temps forts, 8 raccords à ±0,2 s, version « téléphone ») et instantanés ciblés après chaque correction.
- **Jamais écouté** : la musique, le mix et la synchronisation des effets ont été mesurés et calés sur des timecodes, mais **personne ne les a entendus**. À écouter en priorité :
  - la respiration de 26,5 à 28,6 s ;
  - le sommet de 76,6 s ;
  - l'équilibre voix et musique entre 110 et 113 s.
- Les liens Pinterest étaient bloqués par le réseau du conteneur. L'inspiration vient des trois MP4 de référence fournis.

## Plan le plus faible

- **Acte 5 (67,8–80,6 s), le monde du graphe.** La plongée dans l'écran « Enquête financière » fonctionne, mais le graphe reconstruit reste plat. Les montants et l'alerte arrivent vite, et l'alerte quitte l'écran 0,2 s avant son seuil de lecture.
- Avec plus de temps, j'aurais :
  - tenu l'alerte 1 s de plus, quitte à raccourcir le compteur « 5 / 6 transactions » ;
  - ajouté une vraie profondeur aux nœuds (taille et flou selon la distance) ;
  - fait voyager les montants le long des arêtes au lieu de les poser.
- **Le « Hébergement souverain » (≈ 109–111 s)** est aussi un peu court. C'est la voix qui porte l'information.

## Avertissements conservés volontairement

- `composition_file_too_large` (act1) : l'acte 1 est un seul mouvement continu de 28,6 s (carte → lettre → montant → silos → tampon). Le découper casserait la chaîne d'objets. Le source lisible est dans `src/acts/act1.html`.
- `text_below_floor` : il porte sur les libellés fins dans l'UI réelle et sur les cartes (statuts, dates, mentions). Le film est livré en desktop, pas pour un téléphone. Les informations clés sont toujours à 28 px ou plus, ou agrandies par un punch caméra.
- `line_unread` : il s'agit surtout des rouleaux de chiffres J+12 → J+90 (illisibles volontairement, c'est le temps qui passe) et de sous-titres de cartes que la voix prononce en même temps. Le pied de page final a été allongé pour tenir plus de 5,5 s.
