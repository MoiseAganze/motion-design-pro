# REVIEW — ESURSI · Signalement national, v3 (70,2 s, 1920×1080, 30 fps)

Version 3 : le film suit mot pour mot le nouveau script du client. Même voix (ElevenLabs
« Audrey », `McVZB9hVxVSk3Equu8EH`), même musique. Chaque image « joue » le mot que la voix dit.

## Choix d'interprétation (à valider)

- **« des fonds détournés »** est ajouté dans la liste d'ouverture (« des frais illégaux, des fonds
  détournés, de faux diplômes… »). Le client demande d'insister légèrement sur le détournement, et
  une règle précédente veut que tout abus montré soit dit. Le plan dure 1,35 s, en marine, avec les
  billets déviés hors de leur route. La tuile « Détournement » reçoit aussi un liseré doré dans la
  grille des 13 catégories.
- **Nom du Ministère** : le script dit « du ministère de l'Enseignement supérieur ». La voix dit le
  nom complet corrigé, « Ministère de l'Enseignement Supérieur, Universitaire, Recherche
  Scientifique et Innovations » (sans « de l' »), parce que le client tenait à ce qu'on l'entende. Le
  même libellé est écrit sur la révélation et sur la carte de fin.
- **Durée** : le script lu à un débit naturel donne 67,5 s de voix. Le film dure 70,2 s, et la fin
  naturelle du morceau tombe sur la dernière image.

## Déroulé

| Temps | Voix | Image |
| --- | --- | --- |
| 0–9,4 s | « Un abus dans votre université ? Des points qui se vendent, des frais illégaux, des fonds détournés, de faux diplômes, du harcèlement. » | Six plans illustrés, un par abus, coupés sur la voix : relevé 18/20 et étiquette de prix, reçu tamponné ILLÉGAL, billets déviés, diplôme tamponné FAUX, bulles d'alerte qui se resserrent. |
| 9,4–14,1 s | « Trop souvent, on se tait. Par peur… ou faute de savoir à qui parler. » | Une bulle qui parle ; sur la coupure musicale, une fermeture éclair la ferme. Elle tremble, puis un tracé erre vers des points d'interrogation. |
| 14,1–22,4 s | « Voici la plateforme nationale de signalement du Ministère… » | Sur la reprise de la musique : l'affiche officielle, puis un panneau bleu avec le sceau, ESURSI et le nom du Ministère, mot à mot. |
| 22,2–37,4 s | Téléphone, 13 catégories, 8 étapes | Vraie version mobile du site : tap sur « Déposer un signalement », chronomètre (« quelques minutes »). Les 13 vraies catégories jaillissent de l'écran et les quatre citées s'allument. Les 8 vraies étapes s'affichent à côté de l'écran réel (province, établissement, faits, preuves). |
| 37,4–43,6 s | Anonyme ou identifié ; aucune donnée conservée | L'étape « Mode » devient un interrupteur, avec un vrai tap sur la carte « Signalement anonyme ». Nom, e-mail, téléphone et adresse IP sont barrés puis s'évaporent avant le stockage, qui reste à 0. Citation du vrai texte du site. |
| 43,5–49 s | Référence et code de suivi ; étape par étape | Envoi réel, puis un ticket sort du téléphone. La référence et le code volent dans la vraie page « Suivre un signalement ». Le dossier parcourt le circuit officiel en 8 statuts. |
| 48,9–56,7 s | Côté ministère : tableau de bord, carte | MacBook : le dossier arrive en tête de la vraie liste. Clic sur le tableau de bord national (indicateurs réels), plongée dans la carte reconstruite, remplie province par province, avec la bulle Kinshasa (13). |
| 56,6–60,1 s | « Un dossier critique… sous 24 heures » | Vraie ligne d'un dossier Critique dans la liste des agents, avec son échéance SLA. Cadran 24 h et vrais délais (24 h / 72 h / 7 j / 15 j). |
| 60–64,6 s | « Justice. Transparence. Mérite. Votre voix compte. » | Balance, œil, médaille, porte-voix avec ondes ; la devise réelle du site se remplit mot à mot. |
| 64,5–70,2 s | « Signalez sur signal.minesursi.gouv.cd » | Carte de fin : sceau, ESURSI, nom du Ministère, adresse tapée au rythme de la voix. |

## Données et honnêteté

- **Interfaces** : captures du vrai site (public et `/admin`) du 22/10/2026, faites en lecture
  seule. Les requêtes non-GET étaient bloquées : rien n'a été envoyé ni modifié.
- **Contenus réels repris** :
  - les 13 catégories (libellés exacts) ;
  - les 8 étapes (Catégorie, Province, Établissement, Personne concernée, Description, Preuves, Mode,
    Prévisualisation) ;
  - le texte du mode anonyme (« Aucune donnée personnelle ni adresse IP n'est conservée ») ;
  - les 8 statuts du circuit officiel ;
  - les délais de prise en charge (page Procédure) ;
  - la devise « Justice · Transparence · Mérite » ;
  - les indicateurs du tableau de bord ;
  - Kinshasa = 13 (statistiques publiques).
- **Dossier de démonstration** : `SIG-ESURSI-2026-4F7A2D` (« Vente de points avant la délibération »).
- **Dossier Critique (scène 24 h)** : c'est un vrai dossier de la liste des agents. Sa référence et
  son titre sont floutés ; la gravité, le statut, l'échéance SLA et la date sont lisibles.
- **Reconstruits ou illustrés** :
  - le ticket « référence + code de suivi » (aucun vrai signalement déposé) ;
  - l'interrupteur anonyme/identifié, le stockage « 0 » et le cadran 24 h, qui illustrent des
    règles réelles ;
  - la carte nationale améliorée, tirée du GeoJSON réel de l'application, avec la palette réelle,
    les noms des provinces, une légende et les pays voisins.
- **Pictogrammes** : Streamline Plump (CC BY 4.0), recolorés à la charte. Le crédit apparaît sur la
  carte de fin.

## Mesuré / regardé / non vérifié

- `npx hyperframes check` : réussi.
  - 0 erreur lint, runtime et motion.
  - Avertissements gardés volontairement :
    - textes d'UI petits dans les appareils et dans les tuiles en vol ;
    - les lignes « line_unread » des tuiles pendant leur envol (elles restent ensuite 5 s à l'écran) ;
    - un contraste mesuré pendant un fondu de couleur.
- Images regardées : chaque scène et chaque couture (planches de contact). Un plan v2 restait dans
  le film (révélation) ; il a été réécrit.
- Son : **mesuré, pas écouté**.
  - Voix normalisée à −16 LUFS.
  - Musique à ≈ 0,22 sous la voix, remontée sur la coupure (« on se tait ») et sur la fin.
  - Mesures du fichier final ci-dessous.

## Le plan le plus faible / avec plus de temps

- La scène 24 h ne dure que 3,5 s pour trois informations (dossier critique, cadran, délais) ; une
  version 75 s la laisserait respirer.
- Le ticket « référence + code » est reconstruit. Une capture de la vraie page affichée après
  « Envoyer le signalement » le remplacerait.

## Rendu

- `renders/esursi-signalement-national.mp4` : 70,2 s, 1920×1080, 30 fps, H.264 + AAC, ~23 Mo
  (qualité « delivery »).
- Son mesuré sur le fichier final : −14,1 LUFS intégré, pic vrai −1,3 dBTP, aucun écrêtage.
- Huit images extraites du MP4 final ont été comparées aux aperçus : identiques.
- Rendu local : `npx hyperframes render --quality delivery --output renders/esursi-signalement-national.mp4`
  (GSAP est embarqué dans `assets/vendor/`, le rendu ne dépend d'aucun réseau).

## Historique

- v1 (60 s) puis v2 (62 s) : storyline « le voyage d'un dossier », hook en 9 abus, traitement du
  dossier sur Mac. Remplacées par la v3 à la demande du client (nouveau script).
