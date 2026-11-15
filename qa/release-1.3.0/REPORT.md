# Kleyos 1.3.0 — contrôles de publication

Contrôles exécutés le 15 novembre 2026 sur **Kleyos Regular** (OpenType 1.411).

| Contrôle | Résultat |
|---|---|
| Archive source i33 | 558 empreintes vérifiées |
| Reconstruction depuis le maître UFOZ | Deux builds identiques octet par octet, 14 tables identiques à i33 Display |
| Couverture | 334 points de code, 340 glyphes, 324 entrées Latin Core vérifiées |
| OTS | TTF et WOFF2 validés |
| Chrome Headless Shell 151.0.7922.34 | HTTP 200, police chargée, SHA-256 du WOFF2 vérifié |
| Firefox 153.0 | HTTP 200, police chargée, SHA-256 du WOFF2 vérifié |
| FontBakery 1.1.0, profil Google Fonts | 0 échec, 0 erreur, 12 avertissements, 108 réussites, 108 contrôles ignorés |

## Avertissements FontBakery

- **Contours** — carons décomposés, nombre de contours, segments superposés,
  sens de certains contours externes, angles aigus et tracés proches d’un
  axe. Le build public conserve le dessin i33. L’épreuve permet une revue
  visuelle des formes, accents et signes à leur taille d’emploi.
- **Diffusion** — article de famille, symboles en dehors des sous-ensembles
  déclarés et avertissement de mise en forme heuristique sur des langues
  hors du jeu Latin Core contrôlé. Le traitement des sous-ensembles reste à
  discuter lors de l’intégration au catalogue.
- **Métadonnées** — déclaration du nom réservé dans l’en-tête OFL, table
  `meta` de scripts absente et identifiant de fournisseur `KLYS` absent de
  la liste intégrée à l’outil.

Le [rapport complet](FontBakery.json.gz) se lit avec
`gzip -dc FontBakery.json.gz`. Les [résultats navigateur](BROWSER-TESTS.json)
comparent la réponse HTTP au WOFF2 publié et mesurent l’égalité des avances
NFC/NFD sur trois exemples. La revue Google Fonts reste ouverte.

## Espacement du jeu de cartes

[Mesures HarfBuzz](card-spacing.json) sur quatre calques de B001, en français,
anglais et allemand. Les 8 lignes Display mesurées ont la même largeur.
Les 17 lignes Text se resserrent de 0 à 6,72 px sur des calques de 900 px.
Les calques dont les textes ont été convertis en tracés conservent leur
rendu. Pour les régénérations depuis un texte éditable, comparer les
coupures et les marges en utilisant le WOFF2 de la version visée.
