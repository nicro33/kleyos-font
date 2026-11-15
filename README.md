# Kleyos

Kleyos est une police manuscrite de type brush dessinée sous la direction de
Nicolas Gros pour les titres et les phrases courtes. La version 1.3.0
regroupe ces usages dans une seule famille, **Kleyos**, style **Regular**.
Elle reprend les contours et le crénage d’i33 et couvre Google Fonts Latin Core.

[Épreuve de Kleyos Regular](qa/release-1.3.0/Specimen.png) ·
[Contrôles de la 1.3.0](qa/release-1.3.0/REPORT.md)

## Installer et utiliser

- [TTF pour les applications](fonts/ttf/Kleyos-Regular.ttf)
- [WOFF2 pour le web](fonts/woff2/Kleyos-Regular.woff2)
- [Feuille CSS](css/kleyos-regular.css)

Pour l’hébergement web, conserver les chemins relatifs du WOFF2 et de la CSS.

```html
<link rel="stylesheet" href="/css/kleyos-regular.css">
<h1 class="kleyos">Kleyos</h1>
<p class="kleyos">Écouter le vent et laisser venir les mots.</p>
```

Les fichiers, noms de famille et règles CSS de la [version 1.2.0](https://github.com/nicro33/kleyos-font/tree/b4412dec8b36b763e583524f922d0ebc2b91d3d6)
restent disponibles pour les intégrations Display et Text existantes.
La 1.3.0 reprend l’espacement Display de 250 unités pour l’espace courant et
l’insécable, et de 125 pour l’insécable fine. Les titres et les phrases
gardent leurs tailles propres dans la mise en page. Vérifier les coupures
lors du passage des calques éditables de Text à Kleyos.

## Construire depuis les sources

Le maître [KleyosMaster.ufoz](sources/KleyosMaster.ufoz) est l’UFO 3 i33
compressé. Extraire le fichier avec `unzip` pour éditer le dossier
`KleyosMaster.ufo` avec un éditeur UFO. Les références du maître sont
consignées dans [le manifeste](manifest.json).

Avec Python 3.12, dans un environnement virtuel :

```sh
python -m pip install -r sources/requirements-build.lock
python sources/build_public.py
cmp build/public/fonts/ttf/Kleyos-Regular.ttf fonts/ttf/Kleyos-Regular.ttf
cmp build/public/fonts/woff2/Kleyos-Regular.woff2 fonts/woff2/Kleyos-Regular.woff2
cmp build/public/manifest.json manifest.json
```

Les deux fichiers et le manifeste sont générés dans `build/public/`.
[Procédure de vérification et de publication](documentation/PUBLICATION.md).

## Licence

[SIL Open Font License 1.1](OFL.txt). Nom réservé **Kleyos**.
[Crédits](AUTHORS.txt) et [provenance](documentation/PROVENANCE.md).
