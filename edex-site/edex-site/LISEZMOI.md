# Site EdEx — mise en ligne et maintenance

Site statique (HTML, CSS, JavaScript) : aucun serveur, aucune base de données, aucun abonnement obligatoire.

## 1. Mettre le site en ligne (5 minutes)

Le dossier `edex-site` est prêt à être publié tel quel. `index.html` doit se trouver à la racine de l'hébergement.

- **Le plus simple (gratuit)** : Netlify Drop (app.netlify.com/drop) ou Cloudflare Pages. Glissez-déposez le dossier ; le site est en ligne immédiatement, puis rattachez votre nom de domaine.
- **Hébergement classique (cPanel / FTP)** : envoyez le contenu du dossier dans `public_html`.

Le fichier `404.html` est utilisé automatiquement par Netlify et Cloudflare pour les pages introuvables.

Aperçu sur votre ordinateur : double-cliquez sur `index.html`. La navigation fonctionne (les liens sont adaptés automatiquement).

## 2. À valider par EdEx avant la mise en ligne

1. **Tarifs** : le cahier indique « validation obligatoire avant publication ». Les tarifs affichés sont ceux du cahier V2.
2. **Reliure** : le cahier donne « 500 FCFA / 1 000 FCFA » sans préciser la distinction (Licence / Master ? type de reliure ?). Affiché tel quel ; à préciser.
3. **Valeurs** : le cahier V2 en liste 6 (Excellence, Transmission, Intégrité, Innovation, Responsabilité, Impact), la charte en liste 4 (Exigence, Égalité, Clarté, Entraide). Le site suit le cahier.
4. **Intitulés des 5 pôles** et statuts (le cahier demande de les valider).
5. **Pages légales** : `mentions-legales` et `politique-confidentialite` sont des cadres. Les éléments surlignés `[à compléter]` (forme juridique, RCCM/IFU, directeur de publication, hébergeur, durée de conservation, références légales) doivent être renseignés, puis le texte validé.
6. **Numéro WhatsApp** : le lien utilise +229 01 42 01 63 26. Cliquez dessus une fois en ligne pour vérifier qu'il ouvre bien la bonne conversation.
7. **Réseaux sociaux** : « EdEx-Corporation » est affiché en texte. Donnez les liens des comptes pour les rendre cliquables.

## 3. Formulaires (diagnostic et contact)

Sans service d'envoi, le formulaire prépare le message et ouvre **WhatsApp** ou **l'e-mail** du visiteur, qui n'a plus qu'à l'envoyer. Le site n'affiche donc pas « demande reçue » tant qu'aucun service n'est branché.

Pour recevoir les demandes directement (et afficher la confirmation du cahier) : créez un formulaire sur Formspree (ou équivalent) et collez son adresse dans `assets/js/config.js` (`formEndpoint`). Le champ d'ajout de documents apparaît alors automatiquement.

## 4. Ce qui reste à fournir

- **Photos** : aucune photo n'est intégrée (le livre de marque demande de photographier le travail, pas la réussite). Pour ajouter une image de fond au hero de l'accueil : déposer `assets/img/hero.jpg`, puis régénérer le site (voir 5).
- **Logo officiel vectoriel (SVG)** : les logos utilisés (`assets/img/logo-*.webp`) ont été reconstitués à partir de la page 15 de la charte (image, ~600 px de large). Ils sont nets aux tailles du site, mais un SVG officiel est préférable pour l'impression et les très grands écrans.
- **Domaine** : après choix du nom de domaine, ajouter l'image de partage (`assets/img/og-image.jpg`, déjà créée), l'adresse canonique et un `sitemap.xml`.
- **Mesure d'audience** : aucun outil installé (à définir).

## 5. Modifier le site

- **Contacts, textes, tarifs, pôles** : tout est généré depuis `_build/build.py` (contacts en tête de fichier, tarifs dans les listes `SVC_*`). Après modification : `python3 _build/build.py` (Python 3 et la bibliothèque Pillow requis). Sinon, demandez la modification : c'est une affaire de quelques minutes.
- **Couleurs et typographies** : variables en tête de `assets/css/main.css`.
- **Niveau d'animation** : le site respecte automatiquement le réglage « réduire les animations » du visiteur.

## 6. Contenu du dossier

```
index.html · qui-sommes-nous/ · ecosysteme/ (+ pole-1 à pole-5) · comment-ca-marche/
prestations/ · diagnostic/ · contact/ · mentions-legales/ · politique-confidentialite/ · 404.html
assets/  css · js (config.js = réglages) · vendor (GSAP, Lenis, SplitType, en local) · fonts · img
_build/build.py  générateur des pages
```

Polices : Cormorant Garamond Bold et Inter, hébergées localement (aucun appel à Google). Aucune dépendance externe au chargement.
