import logging
import sys

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

url = "https://eloratings.net/World.tsv"

logger.info("Downloading Elo ratings from %s", url)

response = requests.get(url, timeout=30)
response.raise_for_status()

if not response.content:
    logger.error("Empty response from %s", url)
    sys.exit(1)

with open("elo_ratings.tsv", "wb") as f:
    f.write(response.content)

logger.info("File downloaded.")

df = pd.read_csv(
    "elo_ratings.tsv",
    sep="\t",
    header=None
)

logger.info("Detected shape: %s", df.shape)

expected_columns = {0, 2, 3}
if not expected_columns.issubset(set(df.columns)):
    logger.error(
        "TSV missing expected columns %s; got %s",
        expected_columns, list(df.columns)
    )
    sys.exit(1)

df_clean = pd.DataFrame({
    "rank": df[0],
    "country_code": df[2],
    "elo_rating": df[3]
})

if df_clean.empty:
    logger.error("Parsed DataFrame is empty — aborting.")
    sys.exit(1)

df_clean.to_csv(
    "elo_ratings_raw.csv",
    index=False
)

logger.info("elo_ratings_raw.csv created with %d rows.", len(df_clean))
logger.info("First rows:\n%s", df_clean.head(10))
logger.info("Last rows:\n%s", df_clean.tail(10))
