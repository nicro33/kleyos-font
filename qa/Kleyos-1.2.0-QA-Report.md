# Kleyos 1.2.0 — Contrôles de publication

Base : H2-i31 Assemblages. Date : 28 octobre 2026.

Les deux TTF ont des noms publics stables et la version OpenType 1.310.
Le script de publication vérifie que toutes les tables autres que `name` et
`head` restent identiques aux fontes i31 validées, y compris `glyf`, `hmtx`,
`GPOS` et `kern`. Le même contrôle passe après conversion WOFF2.

Les quatre fichiers TTF/WOFF2 passent OpenType Sanitizer 9.2.0.
Les contrôles numériques d'i31, dont 15 129 paires par variante, sont conservés
dans `i31-VALIDATION.json`. Les seuls changements de cette publication sont
les métadonnées de nommage et le libellé normalisé de licence.

## Profil Google Fonts

FontBakery 0.12.10, profil `googlefonts`, exécuté séparément sur chaque famille.
Par variante : **88 PASS, 9 FAIL, 10 WARN, 136 SKIP, 8 INFO, 0 ERROR**.
Les vérifications nécessitant le réseau sont ignorées. Les autres SKIP
comprennent des contrôles non applicables à ces fichiers ; les rapports
complets précisent chaque condition.

Les échecs concernent : pages de codes OS/2, forme des mentions de copyright,
noms de fichiers et noms OpenType, couverture de glyphes, table `gasp`,
`USE_TYPO_METRICS` et préparation sans hinting / smart dropout. Ils ne sont
pas présentés comme résolus par la publication.

La comparaison avec le jeu GF Latin Core courant retrouve **163 caractères
Unicode manquants**, plus quatre noms de glyphes non encodés à traiter.
Le jeu de référence est conservé avec sa provenance et sa date de consultation.

Le nom réservé Kleyos est maintenu dans la licence. Le guide Google Fonts
demande de traiter ce point avant admission. Les sources éditables UFO/Glyphs,
la fabrication Google Fonts reproductible et la signature du CLA restent à
préparer. Aucun ticket de demande d'ajout Kleyos n'a été retrouvé dans
`google/fonts` à la vérification du 28 octobre 2026.

## Vérifications restantes

Le chargement et le rendu effectifs dans Chrome, Firefox, Safari, ainsi que
sur les systèmes visés, ne sont pas vérifiés ici. Le navigateur automatisé
n'a pas pu être installé dans cet environnement. OTS ne remplace pas ce test.
L'épreuve physique à 100 % reste à examiner.

Voir `documentation/PUBLICATION.md` pour les sources officielles et la
différence entre diffusion web et admission à un catalogue.
