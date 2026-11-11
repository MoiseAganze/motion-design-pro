# SPEC — KWIKAMA v2, « Le dossier en cinq écrans »

- **GOAL :** un ministre comprend en 2 min 32 que KWIKAMA filtre la légalité, protège la preuve, croise les dossiers, mesure la coopération et ramène l'argent au Trésor. Il voit les cinq vrais écrans dans l'ordre de la note de démonstration, plus un changement de rôle de 15 s qui prouve le cloisonnement.
- **OUTPUT :** HyperFrames, 1920 x 1080, 30 fps, 152 s = 4 560 images, MP4 H.264 + AAC.
- **TIME :**
  - La voix off est l'horloge : 17 phrases, placées par `tools/vo/cut_vo.py`.
  - Les mots repères sont lus dans `assets/audio/vo/words_film.json` ; chaque animation clé tombe sur son mot à ±0,1 s.

## LOOK

- **Nuit :** fond du site #031829, arcs or et bleu en lente rotation, constellation à 16 %.
- **Papier :** l'UI réelle (#FBF9F5), capturée en 2x dans un MacBook.
- **Accent or #D8A828,** réservé à :
  - les numéros de chapitre ;
  - les surlignages d'UI (cadre 3 px, halo 24 px) ;
  - l'argent ;
  - le bouclier.
- **Statuts de l'app :** vert #1E6B4F (validé, scellé intact, répondue), rouge #9B2C24 (bloqué, en retard), ambre #8A6512 (clarification).
- **Typographie :**
  - Fraunces 600 pour les numéros (200 px) et les titres (64–72 px) ;
  - Inter 500/600 pour les libellés (24–34 px) ;
  - mot-symbole KWIKAMA en Fraunces 700, interlettrage +14 %.

## GRAMMAIRE (identique pour les cinq chapitres)

1. **Carte de chapitre :**
   - le Mac recule à droite (`CHP` : x +300, y +20, échelle 0,66, rotationY −12°, rotationX 6°) ;
   - à gauche, le numéro or 01–05, l'écran n/5, le titre et une ligne-message ;
   - le curseur clique le module dans la barre latérale ;
   - durée 2,6–3,0 s, puis la caméra replonge dans l'écran (power2.inOut 1,0 s).
2. **Dans l'écran :**
   - la caméra cadre l'élément dit par la voix ;
   - un cadre or le désigne au mot près ;
   - le défilement se fait par composite (barre latérale et en-tête fixes, contenu qui défile), comme dans le navigateur.
3. **Illustration :**
   - quand l'idée dépasse l'écran (verrou de légalité, chaîne de garde, deux dossiers sur la carte, météo, trois périmètres, trajectoire des biens), le Mac s'efface à droite ou en bas ;
   - l'illustration réutilise les composants de l'app : cartes blanches, puces de statut, hexagone des six institutions.
4. **Changement de rôle :**
   - le curseur clique « Changer de rôle », la page « Choisir un poste de travail » apparaît, le curseur clique le poste ;
   - une étiquette personne (nom, poste, niveau d'habilitation) monte en bas à gauche.

## MOUVEMENT

| Élément | Réglage |
|---|---|
| Entrées | expo.out 0,6–0,8 s |
| Caméra | power2.inOut 0,9–1,2 s |
| Sorties | power3.in, 40–50 % de l'entrée |
| Clic | curseur à 0,8 puis 1, et anneau or de 0 à 46 px en 0,4 s |
| Mots | flou 10 → 0 px, décalage de 0,07 s |
| Comptes | odomètre 1,3–1,5 s power3.out |
| Boucles | aucune boucle d'ambiance ; tout est fonction du temps |

## SON

- **Musique composée pour le film :**
  - drone et horloge pendant l'accroche ;
  - ouverture en majeur sur « KWIKAMA » (14,36 s), puis pulsation 100 BPM pendant les cinq écrans ;
  - accent à chaque carte de chapitre et montée à partir de 131 s ;
  - accord final sur le logo (144,46 s).
- **Effets :** un clic par clic de souris, un souffle par grand mouvement de caméra, un « pop » par surlignage. Rien sans cause à l'écran.
