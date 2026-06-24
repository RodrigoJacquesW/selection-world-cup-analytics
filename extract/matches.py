import json
import logging
import sys
import time

from playwright.sync_api import sync_playwright
from teams import teams

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


all_matches = []
parse_errors = 0

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.sofascore.com")

    for team_name, team_id in teams.items():

        logger.info("Fetching matches for %s", team_name)

        offset = 0

        while True:

            url = f"https://www.sofascore.com/api/v1/team/{team_id}/events/last/{offset}"

            response = page.request.get(url)

            if response.status != 200:
                logger.warning(
                    "Non-200 response (%d) for %s at offset %d — stopping pagination.",
                    response.status, team_name, offset
                )
                break

            data = response.json()
            events = data.get("events", [])

            if not events:
                break

            for event in events:

                try:

                    match_data = {

                        "team": team_name,
                        "event_id": event["id"],

                        "home_team": event["homeTeam"]["name"],
                        "away_team": event["awayTeam"]["name"],

                        "home_score": event["homeScore"]["current"],
                        "away_score": event["awayScore"]["current"],

                        "date": event["startTimestamp"],

                        "tournament": event["tournament"]["name"],

                        "season": event["season"]["name"],

                        "status": event["status"]["type"]

                    }

                    all_matches.append(match_data)

                except KeyError as e:
                    parse_errors += 1
                    logger.warning(
                        "Missing key %s in event %s for %s — skipping event.",
                        e, event.get("id", "unknown"), team_name
                    )

            offset += 20

            time.sleep(1)

    browser.close()

if parse_errors:
    logger.warning("Total events skipped due to parse errors: %d", parse_errors)

if not all_matches:
    logger.error("No matches were collected — aborting.")
    sys.exit(1)

# remover duplicados
unique_matches = {
    match["event_id"]: match
    for match in all_matches
}

all_matches = list(unique_matches.values())

logger.info("Collected %d unique matches.", len(all_matches))

with open("matches.json", "w") as f:
    json.dump(all_matches, f, indent=2)

logger.info("matches.json created.")
