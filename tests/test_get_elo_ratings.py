import os
import tempfile

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from extract.get_elo_ratings import (
    download_elo_file,
    extract_elo_columns,
    get_elo_ratings,
    parse_elo_tsv,
)


@pytest.fixture
def sample_tsv_content():
    return (
        b"1\tBR\tBrazil\t2150\t100\n"
        b"2\tAR\tArgentina\t2100\t95\n"
        b"3\tFR\tFrance\t2050\t90\n"
    )


@pytest.fixture
def sample_tsv_file(sample_tsv_content, tmp_path):
    path = tmp_path / "test_elo.tsv"
    path.write_bytes(sample_tsv_content)
    return str(path)


@pytest.fixture
def sample_raw_df():
    return pd.DataFrame({
        0: [1, 2, 3],
        1: ["BR", "AR", "FR"],
        2: ["Brazil", "Argentina", "France"],
        3: [2150, 2100, 2050],
        4: [100, 95, 90]
    })


class TestDownloadEloFile:
    @patch("extract.get_elo_ratings.requests.get")
    def test_successful_download(self, mock_get, tmp_path):
        mock_response = MagicMock()
        mock_response.content = b"fake tsv data"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        output = str(tmp_path / "output.tsv")
        result = download_elo_file("https://example.com/data.tsv", output)

        assert result == output
        assert os.path.exists(output)
        with open(output, "rb") as f:
            assert f.read() == b"fake tsv data"
        mock_response.raise_for_status.assert_called_once()

    @patch("extract.get_elo_ratings.requests.get")
    def test_http_error_raises(self, mock_get, tmp_path):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        output = str(tmp_path / "output.tsv")
        with pytest.raises(Exception, match="404 Not Found"):
            download_elo_file("https://example.com/data.tsv", output)


class TestParseEloTsv:
    def test_parses_tsv_correctly(self, sample_tsv_file):
        df = parse_elo_tsv(sample_tsv_file)
        assert len(df) == 3
        assert df.iloc[0][0] == 1
        assert df.iloc[0][2] == "Brazil"

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            parse_elo_tsv("/nonexistent/path.tsv")


class TestExtractEloColumns:
    def test_extracts_correct_columns(self, sample_raw_df):
        result = extract_elo_columns(sample_raw_df)
        assert list(result.columns) == ["rank", "country_code", "elo_rating"]
        assert len(result) == 3

    def test_rank_values(self, sample_raw_df):
        result = extract_elo_columns(sample_raw_df)
        assert list(result["rank"]) == [1, 2, 3]

    def test_country_codes(self, sample_raw_df):
        result = extract_elo_columns(sample_raw_df)
        assert list(result["country_code"]) == ["Brazil", "Argentina", "France"]

    def test_elo_ratings(self, sample_raw_df):
        result = extract_elo_columns(sample_raw_df)
        assert list(result["elo_rating"]) == [2150, 2100, 2050]

    def test_single_row(self):
        df = pd.DataFrame({0: [1], 1: ["X"], 2: ["Team"], 3: [1500], 4: [50]})
        result = extract_elo_columns(df)
        assert len(result) == 1
        assert result.iloc[0]["elo_rating"] == 1500


class TestGetEloRatings:
    @patch("extract.get_elo_ratings.download_elo_file")
    @patch("extract.get_elo_ratings.parse_elo_tsv")
    def test_end_to_end(self, mock_parse, mock_download, sample_raw_df, tmp_path):
        mock_download.return_value = str(tmp_path / "elo.tsv")
        mock_parse.return_value = sample_raw_df

        csv_path = str(tmp_path / "output.csv")
        result = get_elo_ratings(
            "https://example.com",
            tsv_path=str(tmp_path / "elo.tsv"),
            csv_path=csv_path
        )

        assert len(result) == 3
        assert list(result.columns) == ["rank", "country_code", "elo_rating"]
        assert os.path.exists(csv_path)

        saved = pd.read_csv(csv_path)
        assert len(saved) == 3
