from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

from src.main import parse_urls
from src.scrapper import get_top_ten_tags

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)}

with DAG("scrapper", start_date=datetime(2021, 1, 12),
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:
    get_top_ten_tags = PythonOperator(
        task_id='get_top_ten_tags',
        python_callable=get_top_ten_tags
    )
    parse_urls = PythonOperator(
        task_id='parse_urls',
        python_callable=parse_urls
    )


