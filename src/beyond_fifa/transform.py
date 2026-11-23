"""Run the Dataform project (definitions/) against the configured GCP project."""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from .config import ROOT_DIR, Settings


def run_dataform(settings: Settings) -> None:
    if shutil.which("dataform") is None:
        raise SystemExit(
            "Dataform CLI not found. Install it with: npm install -g @dataform/cli@3.0.38"
        )

    # The CLI requires a credentials file. Generating it from .env on every run keeps a
    # single source of truth for the project id. With no key inside, the CLI falls back
    # to Application Default Credentials (`gcloud auth application-default login`).
    with tempfile.TemporaryDirectory() as tmp:
        credentials = Path(tmp) / "df-credentials.json"
        credentials.write_text(
            json.dumps({"projectId": settings.gcp_project_id, "location": settings.bq_location})
        )
        subprocess.run(
            [
                "dataform", "run", str(ROOT_DIR),
                "--default-database", settings.gcp_project_id,
                "--default-location", settings.bq_location,
                "--credentials", str(credentials),
                "--vars", f"raw_dataset={settings.raw_dataset}",
            ],
            check=True,
        )
