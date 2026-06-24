import requests
import pandas as pd
import os
import time

teams = {
    "Argentina": "ar",
    "Brazil": "br",
    "France": "fr",
    "England": "gb-eng",
    "Spain": "es",
    "Germany": "de",
    "Portugal": "pt",
    "Netherlands": "nl",
    "Italy": "it",
    "Belgium": "be",
    "Croatia": "hr",
    "Uruguay": "uy",
    "Colombia": "co",
    "Morocco": "ma",
    "Japan": "jp",
    "Mexico": "mx",
    "USA": "us",
    "Denmark": "dk",
    "Switzerland": "ch",
    "Austria": "at",
    "Serbia": "rs",
    "Ukraine": "ua",
    "Poland": "pl",
    "Sweden": "se",
    "Norway": "no",
    "South Korea": "kr",
    "Senegal": "sn",
    "Nigeria": "ng",
    "Ecuador": "ec"
}


def build_flag_url(country_code, base_url="https://flagcdn.com/w320"):
    return f"{base_url}/{country_code}.png"


def make_file_name(team_name):
    return team_name.lower().replace(" ", "_") + ".png"


def download_flag(url, output_path, timeout=30):
    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=timeout
    )
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def download_all_shields(teams_dict, output_dir="assets/shields", delay=1):
    os.makedirs(output_dir, exist_ok=True)
    rows = []

    for team, code in teams_dict.items():
        url = build_flag_url(code)
        try:
            file_name = make_file_name(team)
            path = os.path.join(output_dir, file_name)
            download_flag(url, path)
            rows.append({"team": team, "image_path": path})
            print(f"OK {team}")
            time.sleep(delay)
        except Exception as e:
            print(f"FAIL {team}: {e}")

    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = download_all_shields(teams)
    df.to_csv("assets/team_shields.csv", index=False)
    print("\nCSV criado com sucesso.")
