"""Refresh the raw snapshot in data/raw/ from SofaScore and eloratings.net.

Only used with `python main.py --scrape`. The committed snapshot (collected in May 2026,
before the World Cup) is what the published ranking was built from, so a new scrape
answers a different question: it will pick up later matches.

SofaScore only answers its API from a browser session, hence Playwright.
eloratings.net may also block non-browser requests; download World.tsv manually if so.
"""

import json
import time

import pandas as pd
import requests

from .config import RAW_DIR, REFERENCE_DIR

SOFASCORE = "https://www.sofascore.com"
ELO_URL = "https://www.eloratings.net/World.tsv"


def _tracked_teams() -> dict[str, int]:
    df = pd.read_csv(REFERENCE_DIR / "teams.csv")
    return dict(zip(df["team"], df["sofascore_id"]))


def scrape_sofascore(pages_per_team: int = 3) -> None:
    from playwright.sync_api import sync_playwright

    matches: dict[int, dict] = {}
    stats: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SOFASCORE)

        for team, team_id in _tracked_teams().items():
            print(f"  matches: {team}")
            for offset in range(pages_per_team):
                r = page.request.get(f"{SOFASCORE}/api/v1/team/{team_id}/events/last/{offset}")
                events = r.json().get("events", []) if r.status == 200 else []
                if not events:
                    break
                for e in events:
                    matches[e["id"]] = {
                        "team": team,
                        "event_id": e["id"],
                        "home_team": e["homeTeam"]["name"],
                        "away_team": e["awayTeam"]["name"],
                        "home_score": e.get("homeScore", {}).get("current"),
                        "away_score": e.get("awayScore", {}).get("current"),
                        "date": e["startTimestamp"],
                        "tournament": e["tournament"]["name"],
                        "season": e.get("season", {}).get("name"),
                        "status": e["status"]["type"],
                    }
                time.sleep(1)

        for i, m in enumerate(matches.values(), 1):
            r = page.request.get(f"{SOFASCORE}/api/v1/event/{m['event_id']}/statistics")
            if r.status != 200:
                continue
            row = {k: m[k] for k in ("event_id", "team", "home_team", "away_team")}
            # "ALL" period = whole match
            for group in r.json()["statistics"][0]["groups"]:
                for item in group["statisticsItems"]:
                    row[f"{item['name']}_home"] = item.get("home")
                    row[f"{item['name']}_away"] = item.get("away")
            stats.append(row)
            if i % 50 == 0:
                print(f"  stats: {i}/{len(matches)}")
            time.sleep(1)

        browser.close()

    (RAW_DIR / "matches.json").write_text(json.dumps(list(matches.values()), indent=2))
    (RAW_DIR / "match_stats.json").write_text(json.dumps(stats, indent=2))
    print(f"  saved {len(matches)} matches, {len(stats)} with statistics")


def download_elo() -> None:
    r = requests.get(ELO_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    if r.text.lstrip().startswith("<"):
        raise SystemExit(
            f"eloratings.net returned an HTML page (bot protection). "
            f"Download {ELO_URL} in a browser and save it as data/raw/elo_ratings.tsv."
        )
    (RAW_DIR / "elo_ratings.tsv").write_bytes(r.content)
