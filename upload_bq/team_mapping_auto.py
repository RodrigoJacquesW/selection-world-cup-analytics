import sys
sys.path.append("..")

from shared.data_io import load_csv_as_df
from shared.bq_upload import upload_dataframe_to_bq

df = load_csv_as_df("team_mapping_auto.csv")

print("Linhas:", len(df))
print("Colunas:", len(df.columns))
print(df.head())

upload_dataframe_to_bq(df, "team_mapping_auto")
