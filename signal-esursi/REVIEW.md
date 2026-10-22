# REVIEW — ESURSI · Signalement national (60 s, 1920×1080, 30 fps)

## Ce qui a été construit

Storyline A « Le voyage d'un dossier » (voir `STORYLINES.md`) : un seul dossier traverse le film,
du téléphone de l'étudiant jusqu'au Mac de l'agent du Ministère. Non construites : B « Une voix
dans l'amphi » (plan unique dans la main de l'étudiante) et C « Le pays s'allume » (vol au-dessus
de la carte).

| Temps | Scène | Contenu réel montré |
| --- | --- | --- |
| 0–9,7 s | Hook | Abus tirés des 13 catégories officielles du site, puis le mur des 13 catégories « noirci » (sous silence) |
| 9,7–19,7 s | Révélation | Affiche officielle « Signalez les abus » ; sceau ; nom complet du Ministère, mot à mot avec la voix |
| 19,2–30 s | Téléphone | Accueil mobile réel + les 8 étapes réelles du formulaire (captures iPhone @3×), référence + code de suivi |
| 29–39 s | Carte | Tableau de bord national réel → carte reconstruite depuis le GeoJSON de l'application (26 provinces) → clic Kinshasa → panneau des établissements |
| 38,6–47,6 s | Mac | Gestion des dossiers → fiche → « Faire évoluer le dossier » (En vérification → Valider) → messagerie chiffrée → historique |
| 47,2–56,3 s | Valeur | Téléphone (« Suivre un signalement ») + Mac reliés ; Anonyme ou identifié ; circuit officiel ; 26 provinces · 1 618 établissements |
| 56–60 s | Fin | Sceau, ESURSI, « Application de signalement », nom du Ministère, « Justice · Transparence · Mérite », bouton + URL |

## Données et honnêteté

- **Interfaces** : toutes sont des captures du vrai site (public et `/admin`) du 22/10/2026, en lecture
  seule (les requêtes non-GET étaient bloquées pendant la capture : rien n'a été envoyé ni modifié).
- **Dossier de démonstration** : `SIG-ESURSI-2026-4F7A2D` (« Vente de points avant la délibération »)
  est posé sur les vrais gabarits (formulaire, liste, fiche, historique). Établissement, territoire
  et ID référentiel sont floutés ; aucun nom de personne mise en cause n'apparaît.
- **Reconstruits (pas de capture possible)** : la carte « référence + code de suivi » après l'envoi
  (aucun vrai signalement n'a été déposé ; libellés repris de la page « Suivre un dossier ») ; le menu
  déroulant natif du select « Faire évoluer le dossier » (options réelles) ; la carte nationale
  améliorée (GeoJSON réel de l'application, palette réelle, + noms, légende, pays voisins).
- **Chiffres** : 26 signalements / 26 provinces / 1 618 établissements (accueil public) ; Kinshasa 13
  (statistiques publiques) ; panneau Kinshasa « 6 établissement(s) · 12 signalement(s) » et compteurs
  5-3-1-1-1-1 (tableau de bord), noms d'établissements floutés. Les autres provinces n'affichent pas
  de chiffre, comme la plateforme qui masque les effectifs < 5.
- **Application mobile native** : l'historique d'un dossier mentionne « déposé via l'application
  mobile ». Je n'y ai pas accès ; le parcours téléphone montre la version web mobile du formulaire.

## Mesuré / regardé / non vérifié

- `npx hyperframes check` : OK (0 erreur lint, runtime, layout, motion, contraste).
- Revue image par image : planches beats, coutures (11 seams), feuille téléphone 360 px.
- Son : **mesuré, pas écouté**. Voix normalisée à −16 LUFS (pic −1,7 dBTP) ; musique ≈ 0,22 sous la
  voix, ≈ 0,5 entre les phrases ; effets calés pic + 1 image. Mesures du fichier final dans la section
  « Rendu » ci-dessous.

## Avertissements gardés volontairement

- `line_unread` sur le montage d'ouverture (0–6 s) : coupes au temps (124 BPM) voulues ; chaque mot
  principal reste ≥ 0,43 s et la voix les dit.
- `line_unread` sur les libellés du rail d'étapes et du menu déroulant : le processus défile vite,
  la voix porte le sens ; « Mode anonyme » et la fiche dossier tiennent plus longtemps.
- `text_below_floor` : textes d'UI à l'intérieur des appareils (barre d'URL, heure, noms des
  provinces 18–21 px, menu 15 px avant zoom) — ce sont des détails d'interface, pas des titres.
- `escaped_container` : l'encoche du MacBook dépasse volontairement de l'écran.

## Le plan le plus faible / avec plus de temps

- Le passage carte (31,7–32,4 s) : la carte reconstruite arrive vide (blanche) avant que les couleurs
  se propagent ; avec plus de temps je ferais un vrai morphing des polygones Leaflet → SVG.
- Le traitement Mac est dense (5 actions en 8 s) ; une version 75 s laisserait respirer la messagerie.
- Le rendu final de l'écran de confirmation devrait idéalement être une vraie capture : envoyez-moi
  une capture de la page affichée après « Envoyer le signalement » et je la remplace.

## Rendu

- `renders/esursi-signalement-national.mp4` — 60,0 s, 1920×1080, 30 fps, H.264 + AAC, ~23 Mo
  (qualité « delivery »).
- Son mesuré sur le fichier final : −14,7 LUFS intégré, pic vrai −1,4 dBTP, aucun écrêtage.
- Rendu local : `npx hyperframes render --quality delivery --output renders/esursi-signalement-national.mp4`
  (GSAP est embarqué dans `assets/vendor/`, le rendu ne dépend d'aucun réseau).
