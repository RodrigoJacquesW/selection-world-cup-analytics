"""Download country flags (flagcdn.com) used by the Power BI report.

Output: assets/shields/<team>.png and assets/team_shields.csv (team -> image path).
"""

import time

import pandas as pd
import requests

from .config import REFERENCE_DIR, ROOT_DIR

OUTPUT_DIR = ROOT_DIR / "assets" / "shields"


def download_flags() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for team, code in pd.read_csv(REFERENCE_DIR / "teams.csv")[["team", "flag_code"]].itertuples(index=False):
        path = OUTPUT_DIR / f"{team.lower().replace(' ', '_')}.png"
        if not path.exists():
            r = requests.get(f"https://flagcdn.com/w320/{code}.png", timeout=30)
            r.raise_for_status()
            path.write_bytes(r.content)
            time.sleep(0.5)
        rows.append({"team": team, "image_path": path.relative_to(ROOT_DIR).as_posix()})
    pd.DataFrame(rows).to_csv(ROOT_DIR / "assets" / "team_shields.csv", index=False)
    print(f"  {len(rows)} flags in {OUTPUT_DIR.relative_to(ROOT_DIR)}")
