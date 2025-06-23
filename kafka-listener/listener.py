import os
import json
import requests
from kafka import KafkaConsumer
from kafka_notify_slack import envoyer_message_slack

topic = os.getenv("KAFKA_TOPIC")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
airflow_api = os.getenv("AIRFLOW_API")
user = os.getenv("AIRFLOW_USER")
pwd = os.getenv("AIRFLOW_PASSWORD")

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def trigger_dag(dag_id):
    url = f"{airflow_api}/{dag_id}/dagRuns"
    try:
        r = requests.post(url, auth=(user, pwd), json={})
        print(f" DAG {dag_id} déclenché : {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f" Impossible de déclencher le DAG {dag_id} : {e}")

for msg in consumer:
    print(" Changement détecté dans activites.")
    payload = msg.value.get("payload", {}).get("after", {})
    
    #  Ignore les données générées automatiquement
    if payload.get("source") == "auto":
        print(" Activité ignorée (source = auto)")
        continue

    envoyer_message_slack(msg.value)
    trigger_dag("generate_eligibilite")
    trigger_dag("compute_indemnites")
