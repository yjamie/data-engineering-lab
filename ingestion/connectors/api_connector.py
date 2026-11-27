import logging
import requests

from ingestion.connectors.base_connector import BaseConnector

logger = logging.getLogger(__name__)

class APIConnector(BaseConnector):
    """Handles connection management, disconnection, and get requests"""

    def __init__(self, base_url:str, api_key:str=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None

    def connect(self) -> None:
        """Establishes connection to API"""
        if self.is_connected():
            return

        logger.info("Starting API connection: %s", self.base_url)
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}"
            })

    def disconnect(self) -> None:
        """Disconnects API connection"""
        if self.session is not None:
            logger.info("Ending API connection: %s", self.base_url)
            self.session.close()
            self.session = None

    def is_connected(self) -> bool:
        """Checks if connection is active"""
        return self.session is not None

    def get(self, endpoint:str, params:dict=None, timeout:int=30) -> requests.Response:
        """Sends get request and returns response"""
        if not self.is_connected():
            raise RuntimeError("API connector is not connected")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            logger.info("Starting GET request: %s", url)

            response = self.session.get(
                url = url,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()

            return response

        except requests.exceptions.HTTPError:
            logger.exception("GET request failed with HTTP error: %s", url)
            raise
        except requests.exceptions.Timeout:
            logger.exception("GET request timed out: %s", url)
            raise
        except requests.RequestException:
            logger.exception("GET request failed: %s", url)
            raise