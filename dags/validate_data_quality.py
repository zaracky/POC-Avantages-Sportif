from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess
import json
import os
import requests

SLACK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def run_soda_and_notify():
    result = subprocess.run(
        [
            "soda", "scan",
            "-d", "postgres",
            "-c", "/opt/airflow/soda/config.yml",
            "/opt/airflow/soda/checks.yml"
        ],
        capture_output=True,
        text=True
    )

    print("=== SODA OUTPUT START ===")
    print(result.stdout)
    print("=== SODA OUTPUT END ===")

    # Compter les échecs à partir du texte
    failed = "FAIL" in result.stdout.upper()
    warn = "WARN" in result.stdout.upper()

    if not failed and not warn:
        msg = " Vérification des données : tout est OK "
    elif failed:
        msg = " Des erreurs de qualité de données ont été détectées lors du scan."
    else:
        msg = " Des avertissements ont été détectés dans les données."

    # Slack
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if webhook:
        requests.post(webhook, json={"text": msg})
    else:
        print(" SLACK_WEBHOOK_URL non défini")


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="validate_data_quality",
    default_args=default_args,
    schedule_interval="@hourly",
    catchup=False,
    is_paused_upon_creation=False,
) as dag:
    validate_task = PythonOperator(
        task_id="validate_with_soda",
        python_callable=run_soda_and_notify
    )
