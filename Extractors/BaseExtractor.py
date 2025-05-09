from abc import ABC, abstractmethod
import pandas as pd

class BaseExtractor(ABC):
    def __init__(self, file: str):
        """
        Constructor to initialize the BaseExtractor with a file attribute.

        Args:
            file (str): The file path or name associated with the extractor.
        """
        self.file = file

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Abstract method to extract data from a source to be implemented by subclasses.
        
        Returns:
            pd.DataFrame: Extracted data as a pandas DataFrame.
        """
        pass

