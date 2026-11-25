from ingestion.connectors.base import BaseConnector
import pandas as pd

class CSVConnector(BaseConnector):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract(self) -> pd.DataFrame:
        df = pd.DataFrame()
        return df
