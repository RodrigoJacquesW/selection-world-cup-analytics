import sys
sys.path.append("..")

from shared.data_io import load_json_as_df
from shared.bq_upload import upload_dataframe_to_bq

df = load_json_as_df("matches.json")
upload_dataframe_to_bq(df, "matches")
