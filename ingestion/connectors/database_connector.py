from ingestion.connectors.base import BaseConnector
import pandas as pd

class DatabaseConnector(BaseConnector):

    def __init__(self):
        pass

    def extract(self) -> pd.DataFrame:
        pass