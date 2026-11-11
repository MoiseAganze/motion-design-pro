# REVIEW — KWIKAMA v2, « Le dossier en cinq écrans »

- **Format :** 1920 x 1080, 30 fps, 153 s.
- **Rendu :** `renders/kwikama-demonstration.mp4`.
- **Application filmée :** https://kwikamademo.vercel.app/.

## Ce qui a changé par rapport à la v1, et pourquoi

| Point | Choix | Pourquoi |
|---|---|---|
| Parcours | Les cinq écrans de la note de démonstration, dans son ordre : contrôle de légalité, preuves et scellés, analyse et enquête financière, coordination, avoirs (RI 8) | « En 5 clics, pas un de plus » |
| Fil rouge | Le dossier DPJ-2026-014 | Il est présent sur chaque écran |
| Messages au Ministre | Repris presque mot pour mot ; seule la formule « Monsieur le Ministre » est retirée | Le film peut ainsi être montré à d'autres publics |
| Changement de rôle | Montré deux fois en vrai, avec le bouton « Changer de rôle » et la page « Choisir un poste de travail » : Magistrat → Coordonnateur UNICEP, puis → Point focal CENAREF pendant 15 s (modules verrouillés, « hors habilitation »), enfin retour au Magistrat pour les avoirs | Conseil de la note, et « chorégraphie conseillée » de l'app |
| Écrans à double tranchant | Passerelles d'interconnexion (les trois registres de l'État) et sélecteur de rôles laissés hors champ | Avertissement de la note (« à réfléchir avec Zaina ») |
| « Bandeau jaune » | L'encadré « Infrastructure requise » de l'écran d'analyse est surligné en or au moment de la phrase sur l'infrastructure souveraine | Dans la nouvelle version, c'est cet encadré qui porte le message |
| Apothéose | Le panneau bleu nuit « Résultat immédiat 8 du GAFI » de l'écran Avoirs s'ouvre en plein cadre (3 550 000 $US acquis, 3 436 000 $US sous main de justice, 73 %), puis la signature | Conclusion demandée par la note |
| Pied de page final | Libellé de la nouvelle app : « Supervision : Ministère de la Justice, autorité de tutelle de l'UNICEP » | L'hébergement APLC et les bailleurs, cités en v1, n'apparaissent plus dans la nouvelle version |

## Cohérence des animations

Chaque chapitre suit la même grammaire :

1. **Carte de chapitre :** le Mac recule à droite (position `CHP`) et le numéro or 01–05 entre à gauche, avec le titre et une ligne-message.
2. **Clic :** le curseur clique le module dans la vraie barre latérale (anneau or).
3. **Plongée :** la caméra entre dans l'écran, et des cadres or désignent chaque élément au mot près de la voix.
4. **Illustration :** quand l'idée dépasse l'écran, une illustration réutilise les composants de l'app (cartes blanches, puces de statut, hexagone des six institutions).

L'hexagone des six institutions de l'écran Coordination ouvre aussi le film (les six silos qui se rejoignent) et le referme (l'anneau autour du logo).

Les illustrations :

- verrou de légalité (signalement validé / article de presse bloqué) ;
- pièce perdue « sur papier », puis chaîne horodatée, nominative et scellée ;
- les deux dossiers sur la carte de la RDC (Matadi, Kolwezi) reliés au compte BCF 00214-…-77 avec la jauge 84 % ;
- la météo posée sur l'hexagone réel ;
- trois périmètres d'habilitation (les barres latérales des trois postes) ;
- la trajectoire identifié → gelé → saisi → confisqué → Trésor.

## Pistes non construites

Le parcours a été fixé par la note de démonstration, donc pas de choix de piste cette fois.

Deux variantes restent possibles :

- **une version 60 s,** qui ne garde que les cartes de chapitre et un plan par écran ;
- **une version « présentateur »,** sans voix, à projeter derrière la démonstration en direct.

## Mesuré, regardé, non vérifié

- **Mesuré :**
  - `hyperframes check` : 0 erreur ;
  - mix de référence à −16,1 LUFS intégré, crête vraie −2,0 dBTP ;
  - voix ramenée à −19 LUFS en mono, musique atténuée de 11 dB sous la voix ;
  - durée et pistes du MP4 contrôlées après rendu.
- **Regardé :** instantanés de chaque scène à chaque correction, planche de revue complète (temps forts, 6 raccords à ±0,2 s : tous continus).
- **Jamais écouté :** la musique (nouvelle partition, une phrase par chapitre), le mix et les 122 bruitages sont mesurés, pas entendus. À écouter en priorité :
  - la respiration avant « KWIKAMA » (13,5–14,3 s) ;
  - le passage dépouillé de la vue CENAREF (110–117 s) ;
  - l'apothéose RI 8 (137,7–143,3 s).
- **Données :** toutes reprises des écrans capturés le 9 novembre 2026. Si l'application change d'ici la présentation, les captures sont à refaire (`assets/ui/`, script de capture décrit dans le README).

## Plan le plus faible

- **Le passage 87,5–93,5 s** (graphe des flux puis infrastructure souveraine) enchaîne deux défilements rapides dans l'écran d'analyse. C'est lisible, mais dense.
- **Avec plus de temps,** je remplacerais le défilement vers le graphe par une coupe nette, et je tiendrais l'encadré « Infrastructure requise » une seconde de plus.

## Avertissements conservés

- **`composition_file_too_large`** (s0 et s4, environ 320 lignes) : chaque scène reste une seule continuité de caméra. La source lisible est dans `src/acts/`.
- **`text_below_floor`** : libellés fins de l'UI réelle et mentions secondaires. Le film est fait pour un écran de présentation, pas un téléphone ; l'information clé est toujours surlignée ou agrandie.
- **`line_unread`** :
  - pour les compteurs, ce sont des faux positifs (les bandes de chiffres comptent comme des mots) ;
  - pour les lignes-messages des cartes de chapitre (2,3–2,5 s), la voix dit la même chose au même moment.
