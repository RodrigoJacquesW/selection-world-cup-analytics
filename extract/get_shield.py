import logging
import os
import sys
import time

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

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

output_dir = "assets/shields"
os.makedirs(output_dir, exist_ok=True)

rows = []
failed_teams = []

for team, code in teams.items():

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

        logger.info("Downloaded shield for %s", team)

        time.sleep(1)

    except requests.exceptions.Timeout:
        logger.error("Timeout downloading shield for %s from %s", team, url)
        failed_teams.append(team)
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error for %s: %s", team, e)
        failed_teams.append(team)
    except requests.exceptions.RequestException as e:
        logger.error("Request failed for %s: %s", team, e)
        failed_teams.append(team)
    except OSError as e:
        logger.error("Failed to write file for %s: %s", team, e)
        failed_teams.append(team)

if failed_teams:
    logger.warning(
        "%d/%d shields failed: %s",
        len(failed_teams), len(teams), failed_teams
    )

if not rows:
    logger.error("All shield downloads failed — aborting CSV creation.")
    sys.exit(1)

df = pd.DataFrame(rows)

df.to_csv(
    "assets/team_shields.csv",
    index=False
)

logger.info(
    "CSV created with %d/%d teams.", len(rows), len(teams)
)
