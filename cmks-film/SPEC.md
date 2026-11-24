# SPEC — « Une demande, un parcours »

GOAL:    La Direction du CMKS finit le film fière de sa plateforme et décidée à l'adopter : « un centre moderne, des patients mieux accueillis, une Direction qui garde la main ».
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps.
TIME:    ~81 s x 30 = ~2430 frames. Musique 120 BPM = 15 images par temps, 60 par mesure. La voix est l'horloge.

LOOK:    Deux sols qui alternent : blanc #FFFFFF (le site public) et bleu canard #07293A → #0B6B91 (les coulisses, la nuit).
         Encre : #113F55 sur blanc, blanc sur bleu. Accent : orange #E99841 / #D4761B, réservé aux bandes, aux anneaux et à un mot par plan.
         Titres : Bricolage Grotesque 800 en capitales, 120 à 200 px, approche -2 %. Texte courant : Plus Jakarta Sans 600, 34 à 44 px.
         Matières : les vraies captures (2880 x 1800, capturées en 2x), les photos rondes cerclées (anneau de 12 px orange ou #15A8D6, liseré blanc de 8 px, ombre 0 18px 40px rgba(7,41,58,.25)),
         les bandes obliques à 45° (une bleue de 90 px, une orange de 34 px, en parallèle, comme sur l'affiche).
         Pas de grain, pas de vignettage, pas de lueur.
OBJECTS: la bande oblique (le fil conducteur), la photo ronde (les pôles, les avatars), le curseur (flèche blanche bordée de #07293A, 56 px), la pastille de statut (vert #10B981 / orange #F59E0B / gris #94A3B8).
MOTION:  entrées expo.out 0,7 à 0,9 s ; caméra sur les captures power2.inOut 0,9 à 1,4 s ; sorties power3.in 0,35 s ;
         les bandes balaient en 0,6 s power3.inOut ; anneaux : stroke dessiné 0,6 s ; pops back.out(1.6) 0,4 s ; décalage des mots 0,08 s.
SHOTS:   A 0–9 nuit : « 21:00 », « KINSHASA », la question, puis un iris rond s'ouvre sur l'affiche.
         B 9–20,6 affiche → 8 photos rondes, pôles numérotés → barres de statut par pôle (données réelles).
         C 20,6–25,8 page du service Kinésithérapie, plongée sur le prix et les 4 étapes.
         D 25,8–33,2 formulaire rempli, clic « Envoyer » → « Demande envoyée » → le bouton WhatsApp.
         E 33,2–37,6 bascule : une bande bleue envahit l'écran, « L'ENVERS DU DÉCOR ».
         F 37,6–42,4 connexion → « Essayer avec un compte de démonstration » → 15 profils.
         G 42,4–50,6 accueil (Nadine) : DR-0002 « Nouvelle » → planifier avec Josué Kalala → « Planifiée ».
         H 50,6–59,4 montage de 4 modules (kiné, médecin, coach, caisse), une coupe sur chaque phrase.
         I 59,4–68,2 Direction : tableau de bord, puis Partenaires, clic « Ne plus mettre en avant ».
         J 68,2–73,6 les trois phrases de la promesse, une par une, sur la bande.
         K 73,6–81 logo porté par la bande, CMKS, la devise, l'adresse du site.
BANNED:  sol sombre vide avec de petits éléments au centre ; lueurs, particules ; dégradés violets ; trois cartes alignées ;
         tout qui fond-et-monte ; titres qui dérivent après leur arrivée ; logo calé dans un coin ; une interface inventée
         (tout écran du produit est une vraie capture ; les seules reconstructions sont des données réelles redessinées : barres de statut, pastilles).
QA:      t=1 (premier visuel, jamais noir), 10, 16, 23, 30, 35, 40, 46, 49, 55, 63, 66, 71, 78.
