from google.cloud import bigquery
import pandas as pd

PROJECT_ID = "project-be319738-ee9e-43d7-ada"
DATASET = "selections"


def upload_dataframe_to_bq(df, table_name):
    """Upload a DataFrame to BigQuery, replacing the existing table."""
    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=job_config,
    )

    job.result()
    print(f"Upload {table_name} concluído!")
