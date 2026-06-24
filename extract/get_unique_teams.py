import json
import logging
import sys

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

try:
    with open("matches.json") as f:
        matches = json.load(f)
except FileNotFoundError:
    logger.error("matches.json not found — run matches.py first.")
    sys.exit(1)
except json.JSONDecodeError as e:
    logger.error("matches.json contains invalid JSON: %s", e)
    sys.exit(1)

if not matches:
    logger.error("matches.json is empty — no matches to process.")
    sys.exit(1)

df = pd.DataFrame(matches)

for col in ("home_team", "away_team"):
    if col not in df.columns:
        logger.error("Missing expected column '%s' in matches data.", col)
        sys.exit(1)

teams = set(df["home_team"]) | set(df["away_team"])

teams = sorted(list(teams))

df_teams = pd.DataFrame({
    "team_name": teams
})

df_teams.to_csv(
    "teams_from_matches.csv",
    index=False
)

logger.info("teams_from_matches.csv created.")
logger.info("Total teams: %d", len(df_teams))
logger.info("\n%s", df_teams.head(30))
