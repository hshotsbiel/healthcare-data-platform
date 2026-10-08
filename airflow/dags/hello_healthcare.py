from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def hello_healthcare():
    print("Healthcare Data Platform funcionando!")


with DAG(
    dag_id="hello_healthcare",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=hello_healthcare,
    )