import logging
import pandas as pd

from ingestion.connectors.api_connector import APIConnector
from ingestion.extractors.base_extractor import BaseExtractor

logger = logging.getLogger(__name__)

class APIExtractor(BaseExtractor):
    """Handles data extraction from API source"""

    def __init__(self, connector: APIConnector):
        self.connector = connector

    def extract(self, endpoint:str, params:dict = None) -> pd.DataFrame:
        """Extracts API response data and return as a DataFrame"""
        logger.info("Starting API extraction: %s", endpoint)
        response = self.connector.get(endpoint, params)

        try:
            data = response.json()
            df = pd.DataFrame(data)

            if df.empty:
                logger.warning("API returned empty dataset: %s", endpoint)
            else:
                logger.info("API extraction successful: %d records retrieved", len(df))

            return df

        except ValueError:
            logger.exception("Failed to parse API response into JSON: %s", endpoint)
            raise