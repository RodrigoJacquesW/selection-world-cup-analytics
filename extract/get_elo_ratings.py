import sys
sys.path.append("..")

import pandas as pd
import requests

from shared.data_io import load_csv_as_df

url = "https://eloratings.net/World.tsv"

print("Baixando dados Elo...")

response = requests.get(url)

with open("elo_ratings.tsv", "wb") as f:
    f.write(response.content)

print("Arquivo baixado.")

# ler arquivo
df = load_csv_as_df("elo_ratings.tsv", sep="\t", header=None)

print("Formato detectado:", df.shape)

# extrair apenas colunas essenciais
df_clean = pd.DataFrame({
    "rank": df[0],
    "country_code": df[2],
    "elo_rating": df[3]
})

# salvar bruto
df_clean.to_csv(
    "elo_ratings_raw.csv",
    index=False
)

print("elo_ratings_raw.csv criado!")

# mostrar preview
print("\nPrimeiras linhas:")
print(df_clean.head(10))

print("\nUltimas linhas:")
print(df_clean.tail(10))
