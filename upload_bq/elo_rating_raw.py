import logging
import sys

import pandas as pd
from google.cloud import bigquery

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

project_id = "project-be319738-ee9e-43d7-ada"

try:
    df = pd.read_csv("elo_ratings_raw.csv")
except FileNotFoundError:
    logger.error("elo_ratings_raw.csv not found — run get_elo_ratings.py first.")
    sys.exit(1)

if df.empty:
    logger.error("elo_ratings_raw.csv is empty — nothing to upload.")
    sys.exit(1)

logger.info("Rows: %d", len(df))
logger.info("Columns: %d", len(df.columns))
logger.info("\n%s", df.head())

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

if job.errors:
    logger.error("BigQuery load errors: %s", job.errors)
    sys.exit(1)

logger.info(
    "Upload elo_ratings_raw complete — %d rows loaded.", job.output_rows
)
