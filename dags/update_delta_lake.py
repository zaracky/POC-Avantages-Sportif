from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0,
}

with DAG(
    dag_id='update_delta_lake_parquet',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='Ingestion PostgreSQL, puis export Parquet pour Power BI',
) as dag:

    run_spark_job = DockerOperator(
        task_id='run_spark_job',
        image='custom-spark:delta',
        api_version='auto',
        auto_remove=True,
        command='spark-submit /opt/spark-apps/spark_write_delta.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='p12_airflow_net',
        mount_tmp_dir=False,
        mounts=[
            Mount(source="C:/Users/Loic/Documents/p12/spark-jobs", target="/opt/spark-apps", type="bind"),
            Mount(source="C:/Users/Loic/Documents/p12/data", target="/opt/spark-data", type="bind"),
        ],
    )

    export_parquet = DockerOperator(
        task_id='export_to_parquet',
        image='custom-spark:delta',
        api_version='auto',
        auto_remove=True,
        command='spark-submit /opt/spark-apps/spark_export_parquet.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='p12_airflow_net',
        mount_tmp_dir=False,
        mounts=[
            Mount(source="C:/Users/Loic/Documents/p12/spark-jobs", target="/opt/spark-apps", type="bind"),
            Mount(source="C:/Users/Loic/Documents/p12/data", target="/opt/spark-data", type="bind"),
        ],
    )

    run_spark_job >> export_parquet
