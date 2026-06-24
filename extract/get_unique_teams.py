import json
import pandas as pd


def load_matches(file_path):
    with open(file_path) as f:
        matches = json.load(f)
    return matches


def extract_unique_teams(matches):
    df = pd.DataFrame(matches)
    teams = set(df["home_team"]) | set(df["away_team"])
    return sorted(list(teams))


def build_teams_dataframe(team_names):
    return pd.DataFrame({"team_name": team_names})


def get_unique_teams(matches_path, output_path="teams_from_matches.csv"):
    matches = load_matches(matches_path)
    team_names = extract_unique_teams(matches)
    df_teams = build_teams_dataframe(team_names)

    df_teams.to_csv(output_path, index=False)

    return df_teams


if __name__ == "__main__":
    df_teams = get_unique_teams("matches.json")

    print("teams_from_matches.csv criado!")
    print("Total times:", len(df_teams))
    print(df_teams.head(30))
