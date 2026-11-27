import logging
import pandas as pd
import pandas.errors

from ingestion.extractors.base_extractor import BaseExtractor

logger = logging.getLogger(__name__)

class XLSXExtractor(BaseExtractor):
    """Handles data extraction from Excel source"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pd.DataFrame:
        """Extract XLSX data and return as DataFrame"""
        try:
            logger.info("Starting XLSX extraction: %s", self.file_path)
            df = pd.read_excel(self.file_path)

            if len(df) == 0:
                logger.warning("XLSX returned empty dataset: %s", self.file_path)
            else:
                logger.info("XLSX extraction completed: %d records retrieved", len(df))

            return df
        except FileNotFoundError:
            logger.exception("XLSX file not found: %s", self.file_path)
            raise
        except pandas.errors.ParserError:
            logger.exception("Failed to parse XLSX file: %s", self.file_path)
            raise
        except Exception:
            logger.exception("Unexpected XLSX extraction error")
            raise
