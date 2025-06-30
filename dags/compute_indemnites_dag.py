# === compute_indemnites_dag.py (modifié) ===
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
            a.id_salarie,
            r.nom,
            r.prenom,
            a.date_debut AS date_activite,
            a.type AS type_activite,
            a.distance_m,
            a.duree_s,
            a.commentaire,
            CASE 
                WHEN e.est_eligible THEN TRUE
                ELSE FALSE
            END AS est_eligible,
            CASE 
                WHEN e.est_eligible THEN ROUND((a.distance_m / 1000.0) * 0.25, 2)
                ELSE 0
            END AS montant_rembourse
        FROM activites a
        JOIN rh r ON a.id_salarie = r.id_salarie
        LEFT JOIN eligibilite e ON a.id_salarie = e.id_salarie
    """
    df = pd.read_sql(query, engine)
    df.to_sql("activites_detaillees", engine, if_exists="replace", index=False)

# Définition du DAG
with DAG(
    dag_id="compute_indemnites",
    description="Calcule les indemnités pour chaque activité des salariés",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
    tags=["indemnites", "remboursement"]
) as dag:

    compute_task = PythonOperator(
        task_id="compute_indemnites",
        python_callable=compute_indemnites
    )