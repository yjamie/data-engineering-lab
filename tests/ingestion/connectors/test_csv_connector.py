import pandas as pd
import pytest

from unittest.mock import patch

from pandas.errors import NullFrequencyError

from ingestion.connectors.csv_connector import CSVConnector


@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_successful_extraction(mock_read_csv):
    """Tests successful CSV extraction"""
    expected_df = pd.DataFrame({
        "name": ["Bruce Wayne", "Peter Parker"],
        "occupation": ["Batman", "Spiderman"]
    })

    mock_read_csv.return_value = expected_df

    connector = CSVConnector("superheroes.csv")
    result = connector.extract()

    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_csv.assert_called_once_with("superheroes.csv")


@patch("ingestion.connectors.csv_connector.logger.warning")
@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_empty_dataset(mock_read_csv, mock_warning):
    """Tests empty dataset"""
    expected_df = pd.DataFrame()

    mock_read_csv.return_value = expected_df

    connector = CSVConnector("superheroes.csv")
    result = connector.extract()

    assert len(result) == 0
    assert result.empty
    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_csv.assert_called_once_with("superheroes.csv")
    mock_warning.assert_called_once_with(
        "CSV returned empty dataset: %s",
        "superheroes.csv"
    )


@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_file_not_found(mock_read_csv):
    """Tests FileNotFoundError handling"""
    mock_read_csv.side_effect = FileNotFoundError

    connector = CSVConnector("superheroes.csv")

    with pytest.raises(FileNotFoundError):
        connector.extract()


@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_parser_error(mock_read_csv):
    """Tests pandas ParserError handling"""
    mock_read_csv.side_effect = pd.errors.ParserError

    connector = CSVConnector("superheroes.csv")

    with pytest.raises(pd.errors.ParserError):
        connector.extract()


@patch("ingestion.connectors.csv_connector.logger.exception")
@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_unexpected_error(mock_read_csv, mock_exception):
    """Tests handling of unexpected Exceptions"""
    mock_read_csv.side_effect = NullFrequencyError

    connector = CSVConnector("superheroes.csv")

    with pytest.raises(NullFrequencyError):
        connector.extract()

    mock_exception.assert_called_once_with(
        "Unexpected CSV extraction error"
    )


@patch("ingestion.connectors.csv_connector.logger.info")
@patch("ingestion.connectors.csv_connector.pd.read_csv")
def test_logs_record_count(mock_read_csv, mock_info):
    """Test the record count in logs"""
    mock_read_csv.return_value = pd.DataFrame({"name": ["Robin", "Starfire", "Cyborg", "Beast Boy", "Raven"]})

    connector = CSVConnector("superheroes.csv")
    result = connector.extract()

    assert len(result) == 5
    mock_info.assert_any_call(
        "CSV extraction completed: %d records retrieved",
        len(result)
    )
