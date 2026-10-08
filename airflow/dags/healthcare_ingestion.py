from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="healthcare_ingestion",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    ingest_patients = BashOperator(
        task_id="ingest_patients",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.ingestion.ingest_patients"
        ),
    )

    ingest_doctors = BashOperator(
        task_id="ingest_doctors",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.ingestion.ingest_doctors"
        ),
    )

    ingest_hospitals = BashOperator(
        task_id="ingest_hospitals",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.ingestion.ingest_hospitals"
        ),
    )

    ingest_appointments = BashOperator(
        task_id="ingest_appointments",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.ingestion.ingest_appointments"
        ),
    )

    ingest_procedures = BashOperator(
        task_id="ingest_procedures",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.ingestion.ingest_procedures"
        ),
    )

    [
        ingest_patients,
        ingest_doctors,
        ingest_hospitals,
        ingest_appointments,
        ingest_procedures,
    ]