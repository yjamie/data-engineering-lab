import logging
import pandas as pd
import requests

from ingestion.connectors.base import BaseConnector

logger = logging.getLogger(__name__)

class APIConnector(BaseConnector):

    def __init__(self, url: str, headers=None, timeout: int = 30):
        self.url = url
        self.timeout = timeout
        self.headers = headers

    def extract(self) -> pd.DataFrame:
        """Extracts API response data and return as a DataFrame"""
        try:
            logger.info("Starting API extraction: %s", self.url)

            response = requests.get(
                url=self.url,
                headers=self.headers,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            response.close()

            if df.empty:
                logger.warning("API returned empty dataset: %s", self.url)
            else:
                logger.info("API extraction successful: %d records retrieved", len(df))

            return df

        except requests.RequestException:
            logger.exception("API extraction failed: %s", self.url)
            raise
        except ValueError:
            logger.exception("Failed to parse API response into JSON")
            raise