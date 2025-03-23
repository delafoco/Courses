# Application de Matching Client

Cette application propose deux versions pour le matching de clients :

## Version Simple (`app_base.py`)

La version simple utilise un algorithme de matching basique avec les caractéristiques suivantes :
- Utilisation de l'algorithme Jaro-Winkler pour la comparaison des chaînes
- Score final calculé comme moyenne simple des scores individuels
- Interface simplifiée avec :
  - Sélection du nombre de clients
  - Ajustement du seuil de matching
  - Affichage des matches trouvés avec leurs scores

Pour lancer la version simple :
```bash
streamlit run app_base.py
```

## Version Avancée (`app_advanced.py`)

La version avancée offre des fonctionnalités plus sophistiquées :
- Algorithme de matching pondéré
- Normalisation avancée des chaînes de caractères
- Pondération personnalisable des différents champs
- Visualisation des scores avec histogramme
- Affichage détaillé des données brutes
- Plus de variations dans la génération des données de test

Pour lancer la version avancée :
```bash
streamlit run app_advanced.py
```

## Différences principales

1. **Algorithme de matching** :
   - Version simple : moyenne simple des scores
   - Version avancée : score pondéré avec normalisation

2. **Interface** :
   - Version simple : interface minimaliste
   - Version avancée : interface complète avec visualisations

3. **Données de test** :
   - Version simple : variations basiques
   - Version avancée : plus de variations et d'erreurs possibles

4. **Visualisation** :
   - Version simple : affichage basique des scores
   - Version avancée : histogramme des scores et détails complets

## Prérequis

Les deux versions nécessitent les packages Python suivants :
- streamlit
- pandas
- numpy
- fuzzywuzzy
- python-Levenshtein
- unidecode
- plotly (uniquement pour la version avancée)

Pour installer les dépendances :
```bash
pip install -r requirements.txt
```

## Fonctionnalités

- Génération de données clients simulées
- Configuration des poids des attributs
- Calcul de similarité entre les clients
- Visualisation des résultats
- Analyse des performances
- Recommandations d'optimisation

## Installation

1. Clonez le repository :
```bash
git clone [URL_DU_REPO]
cd matching_customers
```

2. Créez un environnement virtuel et activez-le :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Pour lancer l'application :
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## Configuration

Vous pouvez ajuster les paramètres suivants dans l'interface :
- Nombre de clients à générer
- Taux d'erreur dans les données
- Poids des différents attributs
- Seuil de similarité

## Structure du projet

```
matching_customers/
├── app.py              # Application principale
├── requirements.txt    # Dépendances
└── README.md          # Documentation
```

## Algorithme de Matching

L'application utilise :
- L'algorithme Jaro-Winkler via la bibliothèque fuzzywuzzy pour comparer les chaînes de caractères
- Une approche pondérée pour combiner les scores de similarité des différents attributs
- Un système de regroupement pour identifier les ensembles de clients similaires 