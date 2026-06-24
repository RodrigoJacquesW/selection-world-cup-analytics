import pandas as pd
import pytest

from transform.build_team_mapping import (
    EXCLUDED_TEAMS,
    build_team_mapping,
    filter_excluded_teams,
    find_missing_mappings,
    iso_map,
    map_country_codes,
)


@pytest.fixture
def sample_teams_df():
    return pd.DataFrame({
        "team_name": ["Brazil", "Argentina", "France", "England", "Unknown FC"]
    })


@pytest.fixture
def excluded_teams_df():
    return pd.DataFrame({
        "team_name": [
            "Brazil",
            "Basque Country",
            "Internacional",
            "River Plate",
            "Argentina",
        ]
    })


class TestMapCountryCodes:
    def test_known_teams_get_mapped(self, sample_teams_df):
        result = map_country_codes(sample_teams_df)
        assert result.loc[result["team_name"] == "Brazil", "country_code"].iloc[0] == "BR"
        assert result.loc[result["team_name"] == "Argentina", "country_code"].iloc[0] == "AR"
        assert result.loc[result["team_name"] == "France", "country_code"].iloc[0] == "FR"
        assert result.loc[result["team_name"] == "England", "country_code"].iloc[0] == "EN"

    def test_unknown_team_gets_nan(self, sample_teams_df):
        result = map_country_codes(sample_teams_df)
        assert pd.isna(result.loc[result["team_name"] == "Unknown FC", "country_code"].iloc[0])

    def test_custom_mapping(self, sample_teams_df):
        custom = {"Brazil": "XX", "Argentina": "YY"}
        result = map_country_codes(sample_teams_df, mapping=custom)
        assert result.loc[result["team_name"] == "Brazil", "country_code"].iloc[0] == "XX"
        assert result.loc[result["team_name"] == "Argentina", "country_code"].iloc[0] == "YY"
        assert pd.isna(result.loc[result["team_name"] == "France", "country_code"].iloc[0])

    def test_does_not_mutate_input(self, sample_teams_df):
        original_cols = list(sample_teams_df.columns)
        map_country_codes(sample_teams_df)
        assert list(sample_teams_df.columns) == original_cols
        assert "country_code" not in sample_teams_df.columns

    def test_empty_dataframe(self):
        df = pd.DataFrame({"team_name": []})
        result = map_country_codes(df)
        assert len(result) == 0
        assert "country_code" in result.columns


class TestFilterExcludedTeams:
    def test_default_exclusions(self, excluded_teams_df):
        result = filter_excluded_teams(excluded_teams_df)
        assert "Basque Country" not in result["team_name"].values
        assert "Internacional" not in result["team_name"].values
        assert "River Plate" not in result["team_name"].values
        assert "Brazil" in result["team_name"].values
        assert "Argentina" in result["team_name"].values

    def test_custom_exclusions(self, excluded_teams_df):
        result = filter_excluded_teams(excluded_teams_df, excluded=["Brazil"])
        assert "Brazil" not in result["team_name"].values
        assert "Argentina" in result["team_name"].values
        assert "Basque Country" in result["team_name"].values

    def test_empty_exclusion_list(self, excluded_teams_df):
        result = filter_excluded_teams(excluded_teams_df, excluded=[])
        assert len(result) == len(excluded_teams_df)

    def test_does_not_mutate_input(self, excluded_teams_df):
        original_len = len(excluded_teams_df)
        filter_excluded_teams(excluded_teams_df)
        assert len(excluded_teams_df) == original_len


class TestFindMissingMappings:
    def test_identifies_missing_codes(self):
        df = pd.DataFrame({
            "team_name": ["Brazil", "Unknown", "France"],
            "country_code": ["BR", None, "FR"]
        })
        result = find_missing_mappings(df)
        assert len(result) == 1
        assert result.iloc[0]["team_name"] == "Unknown"

    def test_no_missing(self):
        df = pd.DataFrame({
            "team_name": ["Brazil", "France"],
            "country_code": ["BR", "FR"]
        })
        result = find_missing_mappings(df)
        assert len(result) == 0

    def test_all_missing(self):
        df = pd.DataFrame({
            "team_name": ["X", "Y"],
            "country_code": [None, None]
        })
        result = find_missing_mappings(df)
        assert len(result) == 2


class TestBuildTeamMapping:
    def test_full_pipeline(self):
        df = pd.DataFrame({
            "team_name": [
                "Brazil", "Argentina", "Unknown FC",
                "Basque Country", "River Plate"
            ]
        })
        result, missing = build_team_mapping(df)
        assert "Basque Country" not in result["team_name"].values
        assert "River Plate" not in result["team_name"].values
        assert "Brazil" in result["team_name"].values
        assert result.loc[result["team_name"] == "Brazil", "country_code"].iloc[0] == "BR"
        assert len(missing) == 1
        assert missing.iloc[0]["team_name"] == "Unknown FC"

    def test_all_known_teams(self):
        df = pd.DataFrame({"team_name": ["Brazil", "Argentina", "France"]})
        result, missing = build_team_mapping(df)
        assert len(missing) == 0
        assert len(result) == 3

    def test_empty_input(self):
        df = pd.DataFrame({"team_name": []})
        result, missing = build_team_mapping(df)
        assert len(result) == 0
        assert len(missing) == 0


class TestIsoMapIntegrity:
    def test_all_codes_are_two_chars(self):
        for team, code in iso_map.items():
            assert len(code) == 2, f"{team} has code '{code}' (expected 2 chars)"

    def test_all_codes_are_uppercase(self):
        for team, code in iso_map.items():
            assert code == code.upper(), f"{team} has non-uppercase code '{code}'"

    def test_no_duplicate_codes(self):
        codes = list(iso_map.values())
        assert len(codes) == len(set(codes)), "Duplicate country codes found"

    def test_expected_teams_present(self):
        expected = ["Brazil", "Argentina", "France", "Germany", "Spain",
                    "England", "Italy", "Netherlands", "Portugal", "Japan"]
        for team in expected:
            assert team in iso_map, f"{team} missing from iso_map"


class TestExcludedTeams:
    def test_excluded_list_has_expected_entries(self):
        assert "Basque Country" in EXCLUDED_TEAMS
        assert "Internacional" in EXCLUDED_TEAMS
        assert "Valencia" in EXCLUDED_TEAMS

    def test_no_national_teams_excluded(self):
        for team in EXCLUDED_TEAMS:
            assert team not in iso_map, f"{team} is in iso_map but also excluded"
