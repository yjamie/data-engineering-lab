from ingestion.connectors.base import BaseConnector
import pandas as pd
import requests
import io


class APIConnector(BaseConnector):

    def __init__(self, url: str, headers=None):
        self.url = url
        self.headers = headers

    def extract(self) -> pd.DataFrame:
        df = pd.DataFrame()
        return df
