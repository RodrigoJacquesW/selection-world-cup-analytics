import json
import logging
import sys
import time

from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

try:
    with open("matches.json", "r") as f:
        matches = json.load(f)
except FileNotFoundError:
    logger.error("matches.json not found — run matches.py first.")
    sys.exit(1)
except json.JSONDecodeError as e:
    logger.error("matches.json contains invalid JSON: %s", e)
    sys.exit(1)

if not matches:
    logger.error("matches.json is empty — nothing to process.")
    sys.exit(1)

all_stats = []
api_errors = 0
parse_errors = 0

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.sofascore.com")

    for i, match in enumerate(matches):

        event_id = match["event_id"]

        url = f"https://www.sofascore.com/api/v1/event/{event_id}/statistics"

        logger.info(
            "%d/%d — Fetching stats for event %s",
            i + 1, len(matches), event_id
        )

        response = page.request.get(url)

        if response.status != 200:
            api_errors += 1
            logger.warning(
                "Non-200 response (%d) for event %s — skipping.",
                response.status, event_id
            )
            continue

        data = response.json()

        try:
            stats = data["statistics"][0]["groups"]
        except (KeyError, IndexError, TypeError) as e:
            parse_errors += 1
            logger.warning(
                "Unexpected stats structure for event %s: %s — skipping.",
                event_id, e
            )
            continue

        parsed_stats = {
            "event_id": event_id,
            "team": match["team"],
            "home_team": match["home_team"],
            "away_team": match["away_team"],
        }

        for group in stats:
            for item in group.get("statisticsItems", []):

                name = item.get("name")
                if name is None:
                    continue
                home = item.get("home")
                away = item.get("away")

                parsed_stats[f"{name}_home"] = home
                parsed_stats[f"{name}_away"] = away

        all_stats.append(parsed_stats)

        time.sleep(1)

    browser.close()

if api_errors:
    logger.warning("Total API errors: %d/%d", api_errors, len(matches))
if parse_errors:
    logger.warning("Total parse errors: %d/%d", parse_errors, len(matches))

if not all_stats:
    logger.error("No stats were collected — aborting.")
    sys.exit(1)

with open("match_stats.json", "w") as f:
    json.dump(all_stats, f, indent=2)

logger.info(
    "match_stats.json created with %d entries (%d matches total).",
    len(all_stats), len(matches)
)
