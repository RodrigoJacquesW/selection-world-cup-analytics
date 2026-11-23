"""Load the snapshot (data/raw) and reference tables (data/reference) into BigQuery."""

import json
import re
from datetime import datetime, timezone

import pandas as pd
from google.cloud import bigquery

from .config import RAW_DIR, REFERENCE_DIR, Settings


def _snake(name: str) -> str:
    return re.sub(r"[^0-9a-z]+", "_", name.lower()).strip("_")


def _as_text(value) -> str | None:
    """12 -> "12" (not "12.0": columns with gaps become float in pandas)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def read_sources() -> dict[str, pd.DataFrame]:
    matches = pd.DataFrame(json.loads((RAW_DIR / "matches.json").read_text()))

    # SofaScore statistics come as one column per "<stat name>_<side>", with mixed
    # types ("55%", 12, "3/7"). Raw keeps them as text; staging does the casting.
    stats = pd.DataFrame(json.loads((RAW_DIR / "match_stats.json").read_text()))
    stats.columns = [_snake(c) for c in stats.columns]
    value_cols = [c for c in stats.columns if c not in ("event_id", "team", "home_team", "away_team")]
    stats[value_cols] = stats[value_cols].apply(lambda col: col.map(_as_text))

    # World.tsv has no header: column 2 is the team code, column 3 the rating.
    # keep_default_na=False matters: Namibia's code is "NA".
    elo = pd.read_csv(RAW_DIR / "elo_ratings.tsv", sep="\t", header=None, keep_default_na=False)
    elo = pd.DataFrame({"rank": elo[0], "elo_code": elo[2], "elo_rating": elo[3]})

    return {
        "matches": matches,
        "match_stats": stats,
        "elo_ratings": elo,
        "teams": pd.read_csv(REFERENCE_DIR / "teams.csv"),
        "elo_codes": pd.read_csv(REFERENCE_DIR / "elo_codes.csv", keep_default_na=False),
    }


def load_all(settings: Settings) -> None:
    client = bigquery.Client(project=settings.gcp_project_id, location=settings.bq_location)
    dataset = bigquery.Dataset(f"{settings.gcp_project_id}.{settings.raw_dataset}")
    dataset.location = settings.bq_location
    client.create_dataset(dataset, exists_ok=True)

    loaded_at = datetime.now(timezone.utc)
    for table, df in read_sources().items():
        df = df.assign(_loaded_at=loaded_at)
        client.load_table_from_dataframe(
            df,
            settings.table_id(table),
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"),
        ).result()
        print(f"  loaded {len(df):>4} rows -> {settings.table_id(table)}")
