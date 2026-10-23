# SPEC — MINESURSI, pub TikTok 29 s

GOAL:    le spectateur retient que tout le Ministère (communiqués, actualités, vidéos, offres, vérification d'établissements, documents) tient dans une seule app officielle, et reconnaît le nom MINESURSI.
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps
TIME:    29.03 s x 30 = 871 frames. Musique 124 BPM : 1 temps = 0.48387 s = 14.52 frames, 1 mesure = 1.935 s.
         Musique lue à partir de 7.742 s (mesure 4) : charleston à 7.74 s vidéo, section pleine (drop) à 23.226 s vidéo = temps 48.
         Voix : partie A (0 → 22.05 s du fichier) posée à 0.30 s ; partie B (22.05 s → fin) posée à 23.032 s pour que « Minesursi » tombe sur le drop.

LOOK:    sol de base marine #0B2B5E (barre d'app MINESURSI), bandeau-titre marine 0–454 px fermé par la bande tricolore de l'app
         (bleu #007DFE 46 %, jaune #F5D522 7.6 %, rouge #C8131F 46 %, 16 px).
         Sols de scène pleins, changés par « colour flood » : blanc froid #EAF0F8, jaune #F5D522, bleu #0A6CDC, rouge #C8131F ; lumière radiale +8 % au centre.
         Titres : Montserrat 800, 84 px, interlignage 1.0, blanc, barre rouge #CE0F1E 12 px à gauche (langage des en-têtes de section de l'app).
         Hook : Montserrat 800 116 px, mots éteints #2E4D86 puis allumés #FFFFFF.
         Fin : « MINESURSI » Montserrat 900, sceau de l'app (recadré de la capture), slogan Montserrat 700 56 px + « à portée de main » jaune 76 px.
         Matière : captures réelles 1152 px (barre d'état système masquée, barre de navigation système retirée), téléphone graphite #1b1d22→#343740, bord 15 px, rayon 70 px,
         ombre 0 40px 90px rgba(0,0,0,.35) + 0 12px 28px rgba(0,0,0,.25).
OBJECTS: le téléphone (graphite, bouton latéral, poinçon caméra, barre d'état propre 08:30) ; les cinq écrans réels ; l'indicateur de toucher Android (disque blanc 38 %, bord 70 %) et l'ondulation Material sur la cible.
MOTION:  arrivée expo.out / power4.out ; caméra power2.inOut 0.45–0.6 s ; sortie/zoom-through power3.in ; titres mot à mot flou 6 px → 0 en 0.13 s, 0.067 s d'écart ;
         poussée d'écran Android 0.42 s expo.out ; fade-through de la barre de navigation 0.09 s sortie + 0.21 s entrée (échelle 0.94 → 1).
SHOTS:   0.00–3.39  Hook : trois mots s'allument (0.0 / 1.50 / 2.42), la bande se dessine segment par segment.
         3.39–6.29  La bande monte à 454 px, le sol blanc la suit, le téléphone monte (Accueil). Titre « Le Ministère / dans votre poche ». Caméra sur le raccourci Communiqués, toucher à 6.02.
         6.29–8.23  Poussée vers Communiqués, flood jaune, cadrage ×1.75 sur les cartes. Titre « Communiqués / officiels ». Caméra vers la barre de nav, toucher Actualités 8.05.
         8.23–10.65 Fade-through vers l'Article, flood bleu, photo puis titre de l'article. Titre « Toute / l'actualité ». Recul, toucher Accueil 10.42.
         10.65–12.58 Accueil, flood rouge, plongée ×1.9 sur la carte vidéo ESURSI TV. Titre « Vidéos / ESURSI TV ». Whip vers la nav, toucher Plus 12.43.
         12.58–16.45 Plus, flood blanc, ligne « Offres & bourses » puis « Centres de recherche », recul « tout est là ».
         16.45–19.35 Défilement vers le haut (whip vertical), flood bleu, « Vérifier un établissement » ×1.85.
         19.35–22.20 Panoramique vers « Mes documents », flood jaune, recul sur tout « Mon espace / Le Ministère ».
         22.20–29.03 Toucher Accueil 22.30, sol marine, le téléphone recule en bas, la bande file sous « MINESURSI » au drop (23.226), slogan 24.3 / 25.85, tenue.
BANNED:  vide sombre avec petits éléments flottants ; lueurs, particules ; dégradés violets ; papier crème + serif ; tout centré qui glisse vers le haut ;
         texte qui bouge pendant la lecture ; logo dans un coin ; trois cartes en ligne ; UI inclinée en 3D ; toute fonctionnalité absente des captures ;
         modification du contenu des captures.
QA:      0.0 (vignette : trois mots lisibles), 2.6 (bande complète), 4.6 (téléphone + titre), 6.4 (Communiqués), 9.4 (article), 11.4 (carte vidéo),
         13.4 (Offres & bourses), 17.4 (Vérifier un établissement), 20.2 (Mes documents), 23.5 (drop / logo), 27.5 (carte finale).
