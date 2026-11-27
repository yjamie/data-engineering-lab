from abc import ABC, abstractmethod


class BaseConnector(ABC):
    """Abstract class for all connectors"""

    @abstractmethod
    def connect(self) -> None:
        """Establishes connection to source"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects connection to source"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Checks connection status"""
        pass
