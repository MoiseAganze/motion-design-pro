# REVIEW — MINESURSI, pub TikTok

## Version 4 (nom officiel + format YouTube)
- Libellé du Ministère aligné sur l'en-tête de l'app : « Ministère de l'Enseignement Supérieur, Universitaire, Recherche Scientifique et Innovations ».
- Ouverture et fin régénérées (même voix ElevenLabs, eleven_v4) : voiceover-open.mp3 et voiceover-end.mp3 ; le milieu de la voix est inchangé. « Minesursi » toujours posé sur le drop (26,129 s).
- Deux livrables : minesursi-promo (TikTok 1080x1920) et minesursi-youtube (16:9 1920x1080 : titres dans un panneau marine à gauche fermé par la bande tricolore verticale, téléphone à droite, carte finale logo à gauche / téléphone à droite).
- Son des deux MP4 normalisé après rendu : -16 LUFS, crête vraie -1,5 dBTP, sans écrêtage (mesuré, pas écouté).


## Version 3 (nouvelle phrase d'ouverture)
- Ouverture régénérée seule (même voix, eleven_v4) : « Le Ministère de l'Enseignement Supérieur et Universitaire, de la Recherche Scientifique et de l'Innovation vous présente sa toute nouvelle application mobile. » (« sa toute nouvelle » : accord féminin d'« application »). Fichier assets/audio/voiceover-open.mp3, le reste de la voix v2 est conservé.
- Accroche : « Le Ministère de… » ; titre du bandeau à l'apparition du téléphone : « Sa toute nouvelle / application mobile ».
- Son du MP4 livré normalisé après rendu (ffmpeg loudnorm, image copiée sans réencodage) : -16,2 LUFS, crête vraie -1,6 dBTP.

## Version 2 (demande : nom complet du Ministère au début et à la fin)
- Nouvelle voix ElevenLabs (même voix, eleven_v4, prise 1 sur 2, 33 s) : ouverture « Ministère de l'Enseignement Supérieur et Universitaire, de la Recherche Scientifique et de l'Innovation… tout le Ministère, désormais dans votre poche », fin « Minesursi. La plateforme du Ministère de l'Enseignement Supérieur et Universitaire, de la Recherche Scientifique et de l'Innovation, à portée de main ».
- Minutage mot à mot : alignement ElevenLabs (il reprend le texte envoyé, ce n'est pas une vérification indépendante de la prononciation).
- Accroche : le nom complet sur 7 lignes qui s'allument au fil de la voix. Tout le parcours est décalé de 6 temps (2,903 s) ; musique lue à partir de 4,839 s pour que le drop tombe toujours sur « Minesursi » (26,129 s). Une phrase de voix par clip, posée sur son plan.
- Carte finale : slogan complet ligne par ligne, téléphone réduit (×0,5).
- Durée : 35,8 s (le nom complet prononcé deux fois ajoute ~6 s). Son : -17 LUFS, crête vraie -1,6 dBTP, sans écrêtage (mesuré, pas écouté).

## Version 1

## Choix créatifs
- Piste A « Le Ministère dans la poche » (voir STORYLINES.md). Pistes B (veille d'inscription) et C (mur d'écrans) écartées : B exigerait un écran de résultat de vérification absent des captures.
- 1080 x 1920, 30 fps, 29,03 s (fin sur une barre de mesure de la musique).
- Les cinq captures sont utilisées telles quelles. Seules retouches : la barre d'état système (icônes Snapchat, ChatGPT, LinkedIn, batterie 18 %) remplacée par une barre d'état neutre « 08:30 », et la barre de navigation système Android retirée. Aucun contenu de l'app n'est modifié ni inventé.
- Seuls des gestes réels sont montrés : toucher le raccourci « Communiqués » ouvre la capture Communiqués, les onglets Actualités / Accueil / Plus ouvrent leurs captures. Les lignes « Offres & bourses », « Centres de recherche », « Vérifier un établissement », « Mes documents » sont mises en avant par la caméra, jamais ouvertes (leurs écrans ne sont pas fournis).
- Fil conducteur : la bande tricolore de l'en-tête de l'app.
- Voix : ElevenLabs, voix McVZB9hVxVSk3Equu8EH (« Audrey – Energetic Commercial »), modèle eleven_v4, prise 1 sur 2. Coupée en deux au silence avant « Minesursi » pour que le nom tombe sur l'entrée de la section pleine de la musique (23,226 s).
- Musique : piste fournie, lue à partir de 7,742 s (mesure 4) ; fondu de sortie 1,6 s.
- Logo : le sceau tel qu'il apparaît dans l'en-tête de l'app (pas de fichier source disponible, le réseau du conteneur bloque le site du ministère) ; il est un peu doux à 148 px.

## Ce qui a été mesuré / regardé
- `hyperframes check` : 0 erreur (un avertissement de taille de fichier sur stage.html, gardé : le plan-séquence du téléphone est une seule scène).
- Planches `snapshot --review`, plages autour de chaque toucher, du whip, du défilement et du drop : relues.
- Son du MP4 final (mesuré avec `hyperframes audio` et ffmpeg, pas écouté) : -15,8 LUFS intégrés, crête vraie -1,5 dBTP, aucun écrêtage ; voix environ 10 dB au-dessus de la musique ; clics présents sur les touchers (6,02 / 8,01 / 12,44 / 22,31 s) ; l'impact culmine sur le drop (max court terme -12 LUFS).
- Rendu : renders/minesursi-pub-tiktok.mp4, H.264 1080 x 1920, 30 fps, AAC 48 kHz, 29,03 s, 12,7 Mo.

## Corrigé pendant la revue
- t=3,6 s · les mots de l'accroche passaient sur le téléphone → sortie avancée à 3,29 s.
- t=8,2 s · l'Accueil réapparaissait en transparence pendant le fade-through Communiqués → Article → écran masqué après la poussée.
- t=6,1 s · la poussée démarrait avant le relâchement du doigt → départ au relâchement (6,12 s).

## Plan le plus faible
- 22,5–23,2 s : le recul du téléphone avant le drop est calme (voulu, respiration avant le nom) ; avec plus de temps, un effet de montée plus long ou un petit mouvement de la bande.
- Les floods jaune/rouge sont en partie cachés par le téléphone en gros plan ; ils se lisent surtout pendant les mouvements.
