from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import random

ACTIVITES = ["marche", "vélo", "course", "yoga", "natation"]

def generer_activites():
    conn = psycopg2.connect(
        host="postgres",
        database="sportdb",
        user="user",
        password="password"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT id_salarie FROM rh")
    salaries = cursor.fetchall()

    if not salaries:
        print("⚠️ Aucun salarié trouvé dans la table rh.")
        return

    for _ in range(300):
        id_salarie = random.choice(salaries)[0]
        date_debut = datetime.now() - timedelta(days=random.randint(0, 365))
        type_activite = random.choice(ACTIVITES)
        distance_m = random.randint(1000, 15000)
        duree_s = random.randint(600, 7200)
        commentaire = random.choice([
            "Super sortie !", "Belle perf", "Reprise du sport :)",
            "Jambes lourdes", "Top météo aujourd’hui", ""
        ])

        cursor.execute(
            """
            INSERT INTO activites (
                id_salarie, date_debut, type, distance_m, duree_s, commentaire, source
            ) VALUES (%s, %s, %s, %s, %s, %s, 'auto')
            """,
            (id_salarie, date_debut, type_activite, distance_m, duree_s, commentaire)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(" Activités générées automatiquement.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='generate_activities',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    is_paused_upon_creation=False,
) as dag:
    generate = PythonOperator(
        task_id='generate_activities',
        python_callable=generer_activites
    )
