import pandas as pd
import pytest

from unittest.mock import patch

from pandas.errors import NullFrequencyError

from ingestion.extractors.xlsx_extractor import XLSXExtractor


@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_successful_extraction(mock_read_excel):
    """Tests successful XLSX extraction"""
    expected_df = pd.DataFrame({
        "name": ["Bruce Wayne", "Peter Parker"],
        "occupation": ["Batman", "Spiderman"]
    })

    mock_read_excel.return_value = expected_df

    extractor = XLSXExtractor("superheroes.xlsx")
    result = extractor.extract()

    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_excel.assert_called_once_with("superheroes.xlsx")


@patch("ingestion.extractors.xlsx_extractor.logger.warning")
@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_empty_dataset(mock_read_excel, mock_warning):
    """Tests empty dataset"""
    expected_df = pd.DataFrame()

    mock_read_excel.return_value = expected_df

    extractor = XLSXExtractor("superheroes.xlsx")
    result = extractor.extract()

    assert len(result) == 0
    assert result.empty
    pd.testing.assert_frame_equal(result, expected_df)
    mock_read_excel.assert_called_once_with("superheroes.xlsx")
    mock_warning.assert_called_once_with(
        "XLSX returned empty dataset: %s",
        "superheroes.xlsx"
    )


@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_file_not_found(mock_read_excel):
    """Tests FileNotFoundError handling"""
    mock_read_excel.side_effect = FileNotFoundError

    extractor = XLSXExtractor("superheroes.xlsx")

    with pytest.raises(FileNotFoundError):
        extractor.extract()


@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_parser_error(mock_read_excel):
    """Tests pandas ParserError handling"""
    mock_read_excel.side_effect = pd.errors.ParserError

    extractor = XLSXExtractor("superheroes.xlsx")

    with pytest.raises(pd.errors.ParserError):
        extractor.extract()


@patch("ingestion.extractors.xlsx_extractor.logger.exception")
@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_unexpected_error(mock_read_excel, mock_exception):
    """Tests handling of unexpected Exceptions"""
    mock_read_excel.side_effect = NullFrequencyError

    extractor = XLSXExtractor("superheroes.xlsx")

    with pytest.raises(NullFrequencyError):
        extractor.extract()

    mock_exception.assert_called_once_with(
        "Unexpected XLSX extraction error"
    )


@patch("ingestion.extractors.xlsx_extractor.logger.info")
@patch("ingestion.extractors.xlsx_extractor.pd.read_excel")
def test_logs_record_count(mock_read_excel, mock_info):
    """Test the record count in logs"""
    mock_read_excel.return_value = pd.DataFrame({"name": ["Robin", "Starfire", "Cyborg", "Beast Boy", "Raven"]})

    extractor = XLSXExtractor("superheroes.xlsx")
    result = extractor.extract()

    assert len(result) == 5
    mock_info.assert_any_call(
        "XLSX extraction completed: %d records retrieved",
        len(result)
    )
