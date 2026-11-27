from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    """Abstract class for all data source extractors"""

    @abstractmethod
    def extract(self, **kwargs) -> pd.DataFrame:
        """Extract source data and return as a DataFrame"""
        pass