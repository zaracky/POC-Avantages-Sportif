from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Fonction exécutée par le DAG
def compute_indemnites():
    TARIF_KM = 0.25
    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/sportdb")

    query = """
        SELECT 
            e.id_salarie,
            r.nom,
            r.prenom,
            e.distance_totale_m / 1000.0 AS distance_km,
            e.nb_activites,
            e.duree_totale_s,
            e.est_eligible
        FROM eligibilite e
        JOIN rh r ON e.id_salarie = r.id_salarie
        WHERE e.est_eligible = TRUE
    """
    df = pd.read_sql(query, engine)
    df["montant_rembourse"] = df["distance_km"] * TARIF_KM
    df.to_sql("indemnites", engine, if_exists="replace", index=False)

# Définition du DAG
with DAG(
    dag_id="compute_indemnites",
    description="Calculer les indemnités pour les salariés éligibles",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["indemnites", "remboursement"]
) as dag:

    compute_task = PythonOperator(
        task_id="compute_indemnites",
        python_callable=compute_indemnites
    )
