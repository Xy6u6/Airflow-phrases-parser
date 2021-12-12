import logging

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

from src.main import parse_urls, upload_files_to_cloud
from src.scrapper import get_top_ten_tags, write_phrases_to_file


def get_dict_of_qoutes(ti):
    list_of_urls = ti.xcom_pull(task_ids='get_top_ten_tags', key='return_value')
    dict_of_quotes = parse_urls(list_of_urls)
    logging.info(f'got dict of quotes{type(dict_of_quotes)}, details: {dict_of_quotes}')
    ti.xcom_push(key='dict_of_quotes', value=dict_of_quotes)


def phrases_to_files(ti):
    dict_of_quotes = ti.xcom_pull(key='dict_of_quotes', task_ids='parse_urls')
    write_phrases_to_file(dict_of_quotes, 'csv')


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
    parse_my_urls = PythonOperator(
        task_id='parse_urls',
        python_callable=get_dict_of_qoutes
    )
    write_to_files = PythonOperator(
        task_id='phrases_to_files',
        python_callable=phrases_to_files
    )
    upload = PythonOperator(
        task_id='upload_to_gcs',
        python_callable=upload_files_to_cloud
    )
get_top_ten_tags >> parse_my_urls >> write_to_files >> upload