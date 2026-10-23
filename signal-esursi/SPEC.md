# SPEC v3 — script client, animations « parlantes » (ESURSI · Signalement national)

GOAL:    le spectateur comprend qu'un abus à l'université peut enfin être signalé, simplement et
         sans risque, sur la plateforme officielle du Ministère — et il retient l'adresse.
OUTPUT:  HyperFrames, 1920 × 1080, 30 fps, 70,2 s.
VOICE:   ElevenLabs « Audrey » (McVZB9hVxVSk3Equu8EH), une prise continue (67,55 s) posée à 0,35 s,
         normalisée −16 LUFS. Script du client + « des fonds détournés » (appui demandé) et le nom
         complet du Ministère dans « Voici la plateforme… ».
MUSIC:   piste fournie, 124 BPM, en deux clips de la même piste raccordés sur une mesure (39,26 s) :
         clip 1 dès 47,875 s → la coupure tombe sur « on se tait » (10,23 s), la reprise sur
         « Voici » (14,09 s) ; clip 2 cale la fin naturelle du morceau sur la fin du film (70,2 s).
LOOK:    charte du site : bleu #0057B8, marine #002654, ciel #007FFF, jaune #F7D618, rouge #CE1021,
         brume #F5F9FC ; Source Serif 4 (titres) + Source Sans 3 (texte) ; bande tricolore oblique.
         Illustrations : pictogrammes Streamline Plump (CC BY 4.0) recolorés à la charte, animés
         pièce par pièce ; UI réelle du site (captures iPhone @3×, Mac @2×).
MOTION:  arrivées expo.out 0,4–0,6 s ; caméra power2.inOut ; tampons et pastilles back.out ;
         une idée = une image qui « joue » le mot dit (le tampon tombe sur « faux », le billet
         dévie sur « détournés », la fermeture éclair se ferme sur « on se tait »).

SHOTS (film s ; mot de la voix entre guillemets)
  0,0–2,3    « Un abus dans votre université ? » — bâtiment universitaire illustré, alerte qui
             clignote ; la question s'écrit mot à mot.
  2,3–3,75   « Des points qui se vendent » — relevé de cotes 18/20, étiquette de prix qui tombe.
  3,75–5,2   « des frais illégaux » — un reçu s'imprime, tampon rouge ILLÉGAL.
  5,2–6,55   « des fonds détournés » (appui) — des billets quittent la caisse de l'université et
             sont déviés hors de leur route par une flèche rouge.
  6,55–7,95  « de faux diplômes » — diplôme, tampon FAUX.
  7,95–9,4   « du harcèlement » — des bulles d'alerte se resserrent sur une personne.
  9,4–14,1   « Trop souvent, on se tait. Par peur… ou faute de savoir à qui parler. » — une bulle
             qui « parle » (3 points) ; sur la coupure musicale une fermeture éclair la ferme ;
             elle tremble ; un tracé erre vers des points d'interrogation.
  14,1–22,4  Reprise : la bulle éclate → affiche officielle ; panneau bleu : sceau, ESURSI,
             « Plateforme nationale de signalement », nom complet du Ministère mot à mot.
  22,2–37,4  Téléphone : « Depuis votre téléphone… » → accueil réel, tap « Déposer un signalement »,
             chronomètre (« quelques minutes ») ; « 13 catégories officielles » → les 13 tuiles
             illustrées jaillissent de l'écran, les 4 citées s'allument ; « 8 étapes guidées » →
             parcours illustré en 8 étapes, l'écran réel suit (province, établissement, faits,
             preuves).
  37,4–43,6  « Anonyme ou identifié » → interrupteur illustré ; « aucune donnée personnelle… » →
             nom, e-mail, téléphone, adresse IP se dissolvent avant le bouclier.
  43,5–49,0  « une référence et un code de suivi » → ticket qui s'imprime ; « étape par étape » →
             le circuit officiel (Reçu → … → Clôturé) avance.
  48,9–56,7  « côté ministère… tableau de bord national » → MacBook : le dossier arrive en tête de
             la vraie liste, clic « Tableau de bord » ; « province par province, carte de la RDC »
             → plongée dans la carte reconstruite, remplie province par province.
  56,6–60,1  « Un dossier critique… sous 24 heures » → la vraie ligne Critique de la liste des agents
             (référence floutée) et son échéance SLA, cadran 24 h, délais réels (24 h / 72 h /
             7 j / 15 j).
  60,0–64,6  « Justice. Transparence. Mérite. » → balance, œil, médaille ; « Votre voix compte » →
             porte-voix et ondes.
  64,5–70,2  « Signalez sur signal.minesursi.gouv.cd » → l'adresse se tape ; carte de fin.

BANNED:  fond sombre vide ; glow, particules ; trois cartes en ligne ; titres qui dérivent ; texte
         affiché sans être dit dans le hook ; fausse fonctionnalité ; données personnelles lisibles.
DATA:    chiffres réels (13 catégories, 8 étapes, 26 provinces, délais cibles de la page
         Procédure) ; dossier de démonstration SIG-ESURSI-2026-4F7A2D sur les vrais écrans.
