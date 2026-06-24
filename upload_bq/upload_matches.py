import json
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
    with open("matches.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error("matches.json not found — run matches.py first.")
    sys.exit(1)
except json.JSONDecodeError as e:
    logger.error("matches.json contains invalid JSON: %s", e)
    sys.exit(1)

if not data:
    logger.error("matches.json is empty — nothing to upload.")
    sys.exit(1)

df = pd.DataFrame(data)

logger.info("Rows: %d", len(df))
logger.info("Columns: %d", len(df.columns))

client = bigquery.Client(project=project_id)

table_id = f"{project_id}.selections.matches"

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
    "Upload matches complete — %d rows loaded.", job.output_rows
)
