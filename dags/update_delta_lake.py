from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime
from docker.types import Mount

with DAG(
    dag_id="update_delta_lake",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    schedule_interval=None,
    is_paused_upon_creation=False,
) as dag:

    spark_job = DockerOperator(
        task_id="run_spark_job",
        image="custom-spark:delta",
        container_name="spark-job",
        api_version="auto",
        auto_remove=True,
        command="spark-submit /opt/spark-apps/spark_write_delta.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="container:p12-airflow-webserver-1",
        mounts=[
            Mount(source="C:/Users/Loic/Documents/p12/spark-jobs", target="/opt/spark-apps", type="bind"),
            Mount(source="C:/Users/Loic/Documents/p12/data", target="/opt/spark-data", type="bind"),
        ],
        mount_tmp_dir=False,
    )
