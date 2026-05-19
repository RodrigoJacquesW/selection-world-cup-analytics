import json
import pandas as pd

# carregar matches
with open("matches.json") as f:
    matches = json.load(f)

df = pd.DataFrame(matches)

# pegar todos os times
teams = set(df["home_team"]) | set(df["away_team"])

teams = sorted(list(teams))

df_teams = pd.DataFrame({
    "team_name": teams
})

df_teams.to_csv(
    "teams_from_matches.csv",
    index=False
)

print("teams_from_matches.csv criado!")
print("Total times:", len(df_teams))
print(df_teams.head(30))