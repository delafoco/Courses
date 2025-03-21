# Démonstration SARIMA avec Streamlit

Cette application Streamlit permet de démontrer l'utilisation du modèle SARIMA (Seasonal ARIMA) pour la prédiction de séries temporelles.

## Fonctionnalités

- Génération de données synthétiques avec tendance et saisonnalité
- Configuration interactive des paramètres SARIMA
- Visualisation des données et des prédictions
- Calcul des métriques de performance
- Diagnostics du modèle

## Installation locale

1. Clonez ce dépôt
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation locale

Pour lancer l'application :
```bash
streamlit run app.py
```

## Déploiement sur Streamlit Cloud

1. Créez un compte sur [Streamlit Cloud](https://share.streamlit.io/)
2. Connectez votre compte GitHub/GitLab
3. Cliquez sur "New app"
4. Sélectionnez ce dépôt
5. Définissez le fichier principal comme `app.py`
6. Cliquez sur "Deploy"

## Paramètres SARIMA

- **Ordre du modèle** :
  - p : ordre AR (Auto-Régressif)
  - d : ordre de différenciation
  - q : ordre MA (Moyenne Mobile)

- **Ordre saisonnier** :
  - P : ordre AR saisonnier
  - D : ordre de différenciation saisonnière
  - Q : ordre MA saisonnier
  - s : période saisonnière 