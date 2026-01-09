# dags/ingest_bronze_dag.py
from datetime import datetime ,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import os

# ---- Configuration ----
DAG_ID = "ingest_bronze_taxi"
DATASET_PATH = "/opt/airflow/data/dataset.parquet"
BRONZE_PATH = "/opt/airflow/data/bronze_taxi.parquet"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 3),
    "retries": 1,
}

dag = DAG(
    DAG_ID,
    default_args=default_args,
    description="Ingestion dataset NYC Taxi et stockage Bronze",
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)

# ---- Fonction Python ----
def ingest_bronze():
    """Lire le dataset brut et le sauvegarder comme Bronze"""

    df = pd.read_parquet(DATASET_PATH)


    os.makedirs(os.path.dirname(BRONZE_PATH), exist_ok=True)


    df.to_parquet(BRONZE_PATH, index=False)
    print(f"Dataset Bronze sauvegardé à {BRONZE_PATH}")


task_ingest_bronze = PythonOperator(
    task_id="ingest_bronze",
    python_callable=ingest_bronze,
    dag=dag,
)


task_ingest_bronze





#######################3

def download_dataset():
  # télécharger le fichier depuis le lien GDrive (ou l’ajouter déjà dans le projet)
  pass

def bronze_step():
  # déplacer / copier le CSV brut dans un dossier "data/bronze"
  pass

def silver_step():
  # lire le CSV avec PySpark, nettoyer, features, puis écrire en PostgreSQL
  pass

def train_model_step():
  # lire la table Silver depuis PostgreSQL, entraîner un modèle, sauvegarder model.pkl
  pass

with DAG(
  dag_id="taxi_eta_pipeline",
  start_date=datetime(2024, 1, 1),
  schedule_interval=None,
  catchup=False,
) as dag:
  t1 = PythonOperator(task_id="download_dataset", python_callable=download_dataset)
  t2 = PythonOperator(task_id="bronze_step", python_callable=bronze_step)
  t3 = PythonOperator(task_id="silver_step", python_callable=silver_step)
  t4 = PythonOperator(task_id="train_model_step", python_callable=train_model_step)

  t1 >> t2 >> t3 >> t4