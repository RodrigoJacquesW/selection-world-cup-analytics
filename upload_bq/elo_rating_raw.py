from google.cloud import bigquery
import pandas as pd

project_id = "project-be319738-ee9e-43d7-ada"

# ler CSV
df = pd.read_csv("elo_ratings_raw.csv")

print("Linhas:", len(df))
print("Colunas:", len(df.columns))
print(df.head())

client = bigquery.Client(project=project_id)

table_id = f"{project_id}.selections.elo_ratings_raw"

job_config = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE"
)

job = client.load_table_from_dataframe(
    df,
    table_id,
    job_config=job_config
)

job.result()

print("Upload elo_ratings_raw concluído!")