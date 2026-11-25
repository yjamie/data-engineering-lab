from abc import ABC, abstractmethod
import pandas as pd

class BaseConnector(ABC):
    """Abstract interface for all data source connectors"""

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """Extract source data and return as a DataFrame"""
        pass