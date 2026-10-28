# Publication de Kleyos

Le dépôt existant publiait les familles **Kleyos Display** et **Kleyos Text**
avec TTF, WOFF2, CSS, licence OFL et un ZIP dans `dist/`. Son README affichait
1.1.0 (H2-i25b-balanced), alors que le dernier message de commit annonçait
encore 1.0.0. Aucun tag ni objet GitHub Release n'était présent à la vérification
du 28 octobre 2026. Cette procédure reprend la structure effectivement publiée
et rend la version courante explicite.

1. Identifier et vérifier les fontes candidates, leurs empreintes et leurs QA.
2. Produire les binaires publics avec les noms de familles stables. Préserver
   les dessins, le crénage et les métriques de la candidate retenue.
3. Actualiser README, CHANGELOG, FONTLOG, manifeste, CSS et sommes SHA-256.
4. Vérifier la conversion WOFF2 et le chargement web ; conserver les limites
   des contrôles. Les tests Google Fonts ne valent pas une admission au catalogue.
5. Construire l'archive versionnée dans `dist/`, publier le commit et un tag
   immuable. Une page GitHub Release peut être ajoutée à ce tag indépendamment.
6. Vérifier les fichiers sur GitHub et les URL web avec version explicite.

## Version 1.2.0

Base : **H2-i31 Assemblages**. Les métadonnées publiques gardent les familles
Kleyos Display / Kleyos Text. Le numéro OpenType reste **1.310**, supérieur à
celui de l'ancienne publication ; **1.2.0** est le numéro public de distribution.
La différence est consignée dans `manifest.json`.

Le script `sources/build_public.py` reconstruit les métadonnées publiques
à partir des TTF i31 identifiés par SHA-256. Les entrées binaires sont dans
`sources/validated-i31/`. Ce mécanisme n'est pas encore une chaîne Google Fonts
fondée sur des sources de dessin éditables UFO/Glyphs.

## Police web et catalogue

Les WOFF2 peuvent être hébergées et chargées avec `@font-face`, sans inscription
dans un catalogue. Le tag public permet aussi la distribution par jsDelivr :

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/nicro33/kleyos-font@v1.2.0/css/kleyos.css">
```

L'inscription à **Google Fonts** est une démarche distincte. Le dépôt et la
licence ouverts sont des prérequis ; les points restant à traiter sont :

- compléter **GF Latin Core** ; voir `qa/googlefonts/Latin-Core-Coverage.json` ;
- examiner et corriger les échecs réels du profil FontBakery `googlefonts` ;
- fournir les sources éditables et une construction reproductible en une commande ;
- traiter le **Reserved Font Name Kleyos**, conservé dans cette publication.
  Le guide d'admission demande une OFL sans RFN ; toute modification de ce choix
  doit être décidée par Nicolas Gros, détenteur des droits ;
- vérifier les métriques, les noms et les rendus sur les navigateurs et systèmes visés ;
- remplir le CLA Google, puis ouvrir une demande d'ajout et attendre la revue.

Références officielles vérifiées le 28 octobre 2026 :

- https://googlefonts.github.io/gf-guide/onboarding.html
- https://googlefonts.github.io/gf-guide/requirements.html
- https://googlefonts.github.io/gf-guide/production.html
- https://googlefonts.github.io/gf-guide/upstream.html
- https://github.com/jsdelivr/jsdelivr#github

Une demande Google Fonts et la signature du CLA ne font pas partie de cette
publication GitHub ; aucun statut d'admission n'est revendiqué.
