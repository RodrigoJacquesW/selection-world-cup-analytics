from google.cloud import bigquery
import pandas as pd
import json
import os


project_id = os.environ["GCP_PROJECT_ID"]


with open("matches.json", "r") as f:
    data = json.load(f)


df = pd.DataFrame(data)


client = bigquery.Client(project=project_id)

table_id = f"{project_id}.selections.matches"

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE"  # recria tabela
)


job = client.load_table_from_dataframe(
    df,
    table_id,
    job_config=job_config
)

job.result()

print("Upload concluído!")