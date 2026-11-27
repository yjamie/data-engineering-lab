import pytest
import requests

from unittest.mock import MagicMock, patch
from ingestion.connectors.api_connector import APIConnector

@pytest.fixture
def mock_response():
    """Create a fake API response"""
    response = MagicMock()
    response.json.return_value = [
        {"id": 1, "name":"Peter Parker"},
        {"id": 2, "name":"Bruce Wayne"}
    ]
    return response


def setup_mock_response(mock_get, mock_response):
    """Replace requests.get function used inside API connector with mock"""
    mock_get.return_value = mock_response


@patch("ingestion.connectors.api_connector.requests.Session")
def test_connection(mock_session):
    connector = APIConnector(base_url="http://jamieisthebest.com/api", api_key="test-api-key")
    connector.connect()

    mock_session.assert_called_once()
    assert connector.session == mock_session.return_value


@patch("ingestion.connectors.api_connector.requests.Session")
def test_connection_sets_accept_header(mock_session):
    connector = APIConnector(base_url="http://jamieisthebest.com/api", api_key=None)
    connector.connect()
    session = mock_session.return_value

    session.headers.update.assert_any_call({
        "Accept": "application/json"
    })


@patch("ingestion.connectors.api_connector.requests.Session")
def test_connection_set_auth_header(mock_session):
    connector = APIConnector(base_url="http://jamieisthebest.com/api", api_key="test-api-key")
    connector.connect()
    session = mock_session.return_value

    session.headers.update.assert_any_call({
        "Authorization": "Bearer test-api-key"
    })
    assert session.headers.update.call_count == 2


@patch("ingestion.connectors.api_connector.requests.Session")
def test_disconnection(mock_session):
    connector = APIConnector(base_url="http://jamieisthebest.com/api", api_key="test-api-key")
    connector.connect()
    connector.disconnect()
    session = mock_session.return_value

    session.close.assert_called_once()
    assert connector.session is None


@patch("ingestion.connectors.api_connector.requests.Session")
def test_connect_when_already_connected(mock_session):
    connector = APIConnector(base_url="http://jamieisthebest.com/api", api_key="test-api-key")
    connector.connect()
    original_session = connector.session
    connector.connect()

    mock_session.assert_called_once()
    assert connector.session is original_session


@patch("ingestion.connectors.api_connector.requests.Session")
def test_successful_get(mock_session):
    """Test successful API get request"""
    mock_response = MagicMock()
    mock_session.return_value.get.return_value = mock_response

    connector = APIConnector(base_url="http://jamieisthebest.com/")
    connector.connect()
    response = connector.get(endpoint="/api")

    assert response == mock_response
    mock_response.raise_for_status.assert_called_once()
    mock_session.return_value.get.assert_called_once_with(
        url="http://jamieisthebest.com/api",
        params=None,
        timeout=30
    )


@patch("ingestion.connectors.api_connector.requests.Session")
def test_http_error(mock_session):
    """Tests HTTP error"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError()
    mock_session.return_value.get.return_value = mock_response

    connector = APIConnector(base_url="http://jamieisthebest.com/")
    connector.connect()

    with pytest.raises(requests.HTTPError):
        connector.get(endpoint="api")
    mock_response.raise_for_status.assert_called_once()


@patch("ingestion.connectors.api_connector.requests.Session")
def test_timeout_error(mock_session):
    """Tests Timeout error"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.Timeout
    mock_session.return_value.get.return_value = mock_response

    connector = APIConnector(base_url="http://jamieisthebest.com/")
    connector.connect()

    with pytest.raises(requests.Timeout):
        connector.get(endpoint="api")
    mock_response.raise_for_status.assert_called_once()