from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import random
from datetime import timedelta
from sqlalchemy import create_engine

def generate_activities():
    engine = create_engine("postgresql+psycopg2://user:password@postgres:5432/sportdb")

    ACTIVITES = ["marche", "vélo", "course", "yoga", "natation"]

    def generer_une_activite(id_salarie):
        type_activite = random.choice(ACTIVITES)
        distance = random.randint(1000, 10000)
        duree = random.randint(600, 3600)
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        return {
            "id_salarie": id_salarie,
            "date_debut": date.date(),
            "type": type_activite,
            "distance_m": distance,
            "duree_s": duree,
            "commentaire": ""
        }

    df_rh = pd.read_sql("SELECT id_salarie FROM rh WHERE sport_pratique_declare = TRUE", engine)

    activites = []
    for _, row in df_rh.iterrows():
        for _ in range(random.randint(5, 15)):
            activites.append(generer_une_activite(row["id_salarie"]))

    df = pd.DataFrame(activites)
    df.to_sql("activites", engine, if_exists="append", index=False)

with DAG(
    dag_id="generate_activities",
    description="Générer des activités sportives fictives pour les salariés",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["sport", "activities"]
) as dag:

    generate_activities_task = PythonOperator(
        task_id="generate_activities",
        python_callable=generate_activities
    )
