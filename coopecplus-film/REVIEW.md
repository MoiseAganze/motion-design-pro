# REVIEW — film COOPECPLUS (v1)

Rendu : `renders/coopecplus-presentation.mp4` — 1920 x 1080, 30 fps, 112 s, H.264 + AAC.

## Choix créatifs
- Piste A « Une journée à la COOPEC » (voir `STORYLINES.md`) : un seul fil, David, nouveau membre, de 7 h 30 au soir, passé de rôle en rôle (directeur, caissière, gestionnaire des membres, gestionnaire de crédit, comptable, administrateur, contrôleur). Non construites : B « Avant / après » et C « Quatre yeux ».
- Tout ce qui est montré est l'appli réelle, jouée de bout en bout avec Playwright sur la base de démonstration : ouverture de journée, billetage, inscription en 5 étapes, encaissement de l'adhésion, ouverture de compte, dépôt, retrait au-delà d'un seuil de 500 000 CDF créé pour l'occasion, approbation par le directeur, demande de crédit, analyse, comité, déblocage, contrat, création d'un utilisateur, mot de passe refusé, vérification du journal d'audit, clôture de caisse.
- Le bandeau « Base de démonstration » de l'appli est masqué sur les captures ; les reçus et le contrat gardent leur mention « Document de démonstration ».
- La scène « avant » (registres, Excel, 9 836 500 ≠ 9 786 500) est une illustration, pas une donnée de l'appli.

## Mesuré
- `check` : aucune erreur. Avertissements gardés : contraste du slogan final pendant son passage du gris au blanc (voulu, 0,5 s).
- Son mesuré, pas écouté : −13,5 LUFS intégrés, crête −1,2 dBFS, aucune saturation. Voix normalisée (loudnorm −15 LUFS).
- Revue des 12 raccords à ±0,2 s : le raccord logo → appli (21,9 s) et appli → logo (104,6 s) tombent juste ; les whips montrent l'écran entrant dès la coupe.

## Non vérifié
- Prononciation écoutée par personne : la transcription automatique entend « Copec Plus » et « Bukavu ».
- Pas de musique : aucune source (catalogue HeyGen non connecté). Voix + effets seuls.

## Plan le plus faible
- La transition « confiance » → reveal (15,3 s) : le mot disparaît d'une image à l'autre avant l'inondation marine. Avec plus de temps : laisser le mot fissuré sous l'inondation.
- La date de naissance apparaît au format mm/jj/aaaa dans la capture du formulaire (locale du navigateur de capture).

## Prochaines étapes possibles
- Musique de fond (connexion HeyGen gratuite, puis `media-use` bgm) calée sur 104,6 s pour l'impact du logo.
- Version verticale 9:16 et version courte de 30 s pour les réseaux.
