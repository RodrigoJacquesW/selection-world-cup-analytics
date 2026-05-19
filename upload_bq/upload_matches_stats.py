from google.cloud import bigquery
import pandas as pd
import json

project_id = "project-be319738-ee9e-43d7-ada"

# abrir json
with open("match_stats.json", "r") as f:
    data = json.load(f)

# dataframe
df = pd.DataFrame(data)

print("Linhas:", len(df))
print("Colunas:", len(df.columns))

client = bigquery.Client(project=project_id)

table_id = f"{project_id}.selections.match_stats"

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE"
)

job = client.load_table_from_dataframe(
    df,
    table_id,
    job_config=job_config
)

job.result()

print("Upload match_stats concluído!")