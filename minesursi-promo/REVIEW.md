# REVIEW — MINESURSI, pub TikTok

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
