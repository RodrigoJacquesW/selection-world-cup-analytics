import sys
sys.path.append("..")

import os
import time

import pandas as pd
import requests

from shared.teams_config import TEAMS_FLAG_CODES

# pasta output
output_dir = "assets/shields"
os.makedirs(output_dir, exist_ok=True)

rows = []

for team, code in TEAMS_FLAG_CODES.items():

    # bandeiras PNG prontas
    url = f"https://flagcdn.com/w320/{code}.png"

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        response.raise_for_status()

        file_name = (
            team.lower()
            .replace(" ", "_") + ".png"
        )

        path = os.path.join(output_dir, file_name)

        with open(path, "wb") as f:
            f.write(response.content)

        rows.append({
            "team": team,
            "image_path": path
        })

        print(f"OK {team}")

        time.sleep(1)

    except Exception as e:
        print(f"FAIL {team}: {e}")

# csv para o power bi
df = pd.DataFrame(rows)

df.to_csv(
    "assets/team_shields.csv",
    index=False
)

print("\nCSV criado com sucesso.")
