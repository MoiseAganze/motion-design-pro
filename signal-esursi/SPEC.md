# SPEC — « Le voyage d'un dossier » (ESURSI · Signalement national)

GOAL:    à la fin, le spectateur sait qu'il existe une application officielle du Ministère ESURSI
         pour signaler un abus depuis son téléphone, que le Ministère le voit sur une carte
         nationale et le traite selon un circuit tracé — et il a l'adresse pour le faire.
OUTPUT:  HyperFrames, 1920 × 1080, 30 fps.
TIME:    61,94 s × 30 ≈ 1858 frames (rév. 2 : tout ce qui suit le hook décalé d'une mesure). Musique 124 BPM → 1 temps = 0,4839 s (14,52 f), 1 mesure =
         1,9355 s. La piste démarre à 48,425 s (un temps fort) : coupure de 2 mesures à 9,68 s,
         reprise (drop) à 13,54 s, fin naturelle 58–60 s.

LOOK:    la charte du site, rien d'autre.
         - Fonds : brume #F5F9FC, ciel doux #E8F4FF, blanc ; aplats drapeau pour le hook.
         - Encre #0F2744 ; bleu ESURSI #0057B8 ; marine #002654 ; ciel #007FFF ;
           jaune #F7D618 / or #E6B800 ; rouge #CE1021.
         - Accent = la bande tricolore oblique du site (115°, ciel 0–38 %, jaune 38–41 %, rouge
           41–59 %, jaune 59–62 %, ciel 62–100 %) : haut des cartes, balayages de transition.
         - Titres : Source Serif 4, 700, 150–170 px (hook), 64–96 px (titres), tracking −1 %.
           Texte : Source Sans 3, 400/600/700, ≥ 28 px pour ce qui doit se lire.
         - Matière : l'UI réelle capturée (téléphone @3×, Mac @2×), dans un iPhone titane
           #1C2430 et un MacBook gris sidéral #2B2F36 dessinés en CSS. Ombre portée appareils :
           0 40px 80px rgba(0,38,84,.22). Pas de grain, pas de vignette.
OBJECTS: iPhone (îlot dynamique, barre d'état 9:41) ; MacBook (encoche, charnière, base) ;
         la référence SIG-ESURSI-2026-4F7A2D en pastille (le porteur du récit) ; la carte de la
         RDC (26 provinces, GeoJSON réel de l'application) avec pays voisins en gris bleuté.
MOTION:  arrivées expo.out / power4.out (0,5–0,7 s) ; caméra power2.inOut (0,6–0,9 s) ;
         sorties et zooms-à-travers power3.in (0,3–0,4 s) ; pastilles/compteurs back.out(1.4).
         Flou de mouvement 8–16 px au pic des déplacements rapides. Titres posés = immobiles.
SHOTS:   (s)
  0,00–9,69   HOOK — aplats drapeau coupés au temps : « Vente de points », « Faux diplômes »,
              « Harcèlement »… puis le mur des 13 catégories officielles, qui se tait (gris).
  9,69–13,54  SILENCE — affiche officielle, portrait de l'étudiante ; « Votre voix compte ».
  13,54–19,7  RÉVÉLATION — l'affiche s'ouvre plein cadre sur le drop ; panneau bleu en
              diagonale : sceau + ESURSI + nom complet du Ministère, mot à mot avec la voix.
  19,2–30,0   TÉLÉPHONE — l'accueil mobile ; « Déposer un signalement » ; 8 étapes réelles
              (catégorie, province, établissement, personne, description, preuves, mode,
              prévisualisation) avec la colonne d'étapes lisible à droite ; envoi ; référence
              + code de suivi. La pastille référence s'envole.
  29,2–39,0   CARTE — MacBook, tableau de bord national ; la pastille tombe sur la carte ;
              plongée dans la carte reconstruite (26 provinces nommées, intensité réelle) ;
              clic sur Kinshasa → panneau des établissements (noms floutés).
  38,6–47,6   TRAITEMENT — liste des dossiers (nouveau dossier en tête) → fiche → « Faire
              évoluer le dossier » : En vérification → Valider ; messagerie chiffrée ;
              historique tracé.
  47,2–56,3   VALEUR — téléphone + Mac ensemble ; 3 preuves : Anonyme ou identifié /
              circuit officiel tracé / 26 provinces · 1 618 établissements.
  56,0–60,0   FIN — sceau, ESURSI · Signalement national, nom du Ministère, « Justice ·
              Transparence · Mérite », bouton « Déposer un signalement », signal.minesursi.gouv.cd.
SOUND:   voix ElevenLabs « Audrey » (McVZB9hVxVSk3Equu8EH) découpée en 11 phrases calées sur
         l'image ; musique fournie ≈ 0,22 sous la voix ; clics/whooshes Pixabay rares.
BANNED:  fond sombre vide avec petits éléments flottants ; glow, particules, néons ; dégradés
         violets ; cartes de verre ; trois cartes en ligne ; logo docké en coin ; titres qui
         dérivent après s'être posés ; UI inclinée en 3D ; fausse fonctionnalité ; données
         personnelles lisibles (noms d'établissements et de personnes floutés).
QA:      0,0 (vignette non vide) · 2,6 · 7,9 · 11,0 · 13,6 · 16,5 · 21,6 · 23,3 · 25,2 · 27,4 ·
         31,0 · 34,6 · 37,0 · 40,4 · 42,4 · 44,4 · 46,1 · 49,5 · 51,9 · 53,4 · 55,2 · 58,5.

DONNÉES: chiffres réels (accueil public et tableau de bord, 22/10/2026) : 26 signalements,
         26 provinces, 1 618 établissements, Kinshasa 13 ; effectifs < 5 affichés « < 5 »
         comme le fait la plateforme. Le dossier SIG-ESURSI-2026-4F7A2D est un dossier de
         démonstration posé sur les vrais écrans (aucun envoi réel n'a été fait).
