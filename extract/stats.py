import sys
sys.path.append("..")

import time

from shared.browser import sofascore_browser
from shared.data_io import load_json, save_json

# carregar matches
matches = load_json("matches.json")

all_stats = []

with sofascore_browser() as page:

    for i, match in enumerate(matches):

        event_id = match["event_id"]

        url = f"https://www.sofascore.com/api/v1/event/{event_id}/statistics"

        print(f"{i+1}/{len(matches)} - Pegando stats do jogo {event_id}")

        response = page.request.get(url)

        if response.status != 200:
            print("Erro:", response.status)
            continue

        data = response.json()

        try:
            stats = data["statistics"][0]["groups"]

            parsed_stats = {
                "event_id": event_id,
                "team": match["team"],
                "home_team": match["home_team"],
                "away_team": match["away_team"],
            }

            # extrair stats principais
            for group in stats:
                for item in group["statisticsItems"]:

                    name = item["name"]
                    home = item.get("home")
                    away = item.get("away")

                    parsed_stats[f"{name}_home"] = home
                    parsed_stats[f"{name}_away"] = away

            all_stats.append(parsed_stats)

        except Exception as e:
            print("Erro ao parsear:", e)

        time.sleep(1)

# salvar
save_json(all_stats, "match_stats.json")

print("Arquivo match_stats.json criado!")
