import requests
import pandas as pd
import os
import time

teams = {
    "Argentina": "ar",
    "Brazil": "br",
    "France": "fr",
    "England": "gb-eng",
    "Spain": "es",
    "Germany": "de",
    "Portugal": "pt",
    "Netherlands": "nl",
    "Italy": "it",
    "Belgium": "be",
    "Croatia": "hr",
    "Uruguay": "uy",
    "Colombia": "co",
    "Morocco": "ma",
    "Japan": "jp",
    "Mexico": "mx",
    "USA": "us",
    "Denmark": "dk",
    "Switzerland": "ch",
    "Austria": "at",
    "Serbia": "rs",
    "Ukraine": "ua",
    "Poland": "pl",
    "Sweden": "se",
    "Norway": "no",
    "South Korea": "kr",
    "Senegal": "sn",
    "Nigeria": "ng",
    "Ecuador": "ec"
}

# pasta output
output_dir = "assets/shields"
os.makedirs(output_dir, exist_ok=True)

rows = []

for team, code in teams.items():

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

        print(f"✅ {team}")

        time.sleep(1)

    except Exception as e:
        print(f"❌ {team}: {e}")

# csv para o power bi
df = pd.DataFrame(rows)

df.to_csv(
    "assets/team_shields.csv",
    index=False
)

print("\nCSV criado com sucesso.")