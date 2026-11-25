import pandas as pd
import pytest
import requests

from unittest.mock import MagicMock, patch
from ingestion.connectors.api_connector import APIConnector

@pytest.fixture
def mock_response():
    """Create a fake API repsonse"""
    response = MagicMock()
    response.json.return_value = [
        {"id": 1, "name":"Peter Parker"},
        {"id": 2, "name":"Bruce Wayne"}
    ]
    return response


def setup_mock_response(mock_get, mock_response):
    """Replace requests.get function used inside API connector with mock"""
    mock_get.return_value = mock_response


@patch("ingestion.connectors.api_connector.requests.get")
def test_successful_extraction(mock_get, mock_response):
    """Test successful API extraction"""
    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api")
    df = connector.extract()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["id", "name"]
    assert df.iloc[0]["name"] == "Peter Parker"

    mock_get.assert_called_once()


@patch("ingestion.connectors.api_connector.requests.get")
def test_empty_response(mock_get):
    """Tests API returning empty dataset"""
    mock_response = MagicMock()
    mock_response.json.return_value = []

    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api")
    df = connector.extract()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0


@patch("ingestion.connectors.api_connector.requests.get")
def test_http_error(mock_get):
    """Tests HTTP error"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()

    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api")

    with pytest.raises(requests.HTTPError):
        connector.extract()


@patch("ingestion.connectors.api_connector.requests.get")
def test_timeout_error(mock_get):
    """Tests timeout error"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.Timeout()

    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api")

    with pytest.raises(requests.Timeout):
        connector.extract()


@patch("ingestion.connectors.api_connector.requests.get")
def test_custom_timeout(mock_get, mock_response):
    """Tests custom timeout"""
    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api", timeout=60)
    connector.extract()

    assert mock_get.call_args.kwargs["timeout"] == 60
    mock_get.assert_called_once_with(
        url="http://jamieisthebest.com/api", headers=None, timeout=60
    )


@patch("ingestion.connectors.api_connector.requests.get")
def test_invalid_response(mock_get):
    """Tests invalid response"""
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError()

    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api")

    with pytest.raises(ValueError):
        connector.extract()


@patch("ingestion.connectors.api_connector.requests.get")
def test_custom_headers(mock_get, mock_response):
    """Tests custom headers"""
    headers = {
        "Authorization": "test-token"
    }

    setup_mock_response(mock_get, mock_response)

    connector = APIConnector(url="http://jamieisthebest.com/api", headers=headers, timeout=30)
    connector.extract()

    assert mock_get.call_args.kwargs["headers"] == headers
    mock_get.assert_called_once_with(
        url="http://jamieisthebest.com/api", headers=headers, timeout=30
    )