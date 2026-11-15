# Publication de Kleyos 1.3.0

1. Installer les dépendances de build sur Python 3.12 et lancer
   `python sources/build_public.py`. Comparer les sorties au manifeste
   et aux deux polices publiques comme indiqué dans le README.
2. Vérifier le profil Google Fonts avec FontBakery 1.1.0, la couverture
   Latin Core, OTS et le chargement HTTP dans Chrome et Firefox.
3. Lancer `python sources/package_public.py` pour construire le ZIP et son
   empreinte. Décompresser une copie et lancer `sha256sum -c SHA256SUMS.txt`
   à la racine de l’archive.
4. Vérifier le SHA distant du commit et la disponibilité du tag `v1.3.0`.
   Publier le tag sur ce commit et joindre le ZIP et son fichier `.sha256`
   à la Release GitHub. Comparer les empreintes après téléchargement.

## Catalogue Google Fonts

La candidature concerne **Kleyos**, en **Regular**. Elle s’appuie sur les
sources éditables, le TTF, le build, le spécimen et les rapports liés à un
commit immuable. Le nom réservé Kleyos est toujours déclaré dans l’OFL.
Le périmètre d’une autorisation spéciale doit être discuté avec Google
Fonts. La revue du catalogue et le CLA restent des démarches séparées.

- [Guide de soumission](https://googlefonts.github.io/gf-guide/onboarding.html)
- [Formulaire Add Font](https://github.com/google/fonts/issues/new?template=1_add-font.md)
- [Version 1.2.0, Display et Text](https://github.com/nicro33/kleyos-font/tree/b4412dec8b36b763e583524f922d0ebc2b91d3d6)
