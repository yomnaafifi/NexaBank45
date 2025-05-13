from abc import ABC, abstractmethod
import pandas as pd
from utils.logger import logger
class BaseExtractor(ABC):
    def __init__(self, file: str):
        """
        Constructor to initialize the BaseExtractor with a file attribute.

        Args:
            file (str): The file path or name associated with the extractor.
        """
        self.file = file
    @logger
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        """
        Abstract method to extract data from a source to be implemented by subclasses.
        
        Returns:
            pd.DataFrame: Extracted data as a pandas DataFrame.
        """
        pass


class CSVExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)
        
    @logger
    def extract(self) -> pd.DataFrame:
        """
        Extract data from a CSV file using pandas.
        """
        return pd.read_csv(self.file) 


class JSONExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)

    @logger
    def extract(self) -> pd.DataFrame:
        """
        Extract data from a JSON file using pandas.
        """
        return pd.read_json(self.file)
    

class TextExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)

    @logger
    def extract(self) -> pd.DataFrame:
        """
        Extract data from a plain text file using pandas.
        """
        return pd.read_csv(self.file, sep='|')