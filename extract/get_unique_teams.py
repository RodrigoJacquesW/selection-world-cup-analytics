import sys
sys.path.append("..")

import pandas as pd

from shared.data_io import load_json_as_df

df = load_json_as_df("matches.json")

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
