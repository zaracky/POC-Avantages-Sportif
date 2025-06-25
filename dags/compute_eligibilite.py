from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

def generate_eligibilite():
    # Connexion à PostgreSQL
    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/sportdb")

    # Tous les salariés
    df_salaries = pd.read_sql("SELECT id_salarie FROM rh", engine)

    # Activités (si table vide, retourne un DataFrame vide)
    df_activites = pd.read_sql("SELECT * FROM activites", engine)

    # Agrégation
    df_agg = df_activites.groupby("id_salarie").agg(
        nb_activites=pd.NamedAgg(column="id_salarie", aggfunc="count"),
        distance_totale_m=pd.NamedAgg(column="distance_m", aggfunc="sum"),
        duree_totale_s=pd.NamedAgg(column="duree_s", aggfunc="sum")
    ).reset_index()

    # Jointure RH pour inclure tous les salariés
    df_elig = df_salaries.merge(df_agg, on="id_salarie", how="left").fillna(0)

    # Règle d’éligibilité
    df_elig["est_eligible"] = (
        (df_elig["nb_activites"] >= 10) &
        (df_elig["distance_totale_m"] >= 20000) &
        (df_elig["duree_totale_s"] >= 7200)
    )

    df_elig.to_sql("eligibilite", engine, if_exists="replace", index=False)
    print(f"✅ {len(df_elig)} lignes insérées dans eligibilite")

# Définir le DAG
with DAG(
    dag_id="generate_eligibilite",
    description="Génère la table d'éligibilité pour les salariés sportifs",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,  # désactivé pour démarrage manuel
    catchup=False,
    is_paused_upon_creation=False,
    tags=["etl", "eligibilite"]
) as dag:

    generate_eligibilite_task = PythonOperator(
        task_id="generate_eligibilite_task",
        python_callable=generate_eligibilite
    )
