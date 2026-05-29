# IDF Coworking Hub - M2 MSSI

## Présentation du Projet
Ce projet a été réalisé dans le cadre du cours Python du Master 2 Management de la Sécurité des Systèmes d'Information (MSSI). L'objectif est de fournir une plateforme d'aide à la décision pour les travailleurs nomades en Île-de-France, permettant de localiser et d'évaluer la fiabilité des espaces de coworking.

L'application transforme des données brutes scrapées sur le web en une interface interactive, sécurisée et accessible.

## Architecture Technique
Le projet suit une pipeline de données structurée :
1. **Collecte (Scraping) :** Extraction des données depuis `leportagesalarial.com` via `Requests` et `PyQuery`.
2. **Enrichissement :** Utilisation de l'API Serper (Google Search Data) pour vérifier la cohérence SEO et récupérer les emails officiels.
3. **Traitement & Géocodage :** Nettoyage des données avec `Pandas` et conversion des adresses en coordonnées GPS avec `GeoPy`.
4. **Visualisation :** Interface utilisateur développée avec `Streamlit` et cartographie dynamique via `Folium`.

## Fonctionnalités Clés
- **Carte Interactive :** Visualisation des espaces avec regroupement (clusters) pour une meilleure lisibilité.
- **Filtres Avancés :** Recherche par département (75, 77, 78, 91, 92, 93, 94, 95) et par nom.
- **Indicateur de Fiabilité :** Identification des espaces "SEO Consistent" pour garantir la légitimité des établissements.
- **Accessibilité :** Export des données en format CSV et affichage d'un tableau de données brut conforme aux standards d'accessibilité.

## Installation et Utilisation Locale
1. Clonez le dépôt :
   ```bash
   git clone [URL]
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
3. Préparez les données :
   ```bash
   python clean_data.py
4. Lancez l'application :
   ```bash
   streamlit run app.py
