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
    with open("match_stats.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    logger.error("match_stats.json not found — run stats.py first.")
    sys.exit(1)
except json.JSONDecodeError as e:
    logger.error("match_stats.json contains invalid JSON: %s", e)
    sys.exit(1)

if not data:
    logger.error("match_stats.json is empty — nothing to upload.")
    sys.exit(1)

df = pd.DataFrame(data)

logger.info("Rows: %d", len(df))
logger.info("Columns: %d", len(df.columns))

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

if job.errors:
    logger.error("BigQuery load errors: %s", job.errors)
    sys.exit(1)

logger.info(
    "Upload match_stats complete — %d rows loaded.", job.output_rows
)
