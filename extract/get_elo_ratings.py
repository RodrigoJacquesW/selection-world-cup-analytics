import requests
import pandas as pd


def download_elo_file(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)
    return output_path


def parse_elo_tsv(file_path):
    df = pd.read_csv(
        file_path,
        sep="\t",
        header=None
    )
    return df


def extract_elo_columns(df):
    df_clean = pd.DataFrame({
        "rank": df[0],
        "country_code": df[2],
        "elo_rating": df[3]
    })
    return df_clean


def get_elo_ratings(url, tsv_path="elo_ratings.tsv", csv_path="elo_ratings_raw.csv"):
    print("Baixando dados Elo...")
    download_elo_file(url, tsv_path)
    print("Arquivo baixado.")

    df = parse_elo_tsv(tsv_path)
    print("Formato detectado:", df.shape)

    df_clean = extract_elo_columns(df)

    df_clean.to_csv(csv_path, index=False)
    print(f"{csv_path} criado!")

    return df_clean


if __name__ == "__main__":
    url = "https://eloratings.net/World.tsv"
    df_clean = get_elo_ratings(url)

    print("\nPrimeiras linhas:")
    print(df_clean.head(10))

    print("\nUltimas linhas:")
    print(df_clean.tail(10))
