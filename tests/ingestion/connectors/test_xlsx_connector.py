import pandas as pd
import pytest

from unittest.mock import patch

from pandas.errors import NullFrequencyError

from ingestion.connectors.xlsx_connector import XLSXConnector


@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_successful_extraction(mock_read_excel):
    """Tests successful XLSX extraction"""
    expected_df = pd.DataFrame({
        "name": ["Bruce Wayne", "Peter Parker"],
        "occupation": ["Batman", "Spiderman"]
    })

    mock_read_excel.return_value = expected_df

    connector = XLSXConnector("superheroes.xlsx")
    result = connector.extract()

    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_excel.assert_called_once_with("superheroes.xlsx")


@patch("ingestion.connectors.xlsx_connector.logger.warning")
@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_empty_dataset(mock_read_excel, mock_warning):
    """Tests empty dataset"""
    expected_df = pd.DataFrame()

    mock_read_excel.return_value = expected_df

    connector = XLSXConnector("superheroes.xlsx")
    result = connector.extract()

    assert len(result) == 0
    assert result.empty
    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_excel.assert_called_once_with("superheroes.xlsx")
    mock_warning.assert_called_once_with(
        "XLSX returned empty dataset: %s",
        "superheroes.xlsx"
    )


@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_file_not_found(mock_read_excel):
    """Tests FileNotFoundError handling"""
    mock_read_excel.side_effect = FileNotFoundError

    connector = XLSXConnector("superheroes.xlsx")

    with pytest.raises(FileNotFoundError):
        connector.extract()


@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_parser_error(mock_read_excel):
    """Tests pandas ParserError handling"""
    mock_read_excel.side_effect = pd.errors.ParserError

    connector = XLSXConnector("superheroes.xlsx")

    with pytest.raises(pd.errors.ParserError):
        connector.extract()


@patch("ingestion.connectors.xlsx_connector.logger.exception")
@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_unexpected_error(mock_read_excel, mock_exception):
    """Tests handling of unexpected Exceptions"""
    mock_read_excel.side_effect = NullFrequencyError

    connector = XLSXConnector("superheroes.xlsx")

    with pytest.raises(NullFrequencyError):
        connector.extract()

    mock_exception.assert_called_once_with(
        "Unexpected XLSX extraction error"
    )


@patch("ingestion.connectors.xlsx_connector.logger.info")
@patch("ingestion.connectors.xlsx_connector.pd.read_excel")
def test_logs_record_count(mock_read_excel, mock_info):
    """Test the record count in logs"""
    mock_read_excel.return_value = pd.DataFrame({"name": ["Robin", "Starfire", "Cyborg", "Beast Boy", "Raven"]})

    connector = XLSXConnector("superheroes.xlsx")
    result = connector.extract()

    assert len(result) == 5
    mock_info.assert_any_call(
        "XLSX extraction completed: %d records retrieved",
        len(result)
    )
