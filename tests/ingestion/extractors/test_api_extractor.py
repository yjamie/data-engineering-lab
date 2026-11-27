import pandas as pd
import pytest

from unittest.mock import MagicMock, patch
from ingestion.extractors.api_extractor import APIExtractor

@pytest.fixture
def mock_connector():
    return MagicMock()

@pytest.fixture
def mock_response():
    """Create a fake API response"""
    response = MagicMock()
    response.json.return_value = [
        {"id": 1, "name":"Peter Parker"},
        {"id": 2, "name":"Bruce Wayne"}
    ]
    return response


def test_successful_extraction(mock_connector, mock_response):
    """Test successful API extraction"""
    mock_connector.get.return_value = mock_response

    extractor = APIExtractor(mock_connector)
    df = extractor.extract(endpoint="/api")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]
    assert df.iloc[0]["name"] == "Peter Parker"
    mock_connector.get.assert_called_once_with("/api", None)


@patch("ingestion.extractors.api_extractor.logger.warning")
def test_empty_response(mock_warning, mock_connector):
    """Tests API returning empty dataset"""
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_connector.get.return_value = mock_response

    extractor = APIExtractor(mock_connector)
    df = extractor.extract(endpoint="/api")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    mock_warning.assert_called_once_with(
        "API returned empty dataset: %s",
        "/api"
    )


def test_invalid_response(mock_connector):
    """Tests invalid response"""
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError()
    mock_connector.get.return_value = mock_response

    extractor = APIExtractor(mock_connector)

    with pytest.raises(ValueError):
        extractor.extract(endpoint="/api")