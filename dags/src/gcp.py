import logging

from google.cloud import storage
from google.cloud import bigquery

from dags.src.constants import service_acc_key_path, gcs_bucket_path


def create_bucket(bucket_name: str):
    try:
        storage_client = storage.Client.from_service_account_json(service_acc_key_path)
        new_bucket = storage_client.create_bucket(bucket_name)
        logging.info(f"Bucket with name {new_bucket.name} has been created")
    except:
        logging.info(f'Bucket with name {bucket_name} already exist')


def upload_to_cloud(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json(service_acc_key_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    logging.info("File {} uploaded to {}.".format(source_file_name, destination_blob_name))


def gcs_to_bq(file: str):
    """from cloud storage to bigquery"""
    client = bigquery.Client.from_service_account_json(service_acc_key_path)
    table_id = "testing.parser"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("tag", "STRING"),
            bigquery.SchemaField("author", "STRING"),
            bigquery.SchemaField("quote", "STRING"),
        ],
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
    )
    uri = gcs_bucket_path + file
    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    load_job.result()
    destination_table = client.get_table(table_id)
    logging.info("Loaded {} rows.".format(destination_table.num_rows))


if __name__ == '__main__':
    pass
