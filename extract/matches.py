import sys
sys.path.append("..")

import time

from shared.browser import sofascore_browser
from shared.data_io import save_json
from shared.teams_config import TEAMS_SOFASCORE

all_matches = []

with sofascore_browser() as page:

    for team_name, team_id in TEAMS_SOFASCORE.items():

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

# remover duplicados
unique_matches = {
    match["event_id"]: match
    for match in all_matches
}

all_matches = list(unique_matches.values())

save_json(all_matches, "matches.json")
