# dags/ingest_bronze_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd   

print("DAG chargé !")
def test_function():
    print("Airflow is working correctly!")
with DAG(
    dag_id="test_airflow",
    start_date=datetime(2026, 1, 12),
    schedule_interval=None,
    catchup=False,
) as dag:
    test_task = PythonOperator(
        task_id="test_airflow_task",
        python_callable=test_function,
    )










# ---- Fonction Python ----
# def ingest_bronze():
#     """Lire le dataset brut et le sauvegarder comme Bronze"""

#     df = pd.read_parquet(DATASET_PATH)


#     os.makedirs(os.path.dirname(BRONZE_PATH), exist_ok=True)


#     df.to_parquet(BRONZE_PATH, index=False)
#     print(f"Dataset Bronze sauvegardé à {BRONZE_PATH}")


# task_ingest_bronze = PythonOperator(
#     task_id="ingest_bronze",
#     python_callable=ingest_bronze,
#     dag=dag,
# )


# task_ingest_bronze





#######################3

# def download_dataset():
#   # télécharger le fichier depuis le lien GDrive (ou l’ajouter déjà dans le projet)
#   pass

# def bronze_step():
#   # déplacer / copier le CSV brut dans un dossier "data/bronze"
#   pass

# def silver_step():
#   # lire le CSV avec PySpark, nettoyer, features, puis écrire en PostgreSQL
#   pass

# def train_model_step():
#   # lire la table Silver depuis PostgreSQL, entraîner un modèle, sauvegarder model.pkl
#   pass

# with DAG(
#   dag_id="taxi_eta_pipeline",
#   start_date=datetime(2024, 1, 1),
#   schedule_interval=None,
#   catchup=False,
# ) as dag:
#   t1 = PythonOperator(task_id="download_dataset", python_callable=download_dataset)
#   t2 = PythonOperator(task_id="bronze_step", python_callable=bronze_step)
#   t3 = PythonOperator(task_id="silver_step", python_callable=silver_step)
#   t4 = PythonOperator(task_id="train_model_step", python_callable=train_model_step)

#   t1 >> t2 >> t3 >> t4