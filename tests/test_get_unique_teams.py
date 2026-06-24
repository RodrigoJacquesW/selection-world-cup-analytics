import json
import os

import pandas as pd
import pytest

from extract.get_unique_teams import (
    build_teams_dataframe,
    extract_unique_teams,
    get_unique_teams,
    load_matches,
)


@pytest.fixture
def sample_matches():
    return [
        {"home_team": "Brazil", "away_team": "Argentina", "event_id": 1},
        {"home_team": "France", "away_team": "Germany", "event_id": 2},
        {"home_team": "Brazil", "away_team": "France", "event_id": 3},
    ]


@pytest.fixture
def sample_matches_file(sample_matches, tmp_path):
    path = tmp_path / "matches.json"
    path.write_text(json.dumps(sample_matches))
    return str(path)


class TestLoadMatches:
    def test_loads_json_correctly(self, sample_matches_file, sample_matches):
        result = load_matches(sample_matches_file)
        assert len(result) == 3
        assert result[0]["home_team"] == "Brazil"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_matches("/nonexistent/matches.json")

    def test_empty_list(self, tmp_path):
        path = tmp_path / "empty.json"
        path.write_text("[]")
        result = load_matches(str(path))
        assert result == []


class TestExtractUniqueTeams:
    def test_deduplicates_teams(self, sample_matches):
        result = extract_unique_teams(sample_matches)
        assert len(result) == 4
        assert "Brazil" in result
        assert "Argentina" in result
        assert "France" in result
        assert "Germany" in result

    def test_returns_sorted(self, sample_matches):
        result = extract_unique_teams(sample_matches)
        assert result == sorted(result)

    def test_single_match(self):
        matches = [{"home_team": "A", "away_team": "B", "event_id": 1}]
        result = extract_unique_teams(matches)
        assert result == ["A", "B"]

    def test_same_team_both_sides(self):
        matches = [
            {"home_team": "Brazil", "away_team": "Argentina", "event_id": 1},
            {"home_team": "Argentina", "away_team": "Brazil", "event_id": 2},
        ]
        result = extract_unique_teams(matches)
        assert len(result) == 2


class TestBuildTeamsDataframe:
    def test_creates_correct_dataframe(self):
        names = ["Argentina", "Brazil", "France"]
        result = build_teams_dataframe(names)
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["team_name"]
        assert len(result) == 3
        assert list(result["team_name"]) == names

    def test_empty_list(self):
        result = build_teams_dataframe([])
        assert len(result) == 0
        assert "team_name" in result.columns

    def test_single_team(self):
        result = build_teams_dataframe(["Brazil"])
        assert len(result) == 1


class TestGetUniqueTeams:
    def test_full_pipeline(self, sample_matches_file, tmp_path):
        output = str(tmp_path / "output.csv")
        result = get_unique_teams(sample_matches_file, output_path=output)

        assert len(result) == 4
        assert os.path.exists(output)

        saved = pd.read_csv(output)
        assert len(saved) == 4
        assert "team_name" in saved.columns
