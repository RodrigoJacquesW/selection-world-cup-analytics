import logging
import sys

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

try:
    teams = pd.read_csv("teams_from_matches.csv")
except FileNotFoundError:
    logger.error(
        "teams_from_matches.csv not found — run get_unique_teams.py first."
    )
    sys.exit(1)

try:
    elo = pd.read_csv("elo_ratings_raw.csv")
except FileNotFoundError:
    logger.error(
        "elo_ratings_raw.csv not found — run get_elo_ratings.py first."
    )
    sys.exit(1)

if "team_name" not in teams.columns:
    logger.error("teams_from_matches.csv missing 'team_name' column.")
    sys.exit(1)

# tabela ISO padrão manual mínima
iso_map = {

    "Albania": "AL",
    "Algeria": "DZ",
    "Andorra": "AD",
    "Angola": "AO",
    "Argentina": "AR",
    "Armenia": "AM",
    "Australia": "AU",
    "Austria": "AT",
    "Azerbaijan": "AZ",
    "Bahrain": "BH",
    "Belarus": "BY",
    "Belgium": "BE",
    "Benin": "BJ",
    "Bolivia": "BO",
    "Bosnia & Herzegovina": "BA",
    "Botswana": "BW",
    "Brazil": "BR",
    "Bulgaria": "BG",
    "Cameroon": "CM",
    "Canada": "CA",
    "Chile": "CL",
    "China": "CN",
    "Colombia": "CO",
    "Comoros": "KM",
    "Congo Republic": "CG",
    "Costa Rica": "CR",
    "Croatia": "HR",
    "Cyprus": "CY",
    "Czechia": "CZ",
    "Côte d'Ivoire": "CI",
    "DR Congo": "CD",
    "Denmark": "DK",
    "Dominican Republic": "DO",
    "Ecuador": "EC",
    "Egypt": "EG",
    "El Salvador": "SV",
    "England": "EN",
    "Estonia": "EE",
    "Faroe Islands": "FO",
    "Finland": "FI",
    "France": "FR",
    "Gabon": "GA",
    "Gambia": "GM",
    "Georgia": "GE",
    "Germany": "DE",
    "Ghana": "GH",
    "Gibraltar": "GI",
    "Greece": "GR",
    "Guatemala": "GT",
    "Guinea": "GN",
    "Haiti": "HT",
    "Honduras": "HN",
    "Hong Kong": "HK",
    "Hungary": "HU",
    "Iceland": "IS",
    "Indonesia": "ID",
    "Iran": "IR",
    "Iraq": "IQ",
    "Ireland": "IE",
    "Israel": "IL",
    "Italy": "IT",
    "Jamaica": "JM",
    "Japan": "JP",
    "Jordan": "JO",
    "Kazakhstan": "KZ",
    "Kenya": "KE",
    "Kosovo": "XK",
    "Kuwait": "KW",
    "Latvia": "LV",
    "Lesotho": "LS",
    "Liberia": "LR",
    "Libya": "LY",
    "Liechtenstein": "LI",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Madagascar": "MG",
    "Malaysia": "MY",
    "Mali": "ML",
    "Malta": "MT",
    "Mauritania": "MR",
    "Mexico": "MX",
    "Moldova": "MD",
    "Montenegro": "ME",
    "Morocco": "MA",
    "Mozambique": "MZ",
    "Myanmar": "MM",
    "Netherlands": "NL",
    "New Zealand": "NZ",
    "Niger": "NE",
    "Nigeria": "NG",
    "North Korea": "KP",
    "North Macedonia": "MK",
    "Northern Ireland": "NI",
    "Norway": "NO",
    "Oman": "OM",
    "Palestine": "PS",
    "Panama": "PA",
    "Paraguay": "PY",
    "Peru": "PE",
    "Poland": "PL",
    "Portugal": "PT",
    "Puerto Rico": "PR",
    "Romania": "RO",
    "Russia": "RU",
    "Rwanda": "RW",
    "San Marino": "SM",
    "Saudi Arabia": "SA",
    "Scotland": "SC",
    "Senegal": "SN",
    "Serbia": "RS",
    "Singapore": "SG",
    "Slovakia": "SK",
    "Slovenia": "SI",
    "South Africa": "ZA",
    "South Korea": "KR",
    "South Sudan": "SS",
    "Spain": "ES",
    "Sudan": "SD",
    "Suriname": "SR",
    "Sweden": "SE",
    "Switzerland": "CH",
    "Syria": "SY",
    "Tanzania": "TZ",
    "Thailand": "TH",
    "Togo": "TG",
    "Trinidad and Tobago": "TT",
    "Tunisia": "TN",
    "Türkiye": "TR",
    "USA": "US",
    "Uganda": "UG",
    "Ukraine": "UA",
    "United Arab Emirates": "AE",
    "Uruguay": "UY",
    "Uzbekistan": "UZ",
    "Venezuela": "VE",
    "Vietnam": "VN",
    "Wales": "WA",
    "Zambia": "ZM",
    "Zimbabwe": "ZW"
}

teams["country_code"] = teams["team_name"].map(iso_map)

teams = teams[
    ~teams["team_name"].isin([
        "Basque Country",
        "Internacional",
        "KS Lechia Gdańsk",
        "River Plate",
        "Valencia"
    ])
]

missing = teams[teams["country_code"].isna()]

if not missing.empty:
    logger.warning(
        "%d teams have no ISO mapping:\n%s",
        len(missing), missing["team_name"].tolist()
    )

teams.to_csv(
    "team_mapping_auto.csv",
    index=False
)

missing.to_csv(
    "team_mapping_missing.csv",
    index=False
)

logger.info("team_mapping_auto.csv created with %d teams.", len(teams))
logger.info("team_mapping_missing.csv created with %d teams.", len(missing))
