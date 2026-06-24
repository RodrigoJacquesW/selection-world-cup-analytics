import os

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from extract.get_shield import (
    build_flag_url,
    download_all_shields,
    download_flag,
    make_file_name,
    teams,
)


class TestBuildFlagUrl:
    def test_default_base_url(self):
        result = build_flag_url("br")
        assert result == "https://flagcdn.com/w320/br.png"

    def test_custom_base_url(self):
        result = build_flag_url("ar", base_url="https://custom.cdn/flags")
        assert result == "https://custom.cdn/flags/ar.png"

    def test_england_code(self):
        result = build_flag_url("gb-eng")
        assert result == "https://flagcdn.com/w320/gb-eng.png"


class TestMakeFileName:
    def test_simple_name(self):
        assert make_file_name("Brazil") == "brazil.png"

    def test_name_with_space(self):
        assert make_file_name("South Korea") == "south_korea.png"

    def test_single_word(self):
        assert make_file_name("France") == "france.png"

    def test_usa(self):
        assert make_file_name("USA") == "usa.png"

    def test_multiple_spaces(self):
        assert make_file_name("Trinidad and Tobago") == "trinidad_and_tobago.png"


class TestDownloadFlag:
    @patch("extract.get_shield.requests.get")
    def test_successful_download(self, mock_get, tmp_path):
        mock_response = MagicMock()
        mock_response.content = b"\x89PNG fake image data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        output = str(tmp_path / "flag.png")
        result = download_flag("https://example.com/flag.png", output)

        assert result == output
        assert os.path.exists(output)
        with open(output, "rb") as f:
            assert f.read() == b"\x89PNG fake image data"

    @patch("extract.get_shield.requests.get")
    def test_http_error(self, mock_get, tmp_path):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("403 Forbidden")
        mock_get.return_value = mock_response

        output = str(tmp_path / "flag.png")
        with pytest.raises(Exception, match="403 Forbidden"):
            download_flag("https://example.com/flag.png", output)

    @patch("extract.get_shield.requests.get")
    def test_passes_user_agent(self, mock_get, tmp_path):
        mock_response = MagicMock()
        mock_response.content = b"data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        output = str(tmp_path / "flag.png")
        download_flag("https://example.com/flag.png", output, timeout=10)

        call_kwargs = mock_get.call_args
        assert call_kwargs.kwargs["headers"]["User-Agent"] == "Mozilla/5.0"
        assert call_kwargs.kwargs["timeout"] == 10


class TestDownloadAllShields:
    @patch("extract.get_shield.download_flag")
    @patch("extract.get_shield.time.sleep")
    def test_successful_download_all(self, mock_sleep, mock_download, tmp_path):
        mock_download.return_value = "fake_path.png"
        test_teams = {"Brazil": "br", "Argentina": "ar"}
        output_dir = str(tmp_path / "shields")

        result = download_all_shields(test_teams, output_dir=output_dir, delay=0)

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "team" in result.columns
        assert "image_path" in result.columns
        assert set(result["team"]) == {"Brazil", "Argentina"}

    @patch("extract.get_shield.download_flag")
    @patch("extract.get_shield.time.sleep")
    def test_partial_failure(self, mock_sleep, mock_download, tmp_path):
        def side_effect(url, path, **kwargs):
            if "ar" in url:
                raise Exception("Network error")
            return path

        mock_download.side_effect = side_effect
        test_teams = {"Brazil": "br", "Argentina": "ar"}
        output_dir = str(tmp_path / "shields")

        result = download_all_shields(test_teams, output_dir=output_dir, delay=0)

        assert len(result) == 1
        assert result.iloc[0]["team"] == "Brazil"

    @patch("extract.get_shield.download_flag")
    @patch("extract.get_shield.time.sleep")
    def test_creates_output_directory(self, mock_sleep, mock_download, tmp_path):
        mock_download.return_value = "fake_path.png"
        output_dir = str(tmp_path / "new_dir" / "shields")

        download_all_shields({"Brazil": "br"}, output_dir=output_dir, delay=0)

        assert os.path.isdir(output_dir)

    @patch("extract.get_shield.download_flag")
    @patch("extract.get_shield.time.sleep")
    def test_empty_teams(self, mock_sleep, mock_download, tmp_path):
        result = download_all_shields({}, output_dir=str(tmp_path / "shields"), delay=0)
        assert len(result) == 0
        assert isinstance(result, pd.DataFrame)


class TestTeamsDict:
    def test_has_expected_count(self):
        assert len(teams) == 29

    def test_expected_teams_present(self):
        expected = ["Argentina", "Brazil", "France", "Germany", "Spain",
                    "England", "Italy", "Netherlands", "Portugal", "Japan"]
        for team in expected:
            assert team in teams

    def test_all_codes_are_strings(self):
        for team, code in teams.items():
            assert isinstance(code, str), f"{team} has non-string code"

    def test_no_empty_codes(self):
        for team, code in teams.items():
            assert len(code) > 0, f"{team} has empty code"
