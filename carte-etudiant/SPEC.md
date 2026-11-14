# SPEC — « Ta carte, ton avenir » (TikTok)

GOAL:    l'étudiant finit la vidéo en se disant « mon université doit y être, je vais le réclamer » et retient carte.minesursi.gouv.cd
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps
TIME:    37.5 s x 30 = 1125 frames. Horloge = voix off (ElevenLabs, voix PSVUmed8NvS8aUA3d5oO, prise 1, 35.4 s). Pas de musique (aucune source disponible).
LOOK:    affiche officielle du Ministère animée. Fond #F4F7FB à plat ; aplats de marque #0B2C5A (marine), #FCD116 (jaune), #D21034 (rouge), bleu ciel #2F86E0.
         Encre #0B2C5A. Accent jaune : un mot par plan (surligneur derrière le mot, comme « FIERS » sur l'affiche).
         Titres Montserrat 900, 120–260 px, tracking -2 %. Texte Open Sans 600–700. Sous-titres Montserrat 800 64 px, boîte marine, mot clé jaune.
         Matière : la vraie carte (recto/verso de l'affiche) en HTML, ombre 0 30px 60px rgba(11,44,90,.28) ; liseré tricolore bleu/jaune/rouge.
OBJECTS: carte nationale recto (bandeau bleu, sceau RDC, photo, « Statut : valide », liseré tricolore) et verso (QR réel vers carte.minesursi.gouv.cd) ;
         dossier de fin de cycle (feuille A4, cases à cocher) ; cartes papier artisanales (carton beige, écriture manuscrite, tampon flou) ;
         téléphone (cadre marine, écran « Vérification ») ; base nationale (cylindre de base de données) ; recherche d'établissements.
MOTION:  arrivée expo.out / power4.out 0.5–0.8 s ; caméra power2.inOut ; sortie power3.in, 40–50 % plus courte ; ressort back.out(1.6) sur les badges seulement.
         Mots : flou 8px→0 en 0.15 s, décalage 0.07 s. Rien ne bouge pendant qu'on le lit.
SHOTS:   S1 0–7.55 dossier de fin de cycle, 3 coches, la 4e « Preuve d'identité étudiante » vire au rouge, poussée caméra, « ? » géant. → whip vertical
         S2 7.55–9.62 cartes papier hétéroclites tombent, tampon NON VÉRIFIABLE sur « suffit plus ». → balayage tricolore
         S3 9.3–13.25 fond marine, la carte pivote de la tranche à face, titre CARTE NATIONALE DE L'ÉTUDIANT, sceau du Ministère. → continuité
         S4 13.25–18.95 la carte se retourne, poussée sur le QR, lignes vers BASE NATIONALE, téléphone scanne, « Carte valide ». → l'écran devient le monde
         S5 18.9–23.35 une carte → 26 cartes portant les 26 provinces, compteur 26, « LA NORME » surlignée. → coupe sèche + glitch
         S6 23.35–27.5 recherche d'établissements : « Ton université — NON INSCRITE », carte vide en pointillés « AUCUNE CARTE ». → aplat jaune
         S7 27.5–32.85 BOUGE ! / PARLE À ton délégué, ton secrétariat / RÉCLAME TA CARTE MAINTENANT ! → iris blanc
         S8 32.85–37.5 en-tête Ministère, carte, URL tapée lettre à lettre, bandeau « Réclame ta carte auprès de ton établissement ! »
BANNED:  fond noir/vide, glow, néon, particules, dégradés violets, cartes en verre, tout centré qui flotte, tout en fondu-montée,
         titres qui dérivent après atterrissage, logo dans un coin, boucles de respiration.
QA:      0 (accroche lisible), 4.5 (ligne rouge), 6.8 (?), 8.9 (tampon), 10.8 (carte), 14.4 (QR), 18.2 (valide), 21.4 (26), 22.9 (norme), 26.6 (aucune carte), 28.0, 32.2, 36.5
