# 🏥 Cancer Prediction Application

Application web professionnelle pour la prédiction du cancer basée sur des données épidémiologiques et l'apprentissage automatique.

## 📋 Table des matières

- [Architecture](#architecture)
- [Fonctionnalités](#fonctionnalités)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API Documentation](#api-documentation)
- [Structure du Projet](#structure-du-projet)

## 🏗️ Architecture

L'application suit une **architecture modulaire et professionnelle** avec séparation des responsabilités :

```
app_module/
├── __init__.py              # Application Factory
├── config/
│   ├── settings.py          # Configuration centralisée
│   └── __init__.py
├── routes/
│   ├── prediction.py        # Routes prédiction
│   ├── dashboard.py         # Dashboard Dash
│   ├── health.py            # Health checks
│   └── __init__.py
└── utils/
    ├── models.py            # Gestionnaire de modèles ML
    ├── data.py              # Utilitaires données
    ├── __init__.py          # Réponses API standardisées
    └── helpers.py           # Fonctions utilitaires
```

## ✨ Fonctionnalités

### 1. **Prédiction ML** 
- 4 modèles disponibles : Logistic Regression, Random Forest, Gradient Boosting, KNN
- Interface web et API JSON
- Gestion des erreurs robuste

### 2. **Dashboard Interactif** (Dash)
- Visualisations en temps réel
- Filtres dynamiques par âge, sexe, santé
- Statistiques détaillées
- Graphiques professionnels

### 3. **API REST**
- Endpoints structurés avec Blueprint
- Logging centralisé
- Réponses standardisées
- Health checks

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip ou conda

### Étapes

1. **Cloner le projet**
```bash
cd /home/sebabte/cancer_app
```

2. **Créer un environnement virtuel**
```bash
python -m venv cancer
source cancer/bin/activate  # Linux/Mac
# ou
cancer\Scripts\activate     # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration**
```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer .env selon vos besoins
nano .env
```

5. **Lancer l'application**
```bash
python run.py
```

L'application sera accessible à : `http://localhost:5000`

## 📖 Utilisation

### Interface Web Principale
```
http://localhost:5000/api/prediction/
```
- Remplir le formulaire avec les paramètres du patient
- Sélectionner un modèle
- Obtenir la prédiction et la probabilité

### Dashboard
```
http://localhost:5000/dashboard/
```
- Visualiser les statistiques de la population
- Appliquer des filtres interactifs
- Exporter les données

## 🔌 API Documentation

### 1. Prédiction (POST)
```bash
POST /api/prediction/api
Content-Type: application/json

{
  "model_choice": "random_forest",
  "HeartDisease": "No",
  "BMI": 25.5,
  "Smoking": "No",
  "Sex": "Male",
  "AgeCategory": "35-39",
  ...
}

Response (200):
{
  "status": "success",
  "message": "Succès",
  "data": {
    "prediction": 0,
    "probability": 0.123,
    "model": "random_forest"
  }
}
```

### 2. Modèles Disponibles (GET)
```bash
GET /api/prediction/models

Response (200):
{
  "status": "success",
  "data": {
    "models": ["log_reg", "random_forest", "gradient_boosting", "knn"]
  }
}
```

### 3. Health Check (GET)
```bash
GET /api/health

Response (200):
{
  "status": "success",
  "data": {
    "status": "healthy",
    "models_loaded": 4,
    "available_models": ["log_reg", "random_forest", "gradient_boosting", "knn"]
  }
}
```

### 4. Info Application (GET)
```bash
GET /api/info

Response (200):
{
  "status": "success",
  "data": {
    "app_name": "Cancer Prediction API",
    "version": "2.0.0",
    "endpoints": {
      "prediction": "/api/prediction",
      "health": "/api/health",
      "dashboard": "/dashboard/"
    }
  }
}
```

## 📁 Structure du Projet

```
cancer_app/
├── app_module/              # Package principal
│   ├── __init__.py         # Factory pattern
│   ├── config/             # Configuration
│   ├── routes/             # Routes et blueprints
│   ├── utils/              # Utilitaires réutilisables
├── data/                    # Données
│   └── dataset.csv
├── models/                  # Modèles ML préentraînés
│   ├── pipeline_logistic_regression.pkl
│   ├── pipeline_random_forest.pkl
│   ├── pipeline_gradient_boosting.pkl
│   └── pipeline_knn.pkl
├── static/                  # Fichiers statiques
│   ├── style.css
│   └── form.js
├── templates/               # Templates HTML
│   ├── index.html
│   └── dashboard.html
├── run.py                   # Point d'entrée
├── wsgi.py                  # WSGI pour production
├── requirements.txt         # Dépendances
└── README.md               # This file
```

## 🔧 Configuration

### Variables d'environnement (.env)

```
FLASK_ENV=development          # development ou production
FLASK_HOST=0.0.0.0            # Adresse du serveur
FLASK_PORT=5000               # Port d'écoute
SECRET_KEY=your-key           # Clé secrète (CHANGE en prod)
LOG_LEVEL=INFO                # Niveau de logging
```

## 🚢 Déploiement Production

### Avec Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Avec Docker (optionnel)

Créer un `Dockerfile` :

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

Construire et lancer :
```bash
docker build -t cancer-app .
docker run -p 5000:5000 cancer-app
```

## 📊 Logging

Les logs sont enregistrés avec timestamps et niveaux :

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message informatif")
logger.error("Message d'erreur")
```

## 🧪 Tests

```bash
# Exécuter les tests
pytest

# Avec couverture
pytest --cov=app_module
```

## 📝 Licence

MIT License

## 👥 Support

Pour toute question ou problème, consultez la documentation ou ouvrez une issue.

---

**Dernière mise à jour**: Décembre 2024
