import logging
import pandas as pd
import pandas.errors

from ingestion.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class CSVConnector(BaseConnector):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pd.DataFrame:
        """Extract CSV data and return as DataFrame"""
        try:
            logger.info("Starting CSV extraction: %s", self.file_path)
            df = pd.read_csv(self.file_path)

            if len(df) == 0:
                logger.warning("CSV returned empty dataset: %s", self.file_path)
            else:
                logger.info("CSV extraction completed: %d records retrieved", len(df))

            return df
        except FileNotFoundError:
            logger.exception("CSV file not found: %s", self.file_path)
            raise
        except pandas.errors.ParserError:
            logger.exception("Failed to parse CSV file: %s", self.file_path)
            raise
        except Exception:
            logger.exception("Unexpected CSV extraction error")
            raise
