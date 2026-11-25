from abc import ABC, abstractmethod
import pandas as pd

class BaseConnector(ABC):

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        pass