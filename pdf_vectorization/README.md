# Assistant PDF Intelligent

Cette application permet de vectoriser des documents PDF, de les stocker dans une base vectorielle et d'interroger leur contenu via un LLM.

## Fonctionnalités

- Téléchargement et traitement de documents PDF
- Vectorisation automatique des documents
- Interface de chat pour interroger le contenu des documents
- Stockage persistant des vecteurs
- Support multilingue

## Prérequis

- Python 3.8+
- Une clé API OpenAI

## Installation

1. Clonez ce dépôt
2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Créez un fichier `.env` à la racine du projet avec votre clé API OpenAI :
```
OPENAI_API_KEY=votre_clé_api
```

## Utilisation

1. Lancez l'application :
```bash
streamlit run src/app.py
```

2. Dans l'interface web :
   - Utilisez la barre latérale pour télécharger vos PDFs
   - Une fois les documents traités, vous pouvez poser des questions sur leur contenu
   - L'historique de la conversation est conservé pendant la session

## Structure du projet

```
pdf_vectorization/
├── src/
│   ├── app.py           # Interface utilisateur Streamlit
│   └── pdf_processor.py # Logique de traitement des PDFs
├── data/                # Stockage temporaire des PDFs
├── models/              # Stockage des vecteurs
├── ui/                  # Composants d'interface utilisateur
└── requirements.txt     # Dépendances Python
```

## Notes

- Les documents sont vectorisés en utilisant le modèle `sentence-transformers/all-MiniLM-L6-v2`
- Les vecteurs sont stockés localement dans le dossier `models/vector_store`
- L'application utilise OpenAI pour les réponses aux questions 