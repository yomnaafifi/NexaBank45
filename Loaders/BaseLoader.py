from abc import ABC, abstractmethod
import pandas as pd

class BaseLoader(ABC):
    def __init__(self, data: pd.DataFrame):
        """
        Constructor to initialize the BaseLoader with a data attribute.

        Args:
            data (pandas.DataFrame): The data to be loaded, represented as a pandas DataFrame.
        """
        self.data = data

    @abstractmethod
    def load(self) -> bool:
        """
        Abstract method to load the data to be implemented by subclasses.

        Returns:
            bool: True if the data is successfully loaded, False otherwise.
        """
        pass
