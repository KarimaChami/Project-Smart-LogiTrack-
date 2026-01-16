# Smart LogiTrack – Système Prédictif d’ETA Taxi

Smart LogiTrack est une solution Big Data & IA qui prédit la durée estimée d’arrivée (ETA) de trajets taxi et expose ces prédictions via une API REST sécurisée.

---

## 🚀 Objectifs du projet

- Mettre en place une architecture Big Data de bout en bout (Bronze → Silver → ML).
- Nettoyer et préparer le dataset Taxi pour l’entraînement d’un modèle de régression ETA.
- Entraîner, évaluer et versionner un modèle de prédiction de durée de trajet.
- Exposer un endpoint `/predict` et des endpoints `/analytics` via une API FastAPI sécurisée (JWT).
- Orchestrer l’ensemble des étapes avec Apache Airflow (ingestion, nettoyage, ML, chargement BDD).

---

## 🏗️ Stack technique

- **Orchestration** : Apache Airflow (DAG Bronze → Silver → ML).
- **Traitement de données** : PySpark (nettoyage, features, préparation pour le ML).
- **Base de données** : PostgreSQL (zone Silver + logs de prédictions).
- **API** : FastAPI + authentification JWT (endpoints prédiction & analytics). 
- **Conteneurisation** : Docker & docker-compose (tous les services). 
- **Tests** : Pytest (API, modèle, fonctions utilitaires). 

---

## 📁 Structure du projet (exemple)

```bash
.

├── dags/
│     └── smart_logitrack_dag.py
│  
├── data/
│   ├── bronze/          # Données brutes
│   └── silver/          # Données nettoyées / features
├── models/
│   ├── taxi_duration_model/
│       ├── metadata/
│       └── stages/
├── spark/
│   ├── bronze_to_silver.ipynb
│   ├── utils.py
│   └── train_model.py
├── api/
│   ├── auth.py          # FastAPI app
│   ├── db.py
│   ├── main.py          # FastAPI app
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_predict.py
├── docker-compose.yml
├── init_airflow.sh
├── Dockerfile
├── requirements.txt
└── README.md


# Cloner le repo
git clone https://github.com/KarimaChami/Project-Smart-LogiTrack-
cd smart-logitrack

# Lancer l’infrastructure
docker-compose up -d --build

