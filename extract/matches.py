from playwright.sync_api import sync_playwright
from teams import teams
import json
import time


all_matches = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.sofascore.com")

    for team_name, team_id in teams.items():

        print(f"\nPegando jogos de {team_name}")

        offset = 0

        while True:

            url = f"https://www.sofascore.com/api/v1/team/{team_id}/events/last/{offset}"

            response = page.request.get(url)

            if response.status != 200:
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

                except Exception as e:
                    print("Erro:", e)

            offset += 20

            time.sleep(1)

    browser.close()

# remover duplicados
unique_matches = {
    match["event_id"]: match
    for match in all_matches
}

all_matches = list(unique_matches.values())

with open("matches.json", "w") as f:
    json.dump(all_matches, f, indent=2)