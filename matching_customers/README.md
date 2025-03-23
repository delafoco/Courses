# Application de Matching Client

Cette application Streamlit permet de simuler et d'analyser le matching de clients en utilisant différents attributs (nom, prénom, email, téléphone, etc.).

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