"""Runtime configuration, read from environment variables (or a local .env file)."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
REFERENCE_DIR = ROOT_DIR / "data" / "reference"

load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    gcp_project_id: str
    bq_location: str
    raw_dataset: str

    def table_id(self, table: str) -> str:
        return f"{self.gcp_project_id}.{self.raw_dataset}.{table}"


def get_settings() -> Settings:
    project = os.getenv("GCP_PROJECT_ID")
    if not project:
        raise SystemExit(
            "GCP_PROJECT_ID is not set. Copy .env.example to .env and fill in your project id."
        )
    return Settings(
        gcp_project_id=project,
        bq_location=os.getenv("BQ_LOCATION", "US"),
        raw_dataset=os.getenv("BQ_RAW_DATASET", "selections_raw"),
    )
