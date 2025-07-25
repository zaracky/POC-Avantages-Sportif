from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

#  Tâche de chargement du CSV dans PostgreSQL
def load_csv():
    file_path = "/opt/airflow/data/donnees_rh_enrichies.csv"
    df = pd.read_csv(file_path)
    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/sportdb")
    df.to_sql("rh", engine, if_exists="append", index=False)

#  Définition du DAG
with DAG(
    dag_id="load_rh_csv",
    description="Charge les données RH dans PostgreSQL et déclenche les étapes suivantes",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@once",
    catchup=False,
    is_paused_upon_creation=False,
    tags=["etl", "rh"]
) as dag:

    load_task = PythonOperator(
        task_id="load_csv",
        python_callable=load_csv
    )

    trigger_activities = TriggerDagRunOperator(
        task_id='trigger_generate_activities',
        trigger_dag_id='generate_activities'
    )

    # Enchaînement des DAGs
    load_task >> trigger_activities 
